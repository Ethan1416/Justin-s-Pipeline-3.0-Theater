#!/usr/bin/env python3
"""
Title Validator Skill

Validates slide titles against R1 character constraints.
Provides detailed violation reports and revision hints.

Constraints:
- R1.1: Maximum 36 characters per line
- R1.2: Maximum 2 lines
- Total maximum: 72 characters

Created: 2026-01-06
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum


# Character limits - Single line only
MAX_CHARS_PER_LINE = 36
MAX_LINES = 1
MAX_TOTAL_CHARS = MAX_CHARS_PER_LINE  # 36 chars, single line


class ViolationSeverity(Enum):
    ERROR = "ERROR"
    WARNING = "WARNING"
    INFO = "INFO"


@dataclass
class LineAnalysis:
    """Analysis of a single line."""
    number: int
    text: str
    char_count: int
    within_limit: bool
    excess_chars: int


@dataclass
class Violation:
    """A constraint violation."""
    code: str
    description: str
    severity: ViolationSeverity
    location: str
    excess: int = 0


def analyze_line(line_number: int, text: str) -> LineAnalysis:
    """Analyze a single line for constraints."""
    char_count = len(text)
    within_limit = char_count <= MAX_CHARS_PER_LINE
    excess = max(0, char_count - MAX_CHARS_PER_LINE)

    return LineAnalysis(
        number=line_number,
        text=text,
        char_count=char_count,
        within_limit=within_limit,
        excess_chars=excess
    )


def generate_revision_hints(title: str, violations: List[Violation]) -> List[str]:
    """Generate helpful hints for revising a title."""
    hints = []

    for violation in violations:
        if violation.code == "R1.1":
            excess = violation.excess
            hints.append(f"Line exceeds limit by {excess} chars - needs shortening")

            # Suggest abbreviations
            if "medication" in title.lower():
                hints.append("Try: 'Medication' → 'Med'")
            if "administration" in title.lower():
                hints.append("Try: 'Administration' → 'Admin'")
            if "patient" in title.lower():
                hints.append("Try: 'Patient' → 'Pt'")
            if "assessment" in title.lower():
                hints.append("Try: 'Assessment' → 'Assess'")
            if " and " in title.lower():
                hints.append("Try: 'and' → '&'")

            # Suggest splitting
            if '\n' not in title:
                hints.append("Consider splitting into 2 lines")

        elif violation.code == "R1.2":
            hints.append("Combine content into 2 lines maximum")
            hints.append("Consider condensing or removing least important line")

        elif violation.code == "R1.3":
            hints.append("Total character count too high - need significant revision")
            hints.append("Focus on core concept only")

    return hints


def validate_title(
    title: str,
    slide_number: Optional[int] = None,
    slide_type: Optional[str] = None
) -> Dict[str, Any]:
    """
    Validate a title against R1 constraints.

    Args:
        title: The title to validate
        slide_number: Optional slide reference
        slide_type: Optional slide type for context

    Returns:
        Comprehensive validation result
    """
    # Handle empty/None titles
    if not title:
        return {
            "valid": False,
            "title": title or "",
            "analysis": {
                "total_chars": 0,
                "line_count": 0,
                "lines": []
            },
            "violations": [
                Violation(
                    code="R1.0",
                    description="Title is empty",
                    severity=ViolationSeverity.ERROR,
                    location="Overall"
                ).__dict__
            ],
            "revision_needed": True,
            "revision_hints": ["Title is required"]
        }

    # Split into lines
    lines = title.split('\n')
    line_analyses = [analyze_line(i + 1, line) for i, line in enumerate(lines)]

    # Calculate totals
    total_chars = sum(la.char_count for la in line_analyses)
    line_count = len(lines)

    # Check for violations
    violations = []

    # R1.1: Character limit per line
    for la in line_analyses:
        if not la.within_limit:
            violations.append(Violation(
                code="R1.1",
                description=f"Line {la.number} exceeds {MAX_CHARS_PER_LINE}-character limit ({la.char_count} chars, {la.excess_chars} over)",
                severity=ViolationSeverity.ERROR,
                location=f"Line {la.number}",
                excess=la.excess_chars
            ))

    # R1.2: Line count limit
    if line_count > MAX_LINES:
        violations.append(Violation(
            code="R1.2",
            description=f"Title has {line_count} lines, maximum is {MAX_LINES}",
            severity=ViolationSeverity.ERROR,
            location="Overall",
            excess=line_count - MAX_LINES
        ))

    # R1.3: Total character limit (warning)
    if total_chars > MAX_TOTAL_CHARS:
        violations.append(Violation(
            code="R1.3",
            description=f"Total characters ({total_chars}) exceed maximum ({MAX_TOTAL_CHARS})",
            severity=ViolationSeverity.WARNING,
            location="Overall",
            excess=total_chars - MAX_TOTAL_CHARS
        ))

    # R1.4: Truncation detection
    if "..." in title or "…" in title:
        violations.append(Violation(
            code="R1.4",
            description="Title appears to be truncated (contains '...')",
            severity=ViolationSeverity.ERROR,
            location="Overall"
        ))

    # Determine overall validity
    has_errors = any(v.severity == ViolationSeverity.ERROR for v in violations)
    valid = not has_errors

    # Generate revision hints if needed
    revision_hints = generate_revision_hints(title, violations) if violations else []

    return {
        "valid": valid,
        "title": title,
        "slide_number": slide_number,
        "slide_type": slide_type,
        "analysis": {
            "total_chars": total_chars,
            "line_count": line_count,
            "lines": [
                {
                    "number": la.number,
                    "text": la.text,
                    "char_count": la.char_count,
                    "within_limit": la.within_limit,
                    "excess_chars": la.excess_chars
                }
                for la in line_analyses
            ]
        },
        "violations": [v.__dict__ for v in violations],
        "revision_needed": has_errors,
        "revision_hints": revision_hints
    }


def validate_blueprint_titles(blueprint: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate all slide titles in a blueprint.

    Args:
        blueprint: Blueprint dictionary with 'slides' list

    Returns:
        Summary of all title validations
    """
    if 'slides' not in blueprint:
        return {
            "error": "No slides in blueprint",
            "valid": False
        }

    results = {
        "total_slides": len(blueprint['slides']),
        "valid_count": 0,
        "invalid_count": 0,
        "violations": [],
        "all_valid": True
    }

    for slide in blueprint['slides']:
        title = slide.get('header', '')
        validation = validate_title(
            title=title,
            slide_number=slide.get('slide_number'),
            slide_type=slide.get('slide_type')
        )

        if validation['valid']:
            results['valid_count'] += 1
        else:
            results['invalid_count'] += 1
            results['all_valid'] = False
            results['violations'].append({
                "slide_number": slide.get('slide_number'),
                "title": title,
                "issues": validation['violations'],
                "hints": validation['revision_hints']
            })

    results['pass_rate'] = (
        results['valid_count'] / results['total_slides'] * 100
        if results['total_slides'] > 0 else 0
    )

    return results


