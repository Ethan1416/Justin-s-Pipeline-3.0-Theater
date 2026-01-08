# Sub-Orchestrator: PowerPoint Pipeline

**Version:** 1.0
**Purpose:** Handle PowerPoint assembly from integrated blueprints and generated visuals
**Parent:** `lecture_pipeline.md`

---

## Overview

The PowerPoint Pipeline orchestrates the final assembly of PowerPoint presentations from integrated blueprints and generated visual content. It handles template population, shape rendering, text formatting, and final validation.

---

## Agents Managed

### Primary Assembly Agents

| Agent | Purpose | Input Schema | Output Schema |
|-------|---------|--------------|---------------|
| pptx_populator | Populate PowerPoint templates | pptx_input.schema.json | pptx_output.schema.json |
| slide_assembler | Assemble final slides | assemble_input.schema.json | assemble_output.schema.json |
| final_validator | Final output validation | final_input.schema.json | final_output.schema.json |

### Rendering Agents

| Agent | Purpose | Input Schema | Output Schema |
|-------|---------|--------------|---------------|
| shape_renderer | Render shapes/visuals | shape_input.schema.json | shape_output.schema.json |
| text_formatter | Format text content | text_input.schema.json | text_output.schema.json |
| color_applier | Apply color schemes | color_input.schema.json | color_output.schema.json |
| position_calculator | Calculate element positions | position_input.schema.json | position_output.schema.json |
| connector_drawer | Draw connectors/arrows | connector_input.schema.json | connector_output.schema.json |

---

## Skill Assignments

```yaml
agents:
  pptx_populator:
    skills:
      - skill: step12_powerpoint_population
        path: skills/generation/step12_powerpoint_population.py
        purpose: Main PowerPoint population logic
      - skill: template_loader
        path: skills/utilities/template_loader.py
        purpose: Load PowerPoint templates
      - skill: shape_mapper
        path: skills/utilities/shape_mapper.py
        purpose: Map content to template shapes

  slide_assembler:
    skills:
      - skill: slide_builder
        path: skills/generation/pptx_slide_builder.py
        purpose: Build individual slides
      - skill: content_placer
        path: skills/generation/content_placer.py
        purpose: Place content in slide regions
      - skill: visual_inserter
        path: skills/generation/visual_inserter.py
        purpose: Insert visual graphics into slides

  shape_renderer:
    skills:
      - skill: table_renderer
        path: skills/generation/renderers/table_renderer.py
        purpose: Render table shapes
      - skill: flowchart_renderer
        path: skills/generation/renderers/flowchart_renderer.py
        purpose: Render flowchart shapes
      - skill: dtree_renderer
        path: skills/generation/renderers/dtree_renderer.py
        purpose: Render decision tree shapes
      - skill: timeline_renderer
        path: skills/generation/renderers/timeline_renderer.py
        purpose: Render timeline shapes
      - skill: hierarchy_renderer
        path: skills/generation/renderers/hierarchy_renderer.py
        purpose: Render hierarchy shapes
      - skill: spectrum_renderer
        path: skills/generation/renderers/spectrum_renderer.py
        purpose: Render spectrum shapes
      - skill: keydiff_renderer
        path: skills/generation/renderers/keydiff_renderer.py
        purpose: Render key differentiator shapes

  text_formatter:
    skills:
      - skill: font_applier
        path: skills/utilities/font_applier.py
        purpose: Apply font settings
      - skill: text_fitter
        path: skills/utilities/text_fitter.py
        purpose: Fit text within shape bounds
      - skill: bullet_renderer
        path: skills/utilities/bullet_renderer.py
        purpose: Render bullet point formatting

  color_applier:
    skills:
      - skill: theme_loader
        path: skills/utilities/theme_loader.py
        purpose: Load domain color themes
      - skill: rgb_converter
        path: skills/utilities/rgb_converter.py
        purpose: Convert RGB to PowerPoint colors
      - skill: gradient_generator
        path: skills/utilities/gradient_generator.py
        purpose: Generate gradient fills

  position_calculator:
    skills:
      - skill: layout_calculator
        path: skills/utilities/layout_calculator.py
        purpose: Calculate layout positions
      - skill: bounds_checker
        path: skills/utilities/bounds_checker.py
        purpose: Check shape bounds
      - skill: spacing_optimizer
        path: skills/utilities/spacing_optimizer.py
        purpose: Optimize spacing between elements

  connector_drawer:
    skills:
      - skill: arrow_renderer
        path: skills/utilities/arrow_renderer.py
        purpose: Render arrows and connectors
      - skill: path_calculator
        path: skills/utilities/path_calculator.py
        purpose: Calculate connector paths
      - skill: elbow_connector
        path: skills/utilities/elbow_connector.py
        purpose: Create elbow connectors

  final_validator:
    skills:
      - skill: pptx_validator
        path: skills/validation/pptx_validator.py
        purpose: Validate PowerPoint file integrity
      - skill: content_checker
        path: skills/validation/content_checker.py
        purpose: Verify all content is present
      - skill: visual_checker
        path: skills/validation/visual_checker.py
        purpose: Verify all visuals rendered correctly
```

