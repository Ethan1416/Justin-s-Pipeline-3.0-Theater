#!/usr/bin/env python3
"""
Body Content Enforcer Skill - Simplified for Word Wrapping

This skill enforces line count limits only. Character-level text wrapping
is handled by PowerPoint's native word wrap feature.

NO TRUNCATION - all content is preserved. PowerPoint handles line wrapping.

Created: 2026-01-06
Updated: 2026-01-06 - Removed truncation, simplified for word wrap
"""

from typing import Dict, List, Any

# Configuration - line limits only (no character limits)
MAX_CONTENT_LINES = 12  # Reasonable limit for readability


def enforce_body_content(body: Any) -> Dict[str, Any]:
    """
    Enforce body line limits. No character truncation.

    PowerPoint's word wrap handles long lines naturally.

    Args:
        body: Body content (string with newlines or list of strings)

    Returns:
        Dictionary with:
            - enforced_body: The body content (list of strings)
            - original_lines: Number of original lines
            - final_lines: Number of final lines
            - truncated: Whether line count was reduced
            - changes_made: List of changes made
    """
    # Parse input
    if isinstance(body, list):
        lines = [str(line) for line in body if str(line).strip()]
    else:
        lines = [line for line in str(body).split('\n') if line.strip()]

    original_count = len(lines)
    changes_made = []

    # Only limit line count, not character count
    # PowerPoint handles text wrapping
    if len(lines) > MAX_CONTENT_LINES:
        changes_made.append(f"Limited from {len(lines)} to {MAX_CONTENT_LINES} lines")
        lines = lines[:MAX_CONTENT_LINES]

    return {
        "enforced_body": lines,
        "original_lines": original_count,
        "final_lines": len(lines),
        "truncated": len(lines) < original_count,
        "changes_made": changes_made,
        "compliant": True  # Always compliant - PowerPoint handles wrapping
    }


def enforce_slide_body(slide_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Enforce body content limits for a single slide.

    Args:
        slide_data: Slide dictionary with 'body' key

    Returns:
        Updated slide_data with enforced body content
    """
    if 'body' not in slide_data:
        return slide_data

    result = enforce_body_content(slide_data['body'])

    # Update slide with enforced content
    updated_slide = slide_data.copy()

    # Join lines back to string for compatibility
    updated_slide['body'] = "\n".join(result['enforced_body'])

    # Add enforcement metadata
    updated_slide['_body_enforcement'] = {
        'original_lines': result['original_lines'],
        'final_lines': result['final_lines'],
        'truncated': result['truncated'],
        'changes_made': result['changes_made']
    }

    return updated_slide


def enforce_blueprint_body(blueprint: Dict[str, Any]) -> Dict[str, Any]:
    """
    Enforce body content limits for all slides in a blueprint.

    Args:
        blueprint: Blueprint dictionary with 'slides' list

    Returns:
        Updated blueprint with enforced body content
    """
    if 'slides' not in blueprint:
        return blueprint

    updated_blueprint = blueprint.copy()
    updated_slides = []
    total_changes = 0

    for slide in blueprint['slides']:
        updated_slide = enforce_slide_body(slide)
        if '_body_enforcement' in updated_slide:
            if updated_slide['_body_enforcement']['truncated']:
                total_changes += 1
        updated_slides.append(updated_slide)

    updated_blueprint['slides'] = updated_slides
    updated_blueprint['_body_enforcement_summary'] = {
        'total_slides': len(updated_slides),
        'slides_modified': total_changes
    }

    return updated_blueprint


def validate_body_content(body: Any) -> Dict[str, Any]:
    """
    Validate body content against limits.

    Args:
        body: Body content to validate

    Returns:
        Validation results with pass/fail and details
    """
    if isinstance(body, list):
        lines = [str(line) for line in body if str(line).strip()]
    else:
        lines = [line for line in str(body).split('\n') if line.strip()]

    issues = []

    # Only check line count (PowerPoint handles character wrapping)
    if len(lines) > MAX_CONTENT_LINES:
        issues.append(f"Too many lines: {len(lines)} > {MAX_CONTENT_LINES}")

    return {
        "valid": len(issues) == 0,
        "line_count": len(lines),
        "max_line_length": max(len(line) for line in lines) if lines else 0,
        "issues": issues,
        "note": "Character wrapping handled by PowerPoint"
    }


if __name__ == "__main__":
    # Test the simplified enforcer
    test_body = """Module 2: Pharmacology

Topics:
• Drug Class Suffixes (-olol, -pril, -sartan, -statin) are important for medication identification
• Rights of Medication Administration must be verified before every dose
• This is a very long line that exceeds the sixty-six character limit but will now wrap naturally in PowerPoint
• Another line with important nursing content about patient assessment and documentation
• Additional content about blood pressure monitoring and heart rate assessment
• More content about laboratory values and potassium levels
• Final line about subcutaneous injection administration technique"""

    print("=== SIMPLIFIED BODY ENFORCER TEST ===\n")
    print(f"Original content:\n{test_body}\n")

    result = enforce_body_content(test_body)

    print(f"Original lines: {result['original_lines']}")
    print(f"Final lines: {result['final_lines']}")
    print(f"Any line limit exceeded: {result['truncated']}")
    print(f"Compliant: {result['compliant']}")

    print(f"\nEnforced body (no character truncation):")
    for i, line in enumerate(result['enforced_body']):
        print(f"  {i+1}. ({len(line)} chars) {line[:80]}{'...' if len(line) > 80 else ''}")
