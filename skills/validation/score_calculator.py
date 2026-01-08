"""
Score Calculator - Calculate weighted QA scores for Step 8 in NCLEX pipeline.

This module provides functions for calculating weighted scores, applying deductions,
checking automatic fail conditions, and determining pass/fail status based on
the scoring criteria defined in config/constraints.yaml.

Usage:
    from skills.validation.score_calculator import (
        calculate_weighted_score,
        apply_deductions,
        check_automatic_fail_conditions,
        generate_score_breakdown,
        determine_status
    )

    weighted_score = calculate_weighted_score(category_scores, weights)
    adjusted_score = apply_deductions(base_score, violations)
    is_fail, reasons = check_automatic_fail_conditions(blueprint_data)
    breakdown = generate_score_breakdown(category_scores, weights)
    status = determine_status(score, has_auto_fail)
"""

from pathlib import Path
from typing import Dict, List, Tuple, Any, Optional
from dataclasses import dataclass, field
import yaml


@dataclass
class ScoreBreakdownItem:
    """Represents a single category's score breakdown."""
    category: str
    raw_score: float
    weight: float
    weighted_contribution: float
    max_possible: float
    issues: List[str] = field(default_factory=list)


@dataclass
class ScoreBreakdown:
    """Container for complete score breakdown."""
    categories: List[ScoreBreakdownItem]
    total_weighted_score: float
    total_max_possible: float
    percentage: float


# Default weights from quality_reviewer.md
DEFAULT_WEIGHTS = {
    'outline_adherence': 0.10,
    'anchor_coverage': 0.20,
    'line_count': 0.10,
    'character_count': 0.10,
    'presentation_timing': 0.10,
    'nclex_tip_presence': 0.10,
    'visual_quota': 0.10,
    'r10_vignette': 0.10,
    'r11_answer': 0.05,
    'r14_markers': 0.05
}

# Deduction amounts by violation type
DEDUCTION_AMOUNTS = {
    'missing_anchor': 10,
    'mispositioned_frontload_anchor': 5,
    'missing_fixed_slide': 15,
    'incomplete_fixed_slide': 5,
    'line_limit_exceeded': 5,
    'char_limit_exceeded': 3,
    'timing_exceeded': 5,
    'missing_tip': 5,
    'inappropriate_tip': 2,
    'below_visual_minimum': 10,
    'exceeds_visual_maximum': 5,
    'vignette_missing_option': 25,
    'vignette_wrong_format': 50,
    'vignette_stem_issue': 50,
    'answer_missing_rationale': 50,
    'answer_missing_distractor_analysis': 50,
    'answer_missing_correct_label': 75,
    'marker_pause_missing': 5,
    'marker_emphasis_missing': 3
}


def _load_constraints() -> Dict:
    """Load constraints from config/constraints.yaml."""
    base_path = Path(__file__).parent.parent.parent
    config_path = base_path / "config" / "constraints.yaml"

    if config_path.exists():
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except Exception as e:
            print(f"Warning: Could not load constraints: {e}")

    return {}


def calculate_weighted_score(
    category_scores: Dict[str, Any],
    weights: Optional[Dict[str, float]] = None
) -> float:
    """
    Calculate the weighted average score from category scores.

    The formula from quality_reviewer.md:
        score = (outline * 0.10 + anchor * 0.20 + line_count * 0.10 +
                 char_count * 0.10 + timing * 0.10 + nclex_tip * 0.10 +
                 visual_quota * 0.10 + vignette * 0.10 + answer * 0.05 +
                 marker * 0.05)

    Args:
        category_scores: Dictionary with category names as keys. Each value can be:
            - An integer/float score (0-100)
            - A dict with 'raw_score' or 'score' key
        weights: Optional dictionary of weights per category (default: DEFAULT_WEIGHTS)

    Returns:
        Weighted average score (0-100)

    Examples:
        >>> scores = {'outline_adherence': 95, 'anchor_coverage': 88, ...}
        >>> calculate_weighted_score(scores)
        91.5
    """
    if weights is None:
        weights = DEFAULT_WEIGHTS.copy()

    total_weighted = 0.0
    total_weight = 0.0

    for category, weight in weights.items():
        score_data = category_scores.get(category)

        if score_data is None:
            continue

        # Extract raw score from various formats
        if isinstance(score_data, (int, float)):
            raw_score = float(score_data)
        elif isinstance(score_data, dict):
            raw_score = float(score_data.get('raw_score', score_data.get('score', 0)))
        else:
            raw_score = 0.0

        # Clamp score to 0-100 range
        raw_score = max(0.0, min(100.0, raw_score))

        total_weighted += raw_score * weight
        total_weight += weight

    # Normalize if weights don't sum to 1.0
    if total_weight > 0:
        # Scale to 100 based on actual weight sum
        return round(total_weighted / total_weight, 2)

    return 0.0


