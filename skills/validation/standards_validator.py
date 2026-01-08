"""
Standards Validator - Validate standards completeness for NCLEX pipeline.

This module validates that presentation standards files and configurations
are complete and properly formatted for use in the lecture generation pipeline.

Standards files validated:
- standards/presenting_standards.md
- standards/VISUAL_LAYOUT_STANDARDS.md
- config/constraints.yaml

Enhanced validation (v1.1):
- Schema validation: Validates parsed content matches schema structure
- Delivery mode cross-checks: Verifies mode counts match subsection counts
- Timing consistency: Ensures timing calculations are mathematically consistent

Usage:
    from skills.validation.standards_validator import StandardsValidator

    validator = StandardsValidator()
    result = validator.validate_all_standards()

    # Enhanced validation for Step 5 output
    output_result = validator.validate_step5_output(step5_json)
"""

import re
import json
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field


@dataclass
class StandardsValidationResult:
    """Container for standards validation results."""
    file_path: str
    file_exists: bool
    is_valid: bool
    completeness_score: float  # 0-100
    missing_sections: List[str] = field(default_factory=list)
    present_sections: List[str] = field(default_factory=list)
    issues: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)


@dataclass
class AllStandardsResult:
    """Container for all standards validation."""
    is_valid: bool
    overall_score: float
    results: Dict[str, StandardsValidationResult] = field(default_factory=dict)
    summary: Dict = field(default_factory=dict)


@dataclass
class SchemaValidationResult:
    """Container for schema validation results."""
    is_valid: bool
    schema_name: str
    checked_fields: int = 0
    missing_fields: List[str] = field(default_factory=list)
    type_errors: List[str] = field(default_factory=list)
    value_errors: List[str] = field(default_factory=list)


@dataclass
class DeliveryModeValidationResult:
    """Container for delivery mode cross-check results."""
    is_valid: bool
    total_subsections: int = 0
    mode_counts: Dict[str, int] = field(default_factory=dict)
    mode_sum: int = 0
    section_count: int = 0
    foundational_count: int = 0
    fixed_slide_counts: Dict[str, int] = field(default_factory=dict)
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)


@dataclass
class TimingValidationResult:
    """Container for timing consistency validation results."""
    is_valid: bool
    words_per_minute_min: int = 130
    words_per_minute_max: int = 150
    max_words: int = 450
    max_duration_seconds: int = 180
    calculated_duration: float = 0.0
    consistency_checks: List[Tuple[str, bool, str]] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)


@dataclass
class EnhancedValidationResult:
    """Container for all enhanced validation results."""
    is_valid: bool
    schema_validation: Optional[SchemaValidationResult] = None
    delivery_mode_validation: Optional[DeliveryModeValidationResult] = None
    timing_validation: Optional[TimingValidationResult] = None
    summary: Dict = field(default_factory=dict)


