"""
Step 8 QA Score Calculator Tests
Tests for weighted scoring, deductions, auto-fail conditions, and status determination.

Run: python -m pytest tests/test_step8_qa.py -v
"""

import sys
import unittest
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from skills.validation.score_calculator import (
    calculate_weighted_score,
    apply_deductions,
    check_automatic_fail_conditions,
    generate_score_breakdown,
    determine_status,
    ScoreCalculator,
    DEFAULT_WEIGHTS,
    DEDUCTION_AMOUNTS,
    format_score_report,
    get_quality_thresholds
)


class TestCalculateWeightedScore(unittest.TestCase):
    """Tests for calculate_weighted_score function."""

    def test_perfect_score_all_categories(self):
        """Perfect 100 in all categories returns 100."""
        scores = {
            'outline_adherence': 100,
            'anchor_coverage': 100,
            'line_count': 100,
            'character_count': 100,
            'presentation_timing': 100,
            'nclex_tip_presence': 100,
            'visual_quota': 100,
            'r10_vignette': 100,
            'r11_answer': 100,
            'r14_markers': 100
        }
        result = calculate_weighted_score(scores)
        self.assertEqual(result, 100.0)

    def test_zero_score_all_categories(self):
        """Zero in all categories returns 0."""
        scores = {
            'outline_adherence': 0,
            'anchor_coverage': 0,
            'line_count': 0,
            'character_count': 0,
            'presentation_timing': 0,
            'nclex_tip_presence': 0,
            'visual_quota': 0,
            'r10_vignette': 0,
            'r11_answer': 0,
            'r14_markers': 0
        }
        result = calculate_weighted_score(scores)
        self.assertEqual(result, 0.0)

    def test_weighted_calculation_accuracy(self):
        """Weighted calculation produces expected result."""
        # Using the formula from quality_reviewer.md
        scores = {
            'outline_adherence': 90,       # * 0.10 = 9
            'anchor_coverage': 80,         # * 0.20 = 16
            'line_count': 100,             # * 0.10 = 10
            'character_count': 100,        # * 0.10 = 10
            'presentation_timing': 100,    # * 0.10 = 10
            'nclex_tip_presence': 90,      # * 0.10 = 9
            'visual_quota': 100,           # * 0.10 = 10
            'r10_vignette': 100,           # * 0.10 = 10
            'r11_answer': 100,             # * 0.05 = 5
            'r14_markers': 80              # * 0.05 = 4
        }
        # Expected: 9 + 16 + 10 + 10 + 10 + 9 + 10 + 10 + 5 + 4 = 93
        result = calculate_weighted_score(scores)
        self.assertEqual(result, 93.0)

    def test_accepts_dict_with_raw_score(self):
        """Accepts dictionary with 'raw_score' key."""
        scores = {
            'outline_adherence': {'raw_score': 95, 'issues': []},
            'anchor_coverage': {'raw_score': 88, 'max': 100},
            'line_count': {'raw_score': 100, 'issues': []},
            'character_count': {'raw_score': 92, 'issues': []},
            'presentation_timing': {'raw_score': 100, 'issues': []},
            'nclex_tip_presence': {'raw_score': 95, 'issues': []},
            'visual_quota': {'raw_score': 100, 'issues': []},
            'r10_vignette': {'raw_score': 100, 'issues': []},
            'r11_answer': {'raw_score': 100, 'issues': []},
            'r14_markers': {'raw_score': 85, 'issues': []}
        }
        result = calculate_weighted_score(scores)
        # 9.5 + 17.6 + 10 + 9.2 + 10 + 9.5 + 10 + 10 + 5 + 4.25 = 95.05
        self.assertAlmostEqual(result, 95.05, places=1)

    def test_accepts_dict_with_score_key(self):
        """Accepts dictionary with 'score' key (alternative format)."""
        scores = {
            'outline_adherence': {'score': 90},
            'anchor_coverage': {'score': 90}
        }
        result = calculate_weighted_score(scores)
        # Only 2 categories present, so weights are normalized
        # (90 * 0.10 + 90 * 0.20) / (0.10 + 0.20) = 27 / 0.30 = 90
        self.assertEqual(result, 90.0)

    def test_missing_categories_handled(self):
        """Missing categories are skipped, remaining normalized."""
        scores = {
            'outline_adherence': 100,
            'anchor_coverage': 100
        }
        result = calculate_weighted_score(scores)
        # Only these two categories, weights normalized
        # (100 * 0.10 + 100 * 0.20) / (0.10 + 0.20) = 30 / 0.30 = 100
        self.assertEqual(result, 100.0)

    def test_custom_weights(self):
        """Custom weights can be provided."""
        scores = {
            'outline_adherence': 100,
            'anchor_coverage': 50
        }
        custom_weights = {
            'outline_adherence': 0.50,
            'anchor_coverage': 0.50
        }
        result = calculate_weighted_score(scores, custom_weights)
        # (100 * 0.50 + 50 * 0.50) / 1.0 = 75
        self.assertEqual(result, 75.0)

    def test_clamps_scores_to_valid_range(self):
        """Scores above 100 or below 0 are clamped."""
        scores = {
            'outline_adherence': 150,  # Should be clamped to 100
            'anchor_coverage': -20     # Should be clamped to 0
        }
        result = calculate_weighted_score(scores)
        # (100 * 0.10 + 0 * 0.20) / (0.10 + 0.20) = 10 / 0.30 = 33.33
        self.assertAlmostEqual(result, 33.33, places=1)

    def test_empty_scores_returns_zero(self):
        """Empty scores dictionary returns 0."""
        result = calculate_weighted_score({})
        self.assertEqual(result, 0.0)


