"""
Format Generation Agents (HARDCODED)
====================================

Specialized agents for generating HTML and PDF versions of handouts,
with format analysis, copying, and enhancement capabilities.

Includes answer key extraction and separate PDF generation.
"""

from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple
from pathlib import Path
from dataclasses import dataclass, field
import re
import shutil

from .base import Agent, AgentResult, AgentStatus

# Try to import required libraries
try:
    from weasyprint import HTML, CSS
    WEASYPRINT_AVAILABLE = True
except ImportError:
    WEASYPRINT_AVAILABLE = False

try:
    from docx import Document
    DOCX_AVAILABLE = True
except ImportError:
    DOCX_AVAILABLE = False


# =============================================================================
# HARDCODED STYLE TEMPLATES
# =============================================================================

# HARDCODED: CSS styles for HTML/PDF output
HTML_STYLES = {
    "base": """
        body {
            font-family: 'Segoe UI', Arial, sans-serif;
            font-size: 11pt;
            line-height: 1.6;
            color: #333;
            max-width: 8.5in;
            margin: 0 auto;
            padding: 0.5in;
        }
        h1 {
            color: #003366;
            font-size: 20pt;
            border-bottom: 2px solid #003366;
            padding-bottom: 8px;
            margin-top: 0;
        }
        h2 {
            color: #003366;
            font-size: 14pt;
            margin-top: 20px;
            border-bottom: 1px solid #ccc;
            padding-bottom: 4px;
        }
        h3 {
            color: #333;
            font-size: 12pt;
            margin-top: 16px;
        }
        p {
            margin: 10px 0;
        }
        ul, ol {
            margin: 10px 0 10px 20px;
        }
        li {
            margin: 5px 0;
        }
        table {
            border-collapse: collapse;
            width: 100%;
            margin: 15px 0;
        }
        th, td {
            border: 1px solid #ccc;
            padding: 8px 12px;
            text-align: left;
        }
        th {
            background-color: #003366;
            color: white;
            font-weight: bold;
        }
        tr:nth-child(even) {
            background-color: #f9f9f9;
        }
        .answer-line {
            border-bottom: 1px solid #333;
            min-width: 200px;
            display: inline-block;
            margin: 5px 0;
        }
        .question-box {
            border: 1px solid #ccc;
            padding: 15px;
            margin: 10px 0;
            background-color: #f9f9f9;
        }
        .instructions {
            background-color: #e6f3ff;
            padding: 10px 15px;
            border-left: 4px solid #003366;
            margin: 15px 0;
        }
        .header-info {
            display: flex;
            justify-content: space-between;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 1px solid #ccc;
        }
        .name-date {
            font-size: 10pt;
        }
        .name-date span {
            margin-right: 30px;
        }
        blockquote {
            border-left: 4px solid #003366;
            margin: 15px 0;
            padding: 10px 20px;
            background-color: #f5f5f5;
            font-style: italic;
        }
        code {
            background-color: #f4f4f4;
            padding: 2px 6px;
            font-family: 'Courier New', monospace;
            font-size: 10pt;
        }
        .page-break {
            page-break-after: always;
        }
    """,
    "answer_key": """
        body {
            font-family: 'Segoe UI', Arial, sans-serif;
            font-size: 11pt;
            line-height: 1.6;
            color: #333;
            max-width: 8.5in;
            margin: 0 auto;
            padding: 0.5in;
        }
        h1 {
            color: #8B0000;
            font-size: 20pt;
            border-bottom: 2px solid #8B0000;
            padding-bottom: 8px;
        }
        h2 {
            color: #8B0000;
            font-size: 14pt;
        }
        .answer {
            color: #006400;
            font-weight: bold;
            background-color: #e6ffe6;
            padding: 5px 10px;
            margin: 5px 0;
            border-left: 4px solid #006400;
        }
        .question {
            margin: 15px 0 5px 0;
            font-weight: bold;
        }
        .watermark {
            color: #8B0000;
            font-size: 14pt;
            text-align: center;
            padding: 10px;
            background-color: #ffe6e6;
            margin-bottom: 20px;
        }
    """
}

