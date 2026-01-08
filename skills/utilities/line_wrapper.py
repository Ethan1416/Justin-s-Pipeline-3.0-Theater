"""
Line Wrapper Skill
Wraps text to fit character limits at word boundaries.

Usage:
    from skills.utilities.line_wrapper import LineWrapper, wrap_text

    wrapper = LineWrapper(max_chars=66)
    wrapped = wrapper.wrap(text)
    # or
    lines = wrap_text(text, max_chars=66)
"""

import re
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass


@dataclass
class WrapResult:
    """Result of text wrapping."""
    original_text: str
    wrapped_text: str
    original_lines: int
    wrapped_lines: int
    was_modified: bool
    max_char_per_line: int


class LineWrapper:
    """Wrap text to fit character limits."""

    def __init__(self,
                 max_chars: int = 66,
                 preserve_bullets: bool = True,
                 hanging_indent: str = "  "):
        """
        Initialize LineWrapper.

        Args:
            max_chars: Maximum characters per line
            preserve_bullets: Keep bullet formatting when wrapping
            hanging_indent: Indent for wrapped continuation lines
        """
        self.max_chars = max_chars
        self.preserve_bullets = preserve_bullets
        self.hanging_indent = hanging_indent

    def wrap_line(self, line: str) -> List[str]:
        """
        Wrap a single line to fit character limit.

        Args:
            line: Line to wrap

        Returns:
            List of wrapped lines
        """
        if len(line) <= self.max_chars:
            return [line]

        # Detect bullet point
        bullet_match = re.match(r'^(\s*[*\-•·]\s*)', line)
        if bullet_match and self.preserve_bullets:
            bullet_prefix = bullet_match.group(1)
            text = line[len(bullet_prefix):]
            continuation_prefix = " " * len(bullet_prefix)
        else:
            bullet_prefix = ""
            continuation_prefix = self.hanging_indent
            text = line

        # Calculate available width
        first_line_width = self.max_chars - len(bullet_prefix)
        continuation_width = self.max_chars - len(continuation_prefix)

        # Split into words
        words = text.split()
        lines = []
        current_line = ""
        is_first_line = True

        for word in words:
            max_width = first_line_width if is_first_line else continuation_width

            if not current_line:
                current_line = word
            elif len(current_line) + 1 + len(word) <= max_width:
                current_line += " " + word
            else:
                # Output current line
                if is_first_line:
                    lines.append(bullet_prefix + current_line)
                    is_first_line = False
                else:
                    lines.append(continuation_prefix + current_line)
                current_line = word

        # Output final line
        if current_line:
            if is_first_line:
                lines.append(bullet_prefix + current_line)
            else:
                lines.append(continuation_prefix + current_line)

        return lines

    def wrap(self, text: str) -> WrapResult:
        """
        Wrap text to fit character limits.

        Args:
            text: Text to wrap

        Returns:
            WrapResult with wrapped text and metadata
        """
        if not text:
            return WrapResult(
                original_text="",
                wrapped_text="",
                original_lines=0,
                wrapped_lines=0,
                was_modified=False,
                max_char_per_line=0
            )

        original_lines = text.split('\n')
        wrapped_lines = []

        for line in original_lines:
            wrapped_lines.extend(self.wrap_line(line))

        wrapped_text = '\n'.join(wrapped_lines)
        max_char = max(len(line) for line in wrapped_lines) if wrapped_lines else 0

        return WrapResult(
            original_text=text,
            wrapped_text=wrapped_text,
            original_lines=len(original_lines),
            wrapped_lines=len(wrapped_lines),
            was_modified=text != wrapped_text,
            max_char_per_line=max_char
        )

    def wrap_header(self, header: str) -> WrapResult:
        """Wrap header with 32-char limit."""
        wrapper = LineWrapper(max_chars=32, preserve_bullets=False)
        return wrapper.wrap(header)

    def wrap_body(self, body: str) -> WrapResult:
        """Wrap body with 66-char limit."""
        return self.wrap(body)

    def wrap_tip(self, tip: str) -> WrapResult:
        """Wrap NCLEX tip with 66-char limit."""
        wrapper = LineWrapper(max_chars=66, preserve_bullets=False)
        return wrapper.wrap(tip)

    def wrap_slide(self, slide: Dict[str, Any]) -> Dict[str, Any]:
        """
        Wrap all text fields in a slide.

        Args:
            slide: Slide dictionary

        Returns:
            Slide with wrapped text
        """
        result = slide.copy()

        if 'header' in result:
            wrap_result = self.wrap_header(result['header'])
            result['header'] = wrap_result.wrapped_text

        if 'body' in result:
            wrap_result = self.wrap_body(result['body'])
            result['body'] = wrap_result.wrapped_text

        tip_key = 'nclex_tip' if 'nclex_tip' in result else 'tip'
        if tip_key in result and result[tip_key]:
            wrap_result = self.wrap_tip(result[tip_key])
            result[tip_key] = wrap_result.wrapped_text

        return result


def wrap_text(text: str, max_chars: int = 66, preserve_bullets: bool = True) -> str:
    """
    Convenience function to wrap text.

    Args:
        text: Text to wrap
        max_chars: Maximum characters per line
        preserve_bullets: Keep bullet formatting

    Returns:
        Wrapped text
    """
    wrapper = LineWrapper(max_chars=max_chars, preserve_bullets=preserve_bullets)
    result = wrapper.wrap(text)
    return result.wrapped_text


def wrap_to_lines(text: str, max_chars: int = 66) -> List[str]:
    """
    Wrap text and return as list of lines.

    Args:
        text: Text to wrap
        max_chars: Maximum characters per line

    Returns:
        List of wrapped lines
    """
    wrapped = wrap_text(text, max_chars)
    return wrapped.split('\n') if wrapped else []


def wrap_header(header: str) -> str:
    """Wrap header to 32 characters per line."""
    return wrap_text(header, max_chars=32, preserve_bullets=False)


def wrap_body(body: str) -> str:
    """Wrap body to 66 characters per line."""
    return wrap_text(body, max_chars=66, preserve_bullets=True)


if __name__ == "__main__":
    # Test
    wrapper = LineWrapper(max_chars=66)

    test_text = """* This is a very long bullet point that definitely exceeds the sixty-six character limit and needs to be wrapped properly at word boundaries
* Short bullet point
* Another extremely long bullet point that contains a lot of information about various topics and should be split across multiple lines
  - A sub-bullet that is also quite long and needs wrapping to fit within limits"""

    print("LineWrapper Test")
    print("=" * 50)
    print("Original:")
    print(test_text)
    print()
    print("Wrapped:")
    result = wrapper.wrap(test_text)
    print(result.wrapped_text)
    print()
    print(f"Original lines: {result.original_lines}")
    print(f"Wrapped lines: {result.wrapped_lines}")
    print(f"Max char per line: {result.max_char_per_line}")
    print(f"Was modified: {result.was_modified}")
