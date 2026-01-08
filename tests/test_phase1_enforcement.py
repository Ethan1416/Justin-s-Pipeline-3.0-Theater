"""
Unit Tests for Phase 1 Enforcement Skills
Tests slide numbering (R15) and NCLEX tip fallback (R4)
"""

import unittest
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from skills.enforcement.slide_numbering import (
    enforce_sequential_numbering,
    validate_sequential_numbering
)
from skills.enforcement.nclex_tip_fallback import (
    ensure_nclex_tip,
    ensure_all_tips,
    validate_nclex_tips,
    get_fallback_tip
)


class TestSlideNumbering(unittest.TestCase):
    """Tests for R15: Sequential slide numbering"""

    def test_sequential_enforcement_basic(self):
        """Test basic sequential numbering enforcement"""
        slides = [
            {'slide_number': 5},
            {'slide_number': 10},
            {'slide_number': 1}
        ]
        fixed = enforce_sequential_numbering(slides)
        self.assertEqual([s['slide_number'] for s in fixed], [1, 2, 3])

    def test_sequential_enforcement_empty(self):
        """Test with empty list"""
        slides = []
        fixed = enforce_sequential_numbering(slides)
        self.assertEqual(fixed, [])

    def test_sequential_enforcement_already_correct(self):
        """Test with already correct numbering"""
        slides = [
            {'slide_number': 1},
            {'slide_number': 2},
            {'slide_number': 3}
        ]
        fixed = enforce_sequential_numbering(slides)
        self.assertEqual([s['slide_number'] for s in fixed], [1, 2, 3])

    def test_validation_pass(self):
        """Test validation passes for correct numbering"""
        slides = [{'slide_number': i} for i in [1, 2, 3]]
        result = validate_sequential_numbering(slides)
        self.assertTrue(result['valid'])
        self.assertEqual(result['issues'], [])

    def test_validation_fail_gap(self):
        """Test validation fails for gaps in numbering"""
        slides = [{'slide_number': i} for i in [1, 3, 5]]
        result = validate_sequential_numbering(slides)
        self.assertFalse(result['valid'])
        self.assertEqual(len(result['issues']), 1)

    def test_validation_fail_wrong_start(self):
        """Test validation fails for wrong starting number"""
        slides = [{'slide_number': i} for i in [0, 1, 2]]
        result = validate_sequential_numbering(slides)
        self.assertFalse(result['valid'])

    def test_preserves_other_fields(self):
        """Test that other slide fields are preserved"""
        slides = [
            {'slide_number': 5, 'title': 'First', 'type': 'content'},
            {'slide_number': 10, 'title': 'Second', 'body': 'text'}
        ]
        fixed = enforce_sequential_numbering(slides)
        self.assertEqual(fixed[0]['title'], 'First')
        self.assertEqual(fixed[0]['type'], 'content')
        self.assertEqual(fixed[1]['title'], 'Second')
        self.assertEqual(fixed[1]['body'], 'text')


