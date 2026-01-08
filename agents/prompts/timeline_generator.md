# Timeline Generator Agent

## Agent Identity
- **Name:** timeline_generator
- **Step:** 12 (PowerPoint Population - Timeline Generation)
- **Purpose:** Generate timeline visual aids for chronological sequences, developmental stages, and temporal progressions

---

## Input Schema
```json
{
  "slide_data": {
    "header": "string (slide title)",
    "visual_spec": "string (timeline specification)",
    "layout": "string (A/B/C/D/E or AUTO)",
    "events": "array of event objects",
    "start_label": "string (optional)",
    "end_label": "string (optional)",
    "presenter_notes": "string"
  },
  "template_path": "string (path to visual template)",
  "domain_config": "reference to config/theater.yaml"
}
```

## Output Schema
```json
{
  "slide": "PowerPoint slide object with timeline",
  "shapes": {
    "timeline_bar": "shape object",
    "event_markers": "array of marker shapes",
    "event_cards": "array of card shapes",
    "connectors": "array of connector shapes"
  },
  "metadata": {
    "layout": "string",
    "event_count": "number",
    "timeline_type": "string"
  },
  "validation": {
    "all_events_rendered": "boolean",
    "markers_aligned": "boolean",
    "colors_correct": "boolean"
  }
}
```

---

## Required Skills (Hardcoded)

1. **Timeline Structure Parsing** - Parse events, dates, and stages from specifications
2. **Timeline Bar Generation** - Create horizontal or vertical timeline bars
3. **Event Card Rendering** - Generate two-tone event cards with headers and descriptions
4. **Marker Creation** - Create event markers on timeline
5. **Connector Drawing** - Draw lines connecting markers to cards

---

## Timeline Identification Conditions

Content should be a TIMELINE when:

1. **CHRONOLOGICAL SEQUENCES** - Events ordered by time
2. **DEVELOPMENTAL STAGES** - Age-related or stage-based progressions
3. **DISEASE/DISORDER PROGRESSION** - How conditions evolve over time
4. **TREATMENT PHASES** - Therapeutic interventions across time
5. **HISTORICAL DEVELOPMENT** - Evolution of theories or practices

DO NOT use timeline when:
- Content is a process without time dimension (use flowchart)
- Content repeats cyclically (use cycle diagram)
- Content compares simultaneous events (use table)
- Content shows non-temporal cause-effect (use flowchart)

---

## Color Scheme (Purple/Violet Theme)

```
PRIMARY COLORS:
- Timeline Bar: RGB(74, 20, 140) - Deep Purple #4A148C
- Event Marker: RGB(123, 31, 162) - Purple #7B1FA2
- Event Card Background: RGB(243, 229, 245) - Light Purple #F3E5F5
- Event Card Border: RGB(74, 20, 140) - Deep Purple #4A148C

ACCENT COLORS:
- Start Marker: RGB(106, 27, 154) - Purple #6A1B9A
- End Marker: RGB(49, 27, 146) - Deep Indigo #311B92
- Connector Lines: RGB(149, 117, 205) - Medium Purple #9575CD
- Year/Date Text: RGB(74, 20, 140) - Deep Purple #4A148C

TEXT COLORS:
- Card Header: RGB(74, 20, 140) - Deep Purple
- Card Body: RGB(0, 0, 0) - Black
- Date Labels: RGB(255, 255, 255) - White (on markers)
```

---

## Layout Specifications

### Layout A: Horizontal Timeline (3-5 events)
```
                    [Event 2]         [Event 4]
                        |                 |
----@-------------@-----------@-----------@-------------@----
  START        [Event 1]   [Event 3]   [Event 5]       END

Dimensions:
- Timeline bar: 11.5 inches wide, centered
- Event markers: 0.3 inch diameter circles
- Event cards: 2.0 x 1.2 inches
- Cards alternate above/below line
```

### Layout B: Vertical Timeline (4-7 events)
```
@---- [Event 1: Description]
|
@---- [Event 2: Description]
|
@---- [Event 3: Description]
|
@---- [Event 4: Description]
|
@---- [Event 5: Description]

Dimensions:
- Timeline bar: Vertical, left-aligned at 1.5 inches
- Event cards: 4.5 x 0.9 inches
- Extends from markers to right
- Spacing: 0.8 inches between events
```

