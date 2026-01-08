# Color Applier Agent

## Agent Identity
- **Name:** color_applier
- **Step:** 12 (PowerPoint Population - Color Application)
- **Purpose:** Apply color schemes to PowerPoint shapes with RGB conversion, fill application, and border coloring

---

## Input Schema
```json
{
  "shape": "PowerPoint shape object",
  "color_spec": {
    "fill": {
      "type": "string (solid/gradient/none)",
      "color": "array [R, G, B] or hex string",
      "gradient_colors": "array of [R, G, B] arrays (for gradient)",
      "gradient_angle": "number (degrees)",
      "transparency": "number (0-100)"
    },
    "line": {
      "color": "array [R, G, B] or hex string",
      "width": "number (points)",
      "transparency": "number (0-100)"
    }
  },
  "color_scheme": "string (optional, e.g., 'nclex_primary', 'decision_node')"
}
```

## Output Schema
```json
{
  "shape": "colored PowerPoint shape object",
  "applied": "boolean",
  "fill_applied": "boolean",
  "line_applied": "boolean",
  "validation": {
    "fill_color_correct": "boolean",
    "line_color_correct": "boolean",
    "transparency_applied": "boolean"
  }
}
```

---

## Required Skills (Hardcoded)

1. **rgb_conversion** - Convert hex, names, and arrays to RGB values
2. **fill_application** - Apply solid and gradient fills
3. **border_coloring** - Apply line/border colors
4. **transparency_setting** - Apply transparency to fills and lines
5. **color_scheme_lookup** - Look up predefined color schemes

---

## Step-by-Step Instructions

### Step 1: RGB Conversion
```python
from pptx.dml.color import RGBColor
from pptx.util import Pt
from pptx.enum.dml import MSO_LINE_DASH_STYLE

def hex_to_rgb(hex_color):
    """Convert hex color string to RGB tuple."""

    # Remove # if present
    hex_color = hex_color.lstrip('#')

    # Handle short form (#RGB -> #RRGGBB)
    if len(hex_color) == 3:
        hex_color = ''.join([c*2 for c in hex_color])

    # Convert to RGB
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)

    return [r, g, b]

def name_to_rgb(color_name):
    """Convert named color to RGB values."""

    COLOR_NAMES = {
        # Basic colors
        'white': [255, 255, 255],
        'black': [0, 0, 0],
        'red': [255, 0, 0],
        'green': [0, 128, 0],
        'blue': [0, 0, 255],
        'yellow': [255, 255, 0],
        'cyan': [0, 255, 255],
        'magenta': [255, 0, 255],
        'gray': [128, 128, 128],
        'grey': [128, 128, 128],

        # NCLEX brand colors
        'nclex_dark_blue': [0, 51, 102],
        'nclex_light_blue': [66, 133, 244],
        'nclex_red': [220, 53, 69],
        'nclex_green': [0, 102, 68],
        'nclex_teal': [23, 162, 184],
        'nclex_yellow': [255, 193, 7],
        'nclex_dark_gray': [33, 37, 41],
        'nclex_light_gray': [108, 117, 125],

        # Visual element colors
        'header_blue': [0, 51, 102],
        'body_light': [240, 244, 248],
        'success_green': [0, 102, 68],
        'warning_amber': [255, 193, 7],
        'danger_red': [220, 53, 69],
        'info_blue': [23, 162, 184]
    }

    return COLOR_NAMES.get(color_name.lower(), [0, 0, 0])

def normalize_color(color_input):
    """Normalize any color input to RGB array."""

    if isinstance(color_input, list) and len(color_input) == 3:
        # Already RGB array
        return [max(0, min(255, int(c))) for c in color_input]

    elif isinstance(color_input, str):
        if color_input.startswith('#') or len(color_input) in [3, 6]:
            # Hex color
            return hex_to_rgb(color_input)
        else:
            # Named color
            return name_to_rgb(color_input)

    elif isinstance(color_input, tuple):
        # Convert tuple to list
        return [max(0, min(255, int(c))) for c in color_input]

    else:
        # Default to black
        return [0, 0, 0]

def create_rgb_color(color_input):
    """Create RGBColor object from any color input."""

    rgb = normalize_color(color_input)
    return RGBColor(rgb[0], rgb[1], rgb[2])
```

