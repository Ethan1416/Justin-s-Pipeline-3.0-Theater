"""
Step 10 Visual Integration Tests
Tests for visual_merger.py skill - visual specification integration.
Also includes tests for marker_inserter.py - visual marker management.

Run: python -m pytest tests/test_step10_integration.py -v
"""

import sys
import unittest
import copy
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from skills.generation.visual_merger import (
    merge_visual_spec,
    format_visual_section,
    clear_body_for_visual,
    preserve_presenter_notes,
    clear_nclex_tip_for_visual,
    integrate_all_visuals,
    get_integration_summary,
    validate_integration,
    VALID_VISUAL_TYPES as MERGER_VISUAL_TYPES
)

from skills.utilities.marker_inserter import (
    add_visual_marker,
    validate_all_markers,
    count_markers,
    fix_missing_markers,
    validate_marker_format,
    get_visual_type_counts,
    get_slides_by_marker_type,
    VALID_VISUAL_TYPES
)


class TestAddVisualMarker(unittest.TestCase):
    """Tests for add_visual_marker function."""

    def test_add_visual_yes_marker_table(self):
        """Adding Visual: Yes - TABLE marker works correctly."""
        slide = {'slide_number': 1, 'header': 'Test'}
        result = add_visual_marker(slide, has_visual=True, visual_type="TABLE")
        self.assertEqual(result['visual_marker'], "Visual: Yes - TABLE")

    def test_add_visual_yes_marker_flowchart(self):
        """Adding Visual: Yes - FLOWCHART marker works correctly."""
        slide = {'slide_number': 2, 'header': 'Process'}
        result = add_visual_marker(slide, has_visual=True, visual_type="FLOWCHART")
        self.assertEqual(result['visual_marker'], "Visual: Yes - FLOWCHART")

    def test_add_visual_yes_marker_decision_tree(self):
        """Adding Visual: Yes - DECISION_TREE marker works correctly."""
        slide = {'slide_number': 3, 'header': 'Decision'}
        result = add_visual_marker(slide, has_visual=True, visual_type="DECISION_TREE")
        self.assertEqual(result['visual_marker'], "Visual: Yes - DECISION_TREE")

    def test_add_visual_yes_marker_timeline(self):
        """Adding Visual: Yes - TIMELINE marker works correctly."""
        slide = {'slide_number': 4, 'header': 'History'}
        result = add_visual_marker(slide, has_visual=True, visual_type="TIMELINE")
        self.assertEqual(result['visual_marker'], "Visual: Yes - TIMELINE")

    def test_add_visual_yes_marker_hierarchy(self):
        """Adding Visual: Yes - HIERARCHY marker works correctly."""
        slide = {'slide_number': 5, 'header': 'Organization'}
        result = add_visual_marker(slide, has_visual=True, visual_type="HIERARCHY")
        self.assertEqual(result['visual_marker'], "Visual: Yes - HIERARCHY")

    def test_add_visual_yes_marker_spectrum(self):
        """Adding Visual: Yes - SPECTRUM marker works correctly."""
        slide = {'slide_number': 6, 'header': 'Range'}
        result = add_visual_marker(slide, has_visual=True, visual_type="SPECTRUM")
        self.assertEqual(result['visual_marker'], "Visual: Yes - SPECTRUM")

    def test_add_visual_yes_marker_key_differentiators(self):
        """Adding Visual: Yes - KEY_DIFFERENTIATORS marker works correctly."""
        slide = {'slide_number': 7, 'header': 'Compare'}
        result = add_visual_marker(slide, has_visual=True, visual_type="KEY_DIFFERENTIATORS")
        self.assertEqual(result['visual_marker'], "Visual: Yes - KEY_DIFFERENTIATORS")

    def test_add_visual_no_marker(self):
        """Adding Visual: No marker works correctly."""
        slide = {'slide_number': 8, 'header': 'Content Only'}
        result = add_visual_marker(slide, has_visual=False)
        self.assertEqual(result['visual_marker'], "Visual: No")

    def test_visual_type_case_insensitive(self):
        """Visual type is case-insensitive and normalized to uppercase."""
        slide = {'slide_number': 1, 'header': 'Test'}
        result = add_visual_marker(slide, has_visual=True, visual_type="table")
        self.assertEqual(result['visual_marker'], "Visual: Yes - TABLE")

    def test_original_slide_not_modified(self):
        """Original slide dictionary is not modified."""
        slide = {'slide_number': 1, 'header': 'Test'}
        result = add_visual_marker(slide, has_visual=True, visual_type="TABLE")
        self.assertNotIn('visual_marker', slide)
        self.assertIn('visual_marker', result)

    def test_existing_fields_preserved(self):
        """Existing slide fields are preserved."""
        slide = {
            'slide_number': 1,
            'header': 'Test Header',
            'body': 'Test body content',
            'nclex_tip': 'Test tip',
            'presenter_notes': 'Test notes'
        }
        result = add_visual_marker(slide, has_visual=True, visual_type="TABLE")
        self.assertEqual(result['header'], 'Test Header')
        self.assertEqual(result['body'], 'Test body content')
        self.assertEqual(result['nclex_tip'], 'Test tip')
        self.assertEqual(result['presenter_notes'], 'Test notes')

    def test_raises_on_missing_visual_type(self):
        """Raises ValueError if has_visual is True but visual_type is None."""
        slide = {'slide_number': 1}
        with self.assertRaises(ValueError) as context:
            add_visual_marker(slide, has_visual=True, visual_type=None)
        self.assertIn("visual_type is required", str(context.exception))

    def test_raises_on_invalid_visual_type(self):
        """Raises ValueError for invalid visual type."""
        slide = {'slide_number': 1}
        with self.assertRaises(ValueError) as context:
            add_visual_marker(slide, has_visual=True, visual_type="INVALID_TYPE")
        self.assertIn("Invalid visual_type", str(context.exception))


