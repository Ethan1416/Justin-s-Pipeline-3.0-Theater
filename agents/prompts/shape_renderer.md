# Shape Renderer Agent

## Agent Identity
- **Name:** shape_renderer
- **Step:** 12 (PowerPoint Population - Shape Rendering)
- **Purpose:** Render individual PowerPoint shapes with precise styling, positioning, and text formatting

---

## Input Schema
```json
{
  "slide": "PowerPoint slide object",
  "shape_spec": {
    "shape_type": "string (RECTANGLE/OVAL/ROUNDED_RECTANGLE/etc.)",
    "position": {"left": "number", "top": "number"},
    "size": {"width": "number", "height": "number"},
    "fill": {"type": "solid/gradient/none", "color": "array RGB"},
    "line": {"color": "array RGB", "width": "number", "style": "string"},
    "text": {
      "content": "string",
      "font": {"name": "string", "size": "number", "bold": "boolean"},
      "color": "array RGB",
      "alignment": "string (LEFT/CENTER/RIGHT)"
    }
  }
}
```

## Output Schema
```json
{
  "shape": "PowerPoint shape object",
  "rendered": "boolean",
  "actual_position": {"left": "number", "top": "number"},
  "actual_size": {"width": "number", "height": "number"},
  "validation": {
    "position_accurate": "boolean",
    "styling_applied": "boolean",
    "text_formatted": "boolean"
  }
}
```

---

## Required Skills (Hardcoded)

1. **Shape Creation** - Create various PowerPoint shape types
2. **Fill Styling** - Apply solid, gradient, or transparent fills
3. **Line Styling** - Configure borders and outlines
4. **Text Formatting** - Apply font, size, color, and alignment
5. **Position Calculation** - Convert inches/EMUs and position accurately

---

## Supported Shape Types

```python
SHAPE_TYPES = {
    'RECTANGLE': MSO_SHAPE.RECTANGLE,
    'ROUNDED_RECTANGLE': MSO_SHAPE.ROUNDED_RECTANGLE,
    'OVAL': MSO_SHAPE.OVAL,
    'DIAMOND': MSO_SHAPE.DIAMOND,
    'RIGHT_ARROW': MSO_SHAPE.RIGHT_ARROW,
    'LEFT_ARROW': MSO_SHAPE.LEFT_ARROW,
    'DOWN_ARROW': MSO_SHAPE.DOWN_ARROW,
    'UP_ARROW': MSO_SHAPE.UP_ARROW,
    'CHEVRON': MSO_SHAPE.CHEVRON,
    'PENTAGON': MSO_SHAPE.PENTAGON,
    'HEXAGON': MSO_SHAPE.HEXAGON,
    'PARALLELOGRAM': MSO_SHAPE.PARALLELOGRAM,
    'TRAPEZOID': MSO_SHAPE.TRAPEZOID,
    'FLOWCHART_PROCESS': MSO_SHAPE.FLOWCHART_PROCESS,
    'FLOWCHART_DECISION': MSO_SHAPE.FLOWCHART_DECISION,
    'FLOWCHART_TERMINATOR': MSO_SHAPE.FLOWCHART_TERMINATOR,
}

CONNECTOR_TYPES = {
    'STRAIGHT': MSO_CONNECTOR.STRAIGHT,
    'ELBOW': MSO_CONNECTOR.ELBOW,
    'CURVE': MSO_CONNECTOR.CURVE,
}
```

---

## Step-by-Step Instructions

### Step 1: Create Base Shape
```python
def create_shape(slide, shape_type, left, top, width, height):
    """Create a base shape on the slide."""

    # Get MSO_SHAPE type
    mso_type = SHAPE_TYPES.get(shape_type.upper(), MSO_SHAPE.RECTANGLE)

    # Create shape
    shape = slide.shapes.add_shape(
        mso_type,
        Inches(left),
        Inches(top),
        Inches(width),
        Inches(height)
    )

    return shape
```

