# Connector Drawer Agent

## Agent Identity
- **Name:** connector_drawer
- **Step:** 12 (PowerPoint Population - Connector Drawing)
- **Purpose:** Draw connectors, arrows, and lines between shapes with line drawing, arrow creation, and rotation calculation

---

## Input Schema
```json
{
  "slide": "PowerPoint slide object",
  "connector_spec": {
    "type": "string (straight/elbow/curve/arrow)",
    "start": {
      "shape": "PowerPoint shape object (optional)",
      "point": {"x": "number", "y": "number"},
      "anchor": "string (top/bottom/left/right/center)"
    },
    "end": {
      "shape": "PowerPoint shape object (optional)",
      "point": {"x": "number", "y": "number"},
      "anchor": "string (top/bottom/left/right/center)"
    },
    "line_style": {
      "color": "array [R, G, B]",
      "width": "number (points)",
      "dash_style": "string (solid/dash/dot)"
    },
    "arrow_style": {
      "start_arrow": "string (none/triangle/stealth/diamond/oval)",
      "end_arrow": "string (none/triangle/stealth/diamond/oval)",
      "arrow_size": "string (small/medium/large)"
    }
  }
}
```

## Output Schema
```json
{
  "connector": "PowerPoint connector/line object",
  "created": "boolean",
  "start_point": {"x": "number", "y": "number"},
  "end_point": {"x": "number", "y": "number"},
  "rotation": "number (degrees)",
  "validation": {
    "connected_to_shapes": "boolean",
    "line_styled": "boolean",
    "arrows_applied": "boolean"
  }
}
```

---

## Required Skills (Hardcoded)

1. **line_drawing** - Draw straight lines between points
2. **arrow_creation** - Add arrowheads to connectors
3. **rotation_calculation** - Calculate connector rotation angles
4. **elbow_connector** - Create elbow (right-angle) connectors
5. **curve_connector** - Create curved connectors

---

## Step-by-Step Instructions

### Step 1: Line Drawing
```python
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_CONNECTOR
from pptx.enum.dml import MSO_LINE_DASH_STYLE
import math

def draw_line(slide, start_x, start_y, end_x, end_y):
    """Draw a straight line between two points."""

    connector = slide.shapes.add_connector(
        MSO_CONNECTOR.STRAIGHT,
        Inches(start_x),
        Inches(start_y),
        Inches(end_x),
        Inches(end_y)
    )

    return connector

def draw_elbow_connector(slide, start_x, start_y, end_x, end_y):
    """Draw an elbow (right-angle) connector."""

    connector = slide.shapes.add_connector(
        MSO_CONNECTOR.ELBOW,
        Inches(start_x),
        Inches(start_y),
        Inches(end_x),
        Inches(end_y)
    )

    return connector

def draw_curve_connector(slide, start_x, start_y, end_x, end_y):
    """Draw a curved connector."""

    connector = slide.shapes.add_connector(
        MSO_CONNECTOR.CURVE,
        Inches(start_x),
        Inches(start_y),
        Inches(end_x),
        Inches(end_y)
    )

    return connector

# Connector type mapping
CONNECTOR_TYPES = {
    'straight': MSO_CONNECTOR.STRAIGHT,
    'elbow': MSO_CONNECTOR.ELBOW,
    'curve': MSO_CONNECTOR.CURVE
}

def draw_connector(slide, connector_type, start_x, start_y, end_x, end_y):
    """Draw a connector of specified type."""

    mso_type = CONNECTOR_TYPES.get(connector_type.lower(), MSO_CONNECTOR.STRAIGHT)

    connector = slide.shapes.add_connector(
        mso_type,
        Inches(start_x),
        Inches(start_y),
        Inches(end_x),
        Inches(end_y)
    )

    return connector
```