class TestValidateMarkerFormat(unittest.TestCase):
    """Tests for validate_marker_format function."""

    def test_valid_visual_yes_table(self):
        """Visual: Yes - TABLE is valid."""
        is_valid, error = validate_marker_format("Visual: Yes - TABLE")
        self.assertTrue(is_valid)
        self.assertEqual(error, "")

    def test_valid_visual_yes_all_types(self):
        """All valid visual types are accepted."""
        for visual_type in VALID_VISUAL_TYPES:
            marker = f"Visual: Yes - {visual_type}"
            is_valid, error = validate_marker_format(marker)
            self.assertTrue(is_valid, f"Failed for type: {visual_type}")
            self.assertEqual(error, "")

    def test_valid_visual_no(self):
        """Visual: No is valid."""
        is_valid, error = validate_marker_format("Visual: No")
        self.assertTrue(is_valid)
        self.assertEqual(error, "")

    def test_invalid_empty_marker(self):
        """Empty marker is invalid."""
        is_valid, error = validate_marker_format("")
        self.assertFalse(is_valid)
        self.assertIn("empty", error.lower())

    def test_invalid_none_marker(self):
        """None marker is invalid."""
        is_valid, error = validate_marker_format(None)
        self.assertFalse(is_valid)
        self.assertIn("empty", error.lower())

    def test_invalid_visual_type(self):
        """Invalid visual type is rejected."""
        is_valid, error = validate_marker_format("Visual: Yes - INVALID_TYPE")
        self.assertFalse(is_valid)
        self.assertIn("Invalid visual type", error)

    def test_invalid_format_no_colon(self):
        """Marker without colon is invalid."""
        is_valid, error = validate_marker_format("Visual Yes TABLE")
        self.assertFalse(is_valid)
        self.assertIn("Invalid marker format", error)

    def test_invalid_format_random_text(self):
        """Random text is invalid marker."""
        is_valid, error = validate_marker_format("Some random text")
        self.assertFalse(is_valid)
        self.assertIn("Invalid marker format", error)

    def test_whitespace_trimmed(self):
        """Whitespace is trimmed before validation."""
        is_valid, error = validate_marker_format("  Visual: No  ")
        self.assertTrue(is_valid)
        self.assertEqual(error, "")

    def test_case_sensitive_visual_type(self):
        """Visual type must be uppercase."""
        # Lowercase visual type should be invalid (exact format match)
        is_valid, error = validate_marker_format("Visual: Yes - table")
        self.assertFalse(is_valid)


class TestValidateAllMarkers(unittest.TestCase):
    """Tests for validate_all_markers function."""

    def test_all_valid_markers(self):
        """Blueprint with all valid markers returns valid."""
        blueprint = {
            'slides': [
                {'slide_number': 1, 'visual_marker': 'Visual: Yes - TABLE'},
                {'slide_number': 2, 'visual_marker': 'Visual: No'},
                {'slide_number': 3, 'visual_marker': 'Visual: Yes - FLOWCHART'},
            ]
        }
        result = validate_all_markers(blueprint)
        self.assertTrue(result['valid'])
        self.assertEqual(result['total_slides'], 3)
        self.assertEqual(result['slides_with_marker'], 3)
        self.assertEqual(result['slides_missing_marker'], [])
        self.assertEqual(result['invalid_markers'], [])

    def test_missing_markers_detected(self):
        """Missing markers are detected."""
        blueprint = {
            'slides': [
                {'slide_number': 1, 'visual_marker': 'Visual: Yes - TABLE'},
                {'slide_number': 2},  # Missing marker
                {'slide_number': 3, 'visual_marker': 'Visual: No'},
                {'slide_number': 4},  # Missing marker
            ]
        }
        result = validate_all_markers(blueprint)
        self.assertFalse(result['valid'])
        self.assertEqual(result['slides_missing_marker'], [2, 4])

    def test_invalid_markers_detected(self):
        """Invalid markers are detected."""
        blueprint = {
            'slides': [
                {'slide_number': 1, 'visual_marker': 'Visual: Yes - TABLE'},
                {'slide_number': 2, 'visual_marker': 'Invalid marker'},
                {'slide_number': 3, 'visual_marker': 'Visual: Yes - INVALID_TYPE'},
            ]
        }
        result = validate_all_markers(blueprint)
        self.assertFalse(result['valid'])
        self.assertEqual(len(result['invalid_markers']), 2)

    def test_step7_blueprint_structure(self):
        """Handles step7_blueprint nested structure."""
        blueprint = {
            'step7_blueprint': {
                'slides': [
                    {'slide_number': 3, 'visual_marker': 'Visual: Yes - TABLE'},
                    {'slide_number': 4, 'visual_marker': 'Visual: No'},
                ]
            }
        }
        result = validate_all_markers(blueprint)
        self.assertTrue(result['valid'])
        self.assertEqual(result['total_slides'], 2)

    def test_empty_blueprint(self):
        """Empty blueprint returns valid with zero slides."""
        blueprint = {'slides': []}
        result = validate_all_markers(blueprint)
        self.assertTrue(result['valid'])
        self.assertEqual(result['total_slides'], 0)

    def test_no_slides_key(self):
        """Blueprint without slides key returns valid with zero slides."""
        blueprint = {'metadata': {'version': '1.0'}}
        result = validate_all_markers(blueprint)
        self.assertTrue(result['valid'])
        self.assertEqual(result['total_slides'], 0)


