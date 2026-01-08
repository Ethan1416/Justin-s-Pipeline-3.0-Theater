"""
Utility Skills Package
Skills for utility functions in the theater education pipeline.

Theater Pipeline - Timing, objectives, text processing utilities.
"""

# =============================================================================
# THEATER-SPECIFIC UTILITY SKILLS
# =============================================================================

# Timing Pacer (pace content to duration)
from .timing_pacer import (
    pace_content,
    pace_presentation,
    calculate_target_words,
    suggest_content_adjustments,
    validate_pacing,
    distribute_words,
    estimate_duration as pacer_estimate_duration,
    count_words as pacer_count_words,
    SPEAKING_RATE_WPM,
    TOTAL_WORDS_MIN,
    TOTAL_WORDS_MAX,
    TOTAL_WORDS_TARGET,
    SLIDE_WORD_TARGETS
)

# Bloom's Verb Selector (learning objectives)
from .blooms_verb_selector import (
    select_verb,
    get_verbs_for_level,
    classify_verb,
    validate_objective,
    generate_objective,
    suggest_objectives_for_lesson,
    get_level_info,
    BLOOMS_LEVELS,
    BLOOMS_VERBS,
    THEATER_VERBS,
    LEVEL_DESCRIPTIONS
)

# Timing Allocator (56-minute structure)
from .timing_allocator import (
    allocate_lesson_time,
    allocate_activity_time,
    allocate_reflection_time,
    validate_timing,
    suggest_adjustments,
    generate_timing_script,
    format_time_marker,
    get_time_markers,
    LESSON_STRUCTURE,
    ACTIVITY_STRUCTURE,
    REFLECTION_STRUCTURE,
    ACTIVITY_TYPE_TIMING
)

# =============================================================================
# LEGACY UTILITY SKILLS (from NCLEX pipeline)
# =============================================================================

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
    # ==========================================================================
    # THEATER-SPECIFIC UTILITY SKILLS
    # ==========================================================================

    # Timing Pacer (pace content to duration targets)
    'pace_content',
    'pace_presentation',
    'calculate_target_words',
    'suggest_content_adjustments',
    'validate_pacing',
    'distribute_words',
    'pacer_estimate_duration',
    'pacer_count_words',
    'SPEAKING_RATE_WPM',
    'TOTAL_WORDS_MIN',
    'TOTAL_WORDS_MAX',
    'TOTAL_WORDS_TARGET',
    'SLIDE_WORD_TARGETS',

    # Bloom's Verb Selector (learning objectives)
    'select_verb',
    'get_verbs_for_level',
    'classify_verb',
    'validate_objective',
    'generate_objective',
    'suggest_objectives_for_lesson',
    'get_level_info',
    'BLOOMS_LEVELS',
    'BLOOMS_VERBS',
    'THEATER_VERBS',
    'LEVEL_DESCRIPTIONS',

    # Timing Allocator (56-minute structure)
    'allocate_lesson_time',
    'allocate_activity_time',
    'allocate_reflection_time',
    'validate_timing',
    'suggest_adjustments',
    'generate_timing_script',
    'format_time_marker',
    'get_time_markers',
    'LESSON_STRUCTURE',
    'ACTIVITY_STRUCTURE',
    'REFLECTION_STRUCTURE',
    'ACTIVITY_TYPE_TIMING',

    # ==========================================================================
    # LEGACY UTILITY SKILLS
    # ==========================================================================

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
