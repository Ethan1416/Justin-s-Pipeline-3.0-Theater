"""
Anchor Validator - Validate anchor structure and content for NCLEX pipeline.

This module validates that anchor documents meet the requirements for
the NCLEX lecture generation pipeline, including structure, content
completeness, and format standards.

Usage:
    from skills.validation.anchor_validator import AnchorValidator

    validator = AnchorValidator()
    result = validator.validate_anchors(anchors)
"""

import re
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field


@dataclass
class ValidationIssue:
    """Represents a single validation issue."""
    severity: str  # "error", "warning", "info"
    anchor_id: Optional[str]
    field: str
    message: str
    suggested_fix: Optional[str] = None


@dataclass
class AnchorValidationResult:
    """Container for anchor validation results."""
    total_anchors: int
    valid_anchors: int
    invalid_anchors: int
    is_valid: bool
    score: float  # 0-100
    issues: List[ValidationIssue] = field(default_factory=list)
    summary: Dict = field(default_factory=dict)


class AnchorValidator:
    """Validate anchor structure and content."""

    # Minimum requirements
    MIN_ANCHOR_COUNT = 20
    MIN_TITLE_LENGTH = 3
    MAX_TITLE_LENGTH = 100
    MIN_CONTENT_WORDS = 5

    # Required anchor fields
    REQUIRED_FIELDS = ['id', 'title']
    RECOMMENDED_FIELDS = ['number', 'full_text']

    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize the AnchorValidator.

        Args:
            config_path: Optional path to constraints config
        """
        self.config_path = config_path
        self._load_config()

    def _load_config(self):
        """Load configuration if available."""
        try:
            from skills.utilities.yaml_parser import YAMLParser
            parser = YAMLParser()

            if self.config_path:
                result = parser.load(self.config_path)
            else:
                result = parser.load("config/constraints.yaml")

            if result.success:
                self.config = result.data
            else:
                self.config = {}
        except ImportError:
            self.config = {}

    def validate_anchors(
        self,
        anchors: List[Dict],
        strict: bool = False
    ) -> AnchorValidationResult:
        """
        Validate a list of anchors.

        Args:
            anchors: List of anchor dictionaries
            strict: If True, treat warnings as errors

        Returns:
            AnchorValidationResult with validation details
        """
        issues = []
        valid_count = 0
        invalid_count = 0

        # Check overall anchor count
        if len(anchors) < self.MIN_ANCHOR_COUNT:
            issues.append(ValidationIssue(
                severity="warning",
                anchor_id=None,
                field="count",
                message=f"Low anchor count: {len(anchors)} (recommended >= {self.MIN_ANCHOR_COUNT})",
                suggested_fix="Add more anchor points to ensure comprehensive coverage"
            ))

        if len(anchors) == 0:
            issues.append(ValidationIssue(
                severity="error",
                anchor_id=None,
                field="count",
                message="No anchors found",
                suggested_fix="Ensure anchor document contains properly formatted anchor points"
            ))

        # Validate each anchor
        seen_ids = set()
        seen_titles = set()

        for i, anchor in enumerate(anchors):
            anchor_issues = self._validate_single_anchor(anchor, i, seen_ids, seen_titles)
            issues.extend(anchor_issues)

            # Track if anchor is valid
            has_errors = any(issue.severity == "error" for issue in anchor_issues)
            if has_errors:
                invalid_count += 1
            else:
                valid_count += 1

            # Track seen values
            if 'id' in anchor:
                seen_ids.add(anchor['id'])
            if 'title' in anchor:
                seen_titles.add(anchor['title'].lower())

        # Calculate score
        total = len(anchors) if anchors else 1
        error_count = sum(1 for i in issues if i.severity == "error")
        warning_count = sum(1 for i in issues if i.severity == "warning")

        # Score calculation: start at 100, deduct for issues
        score = 100.0
        score -= (error_count * 10)  # -10 per error
        score -= (warning_count * 2)  # -2 per warning
        score = max(0, min(100, score))

        # Determine if valid
        is_valid = error_count == 0
        if strict:
            is_valid = is_valid and warning_count == 0

        return AnchorValidationResult(
            total_anchors=len(anchors),
            valid_anchors=valid_count,
            invalid_anchors=invalid_count,
            is_valid=is_valid,
            score=score,
            issues=issues,
            summary={
                'errors': error_count,
                'warnings': warning_count,
                'info': sum(1 for i in issues if i.severity == "info")
            }
        )

    def _validate_single_anchor(
        self,
        anchor: Dict,
        index: int,
        seen_ids: set,
        seen_titles: set
    ) -> List[ValidationIssue]:
        """
        Validate a single anchor.

        Args:
            anchor: Anchor dictionary
            index: Anchor index in list
            seen_ids: Set of already-seen IDs
            seen_titles: Set of already-seen titles

        Returns:
            List of ValidationIssues for this anchor
        """
        issues = []
        anchor_id = anchor.get('id', f'anchor_{index + 1}')

        # Check required fields
        for field in self.REQUIRED_FIELDS:
            if field not in anchor or not anchor[field]:
                issues.append(ValidationIssue(
                    severity="error",
                    anchor_id=anchor_id,
                    field=field,
                    message=f"Missing required field: {field}",
                    suggested_fix=f"Add '{field}' field to anchor"
                ))

        # Check recommended fields
        for field in self.RECOMMENDED_FIELDS:
            if field not in anchor:
                issues.append(ValidationIssue(
                    severity="info",
                    anchor_id=anchor_id,
                    field=field,
                    message=f"Missing recommended field: {field}",
                    suggested_fix=f"Consider adding '{field}' for better processing"
                ))

        # Validate ID uniqueness
        if 'id' in anchor and anchor['id'] in seen_ids:
            issues.append(ValidationIssue(
                severity="error",
                anchor_id=anchor_id,
                field="id",
                message=f"Duplicate anchor ID: {anchor['id']}",
                suggested_fix="Ensure each anchor has a unique ID"
            ))

        # Validate title
        if 'title' in anchor:
            title = anchor['title']
            title_issues = self._validate_title(anchor_id, title, seen_titles)
            issues.extend(title_issues)

        # Validate content if present
        if 'full_text' in anchor:
            content_issues = self._validate_content(anchor_id, anchor['full_text'])
            issues.extend(content_issues)

        return issues

    def _validate_title(
        self,
        anchor_id: str,
        title: str,
        seen_titles: set
    ) -> List[ValidationIssue]:
        """Validate anchor title."""
        issues = []

        # Check length
        if len(title) < self.MIN_TITLE_LENGTH:
            issues.append(ValidationIssue(
                severity="error",
                anchor_id=anchor_id,
                field="title",
                message=f"Title too short: '{title}' ({len(title)} chars)",
                suggested_fix=f"Title should be at least {self.MIN_TITLE_LENGTH} characters"
            ))
        elif len(title) > self.MAX_TITLE_LENGTH:
            issues.append(ValidationIssue(
                severity="warning",
                anchor_id=anchor_id,
                field="title",
                message=f"Title too long: {len(title)} chars (max {self.MAX_TITLE_LENGTH})",
                suggested_fix="Consider shortening the title"
            ))

        # Check for duplicate titles
        if title.lower() in seen_titles:
            issues.append(ValidationIssue(
                severity="warning",
                anchor_id=anchor_id,
                field="title",
                message=f"Duplicate title found: '{title[:50]}'",
                suggested_fix="Consider making titles more specific"
            ))

        # Check for problematic characters
        if re.search(r'[<>{}|\\^~\[\]]', title):
            issues.append(ValidationIssue(
                severity="warning",
                anchor_id=anchor_id,
                field="title",
                message="Title contains special characters that may cause issues",
                suggested_fix="Remove or replace special characters"
            ))

        # Check for empty or whitespace-only
        if not title.strip():
            issues.append(ValidationIssue(
                severity="error",
                anchor_id=anchor_id,
                field="title",
                message="Title is empty or whitespace only",
                suggested_fix="Provide a meaningful title"
            ))

        return issues

    def _validate_content(
        self,
        anchor_id: str,
        content: str
    ) -> List[ValidationIssue]:
        """Validate anchor content."""
        issues = []

        if not content or not content.strip():
            issues.append(ValidationIssue(
                severity="warning",
                anchor_id=anchor_id,
                field="full_text",
                message="No content provided",
                suggested_fix="Add descriptive content for the anchor"
            ))
            return issues

        word_count = len(content.split())
        if word_count < self.MIN_CONTENT_WORDS:
            issues.append(ValidationIssue(
                severity="warning",
                anchor_id=anchor_id,
                field="full_text",
                message=f"Content is brief: {word_count} words",
                suggested_fix=f"Consider adding more detail (at least {self.MIN_CONTENT_WORDS} words)"
            ))

        return issues

    def validate_anchor_document(
        self,
        parsed_document: Any
    ) -> AnchorValidationResult:
        """
        Validate a parsed document (from file_parser).

        Args:
            parsed_document: ParsedDocument object from file_parser

        Returns:
            AnchorValidationResult
        """
        # Handle ParsedDocument dataclass
        if hasattr(parsed_document, 'anchors'):
            anchors = parsed_document.anchors
        elif isinstance(parsed_document, dict):
            anchors = parsed_document.get('anchors', [])
        else:
            anchors = []

        return self.validate_anchors(anchors)

    def format_report(self, result: AnchorValidationResult) -> str:
        """
        Format validation result as a human-readable report.

        Args:
            result: AnchorValidationResult to format

        Returns:
            Formatted report string
        """
        lines = [
            "=" * 60,
            "ANCHOR VALIDATION REPORT",
            "=" * 60,
            f"Total Anchors: {result.total_anchors}",
            f"Valid: {result.valid_anchors}",
            f"Invalid: {result.invalid_anchors}",
            f"Score: {result.score:.1f}/100",
            f"Status: {'PASS' if result.is_valid else 'FAIL'}",
            "",
            f"Summary: {result.summary['errors']} errors, "
            f"{result.summary['warnings']} warnings, "
            f"{result.summary['info']} info",
            ""
        ]

        if result.issues:
            lines.append("-" * 60)
            lines.append("ISSUES:")
            lines.append("-" * 60)

            # Group by severity
            for severity in ["error", "warning", "info"]:
                severity_issues = [i for i in result.issues if i.severity == severity]
                if severity_issues:
                    lines.append(f"\n{severity.upper()}S:")
                    for issue in severity_issues:
                        anchor_ref = f"[{issue.anchor_id}]" if issue.anchor_id else "[General]"
                        lines.append(f"  {anchor_ref} {issue.field}: {issue.message}")
                        if issue.suggested_fix:
                            lines.append(f"    Fix: {issue.suggested_fix}")

        lines.append("")
        lines.append("=" * 60)
        return "\n".join(lines)


def validate_anchors(anchors: List[Dict]) -> AnchorValidationResult:
    """
    Convenience function to validate anchors.

    Args:
        anchors: List of anchor dictionaries

    Returns:
        AnchorValidationResult
    """
    validator = AnchorValidator()
    return validator.validate_anchors(anchors)


if __name__ == "__main__":
    import sys

    print("Anchor Validator - NCLEX Pipeline Validation Skill")
    print("=" * 50)

    validator = AnchorValidator()

    # Demo with sample anchors
    sample_anchors = [
        {
            'id': 'anchor_1',
            'number': 1,
            'title': 'Assessment Fundamentals',
            'full_text': 'Understanding patient assessment is critical for nursing practice.'
        },
        {
            'id': 'anchor_2',
            'number': 2,
            'title': 'Vital Signs',
            'full_text': 'Accurate measurement and interpretation of vital signs.'
        },
        {
            'id': 'anchor_3',
            'number': 3,
            'title': '',  # Invalid - empty title
            'full_text': 'Content here'
        },
        {
            'id': 'anchor_2',  # Invalid - duplicate ID
            'number': 4,
            'title': 'Documentation',
            'full_text': 'Short'  # Warning - brief content
        },
        {
            # Missing id field
            'number': 5,
            'title': 'Patient Safety',
            'full_text': 'Safety protocols and procedures for patient care.'
        }
    ]

    print("\nValidating sample anchors...")
    print()

    result = validator.validate_anchors(sample_anchors)
    report = validator.format_report(result)
    print(report)