class TestCountMarkers(unittest.TestCase):
    """Tests for count_markers function."""

    def test_count_all_types(self):
        """Counts all marker types correctly."""
        blueprint = {
            'slides': [
                {'slide_number': 1, 'visual_marker': 'Visual: Yes - TABLE'},
                {'slide_number': 2, 'visual_marker': 'Visual: Yes - FLOWCHART'},
                {'slide_number': 3, 'visual_marker': 'Visual: No'},
                {'slide_number': 4, 'visual_marker': 'Visual: No'},
                {'slide_number': 5},  # Missing
                {'slide_number': 6, 'visual_marker': 'Invalid'},  # Invalid
            ]
        }
        result = count_markers(blueprint)
        self.assertEqual(result['yes'], 2)
        self.assertEqual(result['no'], 2)
        self.assertEqual(result['missing'], 1)
        self.assertEqual(result['invalid'], 1)
        self.assertEqual(result['total'], 6)

    def test_count_empty_blueprint(self):
        """Empty blueprint returns zero counts."""
        blueprint = {'slides': []}
        result = count_markers(blueprint)
        self.assertEqual(result['yes'], 0)
        self.assertEqual(result['no'], 0)
        self.assertEqual(result['missing'], 0)
        self.assertEqual(result['invalid'], 0)
        self.assertEqual(result['total'], 0)

    def test_count_all_yes(self):
        """Blueprint with all yes markers counted correctly."""
        blueprint = {
            'slides': [
                {'slide_number': i, 'visual_marker': 'Visual: Yes - TABLE'}
                for i in range(1, 6)
            ]
        }
        result = count_markers(blueprint)
        self.assertEqual(result['yes'], 5)
        self.assertEqual(result['no'], 0)

    def test_count_all_no(self):
        """Blueprint with all no markers counted correctly."""
        blueprint = {
            'slides': [
                {'slide_number': i, 'visual_marker': 'Visual: No'}
                for i in range(1, 6)
            ]
        }
        result = count_markers(blueprint)
        self.assertEqual(result['yes'], 0)
        self.assertEqual(result['no'], 5)


class TestFixMissingMarkers(unittest.TestCase):
    """Tests for fix_missing_markers function."""

    def test_fix_missing_with_default(self):
        """Missing markers are filled with default 'Visual: No'."""
        blueprint = {
            'slides': [
                {'slide_number': 1, 'visual_marker': 'Visual: Yes - TABLE'},
                {'slide_number': 2},  # Missing
                {'slide_number': 3, 'visual_marker': 'Visual: No'},
                {'slide_number': 4},  # Missing
            ]
        }
        result = fix_missing_markers(blueprint)

        # Verify all slides now have markers
        validation = validate_all_markers(result)
        self.assertEqual(validation['slides_missing_marker'], [])

        # Verify the fixed markers are Visual: No
        self.assertEqual(result['slides'][1]['visual_marker'], 'Visual: No')
        self.assertEqual(result['slides'][3]['visual_marker'], 'Visual: No')

    def test_fix_with_custom_default(self):
        """Custom default marker is applied."""
        blueprint = {
            'slides': [
                {'slide_number': 1},  # Missing
            ]
        }
        result = fix_missing_markers(blueprint, default_marker="Visual: Yes - TABLE")
        self.assertEqual(result['slides'][0]['visual_marker'], 'Visual: Yes - TABLE')

    def test_original_not_modified(self):
        """Original blueprint is not modified."""
        blueprint = {
            'slides': [
                {'slide_number': 1},  # Missing
            ]
        }
        result = fix_missing_markers(blueprint)
        self.assertNotIn('visual_marker', blueprint['slides'][0])
        self.assertIn('visual_marker', result['slides'][0])

    def test_existing_markers_preserved(self):
        """Existing valid markers are not changed."""
        blueprint = {
            'slides': [
                {'slide_number': 1, 'visual_marker': 'Visual: Yes - TABLE'},
                {'slide_number': 2},  # Missing
            ]
        }
        result = fix_missing_markers(blueprint)
        self.assertEqual(result['slides'][0]['visual_marker'], 'Visual: Yes - TABLE')

    def test_invalid_default_raises_error(self):
        """Invalid default marker raises ValueError."""
        blueprint = {'slides': [{'slide_number': 1}]}
        with self.assertRaises(ValueError):
            fix_missing_markers(blueprint, default_marker="Invalid marker")

    def test_fix_step7_blueprint_structure(self):
        """Fixes nested step7_blueprint structure."""
        blueprint = {
            'step7_blueprint': {
                'slides': [
                    {'slide_number': 3},  # Missing
                    {'slide_number': 4, 'visual_marker': 'Visual: No'},
                ]
            }
        }
        result = fix_missing_markers(blueprint)
        self.assertEqual(
            result['step7_blueprint']['slides'][0]['visual_marker'],
            'Visual: No'
        )


class TestGetVisualTypeCounts(unittest.TestCase):
    """Tests for get_visual_type_counts function."""

    def test_count_visual_types(self):
        """Visual types are counted correctly."""
        blueprint = {
            'slides': [
                {'slide_number': 1, 'visual_marker': 'Visual: Yes - TABLE'},
                {'slide_number': 2, 'visual_marker': 'Visual: Yes - TABLE'},
                {'slide_number': 3, 'visual_marker': 'Visual: Yes - FLOWCHART'},
                {'slide_number': 4, 'visual_marker': 'Visual: No'},
            ]
        }
        result = get_visual_type_counts(blueprint)
        self.assertEqual(result['TABLE'], 2)
        self.assertEqual(result['FLOWCHART'], 1)
        self.assertEqual(result['DECISION_TREE'], 0)

    def test_all_types_initialized(self):
        """All valid types are in result, even with zero count."""
        blueprint = {'slides': []}
        result = get_visual_type_counts(blueprint)
        for visual_type in VALID_VISUAL_TYPES:
            self.assertIn(visual_type, result)
            self.assertEqual(result[visual_type], 0)


class TestGetSlidesByMarkerType(unittest.TestCase):
    """Tests for get_slides_by_marker_type function."""

    def test_group_slides_by_type(self):
        """Slides are grouped correctly by marker type."""
        blueprint = {
            'slides': [
                {'slide_number': 1, 'visual_marker': 'Visual: Yes - TABLE'},
                {'slide_number': 2, 'visual_marker': 'Visual: No'},
                {'slide_number': 3},  # Missing
                {'slide_number': 4, 'visual_marker': 'Invalid'},  # Invalid
                {'slide_number': 5, 'visual_marker': 'Visual: Yes - FLOWCHART'},
            ]
        }
        result = get_slides_by_marker_type(blueprint)
        self.assertEqual(result['visual_yes'], [1, 5])
        self.assertEqual(result['visual_no'], [2])
        self.assertEqual(result['missing'], [3])
        self.assertEqual(result['invalid'], [4])


