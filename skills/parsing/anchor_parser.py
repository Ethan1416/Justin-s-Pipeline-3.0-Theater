"""
Anchor Parser - Parse anchor point documents for NCLEX pipeline.

This module provides specialized parsing for anchor point documents,
extracting structured anchor data from various document formats.

Supports:
- .docx files (requires python-docx)
- .txt files with standard anchor formatting
- Raw text input

Usage:
    from skills.parsing.anchor_parser import AnchorParser

    parser = AnchorParser()
    anchors = parser.parse_file("path/to/anchors.docx")
"""

import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field


@dataclass
class Anchor:
    """Represents a single anchor point."""
    id: str
    number: int
    title: str
    content: str = ""
    full_text: str = ""
    style: str = "Normal"
    metadata: Dict = field(default_factory=dict)


@dataclass
class AnchorParseResult:
    """Container for anchor parsing results."""
    file_path: str
    success: bool
    anchors: List[Anchor] = field(default_factory=list)
    total_count: int = 0
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    metadata: Dict = field(default_factory=dict)


class AnchorParser:
    """Parse anchor point documents."""

    # Patterns for identifying anchors
    ANCHOR_PATTERNS = [
        # "Anchor 1: Title" or "Anchor 1. Title"
        (r'^(?:Anchor\s+)?(\d+)[\.:]\s*(.+)$', 'numbered'),
        # "1. Title" or "1: Title"
        (r'^(\d+)[\.:]\s+(.+)$', 'simple_numbered'),
        # "## Title" (Markdown H2)
        (r'^##\s+(.+)$', 'markdown_h2'),
        # "### Title" (Markdown H3)
        (r'^###\s+(.+)$', 'markdown_h3'),
        # "**Title**" (Bold in Markdown)
        (r'^\*\*(.+?)\*\*$', 'bold'),
        # "Topic: Title" or "Concept: Title"
        (r'^(?:Topic|Concept|Point|Item)\s*\d*[\.:]\s*(.+)$', 'labeled'),
    ]

    # Content delimiters (what separates anchor content from next anchor)
    CONTENT_DELIMITERS = [
        r'^(?:Anchor\s+)?\d+[\.:]\s',  # Next anchor number
        r'^##\s',                       # Next markdown header
        r'^\*\*[^*]+\*\*$',            # Next bold title
        r'^---+$',                      # Horizontal rule
        r'^===+$',                      # Double horizontal rule
    ]

    def __init__(self):
        """Initialize the AnchorParser."""
        pass

    def parse_file(self, file_path: str) -> AnchorParseResult:
        """
        Parse anchors from a file.

        Args:
            file_path: Path to file to parse

        Returns:
            AnchorParseResult with parsed anchors
        """
        path = Path(file_path)
        result = AnchorParseResult(
            file_path=str(path),
            success=False
        )

        if not path.exists():
            result.errors.append(f"File not found: {file_path}")
            return result

        # Route to appropriate parser based on extension
        extension = path.suffix.lower()

        if extension == '.docx':
            return self._parse_docx(path, result)
        elif extension in ['.txt', '.md']:
            return self._parse_text_file(path, result)
        else:
            result.errors.append(f"Unsupported file format: {extension}")
            return result

    def parse_text(self, text: str, source_name: str = "text_input") -> AnchorParseResult:
        """
        Parse anchors from raw text.

        Args:
            text: Raw text content
            source_name: Name for the source

        Returns:
            AnchorParseResult with parsed anchors
        """
        result = AnchorParseResult(
            file_path=source_name,
            success=False
        )

        try:
            anchors = self._extract_anchors_from_text(text)
            result.anchors = anchors
            result.total_count = len(anchors)
            result.success = True

            if not anchors:
                result.warnings.append("No anchors found in text")

        except Exception as e:
            result.errors.append(f"Parse error: {e}")

        return result

    def _parse_docx(self, path: Path, result: AnchorParseResult) -> AnchorParseResult:
        """Parse anchors from a .docx file."""
        try:
            from docx import Document
        except ImportError:
            result.errors.append("python-docx not installed. Run: pip install python-docx")
            return result

        try:
            doc = Document(str(path))

            # Extract text with style information
            paragraphs = []
            for para in doc.paragraphs:
                text = para.text.strip()
                if text:
                    paragraphs.append({
                        'text': text,
                        'style': para.style.name if para.style else 'Normal',
                        'is_heading': 'Heading' in (para.style.name if para.style else '')
                    })

            # Convert to full text for parsing
            full_text = '\n'.join([p['text'] for p in paragraphs])
            anchors = self._extract_anchors_from_text(full_text, paragraphs)

            result.anchors = anchors
            result.total_count = len(anchors)
            result.success = True

            # Add metadata
            try:
                result.metadata = {
                    'author': doc.core_properties.author or '',
                    'title': doc.core_properties.title or '',
                    'paragraphs': len(paragraphs)
                }
            except Exception:
                pass

        except Exception as e:
            result.errors.append(f"Error parsing DOCX: {e}")

        return result

    def _parse_text_file(self, path: Path, result: AnchorParseResult) -> AnchorParseResult:
        """Parse anchors from a text file."""
        try:
            with open(path, 'r', encoding='utf-8') as f:
                text = f.read()

            anchors = self._extract_anchors_from_text(text)
            result.anchors = anchors
            result.total_count = len(anchors)
            result.success = True

            if not anchors:
                result.warnings.append("No anchors found in file")

        except UnicodeDecodeError:
            try:
                # Try with latin-1 encoding
                with open(path, 'r', encoding='latin-1') as f:
                    text = f.read()
                anchors = self._extract_anchors_from_text(text)
                result.anchors = anchors
                result.total_count = len(anchors)
                result.success = True
                result.warnings.append("File read with latin-1 encoding (UTF-8 failed)")
            except Exception as e:
                result.errors.append(f"Encoding error: {e}")

        except Exception as e:
            result.errors.append(f"Error reading file: {e}")

        return result

    def _extract_anchors_from_text(
        self,
        text: str,
        paragraphs: Optional[List[Dict]] = None
    ) -> List[Anchor]:
        """
        Extract anchors from text content.

        Args:
            text: Full text content
            paragraphs: Optional list of paragraph dicts with style info

        Returns:
            List of Anchor objects
        """
        anchors = []
        lines = text.split('\n')
        anchor_num = 0

        i = 0
        while i < len(lines):
            line = lines[i].strip()

            # Try to match anchor patterns
            matched = False
            for pattern, pattern_type in self.ANCHOR_PATTERNS:
                match = re.match(pattern, line, re.IGNORECASE)
                if match:
                    anchor_num += 1
                    groups = match.groups()

                    # Extract title based on pattern type
                    if pattern_type in ['numbered', 'simple_numbered']:
                        explicit_num = int(groups[0])
                        title = groups[1].strip()
                        anchor_num = explicit_num  # Use explicit number
                    else:
                        title = groups[0].strip() if groups else line

                    # Collect content until next anchor
                    content_lines = []
                    j = i + 1
                    while j < len(lines):
                        next_line = lines[j].strip()
                        # Check if this is the start of a new anchor
                        is_new_anchor = False
                        for p, _ in self.ANCHOR_PATTERNS:
                            if re.match(p, next_line, re.IGNORECASE):
                                is_new_anchor = True
                                break
                        if is_new_anchor:
                            break
                        if next_line:
                            content_lines.append(next_line)
                        j += 1

                    content = '\n'.join(content_lines)

                    # Get style from paragraphs if available
                    style = 'Normal'
                    if paragraphs and i < len(paragraphs):
                        style = paragraphs[i].get('style', 'Normal')

                    anchor = Anchor(
                        id=f"anchor_{anchor_num}",
                        number=anchor_num,
                        title=title,
                        content=content,
                        full_text=f"{title}\n{content}".strip(),
                        style=style
                    )
                    anchors.append(anchor)
                    matched = True
                    i = j - 1  # Continue from where content ended
                    break

            i += 1

        return anchors

    def to_dict_list(self, anchors: List[Anchor]) -> List[Dict]:
        """
        Convert list of Anchor objects to list of dictionaries.

        Args:
            anchors: List of Anchor objects

        Returns:
            List of anchor dictionaries
        """
        return [
            {
                'id': a.id,
                'number': a.number,
                'title': a.title,
                'content': a.content,
                'full_text': a.full_text,
                'style': a.style,
                'metadata': a.metadata
            }
            for a in anchors
        ]

    def format_report(self, result: AnchorParseResult) -> str:
        """Format parse result as report."""
        lines = [
            "=" * 60,
            "ANCHOR PARSE REPORT",
            "=" * 60,
            f"File: {result.file_path}",
            f"Status: {'SUCCESS' if result.success else 'FAILED'}",
            f"Anchors Found: {result.total_count}",
            ""
        ]

        if result.errors:
            lines.append("ERRORS:")
            for error in result.errors:
                lines.append(f"  - {error}")
            lines.append("")

        if result.warnings:
            lines.append("WARNINGS:")
            for warn in result.warnings:
                lines.append(f"  - {warn}")
            lines.append("")

        if result.anchors:
            lines.append("-" * 60)
            lines.append("ANCHORS:")
            for anchor in result.anchors[:10]:
                lines.append(f"\n  {anchor.number}. {anchor.title[:50]}")
                if anchor.content:
                    preview = anchor.content[:100].replace('\n', ' ')
                    lines.append(f"     {preview}...")

            if len(result.anchors) > 10:
                lines.append(f"\n  ... and {len(result.anchors) - 10} more anchors")

        lines.append("")
        lines.append("=" * 60)
        return "\n".join(lines)