### Step 2: Arrow Creation
```python
from lxml import etree
from pptx.oxml.ns import qn

# Arrow type mapping (OOXML values)
ARROW_TYPES = {
    'none': 'none',
    'triangle': 'triangle',
    'stealth': 'stealth',
    'diamond': 'diamond',
    'oval': 'oval',
    'arrow': 'arrow',
    'open': 'open'
}

# Arrow size mapping
ARROW_SIZES = {
    'small': ('sm', 'sm'),
    'medium': ('med', 'med'),
    'large': ('lg', 'lg')
}

def add_start_arrow(connector, arrow_type='triangle', size='medium'):
    """Add arrowhead to start of connector."""

    arrow_type_val = ARROW_TYPES.get(arrow_type, 'triangle')
    width, length = ARROW_SIZES.get(size, ('med', 'med'))

    # Access line element
    ln = connector._element.spPr.ln

    if ln is None:
        # Create line element if it doesn't exist
        spPr = connector._element.spPr
        ln = etree.SubElement(spPr, qn('a:ln'))

    # Remove existing headEnd
    existing = ln.find(qn('a:headEnd'))
    if existing is not None:
        ln.remove(existing)

    # Add new arrow
    if arrow_type_val != 'none':
        head_end = etree.SubElement(ln, qn('a:headEnd'))
        head_end.set('type', arrow_type_val)
        head_end.set('w', width)
        head_end.set('len', length)

    return connector

def add_end_arrow(connector, arrow_type='triangle', size='medium'):
    """Add arrowhead to end of connector."""

    arrow_type_val = ARROW_TYPES.get(arrow_type, 'triangle')
    width, length = ARROW_SIZES.get(size, ('med', 'med'))

    ln = connector._element.spPr.ln

    if ln is None:
        spPr = connector._element.spPr
        ln = etree.SubElement(spPr, qn('a:ln'))

    # Remove existing tailEnd
    existing = ln.find(qn('a:tailEnd'))
    if existing is not None:
        ln.remove(existing)

    # Add new arrow
    if arrow_type_val != 'none':
        tail_end = etree.SubElement(ln, qn('a:tailEnd'))
        tail_end.set('type', arrow_type_val)
        tail_end.set('w', width)
        tail_end.set('len', length)

    return connector

def add_arrows(connector, start_arrow='none', end_arrow='triangle', size='medium'):
    """Add arrowheads to both ends of connector."""

    add_start_arrow(connector, start_arrow, size)
    add_end_arrow(connector, end_arrow, size)

    return connector

def create_arrow(slide, start_x, start_y, end_x, end_y, arrow_style='single'):
    """Create an arrow (line with arrowhead)."""

    connector = draw_line(slide, start_x, start_y, end_x, end_y)

    if arrow_style == 'single':
        add_end_arrow(connector, 'triangle', 'medium')
    elif arrow_style == 'double':
        add_start_arrow(connector, 'triangle', 'medium')
        add_end_arrow(connector, 'triangle', 'medium')
    elif arrow_style == 'none':
        pass

    return connector
```

### Step 3: Rotation Calculation
```python
def calculate_angle(start_x, start_y, end_x, end_y):
    """Calculate angle between two points in degrees."""

    dx = end_x - start_x
    dy = end_y - start_y

    # Calculate angle in radians
    angle_rad = math.atan2(dy, dx)

    # Convert to degrees
    angle_deg = math.degrees(angle_rad)

    return angle_deg

def calculate_distance(start_x, start_y, end_x, end_y):
    """Calculate distance between two points."""

    dx = end_x - start_x
    dy = end_y - start_y

    return math.sqrt(dx * dx + dy * dy)

def get_anchor_point(shape, anchor='center'):
    """Get anchor point on a shape."""

    # Get shape bounds in inches
    left = shape.left / 914400
    top = shape.top / 914400
    width = shape.width / 914400
    height = shape.height / 914400

    center_x = left + width / 2
    center_y = top + height / 2

    ANCHOR_POINTS = {
        'top': {'x': center_x, 'y': top},
        'bottom': {'x': center_x, 'y': top + height},
        'left': {'x': left, 'y': center_y},
        'right': {'x': left + width, 'y': center_y},
        'center': {'x': center_x, 'y': center_y},
        'top-left': {'x': left, 'y': top},
        'top-right': {'x': left + width, 'y': top},
        'bottom-left': {'x': left, 'y': top + height},
        'bottom-right': {'x': left + width, 'y': top + height}
    }

    return ANCHOR_POINTS.get(anchor, ANCHOR_POINTS['center'])

def calculate_best_anchor(start_shape, end_shape):
    """Calculate best anchor points for connecting two shapes."""

    # Get shape centers
    start_center = get_anchor_point(start_shape, 'center')
    end_center = get_anchor_point(end_shape, 'center')

    dx = end_center['x'] - start_center['x']
    dy = end_center['y'] - start_center['y']

    # Determine primary direction
    if abs(dx) > abs(dy):
        # Horizontal primary
        if dx > 0:
            start_anchor = 'right'
            end_anchor = 'left'
        else:
            start_anchor = 'left'
            end_anchor = 'right'
    else:
        # Vertical primary
        if dy > 0:
            start_anchor = 'bottom'
            end_anchor = 'top'
        else:
            start_anchor = 'top'
            end_anchor = 'bottom'

    return {
        'start': get_anchor_point(start_shape, start_anchor),
        'end': get_anchor_point(end_shape, end_anchor),
        'start_anchor': start_anchor,
        'end_anchor': end_anchor
    }

def rotate_point(x, y, cx, cy, angle_deg):
    """Rotate a point around a center point."""

    angle_rad = math.radians(angle_deg)

    # Translate to origin
    tx = x - cx
    ty = y - cy

    # Rotate
    rx = tx * math.cos(angle_rad) - ty * math.sin(angle_rad)
    ry = tx * math.sin(angle_rad) + ty * math.cos(angle_rad)

    # Translate back
    return {
        'x': rx + cx,
        'y': ry + cy
    }
```

