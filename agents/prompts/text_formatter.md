# Text Formatter Agent

## Agent Identity
- **Name:** text_formatter
- **Step:** 12 (PowerPoint Population - Text Formatting)
- **Purpose:** Format text content with precise font application, size settings, and color application for PowerPoint shapes

---

## Input Schema
```json
{
  "text_frame": "PowerPoint text frame object",
  "text_content": {
    "text": "string (content to format)",
    "paragraphs": "array of paragraph objects (optional)"
  },
  "font_config": {
    "name": "string (font family, e.g., 'Aptos')",
    "size": "number (point size)",
    "bold": "boolean",
    "italic": "boolean",
    "underline": "boolean"
  },
  "color_config": {
    "rgb": "array [R, G, B]",
    "theme_color": "string (optional, e.g., 'ACCENT_1')"
  },
  "alignment_config": {
    "horizontal": "string (LEFT/CENTER/RIGHT/JUSTIFY)",
    "vertical": "string (TOP/MIDDLE/BOTTOM)"
  }
}
```

## Output Schema
```json
{
  "text_frame": "formatted PowerPoint text frame object",
  "formatted": "boolean",
  "paragraphs_processed": "number",
  "runs_processed": "number",
  "validation": {
    "font_applied": "boolean",
    "size_applied": "boolean",
    "color_applied": "boolean",
    "alignment_applied": "boolean"
  }
}
```

---

## Required Skills (Hardcoded)

1. **font_application** - Apply font family to text runs
2. **size_setting** - Set font size in points
3. **color_application** - Apply RGB or theme colors to text
4. **bold_italic_setting** - Apply bold, italic, underline styles
5. **alignment_configuration** - Set horizontal and vertical alignment

---

## Step-by-Step Instructions

### Step 1: Font Application
```python
from pptx.util import Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR

def apply_font_to_run(run, font_config):
    """Apply font settings to a single run."""

    # Font family
    font_name = font_config.get('name', 'Aptos')
    run.font.name = font_name

    # Ensure font is available (fallback)
    FONT_FALLBACKS = {
        'Aptos': 'Calibri',
        'Calibri': 'Arial',
        'Arial': None  # System default
    }

    # Font family validation happens at render time
    # Set the requested font, python-pptx doesn't validate

    return run

def apply_font_to_paragraph(paragraph, font_config):
    """Apply font settings to all runs in a paragraph."""

    for run in paragraph.runs:
        apply_font_to_run(run, font_config)

    return paragraph

def apply_font_to_text_frame(text_frame, font_config):
    """Apply font settings to entire text frame."""

    runs_processed = 0

    for paragraph in text_frame.paragraphs:
        for run in paragraph.runs:
            apply_font_to_run(run, font_config)
            runs_processed += 1

    return runs_processed
```

### Step 2: Size Setting
```python
def set_font_size(run, size_pt):
    """Set font size in points."""

    # Validate size range (minimum 8pt, maximum 96pt)
    MIN_SIZE = 8
    MAX_SIZE = 96

    clamped_size = max(MIN_SIZE, min(MAX_SIZE, size_pt))

    if clamped_size != size_pt:
        print(f"Warning: Font size {size_pt} clamped to {clamped_size}")

    run.font.size = Pt(clamped_size)

    return clamped_size

def set_paragraph_font_size(paragraph, size_pt):
    """Set font size for all runs in paragraph."""

    for run in paragraph.runs:
        set_font_size(run, size_pt)

    return paragraph

def set_text_frame_font_size(text_frame, size_pt):
    """Set font size for entire text frame."""

    for paragraph in text_frame.paragraphs:
        set_paragraph_font_size(paragraph, size_pt)

    return text_frame

# Common size presets for NCLEX slides
FONT_SIZE_PRESETS = {
    'title': 36,
    'subtitle': 28,
    'heading': 24,
    'body': 20,
    'body_small': 18,
    'caption': 14,
    'tip': 18,
    'label': 16,
    'note': 12
}

def apply_preset_size(run, preset_name):
    """Apply a preset font size."""

    size = FONT_SIZE_PRESETS.get(preset_name, 18)
    return set_font_size(run, size)
```