class TestStep10Integration(unittest.TestCase):
    """Integration tests for Step 10 Visual Integration workflow."""

    def test_complete_integration_workflow(self):
        """Complete Step 10 workflow with sample input."""
        # Sample input similar to sample_integration_input.json
        blueprint = {
            'metadata': {
                'domain': 'Pharmacology',
                'section': 'Cardiovascular Medications'
            },
            'step7_blueprint': {
                'slides': [
                    {
                        'slide_number': 3,
                        'slide_type': 'Content',
                        'header': 'ACE Inhibitors vs ARBs',
                        'body': '* ACE-I: Block conversion\n* ARBs: Block receptor',
                        'nclex_tip': 'NCLEX often compares ACE-I and ARB side effects',
                        'presenter_notes': 'Let us compare these two important drug classes.',
                        'visual_marker': None
                    },
                    {
                        'slide_number': 4,
                        'slide_type': 'Content',
                        'header': 'Beta Blocker Classes',
                        'body': '* Cardioselective: Metoprolol\n* Non-selective: Propranolol',
                        'nclex_tip': 'Know which beta blockers are cardioselective',
                        'presenter_notes': 'Beta blockers are classified by selectivity.',
                        'visual_marker': None
                    }
                ]
            },
            'step9_visual_specs': [
                {'slide_number': 3, 'visual_type': 'TABLE'},
                {'slide_number': 4, 'visual_type': 'HIERARCHY'}
            ]
        }

        # Step 1: Add visual markers based on step9_visual_specs
        visual_spec_slides = {
            spec['slide_number']: spec['visual_type']
            for spec in blueprint['step9_visual_specs']
        }

        for slide in blueprint['step7_blueprint']['slides']:
            slide_num = slide['slide_number']
            if slide_num in visual_spec_slides:
                updated_slide = add_visual_marker(
                    slide,
                    has_visual=True,
                    visual_type=visual_spec_slides[slide_num]
                )
                slide['visual_marker'] = updated_slide['visual_marker']
            else:
                updated_slide = add_visual_marker(slide, has_visual=False)
                slide['visual_marker'] = updated_slide['visual_marker']

        # Step 2: Validate all markers
        validation = validate_all_markers(blueprint)
        self.assertTrue(validation['valid'])
        self.assertEqual(validation['slides_missing_marker'], [])

        # Step 3: Count markers
        counts = count_markers(blueprint)
        self.assertEqual(counts['yes'], 2)
        self.assertEqual(counts['no'], 0)
        self.assertEqual(counts['missing'], 0)
        self.assertEqual(counts['total'], 2)

        # Step 4: Verify visual type counts
        type_counts = get_visual_type_counts(blueprint)
        self.assertEqual(type_counts['TABLE'], 1)
        self.assertEqual(type_counts['HIERARCHY'], 1)

    def test_fix_and_validate_workflow(self):
        """Workflow: fix missing markers then validate."""
        # Blueprint with missing markers
        blueprint = {
            'slides': [
                {'slide_number': 1, 'header': 'Intro'},
                {'slide_number': 2, 'header': 'Content', 'visual_marker': 'Visual: Yes - TABLE'},
                {'slide_number': 3, 'header': 'More Content'},
                {'slide_number': 4, 'header': 'Visual', 'visual_marker': 'Visual: Yes - FLOWCHART'},
                {'slide_number': 5, 'header': 'Conclusion'},
            ]
        }

        # Initial validation should fail
        initial_validation = validate_all_markers(blueprint)
        self.assertFalse(initial_validation['valid'])
        self.assertEqual(len(initial_validation['slides_missing_marker']), 3)

        # Fix missing markers
        fixed_blueprint = fix_missing_markers(blueprint)

        # Final validation should pass
        final_validation = validate_all_markers(fixed_blueprint)
        self.assertTrue(final_validation['valid'])
        self.assertEqual(final_validation['slides_missing_marker'], [])
        self.assertEqual(final_validation['slides_with_marker'], 5)

    def test_marker_counts_match_validation(self):
        """Marker counts should be consistent with validation results."""
        blueprint = {
            'slides': [
                {'slide_number': 1, 'visual_marker': 'Visual: Yes - TABLE'},
                {'slide_number': 2, 'visual_marker': 'Visual: No'},
                {'slide_number': 3},  # Missing
            ]
        }

        validation = validate_all_markers(blueprint)
        counts = count_markers(blueprint)

        # slides_with_marker should equal yes + no (valid markers)
        self.assertEqual(
            validation['slides_with_marker'],
            counts['yes'] + counts['no']
        )

        # Missing count should match
        self.assertEqual(
            len(validation['slides_missing_marker']),
            counts['missing']
        )


class TestEdgeCases(unittest.TestCase):
    """Tests for edge cases and boundary conditions."""

    def test_slide_number_from_index(self):
        """Uses index+1 when slide_number is missing."""
        blueprint = {
            'slides': [
                {'header': 'Slide without number'},  # Missing
            ]
        }
        validation = validate_all_markers(blueprint)
        # Should use index+1 (which is 1) as slide number
        self.assertIn(1, validation['slides_missing_marker'])

    def test_deeply_nested_blueprint(self):
        """Handles integrated_blueprint structure."""
        blueprint = {
            'integrated_blueprint': {
                'slides': [
                    {'slide_number': 1, 'visual_marker': 'Visual: No'},
                ]
            }
        }
        validation = validate_all_markers(blueprint)
        self.assertTrue(validation['valid'])
        self.assertEqual(validation['total_slides'], 1)

    def test_marker_with_extra_spaces(self):
        """Marker format validation handles extra spaces flexibly."""
        # The regex uses \s* which allows flexible spacing
        # This is intentional for robustness when parsing various inputs
        is_valid, _ = validate_marker_format("Visual:   Yes   -   TABLE")
        self.assertTrue(is_valid)  # Flexible spacing is allowed