### Step 4: Line Styling
```python
def style_connector(connector, color=None, width=2, dash_style='solid'):
    """Apply styling to connector."""

    # Color
    if color:
        if isinstance(color, list):
            connector.line.color.rgb = RGBColor(color[0], color[1], color[2])
        else:
            # Assume RGBColor
            connector.line.color.rgb = color
    else:
        # Default gray
        connector.line.color.rgb = RGBColor(100, 100, 100)

    # Width
    connector.line.width = Pt(width)

    # Dash style
    DASH_STYLES = {
        'solid': MSO_LINE_DASH_STYLE.SOLID,
        'dash': MSO_LINE_DASH_STYLE.DASH,
        'dot': MSO_LINE_DASH_STYLE.ROUND_DOT,
        'dash_dot': MSO_LINE_DASH_STYLE.DASH_DOT,
        'long_dash': MSO_LINE_DASH_STYLE.LONG_DASH,
        'square_dot': MSO_LINE_DASH_STYLE.SQUARE_DOT
    }

    style = DASH_STYLES.get(dash_style.lower(), MSO_LINE_DASH_STYLE.SOLID)
    connector.line.dash_style = style

    return connector

# Predefined connector styles
CONNECTOR_STYLES = {
    'default': {
        'color': [100, 100, 100],
        'width': 2,
        'dash_style': 'solid',
        'end_arrow': 'triangle'
    },
    'yes_path': {
        'color': [0, 102, 68],
        'width': 2.5,
        'dash_style': 'solid',
        'end_arrow': 'triangle'
    },
    'no_path': {
        'color': [220, 53, 69],
        'width': 2.5,
        'dash_style': 'solid',
        'end_arrow': 'triangle'
    },
    'neutral': {
        'color': [66, 133, 244],
        'width': 2,
        'dash_style': 'solid',
        'end_arrow': 'triangle'
    },
    'hierarchy': {
        'color': [0, 51, 102],
        'width': 2,
        'dash_style': 'solid',
        'end_arrow': 'none'
    },
    'dashed': {
        'color': [128, 128, 128],
        'width': 1.5,
        'dash_style': 'dash',
        'end_arrow': 'none'
    },
    'timeline': {
        'color': [66, 133, 244],
        'width': 3,
        'dash_style': 'solid',
        'end_arrow': 'triangle'
    }
}

def apply_connector_style(connector, style_name):
    """Apply a predefined connector style."""

    style = CONNECTOR_STYLES.get(style_name, CONNECTOR_STYLES['default'])

    style_connector(
        connector,
        color=style.get('color'),
        width=style.get('width', 2),
        dash_style=style.get('dash_style', 'solid')
    )

    end_arrow = style.get('end_arrow', 'triangle')
    start_arrow = style.get('start_arrow', 'none')

    if end_arrow != 'none':
        add_end_arrow(connector, end_arrow)
    if start_arrow != 'none':
        add_start_arrow(connector, start_arrow)

    return connector
```

