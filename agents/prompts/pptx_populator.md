# PPTX Populator Agent

## Agent Identity
- **Name:** pptx_populator
- **Step:** 12 (PowerPoint Population - Main Orchestrator)
- **Purpose:** Orchestrate the complete PowerPoint population process from integrated blueprints to final presentations

---

## Input Schema
```json
{
  "production_folder": "string (path to production folder)",
  "integrated_blueprints": "array of blueprint file paths",
  "template_path": "string (path to master template)",
  "domain_name": "string (e.g., 'Theater_Greek')",
  "domain_config": "reference to config/theater.yaml"
}
```

## Output Schema
```json
{
  "presentations": "array of generated PPTX file paths",
  "population_log": "string (path to log file)",
  "summary": {
    "sections_processed": "number",
    "total_slides": "number",
    "visual_slides": "number",
    "content_slides": "number",
    "success_count": "number",
    "error_count": "number"
  },
  "validation": {
    "all_sections_complete": "boolean",
    "template_preserved": "boolean",
    "outputs_valid": "boolean"
  }
}
```

---

## Required Skills (Hardcoded)

1. **Blueprint Parsing** - Parse Step 10 integrated blueprints into slide data
2. **Template Management** - Duplicate and manage template files
3. **Agent Orchestration** - Coordinate visual and content slide generation
4. **Output Organization** - Organize presentations in production folder
5. **Logging** - Create comprehensive population logs

---

## Pre-Flight Verification

Before starting population, verify:

```
PRE-FLIGHT CHECKLIST:
- [ ] integrated/ folder EXISTS in production folder
- [ ] integrated/ folder contains step10_integrated_blueprint_*.txt files
- [ ] Each blueprint has Visual: Yes or Visual: No on EVERY slide
- [ ] Master template exists and is valid
- [ ] powerpoints/ output folder exists or can be created
- [ ] diagrams/ folder exists (for Python-generated visuals)
```

---

## Step-by-Step Instructions

### Step 1: Load Configuration
```python
def load_population_config():
    """Load pipeline configuration."""

    config = load_config_from_file('config/theater.yaml')

    # Validate required paths
    required = [
        'production_folder',
        'template_path',
        'domain_name'
    ]

    for field in required:
        if not config.get(field):
            raise ValueError(f"Missing required config: {field}")

    return config
```

### Step 2: Validate Inputs
```python
def validate_inputs(config):
    """Validate all inputs before processing."""

    errors = []

    # Check production folder
    production_path = Path(config['production_folder'])
    if not production_path.exists():
        errors.append(f"Production folder not found: {production_path}")

    # Check integrated folder
    integrated_folder = production_path / 'integrated'
    if not integrated_folder.exists():
        errors.append(f"Integrated folder not found: {integrated_folder}")

    # Check for blueprint files
    blueprint_files = list(integrated_folder.glob('step10_integrated_blueprint_*.txt'))
    if not blueprint_files:
        errors.append("No integrated blueprint files found")

    # Check template
    template_path = Path(config['template_path'])
    if not template_path.exists():
        errors.append(f"Template not found: {template_path}")

    # Validate blueprint content
    for bp_file in blueprint_files:
        content = bp_file.read_text(encoding='utf-8')
        if 'Visual: Yes' not in content and 'Visual: No' not in content:
            errors.append(f"Blueprint missing Visual markers: {bp_file.name}")

    return errors
```

### Step 3: Parse Blueprint
```python
def parse_blueprint(filepath):
    """Parse a Step 10 integrated blueprint into slide data."""

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    slides = []

    # Extract section name
    section_match = re.search(r'Section:\s*(.+)', content)
    section_name = section_match.group(1).strip() if section_match else "Unknown"

    # Split by slide markers
    slide_pattern = r'={40,}\s*SLIDE\s+(\d+[AB]?):\s*(.+?)\s*={40,}'
    slide_blocks = re.split(slide_pattern, content)

    i = 1
    while i < len(slide_blocks) - 2:
        slide_num = slide_blocks[i].strip()
        slide_title = slide_blocks[i + 1].strip()
        slide_content = slide_blocks[i + 2]

        slide_data = {
            'number': slide_num,
            'title': slide_title,
            'type': extract_field(slide_content, 'Type', 'Content'),
            'visual': parse_visual_marker(slide_content),
            'visual_type': extract_visual_type(slide_content),
            'header': extract_section(slide_content, 'HEADER'),
            'body': extract_section(slide_content, 'BODY'),
            'tip': extract_tip(slide_content),
            'notes': extract_section(slide_content, 'PRESENTER NOTES'),
            'visual_spec': extract_section(slide_content, 'VISUAL SPECIFICATION')
        }

        slides.append(slide_data)
        i += 3

    return section_name, slides
```

