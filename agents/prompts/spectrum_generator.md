# Spectrum Generator Agent

## Agent Identity
- **Name:** spectrum_generator
- **Step:** 12 (PowerPoint Population - Spectrum Generation)
- **Purpose:** Generate spectrum and continuum visual aids for gradients, ranges, and continuous dimensions

---

## Input Schema
```json
{
  "slide_data": {
    "header": "string (slide title)",
    "visual_spec": "string (spectrum specification)",
    "layout": "string (A/B/C/D/E or AUTO)",
    "gradient": "string (blue/alert/bipolar)",
    "dimension": "string (name of scale)",
    "endpoints": {"low": "string", "high": "string"},
    "segments": "array of segment objects",
    "presenter_notes": "string"
  },
  "template_path": "string (path to visual template)",
  "domain_config": "reference to config/nclex.yaml"
}
```

## Output Schema
```json
{
  "slide": "PowerPoint slide object with spectrum",
  "shapes": {
    "gradient_bar": "shape object",
    "segment_boxes": "array of segment shapes",
    "endpoint_labels": "array of label shapes",
    "markers": "array of marker shapes"
  },
  "metadata": {
    "layout": "string",
    "segment_count": "number",
    "gradient_type": "string"
  },
  "validation": {
    "gradient_rendered": "boolean",
    "segments_visible": "boolean",
    "labels_readable": "boolean"
  }
}
```

---

## Required Skills (Hardcoded)

1. **Spectrum Structure Parsing** - Parse segments, endpoints, and gradient type
2. **Gradient Bar Generation** - Create horizontal or vertical gradient bars
3. **Segment Box Rendering** - Generate color-coded segment boxes
4. **Endpoint Labeling** - Add extreme labels at spectrum ends
5. **Direction Arrow Creation** - Add directional indicators

---

## Spectrum Identification Conditions

Content should be a SPECTRUM when:

1. **DEGREE VARIATIONS** - Concepts that vary by intensity
2. **CONTINUOUS DIMENSIONS** - Traits on a scale
3. **PROGRESSIVE SCALES** - Measurements with gradual change
4. **BIPOLAR CONSTRUCTS** - Opposites with middle ground
5. **SEVERITY GRADIENTS** - Clinical severity scales

DO NOT use spectrum when:
- Categories are discrete/separate (use table)
- Content is a process (use flowchart)
- Content cycles back (use cycle diagram)
- Comparing distinct groups (use key differentiators)

---

## Color Schemes (Three Gradient Options)

```
OPTION 1: BLUE GRADIENT (Intensity/Severity)
- Low End: RGB(227, 242, 253) - Light Blue #E3F2FD
- Mid Point: RGB(100, 181, 246) - Medium Blue #64B5F6
- High End: RGB(13, 71, 161) - Dark Blue #0D47A1

OPTION 2: ALERT GRADIENT (Warning/Risk)
- Low End: RGB(76, 175, 80) - Green #4CAF50
- Mid Point: RGB(255, 235, 59) - Yellow #FFEB3B
- High End: RGB(244, 67, 54) - Red #F44336

OPTION 3: BIPOLAR GRADIENT (Cool-Warm)
- Left End: RGB(33, 150, 243) - Blue #2196F3
- Center: RGB(158, 158, 158) - Gray #9E9E9E
- Right End: RGB(255, 87, 34) - Orange #FF5722

TEXT COLORS:
- On Light Background: RGB(0, 0, 0) - Black
- On Dark Background: RGB(255, 255, 255) - White
- End Labels: Match gradient ends
```

---

## Layout Specifications

### Layout A: Horizontal Bar Spectrum
```
[Low]====================================[High]
  |         |         |         |         |
Label 1  Label 2  Label 3  Label 4  Label 5

Dimensions:
- Bar width: 10.0 inches
- Bar height: 0.5 inches
- Marker spacing: Even distribution
- Labels below bar
```

### Layout B: Vertical Bar Spectrum
```
    [High]
      ||
      || <- Label 5
      ||
      || <- Label 4
      ||
      || <- Label 3
      ||
      || <- Label 2
      ||
      || <- Label 1
      ||
    [Low]

Dimensions:
- Bar height: 4.5 inches
- Bar width: 0.5 inches
- Labels to the right
- Gradient from bottom to top
```

