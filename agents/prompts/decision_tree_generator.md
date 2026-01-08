# Decision Tree Generator Agent

## Agent Identity
- **Name:** decision_tree_generator
- **Step:** 12 (PowerPoint Population - Decision Tree Generation)
- **Purpose:** Generate decision tree visual aids for diagnostic criteria, if-then logic, and classification systems

---

## Input Schema
```json
{
  "slide_data": {
    "header": "string (slide title)",
    "visual_spec": "string (decision tree specification)",
    "layout": "string (A/B/C/D/E/F or AUTO)",
    "level1": {"header": "string", "question": "string", "paths": ["string"]},
    "level2a": {"header": "string", "question": "string", "paths": ["string"]},
    "level2b": {"header": "string", "question": "string", "paths": ["string"]},
    "outcomes": [{"name": "string", "color": "string"}],
    "presenter_notes": "string"
  },
  "template_path": "string (path to visual template)",
  "domain_config": "reference to config/nclex.yaml"
}
```

## Output Schema
```json
{
  "slide": "PowerPoint slide object with decision tree",
  "shapes": {
    "decision_panels": "array of decision node shapes",
    "outcome_panels": "array of outcome node shapes",
    "connectors": "array of arrow connectors",
    "path_labels": "array of path label shapes"
  },
  "metadata": {
    "layout": "string",
    "outcome_count": "number",
    "level_count": "number"
  },
  "validation": {
    "all_nodes_rendered": "boolean",
    "connectors_complete": "boolean",
    "colors_correct": "boolean"
  }
}
```

---

## Required Skills (Hardcoded)

1. **Tree Structure Parsing** - Parse decision levels and outcomes from specifications
2. **Panel Generation** - Create two-tone rectangular panels for decisions
3. **Outcome Rendering** - Generate color-coded outcome boxes
4. **Connector Drawing** - Draw arrows with proper arrowheads
5. **Path Label Creation** - Add colored path labels on connectors

---

## Decision Tree Identification Conditions

Content should be a DECISION_TREE when:

1. **DIAGNOSTIC CRITERIA DIFFERENTIATION** - Distinguishing similar diagnoses
2. **SEQUENTIAL DECISION PROCESS** - If-then logic paths
3. **CLASSIFICATION SYSTEMS** - Categorizing based on criteria
4. **RULE-OUT PROCESSES** - Eliminating possibilities sequentially

DO NOT use decision tree when:
- Content is purely definitional (use content slide)
- Content is a simple list (use content slide)
- Content compares without classification (use table)
- Content has more than 15 endpoints (use table or split)

---

## Color Scheme

```
DECISION NODES:
- Header Background: RGB(0, 51, 102) - Dark Navy
- Body Background: RGB(240, 244, 248) - Light Gray-Blue
- Border: RGB(0, 51, 102) - Dark Navy
- Header Text: RGB(255, 255, 255) - White
- Body Text: RGB(33, 37, 41) - Dark Gray

OUTCOME NODES:
- Green: RGB(0, 102, 68) - For positive/YES paths
- Red: RGB(153, 0, 0) - For negative/NO paths
- Blue: RGB(0, 71, 133) - For neutral/alternative paths
- Purple: RGB(75, 0, 110) - For additional distinctions

PATH LABELS:
- Use same colors as destination outcomes
- White text on colored background

CONNECTORS:
- Color: RGB(100, 100, 100) - Medium Gray
- Width: 2.5pt
- Arrow head: Triangle, medium size
```

---

## Layout Variations

### Layout A: Three-Level Binary (1 -> 2 -> 4)
```
                [Level 1]
               /         \
        [Level 2A]    [Level 2B]
         /    \        /    \
      [O1]  [O2]    [O3]  [O4]

Nodes: 7 (1 + 2 + 4)
Use: 4 final outcomes with symmetric branching
```

### Layout B: Two-Level Binary (1 -> 2)
```
                [Level 1]
               /         \
            [O1]        [O2]

Nodes: 3 (1 + 2)
Use: Simple binary distinction
```

### Layout C: Two-Level Triple (1 -> 3)
```
                [Level 1]
              /     |     \
           [O1]   [O2]   [O3]

Nodes: 4 (1 + 3)
Use: Three distinct categories
```

### Layout D: Three-Level Asymmetric
```
                [Level 1]
               /         \
        [Level 2A]       [O1]
         /    \
      [O2]   [O3]

Nodes: 5 (1 + 1 + 1 + 2)
Use: One path requires further differentiation
```

### Layout E: Three-Level Extended (1 -> 2 -> 6)
```
                [Level 1]
               /         \
        [Level 2A]    [Level 2B]
        /   |   \      /   |   \
     [O1] [O2] [O3] [O4] [O5] [O6]

Nodes: 9 (1 + 2 + 6)
Use: Each secondary decision has 3 outcomes
```

