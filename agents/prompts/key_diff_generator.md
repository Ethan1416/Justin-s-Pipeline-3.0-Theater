# Key Differentiators Generator Agent

## Agent Identity
- **Name:** key_diff_generator
- **Step:** 12 (PowerPoint Population - Key Differentiators Generation)
- **Purpose:** Generate key differentiators visual aids for differential diagnosis and distinguishing similar concepts

---

## Input Schema
```json
{
  "slide_data": {
    "header": "string (slide title)",
    "visual_spec": "string (key differentiators specification)",
    "layout": "string (A/B/C/D/E or AUTO)",
    "concepts": "array of concept objects",
    "features": "array of feature objects with is_key flag",
    "presenter_notes": "string"
  },
  "template_path": "string (path to visual template)",
  "domain_config": "reference to config/nclex.yaml"
}
```

## Output Schema
```json
{
  "slide": "PowerPoint slide object with key differentiators",
  "shapes": {
    "concept_headers": "array of header shapes",
    "feature_rows": "array of feature row shapes",
    "key_diff_boxes": "array of highlighted key difference shapes",
    "separator": "VS separator shape"
  },
  "metadata": {
    "layout": "string",
    "concept_count": "number",
    "key_diff_count": "number"
  },
  "validation": {
    "concepts_rendered": "boolean",
    "key_diffs_highlighted": "boolean",
    "colors_contrasting": "boolean"
  }
}
```

---

## Required Skills (Hardcoded)

1. **Key Differentiator Parsing** - Parse concepts, features, and key differences
2. **Concept Header Generation** - Create colored concept header boxes
3. **Feature Row Rendering** - Generate parallel feature comparison rows
4. **Key Difference Highlighting** - Apply amber highlighting to key differences
5. **VS Separator Creation** - Add visual separator between concepts

---

## Key Differentiators Identification Conditions

Content should be KEY_DIFFERENTIATORS when:

1. **DIFFERENTIAL DIAGNOSIS** - Distinguishing similar disorders
2. **COMMONLY CONFUSED CONCEPTS** - Items frequently mistaken
3. **CRITICAL DISTINGUISHING FEATURES** - One feature determines classification
4. **NCLEX DISCRIMINATION ITEMS** - Content for discrimination questions
5. **SIDE-BY-SIDE COMPARISONS** - Mutually exclusive categories

DO NOT use key differentiators when:
- Concepts overlap significantly (use Venn diagram)
- Content is hierarchical (use hierarchy)
- Comparing many items at once (use table)
- Content is a process (use flowchart)

---

## Color Scheme (Contrasting Theme)

```
PRIMARY COLORS:
- Concept 1 Header: RGB(21, 101, 192) - Blue #1565C0
- Concept 2 Header: RGB(183, 28, 28) - Red #B71C1C
- Concept 1 Light: RGB(227, 242, 253) - Light Blue #E3F2FD
- Concept 2 Light: RGB(255, 235, 238) - Light Red #FFEBEE

DIFFERENTIATOR EMPHASIS:
- Key Difference Icon: RGB(255, 193, 7) - Amber #FFC107
- Key Difference Background: RGB(255, 243, 224) - Light Amber #FFF3E0
- Key Difference Border: RGB(255, 160, 0) - Orange #FFA000

THIRD CONCEPT (if needed):
- Concept 3 Header: RGB(27, 94, 32) - Green #1B5E20
- Concept 3 Light: RGB(232, 245, 233) - Light Green #E8F5E9

NEUTRAL COLORS:
- VS/Separator: RGB(97, 97, 97) - Dark Gray #616161
- Border Lines: RGB(189, 189, 189) - Medium Gray #BDBDBD
- Arrow/Indicator: RGB(0, 0, 0) - Black

TEXT COLORS:
- Header Text: RGB(255, 255, 255) - White
- Feature Text: RGB(0, 0, 0) - Black
- Key Difference Text: RGB(0, 0, 0) - Black (bold)
```

---

## Layout Specifications