### Layout C: Bipolar Spectrum with Center
```
[Extreme A]=============@==============[Extreme B]
                     CENTER
     <---------------|---------------->
   Features A                Features B

Dimensions:
- Bar width: 10.0 inches
- Center marker emphasized
- Features listed on each side
```

### Layout D: Segmented Spectrum
```
+---------+---------+---------+---------+---------+
|  None   |  Mild   |Moderate | Severe  | Extreme |
+---------+---------+---------+---------+---------+
| Desc 1  | Desc 2  | Desc 3  | Desc 4  | Desc 5  |
+---------+---------+---------+---------+---------+
--------------------------------------------------->
Low Severity                          High Severity

Dimensions:
- 3-6 segments
- Each segment: ~2.0 inches wide
- Description under each segment
- Arrow showing direction
```

### Layout E: Dual-Axis Spectrum
```
                      HIGH
                       ^
                       |
            Q2         |         Q1
         [Label]       |       [Label]
                       |
     LOW <-------------+-------------> HIGH
                       |
            Q3         |         Q4
         [Label]       |       [Label]
                       |
                       v
                      LOW

Dimensions:
- Grid: 8.0 x 6.0 inches
- Four quadrants
- Axis labels at ends
```

---

## Step-by-Step Instructions

### Step 1: Parse Spectrum Data
```python
def parse_spectrum_spec(spec_text):
    """Parse spectrum specification."""

    data = {
        'layout': 'AUTO',
        'gradient': 'blue',
        'dimension': 'Severity',
        'endpoints': {'low': 'Low', 'high': 'High'},
        'segments': [],
        'center_label': None
    }

    # Extract layout
    layout_match = re.search(r'Layout:\s*([A-E])', spec_text)
    if layout_match:
        data['layout'] = layout_match.group(1)

    # Extract gradient type
    gradient_match = re.search(r'Gradient:\s*(\w+)', spec_text)
    if gradient_match:
        data['gradient'] = gradient_match.group(1).lower()

    # Extract endpoints
    low_match = re.search(r'Low:\s*"([^"]+)"', spec_text)
    high_match = re.search(r'High:\s*"([^"]+)"', spec_text)
    if low_match:
        data['endpoints']['low'] = low_match.group(1)
    if high_match:
        data['endpoints']['high'] = high_match.group(1)

    # Extract segments
    segment_pattern = r'(\d+)\.\s*Label:\s*"([^"]+)".*?Description:\s*"([^"]+)"'
    for match in re.finditer(segment_pattern, spec_text, re.DOTALL):
        data['segments'].append({
            'number': int(match.group(1)),
            'label': match.group(2),
            'description': match.group(3)
        })

    # Extract center label for bipolar
    center_match = re.search(r'Center:\s*"([^"]+)"', spec_text)
    if center_match:
        data['center_label'] = center_match.group(1)

    return data
```

### Step 2: Get Gradient Colors
```python
BLUE_GRADIENT = [
    RGBColor(227, 242, 253),  # Light
    RGBColor(144, 202, 249),
    RGBColor(100, 181, 246),
    RGBColor(66, 165, 245),
    RGBColor(13, 71, 161),    # Dark
]

ALERT_GRADIENT = [
    RGBColor(76, 175, 80),    # Green
    RGBColor(205, 220, 57),
    RGBColor(255, 235, 59),   # Yellow
    RGBColor(255, 152, 0),
    RGBColor(244, 67, 54),    # Red
]

BIPOLAR_GRADIENT = [
    RGBColor(33, 150, 243),   # Blue (cool)
    RGBColor(144, 202, 249),
    RGBColor(158, 158, 158),  # Gray (neutral)
    RGBColor(255, 171, 145),
    RGBColor(255, 87, 34),    # Orange (warm)
]

def get_gradient_colors(gradient_type, count):
    """Get interpolated colors for segment count."""
    gradients = {
        'blue': BLUE_GRADIENT,
        'alert': ALERT_GRADIENT,
        'bipolar': BIPOLAR_GRADIENT
    }

    base_colors = gradients.get(gradient_type, BLUE_GRADIENT)

    if count <= len(base_colors):
        step = len(base_colors) / count
        return [base_colors[int(i * step)] for i in range(count)]
    else:
        return interpolate_colors(base_colors, count)
```