---

## Step-by-Step Instructions

### Step 1: Parse Decision Tree Data
```python
def parse_decision_tree_spec(spec_text):
    """Parse decision tree specification."""

    data = {
        'layout': 'AUTO',
        'level1': None,
        'level2a': None,
        'level2b': None,
        'outcomes': []
    }

    # Extract layout
    layout_match = re.search(r'Layout:\s*([A-F])', spec_text)
    if layout_match:
        data['layout'] = layout_match.group(1)

    # Extract Level 1
    l1_match = re.search(
        r'LEVEL 1:.*?Header:\s*"([^"]+)".*?Question:\s*"([^"]+)".*?Paths:\s*([^\n]+)',
        spec_text, re.DOTALL
    )
    if l1_match:
        data['level1'] = {
            'header': l1_match.group(1),
            'question': l1_match.group(2),
            'paths': [p.strip() for p in l1_match.group(3).split(',')]
        }

    # Extract outcomes
    outcome_pattern = r'O(\d+):\s*"([^"]+)"\s*\|\s*Color:\s*(\w+)'
    for match in re.finditer(outcome_pattern, spec_text):
        data['outcomes'].append({
            'number': int(match.group(1)),
            'name': match.group(2),
            'color': match.group(3)
        })

    return data
```

### Step 2: Add Decision Panel
```python
def add_decision_panel(slide, left, top, width, height, header_text, body_text):
    """Add professional two-tone decision panel."""

    header_height = Inches(0.45)
    body_height = height - header_height

    # Header bar (dark)
    header = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, left, top, width, header_height
    )
    header.fill.solid()
    header.fill.fore_color.rgb = RGBColor(0, 51, 102)
    header.line.fill.background()

    tf = header.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    run = p.add_run()
    run.text = header_text
    run.font.name = 'Aptos'
    run.font.size = Pt(18)
    run.font.bold = True
    run.font.color.rgb = RGBColor(255, 255, 255)

    # Body area (light)
    body = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, left, top + header_height, width, body_height
    )
    body.fill.solid()
    body.fill.fore_color.rgb = RGBColor(240, 244, 248)
    body.line.color.rgb = RGBColor(0, 51, 102)
    body.line.width = Pt(2)

    tf = body.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    run = p.add_run()
    run.text = body_text
    run.font.name = 'Aptos'
    run.font.size = Pt(22)
    run.font.bold = True
    run.font.color.rgb = RGBColor(33, 37, 41)

    return header, body
```

### Step 3: Add Outcome Panel
```python
def add_outcome_panel(slide, left, top, width, height, header_text, body_text, color_name):
    """Add color-coded outcome panel."""

    color_map = {
        'green': RGBColor(0, 102, 68),
        'red': RGBColor(153, 0, 0),
        'blue': RGBColor(0, 71, 133),
        'purple': RGBColor(75, 0, 110)
    }
    color = color_map.get(color_name.lower(), color_map['blue'])

    header_height = Inches(0.35)
    body_height = height - header_height

    # Header bar
    header = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, left, top, width, header_height
    )
    header.fill.solid()
    header.fill.fore_color.rgb = color
    header.line.fill.background()

    tf = header.text_frame
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    run = p.add_run()
    run.text = header_text
    run.font.name = 'Aptos'
    run.font.size = Pt(18)
    run.font.bold = True
    run.font.color.rgb = RGBColor(255, 255, 255)

    # Body area
    body = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, left, top + header_height, width, body_height
    )
    body.fill.solid()
    body.fill.fore_color.rgb = RGBColor(255, 255, 255)
    body.line.color.rgb = color
    body.line.width = Pt(2.5)

    tf = body.text_frame
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    run = p.add_run()
    run.text = body_text
    run.font.name = 'Aptos'
    run.font.size = Pt(20)
    run.font.bold = True
    run.font.color.rgb = color

    return header, body
```