### Layout A: Side-by-Side Comparison (2 concepts, 3-5 features)
```
+------------------------+   VS   +------------------------+
|     CONCEPT A          |        |     CONCEPT B          |
|    [Blue Header]       |        |    [Red Header]        |
+------------------------+        +------------------------+
| Feature 1: Description |        | Feature 1: Description |
+------------------------+        +------------------------+
| Feature 2: Description |        | Feature 2: Description |
+------------------------+        +------------------------+
|*KEY DIFFERENTIATOR *   |   !=   |*KEY DIFFERENTIATOR *   |
|   [Amber Highlight]    |        |   [Amber Highlight]    |
+------------------------+        +------------------------+
| Feature 4: Description |        | Feature 4: Description |
+------------------------+        +------------------------+

Dimensions:
- Each column: 5.5 inches wide
- Gap between: 1.0 inch (contains VS)
- Feature rows: 0.7-0.9 inches
- Key differentiator row: Amber highlighted
```

### Layout B: Centered Key Differentiator (Focus on single difference)
```
        +-----------------------------------+
        |      KEY DIFFERENTIATOR            |
        |   [The critical distinction]       |
        +-----------------------------------+
                        |
         +--------------+--------------+
         |                              |
         v                              v
+-----------------+           +-----------------+
|   CONCEPT A     |           |   CONCEPT B     |
| -------------- |           | -------------- |
| Because of X:   |           | Because of Y:   |
|  * Feature 1    |           |  * Feature 1    |
|  * Feature 2    |           |  * Feature 2    |
+-----------------+           +-----------------+

Dimensions:
- Key differentiator box: 8.0 x 1.2 inches (centered)
- Concept boxes: 4.5 x 3.0 inches each
```

### Layout C: Multiple Differentiators (2-4 key differences)
```
      CONCEPT A               CONCEPT B
+---------------------------------------------+
|    +----------+    X    +----------+        |
|    |  Value A |         |  Value B | Feature|
|    +----------+         +----------+        |
+---------------------------------------------+
|    +----------+    X    +----------+        |
|    |  Value A |         |  Value B | Feature|
|    +----------+         +----------+        |
+---------------------------------------------+

Dimensions:
- Full width: 11.0 inches
- Each row: 1.2 inches
- Value boxes: 3.5 x 0.8 inches
```

### Layout D: Three-Way Discrimination
```
                    +-----------+
                    | CONCEPT A |
                    |  (Blue)   |
                    +-----+-----+
                          |
         KEY DIFF --------+-------- KEY DIFF
         (A vs B)         |         (A vs C)
                          |
    +-----------+         |         +-----------+
    | CONCEPT B |         |         | CONCEPT C |
    |  (Red)    +---------+---------+  (Green)  |
    +-----------+    KEY DIFF       +-----------+
                     (B vs C)

Dimensions:
- Triangle arrangement
- Concept boxes: 3.0 x 1.5 inches
```

### Layout E: Feature Matrix (Multiple concepts, multiple features)
```
                    Concept A   Concept B   Concept C
                    ---------   ---------   ---------
Feature 1          |   check   |     X     |   check |
(Key Diff) *       | Duration  | <6 months | >=6 mo  |
Feature 2          |  Value    |   Value   |  Value  |
Feature 3          |  Value    |   Value   |  Value  |
--------------------------------------------------------

Dimensions:
- Header row: Bold with concept names
- Feature rows: Alternating light backgrounds
- Key differentiator row: Amber highlight
```

---

## Step-by-Step Instructions

