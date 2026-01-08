"""
Text Splitter
Splits overlong text at word boundaries for slide content.

Usage:
    from skills.utilities.text_splitter import (
        split_at_word_boundary, split_slide_content, smart_split
    )
"""

import re
from typing import List, Tuple, Optional


def split_at_word_boundary(text: str, max_chars: int) -> List[str]:
    """
    Split text at word boundaries to fit character limit.

    Args:
        text: Text to split
        max_chars: Maximum characters per segment

    Returns:
        List of text segments
    """
    if len(text) <= max_chars:
        return [text]

    words = text.split()
    segments = []
    current = ""

    for word in words:
        if not current:
            current = word
        elif len(current) + 1 + len(word) <= max_chars:
            current += " " + word
        else:
            segments.append(current)
            current = word

    if current:
        segments.append(current)

    return segments


def split_slide_content(
    body: str,
    max_lines: int = 8
) -> Tuple[str, Optional[str]]:
    """
    Split slide body content if it exceeds line limit.

    Args:
        body: Slide body text
        max_lines: Maximum lines allowed

    Returns:
        Tuple of (first_part, overflow_part or None)
    """
    lines = body.split('\n')

    if len(lines) <= max_lines:
        return (body, None)

    # Split at max_lines boundary
    first_part = '\n'.join(lines[:max_lines])
    overflow = '\n'.join(lines[max_lines:])

    return (first_part, overflow if overflow.strip() else None)


def smart_split(
    text: str,
    max_chars: int = 66,
    preserve_bullets: bool = True
) -> List[str]:
    """
    Smart split that preserves formatting.

    Args:
        text: Text to split
        max_chars: Maximum chars per line
        preserve_bullets: Keep bullet points on their own lines

    Returns:
        List of properly formatted lines
    """
    lines = text.split('\n')
    result = []

    for line in lines:
        # Check if bullet line
        is_bullet = line.strip().startswith(('*', '-', '*', '.'))

        if len(line) <= max_chars:
            result.append(line)
        else:
            # Split long line
            if is_bullet and preserve_bullets:
                # Extract bullet and text
                match = re.match(r'^(\s*[*\-*\.]\s*)(.*)', line)
                if match:
                    bullet_prefix = match.group(1)
                    text_part = match.group(2)
                    # Split text, add hanging indent for continuations
                    segments = split_at_word_boundary(text_part, max_chars - len(bullet_prefix))
                    for i, seg in enumerate(segments):
                        if i == 0:
                            result.append(bullet_prefix + seg)
                        else:
                            result.append("  " + seg)  # Hanging indent
                else:
                    result.extend(split_at_word_boundary(line, max_chars))
            else:
                result.extend(split_at_word_boundary(line, max_chars))

    return result


def split_for_continuation_slide(
    body: str,
    max_lines: int = 8,
    max_chars: int = 66
) -> List[str]:
    """
    Split body into multiple slide-worth chunks.

    Args:
        body: Full body content
        max_lines: Max lines per slide
        max_chars: Max chars per line

    Returns:
        List of slide body strings
    """
    # First, ensure all lines fit char limit
    formatted_lines = smart_split(body, max_chars)

    # Then split into slide-sized chunks
    slides = []
    current_slide = []

    for line in formatted_lines:
        if len(current_slide) >= max_lines:
            slides.append('\n'.join(current_slide))
            current_slide = []
        current_slide.append(line)

    if current_slide:
        slides.append('\n'.join(current_slide))

    return slides


if __name__ == "__main__":
    # Test
    test_text = """* This is a very long bullet point that definitely exceeds the sixty-six character limit and needs to be wrapped properly
* Short point
* Another long point that needs to be split because it is way too long for a single line in the presentation
* Final point"""

    print("Original:")
    print(test_text)
    print("\nAfter smart_split:")
    for line in smart_split(test_text, 66):
        print(f"[{len(line):2d}] {line}")
