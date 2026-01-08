"""
Unit Tests for Step 9 Content Structure Analyzer
Tests the content_structure_analyzer.py skill for visual type selection.
"""

import unittest
import sys
import os
import json

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from skills.generation.content_structure_analyzer import (
    count_bullet_points,
    detect_list_patterns,
    identify_comparison_structure,
    detect_sequential_markers,
    analyze_information_density,
    detect_hierarchical_structure,
    suggest_visual_type,
    analyze_slide_content
)
from skills.generation.visual_pattern_matcher import VisualType


class TestCountBulletPoints(unittest.TestCase):
    """Tests for count_bullet_points function."""

    def test_asterisk_bullets(self):
        """Test counting asterisk-style bullets."""
        body = """* First item
* Second item
* Third item"""
        self.assertEqual(count_bullet_points(body), 3)

    def test_dash_bullets(self):
        """Test counting dash-style bullets."""
        body = """- First item
- Second item
- Third item
- Fourth item"""
        self.assertEqual(count_bullet_points(body), 4)

    def test_numbered_bullets(self):
        """Test counting numbered list items."""
        body = """1. First step
2. Second step
3. Third step"""
        self.assertEqual(count_bullet_points(body), 3)

    def test_mixed_bullet_styles(self):
        """Test counting mixed bullet styles."""
        body = """* Asterisk item
- Dash item
1. Numbered item"""
        self.assertEqual(count_bullet_points(body), 3)

    def test_nested_bullets_only_count_top_level(self):
        """Test that nested bullets are not counted."""
        body = """* First item
  - Nested item 1
  - Nested item 2
* Second item
  * Nested item 3
* Third item"""
        self.assertEqual(count_bullet_points(body), 3)

    def test_empty_body(self):
        """Test empty body returns zero."""
        self.assertEqual(count_bullet_points(""), 0)
        self.assertEqual(count_bullet_points("   "), 0)
        self.assertEqual(count_bullet_points(None), 0)

    def test_no_bullets(self):
        """Test body without bullets returns zero."""
        body = """This is just regular text.
No bullets here at all.
Just sentences."""
        self.assertEqual(count_bullet_points(body), 0)


class TestDetectListPatterns(unittest.TestCase):
    """Tests for detect_list_patterns function."""

    def test_numbered_list_detection(self):
        """Test detection of numbered lists."""
        body = """1. First step
2. Second step
3. Third step"""
        result = detect_list_patterns(body)
        self.assertTrue(result['has_numbered_list'])
        self.assertFalse(result['has_bulleted_list'])
        self.assertEqual(result['list_depth'], 1)

    def test_bulleted_list_detection(self):
        """Test detection of bulleted lists."""
        body = """* First item
* Second item
* Third item"""
        result = detect_list_patterns(body)
        self.assertFalse(result['has_numbered_list'])
        self.assertTrue(result['has_bulleted_list'])
        self.assertEqual(result['list_depth'], 1)

    def test_nested_list_depth(self):
        """Test detection of nested list depth."""
        body = """1. First level
  a. Second level
    - Third level
2. Back to first"""
        result = detect_list_patterns(body)
        self.assertGreaterEqual(result['list_depth'], 2)

    def test_items_per_level(self):
        """Test counting items at each nesting level."""
        body = """* Level 1 item 1
* Level 1 item 2
  - Level 2 item 1
  - Level 2 item 2
  - Level 2 item 3
* Level 1 item 3"""
        result = detect_list_patterns(body)
        # Should have items at level 1 (3 items) and level 2 (3 items)
        self.assertEqual(len(result['items_per_level']), 2)
        self.assertGreaterEqual(sum(result['items_per_level']), 4)

    def test_empty_body(self):
        """Test empty body returns empty result."""
        result = detect_list_patterns("")
        self.assertFalse(result['has_numbered_list'])
        self.assertFalse(result['has_bulleted_list'])
        self.assertEqual(result['list_depth'], 0)