### Step 5: Shape-to-Shape Connectors
```python
def connect_shapes(slide, start_shape, end_shape, connector_type='straight',
                   style='default', start_anchor=None, end_anchor=None):
    """Connect two shapes with a connector."""

    # Calculate anchor points
    if start_anchor and end_anchor:
        start_point = get_anchor_point(start_shape, start_anchor)
        end_point = get_anchor_point(end_shape, end_anchor)
    else:
        anchors = calculate_best_anchor(start_shape, end_shape)
        start_point = anchors['start']
        end_point = anchors['end']

    # Draw connector
    connector = draw_connector(
        slide, connector_type,
        start_point['x'], start_point['y'],
        end_point['x'], end_point['y']
    )

    # Apply style
    apply_connector_style(connector, style)

    return {
        'connector': connector,
        'start_point': start_point,
        'end_point': end_point,
        'angle': calculate_angle(
            start_point['x'], start_point['y'],
            end_point['x'], end_point['y']
        )
    }

def connect_with_label(slide, start_shape, end_shape, label_text,
                       connector_type='straight', style='default'):
    """Connect shapes with a label on the connector."""

    # Connect shapes
    result = connect_shapes(slide, start_shape, end_shape, connector_type, style)

    # Calculate label position (midpoint)
    mid_x = (result['start_point']['x'] + result['end_point']['x']) / 2
    mid_y = (result['start_point']['y'] + result['end_point']['y']) / 2

    # Create label textbox
    from pptx.util import Inches

    label_width = 0.8
    label_height = 0.3

    label = slide.shapes.add_textbox(
        Inches(mid_x - label_width / 2),
        Inches(mid_y - label_height / 2),
        Inches(label_width),
        Inches(label_height)
    )

    tf = label.text_frame
    p = tf.paragraphs[0]
    p.text = label_text
    p.font.size = Pt(14)
    p.font.bold = True

    from pptx.enum.text import PP_ALIGN
    p.alignment = PP_ALIGN.CENTER

    result['label'] = label

    return result
```

### Step 6: Complete Connector Drawer Function
```python
def draw_complete_connector(slide, connector_spec):
    """Complete connector drawing function."""

    validation = {
        'connected_to_shapes': False,
        'line_styled': False,
        'arrows_applied': False
    }

    # Get connector type
    connector_type = connector_spec.get('type', 'straight')

    # Determine start and end points
    start_spec = connector_spec.get('start', {})
    end_spec = connector_spec.get('end', {})

    # Start point
    if start_spec.get('shape'):
        start_shape = start_spec['shape']
        start_anchor = start_spec.get('anchor', 'center')
        start_point = get_anchor_point(start_shape, start_anchor)
        validation['connected_to_shapes'] = True
    else:
        start_point = start_spec.get('point', {'x': 0, 'y': 0})

    # End point
    if end_spec.get('shape'):
        end_shape = end_spec['shape']
        end_anchor = end_spec.get('anchor', 'center')
        end_point = get_anchor_point(end_shape, end_anchor)
        validation['connected_to_shapes'] = True
    else:
        end_point = end_spec.get('point', {'x': 1, 'y': 1})

    # Draw the connector
    connector = draw_connector(
        slide, connector_type,
        start_point['x'], start_point['y'],
        end_point['x'], end_point['y']
    )

    # Apply line style
    line_style = connector_spec.get('line_style', {})
    color = line_style.get('color', [100, 100, 100])
    width = line_style.get('width', 2)
    dash_style = line_style.get('dash_style', 'solid')

    style_connector(connector, color, width, dash_style)
    validation['line_styled'] = True

    # Apply arrows
    arrow_style = connector_spec.get('arrow_style', {})
    start_arrow = arrow_style.get('start_arrow', 'none')
    end_arrow = arrow_style.get('end_arrow', 'triangle')
    arrow_size = arrow_style.get('arrow_size', 'medium')

    add_arrows(connector, start_arrow, end_arrow, arrow_size)
    validation['arrows_applied'] = True

    # Calculate rotation
    rotation = calculate_angle(
        start_point['x'], start_point['y'],
        end_point['x'], end_point['y']
    )

    return {
        'connector': connector,
        'created': True,
        'start_point': start_point,
        'end_point': end_point,
        'rotation': rotation,
        'validation': validation
    }
```

