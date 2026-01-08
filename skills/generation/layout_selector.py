"""
Layout Selector for Step 9 Visual Identification
Selects optimal layouts for each visual type based on content characteristics.

Usage:
    from skills.generation.layout_selector import (
        select_table_layout, select_flowchart_layout, select_decision_tree_layout,
        select_timeline_layout, select_hierarchy_layout, select_spectrum_layout,
        select_keydiff_layout, auto_select_layout
    )
"""

from typing import Dict, List, Any, Optional
from enum import Enum


class Layout(Enum):
    """Standard layout options A-E for all visual types."""
    A = "A"
    B = "B"
    C = "C"
    D = "D"
    E = "E"


# =============================================================================
# VISUAL TYPE CONSTRAINTS (from visual_identifier.md)
# =============================================================================

VISUAL_CONSTRAINTS = {
    "TABLE": {
        "max_columns": 4,
        "max_rows": 6,
        "font_minimum": 18
    },
    "FLOWCHART": {
        "max_steps": 7,
        "font_minimum": 18
    },
    "DECISION_TREE": {
        "max_nodes": 15,
        "max_levels": 4,
        "font_minimum": 18
    },
    "TIMELINE": {
        "max_events": 8,
        "font_minimum": 18
    },
    "HIERARCHY": {
        "max_nodes": 15,
        "max_levels": 4,
        "font_minimum": 18
    },
    "SPECTRUM": {
        "max_segments": 6,
        "font_minimum": 18
    },
    "KEY_DIFFERENTIATORS": {
        "max_items": 3,
        "max_features": 4,
        "font_minimum": 18
    }
}


# =============================================================================
# TABLE LAYOUT SELECTION
# =============================================================================

def select_table_layout(data: Dict[str, Any]) -> str:
    """
    Analyze table data and return optimal layout (A, B, C, D, or E).

    Layout Definitions:
        A: 2-3 columns, simple comparison (standard)
        B: 3-4 columns, detailed comparison (default)
        C: 2 columns, feature list style
        D: 4+ columns, comprehensive matrix
        E: Compact, high-density data

    Args:
        data: Dictionary containing table structure information:
            - headers: List of column headers
            - rows: List of row data
            - columns (optional): Number of columns
            - row_count (optional): Number of rows
            - content_density (optional): 'low', 'medium', 'high'

    Returns:
        Layout letter (A, B, C, D, or E)

    Examples:
        >>> select_table_layout({"headers": ["A", "B"], "rows": [["1", "2"]]})
        'A'
        >>> select_table_layout({"headers": ["A", "B", "C", "D", "E"], "rows": [...]})
        'D'
    """
    # Extract column count
    headers = data.get("headers", [])
    rows = data.get("rows", [])
    columns = data.get("columns", len(headers)) if headers else data.get("columns", 0)
    row_count = data.get("row_count", len(rows)) if rows else data.get("row_count", 0)
    content_density = data.get("content_density", "medium")

    # Enforce constraints
    columns = min(columns, VISUAL_CONSTRAINTS["TABLE"]["max_columns"])
    row_count = min(row_count, VISUAL_CONSTRAINTS["TABLE"]["max_rows"])

    # Calculate average cell content length for density analysis
    avg_cell_length = _calculate_avg_cell_length(rows)

    # Layout selection logic
    if columns >= 4:
        # Many columns -> comprehensive matrix
        return Layout.D.value

    if columns == 2:
        if _is_feature_list_pattern(data):
            # 2 columns with feature-value pattern
            return Layout.C.value
        # Simple 2-column comparison
        return Layout.A.value

    if columns == 3:
        if content_density == "high" or avg_cell_length > 30:
            # High density content needs more space
            return Layout.E.value
        # Standard 3-column comparison
        return Layout.A.value

    if content_density == "high" or row_count >= 5:
        # High density or many rows
        return Layout.E.value

    # Default: detailed comparison layout
    return Layout.B.value


