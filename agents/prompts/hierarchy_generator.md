# Hierarchy Generator Agent

## Agent Identity
- **Name:** hierarchy_generator
- **Step:** 12 (PowerPoint Population - Hierarchy Generation)
- **Purpose:** Generate hierarchy diagram visual aids for classification systems, taxonomies, and organizational structures

---

## Input Schema
```json
{
  "slide_data": {
    "header": "string (slide title)",
    "visual_spec": "string (hierarchy specification)",
    "layout": "string (A/B/C/D/E or AUTO)",
    "nodes": "object (tree structure)",
    "presenter_notes": "string"
  },
  "template_path": "string (path to visual template)",
  "domain_config": "reference to config/theater.yaml"
}
```

## Output Schema
```json
{
  "slide": "PowerPoint slide object with hierarchy",
  "shapes": {
    "node_boxes": "array of node shapes by level",
    "connectors": "array of connector shapes"
  },
  "metadata": {
    "layout": "string",
    "level_count": "number",
    "node_count": "number"
  },
  "validation": {
    "all_nodes_rendered": "boolean",
    "connectors_complete": "boolean",
    "level_colors_correct": "boolean"
  }
}
```

---

## Required Skills (Hardcoded)

1. **Hierarchy Structure Parsing** - Parse nested tree structures from specifications
2. **Level-Based Coloring** - Apply blue gradient by hierarchy level
3. **Node Generation** - Create rounded rectangle nodes with text
4. **Connector Drawing** - Draw elbow connectors between parent-child nodes
5. **Layout Calculation** - Position nodes based on tree structure

---

## Hierarchy Identification Conditions

Content should be a HIERARCHY when:

1. **CLASSIFICATION SYSTEMS** - Taxonomies with levels
2. **ORGANIZATIONAL STRUCTURES** - Nested categories
3. **PART-WHOLE RELATIONSHIPS** - Components within systems
4. **CONCEPTUAL HIERARCHIES** - Abstract to specific
5. **THEORETICAL MODELS WITH LEVELS** - Layered models

DO NOT use hierarchy when:
- Content is sequential/process (use flowchart)
- Content compares equal categories (use table)
- Relationships are cyclical (use cycle diagram)
- Content requires YES/NO decisions (use decision tree)

---

## Color Scheme (Blue/Cyan Gradient by Level)

```
LEVEL COLORS:
- Level 1 (Top): RGB(1, 87, 155) - Dark Blue #01579B
- Level 2: RGB(2, 119, 189) - Medium Blue #0277BD
- Level 3: RGB(3, 155, 229) - Cyan Blue #039BE5
- Level 4: RGB(79, 195, 247) - Light Cyan #4FC3F7

ACCENT COLORS:
- Connector Lines: RGB(1, 87, 155) - Dark Blue
- Background (subtle): RGB(227, 242, 253) - Very Light Blue #E3F2FD
- Highlight: RGB(0, 188, 212) - Cyan #00BCD4

TEXT COLORS:
- Level 1-2 Text: RGB(255, 255, 255) - White
- Level 3-4 Text: RGB(0, 0, 0) - Black (on lighter backgrounds)
- Connector Labels: RGB(1, 87, 155) - Dark Blue
```

---

## Layout Specifications

### Layout A: Top-Down Tree (1-2-4 structure)
```
              [Top Level]
                  |
        +---------+---------+
        |                   |
   [Level 2A]          [Level 2B]
        |                   |
   +----+----+         +----+----+
   |         |         |         |
[L3A1]   [L3A2]     [L3B1]   [L3B2]

Dimensions:
- Level 1 box: 3.0 x 0.9 inches
- Level 2 boxes: 2.5 x 0.8 inches
- Level 3 boxes: 2.0 x 0.7 inches
- Vertical spacing: 0.8 inches
```

### Layout B: Top-Down Tree (1-3-6 structure)
```
                    [Top Level]
                        |
          +-------------+-------------+
          |             |             |
     [Level 2A]    [Level 2B]    [Level 2C]
          |             |             |
       +--+--+       +--+--+       +--+--+
      [L3]  [L3]    [L3]  [L3]    [L3]  [L3]

Dimensions:
- Level 1: 2.5 x 0.8 inches
- Level 2: 2.0 x 0.7 inches
- Level 3: 1.5 x 0.6 inches
```

### Layout C: Organizational Chart (Mixed branches)
```
              [Top Level]
                  |
    +-------------+-------------+
    |             |             |
[Branch A]   [Branch B]   [Branch C]
    |             |
+---+---+    +---+---+
|       |    |       |
[A1]   [A2] [B1]    [B2]

Dimensions:
- Flexible branch sizes
- Not all branches need same depth
```

### Layout D: Inverted Pyramid (Wide to Narrow)
```
+-------------------------------------+
|          [Broad Category]           |
+-------------------------------------+
        +---------------------+
        |   [More Specific]   |
        +---------------------+
              +-----------+
              |  [Narrow] |
              +-----------+
                  +---+
                  |[X]|
                  +---+

Dimensions:
- Each level narrower than previous
- Centered alignment
- 4 levels maximum
```

