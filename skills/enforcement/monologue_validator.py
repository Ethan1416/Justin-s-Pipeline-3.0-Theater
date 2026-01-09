"""
Monologue Validator Skill
=========================

HARDCODED validator for presenter notes (monologues).
This validator CANNOT be bypassed - all slides MUST pass validation.

Validation Rules:
- R1: 150-200 words per content slide (HARDCODED)
- R2: Minimum 2 [PAUSE] markers per slide (HARDCODED)
- R3: Minimum 1 [EMPHASIS] marker per slide (HARDCODED)
- R4: No bullet-point style writing
- R5: Natural speech flow
- R6: Presentation-level minimums (24 [PAUSE], 12 [EMPHASIS], 3 [CHECK])

Pipeline: Theater Education
"""

import re
from typing import Dict, Any, List, Tuple


# =============================================================================
# HARDCODED VALIDATION THRESHOLDS (CANNOT BE MODIFIED)
# =============================================================================

# Per-slide requirements
MIN_WORDS = 150
MAX_WORDS = 200
MIN_PAUSE_PER_SLIDE = 2
MIN_EMPHASIS_PER_SLIDE = 1

# Presentation-level requirements (16 slides)
MIN_TOTAL_WORDS = 2400  # 150 * 16
MAX_TOTAL_WORDS = 3200  # 200 * 16
MIN_TOTAL_PAUSE = 24    # 2 * 12 content slides (auxiliary can have fewer)
MIN_TOTAL_EMPHASIS = 12 # 1 * 12 content slides
MIN_TOTAL_CHECK = 3     # At least 3 check-for-understanding

# Marker patterns
MARKER_PATTERNS = {
    "PAUSE": r'\[PAUSE\]',
    "EMPHASIS": r'\[EMPHASIS[:\s]?[^\]]*\]',
    "GESTURE": r'\[GESTURE[:\s]?[^\]]*\]',
    "CHECK": r'\[CHECK[:\s]?[^\]]*\]',
    "TRANSITION": r'\[TRANSITION\]',
    "WAIT": r'\[WAIT[:\s]?[^\]]*\]',
}

# Forbidden patterns (bullet-point style)
FORBIDDEN_PATTERNS = [
    r'^\s*[\•\-\*]\s',      # Bullet points at line start
    r'^\s*\d+\.\s',          # Numbered lists at line start
    r'TODO',                 # Placeholder text
    r'PLACEHOLDER',          # Placeholder text
    r'INSERT HERE',          # Placeholder text
    r'\[CONTENT\]',          # Placeholder marker
]


# =============================================================================
# SLIDE-LEVEL VALIDATION
# =============================================================================