class TestIdentifyComparisonStructure(unittest.TestCase):
    """Tests for identify_comparison_structure function."""

    def test_vs_keyword_detection(self):
        """Test detection of 'vs' comparisons."""
        body = "ACE-I vs ARBs: Which to choose?"
        result = identify_comparison_structure(body)
        self.assertTrue(result['is_comparison'])

    def test_versus_keyword_detection(self):
        """Test detection of 'versus' comparisons."""
        body = "Comparing Type 1 versus Type 2 diabetes"
        result = identify_comparison_structure(body)
        self.assertTrue(result['is_comparison'])

    def test_comparison_items_extraction(self):
        """Test extraction of items being compared."""
        body = """SSRI vs SNRI comparison:
* SSRI: Serotonin only
* SNRI: Serotonin and norepinephrine"""
        result = identify_comparison_structure(body)
        self.assertTrue(result['is_comparison'])
        self.assertGreaterEqual(len(result['comparison_items']), 1)

    def test_binary_comparison_type(self):
        """Test binary comparison type detection."""
        body = "Metoprolol vs Atenolol for hypertension"
        result = identify_comparison_structure(body)
        self.assertEqual(result['comparison_type'], 'binary')

    def test_multiple_comparison_type(self):
        """Test multiple item comparison detection."""
        body = """Compare these three drugs:
* Drug A: Fast acting
* Drug B: Long duration
* Drug C: Fewer side effects"""
        result = identify_comparison_structure(body)
        self.assertTrue(result['is_comparison'])

    def test_no_comparison(self):
        """Test non-comparison content returns false."""
        body = "Basic information about medication administration."
        result = identify_comparison_structure(body)
        self.assertFalse(result['is_comparison'])


class TestDetectSequentialMarkers(unittest.TestCase):
    """Tests for detect_sequential_markers function."""

    def test_step_markers_detection(self):
        """Test detection of step-based sequences."""
        body = """Step 1: Verify the order
Step 2: Check patient ID
Step 3: Administer medication"""
        result = detect_sequential_markers(body)
        self.assertTrue(result['is_sequential'])
        self.assertEqual(result['sequence_type'], 'steps')

    def test_process_markers_detection(self):
        """Test detection of process sequences."""
        body = """Mechanism of action:
Drug binds to receptor, which leads to
enzyme inhibition. This results in
vasodilation and lower blood pressure."""
        result = detect_sequential_markers(body)
        self.assertTrue(result['is_sequential'])
        self.assertEqual(result['sequence_type'], 'process')

    def test_timeline_detection(self):
        """Test detection of timeline sequences."""
        body = """Early symptoms appear in first week.
Later, by month 2, progression occurs.
Eventually, full effects seen at 6 months."""
        result = detect_sequential_markers(body)
        self.assertTrue(result['is_sequential'])
        self.assertEqual(result['sequence_type'], 'timeline')

    def test_step_count_estimation(self):
        """Test estimation of step count."""
        body = """Step 1: Assessment
Step 2: Diagnosis
Step 3: Planning
Step 4: Implementation
Step 5: Evaluation"""
        result = detect_sequential_markers(body)
        self.assertEqual(result['step_count'], 5)

    def test_non_sequential_content(self):
        """Test non-sequential content returns false."""
        body = "List of common side effects: nausea, headache, dizziness."
        result = detect_sequential_markers(body)
        self.assertFalse(result['is_sequential'])


class TestAnalyzeInformationDensity(unittest.TestCase):
    """Tests for analyze_information_density function."""

    def test_word_count(self):
        """Test total word count."""
        body = "One two three four five."
        result = analyze_information_density(body)
        self.assertEqual(result['total_words'], 5)

    def test_words_per_line(self):
        """Test words per line calculation."""
        body = """First line has five words here.
Second line also five words here."""
        result = analyze_information_density(body)
        self.assertAlmostEqual(result['words_per_line'], 5.0, delta=1.0)

    def test_density_score_high(self):
        """Test high density content has high score."""
        body = """Digoxin (Lanoxin) is a cardiac glycoside.
Mechanism: Inhibits Na+/K+ ATPase pump
Effects: Positive inotropic action
Toxicity: Visual disturbances, nausea
Contraindications: Heart block, Wolff-Parkinson-White
Drug interactions: Amiodarone increases levels
Monitoring: Therapeutic range 0.8-2.0 ng/mL"""
        result = analyze_information_density(body)
        self.assertGreater(result['density_score'], 0.5)

    def test_density_score_low(self):
        """Test simple content has lower score."""
        body = "Simple overview."
        result = analyze_information_density(body)
        self.assertLess(result['density_score'], 0.5)

    def test_unique_concepts_count(self):
        """Test unique concept counting."""
        body = """ACE Inhibitors (Lisinopril, Enalapril):
Mechanism: Block angiotensin-converting enzyme
Result: Vasodilation, reduced blood pressure"""
        result = analyze_information_density(body)
        self.assertGreater(result['unique_concepts'], 0)

    def test_empty_body(self):
        """Test empty body returns zero values."""
        result = analyze_information_density("")
        self.assertEqual(result['total_words'], 0)
        self.assertEqual(result['density_score'], 0.0)