### Step 3: Add Gradient Bar
```python
def add_gradient_bar(slide, left, top, width, height, gradient_type):
    """Add horizontal gradient bar."""

    bar = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE,
        Inches(left), Inches(top), Inches(width), Inches(height)
    )

    # For simplified implementation, use middle color as solid
    colors = get_gradient_colors(gradient_type, 5)
    bar.fill.solid()
    bar.fill.fore_color.rgb = colors[len(colors) // 2]

    return bar
```

### Step 4: Generate Layout D (Segmented Spectrum)
```python
def generate_layout_d(slide, spectrum_data):
    """Generate Layout D: Discrete segments on a continuum."""

    segments = spectrum_data.get('segments', [])
    gradient_type = spectrum_data.get('gradient', 'blue')
    endpoints = spectrum_data.get('endpoints', {})

    segment_count = len(segments)

    # Calculate dimensions
    total_width = 10.5
    segment_width = total_width / segment_count
    segment_height = 1.0
    desc_height = 1.2

    start_left = 1.4
    top = 2.0

    # Get gradient colors
    colors = get_gradient_colors(gradient_type, segment_count)

    for i, segment in enumerate(segments):
        left = start_left + i * segment_width

        # Segment header box
        header_box = slide.shapes.add_shape(
            MSO_SHAPE.RECTANGLE,
            Inches(left), Inches(top),
            Inches(segment_width - 0.05), Inches(segment_height)
        )
        header_box.fill.solid()
        header_box.fill.fore_color.rgb = colors[i]
        header_box.line.color.rgb = RGBColor(0, 0, 0)
        header_box.line.width = Pt(1)

        # Header text
        tf = header_box.text_frame
        tf.paragraphs[0].text = segment['label']
        tf.paragraphs[0].font.size = Pt(20)
        tf.paragraphs[0].font.bold = True
        tf.paragraphs[0].font.name = 'Aptos'
        # White text on dark colors, black on light
        text_color = RGBColor(255, 255, 255) if i >= segment_count // 2 else RGBColor(0, 0, 0)
        tf.paragraphs[0].font.color.rgb = text_color
        tf.paragraphs[0].alignment = PP_ALIGN.CENTER

        # Description box
        desc_box = slide.shapes.add_shape(
            MSO_SHAPE.RECTANGLE,
            Inches(left), Inches(top + segment_height),
            Inches(segment_width - 0.05), Inches(desc_height)
        )
        desc_box.fill.solid()
        desc_box.fill.fore_color.rgb = lighten_color(colors[i], 0.5)
        desc_box.line.color.rgb = RGBColor(0, 0, 0)
        desc_box.line.width = Pt(1)

        if segment.get('description'):
            tf = desc_box.text_frame
            tf.word_wrap = True
            tf.paragraphs[0].text = segment['description']
            tf.paragraphs[0].font.size = Pt(18)
            tf.paragraphs[0].font.name = 'Aptos'
            tf.paragraphs[0].font.color.rgb = RGBColor(0, 0, 0)
            tf.paragraphs[0].alignment = PP_ALIGN.CENTER

    # Add direction arrow
    arrow_top = top + segment_height + desc_height + 0.3
    arrow = slide.shapes.add_shape(
        MSO_SHAPE.RIGHT_ARROW,
        Inches(start_left), Inches(arrow_top),
        Inches(total_width), Inches(0.3)
    )
    arrow.fill.solid()
    arrow.fill.fore_color.rgb = colors[-1]

    # Endpoint labels
    if endpoints:
        add_text_label(slide, start_left - 0.3, arrow_top + 0.4,
                      2.5, 0.4, endpoints.get('low', ''), 18, False, RGBColor(0, 0, 0))
        add_text_label(slide, start_left + total_width - 2.2, arrow_top + 0.4,
                      2.5, 0.4, endpoints.get('high', ''), 18, False, RGBColor(0, 0, 0))

def lighten_color(color, factor):
    """Lighten a color by factor (0-1)."""
    r = min(255, int(color[0] + (255 - color[0]) * factor))
    g = min(255, int(color[1] + (255 - color[1]) * factor))
    b = min(255, int(color[2] + (255 - color[2]) * factor))
    return RGBColor(r, g, b)
```