### Layout C: Horizontal with Era Blocks (3-4 eras)
```
+---------------+---------------+---------------+
|    Era 1      |    Era 2      |    Era 3      |
|  1900-1950    |  1950-1980    |  1980-2020    |
|    * Event    |    * Event    |    * Event    |
|    * Event    |    * Event    |    * Event    |
+---------------+---------------+---------------+

Dimensions:
- Era blocks: Equal width, ~3.8 inches each
- Total width: ~11.5 inches
- Height: 4.0 inches
- 2-4 bullet events per era
```

### Layout D: Developmental Stages (4-6 stages)
```
+---------+   +---------+   +---------+   +---------+
| Stage 1 |-> | Stage 2 |-> | Stage 3 |-> | Stage 4 |
| Age 0-2 |   | Age 2-7 |   | Age 7-11|   | Age 11+ |
+---------+   +---------+   +---------+   +---------+
|Features |   |Features |   |Features |   |Features |
|  * xxx  |   |  * xxx  |   |  * xxx  |   |  * xxx  |
|  * xxx  |   |  * xxx  |   |  * xxx  |   |  * xxx  |
+---------+   +---------+   +---------+   +---------+

Dimensions:
- Stage boxes: 2.5 x 3.5 inches
- Header height: 0.8 inches
- Age band: 0.4 inches
- Feature area: 2.3 inches
```

### Layout E: Milestone Timeline (5-8 milestones)
```
     @          @          @          @          @
     |          |          |          |          |
-----+----------+----------+----------+----------+-----
    1905       1916       1939       1955       1969
   Label     Label      Label      Label      Label
   -----     -----      -----      -----      -----
   Desc      Desc       Desc       Desc       Desc

Dimensions:
- Timeline bar: Full width with date markers
- Milestone labels above/below alternating
- Short description under each date
```

---

## Step-by-Step Instructions

### Step 1: Parse Timeline Data
```python
def parse_timeline_spec(spec_text):
    """Parse timeline specification."""

    data = {
        'layout': 'AUTO',
        'events': [],
        'start_label': 'START',
        'end_label': 'END'
    }

    # Extract layout
    layout_match = re.search(r'Layout:\s*([A-E])', spec_text)
    if layout_match:
        data['layout'] = layout_match.group(1)

    # Extract events
    event_pattern = r'(\d+)\.\s*(?:Header:|Label:)\s*"([^"]+)".*?(?:Date:|Age:)\s*"([^"]+)"'
    for match in re.finditer(event_pattern, spec_text, re.DOTALL):
        data['events'].append({
            'number': int(match.group(1)),
            'header': match.group(2),
            'date': match.group(3)
        })

    # Extract features for developmental stages
    feature_pattern = r'Features:\s*\[([^\]]+)\]'
    for i, match in enumerate(re.finditer(feature_pattern, spec_text)):
        if i < len(data['events']):
            features = [f.strip().strip('"') for f in match.group(1).split(',')]
            data['events'][i]['features'] = features

    return data
```

### Step 2: Add Timeline Bar
```python
def add_timeline_bar(slide, is_horizontal=True):
    """Add the main timeline bar."""

    if is_horizontal:
        bar_left = Inches(0.9)
        bar_width = Inches(11.5)
        bar_top = Inches(3.8)
        bar_height = Inches(0.08)
    else:
        bar_left = Inches(1.5)
        bar_width = Inches(0.08)
        bar_top = Inches(1.5)
        bar_height = Inches(5.0)

    bar = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE,
        bar_left, bar_top, bar_width, bar_height
    )
    bar.fill.solid()
    bar.fill.fore_color.rgb = RGBColor(74, 20, 140)  # Deep Purple
    bar.line.fill.background()

    return bar
```

### Step 3: Add Event Marker
```python
def add_event_marker(slide, left, top, size=0.3):
    """Add circular event marker on timeline."""

    marker = slide.shapes.add_shape(
        MSO_SHAPE.OVAL,
        Inches(left), Inches(top),
        Inches(size), Inches(size)
    )
    marker.fill.solid()
    marker.fill.fore_color.rgb = RGBColor(123, 31, 162)  # Purple
    marker.line.fill.background()

    return marker
```

