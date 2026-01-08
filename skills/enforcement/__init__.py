"""
Enforcement Skills Package
Skills for enforcing requirements on generated content.

Theater Pipeline Version - Uses performance tips instead of NCLEX tips.
"""

from .slide_numbering import (
    enforce_sequential_numbering,
    validate_sequential_numbering
)
from .performance_tip_fallback import (
    ensure_performance_tip,
    ensure_all_tips,
    validate_performance_tips,
    get_fallback_tip
)
from .header_enforcer import (
    enforce_header_limits,
    validate_header,
    abbreviate_text,
    smart_truncate,
    split_into_lines
)
from .body_line_enforcer import (
    enforce_body_lines,
    validate_body_lines,
    count_non_empty_lines,
    condense_bullets,
    split_body_content
)
from .body_char_enforcer import (
    enforce_body_chars,
    validate_body_chars,
    is_bullet_line,
    get_indent
)
from .text_limits_enforcer import (
    enforce_all_text_limits,
    validate_all_text_limits,
    enforce_all_slides
)
from .marker_insertion import (
    insert_markers,
    validate_markers,
    count_markers,
    insert_pause_markers,
    insert_emphasis_markers,
    find_key_terms
)
from .body_overflow_enforcer import (
    enforce_body_content,
    enforce_slide_body,
    enforce_blueprint_body,
    validate_body_content
)
from .title_reviser_skill import (
    revise_title,
    revise_slide_title,
    revise_blueprint_titles,
    apply_abbreviations as title_abbreviations
)

__all__ = [
    # Slide numbering (R15)
    'enforce_sequential_numbering',
    'validate_sequential_numbering',
    # Performance tips (Theater equivalent of R4)
    'ensure_performance_tip',
    'ensure_all_tips',
    'validate_performance_tips',
    'get_fallback_tip',
    # Header limits (R1)
    'enforce_header_limits',
    'validate_header',
    'abbreviate_text',
    'smart_truncate',
    'split_into_lines',
    # Body line limits (R2)
    'enforce_body_lines',
    'validate_body_lines',
    'count_non_empty_lines',
    'condense_bullets',
    'split_body_content',
    # Body char limits (R3)
    'enforce_body_chars',
    'validate_body_chars',
    'is_bullet_line',
    'get_indent',
    # Unified enforcement
    'enforce_all_text_limits',
    'validate_all_text_limits',
    'enforce_all_slides',
    # Marker insertion (R14)
    'insert_markers',
    'validate_markers',
    'count_markers',
    'insert_pause_markers',
    'insert_emphasis_markers',
    'find_key_terms',
    # Body overflow enforcement (template capacity)
    'enforce_body_content',
    'enforce_slide_body',
    'enforce_blueprint_body',
    'validate_body_content',
    # Title revision (R1 - no truncation, only revision)
    'revise_title',
    'revise_slide_title',
    'revise_blueprint_titles',
    'title_abbreviations',
]