def _calculate_avg_cell_length(rows: List[List[str]]) -> float:
    """Calculate average cell content length."""
    if not rows:
        return 0.0

    total_length = 0
    cell_count = 0

    for row in rows:
        for cell in row:
            if isinstance(cell, str):
                total_length += len(cell)
                cell_count += 1

    return total_length / cell_count if cell_count > 0 else 0.0


def _is_feature_list_pattern(data: Dict[str, Any]) -> bool:
    """Check if data follows a feature-value list pattern."""
    headers = data.get("headers", [])
    if len(headers) == 2:
        # Check for common feature-list header patterns
        feature_keywords = ["feature", "property", "attribute", "parameter", "criteria"]
        value_keywords = ["value", "description", "detail", "finding", "result"]

        h0_lower = headers[0].lower() if headers else ""
        h1_lower = headers[1].lower() if len(headers) > 1 else ""

        return (
            any(kw in h0_lower for kw in feature_keywords) or
            any(kw in h1_lower for kw in value_keywords)
        )
    return False


# =============================================================================
# FLOWCHART LAYOUT SELECTION
# =============================================================================

def select_flowchart_layout(steps: List[str]) -> str:
    """
    Analyze process steps and return optimal flowchart layout.

    Layout Definitions:
        A: Linear horizontal (3-4 steps)
        B: Linear vertical with branches (5-6 steps)
        C: Circular/cycle
        D: Complex branching (7+ steps)
        E: Swimlane style

    Args:
        steps: List of step descriptions in the process

    Returns:
        Layout letter (A, B, C, D, or E)

    Examples:
        >>> select_flowchart_layout(["Step 1", "Step 2", "Step 3"])
        'A'
        >>> select_flowchart_layout(["S1", "S2", "S3", "S4", "S5", "S6", "S7"])
        'D'
    """
    step_count = len(steps)

    # Enforce constraint
    step_count = min(step_count, VISUAL_CONSTRAINTS["FLOWCHART"]["max_steps"])

    # Check for cycle pattern (last step references first)
    is_cycle = _detect_cycle_pattern(steps)
    if is_cycle:
        return Layout.C.value

    # Check for swimlane pattern (parallel processes)
    has_parallel = _detect_parallel_pattern(steps)
    if has_parallel:
        return Layout.E.value

    # Linear selection based on step count
    if step_count <= 4:
        return Layout.A.value  # Linear horizontal
    elif step_count <= 6:
        return Layout.B.value  # Linear vertical with branches
    else:
        return Layout.D.value  # Complex branching


def _detect_cycle_pattern(steps: List[str]) -> bool:
    """Detect if steps form a cycle (last connects to first)."""
    if len(steps) < 3:
        return False

    cycle_keywords = [
        "repeat", "cycle", "return to", "back to", "loop",
        "continuous", "ongoing", "iterative"
    ]

    last_step = steps[-1].lower() if steps else ""
    first_step = steps[0].lower() if steps else ""

    # Check for explicit cycle keywords
    for kw in cycle_keywords:
        if kw in last_step:
            return True

    # Check if last step explicitly references first step
    # Require longer, more specific words (6+ chars) to avoid false positives
    first_words = first_step.split()[:3]
    for word in first_words:
        # Require longer words and explicit reference pattern
        if len(word) > 5 and word in last_step and word not in ["start", "begin", "first"]:
            return True

    return False


def _detect_parallel_pattern(steps: List[str]) -> bool:
    """Detect if steps suggest parallel processes (swimlane appropriate)."""
    # Only consider swimlane for 5+ steps
    if len(steps) < 5:
        return False

    parallel_keywords = [
        "simultaneously", "at the same time", "concurrent",
        "parallel", "meanwhile"
    ]

    parallel_count = 0
    for step in steps:
        step_lower = step.lower()
        for kw in parallel_keywords:
            if kw in step_lower:
                parallel_count += 1
                break

    # Need multiple parallel indicators for swimlane
    return parallel_count >= 2


# =============================================================================
# DECISION TREE LAYOUT SELECTION
# =============================================================================