class TestNclexTipFallback(unittest.TestCase):
    """Tests for R4: NCLEX tip required on content slides"""

    def test_fallback_tip_added_to_content(self):
        """Test that fallback tip is added to content slide without tip"""
        slide = {'type': 'content', 'nclex_tip': ''}
        fixed = ensure_nclex_tip(slide, 'fundamentals')
        self.assertTrue(len(fixed['nclex_tip']) > 0)
        self.assertEqual(fixed['nclex_tip_source'], 'fallback')

    def test_existing_tip_preserved(self):
        """Test that existing tip is not overwritten"""
        slide = {'type': 'content', 'nclex_tip': 'My custom tip'}
        fixed = ensure_nclex_tip(slide, 'fundamentals')
        self.assertEqual(fixed['nclex_tip'], 'My custom tip')
        self.assertNotIn('nclex_tip_source', fixed)

    def test_non_content_ignored(self):
        """Test that non-content slides are not modified"""
        slide = {'type': 'vignette', 'nclex_tip': ''}
        fixed = ensure_nclex_tip(slide, 'fundamentals')
        self.assertEqual(fixed['nclex_tip'], '')
        self.assertNotIn('nclex_tip_source', fixed)

    def test_section_intro_ignored(self):
        """Test that section intro slides are not modified"""
        slide = {'type': 'section_intro', 'nclex_tip': ''}
        fixed = ensure_nclex_tip(slide, 'fundamentals')
        self.assertEqual(fixed['nclex_tip'], '')

    def test_all_domains_have_tips(self):
        """Test that all domains have fallback tips"""
        domains = ['fundamentals', 'pharmacology', 'medical_surgical',
                   'ob_maternity', 'pediatric', 'mental_health', 'unknown']
        for domain in domains:
            tip = get_fallback_tip(domain)
            self.assertTrue(len(tip) > 0, f"No tip for {domain}")

    def test_tip_rotation(self):
        """Test that tips rotate through available options"""
        tip1 = get_fallback_tip('fundamentals')
        tip2 = get_fallback_tip('fundamentals')
        tip3 = get_fallback_tip('fundamentals')
        # After 3 calls, should have cycled through all 3 tips
        tip4 = get_fallback_tip('fundamentals')
        self.assertEqual(tip1, tip4)  # Back to first tip

    def test_ensure_all_tips(self):
        """Test batch processing of slides"""
        slides = [
            {'type': 'section_intro'},
            {'type': 'content', 'nclex_tip': ''},
            {'type': 'content', 'nclex_tip': 'Existing'},
            {'type': 'vignette'},
        ]
        fixed = ensure_all_tips(slides, 'pharmacology')

        # Section intro unchanged
        self.assertNotIn('nclex_tip_source', fixed[0])

        # First content slide got fallback
        self.assertTrue(len(fixed[1]['nclex_tip']) > 0)
        self.assertEqual(fixed[1]['nclex_tip_source'], 'fallback')

        # Second content slide preserved
        self.assertEqual(fixed[2]['nclex_tip'], 'Existing')

        # Vignette unchanged
        self.assertNotIn('nclex_tip_source', fixed[3])

    def test_validate_nclex_tips_pass(self):
        """Test validation passes when all content slides have tips"""
        slides = [
            {'type': 'section_intro'},
            {'type': 'content', 'nclex_tip': 'Tip 1'},
            {'type': 'content', 'nclex_tip': 'Tip 2'},
        ]
        result = validate_nclex_tips(slides)
        self.assertTrue(result['valid'])
        self.assertEqual(result['content_slides_checked'], 2)

    def test_validate_nclex_tips_fail(self):
        """Test validation fails when content slides missing tips"""
        slides = [
            {'type': 'content', 'nclex_tip': 'Has tip'},
            {'type': 'content', 'nclex_tip': ''},  # Missing!
            {'type': 'content'},  # Missing nclex_tip field entirely
        ]
        result = validate_nclex_tips(slides)
        self.assertFalse(result['valid'])
        self.assertEqual(len(result['issues']), 2)

    def test_none_tip_handled(self):
        """Test that [None] placeholder is treated as missing"""
        slide = {'type': 'content', 'nclex_tip': '[None]'}
        fixed = ensure_nclex_tip(slide, 'fundamentals')
        self.assertNotEqual(fixed['nclex_tip'], '[None]')
        self.assertEqual(fixed['nclex_tip_source'], 'fallback')

    def test_slide_type_variations(self):
        """Test different slide_type field names"""
        # Using 'type' field
        slide1 = {'type': 'content', 'nclex_tip': ''}
        fixed1 = ensure_nclex_tip(slide1, 'fundamentals')
        self.assertTrue(len(fixed1['nclex_tip']) > 0)

        # Using 'slide_type' field
        slide2 = {'slide_type': 'content', 'nclex_tip': ''}
        fixed2 = ensure_nclex_tip(slide2, 'fundamentals')
        self.assertTrue(len(fixed2['nclex_tip']) > 0)


class TestIntegration(unittest.TestCase):
    """Integration tests for Phase 1 enforcement"""

    def test_full_pipeline(self):
        """Test both enforcements in sequence"""
        slides = [
            {'slide_number': 5, 'type': 'section_intro'},
            {'slide_number': 10, 'type': 'content', 'nclex_tip': ''},
            {'slide_number': 15, 'type': 'content', 'nclex_tip': 'Existing'},
            {'slide_number': 20, 'type': 'vignette'},
            {'slide_number': 1, 'type': 'answer'},  # Wrong number!
        ]

        # Apply numbering first
        slides = enforce_sequential_numbering(slides)

        # Verify numbering
        numbering_result = validate_sequential_numbering(slides)
        self.assertTrue(numbering_result['valid'])

        # Apply tip enforcement
        slides = ensure_all_tips(slides, 'fundamentals')

        # Verify tips
        tip_result = validate_nclex_tips(slides)
        self.assertTrue(tip_result['valid'])

        # Verify final state
        self.assertEqual([s['slide_number'] for s in slides], [1, 2, 3, 4, 5])
        self.assertTrue(len(slides[1]['nclex_tip']) > 0)  # Was empty, now filled
        self.assertEqual(slides[2]['nclex_tip'], 'Existing')  # Preserved


if __name__ == '__main__':
    unittest.main(verbosity=2)