### Step 2: Apply Fill
```python
def apply_fill(shape, fill_spec):
    """Apply fill styling to shape."""

    fill_type = fill_spec.get('type', 'solid')

    if fill_type == 'solid':
        shape.fill.solid()
        color = fill_spec.get('color', [255, 255, 255])
        shape.fill.fore_color.rgb = RGBColor(*color)

    elif fill_type == 'gradient':
        # Gradient fills require more complex setup
        apply_gradient_fill(shape, fill_spec)

    elif fill_type == 'none':
        shape.fill.background()

    # Transparency
    if fill_spec.get('transparency'):
        # Transparency is percentage (0-100)
        # Note: python-pptx doesn't directly support this,
        # but can be set via XML manipulation if needed
        pass

def apply_gradient_fill(shape, fill_spec):
    """Apply gradient fill to shape."""

    gradient_type = fill_spec.get('gradient_type', 'linear')
    colors = fill_spec.get('colors', [[255, 255, 255], [200, 200, 200]])

    shape.fill.gradient()

    # Set gradient direction
    angle = fill_spec.get('angle', 0)
    shape.fill.gradient_angle = angle

    # Set gradient stops
    stops = shape.fill.gradient_stops
    for i, color in enumerate(colors):
        if i < len(stops):
            stops[i].color.rgb = RGBColor(*color)
```

### Step 3: Apply Line Styling
```python
def apply_line(shape, line_spec):
    """Apply line/border styling to shape."""

    if not line_spec or line_spec.get('type') == 'none':
        shape.line.fill.background()
        return

    # Line color
    color = line_spec.get('color', [0, 0, 0])
    shape.line.color.rgb = RGBColor(*color)

    # Line width
    width = line_spec.get('width', 1)
    shape.line.width = Pt(width)

    # Dash style (if specified)
    dash_style = line_spec.get('dash_style')
    if dash_style:
        DASH_STYLES = {
            'solid': MSO_LINE_DASH_STYLE.SOLID,
            'dash': MSO_LINE_DASH_STYLE.DASH,
            'dot': MSO_LINE_DASH_STYLE.ROUND_DOT,
            'dash_dot': MSO_LINE_DASH_STYLE.DASH_DOT,
        }
        shape.line.dash_style = DASH_STYLES.get(dash_style, MSO_LINE_DASH_STYLE.SOLID)
```

### Step 4: Apply Text Formatting
```python
def apply_text(shape, text_spec):
    """Apply text and formatting to shape."""

    if not text_spec or not text_spec.get('content'):
        return

    tf = shape.text_frame
    tf.word_wrap = text_spec.get('word_wrap', True)

    # Text frame margins
    margins = text_spec.get('margins', {})
    tf.margin_left = Inches(margins.get('left', 0.05))
    tf.margin_right = Inches(margins.get('right', 0.05))
    tf.margin_top = Inches(margins.get('top', 0.05))
    tf.margin_bottom = Inches(margins.get('bottom', 0.05))

    # Vertical alignment
    v_align = text_spec.get('vertical_align', 'MIDDLE')
    V_ALIGN_MAP = {
        'TOP': MSO_ANCHOR.TOP,
        'MIDDLE': MSO_ANCHOR.MIDDLE,
        'BOTTOM': MSO_ANCHOR.BOTTOM,
    }
    tf.vertical_anchor = V_ALIGN_MAP.get(v_align.upper(), MSO_ANCHOR.MIDDLE)

    # Clear existing text
    for para in tf.paragraphs:
        para.clear()

    # Add text content
    content = text_spec['content']
    font_spec = text_spec.get('font', {})
    color = text_spec.get('color', [0, 0, 0])
    alignment = text_spec.get('alignment', 'CENTER')

    # Handle multi-line text
    lines = content.split('\n') if isinstance(content, str) else [content]

    for i, line in enumerate(lines):
        if i == 0:
            p = tf.paragraphs[0]
        else:
            p = tf.add_paragraph()

        run = p.add_run()
        run.text = line

        # Font settings
        run.font.name = font_spec.get('name', 'Aptos')
        run.font.size = Pt(font_spec.get('size', 18))
        run.font.bold = font_spec.get('bold', False)
        run.font.italic = font_spec.get('italic', False)
        run.font.color.rgb = RGBColor(*color)

        # Paragraph alignment
        ALIGN_MAP = {
            'LEFT': PP_ALIGN.LEFT,
            'CENTER': PP_ALIGN.CENTER,
            'RIGHT': PP_ALIGN.RIGHT,
            'JUSTIFY': PP_ALIGN.JUSTIFY,
        }
        p.alignment = ALIGN_MAP.get(alignment.upper(), PP_ALIGN.CENTER)

        # Line spacing
        if font_spec.get('line_spacing'):
            p.line_spacing = font_spec['line_spacing']
```

