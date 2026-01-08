"""
Error Recovery System
Unified error handling and recovery strategies for the NCLEX pipeline.

Provides:
- Error classification and categorization
- Automatic recovery strategies
- Fallback actions for common failure scenarios
- Integration with StepStateManager for retry coordination

Usage:
    from skills.utilities.error_recovery import (
        ErrorRecovery, PipelineError, ErrorType,
        handle_error, get_recovery_strategy
    )

    recovery = ErrorRecovery(state_manager=manager)

    # Handle specific error
    result = recovery.handle(
        error_type=ErrorType.QA_SCORE_LOW,
        context={'score': 75, 'step': 8}
    )

    # Get recovery strategy
    strategy = get_recovery_strategy(ErrorType.QUOTA_NOT_MET)
"""

from enum import Enum, auto
from typing import Dict, Any, List, Optional, Callable, Tuple
from dataclasses import dataclass, field
from datetime import datetime
import traceback


class ErrorType(Enum):
    """Classification of pipeline errors."""
    # Step 8 - QA errors
    QA_SCORE_LOW = auto()
    QA_CATEGORY_FAIL = auto()
    QA_AUTO_FAIL = auto()

    # Step 9 - Visual identification errors
    QUOTA_NOT_MET = auto()
    QUOTA_EXCEEDED = auto()
    VISUAL_TYPE_INVALID = auto()

    # Step 10 - Visual integration errors
    MISSING_MARKER = auto()
    SPEC_MISMATCH = auto()
    INTEGRATION_FAIL = auto()

    # General pipeline errors
    MISSING_INPUT = auto()
    INVALID_FORMAT = auto()
    CONSTRAINT_VIOLATION = auto()
    STEP_DEPENDENCY_FAIL = auto()

    # System errors
    FILE_NOT_FOUND = auto()
    PARSE_ERROR = auto()
    TIMEOUT = auto()
    UNKNOWN = auto()


class RecoveryAction(Enum):
    """Actions that can be taken to recover from errors."""
    RETRY_FROM_STEP = auto()
    FORCE_VISUAL_IDENTIFICATION = auto()
    ADD_DEFAULT_MARKERS = auto()
    REGENERATE_VISUAL_SPEC = auto()
    APPLY_FALLBACK = auto()
    SKIP_AND_CONTINUE = auto()
    ESCALATE_TO_USER = auto()
    ABORT = auto()


@dataclass
class PipelineError:
    """Detailed error information."""
    error_type: ErrorType
    message: str
    step: int
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    details: Dict[str, Any] = field(default_factory=dict)
    recoverable: bool = True
    stack_trace: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'error_type': self.error_type.name,
            'message': self.message,
            'step': self.step,
            'timestamp': self.timestamp,
            'details': self.details,
            'recoverable': self.recoverable,
            'stack_trace': self.stack_trace
        }


@dataclass
class RecoveryStrategy:
    """Strategy for recovering from an error."""
    action: RecoveryAction
    target_step: Optional[int] = None
    parameters: Dict[str, Any] = field(default_factory=dict)
    description: str = ""
    max_attempts: int = 3
    fallback_action: Optional[RecoveryAction] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'action': self.action.name,
            'target_step': self.target_step,
            'parameters': self.parameters,
            'description': self.description,
            'max_attempts': self.max_attempts,
            'fallback_action': self.fallback_action.name if self.fallback_action else None
        }


@dataclass
class RecoveryResult:
    """Result of a recovery attempt."""
    success: bool
    action_taken: RecoveryAction
    message: str
    new_state: Optional[Dict[str, Any]] = None
    retry_recommended: bool = False
    next_step: Optional[int] = None


# =============================================================================
# ERROR HANDLERS - Specific recovery logic for each error type
# =============================================================================

ERROR_HANDLERS: Dict[ErrorType, Callable] = {}