---

## Execution Order

```
POWERPOINT ASSEMBLY PIPELINE
│
├── Phase 1: PREPARATION
│   ├── Load template: templates/content_master.pptx
│   ├── Load integrated blueprints from outputs/integrated/
│   └── Load generated visuals from outputs/visuals/
│
├── Phase 2: SLIDE GENERATION (per section)
│   │
│   └── FOR EACH section:
│       │
│       ├── Step 1: Initialize Section
│       │   ├── Agent: pptx_populator
│       │   ├── Skills: template_loader, shape_mapper
│       │   └── Output: Section slide deck initialized
│       │
│       ├── Step 2: Process Each Slide
│       │   │
│       │   └── FOR EACH slide in blueprint:
│       │       │
│       │       ├── 2a: Text Population
│       │       │   ├── Agent: text_formatter
│       │       │   ├── Skills: font_applier, text_fitter, bullet_renderer
│       │       │   ├── Populate: Title, Body, Tip
│       │       │   └── Apply: Domain colors via color_applier
│       │       │
│       │       ├── 2b: Visual Rendering (if Visual: Yes)
│       │       │   ├── Agent: shape_renderer
│       │       │   ├── Route to type-specific renderer
│       │       │   ├── Agent: position_calculator
│       │       │   ├── Agent: connector_drawer (if needed)
│       │       │   └── Output: Visual shapes added to slide
│       │       │
│       │       └── 2c: Slide Assembly
│       │           ├── Agent: slide_assembler
│       │           └── Output: Complete slide
│       │
│       └── Step 3: Section Finalization
│           ├── Add presenter notes
│           └── Save section PowerPoint
│
├── Phase 3: VALIDATION
│   ├── Agent: final_validator
│   ├── Checks:
│   │   ├── All slides present
│   │   ├── All visuals rendered
│   │   ├── All text within bounds
│   │   ├── File integrity
│   │   └── Schema compliance
│   └── Output: Validation report
│
└── OUTPUT: Final PowerPoint files
```

---

## Input Schema Contract

```yaml
input:
  type: object
  required:
    - run_id
    - integrated_blueprints
    - visual_data
    - domain
  properties:
    run_id:
      type: string
    domain:
      type: string
      enum: [fundamentals, pharmacology, medical_surgical, ob_maternity, pediatric, mental_health]
    integrated_blueprints:
      type: array
      items:
        type: object
        required:
          - section_number
          - section_name
          - blueprint_path
        properties:
          section_number:
            type: integer
          section_name:
            type: string
          blueprint_path:
            type: string
            description: Path to step10_integrated file
    visual_data:
      type: array
      items:
        type: object
        required:
          - section_number
          - slide_number
          - visual_path
        properties:
          section_number:
            type: integer
          slide_number:
            type: integer
          visual_path:
            type: string
            description: Path to generated visual JSON
    template:
      type: string
      default: templates/content_master.pptx
```

---

## Output Schema Contract

```yaml
output:
  type: object
  required:
    - run_id
    - powerpoints
    - validation_status
  properties:
    run_id:
      type: string
    powerpoints:
      type: array
      items:
        type: object
        required:
          - section_number
          - section_name
          - file_path
          - slide_count
          - visual_count
        properties:
          section_number:
            type: integer
          section_name:
            type: string
          file_path:
            type: string
          slide_count:
            type: integer
          visual_count:
            type: integer
    validation_status:
      type: string
      enum: [PASS, FAIL, PARTIAL]
    validation_report:
      type: object
      properties:
        total_slides:
          type: integer
        total_visuals:
          type: integer
        issues:
          type: array
          items:
            type: object
            properties:
              section:
                type: integer
              slide:
                type: integer
              issue:
                type: string
              severity:
                type: string
                enum: [error, warning, info]
    statistics:
      type: object
      properties:
        generation_time_seconds:
          type: number
        file_sizes_bytes:
          type: object
          additionalProperties:
            type: integer
```

---

## Template Shape Mappings

From `config/visuals.yaml`:

```yaml
shape_mappings:
  required_shapes:
    - "TextBox 2"    # Title
    - "TextBox 19"   # Body
    - "TextBox 18"   # Tip

  mappings:
    "TextBox 2": "title"
    "TextBox 19": "body"
    "TextBox 18": "tip"

slide_dimensions:
  width_inches: 13.33
  height_inches: 7.5
```

---

## Visual Rendering Configuration

### Positioning (from config/visuals.yaml)

```yaml
visual_positions:
  table:
    left_inches: 0.5
    top_inches: 1.8
    width_inches: 12.3
    max_height_inches: 4.5

  # Other visuals use dynamic positioning based on content
  flowchart:
    margin_inches: 0.5
    connector_clearance: 0.2

  decision_tree:
    margin_inches: 0.5
    level_spacing_inches: 1.2

  timeline:
    bar_height_inches: 0.3
    card_width_inches: 1.8

  hierarchy:
    margin_inches: 0.5
    level_spacing_inches: 1.0

  spectrum:
    bar_height_inches: 0.6
    margin_inches: 0.5

  key_differentiators:
    margin_inches: 0.5
    separator_width_inches: 0.1
```

