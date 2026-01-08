"""
Marker Inserter Skill
Manages visual markers for Step 10 Visual Integration in the NCLEX pipeline.

This skill handles adding, validating, counting, and fixing visual markers
on slides within blueprints.

Usage:
    from skills.utilities.marker_inserter import (
        add_visual_marker, validate_all_markers, count_markers,
        fix_missing_markers, validate_marker_format
    )

    # Add marker to a slide
    slide = add_visual_marker(slide, has_visual=True, visual_type="TABLE")

    # Validate all markers in blueprint
    validation = validate_all_markers(blueprint)

    # Count markers
    counts = count_markers(blueprint)

    # Fix missing markers
    fixed_blueprint = fix_missing_markers(blueprint)

    # Validate marker format
    is_valid, error = validate_marker_format("Visual: Yes - TABLE")
"""

import re
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass


# Valid visual types as defined in constraints.yaml and visual_integrator.md
VALID_VISUAL_TYPES = [
    "TABLE",
    "FLOWCHART",
    "DECISION_TREE",
    "TIMELINE",
    "HIERARCHY",
    "SPECTRUM",
    "KEY_DIFFERENTIATORS"
]

# Marker patterns for validation
VISUAL_YES_PATTERN = r"^Visual:\s*Yes\s*-\s*([A-Z_]+)$"
VISUAL_NO_PATTERN = r"^Visual:\s*No$"


@dataclass
class MarkerValidationResult:
    """Result of marker format validation."""
    is_valid: bool
    error_message: str
    marker_type: Optional[str] = None  # "yes" or "no" if valid
    visual_type: Optional[str] = None  # Only set for "Visual: Yes - TYPE"


def add_visual_marker(
    slide: Dict[str, Any],
    has_visual: bool,
    visual_type: Optional[str] = None
) -> Dict[str, Any]:
    """
    Add visual marker to a slide.

    If has_visual is True, adds "Visual: Yes - {visual_type}" marker.
    If has_visual is False, adds "Visual: No" marker.

    Args:
        slide: Slide dictionary to modify
        has_visual: Whether the slide has a visual
        visual_type: Type of visual (required if has_visual is True)
                    Must be one of: TABLE, FLOWCHART, DECISION_TREE,
                    TIMELINE, HIERARCHY, SPECTRUM, KEY_DIFFERENTIATORS

    Returns:
        Modified slide dictionary with visual_marker field

    Raises:
        ValueError: If has_visual is True but visual_type is not provided
                   or visual_type is not a valid type
    """
    # Create a copy to avoid modifying original
    result = slide.copy()

    if has_visual:
        if visual_type is None:
            raise ValueError(
                "visual_type is required when has_visual is True"
            )

        # Normalize visual type to uppercase
        visual_type_upper = visual_type.upper()

        if visual_type_upper not in VALID_VISUAL_TYPES:
            raise ValueError(
                f"Invalid visual_type '{visual_type}'. "
                f"Must be one of: {', '.join(VALID_VISUAL_TYPES)}"
            )

        result['visual_marker'] = f"Visual: Yes - {visual_type_upper}"
    else:
        result['visual_marker'] = "Visual: No"

    return result


def validate_marker_format(marker: str) -> Tuple[bool, str]:
    """
    Validate marker format.

    Valid formats:
    - "Visual: Yes - TABLE"
    - "Visual: Yes - FLOWCHART"
    - "Visual: Yes - DECISION_TREE"
    - "Visual: Yes - TIMELINE"
    - "Visual: Yes - HIERARCHY"
    - "Visual: Yes - SPECTRUM"
    - "Visual: Yes - KEY_DIFFERENTIATORS"
    - "Visual: No"

    Args:
        marker: The marker string to validate

    Returns:
        Tuple of (is_valid, error_message)
        If valid, error_message is empty string
    """
    if not marker:
        return (False, "Marker is empty or None")

    marker = marker.strip()

    # Check for "Visual: No" format
    if re.match(VISUAL_NO_PATTERN, marker):
        return (True, "")

    # Check for "Visual: Yes - TYPE" format
    yes_match = re.match(VISUAL_YES_PATTERN, marker)
    if yes_match:
        visual_type = yes_match.group(1)
        if visual_type in VALID_VISUAL_TYPES:
            return (True, "")
        else:
            return (
                False,
                f"Invalid visual type '{visual_type}'. "
                f"Valid types: {', '.join(VALID_VISUAL_TYPES)}"
            )

    # If neither pattern matches
    return (
        False,
        f"Invalid marker format '{marker}'. "
        f"Expected 'Visual: Yes - TYPE' or 'Visual: No'"
    )


def _get_marker_details(marker: str) -> MarkerValidationResult:
    """
    Parse and validate a marker, returning detailed information.

    Args:
        marker: The marker string to parse

    Returns:
        MarkerValidationResult with validation details
    """
    is_valid, error = validate_marker_format(marker)

    if not is_valid:
        return MarkerValidationResult(
            is_valid=False,
            error_message=error
        )

    marker = marker.strip()

    if re.match(VISUAL_NO_PATTERN, marker):
        return MarkerValidationResult(
            is_valid=True,
            error_message="",
            marker_type="no"
        )

    yes_match = re.match(VISUAL_YES_PATTERN, marker)
    if yes_match:
        return MarkerValidationResult(
            is_valid=True,
            error_message="",
            marker_type="yes",
            visual_type=yes_match.group(1)
        )

    # Should not reach here if validate_marker_format works correctly
    return MarkerValidationResult(
        is_valid=False,
        error_message="Unexpected parsing error"
    )