class TestAllVisualTypes(unittest.TestCase):
    """Tests ensuring all 7 visual types work correctly."""

    def test_all_visual_types_valid(self):
        """All 7 visual types are valid for markers."""
        expected_types = [
            "TABLE",
            "FLOWCHART",
            "DECISION_TREE",
            "TIMELINE",
            "HIERARCHY",
            "SPECTRUM",
            "KEY_DIFFERENTIATORS"
        ]
        self.assertEqual(set(VALID_VISUAL_TYPES), set(expected_types))

    def test_add_marker_all_types(self):
        """Can add marker for all visual types."""
        for visual_type in VALID_VISUAL_TYPES:
            slide = {'slide_number': 1}
            result = add_visual_marker(slide, has_visual=True, visual_type=visual_type)
            expected_marker = f"Visual: Yes - {visual_type}"
            self.assertEqual(result['visual_marker'], expected_marker)

    def test_validate_all_types(self):
        """Can validate markers for all visual types."""
        for visual_type in VALID_VISUAL_TYPES:
            marker = f"Visual: Yes - {visual_type}"
            is_valid, error = validate_marker_format(marker)
            self.assertTrue(is_valid, f"Type {visual_type} should be valid")
            self.assertEqual(error, "")


# =============================================================================
# Visual Merger Tests (visual_merger.py)
# =============================================================================


class TestMergeVisualSpec(unittest.TestCase):
    """Tests for merge_visual_spec function."""

    def setUp(self):
        """Set up test fixtures."""
        self.sample_slide = {
            "slide_number": 3,
            "slide_type": "Content",
            "header": "ACE Inhibitors vs ARBs",
            "body": "* ACE-I: Block conversion\n* ARBs: Block receptor\n* ACE-I: Cough side effect",
            "nclex_tip": "NCLEX often compares ACE-I and ARB side effects",
            "presenter_notes": "[PAUSE] Let's compare these two important drug classes. [EMPHASIS: ACE inhibitors] work by blocking the enzyme.",
            "visual_marker": None
        }

        self.sample_visual_spec = {
            "slide_number": 3,
            "visual_type": "TABLE",
            "layout": "B",
            "specification": {
                "title": "ACE Inhibitors vs ARBs Comparison",
                "columns": ["Feature", "ACE Inhibitors", "ARBs"],
                "rows": [
                    ["Mechanism", "Block ACE enzyme", "Block AT1 receptor"],
                    ["Cough", "Yes (10%)", "No"]
                ],
                "colors": {
                    "header_bg": "#1a5276",
                    "row_alt": "#d4e6f1"
                }
            }
        }

    def test_merge_visual_spec_adds_visual_marker(self):
        """Visual marker is added with correct format."""
        result = merge_visual_spec(self.sample_slide, self.sample_visual_spec)
        self.assertEqual(result["visual_marker"], "Visual: Yes - TABLE")

    def test_merge_visual_spec_clears_body(self):
        """Body is replaced with '[See Visual]'."""
        result = merge_visual_spec(self.sample_slide, self.sample_visual_spec)
        self.assertEqual(result["body"], "[See Visual]")

    def test_merge_visual_spec_clears_nclex_tip(self):
        """NCLEX tip is set to 'None'."""
        result = merge_visual_spec(self.sample_slide, self.sample_visual_spec)
        self.assertEqual(result["nclex_tip"], "None")

    def test_merge_visual_spec_preserves_presenter_notes(self):
        """Presenter notes are preserved unchanged."""
        original_notes = self.sample_slide["presenter_notes"]
        result = merge_visual_spec(self.sample_slide, self.sample_visual_spec)
        self.assertEqual(result["presenter_notes"], original_notes)
        self.assertIn("[PAUSE]", result["presenter_notes"])
        self.assertIn("[EMPHASIS:", result["presenter_notes"])

    def test_merge_visual_spec_adds_visual_specification(self):
        """Visual specification section is added."""
        result = merge_visual_spec(self.sample_slide, self.sample_visual_spec)
        self.assertIn("visual_specification", result)
        self.assertEqual(result["visual_specification"]["type"], "TABLE")
        self.assertEqual(result["visual_specification"]["layout"], "B")

    def test_merge_visual_spec_does_not_modify_original(self):
        """Original slide is not modified."""
        original_body = self.sample_slide["body"]
        merge_visual_spec(self.sample_slide, self.sample_visual_spec)
        self.assertEqual(self.sample_slide["body"], original_body)

    def test_merge_visual_spec_handles_all_visual_types(self):
        """All valid visual types are handled."""
        for visual_type in MERGER_VISUAL_TYPES:
            visual_spec = {
                "slide_number": 3,
                "visual_type": visual_type,
                "layout": "A",
                "specification": {}
            }
            result = merge_visual_spec(self.sample_slide, visual_spec)
            self.assertEqual(result["visual_marker"], f"Visual: Yes - {visual_type}")


class TestPreservePresenterNotes(unittest.TestCase):
    """Tests for preserve_presenter_notes function."""

    def test_preserve_notes_extracts_correctly(self):
        """Notes are extracted unchanged."""
        slide = {
            "presenter_notes": "[PAUSE] Important clinical note. [EMPHASIS: key term]"
        }
        result = preserve_presenter_notes(slide)
        self.assertEqual(result, "[PAUSE] Important clinical note. [EMPHASIS: key term]")

    def test_preserve_notes_returns_empty_string_if_missing(self):
        """Returns empty string if notes not present."""
        slide = {"header": "Test"}
        result = preserve_presenter_notes(slide)
        self.assertEqual(result, "")

    def test_preserve_notes_handles_empty_notes(self):
        """Handles empty presenter notes."""
        slide = {"presenter_notes": ""}
        result = preserve_presenter_notes(slide)
        self.assertEqual(result, "")