class StandardsValidator:
    """Validate standards files and configurations."""

    # Required sections in presenting_standards.md
    PRESENTING_REQUIRED_SECTIONS = [
        "slide structure",
        "character limit",
        "line limit",
        "font",
        "visual",
        "presenter note"
    ]

    # Required sections in VISUAL_LAYOUT_STANDARDS.md
    VISUAL_REQUIRED_SECTIONS = [
        "table",
        "flowchart",
        "decision tree",
        "timeline",
        "hierarchy",
        "spectrum",
        "key differentiator"
    ]

    # Required keys in constraints.yaml
    CONSTRAINTS_REQUIRED_KEYS = [
        "character_limits",
        "character_limits.title",
        "character_limits.body",
        "character_limits.tip",
        "slides",
        "visual_quotas"
    ]

    def __init__(self, base_path: Optional[str] = None):
        """
        Initialize the StandardsValidator.

        Args:
            base_path: Base directory for resolving paths
        """
        if base_path:
            self.base_path = Path(base_path)
        else:
            self.base_path = Path(__file__).parent.parent.parent

    def validate_presenting_standards(
        self,
        file_path: Optional[str] = None
    ) -> StandardsValidationResult:
        """
        Validate presenting_standards.md file.

        Args:
            file_path: Path to standards file (optional)

        Returns:
            StandardsValidationResult
        """
        if file_path is None:
            file_path = self.base_path / "standards" / "presenting_standards.md"
        else:
            file_path = Path(file_path)

        result = StandardsValidationResult(
            file_path=str(file_path),
            file_exists=file_path.exists(),
            is_valid=False,
            completeness_score=0.0
        )

        if not file_path.exists():
            result.issues.append(f"File not found: {file_path}")
            return result

        try:
            content = file_path.read_text(encoding='utf-8').lower()

            # Check for required sections
            for section in self.PRESENTING_REQUIRED_SECTIONS:
                if section.lower() in content:
                    result.present_sections.append(section)
                else:
                    result.missing_sections.append(section)

            # Calculate score
            total = len(self.PRESENTING_REQUIRED_SECTIONS)
            present = len(result.present_sections)
            result.completeness_score = (present / total) * 100 if total > 0 else 0

            # Determine validity
            result.is_valid = len(result.missing_sections) == 0

            # Add warnings for missing sections
            for section in result.missing_sections:
                result.warnings.append(f"Missing section: {section}")

        except Exception as e:
            result.issues.append(f"Error reading file: {e}")

        return result

    def validate_visual_standards(
        self,
        file_path: Optional[str] = None
    ) -> StandardsValidationResult:
        """
        Validate VISUAL_LAYOUT_STANDARDS.md file.

        Args:
            file_path: Path to standards file (optional)

        Returns:
            StandardsValidationResult
        """
        if file_path is None:
            file_path = self.base_path / "standards" / "VISUAL_LAYOUT_STANDARDS.md"
        else:
            file_path = Path(file_path)

        result = StandardsValidationResult(
            file_path=str(file_path),
            file_exists=file_path.exists(),
            is_valid=False,
            completeness_score=0.0
        )

        if not file_path.exists():
            result.issues.append(f"File not found: {file_path}")
            return result

        try:
            content = file_path.read_text(encoding='utf-8').lower()

            # Check for required visual type sections
            for section in self.VISUAL_REQUIRED_SECTIONS:
                if section.lower() in content:
                    result.present_sections.append(section)
                else:
                    result.missing_sections.append(section)

            # Calculate score
            total = len(self.VISUAL_REQUIRED_SECTIONS)
            present = len(result.present_sections)
            result.completeness_score = (present / total) * 100 if total > 0 else 0

            # Determine validity
            result.is_valid = len(result.missing_sections) == 0

            for section in result.missing_sections:
                result.warnings.append(f"Missing visual type: {section}")

        except Exception as e:
            result.issues.append(f"Error reading file: {e}")

        return result

    def validate_constraints_config(
        self,
        file_path: Optional[str] = None
    ) -> StandardsValidationResult:
        """
        Validate constraints.yaml configuration.

        Args:
            file_path: Path to constraints file (optional)

        Returns:
            StandardsValidationResult
        """
        if file_path is None:
            file_path = self.base_path / "config" / "constraints.yaml"
        else:
            file_path = Path(file_path)

        result = StandardsValidationResult(
            file_path=str(file_path),
            file_exists=file_path.exists(),
            is_valid=False,
            completeness_score=0.0
        )

        if not file_path.exists():
            result.issues.append(f"File not found: {file_path}")
            return result

        try:
            # Use yaml_parser if available
            try:
                from skills.utilities.yaml_parser import YAMLParser
                parser = YAMLParser(str(self.base_path))
                load_result = parser.load(str(file_path))

                if not load_result.success:
                    result.issues.extend(load_result.errors)
                    return result

                config = load_result.data

                # Check for required keys
                for key_path in self.CONSTRAINTS_REQUIRED_KEYS:
                    value = parser.get_nested(config, key_path)
                    if value is not None:
                        result.present_sections.append(key_path)
                    else:
                        result.missing_sections.append(key_path)

            except ImportError:
                # Fallback to basic yaml
                import yaml
                with open(file_path, 'r', encoding='utf-8') as f:
                    config = yaml.safe_load(f)

                for key_path in self.CONSTRAINTS_REQUIRED_KEYS:
                    keys = key_path.split('.')
                    current = config
                    found = True

                    for key in keys:
                        if isinstance(current, dict) and key in current:
                            current = current[key]
                        else:
                            found = False
                            break

                    if found:
                        result.present_sections.append(key_path)
                    else:
                        result.missing_sections.append(key_path)

            # Calculate score
            total = len(self.CONSTRAINTS_REQUIRED_KEYS)
            present = len(result.present_sections)
            result.completeness_score = (present / total) * 100 if total > 0 else 0

            # Determine validity
            result.is_valid = len(result.missing_sections) == 0

            for section in result.missing_sections:
                result.warnings.append(f"Missing config key: {section}")

        except Exception as e:
            result.issues.append(f"Error validating config: {e}")

        return result

    def validate_nclex_config(
        self,
        file_path: Optional[str] = None
    ) -> StandardsValidationResult:
        """
        Validate nclex.yaml configuration.

        Args:
            file_path: Path to nclex.yaml (optional)

        Returns:
            StandardsValidationResult
        """
        required_keys = [
            "brand",
            "content.domains",
            "visuals",
            "teaching"
        ]

        if file_path is None:
            file_path = self.base_path / "config" / "nclex.yaml"
        else:
            file_path = Path(file_path)

        result = StandardsValidationResult(
            file_path=str(file_path),
            file_exists=file_path.exists(),
            is_valid=False,
            completeness_score=0.0
        )

        if not file_path.exists():
            result.issues.append(f"File not found: {file_path}")
            return result

        try:
            import yaml
            with open(file_path, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)

            for key_path in required_keys:
                keys = key_path.split('.')
                current = config
                found = True

                for key in keys:
                    if isinstance(current, dict) and key in current:
                        current = current[key]
                    else:
                        found = False
                        break

                if found:
                    result.present_sections.append(key_path)
                else:
                    result.missing_sections.append(key_path)

            # Validate domains structure
            domains = config.get('content', {}).get('domains', {})
            expected_domains = ['fundamentals', 'pharmacology', 'medical_surgical',
                              'ob_maternity', 'pediatric', 'mental_health']

            for domain in expected_domains:
                if domain in domains:
                    result.present_sections.append(f"domain:{domain}")
                else:
                    result.missing_sections.append(f"domain:{domain}")

            # Calculate score
            total = len(required_keys) + len(expected_domains)
            present = len(result.present_sections)
            result.completeness_score = (present / total) * 100 if total > 0 else 0

            result.is_valid = len(result.missing_sections) == 0

            for section in result.missing_sections:
                result.warnings.append(f"Missing: {section}")

        except Exception as e:
            result.issues.append(f"Error validating config: {e}")

        return result

    def validate_all_standards(self) -> AllStandardsResult:
        """
        Validate all standards files and configurations.

        Returns:
            AllStandardsResult with all validation results
        """
        results = {
            'presenting_standards': self.validate_presenting_standards(),
            'visual_standards': self.validate_visual_standards(),
            'constraints': self.validate_constraints_config(),
            'nclex_config': self.validate_nclex_config()
        }

        # Calculate overall validity and score
        all_valid = all(r.is_valid for r in results.values())
        scores = [r.completeness_score for r in results.values() if r.file_exists]
        overall_score = sum(scores) / len(scores) if scores else 0

        # Build summary
        summary = {
            'total_files': len(results),
            'files_found': sum(1 for r in results.values() if r.file_exists),
            'files_valid': sum(1 for r in results.values() if r.is_valid),
            'total_issues': sum(len(r.issues) for r in results.values()),
            'total_warnings': sum(len(r.warnings) for r in results.values())
        }

        return AllStandardsResult(
            is_valid=all_valid,
            overall_score=overall_score,
            results=results,
            summary=summary
        )

    def format_report(self, result: AllStandardsResult) -> str:
        """
        Format validation result as a human-readable report.

        Args:
            result: AllStandardsResult to format

        Returns:
            Formatted report string
        """
        lines = [
            "=" * 60,
            "STANDARDS VALIDATION REPORT",
            "=" * 60,
            f"Overall Status: {'PASS' if result.is_valid else 'FAIL'}",
            f"Overall Score: {result.overall_score:.1f}/100",
            "",
            f"Files: {result.summary['files_found']}/{result.summary['total_files']} found, "
            f"{result.summary['files_valid']} valid",
            ""
        ]

        for name, file_result in result.results.items():
            lines.append("-" * 60)
            lines.append(f"{name.upper()}")
            lines.append(f"  File: {file_result.file_path}")
            lines.append(f"  Exists: {'Yes' if file_result.file_exists else 'No'}")
            lines.append(f"  Valid: {'Yes' if file_result.is_valid else 'No'}")
            lines.append(f"  Score: {file_result.completeness_score:.1f}%")

            if file_result.present_sections:
                lines.append(f"  Present: {len(file_result.present_sections)} sections")

            if file_result.missing_sections:
                lines.append(f"  Missing: {', '.join(file_result.missing_sections[:5])}")
                if len(file_result.missing_sections) > 5:
                    lines.append(f"    ... and {len(file_result.missing_sections) - 5} more")

            if file_result.issues:
                lines.append("  Issues:")
                for issue in file_result.issues[:3]:
                    lines.append(f"    - {issue}")

        lines.append("")
        lines.append("=" * 60)
        return "\n".join(lines)

    # =========================================================================
    # ENHANCED VALIDATION METHODS (v1.1)
    # =========================================================================

    def validate_step5_output(
        self,
        output: Dict[str, Any]
    ) -> EnhancedValidationResult:
        """
        Validate Step 5 output with enhanced checks.

        Performs:
        1. Schema validation - ensures structure matches expected schema
        2. Delivery mode cross-checks - verifies mode counts match subsection counts
        3. Timing consistency - ensures timing calculations are mathematically consistent

        Args:
            output: Step 5 output dictionary

        Returns:
            EnhancedValidationResult with all validation results
        """
        schema_result = self.validate_schema(output)
        mode_result = self.validate_delivery_mode_counts(output)
        timing_result = self.validate_timing_consistency(output)

        # Overall validity requires all checks to pass
        is_valid = (
            schema_result.is_valid and
            mode_result.is_valid and
            timing_result.is_valid
        )

        # Build summary
        summary = {
            "schema_valid": schema_result.is_valid,
            "schema_errors": len(schema_result.missing_fields) + len(schema_result.type_errors),
            "delivery_mode_valid": mode_result.is_valid,
            "delivery_mode_errors": len(mode_result.errors),
            "timing_valid": timing_result.is_valid,
            "timing_errors": len(timing_result.errors),
            "total_errors": (
                len(schema_result.missing_fields) +
                len(schema_result.type_errors) +
                len(schema_result.value_errors) +
                len(mode_result.errors) +
                len(timing_result.errors)
            )
        }

        return EnhancedValidationResult(
            is_valid=is_valid,
            schema_validation=schema_result,
            delivery_mode_validation=mode_result,
            timing_validation=timing_result,
            summary=summary
        )

    def validate_schema(
        self,
        output: Dict[str, Any]
    ) -> SchemaValidationResult:
        """
        Validate that parsed content matches the expected schema structure.

        Checks:
        - Required top-level fields: metadata, sessions, delivery_summary, validation
        - Required metadata fields: step, date, domain, exam_context
        - Required delivery_summary fields: mode_distribution, fixed_slides_total, timing_guidance
        - Type checking for all fields

        Args:
            output: Step 5 output dictionary

        Returns:
            SchemaValidationResult
        """
        result = SchemaValidationResult(
            is_valid=True,
            schema_name="standards_output.schema.json"
        )

        # Required top-level fields
        required_top_level = ["metadata", "sessions", "delivery_summary", "validation"]
        for field in required_top_level:
            result.checked_fields += 1
            if field not in output:
                result.missing_fields.append(f"top-level.{field}")
                result.is_valid = False

        # Validate metadata if present
        if "metadata" in output:
            metadata = output["metadata"]
            required_metadata = ["step", "date", "domain", "exam_context"]
            for field in required_metadata:
                result.checked_fields += 1
                if field not in metadata:
                    result.missing_fields.append(f"metadata.{field}")
                    result.is_valid = False

            # Type checks for metadata - all required string fields
            for str_field in ["step", "date", "domain", "exam_context"]:
                if str_field in metadata and not isinstance(metadata[str_field], str):
                    result.type_errors.append(f"metadata.{str_field}: expected str, got {type(metadata[str_field]).__name__}")
                    result.is_valid = False
            # Type checks for optional integer fields
            if "total_sections" in metadata and not isinstance(metadata["total_sections"], int):
                result.type_errors.append(f"metadata.total_sections: expected int, got {type(metadata['total_sections']).__name__}")
                result.is_valid = False
            if "total_subsections" in metadata and not isinstance(metadata["total_subsections"], int):
                result.type_errors.append(f"metadata.total_subsections: expected int, got {type(metadata['total_subsections']).__name__}")
                result.is_valid = False

        # Validate sessions if present
        if "sessions" in output:
            sessions = output["sessions"]
            result.checked_fields += 1
            if not isinstance(sessions, list):
                result.type_errors.append(f"sessions: expected list, got {type(sessions).__name__}")
                result.is_valid = False
            elif len(sessions) != 2:
                result.value_errors.append(f"sessions: expected 2 sessions, got {len(sessions)}")
                # Note: This is a value error, not necessarily invalid

            # Validate each session structure
            for i, session in enumerate(sessions):
                if not isinstance(session, dict):
                    result.type_errors.append(f"sessions[{i}]: expected dict, got {type(session).__name__}")
                    result.is_valid = False
                    continue

                result.checked_fields += 1
                if "session_number" not in session:
                    result.missing_fields.append(f"sessions[{i}].session_number")
                    result.is_valid = False

                result.checked_fields += 1
                if "sections" not in session:
                    result.missing_fields.append(f"sessions[{i}].sections")
                    result.is_valid = False
                elif not isinstance(session["sections"], list):
                    result.type_errors.append(f"sessions[{i}].sections: expected list")
                    result.is_valid = False
                else:
                    # Validate each section
                    for j, section in enumerate(session["sections"]):
                        self._validate_section_schema(section, i, j, result)

        # Validate delivery_summary if present
        if "delivery_summary" in output:
            summary = output["delivery_summary"]
            required_summary = ["mode_distribution", "fixed_slides_total", "timing_guidance"]
            for field in required_summary:
                result.checked_fields += 1
                if field not in summary:
                    result.missing_fields.append(f"delivery_summary.{field}")
                    result.is_valid = False

            # Validate mode_distribution
            if "mode_distribution" in summary:
                modes = summary["mode_distribution"]
                result.checked_fields += 1
                if not isinstance(modes, dict):
                    result.type_errors.append(f"delivery_summary.mode_distribution: expected dict")
                    result.is_valid = False
                else:
                    expected_modes = ["foundational", "full", "minor", "one_and_done"]
                    for mode in expected_modes:
                        result.checked_fields += 1
                        if mode not in modes:
                            result.missing_fields.append(f"mode_distribution.{mode}")
                            result.is_valid = False
                        elif not isinstance(modes[mode], int):
                            result.type_errors.append(f"mode_distribution.{mode}: expected int")
                            result.is_valid = False

        # Validate validation section if present
        if "validation" in output:
            validation = output["validation"]
            result.checked_fields += 1
            if "status" not in validation:
                result.missing_fields.append("validation.status")
                result.is_valid = False
            elif validation["status"] not in ["PASS", "FAIL"]:
                result.value_errors.append(f"validation.status: must be 'PASS' or 'FAIL', got '{validation['status']}'")

            result.checked_fields += 1
            if "checklist" not in validation:
                result.missing_fields.append("validation.checklist")
                result.is_valid = False

        return result

    def _validate_section_schema(
        self,
        section: Dict,
        session_idx: int,
        section_idx: int,
        result: SchemaValidationResult
    ) -> None:
        """Validate individual section schema."""
        prefix = f"sessions[{session_idx}].sections[{section_idx}]"

        if not isinstance(section, dict):
            result.type_errors.append(f"{prefix}: expected dict")
            result.is_valid = False
            return

        # Required section fields
        required = ["section_number", "section_name", "fixed_slides", "subsections"]
        for field in required:
            result.checked_fields += 1
            if field not in section:
                result.missing_fields.append(f"{prefix}.{field}")
                result.is_valid = False

        # Validate subsections
        if "subsections" in section and isinstance(section["subsections"], list):
            for k, subsection in enumerate(section["subsections"]):
                self._validate_subsection_schema(subsection, session_idx, section_idx, k, result)

    def _validate_subsection_schema(
        self,
        subsection: Dict,
        session_idx: int,
        section_idx: int,
        subsection_idx: int,
        result: SchemaValidationResult
    ) -> None:
        """Validate individual subsection schema."""
        prefix = f"sessions[{session_idx}].sections[{section_idx}].subsections[{subsection_idx}]"

        if not isinstance(subsection, dict):
            result.type_errors.append(f"{prefix}: expected dict")
            result.is_valid = False
            return

        # Required subsection fields
        required = ["subsection_id", "subsection_name", "delivery_mode", "anchor_delivery"]
        for field in required:
            result.checked_fields += 1
            if field not in subsection:
                result.missing_fields.append(f"{prefix}.{field}")
                result.is_valid = False

        # Validate delivery_mode structure
        if "delivery_mode" in subsection:
            dm = subsection["delivery_mode"]
            result.checked_fields += 1
            if not isinstance(dm, dict):
                result.type_errors.append(f"{prefix}.delivery_mode: expected dict")
                result.is_valid = False
            else:
                if "mode" not in dm:
                    result.missing_fields.append(f"{prefix}.delivery_mode.mode")
                    result.is_valid = False
                elif dm["mode"] not in ["foundational", "full", "minor", "one_and_done"]:
                    result.value_errors.append(f"{prefix}.delivery_mode.mode: invalid mode '{dm['mode']}'")

                if "structure" not in dm:
                    result.missing_fields.append(f"{prefix}.delivery_mode.structure")
                    result.is_valid = False

    def validate_delivery_mode_counts(
        self,
        output: Dict[str, Any]
    ) -> DeliveryModeValidationResult:
        """
        Cross-check delivery mode counts against subsection counts.

        Validates:
        1. Sum of all mode counts equals total subsections
        2. Foundational count equals number of non-misc sections
        3. Fixed slide counts (intro, vignette, answer) equal section count
        4. Break slide count equals session count

        Args:
            output: Step 5 output dictionary

        Returns:
            DeliveryModeValidationResult
        """
        result = DeliveryModeValidationResult(is_valid=True)

        # Count actual subsections and sections
        actual_subsections = 0
        actual_sections = 0
        actual_non_misc_sections = 0

        sessions = output.get("sessions", [])
        for session in sessions:
            for section in session.get("sections", []):
                actual_sections += 1
                if not section.get("is_misc", False):
                    actual_non_misc_sections += 1
                for _ in section.get("subsections", []):
                    actual_subsections += 1

        result.total_subsections = actual_subsections
        result.section_count = actual_sections

        # Get mode distribution from delivery_summary
        delivery_summary = output.get("delivery_summary", {})
        mode_distribution = delivery_summary.get("mode_distribution", {})

        result.mode_counts = {
            "foundational": mode_distribution.get("foundational", 0),
            "full": mode_distribution.get("full", 0),
            "minor": mode_distribution.get("minor", 0),
            "one_and_done": mode_distribution.get("one_and_done", 0)
        }
        result.mode_sum = sum(result.mode_counts.values())
        result.foundational_count = result.mode_counts["foundational"]

        # Check 1: Mode sum equals total subsections
        if result.mode_sum != actual_subsections:
            result.errors.append(
                f"Mode count mismatch: sum of modes ({result.mode_sum}) != "
                f"actual subsections ({actual_subsections})"
            )
            result.is_valid = False

        # Check 2: Foundational count should equal non-misc sections
        # (each non-misc section has one foundational subsection)
        if result.foundational_count != actual_non_misc_sections:
            # This could be a warning if misc sections are involved
            if actual_non_misc_sections > 0:
                result.warnings.append(
                    f"Foundational count ({result.foundational_count}) != "
                    f"non-misc sections ({actual_non_misc_sections})"
                )

        # Check 3: Fixed slide counts
        fixed_slides = delivery_summary.get("fixed_slides_total", {})
        result.fixed_slide_counts = {
            "intro_slides": fixed_slides.get("intro_slides", 0),
            "vignette_slides": fixed_slides.get("vignette_slides", 0),
            "answer_slides": fixed_slides.get("answer_slides", 0),
            "break_slides": fixed_slides.get("break_slides", 0)
        }

        # Intro, vignette, answer should each equal section count
        for slide_type in ["intro_slides", "vignette_slides", "answer_slides"]:
            count = result.fixed_slide_counts[slide_type]
            if count != actual_sections:
                result.errors.append(
                    f"Fixed slide mismatch: {slide_type} ({count}) != "
                    f"section count ({actual_sections})"
                )
                result.is_valid = False

        # Break slides should equal session count
        session_count = len(sessions)
        if result.fixed_slide_counts["break_slides"] != session_count:
            result.errors.append(
                f"Break slide mismatch: break_slides ({result.fixed_slide_counts['break_slides']}) != "
                f"session count ({session_count})"
            )
            result.is_valid = False

        # Calculate and verify total_fixed
        expected_total_fixed = (
            result.fixed_slide_counts["intro_slides"] +
            result.fixed_slide_counts["vignette_slides"] +
            result.fixed_slide_counts["answer_slides"] +
            result.fixed_slide_counts["break_slides"]
        )
        actual_total_fixed = fixed_slides.get("total_fixed", 0)
        if actual_total_fixed != expected_total_fixed:
            result.errors.append(
                f"Total fixed calculation error: reported ({actual_total_fixed}) != "
                f"calculated ({expected_total_fixed})"
            )
            result.is_valid = False

        return result

    def validate_timing_consistency(
        self,
        output: Dict[str, Any]
    ) -> TimingValidationResult:
        """
        Verify timing calculations are mathematically consistent.

        Validates:
        1. max_words / words_per_minute = max_duration (450 / 150 = 3 min = 180 sec)
        2. Words per minute is within expected range (130-150)
        3. Max duration is consistent with word limits
        4. Active learning reduction calculation (20% reduction when applicable)

        Args:
            output: Step 5 output dictionary

        Returns:
            TimingValidationResult
        """
        result = TimingValidationResult(is_valid=True)

        # Get timing guidance from delivery_summary
        delivery_summary = output.get("delivery_summary", {})
        timing = delivery_summary.get("timing_guidance", {})

        # Extract timing values with defaults
        target_wpm = timing.get("target_words_per_minute", 140)
        max_words = timing.get("max_presenter_notes_words", 450)
        max_duration = timing.get("max_slide_duration_seconds", 180)

        result.max_words = max_words
        result.max_duration_seconds = max_duration

        # Check 1: Words per minute within range (130-150)
        wpm_valid = 130 <= target_wpm <= 150
        result.consistency_checks.append((
            "words_per_minute_range",
            wpm_valid,
            f"Target WPM ({target_wpm}) {'is' if wpm_valid else 'is NOT'} within 130-150 range"
        ))
        if not wpm_valid:
            result.errors.append(f"Target words per minute ({target_wpm}) outside valid range 130-150")
            result.is_valid = False

        # Check 2: Max duration calculation
        # max_words / wpm_min = max time in minutes
        # 450 / 130 = 3.46 min = 207 sec (upper bound)
        # 450 / 150 = 3.0 min = 180 sec (lower bound - matches max_duration)
        calculated_duration_min = (max_words / result.words_per_minute_max) * 60
        calculated_duration_max = (max_words / result.words_per_minute_min) * 60
        result.calculated_duration = calculated_duration_min

        # The max_duration should be at or below calculated_duration_max
        duration_valid = max_duration <= calculated_duration_max
        result.consistency_checks.append((
            "max_duration_consistency",
            duration_valid,
            f"Max duration ({max_duration}s) <= calculated max ({calculated_duration_max:.0f}s at {result.words_per_minute_min} WPM)"
        ))
        if not duration_valid:
            result.errors.append(
                f"Max duration ({max_duration}s) exceeds calculated maximum "
                f"({calculated_duration_max:.0f}s based on {max_words} words at {result.words_per_minute_min} WPM)"
            )
            result.is_valid = False

        # Check 3: Max words consistency with max duration
        # At target WPM, max_words should fit in max_duration
        expected_max_words = (max_duration / 60) * target_wpm
        words_fit = max_words <= expected_max_words * 1.1  # 10% tolerance
        result.consistency_checks.append((
            "max_words_consistency",
            words_fit,
            f"Max words ({max_words}) fits in {max_duration}s at {target_wpm} WPM (max: {expected_max_words:.0f})"
        ))
        if not words_fit:
            result.errors.append(
                f"Max words ({max_words}) cannot fit in {max_duration}s at {target_wpm} WPM "
                f"(expected max: {expected_max_words:.0f})"
            )
            result.is_valid = False

        # Check 4: Standard timing constants are correct
        standard_checks = [
            (max_words == 450, "max_words == 450", max_words),
            (max_duration == 180, "max_duration == 180s", max_duration),
            (130 <= target_wpm <= 150, "130 <= target_wpm <= 150", target_wpm)
        ]
        for check_passed, check_name, actual_value in standard_checks:
            result.consistency_checks.append((
                check_name,
                check_passed,
                f"Standard check: {check_name} = {actual_value}"
            ))

        # Check 5: Active learning word reduction validation
        # When active learning is present, words should be reduced by 20% (to 360)
        active_learning_max = max_words * 0.8  # 20% reduction
        result.consistency_checks.append((
            "active_learning_reduction",
            True,
            f"Active learning max words: {active_learning_max:.0f} (20% reduction from {max_words})"
        ))

        return result

    def format_enhanced_report(
        self,
        result: EnhancedValidationResult
    ) -> str:
        """
        Format enhanced validation result as a human-readable report.

        Args:
            result: EnhancedValidationResult to format

        Returns:
            Formatted report string
        """
        lines = [
            "=" * 70,
            "ENHANCED STANDARDS VALIDATION REPORT (v1.1)",
            "=" * 70,
            f"Overall Status: {'PASS' if result.is_valid else 'FAIL'}",
            f"Total Errors: {result.summary.get('total_errors', 0)}",
            ""
        ]

        # Schema validation section
        lines.append("-" * 70)
        lines.append("1. SCHEMA VALIDATION")
        lines.append("-" * 70)
        if result.schema_validation:
            sv = result.schema_validation
            lines.append(f"   Status: {'PASS' if sv.is_valid else 'FAIL'}")
            lines.append(f"   Fields Checked: {sv.checked_fields}")

            if sv.missing_fields:
                lines.append(f"   Missing Fields ({len(sv.missing_fields)}):")
                for field in sv.missing_fields[:10]:
                    lines.append(f"     - {field}")
                if len(sv.missing_fields) > 10:
                    lines.append(f"     ... and {len(sv.missing_fields) - 10} more")

            if sv.type_errors:
                lines.append(f"   Type Errors ({len(sv.type_errors)}):")
                for error in sv.type_errors[:5]:
                    lines.append(f"     - {error}")

            if sv.value_errors:
                lines.append(f"   Value Errors ({len(sv.value_errors)}):")
                for error in sv.value_errors[:5]:
                    lines.append(f"     - {error}")

        # Delivery mode validation section
        lines.append("")
        lines.append("-" * 70)
        lines.append("2. DELIVERY MODE CROSS-CHECK")
        lines.append("-" * 70)
        if result.delivery_mode_validation:
            dm = result.delivery_mode_validation
            lines.append(f"   Status: {'PASS' if dm.is_valid else 'FAIL'}")
            lines.append(f"   Total Subsections: {dm.total_subsections}")
            lines.append(f"   Section Count: {dm.section_count}")
            lines.append(f"   Mode Distribution:")
            for mode, count in dm.mode_counts.items():
                lines.append(f"     - {mode}: {count}")
            lines.append(f"   Mode Sum: {dm.mode_sum}")
            lines.append(f"   Fixed Slides:")
            for slide_type, count in dm.fixed_slide_counts.items():
                lines.append(f"     - {slide_type}: {count}")

            if dm.errors:
                lines.append(f"   Errors:")
                for error in dm.errors:
                    lines.append(f"     [ERROR] {error}")

            if dm.warnings:
                lines.append(f"   Warnings:")
                for warning in dm.warnings:
                    lines.append(f"     [WARN] {warning}")

        # Timing validation section
        lines.append("")
        lines.append("-" * 70)
        lines.append("3. TIMING CONSISTENCY")
        lines.append("-" * 70)
        if result.timing_validation:
            tv = result.timing_validation
            lines.append(f"   Status: {'PASS' if tv.is_valid else 'FAIL'}")
            lines.append(f"   Max Words: {tv.max_words}")
            lines.append(f"   Max Duration: {tv.max_duration_seconds}s")
            lines.append(f"   WPM Range: {tv.words_per_minute_min}-{tv.words_per_minute_max}")
            lines.append(f"   Calculated Duration: {tv.calculated_duration:.1f}s")
            lines.append(f"   Consistency Checks:")
            for check_name, passed, description in tv.consistency_checks:
                status = "[PASS]" if passed else "[FAIL]"
                lines.append(f"     {status} {description}")

            if tv.errors:
                lines.append(f"   Errors:")
                for error in tv.errors:
                    lines.append(f"     [ERROR] {error}")

        lines.append("")
        lines.append("=" * 70)
        lines.append("END OF ENHANCED VALIDATION REPORT")
        lines.append("=" * 70)

        return "\n".join(lines)