class TestApplyDeductions(unittest.TestCase):
    """Tests for apply_deductions function."""

    def test_no_violations_returns_base_score(self):
        """No violations returns original base score."""
        result = apply_deductions(95.0, [])
        self.assertEqual(result, 95.0)

    def test_single_violation_deducts_correctly(self):
        """Single violation applies correct deduction."""
        violations = [{'type': 'char_limit_exceeded'}]  # 3 point deduction
        result = apply_deductions(95.0, violations)
        self.assertEqual(result, 92.0)

    def test_multiple_violations_cumulative(self):
        """Multiple violations are cumulative."""
        violations = [
            {'type': 'char_limit_exceeded'},  # 3 points
            {'type': 'missing_tip'},          # 5 points
            {'type': 'timing_exceeded'}       # 5 points
        ]
        result = apply_deductions(95.0, violations)
        self.assertEqual(result, 82.0)

    def test_violation_with_count_multiplier(self):
        """Violations with count apply multiplier."""
        violations = [{'type': 'char_limit_exceeded', 'count': 3}]  # 3 * 3 = 9
        result = apply_deductions(95.0, violations)
        self.assertEqual(result, 86.0)

    def test_explicit_deduction_amount(self):
        """Explicit deduction overrides type lookup."""
        violations = [{'type': 'custom_error', 'deduction': 15}]
        result = apply_deductions(100.0, violations)
        self.assertEqual(result, 85.0)

    def test_score_cannot_go_below_zero(self):
        """Score is clamped at minimum 0."""
        violations = [{'type': 'missing_anchor', 'count': 20}]  # 10 * 20 = 200
        result = apply_deductions(95.0, violations)
        self.assertEqual(result, 0.0)

    def test_unknown_violation_type_uses_default(self):
        """Unknown violation type uses 5 point default."""
        violations = [{'type': 'some_unknown_violation'}]
        result = apply_deductions(95.0, violations)
        self.assertEqual(result, 90.0)  # 5 point default deduction

    def test_severe_deductions(self):
        """Major violations have significant impact."""
        violations = [
            {'type': 'missing_anchor'},           # 10 points
            {'type': 'missing_fixed_slide'}       # 15 points
        ]
        result = apply_deductions(100.0, violations)
        self.assertEqual(result, 75.0)


