"""
Visual Merger
Merges visual specifications into slide blueprints for Step 10 Visual Integration.

Usage:
    from skills.generation.visual_merger import (
        merge_visual_spec, format_visual_section, clear_body_for_visual,
        preserve_presenter_notes, clear_nclex_tip_for_visual, integrate_all_visuals
    )
"""

import copy
from typing import Dict, Any, List, Optional


# Valid visual types from config/constraints.yaml
VALID_VISUAL_TYPES = [
    "TABLE",
    "FLOWCHART",
    "DECISION_TREE",
    "TIMELINE",
    "HIERARCHY",
    "SPECTRUM",
    "KEY_DIFFERENTIATORS"
]


def merge_visual_spec(slide: Dict[str, Any], visual_spec: Dict[str, Any]) -> Dict[str, Any]:
    """
    Merge a visual specification into a slide.

    Integration rules:
    - Replace body with "[See Visual]"
    - Add visual_marker: "Visual: Yes - {TYPE}"
    - Add visual_specification section
    - Clear NCLEX tip (set to "None")
    - PRESERVE presenter_notes (do not modify)

    Args:
        slide: Slide dictionary with header, body, nclex_tip, presenter_notes
        visual_spec: Visual specification with visual_type, layout, specification

    Returns:
        The integrated slide with visual marker and specification
    """
    # Create a deep copy to avoid modifying the original
    integrated_slide = copy.deepcopy(slide)

    # Extract visual type from specification
    visual_type = visual_spec.get("visual_type", "UNKNOWN")

    # Validate visual type
    if visual_type not in VALID_VISUAL_TYPES:
        visual_type = "UNKNOWN"

    # Add visual marker
    integrated_slide["visual_marker"] = f"Visual: Yes - {visual_type}"

    # Preserve presenter notes before any modifications
    original_notes = preserve_presenter_notes(slide)

    # Clear body for visual (replace with placeholder)
    integrated_slide = clear_body_for_visual(integrated_slide)

    # Clear NCLEX tip for visual slides
    integrated_slide = clear_nclex_tip_for_visual(integrated_slide)

    # Add visual specification section
    integrated_slide["visual_specification"] = {
        "type": visual_type,
        "layout": visual_spec.get("layout", "A"),
        "specification": visual_spec.get("specification", {})
    }

    # Ensure presenter notes are preserved (restore if accidentally modified)
    integrated_slide["presenter_notes"] = original_notes

    return integrated_slide


def format_visual_section(spec: Dict[str, Any], visual_type: str) -> str:
    """
    Format the visual specification as a string for the blueprint.

    Include all specification details (title, columns, rows, colors, etc.)

    Args:
        spec: The specification dictionary containing visual details
        visual_type: Type of visual (TABLE, FLOWCHART, etc.)

    Returns:
        Formatted string representation of the visual specification
    """
    lines = []
    lines.append(f"Type: {visual_type}")

    # Add title if present
    if "title" in spec:
        lines.append(f"Title: {spec['title']}")

    # Format based on visual type
    if visual_type == "TABLE":
        lines.extend(_format_table_spec(spec))
    elif visual_type == "FLOWCHART":
        lines.extend(_format_flowchart_spec(spec))
    elif visual_type == "DECISION_TREE":
        lines.extend(_format_decision_tree_spec(spec))
    elif visual_type == "TIMELINE":
        lines.extend(_format_timeline_spec(spec))
    elif visual_type == "HIERARCHY":
        lines.extend(_format_hierarchy_spec(spec))
    elif visual_type == "SPECTRUM":
        lines.extend(_format_spectrum_spec(spec))
    elif visual_type == "KEY_DIFFERENTIATORS":
        lines.extend(_format_key_diff_spec(spec))

    # Add colors if present
    if "colors" in spec:
        lines.append("")
        lines.append("Colors:")
        for color_key, color_value in spec["colors"].items():
            lines.append(f"  {color_key}: {color_value}")

    return "\n".join(lines)


def _format_table_spec(spec: Dict[str, Any]) -> List[str]:
    """Format TABLE specification details."""
    lines = []

    if "columns" in spec:
        columns = spec["columns"]
        lines.append(f"Columns: {len(columns)}")
        lines.append(f"Headers: {', '.join(columns)}")

    if "rows" in spec:
        rows = spec["rows"]
        lines.append(f"Rows: {len(rows)}")
        lines.append("")
        lines.append("TABLE CONTENT:")

        # Format as markdown table
        if "columns" in spec:
            header_row = "| " + " | ".join(spec["columns"]) + " |"
            separator = "|" + "|".join(["---" for _ in spec["columns"]]) + "|"
            lines.append(header_row)
            lines.append(separator)

        for row in rows:
            if isinstance(row, list):
                row_str = "| " + " | ".join(str(cell) for cell in row) + " |"
                lines.append(row_str)

    return lines


