"""
Bullet Formatter Skill
Formats bullet points consistently for slide content.

Usage:
    from skills.utilities.bullet_formatter import BulletFormatter, format_bullets

    formatter = BulletFormatter()
    formatted = formatter.format(text)
    # or
    formatted = format_bullets(text)
"""

import re
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field


@dataclass
class BulletFormatResult:
    """Result of bullet formatting."""
    original_text: str
    formatted_text: str
    bullet_count: int
    sub_bullet_count: int
    was_modified: bool
    changes: List[str] = field(default_factory=list)


class BulletFormatter:
    """Format bullet points consistently."""

    # Standard bullet characters
    PRIMARY_BULLET = "•"
    ALT_BULLET = "*"
    SUB_BULLET = "-"

    def __init__(self,
                 primary_bullet: str = "•",
                 sub_bullet: str = "-",
                 normalize_bullets: bool = True,
                 consistent_spacing: bool = True):
        """
        Initialize BulletFormatter.

        Args:
            primary_bullet: Character for main bullets
            sub_bullet: Character for sub-bullets
            normalize_bullets: Convert all bullet chars to standard
            consistent_spacing: Ensure consistent spacing after bullets
        """
        self.primary_bullet = primary_bullet
        self.sub_bullet = sub_bullet
        self.normalize_bullets = normalize_bullets
        self.consistent_spacing = consistent_spacing

    def detect_bullet_type(self, line: str) -> Optional[str]:
        """
        Detect the type of bullet in a line.

        Args:
            line: Line to check

        Returns:
            'primary', 'sub', or None
        """
        stripped = line.lstrip()

        # Check for sub-bullet (indented)
        indent = len(line) - len(stripped)
        if indent >= 2:
            if stripped.startswith(('-', '–', '—', '·', '○')):
                return 'sub'
            if stripped.startswith(('*', '•', '►', '▪')):
                return 'sub'

        # Check for primary bullet
        if stripped.startswith(('*', '•', '-', '–', '—', '►', '▪', '·')):
            return 'primary'

        return None

    def format_line(self, line: str) -> str:
        """
        Format a single line's bullet point.

        Args:
            line: Line to format

        Returns:
            Formatted line
        """
        stripped = line.lstrip()
        indent = len(line) - len(stripped)

        bullet_type = self.detect_bullet_type(line)

        if bullet_type is None:
            return line

        # Extract bullet and content
        match = re.match(r'^([*•\-–—►▪·○]\s*)', stripped)
        if not match:
            return line

        content = stripped[len(match.group(1)):].strip()

        if bullet_type == 'sub':
            # Format as sub-bullet with proper indentation
            return f"  {self.sub_bullet} {content}"
        else:
            # Format as primary bullet
            return f"{self.primary_bullet} {content}"

    def format(self, text: str) -> BulletFormatResult:
        """
        Format all bullet points in text.

        Args:
            text: Text to format

        Returns:
            BulletFormatResult with formatted text and metadata
        """
        if not text:
            return BulletFormatResult(
                original_text="",
                formatted_text="",
                bullet_count=0,
                sub_bullet_count=0,
                was_modified=False
            )

        lines = text.split('\n')
        formatted_lines = []
        changes = []
        bullet_count = 0
        sub_bullet_count = 0

        for i, line in enumerate(lines):
            bullet_type = self.detect_bullet_type(line)

            if bullet_type is not None:
                formatted = self.format_line(line)
                formatted_lines.append(formatted)

                if bullet_type == 'primary':
                    bullet_count += 1
                else:
                    sub_bullet_count += 1

                if formatted != line:
                    changes.append(f"Line {i + 1}: '{line.strip()}' -> '{formatted.strip()}'")
            else:
                formatted_lines.append(line)

        formatted_text = '\n'.join(formatted_lines)

        return BulletFormatResult(
            original_text=text,
            formatted_text=formatted_text,
            bullet_count=bullet_count,
            sub_bullet_count=sub_bullet_count,
            was_modified=text != formatted_text,
            changes=changes
        )

    def combine_bullets(self, bullets: List[str], max_items: int = 3) -> str:
        """
        Combine multiple short bullets into fewer lines.

        Args:
            bullets: List of bullet point texts
            max_items: Maximum items to combine per line

        Returns:
            Combined bullet text
        """
        if len(bullets) <= max_items:
            return ", ".join(bullets)

        # Group into chunks
        chunks = []
        for i in range(0, len(bullets), max_items):
            chunk = bullets[i:i + max_items]
            chunks.append(", ".join(chunk))

        return "\n".join(f"{self.primary_bullet} {chunk}" for chunk in chunks)

    def split_bullet(self, bullet_text: str, max_chars: int = 66) -> List[str]:
        """
        Split a long bullet point into multiple lines.

        Args:
            bullet_text: Bullet content (without bullet character)
            max_chars: Maximum characters per line

        Returns:
            List of formatted lines
        """
        if len(bullet_text) <= max_chars - 2:  # Account for bullet and space
            return [f"{self.primary_bullet} {bullet_text}"]

        words = bullet_text.split()
        lines = []
        current_line = ""

        for word in words:
            test_line = f"{current_line} {word}".strip() if current_line else word

            if len(test_line) <= max_chars - 2:
                current_line = test_line
            else:
                if current_line:
                    if not lines:
                        lines.append(f"{self.primary_bullet} {current_line}")
                    else:
                        lines.append(f"  {current_line}")
                current_line = word

        if current_line:
            if not lines:
                lines.append(f"{self.primary_bullet} {current_line}")
            else:
                lines.append(f"  {current_line}")

        return lines

    def format_slide(self, slide: Dict[str, Any]) -> Dict[str, Any]:
        """
        Format bullet points in a slide's body.

        Args:
            slide: Slide dictionary

        Returns:
            Slide with formatted bullets
        """
        result = slide.copy()

        if 'body' in result and result['body']:
            format_result = self.format(result['body'])
            result['body'] = format_result.formatted_text

        return result