def _handle_qa_score_low(
    context: Dict[str, Any],
    state_manager: Optional[Any] = None
) -> RecoveryResult:
    """
    Handle QA score below pass threshold.

    Strategy:
    1. Identify failing categories
    2. Lock passing slides
    3. Retry from Step 7 (content generation)
    """
    score = context.get('score', 0)
    step = context.get('step', 8)
    category_scores = context.get('category_scores', {})

    # Find failing categories
    failing = [
        cat for cat, data in category_scores.items()
        if (data.get('raw_score', data) if isinstance(data, dict) else data) < 80
    ]

    # Find passing slides to lock
    passing_slides = context.get('passing_slides', [])

    if state_manager:
        state_manager.mark_slides_locked(passing_slides)
        state_manager.set_retry_context(
            step=step,
            failing_categories=failing
        )
        state_manager.record_score(step=step, score=score)

    return RecoveryResult(
        success=True,
        action_taken=RecoveryAction.RETRY_FROM_STEP,
        message=f"Score {score:.1f} below threshold. Retrying with focus on: {', '.join(failing)}",
        retry_recommended=True,
        next_step=7  # Retry from content generation
    )


def _handle_quota_not_met(
    context: Dict[str, Any],
    state_manager: Optional[Any] = None
) -> RecoveryResult:
    """
    Handle visual quota not met.

    Strategy:
    1. Rank non-visual slides by visual opportunity
    2. Force top candidates to become visuals
    """
    current_count = context.get('current_visual_count', 0)
    min_required = context.get('min_required', 2)
    slides = context.get('slides', [])

    # Import here to avoid circular dependency
    try:
        from skills.generation.visual_pattern_matcher import generate_fallback_visual
        candidates = generate_fallback_visual(slides, current_count, min_required)
    except ImportError:
        candidates = []

    return RecoveryResult(
        success=len(candidates) > 0,
        action_taken=RecoveryAction.FORCE_VISUAL_IDENTIFICATION,
        message=f"Quota not met ({current_count}/{min_required}). Suggested slides for visuals: {candidates}",
        new_state={'visual_candidates': candidates},
        retry_recommended=True,
        next_step=9
    )


def _handle_missing_marker(
    context: Dict[str, Any],
    state_manager: Optional[Any] = None
) -> RecoveryResult:
    """
    Handle slides missing visual markers.

    Strategy:
    Add default "Visual: No" markers to unmarked slides.
    """
    slides = context.get('slides', [])
    missing_count = context.get('missing_count', 0)

    # Import and use marker inserter
    try:
        from skills.utilities.marker_inserter import fix_missing_markers
        blueprint = {'slides': slides}
        fixed = fix_missing_markers(blueprint)
        fixed_slides = fixed.get('slides', slides)
    except ImportError:
        fixed_slides = slides

    return RecoveryResult(
        success=True,
        action_taken=RecoveryAction.ADD_DEFAULT_MARKERS,
        message=f"Added default markers to {missing_count} slides",
        new_state={'slides': fixed_slides},
        retry_recommended=False
    )


def _handle_spec_mismatch(
    context: Dict[str, Any],
    state_manager: Optional[Any] = None
) -> RecoveryResult:
    """
    Handle visual specification mismatch.

    Strategy:
    Regenerate visual specification for the affected slide.
    """
    slide_number = context.get('slide_number')
    expected_type = context.get('expected_type')
    actual_type = context.get('actual_type')

    return RecoveryResult(
        success=True,
        action_taken=RecoveryAction.REGENERATE_VISUAL_SPEC,
        message=f"Slide {slide_number}: Expected {expected_type}, got {actual_type}. Regenerating spec.",
        new_state={'regenerate_slide': slide_number},
        retry_recommended=True,
        next_step=9
    )


def _handle_constraint_violation(
    context: Dict[str, Any],
    state_manager: Optional[Any] = None
) -> RecoveryResult:
    """
    Handle text constraint violations.

    Strategy:
    Apply text enforcement skills to fix violations.
    """
    violation_type = context.get('violation_type', 'unknown')
    slide_number = context.get('slide_number')
    field = context.get('field', 'body')

    return RecoveryResult(
        success=True,
        action_taken=RecoveryAction.APPLY_FALLBACK,
        message=f"Constraint violation ({violation_type}) on slide {slide_number} {field}",
        new_state={
            'fix_constraint': True,
            'slide_number': slide_number,
            'field': field,
            'violation_type': violation_type
        },
        retry_recommended=True,
        next_step=7
    )


