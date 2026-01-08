# Slide Assembler Agent

## Agent Identity
- **Name:** slide_assembler
- **Step:** 12 (PowerPoint Population - Slide Assembly)
- **Purpose:** Assemble individual slides by combining shapes, text, and visual elements into cohesive slide layouts

---

## Input Schema
```json
{
  "slide": "PowerPoint slide object",
  "slide_data": {
    "header": "string",
    "body": "string or null",
    "visual_elements": "array of shape specifications",
    "presenter_notes": "string",
    "slide_type": "string (Content/Visual/Vignette/Answer)"
  },
  "template_config": {
    "shape_mappings": "object (name to purpose mapping)",
    "font_settings": "object (shape-specific font configs)",
    "positions": "object (element positions)"
  }
}
```

## Output Schema
```json
{
  "slide": "assembled PowerPoint slide object",
  "shapes_placed": "number",
  "text_populated": "boolean",
  "notes_added": "boolean",
  "validation": {
    "all_elements_placed": "boolean",
    "text_fits": "boolean",
    "z_order_correct": "boolean"
  }
}
```

---

## Required Skills (Hardcoded)

1. **Shape Placement** - Position shapes at exact coordinates
2. **Text Population** - Fill text frames with content preserving formatting
3. **Z-Order Management** - Control layering of overlapping shapes
4. **Notes Integration** - Add presenter notes to notes slide
5. **Layout Validation** - Verify assembled slide meets requirements

---

## Assembly Process

### Step 1: Prepare Slide Canvas
```python
def prepare_slide(prs, layout_type):
    """Prepare a slide with appropriate layout."""

    # Get blank layout
    blank_layout = None
    for layout in prs.slide_layouts:
        if layout.name == "Blank":
            blank_layout = layout
            break

    if not blank_layout:
        blank_layout = prs.slide_layouts[-1]

    # Create new slide
    slide = prs.slides.add_slide(blank_layout)

    return slide
```

### Step 2: Add Background Elements
```python
def add_background_elements(slide, template_slide):
    """Copy background rectangles and design elements from template."""

    BACKGROUND_SHAPES = [
        'Rectangle 1',   # Dark header bar
        'Rectangle 6',   # Light gray content area
        'Rectangle 7',   # White content box
        'Rectangle 13',  # Footer bar
        'Rounded Rectangle 4'  # Red accent
    ]

    for shape in template_slide.shapes:
        if shape.name in BACKGROUND_SHAPES:
            copy_shape_to_slide(slide, shape)
```

### Step 3: Add Title
```python
def add_title(slide, text, config):
    """Add title text to slide header area."""

    title_config = config.get('title', {})
    left = Inches(title_config.get('left', 0.07))
    top = Inches(title_config.get('top', -0.06))
    width = Inches(title_config.get('width', 11.42))
    height = Inches(title_config.get('height', 0.71))

    title_box = slide.shapes.add_textbox(left, top, width, height)
    tf = title_box.text_frame

    p = tf.paragraphs[0]
    p.text = text
    p.font.size = Pt(title_config.get('font_size', 36))
    p.font.bold = title_config.get('bold', True)
    p.font.name = title_config.get('font_name', 'Aptos')

    # Title text color depends on background
    title_color = title_config.get('color', [255, 255, 255])
    p.font.color.rgb = RGBColor(*title_color)
    p.alignment = PP_ALIGN.LEFT

    return title_box
```

### Step 4: Add Body Content
```python
def add_body_content(slide, text, config):
    """Add body text to main content area."""

    body_config = config.get('body', {})
    left = Inches(body_config.get('left', 0.78))
    top = Inches(body_config.get('top', 1.45))
    width = Inches(body_config.get('width', 11.0))
    height = Inches(body_config.get('height', 4.5))

    body_box = slide.shapes.add_textbox(left, top, width, height)
    tf = body_box.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = text
    p.font.size = Pt(body_config.get('font_size', 20))
    p.font.name = body_config.get('font_name', 'Aptos')

    body_color = body_config.get('color', [255, 255, 255])
    p.font.color.rgb = RGBColor(*body_color)

    return body_box
```