# HARDCODED: Table detection patterns
TABLE_PATTERNS = {
    "list_to_table": [
        r"(?:^|\n)(?:\d+\.\s+.+:\s+.+\n?){3,}",  # Numbered items with colons
        r"(?:^|\n)(?:-\s+\w+:\s+.+\n?){3,}",      # Bullet items with colons
        r"(?:^|\n)(?:\w+\s*[-–]\s*.+\n?){4,}",    # Term - definition patterns
    ],
    "comparison": [
        r"(?:compare|contrast|difference|similar|versus|vs\.)",
    ],
    "characteristics": [
        r"(?:character|trait|feature|attribute|quality|element)",
    ]
}

# HARDCODED: Answer patterns to extract
ANSWER_PATTERNS = [
    r"\*\*Answer[s]?:\*\*\s*(.+?)(?=\n\n|\n\*\*|\Z)",
    r"\*\*Key:\*\*\s*(.+?)(?=\n\n|\Z)",
    r"\*\*Correct[^:]*:\*\*\s*(.+?)(?=\n\n|\Z)",
    r"\*\*Expected Response[s]?:\*\*\s*(.+?)(?=\n\n|\Z)",
    r"\*\*Sample Answer[s]?:\*\*\s*(.+?)(?=\n\n|\Z)",
    r"Answer:\s*(.+?)(?=\n\n|\n\d+\.|\Z)",
    r"\(Answer[s]?:\s*([^)]+)\)",
]


# =============================================================================
# FormatAnalyzerAgent
# =============================================================================

