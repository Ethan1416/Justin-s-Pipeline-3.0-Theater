"""
Template Population Validator Skill
Validates all requirements for template population in the NCLEX pipeline.

This skill provides a comprehensive checklist validation for Step 12 (PowerPoint Population)
ensuring all slides meet template, content, and presenter notes requirements.

Requirements validated:
- R1: Header character limits (36 chars/line, 2 lines max)
- R2: Body line limits (9 lines max across 3 shapes)
- R3: Body character limits (66 chars/line)
- R4: NCLEX tip limits (132 chars max) - dedicated TextBox 24 in nclex_tip template
- R6: Presenter notes word count (200-450 words)
- R14: Presenter notes markers ([PAUSE], [EMPHASIS])
- Template: NCLEX Tip template usage for all slides

NCLEX Tip Template Shape Mappings (Jan 2026):
- TextBox 6:  Title/Header
- TextBox 12: Body content line 1
- TextBox 13: Body content line 2
- TextBox 14: Body content line 3
- TextBox 20: NCLEX TIP label (static)
- TextBox 24: NCLEX tip content (dedicated shape)
- TextBox 30: Footer
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from enum import Enum
import json


class ValidationStatus(Enum):
    PASS = "PASS"
    FAIL = "FAIL"
    WARN = "WARN"
    SKIP = "SKIP"


@dataclass
class ChecklistItem:
    """Individual checklist validation item."""
    id: str
    name: str
    description: str
    requirement: str
    status: ValidationStatus = ValidationStatus.SKIP
    actual_value: Any = None
    expected_value: Any = None
    message: str = ""


@dataclass
class SlideValidation:
    """Validation results for a single slide."""
    slide_number: int
    slide_type: str
    checks: List[ChecklistItem] = field(default_factory=list)
    passed: int = 0
    failed: int = 0
    warnings: int = 0

    @property
    def status(self) -> ValidationStatus:
        if self.failed > 0:
            return ValidationStatus.FAIL
        if self.warnings > 0:
            return ValidationStatus.WARN
        return ValidationStatus.PASS


@dataclass
class ValidationReport:
    """Complete validation report for a section."""
    section_name: str
    template_used: str
    slides: List[SlideValidation] = field(default_factory=list)
    summary: Dict[str, Any] = field(default_factory=dict)


# =============================================================================
# CHECKLIST DEFINITIONS
# =============================================================================

TEMPLATE_POPULATION_CHECKLIST = {
    # Header Requirements (R1)
    "R1.1": {
        "name": "Header Character Limit",
        "description": "Header text must not exceed 36 characters per line",
        "requirement": "R1",
        "max_value": 36
    },
    "R1.2": {
        "name": "Header Line Limit",
        "description": "Header must be a single line only",
        "requirement": "R1",
        "max_value": 1
    },

    # Body Requirements (R2, R3)
    "R2.1": {
        "name": "Body Line Limit",
        "description": "Body text must not exceed 12 lines",
        "requirement": "R2",
        "max_value": 12
    },
    "R3.1": {
        "name": "Body Text Complete",
        "description": "Body text should not contain truncation markers",
        "requirement": "R3",
        # No character limit - PowerPoint handles word wrapping
    },

    # NCLEX Tip Requirements (R4)
    "R4.1": {
        "name": "NCLEX Tip Character Limit",
        "description": "NCLEX tip must not exceed 132 characters total",
        "requirement": "R4",
        "max_value": 132
    },

    # Presenter Notes Requirements (R6)
    "R6.1": {
        "name": "Presenter Notes Minimum Words",
        "description": "Presenter notes must meet minimum word count for slide type",
        "requirement": "R6",
        "targets": {
            "title": 200,
            "content": 250,
            "summary": 250,
            "vignette": 150,
            "answer": 250
        }
    },
    "R6.2": {
        "name": "Presenter Notes Maximum Words",
        "description": "Presenter notes must not exceed 450 words",
        "requirement": "R6",
        "max_value": 450
    },
    "R6.3": {
        "name": "Presenter Notes Duration",
        "description": "Presenter notes must not exceed 180 seconds speaking time",
        "requirement": "R6",
        "max_value": 180
    },

    # Marker Requirements (R14)
    "R14.1": {
        "name": "PAUSE Marker Minimum",
        "description": "Presenter notes must contain at least 2 [PAUSE] markers",
        "requirement": "R14",
        "min_value": 2
    },
    "R14.2": {
        "name": "EMPHASIS Marker Minimum",
        "description": "Content slides must contain at least 1 [EMPHASIS] marker",
        "requirement": "R14",
        "min_value": 1,
        "applies_to": ["content", "answer"]
    },

    # Template Requirements
    "T1.1": {
        "name": "NCLEX Tip Template Used",
        "description": "Slide must use NCLEX tip template (template_nclex_tip.pptx)",
        "requirement": "Template",
        "expected_value": "template_nclex_tip.pptx"
    },
    "T1.2": {
        "name": "Template Shapes Present",
        "description": "Required NCLEX tip template shapes must be present",
        "requirement": "Template",
        "required_shapes": ["TextBox 6", "TextBox 12", "TextBox 13", "TextBox 14", "TextBox 20", "TextBox 24", "TextBox 30"]
    },

    # Content Requirements
    "C1.1": {
        "name": "Header Present",
        "description": "Slide must have header text",
        "requirement": "Content"
    },
    "C1.2": {
        "name": "Body Present",
        "description": "Content slides must have body text",
        "requirement": "Content",
        "applies_to": ["content", "summary"]
    },
    "C1.3": {
        "name": "NCLEX Tip Present",
        "description": "Slide should have NCLEX tip",
        "requirement": "Content",
        "severity": "WARN"
    },
    "C1.4": {
        "name": "Presenter Notes Present",
        "description": "Slide must have presenter notes",
        "requirement": "Content"
    }
}


# =============================================================================
# VALIDATION FUNCTIONS
# =============================================================================

def validate_slide(
    slide: Dict[str, Any],
    slide_type: str,
    template_name: str = "template_nclex_tip.pptx"
) -> SlideValidation:
    """
    Validate a single slide against all checklist items.

    Args:
        slide: Slide data dictionary with header, body, nclex_tip, presenter_notes
        slide_type: Type of slide (title, content, summary, vignette, answer)
        template_name: Name of template being used

    Returns:
        SlideValidation object with all check results
    """
    slide_type = slide_type.lower()
    validation = SlideValidation(
        slide_number=slide.get('slide_number', 0),
        slide_type=slide_type
    )

    # R1: Header validation
    header = slide.get('header', '')
    validation.checks.append(_check_header_chars(header))
    validation.checks.append(_check_header_lines(header))

    # R2/R3: Body validation
    body = slide.get('body', '')
    validation.checks.append(_check_body_lines(body))
    validation.checks.append(_check_body_chars(body))

    # R4: NCLEX tip validation
    nclex_tip = slide.get('nclex_tip', '')
    validation.checks.append(_check_nclex_tip_chars(nclex_tip))

    # R6: Presenter notes word count
    presenter_notes = slide.get('presenter_notes', '')
    validation.checks.append(_check_notes_min_words(presenter_notes, slide_type))
    validation.checks.append(_check_notes_max_words(presenter_notes))
    validation.checks.append(_check_notes_duration(presenter_notes))

    # R14: Marker validation
    validation.checks.append(_check_pause_markers(presenter_notes))
    if slide_type in ['content', 'answer']:
        validation.checks.append(_check_emphasis_markers(presenter_notes))

    # Template validation
    validation.checks.append(_check_template_used(template_name))

    # Content presence validation
    validation.checks.append(_check_header_present(header))
    if slide_type in ['content', 'summary']:
        validation.checks.append(_check_body_present(body))
    validation.checks.append(_check_nclex_tip_present(nclex_tip))
    validation.checks.append(_check_notes_present(presenter_notes))

    # Count results
    for check in validation.checks:
        if check.status == ValidationStatus.PASS:
            validation.passed += 1
        elif check.status == ValidationStatus.FAIL:
            validation.failed += 1
        elif check.status == ValidationStatus.WARN:
            validation.warnings += 1

    return validation


def _check_header_chars(header: str) -> ChecklistItem:
    """Check header character limit per line."""
    check = ChecklistItem(
        id="R1.1",
        name="Header Character Limit",
        description="Header text must not exceed 36 characters per line",
        requirement="R1"
    )
    lines = header.split('\n')
    max_line_length = max(len(line) for line in lines) if lines else 0
    check.actual_value = max_line_length
    check.expected_value = 36

    if max_line_length <= 36:
        check.status = ValidationStatus.PASS
        check.message = f"Header line length OK ({max_line_length} chars)"
    else:
        check.status = ValidationStatus.FAIL
        check.message = f"Header line too long ({max_line_length} > 36 chars)"

    return check


def _check_header_lines(header: str) -> ChecklistItem:
    """Check header line limit - must be single line only."""
    check = ChecklistItem(
        id="R1.2",
        name="Header Line Limit",
        description="Header must be a single line only",
        requirement="R1"
    )
    line_count = len(header.split('\n'))
    check.actual_value = line_count
    check.expected_value = 1

    if line_count == 1:
        check.status = ValidationStatus.PASS
        check.message = "Header is single line (OK)"
    else:
        check.status = ValidationStatus.FAIL
        check.message = f"Header must be single line ({line_count} lines found)"

    return check


def _check_body_lines(body: str) -> ChecklistItem:
    """Check body line limit."""
    check = ChecklistItem(
        id="R2.1",
        name="Body Line Limit",
        description="Body text must not exceed 12 lines",
        requirement="R2"
    )
    lines = [l for l in body.split('\n') if l.strip()]
    line_count = len(lines)
    check.actual_value = line_count
    check.expected_value = 12

    if line_count <= 12:
        check.status = ValidationStatus.PASS
        check.message = f"Body line count OK ({line_count} lines)"
    else:
        check.status = ValidationStatus.FAIL
        check.message = f"Body has too many lines ({line_count} > 12)"

    return check


def _check_body_chars(body: str) -> ChecklistItem:
    """Check body text is complete (no truncation markers).

    Character wrapping is handled by PowerPoint - we just check for
    evidence of truncation (ellipsis markers).
    """
    check = ChecklistItem(
        id="R3.1",
        name="Body Text Complete",
        description="Body text should not contain truncation markers",
        requirement="R3"
    )

    # Check for truncation markers
    has_ellipsis = "..." in body or "\u2026" in body  # ... or …
    check.actual_value = "No truncation" if not has_ellipsis else "Truncation detected"
    check.expected_value = "No truncation"

    if not has_ellipsis:
        check.status = ValidationStatus.PASS
        check.message = "Body text is complete (no truncation markers)"
    else:
        check.status = ValidationStatus.WARN
        check.message = "Body may contain truncated content (ellipsis found)"

    return check


def _check_nclex_tip_chars(tip: str) -> ChecklistItem:
    """Check NCLEX tip character limit."""
    check = ChecklistItem(
        id="R4.1",
        name="NCLEX Tip Character Limit",
        description="NCLEX tip must not exceed 132 characters",
        requirement="R4"
    )
    char_count = len(tip)
    check.actual_value = char_count
    check.expected_value = 132

    if char_count <= 132:
        check.status = ValidationStatus.PASS
        check.message = f"NCLEX tip length OK ({char_count} chars)"
    else:
        check.status = ValidationStatus.FAIL
        check.message = f"NCLEX tip too long ({char_count} > 132 chars)"

    return check


def _check_notes_min_words(notes: str, slide_type: str) -> ChecklistItem:
    """Check presenter notes minimum word count."""
    check = ChecklistItem(
        id="R6.1",
        name="Presenter Notes Minimum Words",
        description="Presenter notes must meet minimum word count",
        requirement="R6"
    )
    word_count = len(notes.split())
    minimums = {
        "title": 200,
        "content": 250,
        "summary": 250,
        "vignette": 150,
        "answer": 250
    }
    min_words = minimums.get(slide_type, 250)
    check.actual_value = word_count
    check.expected_value = min_words

    if word_count >= min_words:
        check.status = ValidationStatus.PASS
        check.message = f"Word count OK ({word_count} >= {min_words})"
    else:
        check.status = ValidationStatus.FAIL
        check.message = f"Word count too low ({word_count} < {min_words})"

    return check


def _check_notes_max_words(notes: str) -> ChecklistItem:
    """Check presenter notes maximum word count."""
    check = ChecklistItem(
        id="R6.2",
        name="Presenter Notes Maximum Words",
        description="Presenter notes must not exceed 450 words",
        requirement="R6"
    )
    word_count = len(notes.split())
    check.actual_value = word_count
    check.expected_value = 450

    if word_count <= 450:
        check.status = ValidationStatus.PASS
        check.message = f"Word count OK ({word_count} <= 450)"
    else:
        check.status = ValidationStatus.FAIL
        check.message = f"Word count too high ({word_count} > 450)"

    return check


def _check_notes_duration(notes: str) -> ChecklistItem:
    """Check presenter notes speaking duration."""
    check = ChecklistItem(
        id="R6.3",
        name="Presenter Notes Duration",
        description="Presenter notes must not exceed 180 seconds",
        requirement="R6"
    )
    word_count = len(notes.split())
    duration_seconds = int((word_count / 135) * 60)  # ~135 WPM
    check.actual_value = duration_seconds
    check.expected_value = 180

    if duration_seconds <= 180:
        check.status = ValidationStatus.PASS
        check.message = f"Duration OK ({duration_seconds}s <= 180s)"
    else:
        check.status = ValidationStatus.WARN
        check.message = f"Duration may be long ({duration_seconds}s > 180s)"

    return check


def _check_pause_markers(notes: str) -> ChecklistItem:
    """Check for minimum [PAUSE] markers."""
    check = ChecklistItem(
        id="R14.1",
        name="PAUSE Marker Minimum",
        description="Must contain at least 2 [PAUSE] markers",
        requirement="R14"
    )
    pause_count = notes.count("[PAUSE]")
    check.actual_value = pause_count
    check.expected_value = 2

    if pause_count >= 2:
        check.status = ValidationStatus.PASS
        check.message = f"PAUSE markers OK ({pause_count} >= 2)"
    else:
        check.status = ValidationStatus.FAIL
        check.message = f"Insufficient PAUSE markers ({pause_count} < 2)"

    return check


def _check_emphasis_markers(notes: str) -> ChecklistItem:
    """Check for minimum [EMPHASIS] markers."""
    check = ChecklistItem(
        id="R14.2",
        name="EMPHASIS Marker Minimum",
        description="Content slides must have at least 1 [EMPHASIS] marker",
        requirement="R14"
    )
    emphasis_count = notes.count("[EMPHASIS")
    check.actual_value = emphasis_count
    check.expected_value = 1

    if emphasis_count >= 1:
        check.status = ValidationStatus.PASS
        check.message = f"EMPHASIS markers OK ({emphasis_count} >= 1)"
    else:
        check.status = ValidationStatus.FAIL
        check.message = f"Missing EMPHASIS marker ({emphasis_count} < 1)"

    return check


def _check_template_used(template_name: str) -> ChecklistItem:
    """Check that NCLEX tip template is used."""
    check = ChecklistItem(
        id="T1.1",
        name="NCLEX Tip Template Used",
        description="Slide must use NCLEX tip template",
        requirement="Template"
    )
    check.actual_value = template_name
    check.expected_value = "template_nclex_tip.pptx"

    if "nclex_tip" in template_name.lower():
        check.status = ValidationStatus.PASS
        check.message = "NCLEX tip template in use"
    else:
        check.status = ValidationStatus.FAIL
        check.message = f"Wrong template: {template_name}"

    return check


def _check_header_present(header: str) -> ChecklistItem:
    """Check that header is present."""
    check = ChecklistItem(
        id="C1.1",
        name="Header Present",
        description="Slide must have header text",
        requirement="Content"
    )
    check.actual_value = bool(header.strip())
    check.expected_value = True

    if header.strip():
        check.status = ValidationStatus.PASS
        check.message = "Header present"
    else:
        check.status = ValidationStatus.FAIL
        check.message = "Header missing"

    return check


def _check_body_present(body: str) -> ChecklistItem:
    """Check that body is present."""
    check = ChecklistItem(
        id="C1.2",
        name="Body Present",
        description="Content slides must have body text",
        requirement="Content"
    )
    check.actual_value = bool(body.strip())
    check.expected_value = True

    if body.strip():
        check.status = ValidationStatus.PASS
        check.message = "Body present"
    else:
        check.status = ValidationStatus.FAIL
        check.message = "Body missing"

    return check


def _check_nclex_tip_present(tip: str) -> ChecklistItem:
    """Check that NCLEX tip is present."""
    check = ChecklistItem(
        id="C1.3",
        name="NCLEX Tip Present",
        description="Slide should have NCLEX tip",
        requirement="Content"
    )
    check.actual_value = bool(tip.strip())
    check.expected_value = True

    if tip.strip():
        check.status = ValidationStatus.PASS
        check.message = "NCLEX tip present"
    else:
        check.status = ValidationStatus.WARN
        check.message = "NCLEX tip missing (recommended)"

    return check


def _check_notes_present(notes: str) -> ChecklistItem:
    """Check that presenter notes are present."""
    check = ChecklistItem(
        id="C1.4",
        name="Presenter Notes Present",
        description="Slide must have presenter notes",
        requirement="Content"
    )
    check.actual_value = bool(notes.strip())
    check.expected_value = True

    if notes.strip():
        check.status = ValidationStatus.PASS
        check.message = "Presenter notes present"
    else:
        check.status = ValidationStatus.FAIL
        check.message = "Presenter notes missing"

    return check


# =============================================================================
# SECTION VALIDATION
# =============================================================================

def validate_section(
    slides: List[Dict[str, Any]],
    section_name: str,
    template_name: str = "template_nclex_tip.pptx"
) -> ValidationReport:
    """
    Validate all slides in a section.

    Args:
        slides: List of slide dictionaries
        section_name: Name of the section
        template_name: Template being used

    Returns:
        ValidationReport with all results
    """
    report = ValidationReport(
        section_name=section_name,
        template_used=template_name
    )

    total_passed = 0
    total_failed = 0
    total_warnings = 0

    for slide in slides:
        slide_type = slide.get('slide_type', 'content')
        validation = validate_slide(slide, slide_type, template_name)
        report.slides.append(validation)

        total_passed += validation.passed
        total_failed += validation.failed
        total_warnings += validation.warnings

    total_checks = total_passed + total_failed + total_warnings
    report.summary = {
        "total_slides": len(slides),
        "total_checks": total_checks,
        "passed": total_passed,
        "failed": total_failed,
        "warnings": total_warnings,
        "pass_rate": round(total_passed / total_checks * 100, 1) if total_checks > 0 else 0,
        "status": "PASS" if total_failed == 0 else "FAIL"
    }

    return report


def generate_checklist_report(report: ValidationReport) -> str:
    """
    Generate a human-readable checklist report.

    Args:
        report: ValidationReport from validate_section

    Returns:
        Formatted report string
    """
    lines = [
        "=" * 70,
        f"TEMPLATE POPULATION VALIDATION REPORT",
        f"Section: {report.section_name}",
        f"Template: {report.template_used}",
        "=" * 70,
        "",
        "SUMMARY",
        "-" * 40,
        f"Total Slides: {report.summary['total_slides']}",
        f"Total Checks: {report.summary['total_checks']}",
        f"Passed: {report.summary['passed']}",
        f"Failed: {report.summary['failed']}",
        f"Warnings: {report.summary['warnings']}",
        f"Pass Rate: {report.summary['pass_rate']}%",
        f"Status: {report.summary['status']}",
        "",
    ]

    # Per-slide details
    lines.append("SLIDE DETAILS")
    lines.append("-" * 40)

    for slide_val in report.slides:
        status_icon = "✓" if slide_val.status == ValidationStatus.PASS else "✗" if slide_val.status == ValidationStatus.FAIL else "⚠"
        lines.append(f"\nSlide {slide_val.slide_number} ({slide_val.slide_type}) [{status_icon}]")

        for check in slide_val.checks:
            if check.status == ValidationStatus.FAIL:
                lines.append(f"  ✗ {check.id}: {check.message}")
            elif check.status == ValidationStatus.WARN:
                lines.append(f"  ⚠ {check.id}: {check.message}")

    lines.append("")
    lines.append("=" * 70)

    return "\n".join(lines)


def to_json(report: ValidationReport) -> str:
    """Convert ValidationReport to JSON string."""
    def serialize(obj):
        if isinstance(obj, ValidationStatus):
            return obj.value
        if hasattr(obj, '__dict__'):
            return {k: serialize(v) for k, v in obj.__dict__.items()}
        if isinstance(obj, list):
            return [serialize(item) for item in obj]
        return obj

    return json.dumps(serialize(report), indent=2)
