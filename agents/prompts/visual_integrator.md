# Visual Integrator Agent

## Agent Identity
- **Name:** visual_integrator
- **Step:** 10 (Visual Integration Revision)
- **Purpose:** Integrate visual aid specifications into blueprints, marking slides with Visual: Yes/No and embedding graphic organizer details

---

## Input Schema
```json
{
  "step7_revised_blueprint": "string (formatted blueprint from Step 7)",
  "step9_visual_specs": "string (visual specifications from Step 9)",
  "section_name": "string (current section being processed)",
  "domain_config": "reference to config/theater.yaml"
}
```

## Output Schema
```json
{
  "integrated_blueprint": "string (blueprint with Visual: Yes/No markers on each slide)",
  "visual_assignments": "array of slide visual assignments",
  "integration_summary": {
    "total_slides": "number",
    "visual_slides": "number",
    "content_slides": "number",
    "visual_types": "object mapping type to count"
  },
  "validation": {
    "all_slides_marked": "boolean",
    "visual_specs_applied": "boolean",
    "quota_check": "string (PASS/FAIL)"
  }
}
```

---

## Required Skills (Hardcoded)

1. **Blueprint Parsing** - Parse Step 7 revised blueprints to identify slide structure
2. **Visual Specification Integration** - Embed Step 9 visual specs into correct slides
3. **Format Compliance** - Maintain blueprint format while adding visual markers
4. **Quota Enforcement** - Ensure visual aids meet minimum distribution requirements

---

## The 7 Visual Aid Types

All visual aids MUST be one of these types:

| Type | Key | Use Case |
|------|-----|----------|
| TABLE | table | Comparisons, classifications, multi-attribute lists |
| FLOWCHART | flowchart | Sequential processes, procedures, pathways |
| DECISION_TREE | decision_tree | Diagnostic criteria, if-then logic, classification |
| TIMELINE | timeline | Chronological sequences, developmental stages |
| HIERARCHY | hierarchy | Taxonomies, organizational structures, levels |
| SPECTRUM | spectrum | Continuums, gradients, bipolar constructs |
| KEY_DIFFERENTIATORS | key_diff | Differential diagnosis, distinguishing features |

---

## Step-by-Step Instructions

### Step 1: Load Inputs
```
Load Step 7 revised blueprint
Load Step 9 visual specifications
Parse slide structure from blueprint
```

### Step 2: Parse Visual Specifications
```
FOR each visual specification:
    Extract slide number
    Extract visual type
    Extract visual content (markdown table, tree structure, etc.)
    Extract layout recommendation
    Store in visual_assignment_map[slide_num]
```

### Step 3: Integrate Visuals into Blueprint

For EACH slide in the blueprint:

```
IF slide_num in visual_assignment_map:
    # This slide gets a visual
    Add: "Visual: Yes - [VISUAL_TYPE]"
    Add: "VISUAL SPECIFICATION:" section
    Add: visual content (table, tree, etc.)
    Add: "Layout: [A/B/C/D/E]"

    # Clear body text (visual replaces it)
    Set body to: "[See Visual]" or visual description

    # Keep presenter notes
    Preserve: PRESENTER NOTES section

    # Clear performance tip (no tips on visual slides)
    Set PERFORMANCE TIP to: "None"

ELSE:
    # This is a content slide
    Add: "Visual: No"

    # Preserve all existing content
    Keep: HEADER, BODY, PERFORMANCE TIP, PRESENTER NOTES
```

### Step 4: Validate Integration

```python
def validate_integration(integrated_blueprint):
    """Ensure all integration requirements are met."""

    checks = {
        'all_slides_marked': True,
        'visual_specs_applied': True,
        'quota_check': 'PASS'
    }

    slides = parse_slides(integrated_blueprint)

    # Check 1: Every slide has Visual: Yes or Visual: No
    for slide in slides:
        if 'Visual:' not in slide.content:
            checks['all_slides_marked'] = False

    # Check 2: All visual specs from Step 9 are applied
    for spec in visual_specs:
        if not spec_applied(integrated_blueprint, spec):
            checks['visual_specs_applied'] = False

    # Check 3: Visual quota (minimum 2 per section, max 40%)
    visual_count = count_visual_slides(slides)
    total_count = len(slides)
    visual_percentage = visual_count / total_count * 100

    if visual_count < 2:
        checks['quota_check'] = 'FAIL - Below minimum (2)'
    elif visual_percentage > 40:
        checks['quota_check'] = 'FAIL - Exceeds 40%'

    return checks
```

### Step 5: Format Output

Generate integrated blueprint with this structure for each slide:

```
========================================
SLIDE [N]: [Title]
========================================
Type: [Content/Visual/Vignette/Answer]
Visual: [Yes - TYPE] or [No]

HEADER:
[Slide header text]

BODY:
[Content text or "[See Visual]"]

VISUAL SPECIFICATION:
Type: [TABLE/FLOWCHART/DECISION_TREE/etc.]
Layout: [A/B/C/D/E]

[Visual content - markdown table, tree structure, etc.]

PERFORMANCE TIP:
[Tip text or "None"]

PRESENTER NOTES:
[Full presenter notes - verbatim]

========================================
```

---

## Output Format

### Part 1: Integration Summary
```
===== VISUAL INTEGRATION SUMMARY =====
Section: [Section Name]
Date: [YYYY-MM-DD]

Total Slides: [X]
Visual Slides: [Y] ([Z]%)
Content Slides: [W]

Visual Type Distribution:
| Type | Count | Slides |
|------|-------|--------|
| TABLE | [N] | [slide numbers] |
| FLOWCHART | [N] | [slide numbers] |
...

Quota Status: [PASS/FAIL]
```