class TestCheckAutomaticFailConditions(unittest.TestCase):
    """Tests for check_automatic_fail_conditions function."""

    def test_no_fail_conditions_returns_false(self):
        """No fail conditions returns (False, [])."""
        data = {
            'automatic_fail_conditions': {
                'missing_anchor': False,
                'missing_fixed_slide': False,
                'excessive_char_violations': False,
                'no_presenter_notes': False,
                'no_vignette': False,
                'no_answer': False,
                'no_pause_markers': False
            }
        }
        is_fail, reasons = check_automatic_fail_conditions(data)
        self.assertFalse(is_fail)
        self.assertEqual(len(reasons), 0)

    def test_missing_anchor_triggers_fail(self):
        """Missing anchor is automatic fail."""
        data = {
            'automatic_fail_conditions': {
                'missing_anchor': True
            }
        }
        is_fail, reasons = check_automatic_fail_conditions(data)
        self.assertTrue(is_fail)
        self.assertIn('Missing anchor completely', reasons)

    def test_missing_vignette_triggers_fail(self):
        """Missing vignette (R10) is automatic fail."""
        data = {
            'automatic_fail_conditions': {
                'no_vignette': True
            }
        }
        is_fail, reasons = check_automatic_fail_conditions(data)
        self.assertTrue(is_fail)
        self.assertTrue(any('vignette' in r.lower() for r in reasons))

    def test_missing_answer_triggers_fail(self):
        """Missing answer (R11) is automatic fail."""
        data = {
            'automatic_fail_conditions': {
                'no_answer': True
            }
        }
        is_fail, reasons = check_automatic_fail_conditions(data)
        self.assertTrue(is_fail)
        self.assertTrue(any('answer' in r.lower() for r in reasons))

    def test_no_pause_markers_triggers_fail(self):
        """No PAUSE markers (R14) is automatic fail."""
        data = {
            'automatic_fail_conditions': {
                'no_pause_markers': True
            }
        }
        is_fail, reasons = check_automatic_fail_conditions(data)
        self.assertTrue(is_fail)
        self.assertTrue(any('[PAUSE]' in r for r in reasons))

    def test_excessive_char_violations_triggers_fail(self):
        """More than 3 char violations is automatic fail."""
        data = {
            'char_violations_count': 5
        }
        is_fail, reasons = check_automatic_fail_conditions(data)
        self.assertTrue(is_fail)
        self.assertTrue(any('character limit' in r.lower() for r in reasons))

    def test_no_presenter_notes_triggers_fail(self):
        """No presenter notes is automatic fail."""
        data = {
            'automatic_fail_conditions': {
                'no_presenter_notes': True
            }
        }
        is_fail, reasons = check_automatic_fail_conditions(data)
        self.assertTrue(is_fail)
        self.assertTrue(any('presenter notes' in r.lower() for r in reasons))

    def test_multiple_fail_conditions_all_reported(self):
        """Multiple fail conditions all appear in reasons."""
        data = {
            'automatic_fail_conditions': {
                'missing_anchor': True,
                'no_vignette': True,
                'no_answer': True
            }
        }
        is_fail, reasons = check_automatic_fail_conditions(data)
        self.assertTrue(is_fail)
        self.assertGreaterEqual(len(reasons), 3)

    def test_slides_data_detection(self):
        """Detection from slides data when auto_fail not provided."""
        data = {
            'slides': [
                {'slide_type': 'Content', 'presenter_notes': 'Notes with [PAUSE] marker'},
                {'slide_type': 'Content', 'presenter_notes': 'More notes [PAUSE]'}
            ]
        }
        is_fail, reasons = check_automatic_fail_conditions(data)
        # Should detect missing vignette and answer
        self.assertTrue(is_fail)
        self.assertTrue(any('vignette' in r.lower() for r in reasons))

    def test_category_scores_zero_vignette_fails(self):
        """R10 vignette score of 0 triggers fail."""
        data = {
            'category_scores': {
                'r10_vignette': {'raw_score': 0}
            }
        }
        is_fail, reasons = check_automatic_fail_conditions(data)
        self.assertTrue(is_fail)