### Step 5: Add NCLEX Tip
```python
def add_nclex_tip(slide, text, config):
    """Add NCLEX tip to bottom of slide."""

    if not text or text.lower() in ['none', 'n/a', '']:
        return None

    tip_config = config.get('tip', {})
    left = Inches(tip_config.get('left', 0.07))
    top = Inches(tip_config.get('top', 6.63))
    width = Inches(tip_config.get('width', 12.0))
    height = Inches(tip_config.get('height', 0.5))

    tip_box = slide.shapes.add_textbox(left, top, width, height)
    tf = tip_box.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = f"NCLEX TIP: {text}"
    p.font.size = Pt(tip_config.get('font_size', 18))
    p.font.name = tip_config.get('font_name', 'Aptos')
    p.font.bold = True

    tip_color = tip_config.get('color', [255, 255, 255])
    p.font.color.rgb = RGBColor(*tip_color)

    return tip_box
```

### Step 6: Add Visual Elements
```python
def add_visual_elements(slide, visual_elements):
    """Add visual elements (shapes, connectors, images) to slide."""

    placed_shapes = []

    for element in visual_elements:
        element_type = element.get('type')

        if element_type == 'shape':
            shape = add_shape_element(slide, element)
            placed_shapes.append(shape)

        elif element_type == 'connector':
            connector = add_connector_element(slide, element)
            placed_shapes.append(connector)

        elif element_type == 'textbox':
            textbox = add_textbox_element(slide, element)
            placed_shapes.append(textbox)

        elif element_type == 'image':
            image = add_image_element(slide, element)
            placed_shapes.append(image)

        elif element_type == 'table':
            table = add_table_element(slide, element)
            placed_shapes.append(table)

    return placed_shapes

def add_shape_element(slide, spec):
    """Add a shape element based on specification."""

    shape_type = getattr(MSO_SHAPE, spec.get('shape_type', 'RECTANGLE'))

    shape = slide.shapes.add_shape(
        shape_type,
        Inches(spec.get('left', 0)),
        Inches(spec.get('top', 0)),
        Inches(spec.get('width', 1)),
        Inches(spec.get('height', 1))
    )

    # Apply fill
    if spec.get('fill_color'):
        shape.fill.solid()
        shape.fill.fore_color.rgb = RGBColor(*spec['fill_color'])
    elif spec.get('no_fill'):
        shape.fill.background()

    # Apply line
    if spec.get('line_color'):
        shape.line.color.rgb = RGBColor(*spec['line_color'])
        shape.line.width = Pt(spec.get('line_width', 1))
    elif spec.get('no_line'):
        shape.line.fill.background()

    # Add text if specified
    if spec.get('text'):
        tf = shape.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = spec['text']

        text_config = spec.get('text_config', {})
        p.font.size = Pt(text_config.get('font_size', 18))
        p.font.name = text_config.get('font_name', 'Aptos')
        p.font.bold = text_config.get('bold', False)

        if text_config.get('color'):
            p.font.color.rgb = RGBColor(*text_config['color'])

        p.alignment = getattr(PP_ALIGN, text_config.get('alignment', 'CENTER'))

    return shape
```

### Step 7: Add Presenter Notes
```python
def add_presenter_notes(slide, notes_text):
    """Add presenter notes to slide."""

    if not notes_text:
        return False

    notes_slide = slide.notes_slide
    notes_frame = notes_slide.notes_text_frame

    # Clear existing notes
    notes_frame.clear()

    # Add new notes
    p = notes_frame.paragraphs[0]
    p.text = notes_text

    return True
```

