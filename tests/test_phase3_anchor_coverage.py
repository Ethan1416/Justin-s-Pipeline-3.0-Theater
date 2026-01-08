"""
Unit tests for Phase 3: Anchor Coverage Tracking (R8)

Tests anchor_coverage_tracker.py and anchor_coverage_enforcer.py
"""

import unittest
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from skills.validation.anchor_coverage_tracker import (
    AnchorCoverageTracker, Anchor, parse_blueprint_coverage
)
from skills.enforcement.anchor_coverage_enforcer import (
    ensure_anchor_coverage, generate_anchor_slide, get_anchor_assignment_plan
)


class TestAnchor(unittest.TestCase):
    """Test the Anchor dataclass."""

    def test_anchor_creation(self):
        anchor = Anchor(
            number=1,
            summary="Test Anchor",
            text="Test content",
            flags=["FRONTLOAD"],
            subsection="Test Section"
        )
        self.assertEqual(anchor.number, 1)
        self.assertEqual(anchor.summary, "Test Anchor")
        self.assertTrue(anchor.is_frontload)
        self.assertFalse(anchor.is_xref)

    def test_anchor_xref_flag(self):
        anchor = Anchor(
            number=2,
            summary="XREF Anchor",
            text="Cross reference content",
            flags=["XREF"],
            subsection="Test"
        )
        self.assertTrue(anchor.is_xref)
        self.assertFalse(anchor.is_frontload)

    def test_anchor_equality(self):
        anchor1 = Anchor(number=1, summary="Same", text="", flags=[])
        anchor2 = Anchor(number=2, summary="Same", text="different", flags=["FLAG"])
        self.assertEqual(anchor1, anchor2)  # Equal by summary

    def test_anchor_hash(self):
        anchor1 = Anchor(number=1, summary="Same", text="")
        anchor2 = Anchor(number=2, summary="Same", text="")
        self.assertEqual(hash(anchor1), hash(anchor2))


class TestAnchorTracker(unittest.TestCase):
    """Test the AnchorCoverageTracker class."""

    def setUp(self):
        self.sample_input = {
            "section": {
                "subsections": [
                    {
                        "subsection_name": "Test Subsection",
                        "anchors": [
                            {"anchor_number": 1, "anchor_summary": "Anchor A", "anchor_text": "Text A", "flags": []},
                            {"anchor_number": 2, "anchor_summary": "Anchor B", "anchor_text": "Text B", "flags": ["FRONTLOAD"]},
                        ]
                    }
                ]
            }
        }
        self.tracker = AnchorCoverageTracker.from_input(self.sample_input)

    def test_from_input(self):
        """Test tracker initialization from Step 4 output."""
        self.assertEqual(len(self.tracker.anchors), 2)
        self.assertIn("Anchor A", self.tracker.anchors)
        self.assertIn("Anchor B", self.tracker.anchors)

    def test_mark_covered_single(self):
        """Test marking a single anchor as covered."""
        self.tracker.mark_covered(["Anchor A"], slide_number=2)
        self.assertEqual(len(self.tracker.get_covered()), 1)
        self.assertEqual(len(self.tracker.get_missing()), 1)

    def test_mark_covered_string(self):
        """Test marking with string instead of list."""
        self.tracker.mark_covered("Anchor A", slide_number=2)
        self.assertEqual(len(self.tracker.get_covered()), 1)

    def test_mark_covered_multiple_slides(self):
        """Test anchor covered by multiple slides."""
        self.tracker.mark_covered(["Anchor A"], slide_number=2)
        self.tracker.mark_covered(["Anchor A"], slide_number=3)
        result = self.tracker.validate()
        # Should still show as covered
        self.assertEqual(result['covered_count'], 1)
        # Should have two slide entries
        self.assertEqual(len(result['coverage_details']["Anchor A"]['slides']), 2)

    def test_validate_all_covered(self):
        """Test validation when all anchors are covered."""
        self.tracker.mark_covered(["Anchor A"], slide_number=2)
        self.tracker.mark_covered(["Anchor B"], slide_number=3)
        result = self.tracker.validate()
        self.assertTrue(result['valid'])
        self.assertEqual(result['missing_count'], 0)

    def test_validate_missing(self):
        """Test validation with missing anchors."""
        self.tracker.mark_covered(["Anchor A"], slide_number=2)
        result = self.tracker.validate()
        self.assertFalse(result['valid'])
        self.assertEqual(result['missing_count'], 1)
        self.assertEqual(result['missing_anchors'][0]['summary'], "Anchor B")

    def test_frontload_violation(self):
        """Test detection of FRONTLOAD anchors appearing too late."""
        self.tracker.mark_covered(["Anchor A"], slide_number=2)
        self.tracker.mark_covered(["Anchor B"], slide_number=10)  # Too late for FRONTLOAD
        result = self.tracker.validate()
        self.assertTrue(result['valid'])  # All covered
        self.assertEqual(len(result['frontload_violations']), 1)

    def test_get_coverage_report(self):
        """Test coverage report generation."""
        self.tracker.mark_covered(["Anchor A"], slide_number=2)
        report = self.tracker.get_coverage_report()
        self.assertIn("ANCHOR COVERAGE REPORT", report)
        self.assertIn("MISSING ANCHORS", report)
        self.assertIn("STATUS: FAIL", report)

    def test_empty_tracker(self):
        """Test tracker with no anchors."""
        empty_tracker = AnchorCoverageTracker()
        result = empty_tracker.validate()
        self.assertTrue(result['valid'])
        self.assertEqual(result['total_anchors'], 0)