def apply_deductions(
    base_score: float,
    violations: List[Dict[str, Any]]
) -> float:
    """
    Apply deductions to base score based on violations.

    Each violation type has a specific deduction amount defined in DEDUCTION_AMOUNTS.
    The score cannot go below 0.

    Args:
        base_score: The initial score (0-100)
        violations: List of violation dictionaries with 'type' key
            Each violation may have:
            - 'type': Violation type string (e.g., 'missing_anchor')
            - 'deduction': Optional specific deduction amount
            - 'count': Optional count for repeated violations

    Returns:
        Adjusted score after deductions (0-100)

    Examples:
        >>> violations = [{'type': 'char_limit_exceeded', 'count': 2}]
        >>> apply_deductions(95.0, violations)
        89.0
    """
    if not violations:
        return base_score

    total_deduction = 0.0

    for violation in violations:
        violation_type = violation.get('type', '')

        # Check for explicit deduction amount
        if 'deduction' in violation:
            deduction = float(violation['deduction'])
        else:
            # Look up deduction from DEDUCTION_AMOUNTS
            deduction = DEDUCTION_AMOUNTS.get(violation_type, 5)  # Default 5 point deduction

        # Apply count multiplier if present
        count = violation.get('count', 1)
        total_deduction += deduction * count

    adjusted_score = base_score - total_deduction
    return max(0.0, adjusted_score)


def check_automatic_fail_conditions(
    blueprint_data: Dict[str, Any]
) -> Tuple[bool, List[str]]:
    """
    Check for automatic fail conditions in blueprint data.

    Automatic fail conditions from quality_reviewer.md:
    - Missing anchor completely
    - Missing fixed slide (Section Intro, Vignette, Answer)
    - More than 3 character limit violations
    - No presenter notes on any slide
    - No vignette slide (R10 violation)
    - No answer slide (R11 violation)
    - No [PAUSE] markers in any slide (R14 violation)

    Args:
        blueprint_data: Dictionary containing blueprint information with keys:
            - 'slides': List of slide dictionaries
            - 'anchors': List of required anchors (optional)
            - 'anchor_coverage': Dict with coverage info (optional)
            - 'category_scores': Dict with category scores (optional)
            - 'automatic_fail_conditions': Dict with pre-computed conditions (optional)
            - 'char_violations_count': Number of character violations (optional)

    Returns:
        Tuple of (is_fail: bool, list_of_reasons: List[str])

    Examples:
        >>> data = {'slides': [...], 'automatic_fail_conditions': {'no_vignette': True}}
        >>> is_fail, reasons = check_automatic_fail_conditions(data)
        >>> is_fail
        True
        >>> reasons
        ['No vignette slide present (R10 violation)']
    """
    reasons = []

    # Check pre-computed automatic fail conditions if present
    auto_fail = blueprint_data.get('automatic_fail_conditions', {})

    if auto_fail.get('missing_anchor', False):
        reasons.append("Missing anchor completely")

    if auto_fail.get('missing_fixed_slide', False):
        reasons.append("Missing required fixed slide")

    if auto_fail.get('excessive_char_violations', False):
        reasons.append("More than 3 character limit violations")

    if auto_fail.get('no_presenter_notes', False):
        reasons.append("No presenter notes on any slide")

    if auto_fail.get('no_vignette', False):
        reasons.append("No vignette slide present (R10 violation)")

    if auto_fail.get('no_answer', False):
        reasons.append("No answer slide present (R11 violation)")

    if auto_fail.get('no_pause_markers', False):
        reasons.append("No [PAUSE] markers in any slide (R14 violation)")

    # Additional checks from slides data if auto_fail not provided
    slides = blueprint_data.get('slides', [])

    if slides and not auto_fail:
        # Check for required slide types
        slide_types = [s.get('slide_type', '').lower() for s in slides]

        has_vignette = any('vignette' in st for st in slide_types)
        has_answer = any('answer' in st for st in slide_types)
        has_intro = any('intro' in st or 'section intro' in st for st in slide_types)

        if not has_vignette and 'no_vignette' not in [r.lower() for r in reasons]:
            reasons.append("No vignette slide present (R10 violation)")

        if not has_answer and 'no_answer' not in [r.lower() for r in reasons]:
            reasons.append("No answer slide present (R11 violation)")

        # Check for presenter notes
        has_any_notes = any(
            s.get('presenter_notes', '').strip() or s.get('notes', '').strip()
            for s in slides
        )
        if not has_any_notes:
            if "No presenter notes on any slide" not in reasons:
                reasons.append("No presenter notes on any slide")

        # Check for PAUSE markers
        has_pause_marker = any(
            '[PAUSE]' in (s.get('presenter_notes', '') + s.get('notes', ''))
            for s in slides
        )
        if not has_pause_marker:
            if "No [PAUSE] markers" not in str(reasons):
                reasons.append("No [PAUSE] markers in any slide (R14 violation)")

    # Check character violation count
    char_violations = blueprint_data.get('char_violations_count', 0)
    if char_violations > 3 and "character limit violations" not in str(reasons):
        reasons.append(f"More than 3 character limit violations ({char_violations} found)")

    # Check category scores for specific failures
    category_scores = blueprint_data.get('category_scores', {})

    # R10 Vignette check from scores
    vignette_score = category_scores.get('r10_vignette', {})
    if isinstance(vignette_score, dict):
        if vignette_score.get('raw_score', vignette_score.get('score', 100)) == 0:
            if "vignette" not in str(reasons).lower():
                reasons.append("No vignette slide present (R10 violation)")

    # R11 Answer check from scores
    answer_score = category_scores.get('r11_answer', {})
    if isinstance(answer_score, dict):
        if answer_score.get('raw_score', answer_score.get('score', 100)) == 0:
            if "answer" not in str(reasons).lower():
                reasons.append("No answer slide present (R11 violation)")

    # R14 Markers check from scores
    marker_score = category_scores.get('r14_markers', {})
    if isinstance(marker_score, dict):
        if marker_score.get('raw_score', marker_score.get('score', 100)) == 0:
            if "[PAUSE] markers" not in str(reasons):
                reasons.append("No [PAUSE] markers in any slide (R14 violation)")

    # Anchor coverage check
    anchor_coverage = blueprint_data.get('anchor_coverage', {})
    if isinstance(anchor_coverage, dict):
        missing_anchors = anchor_coverage.get('missing_anchors', [])
        if missing_anchors and "Missing anchor" not in str(reasons):
            reasons.append(f"Missing anchor completely: {', '.join(missing_anchors[:3])}")

    is_fail = len(reasons) > 0
    return is_fail, reasons