def parse_anchors(file_path: str) -> AnchorParseResult:
    """Convenience function to parse anchors from file."""
    parser = AnchorParser()
    return parser.parse_file(file_path)


def parse_anchor_text(text: str) -> List[Dict]:
    """Convenience function to parse anchors from text."""
    parser = AnchorParser()
    result = parser.parse_text(text)
    return parser.to_dict_list(result.anchors)


if __name__ == "__main__":
    import sys

    print("Anchor Parser - NCLEX Pipeline Parsing Skill")
    print("=" * 50)

    parser = AnchorParser()

    if len(sys.argv) > 1:
        file_path = sys.argv[1]
        print(f"\nParsing: {file_path}")
        result = parser.parse_file(file_path)
    else:
        # Demo with sample text
        sample_text = """
        Anchor 1: Introduction to Patient Assessment
        This section covers the fundamentals of patient assessment
        including health history and physical examination.

        Anchor 2: Vital Signs Measurement
        Understanding how to measure and interpret vital signs
        is essential for nursing practice.

        Anchor 3: Documentation Standards
        Proper documentation ensures continuity of care
        and legal protection for healthcare providers.

        Anchor 4: Physical Examination Techniques
        Systematic approach to conducting a complete
        physical examination of patients.

        Anchor 5: Patient Communication
        Therapeutic communication techniques for
        effective patient interaction.
        """

        print("\nDemo mode - parsing sample text")
        result = parser.parse_text(sample_text, "demo_input")

    report = parser.format_report(result)
    print(report)

    if result.success:
        print("\nAnchor IDs:", [a.id for a in result.anchors])