def _format_flowchart_spec(spec: Dict[str, Any]) -> List[str]:
    """Format FLOWCHART specification details."""
    lines = []

    if "start" in spec:
        lines.append(f"START: \"{spec['start']}\"")

    if "steps" in spec:
        lines.append("")
        lines.append("STEPS:")
        for i, step in enumerate(spec["steps"], 1):
            if isinstance(step, dict):
                lines.append(f"{i}. Header: \"{step.get('header', '')}\"")
                if "body" in step:
                    lines.append(f"   Body: \"{step['body']}\"")
            else:
                lines.append(f"{i}. {step}")

    if "end" in spec:
        lines.append(f"END: \"{spec['end']}\"")

    return lines


def _format_decision_tree_spec(spec: Dict[str, Any]) -> List[str]:
    """Format DECISION_TREE specification details."""
    lines = []

    if "root" in spec:
        lines.append(f"ROOT: \"{spec['root']}\"")

    if "levels" in spec:
        for level_name, level_data in spec["levels"].items():
            lines.append("")
            lines.append(f"{level_name}:")
            if isinstance(level_data, dict):
                if "header" in level_data:
                    lines.append(f"  Header: \"{level_data['header']}\"")
                if "question" in level_data:
                    lines.append(f"  Question: \"{level_data['question']}\"")
                if "paths" in level_data:
                    lines.append(f"  Paths: {level_data['paths']}")

    if "outcomes" in spec:
        lines.append("")
        lines.append("OUTCOMES:")
        for outcome in spec["outcomes"]:
            if isinstance(outcome, dict):
                lines.append(f"  - {outcome.get('name', 'Unknown')}")
            else:
                lines.append(f"  - {outcome}")

    return lines


def _format_timeline_spec(spec: Dict[str, Any]) -> List[str]:
    """Format TIMELINE specification details."""
    lines = []

    if "events" in spec:
        lines.append("")
        lines.append("EVENTS:")
        for i, event in enumerate(spec["events"], 1):
            if isinstance(event, dict):
                lines.append(f"{i}. Date: \"{event.get('date', '')}\"")
                if "header" in event:
                    lines.append(f"   Header: \"{event['header']}\"")
                if "description" in event:
                    lines.append(f"   Description: \"{event['description']}\"")
                if "features" in event:
                    lines.append(f"   Features: {event['features']}")
            else:
                lines.append(f"{i}. {event}")

    return lines


def _format_hierarchy_spec(spec: Dict[str, Any]) -> List[str]:
    """Format HIERARCHY specification details."""
    lines = []

    if "root" in spec:
        lines.append(f"ROOT: \"{spec['root']}\"")

    if "children" in spec:
        lines.append("")
        lines.append("LEVELS:")
        _format_hierarchy_children(spec["children"], lines, indent=0)

    return lines


def _format_hierarchy_children(children: List[Any], lines: List[str], indent: int) -> None:
    """Recursively format hierarchy children."""
    prefix = "  " * indent
    for child in children:
        if isinstance(child, dict):
            label = child.get("label", "Unknown")
            lines.append(f"{prefix}- \"{label}\"")
            if "children" in child:
                _format_hierarchy_children(child["children"], lines, indent + 1)
        elif isinstance(child, str):
            lines.append(f"{prefix}- \"{child}\"")


def _format_spectrum_spec(spec: Dict[str, Any]) -> List[str]:
    """Format SPECTRUM specification details."""
    lines = []

    if "gradient" in spec:
        lines.append(f"Gradient: {spec['gradient']}")

    if "endpoints" in spec:
        lines.append("")
        lines.append("ENDPOINTS:")
        endpoints = spec["endpoints"]
        if "low" in endpoints:
            lines.append(f"  Low: \"{endpoints['low']}\"")
        if "high" in endpoints:
            lines.append(f"  High: \"{endpoints['high']}\"")

    if "segments" in spec:
        lines.append("")
        lines.append("SEGMENTS:")
        for i, segment in enumerate(spec["segments"], 1):
            if isinstance(segment, dict):
                lines.append(f"{i}. Label: \"{segment.get('label', '')}\"")
                if "description" in segment:
                    lines.append(f"   Description: \"{segment['description']}\"")
            else:
                lines.append(f"{i}. {segment}")

    return lines


