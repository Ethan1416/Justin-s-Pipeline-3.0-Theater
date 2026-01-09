"""
English Standards Validator Skill
=================================

HARDCODED validator for English/Language Arts standards in lesson materials.
This validator CANNOT be bypassed - all lessons MUST pass standards validation.

Validation Rules:
- R1: Each lesson must have 1-3 English standards (HARDCODED)
- R2: Standards must have valid codes (HARDCODED)
- R3: Standards must include full text (HARDCODED)
- R4: Lesson plan must cite standards (HARDCODED)
- R5: Exit tickets must align with at least one standard (HARDCODED)
- R6: Activities must reference applicable standards (HARDCODED)

Pipeline: Theater Education
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
import re


# =============================================================================
# HARDCODED VALIDATION THRESHOLDS (CANNOT BE MODIFIED)
# =============================================================================

# Minimum and maximum standards per lesson
MIN_STANDARDS = 1
MAX_STANDARDS = 3

# Valid standard code patterns (California Common Core)
VALID_STANDARD_PATTERNS = [
    r"^RL\.\d{1,2}-\d{1,2}\.\d+[a-z]?$",  # Reading Literature (e.g., RL.9-10.4)
    r"^RI\.\d{1,2}-\d{1,2}\.\d+[a-z]?$",  # Reading Informational
    r"^W\.\d{1,2}-\d{1,2}\.\d+[a-z]?$",   # Writing
    r"^SL\.\d{1,2}-\d{1,2}\.\d+[a-z]?$",  # Speaking & Listening
    r"^L\.\d{1,2}-\d{1,2}\.\d+[a-z]?$",   # Language
]

# Minimum length for standard full text
MIN_STANDARD_TEXT_LENGTH = 20


# =============================================================================
# DATA CLASSES
# =============================================================================

@dataclass
class StandardValidationIssue:
    """A validation issue for a standard."""
    rule: str
    severity: str  # CRITICAL, WARNING, INFO
    message: str
    standard_code: Optional[str] = None


@dataclass
class StandardsValidationResult:
    """Result of standards validation."""
    valid: bool
    standards_count: int
    standards_found: List[Dict[str, str]]
    valid_codes: List[str]
    invalid_codes: List[str]
    issues: List[StandardValidationIssue] = field(default_factory=list)
    warnings: List[StandardValidationIssue] = field(default_factory=list)
    lesson_plan_cites_standards: bool = False
    exit_tickets_aligned: bool = False
    activity_references_standards: bool = False


# =============================================================================
# VALIDATION FUNCTIONS
# =============================================================================

def is_valid_standard_code(code: str) -> bool:
    """
    Check if a standard code is valid.

    HARDCODED: Must match California Common Core ELA format.

    Args:
        code: Standard code to validate

    Returns:
        True if valid, False otherwise
    """
    if not code:
        return False

    for pattern in VALID_STANDARD_PATTERNS:
        if re.match(pattern, code):
            return True

    return False


def validate_standard(standard: Dict[str, str]) -> List[StandardValidationIssue]:
    """
    Validate a single standard entry.

    HARDCODED validation rules.

    Args:
        standard: Standard dictionary with 'code' and 'full_text' keys

    Returns:
        List of validation issues (empty if valid)
    """
    issues = []

    code = standard.get("code", "")
    full_text = standard.get("full_text", "")

    # R2: Check valid code format
    if not code:
        issues.append(StandardValidationIssue(
            rule="R2",
            severity="CRITICAL",
            message="Standard is missing code"
        ))
    elif not is_valid_standard_code(code):
        issues.append(StandardValidationIssue(
            rule="R2",
            severity="CRITICAL",
            message=f"Invalid standard code format: {code}",
            standard_code=code
        ))

    # R3: Check full text presence
    if not full_text:
        issues.append(StandardValidationIssue(
            rule="R3",
            severity="CRITICAL",
            message=f"Standard {code} is missing full text",
            standard_code=code
        ))
    elif len(full_text) < MIN_STANDARD_TEXT_LENGTH:
        issues.append(StandardValidationIssue(
            rule="R3",
            severity="WARNING",
            message=f"Standard {code} has very short text ({len(full_text)} chars)",
            standard_code=code
        ))

    return issues


def validate_standards_count(standards: List[Dict[str, str]]) -> List[StandardValidationIssue]:
    """
    Validate that lesson has correct number of standards.

    HARDCODED: Must have 1-3 standards.

    Args:
        standards: List of standards

    Returns:
        List of validation issues
    """
    issues = []
    count = len(standards)

    # R1: Check count range
    if count < MIN_STANDARDS:
        issues.append(StandardValidationIssue(
            rule="R1",
            severity="CRITICAL",
            message=f"Lesson has {count} standards (minimum {MIN_STANDARDS} required)"
        ))
    elif count > MAX_STANDARDS:
        issues.append(StandardValidationIssue(
            rule="R1",
            severity="WARNING",
            message=f"Lesson has {count} standards (maximum {MAX_STANDARDS} recommended)"
        ))

    return issues


def validate_lesson_plan_citations(
    lesson_plan: str,
    standards: List[Dict[str, str]]
) -> List[StandardValidationIssue]:
    """
    Validate that lesson plan cites all standards.

    HARDCODED: Lesson plan must reference each standard.

    Args:
        lesson_plan: Lesson plan text (markdown)
        standards: List of standards

    Returns:
        List of validation issues
    """
    issues = []

    if not lesson_plan:
        issues.append(StandardValidationIssue(
            rule="R4",
            severity="CRITICAL",
            message="Lesson plan is empty - cannot validate standards citations"
        ))
        return issues

    # Check that each standard code appears in the lesson plan
    for std in standards:
        code = std.get("code", "")
        if code and code not in lesson_plan:
            issues.append(StandardValidationIssue(
                rule="R4",
                severity="CRITICAL",
                message=f"Standard {code} not cited in lesson plan",
                standard_code=code
            ))

    # Check for standards section header
    if "standards" not in lesson_plan.lower():
        issues.append(StandardValidationIssue(
            rule="R4",
            severity="WARNING",
            message="Lesson plan may be missing 'Standards' section header"
        ))

    return issues


def validate_exit_ticket_alignment(
    exit_tickets: List[str],
    standards: List[Dict[str, str]]
) -> List[StandardValidationIssue]:
    """
    Validate that exit tickets align with standards.

    HARDCODED: At least one exit ticket must align with each standard strand.

    Args:
        exit_tickets: List of exit ticket questions
        standards: List of standards

    Returns:
        List of validation issues
    """
    issues = []

    if not exit_tickets:
        issues.append(StandardValidationIssue(
            rule="R5",
            severity="CRITICAL",
            message="No exit tickets to validate"
        ))
        return issues

    if not standards:
        issues.append(StandardValidationIssue(
            rule="R5",
            severity="CRITICAL",
            message="No standards to align with exit tickets"
        ))
        return issues

    # Get standard strands (RL, SL, W, L, RI)
    strands = set()
    for std in standards:
        code = std.get("code", "")
        if "." in code:
            strand = code.split(".")[0]
            strands.add(strand)

    # Check that exit tickets have assessment-type language
    assessment_keywords = {
        "RL": ["analyze", "explain", "describe", "character", "theme", "meaning", "text"],
        "SL": ["discuss", "explain", "share", "present", "describe"],
        "W": ["write", "explain", "describe", "argument"],
        "L": ["define", "word", "vocabulary", "meaning", "phrase"],
        "RI": ["explain", "analyze", "describe", "evidence"]
    }

    # Check that at least one exit ticket can align with the standards
    ticket_text = " ".join(exit_tickets).lower()
    has_alignment = False

    for strand in strands:
        keywords = assessment_keywords.get(strand, [])
        if any(keyword in ticket_text for keyword in keywords):
            has_alignment = True
            break

    if not has_alignment and strands:
        issues.append(StandardValidationIssue(
            rule="R5",
            severity="WARNING",
            message=f"Exit tickets may not align with standards strands: {', '.join(strands)}"
        ))

    return issues


def validate_activity_standards_reference(
    activity: Dict[str, Any],
    standards: List[Dict[str, str]]
) -> List[StandardValidationIssue]:
    """
    Validate that activity references applicable standards.

    HARDCODED: Activities should reference at least one standard.

    Args:
        activity: Activity data
        standards: List of standards

    Returns:
        List of validation issues
    """
    issues = []

    if not activity:
        return issues  # No activity to validate

    activity_type = activity.get("type", "").lower()
    activity_name = activity.get("name", "Unnamed Activity")

    # Map activity types to expected standard strands
    type_to_strand = {
        "discussion": "SL",
        "collaborative": "SL",
        "critical_thinking": "RL",
        "writing": "W",
        "performance": "SL",
        "annotation": "RL",
        "analysis": "RL",
        "vocabulary": "L",
        "creative": "W",
        "presentation": "SL",
    }

    expected_strand = type_to_strand.get(activity_type)

    if expected_strand:
        # Check if any standard matches the expected strand
        has_matching_standard = any(
            std.get("code", "").startswith(expected_strand)
            for std in standards
        )

        if not has_matching_standard:
            issues.append(StandardValidationIssue(
                rule="R6",
                severity="WARNING",
                message=f"Activity '{activity_name}' ({activity_type}) would benefit from a {expected_strand} standard"
            ))

    return issues


def validate_lesson_standards(
    lesson_data: Dict[str, Any],
    lesson_plan_text: Optional[str] = None
) -> StandardsValidationResult:
    """
    Full validation of standards in a lesson.

    HARDCODED validation that cannot be bypassed.

    Args:
        lesson_data: Complete lesson data dictionary
        lesson_plan_text: Optional lesson plan markdown text

    Returns:
        StandardsValidationResult with all validation results
    """
    standards = lesson_data.get("standards", [])
    exit_tickets = lesson_data.get("exit_tickets", [])
    activity = lesson_data.get("activity", {})

    all_issues = []
    all_warnings = []
    valid_codes = []
    invalid_codes = []

    # R1: Validate standards count
    count_issues = validate_standards_count(standards)
    for issue in count_issues:
        if issue.severity == "CRITICAL":
            all_issues.append(issue)
        else:
            all_warnings.append(issue)

    # R2, R3: Validate each standard
    for std in standards:
        std_issues = validate_standard(std)
        code = std.get("code", "")

        has_critical = False
        for issue in std_issues:
            if issue.severity == "CRITICAL":
                all_issues.append(issue)
                has_critical = True
            else:
                all_warnings.append(issue)

        if has_critical:
            invalid_codes.append(code)
        else:
            valid_codes.append(code)

    # R4: Validate lesson plan citations (if provided)
    lesson_plan_cites = False
    if lesson_plan_text:
        citation_issues = validate_lesson_plan_citations(lesson_plan_text, standards)
        for issue in citation_issues:
            if issue.severity == "CRITICAL":
                all_issues.append(issue)
            else:
                all_warnings.append(issue)
        lesson_plan_cites = not any(
            i.rule == "R4" and i.severity == "CRITICAL"
            for i in citation_issues
        )

    # R5: Validate exit ticket alignment
    exit_aligned = False
    if exit_tickets:
        exit_issues = validate_exit_ticket_alignment(exit_tickets, standards)
        for issue in exit_issues:
            if issue.severity == "CRITICAL":
                all_issues.append(issue)
            else:
                all_warnings.append(issue)
        exit_aligned = not any(
            i.rule == "R5" and i.severity == "CRITICAL"
            for i in exit_issues
        )

    # R6: Validate activity standards reference
    activity_refs = False
    if activity:
        activity_issues = validate_activity_standards_reference(activity, standards)
        for issue in activity_issues:
            if issue.severity == "CRITICAL":
                all_issues.append(issue)
            else:
                all_warnings.append(issue)
        activity_refs = not any(
            i.rule == "R6" and i.severity == "CRITICAL"
            for i in activity_issues
        )

    # Determine overall validity
    critical_issues = [i for i in all_issues if i.severity == "CRITICAL"]
    is_valid = len(critical_issues) == 0

    return StandardsValidationResult(
        valid=is_valid,
        standards_count=len(standards),
        standards_found=standards,
        valid_codes=valid_codes,
        invalid_codes=invalid_codes,
        issues=all_issues,
        warnings=all_warnings,
        lesson_plan_cites_standards=lesson_plan_cites,
        exit_tickets_aligned=exit_aligned,
        activity_references_standards=activity_refs
    )


# =============================================================================
# QUICK VALIDATION FUNCTIONS
# =============================================================================

def has_valid_standards(lesson_data: Dict[str, Any]) -> bool:
    """Quick check if lesson has valid standards."""
    result = validate_lesson_standards(lesson_data)
    return result.valid


def get_standards_issues(lesson_data: Dict[str, Any]) -> List[str]:
    """Get list of standards validation issue messages."""
    result = validate_lesson_standards(lesson_data)
    return [issue.message for issue in result.issues]


def count_standards(lesson_data: Dict[str, Any]) -> int:
    """Count standards in a lesson."""
    return len(lesson_data.get("standards", []))


def standards_in_range(lesson_data: Dict[str, Any]) -> bool:
    """Check if standards count is in valid range (1-3)."""
    count = count_standards(lesson_data)
    return MIN_STANDARDS <= count <= MAX_STANDARDS


# =============================================================================
# REPORT GENERATION
# =============================================================================

def generate_validation_report(result: StandardsValidationResult) -> str:
    """Generate human-readable validation report."""
    lines = [
        "=" * 60,
        "ENGLISH STANDARDS VALIDATION REPORT",
        "=" * 60,
        f"Status: {'PASSED' if result.valid else 'FAILED'}",
        f"Standards Count: {result.standards_count} (required: {MIN_STANDARDS}-{MAX_STANDARDS})",
        ""
    ]

    # List standards found
    lines.append("Standards Found:")
    for std in result.standards_found:
        code = std.get("code", "Unknown")
        status = "VALID" if code in result.valid_codes else "INVALID"
        lines.append(f"  [{status}] {code}")

    # Validation checks
    lines.append("")
    lines.append("Validation Checks:")
    lines.append(f"  [{'OK' if result.lesson_plan_cites_standards else 'FAIL'}] Lesson plan cites standards")
    lines.append(f"  [{'OK' if result.exit_tickets_aligned else 'WARN'}] Exit tickets aligned")
    lines.append(f"  [{'OK' if result.activity_references_standards else 'WARN'}] Activity references standards")

    # Issues
    if result.issues:
        lines.append("")
        lines.append("Issues (must fix):")
        for issue in result.issues[:5]:
            lines.append(f"  [{issue.rule}] {issue.message}")
        if len(result.issues) > 5:
            lines.append(f"  ... and {len(result.issues) - 5} more")

    # Warnings
    if result.warnings:
        lines.append("")
        lines.append("Warnings (recommended):")
        for warning in result.warnings[:3]:
            lines.append(f"  [{warning.rule}] {warning.message}")
        if len(result.warnings) > 3:
            lines.append(f"  ... and {len(result.warnings) - 3} more")

    lines.append("=" * 60)
    return "\n".join(lines)


# =============================================================================
# EXPORTS
# =============================================================================

__all__ = [
    # Constants
    "MIN_STANDARDS",
    "MAX_STANDARDS",
    "VALID_STANDARD_PATTERNS",
    # Validation functions
    "is_valid_standard_code",
    "validate_standard",
    "validate_standards_count",
    "validate_lesson_plan_citations",
    "validate_exit_ticket_alignment",
    "validate_activity_standards_reference",
    "validate_lesson_standards",
    # Quick checks
    "has_valid_standards",
    "get_standards_issues",
    "count_standards",
    "standards_in_range",
    # Report
    "generate_validation_report",
    # Data classes
    "StandardValidationIssue",
    "StandardsValidationResult",
]
