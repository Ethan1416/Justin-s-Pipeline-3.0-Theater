"""
Body Line Enforcement Skill
Ensures body content fits within 12 non-empty lines.

UPDATED: Changed from 8 to 12 lines.
PowerPoint handles text wrapping - we only limit line count.

Usage:
    from skills.enforcement.body_line_enforcer import enforce_body_lines
    result = enforce_body_lines(body)
"""

from typing import Dict, Any, List


MAX_BODY_LINES = 12  # Updated from 8 to 12


def count_non_empty_lines(text: str) -> int:
    """Count non-empty lines in text."""
    return len([l for l in text.split('\n') if l.strip()])


def enforce_body_lines(
    body: str,
    max_lines: int = MAX_BODY_LINES,
    strategy: str = 'truncate'  # Changed default from 'condense' to 'truncate'
) -> Dict[str, Any]:
    """
    Enforce body line limits.

    UPDATED: Simple line limiting only. No content condensation.
    PowerPoint handles text wrapping within lines.

    Args:
        body: Original body text
        max_lines: Maximum non-empty lines (default: 12)
        strategy: 'truncate' (keep first N lines) or 'split' (multiple slides)

    Returns:
        {
            'body': str or list (if split),
            'original_lines': int,
            'final_lines': int,
            'action': str,
            'split_count': int (if split)
        }
    """
    lines = [l for l in body.split('\n') if l.strip()]
    original_count = len(lines)

    if original_count <= max_lines:
        return {
            'body': body,
            'original_lines': original_count,
            'final_lines': original_count,
            'action': 'none',
            'split_count': 1
        }

    if strategy == 'split':
        chunks = split_body_content(body, max_lines)
        return {
            'body': chunks,
            'original_lines': original_count,
            'final_lines': max_lines,
            'action': 'split',
            'split_count': len(chunks)
        }
    else:  # truncate - keep first N lines
        limited_lines = lines[:max_lines]
        return {
            'body': '\n'.join(limited_lines),
            'original_lines': original_count,
            'final_lines': len(limited_lines),
            'action': 'limited',
            'split_count': 1
        }


def split_body_content(body: str, max_lines: int = MAX_BODY_LINES) -> List[str]:
    """
    Split body content into multiple slide-sized chunks.

    Args:
        body: Original body text
        max_lines: Maximum lines per chunk

    Returns:
        List of body chunks, each within line limit
    """
    lines = [l for l in body.split('\n') if l.strip()]

    if len(lines) <= max_lines:
        return [body]

    chunks = []
    for i in range(0, len(lines), max_lines):
        chunk_lines = lines[i:i + max_lines]
        chunks.append('\n'.join(chunk_lines))

    return chunks


def validate_body_lines(body: str, max_lines: int = MAX_BODY_LINES) -> Dict[str, Any]:
    """
    Validate body line count.

    Args:
        body: Body text to validate
        max_lines: Maximum allowed lines (default: 12)

    Returns:
        {
            'valid': bool,
            'line_count': int,
            'max_allowed': int,
            'issues': list
        }
    """
    line_count = count_non_empty_lines(body)
    issues = []

    if line_count > max_lines:
        issues.append(f"Body has {line_count} lines, max is {max_lines}")

    return {
        'valid': line_count <= max_lines,
        'line_count': line_count,
        'max_allowed': max_lines,
        'issues': issues
    }


# Legacy function for backward compatibility (simplified)
def condense_bullets(lines: List[str], target: int = MAX_BODY_LINES) -> List[str]:
    """
    DEPRECATED: Simple truncation instead of complex condensation.

    Just returns first `target` lines.
    """
    return lines[:target]


if __name__ == "__main__":
    # Test
    test_body = """The WHO identifies five critical moments:

1. Before patient contact - protect patient
2. Before aseptic procedure - sterile technique
3. After body fluid exposure - protect self
4. After patient contact - prevent spread
5. After touching surroundings - environment control
6. Additional consideration one
7. Additional consideration two
8. Additional consideration three
9. Line nine
10. Line ten
11. Line eleven
12. Line twelve - at limit
13. Line thirteen - over limit
14. Line fourteen - over limit"""

    print(f"Original lines: {count_non_empty_lines(test_body)}")
    print(f"Max allowed: {MAX_BODY_LINES}")

    # Test truncate
    result = enforce_body_lines(test_body, strategy='truncate')
    print(f"\nLimited to {result['final_lines']} lines:")
    print(result['body'])

    # Test split
    result = enforce_body_lines(test_body, strategy='split')
    print(f"\nSplit into {result['split_count']} slides")

    # Validation
    print(f"\nValidation (before): {validate_body_lines(test_body)}")
    print(f"Validation (after): {validate_body_lines(result['body'][0] if isinstance(result['body'], list) else result['body'])}")