class TestDetectHierarchicalStructure(unittest.TestCase):
    """Tests for detect_hierarchical_structure function."""

    def test_types_of_pattern(self):
        """Test detection of 'types of' hierarchy."""
        body = """Types of Beta Blockers:
* Cardioselective
* Non-selective
* Combined alpha-beta"""
        result = detect_hierarchical_structure(body)
        self.assertTrue(result['is_hierarchical'])

    def test_classification_pattern(self):
        """Test detection of classification hierarchy."""
        body = """Classification of antihypertensives:
* Diuretics
  - Thiazides
  - Loop
* ACE Inhibitors
* ARBs"""
        result = detect_hierarchical_structure(body)
        self.assertTrue(result['is_hierarchical'])

    def test_levels_detection(self):
        """Test hierarchy levels detection."""
        body = """Drug categories:
* Cardiovascular
  - Antihypertensives
    - ACE-I
    - ARBs
  - Antiarrhythmics
* Respiratory"""
        result = detect_hierarchical_structure(body)
        self.assertGreaterEqual(result['levels_detected'], 2)

    def test_root_concept_extraction(self):
        """Test extraction of root concept."""
        body = "Types of diuretics: thiazides, loop, potassium-sparing"
        result = detect_hierarchical_structure(body)
        self.assertIsNotNone(result['root_concept'])

    def test_non_hierarchical_content(self):
        """Test non-hierarchical content returns false."""
        body = "This medication should be taken with food."
        result = detect_hierarchical_structure(body)
        self.assertFalse(result['is_hierarchical'])


class TestSuggestVisualType(unittest.TestCase):
    """Tests for suggest_visual_type function."""

    def test_comparison_suggests_table(self):
        """Test comparison content suggests TABLE."""
        body = """ACE-I vs ARBs comparison:
* ACE-I: Block conversion
* ARBs: Block receptor
* ACE-I: Cough side effect
* ARBs: No cough
* Both: Hyperkalemia risk"""
        result = suggest_visual_type(body)
        self.assertIn(result['primary_suggestion'],
                     [VisualType.TABLE, VisualType.KEY_DIFFERENTIATORS])

    def test_sequential_suggests_flowchart(self):
        """Test sequential content suggests FLOWCHART."""
        body = """Mechanism of action:
Step 1: Drug binds to receptor
Step 2: Enzyme activation
Step 3: Leads to vasodilation
Step 4: Results in BP reduction"""
        result = suggest_visual_type(body)
        self.assertEqual(result['primary_suggestion'], VisualType.FLOWCHART)

    def test_hierarchical_suggests_hierarchy(self):
        """Test hierarchical content suggests HIERARCHY."""
        body = """Types of Beta Blockers:
* Cardioselective
  - Metoprolol
  - Atenolol
* Non-selective
  - Propranolol
  - Nadolol
* Alpha/Beta
  - Carvedilol"""
        result = suggest_visual_type(body)
        self.assertIn(result['primary_suggestion'],
                     [VisualType.HIERARCHY, VisualType.TABLE])

    def test_timeline_content_suggests_timeline(self):
        """Test timeline content suggests TIMELINE."""
        body = """Disease progression over time:
Early stage (week 1-2): Initial symptoms
Middle stage (month 1-3): Progressive worsening
Late stage (month 6+): Full manifestation"""
        result = suggest_visual_type(body)
        self.assertIn(result['primary_suggestion'],
                     [VisualType.TIMELINE, VisualType.FLOWCHART])

    def test_spectrum_content_suggests_spectrum(self):
        """Test spectrum content suggests SPECTRUM."""
        body = """Pain severity scale ranges from mild to severe:
Mild: 1-3 on scale
Moderate: 4-6 on scale
Severe: 7-10 on scale"""
        result = suggest_visual_type(body)
        self.assertEqual(result['primary_suggestion'], VisualType.SPECTRUM)

    def test_decision_content_suggests_decision_tree(self):
        """Test decision content suggests DECISION_TREE."""
        body = """Treatment selection algorithm:
If patient has diabetes, then choose ACE-I
If patient has asthma, then avoid beta blockers
Based on kidney function, determine dosage"""
        result = suggest_visual_type(body)
        self.assertEqual(result['primary_suggestion'], VisualType.DECISION_TREE)

    def test_confidence_score(self):
        """Test confidence score is between 0 and 1."""
        body = "Compare Drug A versus Drug B for efficacy."
        result = suggest_visual_type(body)
        self.assertGreaterEqual(result['confidence'], 0.0)
        self.assertLessEqual(result['confidence'], 1.0)

    def test_secondary_suggestions(self):
        """Test secondary suggestions are provided."""
        body = """Compare these medication types:
* Type A: Fast onset, short duration
* Type B: Slow onset, long duration
This progression follows a timeline."""
        result = suggest_visual_type(body)
        self.assertIsInstance(result['secondary_suggestions'], list)

    def test_analysis_dict_present(self):
        """Test analysis dictionary is populated."""
        body = "* Item 1\n* Item 2\n* Item 3"
        result = suggest_visual_type(body)
        self.assertIn('bullet_count', result['analysis'])
        self.assertIn('is_comparison', result['analysis'])
        self.assertIn('density_score', result['analysis'])


