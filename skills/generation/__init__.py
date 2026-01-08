"""
Generation skills for the NCLEX pipeline.
"""

from .slide_builder import (
    SlideStructure, build_slide, build_section_intro,
    build_content_slide, allocate_content
)
from .content_expander import (
    expand_anchor, fit_to_body, expand_key_points
)
from .visual_pattern_matcher import (
    VisualType, identify_visual_opportunity,
    score_visual_fit, get_visual_type
)
from .text_condenser import (
    TextCondenser, CondenseResult,
    condense_text, condense_to_lines, remove_fillers
)
from .content_condenser import (
    ContentCondenser, ContentCondenseResult,
    condense_content, condense_body
)
from .content_structure_analyzer import (
    count_bullet_points, detect_list_patterns,
    identify_comparison_structure, detect_sequential_markers,
    analyze_information_density, detect_hierarchical_structure,
    suggest_visual_type, analyze_slide_content
)
from .layout_selector import (
    Layout, select_table_layout, select_flowchart_layout,
    select_decision_tree_layout, select_timeline_layout,
    select_hierarchy_layout, select_spectrum_layout,
    select_keydiff_layout, auto_select_layout,
    get_layout_description, get_constraints
)
from .visual_merger import (
    merge_visual_spec, format_visual_section,
    clear_body_for_visual, preserve_presenter_notes,
    clear_nclex_tip_for_visual, integrate_all_visuals,
    get_integration_summary, validate_integration,
    VALID_VISUAL_TYPES
)
from .ml_visual_recommender import (
    MLVisualRecommender, SlideFeatures, TrainingExample,
    extract_features, get_ml_recommendation,
    train_from_samples, ensemble_predict,
    initialize_with_patterns, generate_training_data_from_patterns
)
from .presenter_notes_generator import (
    generate_presenter_notes, validate_presenter_notes,
    count_words, estimate_duration
)

__all__ = [
    # Slide building
    'SlideStructure', 'build_slide', 'build_section_intro',
    'build_content_slide', 'allocate_content',
    # Content expansion
    'expand_anchor', 'fit_to_body', 'expand_key_points',
    # Visual matching
    'VisualType', 'identify_visual_opportunity',
    'score_visual_fit', 'get_visual_type',
    # Text condensation
    'TextCondenser', 'CondenseResult',
    'condense_text', 'condense_to_lines', 'remove_fillers',
    # Content condensation
    'ContentCondenser', 'ContentCondenseResult',
    'condense_content', 'condense_body',
    # Content structure analysis
    'count_bullet_points', 'detect_list_patterns',
    'identify_comparison_structure', 'detect_sequential_markers',
    'analyze_information_density', 'detect_hierarchical_structure',
    'suggest_visual_type', 'analyze_slide_content',
    # Layout selection (Step 9)
    'Layout', 'select_table_layout', 'select_flowchart_layout',
    'select_decision_tree_layout', 'select_timeline_layout',
    'select_hierarchy_layout', 'select_spectrum_layout',
    'select_keydiff_layout', 'auto_select_layout',
    'get_layout_description', 'get_constraints',
    # Visual merger (Step 10)
    'merge_visual_spec', 'format_visual_section',
    'clear_body_for_visual', 'preserve_presenter_notes',
    'clear_nclex_tip_for_visual', 'integrate_all_visuals',
    'get_integration_summary', 'validate_integration',
    'VALID_VISUAL_TYPES',
    # ML Visual Recommender (P3 Enhancement)
    'MLVisualRecommender', 'SlideFeatures', 'TrainingExample',
    'extract_features', 'get_ml_recommendation',
    'train_from_samples', 'ensemble_predict',
    'initialize_with_patterns', 'generate_training_data_from_patterns',
    # Presenter Notes Generator (R6)
    'generate_presenter_notes', 'validate_presenter_notes',
    'count_words', 'estimate_duration',
]