def _handle_unknown(
    context: Dict[str, Any],
    state_manager: Optional[Any] = None
) -> RecoveryResult:
    """Handle unknown errors by escalating to user."""
    error_msg = context.get('error_message', 'Unknown error')

    return RecoveryResult(
        success=False,
        action_taken=RecoveryAction.ESCALATE_TO_USER,
        message=f"Unhandled error: {error_msg}",
        retry_recommended=False
    )


# Register handlers
ERROR_HANDLERS = {
    ErrorType.QA_SCORE_LOW: _handle_qa_score_low,
    ErrorType.QA_CATEGORY_FAIL: _handle_qa_score_low,  # Same handler
    ErrorType.QUOTA_NOT_MET: _handle_quota_not_met,
    ErrorType.MISSING_MARKER: _handle_missing_marker,
    ErrorType.SPEC_MISMATCH: _handle_spec_mismatch,
    ErrorType.CONSTRAINT_VIOLATION: _handle_constraint_violation,
    ErrorType.UNKNOWN: _handle_unknown,
}


# =============================================================================
# RECOVERY STRATEGIES - Pre-defined strategies for each error type
# =============================================================================

RECOVERY_STRATEGIES: Dict[ErrorType, RecoveryStrategy] = {
    ErrorType.QA_SCORE_LOW: RecoveryStrategy(
        action=RecoveryAction.RETRY_FROM_STEP,
        target_step=7,
        description="Retry content generation with focus on failing categories",
        max_attempts=3,
        fallback_action=RecoveryAction.ESCALATE_TO_USER
    ),
    ErrorType.QA_CATEGORY_FAIL: RecoveryStrategy(
        action=RecoveryAction.RETRY_FROM_STEP,
        target_step=7,
        description="Retry with specific category fixes",
        max_attempts=3
    ),
    ErrorType.QA_AUTO_FAIL: RecoveryStrategy(
        action=RecoveryAction.RETRY_FROM_STEP,
        target_step=6,
        description="Auto-fail requires earlier retry",
        max_attempts=2
    ),
    ErrorType.QUOTA_NOT_MET: RecoveryStrategy(
        action=RecoveryAction.FORCE_VISUAL_IDENTIFICATION,
        target_step=9,
        description="Force visual identification on best candidates",
        max_attempts=2
    ),
    ErrorType.QUOTA_EXCEEDED: RecoveryStrategy(
        action=RecoveryAction.APPLY_FALLBACK,
        target_step=9,
        description="Remove lowest-scored visuals",
        max_attempts=1
    ),
    ErrorType.MISSING_MARKER: RecoveryStrategy(
        action=RecoveryAction.ADD_DEFAULT_MARKERS,
        description="Add default Visual: No markers",
        max_attempts=1
    ),
    ErrorType.SPEC_MISMATCH: RecoveryStrategy(
        action=RecoveryAction.REGENERATE_VISUAL_SPEC,
        target_step=9,
        description="Regenerate visual specification",
        max_attempts=2
    ),
    ErrorType.CONSTRAINT_VIOLATION: RecoveryStrategy(
        action=RecoveryAction.APPLY_FALLBACK,
        target_step=7,
        description="Apply text enforcement skills",
        max_attempts=3
    ),
    ErrorType.MISSING_INPUT: RecoveryStrategy(
        action=RecoveryAction.ABORT,
        description="Cannot proceed without required input",
        max_attempts=0
    ),
    ErrorType.STEP_DEPENDENCY_FAIL: RecoveryStrategy(
        action=RecoveryAction.RETRY_FROM_STEP,
        description="Retry from failed dependency step",
        max_attempts=2
    )
}


# =============================================================================
# ERROR RECOVERY CLASS
# =============================================================================

