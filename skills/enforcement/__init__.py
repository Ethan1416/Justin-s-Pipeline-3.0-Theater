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
from .monologue_generator import (
    generate_monologue,
    generate_all_monologues,
    generate_agenda_monologue,
    generate_warmup_monologue,
    generate_content_monologue,
    generate_activity_monologue,
    generate_journal_monologue,
    validate_monologue as validate_generated_monologue,
    count_markers as count_monologue_markers_gen,
    MIN_WORDS_PER_SLIDE,
    MAX_WORDS_PER_SLIDE,
    REQUIRED_MARKERS
)
from .monologue_validator import (
    validate_slide_monologue,
    validate_presentation_monologues,
    has_valid_monologue,
    get_monologue_issues,
    count_monologue_words,
    count_monologue_markers,
    MIN_WORDS,
    MAX_WORDS,
    MIN_PAUSE_PER_SLIDE,
    MIN_EMPHASIS_PER_SLIDE,
    MIN_TOTAL_PAUSE,
    MIN_TOTAL_EMPHASIS,
    MIN_TOTAL_CHECK,
    MARKER_PATTERNS
)
from .handout_generator import (
    generate_activity_handout,
    generate_sorting_handout,
    generate_matching_handout,
    generate_sequencing_handout,
    generate_discussion_handout,
    create_base_document,
    add_instructions,
    add_answer_key_page,
    add_footer,
    ACTIVITY_TYPES_REQUIRING_HANDOUTS,
    MIN_ITEMS_PER_ACTIVITY,
    MAX_ITEMS_PER_ACTIVITY
)
from .handout_validator import (
    validate_handout_file,
    validate_activity_data,
    validate_lesson_handouts,
    has_valid_handout,
    get_handout_issues,
    MIN_ITEMS,
    MAX_ITEMS,
    REQUIRED_SECTIONS
)
from .production_folder_generator import (
    create_production_structure,
    copy_to_production,
    copy_all_lesson_files,
    export_lesson_to_production,
    get_production_path,
    list_production_contents,
    open_production_folder,
    PRODUCTION_ROOT,
    DESKTOP_PATH,
    REQUIRED_FILES as PRODUCTION_REQUIRED_FILES,
    UNIT_NAMES
)
from .production_folder_validator import (
    validate_production_root,
    validate_unit_folder,
    validate_day_folder,
    validate_powerpoint_slides,
    validate_production_output,
    has_valid_production,
    get_production_issues,
    production_folder_exists,
    REQUIRED_SLIDE_COUNT,
    MIN_FILE_SIZES
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
    # Monologue generation (HARDCODED)
    'generate_monologue',
    'generate_all_monologues',
    'generate_agenda_monologue',
    'generate_warmup_monologue',
    'generate_content_monologue',
    'generate_activity_monologue',
    'generate_journal_monologue',
    'validate_generated_monologue',
    'count_monologue_markers_gen',
    'MIN_WORDS_PER_SLIDE',
    'MAX_WORDS_PER_SLIDE',
    'REQUIRED_MARKERS',
    # Monologue validation (HARDCODED)
    'validate_slide_monologue',
    'validate_presentation_monologues',
    'has_valid_monologue',
    'get_monologue_issues',
    'count_monologue_words',
    'count_monologue_markers',
    'MIN_WORDS',
    'MAX_WORDS',
    'MIN_PAUSE_PER_SLIDE',
    'MIN_EMPHASIS_PER_SLIDE',
    'MIN_TOTAL_PAUSE',
    'MIN_TOTAL_EMPHASIS',
    'MIN_TOTAL_CHECK',
    'MARKER_PATTERNS',
    # Handout generation (HARDCODED)
    'generate_activity_handout',
    'generate_sorting_handout',
    'generate_matching_handout',
    'generate_sequencing_handout',
    'generate_discussion_handout',
    'create_base_document',
    'add_instructions',
    'add_answer_key_page',
    'add_footer',
    'ACTIVITY_TYPES_REQUIRING_HANDOUTS',
    'MIN_ITEMS_PER_ACTIVITY',
    'MAX_ITEMS_PER_ACTIVITY',
    # Handout validation (HARDCODED)
    'validate_handout_file',
    'validate_activity_data',
    'validate_lesson_handouts',
    'has_valid_handout',
    'get_handout_issues',
    'MIN_ITEMS',
    'MAX_ITEMS',
    'REQUIRED_SECTIONS',
    # Production folder generation (HARDCODED)
    'create_production_structure',
    'copy_to_production',
    'copy_all_lesson_files',
    'export_lesson_to_production',
    'get_production_path',
    'list_production_contents',
    'open_production_folder',
    'PRODUCTION_ROOT',
    'DESKTOP_PATH',
    'PRODUCTION_REQUIRED_FILES',
    'UNIT_NAMES',
    # Production folder validation (HARDCODED)
    'validate_production_root',
    'validate_unit_folder',
    'validate_day_folder',
    'validate_powerpoint_slides',
    'validate_production_output',
    'has_valid_production',
    'get_production_issues',
    'production_folder_exists',
    'REQUIRED_SLIDE_COUNT',
    'MIN_FILE_SIZES',
]