class TestClearBodyForVisual(unittest.TestCase):
    """Tests for clear_body_for_visual function."""

    def test_clear_body_replaces_with_placeholder(self):
        """Body is replaced with '[See Visual]'."""
        slide = {"body": "* Point 1\n* Point 2\n* Point 3"}
        result = clear_body_for_visual(slide)
        self.assertEqual(result["body"], "[See Visual]")

    def test_clear_body_does_not_modify_original(self):
        """Original slide is not modified."""
        original_body = "* Point 1\n* Point 2"
        slide = {"body": original_body}
        clear_body_for_visual(slide)
        self.assertEqual(slide["body"], original_body)

    def test_clear_body_handles_empty_body(self):
        """Handles slides with empty body."""
        slide = {"body": ""}
        result = clear_body_for_visual(slide)
        self.assertEqual(result["body"], "[See Visual]")


class TestClearNclexTipForVisual(unittest.TestCase):
    """Tests for clear_nclex_tip_for_visual function."""

    def test_clear_tip_sets_to_none(self):
        """NCLEX tip is set to 'None'."""
        slide = {"nclex_tip": "Important exam tip about medications"}
        result = clear_nclex_tip_for_visual(slide)
        self.assertEqual(result["nclex_tip"], "None")

    def test_clear_tip_does_not_modify_original(self):
        """Original slide is not modified."""
        original_tip = "Important tip"
        slide = {"nclex_tip": original_tip}
        clear_nclex_tip_for_visual(slide)
        self.assertEqual(slide["nclex_tip"], original_tip)

    def test_clear_tip_handles_missing_tip(self):
        """Handles slides without nclex_tip field."""
        slide = {"header": "Test"}
        result = clear_nclex_tip_for_visual(slide)
        self.assertEqual(result["nclex_tip"], "None")


class TestFormatVisualSection(unittest.TestCase):
    """Tests for format_visual_section function."""

    def test_format_table_spec(self):
        """TABLE specification is formatted correctly."""
        spec = {
            "title": "Drug Comparison",
            "columns": ["Drug", "Class", "Side Effects"],
            "rows": [
                ["Metoprolol", "Beta-blocker", "Bradycardia"],
                ["Lisinopril", "ACE-I", "Cough"]
            ],
            "colors": {"header_bg": "#1a5276"}
        }
        result = format_visual_section(spec, "TABLE")

        self.assertIn("Type: TABLE", result)
        self.assertIn("Title: Drug Comparison", result)
        self.assertIn("Columns: 3", result)
        self.assertIn("TABLE CONTENT:", result)
        self.assertIn("Drug | Class | Side Effects", result)

    def test_format_hierarchy_spec(self):
        """HIERARCHY specification is formatted correctly."""
        spec = {
            "title": "Beta Blocker Classification",
            "root": "Beta Blockers",
            "children": [
                {"label": "Cardioselective", "children": ["Metoprolol", "Atenolol"]},
                {"label": "Non-selective", "children": ["Propranolol"]}
            ]
        }
        result = format_visual_section(spec, "HIERARCHY")

        self.assertIn("Type: HIERARCHY", result)
        self.assertIn("ROOT: \"Beta Blockers\"", result)
        self.assertIn("LEVELS:", result)

    def test_format_flowchart_spec(self):
        """FLOWCHART specification is formatted correctly."""
        spec = {
            "start": "Assess Patient",
            "steps": [
                {"header": "Check Vitals", "body": "BP, HR, RR"},
                {"header": "Review Labs", "body": "CBC, BMP"}
            ],
            "end": "Document Findings"
        }
        result = format_visual_section(spec, "FLOWCHART")

        self.assertIn("Type: FLOWCHART", result)
        self.assertIn("START: \"Assess Patient\"", result)
        self.assertIn("STEPS:", result)
        self.assertIn("END: \"Document Findings\"", result)

    def test_format_timeline_spec(self):
        """TIMELINE specification is formatted correctly."""
        spec = {
            "events": [
                {"date": "Day 1", "header": "Admission", "description": "Initial assessment"},
                {"date": "Day 2", "header": "Treatment", "description": "Begin therapy"}
            ]
        }
        result = format_visual_section(spec, "TIMELINE")

        self.assertIn("Type: TIMELINE", result)
        self.assertIn("EVENTS:", result)
        self.assertIn("Date: \"Day 1\"", result)

    def test_format_spectrum_spec(self):
        """SPECTRUM specification is formatted correctly."""
        spec = {
            "gradient": "blue",
            "endpoints": {"low": "Mild", "high": "Severe"},
            "segments": [
                {"label": "Stage 1", "description": "Early symptoms"}
            ]
        }
        result = format_visual_section(spec, "SPECTRUM")

        self.assertIn("Type: SPECTRUM", result)
        self.assertIn("Gradient: blue", result)
        self.assertIn("ENDPOINTS:", result)
        self.assertIn("Low: \"Mild\"", result)
        self.assertIn("High: \"Severe\"", result)