### Step 3: Color Application
```python
def apply_rgb_color(run, rgb_values):
    """Apply RGB color to text."""

    # Validate RGB values (0-255)
    validated_rgb = []
    for value in rgb_values:
        clamped = max(0, min(255, int(value)))
        validated_rgb.append(clamped)

    r, g, b = validated_rgb
    run.font.color.rgb = RGBColor(r, g, b)

    return run

def apply_theme_color(run, theme_color_name):
    """Apply theme color to text."""

    from pptx.enum.dml import MSO_THEME_COLOR

    THEME_COLOR_MAP = {
        'DARK_1': MSO_THEME_COLOR.DARK_1,
        'LIGHT_1': MSO_THEME_COLOR.LIGHT_1,
        'DARK_2': MSO_THEME_COLOR.DARK_2,
        'LIGHT_2': MSO_THEME_COLOR.LIGHT_2,
        'ACCENT_1': MSO_THEME_COLOR.ACCENT_1,
        'ACCENT_2': MSO_THEME_COLOR.ACCENT_2,
        'ACCENT_3': MSO_THEME_COLOR.ACCENT_3,
        'ACCENT_4': MSO_THEME_COLOR.ACCENT_4,
        'ACCENT_5': MSO_THEME_COLOR.ACCENT_5,
        'ACCENT_6': MSO_THEME_COLOR.ACCENT_6,
    }

    theme_color = THEME_COLOR_MAP.get(theme_color_name.upper())

    if theme_color:
        run.font.color.theme_color = theme_color
    else:
        # Fallback to black
        run.font.color.rgb = RGBColor(0, 0, 0)

    return run

# NCLEX brand color palette
NCLEX_COLORS = {
    'white': [255, 255, 255],
    'dark_blue': [0, 51, 102],
    'light_blue': [66, 133, 244],
    'dark_gray': [33, 37, 41],
    'light_gray': [108, 117, 125],
    'red_accent': [220, 53, 69],
    'green_success': [0, 102, 68],
    'yellow_warning': [255, 193, 7],
    'teal': [23, 162, 184]
}

def apply_nclex_color(run, color_name):
    """Apply NCLEX brand color to text."""

    rgb = NCLEX_COLORS.get(color_name, [0, 0, 0])
    return apply_rgb_color(run, rgb)
```

### Step 4: Bold, Italic, Underline Settings
```python
def apply_text_style(run, bold=None, italic=None, underline=None):
    """Apply text styling (bold, italic, underline)."""

    if bold is not None:
        run.font.bold = bold

    if italic is not None:
        run.font.italic = italic

    if underline is not None:
        run.font.underline = underline

    return run

def apply_paragraph_style(paragraph, bold=None, italic=None, underline=None):
    """Apply text styling to all runs in paragraph."""

    for run in paragraph.runs:
        apply_text_style(run, bold, italic, underline)

    return paragraph

# Style presets for different content types
STYLE_PRESETS = {
    'title': {'bold': True, 'italic': False, 'underline': False},
    'heading': {'bold': True, 'italic': False, 'underline': False},
    'emphasis': {'bold': False, 'italic': True, 'underline': False},
    'strong': {'bold': True, 'italic': False, 'underline': False},
    'link': {'bold': False, 'italic': False, 'underline': True},
    'normal': {'bold': False, 'italic': False, 'underline': False},
    'tip': {'bold': True, 'italic': False, 'underline': False}
}

def apply_style_preset(run, preset_name):
    """Apply a style preset."""

    preset = STYLE_PRESETS.get(preset_name, STYLE_PRESETS['normal'])
    return apply_text_style(run, **preset)
```