### Step 2: Fill Application
```python
def apply_solid_fill(shape, color, transparency=0):
    """Apply solid color fill to shape."""

    rgb = normalize_color(color)

    shape.fill.solid()
    shape.fill.fore_color.rgb = RGBColor(rgb[0], rgb[1], rgb[2])

    # Apply transparency if specified (0-100)
    if transparency > 0:
        # Note: python-pptx doesn't directly support fill transparency
        # This requires OOXML manipulation
        apply_fill_transparency(shape, transparency)

    return shape

def apply_gradient_fill(shape, colors, angle=0):
    """Apply gradient fill to shape."""

    shape.fill.gradient()

    # Set gradient angle
    shape.fill.gradient_angle = angle

    # Get gradient stops
    stops = shape.fill.gradient_stops

    # Apply colors to stops
    for i, color in enumerate(colors):
        if i < len(stops):
            rgb = normalize_color(color)
            stops[i].color.rgb = RGBColor(rgb[0], rgb[1], rgb[2])
            stops[i].position = i / max(1, len(colors) - 1)

    return shape

def apply_no_fill(shape):
    """Remove fill from shape (transparent background)."""

    shape.fill.background()

    return shape

def apply_fill_transparency(shape, transparency_percent):
    """Apply transparency to shape fill using OOXML."""

    from lxml import etree
    from pptx.oxml.ns import qn

    # Transparency in OOXML is 0-100000 (100000 = 100%)
    alpha = int((100 - transparency_percent) * 1000)

    spPr = shape._element.spPr
    solidFill = spPr.find(qn('a:solidFill'))

    if solidFill is not None:
        srgbClr = solidFill.find(qn('a:srgbClr'))
        if srgbClr is not None:
            alpha_elem = etree.SubElement(srgbClr, qn('a:alpha'))
            alpha_elem.set('val', str(alpha))

    return shape
```

### Step 3: Border/Line Coloring
```python
def apply_line_color(shape, color, width=1):
    """Apply line/border color to shape."""

    rgb = normalize_color(color)

    shape.line.color.rgb = RGBColor(rgb[0], rgb[1], rgb[2])
    shape.line.width = Pt(width)

    return shape

def apply_no_line(shape):
    """Remove line/border from shape."""

    shape.line.fill.background()

    return shape

def apply_line_style(shape, color, width=1, dash_style='solid'):
    """Apply complete line styling."""

    rgb = normalize_color(color)

    shape.line.color.rgb = RGBColor(rgb[0], rgb[1], rgb[2])
    shape.line.width = Pt(width)

    # Dash style
    DASH_STYLES = {
        'solid': MSO_LINE_DASH_STYLE.SOLID,
        'dash': MSO_LINE_DASH_STYLE.DASH,
        'dot': MSO_LINE_DASH_STYLE.ROUND_DOT,
        'dash_dot': MSO_LINE_DASH_STYLE.DASH_DOT,
        'long_dash': MSO_LINE_DASH_STYLE.LONG_DASH,
        'long_dash_dot': MSO_LINE_DASH_STYLE.LONG_DASH_DOT
    }

    style = DASH_STYLES.get(dash_style.lower(), MSO_LINE_DASH_STYLE.SOLID)
    shape.line.dash_style = style

    return shape

def apply_line_transparency(shape, transparency_percent):
    """Apply transparency to shape line using OOXML."""

    from lxml import etree
    from pptx.oxml.ns import qn

    alpha = int((100 - transparency_percent) * 1000)

    spPr = shape._element.spPr
    ln = spPr.find(qn('a:ln'))

    if ln is not None:
        solidFill = ln.find(qn('a:solidFill'))
        if solidFill is not None:
            srgbClr = solidFill.find(qn('a:srgbClr'))
            if srgbClr is not None:
                alpha_elem = etree.SubElement(srgbClr, qn('a:alpha'))
                alpha_elem.set('val', str(alpha))

    return shape
```

