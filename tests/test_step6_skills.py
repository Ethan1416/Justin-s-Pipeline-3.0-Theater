"""
Unit Tests for Step 6 Skills
Tests slide_builder, content_expander, visual_pattern_matcher,
visual_quota_tracker, and text_splitter.
"""

import unittest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from skills.generation.slide_builder import (
    SlideStructure, build_slide, build_section_intro,
    build_content_slide, allocate_content
)
from skills.generation.content_expander import (
    expand_anchor, fit_to_body, expand_key_points
)
from skills.generation.visual_pattern_matcher import (
    VisualType, identify_visual_opportunity, score_visual_fit
)
from skills.validation.visual_quota_tracker import (
    VisualQuotaTracker, QuotaStatus, check_quota, get_quota_requirements
)
from skills.utilities.text_splitter import (
    split_at_word_boundary, split_slide_content, smart_split
)


class TestSlideBuilder(unittest.TestCase):
    """Tests for slide_builder.py"""

    def setUp(self):
        self.section_context = {
            'section_name': 'Infection Control',
            'domain': 'fundamentals',
            'total_slides': 15
        }
        self.anchor_content = [
            {
                'anchor_id': 'anchor_1',
                'summary': 'Hand hygiene basics',
                'key_points': ['Wash before contact', 'Use alcohol rub']
            },
            {
                'anchor_id': 'anchor_2',
                'summary': 'PPE usage',
                'key_points': ['Gloves for fluids', 'Gowns for splash']
            }
        ]

    def test_build_section_intro(self):
        """Test section intro slide generation."""
        slide = build_section_intro(1, self.section_context)
        self.assertEqual(slide.slide_number, 1)
        self.assertEqual(slide.slide_type, 'Section Intro')
        self.assertIn('Infection Control', slide.header)

    def test_build_content_slide(self):
        """Test content slide generation."""
        plan_item = {
            'slide_number': 2,
            'slide_type': 'Content',
            'title_hint': 'Standard Precautions',
            'assigned_anchors': ['anchor_1', 'anchor_2']
        }
        slide = build_content_slide(plan_item, self.anchor_content, self.section_context)
        self.assertEqual(slide.slide_number, 2)
        self.assertEqual(slide.slide_type, 'Content')
        self.assertIn('anchor_1', slide.anchors_covered)

    def test_allocate_content(self):
        """Test anchor allocation to slides."""
        anchors = [{'anchor_id': f'a{i}'} for i in range(6)]
        allocation = allocate_content(anchors, 3)
        self.assertEqual(len(allocation), 3)
        # All anchors should be allocated
        all_allocated = []
        for anchor_list in allocation.values():
            all_allocated.extend(anchor_list)
        self.assertEqual(len(all_allocated), 6)

    def test_header_length_limit(self):
        """Test that headers respect 32 char limit."""
        slide = build_section_intro(1, {
            'section_name': 'A Very Long Section Name That Exceeds The Limit'
        })
        self.assertLessEqual(len(slide.header), 32)


class TestContentExpander(unittest.TestCase):
    """Tests for content_expander.py"""

    def setUp(self):
        self.anchor = {
            'summary': 'Standard precautions basics',
            'key_points': [
                'Hand hygiene before patient contact',
                'Use PPE based on exposure risk',
                'Safe injection practices'
            ],
            'clinical_relevance': 'Prevents infections'
        }

    def test_expand_anchor_creates_output(self):
        """Test basic anchor expansion."""
        result = expand_anchor(self.anchor)
        self.assertIsInstance(result, str)
        self.assertTrue(len(result) > 0)

    def test_expand_anchor_respects_line_limit(self):
        """Test that expansion respects line limits."""
        result = expand_anchor(self.anchor, {'max_lines': 8})
        lines = result.split('\n')
        self.assertLessEqual(len(lines), 8)

    def test_fit_to_body_truncates(self):
        """Test that fit_to_body truncates long content."""
        long_content = '\n'.join([f'Line {i}' for i in range(20)])
        result = fit_to_body(long_content, max_lines=8)
        self.assertLessEqual(len(result.split('\n')), 8)

    def test_expand_key_points_bullets(self):
        """Test bullet formatting."""
        points = ['Point one', 'Point two', 'Point three']
        result = expand_key_points(points)
        self.assertIn('*', result)
        self.assertEqual(result.count('*'), 3)