### Step 1: Parse Key Differentiators Data
```python
def parse_key_differentiator_spec(spec_text):
    """Parse key differentiator specification."""

    data = {
        'layout': 'AUTO',
        'concepts': [],
        'features': [],
        'key_differences': []
    }

    # Extract layout
    layout_match = re.search(r'Layout:\s*([A-E])', spec_text)
    if layout_match:
        data['layout'] = layout_match.group(1)

    # Extract concepts
    concept_pattern = r'Concept\s*(\d+):\s*"([^"]+)"'
    for match in re.finditer(concept_pattern, spec_text):
        data['concepts'].append({
            'number': int(match.group(1)),
            'name': match.group(2),
            'color': 'blue' if int(match.group(1)) == 1 else 'red'
        })

    # Extract features with key flag
    feature_pattern = r'Feature:\s*"([^"]+)".*?Values:\s*\[([^\]]+)\].*?IS_KEY:\s*(Yes|No)'
    for match in re.finditer(feature_pattern, spec_text, re.DOTALL):
        values = [v.strip().strip('"') for v in match.group(2).split(',')]
        data['features'].append({
            'label': match.group(1),
            'values': values,
            'is_key': match.group(3).lower() == 'yes'
        })

    # Extract key differences explicitly listed
    kd_pattern = r'KD\d+:\s*"([^"]+)"'
    data['key_differences'] = re.findall(kd_pattern, spec_text)

    return data
```

### Step 2: Add Concept Header
```python
def add_concept_header(slide, left, top, width, height, name, color):
    """Add colored concept header box."""

    COLOR_MAP = {
        'blue': RGBColor(21, 101, 192),
        'red': RGBColor(183, 28, 28),
        'green': RGBColor(27, 94, 32)
    }

    header = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE,
        Inches(left), Inches(top), Inches(width), Inches(height)
    )
    header.fill.solid()
    header.fill.fore_color.rgb = COLOR_MAP.get(color, COLOR_MAP['blue'])

    tf = header.text_frame
    tf.paragraphs[0].text = name
    tf.paragraphs[0].font.size = Pt(24)
    tf.paragraphs[0].font.bold = True
    tf.paragraphs[0].font.name = 'Aptos'
    tf.paragraphs[0].font.color.rgb = RGBColor(255, 255, 255)
    tf.paragraphs[0].alignment = PP_ALIGN.CENTER

    return header
```

### Step 3: Add Feature Row
```python
def add_feature_row(slide, left, top, width, height, label, value, is_key, concept_color):
    """Add a feature row with optional key highlighting."""

    LIGHT_COLORS = {
        'blue': RGBColor(227, 242, 253),
        'red': RGBColor(255, 235, 238),
        'green': RGBColor(232, 245, 233)
    }

    # Use amber for key differentiator
    if is_key:
        bg_color = RGBColor(255, 243, 224)  # Light Amber
        border_color = RGBColor(255, 160, 0)  # Orange
        border_width = Pt(2)
    else:
        bg_color = LIGHT_COLORS.get(concept_color, LIGHT_COLORS['blue'])
        border_color = RGBColor(189, 189, 189)
        border_width = Pt(1)

    row = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE,
        Inches(left), Inches(top), Inches(width), Inches(height)
    )
    row.fill.solid()
    row.fill.fore_color.rgb = bg_color
    row.line.color.rgb = border_color
    row.line.width = border_width

    # Value text with optional key indicator
    display_text = f"{label}: {value}"
    if is_key:
        display_text = f"* {label}: {value} *"

    tf = row.text_frame
    tf.word_wrap = True
    tf.paragraphs[0].text = display_text
    tf.paragraphs[0].font.size = Pt(18)
    tf.paragraphs[0].font.bold = is_key
    tf.paragraphs[0].font.name = 'Aptos'
    tf.paragraphs[0].font.color.rgb = RGBColor(0, 0, 0)
    tf.paragraphs[0].alignment = PP_ALIGN.CENTER

    return row
```

### Step 4: Add VS Separator
```python
def add_vs_separator(slide, left, top, width, height):
    """Add VS separator between concepts."""

    textbox = slide.shapes.add_textbox(
        Inches(left), Inches(top), Inches(width), Inches(height)
    )
    tf = textbox.text_frame
    tf.paragraphs[0].text = "VS"
    tf.paragraphs[0].font.size = Pt(28)
    tf.paragraphs[0].font.bold = True
    tf.paragraphs[0].font.name = 'Aptos'
    tf.paragraphs[0].font.color.rgb = RGBColor(97, 97, 97)
    tf.paragraphs[0].alignment = PP_ALIGN.CENTER

    return textbox
```