def _format_key_diff_spec(spec: Dict[str, Any]) -> List[str]:
    """Format KEY_DIFFERENTIATORS specification details."""
    lines = []

    if "concepts" in spec:
        lines.append("")
        lines.append("CONCEPTS:")
        for concept in spec["concepts"]:
            if isinstance(concept, dict):
                lines.append(f"  - Concept: \"{concept.get('name', '')}\"")
                if "color" in concept:
                    lines.append(f"    Color: {concept['color']}")
                if "features" in concept:
                    lines.append(f"    Features: {concept['features']}")
            else:
                lines.append(f"  - {concept}")

    if "key_differences" in spec:
        lines.append("")
        lines.append("KEY DIFFERENCES:")
        for i, diff in enumerate(spec["key_differences"], 1):
            lines.append(f"  KD{i}: \"{diff}\"")

    return lines


def clear_body_for_visual(slide: Dict[str, Any]) -> Dict[str, Any]:
    """
    Replace body content with "[See Visual]".

    Args:
        slide: Slide dictionary with body content

    Returns:
        Modified slide with body set to "[See Visual]"
    """
    result = copy.deepcopy(slide)
    result["body"] = "[See Visual]"
    return result


def preserve_presenter_notes(slide: Dict[str, Any]) -> str:
    """
    Extract and return presenter notes unchanged.

    Used to verify notes are not modified during visual integration.

    Args:
        slide: Slide dictionary with presenter_notes

    Returns:
        The original presenter notes string (empty string if not present)
    """
    return slide.get("presenter_notes", "")


def clear_nclex_tip_for_visual(slide: Dict[str, Any]) -> Dict[str, Any]:
    """
    Set nclex_tip to "None" for visual slides.

    Visual slides should not have NCLEX tips as the visual itself
    is the primary content focus.

    Args:
        slide: Slide dictionary with nclex_tip

    Returns:
        Modified slide with nclex_tip set to "None"
    """
    result = copy.deepcopy(slide)
    result["nclex_tip"] = "None"
    return result