class TestIntegrateAllVisuals(unittest.TestCase):
    """Tests for integrate_all_visuals function."""

    def setUp(self):
        """Set up test fixtures with multiple slides.

        Note: 2 visuals out of 6 slides = 33.3%, which passes the 40% max quota.
        """
        self.blueprint = {
            "slides": [
                {
                    "slide_number": 1,
                    "header": "Introduction",
                    "body": "* Overview of topic",
                    "nclex_tip": "Tip for slide 1",
                    "presenter_notes": "Notes for slide 1"
                },
                {
                    "slide_number": 2,
                    "header": "Comparison",
                    "body": "* Compare A vs B",
                    "nclex_tip": "Comparison tip",
                    "presenter_notes": "Comparison notes [PAUSE]"
                },
                {
                    "slide_number": 3,
                    "header": "Process",
                    "body": "* Step 1\n* Step 2",
                    "nclex_tip": "Process tip",
                    "presenter_notes": "Process notes [EMPHASIS: key]"
                },
                {
                    "slide_number": 4,
                    "header": "Details",
                    "body": "* More details here",
                    "nclex_tip": "Details tip",
                    "presenter_notes": "Details notes"
                },
                {
                    "slide_number": 5,
                    "header": "Clinical Application",
                    "body": "* Apply to patient care",
                    "nclex_tip": "Application tip",
                    "presenter_notes": "Application notes"
                },
                {
                    "slide_number": 6,
                    "header": "Summary",
                    "body": "* Key points",
                    "nclex_tip": "Summary tip",
                    "presenter_notes": "Summary notes"
                }
            ]
        }

        self.visual_specs = [
            {
                "slide_number": 2,
                "visual_type": "TABLE",
                "layout": "B",
                "specification": {"title": "Comparison Table"}
            },
            {
                "slide_number": 3,
                "visual_type": "FLOWCHART",
                "layout": "A",
                "specification": {"start": "Begin"}
            }
        ]

    def test_integrate_marks_visual_slides(self):
        """Visual slides are marked correctly."""
        result = integrate_all_visuals(self.blueprint, self.visual_specs)

        slide2 = next(s for s in result["slides"] if s["slide_number"] == 2)
        slide3 = next(s for s in result["slides"] if s["slide_number"] == 3)

        self.assertEqual(slide2["visual_marker"], "Visual: Yes - TABLE")
        self.assertEqual(slide3["visual_marker"], "Visual: Yes - FLOWCHART")

    def test_integrate_marks_content_slides(self):
        """Non-visual slides are marked 'Visual: No'."""
        result = integrate_all_visuals(self.blueprint, self.visual_specs)

        slide1 = next(s for s in result["slides"] if s["slide_number"] == 1)
        slide6 = next(s for s in result["slides"] if s["slide_number"] == 6)

        self.assertEqual(slide1["visual_marker"], "Visual: No")
        self.assertEqual(slide6["visual_marker"], "Visual: No")

    def test_integrate_clears_body_for_visuals(self):
        """Visual slide bodies are cleared."""
        result = integrate_all_visuals(self.blueprint, self.visual_specs)

        slide2 = next(s for s in result["slides"] if s["slide_number"] == 2)
        slide3 = next(s for s in result["slides"] if s["slide_number"] == 3)

        self.assertEqual(slide2["body"], "[See Visual]")
        self.assertEqual(slide3["body"], "[See Visual]")

    def test_integrate_preserves_content_slide_body(self):
        """Content slide bodies are preserved."""
        result = integrate_all_visuals(self.blueprint, self.visual_specs)

        slide1 = next(s for s in result["slides"] if s["slide_number"] == 1)
        slide6 = next(s for s in result["slides"] if s["slide_number"] == 6)

        self.assertEqual(slide1["body"], "* Overview of topic")
        self.assertEqual(slide6["body"], "* Key points")

    def test_integrate_clears_tips_for_visuals(self):
        """Visual slide NCLEX tips are cleared."""
        result = integrate_all_visuals(self.blueprint, self.visual_specs)

        slide2 = next(s for s in result["slides"] if s["slide_number"] == 2)
        slide3 = next(s for s in result["slides"] if s["slide_number"] == 3)

        self.assertEqual(slide2["nclex_tip"], "None")
        self.assertEqual(slide3["nclex_tip"], "None")

    def test_integrate_preserves_notes_for_visuals(self):
        """Visual slide presenter notes are preserved."""
        result = integrate_all_visuals(self.blueprint, self.visual_specs)

        slide2 = next(s for s in result["slides"] if s["slide_number"] == 2)
        slide3 = next(s for s in result["slides"] if s["slide_number"] == 3)

        self.assertEqual(slide2["presenter_notes"], "Comparison notes [PAUSE]")
        self.assertEqual(slide3["presenter_notes"], "Process notes [EMPHASIS: key]")

    def test_integrate_adds_integration_summary(self):
        """Integration summary is added to blueprint."""
        result = integrate_all_visuals(self.blueprint, self.visual_specs)

        self.assertIn("integration_summary", result)
        self.assertEqual(result["integration_summary"]["total_slides"], 6)
        self.assertEqual(result["integration_summary"]["visual_slides"], 2)
        self.assertEqual(result["integration_summary"]["content_slides"], 4)

    def test_integrate_adds_validation_results(self):
        """Validation results are added to blueprint."""
        result = integrate_all_visuals(self.blueprint, self.visual_specs)

        self.assertIn("validation", result)
        self.assertTrue(result["validation"]["all_slides_marked"])
        self.assertTrue(result["validation"]["visual_specs_applied"])
        self.assertEqual(result["validation"]["quota_check"], "PASS")

    def test_integrate_does_not_modify_original(self):
        """Original blueprint is not modified."""
        original_body = self.blueprint["slides"][1]["body"]
        integrate_all_visuals(self.blueprint, self.visual_specs)
        self.assertEqual(self.blueprint["slides"][1]["body"], original_body)

    def test_integrate_quota_fail_below_minimum(self):
        """Quota check fails when below minimum."""
        # Create blueprint with 20 slides but only 1 visual
        large_blueprint = {
            "slides": [
                {"slide_number": i, "header": f"Slide {i}", "body": "Content",
                 "nclex_tip": "Tip", "presenter_notes": "Notes"}
                for i in range(1, 21)
            ]
        }
        single_visual = [{"slide_number": 1, "visual_type": "TABLE", "layout": "A", "specification": {}}]

        result = integrate_all_visuals(large_blueprint, single_visual)
        self.assertIn("Below minimum", result["validation"]["quota_check"])