### Step 5: Generate Layout A (Side-by-Side)
```python
def generate_layout_a(slide, kd_data):
    """Generate Layout A: Side-by-side comparison."""

    concepts = kd_data['concepts']
    features = kd_data['features']

    # Column dimensions
    col_width = 5.5
    gap = 1.0
    left_col_start = 0.9
    right_col_start = left_col_start + col_width + gap

    header_top = 1.5
    header_height = 0.8

    # Add concept headers
    for i, concept in enumerate(concepts[:2]):
        col_start = left_col_start if i == 0 else right_col_start
        add_concept_header(
            slide, col_start, header_top, col_width, header_height,
            concept['name'], concept.get('color', 'blue' if i == 0 else 'red')
        )

    # Add VS separator
    vs_left = left_col_start + col_width + 0.15
    add_vs_separator(slide, vs_left, header_top + 0.1, gap - 0.3, header_height)

    # Add feature rows
    row_top = header_top + header_height + 0.1
    row_height = 0.75

    for feature in features:
        is_key = feature.get('is_key', False)

        for j, concept in enumerate(concepts[:2]):
            col_start = left_col_start if j == 0 else right_col_start
            value = feature['values'][j] if j < len(feature['values']) else ''

            add_feature_row(
                slide, col_start, row_top, col_width, row_height,
                feature['label'], value, is_key,
                concept.get('color', 'blue' if j == 0 else 'red')
            )

        # Add != symbol between key differentiator rows
        if is_key:
            neq_left = left_col_start + col_width + 0.25
            neq_box = slide.shapes.add_textbox(
                Inches(neq_left), Inches(row_top),
                Inches(0.5), Inches(row_height)
            )
            tf = neq_box.text_frame
            tf.paragraphs[0].text = "!="
            tf.paragraphs[0].font.size = Pt(24)
            tf.paragraphs[0].font.bold = True
            tf.paragraphs[0].font.color.rgb = RGBColor(255, 160, 0)
            tf.paragraphs[0].alignment = PP_ALIGN.CENTER

        row_top += row_height + 0.05
```

### Step 6: Generate Layout B (Centered Key Diff)
```python
def generate_layout_b(slide, kd_data):
    """Generate Layout B: Single key differentiator emphasized at top."""

    concepts = kd_data['concepts']
    features = kd_data['features']

    # Find key differentiator
    key_diff = None
    for f in features:
        if f.get('is_key', False):
            key_diff = f
            break

    # Key differentiator box at top
    key_box_width = 8.0
    key_box_height = 1.2
    key_box_left = (13.33 - key_box_width) / 2
    key_box_top = 1.5

    key_box = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE,
        Inches(key_box_left), Inches(key_box_top),
        Inches(key_box_width), Inches(key_box_height)
    )
    key_box.fill.solid()
    key_box.fill.fore_color.rgb = RGBColor(255, 243, 224)  # Light Amber
    key_box.line.color.rgb = RGBColor(255, 160, 0)  # Orange
    key_box.line.width = Pt(3)

    if key_diff:
        tf = key_box.text_frame
        tf.paragraphs[0].text = f"KEY DIFFERENTIATOR: {key_diff['label']}"
        tf.paragraphs[0].font.size = Pt(22)
        tf.paragraphs[0].font.bold = True
        tf.paragraphs[0].font.name = 'Aptos'
        tf.paragraphs[0].font.color.rgb = RGBColor(0, 0, 0)
        tf.paragraphs[0].alignment = PP_ALIGN.CENTER

    # Concept boxes below
    concept_width = 4.5
    concept_height = 3.0
    concept_top = key_box_top + key_box_height + 0.8
    concept_spacing = 1.5

    COLOR_MAP = {
        'blue': (RGBColor(21, 101, 192), RGBColor(227, 242, 253)),
        'red': (RGBColor(183, 28, 28), RGBColor(255, 235, 238))
    }

    for i, concept in enumerate(concepts[:2]):
        if i == 0:
            concept_left = 13.33 / 2 - concept_width - concept_spacing / 2
        else:
            concept_left = 13.33 / 2 + concept_spacing / 2

        color = concept.get('color', 'blue' if i == 0 else 'red')
        header_color, bg_color = COLOR_MAP.get(color, COLOR_MAP['blue'])

        # Header
        header = slide.shapes.add_shape(
            MSO_SHAPE.RECTANGLE,
            Inches(concept_left), Inches(concept_top),
            Inches(concept_width), Inches(0.6)
        )
        header.fill.solid()
        header.fill.fore_color.rgb = header_color

        tf = header.text_frame
        tf.paragraphs[0].text = concept['name']
        tf.paragraphs[0].font.size = Pt(20)
        tf.paragraphs[0].font.bold = True
        tf.paragraphs[0].font.name = 'Aptos'
        tf.paragraphs[0].font.color.rgb = RGBColor(255, 255, 255)
        tf.paragraphs[0].alignment = PP_ALIGN.CENTER

        # Body with key diff value
        body = slide.shapes.add_shape(
            MSO_SHAPE.RECTANGLE,
            Inches(concept_left), Inches(concept_top + 0.6),
            Inches(concept_width), Inches(concept_height - 0.6)
        )
        body.fill.solid()
        body.fill.fore_color.rgb = bg_color

        if key_diff and i < len(key_diff['values']):
            tf = body.text_frame
            tf.paragraphs[0].text = key_diff['values'][i]
            tf.paragraphs[0].font.size = Pt(22)
            tf.paragraphs[0].font.bold = True
            tf.paragraphs[0].font.name = 'Aptos'
            tf.paragraphs[0].font.color.rgb = RGBColor(0, 0, 0)
            tf.paragraphs[0].alignment = PP_ALIGN.CENTER
```

