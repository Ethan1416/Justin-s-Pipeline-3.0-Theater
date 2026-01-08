"""
Constraint Validator - Validate character and line limits for NCLEX pipeline.

This module validates slide content against the constraints defined in
config/constraints.yaml, including character limits, line limits, and
visual-specific constraints.

Usage:
    from skills.validation.constraint_validator import ConstraintValidator

    validator = ConstraintValidator()
    result = validator.validate_slide(slide_content)
"""

import re
from pathlib import Path
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, field


@dataclass
class ConstraintViolation:
    """Represents a single constraint violation."""
    field: str
    constraint_type: str  # "char_limit", "line_limit", "element_count"
    actual_value: int
    max_allowed: int
    line_number: Optional[int] = None
    message: str = ""


@dataclass
class SlideValidationResult:
    """Container for slide validation results."""
    slide_id: str
    is_valid: bool
    violations: List[ConstraintViolation] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    stats: Dict = field(default_factory=dict)


@dataclass
class BatchValidationResult:
    """Container for batch validation results."""
    total_slides: int
    valid_slides: int
    invalid_slides: int
    total_violations: int
    slide_results: List[SlideValidationResult] = field(default_factory=list)
    summary: Dict = field(default_factory=dict)


class ConstraintValidator:
    """Validate content against character and line constraints."""

    # Default constraints (fallback if config not loaded)
    # CANONICAL VALUES from config/constraints.yaml
    DEFAULT_CONSTRAINTS = {
        'title': {'chars_per_line': 32, 'max_lines': 2},
        'body': {'chars_per_line': 66, 'max_lines': 8},  # Fixed: was 10, now 8 per R2
        'tip': {'chars_per_line': 66, 'max_lines': 2, 'total_max_chars': 132},
        'presenter_notes': {'max_words': 450, 'max_duration_seconds': 180}
    }

    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize the ConstraintValidator.

        Args:
            config_path: Path to constraints.yaml config
        """
        self.constraints = self._load_constraints(config_path)

    def _load_constraints(self, config_path: Optional[str]) -> Dict:
        """Load constraints from configuration."""
        if config_path is None:
            base_path = Path(__file__).parent.parent.parent
            config_path = base_path / "config" / "constraints.yaml"
        else:
            config_path = Path(config_path)

        if config_path.exists():
            try:
                import yaml
                with open(config_path, 'r', encoding='utf-8') as f:
                    config = yaml.safe_load(f)
                return config
            except Exception as e:
                print(f"Warning: Could not load constraints: {e}")

        return {'character_limits': self.DEFAULT_CONSTRAINTS}

    def get_constraint(self, field: str, constraint_key: str) -> Optional[int]:
        """
        Get a specific constraint value.

        Args:
            field: Field name (title, body, tip, etc.)
            constraint_key: Constraint key (chars_per_line, max_lines, etc.)

        Returns:
            Constraint value or None
        """
        char_limits = self.constraints.get('character_limits', {})
        field_constraints = char_limits.get(field, {})
        return field_constraints.get(constraint_key)

    def count_lines(self, text: str) -> int:
        """Count non-empty lines in text."""
        if not text:
            return 0
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        return len(lines)

    def count_chars_per_line(self, text: str) -> List[int]:
        """Get character count for each line."""
        if not text:
            return []
        return [len(line) for line in text.split('\n')]

    def count_words(self, text: str) -> int:
        """Count words in text, excluding markers like [PAUSE]."""
        if not text:
            return 0
        # Remove markers
        cleaned = re.sub(r'\[[^\]]+\]', '', text)
        return len(cleaned.split())

    def validate_title(
        self,
        title: str,
        slide_id: str = "unknown"
    ) -> List[ConstraintViolation]:
        """
        Validate title against constraints.

        Args:
            title: Title text
            slide_id: Slide identifier for error messages

        Returns:
            List of violations
        """
        violations = []
        char_limits = self.constraints.get('character_limits', {}).get('title', {})

        max_chars = char_limits.get('chars_per_line', self.DEFAULT_CONSTRAINTS['title']['chars_per_line'])
        max_lines = char_limits.get('max_lines', self.DEFAULT_CONSTRAINTS['title']['max_lines'])

        # Check line count
        line_count = self.count_lines(title)
        if line_count > max_lines:
            violations.append(ConstraintViolation(
                field="title",
                constraint_type="line_limit",
                actual_value=line_count,
                max_allowed=max_lines,
                message=f"Title has {line_count} lines (max {max_lines})"
            ))

        # Check character count per line
        for i, char_count in enumerate(self.count_chars_per_line(title)):
            if char_count > max_chars:
                violations.append(ConstraintViolation(
                    field="title",
                    constraint_type="char_limit",
                    actual_value=char_count,
                    max_allowed=max_chars,
                    line_number=i + 1,
                    message=f"Title line {i + 1} has {char_count} chars (max {max_chars})"
                ))

        return violations

    def validate_body(
        self,
        body: str,
        slide_id: str = "unknown"
    ) -> List[ConstraintViolation]:
        """
        Validate body text against constraints.

        Args:
            body: Body text
            slide_id: Slide identifier

        Returns:
            List of violations
        """
        violations = []
        char_limits = self.constraints.get('character_limits', {}).get('body', {})

        max_chars = char_limits.get('chars_per_line', self.DEFAULT_CONSTRAINTS['body']['chars_per_line'])
        max_lines = char_limits.get('max_lines', self.DEFAULT_CONSTRAINTS['body']['max_lines'])

        # Check line count
        line_count = self.count_lines(body)
        if line_count > max_lines:
            violations.append(ConstraintViolation(
                field="body",
                constraint_type="line_limit",
                actual_value=line_count,
                max_allowed=max_lines,
                message=f"Body has {line_count} lines (max {max_lines})"
            ))

        # Check character count per line
        for i, char_count in enumerate(self.count_chars_per_line(body)):
            if char_count > max_chars:
                violations.append(ConstraintViolation(
                    field="body",
                    constraint_type="char_limit",
                    actual_value=char_count,
                    max_allowed=max_chars,
                    line_number=i + 1,
                    message=f"Body line {i + 1} has {char_count} chars (max {max_chars})"
                ))

        return violations

    def validate_tip(
        self,
        tip: str,
        slide_id: str = "unknown"
    ) -> List[ConstraintViolation]:
        """
        Validate tip text against constraints.

        Args:
            tip: Tip text
            slide_id: Slide identifier

        Returns:
            List of violations
        """
        violations = []

        # Skip validation for empty or "None" tips
        if not tip or tip.strip().lower() in ['none', 'n/a', '']:
            return violations

        char_limits = self.constraints.get('character_limits', {}).get('tip', {})

        max_chars = char_limits.get('chars_per_line', self.DEFAULT_CONSTRAINTS['tip']['chars_per_line'])
        max_lines = char_limits.get('max_lines', self.DEFAULT_CONSTRAINTS['tip']['max_lines'])

        # Check line count
        line_count = self.count_lines(tip)
        if line_count > max_lines:
            violations.append(ConstraintViolation(
                field="tip",
                constraint_type="line_limit",
                actual_value=line_count,
                max_allowed=max_lines,
                message=f"Tip has {line_count} lines (max {max_lines})"
            ))

        # Check character count per line
        for i, char_count in enumerate(self.count_chars_per_line(tip)):
            if char_count > max_chars:
                violations.append(ConstraintViolation(
                    field="tip",
                    constraint_type="char_limit",
                    actual_value=char_count,
                    max_allowed=max_chars,
                    line_number=i + 1,
                    message=f"Tip line {i + 1} has {char_count} chars (max {max_chars})"
                ))

        return violations

    def validate_presenter_notes(
        self,
        notes: str,
        slide_id: str = "unknown"
    ) -> List[ConstraintViolation]:
        """
        Validate presenter notes against word limit.

        Args:
            notes: Presenter notes text
            slide_id: Slide identifier

        Returns:
            List of violations
        """
        violations = []

        if not notes:
            return violations

        notes_limits = self.constraints.get('character_limits', {}).get('presenter_notes', {})
        max_words = notes_limits.get('max_words', self.DEFAULT_CONSTRAINTS['presenter_notes']['max_words'])

        word_count = self.count_words(notes)
        if word_count > max_words:
            violations.append(ConstraintViolation(
                field="presenter_notes",
                constraint_type="word_limit",
                actual_value=word_count,
                max_allowed=max_words,
                message=f"Presenter notes has {word_count} words (max {max_words})"
            ))

        return violations

    def validate_visual_content(
        self,
        visual_type: str,
        content: Dict,
        slide_id: str = "unknown"
    ) -> List[ConstraintViolation]:
        """
        Validate visual-specific constraints.

        Args:
            visual_type: Type of visual (table, flowchart, etc.)
            content: Visual content dictionary
            slide_id: Slide identifier

        Returns:
            List of violations
        """
        violations = []

        visual_limits = self.constraints.get('visual_limits', {}).get(visual_type, {})
        element_limits = self.constraints.get('visual_elements', {}).get(visual_type, {})

        if visual_type == 'table':
            # Check table dimensions
            columns = content.get('columns', [])
            rows = content.get('rows', [])

            col_limit = element_limits.get('columns', {})
            if col_limit:
                if len(columns) > col_limit.get('max', 6):
                    violations.append(ConstraintViolation(
                        field="table_columns",
                        constraint_type="element_count",
                        actual_value=len(columns),
                        max_allowed=col_limit.get('max', 6),
                        message=f"Table has {len(columns)} columns (max {col_limit.get('max', 6)})"
                    ))

            row_limit = element_limits.get('rows', {})
            if row_limit:
                if len(rows) > row_limit.get('max', 10):
                    violations.append(ConstraintViolation(
                        field="table_rows",
                        constraint_type="element_count",
                        actual_value=len(rows),
                        max_allowed=row_limit.get('max', 10),
                        message=f"Table has {len(rows)} rows (max {row_limit.get('max', 10)})"
                    ))

        elif visual_type == 'flowchart':
            steps = content.get('steps', [])
            max_steps = element_limits.get('max_steps', 7)
            if len(steps) > max_steps:
                violations.append(ConstraintViolation(
                    field="flowchart_steps",
                    constraint_type="element_count",
                    actual_value=len(steps),
                    max_allowed=max_steps,
                    message=f"Flowchart has {len(steps)} steps (max {max_steps})"
                ))

        elif visual_type == 'decision_tree':
            nodes = content.get('nodes', [])
            max_nodes = element_limits.get('max_nodes', 15)
            if len(nodes) > max_nodes:
                violations.append(ConstraintViolation(
                    field="decision_tree_nodes",
                    constraint_type="element_count",
                    actual_value=len(nodes),
                    max_allowed=max_nodes,
                    message=f"Decision tree has {len(nodes)} nodes (max {max_nodes})"
                ))

        return violations

    def validate_slide(
        self,
        slide: Dict,
        slide_id: Optional[str] = None
    ) -> SlideValidationResult:
        """
        Validate a complete slide against all constraints.

        Args:
            slide: Slide dictionary with title, body, tip, notes
            slide_id: Optional slide identifier

        Returns:
            SlideValidationResult
        """
        slide_id = slide_id or slide.get('number', slide.get('id', 'unknown'))
        violations = []
        warnings = []

        # Validate title/header
        title = slide.get('title') or slide.get('header', '')
        violations.extend(self.validate_title(title, slide_id))

        # Validate body
        body = slide.get('body', '')
        violations.extend(self.validate_body(body, slide_id))

        # Validate tip
        tip = slide.get('tip', '')
        violations.extend(self.validate_tip(tip, slide_id))

        # Validate presenter notes
        notes = slide.get('notes') or slide.get('presenter_notes', '')
        violations.extend(self.validate_presenter_notes(notes, slide_id))

        # Validate visual if present
        if slide.get('visual_type') and slide.get('visual_data'):
            violations.extend(self.validate_visual_content(
                slide['visual_type'],
                slide['visual_data'],
                slide_id
            ))

        # Calculate stats
        stats = {
            'title_lines': self.count_lines(title),
            'body_lines': self.count_lines(body),
            'tip_lines': self.count_lines(tip),
            'notes_words': self.count_words(notes)
        }

        return SlideValidationResult(
            slide_id=str(slide_id),
            is_valid=len(violations) == 0,
            violations=violations,
            warnings=warnings,
            stats=stats
        )

    def validate_slides(
        self,
        slides: List[Dict]
    ) -> BatchValidationResult:
        """
        Validate multiple slides.

        Args:
            slides: List of slide dictionaries

        Returns:
            BatchValidationResult
        """
        results = []
        valid_count = 0
        total_violations = 0

        for i, slide in enumerate(slides):
            slide_id = slide.get('number', slide.get('id', i + 1))
            result = self.validate_slide(slide, str(slide_id))
            results.append(result)

            if result.is_valid:
                valid_count += 1
            total_violations += len(result.violations)

        # Build summary
        summary = {
            'violations_by_field': {},
            'violations_by_type': {}
        }

        for result in results:
            for violation in result.violations:
                # Count by field
                field = violation.field
                summary['violations_by_field'][field] = \
                    summary['violations_by_field'].get(field, 0) + 1

                # Count by type
                vtype = violation.constraint_type
                summary['violations_by_type'][vtype] = \
                    summary['violations_by_type'].get(vtype, 0) + 1

        return BatchValidationResult(
            total_slides=len(slides),
            valid_slides=valid_count,
            invalid_slides=len(slides) - valid_count,
            total_violations=total_violations,
            slide_results=results,
            summary=summary
        )

    def format_report(self, result: Union[SlideValidationResult, BatchValidationResult]) -> str:
        """Format validation result as report."""
        lines = [
            "=" * 60,
            "CONSTRAINT VALIDATION REPORT",
            "=" * 60
        ]

        if isinstance(result, BatchValidationResult):
            lines.extend([
                f"Total Slides: {result.total_slides}",
                f"Valid: {result.valid_slides}",
                f"Invalid: {result.invalid_slides}",
                f"Total Violations: {result.total_violations}",
                ""
            ])

            if result.summary.get('violations_by_field'):
                lines.append("Violations by Field:")
                for field, count in result.summary['violations_by_field'].items():
                    lines.append(f"  {field}: {count}")
                lines.append("")

            # Show first few invalid slides
            invalid = [r for r in result.slide_results if not r.is_valid]
            if invalid:
                lines.append("Invalid Slides:")
                for slide_result in invalid[:5]:
                    lines.append(f"  Slide {slide_result.slide_id}:")
                    for v in slide_result.violations[:3]:
                        lines.append(f"    - {v.message}")
                if len(invalid) > 5:
                    lines.append(f"  ... and {len(invalid) - 5} more")

        else:
            lines.extend([
                f"Slide: {result.slide_id}",
                f"Status: {'PASS' if result.is_valid else 'FAIL'}",
                ""
            ])

            if result.violations:
                lines.append("Violations:")
                for v in result.violations:
                    lines.append(f"  - {v.message}")

            lines.append("")
            lines.append("Stats:")
            for key, value in result.stats.items():
                lines.append(f"  {key}: {value}")

        lines.append("=" * 60)
        return "\n".join(lines)


def validate_slide(slide: Dict) -> SlideValidationResult:
    """Convenience function to validate a single slide."""
    validator = ConstraintValidator()
    return validator.validate_slide(slide)


if __name__ == "__main__":
    print("Constraint Validator - NCLEX Pipeline Validation Skill")
    print("=" * 50)

    validator = ConstraintValidator()

    # Demo with sample slides
    sample_slides = [
        {
            'number': 1,
            'title': 'Assessment Fundamentals',
            'body': '''Line 1: Patient assessment overview
Line 2: Vital signs importance
Line 3: Documentation requirements
Line 4: Safety considerations
Line 5: Communication skills''',
            'tip': 'Focus on systematic assessment approach',
            'notes': 'Explain each step of the assessment process. Emphasize safety first.'
        },
        {
            'number': 2,
            'title': 'This is a very long title that exceeds the character limit and should trigger a violation',
            'body': '''This body text has too many lines
Line 2
Line 3
Line 4
Line 5
Line 6
Line 7
Line 8
Line 9
Line 10
Line 11
Line 12 - this exceeds the limit''',
            'tip': 'Short tip',
            'notes': 'Brief notes.'
        }
    ]

    print("\nValidating sample slides...")
    result = validator.validate_slides(sample_slides)
    report = validator.format_report(result)
    print(report)