def _extract_slides(blueprint: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Extract slides list from blueprint structure.

    Handles various blueprint formats:
    - Direct 'slides' key
    - 'step7_blueprint' > 'slides' structure
    - 'integrated_blueprint' > 'slides' structure

    Args:
        blueprint: Blueprint dictionary

    Returns:
        List of slide dictionaries
    """
    # Direct slides key
    if 'slides' in blueprint:
        return blueprint['slides']

    # Step 7 blueprint structure
    if 'step7_blueprint' in blueprint and 'slides' in blueprint['step7_blueprint']:
        return blueprint['step7_blueprint']['slides']

    # Integrated blueprint structure
    if 'integrated_blueprint' in blueprint and 'slides' in blueprint['integrated_blueprint']:
        return blueprint['integrated_blueprint']['slides']

    # Empty case
    return []


def validate_all_markers(blueprint: Dict[str, Any]) -> Dict[str, Any]:
    """
    Check that every slide has exactly one Visual: Yes or Visual: No marker.

    Args:
        blueprint: Blueprint dictionary containing slides

    Returns:
        Validation result dictionary:
        {
            'valid': bool,                    # True if all slides have valid markers
            'total_slides': int,              # Total number of slides
            'slides_with_marker': int,        # Slides with valid markers
            'slides_missing_marker': List[int], # Slide numbers missing markers
            'invalid_markers': List[Dict]     # Details about invalid markers
        }
    """
    slides = _extract_slides(blueprint)

    total_slides = len(slides)
    slides_with_marker = 0
    slides_missing_marker: List[int] = []
    invalid_markers: List[Dict[str, Any]] = []

    for i, slide in enumerate(slides):
        slide_number = slide.get('slide_number', i + 1)
        marker = slide.get('visual_marker')

        if marker is None:
            slides_missing_marker.append(slide_number)
            continue

        is_valid, error = validate_marker_format(marker)

        if is_valid:
            slides_with_marker += 1
        else:
            invalid_markers.append({
                'slide_number': slide_number,
                'marker': marker,
                'error': error
            })

    valid = (
        len(slides_missing_marker) == 0 and
        len(invalid_markers) == 0 and
        slides_with_marker == total_slides
    )

    return {
        'valid': valid,
        'total_slides': total_slides,
        'slides_with_marker': slides_with_marker,
        'slides_missing_marker': slides_missing_marker,
        'invalid_markers': invalid_markers
    }


def count_markers(blueprint: Dict[str, Any]) -> Dict[str, int]:
    """
    Count visual markers in blueprint.

    Args:
        blueprint: Blueprint dictionary containing slides

    Returns:
        Dictionary with counts:
        {
            'yes': int,      # Count of "Visual: Yes - TYPE" markers
            'no': int,       # Count of "Visual: No" markers
            'missing': int,  # Slides without markers
            'invalid': int,  # Slides with invalid markers
            'total': int     # Total number of slides
        }
    """
    slides = _extract_slides(blueprint)

    yes_count = 0
    no_count = 0
    missing_count = 0
    invalid_count = 0

    for slide in slides:
        marker = slide.get('visual_marker')

        if marker is None:
            missing_count += 1
            continue

        details = _get_marker_details(marker)

        if not details.is_valid:
            invalid_count += 1
        elif details.marker_type == "yes":
            yes_count += 1
        elif details.marker_type == "no":
            no_count += 1

    return {
        'yes': yes_count,
        'no': no_count,
        'missing': missing_count,
        'invalid': invalid_count,
        'total': len(slides)
    }


def fix_missing_markers(
    blueprint: Dict[str, Any],
    default_marker: str = "Visual: No"
) -> Dict[str, Any]:
    """
    Add default marker to slides missing visual marker.

    Args:
        blueprint: Blueprint dictionary containing slides
        default_marker: Default marker to add (default: "Visual: No")

    Returns:
        Fixed blueprint with all slides having markers

    Raises:
        ValueError: If default_marker is not a valid marker format
    """
    # Validate the default marker
    is_valid, error = validate_marker_format(default_marker)
    if not is_valid:
        raise ValueError(f"Invalid default_marker: {error}")

    # Create a deep copy of the blueprint
    import copy
    result = copy.deepcopy(blueprint)

    # Find the slides list in the result
    slides = None
    slides_key = None

    if 'slides' in result:
        slides = result['slides']
        slides_key = 'slides'
    elif 'step7_blueprint' in result and 'slides' in result['step7_blueprint']:
        slides = result['step7_blueprint']['slides']
        slides_key = ('step7_blueprint', 'slides')
    elif 'integrated_blueprint' in result and 'slides' in result['integrated_blueprint']:
        slides = result['integrated_blueprint']['slides']
        slides_key = ('integrated_blueprint', 'slides')

    if slides is None:
        return result

    # Add missing markers
    for slide in slides:
        marker = slide.get('visual_marker')

        if marker is None:
            slide['visual_marker'] = default_marker

    return result


def get_visual_type_counts(blueprint: Dict[str, Any]) -> Dict[str, int]:
    """
    Count occurrences of each visual type in the blueprint.

    Args:
        blueprint: Blueprint dictionary containing slides

    Returns:
        Dictionary mapping visual type to count
        e.g., {'TABLE': 2, 'FLOWCHART': 1, 'DECISION_TREE': 0, ...}
    """
    slides = _extract_slides(blueprint)

    # Initialize counts for all valid types
    counts = {vt: 0 for vt in VALID_VISUAL_TYPES}

    for slide in slides:
        marker = slide.get('visual_marker')

        if marker is None:
            continue

        details = _get_marker_details(marker)

        if details.is_valid and details.marker_type == "yes":
            if details.visual_type and details.visual_type in counts:
                counts[details.visual_type] += 1

    return counts


def get_slides_by_marker_type(
    blueprint: Dict[str, Any]
) -> Dict[str, List[int]]:
    """
    Group slide numbers by their marker type.

    Args:
        blueprint: Blueprint dictionary containing slides

    Returns:
        Dictionary with lists of slide numbers:
        {
            'visual_yes': [slide_numbers],   # Slides with Visual: Yes
            'visual_no': [slide_numbers],    # Slides with Visual: No
            'missing': [slide_numbers],      # Slides without markers
            'invalid': [slide_numbers]       # Slides with invalid markers
        }
    """
    slides = _extract_slides(blueprint)

    result: Dict[str, List[int]] = {
        'visual_yes': [],
        'visual_no': [],
        'missing': [],
        'invalid': []
    }

    for i, slide in enumerate(slides):
        slide_number = slide.get('slide_number', i + 1)
        marker = slide.get('visual_marker')

        if marker is None:
            result['missing'].append(slide_number)
            continue

        details = _get_marker_details(marker)

        if not details.is_valid:
            result['invalid'].append(slide_number)
        elif details.marker_type == "yes":
            result['visual_yes'].append(slide_number)
        elif details.marker_type == "no":
            result['visual_no'].append(slide_number)

    return result


if __name__ == "__main__":
    # Self-test demonstration
    print("Marker Inserter Skill - Self Test")
    print("=" * 50)

    # Test 1: add_visual_marker
    print("\n1. Testing add_visual_marker:")
    slide = {'slide_number': 1, 'header': 'Test Slide'}
    visual_slide = add_visual_marker(slide, has_visual=True, visual_type="TABLE")
    no_visual_slide = add_visual_marker(slide, has_visual=False)
    print(f"   Visual slide marker: {visual_slide['visual_marker']}")
    print(f"   No-visual marker: {no_visual_slide['visual_marker']}")

    # Test 2: validate_marker_format
    print("\n2. Testing validate_marker_format:")
    test_markers = [
        "Visual: Yes - TABLE",
        "Visual: Yes - FLOWCHART",
        "Visual: No",
        "Visual: Yes - INVALID_TYPE",
        "Invalid marker",
        ""
    ]
    for marker in test_markers:
        is_valid, error = validate_marker_format(marker)
        status = "VALID" if is_valid else f"INVALID: {error}"
        print(f"   '{marker}' -> {status}")

    # Test 3: validate_all_markers
    print("\n3. Testing validate_all_markers:")
    blueprint = {
        'slides': [
            {'slide_number': 1, 'visual_marker': 'Visual: Yes - TABLE'},
            {'slide_number': 2, 'visual_marker': 'Visual: No'},
            {'slide_number': 3},  # Missing marker
            {'slide_number': 4, 'visual_marker': 'Invalid'},
        ]
    }
    validation = validate_all_markers(blueprint)
    print(f"   Valid: {validation['valid']}")
    print(f"   Total slides: {validation['total_slides']}")
    print(f"   Slides with marker: {validation['slides_with_marker']}")
    print(f"   Missing markers on slides: {validation['slides_missing_marker']}")
    print(f"   Invalid markers: {len(validation['invalid_markers'])}")

    # Test 4: count_markers
    print("\n4. Testing count_markers:")
    counts = count_markers(blueprint)
    print(f"   Yes: {counts['yes']}, No: {counts['no']}, "
          f"Missing: {counts['missing']}, Invalid: {counts['invalid']}, "
          f"Total: {counts['total']}")

    # Test 5: fix_missing_markers
    print("\n5. Testing fix_missing_markers:")
    fixed_blueprint = fix_missing_markers(blueprint)
    fixed_validation = validate_all_markers(fixed_blueprint)
    print(f"   Before fix - Missing: {validation['slides_missing_marker']}")
    print(f"   After fix - Missing: {fixed_validation['slides_missing_marker']}")
    # Note: Invalid markers are not fixed by this function
    print(f"   Invalid markers still present: {len(fixed_validation['invalid_markers'])}")

    print("\n" + "=" * 50)
    print("Self-test complete.")