---

## Character Limits

```
CONCEPT HEADER:
- Characters per line: 22
- Maximum lines: 2

FEATURE LABEL:
- Characters per line: 18
- Maximum lines: 1

FEATURE VALUE:
- Characters per line: 25
- Maximum lines: 2

KEY DIFFERENTIATOR VALUE:
- Characters per line: 28
- Maximum lines: 2

DIFFERENTIATOR EXPLANATION:
- Characters per line: 35
- Maximum lines: 2
```

---

## Validation Checklist

### Structure
- [ ] Layout selected (A/B/C/D/E) matches content
- [ ] At least one key differentiator identified
- [ ] Features parallel across concepts
- [ ] Concept count matches layout (2 for A-C, 3 for D, 2+ for E)

### Concept Styling
- [ ] Concept 1: Blue header (#1565C0), light blue rows
- [ ] Concept 2: Red header (#B71C1C), light red rows
- [ ] Concept 3 (if used): Green header (#1B5E20)
- [ ] Headers: 24pt bold white text

### Key Differentiator Highlighting
- [ ] Amber background (#FFF3E0) on key diff rows
- [ ] Orange border (#FFA000), 2pt width
- [ ] Star symbols (*) around key diff text
- [ ] != symbol between key diff columns (Layout A)

### Separator
- [ ] VS text: 28pt bold, dark gray (#616161)
- [ ] Positioned between concept columns

---

## Error Handling

| Error | Action |
|-------|--------|
| No clear key differentiator | Consider using table instead |
| Features not parallel | Reframe features to apply universally |
| Too many key differentiators (4+) | Limit to 1-2 most critical |
| Colors too similar | Use specified blue/red contrast |

---

## NCLEX Discrimination Strategy

Key Differentiators are especially valuable for commonly confused nursing concepts:

**Nursing Assessments:**
- Subjective vs Objective Data
- Primary vs Secondary Assessment
- Focused vs Comprehensive Assessment

**Medication Classifications:**
- ACE Inhibitors vs ARBs
- Opioid vs Non-opioid Analgesics
- Loop vs Thiazide Diuretics

**Clinical Conditions:**
- Type 1 vs Type 2 Diabetes
- Hyperthyroidism vs Hypothyroidism
- Systolic vs Diastolic Heart Failure

**Nursing Interventions:**
- Sterile vs Medical Aseptic Technique
- Isolation Precautions Types
- NG vs PEG Tube Feeding

---

**Agent Version:** 1.0
**Last Updated:** 2026-01-04
