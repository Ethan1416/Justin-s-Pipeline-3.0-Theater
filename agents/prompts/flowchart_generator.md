# Flowchart Generator Agent

## Agent Identity
- **Name:** flowchart_generator
- **Step:** 12 (PowerPoint Population - Flowchart Generation)
- **Purpose:** Generate flowchart visual aids for sequential processes, procedures, and step-by-step pathways

---

## Input Schema
```json
{
  "slide_data": {
    "header": "string (slide title)",
    "visual_spec": "string (flowchart specification)",
    "layout": "string (A/B/C/D/E)",
    "start_label": "string",
    "end_label": "string",
    "steps": "array of step objects",
    "presenter_notes": "string"
  },
  "template_path": "string (path to visual template)",
  "domain_config": "reference to config/theater.yaml"
}
```

## Output Schema
```json
{
  "slide": "PowerPoint slide object with flowchart",
  "shapes": {
    "start_node": "shape object",
    "end_node": "shape object",
    "step_boxes": "array of shape objects",
    "connectors": "array of connector objects"
  },
  "metadata": {
    "step_count": "number",
    "layout": "string"
  },
  "validation": {
    "all_steps_rendered": "boolean",
    "connectors_aligned": "boolean",
    "fonts_compliant": "boolean"
  }
}
```

---

## Required Skills (Hardcoded)

1. **Flowchart Structure Parsing** - Parse step sequences from specifications
2. **Shape Generation** - Create PowerPoint shapes for nodes and boxes
3. **Connector Rendering** - Draw arrows between sequential elements
4. **Layout Calculation** - Position elements based on layout type
5. **Style Application** - Apply teal/green color scheme

---

## Flowchart Identification Conditions

Content should be a FLOWCHART when:

1. **SEQUENTIAL STEPS** - Process with ordered stages
   - Keywords: "first... then... next... finally", "step 1, step 2"

2. **PROCEDURAL CONTENT** - How-to processes or protocols
   - Keywords: "procedure", "protocol", "process", "method"

3. **SINGLE-DIRECTION PATHWAYS** - Linear progressions without branching
   - Keywords: "leads to", "results in", "progresses to"

4. **CAUSAL CHAINS** - Cause-effect sequences
   - Keywords: "causes", "triggers", "produces", "activates"

DO NOT use flowchart when:
- Content requires YES/NO decisions (use decision tree)
- Content is cyclical/repeating (use cycle diagram)
- Content compares categories (use table)
- Content shows parallel processes (use hierarchy)

---

## Color Scheme (Teal/Green Theme)

```
PRIMARY COLORS:
- Step Header Background: RGB(0, 102, 102) - Dark Teal #006666
- Step Header Text: RGB(255, 255, 255) - White
- Step Body Background: RGB(224, 242, 241) - Light Teal #E0F2F1
- Step Body Text: RGB(0, 0, 0) - Black

ACCENT COLORS:
- Start Node: RGB(46, 125, 50) - Green #2E7D32
- End Node: RGB(0, 77, 64) - Dark Green #004D40
- Connector Lines: RGB(0, 102, 102) - Dark Teal
- Arrow Heads: RGB(0, 102, 102) - Dark Teal

HIGHLIGHT COLORS (for emphasis):
- Critical Step: RGB(255, 152, 0) - Orange #FF9800
- Warning Step: RGB(211, 47, 47) - Red #D32F2F
```

---

## Layout Specifications

### Layout A: Linear Horizontal (3-4 steps)
```
[START] --> [Step 1] --> [Step 2] --> [Step 3] --> [END]

Dimensions:
- Step box width: 2.0 inches
- Step box height: 1.2 inches
- Horizontal spacing: 0.5 inches
- Total width: ~11.5 inches
```

### Layout B: Linear Vertical (4-6 steps)
```
[START]
   |
[Step 1]
   |
[Step 2]
   |
[Step 3]
   |
[Step 4]
   |
[END]

Dimensions:
- Step box width: 4.0 inches
- Step box height: 0.8 inches
- Vertical spacing: 0.3 inches
- Centered horizontally
```

### Layout C: Horizontal with Substeps (3-4 main + substeps)
```
[START] --> [Step 1] --> [Step 2] --> [Step 3] --> [END]
                |            |
            [1a][1b]      [2a][2b]

Dimensions:
- Main step box: 2.0 x 1.0 inches
- Substep box: 0.9 x 0.6 inches
```

