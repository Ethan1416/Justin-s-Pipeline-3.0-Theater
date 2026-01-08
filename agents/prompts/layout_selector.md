# Layout Selector Agent (Template for All Visual Types)

## Agent Identity
- **Name:** layout_selector
- **Step:** 12 (PowerPoint Population - Layout Selection)
- **Purpose:** Automatically select optimal layout variant (A/B/C/D/E) for any visual type based on content analysis

---

## Input Schema
```json
{
  "visual_type": "string (TABLE/FLOWCHART/DECISION_TREE/TIMELINE/HIERARCHY/SPECTRUM/KEY_DIFFERENTIATORS)",
  "content_data": {
    "item_count": "number (nodes, rows, steps, etc.)",
    "level_count": "number (hierarchy depth, decision levels)",
    "has_substeps": "boolean",
    "is_comparison": "boolean",
    "is_sequential": "boolean"
  },
  "domain_config": "reference to config/theater.yaml"
}
```

## Output Schema
```json
{
  "recommended_layout": "string (A/B/C/D/E)",
  "reasoning": "string (explanation for selection)",
  "fallback_layout": "string (alternative if primary not suitable)",
  "constraints": {
    "max_items": "number",
    "min_items": "number",
    "requires_substeps": "boolean"
  }
}
```

---

## Required Skills (Hardcoded)

1. **Content Analysis** - Analyze item count, depth, and structure
2. **Layout Rule Application** - Apply type-specific layout selection rules
3. **Constraint Validation** - Verify content fits selected layout
4. **Fallback Selection** - Choose alternative when primary fails constraints

---

## Layout Selection Rules by Visual Type

### TABLE Layouts
```
Layout A: Standard Comparison
- Columns: 2-4
- Rows: 3-6
- Use: Default comparison table

Layout B: Wide Comparison
- Columns: 2
- Rows: 4-8
- Use: Detailed two-item comparison

Layout C: Category List
- Columns: 3
- Rows: 4-6
- Use: First column is category name

Layout D: Compact Reference
- Columns: 4-6
- Rows: 4-5
- Use: Quick reference, short text

Layout E: Tall Comparison
- Columns: 2
- Rows: 6-10
- Use: Extensive side-by-side

Selection Logic:
IF columns == 2 AND rows >= 6: Layout E
IF columns >= 5 OR dense_text: Layout D
IF first_column_is_category: Layout C
IF columns == 2: Layout B
ELSE: Layout A
```

### FLOWCHART Layouts
```
Layout A: Linear Horizontal
- Steps: 3-4
- Use: Simple sequential process

Layout B: Linear Vertical
- Steps: 4-6
- Use: More steps, vertical space

Layout C: Horizontal with Substeps
- Steps: 3-4 main + substeps
- Use: Main steps have sub-components

Layout D: Snake/Zigzag
- Steps: 5-7
- Use: Many steps, space efficiency

Layout E: Branching Linear
- Steps: 4-6 with optional paths
- Use: Parallel alternatives mid-process

Selection Logic:
IF has_substeps: Layout C
IF steps >= 5 AND steps <= 7: Layout D
IF has_branch_points: Layout E
IF steps >= 4: Layout B
ELSE: Layout A
```

### DECISION_TREE Layouts
```
Layout A: Three-Level Binary (1->2->4)
- Outcomes: 4
- Levels: 3
- Use: Symmetric binary branching

Layout B: Two-Level Binary (1->2)
- Outcomes: 2
- Levels: 2
- Use: Simple binary distinction

Layout C: Two-Level Triple (1->3)
- Outcomes: 3
- Levels: 2
- Use: Three distinct categories

Layout D: Three-Level Asymmetric
- Outcomes: 3-4
- Levels: 3 (uneven branches)
- Use: One path needs further differentiation

Layout E: Three-Level Extended (1->2->6)
- Outcomes: 6
- Levels: 3
- Use: Each secondary has 3 outcomes

Layout F: Complex (1->2->4->8)
- Outcomes: 8
- Levels: 4
- Use: Deep binary tree (max complexity)

Selection Logic:
IF outcomes <= 2: Layout B
IF outcomes == 3 AND symmetric: Layout C
IF outcomes == 4 AND symmetric: Layout A
IF outcomes <= 4 AND asymmetric: Layout D
IF outcomes == 6: Layout E
IF outcomes > 6: Layout F (or split)
```