def is_title_valid(title: str) -> bool:
    """Quick check if a title is valid."""
    result = validate_title(title)
    return result['valid']


def get_title_char_count(title: str) -> Dict[str, int]:
    """Get character counts for a title."""
    lines = title.split('\n')
    return {
        "total": sum(len(line) for line in lines),
        "line_count": len(lines),
        "max_line": max(len(line) for line in lines) if lines else 0,
        "per_line": [len(line) for line in lines]
    }


if __name__ == "__main__":
    # Test the validator
    test_titles = [
        "Beta-Blocker Medications",  # Valid
        "Comprehensive Medication Administration Safety Guidelines",  # Too long
        "Short Title\nWith Second Line",  # Valid 2-line
        "Line One\nLine Two\nLine Three",  # Too many lines
        "Valid Title",  # Valid
        "",  # Empty
        "Title with truncation...",  # Truncated
    ]

    print("=== TITLE VALIDATOR SKILL TEST ===\n")

    for title in test_titles:
        print(f"Title: '{title}'")
        result = validate_title(title)
        print(f"  Valid: {result['valid']}")
        print(f"  Total chars: {result['analysis']['total_chars']}")
        print(f"  Lines: {result['analysis']['line_count']}")
        if result['violations']:
            print(f"  Violations:")
            for v in result['violations']:
                print(f"    - [{v['code']}] {v['description']}")
        if result['revision_hints']:
            print(f"  Hints:")
            for h in result['revision_hints']:
                print(f"    - {h}")
        print()
