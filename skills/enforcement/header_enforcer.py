"""
Header Enforcement Skill
Ensures headers fit within 36 chars/line, 2 lines max.

IMPORTANT: This skill should NOT truncate text. If headers exceed limits,
use the title_reviser agent to reword them intelligently.

Usage:
    from skills.enforcement.header_enforcer import enforce_header_limits, validate_header
    result = validate_header(header)
    if not result['valid']:
        # Use title_reviser agent to reword - DO NOT truncate
        pass
"""

import re
from typing import Dict, Any, Tuple


# Character limits - Updated to 36 chars, 1 line only (from config/constraints.yaml)
MAX_CHARS_PER_LINE = 36
MAX_LINES = 1

# Common abbreviations for healthcare/nursing
ABBREVIATIONS = {
    'assessment': 'Assessment',
    'administration': 'Admin',
    'communication': 'Comm',
    'complications': 'Complications',
    'considerations': 'Considerations',
    'documentation': 'Documentation',
    'evaluation': 'Evaluation',
    'fundamentals': 'Fundamentals',
    'implementation': 'Implementation',
    'intervention': 'Intervention',
    'management': 'Management',
    'medication': 'Medication',
    'nursing': 'Nursing',
    'pharmacology': 'Pharm',
    'precautions': 'Precautions',
    'prevention': 'Prevention',
    'principles': 'Principles',
    'procedures': 'Procedures',
    'transmission': 'Transmission',
    'transmission-based': 'Transmission-Based',
    'patient': 'Patient',
    'healthcare': 'Healthcare',
    'infection control': 'Infection Ctrl',
}


def abbreviate_text(text: str) -> str:
    """Apply abbreviations to reduce text length."""
    result = text
    for full, abbrev in ABBREVIATIONS.items():
        # Case-insensitive replacement
        pattern = re.compile(re.escape(full), re.IGNORECASE)
        result = pattern.sub(abbrev, result)
    return result


def smart_truncate(text: str, max_chars: int) -> str:
    """
    Truncate text at word boundary, preserving meaning.

    Args:
        text: Text to truncate
        max_chars: Maximum characters allowed

    Returns:
        Truncated text within limit
    """
    if len(text) <= max_chars:
        return text

    # Try to cut at word boundary
    truncated = text[:max_chars]
    last_space = truncated.rfind(' ')

    if last_space > max_chars * 0.6:  # At least 60% preserved
        return truncated[:last_space].rstrip()

    # If no good break point, hard truncate
    return truncated.rstrip()


def split_into_lines(text: str, max_chars: int = MAX_CHARS_PER_LINE) -> list:
    """
    Split text into lines at word boundaries.

    Args:
        text: Text to split
        max_chars: Maximum characters per line

    Returns:
        List of lines
    """
    words = text.split()
    lines = []
    current_line = []
    current_length = 0

    for word in words:
        word_length = len(word)

        if current_length + word_length + (1 if current_line else 0) <= max_chars:
            current_line.append(word)
            current_length += word_length + (1 if len(current_line) > 1 else 0)
        else:
            if current_line:
                lines.append(' '.join(current_line))
            current_line = [word]
            current_length = word_length

    if current_line:
        lines.append(' '.join(current_line))

    return lines


def enforce_header_limits(
    header: str,
    max_chars_per_line: int = MAX_CHARS_PER_LINE,
    max_lines: int = MAX_LINES
) -> str:
    """
    Enforce header character and line limits.

    Strategy:
    1. Try original text, split into lines
    2. If still too long, apply abbreviations
    3. If still too long, smart truncate

    Args:
        header: Original header text
        max_chars_per_line: Max chars per line (default 36)
        max_lines: Max lines (default 2)

    Returns:
        Header within limits

    NOTE: Prefer using title_reviser agent over truncation for better quality.
    """
    # Clean up input
    header = header.strip()
    header = ' '.join(header.split())  # Normalize whitespace

    # Step 1: Try splitting original
    lines = split_into_lines(header, max_chars_per_line)

    if len(lines) <= max_lines and all(len(l) <= max_chars_per_line for l in lines):
        return '\n'.join(lines[:max_lines])

    # Step 2: Apply abbreviations
    abbreviated = abbreviate_text(header)
    lines = split_into_lines(abbreviated, max_chars_per_line)

    if len(lines) <= max_lines and all(len(l) <= max_chars_per_line for l in lines):
        return '\n'.join(lines[:max_lines])

    # Step 3: Truncate to fit
    lines = lines[:max_lines]
    lines = [smart_truncate(line, max_chars_per_line) for line in lines]

    return '\n'.join(lines)


def validate_header(header: str) -> Dict[str, Any]:
    """
    Validate header meets requirements.

    Returns:
        {
            'valid': bool,
            'line_count': int,
            'max_line_length': int,
            'issues': list
        }
    """
    lines = [l for l in header.split('\n') if l.strip()]
    issues = []

    if len(lines) > MAX_LINES:
        issues.append(f"Header has {len(lines)} lines, max is {MAX_LINES}")

    for i, line in enumerate(lines):
        if len(line) > MAX_CHARS_PER_LINE:
            issues.append(f"Line {i+1} has {len(line)} chars, max is {MAX_CHARS_PER_LINE}")

    return {
        'valid': len(issues) == 0,
        'line_count': len(lines),
        'max_line_length': max(len(l) for l in lines) if lines else 0,
        'issues': issues
    }


if __name__ == "__main__":
    # Test cases
    test_headers = [
        "Infection Control and Disease Prevention Fundamentals for Healthcare Settings",
        "The World Health Organization Five Moments for Hand Hygiene Practice",
        "Simple Header",
        "Standard Precautions",
    ]

    for header in test_headers:
        print(f"\nOriginal ({len(header)} chars): {header}")
        fixed = enforce_header_limits(header)
        print(f"Fixed:\n{fixed}")
        print(f"Valid: {validate_header(fixed)['valid']}")