def select_decision_tree_layout(data: Dict[str, Any]) -> str:
    """
    Analyze decision tree data and return optimal layout.

    Layout Definitions:
        A: Three-level binary (1-2-4 pattern)
        B: Two-level binary (1-2 pattern)
        C: Two-level triple (1-3 pattern)
        D: Three-level asymmetric
        E: Three-level extended (1-2-6 pattern)

    Args:
        data: Dictionary containing:
            - depth: Maximum tree depth (1-4)
            - node_count: Total number of nodes
            - nodes (optional): List of node objects
            - decision_points (optional): Number of decision nodes
            - branches_per_node (optional): Average branches per decision

    Returns:
        Layout letter (A, B, C, D, or E)

    Examples:
        >>> select_decision_tree_layout({"depth": 2, "node_count": 3})
        'B'
        >>> select_decision_tree_layout({"depth": 3, "node_count": 7})
        'A'
    """
    depth = data.get("depth", 2)
    node_count = data.get("node_count", 0)
    branches_per_node = data.get("branches_per_node", 2)

    # Enforce constraints
    depth = min(depth, VISUAL_CONSTRAINTS["DECISION_TREE"]["max_levels"])
    node_count = min(node_count, VISUAL_CONSTRAINTS["DECISION_TREE"]["max_nodes"])

    # Analyze tree structure if nodes provided
    nodes = data.get("nodes", [])
    if nodes:
        tree_structure = _analyze_tree_structure(nodes)
        depth = tree_structure.get("depth", depth)
        branches_per_node = tree_structure.get("avg_branches", branches_per_node)

    # Layout selection based on depth and branching
    if depth <= 2:
        if branches_per_node >= 3:
            return Layout.C.value  # Two-level triple
        return Layout.B.value  # Two-level binary

    if depth == 3:
        if node_count > 10:
            return Layout.E.value  # Three-level extended
        if _is_asymmetric_tree(data):
            return Layout.D.value  # Asymmetric
        return Layout.A.value  # Three-level binary

    # Deep trees (depth 4) - use extended layout
    return Layout.E.value


def _analyze_tree_structure(nodes: List[Dict]) -> Dict[str, Any]:
    """Analyze tree structure from node list."""
    if not nodes:
        return {"depth": 0, "avg_branches": 0}

    max_depth = 0
    branch_counts = []

    for node in nodes:
        level = node.get("level", 0)
        children = node.get("children", [])
        max_depth = max(max_depth, level)
        if children:
            branch_counts.append(len(children))

    avg_branches = sum(branch_counts) / len(branch_counts) if branch_counts else 2

    return {
        "depth": max_depth,
        "avg_branches": avg_branches
    }


def _is_asymmetric_tree(data: Dict[str, Any]) -> bool:
    """Check if tree is asymmetric (unequal branch depths)."""
    nodes = data.get("nodes", [])
    if not nodes:
        return False

    # Check for unequal subtree depths
    leaf_depths = []
    for node in nodes:
        if not node.get("children"):
            leaf_depths.append(node.get("level", 0))

    if leaf_depths:
        return max(leaf_depths) - min(leaf_depths) > 1

    return False


# =============================================================================
# TIMELINE LAYOUT SELECTION
# =============================================================================

def select_timeline_layout(events: List[Dict[str, Any]]) -> str:
    """
    Analyze timeline events and return optimal layout.

    Layout Definitions:
        A: Horizontal timeline (3-5 events)
        B: Vertical timeline (6-8 events)
        C: Milestone style (key events emphasized)
        D: Parallel tracks (multiple concurrent timelines)

    Args:
        events: List of event dictionaries containing:
            - date/time: Event timing
            - title: Event name
            - description (optional): Event details
            - track (optional): Timeline track identifier

    Returns:
        Layout letter (A, B, C, or D)

    Examples:
        >>> select_timeline_layout([{"date": "Day 1"}, {"date": "Day 2"}])
        'A'
        >>> select_timeline_layout([{"date": "2020"}, {"date": "2021"}, ...])
        'B'
    """
    event_count = len(events)

    # Enforce constraint
    event_count = min(event_count, VISUAL_CONSTRAINTS["TIMELINE"]["max_events"])

    # Check for parallel tracks
    tracks = set()
    for event in events:
        track = event.get("track")
        if track:
            tracks.add(track)

    if len(tracks) > 1:
        return Layout.D.value  # Parallel tracks

    # Check for milestone pattern (varying importance)
    has_milestones = _has_milestone_pattern(events)
    if has_milestones:
        return Layout.C.value

    # Select based on event count
    if event_count <= 5:
        return Layout.A.value  # Horizontal
    else:
        return Layout.B.value  # Vertical