def generate_score_breakdown(
    category_scores: Dict[str, Any],
    weights: Optional[Dict[str, float]] = None
) -> Dict[str, Any]:
    """
    Generate a detailed breakdown showing each category's contribution to the total score.

    Args:
        category_scores: Dictionary with category names as keys. Each value can be:
            - An integer/float score (0-100)
            - A dict with 'raw_score' or 'score' key and optional 'issues' list
        weights: Optional dictionary of weights per category (default: DEFAULT_WEIGHTS)

    Returns:
        Dictionary with detailed breakdown including:
        - 'categories': List of category breakdowns
        - 'total_weighted_score': Final weighted score
        - 'total_weight_used': Sum of weights for categories with scores
        - 'summary': Summary statistics

    Examples:
        >>> scores = {'outline_adherence': {'raw_score': 95, 'issues': []}, ...}
        >>> breakdown = generate_score_breakdown(scores)
        >>> breakdown['total_weighted_score']
        91.5
    """
    if weights is None:
        weights = DEFAULT_WEIGHTS.copy()

    categories = []
    total_weighted = 0.0
    total_max_possible = 0.0
    total_weight_used = 0.0

    category_display_names = {
        'outline_adherence': 'Outline Adherence',
        'anchor_coverage': 'Anchor Coverage',
        'line_count': 'Line Count',
        'character_count': 'Character Count',
        'presentation_timing': 'Presentation Timing',
        'nclex_tip_presence': 'NCLEX Tip Presence',
        'visual_quota': 'Visual Quota',
        'r10_vignette': 'Vignette Structure (R10)',
        'r11_answer': 'Answer Structure (R11)',
        'r14_markers': 'Presenter Markers (R14)'
    }

    for category, weight in weights.items():
        score_data = category_scores.get(category)

        if score_data is None:
            # Category not present, skip
            continue

        # Extract raw score and issues
        if isinstance(score_data, (int, float)):
            raw_score = float(score_data)
            issues = []
        elif isinstance(score_data, dict):
            raw_score = float(score_data.get('raw_score', score_data.get('score', 0)))
            issues = score_data.get('issues', [])
        else:
            raw_score = 0.0
            issues = []

        # Clamp score to 0-100 range
        raw_score = max(0.0, min(100.0, raw_score))

        # Calculate weighted contribution
        weighted_contribution = raw_score * weight
        max_possible = 100.0 * weight

        total_weighted += weighted_contribution
        total_max_possible += max_possible
        total_weight_used += weight

        display_name = category_display_names.get(category, category)

        categories.append({
            'category': category,
            'display_name': display_name,
            'raw_score': raw_score,
            'max_score': 100,
            'weight': weight,
            'weight_percent': f"{weight * 100:.0f}%",
            'weighted_contribution': round(weighted_contribution, 2),
            'max_possible': round(max_possible, 2),
            'issues': issues,
            'status': 'PASS' if raw_score >= 80 else ('WARN' if raw_score >= 60 else 'FAIL')
        })

    # Calculate final percentage
    if total_weight_used > 0:
        final_score = total_weighted / total_weight_used
    else:
        final_score = 0.0

    # Build summary
    passing_categories = len([c for c in categories if c['raw_score'] >= 80])
    warning_categories = len([c for c in categories if 60 <= c['raw_score'] < 80])
    failing_categories = len([c for c in categories if c['raw_score'] < 60])

    return {
        'categories': categories,
        'total_weighted_score': round(final_score, 2),
        'total_max_possible': round(total_max_possible, 2),
        'total_weight_used': round(total_weight_used, 2),
        'summary': {
            'total_categories': len(categories),
            'passing_categories': passing_categories,
            'warning_categories': warning_categories,
            'failing_categories': failing_categories,
            'lowest_category': min(categories, key=lambda x: x['raw_score'])['display_name'] if categories else None,
            'highest_category': max(categories, key=lambda x: x['raw_score'])['display_name'] if categories else None
        }
    }


