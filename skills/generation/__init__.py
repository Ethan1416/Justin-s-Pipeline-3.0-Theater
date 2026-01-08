"""
Generation Skills Package
Skills for generating theater education content.

Theater Pipeline - Generates lessons, warmups, activities, and presenter notes.
"""

# New theater-specific generation skills
from .monologue_scripter import (
    generate_presenter_notes,
    generate_slide_notes,
    validate_presenter_notes,
    estimate_duration,
    count_words,
    insert_markers,
    SPEAKING_RATE_WPM,
    TARGET_DURATION_MINUTES,
    MIN_WORDS,
    MAX_WORDS,
    TARGET_WORDS
)

from .warmup_bank_selector import (
    select_warmup,
    get_warmups_by_type,
    get_warmups_for_unit,
    validate_warmup_connection,
    format_warmup_for_output,
    WARMUP_TYPES,
    WARMUP_BANK
)

from .activity_type_selector import (
    select_activity,
    get_activities_by_type,
    get_activities_for_unit,
    validate_activity_structure,
    format_activity_for_output,
    ACTIVITY_TYPES,
    ACTIVITY_BANK,
    ACTIVITY_STRUCTURE
)

__all__ = [
    # ==========================================================================
    # THEATER-SPECIFIC GENERATION SKILLS
    # ==========================================================================

    # Monologue Scripter (Presenter Notes - 15 min verbatim)
    'generate_presenter_notes',
    'generate_slide_notes',
    'validate_presenter_notes',
    'estimate_duration',
    'count_words',
    'insert_markers',
    'SPEAKING_RATE_WPM',
    'TARGET_DURATION_MINUTES',
    'MIN_WORDS',
    'MAX_WORDS',
    'TARGET_WORDS',

    # Warmup Bank Selector (5-min content-connected warmups)
    'select_warmup',
    'get_warmups_by_type',
    'get_warmups_for_unit',
    'validate_warmup_connection',
    'format_warmup_for_output',
    'WARMUP_TYPES',
    'WARMUP_BANK',

    # Activity Type Selector (15-min structured activities)
    'select_activity',
    'get_activities_by_type',
    'get_activities_for_unit',
    'validate_activity_structure',
    'format_activity_for_output',
    'ACTIVITY_TYPES',
    'ACTIVITY_BANK',
    'ACTIVITY_STRUCTURE',
]