def _has_milestone_pattern(events: List[Dict[str, Any]]) -> bool:
    """Check if events have varying importance levels (milestone pattern)."""
    milestone_keywords = [
        "milestone", "key", "major", "significant", "critical",
        "turning point", "landmark"
    ]

    importance_levels = set()
    for event in events:
        importance = event.get("importance", event.get("priority"))
        if importance:
            importance_levels.add(importance)

        title = event.get("title", "").lower()
        for kw in milestone_keywords:
            if kw in title:
                return True

    # Multiple importance levels suggest milestone pattern
    return len(importance_levels) > 1


# =============================================================================
# HIERARCHY LAYOUT SELECTION
# =============================================================================

def select_hierarchy_layout(data: Dict[str, Any]) -> str:
    """
    Analyze hierarchy structure and return optimal layout.

    Layout Definitions:
        A: Top-down tree (1-2-4 pattern)
        B: Top-down wide tree (1-3-6 pattern)
        C: Organizational chart style
        D: Inverted pyramid
        E: Side-by-side hierarchies

    Args:
        data: Dictionary containing:
            - levels: Number of hierarchy levels (1-4)
            - nodes_per_level: List of node counts per level
            - total_nodes: Total node count
            - nodes (optional): List of node objects with parent/child info
            - type (optional): 'org_chart', 'classification', 'taxonomy'

    Returns:
        Layout letter (A, B, C, D, or E)

    Examples:
        >>> select_hierarchy_layout({"levels": 3, "nodes_per_level": [1, 2, 4]})
        'A'
        >>> select_hierarchy_layout({"type": "org_chart", "levels": 3})
        'C'
    """
    levels = data.get("levels", 2)
    total_nodes = data.get("total_nodes", 0)
    nodes_per_level = data.get("nodes_per_level", [])
    hierarchy_type = data.get("type", "").lower()

    # Enforce constraints
    levels = min(levels, VISUAL_CONSTRAINTS["HIERARCHY"]["max_levels"])
    total_nodes = min(total_nodes, VISUAL_CONSTRAINTS["HIERARCHY"]["max_nodes"])

    # Check for explicit type
    if hierarchy_type == "org_chart":
        return Layout.C.value
    if hierarchy_type == "inverted" or hierarchy_type == "pyramid":
        return Layout.D.value

    # Check for side-by-side pattern (multiple roots)
    roots = nodes_per_level[0] if nodes_per_level else 1
    if roots > 1:
        return Layout.E.value  # Side-by-side hierarchies

    # Check for inverted pyramid (more nodes at top)
    if _is_inverted_pyramid(nodes_per_level):
        return Layout.D.value

    # Analyze breadth vs depth
    avg_children = _calculate_avg_children(nodes_per_level)

    if avg_children >= 3:
        return Layout.B.value  # Wide tree
    else:
        return Layout.A.value  # Standard tree


def _is_inverted_pyramid(nodes_per_level: List[int]) -> bool:
    """Check if hierarchy forms an inverted pyramid (decreasing nodes)."""
    if len(nodes_per_level) < 2:
        return False

    # Inverted pyramid: more nodes at top levels
    for i in range(len(nodes_per_level) - 1):
        if nodes_per_level[i] < nodes_per_level[i + 1]:
            return False  # Normal pyramid pattern

    return True