### Step 5: Alignment Configuration
```python
def set_horizontal_alignment(paragraph, alignment):
    """Set horizontal text alignment."""

    ALIGN_MAP = {
        'LEFT': PP_ALIGN.LEFT,
        'CENTER': PP_ALIGN.CENTER,
        'RIGHT': PP_ALIGN.RIGHT,
        'JUSTIFY': PP_ALIGN.JUSTIFY,
        'DISTRIBUTE': PP_ALIGN.DISTRIBUTE
    }

    pp_align = ALIGN_MAP.get(alignment.upper(), PP_ALIGN.LEFT)
    paragraph.alignment = pp_align

    return paragraph

def set_vertical_alignment(text_frame, alignment):
    """Set vertical text alignment for text frame."""

    V_ALIGN_MAP = {
        'TOP': MSO_ANCHOR.TOP,
        'MIDDLE': MSO_ANCHOR.MIDDLE,
        'BOTTOM': MSO_ANCHOR.BOTTOM
    }

    mso_anchor = V_ALIGN_MAP.get(alignment.upper(), MSO_ANCHOR.MIDDLE)
    text_frame.vertical_anchor = mso_anchor

    return text_frame

def set_text_alignment(text_frame, horizontal='LEFT', vertical='MIDDLE'):
    """Set both horizontal and vertical alignment."""

    # Vertical alignment on text frame
    set_vertical_alignment(text_frame, vertical)

    # Horizontal alignment on each paragraph
    for paragraph in text_frame.paragraphs:
        set_horizontal_alignment(paragraph, horizontal)

    return text_frame
```

### Step 6: Line Spacing and Margins
```python
from pptx.util import Inches

def set_line_spacing(paragraph, spacing):
    """Set line spacing for paragraph."""

    # Spacing can be:
    # - Single (1.0)
    # - 1.5 lines (1.5)
    # - Double (2.0)

    paragraph.line_spacing = spacing

    return paragraph

def set_text_frame_margins(text_frame, left=0.05, right=0.05, top=0.05, bottom=0.05):
    """Set text frame margins in inches."""

    text_frame.margin_left = Inches(left)
    text_frame.margin_right = Inches(right)
    text_frame.margin_top = Inches(top)
    text_frame.margin_bottom = Inches(bottom)

    return text_frame

def set_paragraph_spacing(paragraph, space_before=0, space_after=0):
    """Set space before and after paragraph in points."""

    paragraph.space_before = Pt(space_before)
    paragraph.space_after = Pt(space_after)

    return paragraph
```

### Step 7: Complete Text Formatting Function
```python
def format_text(text_frame, text_content, font_config, color_config, alignment_config):
    """Complete text formatting function."""

    validation = {
        'font_applied': False,
        'size_applied': False,
        'color_applied': False,
        'alignment_applied': False
    }

    runs_processed = 0
    paragraphs_processed = 0

    # Clear existing text if new content provided
    if text_content.get('text'):
        for para in text_frame.paragraphs:
            para.clear()

        # Add new text
        p = text_frame.paragraphs[0]
        run = p.add_run()
        run.text = text_content['text']

    # Process each paragraph
    for paragraph in text_frame.paragraphs:
        paragraphs_processed += 1

        # Set alignment
        if alignment_config:
            h_align = alignment_config.get('horizontal', 'LEFT')
            set_horizontal_alignment(paragraph, h_align)
            validation['alignment_applied'] = True

        # Process each run
        for run in paragraph.runs:
            runs_processed += 1

            # Apply font
            if font_config:
                if font_config.get('name'):
                    run.font.name = font_config['name']
                    validation['font_applied'] = True

                if font_config.get('size'):
                    run.font.size = Pt(font_config['size'])
                    validation['size_applied'] = True

                if font_config.get('bold') is not None:
                    run.font.bold = font_config['bold']

                if font_config.get('italic') is not None:
                    run.font.italic = font_config['italic']

            # Apply color
            if color_config:
                if color_config.get('rgb'):
                    apply_rgb_color(run, color_config['rgb'])
                    validation['color_applied'] = True
                elif color_config.get('theme_color'):
                    apply_theme_color(run, color_config['theme_color'])
                    validation['color_applied'] = True

    # Set vertical alignment
    if alignment_config and alignment_config.get('vertical'):
        set_vertical_alignment(text_frame, alignment_config['vertical'])

    return {
        'text_frame': text_frame,
        'formatted': True,
        'paragraphs_processed': paragraphs_processed,
        'runs_processed': runs_processed,
        'validation': validation
    }
```