def integrate_all_visuals(
    blueprint: Dict[str, Any],
    visual_specs: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """
    Apply all visual specs to matching slides in the blueprint.

    Integration rules:
    - Visual slides: body = "[See Visual]", tip = "None", notes = PRESERVED
    - Non-visual slides: Add "Visual: No" marker only

    Args:
        blueprint: Blueprint dictionary with 'slides' list
        visual_specs: List of visual specifications with slide_number

    Returns:
        Fully integrated blueprint with Visual: Yes/No on every slide
    """
    # Create a deep copy of the blueprint
    integrated_blueprint = copy.deepcopy(blueprint)

    # Build a map of slide_number -> visual_spec for quick lookup
    visual_map = {}
    for spec in visual_specs:
        slide_num = spec.get("slide_number")
        if slide_num is not None:
            visual_map[slide_num] = spec

    # Get slides from blueprint (handle different structures)
    slides = integrated_blueprint.get("slides", [])
    if not slides and "step7_blueprint" in integrated_blueprint:
        slides = integrated_blueprint["step7_blueprint"].get("slides", [])
        integrated_blueprint["slides"] = slides

    # Process each slide
    for slide in slides:
        slide_num = slide.get("slide_number")

        if slide_num in visual_map:
            # This slide gets a visual
            visual_spec = visual_map[slide_num]

            # Preserve original presenter notes
            original_notes = preserve_presenter_notes(slide)

            # Get visual type
            visual_type = visual_spec.get("visual_type", "UNKNOWN")

            # Add visual marker
            slide["visual_marker"] = f"Visual: Yes - {visual_type}"

            # Clear body
            slide["body"] = "[See Visual]"

            # Clear NCLEX tip
            slide["nclex_tip"] = "None"

            # Add visual specification
            slide["visual_specification"] = {
                "type": visual_type,
                "layout": visual_spec.get("layout", "A"),
                "specification": visual_spec.get("specification", {})
            }

            # Ensure presenter notes are preserved
            slide["presenter_notes"] = original_notes
        else:
            # This is a content slide - add "Visual: No" marker only
            slide["visual_marker"] = "Visual: No"

    # Add integration summary
    visual_slides = [s for s in slides if s.get("visual_marker", "").startswith("Visual: Yes")]
    content_slides = [s for s in slides if s.get("visual_marker") == "Visual: No"]

    # Count visual types
    visual_type_counts = {}
    for spec in visual_specs:
        vtype = spec.get("visual_type", "UNKNOWN")
        visual_type_counts[vtype] = visual_type_counts.get(vtype, 0) + 1

    integrated_blueprint["integration_summary"] = {
        "total_slides": len(slides),
        "visual_slides": len(visual_slides),
        "content_slides": len(content_slides),
        "visual_types": visual_type_counts
    }

    # Add validation results
    all_marked = all(
        "visual_marker" in s and s["visual_marker"] is not None
        for s in slides
    )
    specs_applied = len(visual_slides) == len(visual_specs)

    # Check quota (minimum 2 per section, max 40%)
    total_count = len(slides)
    visual_count = len(visual_slides)
    visual_percentage = (visual_count / total_count * 100) if total_count > 0 else 0

    if visual_count < 2:
        quota_check = "FAIL - Below minimum (2)"
    elif visual_percentage > 40:
        quota_check = "FAIL - Exceeds 40%"
    else:
        quota_check = "PASS"

    integrated_blueprint["validation"] = {
        "all_slides_marked": all_marked,
        "visual_specs_applied": specs_applied,
        "quota_check": quota_check
    }

    return integrated_blueprint


def get_integration_summary(blueprint: Dict[str, Any]) -> Dict[str, Any]:
    """
    Get a summary of the visual integration status.

    Args:
        blueprint: Integrated blueprint with visual markers

    Returns:
        Summary dictionary with counts and validation status
    """
    slides = blueprint.get("slides", [])

    visual_yes = []
    visual_no = []
    unmarked = []

    for slide in slides:
        marker = slide.get("visual_marker")
        slide_num = slide.get("slide_number", "?")

        if marker is None:
            unmarked.append(slide_num)
        elif marker.startswith("Visual: Yes"):
            visual_yes.append(slide_num)
        elif marker == "Visual: No":
            visual_no.append(slide_num)

    return {
        "total_slides": len(slides),
        "visual_slides": len(visual_yes),
        "visual_slide_numbers": visual_yes,
        "content_slides": len(visual_no),
        "content_slide_numbers": visual_no,
        "unmarked_slides": len(unmarked),
        "unmarked_slide_numbers": unmarked,
        "all_marked": len(unmarked) == 0
    }


def validate_integration(blueprint: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate that the visual integration was performed correctly.

    Checks:
    - Every slide has Visual: Yes or Visual: No marker
    - Visual slides have body = "[See Visual]"
    - Visual slides have nclex_tip = "None"
    - Visual slides have presenter_notes preserved (not empty)
    - Visual specifications are present on visual slides

    Args:
        blueprint: Integrated blueprint

    Returns:
        Validation result dictionary
    """
    slides = blueprint.get("slides", [])
    issues = []

    for slide in slides:
        slide_num = slide.get("slide_number", "?")
        marker = slide.get("visual_marker")

        # Check for visual marker
        if marker is None:
            issues.append({
                "slide": slide_num,
                "issue": "Missing visual marker"
            })
            continue

        if marker.startswith("Visual: Yes"):
            # Validate visual slide requirements
            if slide.get("body") != "[See Visual]":
                issues.append({
                    "slide": slide_num,
                    "issue": f"Visual slide body should be '[See Visual]', got: {slide.get('body', 'None')[:50]}..."
                })

            if slide.get("nclex_tip") != "None":
                issues.append({
                    "slide": slide_num,
                    "issue": f"Visual slide nclex_tip should be 'None', got: {slide.get('nclex_tip', 'None')}"
                })

            if "visual_specification" not in slide:
                issues.append({
                    "slide": slide_num,
                    "issue": "Visual slide missing visual_specification"
                })

    return {
        "valid": len(issues) == 0,
        "issues": issues,
        "checked_slides": len(slides)
    }


if __name__ == "__main__":
    # Test with sample data
    sample_slide = {
        "slide_number": 3,
        "slide_type": "Content",
        "header": "ACE Inhibitors vs ARBs",
        "body": "* ACE-I: Block conversion\n* ARBs: Block receptor",
        "nclex_tip": "NCLEX often compares ACE-I and ARB side effects",
        "presenter_notes": "[PAUSE] Let's compare these two important drug classes.",
        "visual_marker": None
    }

    sample_visual_spec = {
        "slide_number": 3,
        "visual_type": "TABLE",
        "layout": "B",
        "specification": {
            "title": "ACE Inhibitors vs ARBs Comparison",
            "columns": ["Feature", "ACE Inhibitors", "ARBs"],
            "rows": [
                ["Mechanism", "Block ACE enzyme", "Block AT1 receptor"],
                ["Cough", "Yes (10%)", "No"]
            ],
            "colors": {
                "header_bg": "#1a5276",
                "row_alt": "#d4e6f1"
            }
        }
    }

    # Test merge_visual_spec
    integrated = merge_visual_spec(sample_slide, sample_visual_spec)
    print("Integrated slide:")
    print(f"  visual_marker: {integrated['visual_marker']}")
    print(f"  body: {integrated['body']}")
    print(f"  nclex_tip: {integrated['nclex_tip']}")
    print(f"  presenter_notes: {integrated['presenter_notes']}")
    print(f"  visual_specification: {integrated.get('visual_specification', {}).get('type')}")

    # Test format_visual_section
    formatted = format_visual_section(
        sample_visual_spec["specification"],
        sample_visual_spec["visual_type"]
    )
    print("\nFormatted visual section:")
    print(formatted)
