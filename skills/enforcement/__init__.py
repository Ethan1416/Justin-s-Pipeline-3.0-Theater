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
from .english_standards_integrator import (
    get_standard_text,
    suggest_standards_for_activity,
    format_standards_citation,
    format_activity_standards_citation,
    integrate_standards_into_lesson_plan,
    integrate_standards_into_exit_tickets,
    generate_standards_summary,
    integrate_all_standards,
    format_lesson_plan_with_standards,
    MIN_STANDARDS_PER_LESSON,
    MAX_STANDARDS_PER_LESSON,
    CA_ELA_STANDARDS,
    ACTIVITY_STANDARDS_MAP
)
from .english_standards_validator import (
    is_valid_standard_code,
    validate_standard,
    validate_standards_count,
    validate_lesson_plan_citations,
    validate_exit_ticket_alignment,
    validate_activity_standards_reference,
    validate_lesson_standards,
    has_valid_standards,
    get_standards_issues,
    count_standards,
    standards_in_range,
    generate_validation_report as generate_standards_report,
    MIN_STANDARDS,
    MAX_STANDARDS,
    VALID_STANDARD_PATTERNS
)
from .scaffolding_generator import (
    generate_scaffolding_plan,
    generate_scaffolds_for_activity,
    validate_scaffolding_plan,
    has_valid_scaffolding,
    scaffolding_plan_to_dict,
    ScaffoldingPlan,
    Scaffold,
    SupportLevel,
    GRADUAL_RELEASE_PHASES,
    MIN_SCAFFOLDS_PER_LESSON,
    MAX_SCAFFOLDS_PER_LESSON
)
from .formative_activities_generator import (
    generate_formative_plan,
    generate_formative_activity,
    validate_formative_plan,
    has_valid_formatives,
    formative_plan_to_dict,
    FormativeAssessmentPlan,
    FormativeActivity,
    FormativeType,
    FeedbackMethod,
    MIN_FORMATIVE_CHECKS_PER_LESSON,
    MAX_FORMATIVE_CHECKS_PER_LESSON
)
from .blooms_taxonomy_integrator import (
    classify_objective,
    generate_bloom_objectives,
    generate_bloom_integration_plan,
    validate_bloom_integration,
    has_valid_bloom_integration,
    bloom_plan_to_dict,
    get_bloom_verbs_for_level,
    get_theater_activities_for_level,
    suggest_activity_for_objective,
    BloomIntegrationPlan,
    BloomObjective,
    BloomLevel,
    BLOOM_VERBS,
    BLOOM_DEFINITIONS,
    MIN_BLOOM_LEVELS_PER_LESSON
)
from .webbs_dok_integrator import (
    classify_activity_dok,
    generate_dok_activities,
    generate_dok_activity,
    generate_dok_integration_plan,
    validate_dok_integration,
    has_valid_dok_integration,
    dok_plan_to_dict,
    get_dok_keywords,
    get_theater_activities_for_dok,
    suggest_dok_level_for_time,
    DOKIntegrationPlan,
    DOKActivity,
    DOKLevel,
    DOK_DEFINITIONS,
    MIN_DOK_LEVELS_PER_LESSON
)
from .instruction_integrator import (
    generate_integrated_lesson,
    generate_lecture_component,
    generate_reading_activity,
    generate_romeo_juliet_unit_plan,
    build_phase_sequence,
    validate_integrated_lesson,
    has_valid_integration,
    integrated_lesson_to_dict,
    IntegratedLesson,
    LectureComponent,
    ReadingActivity,
    InstructionalPhase,
    ActivityType,
    ROMEO_AND_JULIET_STRUCTURE,
    MIN_LECTURE_DURATION,
    MAX_LECTURE_DURATION,
    DEFAULT_LECTURE_DURATION
)
from .warmup_card_generator import (
    generate_warmup_card,
    validate_warmup_card,
    warmup_card_to_markdown as generate_warmup_card_markdown,
    generate_warmup_cards_for_unit as generate_all_warmup_cards,
    WARMUP_TYPES as WARMUP_EXERCISES,
    SCENE_WARMUP_MAP as SCENE_WARMUP_MAPPING,
    WarmupCard
)
from .activity_instructions_generator import (
    generate_activity_instructions,
    validate_activity_instructions,
    activity_instructions_to_markdown as generate_activity_instructions_markdown,
    generate_activity_instructions_for_unit as generate_all_activity_instructions,
    ACTIVITY_TEMPLATES,
    ActivityInstructions,
    ActivityType
)
from .vocabulary_cards_generator import (
    generate_vocabulary_cards,
    validate_vocabulary_set as validate_vocabulary_cards,
    vocabulary_set_to_markdown as generate_vocabulary_cards_markdown,
    ROMEO_JULIET_VOCABULARY as VOCABULARY_DATABASE,
    VocabularyCard,
    VocabularySet
)
from .rubric_generator import (
    generate_rubric,
    validate_rubric,
    generate_rubric_markdown,
    generate_all_rubrics,
    RUBRIC_TEMPLATES,
    ACTIVITY_TO_RUBRIC,
    Rubric,
    RubricCriterion
)
from .reading_guide_generator import (
    generate_reading_guide,
    validate_reading_guide,
    generate_reading_guide_markdown,
    generate_all_reading_guides,
    READING_GUIDE_DATABASE,
    READING_TYPES,
    ReadingGuide,
    AnnotationPrompt
)
from .differentiation_generator import (
    generate_differentiation_sheet,
    validate_differentiation_sheet,
    generate_differentiation_markdown,
    generate_all_differentiation_sheets,
    DIFFERENTIATION_TEMPLATES,
    DAY_ACTIVITY_TYPES,
    DAY_VOCABULARY,
    DifferentiationSheet
)
from .answer_key_generator import (
    generate_answer_key,
    validate_answer_key,
    generate_answer_key_markdown,
    generate_all_answer_keys,
    EXIT_TICKET_ANSWERS,
    HANDOUT_ANSWER_TEMPLATES,
    AnswerKeyEntry
)
from .materials_checklist_generator import (
    generate_materials_checklist,
    validate_materials_checklist,
    generate_materials_checklist_markdown,
    generate_all_materials_checklists,
    ACTIVITY_MATERIALS,
    DAY_ACTIVITIES,
    STANDARD_DAILY_MATERIALS,
    MaterialsChecklist
)
from .unit_components_generator import (
    generate_unit_calendar,
    generate_sub_folder,
    generate_parent_letter,
    generate_character_tracker,
    generate_standards_alignment,
    generate_assessment_tracker,
    generate_all_unit_components,
    generate_unit_calendar_markdown,
    ROMEO_JULIET_CALENDAR,
    CHARACTERS,
    STANDARDS_ALIGNMENT
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
    # English standards integration (HARDCODED)
    'get_standard_text',
    'suggest_standards_for_activity',
    'format_standards_citation',
    'format_activity_standards_citation',
    'integrate_standards_into_lesson_plan',
    'integrate_standards_into_exit_tickets',
    'generate_standards_summary',
    'integrate_all_standards',
    'format_lesson_plan_with_standards',
    'MIN_STANDARDS_PER_LESSON',
    'MAX_STANDARDS_PER_LESSON',
    'CA_ELA_STANDARDS',
    'ACTIVITY_STANDARDS_MAP',
    # English standards validation (HARDCODED)
    'is_valid_standard_code',
    'validate_standard',
    'validate_standards_count',
    'validate_lesson_plan_citations',
    'validate_exit_ticket_alignment',
    'validate_activity_standards_reference',
    'validate_lesson_standards',
    'has_valid_standards',
    'get_standards_issues',
    'count_standards',
    'standards_in_range',
    'generate_standards_report',
    'MIN_STANDARDS',
    'MAX_STANDARDS',
    'VALID_STANDARD_PATTERNS',
    # Scaffolding generation (HARDCODED)
    'generate_scaffolding_plan',
    'generate_scaffolds_for_activity',
    'validate_scaffolding_plan',
    'has_valid_scaffolding',
    'scaffolding_plan_to_dict',
    'ScaffoldingPlan',
    'Scaffold',
    'SupportLevel',
    'GRADUAL_RELEASE_PHASES',
    'MIN_SCAFFOLDS_PER_LESSON',
    'MAX_SCAFFOLDS_PER_LESSON',
    # Formative activities (HARDCODED)
    'generate_formative_plan',
    'generate_formative_activity',
    'validate_formative_plan',
    'has_valid_formatives',
    'formative_plan_to_dict',
    'FormativeAssessmentPlan',
    'FormativeActivity',
    'FormativeType',
    'FeedbackMethod',
    'MIN_FORMATIVE_CHECKS_PER_LESSON',
    'MAX_FORMATIVE_CHECKS_PER_LESSON',
    # Bloom's Taxonomy (HARDCODED)
    'classify_objective',
    'generate_bloom_objectives',
    'generate_bloom_integration_plan',
    'validate_bloom_integration',
    'has_valid_bloom_integration',
    'bloom_plan_to_dict',
    'get_bloom_verbs_for_level',
    'get_theater_activities_for_level',
    'suggest_activity_for_objective',
    'BloomIntegrationPlan',
    'BloomObjective',
    'BloomLevel',
    'BLOOM_VERBS',
    'BLOOM_DEFINITIONS',
    'MIN_BLOOM_LEVELS_PER_LESSON',
    # Webb's DOK (HARDCODED)
    'classify_activity_dok',
    'generate_dok_activities',
    'generate_dok_activity',
    'generate_dok_integration_plan',
    'validate_dok_integration',
    'has_valid_dok_integration',
    'dok_plan_to_dict',
    'get_dok_keywords',
    'get_theater_activities_for_dok',
    'suggest_dok_level_for_time',
    'DOKIntegrationPlan',
    'DOKActivity',
    'DOKLevel',
    'DOK_DEFINITIONS',
    'MIN_DOK_LEVELS_PER_LESSON',
    # Instruction integration (HARDCODED)
    'generate_integrated_lesson',
    'generate_lecture_component',
    'generate_reading_activity',
    'generate_romeo_juliet_unit_plan',
    'build_phase_sequence',
    'validate_integrated_lesson',
    'has_valid_integration',
    'integrated_lesson_to_dict',
    'IntegratedLesson',
    'LectureComponent',
    'ReadingActivity',
    'InstructionalPhase',
    'ActivityType',
    'ROMEO_AND_JULIET_STRUCTURE',
    'MIN_LECTURE_DURATION',
    'MAX_LECTURE_DURATION',
    'DEFAULT_LECTURE_DURATION',
    # Warm-up card generation (HARDCODED)
    'generate_warmup_card',
    'validate_warmup_card',
    'generate_warmup_card_markdown',
    'generate_all_warmup_cards',
    'WARMUP_EXERCISES',
    'SCENE_WARMUP_MAPPING',
    'WarmupCard',
    # Activity instructions generation (HARDCODED)
    'generate_activity_instructions',
    'validate_activity_instructions',
    'generate_activity_instructions_markdown',
    'generate_all_activity_instructions',
    'ACTIVITY_TEMPLATES',
    'DAY_ACTIVITY_MAPPING',
    'ActivityInstructions',
    # Vocabulary cards generation (HARDCODED)
    'generate_vocabulary_cards',
    'validate_vocabulary_cards',
    'generate_vocabulary_cards_markdown',
    'generate_vocabulary_for_day',
    'generate_all_vocabulary_cards',
    'VOCABULARY_DATABASE',
    'DAY_VOCABULARY_MAPPING',
    'VocabularyCard',
    # Rubric generation (HARDCODED)
    'generate_rubric',
    'validate_rubric',
    'generate_rubric_markdown',
    'generate_all_rubrics',
    'RUBRIC_TEMPLATES',
    'ACTIVITY_TO_RUBRIC',
    'Rubric',
    'RubricCriterion',
    # Reading guide generation (HARDCODED)
    'generate_reading_guide',
    'validate_reading_guide',
    'generate_reading_guide_markdown',
    'generate_all_reading_guides',
    'READING_GUIDE_DATABASE',
    'READING_TYPES',
    'ReadingGuide',
    'AnnotationPrompt',
    # Differentiation sheet generation (HARDCODED)
    'generate_differentiation_sheet',
    'validate_differentiation_sheet',
    'generate_differentiation_markdown',
    'generate_all_differentiation_sheets',
    'DIFFERENTIATION_TEMPLATES',
    'DAY_ACTIVITY_TYPES',
    'DAY_VOCABULARY',
    'DifferentiationSheet',
    # Answer key generation (HARDCODED)
    'generate_answer_key',
    'validate_answer_key',
    'generate_answer_key_markdown',
    'generate_all_answer_keys',
    'EXIT_TICKET_ANSWERS',
    'HANDOUT_ANSWER_TEMPLATES',
    'AnswerKeyEntry',
    # Materials checklist generation (HARDCODED)
    'generate_materials_checklist',
    'validate_materials_checklist',
    'generate_materials_checklist_markdown',
    'generate_all_materials_checklists',
    'ACTIVITY_MATERIALS',
    'DAY_ACTIVITIES',
    'STANDARD_DAILY_MATERIALS',
    'MaterialsChecklist',
    # Unit-level components generation (HARDCODED)
    'generate_unit_calendar',
    'generate_sub_folder',
    'generate_parent_letter',
    'generate_character_tracker',
    'generate_standards_alignment',
    'generate_assessment_tracker',
    'generate_all_unit_components',
    'generate_unit_calendar_markdown',
    'ROMEO_JULIET_CALENDAR',
    'CHARACTERS',
    'STANDARDS_ALIGNMENT',
]