### Step 4: Add Event Card
```python
def add_event_card(slide, left, top, width, height, header, date, description=None):
    """Add event card with header, date, and optional description."""

    # Card background
    card = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE,
        Inches(left), Inches(top), Inches(width), Inches(height)
    )
    card.fill.solid()
    card.fill.fore_color.rgb = RGBColor(243, 229, 245)  # Light Purple
    card.line.color.rgb = RGBColor(74, 20, 140)  # Deep Purple
    card.line.width = Pt(1.5)

    # Header text box
    header_height = height * 0.35
    header_box = slide.shapes.add_textbox(
        Inches(left), Inches(top), Inches(width), Inches(header_height)
    )
    tf = header_box.text_frame
    tf.paragraphs[0].text = header
    tf.paragraphs[0].font.size = Pt(18)
    tf.paragraphs[0].font.bold = True
    tf.paragraphs[0].font.name = 'Aptos'
    tf.paragraphs[0].font.color.rgb = RGBColor(74, 20, 140)
    tf.paragraphs[0].alignment = PP_ALIGN.CENTER

    # Date text
    if date:
        date_top = top + header_height * 0.8
        date_box = slide.shapes.add_textbox(
            Inches(left), Inches(date_top), Inches(width), Inches(0.3)
        )
        tf = date_box.text_frame
        tf.paragraphs[0].text = date
        tf.paragraphs[0].font.size = Pt(18)
        tf.paragraphs[0].font.italic = True
        tf.paragraphs[0].font.name = 'Aptos'
        tf.paragraphs[0].font.color.rgb = RGBColor(123, 31, 162)
        tf.paragraphs[0].alignment = PP_ALIGN.CENTER

    return card
```

### Step 5: Generate Layout A (Horizontal)
```python
def generate_layout_a(slide, timeline_data):
    """Generate Layout A: Horizontal Timeline (3-5 events)."""

    events = timeline_data['events']
    event_count = len(events)

    # Add timeline bar
    bar_left, bar_width = 0.9, 11.5
    bar_top = 3.8
    add_timeline_bar(slide, is_horizontal=True)

    # Calculate marker positions
    spacing = bar_width / (event_count + 1)

    for i, event in enumerate(events):
        # Marker position
        marker_x = bar_left + spacing * (i + 1) - 0.15

        # Add marker
        add_event_marker(slide, marker_x, bar_top - 0.11)

        # Alternate card position above/below
        if i % 2 == 0:  # Above
            card_top = bar_top - 1.8
        else:  # Below
            card_top = bar_top + 0.5

        # Add connector line
        connector = slide.shapes.add_connector(
            MSO_CONNECTOR.STRAIGHT,
            Inches(marker_x + 0.15),
            Inches(bar_top - 0.11 if i % 2 == 0 else bar_top + 0.19),
            Inches(marker_x + 0.15),
            Inches(card_top + 1.2 if i % 2 == 0 else card_top)
        )
        connector.line.color.rgb = RGBColor(149, 117, 205)
        connector.line.width = Pt(1.5)

        # Add event card
        card_left = marker_x + 0.15 - 1.0  # Center card on marker
        add_event_card(
            slide, card_left, card_top, 2.0, 1.2,
            event['header'], event.get('date', ''),
            event.get('description', '')
        )
```