### Step 5: Render Connector
```python
def render_connector(slide, connector_spec):
    """Render a connector between two points or shapes."""

    connector_type = connector_spec.get('type', 'STRAIGHT')
    mso_connector = CONNECTOR_TYPES.get(connector_type.upper(), MSO_CONNECTOR.STRAIGHT)

    start = connector_spec.get('start', {})
    end = connector_spec.get('end', {})

    connector = slide.shapes.add_connector(
        mso_connector,
        Inches(start.get('x', 0)),
        Inches(start.get('y', 0)),
        Inches(end.get('x', 1)),
        Inches(end.get('y', 1))
    )

    # Apply line styling
    line_spec = connector_spec.get('line', {})
    color = line_spec.get('color', [100, 100, 100])
    connector.line.color.rgb = RGBColor(*color)
    connector.line.width = Pt(line_spec.get('width', 2))

    # Add arrowhead
    if connector_spec.get('arrow_end'):
        add_arrowhead(connector, 'end', connector_spec['arrow_end'])

    if connector_spec.get('arrow_start'):
        add_arrowhead(connector, 'start', connector_spec['arrow_start'])

    return connector

def add_arrowhead(connector, end_type, arrow_spec):
    """Add arrowhead to connector using OOXML."""

    from lxml import etree
    from pptx.oxml.ns import qn

    ln = connector._element.spPr.ln

    if end_type == 'end':
        arrow_elem = etree.SubElement(ln, qn('a:tailEnd'))
    else:
        arrow_elem = etree.SubElement(ln, qn('a:headEnd'))

    arrow_elem.set('type', arrow_spec.get('type', 'triangle'))
    arrow_elem.set('w', arrow_spec.get('width', 'med'))
    arrow_elem.set('len', arrow_spec.get('length', 'med'))
```

### Step 6: Render TextBox
```python
def render_textbox(slide, textbox_spec):
    """Render a text box on the slide."""

    left = textbox_spec.get('left', 0)
    top = textbox_spec.get('top', 0)
    width = textbox_spec.get('width', 2)
    height = textbox_spec.get('height', 0.5)

    textbox = slide.shapes.add_textbox(
        Inches(left),
        Inches(top),
        Inches(width),
        Inches(height)
    )

    # Apply text formatting
    text_spec = {
        'content': textbox_spec.get('text', ''),
        'font': textbox_spec.get('font', {}),
        'color': textbox_spec.get('color', [0, 0, 0]),
        'alignment': textbox_spec.get('alignment', 'LEFT'),
        'word_wrap': textbox_spec.get('word_wrap', True)
    }

    apply_text(textbox, text_spec)

    return textbox
```