### Step 7: Specialized Connector Functions
```python
def draw_decision_arrow(slide, start_shape, end_shape, label, is_yes=True):
    """Draw a decision tree arrow with Yes/No label."""

    style = 'yes_path' if is_yes else 'no_path'

    result = connect_with_label(
        slide, start_shape, end_shape, label,
        connector_type='elbow',
        style=style
    )

    # Style the label
    label_color = [0, 102, 68] if is_yes else [220, 53, 69]
    result['label'].text_frame.paragraphs[0].font.color.rgb = RGBColor(*label_color)

    return result

def draw_flowchart_arrow(slide, start_shape, end_shape):
    """Draw a standard flowchart arrow."""

    return connect_shapes(
        slide, start_shape, end_shape,
        connector_type='straight',
        style='default'
    )

def draw_hierarchy_line(slide, parent_shape, child_shape):
    """Draw a hierarchy connector (no arrowhead)."""

    return connect_shapes(
        slide, parent_shape, child_shape,
        connector_type='elbow',
        style='hierarchy',
        start_anchor='bottom',
        end_anchor='top'
    )

def draw_timeline_arrow(slide, start_x, start_y, end_x, end_y):
    """Draw a timeline arrow (horizontal with arrow)."""

    connector = draw_line(slide, start_x, start_y, end_x, end_y)
    apply_connector_style(connector, 'timeline')

    return connector

def draw_multiple_connectors(slide, connections):
    """Draw multiple connectors from a list of specifications."""

    results = []

    for conn_spec in connections:
        result = draw_complete_connector(slide, conn_spec)
        results.append(result)

    return results
```

---

## Common Connector Configurations

### Decision Tree Yes Arrow
```python
YES_ARROW_SPEC = {
    'type': 'elbow',
    'line_style': {
        'color': [0, 102, 68],
        'width': 2.5,
        'dash_style': 'solid'
    },
    'arrow_style': {
        'start_arrow': 'none',
        'end_arrow': 'triangle',
        'arrow_size': 'medium'
    }
}
```

### Decision Tree No Arrow
```python
NO_ARROW_SPEC = {
    'type': 'elbow',
    'line_style': {
        'color': [220, 53, 69],
        'width': 2.5,
        'dash_style': 'solid'
    },
    'arrow_style': {
        'start_arrow': 'none',
        'end_arrow': 'triangle',
        'arrow_size': 'medium'
    }
}
```

### Flowchart Arrow
```python
FLOWCHART_ARROW_SPEC = {
    'type': 'straight',
    'line_style': {
        'color': [100, 100, 100],
        'width': 2,
        'dash_style': 'solid'
    },
    'arrow_style': {
        'start_arrow': 'none',
        'end_arrow': 'triangle',
        'arrow_size': 'medium'
    }
}
```

### Hierarchy Line
```python
HIERARCHY_LINE_SPEC = {
    'type': 'elbow',
    'line_style': {
        'color': [0, 51, 102],
        'width': 2,
        'dash_style': 'solid'
    },
    'arrow_style': {
        'start_arrow': 'none',
        'end_arrow': 'none',
        'arrow_size': 'medium'
    }
}
```

---

## Validation Checklist

### Pre-Drawing
- [ ] Start point is within slide bounds
- [ ] End point is within slide bounds
- [ ] Connector type is valid
- [ ] Shapes exist (if connecting shapes)

### Post-Drawing
- [ ] Connector is visible (length > 0)
- [ ] Line color applied correctly
- [ ] Line width is appropriate
- [ ] Arrowheads rendered correctly
- [ ] Connector does not overlap other elements unexpectedly

---

## Error Handling

| Error | Action |
|-------|--------|
| Invalid connector type | Default to STRAIGHT |
| Invalid arrow type | Default to triangle |
| Points are identical | Log warning, skip drawing |
| Shape anchor not found | Default to center |
| Color value invalid | Default to gray [100,100,100] |
| Line width invalid | Default to 2pt |

---

**Agent Version:** 1.0
**Last Updated:** 2026-01-04