### Layout D: Snake/Zigzag (5-7 steps)
```
[START] --> [Step 1] --> [Step 2] --> [Step 3]
                                          |
         [END] <-- [Step 6] <-- [Step 5] <-- [Step 4]

Dimensions:
- Step box: 1.8 x 0.9 inches
- Two rows, alternating direction
```

### Layout E: Branching Linear (4-6 steps with optional paths)
```
                    /--> [Option A] --\
[START] --> [Step 1]                   --> [Step 3] --> [END]
                    \--> [Option B] --/

Dimensions:
- Main step box: 1.8 x 1.0 inches
- Branch boxes: 1.5 x 0.8 inches
```

---

## Step-by-Step Instructions

### Step 1: Parse Flowchart Data
```python
def parse_flowchart_spec(spec_text):
    """Parse flowchart specification into structured data."""

    data = {
        'start_label': 'START',
        'end_label': 'END',
        'steps': [],
        'substeps': {}
    }

    # Extract START label
    start_match = re.search(r'START:\s*"?([^"\n]+)"?', spec_text)
    if start_match:
        data['start_label'] = start_match.group(1).strip()

    # Extract END label
    end_match = re.search(r'END:\s*"?([^"\n]+)"?', spec_text)
    if end_match:
        data['end_label'] = end_match.group(1).strip()

    # Extract steps
    step_pattern = r'(\d+)\.\s*Header:\s*"([^"]+)"\s*\n\s*Body:\s*"([^"]+)"'
    for match in re.finditer(step_pattern, spec_text):
        data['steps'].append({
            'number': int(match.group(1)),
            'header': match.group(2),
            'body': match.group(3)
        })

    return data
```

### Step 2: Add Step Box
```python
def add_step_box(slide, left, top, width, height, header, body):
    """Add a single step box with header and body."""

    # Header portion (top third)
    header_height = height * 0.35
    header_shape = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE,
        left, top, width, header_height
    )
    header_shape.fill.solid()
    header_shape.fill.fore_color.rgb = RGBColor(0, 102, 102)  # Dark Teal

    tf = header_shape.text_frame
    tf.paragraphs[0].text = header
    tf.paragraphs[0].font.size = Pt(20)
    tf.paragraphs[0].font.bold = True
    tf.paragraphs[0].font.color.rgb = RGBColor(255, 255, 255)
    tf.paragraphs[0].alignment = PP_ALIGN.CENTER

    # Body portion (bottom two-thirds)
    body_top = top + header_height
    body_height = height - header_height
    body_shape = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE,
        left, body_top, width, body_height
    )
    body_shape.fill.solid()
    body_shape.fill.fore_color.rgb = RGBColor(224, 242, 241)  # Light Teal

    tf = body_shape.text_frame
    tf.paragraphs[0].text = body
    tf.paragraphs[0].font.size = Pt(18)
    tf.paragraphs[0].font.color.rgb = RGBColor(0, 0, 0)
    tf.paragraphs[0].alignment = PP_ALIGN.CENTER

    return header_shape, body_shape
```

### Step 3: Add Start/End Nodes
```python
def add_start_end_node(slide, left, top, width, height, text, is_start=True):
    """Add START or END oval node."""

    shape = slide.shapes.add_shape(
        MSO_SHAPE.OVAL,
        left, top, width, height
    )

    color = RGBColor(46, 125, 50) if is_start else RGBColor(0, 77, 64)
    shape.fill.solid()
    shape.fill.fore_color.rgb = color

    tf = shape.text_frame
    tf.paragraphs[0].text = text
    tf.paragraphs[0].font.size = Pt(18)
    tf.paragraphs[0].font.bold = True
    tf.paragraphs[0].font.color.rgb = RGBColor(255, 255, 255)
    tf.paragraphs[0].alignment = PP_ALIGN.CENTER

    return shape
```

### Step 4: Add Arrow Connectors
```python
def add_arrow_connector(slide, start_x, start_y, end_x, end_y):
    """Add arrow connector between shapes."""

    connector = slide.shapes.add_connector(
        MSO_CONNECTOR.STRAIGHT,
        Inches(start_x), Inches(start_y),
        Inches(end_x), Inches(end_y)
    )
    connector.line.color.rgb = RGBColor(0, 102, 102)
    connector.line.width = Pt(2)

    # Add arrowhead
    ln = connector._element.spPr.ln
    tailEnd = etree.SubElement(ln, qn('a:tailEnd'))
    tailEnd.set('type', 'triangle')
    tailEnd.set('w', 'med')
    tailEnd.set('len', 'med')

    return connector
```