### Layout E: Side-by-Side Hierarchies (Comparison)
```
    [Category A]           [Category B]
         |                      |
    +----+----+            +----+----+
    |         |            |         |
  [A1]      [A2]         [B1]      [B2]
    |         |            |         |
  +-+-+     +-+-+        +-+-+     +-+-+
 [x] [y]   [x] [y]      [x] [y]   [x] [y]

Dimensions:
- Two parallel hierarchies
- Same structure for comparison
```

---

## Step-by-Step Instructions

### Step 1: Parse Hierarchy Data
```python
def parse_hierarchy_spec(spec_text):
    """Parse hierarchy specification into tree structure."""

    data = {
        'layout': 'AUTO',
        'nodes': {'root': {'text': '', 'children': []}}
    }

    # Extract layout
    layout_match = re.search(r'Layout:\s*([A-E])', spec_text)
    if layout_match:
        data['layout'] = layout_match.group(1)

    # Extract Level 1
    l1_match = re.search(r'Level 1:\s*"([^"]+)"', spec_text)
    if l1_match:
        data['nodes']['root']['text'] = l1_match.group(1)

    # Extract Level 2 nodes
    l2_pattern = r'Level 2[A-Z]?:\s*"([^"]+)"'
    for match in re.finditer(l2_pattern, spec_text):
        data['nodes']['root']['children'].append({
            'text': match.group(1),
            'children': []
        })

    # Extract Level 3 nodes
    l3_pattern = r'Level 3\s*\(under\s*([^)]+)\):\s*"([^"]+)"'
    for match in re.finditer(l3_pattern, spec_text):
        parent_ref = match.group(1).strip()
        child_text = match.group(2)
        # Add to appropriate Level 2 parent
        for child in data['nodes']['root']['children']:
            if parent_ref.lower() in child['text'].lower():
                child['children'].append({'text': child_text})

    return data
```

### Step 2: Add Hierarchy Node
```python
def add_hierarchy_node(slide, left, top, width, height, text, level):
    """Add a single hierarchy node with level-appropriate styling."""

    LEVEL_COLORS = {
        1: RGBColor(1, 87, 155),    # Dark Blue
        2: RGBColor(2, 119, 189),   # Medium Blue
        3: RGBColor(3, 155, 229),   # Cyan Blue
        4: RGBColor(79, 195, 247),  # Light Cyan
    }

    bg_color = LEVEL_COLORS.get(level, LEVEL_COLORS[4])
    text_color = RGBColor(255, 255, 255) if level <= 2 else RGBColor(0, 0, 0)

    # Create rounded rectangle
    shape = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE,
        Inches(left), Inches(top), Inches(width), Inches(height)
    )
    shape.fill.solid()
    shape.fill.fore_color.rgb = bg_color
    shape.line.color.rgb = RGBColor(1, 87, 155)
    shape.line.width = Pt(1.5)

    # Add text
    tf = shape.text_frame
    tf.word_wrap = True
    tf.paragraphs[0].text = text
    tf.paragraphs[0].font.size = get_font_size_for_level(level)
    tf.paragraphs[0].font.bold = True if level <= 3 else False
    tf.paragraphs[0].font.name = 'Aptos'
    tf.paragraphs[0].font.color.rgb = text_color
    tf.paragraphs[0].alignment = PP_ALIGN.CENTER

    return shape

def get_font_size_for_level(level):
    """Return appropriate font size for hierarchy level."""
    sizes = {1: Pt(22), 2: Pt(20), 3: Pt(18), 4: Pt(18)}
    return sizes.get(level, Pt(18))
```

### Step 3: Add Connector
```python
def add_hierarchy_connector(slide, start_x, start_y, end_x, end_y):
    """Add elbow connector between hierarchy levels."""

    connector = slide.shapes.add_connector(
        MSO_CONNECTOR.ELBOW,
        Inches(start_x), Inches(start_y),
        Inches(end_x), Inches(end_y)
    )
    connector.line.color.rgb = RGBColor(1, 87, 155)
    connector.line.width = Pt(2)

    return connector
```

