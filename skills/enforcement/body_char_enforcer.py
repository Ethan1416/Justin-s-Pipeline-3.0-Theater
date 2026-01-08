"""
Body Character Validation Skill (NO TRUNCATION)

IMPORTANT: This skill NO LONGER truncates or wraps text.
PowerPoint handles text wrapping naturally with word_wrap=True.

This skill now only validates/reports on body content.

Usage:
    from skills.enforcement.body_char_enforcer import validate_body_chars
    result = validate_body_chars(body)
"""

from typing import Dict, Any


def validate_body_chars(body: str) -> Dict[str, Any]:
    """
    Validate body content (informational only).

    NO TRUNCATION - PowerPoint handles word wrapping.
    This function only reports statistics about the content.

    Returns:
        {
            'valid': bool,  # Always True - no char limit enforced
            'max_line_length': int,
            'total_chars': int,
            'line_count': int,
            'has_truncation_markers': bool,
            'issues': list  # Warnings only, not failures
        }
    """
    lines = body.split('\n')
    non_empty_lines = [l for l in lines if l.strip()]

    max_len = max((len(l) for l in lines if l.strip()), default=0)
    total_chars = len(body)

    # Check for truncation markers (ellipsis) which indicate prior truncation
    has_ellipsis = "..." in body or "\u2026" in body

    issues = []
    if has_ellipsis:
        issues.append("WARNING: Content contains truncation markers ('...' or '…')")

    return {
        'valid': True,  # Always valid - no char limit
        'max_line_length': max_len,
        'total_chars': total_chars,
        'line_count': len(non_empty_lines),
        'has_truncation_markers': has_ellipsis,
        'issues': issues
    }


def enforce_body_chars(body: str, max_chars: int = None) -> str:
    """
    DEPRECATED: This function now returns body unchanged.

    PowerPoint handles text wrapping with word_wrap=True.
    This function is kept for backward compatibility but
    performs NO modifications.

    Args:
        body: Original body text
        max_chars: IGNORED - no longer used

    Returns:
        Body unchanged - PowerPoint handles wrapping
    """
    # NO MODIFICATION - return as-is
    return body


# Legacy functions for backward compatibility
def is_bullet_line(line: str) -> bool:
    """Check if line is a bullet point."""
    stripped = line.strip()
    return stripped.startswith(('-', '\u2022', '*', '1.', '2.', '3.', '4.',
                                 '5.', '6.', '7.', '8.', '9.', 'A)', 'B)',
                                 'C)', 'D)'))


def get_indent(line: str) -> str:
    """Get the indentation of a line."""
    return line[:len(line) - len(line.lstrip())]


if __name__ == "__main__":
    # Test
    test_body = """The patient's heart rate of 58 bpm is below the threshold of 60 bpm for holding beta blockers. The nurse should hold the medication and notify the provider for further guidance.

- A) Incorrect because the heart rate is below 60 beats per minute which is the standard hold parameter for beta blockers
- B) Correct answer
- C) Nurses cannot modify prescribed doses independently without provider authorization"""

    print("Original:")
    print(test_body)
    print(f"\nValidation: {validate_body_chars(test_body)}")

    print("\n\nAfter enforce_body_chars (NO CHANGE):")
    result = enforce_body_chars(test_body)
    print(result)
    print(f"\nResult is identical: {result == test_body}")