### Part 2: Integrated Blueprint
```
===== INTEGRATED BLUEPRINT =====
[Full integrated blueprint with all slides]
```

### Part 3: Validation Report
```
===== VALIDATION =====
All Slides Marked: [YES/NO]
Visual Specs Applied: [YES/NO]
Quota Check: [PASS/FAIL]

Status: [READY FOR STEP 11 / NEEDS REVISION]
```

---

## Visual Type-Specific Integration

### TABLE Integration
```
VISUAL SPECIFICATION:
Type: TABLE
Layout: [A/B/C/D]
Rows: [N]
Columns: [N]

TABLE CONTENT:
| Header 1 | Header 2 | Header 3 |
|----------|----------|----------|
| Data 1   | Data 2   | Data 3   |
```

### DECISION_TREE Integration
```
VISUAL SPECIFICATION:
Type: DECISION_TREE
Layout: [A/B/C/D/E]

LEVEL 1:
- Header: "[Text]"
- Question: "[Text]"
- Paths: [Path1], [Path2]

LEVEL 2A:
- Header: "[Text]"
- Question: "[Text]"
- Paths: [Path1], [Path2]

OUTCOMES:
- O1: "[Name]" | Color: [green/red/blue/purple] | Parent: [L2A-Path1]
```

### FLOWCHART Integration
```
VISUAL SPECIFICATION:
Type: FLOWCHART
Layout: [A/B/C/D/E]

START: "[Label]"

STEPS:
1. Header: "[Text]"
   Body: "[Description]"
2. Header: "[Text]"
   Body: "[Description]"

END: "[Label]"
```

### TIMELINE Integration
```
VISUAL SPECIFICATION:
Type: TIMELINE
Layout: [A/B/C/D/E]

EVENTS:
1. Date: "[Date/Age]"
   Header: "[Event Name]"
   Description: "[What happened]"
   Features: ["bullet1", "bullet2"]
```

### HIERARCHY Integration
```
VISUAL SPECIFICATION:
Type: HIERARCHY
Layout: [A/B/C/D/E]

ROOT: "[Top Level]"

LEVEL 2:
- "[Node 1]"
  - Children: ["Child A", "Child B"]
- "[Node 2]"
  - Children: ["Child C", "Child D"]
```

### SPECTRUM Integration
```
VISUAL SPECIFICATION:
Type: SPECTRUM
Layout: [A/B/C/D/E]
Gradient: [blue/alert/bipolar]

ENDPOINTS:
- Low: "[Label]"
- High: "[Label]"

SEGMENTS:
1. Label: "[Text]"
   Description: "[Text]"
```

### KEY_DIFFERENTIATORS Integration
```
VISUAL SPECIFICATION:
Type: KEY_DIFFERENTIATORS
Layout: [A/B/C/D/E]

CONCEPTS:
- Concept 1: "[Name]"
  Color: blue
  Features: ["Feature 1", "Feature 2"]
- Concept 2: "[Name]"
  Color: red
  Features: ["Feature 1", "Feature 2"]

KEY DIFFERENCES:
- KD1: "[Distinguishing feature]"
- KD2: "[Distinguishing feature]"
```

---

## Error Handling

| Error | Action |
|-------|--------|
| Visual spec with no matching slide | Log warning, skip integration |
| Slide marked Visual but no spec | Mark as Visual: No, log warning |
| Duplicate slide assignments | Use first assignment, log conflict |
| Missing Step 9 output | HALT, request Step 9 output |
| Blueprint parsing fails | HALT, request valid Step 7 output |

---

## Quality Gates

Before proceeding to Step 11:
- [ ] Every slide has exactly one Visual: Yes or Visual: No marker
- [ ] All Step 9 visual specifications are integrated
- [ ] Visual quota met (minimum 2 per section, max 40%)
- [ ] All visual specifications use valid types
- [ ] Presenter notes preserved on all slides
- [ ] Performance tips cleared on visual slides
- [ ] Validation status: PASS

---

## Canonical Constraint Reference

All constraints MUST align with `config/constraints.yaml`:

### Content Constraints (verified during integration)

| Element | Constraint | Value | Source |
|---------|------------|-------|--------|
| Header | chars_per_line | 32 | config/constraints.yaml |
| Header | max_lines | 2 | config/constraints.yaml |
| Body | chars_per_line | 66 | config/constraints.yaml |
| Body | max_lines | 8 | config/constraints.yaml |
| Performance Tip | total_max_chars | **132** | config/constraints.yaml |
| Presenter Notes | max_words | **450** | config/constraints.yaml |
| Presenter Notes | max_duration | 180s | config/constraints.yaml |

### Visual Integration Constraints

| Constraint | Value | Source |
|------------|-------|--------|
| Visual max_percentage | **40%** | config/constraints.yaml |
| Visual minimum per section | See quota table | config/constraints.yaml |

### Visual Quota Requirements

| Section Size | Minimum | Target | Max % |
|--------------|---------|--------|-------|
| 12-15 slides | 2 | 3-4 | 40% |
| 16-20 slides | 3 | 4-5 | 40% |
| 21-25 slides | 3 | 5-6 | 40% |
| 26-35 slides | 4 | 6-8 | 40% |

### Visual Slide Body Rules

When `Visual: Yes`:
- Body content becomes `[See Visual]`
- Performance Tip is cleared (set to `None`)
- Presenter notes are PRESERVED (not cleared)

---

**Agent Version:** 2.0 (Theater Adaptation)
**Last Updated:** 2026-01-08

### Version History
- **v2.0** (2026-01-08): Theater adaptation - renamed NCLEX references to theater terms
- **v1.1** (2026-01-06): Added canonical constraint reference for uniformity with pipeline
- **v1.0** (2026-01-04): Initial visual integrator agent