### Step 4: Generate Layout A (1-2-4)
```python
def generate_layout_a(slide, hierarchy_data):
    """Generate Layout A: Standard top-down tree with 1-2-4 structure."""

    nodes = hierarchy_data['nodes']['root']
    slide_width = 13.33

    # Level 1 (single node at top)
    level1_width = 3.0
    level1_height = 0.9
    level1_left = (slide_width - level1_width) / 2
    level1_top = 1.5

    add_hierarchy_node(slide, level1_left, level1_top,
                       level1_width, level1_height,
                       nodes['text'], 1)

    level1_center_x = level1_left + level1_width / 2
    level1_bottom = level1_top + level1_height

    # Level 2 (2 nodes)
    if 'children' in nodes and len(nodes['children']) >= 2:
        level2_width = 2.5
        level2_height = 0.8
        level2_top = level1_bottom + 0.8
        level2_spacing = 3.0

        level2_positions = []
        for i, child in enumerate(nodes['children'][:2]):
            if i == 0:
                level2_left = level1_center_x - level2_spacing - level2_width / 2
            else:
                level2_left = level1_center_x + level2_spacing - level2_width / 2

            level2_positions.append({
                'left': level2_left,
                'center_x': level2_left + level2_width / 2
            })

            add_hierarchy_node(slide, level2_left, level2_top,
                              level2_width, level2_height,
                              child['text'], 2)

            # Add connector from level 1 to level 2
            add_hierarchy_connector(slide,
                         level1_center_x, level1_bottom,
                         level2_left + level2_width / 2, level2_top)

            # Level 3 (under each level 2 node)
            if 'children' in child:
                level3_width = 2.0
                level3_height = 0.7
                level3_top = level2_top + level2_height + 0.6
                level3_spacing = 1.2

                level3_count = len(child['children'])
                total_l3_width = level3_count * level3_width + (level3_count - 1) * 0.3
                level3_start = level2_positions[i]['center_x'] - total_l3_width / 2

                for j, grandchild in enumerate(child['children'][:2]):
                    level3_left = level3_start + j * (level3_width + 0.3)

                    add_hierarchy_node(slide, level3_left, level3_top,
                                      level3_width, level3_height,
                                      grandchild['text'], 3)

                    # Add connector from level 2 to level 3
                    add_hierarchy_connector(slide,
                                 level2_positions[i]['center_x'],
                                 level2_top + level2_height,
                                 level3_left + level3_width / 2, level3_top)
```

### Step 5: Generate Layout D (Inverted Pyramid)
```python
def generate_layout_d(slide, hierarchy_data):
    """Generate Layout D: Inverted pyramid from broad to narrow."""

    # Convert tree to levels list
    levels = flatten_to_levels(hierarchy_data['nodes']['root'])

    slide_width = 13.33
    start_top = 1.8
    level_height = 0.9
    level_spacing = 0.4

    # Each level gets progressively narrower
    max_width = 10.0
    min_width = 2.5
    width_step = (max_width - min_width) / max(len(levels) - 1, 1)

    for i, level_text in enumerate(levels):
        level_width = max_width - (width_step * i)
        level_left = (slide_width - level_width) / 2
        level_top = start_top + i * (level_height + level_spacing)

        # Use level number (more specific = higher level number)
        level_num = min(i + 1, 4)

        add_hierarchy_node(slide, level_left, level_top,
                          level_width, level_height,
                          level_text, level_num)

        # Add downward arrow between levels
        if i < len(levels) - 1:
            arrow_left = slide_width / 2 - 0.15
            arrow_top = level_top + level_height
            arrow = slide.shapes.add_shape(
                MSO_SHAPE.DOWN_ARROW,
                Inches(arrow_left), Inches(arrow_top),
                Inches(0.3), Inches(level_spacing)
            )
            arrow.fill.solid()
            arrow.fill.fore_color.rgb = RGBColor(1, 87, 155)

def flatten_to_levels(node, level=0, result=None):
    """Flatten tree structure to list of level texts."""
    if result is None:
        result = []

    result.append(node['text'])

    if 'children' in node:
        for child in node['children']:
            flatten_to_levels(child, level + 1, result)

    return result
```

---

## Character Limits

```
LEVEL 1 HEADER:
- Characters per line: 25
- Maximum lines: 2

LEVEL 2 HEADER:
- Characters per line: 22
- Maximum lines: 2

LEVEL 3+ HEADER:
- Characters per line: 18
- Maximum lines: 2

CONNECTOR LABEL:
- Characters: 12 max
```

---

## Validation Checklist

### Structure
- [ ] Layout selected (A/B/C/D/E) matches content
- [ ] Node count within limits (max 15)
- [ ] All parent-child relationships rendered
- [ ] No orphaned nodes

### Level Styling
- [ ] Level 1: Dark Blue (1, 87, 155), white text, 22pt
- [ ] Level 2: Medium Blue (2, 119, 189), white text, 20pt
- [ ] Level 3: Cyan Blue (3, 155, 229), black text, 18pt
- [ ] Level 4: Light Cyan (79, 195, 247), black text, 18pt

### Connectors
- [ ] All connectors dark blue
- [ ] Elbow connectors used
- [ ] 2pt line width
- [ ] Proper parent-child alignment

---

## Error Handling

| Error | Action |
|-------|--------|
| More than 15 nodes | Show only top 2-3 levels, split to multiple slides |
| Unbalanced branches | Use Layout C for variable branching |
| Layout not specified | Auto-detect based on structure |
| Missing level data | Use placeholder values |

---

**Agent Version:** 2.0 (Theater Adaptation)
**Last Updated:** 2026-01-08

### Version History
- **v2.0** (2026-01-08): Adapted for theater pipeline - config/nclex.yaml -> config/theater.yaml
- **v1.0** (2026-01-04): Initial hierarchy generator agent