def determine_status(
    score: float,
    has_auto_fail: bool
) -> str:
    """
    Determine the QA status based on score and automatic fail conditions.

    Status criteria from quality_reviewer.md:
    - PASS: score >= 90 AND no auto-fail conditions
    - NEEDS_REVISION: 80 <= score < 90 AND no auto-fail conditions
    - FAIL: score < 80 OR has auto-fail conditions

    Args:
        score: The weighted score (0-100)
        has_auto_fail: Whether any automatic fail condition is triggered

    Returns:
        Status string: "PASS", "NEEDS_REVISION", or "FAIL"

    Examples:
        >>> determine_status(95.0, False)
        'PASS'
        >>> determine_status(95.0, True)
        'FAIL'
        >>> determine_status(85.0, False)
        'NEEDS_REVISION'
        >>> determine_status(75.0, False)
        'FAIL'
    """
    # Automatic fail conditions override score
    if has_auto_fail:
        return "FAIL"

    # Score-based status
    if score >= 90:
        return "PASS"
    elif score >= 80:
        return "NEEDS_REVISION"
    else:
        return "FAIL"


def get_quality_thresholds() -> Dict[str, int]:
    """
    Get quality gate thresholds from config/constraints.yaml.

    Returns:
        Dictionary with 'pass_threshold' and 'warn_threshold'
    """
    config = _load_constraints()
    quality_gates = config.get('quality_gates', {}).get('step_8_qa', {})

    return {
        'pass_threshold': quality_gates.get('pass_threshold', 90),
        'warn_threshold': quality_gates.get('warn_threshold', 80),
        'max_retry_iterations': quality_gates.get('max_retry_iterations', 3)
    }