def validate_slide_monologue(
    monologue: str,
    slide_index: int,
    slide_type: str = "content"
) -> Dict[str, Any]:
    """
    Validate a single slide's presenter notes.

    HARDCODED validation that cannot be bypassed.

    Args:
        monologue: The presenter notes text
        slide_index: Which slide (1-16)
        slide_type: agenda, warmup, content, activity, or journal

    Returns:
        Validation result dictionary
    """
    issues = []
    warnings = []

    # Count words (exclude markers from count)
    clean_text = re.sub(r'\[[^\]]+\]', '', monologue)
    word_count = len(clean_text.split())

    # R1: Word count validation
    # Content slides have strict requirements; auxiliary slides are more lenient
    if slide_type == "content":
        if word_count < MIN_WORDS:
            issues.append({
                "rule": "R1",
                "severity": "CRITICAL",
                "message": f"Slide {slide_index}: Only {word_count} words. MINIMUM is {MIN_WORDS}.",
                "slide": slide_index
            })
        if word_count > MAX_WORDS:
            warnings.append({
                "rule": "R1",
                "severity": "WARNING",
                "message": f"Slide {slide_index}: {word_count} words exceeds recommended maximum of {MAX_WORDS}.",
                "slide": slide_index
            })
    else:
        # Auxiliary slides: minimum 100 words
        if word_count < 100:
            issues.append({
                "rule": "R1",
                "severity": "CRITICAL",
                "message": f"Slide {slide_index} ({slide_type}): Only {word_count} words. Minimum is 100.",
                "slide": slide_index
            })

    # Count markers
    markers = {}
    for name, pattern in MARKER_PATTERNS.items():
        markers[name] = len(re.findall(pattern, monologue, re.IGNORECASE))

    # R2: [PAUSE] markers
    if markers["PAUSE"] < MIN_PAUSE_PER_SLIDE:
        issues.append({
            "rule": "R2",
            "severity": "CRITICAL",
            "message": f"Slide {slide_index}: Only {markers['PAUSE']} [PAUSE] markers. MINIMUM is {MIN_PAUSE_PER_SLIDE}.",
            "slide": slide_index
        })

    # R3: [EMPHASIS] markers (content slides only)
    if slide_type == "content" and markers["EMPHASIS"] < MIN_EMPHASIS_PER_SLIDE:
        issues.append({
            "rule": "R3",
            "severity": "CRITICAL",
            "message": f"Slide {slide_index}: Only {markers['EMPHASIS']} [EMPHASIS] markers. MINIMUM is {MIN_EMPHASIS_PER_SLIDE}.",
            "slide": slide_index
        })

    # R4: No bullet-point style
    for pattern in FORBIDDEN_PATTERNS:
        if re.search(pattern, monologue, re.MULTILINE | re.IGNORECASE):
            issues.append({
                "rule": "R4",
                "severity": "CRITICAL",
                "message": f"Slide {slide_index}: Bullet-point or placeholder text detected (pattern: {pattern}).",
                "slide": slide_index
            })

    # R5: Natural speech flow checks
    if monologue.count("\n\n\n") > 0:
        warnings.append({
            "rule": "R5",
            "severity": "WARNING",
            "message": f"Slide {slide_index}: Excessive blank lines detected.",
            "slide": slide_index
        })

    # Check for missing monologue
    if not monologue or len(monologue.strip()) < 50:
        issues.append({
            "rule": "R1",
            "severity": "CRITICAL",
            "message": f"Slide {slide_index}: Presenter notes missing or too short.",
            "slide": slide_index
        })

    return {
        "slide_index": slide_index,
        "slide_type": slide_type,
        "valid": len(issues) == 0,
        "word_count": word_count,
        "markers": markers,
        "issues": issues,
        "warnings": warnings
    }


# =============================================================================
# PRESENTATION-LEVEL VALIDATION
# =============================================================================

def validate_presentation_monologues(
    monologues: List[str],
    slide_types: List[str] = None
) -> Dict[str, Any]:
    """
    Validate all presenter notes for a 16-slide presentation.

    HARDCODED validation - presentation MUST pass all checks.

    Args:
        monologues: List of 16 presenter notes strings
        slide_types: Optional list of slide types (defaults to standard structure)

    Returns:
        Comprehensive validation result
    """
    # Default slide types
    if slide_types is None:
        slide_types = (
            ["agenda", "warmup"] +
            ["content"] * 12 +
            ["activity", "journal"]
        )

    # Validate each slide
    slide_results = []
    total_issues = []
    total_warnings = []
    total_words = 0
    total_markers = {name: 0 for name in MARKER_PATTERNS}

    for i, (monologue, slide_type) in enumerate(zip(monologues, slide_types)):
        result = validate_slide_monologue(monologue, i + 1, slide_type)
        slide_results.append(result)

        total_issues.extend(result["issues"])
        total_warnings.extend(result["warnings"])
        total_words += result["word_count"]

        for name in total_markers:
            total_markers[name] += result["markers"].get(name, 0)

    # R6: Presentation-level requirements
    presentation_issues = []

    if total_words < MIN_TOTAL_WORDS:
        presentation_issues.append({
            "rule": "R6",
            "severity": "CRITICAL",
            "message": f"Total words ({total_words}) below minimum ({MIN_TOTAL_WORDS})."
        })

    if total_markers["PAUSE"] < MIN_TOTAL_PAUSE:
        presentation_issues.append({
            "rule": "R6",
            "severity": "CRITICAL",
            "message": f"Total [PAUSE] markers ({total_markers['PAUSE']}) below minimum ({MIN_TOTAL_PAUSE})."
        })

    if total_markers["EMPHASIS"] < MIN_TOTAL_EMPHASIS:
        presentation_issues.append({
            "rule": "R6",
            "severity": "CRITICAL",
            "message": f"Total [EMPHASIS] markers ({total_markers['EMPHASIS']}) below minimum ({MIN_TOTAL_EMPHASIS})."
        })

    if total_markers["CHECK"] < MIN_TOTAL_CHECK:
        presentation_issues.append({
            "rule": "R6",
            "severity": "CRITICAL",
            "message": f"Total [CHECK] markers ({total_markers['CHECK']}) below minimum ({MIN_TOTAL_CHECK})."
        })

    # Calculate pass/fail
    all_issues = total_issues + presentation_issues
    critical_issues = [i for i in all_issues if i.get("severity") == "CRITICAL"]
    slides_passed = sum(1 for r in slide_results if r["valid"])

    return {
        "valid": len(critical_issues) == 0,
        "slides_checked": len(monologues),
        "slides_passed": slides_passed,
        "slides_failed": len(monologues) - slides_passed,
        "total_words": total_words,
        "total_markers": total_markers,
        "estimated_duration_minutes": round(total_words / 150, 1),
        "slide_results": slide_results,
        "issues": all_issues,
        "warnings": total_warnings,
        "summary": generate_validation_summary(slide_results, all_issues, total_markers)
    }