class ErrorRecovery:
    """
    Unified error recovery system for the NCLEX pipeline.

    Coordinates error handling, recovery strategies, and retry logic
    with the StepStateManager.
    """

    def __init__(self, state_manager: Optional[Any] = None):
        """
        Initialize error recovery system.

        Args:
            state_manager: Optional StepStateManager instance
        """
        self.state_manager = state_manager
        self.error_history: List[PipelineError] = []
        self.recovery_history: List[RecoveryResult] = []

    def classify_error(
        self,
        error: Exception,
        step: int,
        context: Optional[Dict[str, Any]] = None
    ) -> ErrorType:
        """
        Classify an exception into an ErrorType.

        Args:
            error: The exception that occurred
            step: Current pipeline step
            context: Additional context

        Returns:
            Classified ErrorType
        """
        error_str = str(error).lower()
        context = context or {}

        # QA-related errors
        if 'score' in error_str or 'threshold' in error_str:
            return ErrorType.QA_SCORE_LOW
        if 'category' in error_str and 'fail' in error_str:
            return ErrorType.QA_CATEGORY_FAIL

        # Visual-related errors
        if 'quota' in error_str:
            if 'exceed' in error_str or 'max' in error_str:
                return ErrorType.QUOTA_EXCEEDED
            return ErrorType.QUOTA_NOT_MET
        if 'marker' in error_str:
            return ErrorType.MISSING_MARKER
        if 'spec' in error_str or 'mismatch' in error_str:
            return ErrorType.SPEC_MISMATCH

        # Constraint errors
        if 'constraint' in error_str or 'limit' in error_str:
            return ErrorType.CONSTRAINT_VIOLATION

        # Input/format errors
        if 'not found' in error_str or 'missing' in error_str:
            if 'file' in error_str:
                return ErrorType.FILE_NOT_FOUND
            return ErrorType.MISSING_INPUT
        if 'parse' in error_str or 'format' in error_str:
            return ErrorType.PARSE_ERROR
        if 'timeout' in error_str:
            return ErrorType.TIMEOUT

        return ErrorType.UNKNOWN

    def create_error(
        self,
        error_type: ErrorType,
        message: str,
        step: int,
        details: Optional[Dict[str, Any]] = None,
        exception: Optional[Exception] = None
    ) -> PipelineError:
        """
        Create a PipelineError instance.

        Args:
            error_type: Type of error
            message: Error message
            step: Pipeline step where error occurred
            details: Additional error details
            exception: Original exception if any

        Returns:
            PipelineError instance
        """
        error = PipelineError(
            error_type=error_type,
            message=message,
            step=step,
            details=details or {},
            recoverable=error_type not in [
                ErrorType.MISSING_INPUT,
                ErrorType.FILE_NOT_FOUND
            ],
            stack_trace=traceback.format_exc() if exception else None
        )

        self.error_history.append(error)
        return error

    def handle(
        self,
        error_type: ErrorType,
        context: Dict[str, Any]
    ) -> RecoveryResult:
        """
        Handle an error and attempt recovery.

        Args:
            error_type: Type of error to handle
            context: Error context with relevant data

        Returns:
            RecoveryResult with outcome
        """
        handler = ERROR_HANDLERS.get(error_type, _handle_unknown)
        result = handler(context, self.state_manager)

        self.recovery_history.append(result)
        return result

    def get_strategy(self, error_type: ErrorType) -> RecoveryStrategy:
        """
        Get the recovery strategy for an error type.

        Args:
            error_type: Type of error

        Returns:
            RecoveryStrategy instance
        """
        return RECOVERY_STRATEGIES.get(
            error_type,
            RecoveryStrategy(
                action=RecoveryAction.ESCALATE_TO_USER,
                description="No specific strategy defined"
            )
        )

    def should_attempt_recovery(
        self,
        error_type: ErrorType,
        attempt_count: int = 0
    ) -> bool:
        """
        Determine if recovery should be attempted.

        Args:
            error_type: Type of error
            attempt_count: Number of previous attempts

        Returns:
            True if recovery should be attempted
        """
        strategy = self.get_strategy(error_type)

        if attempt_count >= strategy.max_attempts:
            return False

        if strategy.action == RecoveryAction.ABORT:
            return False

        return True

    def get_error_summary(self) -> Dict[str, Any]:
        """Get summary of all errors encountered."""
        return {
            'total_errors': len(self.error_history),
            'by_type': {
                et.name: len([e for e in self.error_history if e.error_type == et])
                for et in ErrorType
                if any(e.error_type == et for e in self.error_history)
            },
            'recoverable_count': len([e for e in self.error_history if e.recoverable]),
            'recovery_attempts': len(self.recovery_history),
            'successful_recoveries': len([r for r in self.recovery_history if r.success])
        }

    def clear_history(self) -> None:
        """Clear error and recovery history."""
        self.error_history.clear()
        self.recovery_history.clear()