### Step 8: Validate Assembly
```python
def validate_slide_assembly(slide, expected_elements):
    """Validate that slide was assembled correctly."""

    validation = {
        'all_elements_placed': True,
        'text_fits': True,
        'z_order_correct': True,
        'issues': []
    }

    # Check element count
    actual_count = len(slide.shapes)
    if actual_count < expected_elements:
        validation['all_elements_placed'] = False
        validation['issues'].append(
            f"Missing elements: expected {expected_elements}, found {actual_count}"
        )

    # Check text overflow
    for shape in slide.shapes:
        if shape.has_text_frame:
            tf = shape.text_frame
            # Check if text might overflow
            for para in tf.paragraphs:
                if len(para.text) > 500:
                    validation['text_fits'] = False
                    validation['issues'].append(
                        f"Text may overflow in shape {shape.name}"
                    )

    return validation
```

---

## Complete Slide Assembly Function

```python
def assemble_slide(prs, slide_data, template_config, template_slide=None):
    """Assemble a complete slide from components."""

    # Prepare slide
    slide = prepare_slide(prs, slide_data.get('slide_type', 'Content'))

    # Add background elements (if template provided)
    if template_slide:
        add_background_elements(slide, template_slide)

    # Add title
    if slide_data.get('header'):
        add_title(slide, slide_data['header'], template_config)

    # Route based on slide type
    slide_type = slide_data.get('slide_type', 'Content')

    if slide_type == 'Content':
        # Standard content slide
        if slide_data.get('body'):
            add_body_content(slide, slide_data['body'], template_config)

        if slide_data.get('tip'):
            add_nclex_tip(slide, slide_data['tip'], template_config)

    elif slide_type == 'Visual':
        # Visual slide with generated elements
        if slide_data.get('visual_elements'):
            add_visual_elements(slide, slide_data['visual_elements'])

    elif slide_type in ['Vignette', 'Answer']:
        # Case study slides
        if slide_data.get('body'):
            add_body_content(slide, slide_data['body'], template_config)

    # Add presenter notes (all slides)
    if slide_data.get('presenter_notes'):
        add_presenter_notes(slide, slide_data['presenter_notes'])

    # Validate
    expected_shapes = calculate_expected_shapes(slide_data)
    validation = validate_slide_assembly(slide, expected_shapes)

    return slide, validation

def calculate_expected_shapes(slide_data):
    """Calculate expected number of shapes for validation."""

    count = 0

    if slide_data.get('header'):
        count += 1
    if slide_data.get('body'):
        count += 1
    if slide_data.get('tip'):
        count += 1
    if slide_data.get('visual_elements'):
        count += len(slide_data['visual_elements'])

    return count
```

---

## Z-Order Management

Shapes are layered in this order (back to front):
1. Background rectangles (header bar, content area)
2. Accent elements (red rounded rectangle)
3. Content boxes (title, body)
4. Visual elements (tables, diagrams)
5. Overlay elements (connectors, labels)

```python
def ensure_z_order(slide, shape, position):
    """Ensure shape is at correct z-order position."""

    # Move shape to specific position in z-order
    # 0 = back, len(shapes) = front

    shapes_xml = slide.shapes._spTree
    shape_element = shape._element

    # Remove and re-insert at position
    shapes_xml.remove(shape_element)
    shapes_xml.insert(position + 2, shape_element)  # +2 for cSld and spTree
```

---

## Validation Checklist

### Before Assembly
- [ ] Slide data complete
- [ ] Template config loaded
- [ ] Font files available

### After Assembly
- [ ] All text shapes populated
- [ ] Visual elements positioned correctly
- [ ] Presenter notes added
- [ ] Z-order correct (background behind content)
- [ ] Text readable (not overflowing)

---

## Error Handling

| Error | Action |
|-------|--------|
| Missing shape data | Use defaults, log warning |
| Text overflow | Truncate with ellipsis, log warning |
| Shape position invalid | Clamp to slide bounds |
| Font not found | Fall back to Arial |
| Notes empty | Skip notes addition |

---

**Agent Version:** 1.0
**Last Updated:** 2026-01-04
