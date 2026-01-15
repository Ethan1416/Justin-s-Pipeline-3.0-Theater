"""
Agenda Slide Validator - HARDCODED Skill
Validates agenda slide content against theater education requirements.

This skill is HARDCODED and cannot be bypassed during pipeline execution.
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass


# =============================================================================
# HARDCODED VALIDATION RULES - DO NOT MODIFY
# =============================================================================

VALIDATION_RULES = {
    "total_duration_must_equal_class_period": True,
    "components_required": ["agenda", "warmup", "lecture", "activity", "reflection", "buffer"],
    "objectives_max": 3,
    "objectives_min": 1,
    "materials_min": 3,
    "materials_max": 5,
    "description_max_chars": 60,
    "objective_max_chars": 50,
    "time_markers_must_be_sequential": True,
    "time_markers_must_not_overlap": True,
}

# Valid class periods
VALID_CLASS_PERIODS = {
    "standard": 56,
    "block": 90,
    "shortened": 45,
    "extended": 75,
}

# Required component types
REQUIRED_COMPONENTS = [
    "agenda",
    "warmup",
    "lecture",
    "activity",
    "reflection",
    "buffer",
]

# Component sequence order
COMPONENT_ORDER = {
    "agenda": 1,
    "warmup": 2,
    "lecture": 3,
    "activity": 4,
    "reflection": 5,
    "buffer": 6,
}


# =============================================================================
# DATA CLASSES
# =============================================================================

@dataclass
class ValidationResult:
    """Result of agenda validation."""
    valid: bool
    issues: List[str]
    warnings: List[str]
    score: int  # 0-100
    details: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "valid": self.valid,
            "issues": self.issues,
            "warnings": self.warnings,
            "score": self.score,
            "details": self.details,
        }


# =============================================================================
# CORE VALIDATION FUNCTIONS
# =============================================================================

def validate_agenda_structure(agenda_data: Dict[str, Any]) -> ValidationResult:
    """
    Validate complete agenda structure.

    HARDCODED: All validation rules are enforced without exception.

    Args:
        agenda_data: Agenda dictionary (from AgendaSlide.to_dict())

    Returns:
        ValidationResult with pass/fail status and issues
    """
    issues = []
    warnings = []
    details = {}

    agenda = agenda_data.get("agenda", agenda_data)

    # 1. Validate total duration
    total_duration = agenda.get("total_duration", 0)
    if total_duration not in VALID_CLASS_PERIODS.values():
        issues.append(f"Invalid total duration: {total_duration}. Must be one of {list(VALID_CLASS_PERIODS.values())}")
    details["total_duration"] = total_duration

    # 2. Validate components
    components = agenda.get("components", [])
    component_result = _validate_components(components, total_duration)
    issues.extend(component_result["issues"])
    warnings.extend(component_result["warnings"])
    details["components"] = component_result["details"]

    # 3. Validate learning objectives
    objectives = agenda.get("learning_objectives_display", [])
    objectives_result = _validate_objectives(objectives)
    issues.extend(objectives_result["issues"])
    warnings.extend(objectives_result["warnings"])
    details["objectives"] = objectives_result["details"]

    # 4. Validate materials
    materials = agenda.get("materials_preview", [])
    materials_result = _validate_materials(materials)
    issues.extend(materials_result["issues"])
    warnings.extend(materials_result["warnings"])
    details["materials"] = materials_result["details"]

    # 5. Validate unit info
    unit_info = agenda.get("unit_info", "")
    if not unit_info:
        issues.append("Missing unit_info field")
    details["unit_info"] = unit_info

    # 6. Validate lesson title
    lesson_title = agenda.get("lesson_title", "")
    if not lesson_title:
        issues.append("Missing lesson_title field")
    details["lesson_title"] = lesson_title

    # Calculate score
    score = _calculate_validation_score(issues, warnings)

    return ValidationResult(
        valid=len(issues) == 0,
        issues=issues,
        warnings=warnings,
        score=score,
        details=details,
    )


def _validate_components(
    components: List[Dict[str, Any]],
    expected_duration: int
) -> Dict[str, Any]:
    """Validate component structure and timing."""
    issues = []
    warnings = []
    details = {
        "count": len(components),
        "types_present": [],
        "total_time": 0,
    }

    # Check component count
    if len(components) != 6:
        issues.append(f"Expected 6 components, found {len(components)}")

    # Track component types and timing
    total_time = 0
    prev_end = 0
    seen_types = set()

    for i, comp in enumerate(components):
        comp_name = comp.get("component", "").lower().replace(" & ", "_").replace(" ", "_")

        # Normalize component names
        normalized = _normalize_component_name(comp_name)
        if normalized:
            seen_types.add(normalized)
            details["types_present"].append(normalized)

        # Check duration
        duration = comp.get("duration_minutes", 0)
        total_time += duration

        # Check time marker format and sequence
        time_marker = comp.get("time_marker", "")
        if time_marker:
            try:
                parts = time_marker.replace(":00", "").split("-")
                start, end = int(parts[0]), int(parts[1])

                if start != prev_end:
                    issues.append(
                        f"Time gap at component {i+1}: expected start {prev_end}:00, got {start}:00"
                    )
                if end - start != duration:
                    warnings.append(
                        f"Time marker duration mismatch for {comp.get('component')}: "
                        f"marker shows {end-start} min, duration says {duration} min"
                    )
                prev_end = end
            except (ValueError, IndexError):
                issues.append(f"Invalid time marker format: {time_marker}")

        # Check description length
        description = comp.get("description", "")
        if len(description) > VALIDATION_RULES["description_max_chars"]:
            warnings.append(
                f"Description for {comp.get('component')} exceeds "
                f"{VALIDATION_RULES['description_max_chars']} chars"
            )

    details["total_time"] = total_time

    # Check all required components present
    missing = set(REQUIRED_COMPONENTS) - seen_types
    if missing:
        issues.append(f"Missing required components: {list(missing)}")

    # Check total time matches expected
    if total_time != expected_duration:
        issues.append(
            f"Component times sum to {total_time} min, expected {expected_duration} min"
        )

    return {"issues": issues, "warnings": warnings, "details": details}


def _validate_objectives(objectives: List[str]) -> Dict[str, Any]:
    """Validate learning objectives."""
    issues = []
    warnings = []
    details = {
        "count": len(objectives),
        "lengths": [],
    }

    # Check count
    if len(objectives) < VALIDATION_RULES["objectives_min"]:
        issues.append(f"At least {VALIDATION_RULES['objectives_min']} objective required")
    if len(objectives) > VALIDATION_RULES["objectives_max"]:
        issues.append(f"Maximum {VALIDATION_RULES['objectives_max']} objectives allowed")

    # Check each objective
    for i, obj in enumerate(objectives):
        # Remove numbering prefix for length check
        clean_obj = obj.lstrip("0123456789. ")
        details["lengths"].append(len(clean_obj))

        if len(clean_obj) > VALIDATION_RULES["objective_max_chars"]:
            warnings.append(
                f"Objective {i+1} exceeds {VALIDATION_RULES['objective_max_chars']} chars"
            )

        # Check for measurable verbs
        measurable_verbs = [
            "identify", "explain", "compare", "demonstrate", "analyze",
            "evaluate", "create", "describe", "define", "list",
            "perform", "interpret", "apply", "differentiate",
        ]
        has_verb = any(verb in clean_obj.lower() for verb in measurable_verbs)
        if not has_verb:
            warnings.append(f"Objective {i+1} may not have a measurable verb")

    return {"issues": issues, "warnings": warnings, "details": details}


def _validate_materials(materials: List[str]) -> Dict[str, Any]:
    """Validate materials list."""
    issues = []
    warnings = []
    details = {
        "count": len(materials),
        "items": materials,
    }

    # Check count
    if len(materials) < VALIDATION_RULES["materials_min"]:
        issues.append(f"At least {VALIDATION_RULES['materials_min']} materials required")
    if len(materials) > VALIDATION_RULES["materials_max"]:
        warnings.append(f"Materials list exceeds {VALIDATION_RULES['materials_max']} items")

    # Check for required materials
    required = ["powerpoint", "journal", "notebook"]
    has_required = any(
        any(req in mat.lower() for req in required)
        for mat in materials
    )
    if not has_required:
        warnings.append("Materials should include PowerPoint and journal/notebook")

    return {"issues": issues, "warnings": warnings, "details": details}


def _normalize_component_name(name: str) -> Optional[str]:
    """Normalize component name to standard type."""
    name = name.lower().strip()

    mappings = {
        "agenda": ["agenda", "agenda_objectives", "agenda_&_objectives"],
        "warmup": ["warmup", "warm-up", "warm_up"],
        "lecture": ["lecture", "direct_instruction", "instruction"],
        "activity": ["activity", "guided_practice", "practice"],
        "reflection": ["reflection", "reflection_exit", "reflection_&_exit_ticket", "journal"],
        "buffer": ["buffer", "buffer/transition", "transition", "cleanup"],
    }

    for standard, variants in mappings.items():
        if name in variants or any(v in name for v in variants):
            return standard

    return None


def _calculate_validation_score(issues: List[str], warnings: List[str]) -> int:
    """Calculate validation score 0-100."""
    # Start at 100, deduct for issues and warnings
    score = 100

    # Major deductions for issues
    score -= len(issues) * 15

    # Minor deductions for warnings
    score -= len(warnings) * 5

    return max(0, min(100, score))


# =============================================================================
# CONVENIENCE FUNCTIONS
# =============================================================================

def is_valid_agenda(agenda_data: Dict[str, Any]) -> bool:
    """Check if agenda passes all validation rules."""
    result = validate_agenda_structure(agenda_data)
    return result.valid


def get_validation_issues(agenda_data: Dict[str, Any]) -> List[str]:
    """Get list of validation issues."""
    result = validate_agenda_structure(agenda_data)
    return result.issues


def get_validation_warnings(agenda_data: Dict[str, Any]) -> List[str]:
    """Get list of validation warnings."""
    result = validate_agenda_structure(agenda_data)
    return result.warnings


def get_validation_score(agenda_data: Dict[str, Any]) -> int:
    """Get validation score 0-100."""
    result = validate_agenda_structure(agenda_data)
    return result.score


def generate_validation_report(agenda_data: Dict[str, Any]) -> str:
    """Generate human-readable validation report."""
    result = validate_agenda_structure(agenda_data)

    lines = [
        "=" * 50,
        "AGENDA SLIDE VALIDATION REPORT",
        "=" * 50,
        "",
        f"Status: {'PASS' if result.valid else 'FAIL'}",
        f"Score: {result.score}/100",
        "",
    ]

    if result.issues:
        lines.append("ISSUES (must fix):")
        for issue in result.issues:
            lines.append(f"  ✗ {issue}")
        lines.append("")

    if result.warnings:
        lines.append("WARNINGS (should review):")
        for warning in result.warnings:
            lines.append(f"  ⚠ {warning}")
        lines.append("")

    lines.append("DETAILS:")
    for key, value in result.details.items():
        lines.append(f"  {key}: {value}")

    lines.append("")
    lines.append("=" * 50)

    return "\n".join(lines)