def generate_validation_summary(
    slide_results: List[Dict],
    issues: List[Dict],
    markers: Dict[str, int]
) -> str:
    """Generate human-readable validation summary."""
    lines = ["=" * 60]
    lines.append("MONOLOGUE VALIDATION SUMMARY")
    lines.append("=" * 60)

    passed = sum(1 for r in slide_results if r["valid"])
    total = len(slide_results)

    if passed == total:
        lines.append(f"STATUS: PASSED ({passed}/{total} slides)")
    else:
        lines.append(f"STATUS: FAILED ({passed}/{total} slides passed)")

    lines.append("")
    lines.append("Marker Totals:")
    lines.append(f"  [PAUSE]: {markers['PAUSE']} (min: {MIN_TOTAL_PAUSE})")
    lines.append(f"  [EMPHASIS]: {markers['EMPHASIS']} (min: {MIN_TOTAL_EMPHASIS})")
    lines.append(f"  [CHECK]: {markers['CHECK']} (min: {MIN_TOTAL_CHECK})")
    lines.append(f"  [GESTURE]: {markers['GESTURE']}")
    lines.append(f"  [TRANSITION]: {markers['TRANSITION']}")

    if issues:
        lines.append("")
        lines.append("Issues Found:")
        for issue in issues[:10]:  # Show first 10
            severity = issue.get("severity", "INFO")
            message = issue.get("message", "Unknown issue")
            lines.append(f"  [{severity}] {message}")
        if len(issues) > 10:
            lines.append(f"  ... and {len(issues) - 10} more issues")

    lines.append("=" * 60)
    return "\n".join(lines)


# =============================================================================
# QUICK VALIDATION FUNCTIONS
# =============================================================================

def has_valid_monologue(monologue: str, slide_type: str = "content") -> bool:
    """Quick check if a monologue passes validation."""
    result = validate_slide_monologue(monologue, 1, slide_type)
    return result["valid"]


def get_monologue_issues(monologue: str, slide_index: int = 1) -> List[str]:
    """Get list of issue messages for a monologue."""
    result = validate_slide_monologue(monologue, slide_index)
    return [i["message"] for i in result["issues"]]


def count_monologue_words(monologue: str) -> int:
    """Count words in monologue (excluding markers)."""
    clean_text = re.sub(r'\[[^\]]+\]', '', monologue)
    return len(clean_text.split())


def count_monologue_markers(monologue: str) -> Dict[str, int]:
    """Count all markers in a monologue."""
    return {
        name: len(re.findall(pattern, monologue, re.IGNORECASE))
        for name, pattern in MARKER_PATTERNS.items()
    }


# =============================================================================
# EXPORTS
# =============================================================================

__all__ = [
    # Main validation functions
    "validate_slide_monologue",
    "validate_presentation_monologues",
    # Quick checks
    "has_valid_monologue",
    "get_monologue_issues",
    "count_monologue_words",
    "count_monologue_markers",
    # Constants (for external validation)
    "MIN_WORDS",
    "MAX_WORDS",
    "MIN_PAUSE_PER_SLIDE",
    "MIN_EMPHASIS_PER_SLIDE",
    "MIN_TOTAL_PAUSE",
    "MIN_TOTAL_EMPHASIS",
    "MIN_TOTAL_CHECK",
    "MARKER_PATTERNS",
]