class TestVisualPatternMatcher(unittest.TestCase):
    """Tests for visual_pattern_matcher.py"""

    def test_identify_table_opportunity(self):
        """Test TABLE pattern detection."""
        content = "Compare Type 1 and Type 2 diabetes characteristics"
        result = identify_visual_opportunity(content)
        self.assertEqual(result, VisualType.TABLE)

    def test_identify_flowchart_opportunity(self):
        """Test FLOWCHART pattern detection."""
        content = "The steps in the nursing process sequence"
        result = identify_visual_opportunity(content)
        self.assertEqual(result, VisualType.FLOWCHART)

    def test_identify_timeline_opportunity(self):
        """Test TIMELINE pattern detection."""
        content = "Stages of development and progression over time"
        result = identify_visual_opportunity(content)
        self.assertEqual(result, VisualType.TIMELINE)

    def test_no_visual_for_generic_content(self):
        """Test that generic content doesn't trigger visual."""
        content = "This is just regular educational content."
        result = identify_visual_opportunity(content)
        self.assertIsNone(result)

    def test_score_visual_fit(self):
        """Test scoring function returns valid range."""
        content = "compare versus difference contrast"
        score = score_visual_fit(content, VisualType.TABLE)
        self.assertGreaterEqual(score, 0.0)
        self.assertLessEqual(score, 1.0)


class TestVisualQuotaTracker(unittest.TestCase):
    """Tests for visual_quota_tracker.py"""

    def test_quota_requirements_12_15(self):
        """Test quota for 12-15 slides."""
        quota = get_quota_requirements(14)
        self.assertEqual(quota['minimum'], 2)
        self.assertEqual(quota['target_min'], 3)

    def test_quota_requirements_16_20(self):
        """Test quota for 16-20 slides."""
        quota = get_quota_requirements(18)
        self.assertEqual(quota['minimum'], 3)

    def test_check_quota_pass(self):
        """Test passing quota check."""
        status = check_quota(15, 3)
        self.assertIn(status, [QuotaStatus.PASS, QuotaStatus.AT_TARGET])

    def test_check_quota_below_minimum(self):
        """Test below minimum detection."""
        status = check_quota(15, 1)
        self.assertEqual(status, QuotaStatus.BELOW_MINIMUM)

    def test_tracker_validate(self):
        """Test full tracker validation."""
        tracker = VisualQuotaTracker('Test Section', 15)
        tracker.add_visual(3, 'TABLE')
        tracker.add_visual(7, 'FLOWCHART')
        tracker.add_visual(11, 'TIMELINE')
        result = tracker.validate()
        self.assertTrue(result['valid'])
        self.assertEqual(result['visual_count'], 3)


class TestTextSplitter(unittest.TestCase):
    """Tests for text_splitter.py"""

    def test_split_at_word_boundary_short(self):
        """Test that short text isn't split."""
        text = "Short text"
        result = split_at_word_boundary(text, 66)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], text)

    def test_split_at_word_boundary_long(self):
        """Test that long text is split."""
        text = "This is a very long line that definitely exceeds sixty-six characters and needs splitting"
        result = split_at_word_boundary(text, 66)
        self.assertGreater(len(result), 1)
        for segment in result:
            self.assertLessEqual(len(segment), 66)

    def test_split_slide_content_within_limit(self):
        """Test content within limit isn't split."""
        body = "Line 1\nLine 2\nLine 3"
        first, overflow = split_slide_content(body, 8)
        self.assertEqual(first, body)
        self.assertIsNone(overflow)

    def test_split_slide_content_over_limit(self):
        """Test content over limit is split."""
        body = '\n'.join([f'Line {i}' for i in range(12)])
        first, overflow = split_slide_content(body, 8)
        self.assertEqual(len(first.split('\n')), 8)
        self.assertIsNotNone(overflow)

    def test_smart_split_preserves_bullets(self):
        """Test bullet preservation in smart split."""
        text = "* This is a bullet point"
        result = smart_split(text, 66)
        self.assertTrue(result[0].startswith('*'))


if __name__ == '__main__':
    unittest.main(verbosity=2)