### TIMELINE Layouts
```
Layout A: Horizontal Timeline
- Events: 3-5
- Use: Standard horizontal sequence

Layout B: Vertical Timeline
- Events: 4-7
- Use: More events, vertical flow

Layout C: Horizontal with Era Blocks
- Eras: 3-4
- Use: Grouped time periods

Layout D: Developmental Stages
- Stages: 4-6
- Use: Age-based development

Layout E: Milestone Timeline
- Milestones: 5-8
- Use: Key dates with descriptions

Selection Logic:
IF has_age_ranges: Layout D
IF events_grouped_by_era: Layout C
IF events >= 5: Layout E
IF events >= 4: Layout B
ELSE: Layout A
```

### HIERARCHY Layouts
```
Layout A: Top-Down (1-2-4)
- Levels: 3
- Structure: Binary branching
- Use: Standard taxonomy

Layout B: Top-Down (1-3-6)
- Levels: 3
- Structure: Triple branching
- Use: Three main categories

Layout C: Organizational Chart
- Levels: 2-3
- Structure: Mixed branches
- Use: Uneven branching

Layout D: Inverted Pyramid
- Levels: 3-4
- Structure: Narrowing levels
- Use: Broad to specific

Layout E: Side-by-Side Hierarchies
- Trees: 2 parallel
- Use: Comparing structures

Selection Logic:
IF comparing_two_hierarchies: Layout E
IF narrowing_focus: Layout D
IF uneven_branches: Layout C
IF triple_branches: Layout B
ELSE: Layout A
```

### SPECTRUM Layouts
```
Layout A: Horizontal Bar Spectrum
- Segments: 3-5
- Use: Standard gradient bar

Layout B: Vertical Bar Spectrum
- Segments: 4-7
- Use: Vertical orientation

Layout C: Bipolar Spectrum with Center
- Segments: 3-5
- Center: Emphasized
- Use: Opposite poles with neutral

Layout D: Segmented Spectrum
- Segments: 3-6
- Use: Discrete levels on continuum

Layout E: Dual-Axis Spectrum
- Axes: 2
- Quadrants: 4
- Use: Two dimensions

Selection Logic:
IF two_dimensions: Layout E
IF bipolar_with_neutral: Layout C
IF discrete_segments: Layout D
IF many_segments: Layout B
ELSE: Layout A
```

### KEY_DIFFERENTIATORS Layouts
```
Layout A: Side-by-Side Comparison
- Concepts: 2
- Features: 3-5
- Use: Standard VS comparison

Layout B: Centered Key Differentiator
- Concepts: 2
- Key Diffs: 1
- Use: Single critical distinction

Layout C: Multiple Differentiators
- Concepts: 2
- Key Diffs: 2-4
- Use: Several key differences

Layout D: Three-Way Discrimination
- Concepts: 3
- Use: Triangle arrangement

Layout E: Feature Matrix
- Concepts: 2-4
- Features: 4-6
- Use: Matrix comparison

Selection Logic:
IF concepts == 3: Layout D
IF concepts >= 3 OR features >= 5: Layout E
IF key_diffs >= 2: Layout C
IF key_diffs == 1 AND emphasis_needed: Layout B
ELSE: Layout A
```

---

## Step-by-Step Layout Selection Algorithm

