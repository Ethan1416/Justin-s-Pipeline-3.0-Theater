"""
Smart Retry Controller
Implements intelligent retry loops with context passing for the NCLEX pipeline.

Key Features:
- Context-aware retry with failing category targeting
- Slide locking to avoid re-processing passing slides
- Incremental scoring (only revalidate changed slides)
- Score trajectory tracking for early termination
- Configurable retry strategies per error type

Usage:
    from skills.utilities.smart_retry_controller import SmartRetryController

    controller = SmartRetryController(
        state_manager=StepStateManager(),
        error_recovery=ErrorRecovery()
    )

    # Execute with retry logic
    result = controller.execute_with_retry(
        step=8,
        execute_fn=run_quality_review,
        validate_fn=check_qa_score,
        context={'blueprint': blueprint}
    )
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional, Callable, Tuple, Set
from dataclasses import dataclass, field
from enum import Enum, auto
import copy


class RetryStrategy(Enum):
    """Retry strategies for different scenarios."""
    FULL_REPROCESS = auto()      # Reprocess all slides
    TARGETED_REPROCESS = auto()   # Only reprocess failing slides
    INCREMENTAL_FIX = auto()      # Apply minimal fixes
    ESCALATE = auto()             # Stop and escalate to user


class TerminationReason(Enum):
    """Reasons for terminating retry loop."""
    SUCCESS = auto()              # Score threshold met
    MAX_ITERATIONS = auto()       # Hit iteration limit
    NO_IMPROVEMENT = auto()       # Scores not improving
    CRITICAL_ERROR = auto()       # Unrecoverable error
    USER_ABORT = auto()           # User requested stop


@dataclass
class RetryIteration:
    """Data for a single retry iteration."""
    iteration: int
    score: float
    failing_categories: List[str]
    failing_slides: List[int]
    locked_slides: List[int]
    modifications: List[Dict[str, Any]]
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())

    def to_dict(self) -> Dict[str, Any]:
        return {
            'iteration': self.iteration,
            'score': self.score,
            'failing_categories': self.failing_categories,
            'failing_slides': self.failing_slides,
            'locked_slides': self.locked_slides,
            'modifications': self.modifications,
            'timestamp': self.timestamp
        }


@dataclass
class RetryContext:
    """Full context passed between retry iterations."""
    step: int
    target_score: float = 90.0
    max_iterations: int = 3
    current_iteration: int = 0
    iterations: List[RetryIteration] = field(default_factory=list)
    locked_slides: Set[int] = field(default_factory=set)
    failing_categories: List[str] = field(default_factory=list)
    strategy: RetryStrategy = RetryStrategy.TARGETED_REPROCESS
    category_weights: Dict[str, float] = field(default_factory=dict)

    def add_iteration(self, iteration: RetryIteration) -> None:
        """Add an iteration to history."""
        self.iterations.append(iteration)
        self.current_iteration = iteration.iteration

    def get_score_trajectory(self) -> List[float]:
        """Get list of scores across iterations."""
        return [it.score for it in self.iterations]

    def is_improving(self) -> bool:
        """Check if scores are improving."""
        scores = self.get_score_trajectory()
        if len(scores) < 2:
            return True
        return scores[-1] > scores[-2]

    def get_improvement_rate(self) -> float:
        """Calculate average improvement per iteration."""
        scores = self.get_score_trajectory()
        if len(scores) < 2:
            return 0.0
        improvements = [scores[i] - scores[i-1] for i in range(1, len(scores))]
        return sum(improvements) / len(improvements)

    def to_dict(self) -> Dict[str, Any]:
        return {
            'step': self.step,
            'target_score': self.target_score,
            'max_iterations': self.max_iterations,
            'current_iteration': self.current_iteration,
            'iterations': [it.to_dict() for it in self.iterations],
            'locked_slides': list(self.locked_slides),
            'failing_categories': self.failing_categories,
            'strategy': self.strategy.name,
            'category_weights': self.category_weights
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'RetryContext':
        ctx = cls(
            step=data.get('step', 0),
            target_score=data.get('target_score', 90.0),
            max_iterations=data.get('max_iterations', 3),
            current_iteration=data.get('current_iteration', 0),
            locked_slides=set(data.get('locked_slides', [])),
            failing_categories=data.get('failing_categories', []),
            strategy=RetryStrategy[data.get('strategy', 'TARGETED_REPROCESS')],
            category_weights=data.get('category_weights', {})
        )
        # Reconstruct iterations - simplified, not full objects
        return ctx


@dataclass
class RetryResult:
    """Result of retry operation."""
    success: bool
    final_score: float
    iterations_used: int
    termination_reason: TerminationReason
    final_blueprint: Optional[Dict[str, Any]] = None
    context: Optional[RetryContext] = None
    error_message: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            'success': self.success,
            'final_score': self.final_score,
            'iterations_used': self.iterations_used,
            'termination_reason': self.termination_reason.name,
            'error_message': self.error_message
        }


class SmartRetryController:
    """
    Orchestrates intelligent retry loops for pipeline steps.

    Features:
    - Targeted re-processing of failing slides only
    - Category-aware retry with weighted focus
    - Early termination when improvement plateaus
    - Full context preservation across iterations
    """

    # Default category weights for QA scoring
    DEFAULT_CATEGORY_WEIGHTS = {
        'anchor_coverage': 20,
        'char_limits': 15,
        'line_limits': 15,
        'nclex_tip': 10,
        'vignette_structure': 10,
        'answer_structure': 10,
        'markers': 10,
        'numbering': 5,
        'visual_quota': 5
    }

    # Retry strategies per category
    CATEGORY_STRATEGIES = {
        'anchor_coverage': RetryStrategy.FULL_REPROCESS,
        'char_limits': RetryStrategy.INCREMENTAL_FIX,
        'line_limits': RetryStrategy.INCREMENTAL_FIX,
        'nclex_tip': RetryStrategy.TARGETED_REPROCESS,
        'vignette_structure': RetryStrategy.TARGETED_REPROCESS,
        'answer_structure': RetryStrategy.TARGETED_REPROCESS,
        'markers': RetryStrategy.INCREMENTAL_FIX,
        'numbering': RetryStrategy.INCREMENTAL_FIX,
        'visual_quota': RetryStrategy.TARGETED_REPROCESS
    }

    def __init__(
        self,
        state_manager: Optional[Any] = None,
        error_recovery: Optional[Any] = None,
        output_dir: str = "outputs/retry_logs"
    ):
        """
        Initialize the retry controller.

        Args:
            state_manager: StepStateManager instance
            error_recovery: ErrorRecovery instance
            output_dir: Directory for retry logs
        """
        self.state_manager = state_manager
        self.error_recovery = error_recovery
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        self.category_weights = self.DEFAULT_CATEGORY_WEIGHTS.copy()
        self._active_contexts: Dict[int, RetryContext] = {}

    def execute_with_retry(
        self,
        step: int,
        execute_fn: Callable[[Dict[str, Any]], Dict[str, Any]],
        validate_fn: Callable[[Dict[str, Any]], Tuple[float, Dict[str, Any]]],
        initial_input: Dict[str, Any],
        target_score: float = 90.0,
        max_iterations: int = 3,
        on_iteration: Optional[Callable[[RetryIteration], None]] = None
    ) -> RetryResult:
        """
        Execute a step with smart retry logic.

        Args:
            step: Pipeline step number
            execute_fn: Function that processes input and returns output
            validate_fn: Function that validates output and returns (score, details)
            initial_input: Initial input for the step
            target_score: Target score to achieve (default 90)
            max_iterations: Maximum retry iterations (default 3)
            on_iteration: Optional callback after each iteration

        Returns:
            RetryResult with final outcome
        """
        # Initialize retry context
        context = RetryContext(
            step=step,
            target_score=target_score,
            max_iterations=max_iterations,
            category_weights=self.category_weights
        )
        self._active_contexts[step] = context

        current_input = copy.deepcopy(initial_input)
        current_output = None

        for iteration in range(1, max_iterations + 1):
            try:
                # Execute the step
                current_output = execute_fn(current_input)

                # Validate the output
                score, validation_details = validate_fn(current_output)

                # Extract failing categories and slides
                failing_categories = self._extract_failing_categories(
                    validation_details,
                    threshold=80.0
                )
                failing_slides = self._extract_failing_slides(validation_details)
                passing_slides = self._extract_passing_slides(
                    current_output,
                    failing_slides
                )

                # Lock passing slides
                context.locked_slides.update(passing_slides)

                # Record this iteration
                iteration_data = RetryIteration(
                    iteration=iteration,
                    score=score,
                    failing_categories=failing_categories,
                    failing_slides=failing_slides,
                    locked_slides=list(context.locked_slides),
                    modifications=self._get_modifications(current_output)
                )
                context.add_iteration(iteration_data)
                context.failing_categories = failing_categories

                # Callback if provided
                if on_iteration:
                    on_iteration(iteration_data)

                # Update state manager if available
                if self.state_manager:
                    self.state_manager.record_score(step, score)
                    self.state_manager.mark_slides_locked(list(passing_slides))

                # Check success
                if score >= target_score:
                    self._save_retry_log(context)
                    return RetryResult(
                        success=True,
                        final_score=score,
                        iterations_used=iteration,
                        termination_reason=TerminationReason.SUCCESS,
                        final_blueprint=current_output,
                        context=context
                    )

                # Check if we should continue
                should_continue, reason = self._should_continue_retry(context)
                if not should_continue:
                    self._save_retry_log(context)
                    return RetryResult(
                        success=False,
                        final_score=score,
                        iterations_used=iteration,
                        termination_reason=reason,
                        final_blueprint=current_output,
                        context=context
                    )

                # Prepare next iteration input
                current_input = self._prepare_retry_input(
                    current_output,
                    context,
                    validation_details
                )

            except Exception as e:
                self._save_retry_log(context)
                return RetryResult(
                    success=False,
                    final_score=context.iterations[-1].score if context.iterations else 0,
                    iterations_used=iteration,
                    termination_reason=TerminationReason.CRITICAL_ERROR,
                    error_message=str(e),
                    context=context
                )

        # Max iterations reached
        self._save_retry_log(context)
        return RetryResult(
            success=False,
            final_score=context.iterations[-1].score if context.iterations else 0,
            iterations_used=max_iterations,
            termination_reason=TerminationReason.MAX_ITERATIONS,
            final_blueprint=current_output,
            context=context
        )

    def _extract_failing_categories(
        self,
        validation_details: Dict[str, Any],
        threshold: float = 80.0
    ) -> List[str]:
        """Extract categories that are below threshold."""
        failing = []
        category_scores = validation_details.get('category_scores', {})

        for category, data in category_scores.items():
            if isinstance(data, dict):
                score = data.get('raw_score', data.get('score', 100))
            else:
                score = data

            if score < threshold:
                failing.append(category)

        return failing

    def _extract_failing_slides(
        self,
        validation_details: Dict[str, Any]
    ) -> List[int]:
        """Extract slide numbers that have issues."""
        failing = set()

        # From issues list
        for issue in validation_details.get('issues', []):
            if 'slide_number' in issue:
                failing.add(issue['slide_number'])
            elif 'slide' in issue:
                failing.add(issue['slide'])

        # From category details
        for category, data in validation_details.get('category_scores', {}).items():
            if isinstance(data, dict):
                for slide_num in data.get('failing_slides', []):
                    failing.add(slide_num)

        return list(failing)

    def _extract_passing_slides(
        self,
        output: Dict[str, Any],
        failing_slides: List[int]
    ) -> Set[int]:
        """Extract slides that passed validation."""
        all_slides = set()

        for slide in output.get('slides', []):
            slide_num = slide.get('slide_number')
            if slide_num is not None:
                all_slides.add(slide_num)

        return all_slides - set(failing_slides)

    def _get_modifications(
        self,
        output: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Extract modifications made in this iteration."""
        return output.get('modifications', output.get('changes', []))

    def _should_continue_retry(
        self,
        context: RetryContext
    ) -> Tuple[bool, TerminationReason]:
        """Determine if retry should continue."""
        # Check max iterations
        if context.current_iteration >= context.max_iterations:
            return False, TerminationReason.MAX_ITERATIONS

        # Check if improving
        if len(context.iterations) >= 2:
            if not context.is_improving():
                # Allow one more try if close to target
                last_score = context.iterations[-1].score
                if last_score < context.target_score - 10:
                    return False, TerminationReason.NO_IMPROVEMENT

        # Check improvement rate
        if len(context.iterations) >= 3:
            rate = context.get_improvement_rate()
            # If averaging less than 2 points improvement, stop
            if rate < 2.0:
                return False, TerminationReason.NO_IMPROVEMENT

        # No failing categories means we're done
        if not context.failing_categories:
            return False, TerminationReason.SUCCESS

        return True, TerminationReason.SUCCESS  # Continue

    def _prepare_retry_input(
        self,
        current_output: Dict[str, Any],
        context: RetryContext,
        validation_details: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Prepare input for next retry iteration.

        Key features:
        - Includes error context for targeted fixing
        - Marks locked slides to skip
        - Provides category-specific guidance
        """
        # Determine strategy based on failing categories
        strategy = self._determine_strategy(context.failing_categories)
        context.strategy = strategy

        retry_input = {
            'previous_output': current_output,
            'retry_context': {
                'iteration': context.current_iteration + 1,
                'failing_categories': context.failing_categories,
                'failing_slides': context.iterations[-1].failing_slides,
                'locked_slides': list(context.locked_slides),
                'strategy': strategy.name,
                'previous_scores': context.get_score_trajectory(),
                'target_score': context.target_score
            },
            'validation_details': validation_details,
            'category_guidance': self._get_category_guidance(context.failing_categories)
        }

        # Filter slides based on strategy
        if strategy == RetryStrategy.TARGETED_REPROCESS:
            retry_input['slides_to_process'] = [
                s for s in current_output.get('slides', [])
                if s.get('slide_number') not in context.locked_slides
            ]
        elif strategy == RetryStrategy.INCREMENTAL_FIX:
            # Only include slides with issues
            failing_nums = set(context.iterations[-1].failing_slides)
            retry_input['slides_to_fix'] = [
                s for s in current_output.get('slides', [])
                if s.get('slide_number') in failing_nums
            ]

        return retry_input

    def _determine_strategy(
        self,
        failing_categories: List[str]
    ) -> RetryStrategy:
        """Determine best retry strategy based on failing categories."""
        if not failing_categories:
            return RetryStrategy.TARGETED_REPROCESS

        # Check if any category requires full reprocess
        for category in failing_categories:
            if self.CATEGORY_STRATEGIES.get(category) == RetryStrategy.FULL_REPROCESS:
                return RetryStrategy.FULL_REPROCESS

        # Check if all can be fixed incrementally
        all_incremental = all(
            self.CATEGORY_STRATEGIES.get(cat) == RetryStrategy.INCREMENTAL_FIX
            for cat in failing_categories
        )
        if all_incremental:
            return RetryStrategy.INCREMENTAL_FIX

        return RetryStrategy.TARGETED_REPROCESS

    def _get_category_guidance(
        self,
        failing_categories: List[str]
    ) -> Dict[str, str]:
        """Get specific guidance for each failing category."""
        guidance = {}

        category_tips = {
            'anchor_coverage': "Ensure all assigned anchors appear in slide content. Check anchor_assignment for missing IDs.",
            'char_limits': "Apply body_char_enforcer to wrap lines at 66 characters. Check headers for 32 char limit.",
            'line_limits': "Apply body_line_enforcer to limit body to 8 lines. Consider splitting slides if needed.",
            'nclex_tip': "Ensure NCLEX tip is present (max 132 chars, 2 lines). Use nclex_tip_fallback if missing.",
            'vignette_structure': "Verify vignette has 2-4 sentence stem and exactly 4 options (A, B, C, D).",
            'answer_structure': "Verify answer has correct answer statement, rationale, and distractor analysis.",
            'markers': "Insert [PAUSE] (min 2) and [EMPHASIS: term] markers in presenter notes.",
            'numbering': "Renumber slides sequentially starting from 1. No gaps or duplicates.",
            'visual_quota': "Check visual count against quota requirements. Add visuals to high-opportunity slides."
        }

        for category in failing_categories:
            guidance[category] = category_tips.get(category, f"Review {category} requirements.")

        return guidance

    def _save_retry_log(self, context: RetryContext) -> str:
        """Save retry log to disk."""
        filename = f"retry_step{context.step}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        filepath = self.output_dir / filename

        log_data = {
            'context': context.to_dict(),
            'summary': {
                'iterations_used': context.current_iteration,
                'final_score': context.iterations[-1].score if context.iterations else 0,
                'score_trajectory': context.get_score_trajectory(),
                'improvement_rate': context.get_improvement_rate(),
                'final_locked_slides': len(context.locked_slides),
                'final_failing_categories': context.failing_categories
            }
        }

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(log_data, f, indent=2)

        return str(filepath)

    def get_active_context(self, step: int) -> Optional[RetryContext]:
        """Get active retry context for a step."""
        return self._active_contexts.get(step)

    def clear_context(self, step: int) -> None:
        """Clear retry context for a step."""
        if step in self._active_contexts:
            del self._active_contexts[step]


# =============================================================================
# INCREMENTAL SCORING SUPPORT
# =============================================================================

class IncrementalScorer:
    """
    Supports incremental scoring - only revalidate changed slides.

    Caches validation results for locked slides to avoid redundant work.
    """

    def __init__(self):
        self._cache: Dict[str, Dict[str, Any]] = {}

    def _slide_key(self, slide: Dict[str, Any]) -> str:
        """Generate cache key for a slide."""
        slide_num = slide.get('slide_number', 0)
        # Include content hash for invalidation
        content = json.dumps({
            'header': slide.get('header', ''),
            'body': slide.get('body', ''),
            'nclex_tip': slide.get('nclex_tip', '')
        }, sort_keys=True)
        return f"{slide_num}:{hash(content)}"

    def get_cached_result(
        self,
        slide: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """Get cached validation result for a slide."""
        key = self._slide_key(slide)
        return self._cache.get(key)

    def cache_result(
        self,
        slide: Dict[str, Any],
        result: Dict[str, Any]
    ) -> None:
        """Cache validation result for a slide."""
        key = self._slide_key(slide)
        self._cache[key] = result

    def invalidate(self, slide_number: int) -> None:
        """Invalidate all cached results for a slide number."""
        to_remove = [k for k in self._cache if k.startswith(f"{slide_number}:")]
        for key in to_remove:
            del self._cache[key]

    def clear(self) -> None:
        """Clear all cached results."""
        self._cache.clear()

    def score_incrementally(
        self,
        slides: List[Dict[str, Any]],
        locked_slides: Set[int],
        validate_slide_fn: Callable[[Dict[str, Any]], Dict[str, Any]]
    ) -> Tuple[float, Dict[str, Any]]:
        """
        Score slides incrementally, using cache for locked slides.

        Args:
            slides: All slides to score
            locked_slides: Slide numbers that haven't changed
            validate_slide_fn: Function to validate a single slide

        Returns:
            Tuple of (overall_score, detailed_results)
        """
        all_results = []
        slides_validated = 0
        slides_from_cache = 0

        for slide in slides:
            slide_num = slide.get('slide_number')

            if slide_num in locked_slides:
                # Try cache first
                cached = self.get_cached_result(slide)
                if cached:
                    all_results.append(cached)
                    slides_from_cache += 1
                    continue

            # Validate and cache
            result = validate_slide_fn(slide)
            self.cache_result(slide, result)
            all_results.append(result)
            slides_validated += 1

        # Aggregate results
        total_score = sum(r.get('score', 0) for r in all_results) / len(all_results) if all_results else 0

        return total_score, {
            'slide_results': all_results,
            'slides_validated': slides_validated,
            'slides_from_cache': slides_from_cache,
            'incremental': True
        }


# =============================================================================
# CONVENIENCE FUNCTIONS
# =============================================================================

def create_retry_controller(
    output_dir: str = "outputs/retry_logs"
) -> SmartRetryController:
    """Create a retry controller with default state manager and error recovery."""
    try:
        from skills.utilities.step_state_manager import StepStateManager
        from skills.utilities.error_recovery import ErrorRecovery

        state_manager = StepStateManager()
        error_recovery = ErrorRecovery(state_manager)

        return SmartRetryController(
            state_manager=state_manager,
            error_recovery=error_recovery,
            output_dir=output_dir
        )
    except ImportError:
        return SmartRetryController(output_dir=output_dir)


def execute_step_with_retry(
    step: int,
    execute_fn: Callable,
    validate_fn: Callable,
    initial_input: Dict[str, Any],
    **kwargs
) -> RetryResult:
    """
    Convenience function to execute a step with retry.

    Args:
        step: Pipeline step number
        execute_fn: Execution function
        validate_fn: Validation function
        initial_input: Initial input
        **kwargs: Additional arguments for execute_with_retry

    Returns:
        RetryResult
    """
    controller = create_retry_controller()
    return controller.execute_with_retry(
        step=step,
        execute_fn=execute_fn,
        validate_fn=validate_fn,
        initial_input=initial_input,
        **kwargs
    )


# =============================================================================
# SELF TEST
# =============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("SMART RETRY CONTROLLER - SELF TEST")
    print("=" * 60)

    # Mock execute function that improves each iteration
    iteration_counter = [0]

    def mock_execute(input_data: Dict[str, Any]) -> Dict[str, Any]:
        iteration_counter[0] += 1
        # Simulate improvement
        base_score = 70 + (iteration_counter[0] * 8)
        return {
            'slides': [
                {'slide_number': i, 'header': f'Slide {i}'}
                for i in range(1, 11)
            ],
            'iteration': iteration_counter[0],
            'base_score': base_score
        }

    def mock_validate(output: Dict[str, Any]) -> Tuple[float, Dict[str, Any]]:
        score = output.get('base_score', 0)
        failing = []
        failing_slides = []

        if score < 80:
            failing.append('char_limits')
            failing_slides = [1, 3, 5]
        if score < 85:
            failing.append('markers')
            failing_slides.extend([2, 4])
        if score < 90:
            failing.append('nclex_tip')

        return score, {
            'category_scores': {
                'char_limits': {'raw_score': min(score + 5, 100)},
                'markers': {'raw_score': min(score, 100)},
                'nclex_tip': {'raw_score': min(score - 2, 100)}
            },
            'failing_slides': list(set(failing_slides)),
            'issues': [{'slide_number': s} for s in failing_slides]
        }

    # Test 1: Basic retry execution
    print("\n1. Testing retry execution:")
    controller = SmartRetryController(output_dir="outputs/retry_test")

    result = controller.execute_with_retry(
        step=8,
        execute_fn=mock_execute,
        validate_fn=mock_validate,
        initial_input={'blueprint': {}},
        target_score=90.0,
        max_iterations=3
    )

    print(f"   Success: {result.success}")
    print(f"   Final score: {result.final_score}")
    print(f"   Iterations: {result.iterations_used}")
    print(f"   Termination: {result.termination_reason.name}")

    # Test 2: Strategy determination
    print("\n2. Testing strategy determination:")
    strategy = controller._determine_strategy(['char_limits', 'markers'])
    print(f"   char_limits + markers: {strategy.name}")

    strategy = controller._determine_strategy(['anchor_coverage'])
    print(f"   anchor_coverage: {strategy.name}")

    strategy = controller._determine_strategy(['numbering', 'markers'])
    print(f"   numbering + markers: {strategy.name}")

    # Test 3: Incremental scorer
    print("\n3. Testing incremental scorer:")
    scorer = IncrementalScorer()

    slides = [
        {'slide_number': 1, 'header': 'Test 1', 'body': 'Content 1'},
        {'slide_number': 2, 'header': 'Test 2', 'body': 'Content 2'},
    ]

    def mock_slide_validate(slide):
        return {'score': 85, 'slide_number': slide['slide_number']}

    score, details = scorer.score_incrementally(
        slides=slides,
        locked_slides={1},  # Slide 1 is locked
        validate_slide_fn=mock_slide_validate
    )
    print(f"   First pass - Validated: {details['slides_validated']}, Cached: {details['slides_from_cache']}")

    # Second pass - should use cache for slide 1
    score, details = scorer.score_incrementally(
        slides=slides,
        locked_slides={1},
        validate_slide_fn=mock_slide_validate
    )
    print(f"   Second pass - Validated: {details['slides_validated']}, Cached: {details['slides_from_cache']}")

    # Test 4: Context tracking
    print("\n4. Testing context tracking:")
    if result.context:
        print(f"   Score trajectory: {result.context.get_score_trajectory()}")
        print(f"   Improvement rate: {result.context.get_improvement_rate():.2f}")
        print(f"   Locked slides: {len(result.context.locked_slides)}")

    # Cleanup
    import shutil
    shutil.rmtree("outputs/retry_test", ignore_errors=True)

    print("\n" + "=" * 60)
    print("SELF TEST COMPLETE")
    print("=" * 60)