class TestGetIntegrationSummary(unittest.TestCase):
    """Tests for get_integration_summary function."""

    def test_summary_counts_visual_slides(self):
        """Visual slides are counted correctly."""
        blueprint = {
            "slides": [
                {"slide_number": 1, "visual_marker": "Visual: Yes - TABLE"},
                {"slide_number": 2, "visual_marker": "Visual: No"},
                {"slide_number": 3, "visual_marker": "Visual: Yes - FLOWCHART"},
            ]
        }
        result = get_integration_summary(blueprint)

        self.assertEqual(result["visual_slides"], 2)
        self.assertEqual(result["content_slides"], 1)
        self.assertEqual(result["visual_slide_numbers"], [1, 3])
        self.assertEqual(result["content_slide_numbers"], [2])

    def test_summary_identifies_unmarked_slides(self):
        """Unmarked slides are identified."""
        blueprint = {
            "slides": [
                {"slide_number": 1, "visual_marker": "Visual: No"},
                {"slide_number": 2},  # No visual_marker
                {"slide_number": 3, "visual_marker": None},
            ]
        }
        result = get_integration_summary(blueprint)

        self.assertEqual(result["unmarked_slides"], 2)
        self.assertFalse(result["all_marked"])


class TestValidateIntegrationMerger(unittest.TestCase):
    """Tests for validate_integration function from visual_merger."""

    def test_valid_integration_passes(self):
        """Correctly integrated blueprint passes validation."""
        blueprint = {
            "slides": [
                {
                    "slide_number": 1,
                    "visual_marker": "Visual: Yes - TABLE",
                    "body": "[See Visual]",
                    "nclex_tip": "None",
                    "visual_specification": {"type": "TABLE"}
                },
                {
                    "slide_number": 2,
                    "visual_marker": "Visual: No",
                    "body": "* Content here",
                    "nclex_tip": "Some tip"
                }
            ]
        }
        result = validate_integration(blueprint)

        self.assertTrue(result["valid"])
        self.assertEqual(len(result["issues"]), 0)

    def test_missing_marker_detected(self):
        """Missing visual marker is detected."""
        blueprint = {
            "slides": [
                {"slide_number": 1, "body": "Content"}  # No visual_marker
            ]
        }
        result = validate_integration(blueprint)

        self.assertFalse(result["valid"])
        self.assertTrue(any("Missing visual marker" in i["issue"] for i in result["issues"]))

    def test_visual_slide_body_not_cleared_detected(self):
        """Visual slide with incorrect body is detected."""
        blueprint = {
            "slides": [
                {
                    "slide_number": 1,
                    "visual_marker": "Visual: Yes - TABLE",
                    "body": "Still has content",  # Should be "[See Visual]"
                    "nclex_tip": "None",
                    "visual_specification": {}
                }
            ]
        }
        result = validate_integration(blueprint)

        self.assertFalse(result["valid"])
        self.assertTrue(any("[See Visual]" in i["issue"] for i in result["issues"]))

    def test_visual_slide_tip_not_cleared_detected(self):
        """Visual slide with tip not cleared is detected."""
        blueprint = {
            "slides": [
                {
                    "slide_number": 1,
                    "visual_marker": "Visual: Yes - TABLE",
                    "body": "[See Visual]",
                    "nclex_tip": "Should be None",  # Should be "None"
                    "visual_specification": {}
                }
            ]
        }
        result = validate_integration(blueprint)

        self.assertFalse(result["valid"])
        self.assertTrue(any("nclex_tip should be 'None'" in i["issue"] for i in result["issues"]))


class TestVisualMergerEdgeCases(unittest.TestCase):
    """Tests for edge cases in visual_merger module."""

    def test_empty_blueprint(self):
        """Handles empty blueprint."""
        blueprint = {"slides": []}
        result = integrate_all_visuals(blueprint, [])

        self.assertEqual(result["integration_summary"]["total_slides"], 0)

    def test_no_visual_specs(self):
        """All slides marked 'Visual: No' when no specs provided."""
        blueprint = {
            "slides": [
                {"slide_number": 1, "body": "Content 1", "nclex_tip": "Tip", "presenter_notes": "Notes"},
                {"slide_number": 2, "body": "Content 2", "nclex_tip": "Tip", "presenter_notes": "Notes"}
            ]
        }
        result = integrate_all_visuals(blueprint, [])

        for slide in result["slides"]:
            self.assertEqual(slide["visual_marker"], "Visual: No")

    def test_visual_spec_for_nonexistent_slide(self):
        """Visual spec for non-existent slide is ignored."""
        blueprint = {
            "slides": [
                {"slide_number": 1, "body": "Content", "nclex_tip": "Tip", "presenter_notes": "Notes"}
            ]
        }
        visual_specs = [
            {"slide_number": 999, "visual_type": "TABLE", "layout": "A", "specification": {}}
        ]
        result = integrate_all_visuals(blueprint, visual_specs)

        # Slide 1 should be marked as Visual: No
        self.assertEqual(result["slides"][0]["visual_marker"], "Visual: No")

    def test_unknown_visual_type(self):
        """Unknown visual type is handled."""
        slide = {"body": "Content", "nclex_tip": "Tip", "presenter_notes": "Notes"}
        visual_spec = {"visual_type": "UNKNOWN_TYPE", "specification": {}}

        result = merge_visual_spec(slide, visual_spec)
        self.assertEqual(result["visual_marker"], "Visual: Yes - UNKNOWN")

    def test_blueprint_with_nested_structure(self):
        """Handles blueprint with step7_blueprint nested structure."""
        blueprint = {
            "step7_blueprint": {
                "slides": [
                    {"slide_number": 1, "body": "Content", "nclex_tip": "Tip", "presenter_notes": "Notes"}
                ]
            }
        }
        result = integrate_all_visuals(blueprint, [])

        self.assertIn("slides", result)
        self.assertEqual(result["slides"][0]["visual_marker"], "Visual: No")


if __name__ == '__main__':
    unittest.main()