```python
def select_layout(visual_type, content_data):
    """Select optimal layout based on visual type and content."""

    item_count = content_data.get('item_count', 0)
    level_count = content_data.get('level_count', 1)
    has_substeps = content_data.get('has_substeps', False)
    is_comparison = content_data.get('is_comparison', False)

    if visual_type == 'TABLE':
        return select_table_layout(content_data)
    elif visual_type == 'FLOWCHART':
        return select_flowchart_layout(content_data)
    elif visual_type == 'DECISION_TREE':
        return select_decision_tree_layout(content_data)
    elif visual_type == 'TIMELINE':
        return select_timeline_layout(content_data)
    elif visual_type == 'HIERARCHY':
        return select_hierarchy_layout(content_data)
    elif visual_type == 'SPECTRUM':
        return select_spectrum_layout(content_data)
    elif visual_type == 'KEY_DIFFERENTIATORS':
        return select_key_diff_layout(content_data)
    else:
        return {'layout': 'A', 'reasoning': 'Default fallback'}

def select_table_layout(data):
    """Select table layout based on dimensions."""
    rows = data.get('rows', 4)
    cols = data.get('columns', 3)

    if cols == 2 and rows >= 6:
        return {'layout': 'E', 'reasoning': 'Tall two-column comparison'}
    elif cols >= 5:
        return {'layout': 'D', 'reasoning': 'Compact reference for many columns'}
    elif cols == 2:
        return {'layout': 'B', 'reasoning': 'Wide two-column comparison'}
    else:
        return {'layout': 'A', 'reasoning': 'Standard comparison table'}

def select_flowchart_layout(data):
    """Select flowchart layout based on step count and structure."""
    steps = data.get('item_count', 3)
    has_substeps = data.get('has_substeps', False)
    has_branches = data.get('has_branches', False)

    if has_substeps:
        return {'layout': 'C', 'reasoning': 'Main steps with substeps'}
    elif has_branches:
        return {'layout': 'E', 'reasoning': 'Branching linear process'}
    elif steps >= 5:
        return {'layout': 'D', 'reasoning': 'Snake layout for many steps'}
    elif steps >= 4:
        return {'layout': 'B', 'reasoning': 'Vertical linear for 4+ steps'}
    else:
        return {'layout': 'A', 'reasoning': 'Horizontal linear for 3-4 steps'}

def select_decision_tree_layout(data):
    """Select decision tree layout based on outcomes and levels."""
    outcomes = data.get('item_count', 4)
    is_symmetric = data.get('is_symmetric', True)

    if outcomes <= 2:
        return {'layout': 'B', 'reasoning': 'Simple binary distinction'}
    elif outcomes == 3 and is_symmetric:
        return {'layout': 'C', 'reasoning': 'Three distinct categories'}
    elif outcomes == 4 and is_symmetric:
        return {'layout': 'A', 'reasoning': 'Symmetric four outcomes'}
    elif outcomes <= 4:
        return {'layout': 'D', 'reasoning': 'Asymmetric branching'}
    elif outcomes == 6:
        return {'layout': 'E', 'reasoning': 'Extended three-level tree'}
    else:
        return {'layout': 'F', 'reasoning': 'Complex deep tree'}
```

---

## Validation Requirements

Before finalizing layout selection:
- [ ] Item count within layout capacity
- [ ] Text fits character limits for layout
- [ ] Visual complexity appropriate for slide
- [ ] Layout supports required structure (branches, substeps, etc.)

---

## Error Handling

| Error | Action |
|-------|--------|
| Content exceeds all layouts | Split across multiple slides |
| Content too sparse | Use simpler layout or combine items |
| Structure not supported | Recommend different visual type |
| AUTO selection fails | Fall back to Layout A |

---

## Integration Notes

This agent is called by all visual generator agents when:
1. Blueprint specifies `Layout: AUTO`
2. Layout not explicitly specified
3. Validation of explicit layout fails

The layout selector returns both primary and fallback recommendations to ensure visual generation always succeeds.

---

**Agent Version:** 2.0 (Theater Adaptation)
**Last Updated:** 2026-01-08

### Version History
- **v2.0** (2026-01-08): Adapted for theater pipeline - config/nclex.yaml -> config/theater.yaml
- **v1.0** (2026-01-04): Initial layout selector agent