class TestGenerateScoreBreakdown(unittest.TestCase):
    """Tests for generate_score_breakdown function."""

    def test_breakdown_includes_all_categories(self):
        """Breakdown includes all provided categories."""
        scores = {
            'outline_adherence': 95,
            'anchor_coverage': 88,
            'line_count': 100
        }
        breakdown = generate_score_breakdown(scores)
        self.assertEqual(len(breakdown['categories']), 3)

    def test_breakdown_calculates_contributions(self):
        """Each category shows weighted contribution."""
        scores = {
            'outline_adherence': 100,  # 100 * 0.10 = 10
            'anchor_coverage': 100     # 100 * 0.20 = 20
        }
        breakdown = generate_score_breakdown(scores)
        categories = breakdown['categories']

        outline_cat = next(c for c in categories if c['category'] == 'outline_adherence')
        self.assertEqual(outline_cat['weighted_contribution'], 10.0)

        anchor_cat = next(c for c in categories if c['category'] == 'anchor_coverage')
        self.assertEqual(anchor_cat['weighted_contribution'], 20.0)

    def test_breakdown_includes_status_per_category(self):
        """Each category has PASS/WARN/FAIL status."""
        scores = {
            'outline_adherence': 90,   # PASS (>= 80)
            'anchor_coverage': 70,     # WARN (60-79)
            'line_count': 50           # FAIL (< 60)
        }
        breakdown = generate_score_breakdown(scores)

        for cat in breakdown['categories']:
            if cat['category'] == 'outline_adherence':
                self.assertEqual(cat['status'], 'PASS')
            elif cat['category'] == 'anchor_coverage':
                self.assertEqual(cat['status'], 'WARN')
            elif cat['category'] == 'line_count':
                self.assertEqual(cat['status'], 'FAIL')

    def test_breakdown_summary_counts(self):
        """Summary includes counts of passing/warning/failing categories."""
        scores = {
            'outline_adherence': 90,
            'anchor_coverage': 70,
            'line_count': 50
        }
        breakdown = generate_score_breakdown(scores)
        summary = breakdown['summary']

        self.assertEqual(summary['total_categories'], 3)
        self.assertEqual(summary['passing_categories'], 1)
        self.assertEqual(summary['warning_categories'], 1)
        self.assertEqual(summary['failing_categories'], 1)

    def test_breakdown_includes_issues(self):
        """Issues from category scores are preserved."""
        scores = {
            'anchor_coverage': {
                'raw_score': 88,
                'issues': ['Anchor ACE inhibitor not covered']
            }
        }
        breakdown = generate_score_breakdown(scores)
        anchor_cat = breakdown['categories'][0]
        self.assertEqual(len(anchor_cat['issues']), 1)
        self.assertIn('ACE inhibitor', anchor_cat['issues'][0])

    def test_breakdown_total_score_matches_calculate(self):
        """Breakdown total matches calculate_weighted_score."""
        scores = {
            'outline_adherence': 95,
            'anchor_coverage': 88,
            'line_count': 100,
            'character_count': 92,
            'presentation_timing': 100,
            'nclex_tip_presence': 95,
            'visual_quota': 100,
            'r10_vignette': 100,
            'r11_answer': 100,
            'r14_markers': 85
        }
        breakdown = generate_score_breakdown(scores)
        direct_calc = calculate_weighted_score(scores)

        self.assertAlmostEqual(breakdown['total_weighted_score'], direct_calc, places=1)


class TestDetermineStatus(unittest.TestCase):
    """Tests for determine_status function."""

    def test_pass_at_90_no_auto_fail(self):
        """Score >= 90 with no auto-fail returns PASS."""
        self.assertEqual(determine_status(90.0, False), 'PASS')
        self.assertEqual(determine_status(95.0, False), 'PASS')
        self.assertEqual(determine_status(100.0, False), 'PASS')

    def test_needs_revision_80_to_89(self):
        """Score 80-89 with no auto-fail returns NEEDS_REVISION."""
        self.assertEqual(determine_status(80.0, False), 'NEEDS_REVISION')
        self.assertEqual(determine_status(85.0, False), 'NEEDS_REVISION')
        self.assertEqual(determine_status(89.9, False), 'NEEDS_REVISION')

    def test_fail_below_80(self):
        """Score < 80 returns FAIL."""
        self.assertEqual(determine_status(79.9, False), 'FAIL')
        self.assertEqual(determine_status(50.0, False), 'FAIL')
        self.assertEqual(determine_status(0.0, False), 'FAIL')

    def test_auto_fail_overrides_high_score(self):
        """Auto-fail condition returns FAIL regardless of score."""
        self.assertEqual(determine_status(100.0, True), 'FAIL')
        self.assertEqual(determine_status(95.0, True), 'FAIL')
        self.assertEqual(determine_status(90.0, True), 'FAIL')

    def test_boundary_conditions(self):
        """Boundary values handled correctly."""
        self.assertEqual(determine_status(89.999, False), 'NEEDS_REVISION')
        self.assertEqual(determine_status(90.0, False), 'PASS')
        self.assertEqual(determine_status(79.999, False), 'FAIL')
        self.assertEqual(determine_status(80.0, False), 'NEEDS_REVISION')