### Step 4: Color Scheme Application
```python
# Predefined color schemes for NCLEX visual elements
COLOR_SCHEMES = {
    'decision_node_header': {
        'fill': {'type': 'solid', 'color': [0, 51, 102]},
        'line': {'type': 'none'}
    },
    'decision_node_body': {
        'fill': {'type': 'solid', 'color': [240, 244, 248]},
        'line': {'type': 'solid', 'color': [0, 51, 102], 'width': 2}
    },
    'success_outcome': {
        'fill': {'type': 'solid', 'color': [255, 255, 255]},
        'line': {'type': 'solid', 'color': [0, 102, 68], 'width': 2.5}
    },
    'warning_outcome': {
        'fill': {'type': 'solid', 'color': [255, 255, 255]},
        'line': {'type': 'solid', 'color': [255, 193, 7], 'width': 2.5}
    },
    'danger_outcome': {
        'fill': {'type': 'solid', 'color': [255, 255, 255]},
        'line': {'type': 'solid', 'color': [220, 53, 69], 'width': 2.5}
    },
    'path_label_yes': {
        'fill': {'type': 'solid', 'color': [0, 102, 68]},
        'line': {'type': 'none'}
    },
    'path_label_no': {
        'fill': {'type': 'solid', 'color': [220, 53, 69]},
        'line': {'type': 'none'}
    },
    'connector_default': {
        'fill': {'type': 'none'},
        'line': {'type': 'solid', 'color': [100, 100, 100], 'width': 2}
    },
    'table_header': {
        'fill': {'type': 'solid', 'color': [0, 51, 102]},
        'line': {'type': 'solid', 'color': [0, 51, 102], 'width': 1}
    },
    'table_row_even': {
        'fill': {'type': 'solid', 'color': [255, 255, 255]},
        'line': {'type': 'solid', 'color': [200, 200, 200], 'width': 0.5}
    },
    'table_row_odd': {
        'fill': {'type': 'solid', 'color': [240, 244, 248]},
        'line': {'type': 'solid', 'color': [200, 200, 200], 'width': 0.5}
    },
    'timeline_event': {
        'fill': {'type': 'solid', 'color': [66, 133, 244]},
        'line': {'type': 'none'}
    },
    'hierarchy_parent': {
        'fill': {'type': 'solid', 'color': [0, 51, 102]},
        'line': {'type': 'none'}
    },
    'hierarchy_child': {
        'fill': {'type': 'solid', 'color': [66, 133, 244]},
        'line': {'type': 'none'}
    }
}

def apply_color_scheme(shape, scheme_name):
    """Apply a predefined color scheme to shape."""

    scheme = COLOR_SCHEMES.get(scheme_name)

    if not scheme:
        print(f"Warning: Unknown color scheme '{scheme_name}'")
        return shape

    # Apply fill
    fill_spec = scheme.get('fill', {})
    fill_type = fill_spec.get('type', 'none')

    if fill_type == 'solid':
        apply_solid_fill(shape, fill_spec.get('color', [255, 255, 255]))
    elif fill_type == 'gradient':
        apply_gradient_fill(shape, fill_spec.get('colors', [[255, 255, 255]]))
    elif fill_type == 'none':
        apply_no_fill(shape)

    # Apply line
    line_spec = scheme.get('line', {})
    line_type = line_spec.get('type', 'none')

    if line_type == 'solid':
        apply_line_color(
            shape,
            line_spec.get('color', [0, 0, 0]),
            line_spec.get('width', 1)
        )
    elif line_type == 'none':
        apply_no_line(shape)

    return shape
```

### Step 5: Complete Color Application Function
```python
def apply_colors(shape, color_spec=None, color_scheme=None):
    """Complete color application function."""

    validation = {
        'fill_color_correct': False,
        'line_color_correct': False,
        'transparency_applied': False
    }

    fill_applied = False
    line_applied = False

    # Use color scheme if specified
    if color_scheme:
        apply_color_scheme(shape, color_scheme)
        fill_applied = True
        line_applied = True
        validation['fill_color_correct'] = True
        validation['line_color_correct'] = True

    # Override with specific color_spec if provided
    elif color_spec:
        # Apply fill
        fill_spec = color_spec.get('fill')
        if fill_spec:
            fill_type = fill_spec.get('type', 'solid')

            if fill_type == 'solid':
                color = fill_spec.get('color', [255, 255, 255])
                apply_solid_fill(shape, color)

                if fill_spec.get('transparency'):
                    apply_fill_transparency(shape, fill_spec['transparency'])
                    validation['transparency_applied'] = True

                fill_applied = True
                validation['fill_color_correct'] = True

            elif fill_type == 'gradient':
                colors = fill_spec.get('gradient_colors', [[255, 255, 255], [200, 200, 200]])
                angle = fill_spec.get('gradient_angle', 0)
                apply_gradient_fill(shape, colors, angle)
                fill_applied = True
                validation['fill_color_correct'] = True

            elif fill_type == 'none':
                apply_no_fill(shape)
                fill_applied = True

        # Apply line
        line_spec = color_spec.get('line')
        if line_spec:
            color = line_spec.get('color')

            if color:
                width = line_spec.get('width', 1)
                apply_line_color(shape, color, width)

                if line_spec.get('transparency'):
                    apply_line_transparency(shape, line_spec['transparency'])
                    validation['transparency_applied'] = True

                line_applied = True
                validation['line_color_correct'] = True
            else:
                apply_no_line(shape)
                line_applied = True

    return {
        'shape': shape,
        'applied': fill_applied or line_applied,
        'fill_applied': fill_applied,
        'line_applied': line_applied,
        'validation': validation
    }
```