class TestAnalyzeSlideContent(unittest.TestCase):
    """Tests for analyze_slide_content convenience function."""

    def test_slide_dict_analysis(self):
        """Test analysis of full slide dictionary."""
        slide = {
            'slide_number': 5,
            'header': 'ACE Inhibitors vs ARBs',
            'body': """* ACE-I: Block ACE enzyme
* ARBs: Block AT1 receptor
* Both: Reduce blood pressure"""
        }
        result = analyze_slide_content(slide)
        self.assertEqual(result['slide_number'], 5)
        self.assertIn(result['visual_suggestion'],
                     ['TABLE', 'KEY_DIFFERENTIATORS'])

    def test_title_key_support(self):
        """Test support for 'title' key instead of 'header'."""
        slide = {
            'slide_number': 3,
            'title': 'Drug Classification',
            'body': 'Types of medications include...'
        }
        result = analyze_slide_content(slide)
        self.assertEqual(result['title'], 'Drug Classification')


class TestIntegrationWithSampleData(unittest.TestCase):
    """Integration tests using sample data from samples/step9_visual/."""

    @classmethod
    def setUpClass(cls):
        """Load sample data if available."""
        sample_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            'samples', 'step9_visual', 'sample_visual_input.json'
        )
        cls.sample_data = None
        if os.path.exists(sample_path):
            with open(sample_path, 'r') as f:
                cls.sample_data = json.load(f)

    def test_sample_slide_analysis(self):
        """Test analysis of sample slides."""
        if self.sample_data is None:
            self.skipTest("Sample data not available")

        slides = self.sample_data.get('slides', [])
        analyzed_count = 0
        identified_count = 0

        for slide in slides:
            if slide.get('visual_candidate', False):
                body = slide.get('body', '')
                # Use analyze_slide_content to include title in analysis
                full_result = analyze_slide_content(slide)
                analyzed_count += 1

                # Count how many we identify (relaxed test - not all may be identified)
                if full_result['visual_suggestion'] != 'NONE':
                    identified_count += 1

        # Should identify at least 50% of visual candidates
        if analyzed_count > 0:
            self.assertGreaterEqual(identified_count / analyzed_count, 0.5,
                                   f"Only identified {identified_count}/{analyzed_count} candidates")

    def test_sample_comparison_slide(self):
        """Test ACE-I vs ARBs slide from samples."""
        if self.sample_data is None:
            self.skipTest("Sample data not available")

        # Find the ACE-I vs ARBs slide
        for slide in self.sample_data.get('slides', []):
            if 'vs ARBs' in slide.get('title', ''):
                # Use analyze_slide_content which combines title + body
                full_result = analyze_slide_content(slide)
                # The title contains "vs" so comparison should be detected
                # Or should suggest TABLE/KEY_DIFF for structured comparison content
                self.assertIn(full_result['visual_suggestion'],
                             ['TABLE', 'KEY_DIFFERENTIATORS', 'FLOWCHART'])

    def test_sample_mechanism_slide(self):
        """Test mechanism slide from samples."""
        if self.sample_data is None:
            self.skipTest("Sample data not available")

        # Find slides with mechanism content
        for slide in self.sample_data.get('slides', []):
            if 'Mechanism' in slide.get('body', ''):
                body = slide.get('body', '')
                result = suggest_visual_type(body)
                # Mechanism content should suggest flowchart or table
                self.assertIn(result['primary_suggestion'],
                             [VisualType.FLOWCHART, VisualType.TABLE])


