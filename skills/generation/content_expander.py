"""
Content Expander
Expands anchor content to slide-ready format with proper constraints.

Usage:
    from skills.generation.content_expander import (
        expand_anchor, fit_to_body, expand_key_points
    )
"""

import re
from typing import Dict, Any, List, Optional


# Constraints
MAX_BODY_LINES = 8
MAX_CHARS_PER_LINE = 66


def expand_anchor(
    anchor_content: Dict[str, Any],
    constraints: Optional[Dict[str, int]] = None
) -> str:
    """
    Expand anchor content into slide body text.

    Args:
        anchor_content: Anchor with summary, key_points, clinical_relevance
        constraints: Optional override for line/char limits

    Returns:
        Formatted body text
    """
    max_lines = constraints.get('max_lines', MAX_BODY_LINES) if constraints else MAX_BODY_LINES
    max_chars = constraints.get('max_chars', MAX_CHARS_PER_LINE) if constraints else MAX_CHARS_PER_LINE

    lines = []

    # Add summary as intro if present
    summary = anchor_content.get('summary', '')
    if summary:
        wrapped = _wrap_text(summary, max_chars)
        lines.extend(wrapped[:2])  # Limit summary to 2 lines

    # Add key points as bullets
    key_points = anchor_content.get('key_points', [])
    for point in key_points:
        if len(lines) >= max_lines:
            break
        bullet_line = f"* {point}"
        wrapped = _wrap_text(bullet_line, max_chars)
        for line in wrapped:
            if len(lines) < max_lines:
                lines.append(line)

    # Add clinical relevance if space
    clinical = anchor_content.get('clinical_relevance', '')
    if clinical and len(lines) < max_lines - 1:
        lines.append("")
        wrapped = _wrap_text(f"Clinical: {clinical}", max_chars)
        for line in wrapped:
            if len(lines) < max_lines:
                lines.append(line)

    return '\n'.join(lines)


def fit_to_body(
    content: str,
    max_lines: int = MAX_BODY_LINES,
    max_chars: int = MAX_CHARS_PER_LINE
) -> str:
    """
    Fit arbitrary content to body constraints.

    Args:
        content: Raw content text
        max_lines: Maximum lines allowed
        max_chars: Maximum characters per line

    Returns:
        Constrained body text
    """
    lines = content.split('\n')
    result = []

    for line in lines:
        if len(result) >= max_lines:
            break

        if len(line) <= max_chars:
            result.append(line)
        else:
            # Wrap long lines
            wrapped = _wrap_text(line, max_chars)
            for w in wrapped:
                if len(result) < max_lines:
                    result.append(w)

    return '\n'.join(result)


def expand_key_points(
    key_points: List[str],
    max_lines: int = MAX_BODY_LINES,
    max_chars: int = MAX_CHARS_PER_LINE,
    bullet_char: str = "*"
) -> str:
    """
    Expand key points into bulleted list.

    Args:
        key_points: List of key point strings
        max_lines: Maximum lines for output
        max_chars: Maximum chars per line
        bullet_char: Character to use for bullets

    Returns:
        Formatted bullet list
    """
    lines = []

    for point in key_points:
        if len(lines) >= max_lines:
            break

        bullet_line = f"{bullet_char} {point}"

        if len(bullet_line) <= max_chars:
            lines.append(bullet_line)
        else:
            # Wrap with hanging indent
            wrapped = _wrap_text(bullet_line, max_chars)
            for i, w in enumerate(wrapped):
                if len(lines) >= max_lines:
                    break
                if i > 0:
                    w = "  " + w  # Hanging indent
                lines.append(w)

    return '\n'.join(lines)


def _wrap_text(text: str, max_chars: int) -> List[str]:
    """
    Wrap text at word boundaries.

    Args:
        text: Text to wrap
        max_chars: Maximum characters per line

    Returns:
        List of wrapped lines
    """
    if len(text) <= max_chars:
        return [text]

    words = text.split()
    lines = []
    current_line = ""

    for word in words:
        if not current_line:
            current_line = word
        elif len(current_line) + 1 + len(word) <= max_chars:
            current_line += " " + word
        else:
            lines.append(current_line)
            current_line = word

    if current_line:
        lines.append(current_line)

    return lines


if __name__ == "__main__":
    # Test
    anchor = {
        'summary': 'Standard precautions are the minimum infection prevention practices',
        'key_points': [
            'Hand hygiene before and after patient contact',
            'Use of personal protective equipment based on exposure risk',
            'Safe injection practices',
            'Respiratory hygiene and cough etiquette'
        ],
        'clinical_relevance': 'Prevents healthcare-associated infections'
    }

    expanded = expand_anchor(anchor)
    print("Expanded anchor:")
    print(expanded)
    print(f"\nLine count: {len(expanded.split(chr(10)))}")