def _calculate_avg_children(nodes_per_level: List[int]) -> float:
    """Calculate average children per parent node."""
    if len(nodes_per_level) < 2:
        return 0.0

    total_ratio = 0.0
    count = 0

    for i in range(len(nodes_per_level) - 1):
        if nodes_per_level[i] > 0:
            ratio = nodes_per_level[i + 1] / nodes_per_level[i]
            total_ratio += ratio
            count += 1

    return total_ratio / count if count > 0 else 0.0


# =============================================================================
# SPECTRUM LAYOUT SELECTION
# =============================================================================

def select_spectrum_layout(segments: List[Dict[str, Any]]) -> str:
    """
    Analyze spectrum segments and return optimal layout.

    Layout Definitions:
        A: Horizontal bar spectrum (3-5 segments)
        B: Vertical bar spectrum (4-6 segments)
        C: Bipolar spectrum with center point
        D: Segmented spectrum (distinct segments)
        E: Dual-axis spectrum

    Args:
        segments: List of segment dictionaries containing:
            - label: Segment name
            - value (optional): Position or intensity
            - description (optional): Segment details
            - pole (optional): For bipolar spectrums ('left', 'right', 'center')

    Returns:
        Layout letter (A, B, C, D, or E)

    Examples:
        >>> select_spectrum_layout([{"label": "Mild"}, {"label": "Severe"}])
        'A'
        >>> select_spectrum_layout([{"label": "Low", "pole": "left"}, ...])
        'C'
    """
    segment_count = len(segments)

    # Enforce constraint
    segment_count = min(segment_count, VISUAL_CONSTRAINTS["SPECTRUM"]["max_segments"])

    # Check for bipolar pattern
    if _is_bipolar_spectrum(segments):
        return Layout.C.value

    # Check for dual-axis pattern
    if _has_dual_axis(segments):
        return Layout.E.value

    # Check for distinct segments (non-continuous)
    if _are_distinct_segments(segments):
        return Layout.D.value

    # Select based on segment count
    if segment_count <= 4:
        return Layout.A.value  # Horizontal
    else:
        return Layout.B.value  # Vertical


def _is_bipolar_spectrum(segments: List[Dict[str, Any]]) -> bool:
    """Check if spectrum is bipolar (has opposing poles)."""
    # Need at least 2 segments for bipolar
    if len(segments) < 2:
        return False

    bipolar_keywords = [
        ("low", "high"), ("normal", "abnormal"),
        ("negative", "positive"), ("cold", "hot"), ("hypo", "hyper"),
        ("deficit", "excess")
    ]

    labels = [s.get("label", "").lower() for s in segments]

    # Check for explicit pole markers
    poles = [s.get("pole") for s in segments if s.get("pole")]
    if "left" in poles and "right" in poles:
        return True

    # Check for bipolar keyword pairs - only exact/near-exact matches
    # to avoid false positives with severity scales
    for left, right in bipolar_keywords:
        has_left = any(label == left or label.startswith(left + " ") for label in labels)
        has_right = any(label == right or label.startswith(right + " ") for label in labels)
        if has_left and has_right:
            return True

    return False


def _has_dual_axis(segments: List[Dict[str, Any]]) -> bool:
    """Check if spectrum has dual axes."""
    for segment in segments:
        if segment.get("axis") or segment.get("dimension"):
            axes = set()
            for s in segments:
                axis = s.get("axis", s.get("dimension"))
                if axis:
                    axes.add(axis)
            return len(axes) > 1
    return False


def _are_distinct_segments(segments: List[Dict[str, Any]]) -> bool:
    """Check if segments are distinct (categorical) vs continuous."""
    if not segments:
        return False

    # Look for explicit distinct/discrete markers
    explicit_distinct = 0
    for segment in segments:
        # Check for explicit distinct value markers - these are reliable
        if segment.get("distinct") or segment.get("discrete"):
            explicit_distinct += 1

    # Require majority to have explicit markers
    return explicit_distinct >= (len(segments) + 1) // 2