### Step 4: Add Connectors and Path Labels
```python
def add_arrow_connector(slide, start_x, start_y, end_x, end_y):
    """Add connector with arrow."""

    connector = slide.shapes.add_connector(
        MSO_CONNECTOR.STRAIGHT,
        Inches(start_x), Inches(start_y),
        Inches(end_x), Inches(end_y)
    )
    connector.line.color.rgb = RGBColor(100, 100, 100)
    connector.line.width = Pt(2.5)

    # Add arrowhead
    ln = connector._element.spPr.ln
    tailEnd = etree.SubElement(ln, qn('a:tailEnd'))
    tailEnd.set('type', 'triangle')
    tailEnd.set('w', 'med')
    tailEnd.set('len', 'med')

    return connector

def add_path_label(slide, left, top, text, color_name):
    """Add colored path label."""

    color_map = {
        'green': RGBColor(0, 102, 68),
        'red': RGBColor(153, 0, 0),
        'blue': RGBColor(0, 71, 133),
        'purple': RGBColor(75, 0, 110)
    }
    color = color_map.get(color_name.lower(), color_map['blue'])

    label = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE,
        left, top, Inches(1.5), Inches(0.4)
    )
    label.adjustments[0] = 0.5
    label.fill.solid()
    label.fill.fore_color.rgb = color
    label.line.fill.background()

    tf = label.text_frame
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    run = p.add_run()
    run.text = text
    run.font.name = 'Aptos'
    run.font.size = Pt(18)
    run.font.bold = True
    run.font.color.rgb = RGBColor(255, 255, 255)

    return label
```

### Step 5: Generate Layout A
```python
def generate_layout_a(slide, tree_data):
    """Generate Layout A: Three-Level Binary (1 -> 2 -> 4)."""

    # Coordinates
    L1_X, L1_Y, L1_W, L1_H = 4.4, 0.85, 4.5, 1.3
    L2_Y, L2_W, L2_H = 2.9, 4.5, 1.2
    L2_LEFT_X, L2_RIGHT_X = 1.0, 7.8
    L3_Y, L3_W, L3_H = 5.0, 2.9, 1.0
    L3_POSITIONS = [0.2, 3.4, 6.6, 9.9]

    # Level 1
    l1 = tree_data['level1']
    add_decision_panel(
        slide, Inches(L1_X), Inches(L1_Y), Inches(L1_W), Inches(L1_H),
        l1['header'], l1['question']
    )

    # Level 2A
    l2a = tree_data.get('level2a', {'header': 'CHECK', 'question': '?'})
    add_decision_panel(
        slide, Inches(L2_LEFT_X), Inches(L2_Y), Inches(L2_W), Inches(L2_H),
        l2a['header'], l2a['question']
    )

    # Level 2B
    l2b = tree_data.get('level2b', {'header': 'CHECK', 'question': '?'})
    add_decision_panel(
        slide, Inches(L2_RIGHT_X), Inches(L2_Y), Inches(L2_W), Inches(L2_H),
        l2b['header'], l2b['question']
    )

    # Outcomes
    outcomes = tree_data.get('outcomes', [])
    for i, outcome in enumerate(outcomes[:4]):
        add_outcome_panel(
            slide, Inches(L3_POSITIONS[i]), Inches(L3_Y),
            Inches(L3_W), Inches(L3_H),
            'DIAGNOSIS', outcome['name'], outcome['color']
        )

    # Connectors
    add_arrow_connector(slide, L1_X + 0.8, L1_Y + L1_H, L2_LEFT_X + L2_W/2, L2_Y)
    add_arrow_connector(slide, L1_X + L1_W - 0.8, L1_Y + L1_H, L2_RIGHT_X + L2_W/2, L2_Y)

    # Path labels
    paths = l1.get('paths', ['Left', 'Right'])
    add_path_label(slide, Inches(2.6), Inches(2.35), paths[0], 'red')
    add_path_label(slide, Inches(9.3), Inches(2.35), paths[1], 'green')
```

---

## Character Limits

```
DECISION NODES:
- Header: 20 chars, 1 line
- Body: 25 chars per line, 2 lines max

OUTCOME NODES:
- Header: 20 chars, 1 line
- Body: 20 chars per line, 2 lines max

PATH LABELS:
- Text: 12 chars, 1 line
```

---

## Validation Checklist

### Structure
- [ ] Layout selected (A/B/C/D/E) matches content
- [ ] Node count within limits (max 15)
- [ ] All paths lead to valid outcomes
- [ ] No orphaned nodes

### Decision Panels
- [ ] Header: Navy background, white text, bold
- [ ] Body: Light gray-blue background, dark text
- [ ] Border: 2pt navy

### Outcome Panels
- [ ] Distinct colors used (green, red, blue, purple)
- [ ] Border: 2.5pt matching header color
- [ ] "DIAGNOSIS" or appropriate label in header

### Path Labels
- [ ] 12 chars max
- [ ] Colors match destination outcomes
- [ ] Positioned correctly on connectors

---

## Error Handling

| Error | Action |
|-------|--------|
| More than 15 nodes | Fall back to TABLE format |
| Layout not specified | Auto-detect based on outcome count |
| Missing level data | Use placeholder values |
| Invalid color name | Default to blue |

---

**Agent Version:** 1.0
**Last Updated:** 2026-01-04