class TestScoreCalculatorClass(unittest.TestCase):
    """Tests for ScoreCalculator class interface."""

    def setUp(self):
        self.calculator = ScoreCalculator()

    def test_calculate_method(self):
        """Calculate method works and records history."""
        scores = {'outline_adherence': 100, 'anchor_coverage': 100}
        result = self.calculator.calculate(scores)
        self.assertEqual(result, 100.0)
        self.assertEqual(len(self.calculator.history), 1)

    def test_custom_weights_can_be_set(self):
        """Custom weights can be applied."""
        self.calculator.set_custom_weights({'outline_adherence': 0.50})
        self.assertEqual(self.calculator.weights['outline_adherence'], 0.50)

    def test_get_breakdown_method(self):
        """Get breakdown method returns detailed breakdown."""
        scores = {'outline_adherence': 90, 'anchor_coverage': 85}
        breakdown = self.calculator.get_breakdown(scores)
        self.assertIn('categories', breakdown)
        self.assertIn('total_weighted_score', breakdown)

    def test_check_auto_fail_method(self):
        """Check auto fail method works."""
        data = {'automatic_fail_conditions': {'missing_anchor': True}}
        is_fail, reasons = self.calculator.check_auto_fail(data)
        self.assertTrue(is_fail)

    def test_get_status_method(self):
        """Get status method returns correct status."""
        self.assertEqual(self.calculator.get_status(95.0, False), 'PASS')
        self.assertEqual(self.calculator.get_status(85.0, False), 'NEEDS_REVISION')
        self.assertEqual(self.calculator.get_status(75.0, False), 'FAIL')

    def test_generate_report_method(self):
        """Generate report produces formatted string."""
        scores = {
            'outline_adherence': 95,
            'anchor_coverage': 88
        }
        report = self.calculator.generate_report(scores)
        self.assertIn('QA SCORE REPORT', report)
        self.assertIn('Outline Adherence', report)


class TestFormatScoreReport(unittest.TestCase):
    """Tests for format_score_report function."""

    def test_report_includes_header(self):
        """Report includes appropriate header."""
        scores = {'outline_adherence': 100}
        report = format_score_report(scores)
        self.assertIn('STEP 8', report)
        self.assertIn('QA SCORE REPORT', report)

    def test_report_shows_status(self):
        """Report shows determined status."""
        scores = {
            'outline_adherence': 95,
            'anchor_coverage': 95,
            'line_count': 95,
            'character_count': 95,
            'presentation_timing': 95,
            'nclex_tip_presence': 95,
            'visual_quota': 95,
            'r10_vignette': 95,
            'r11_answer': 95,
            'r14_markers': 95
        }
        report = format_score_report(scores)
        self.assertIn('STATUS: PASS', report)

    def test_report_shows_auto_fail_reasons(self):
        """Report includes auto-fail reasons when triggered."""
        scores = {'outline_adherence': 100}
        blueprint = {'automatic_fail_conditions': {'no_vignette': True}}
        report = format_score_report(scores, blueprint_data=blueprint)
        self.assertIn('AUTOMATIC FAIL', report)
        self.assertIn('vignette', report.lower())