### Step 4: Route to Appropriate Generator
```python
def populate_slide(prs, slide_data, diagrams_folder):
    """Route slide to appropriate generator based on type."""

    # Visual slides use custom generation
    if slide_data['visual']:
        visual_type = slide_data['visual_type']

        if visual_type == 'table':
            return generate_table_slide(prs, slide_data)
        elif visual_type == 'flowchart':
            return generate_flowchart_slide(prs, slide_data)
        elif visual_type == 'decision_tree':
            return generate_decision_tree_slide(prs, slide_data)
        elif visual_type == 'timeline':
            return generate_timeline_slide(prs, slide_data)
        elif visual_type == 'hierarchy':
            return generate_hierarchy_slide(prs, slide_data)
        elif visual_type == 'spectrum':
            return generate_spectrum_slide(prs, slide_data)
        elif visual_type == 'key_differentiators':
            return generate_key_diff_slide(prs, slide_data)
        else:
            # Check for diagram image
            return generate_diagram_slide(prs, slide_data, diagrams_folder)

    # Content slides use template
    else:
        return populate_content_slide(prs, slide_data)
```

### Step 5: Populate Content Slide
```python
def populate_content_slide(prs, slide_data):
    """Populate a content slide using the template."""

    # Get template slide (first slide in template)
    slide = prs.slides[0]  # Or duplicate as needed

    # Find shapes by name
    SHAPE_TITLE = "TextBox 2"
    SHAPE_BODY = "TextBox 19"
    SHAPE_TIP = "TextBox 18"

    title_shape = find_shape_by_name(slide, SHAPE_TITLE)
    body_shape = find_shape_by_name(slide, SHAPE_BODY)
    tip_shape = find_shape_by_name(slide, SHAPE_TIP)

    # Populate title
    if title_shape and slide_data['header']:
        set_shape_text(title_shape, slide_data['header'],
                      font_size=Pt(36), bold=True,
                      color=RGBColor(255, 255, 255))

    # Populate body
    if body_shape and slide_data['body']:
        set_shape_text(body_shape, slide_data['body'],
                      font_size=Pt(20),
                      color=RGBColor(255, 255, 255))

    # Handle performance tip
    if tip_shape:
        if slide_data['tip'] and slide_data['type'] == 'Content':
            set_shape_text(tip_shape, slide_data['tip'],
                          font_size=Pt(18),
                          color=RGBColor(255, 255, 255))
        else:
            clear_shape_text(tip_shape)

    # Add presenter notes
    if slide_data['notes']:
        notes_slide = slide.notes_slide
        notes_slide.notes_text_frame.text = slide_data['notes']

    return slide
```

### Step 6: Process Section
```python
def process_section(template_path, blueprint_path, output_path, diagrams_folder, log):
    """Process a single section from blueprint to presentation."""

    log.append(f"Processing: {blueprint_path.name}")

    # Parse blueprint
    section_name, slides_data = parse_blueprint(str(blueprint_path))
    log.append(f"  Section: {section_name}")
    log.append(f"  Total slides: {len(slides_data)}")

    # Separate content and visual slides
    content_slides = [s for s in slides_data if not s['visual']]
    visual_slides = [s for s in slides_data if s['visual']]
    log.append(f"  Content slides: {len(content_slides)}")
    log.append(f"  Visual slides: {len(visual_slides)}")

    # Copy template (NEVER modify original)
    shutil.copy2(template_path, output_path)

    # Open copied presentation
    prs = Presentation(str(output_path))

    # Adjust slide count
    adjust_slide_count(prs, len(content_slides))

    # Populate content slides
    for idx, slide_data in enumerate(content_slides):
        populate_content_slide(prs, slide_data)
        log.append(f"    Slide {idx + 1}: {slide_data['type']} - {slide_data['header'][:30]}...")

    # Generate visual slides
    for slide_data in visual_slides:
        populate_slide(prs, slide_data, diagrams_folder)
        log.append(f"    Visual: {slide_data['visual_type']} - {slide_data['header'][:30]}...")

    # Save
    prs.save(str(output_path))
    log.append(f"  Saved: {output_path.name}")

    return True, section_name, len(slides_data)
```