### Font Settings

```yaml
fonts:
  default:
    font_name: "Aptos"
    min_font_size_pt: 18

  title:
    font_size_pt: 36
    font_color_rgb: [255, 255, 255]
    bold: true

  body:
    font_size_pt: 20
    font_color_rgb: [0, 0, 0]
    bold: false

  tip:
    font_size_pt: 20
    font_color_rgb: [0, 0, 0]
    bold: false
```

### Domain Color Themes

```yaml
domain_colors:
  fundamentals:
    primary_rgb: [0, 102, 68]
    secondary_rgb: [232, 245, 233]

  pharmacology:
    primary_rgb: [25, 118, 210]
    secondary_rgb: [227, 242, 253]

  medical_surgical:
    primary_rgb: [198, 40, 40]
    secondary_rgb: [255, 235, 238]

  ob_maternity:
    primary_rgb: [255, 143, 0]
    secondary_rgb: [255, 243, 224]

  pediatric:
    primary_rgb: [0, 150, 136]
    secondary_rgb: [224, 242, 241]

  mental_health:
    primary_rgb: [106, 27, 154]
    secondary_rgb: [243, 229, 245]
```

---

## Error Handling Procedures

### Phase-Specific Errors

```yaml
preparation_errors:
  - error: TEMPLATE_NOT_FOUND
    action: Halt - template is required
  - error: BLUEPRINT_NOT_FOUND
    action: Skip section with warning
  - error: VISUAL_DATA_MISSING
    action: Continue without visual, log warning

slide_generation_errors:
  - error: SHAPE_NOT_FOUND
    action: Use fallback positioning
  - error: TEXT_OVERFLOW
    action: Apply font scaling, min 18pt
  - error: VISUAL_RENDER_FAILURE
    action: Retry once, then skip with placeholder

validation_errors:
  - error: MISSING_SLIDES
    action: Log critical error, mark FAIL
  - error: MISSING_VISUALS
    action: Log warning, mark PARTIAL
  - error: CORRUPTION_DETECTED
    action: Regenerate section
```

### Recovery Protocol

```
1. ON_SLIDE_ERROR:
   a. Log error with slide context
   b. Attempt recovery (font scaling, repositioning)
   c. If unrecoverable, skip slide with placeholder
   d. Continue processing

2. ON_SECTION_ERROR:
   a. Log error with section context
   b. Attempt section regeneration (max 2 attempts)
   c. If unrecoverable, save partial section
   d. Mark section as PARTIAL in output

3. POST_GENERATION:
   a. Run final_validator
   b. Generate validation report
   c. Flag any issues for manual review
```

---

## Output Files Generated

| Type | Output Pattern | Example |
|------|----------------|---------|
| PowerPoint | `outputs/powerpoints/Section_{num}_{name}.pptx` | Section_01_Cardiovascular_Assessment.pptx |
| Validation | `outputs/logs/pptx_validation_{run_id}.json` | pptx_validation_run_20260104_143000.json |
| Error Log | `outputs/logs/pptx_errors_{run_id}.log` | pptx_errors_run_20260104_143000.log |

---

## Pre-Flight Checklist

Before PowerPoint generation, verify:

```yaml
pre_flight_checks:
  - check: integrated_blueprints_exist
    path: outputs/integrated/
    pattern: step10_integrated_*.txt
    required: true

  - check: visual_data_exists
    path: outputs/visuals/
    pattern: section_*_slide_*_*.json
    required: false  # Slides may not have visuals

  - check: template_exists
    path: templates/content_master.pptx
    required: true

  - check: all_qa_passed
    verify: All step8 scores >= 90
    required: true

  - check: all_visual_quotas_met
    verify: All step9 quota status = PASS
    required: true
```

---

## Quality Validation Criteria

### Final Output Checks

| Check | Requirement | Severity |
|-------|-------------|----------|
| Slide Count | Matches blueprint | Error |
| Visual Count | Matches visual markers | Error |
| Text Bounds | All text within shapes | Warning |
| Font Size | >= 18pt minimum | Warning |
| File Integrity | Valid .pptx structure | Error |
| Presenter Notes | Present on all slides | Warning |

---

## Configuration References

```yaml
configs_used:
  - file: config/pipeline.yaml
    sections:
      - templates
      - output_patterns.step_12_powerpoint
      - output_patterns.step_12_diagrams

  - file: config/visuals.yaml
    sections:
      - slide_dimensions
      - shape_mappings
      - fonts
      - table, flowchart, decision_tree, timeline, hierarchy, spectrum, key_differentiators

  - file: config/nclex.yaml
    sections:
      - content.domains (for colors)
```

---

## Version History

- **v1.0** (2026-01-04): Initial PowerPoint orchestrator configuration