# =============================================================================
# CONVENIENCE FUNCTIONS
# =============================================================================

def handle_error(
    error_type: ErrorType,
    context: Dict[str, Any],
    state_manager: Optional[Any] = None
) -> RecoveryResult:
    """
    Handle an error with optional state manager.

    Args:
        error_type: Type of error
        context: Error context
        state_manager: Optional state manager

    Returns:
        RecoveryResult
    """
    recovery = ErrorRecovery(state_manager)
    return recovery.handle(error_type, context)


def get_recovery_strategy(error_type: ErrorType) -> RecoveryStrategy:
    """
    Get recovery strategy for an error type.

    Args:
        error_type: Type of error

    Returns:
        RecoveryStrategy
    """
    return RECOVERY_STRATEGIES.get(
        error_type,
        RecoveryStrategy(
            action=RecoveryAction.ESCALATE_TO_USER,
            description="No specific strategy"
        )
    )


if __name__ == "__main__":
    print("=" * 60)
    print("ERROR RECOVERY SYSTEM - SELF TEST")
    print("=" * 60)

    recovery = ErrorRecovery()

    # Test 1: Handle QA score low
    print("\n1. Testing QA_SCORE_LOW handling:")
    result = recovery.handle(
        ErrorType.QA_SCORE_LOW,
        {
            'score': 75,
            'step': 8,
            'category_scores': {
                'anchor_coverage': {'raw_score': 65},
                'char_limit': {'raw_score': 92}
            },
            'passing_slides': [1, 2, 5]
        }
    )
    print(f"   Action: {result.action_taken.name}")
    print(f"   Message: {result.message}")
    print(f"   Retry? {result.retry_recommended}")
    print(f"   Next step: {result.next_step}")

    # Test 2: Handle quota not met
    print("\n2. Testing QUOTA_NOT_MET handling:")
    result = recovery.handle(
        ErrorType.QUOTA_NOT_MET,
        {
            'current_visual_count': 1,
            'min_required': 3,
            'slides': [{'slide_number': i} for i in range(1, 16)]
        }
    )
    print(f"   Action: {result.action_taken.name}")
    print(f"   Message: {result.message}")

    # Test 3: Handle missing marker
    print("\n3. Testing MISSING_MARKER handling:")
    result = recovery.handle(
        ErrorType.MISSING_MARKER,
        {
            'slides': [{'slide_number': 1}, {'slide_number': 2}],
            'missing_count': 2
        }
    )
    print(f"   Action: {result.action_taken.name}")
    print(f"   Success: {result.success}")

    # Test 4: Get recovery strategies
    print("\n4. Recovery strategies:")
    for et in [ErrorType.QA_SCORE_LOW, ErrorType.QUOTA_NOT_MET, ErrorType.MISSING_INPUT]:
        strategy = get_recovery_strategy(et)
        print(f"   {et.name}: {strategy.action.name} (max: {strategy.max_attempts})")

    # Test 5: Error classification
    print("\n5. Error classification:")
    test_errors = [
        Exception("Score 75 below threshold"),
        Exception("Visual quota not met"),
        Exception("File not found: blueprint.json")
    ]
    for err in test_errors:
        classified = recovery.classify_error(err, step=8)
        print(f"   '{str(err)[:30]}...' -> {classified.name}")

    # Test 6: Error summary
    print("\n6. Error summary:")
    summary = recovery.get_error_summary()
    print(f"   {summary}")

    print("\n" + "=" * 60)
    print("SELF TEST COMPLETE")
    print("=" * 60)