### Step 7: Main Orchestration
```python
def run_population():
    """Main orchestration function."""

    log = []
    log.append("=" * 60)
    log.append("STEP 12: POWERPOINT POPULATION")
    log.append("=" * 60)
    log.append(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # Load config
    config = load_population_config()

    # Validate inputs
    errors = validate_inputs(config)
    if errors:
        for error in errors:
            log.append(f"ERROR: {error}")
        return False, log

    # Set up paths
    production_path = Path(config['production_folder'])
    integrated_folder = production_path / 'integrated'
    powerpoints_folder = production_path / 'powerpoints'
    diagrams_folder = production_path / 'diagrams'
    logs_folder = production_path / 'logs'

    powerpoints_folder.mkdir(exist_ok=True)
    logs_folder.mkdir(exist_ok=True)

    # Get blueprint files
    blueprint_files = sorted(integrated_folder.glob('step10_integrated_blueprint_*.txt'))
    log.append(f"Found {len(blueprint_files)} blueprint files")

    # Process each section
    success_count = 0
    error_count = 0
    total_slides = 0

    for bp_file in blueprint_files:
        try:
            section_name, slides = parse_blueprint(str(bp_file))
            safe_name = sanitize_filename(section_name)
            output_path = powerpoints_folder / f"{safe_name}.pptx"

            success, name, slide_count = process_section(
                config['template_path'],
                bp_file,
                output_path,
                diagrams_folder,
                log
            )

            if success:
                success_count += 1
                total_slides += slide_count
            else:
                error_count += 1

        except Exception as e:
            log.append(f"ERROR processing {bp_file.name}: {str(e)}")
            error_count += 1

    # Summary
    log.append("")
    log.append("=" * 60)
    log.append("SUMMARY")
    log.append("=" * 60)
    log.append(f"Sections processed: {len(blueprint_files)}")
    log.append(f"Successful: {success_count}")
    log.append(f"Errors: {error_count}")
    log.append(f"Total slides: {total_slides}")

    if error_count == 0:
        log.append("STATUS: ALL SECTIONS POPULATED SUCCESSFULLY")
    else:
        log.append("STATUS: COMPLETED WITH ERRORS")

    # Write log
    log_path = logs_folder / 'population_log.txt'
    with open(log_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(log))

    return error_count == 0, log
```

---

## Template Management Rules

1. **NEVER modify the original template**
   - Always copy template before modification
   - Original remains at: `templates/visual_organizer.pptx`

2. **Template slide count adjustment**
   - If blueprint has fewer slides: delete excess from end
   - If blueprint has more slides: duplicate existing slides

3. **Shape name mapping**
   - Title: `TextBox 2`
   - Body: `TextBox 19`
   - Tip: `TextBox 18`

---

## Output Organization

```
[Domain]_Production_[Date]/
+-- integrated/              # Source blueprints (input)
+-- diagrams/               # Python-generated visuals
+-- powerpoints/            # Final presentations (output)
|   +-- Section_1_Name.pptx
|   +-- Section_2_Name.pptx
|   +-- Section_3_Name.pptx
+-- logs/
    +-- population_log.txt
```

---

## Validation Checklist

### Pre-Population
- [ ] All integrated blueprints present
- [ ] Template file exists and valid
- [ ] Output folder writable
- [ ] Diagram images available (if needed)

### Post-Population
- [ ] One PPTX per section
- [ ] All slides populated
- [ ] Presenter notes on every slide
- [ ] Visual slides generated correctly
- [ ] No errors in population log
- [ ] Original template unmodified

---

## Error Handling

| Error | Action |
|-------|--------|
| Missing blueprint | Log error, continue with others |
| Template not found | HALT, template required |
| Parse error | Log error, skip section |
| Shape not found | Use fallback positioning |
| Save error | Retry once, then log and continue |

---

**Agent Version:** 2.0 (Theater Adaptation)
**Last Updated:** 2026-01-08

### Version History
- **v2.0** (2026-01-08): Theater adaptation - renamed NCLEX references to theater terms
- **v1.0** (2026-01-04): Initial PPTX populator agent