class TestIntegrationWithSampleData(unittest.TestCase):
    """Integration tests using sample QA input data format."""

    def test_sample_qa_input_format(self):
        """Process sample QA input format successfully."""
        # Simulates data from samples/step8_qa/sample_qa_input.json
        sample_input = {
            "metadata": {
                "domain": "Pharmacology",
                "section": "Cardiovascular Medications",
                "step": "Step 8 QA Input"
            },
            "category_scores": {
                "outline_adherence": {"raw_score": 95, "max": 100, "weight": 0.10, "issues": []},
                "anchor_coverage": {"raw_score": 88, "max": 100, "weight": 0.20,
                                   "issues": ["Anchor 'ACE inhibitor mechanism' not fully explained"]},
                "line_count": {"raw_score": 100, "max": 100, "weight": 0.10, "issues": []},
                "character_count": {"raw_score": 92, "max": 100, "weight": 0.10,
                                   "issues": ["Slide 5: Body line 3 has 68 chars (max 66)"]},
                "presentation_timing": {"raw_score": 100, "max": 100, "weight": 0.10, "issues": []},
                "nclex_tip_presence": {"raw_score": 95, "max": 100, "weight": 0.10,
                                      "issues": ["Slide 12: Tip could be more specific to NCLEX"]},
                "visual_quota": {"raw_score": 100, "max": 100, "weight": 0.10, "issues": []},
                "r10_vignette": {"raw_score": 100, "max": 100, "weight": 0.10, "issues": [],
                                "slides_checked": 1, "slides_passed": 1},
                "r11_answer": {"raw_score": 100, "max": 100, "weight": 0.05, "issues": [],
                              "slides_checked": 1, "slides_passed": 1},
                "r14_markers": {"raw_score": 85, "max": 100, "weight": 0.05,
                               "issues": ["Slide 7: Only 1 [PAUSE] marker (min 2)"],
                               "slides_checked": 15, "slides_passed": 14,
                               "total_pause_markers": 31, "total_emphasis_markers": 18}
            },
            "automatic_fail_conditions": {
                "missing_anchor": False,
                "missing_fixed_slide": False,
                "excessive_char_violations": False,
                "no_presenter_notes": False,
                "no_vignette": False,
                "no_answer": False,
                "no_pause_markers": False
            }
        }

        # Calculate weighted score
        weighted_score = calculate_weighted_score(sample_input['category_scores'])

        # Check auto-fail
        is_fail, reasons = check_automatic_fail_conditions(sample_input)

        # Determine status
        status = determine_status(weighted_score, is_fail)

        # Generate breakdown
        breakdown = generate_score_breakdown(sample_input['category_scores'])

        # Assertions
        self.assertGreater(weighted_score, 90)  # Should pass
        self.assertFalse(is_fail)
        self.assertEqual(status, 'PASS')
        self.assertEqual(len(breakdown['categories']), 10)

    def test_full_workflow_with_deductions(self):
        """Full workflow including deductions."""
        scores = {
            'outline_adherence': 100,
            'anchor_coverage': 100,
            'line_count': 100,
            'character_count': 100,
            'presentation_timing': 100,
            'nclex_tip_presence': 100,
            'visual_quota': 100,
            'r10_vignette': 100,
            'r11_answer': 100,
            'r14_markers': 100
        }

        base_score = calculate_weighted_score(scores)
        self.assertEqual(base_score, 100.0)

        # Apply some violations
        violations = [
            {'type': 'char_limit_exceeded', 'count': 2},  # -6
            {'type': 'marker_pause_missing'}              # -5
        ]
        adjusted_score = apply_deductions(base_score, violations)
        self.assertEqual(adjusted_score, 89.0)

        # With violations, status changes
        status = determine_status(adjusted_score, False)
        self.assertEqual(status, 'NEEDS_REVISION')


class TestEdgeCases(unittest.TestCase):
    """Tests for edge cases and error handling."""

    def test_none_values_in_scores(self):
        """None values are handled gracefully."""
        scores = {
            'outline_adherence': None,
            'anchor_coverage': 100
        }
        result = calculate_weighted_score(scores)
        # Should process only anchor_coverage
        self.assertEqual(result, 100.0)

    def test_empty_blueprint_data(self):
        """Empty blueprint data doesn't crash."""
        is_fail, reasons = check_automatic_fail_conditions({})
        # Empty data shouldn't trigger fails from pre-computed conditions
        self.assertIsInstance(is_fail, bool)
        self.assertIsInstance(reasons, list)

    def test_partial_category_scores(self):
        """Partial category scores work correctly."""
        scores = {
            'outline_adherence': 100
        }
        breakdown = generate_score_breakdown(scores)
        self.assertEqual(len(breakdown['categories']), 1)
        self.assertEqual(breakdown['total_weighted_score'], 100.0)

    def test_weights_sum_verification(self):
        """Default weights sum to 1.0."""
        total_weight = sum(DEFAULT_WEIGHTS.values())
        self.assertAlmostEqual(total_weight, 1.0, places=5)


if __name__ == '__main__':
    unittest.main()