class TestAnchorEnforcer(unittest.TestCase):
    """Test the anchor coverage enforcer."""

    def test_generate_slide(self):
        """Test slide generation for missing anchor."""
        anchor = Anchor(
            number=1,
            summary="Test Anchor",
            text="This is test content. With multiple sentences.",
            flags=[],
            subsection="Test Section"
        )
        slide = generate_anchor_slide(anchor, slide_number=5)
        self.assertEqual(slide['slide_number'], 5)
        self.assertEqual(slide['anchors_covered'], ["Test Anchor"])
        self.assertEqual(slide['type'], 'content')
        self.assertEqual(slide['subsection'], "Test Section")
        self.assertTrue(slide['_generated_for_coverage'])

    def test_generate_slide_long_header(self):
        """Test slide generation with header that needs truncation."""
        anchor = Anchor(
            number=1,
            summary="This is a very long anchor summary that exceeds the limit",
            text="Content",
            flags=[]
        )
        slide = generate_anchor_slide(anchor, slide_number=1)
        self.assertLessEqual(len(slide['header']), 32)
        self.assertTrue(slide['header'].endswith("..."))

    def test_ensure_coverage_no_changes(self):
        """Test ensure_coverage when all anchors covered."""
        sample_input = {
            "section": {
                "subsections": [{
                    "subsection_name": "Test",
                    "anchors": [
                        {"anchor_number": 1, "anchor_summary": "Anchor A", "anchor_text": "Text A"},
                    ]
                }]
            }
        }
        slides = [
            {'slide_number': 1, 'type': 'content', 'anchors_covered': ['Anchor A']}
        ]
        result = ensure_anchor_coverage(slides, sample_input)
        self.assertEqual(result['added_slides'], 0)
        self.assertTrue(result['coverage_result']['valid'])

    def test_ensure_coverage_adds_slides(self):
        """Test ensure_coverage adds slides for missing anchors."""
        sample_input = {
            "section": {
                "subsections": [{
                    "subsection_name": "Test",
                    "anchors": [
                        {"anchor_number": 1, "anchor_summary": "Anchor A", "anchor_text": "Text A"},
                        {"anchor_number": 2, "anchor_summary": "Anchor B", "anchor_text": "Text B"},
                    ]
                }]
            }
        }
        slides = [
            {'slide_number': 1, 'type': 'content', 'anchors_covered': ['Anchor A']}
        ]
        result = ensure_anchor_coverage(slides, sample_input)
        self.assertEqual(result['added_slides'], 1)
        self.assertTrue(result['coverage_result']['valid'])

    def test_ensure_coverage_inserts_before_vignette(self):
        """Test that new slides are inserted before vignette."""
        sample_input = {
            "section": {
                "subsections": [{
                    "subsection_name": "Test",
                    "anchors": [
                        {"anchor_number": 1, "anchor_summary": "A", "anchor_text": ""},
                        {"anchor_number": 2, "anchor_summary": "B", "anchor_text": ""},
                    ]
                }]
            }
        }
        slides = [
            {'slide_number': 1, 'type': 'section_intro', 'anchors_covered': []},
            {'slide_number': 2, 'type': 'content', 'anchors_covered': ['A']},
            {'slide_number': 3, 'type': 'vignette', 'anchors_covered': []},
            {'slide_number': 4, 'type': 'answer', 'anchors_covered': []},
        ]
        result = ensure_anchor_coverage(slides, sample_input)

        # Find where vignette is now
        vignette_idx = None
        for i, s in enumerate(result['slides']):
            if s['type'] == 'vignette':
                vignette_idx = i
                break

        # Find the generated slide
        gen_idx = None
        for i, s in enumerate(result['slides']):
            if s.get('_generated_for_coverage'):
                gen_idx = i
                break

        self.assertIsNotNone(vignette_idx)
        self.assertIsNotNone(gen_idx)
        self.assertLess(gen_idx, vignette_idx)