### Step 6: Utility Functions
```python
def get_contrasting_text_color(background_color):
    """Get contrasting text color (black or white) for background."""

    rgb = normalize_color(background_color)

    # Calculate relative luminance
    # Using simplified formula
    luminance = (0.299 * rgb[0] + 0.587 * rgb[1] + 0.114 * rgb[2]) / 255

    # Return white for dark backgrounds, black for light
    if luminance < 0.5:
        return [255, 255, 255]
    else:
        return [0, 0, 0]

def blend_colors(color1, color2, ratio=0.5):
    """Blend two colors by a ratio (0-1)."""

    rgb1 = normalize_color(color1)
    rgb2 = normalize_color(color2)

    blended = [
        int(rgb1[i] * (1 - ratio) + rgb2[i] * ratio)
        for i in range(3)
    ]

    return blended

def lighten_color(color, amount=0.2):
    """Lighten a color by amount (0-1)."""

    return blend_colors(color, [255, 255, 255], amount)

def darken_color(color, amount=0.2):
    """Darken a color by amount (0-1)."""

    return blend_colors(color, [0, 0, 0], amount)

def get_color_palette(base_color, variations=5):
    """Generate a color palette from a base color."""

    rgb = normalize_color(base_color)

    palette = []
    for i in range(variations):
        # Calculate light to dark progression
        ratio = i / (variations - 1)

        # Lighter versions first
        if i < variations // 2:
            variation = lighten_color(rgb, 0.3 - (i * 0.15))
        else:
            variation = darken_color(rgb, (i - variations // 2) * 0.15)

        palette.append(variation)

    return palette
```

---

## Predefined Color Palettes

### NCLEX Primary Palette
```python
NCLEX_PRIMARY_PALETTE = {
    'primary': [0, 51, 102],       # Dark blue
    'secondary': [66, 133, 244],   # Light blue
    'accent': [220, 53, 69],       # Red
    'success': [0, 102, 68],       # Green
    'warning': [255, 193, 7],      # Yellow
    'info': [23, 162, 184],        # Teal
    'light': [240, 244, 248],      # Light gray
    'dark': [33, 37, 41]           # Dark gray
}
```

### Decision Tree Palette
```python
DECISION_TREE_PALETTE = {
    'node_header': [0, 51, 102],
    'node_body': [240, 244, 248],
    'yes_path': [0, 102, 68],
    'no_path': [220, 53, 69],
    'connector': [100, 100, 100],
    'outcome_positive': [0, 102, 68],
    'outcome_negative': [220, 53, 69],
    'outcome_neutral': [255, 193, 7]
}
```

### Table Palette
```python
TABLE_PALETTE = {
    'header': [0, 51, 102],
    'header_text': [255, 255, 255],
    'row_even': [255, 255, 255],
    'row_odd': [240, 244, 248],
    'border': [200, 200, 200],
    'cell_text': [33, 37, 41]
}
```

---

## Validation Checklist

### Pre-Application
- [ ] Shape object is valid
- [ ] Color values are in valid range (0-255)
- [ ] Color scheme name exists (if using scheme)
- [ ] Gradient has at least 2 colors

### Post-Application
- [ ] Fill color matches specification
- [ ] Line color matches specification
- [ ] Transparency applied correctly
- [ ] No fill/line when specified as none
- [ ] Text remains readable against fill

---

## Error Handling

| Error | Action |
|-------|--------|
| Invalid color value | Clamp to 0-255 range |
| Unknown color name | Fall back to black |
| Invalid hex format | Fall back to black |
| Unknown color scheme | Log warning, skip application |
| Invalid gradient colors | Use default white-to-gray |
| Transparency out of range | Clamp to 0-100 |

---

**Agent Version:** 1.0
**Last Updated:** 2026-01-04