### Step 6: Generate Layout D (Developmental Stages)
```python
def generate_layout_d(slide, timeline_data):
    """Generate Layout D: Developmental stage boxes."""

    stages = timeline_data['events']
    stage_count = len(stages)

    # Calculate box dimensions
    total_width = 11.5
    spacing = 0.3
    box_width = (total_width - spacing * (stage_count - 1)) / stage_count
    box_height = 3.5

    start_left = 0.9
    top = 1.8

    for i, stage in enumerate(stages):
        left = start_left + i * (box_width + spacing)

        # Stage header (purple background)
        header_height = 0.7
        header = slide.shapes.add_shape(
            MSO_SHAPE.RECTANGLE,
            Inches(left), Inches(top),
            Inches(box_width), Inches(header_height)
        )
        header.fill.solid()
        header.fill.fore_color.rgb = RGBColor(74, 20, 140)

        tf = header.text_frame
        tf.paragraphs[0].text = stage['header']
        tf.paragraphs[0].font.size = Pt(20)
        tf.paragraphs[0].font.bold = True
        tf.paragraphs[0].font.name = 'Aptos'
        tf.paragraphs[0].font.color.rgb = RGBColor(255, 255, 255)
        tf.paragraphs[0].alignment = PP_ALIGN.CENTER

        # Age band (medium purple)
        age_top = top + header_height
        age_height = 0.4
        age_band = slide.shapes.add_shape(
            MSO_SHAPE.RECTANGLE,
            Inches(left), Inches(age_top),
            Inches(box_width), Inches(age_height)
        )
        age_band.fill.solid()
        age_band.fill.fore_color.rgb = RGBColor(123, 31, 162)

        tf = age_band.text_frame
        tf.paragraphs[0].text = stage.get('date', '')
        tf.paragraphs[0].font.size = Pt(18)
        tf.paragraphs[0].font.bold = True
        tf.paragraphs[0].font.name = 'Aptos'
        tf.paragraphs[0].font.color.rgb = RGBColor(255, 255, 255)
        tf.paragraphs[0].alignment = PP_ALIGN.CENTER

        # Features area (light purple)
        features_top = age_top + age_height
        features_height = box_height - header_height - age_height
        features_box = slide.shapes.add_shape(
            MSO_SHAPE.RECTANGLE,
            Inches(left), Inches(features_top),
            Inches(box_width), Inches(features_height)
        )
        features_box.fill.solid()
        features_box.fill.fore_color.rgb = RGBColor(243, 229, 245)
        features_box.line.color.rgb = RGBColor(74, 20, 140)

        # Add feature bullets
        if 'features' in stage:
            text_box = slide.shapes.add_textbox(
                Inches(left + 0.1), Inches(features_top + 0.1),
                Inches(box_width - 0.2), Inches(features_height - 0.2)
            )
            tf = text_box.text_frame
            tf.word_wrap = True

            for j, feature in enumerate(stage['features']):
                if j == 0:
                    tf.paragraphs[0].text = "* " + feature
                else:
                    p = tf.add_paragraph()
                    p.text = "* " + feature
                p = tf.paragraphs[j]
                p.font.size = Pt(18)
                p.font.name = 'Aptos'
                p.font.color.rgb = RGBColor(0, 0, 0)
```

---

## Character Limits

```
ERA/STAGE HEADER:
- Characters per line: 20
- Maximum lines: 1

DATE/AGE LABEL:
- Characters: 15 max (e.g., "1900-1950", "Age 2-7")

EVENT CARD HEADER:
- Characters per line: 22
- Maximum lines: 1

EVENT CARD BODY:
- Characters per line: 28
- Maximum lines: 2

MILESTONE NAME:
- Characters: 15 max

MILESTONE DESCRIPTION:
- Characters per line: 20
- Maximum lines: 2
```

---

## Validation Checklist

### Structure
- [ ] Layout selected (A/B/C/D/E) matches content
- [ ] Event count within layout capacity
- [ ] Events in chronological order
- [ ] All dates/ages labeled

### Timeline Elements
- [ ] Timeline bar: Deep purple, correct orientation
- [ ] Markers: Purple circles on timeline
- [ ] Cards: Light purple with dark purple border
- [ ] Connectors: Medium purple lines

### Text Styling
- [ ] Headers: 18-20pt bold, Deep Purple
- [ ] Dates: 18pt italic, Medium Purple
- [ ] Body: 18pt regular, Black
- [ ] All text minimum 18pt

---

## Error Handling

| Error | Action |
|-------|--------|
| More than 8 events | Split across multiple slides |
| Layout not specified | Auto-detect based on event count |
| Missing date/age | Use placeholder or derive from context |
| Events not chronological | Log warning, preserve order |

---

**Agent Version:** 2.0 (Theater Adaptation)
**Last Updated:** 2026-01-08

### Version History
- **v2.0** (2026-01-08): Adapted for theater pipeline - config/nclex.yaml -> config/theater.yaml
- **v1.0** (2026-01-04): Initial timeline generator agent