class TestAssignmentPlan(unittest.TestCase):
    """Test anchor assignment plan generation."""

    def test_plan_generation(self):
        """Test basic plan generation."""
        sample_input = {
            "section": {
                "subsections": [{
                    "subsection_name": "Test",
                    "anchors": [
                        {"anchor_number": 1, "anchor_summary": "A", "flags": []},
                        {"anchor_number": 2, "anchor_summary": "B", "flags": []},
                        {"anchor_number": 3, "anchor_summary": "C", "flags": []},
                    ]
                }]
            }
        }
        plan = get_anchor_assignment_plan(sample_input)
        # Should have 2 slides (2 anchors per slide, 3 anchors = 2 slides)
        self.assertEqual(len(plan), 2)
        self.assertEqual(plan[0]['slide_number'], 2)  # Starts after intro

    def test_plan_frontload_first(self):
        """Test that FRONTLOAD anchors are assigned first."""
        sample_input = {
            "section": {
                "subsections": [{
                    "subsection_name": "Test",
                    "anchors": [
                        {"anchor_number": 1, "anchor_summary": "Regular", "flags": []},
                        {"anchor_number": 2, "anchor_summary": "Frontload", "flags": ["FRONTLOAD"]},
                        {"anchor_number": 3, "anchor_summary": "Another", "flags": []},
                    ]
                }]
            }
        }
        plan = get_anchor_assignment_plan(sample_input)
        # FRONTLOAD should be in first batch
        self.assertIn("Frontload", plan[0]['anchors'])

    def test_plan_multiple_subsections(self):
        """Test plan with multiple subsections."""
        sample_input = {
            "section": {
                "subsections": [
                    {
                        "subsection_name": "Sub1",
                        "anchors": [
                            {"anchor_number": 1, "anchor_summary": "A", "flags": []},
                        ]
                    },
                    {
                        "subsection_name": "Sub2",
                        "anchors": [
                            {"anchor_number": 2, "anchor_summary": "B", "flags": []},
                        ]
                    }
                ]
            }
        }
        plan = get_anchor_assignment_plan(sample_input)
        self.assertEqual(len(plan), 2)
        self.assertEqual(plan[0]['subsection'], "Sub1")
        self.assertEqual(plan[1]['subsection'], "Sub2")


class TestBlueprintParsing(unittest.TestCase):
    """Test blueprint coverage parsing."""

    def test_parse_blueprint_coverage(self):
        """Test parsing anchor coverage from blueprint text."""
        blueprint = """
SLIDE 2: Test Slide
Type: Content
Anchors Covered: Hand hygiene, Safety precautions

HEADER:
Test Header

SLIDE 3: Another Slide
Type: Content
Anchors Covered: Infection control

HEADER:
Another Header
"""
        coverage = parse_blueprint_coverage(blueprint)
        self.assertIn("Hand hygiene", coverage)
        self.assertIn("Safety precautions", coverage)
        self.assertIn("Infection control", coverage)
        self.assertEqual(coverage["Hand hygiene"], [2])


if __name__ == '__main__':
    unittest.main()