### Step 7: Complete Shape Render Function
```python
def render_shape(slide, shape_spec):
    """Complete shape rendering with all styling."""

    # Create base shape
    shape_type = shape_spec.get('shape_type', 'RECTANGLE')
    position = shape_spec.get('position', {})
    size = shape_spec.get('size', {})

    shape = create_shape(
        slide,
        shape_type,
        position.get('left', 0),
        position.get('top', 0),
        size.get('width', 1),
        size.get('height', 1)
    )

    # Apply styling
    if shape_spec.get('fill'):
        apply_fill(shape, shape_spec['fill'])

    if shape_spec.get('line'):
        apply_line(shape, shape_spec['line'])

    if shape_spec.get('text'):
        apply_text(shape, shape_spec['text'])

    # Apply rounded rectangle adjustment
    if shape_type == 'ROUNDED_RECTANGLE' and shape_spec.get('corner_radius'):
        shape.adjustments[0] = shape_spec['corner_radius']

    # Validate render
    validation = validate_render(shape, shape_spec)

    return {
        'shape': shape,
        'rendered': True,
        'actual_position': {
            'left': shape.left / 914400,  # EMU to inches
            'top': shape.top / 914400
        },
        'actual_size': {
            'width': shape.width / 914400,
            'height': shape.height / 914400
        },
        'validation': validation
    }

def validate_render(shape, spec):
    """Validate that shape was rendered correctly."""

    validation = {
        'position_accurate': True,
        'styling_applied': True,
        'text_formatted': True
    }

    # Check position (within tolerance)
    expected_left = Inches(spec.get('position', {}).get('left', 0))
    if abs(shape.left - expected_left) > Inches(0.01):
        validation['position_accurate'] = False

    # Check fill applied
    if spec.get('fill') and spec['fill'].get('type') == 'solid':
        if not shape.fill.fore_color:
            validation['styling_applied'] = False

    # Check text exists
    if spec.get('text') and spec['text'].get('content'):
        if not shape.has_text_frame or not shape.text:
            validation['text_formatted'] = False

    return validation
```

---

## Common Shape Configurations

### Decision Node (Two-Tone)
```python
DECISION_NODE = {
    'header': {
        'shape_type': 'RECTANGLE',
        'fill': {'type': 'solid', 'color': [0, 51, 102]},
        'line': {'type': 'none'},
        'text': {
            'font': {'name': 'Aptos', 'size': 18, 'bold': True},
            'color': [255, 255, 255],
            'alignment': 'CENTER'
        }
    },
    'body': {
        'shape_type': 'RECTANGLE',
        'fill': {'type': 'solid', 'color': [240, 244, 248]},
        'line': {'color': [0, 51, 102], 'width': 2},
        'text': {
            'font': {'name': 'Aptos', 'size': 22, 'bold': True},
            'color': [33, 37, 41],
            'alignment': 'CENTER'
        }
    }
}
```

### Outcome Node (Colored)
```python
OUTCOME_NODE = {
    'header': {
        'shape_type': 'RECTANGLE',
        'fill': {'type': 'solid', 'color': [0, 102, 68]},  # Green
        'text': {
            'font': {'name': 'Aptos', 'size': 18, 'bold': True},
            'color': [255, 255, 255]
        }
    },
    'body': {
        'shape_type': 'RECTANGLE',
        'fill': {'type': 'solid', 'color': [255, 255, 255]},
        'line': {'color': [0, 102, 68], 'width': 2.5},
        'text': {
            'font': {'name': 'Aptos', 'size': 20, 'bold': True},
            'color': [0, 102, 68]
        }
    }
}
```

### Path Label (Rounded)
```python
PATH_LABEL = {
    'shape_type': 'ROUNDED_RECTANGLE',
    'corner_radius': 0.5,
    'fill': {'type': 'solid', 'color': [0, 102, 68]},
    'line': {'type': 'none'},
    'text': {
        'font': {'name': 'Aptos', 'size': 18, 'bold': True},
        'color': [255, 255, 255],
        'alignment': 'CENTER'
    }
}
```

---

## Validation Checklist

### Shape Creation
- [ ] Correct shape type used
- [ ] Position within slide bounds (0-13.33" x 0-7.5")
- [ ] Size reasonable for content

### Styling
- [ ] Fill color matches specification
- [ ] Line color and width correct
- [ ] No fill/line when specified as none

### Text
- [ ] Font family correct (Aptos)
- [ ] Font size minimum 18pt
- [ ] Color matches specification
- [ ] Alignment correct (LEFT/CENTER/RIGHT)
- [ ] Word wrap enabled

---

## Error Handling

| Error | Action |
|-------|--------|
| Invalid shape type | Fall back to RECTANGLE |
| Position out of bounds | Clamp to slide dimensions |
| Color values invalid | Use black [0,0,0] |
| Font not found | Fall back to Arial |
| Text overflow | Enable word wrap, truncate if needed |

---

**Agent Version:** 1.0
**Last Updated:** 2026-01-04