# =============================================================================
# KEY DIFFERENTIATORS LAYOUT SELECTION
# =============================================================================

def select_keydiff_layout(concepts: List[Dict[str, Any]]) -> str:
    """
    Analyze key differentiator data and return optimal layout.

    Layout Definitions:
        A: Side-by-side comparison (2 concepts)
        B: Centered key differentiator emphasis
        C: Multiple differentiators highlighted
        D: Three-way discrimination
        E: Feature matrix (3-4 concepts)

    Args:
        concepts: List of concept dictionaries containing:
            - name: Concept name
            - features: List of features
            - key_diff (optional): The key differentiating feature
            - description (optional): Concept overview

    Returns:
        Layout letter (A, B, C, D, or E)

    Examples:
        >>> select_keydiff_layout([{"name": "A", "features": [...]}, {"name": "B", "features": [...]}])
        'A'
    """
    concept_count = len(concepts)

    # Enforce constraint
    concept_count = min(concept_count, VISUAL_CONSTRAINTS["KEY_DIFFERENTIATORS"]["max_items"])

    # Count features across concepts
    max_features = 0
    key_diff_count = 0

    for concept in concepts:
        features = concept.get("features", [])
        max_features = max(max_features, len(features))
        if concept.get("key_diff"):
            key_diff_count += 1

    # Enforce feature constraint
    max_features = min(max_features, VISUAL_CONSTRAINTS["KEY_DIFFERENTIATORS"]["max_features"])

    # Layout selection based on concept count and features
    if concept_count == 2:
        if key_diff_count > 0:
            return Layout.B.value  # Centered key differentiator
        return Layout.A.value  # Side-by-side

    if concept_count == 3:
        if key_diff_count >= 2:
            return Layout.C.value  # Multiple differentiators
        return Layout.D.value  # Three-way discrimination

    # 4+ concepts -> feature matrix
    return Layout.E.value


# =============================================================================
# AUTO-SELECT LAYOUT (DISPATCHER)
# =============================================================================

def auto_select_layout(visual_type: str, content: Dict[str, Any]) -> str:
    """
    Automatically select the best layout for a given visual type.

    This is the main dispatcher function that routes to the appropriate
    layout selector based on visual type.

    Args:
        visual_type: One of TABLE, FLOWCHART, DECISION_TREE, TIMELINE,
                    HIERARCHY, SPECTRUM, KEY_DIFFERENTIATORS
        content: Content dictionary appropriate for the visual type

    Returns:
        Layout letter (A, B, C, D, or E)

    Raises:
        ValueError: If visual_type is not recognized

    Examples:
        >>> auto_select_layout("TABLE", {"headers": ["A", "B"], "rows": []})
        'A'
        >>> auto_select_layout("FLOWCHART", {"steps": ["1", "2", "3"]})
        'A'
    """
    visual_type_upper = visual_type.upper()

    if visual_type_upper == "TABLE":
        return select_table_layout(content)

    elif visual_type_upper == "FLOWCHART":
        steps = content.get("steps", [])
        return select_flowchart_layout(steps)

    elif visual_type_upper == "DECISION_TREE":
        return select_decision_tree_layout(content)

    elif visual_type_upper == "TIMELINE":
        events = content.get("events", [])
        return select_timeline_layout(events)

    elif visual_type_upper == "HIERARCHY":
        return select_hierarchy_layout(content)

    elif visual_type_upper == "SPECTRUM":
        segments = content.get("segments", [])
        return select_spectrum_layout(segments)

    elif visual_type_upper == "KEY_DIFFERENTIATORS":
        concepts = content.get("concepts", [])
        return select_keydiff_layout(concepts)

    else:
        raise ValueError(
            f"Unknown visual type: {visual_type}. "
            f"Expected one of: TABLE, FLOWCHART, DECISION_TREE, "
            f"TIMELINE, HIERARCHY, SPECTRUM, KEY_DIFFERENTIATORS"
        )


# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================