### Step 8: Specialized Formatters
```python
def format_title_text(text_frame, text):
    """Format text as slide title."""

    return format_text(
        text_frame,
        {'text': text},
        {'name': 'Aptos', 'size': 36, 'bold': True},
        {'rgb': [255, 255, 255]},
        {'horizontal': 'LEFT', 'vertical': 'MIDDLE'}
    )

def format_body_text(text_frame, text):
    """Format text as body content."""

    return format_text(
        text_frame,
        {'text': text},
        {'name': 'Aptos', 'size': 20, 'bold': False},
        {'rgb': [255, 255, 255]},
        {'horizontal': 'LEFT', 'vertical': 'TOP'}
    )

def format_nclex_tip(text_frame, text):
    """Format text as NCLEX tip."""

    return format_text(
        text_frame,
        {'text': f"NCLEX TIP: {text}"},
        {'name': 'Aptos', 'size': 18, 'bold': True},
        {'rgb': [255, 255, 255]},
        {'horizontal': 'LEFT', 'vertical': 'MIDDLE'}
    )

def format_shape_label(text_frame, text, center=True):
    """Format text for shape labels."""

    h_align = 'CENTER' if center else 'LEFT'

    return format_text(
        text_frame,
        {'text': text},
        {'name': 'Aptos', 'size': 18, 'bold': True},
        {'rgb': [33, 37, 41]},
        {'horizontal': h_align, 'vertical': 'MIDDLE'}
    )
```

---

## Common Text Format Configurations

### Title Text
```python
TITLE_FORMAT = {
    'font_config': {'name': 'Aptos', 'size': 36, 'bold': True},
    'color_config': {'rgb': [255, 255, 255]},
    'alignment_config': {'horizontal': 'LEFT', 'vertical': 'MIDDLE'}
}
```

### Body Text
```python
BODY_FORMAT = {
    'font_config': {'name': 'Aptos', 'size': 20, 'bold': False},
    'color_config': {'rgb': [255, 255, 255]},
    'alignment_config': {'horizontal': 'LEFT', 'vertical': 'TOP'}
}
```

### Shape Header Text
```python
SHAPE_HEADER_FORMAT = {
    'font_config': {'name': 'Aptos', 'size': 18, 'bold': True},
    'color_config': {'rgb': [255, 255, 255]},
    'alignment_config': {'horizontal': 'CENTER', 'vertical': 'MIDDLE'}
}
```

### Shape Body Text
```python
SHAPE_BODY_FORMAT = {
    'font_config': {'name': 'Aptos', 'size': 22, 'bold': True},
    'color_config': {'rgb': [33, 37, 41]},
    'alignment_config': {'horizontal': 'CENTER', 'vertical': 'MIDDLE'}
}
```

---

## Validation Checklist

### Pre-Formatting
- [ ] Text frame object is valid
- [ ] Text content is not empty
- [ ] Font name is available (or fallback set)
- [ ] Font size within valid range (8-96pt)
- [ ] RGB values within range (0-255)

### Post-Formatting
- [ ] Font family applied to all runs
- [ ] Font size consistent across runs
- [ ] Color applied correctly
- [ ] Alignment matches specification
- [ ] Text is readable (sufficient contrast)

---

## Error Handling

| Error | Action |
|-------|--------|
| Invalid font name | Fall back to Arial |
| Font size out of range | Clamp to valid range |
| Invalid RGB values | Clamp to 0-255 |
| Empty text content | Skip formatting, return early |
| No text frame | Return error, cannot format |
| Invalid alignment | Use LEFT as default |

---

**Agent Version:** 1.0
**Last Updated:** 2026-01-04