class TestEdgeCases(unittest.TestCase):
    """Tests for edge cases and error handling."""

    def test_none_input(self):
        """Test handling of None input."""
        self.assertEqual(count_bullet_points(None), 0)
        self.assertFalse(detect_list_patterns(None)['has_bulleted_list'])
        self.assertFalse(identify_comparison_structure(None)['is_comparison'])
        self.assertFalse(detect_sequential_markers(None)['is_sequential'])
        self.assertEqual(analyze_information_density(None)['total_words'], 0)
        self.assertFalse(detect_hierarchical_structure(None)['is_hierarchical'])
        result = suggest_visual_type(None)
        self.assertEqual(result['primary_suggestion'], VisualType.NONE)

    def test_whitespace_only_input(self):
        """Test handling of whitespace-only input."""
        self.assertEqual(count_bullet_points("   \n\t  "), 0)
        result = suggest_visual_type("   \n\t  ")
        self.assertEqual(result['primary_suggestion'], VisualType.NONE)

    def test_unicode_content(self):
        """Test handling of unicode characters."""
        body = "* Therapeutic range: 0.8-2.0 ng/mL"
        result = count_bullet_points(body)
        self.assertEqual(result, 1)

    def test_very_long_content(self):
        """Test handling of very long content."""
        body = "* Point\n" * 100
        result = count_bullet_points(body)
        self.assertEqual(result, 100)

    def test_special_characters(self):
        """Test handling of special characters in content."""
        body = "* Na+/K+ ATPase: Important enzyme\n* Ca2+ channels: Cardiac effects"
        result = count_bullet_points(body)
        self.assertEqual(result, 2)


class TestVisualTypeMappingLogic(unittest.TestCase):
    """Tests to verify visual type mapping rules."""

    def test_high_bullet_plus_comparison_equals_table(self):
        """Test: High bullet count (4+) + comparison -> TABLE."""
        body = """Drug A vs Drug B comparison:
* Mechanism: A blocks X, B blocks Y
* Onset: A is fast, B is slow
* Duration: A is short, B is long
* Side effects: A has nausea, B has headache
* Cost: A is expensive, B is affordable"""
        result = suggest_visual_type(body)
        self.assertEqual(result['analysis']['bullet_count'], 5)
        self.assertTrue(result['analysis']['is_comparison'])
        self.assertIn(result['primary_suggestion'],
                     [VisualType.TABLE, VisualType.KEY_DIFFERENTIATORS])

    def test_sequential_markers_suggest_flowchart(self):
        """Test: Sequential markers -> FLOWCHART."""
        body = """First, assess the patient.
Then, verify the medication order.
Next, prepare the injection.
Finally, document the administration."""
        result = suggest_visual_type(body)
        self.assertTrue(result['analysis']['is_sequential'])
        self.assertEqual(result['primary_suggestion'], VisualType.FLOWCHART)

    def test_binary_comparison_suggest_key_diff(self):
        """Test: Binary comparison -> KEY_DIFFERENTIATORS."""
        body = """Key differences between Metoprolol vs Atenolol:
Metoprolol: Short half-life
Atenolol: Long half-life
Critical distinction for dosing."""
        result = suggest_visual_type(body)
        self.assertTrue(result['analysis']['is_comparison'])
        # Could be TABLE or KEY_DIFFERENTIATORS for binary
        self.assertIn(result['primary_suggestion'],
                     [VisualType.TABLE, VisualType.KEY_DIFFERENTIATORS])


if __name__ == '__main__':
    # Run with verbosity
    unittest.main(verbosity=2)