def get_layout_description(visual_type: str, layout: str) -> str:
    """
    Get human-readable description of a layout.

    Args:
        visual_type: The visual type
        layout: The layout letter (A-E)

    Returns:
        Description string
    """
    descriptions = {
        "TABLE": {
            "A": "Standard Comparison (2-3 columns)",
            "B": "Detailed Comparison (3-4 columns)",
            "C": "Feature List (2 columns)",
            "D": "Comprehensive Matrix (4+ columns)",
            "E": "Compact High-Density"
        },
        "FLOWCHART": {
            "A": "Linear Horizontal (3-4 steps)",
            "B": "Linear Vertical with Branches (5-6 steps)",
            "C": "Circular/Cycle",
            "D": "Complex Branching (7+ steps)",
            "E": "Swimlane"
        },
        "DECISION_TREE": {
            "A": "Three-level Binary (1-2-4)",
            "B": "Two-level Binary (1-2)",
            "C": "Two-level Triple (1-3)",
            "D": "Three-level Asymmetric",
            "E": "Three-level Extended (1-2-6)"
        },
        "TIMELINE": {
            "A": "Horizontal Timeline (3-5 events)",
            "B": "Vertical Timeline (6-8 events)",
            "C": "Milestone Style",
            "D": "Parallel Tracks"
        },
        "HIERARCHY": {
            "A": "Top-Down Tree (1-2-4)",
            "B": "Top-Down Wide Tree (1-3-6)",
            "C": "Organizational Chart",
            "D": "Inverted Pyramid",
            "E": "Side-by-Side Hierarchies"
        },
        "SPECTRUM": {
            "A": "Horizontal Bar (3-5 segments)",
            "B": "Vertical Bar (4-6 segments)",
            "C": "Bipolar with Center",
            "D": "Segmented Spectrum",
            "E": "Dual-Axis Spectrum"
        },
        "KEY_DIFFERENTIATORS": {
            "A": "Side-by-Side (2 concepts)",
            "B": "Centered Key Differentiator",
            "C": "Multiple Differentiators",
            "D": "Three-Way Discrimination",
            "E": "Feature Matrix (3-4 concepts)"
        }
    }

    type_descs = descriptions.get(visual_type.upper(), {})
    return type_descs.get(layout.upper(), f"Layout {layout}")


def get_constraints(visual_type: str) -> Dict[str, Any]:
    """
    Get constraints for a visual type.

    Args:
        visual_type: The visual type

    Returns:
        Dictionary of constraints
    """
    return VISUAL_CONSTRAINTS.get(visual_type.upper(), {})


# =============================================================================
# MODULE TEST
# =============================================================================

