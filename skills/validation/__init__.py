"""
Validation skills for the NCLEX pipeline.
"""

from .visual_quota_tracker import (
    VisualQuotaTracker, QuotaStatus,
    check_quota, get_quota_requirements, needs_more_visuals
)
from .char_counter import (
    CharCounter, CharCountResult,
    count_chars_per_line, get_max_char_per_line, check_char_limit
)
from .line_counter import (
    LineCounter, LineCountResult,
    count_lines, count_non_empty_lines, check_line_limit
)
from .score_calculator import (
    ScoreCalculator,
    calculate_weighted_score,
    apply_deductions,
    check_automatic_fail_conditions,
    generate_score_breakdown,
    determine_status,
    format_score_report,
    DEFAULT_WEIGHTS,
    DEDUCTION_AMOUNTS
)
from .template_population_validator import (
    ValidationStatus, ChecklistItem, SlideValidation, ValidationReport,
    validate_slide, validate_section,
    generate_checklist_report, to_json,
    TEMPLATE_POPULATION_CHECKLIST
)
from .title_validator_skill import (
    validate_title,
    validate_blueprint_titles,
    is_title_valid,
    get_title_char_count
)

__all__ = [
    # Visual quota
    'VisualQuotaTracker', 'QuotaStatus',
    'check_quota', 'get_quota_requirements', 'needs_more_visuals',
    # Character counting
    'CharCounter', 'CharCountResult',
    'count_chars_per_line', 'get_max_char_per_line', 'check_char_limit',
    # Line counting
    'LineCounter', 'LineCountResult',
    'count_lines', 'count_non_empty_lines', 'check_line_limit',
    # Score calculator (Step 8 QA)
    'ScoreCalculator',
    'calculate_weighted_score', 'apply_deductions',
    'check_automatic_fail_conditions', 'generate_score_breakdown',
    'determine_status', 'format_score_report',
    'DEFAULT_WEIGHTS', 'DEDUCTION_AMOUNTS',
    # Template population validator (Step 12)
    'ValidationStatus', 'ChecklistItem', 'SlideValidation', 'ValidationReport',
    'validate_slide', 'validate_section',
    'generate_checklist_report', 'to_json',
    'TEMPLATE_POPULATION_CHECKLIST',
    # Title validator (R1)
    'validate_title',
    'validate_blueprint_titles',
    'is_title_valid',
    'get_title_char_count',
]