class FormatAnalyzerAgent(Agent):
    """
    HARDCODED agent for analyzing document format and structure.

    Identifies:
    - Document type (lesson plan, handout, exit ticket, etc.)
    - Content sections and hierarchy
    - Potential table candidates
    - Answer key content
    """

    def __init__(self):
        super().__init__(name="FormatAnalyzerAgent")

    def _process(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze document format and structure."""
        content = context.get("content", "")
        file_path = context.get("file_path", "")

        if not content:
            return {"success": False, "error": "No content provided"}

        analysis = {
            "document_type": self._detect_document_type(file_path, content),
            "sections": self._identify_sections(content),
            "table_candidates": self._find_table_candidates(content),
            "has_answers": self._has_answer_content(content),
            "answer_sections": self._extract_answer_sections(content),
            "formatting_suggestions": [],
        }

        # Generate formatting suggestions
        if analysis["table_candidates"]:
            analysis["formatting_suggestions"].append({
                "type": "convert_to_table",
                "count": len(analysis["table_candidates"]),
                "reason": "List content suitable for table format"
            })

        if analysis["document_type"] in ["handout", "exit_ticket"]:
            analysis["formatting_suggestions"].append({
                "type": "add_student_info_header",
                "reason": "Student handout should have name/date fields"
            })

        return {
            "success": True,
            "analysis": analysis,
        }

    def _detect_document_type(self, file_path: str, content: str) -> str:
        """Detect document type from filename and content."""
        filename = Path(file_path).stem.lower() if file_path else ""

        if "lesson_plan" in filename:
            return "lesson_plan"
        elif "exit_ticket" in filename:
            return "exit_ticket"
        elif "journal" in filename:
            return "journal_prompts"
        elif "handout" in filename or "activity" in filename:
            return "handout"
        elif "unit_plan" in filename:
            return "unit_plan"

        # Content-based detection
        content_lower = content.lower()
        if "learning objective" in content_lower or "lesson overview" in content_lower:
            return "lesson_plan"
        elif "exit ticket" in content_lower:
            return "exit_ticket"
        elif "journal" in content_lower:
            return "journal_prompts"

        return "handout"

    def _identify_sections(self, content: str) -> List[Dict]:
        """Identify document sections from headings."""
        sections = []
        heading_pattern = r'^(#{1,3})\s+(.+)$'

        for match in re.finditer(heading_pattern, content, re.MULTILINE):
            level = len(match.group(1))
            title = match.group(2).strip()
            sections.append({
                "level": level,
                "title": title,
                "position": match.start(),
            })

        return sections

    def _find_table_candidates(self, content: str) -> List[Dict]:
        """Find content that could be converted to tables."""
        candidates = []

        # Look for list patterns that would work as tables
        for pattern_type, patterns in TABLE_PATTERNS.items():
            for pattern in patterns:
                matches = re.finditer(pattern, content, re.IGNORECASE | re.MULTILINE)
                for match in matches:
                    candidates.append({
                        "type": pattern_type,
                        "content": match.group(0)[:100] + "...",
                        "position": match.start(),
                    })

        return candidates

    def _has_answer_content(self, content: str) -> bool:
        """Check if document contains answer key content."""
        for pattern in ANSWER_PATTERNS:
            if re.search(pattern, content, re.IGNORECASE | re.DOTALL):
                return True
        return False

    def _extract_answer_sections(self, content: str) -> List[Dict]:
        """Extract answer sections from content."""
        answers = []

        for pattern in ANSWER_PATTERNS:
            for match in re.finditer(pattern, content, re.IGNORECASE | re.DOTALL):
                answers.append({
                    "pattern": pattern[:30],
                    "content": match.group(0)[:200],
                    "position": match.start(),
                })

        return answers


# =============================================================================
# FormatCopierAgent
# =============================================================================

class FormatCopierAgent(Agent):
    """
    HARDCODED agent for copying formatting from one document to another.

    Maintains consistent styling across document types.
    """

    def __init__(self):
        super().__init__(name="FormatCopierAgent")

    def _process(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Copy format from source to target document."""
        source_format = context.get("source_format", {})
        target_content = context.get("target_content", "")
        document_type = context.get("document_type", "handout")

        if not target_content:
            return {"success": False, "error": "No target content provided"}

        # Apply consistent formatting based on document type
        formatted_content = self._apply_format(target_content, document_type, source_format)

        return {
            "success": True,
            "formatted_content": formatted_content,
            "document_type": document_type,
        }

    def _apply_format(self, content: str, doc_type: str, source_format: Dict) -> str:
        """Apply formatting rules to content."""
        # Normalize headings
        content = self._normalize_headings(content, doc_type)

        # Normalize lists
        content = self._normalize_lists(content)

        # Add consistent spacing
        content = self._normalize_spacing(content)

        return content

    def _normalize_headings(self, content: str, doc_type: str) -> str:
        """Normalize heading levels based on document type."""
        # Ensure document starts with H1
        if not re.match(r'^#\s', content):
            lines = content.split('\n')
            # Find first heading and make it H1
            for i, line in enumerate(lines):
                if line.startswith('##'):
                    lines[i] = '#' + line[2:]
                    break
            content = '\n'.join(lines)

        return content

    def _normalize_lists(self, content: str) -> str:
        """Normalize list formatting."""
        # Convert * bullets to - bullets for consistency
        content = re.sub(r'^\*\s+', '- ', content, flags=re.MULTILINE)
        return content

    def _normalize_spacing(self, content: str) -> str:
        """Normalize paragraph spacing."""
        # Ensure blank line before headings
        content = re.sub(r'([^\n])\n(#{1,3}\s)', r'\1\n\n\2', content)
        # Remove excessive blank lines
        content = re.sub(r'\n{4,}', '\n\n\n', content)
        return content


# =============================================================================
# FormatEnhancerAgent
# =============================================================================

class FormatEnhancerAgent(Agent):
    """
    HARDCODED agent for enhancing document format.

    Improvements include:
    - Converting suitable lists to tables
    - Adding visual structure
    - Improving readability
    """

    def __init__(self):
        super().__init__(name="FormatEnhancerAgent")

    def _process(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Enhance document formatting."""
        content = context.get("content", "")
        analysis = context.get("analysis", {})
        document_type = context.get("document_type", "handout")

        if not content:
            return {"success": False, "error": "No content provided"}

        enhanced_content = content
        enhancements_made = []

        # Convert suitable lists to tables
        enhanced_content, table_conversions = self._convert_lists_to_tables(enhanced_content)
        if table_conversions:
            enhancements_made.append(f"Converted {table_conversions} list(s) to table(s)")

        # Add answer lines for handouts
        if document_type in ["handout", "exit_ticket"]:
            enhanced_content, lines_added = self._add_answer_lines(enhanced_content)
            if lines_added:
                enhancements_made.append(f"Added {lines_added} answer line(s)")

        # Add question boxes
        enhanced_content, boxes_added = self._add_question_boxes(enhanced_content)
        if boxes_added:
            enhancements_made.append(f"Added {boxes_added} question box(es)")

        return {
            "success": True,
            "enhanced_content": enhanced_content,
            "enhancements": enhancements_made,
        }

    def _convert_lists_to_tables(self, content: str) -> Tuple[str, int]:
        """Convert definition-style lists to tables."""
        conversions = 0

        # Pattern: term: definition format
        pattern = r'((?:^-\s+\*\*[^*]+\*\*:\s*.+$\n?){3,})'

        def convert_to_table(match):
            nonlocal conversions
            lines = match.group(1).strip().split('\n')

            table = "\n| Term | Description |\n|------|-------------|\n"
            for line in lines:
                # Parse "- **Term**: Description"
                m = re.match(r'-\s+\*\*([^*]+)\*\*:\s*(.+)', line)
                if m:
                    term = m.group(1)
                    desc = m.group(2)
                    table += f"| {term} | {desc} |\n"

            conversions += 1
            return table

        content = re.sub(pattern, convert_to_table, content, flags=re.MULTILINE)
        return content, conversions

    def _add_answer_lines(self, content: str) -> Tuple[str, int]:
        """Add answer lines where appropriate."""
        lines_added = 0

        # Add lines after questions that expect written responses
        pattern = r'(\d+\.\s+(?:Explain|Describe|Write|How|Why|What)[^?]*\?)'

        def add_line(match):
            nonlocal lines_added
            lines_added += 1
            return match.group(1) + "\n\n<div class='answer-line'>&nbsp;</div>\n<div class='answer-line'>&nbsp;</div>\n"

        content = re.sub(pattern, add_line, content, flags=re.IGNORECASE)
        return content, lines_added

    def _add_question_boxes(self, content: str) -> Tuple[str, int]:
        """Wrap question sections in styled boxes."""
        boxes_added = 0

        # Wrap "Question X:" sections
        pattern = r'(###?\s*Question\s*\d+[^#]*?)(?=###?\s*Question|\Z)'

        def add_box(match):
            nonlocal boxes_added
            boxes_added += 1
            return f"\n<div class='question-box'>\n{match.group(1)}\n</div>\n"

        content = re.sub(pattern, add_box, content, flags=re.IGNORECASE | re.DOTALL)
        return content, boxes_added


# =============================================================================
# HTMLGeneratorAgent
# =============================================================================

class HTMLGeneratorAgent(Agent):
    """
    HARDCODED agent for generating HTML from markdown content.

    Creates properly formatted HTML5 documents with embedded CSS.
    """

    def __init__(self):
        super().__init__(name="HTMLGeneratorAgent")

    def _process(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Generate HTML from markdown content."""
        content = context.get("content", "")
        title = context.get("title", "Document")
        output_path = context.get("output_path", "")
        document_type = context.get("document_type", "handout")
        is_answer_key = context.get("is_answer_key", False)

        if not content:
            return {"success": False, "error": "No content provided"}

        # Convert markdown to HTML
        html_body = self._markdown_to_html(content)

        # Add student info header for handouts
        if document_type in ["handout", "exit_ticket"] and not is_answer_key:
            html_body = self._add_student_header(title) + html_body

        # Build complete HTML document
        css = HTML_STYLES["answer_key"] if is_answer_key else HTML_STYLES["base"]

        html_doc = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
{css}
    </style>
</head>
<body>
{html_body}
</body>
</html>"""

        # Save if output path provided
        if output_path:
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(html_doc)

        return {
            "success": True,
            "html": html_doc,
            "output_path": str(output_path) if output_path else None,
        }

    def _markdown_to_html(self, content: str) -> str:
        """Convert markdown to HTML."""
        html = content

        # Convert headings
        html = re.sub(r'^### (.+)$', r'<h3>\1</h3>', html, flags=re.MULTILINE)
        html = re.sub(r'^## (.+)$', r'<h2>\1</h2>', html, flags=re.MULTILINE)
        html = re.sub(r'^# (.+)$', r'<h1>\1</h1>', html, flags=re.MULTILINE)

        # Convert bold and italic
        html = re.sub(r'\*\*\*([^*]+)\*\*\*', r'<strong><em>\1</em></strong>', html)
        html = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', html)
        html = re.sub(r'\*([^*]+)\*', r'<em>\1</em>', html)

        # Convert bullet lists
        html = self._convert_bullet_lists(html)

        # Convert numbered lists
        html = self._convert_numbered_lists(html)

        # Convert tables
        html = self._convert_tables(html)

        # Convert blockquotes
        html = re.sub(r'^>\s*(.+)$', r'<blockquote>\1</blockquote>', html, flags=re.MULTILINE)

        # Convert horizontal rules
        html = re.sub(r'^---+$', r'<hr>', html, flags=re.MULTILINE)

        # Convert paragraphs (lines not already converted)
        lines = html.split('\n')
        result_lines = []
        for line in lines:
            stripped = line.strip()
            if stripped and not stripped.startswith('<') and not stripped.startswith('|'):
                result_lines.append(f'<p>{stripped}</p>')
            else:
                result_lines.append(line)
        html = '\n'.join(result_lines)

        return html

    def _convert_bullet_lists(self, html: str) -> str:
        """Convert markdown bullet lists to HTML."""
        lines = html.split('\n')
        result = []
        in_list = False

        for line in lines:
            if re.match(r'^-\s+', line):
                if not in_list:
                    result.append('<ul>')
                    in_list = True
                item = re.sub(r'^-\s+', '', line)
                result.append(f'  <li>{item}</li>')
            else:
                if in_list:
                    result.append('</ul>')
                    in_list = False
                result.append(line)

        if in_list:
            result.append('</ul>')

        return '\n'.join(result)

    def _convert_numbered_lists(self, html: str) -> str:
        """Convert markdown numbered lists to HTML."""
        lines = html.split('\n')
        result = []
        in_list = False

        for line in lines:
            if re.match(r'^\d+\.\s+', line):
                if not in_list:
                    result.append('<ol>')
                    in_list = True
                item = re.sub(r'^\d+\.\s+', '', line)
                result.append(f'  <li>{item}</li>')
            else:
                if in_list:
                    result.append('</ol>')
                    in_list = False
                result.append(line)

        if in_list:
            result.append('</ol>')

        return '\n'.join(result)

    def _convert_tables(self, html: str) -> str:
        """Convert markdown tables to HTML."""
        # Pattern for markdown tables
        table_pattern = r'(\|[^\n]+\|\n\|[-| ]+\|\n(?:\|[^\n]+\|\n?)+)'

        def convert_table(match):
            table_md = match.group(1)
            rows = table_md.strip().split('\n')

            html_table = '<table>\n'

            for i, row in enumerate(rows):
                if '---' in row:
                    continue

                cells = [c.strip() for c in row.split('|')[1:-1]]

                if i == 0:
                    html_table += '  <thead>\n    <tr>\n'
                    for cell in cells:
                        html_table += f'      <th>{cell}</th>\n'
                    html_table += '    </tr>\n  </thead>\n  <tbody>\n'
                else:
                    html_table += '    <tr>\n'
                    for cell in cells:
                        html_table += f'      <td>{cell}</td>\n'
                    html_table += '    </tr>\n'

            html_table += '  </tbody>\n</table>'
            return html_table

        return re.sub(table_pattern, convert_table, html)

    def _add_student_header(self, title: str) -> str:
        """Add student name/date header for handouts."""
        return f"""
<div class="header-info">
    <div><strong>{title}</strong></div>
    <div class="name-date">
        <span>Name: _______________________</span>
        <span>Date: _______________</span>
        <span>Period: _____</span>
    </div>
</div>
"""


# =============================================================================
# PDFGeneratorAgent
# =============================================================================

class PDFGeneratorAgent(Agent):
    """
    HARDCODED agent for generating PDF from HTML content.

    Uses WeasyPrint for high-quality PDF generation.
    """

    def __init__(self):
        super().__init__(name="PDFGeneratorAgent")

    def _process(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Generate PDF from HTML content."""
        html_content = context.get("html", "")
        output_path = context.get("output_path", "")

        if not html_content:
            return {"success": False, "error": "No HTML content provided"}

        if not output_path:
            return {"success": False, "error": "No output path provided"}

        if not WEASYPRINT_AVAILABLE:
            return {
                "success": False,
                "error": "WeasyPrint not available. Install with: pip install weasyprint"
            }

        try:
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)

            # Generate PDF
            HTML(string=html_content).write_pdf(str(output_path))

            return {
                "success": True,
                "output_path": str(output_path),
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }


# =============================================================================
# AnswerKeyExtractorAgent
# =============================================================================

class AnswerKeyExtractorAgent(Agent):
    """
    HARDCODED agent for extracting answer keys from handouts.

    Separates answers from student materials.
    """

    def __init__(self):
        super().__init__(name="AnswerKeyExtractorAgent")

    def _process(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Extract answer key from content."""
        content = context.get("content", "")
        title = context.get("title", "Document")

        if not content:
            return {"success": False, "error": "No content provided"}

        # Extract answers
        answers = []
        clean_content = content

        for pattern in ANSWER_PATTERNS:
            matches = list(re.finditer(pattern, content, re.IGNORECASE | re.DOTALL))
            for match in matches:
                answers.append({
                    "full_match": match.group(0),
                    "answer_text": match.group(1) if match.lastindex else match.group(0),
                    "position": match.start(),
                })
                # Remove from clean content
                clean_content = clean_content.replace(match.group(0), "")

        # Also look for inline answers in parentheses
        inline_pattern = r'\s*\([Aa]nswer[s]?:[^)]+\)'
        inline_matches = re.findall(inline_pattern, clean_content)
        for match in inline_matches:
            answers.append({
                "full_match": match,
                "answer_text": match,
                "position": -1,
            })
            clean_content = clean_content.replace(match, "")

        # Clean up extra whitespace
        clean_content = re.sub(r'\n{3,}', '\n\n', clean_content)

        return {
            "success": True,
            "has_answers": len(answers) > 0,
            "answer_count": len(answers),
            "answers": answers,
            "clean_content": clean_content,
            "original_title": title,
        }


# =============================================================================
# AnswerKeyGeneratorAgent
# =============================================================================

class AnswerKeyGeneratorAgent(Agent):
    """
    HARDCODED agent for generating answer key PDFs.

    Creates formatted answer key documents.
    """

    def __init__(self):
        super().__init__(name="AnswerKeyGeneratorAgent")
        self.html_generator = HTMLGeneratorAgent()
        self.pdf_generator = PDFGeneratorAgent()

    def _process(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Generate answer key PDF."""
        answers = context.get("answers", [])
        title = context.get("title", "Answer Key")
        output_path = context.get("output_path", "")
        original_content = context.get("original_content", "")

        if not answers and not original_content:
            return {"success": False, "error": "No answers or content provided"}

        # Build answer key content
        ak_content = f"# {title} - ANSWER KEY\n\n"
        ak_content += "<div class='watermark'>TEACHER COPY - ANSWER KEY</div>\n\n"

        if answers:
            ak_content += "## Answers\n\n"
            for i, answer in enumerate(answers, 1):
                answer_text = answer.get("answer_text", "")
                ak_content += f"<div class='question'>Question {i}:</div>\n"
                ak_content += f"<div class='answer'>{answer_text}</div>\n\n"
        elif original_content:
            # If no extracted answers, include full content as reference
            ak_content += "## Complete Reference\n\n"
            ak_content += original_content

        # Generate HTML
        html_result = self.html_generator.execute({
            "content": ak_content,
            "title": f"{title} - Answer Key",
            "is_answer_key": True,
        })

        if not html_result.output.get("success"):
            return {"success": False, "error": "HTML generation failed"}

        # Generate PDF if path provided
        if output_path:
            pdf_result = self.pdf_generator.execute({
                "html": html_result.output.get("html"),
                "output_path": output_path,
            })

            if not pdf_result.output.get("success"):
                return {
                    "success": False,
                    "error": f"PDF generation failed: {pdf_result.output.get('error')}"
                }

            return {
                "success": True,
                "output_path": output_path,
                "answer_count": len(answers),
            }

        return {
            "success": True,
            "html": html_result.output.get("html"),
            "answer_count": len(answers),
        }


# =============================================================================
# ProductionFormatterAgent (Orchestrator)
# =============================================================================

class ProductionFormatterAgent(Agent):
    """
    HARDCODED orchestrator agent for processing all handouts in production.

    Creates HTML and PDF versions, extracts answer keys to separate folder.
    """

    PRODUCTION_PATH = Path(__file__).parent.parent / "production"
    ANSWER_KEY_FOLDER = "answer_keys"

    def __init__(self):
        super().__init__(name="ProductionFormatterAgent")
        self.analyzer = FormatAnalyzerAgent()
        self.copier = FormatCopierAgent()
        self.enhancer = FormatEnhancerAgent()
        self.html_generator = HTMLGeneratorAgent()
        self.pdf_generator = PDFGeneratorAgent()
        self.answer_extractor = AnswerKeyExtractorAgent()
        self.answer_generator = AnswerKeyGeneratorAgent()

    def _process(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Process all handouts in production folder."""
        production_path = context.get("production_path", self.PRODUCTION_PATH)
        production_path = Path(production_path)

        if not production_path.exists():
            return {"success": False, "error": f"Production path not found: {production_path}"}

        # Find all markdown files
        md_files = list(production_path.rglob("*.md"))

        if not md_files:
            return {"success": False, "error": "No markdown files found"}

        results = {
            "total_files": len(md_files),
            "html_generated": 0,
            "pdf_generated": 0,
            "answer_keys_generated": 0,
            "errors": [],
            "files_processed": [],
        }

        for md_file in md_files:
            file_result = self._process_file(md_file, production_path)
            results["files_processed"].append(file_result)

            if file_result.get("html_created"):
                results["html_generated"] += 1
            if file_result.get("pdf_created"):
                results["pdf_generated"] += 1
            if file_result.get("answer_key_created"):
                results["answer_keys_generated"] += 1
            if file_result.get("error"):
                results["errors"].append(file_result["error"])

        results["success"] = len(results["errors"]) == 0
        return results

    def _process_file(self, md_file: Path, production_path: Path) -> Dict[str, Any]:
        """Process a single markdown file."""
        result = {
            "file": str(md_file.relative_to(production_path)),
            "html_created": False,
            "pdf_created": False,
            "answer_key_created": False,
        }

        try:
            # Read content
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()

            # Analyze format
            analysis = self.analyzer.execute({
                "content": content,
                "file_path": str(md_file),
            })

            doc_type = analysis.output.get("analysis", {}).get("document_type", "handout")
            title = self._extract_title(content, md_file)

            # Extract answer key if present
            extract_result = self.answer_extractor.execute({
                "content": content,
                "title": title,
            })

            # Use clean content (answers removed) for student version
            student_content = extract_result.output.get("clean_content", content)

            # Enhance formatting
            enhance_result = self.enhancer.execute({
                "content": student_content,
                "analysis": analysis.output.get("analysis", {}),
                "document_type": doc_type,
            })

            enhanced_content = enhance_result.output.get("enhanced_content", student_content)

            # Generate HTML
            html_path = md_file.with_suffix('.html')
            html_result = self.html_generator.execute({
                "content": enhanced_content,
                "title": title,
                "output_path": str(html_path),
                "document_type": doc_type,
            })

            if html_result.output.get("success"):
                result["html_created"] = True
                result["html_path"] = str(html_path)

            # Generate PDF
            if WEASYPRINT_AVAILABLE and html_result.output.get("html"):
                pdf_path = md_file.with_suffix('.pdf')
                pdf_result = self.pdf_generator.execute({
                    "html": html_result.output.get("html"),
                    "output_path": str(pdf_path),
                })

                if pdf_result.output.get("success"):
                    result["pdf_created"] = True
                    result["pdf_path"] = str(pdf_path)

            # Generate answer key if answers were found
            if extract_result.output.get("has_answers"):
                # Create answer_keys folder in the same unit folder
                unit_folder = md_file.parent
                while unit_folder.name.startswith("Day_"):
                    unit_folder = unit_folder.parent

                ak_folder = unit_folder / self.ANSWER_KEY_FOLDER
                ak_folder.mkdir(exist_ok=True)

                ak_filename = f"{md_file.stem}_answer_key.pdf"
                ak_path = ak_folder / ak_filename

                ak_result = self.answer_generator.execute({
                    "answers": extract_result.output.get("answers", []),
                    "title": title,
                    "output_path": str(ak_path),
                    "original_content": content,
                })

                if ak_result.output.get("success"):
                    result["answer_key_created"] = True
                    result["answer_key_path"] = str(ak_path)

        except Exception as e:
            result["error"] = f"{md_file.name}: {str(e)}"

        return result

    def _extract_title(self, content: str, file_path: Path) -> str:
        """Extract title from content or filename."""
        # Try to get from first heading
        match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
        if match:
            return match.group(1).strip()

        # Generate from filename
        filename = file_path.stem
        return filename.replace('_', ' ').title()