if __name__ == "__main__":
    # Test cases for each visual type

    print("=" * 60)
    print("LAYOUT SELECTOR TEST SUITE")
    print("=" * 60)

    # TABLE tests
    print("\n--- TABLE LAYOUT TESTS ---")
    test_tables = [
        {"headers": ["A", "B"], "rows": [["1", "2"]]},
        {"headers": ["A", "B", "C", "D"], "rows": [["1", "2", "3", "4"]]},
        {"headers": ["Feature", "Value"], "rows": [["X", "Y"]]},
        {"columns": 4, "row_count": 6, "content_density": "high"},
    ]
    for i, data in enumerate(test_tables):
        layout = select_table_layout(data)
        desc = get_layout_description("TABLE", layout)
        print(f"  Test {i + 1}: {layout} - {desc}")

    # FLOWCHART tests
    print("\n--- FLOWCHART LAYOUT TESTS ---")
    test_flowcharts = [
        ["Step 1", "Step 2", "Step 3"],
        ["A", "B", "C", "D", "E", "F"],
        ["Start", "Process", "End", "Return to Start"],
        ["Task A", "Task B simultaneously", "Task C"],
    ]
    for i, steps in enumerate(test_flowcharts):
        layout = select_flowchart_layout(steps)
        desc = get_layout_description("FLOWCHART", layout)
        print(f"  Test {i + 1}: {layout} - {desc}")

    # DECISION_TREE tests
    print("\n--- DECISION TREE LAYOUT TESTS ---")
    test_trees = [
        {"depth": 2, "node_count": 3},
        {"depth": 3, "node_count": 7},
        {"depth": 2, "node_count": 4, "branches_per_node": 3},
        {"depth": 4, "node_count": 15},
    ]
    for i, data in enumerate(test_trees):
        layout = select_decision_tree_layout(data)
        desc = get_layout_description("DECISION_TREE", layout)
        print(f"  Test {i + 1}: {layout} - {desc}")

    # TIMELINE tests
    print("\n--- TIMELINE LAYOUT TESTS ---")
    test_timelines = [
        [{"date": "Day 1"}, {"date": "Day 2"}, {"date": "Day 3"}],
        [{"date": f"Week {i}"} for i in range(1, 8)],
        [{"date": "2020", "importance": "high"}, {"date": "2021", "importance": "low"}],
        [{"date": "T1", "track": "A"}, {"date": "T2", "track": "B"}],
    ]
    for i, events in enumerate(test_timelines):
        layout = select_timeline_layout(events)
        desc = get_layout_description("TIMELINE", layout)
        print(f"  Test {i + 1}: {layout} - {desc}")

    # HIERARCHY tests
    print("\n--- HIERARCHY LAYOUT TESTS ---")
    test_hierarchies = [
        {"levels": 3, "nodes_per_level": [1, 2, 4]},
        {"levels": 3, "nodes_per_level": [1, 3, 6]},
        {"type": "org_chart", "levels": 3},
        {"levels": 3, "nodes_per_level": [2, 4, 8]},
    ]
    for i, data in enumerate(test_hierarchies):
        layout = select_hierarchy_layout(data)
        desc = get_layout_description("HIERARCHY", layout)
        print(f"  Test {i + 1}: {layout} - {desc}")

    # SPECTRUM tests
    print("\n--- SPECTRUM LAYOUT TESTS ---")
    test_spectrums = [
        [{"label": "Mild"}, {"label": "Moderate"}, {"label": "Severe"}],
        [{"label": f"Level {i}"} for i in range(1, 6)],
        [{"label": "Low", "pole": "left"}, {"label": "High", "pole": "right"}],
        [{"label": "Type A", "distinct": True}, {"label": "Type B", "distinct": True}],
    ]
    for i, segments in enumerate(test_spectrums):
        layout = select_spectrum_layout(segments)
        desc = get_layout_description("SPECTRUM", layout)
        print(f"  Test {i + 1}: {layout} - {desc}")

    # KEY_DIFFERENTIATORS tests
    print("\n--- KEY DIFFERENTIATORS LAYOUT TESTS ---")
    test_keydiffs = [
        [{"name": "A", "features": ["f1", "f2"]}, {"name": "B", "features": ["f1", "f2"]}],
        [{"name": "A", "key_diff": "X"}, {"name": "B", "key_diff": "Y"}],
        [{"name": "A"}, {"name": "B"}, {"name": "C"}],
        [{"name": f"Concept {i}"} for i in range(1, 5)],
    ]
    for i, concepts in enumerate(test_keydiffs):
        layout = select_keydiff_layout(concepts)
        desc = get_layout_description("KEY_DIFFERENTIATORS", layout)
        print(f"  Test {i + 1}: {layout} - {desc}")

    # AUTO-SELECT tests
    print("\n--- AUTO-SELECT LAYOUT TESTS ---")
    auto_tests = [
        ("TABLE", {"headers": ["A", "B", "C"], "rows": []}),
        ("FLOWCHART", {"steps": ["1", "2", "3", "4", "5"]}),
        ("TIMELINE", {"events": [{"date": "Jan"}, {"date": "Feb"}]}),
    ]
    for visual_type, content in auto_tests:
        layout = auto_select_layout(visual_type, content)
        desc = get_layout_description(visual_type, layout)
        print(f"  {visual_type}: {layout} - {desc}")

    print("\n" + "=" * 60)
    print("ALL TESTS COMPLETED")
    print("=" * 60)
