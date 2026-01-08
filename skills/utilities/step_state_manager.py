"""
Step State Manager
Manages inter-step state persistence for the NCLEX pipeline.

Provides:
- State saving/loading between pipeline steps
- Retry context management
- Slide locking (prevent re-processing of passing slides)
- Iteration tracking

Usage:
    from skills.utilities.step_state_manager import StepStateManager

    manager = StepStateManager(output_dir="outputs/state")

    # Save state after step completion
    manager.save_state(step=7, state={'slides': [...], 'qa_score': 85})

    # Load state for next step
    state = manager.load_state(step=7)

    # Manage retry context
    manager.set_retry_context(step=8, failing_categories=['anchor_coverage'])
    context = manager.get_retry_context(step=8)

    # Lock passing slides
    manager.mark_slides_locked([1, 2, 5, 7])
    locked = manager.get_locked_slides()
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional, Set
from dataclasses import dataclass, field, asdict
import copy


@dataclass
class RetryContext:
    """Context information for pipeline retry operations."""
    iteration: int = 1
    max_iterations: int = 3
    failing_categories: List[str] = field(default_factory=list)
    locked_slides: Set[int] = field(default_factory=set)
    previous_scores: List[float] = field(default_factory=list)
    modifications_made: List[Dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to JSON-serializable dictionary."""
        return {
            'iteration': self.iteration,
            'max_iterations': self.max_iterations,
            'failing_categories': self.failing_categories,
            'locked_slides': list(self.locked_slides),
            'previous_scores': self.previous_scores,
            'modifications_made': self.modifications_made
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'RetryContext':
        """Create from dictionary."""
        return cls(
            iteration=data.get('iteration', 1),
            max_iterations=data.get('max_iterations', 3),
            failing_categories=data.get('failing_categories', []),
            locked_slides=set(data.get('locked_slides', [])),
            previous_scores=data.get('previous_scores', []),
            modifications_made=data.get('modifications_made', [])
        )


@dataclass
class StepState:
    """State snapshot for a pipeline step."""
    step_number: int
    timestamp: str
    status: str  # 'completed', 'failed', 'in_progress'
    data: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)
    retry_context: Optional[RetryContext] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to JSON-serializable dictionary."""
        return {
            'step_number': self.step_number,
            'timestamp': self.timestamp,
            'status': self.status,
            'data': self.data,
            'metadata': self.metadata,
            'retry_context': self.retry_context.to_dict() if self.retry_context else None
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'StepState':
        """Create from dictionary."""
        retry_ctx = data.get('retry_context')
        return cls(
            step_number=data.get('step_number', 0),
            timestamp=data.get('timestamp', ''),
            status=data.get('status', 'unknown'),
            data=data.get('data', {}),
            metadata=data.get('metadata', {}),
            retry_context=RetryContext.from_dict(retry_ctx) if retry_ctx else None
        )


class StepStateManager:
    """
    Manages state persistence between pipeline steps.

    Features:
    - Save/load state for each step
    - Track retry iterations
    - Lock slides that don't need re-processing
    - Maintain modification history
    """

    def __init__(self, output_dir: str = "outputs/state"):
        """
        Initialize the state manager.

        Args:
            output_dir: Directory to store state files
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # In-memory state cache
        self._states: Dict[int, StepState] = {}
        self._retry_contexts: Dict[int, RetryContext] = {}
        self._locked_slides: Set[int] = set()

        # Load existing states from disk
        self._load_existing_states()

    def _load_existing_states(self) -> None:
        """Load existing state files from disk."""
        for state_file in self.output_dir.glob("step_*_state.json"):
            try:
                with open(state_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    state = StepState.from_dict(data)
                    self._states[state.step_number] = state
                    if state.retry_context:
                        self._retry_contexts[state.step_number] = state.retry_context
            except Exception as e:
                print(f"Warning: Could not load state file {state_file}: {e}")

    def save_state(
        self,
        step: int,
        state: Dict[str, Any],
        status: str = 'completed',
        metadata: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Save state for a pipeline step.

        Args:
            step: Step number (1-12)
            state: State data to save
            status: Step status ('completed', 'failed', 'in_progress')
            metadata: Optional metadata (domain, section, etc.)

        Returns:
            Path to saved state file
        """
        timestamp = datetime.now().isoformat()

        step_state = StepState(
            step_number=step,
            timestamp=timestamp,
            status=status,
            data=state,
            metadata=metadata or {},
            retry_context=self._retry_contexts.get(step)
        )

        # Update cache
        self._states[step] = step_state

        # Save to disk
        filename = f"step_{step}_state.json"
        filepath = self.output_dir / filename

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(step_state.to_dict(), f, indent=2, default=str)

        return str(filepath)

    def load_state(self, step: int) -> Optional[Dict[str, Any]]:
        """
        Load state for a pipeline step.

        Args:
            step: Step number to load

        Returns:
            State data dictionary, or None if not found
        """
        # Check cache first
        if step in self._states:
            return self._states[step].data

        # Try loading from disk
        filepath = self.output_dir / f"step_{step}_state.json"
        if filepath.exists():
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    state = StepState.from_dict(data)
                    self._states[step] = state
                    return state.data
            except Exception as e:
                print(f"Warning: Could not load state for step {step}: {e}")

        return None

    def get_step_status(self, step: int) -> Optional[str]:
        """Get the status of a step."""
        if step in self._states:
            return self._states[step].status
        return None

    def set_retry_context(
        self,
        step: int,
        failing_categories: Optional[List[str]] = None,
        increment_iteration: bool = True
    ) -> RetryContext:
        """
        Set or update retry context for a step.

        Args:
            step: Step number
            failing_categories: Categories that failed validation
            increment_iteration: Whether to increment iteration count

        Returns:
            Updated RetryContext
        """
        if step not in self._retry_contexts:
            self._retry_contexts[step] = RetryContext()

        ctx = self._retry_contexts[step]

        if increment_iteration:
            ctx.iteration += 1

        if failing_categories is not None:
            ctx.failing_categories = failing_categories

        # Preserve locked slides
        ctx.locked_slides = self._locked_slides.copy()

        return ctx

    def get_retry_context(self, step: int) -> Optional[RetryContext]:
        """
        Get retry context for a step.

        Args:
            step: Step number

        Returns:
            RetryContext if exists, None otherwise
        """
        return self._retry_contexts.get(step)

    def mark_slides_locked(self, slide_numbers: List[int]) -> None:
        """
        Mark slides as locked (don't re-process on retry).

        Locked slides are those that passed validation and should
        not be modified in subsequent retry iterations.

        Args:
            slide_numbers: List of slide numbers to lock
        """
        self._locked_slides.update(slide_numbers)

        # Update all retry contexts
        for ctx in self._retry_contexts.values():
            ctx.locked_slides = self._locked_slides.copy()

    def unlock_slides(self, slide_numbers: Optional[List[int]] = None) -> None:
        """
        Unlock slides for re-processing.

        Args:
            slide_numbers: Slides to unlock. If None, unlocks all.
        """
        if slide_numbers is None:
            self._locked_slides.clear()
        else:
            self._locked_slides -= set(slide_numbers)

        # Update all retry contexts
        for ctx in self._retry_contexts.values():
            ctx.locked_slides = self._locked_slides.copy()

    def get_locked_slides(self) -> Set[int]:
        """Get set of locked slide numbers."""
        return self._locked_slides.copy()

    def is_slide_locked(self, slide_number: int) -> bool:
        """Check if a specific slide is locked."""
        return slide_number in self._locked_slides

    def record_modification(
        self,
        step: int,
        slide_number: int,
        modification_type: str,
        details: Dict[str, Any]
    ) -> None:
        """
        Record a modification made during retry.

        Args:
            step: Step number
            slide_number: Slide that was modified
            modification_type: Type of modification
            details: Modification details
        """
        if step not in self._retry_contexts:
            self._retry_contexts[step] = RetryContext()

        ctx = self._retry_contexts[step]
        ctx.modifications_made.append({
            'slide_number': slide_number,
            'type': modification_type,
            'details': details,
            'iteration': ctx.iteration,
            'timestamp': datetime.now().isoformat()
        })

    def record_score(self, step: int, score: float) -> None:
        """
        Record a QA score for tracking improvement across iterations.

        Args:
            step: Step number
            score: QA score (0-100)
        """
        if step not in self._retry_contexts:
            self._retry_contexts[step] = RetryContext()

        self._retry_contexts[step].previous_scores.append(score)

    def get_score_history(self, step: int) -> List[float]:
        """Get score history for a step."""
        if step in self._retry_contexts:
            return self._retry_contexts[step].previous_scores.copy()
        return []

    def should_retry(self, step: int) -> bool:
        """
        Determine if another retry iteration should be attempted.

        Returns False if:
        - Max iterations reached
        - Scores are not improving
        - No failing categories

        Args:
            step: Step number

        Returns:
            True if retry should be attempted
        """
        ctx = self._retry_contexts.get(step)
        if not ctx:
            return True  # No context = first try

        # Check max iterations
        if ctx.iteration >= ctx.max_iterations:
            return False

        # Check if there are failing categories
        if not ctx.failing_categories:
            return False

        # Check if scores are improving
        scores = ctx.previous_scores
        if len(scores) >= 2:
            # If last two scores didn't improve, don't retry
            if scores[-1] <= scores[-2]:
                return False

        return True

    def get_slides_to_process(
        self,
        all_slides: List[Dict[str, Any]],
        respect_locks: bool = True
    ) -> List[Dict[str, Any]]:
        """
        Get slides that need processing (excluding locked slides).

        Args:
            all_slides: Complete list of slides
            respect_locks: Whether to respect slide locks

        Returns:
            List of slides to process
        """
        if not respect_locks:
            return all_slides

        return [
            s for s in all_slides
            if s.get('slide_number') not in self._locked_slides
        ]

    def create_checkpoint(self, name: str) -> str:
        """
        Create a named checkpoint of current state.

        Args:
            name: Checkpoint name

        Returns:
            Path to checkpoint file
        """
        checkpoint = {
            'name': name,
            'timestamp': datetime.now().isoformat(),
            'states': {str(k): v.to_dict() for k, v in self._states.items()},
            'retry_contexts': {str(k): v.to_dict() for k, v in self._retry_contexts.items()},
            'locked_slides': list(self._locked_slides)
        }

        filename = f"checkpoint_{name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        filepath = self.output_dir / filename

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(checkpoint, f, indent=2, default=str)

        return str(filepath)

    def restore_checkpoint(self, filepath: str) -> bool:
        """
        Restore state from a checkpoint file.

        Args:
            filepath: Path to checkpoint file

        Returns:
            True if successful
        """
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                checkpoint = json.load(f)

            self._states = {
                int(k): StepState.from_dict(v)
                for k, v in checkpoint.get('states', {}).items()
            }
            self._retry_contexts = {
                int(k): RetryContext.from_dict(v)
                for k, v in checkpoint.get('retry_contexts', {}).items()
            }
            self._locked_slides = set(checkpoint.get('locked_slides', []))

            return True
        except Exception as e:
            print(f"Error restoring checkpoint: {e}")
            return False

    def clear_step(self, step: int) -> None:
        """Clear state for a specific step."""
        if step in self._states:
            del self._states[step]
        if step in self._retry_contexts:
            del self._retry_contexts[step]

        # Remove from disk
        filepath = self.output_dir / f"step_{step}_state.json"
        if filepath.exists():
            filepath.unlink()

    def clear_all(self) -> None:
        """Clear all state data."""
        self._states.clear()
        self._retry_contexts.clear()
        self._locked_slides.clear()

        # Remove all state files
        for f in self.output_dir.glob("step_*_state.json"):
            f.unlink()

    def get_pipeline_summary(self) -> Dict[str, Any]:
        """Get summary of pipeline state."""
        return {
            'total_steps_with_state': len(self._states),
            'completed_steps': [
                s for s, state in self._states.items()
                if state.status == 'completed'
            ],
            'failed_steps': [
                s for s, state in self._states.items()
                if state.status == 'failed'
            ],
            'in_progress_steps': [
                s for s, state in self._states.items()
                if state.status == 'in_progress'
            ],
            'steps_with_retries': [
                s for s, ctx in self._retry_contexts.items()
                if ctx.iteration > 1
            ],
            'locked_slide_count': len(self._locked_slides),
            'latest_timestamp': max(
                (state.timestamp for state in self._states.values()),
                default=None
            )
        }


if __name__ == "__main__":
    print("=" * 60)
    print("STEP STATE MANAGER - SELF TEST")
    print("=" * 60)

    # Create manager with test directory
    manager = StepStateManager(output_dir="outputs/state_test")

    # Test 1: Save and load state
    print("\n1. Testing save/load state:")
    test_state = {
        'slides': [{'slide_number': 1, 'header': 'Test'}],
        'qa_score': 85
    }
    filepath = manager.save_state(step=7, state=test_state, status='completed')
    print(f"   Saved to: {filepath}")

    loaded = manager.load_state(step=7)
    print(f"   Loaded: {loaded is not None}")
    print(f"   QA Score: {loaded.get('qa_score')}")

    # Test 2: Retry context
    print("\n2. Testing retry context:")
    ctx = manager.set_retry_context(step=8, failing_categories=['anchor_coverage'])
    print(f"   Iteration: {ctx.iteration}")
    print(f"   Failing categories: {ctx.failing_categories}")

    ctx = manager.set_retry_context(step=8, failing_categories=['char_limit'])
    print(f"   After increment - Iteration: {ctx.iteration}")

    # Test 3: Slide locking
    print("\n3. Testing slide locking:")
    manager.mark_slides_locked([1, 2, 5, 7])
    print(f"   Locked slides: {manager.get_locked_slides()}")
    print(f"   Is slide 3 locked? {manager.is_slide_locked(3)}")
    print(f"   Is slide 5 locked? {manager.is_slide_locked(5)}")

    # Test 4: Score tracking
    print("\n4. Testing score tracking:")
    manager.record_score(step=8, score=75)
    manager.record_score(step=8, score=82)
    manager.record_score(step=8, score=91)
    print(f"   Score history: {manager.get_score_history(step=8)}")

    # Test 5: Should retry logic
    print("\n5. Testing should_retry logic:")
    print(f"   Should retry step 8? {manager.should_retry(step=8)}")

    # Test 6: Pipeline summary
    print("\n6. Pipeline summary:")
    summary = manager.get_pipeline_summary()
    print(f"   {summary}")

    # Cleanup
    manager.clear_all()
    import shutil
    shutil.rmtree("outputs/state_test", ignore_errors=True)

    print("\n" + "=" * 60)
    print("SELF TEST COMPLETE")
    print("=" * 60)