### Step 5: Generate Layout
```python
def create_horizontal_linear(slide, data):
    """Layout A: Linear Horizontal (3-4 steps)."""

    steps = data['steps']
    step_count = len(steps)

    # Dimensions
    step_width = Inches(2.0)
    step_height = Inches(1.2)
    node_width = Inches(1.0)
    node_height = Inches(0.8)
    spacing = Inches(0.4)

    # Calculate starting position
    total_width = (node_width * 2 + step_width * step_count +
                   spacing * (step_count + 1))
    start_left = (Inches(13.33) - total_width) / 2

    top = Inches(2.5)
    current_left = start_left

    # Add START node
    add_start_end_node(slide, current_left, top,
                       node_width, node_height,
                       data['start_label'], True)
    current_left += node_width + spacing

    # Add each step with arrows
    for step in steps:
        add_step_box(slide, current_left, top - Inches(0.2),
                    step_width, step_height,
                    step['header'], step['body'])
        current_left += step_width + spacing

    # Add END node
    add_start_end_node(slide, current_left, top,
                       node_width, node_height,
                       data['end_label'], False)

def create_vertical_linear(slide, data):
    """Layout B: Linear Vertical (4-6 steps)."""

    steps = data['steps']
    step_width = Inches(4.0)
    step_height = Inches(0.8)
    node_width = Inches(1.5)
    node_height = Inches(0.6)
    spacing = Inches(0.3)

    center_left = (Inches(13.33) - step_width) / 2
    node_left = (Inches(13.33) - node_width) / 2

    current_top = Inches(1.5)

    # START node
    add_start_end_node(slide, node_left, current_top,
                       node_width, node_height,
                       data['start_label'], True)
    current_top += node_height + spacing

    # Each step
    for step in steps:
        current_top += Inches(0.2)  # Arrow space
        add_step_box(slide, center_left, current_top,
                    step_width, step_height,
                    step['header'], step['body'])
        current_top += step_height + spacing

    # END node
    add_start_end_node(slide, node_left, current_top,
                       node_width, node_height,
                       data['end_label'], False)
```

---

## Font Specifications

```
STEP HEADER:
- Font: Aptos
- Size: 20pt (scale to 18pt if needed)
- Color: White on dark background
- Style: Bold

STEP BODY:
- Font: Aptos
- Size: 18pt minimum
- Color: Black on light background
- Style: Regular

START/END NODES:
- Font: Aptos
- Size: 18pt
- Color: White
- Style: Bold
```

---

## Character Limits

```
STEP HEADER: 20 chars, 1 line
STEP BODY: 25 chars per line, 2 lines max
START/END NODE: 12 chars max
CONNECTOR LABEL: 15 chars max
```

---

## Validation Checklist

### Before Population
- [ ] Step count matches layout (A: 3-4, B: 4-6, C: 3-4+subs, D: 5-7, E: 4-6)
- [ ] Each step has header and body text
- [ ] All text within character limits
- [ ] Start and end labels defined
- [ ] Process is truly sequential

### After Population
- [ ] All step boxes visible and not overlapping
- [ ] All text readable (minimum 18pt)
- [ ] Arrow connectors properly aligned
- [ ] START node at beginning, END node at end
- [ ] Colors match teal theme

---

## Common Issues and Fixes

| Issue | Fix |
|-------|-----|
| Too many steps | Combine steps or use Layout D snake |
| Steps overlap | Scale down box widths, validate positions |
| Text truncated | Enable word_wrap, reduce font to 18pt |
| Arrows misaligned | Calculate from shape centers |
| Wrong layout | Re-evaluate content, select appropriate layout |

---

## Error Handling

| Error | Action |
|-------|--------|
| No steps in specification | HALT, request valid specification |
| Step count exceeds layout | Split into multiple slides or combine steps |
| Missing start/end labels | Use defaults "START" and "END" |
| Layout not specified | Auto-detect based on step count |

---

## Quality Gates

Before completing flowchart generation:
- [ ] All steps rendered with correct styling
- [ ] Connectors have visible arrowheads
- [ ] Text is readable on all elements
- [ ] Layout fits within slide boundaries
- [ ] Presenter notes populated
- [ ] Colors match specification

---

**Agent Version:** 2.0 (Theater Adaptation)
**Last Updated:** 2026-01-08

### Version History
- **v2.0** (2026-01-08): Adapted for theater pipeline - config/nclex.yaml -> config/theater.yaml
- **v1.0** (2026-01-04): Initial flowchart generator agent
