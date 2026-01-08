"""
Utility skills for the NCLEX pipeline.
"""

from .text_splitter import (
    split_at_word_boundary, split_slide_content,
    smart_split, split_for_continuation_slide
)
from .line_wrapper import (
    LineWrapper, WrapResult,
    wrap_text, wrap_to_lines, wrap_header, wrap_body
)
from .bullet_formatter import (
    BulletFormatter, BulletFormatResult,
    format_bullets, normalize_bullets, count_bullets
)
from .marker_inserter import (
    add_visual_marker, validate_all_markers, count_markers,
    fix_missing_markers, validate_marker_format,
    get_visual_type_counts, get_slides_by_marker_type,
    VALID_VISUAL_TYPES
)
from .step_state_manager import (
    StepStateManager, StepState, RetryContext
)
from .error_recovery import (
    ErrorRecovery, PipelineError, RecoveryResult,
    ErrorType, RecoveryAction, RecoveryStrategy,
    handle_error, get_recovery_strategy
)
from .smart_retry_controller import (
    SmartRetryController, IncrementalScorer,
    RetryStrategy, TerminationReason, RetryResult,
    RetryContext as SmartRetryContext, RetryIteration,
    create_retry_controller, execute_step_with_retry
)

__all__ = [
    # Text splitting
    'split_at_word_boundary', 'split_slide_content',
    'smart_split', 'split_for_continuation_slide',
    # Line wrapping
    'LineWrapper', 'WrapResult',
    'wrap_text', 'wrap_to_lines', 'wrap_header', 'wrap_body',
    # Bullet formatting
    'BulletFormatter', 'BulletFormatResult',
    'format_bullets', 'normalize_bullets', 'count_bullets',
    # Marker inserter (Step 10 Visual Integration)
    'add_visual_marker', 'validate_all_markers', 'count_markers',
    'fix_missing_markers', 'validate_marker_format',
    'get_visual_type_counts', 'get_slides_by_marker_type',
    'VALID_VISUAL_TYPES',
    # Step State Manager (inter-step persistence)
    'StepStateManager', 'StepState', 'RetryContext',
    # Error Recovery (unified error handling)
    'ErrorRecovery', 'PipelineError', 'RecoveryResult',
    'ErrorType', 'RecoveryAction', 'RecoveryStrategy',
    'handle_error', 'get_recovery_strategy',
    # Smart Retry Controller (intelligent retry loops)
    'SmartRetryController', 'IncrementalScorer',
    'RetryStrategy', 'TerminationReason', 'RetryResult',
    'SmartRetryContext', 'RetryIteration',
    'create_retry_controller', 'execute_step_with_retry',
]