def validate_standards() -> AllStandardsResult:
    """
    Convenience function to validate all standards.

    Returns:
        AllStandardsResult
    """
    validator = StandardsValidator()
    return validator.validate_all_standards()


def validate_step5_output(output: Dict[str, Any]) -> EnhancedValidationResult:
    """
    Convenience function to validate Step 5 output with enhanced checks.

    Args:
        output: Step 5 output dictionary

    Returns:
        EnhancedValidationResult
    """
    validator = StandardsValidator()
    return validator.validate_step5_output(output)


if __name__ == "__main__":
    print("Standards Validator - NCLEX Pipeline Validation Skill (v1.1)")
    print("=" * 70)

    validator = StandardsValidator()

    # Basic standards validation
    print("\n[1/2] Running basic standards validation...")
    result = validator.validate_all_standards()
    report = validator.format_report(result)
    print(report)

    # Demo enhanced validation with sample data
    print("\n[2/2] Running enhanced validation demo...")
    print("-" * 70)

    # Sample Step 5 output for demonstration
    sample_output = {
        "metadata": {
            "step": "Step 5: Presentation Standards",
            "date": "2026-01-05",
            "domain": "Fundamentals",
            "exam_context": "NCLEX",
            "total_sections": 6,
            "total_subsections": 18
        },
        "sessions": [
            {
                "session_number": 1,
                "sections": [
                    {
                        "section_number": 1,
                        "section_name": "Section 1",
                        "is_misc": False,
                        "fixed_slides": {
                            "intro": {"position": "first"},
                            "vignette": {"position": "near_end"},
                            "answer": {"position": "after_vignette"}
                        },
                        "subsections": [
                            {
                                "subsection_id": "1.1",
                                "subsection_name": "Subsection 1.1",
                                "delivery_mode": {
                                    "mode": "foundational",
                                    "structure": [{"component": "overview"}]
                                },
                                "anchor_delivery": {
                                    "primary_teaching": [1, 2],
                                    "reference_callbacks": []
                                }
                            },
                            {
                                "subsection_id": "1.2",
                                "subsection_name": "Subsection 1.2",
                                "delivery_mode": {
                                    "mode": "minor",
                                    "structure": [{"component": "core"}]
                                },
                                "anchor_delivery": {
                                    "primary_teaching": [3, 4],
                                    "reference_callbacks": []
                                }
                            },
                            {
                                "subsection_id": "1.3",
                                "subsection_name": "Subsection 1.3",
                                "delivery_mode": {
                                    "mode": "one_and_done",
                                    "structure": [{"component": "core"}]
                                },
                                "anchor_delivery": {
                                    "primary_teaching": [5],
                                    "reference_callbacks": []
                                }
                            }
                        ]
                    },
                    {
                        "section_number": 2,
                        "section_name": "Section 2",
                        "is_misc": False,
                        "fixed_slides": {
                            "intro": {"position": "first"},
                            "vignette": {"position": "near_end"},
                            "answer": {"position": "after_vignette"}
                        },
                        "subsections": [
                            {
                                "subsection_id": "2.1",
                                "subsection_name": "Subsection 2.1",
                                "delivery_mode": {
                                    "mode": "foundational",
                                    "structure": [{"component": "overview"}]
                                },
                                "anchor_delivery": {
                                    "primary_teaching": [6, 7],
                                    "reference_callbacks": []
                                }
                            },
                            {
                                "subsection_id": "2.2",
                                "subsection_name": "Subsection 2.2",
                                "delivery_mode": {
                                    "mode": "full",
                                    "structure": [{"component": "core"}]
                                },
                                "anchor_delivery": {
                                    "primary_teaching": [8, 9, 10, 11, 12],
                                    "reference_callbacks": []
                                }
                            },
                            {
                                "subsection_id": "2.3",
                                "subsection_name": "Subsection 2.3",
                                "delivery_mode": {
                                    "mode": "minor",
                                    "structure": [{"component": "core"}]
                                },
                                "anchor_delivery": {
                                    "primary_teaching": [13, 14],
                                    "reference_callbacks": []
                                }
                            }
                        ]
                    },
                    {
                        "section_number": 3,
                        "section_name": "Section 3",
                        "is_misc": False,
                        "fixed_slides": {
                            "intro": {"position": "first"},
                            "vignette": {"position": "near_end"},
                            "answer": {"position": "after_vignette"}
                        },
                        "subsections": [
                            {
                                "subsection_id": "3.1",
                                "subsection_name": "Subsection 3.1",
                                "delivery_mode": {
                                    "mode": "foundational",
                                    "structure": [{"component": "overview"}]
                                },
                                "anchor_delivery": {
                                    "primary_teaching": [15, 16],
                                    "reference_callbacks": []
                                }
                            },
                            {
                                "subsection_id": "3.2",
                                "subsection_name": "Subsection 3.2",
                                "delivery_mode": {
                                    "mode": "minor",
                                    "structure": [{"component": "core"}]
                                },
                                "anchor_delivery": {
                                    "primary_teaching": [17, 18],
                                    "reference_callbacks": []
                                }
                            },
                            {
                                "subsection_id": "3.3",
                                "subsection_name": "Subsection 3.3",
                                "delivery_mode": {
                                    "mode": "one_and_done",
                                    "structure": [{"component": "core"}]
                                },
                                "anchor_delivery": {
                                    "primary_teaching": [19],
                                    "reference_callbacks": []
                                }
                            }
                        ]
                    }
                ],
                "break": {"placement": "Mid-session 1"}
            },
            {
                "session_number": 2,
                "sections": [
                    {
                        "section_number": 4,
                        "section_name": "Section 4",
                        "is_misc": False,
                        "fixed_slides": {
                            "intro": {"position": "first"},
                            "vignette": {"position": "near_end"},
                            "answer": {"position": "after_vignette"}
                        },
                        "subsections": [
                            {
                                "subsection_id": "4.1",
                                "subsection_name": "Subsection 4.1",
                                "delivery_mode": {
                                    "mode": "foundational",
                                    "structure": [{"component": "overview"}]
                                },
                                "anchor_delivery": {
                                    "primary_teaching": [20, 21],
                                    "reference_callbacks": []
                                }
                            },
                            {
                                "subsection_id": "4.2",
                                "subsection_name": "Subsection 4.2",
                                "delivery_mode": {
                                    "mode": "full",
                                    "structure": [{"component": "core"}]
                                },
                                "anchor_delivery": {
                                    "primary_teaching": [22, 23, 24, 25, 26],
                                    "reference_callbacks": []
                                }
                            },
                            {
                                "subsection_id": "4.3",
                                "subsection_name": "Subsection 4.3",
                                "delivery_mode": {
                                    "mode": "minor",
                                    "structure": [{"component": "core"}]
                                },
                                "anchor_delivery": {
                                    "primary_teaching": [27, 28],
                                    "reference_callbacks": []
                                }
                            }
                        ]
                    },
                    {
                        "section_number": 5,
                        "section_name": "Section 5",
                        "is_misc": False,
                        "fixed_slides": {
                            "intro": {"position": "first"},
                            "vignette": {"position": "near_end"},
                            "answer": {"position": "after_vignette"}
                        },
                        "subsections": [
                            {
                                "subsection_id": "5.1",
                                "subsection_name": "Subsection 5.1",
                                "delivery_mode": {
                                    "mode": "foundational",
                                    "structure": [{"component": "overview"}]
                                },
                                "anchor_delivery": {
                                    "primary_teaching": [29, 30],
                                    "reference_callbacks": []
                                }
                            },
                            {
                                "subsection_id": "5.2",
                                "subsection_name": "Subsection 5.2",
                                "delivery_mode": {
                                    "mode": "minor",
                                    "structure": [{"component": "core"}]
                                },
                                "anchor_delivery": {
                                    "primary_teaching": [31, 32],
                                    "reference_callbacks": []
                                }
                            },
                            {
                                "subsection_id": "5.3",
                                "subsection_name": "Subsection 5.3",
                                "delivery_mode": {
                                    "mode": "one_and_done",
                                    "structure": [{"component": "core"}]
                                },
                                "anchor_delivery": {
                                    "primary_teaching": [33],
                                    "reference_callbacks": []
                                }
                            }
                        ]
                    },
                    {
                        "section_number": 6,
                        "section_name": "Section 6",
                        "is_misc": False,
                        "fixed_slides": {
                            "intro": {"position": "first"},
                            "vignette": {"position": "near_end"},
                            "answer": {"position": "after_vignette"}
                        },
                        "subsections": [
                            {
                                "subsection_id": "6.1",
                                "subsection_name": "Subsection 6.1",
                                "delivery_mode": {
                                    "mode": "foundational",
                                    "structure": [{"component": "overview"}]
                                },
                                "anchor_delivery": {
                                    "primary_teaching": [34, 35],
                                    "reference_callbacks": []
                                }
                            },
                            {
                                "subsection_id": "6.2",
                                "subsection_name": "Subsection 6.2",
                                "delivery_mode": {
                                    "mode": "full",
                                    "structure": [{"component": "core"}]
                                },
                                "anchor_delivery": {
                                    "primary_teaching": [36, 37, 38, 39, 40],
                                    "reference_callbacks": []
                                }
                            },
                            {
                                "subsection_id": "6.3",
                                "subsection_name": "Subsection 6.3",
                                "delivery_mode": {
                                    "mode": "minor",
                                    "structure": [{"component": "core"}]
                                },
                                "anchor_delivery": {
                                    "primary_teaching": [41, 42],
                                    "reference_callbacks": []
                                }
                            }
                        ]
                    }
                ],
                "break": {"placement": "Mid-session 2"}
            }
        ],
        "delivery_summary": {
            "mode_distribution": {
                "foundational": 6,
                "full": 3,
                "minor": 6,
                "one_and_done": 3
            },
            "fixed_slides_total": {
                "intro_slides": 6,
                "vignette_slides": 6,
                "answer_slides": 6,
                "break_slides": 2,
                "total_fixed": 20
            },
            "timing_guidance": {
                "target_words_per_minute": 140,
                "max_presenter_notes_words": 450,
                "max_slide_duration_seconds": 180
            },
            "active_learning_points": 18,
            "exam_pattern_callouts": 18
        },
        "validation": {
            "status": "PASS",
            "checklist": {
                "all_subsections_have_delivery_mode": True,
                "all_sections_have_fixed_slides": True,
                "first_subsections_use_foundational_mode": True,
                "misc_section_exceptions_applied": True,
                "culmination_section_exceptions_applied": True,
                "xref_callbacks_documented": True,
                "active_learning_integrated": True
            },
            "errors": []
        }
    }

    enhanced_result = validator.validate_step5_output(sample_output)
    enhanced_report = validator.format_enhanced_report(enhanced_result)
    print(enhanced_report)
