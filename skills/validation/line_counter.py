"""
Line Counter Skill
Counts non-empty lines for constraint validation.

Usage:
    from skills.validation.line_counter import LineCounter, count_lines

    counter = LineCounter()
    result = counter.count(text)
    # or
    line_count = count_lines(text)
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass


@dataclass
class LineCountResult:
    """Result of line counting."""
    total_lines: int
    non_empty_lines: int
    empty_lines: int
    bullet_lines: int
    sub_bullet_lines: int
    is_compliant: bool = True
    limit: Optional[int] = None
    overage: int = 0


class LineCounter:
    """Count lines in text content."""

    # Default limits
    DEFAULT_LIMITS = {
        'header': 2,
        'body': 8,
        'tip': 2,
        'nclex_tip': 2
    }

    def __init__(self,
                 count_blank_lines: bool = False,
                 count_sub_bullets: bool = True):
        """
        Initialize LineCounter.

        Args:
            count_blank_lines: Whether blank lines count toward limit
            count_sub_bullets: Whether sub-bullets count as separate lines
        """
        self.count_blank_lines = count_blank_lines
        self.count_sub_bullets = count_sub_bullets

    def count(self, text: str, limit: Optional[int] = None) -> LineCountResult:
        """
        Count lines in text.

        Args:
            text: Text to count lines in
            limit: Optional line limit to check against

        Returns:
            LineCountResult with counts and compliance info
        """
        if not text:
            return LineCountResult(
                total_lines=0,
                non_empty_lines=0,
                empty_lines=0,
                bullet_lines=0,
                sub_bullet_lines=0,
                is_compliant=True,
                limit=limit,
                overage=0
            )

        lines = text.split('\n')
        total = len(lines)

        non_empty = 0
        empty = 0
        bullets = 0
        sub_bullets = 0

        for line in lines:
            stripped = line.strip()
            if not stripped:
                empty += 1
            else:
                non_empty += 1
                # Check for bullet points
                if stripped.startswith(('*', '-', '•', '·')):
                    if line.startswith(('  ', '\t', '   ')):
                        sub_bullets += 1
                    else:
                        bullets += 1

        # Determine countable lines based on settings
        if self.count_blank_lines:
            countable = total
        else:
            countable = non_empty

        # Check compliance
        overage = 0
        is_compliant = True
        if limit is not None:
            overage = max(0, countable - limit)
            is_compliant = overage == 0

        return LineCountResult(
            total_lines=total,
            non_empty_lines=non_empty,
            empty_lines=empty,
            bullet_lines=bullets,
            sub_bullet_lines=sub_bullets,
            is_compliant=is_compliant,
            limit=limit,
            overage=overage
        )

    def count_header(self, header: str) -> LineCountResult:
        """Count lines in header with 2-line limit."""
        return self.count(header, self.DEFAULT_LIMITS['header'])

    def count_body(self, body: str) -> LineCountResult:
        """Count lines in body with 8-line limit."""
        return self.count(body, self.DEFAULT_LIMITS['body'])

    def count_tip(self, tip: str) -> LineCountResult:
        """Count lines in NCLEX tip with 2-line limit."""
        return self.count(tip, self.DEFAULT_LIMITS['tip'])

    def validate_slide(self, slide: Dict[str, Any]) -> Dict[str, LineCountResult]:
        """
        Validate all text fields in a slide for line counts.

        Args:
            slide: Slide dictionary with header, body, nclex_tip fields

        Returns:
            Dictionary of field -> LineCountResult
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
        Get list of line limit violations for a slide.

        Args:
            slide: Slide dictionary

        Returns:
            List of violation dictionaries
        """
        violations = []
        results = self.validate_slide(slide)

        for field_name, result in results.items():
            if not result.is_compliant:
                violations.append({
                    'field': field_name,
                    'lines': result.non_empty_lines,
                    'limit': result.limit,
                    'overage': result.overage
                })

        return violations


def count_lines(text: str, count_empty: bool = False) -> int:
    """
    Convenience function to count lines.

    Args:
        text: Text to count
        count_empty: Whether to count empty lines

    Returns:
        Line count
    """
    if not text:
        return 0

    lines = text.split('\n')
    if count_empty:
        return len(lines)
    return len([l for l in lines if l.strip()])


def count_non_empty_lines(text: str) -> int:
    """Count non-empty lines in text."""
    return count_lines(text, count_empty=False)


def check_line_limit(text: str, limit: int, count_empty: bool = False) -> Dict[str, Any]:
    """
    Check if text meets line limit.

    Args:
        text: Text to check
        limit: Maximum lines
        count_empty: Whether empty lines count

    Returns:
        Dictionary with compliance result
    """
    counter = LineCounter(count_blank_lines=count_empty)
    result = counter.count(text, limit)
    return {
        'compliant': result.is_compliant,
        'lines': result.non_empty_lines if not count_empty else result.total_lines,
        'limit': limit,
        'overage': result.overage
    }


if __name__ == "__main__":
    # Test
    counter = LineCounter()

    test_text = """First line of content
Second line with some information

* Bullet point 1
* Bullet point 2
  - Sub-bullet A
  - Sub-bullet B
* Bullet point 3

Final summary line"""

    print("LineCounter Test")
    print("=" * 50)

    result = counter.count(test_text, 8)
    print(f"Total lines: {result.total_lines}")
    print(f"Non-empty lines: {result.non_empty_lines}")
    print(f"Empty lines: {result.empty_lines}")
    print(f"Bullet lines: {result.bullet_lines}")
    print(f"Sub-bullet lines: {result.sub_bullet_lines}")
    print(f"Limit: {result.limit}")
    print(f"Overage: {result.overage}")
    print(f"Compliant: {result.is_compliant}")
