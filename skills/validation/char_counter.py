"""
Character Counter Skill
Counts characters per line for constraint validation.

Usage:
    from skills.validation.char_counter import CharCounter, count_chars_per_line

    counter = CharCounter()
    result = counter.count(text)
    # or
    counts = count_chars_per_line(text)
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field


@dataclass
class CharCountResult:
    """Result of character counting."""
    total_chars: int
    line_count: int
    chars_per_line: List[int]
    max_chars_in_line: int
    lines_exceeding_limit: List[int] = field(default_factory=list)
    is_compliant: bool = True


class CharCounter:
    """Count characters in text content."""

    # Default limits from config/constraints.yaml
    DEFAULT_LIMITS = {
        'header': 32,
        'body': 66,
        'tip': 66,
        'nclex_tip': 66
    }

    def __init__(self, limits: Optional[Dict[str, int]] = None):
        """
        Initialize CharCounter.

        Args:
            limits: Custom character limits per field type
        """
        self.limits = limits or self.DEFAULT_LIMITS

    def count(self, text: str, limit: Optional[int] = None) -> CharCountResult:
        """
        Count characters in text.

        Args:
            text: Text to count characters in
            limit: Optional character limit to check against

        Returns:
            CharCountResult with counts and compliance info
        """
        if not text:
            return CharCountResult(
                total_chars=0,
                line_count=0,
                chars_per_line=[],
                max_chars_in_line=0,
                is_compliant=True
            )

        lines = text.split('\n')
        chars_per_line = [len(line) for line in lines]

        exceeding = []
        if limit:
            exceeding = [i + 1 for i, count in enumerate(chars_per_line) if count > limit]

        return CharCountResult(
            total_chars=sum(chars_per_line),
            line_count=len(lines),
            chars_per_line=chars_per_line,
            max_chars_in_line=max(chars_per_line) if chars_per_line else 0,
            lines_exceeding_limit=exceeding,
            is_compliant=len(exceeding) == 0
        )

    def count_header(self, header: str) -> CharCountResult:
        """Count characters in header with 32-char limit."""
        return self.count(header, self.limits.get('header', 32))

    def count_body(self, body: str) -> CharCountResult:
        """Count characters in body with 66-char limit."""
        return self.count(body, self.limits.get('body', 66))

    def count_tip(self, tip: str) -> CharCountResult:
        """Count characters in NCLEX tip with 66-char limit."""
        return self.count(tip, self.limits.get('tip', 66))

    def validate_slide(self, slide: Dict[str, Any]) -> Dict[str, CharCountResult]:
        """
        Validate all text fields in a slide.

        Args:
            slide: Slide dictionary with header, body, nclex_tip fields

        Returns:
            Dictionary of field -> CharCountResult
        """
        results = {}

        if 'header' in slide:
            results['header'] = self.count_header(slide['header'])

        if 'body' in slide:
            results['body'] = self.count_body(slide['body'])

        tip_key = 'nclex_tip' if 'nclex_tip' in slide else 'tip'
        if tip_key in slide and slide[tip_key]:
            results['tip'] = self.count_tip(slide[tip_key])

        return results

    def get_violations(self, slide: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Get list of character limit violations for a slide.

        Args:
            slide: Slide dictionary

        Returns:
            List of violation dictionaries
        """
        violations = []
        results = self.validate_slide(slide)

        for field_name, result in results.items():
            if not result.is_compliant:
                for line_num in result.lines_exceeding_limit:
                    violations.append({
                        'field': field_name,
                        'line': line_num,
                        'chars': result.chars_per_line[line_num - 1],
                        'limit': self.limits.get(field_name, 66),
                        'overage': result.chars_per_line[line_num - 1] - self.limits.get(field_name, 66)
                    })

        return violations


def count_chars_per_line(text: str) -> List[int]:
    """
    Convenience function to count characters per line.

    Args:
        text: Text to count

    Returns:
        List of character counts per line
    """
    if not text:
        return []
    return [len(line) for line in text.split('\n')]


def get_max_char_per_line(text: str) -> int:
    """Get the maximum character count in any line."""
    counts = count_chars_per_line(text)
    return max(counts) if counts else 0


def check_char_limit(text: str, limit: int) -> Dict[str, Any]:
    """
    Check if text meets character limit.

    Args:
        text: Text to check
        limit: Maximum characters per line

    Returns:
        Dictionary with compliance result
    """
    counter = CharCounter()
    result = counter.count(text, limit)
    return {
        'compliant': result.is_compliant,
        'max_chars': result.max_chars_in_line,
        'limit': limit,
        'violations': result.lines_exceeding_limit
    }


if __name__ == "__main__":
    # Test
    counter = CharCounter()

    test_text = """This is a short line
This line is a bit longer than the previous one
This is the longest line in this test and it should definitely exceed the typical 32 character header limit"""

    print("CharCounter Test")
    print("=" * 50)

    result = counter.count(test_text, 32)
    print(f"Total chars: {result.total_chars}")
    print(f"Line count: {result.line_count}")
    print(f"Chars per line: {result.chars_per_line}")
    print(f"Max in line: {result.max_chars_in_line}")
    print(f"Lines exceeding 32: {result.lines_exceeding_limit}")
    print(f"Compliant: {result.is_compliant}")
