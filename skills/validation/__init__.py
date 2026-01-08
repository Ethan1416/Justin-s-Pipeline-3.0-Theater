"""
Validation Skills Package
Skills for validating theater education content.

Theater Pipeline - Validates timing, word counts, structure, and completeness.
"""

# =============================================================================
# THEATER-SPECIFIC VALIDATION SKILLS
# =============================================================================

# Word Count Analyzer (Total: 1,950-2,250 words)
from .word_count_analyzer import (
    count_words,
    count_words_detailed,
    get_slide_targets,
    analyze_slide_word_count,
    get_per_slide_analysis,
    analyze_word_count,
    validate_word_counts,
    calculate_words_needed,
    suggest_distribution,
    SPEAKING_RATE_WPM,
    TOTAL_REQUIREMENTS,
    SLIDE_TARGETS,
    DEFAULT_TARGETS
)

# Duration Estimator (Target: 14-16 minutes)
from .duration_estimator import (
    estimate_duration,
    estimate_slide_duration,
    estimate_presentation_duration,
    validate_timing,
    get_pacing_analysis,
    calculate_time_adjustment,
    count_markers,
    calculate_marker_time,
    SPEAKING_RATE_WPM as DURATION_SPEAKING_RATE_WPM,
    TARGET_DURATION_MINUTES,
    MIN_DURATION_MINUTES,
    MAX_DURATION_MINUTES,
    MARKER_DURATIONS,
    SLIDE_DURATION_TARGETS
)

# Sentence Completeness Checker (HARDCODED - no truncation allowed)
from .sentence_completeness_checker import (
    is_complete_sentence,
    check_bullet_point,
    find_truncations,
    validate_text,
    check_sentence_completeness,
    auto_fix_truncations,
    fix_slide_truncations,
    TERMINAL_PUNCTUATION,
    TRUNCATION_PATTERNS,
    FRAGMENT_STARTERS
)

__all__ = [
    # ==========================================================================
    # WORD COUNT ANALYZER
    # Validates presenter notes meet 1,950-2,250 word requirement
    # ==========================================================================
    'count_words',
    'count_words_detailed',
    'get_slide_targets',
    'analyze_slide_word_count',
    'get_per_slide_analysis',
    'analyze_word_count',
    'validate_word_counts',
    'calculate_words_needed',
    'suggest_distribution',
    'SPEAKING_RATE_WPM',
    'TOTAL_REQUIREMENTS',
    'SLIDE_TARGETS',
    'DEFAULT_TARGETS',

    # ==========================================================================
    # DURATION ESTIMATOR
    # Validates presentation timing meets 14-16 minute requirement
    # ==========================================================================
    'estimate_duration',
    'estimate_slide_duration',
    'estimate_presentation_duration',
    'validate_timing',
    'get_pacing_analysis',
    'calculate_time_adjustment',
    'count_markers',
    'calculate_marker_time',
    'DURATION_SPEAKING_RATE_WPM',
    'TARGET_DURATION_MINUTES',
    'MIN_DURATION_MINUTES',
    'MAX_DURATION_MINUTES',
    'MARKER_DURATIONS',
    'SLIDE_DURATION_TARGETS',

    # ==========================================================================
    # SENTENCE COMPLETENESS CHECKER (HARDCODED VALIDATOR)
    # Detects truncation, incomplete sentences, missing punctuation
    # Content MUST PASS this validator to proceed
    # ==========================================================================
    'is_complete_sentence',
    'check_bullet_point',
    'find_truncations',
    'validate_text',
    'check_sentence_completeness',
    'auto_fix_truncations',
    'fix_slide_truncations',
    'TERMINAL_PUNCTUATION',
    'TRUNCATION_PATTERNS',
    'FRAGMENT_STARTERS',
]