### Step 5: Generate Layout C (Bipolar)
```python
def generate_layout_c(slide, spectrum_data):
    """Generate Layout C: Bipolar spectrum with emphasized center."""

    endpoints = spectrum_data.get('endpoints', {})
    center_label = spectrum_data.get('center_label', 'CENTER')
    gradient_type = spectrum_data.get('gradient', 'bipolar')

    # Bar dimensions
    bar_left = 1.5
    bar_width = 10.0
    bar_top = 3.0
    bar_height = 0.5

    # Create gradient bar
    add_gradient_bar(slide, bar_left, bar_top, bar_width, bar_height, gradient_type)

    # Center marker
    center_x = bar_left + bar_width / 2 - 0.15
    marker = slide.shapes.add_shape(
        MSO_SHAPE.OVAL,
        Inches(center_x), Inches(bar_top - 0.15),
        Inches(0.3), Inches(bar_height + 0.3)
    )
    marker.fill.solid()
    marker.fill.fore_color.rgb = RGBColor(158, 158, 158)  # Gray
    marker.line.color.rgb = RGBColor(0, 0, 0)
    marker.line.width = Pt(2)

    # Center label
    add_text_label(slide, center_x - 0.5, bar_top + bar_height + 0.2,
                  1.3, 0.4, center_label, 18, True, RGBColor(0, 0, 0))

    # Endpoint labels
    add_text_label(slide, bar_left - 0.5, bar_top - 0.6,
                  2.0, 0.5, endpoints.get('low', 'LOW'), 22, True,
                  RGBColor(33, 150, 243))  # Blue

    add_text_label(slide, bar_left + bar_width - 1.5, bar_top - 0.6,
                  2.0, 0.5, endpoints.get('high', 'HIGH'), 22, True,
                  RGBColor(255, 87, 34))  # Orange

def add_text_label(slide, left, top, width, height, text, font_size, bold, color):
    """Add a text box with specified formatting."""
    textbox = slide.shapes.add_textbox(
        Inches(left), Inches(top), Inches(width), Inches(height)
    )
    tf = textbox.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = text
    p.font.size = Pt(font_size)
    p.font.bold = bold
    p.font.name = 'Aptos'
    p.font.color.rgb = color
    p.alignment = PP_ALIGN.CENTER
```

---

## Character Limits

```
END LABELS:
- Characters per line: 15
- Maximum lines: 1

SEGMENT LABELS:
- Characters per line: 12
- Maximum lines: 1

SEGMENT DESCRIPTIONS:
- Characters per line: 20
- Maximum lines: 2

QUADRANT LABELS (Layout E):
- Characters per line: 18
- Maximum lines: 2

AXIS LABELS:
- Characters: 15 max
```

---

## Validation Checklist

### Structure
- [ ] Layout selected (A/B/C/D/E) matches content
- [ ] Segment count: 3-6 segments
- [ ] Content truly continuous (not discrete categories)
- [ ] Gradient type matches content nature

### Gradient Styling
- [ ] Colors flow smoothly
- [ ] Segments evenly distributed
- [ ] Text readable on all background colors
- [ ] White text on dark, black text on light

### Endpoints
- [ ] Low endpoint labeled (left/bottom)
- [ ] High endpoint labeled (right/top)
- [ ] Direction arrow present (Layout D)
- [ ] Center marker emphasized (Layout C)

---

## Error Handling

| Error | Action |
|-------|--------|
| Content not truly continuous | Consider table instead |
| Too many segments (8+) | Combine related levels |
| Gradient not visible | Ensure sufficient color contrast |
| Text overlaps gradient | Position labels outside bar |

---

**Agent Version:** 1.0
**Last Updated:** 2026-01-04