def format_bullets(text: str,
                   primary_bullet: str = "•",
                   sub_bullet: str = "-") -> str:
    """
    Convenience function to format bullet points.

    Args:
        text: Text to format
        primary_bullet: Character for main bullets
        sub_bullet: Character for sub-bullets

    Returns:
        Formatted text
    """
    formatter = BulletFormatter(
        primary_bullet=primary_bullet,
        sub_bullet=sub_bullet
    )
    result = formatter.format(text)
    return result.formatted_text


def normalize_bullets(text: str) -> str:
    """Normalize all bullet characters to standard format."""
    formatter = BulletFormatter(normalize_bullets=True)
    result = formatter.format(text)
    return result.formatted_text


def count_bullets(text: str) -> Dict[str, int]:
    """
    Count bullet points in text.

    Args:
        text: Text to analyze

    Returns:
        Dictionary with bullet counts
    """
    formatter = BulletFormatter()
    result = formatter.format(text)
    return {
        'primary': result.bullet_count,
        'sub': result.sub_bullet_count,
        'total': result.bullet_count + result.sub_bullet_count
    }


if __name__ == "__main__":
    # Test
    formatter = BulletFormatter()

    test_text = """* First bullet point
- Second point with different bullet
► Third point with arrow
  * Sub-bullet with asterisk
  - Sub-bullet with dash
• Fourth point with proper bullet
  · Sub-bullet with middle dot

Regular paragraph text

* Final bullet"""

    print("BulletFormatter Test")
    print("=" * 50)
    print("Original:")
    print(test_text)
    print()
    print("Formatted:")
    result = formatter.format(test_text)
    print(result.formatted_text)
    print()
    print(f"Primary bullets: {result.bullet_count}")
    print(f"Sub-bullets: {result.sub_bullet_count}")
    print(f"Was modified: {result.was_modified}")
    print()
    print("Changes:")
    for change in result.changes:
        print(f"  {change}")