def format_score_report(
    category_scores: Dict[str, Any],
    weights: Optional[Dict[str, float]] = None,
    blueprint_data: Optional[Dict[str, Any]] = None
) -> str:
    """
    Generate a formatted text report of the QA scores.

    Args:
        category_scores: Dictionary of category scores
        weights: Optional custom weights
        blueprint_data: Optional blueprint data for auto-fail checks

    Returns:
        Formatted string report
    """
    breakdown = generate_score_breakdown(category_scores, weights)
    weighted_score = breakdown['total_weighted_score']

    # Check auto-fail conditions
    if blueprint_data:
        has_auto_fail, fail_reasons = check_automatic_fail_conditions(blueprint_data)
    else:
        has_auto_fail = False
        fail_reasons = []

    status = determine_status(weighted_score, has_auto_fail)

    lines = [
        "=" * 60,
        "STEP 8: QA SCORE REPORT",
        "=" * 60,
        "",
        "CATEGORY SCORES",
        "-" * 60,
        f"{'Category':<35} {'Score':>8} {'Weight':>8} {'Contrib':>8}",
        "-" * 60
    ]

    for cat in breakdown['categories']:
        lines.append(
            f"{cat['display_name']:<35} {cat['raw_score']:>7.0f} {cat['weight_percent']:>8} {cat['weighted_contribution']:>8.1f}"
        )

    lines.extend([
        "-" * 60,
        f"{'TOTAL WEIGHTED SCORE':<35} {'':>8} {'':>8} {weighted_score:>8.1f}",
        "=" * 60,
        "",
        f"STATUS: {status}",
    ])

    if has_auto_fail:
        lines.append("")
        lines.append("AUTOMATIC FAIL CONDITIONS TRIGGERED:")
        for reason in fail_reasons:
            lines.append(f"  - {reason}")

    if breakdown['summary']['failing_categories'] > 0:
        lines.append("")
        lines.append("CATEGORIES NEEDING ATTENTION:")
        for cat in breakdown['categories']:
            if cat['raw_score'] < 80:
                lines.append(f"  - {cat['display_name']}: {cat['raw_score']:.0f}/100")
                for issue in cat['issues'][:3]:
                    lines.append(f"      * {issue}")

    lines.append("=" * 60)

    return "\n".join(lines)


# Convenience class for stateful scoring
class ScoreCalculator:
    """
    Class-based interface for score calculation.

    Provides a stateful interface that tracks scoring history
    and provides additional utility methods.
    """

    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize ScoreCalculator.

        Args:
            config_path: Optional path to constraints.yaml
        """
        self.config = _load_constraints()
        self.weights = DEFAULT_WEIGHTS.copy()
        self.history: List[Dict] = []

    def set_custom_weights(self, weights: Dict[str, float]) -> None:
        """Set custom category weights."""
        self.weights.update(weights)

    def calculate(self, category_scores: Dict[str, Any]) -> float:
        """Calculate weighted score and record in history."""
        score = calculate_weighted_score(category_scores, self.weights)
        self.history.append({
            'scores': category_scores,
            'result': score
        })
        return score

    def get_breakdown(self, category_scores: Dict[str, Any]) -> Dict:
        """Generate detailed score breakdown."""
        return generate_score_breakdown(category_scores, self.weights)

    def check_auto_fail(self, blueprint_data: Dict) -> Tuple[bool, List[str]]:
        """Check for automatic fail conditions."""
        return check_automatic_fail_conditions(blueprint_data)

    def get_status(self, score: float, has_auto_fail: bool) -> str:
        """Determine status from score and auto-fail."""
        return determine_status(score, has_auto_fail)

    def generate_report(
        self,
        category_scores: Dict[str, Any],
        blueprint_data: Optional[Dict] = None
    ) -> str:
        """Generate formatted score report."""
        return format_score_report(category_scores, self.weights, blueprint_data)


if __name__ == "__main__":
    print("Score Calculator - NCLEX Pipeline Step 8 QA")
    print("=" * 60)

    # Demo with sample data
    sample_scores = {
        'outline_adherence': {'raw_score': 95, 'issues': []},
        'anchor_coverage': {'raw_score': 88, 'issues': ['Anchor ACE inhibitor not fully covered']},
        'line_count': {'raw_score': 100, 'issues': []},
        'character_count': {'raw_score': 92, 'issues': ['Slide 5 body line 3 exceeds limit']},
        'presentation_timing': {'raw_score': 100, 'issues': []},
        'nclex_tip_presence': {'raw_score': 95, 'issues': []},
        'visual_quota': {'raw_score': 100, 'issues': []},
        'r10_vignette': {'raw_score': 100, 'issues': []},
        'r11_answer': {'raw_score': 100, 'issues': []},
        'r14_markers': {'raw_score': 85, 'issues': ['Slide 7 has only 1 PAUSE marker']}
    }

    sample_blueprint = {
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

    # Calculate and display
    calculator = ScoreCalculator()
    report = calculator.generate_report(sample_scores, sample_blueprint)
    print(report)
