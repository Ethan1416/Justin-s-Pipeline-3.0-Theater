# Visual Quota Checker Agent

## Agent Identity
- **Name:** visual_quota_checker
- **Step:** 8 (Quality Assurance - Visual Quota Verification)
- **Purpose:** Verify that sections meet minimum visual requirements based on slide count from constraints.yaml

---

## Input Schema
```json
{
  "blueprint": "string (blueprint content to validate)",
  "section_name": "string (current section name)",
  "constraints_config": "reference to config/constraints.yaml"
}
```

## Output Schema
```json
{
  "validation_status": "string (PASS/FAIL)",
  "section_name": "string",
  "slide_count": "number",
  "size_category": "string (12-15/16-20/21-25/26-35)",
  "visual_count": "number",
  "required_minimum": "number",
  "target_range": {
    "min": "number",
    "max": "number"
  },
  "meets_minimum": "boolean",
  "meets_target": "boolean",
  "visual_breakdown": {
    "TABLE": "number",
    "FLOWCHART": "number",
    "DECISION_TREE": "number",
    "TIMELINE": "number",
    "HIERARCHY": "number",
    "SPECTRUM": "number",
    "KEY_DIFFERENTIATORS": "number"
  },
  "visual_slides": [
    {
      "slide_number": "number",
      "visual_type": "string",
      "has_specification": "boolean"
    }
  ],
  "deficit": "number (negative if below minimum, 0 if met)",
  "recommendations": "array of strings"
}
```

---

## Required Skills (Hardcoded)

1. **visual_counting** - Count and categorize visual slides by type
2. **quota_comparison** - Compare counts against section-size-based quotas
3. **status_reporting** - Generate pass/fail status with detailed breakdown

---

## Validation Rules

### Visual Quotas by Section Size (from constraints.yaml)

| Section Size | Minimum | Target Min | Target Max |
|--------------|---------|------------|------------|
| 12-15 slides | 2 | 3 | 4 |
| 16-20 slides | 3 | 4 | 5 |
| 21-25 slides | 3 | 5 | 6 |
| 26-35 slides | 4 | 6 | 8 |

### Visual Types Recognized

1. **TABLE** - Comparison tables
2. **FLOWCHART** - Process flowcharts
3. **DECISION_TREE** - Clinical decision trees
4. **TIMELINE** - Event timelines
5. **HIERARCHY** - Classification hierarchies
6. **SPECTRUM** - Severity/progression spectrums
7. **KEY_DIFFERENTIATORS** - Similar condition differentiators

### Counting Rules

1. **Visual Marker Detection:**
   - Look for "Visual: Yes - [TYPE]" markers
   - Each unique slide with Visual: Yes counts as 1 visual
   - Same slide cannot have multiple visual types

2. **Specification Requirement:**
   - Visuals should have VISUAL SPECIFICATION block
   - Missing specification = warning but still counts

3. **Enforcement:**
   - enforcement: "strict" - Must meet minimum
   - fail_action: "return_to_step_9" - Failed quota requires revision

---

## Step-by-Step Instructions

### Step 1: Count Total Slides and Visuals
```python
def count_slides_and_visuals(blueprint_content):
    """Count slides and identify visual slides."""

    slides = []
    current_slide = None

    for line in blueprint_content.split('\n'):
        # Detect slide boundary
        if line.startswith('---SLIDE ') or line.startswith('SLIDE '):
            if current_slide:
                slides.append(current_slide)
            current_slide = {
                'number': extract_slide_number(line),
                'has_visual': False,
                'visual_type': None,
                'has_specification': False
            }

        # Detect visual marker
        elif current_slide and 'Visual:' in line:
            if 'Visual: Yes' in line:
                current_slide['has_visual'] = True
                # Extract visual type
                visual_types = ['TABLE', 'FLOWCHART', 'DECISION_TREE',
                               'TIMELINE', 'HIERARCHY', 'SPECTRUM',
                               'KEY_DIFFERENTIATORS']
                for vtype in visual_types:
                    if vtype in line.upper():
                        current_slide['visual_type'] = vtype
                        break

        # Detect visual specification
        elif current_slide and 'VISUAL SPECIFICATION' in line:
            current_slide['has_specification'] = True

    if current_slide:
        slides.append(current_slide)

    return slides
```

### Step 2: Determine Section Size Category
```python
def get_size_category(slide_count):
    """Determine size category based on slide count."""

    if slide_count >= 26:
        return "26-35"
    elif slide_count >= 21:
        return "21-25"
    elif slide_count >= 16:
        return "16-20"
    else:
        return "12-15"

def get_quota_requirements(size_category, constraints):
    """Get quota requirements for size category."""

    quotas = constraints['visual_quotas']['by_section_size']
    category_quota = quotas.get(size_category, quotas['12-15'])

    return {
        'minimum': category_quota['minimum'],
        'target_min': category_quota['target_min'],
        'target_max': category_quota['target_max']
    }
```

### Step 3: Calculate Visual Breakdown
```python
def calculate_visual_breakdown(slides):
    """Calculate breakdown by visual type."""

    breakdown = {
        'TABLE': 0,
        'FLOWCHART': 0,
        'DECISION_TREE': 0,
        'TIMELINE': 0,
        'HIERARCHY': 0,
        'SPECTRUM': 0,
        'KEY_DIFFERENTIATORS': 0
    }

    visual_slides = []

    for slide in slides:
        if slide['has_visual']:
            vtype = slide['visual_type']
            if vtype and vtype in breakdown:
                breakdown[vtype] += 1
            visual_slides.append({
                'slide_number': slide['number'],
                'visual_type': vtype or 'UNSPECIFIED',
                'has_specification': slide['has_specification']
            })

    return breakdown, visual_slides
```

### Step 4: Validate Against Quotas
```python
def validate_visual_quota(slides, constraints, section_name):
    """Validate visual count against quota requirements."""

    slide_count = len(slides)
    size_category = get_size_category(slide_count)
    requirements = get_quota_requirements(size_category, constraints)

    breakdown, visual_slides = calculate_visual_breakdown(slides)
    visual_count = len(visual_slides)

    meets_minimum = visual_count >= requirements['minimum']
    meets_target = (requirements['target_min'] <= visual_count <= requirements['target_max'])

    deficit = requirements['minimum'] - visual_count if not meets_minimum else 0

    # Generate recommendations
    recommendations = []
    if not meets_minimum:
        recommendations.append(f"ADD {deficit} more visual(s) to meet minimum requirement")
        recommendations.append("Review content for opportunities: tables, flowcharts, decision trees")
    elif not meets_target:
        if visual_count < requirements['target_min']:
            recommendations.append(f"Consider adding {requirements['target_min'] - visual_count} more visual(s) to reach target range")
        elif visual_count > requirements['target_max']:
            recommendations.append(f"Consider consolidating - currently {visual_count - requirements['target_max']} above target max")

    # Check for specification completeness
    missing_specs = [v for v in visual_slides if not v['has_specification']]
    if missing_specs:
        recommendations.append(f"{len(missing_specs)} visual(s) missing VISUAL SPECIFICATION block")

    # Check for visual type diversity
    used_types = [t for t, count in breakdown.items() if count > 0]
    if len(used_types) == 1 and visual_count > 2:
        recommendations.append(f"Consider diversifying visual types (currently all {used_types[0]})")

    return {
        'validation_status': 'PASS' if meets_minimum else 'FAIL',
        'section_name': section_name,
        'slide_count': slide_count,
        'size_category': size_category,
        'visual_count': visual_count,
        'required_minimum': requirements['minimum'],
        'target_range': {
            'min': requirements['target_min'],
            'max': requirements['target_max']
        },
        'meets_minimum': meets_minimum,
        'meets_target': meets_target,
        'visual_breakdown': breakdown,
        'visual_slides': visual_slides,
        'deficit': deficit,
        'recommendations': recommendations
    }
```

---

## Error Codes

| Code | Severity | Description | Action |
|------|----------|-------------|--------|
| VISUAL_001 | ERROR | Below minimum visual quota | Return to Step 9 for visual identification |
| VISUAL_002 | WARNING | Below target range | Consider adding more visuals |
| VISUAL_003 | WARNING | Above target range | Review for consolidation |
| VISUAL_004 | WARNING | Visual missing specification | Add VISUAL SPECIFICATION block |
| VISUAL_005 | WARNING | Low visual diversity | Use different visual types |
| VISUAL_006 | INFO | Visual type unrecognized | Verify visual type spelling |

---

## Output Format

### Text Report
```
===== VISUAL QUOTA VALIDATION REPORT =====
Section: [Section Name]
Date: [YYYY-MM-DD HH:MM:SS]

STATUS: [PASS/FAIL]

SECTION METRICS:
----------------------------------------
Total Slides: [N]
Size Category: [12-15/16-20/21-25/26-35]
Visual Count: [N]
Required Minimum: [N]
Target Range: [N] - [N]

QUOTA STATUS:
----------------------------------------
Meets Minimum: [YES/NO]
Meets Target: [YES/NO]
Deficit: [N] (if any)

VISUAL BREAKDOWN:
----------------------------------------
TABLE:              [N]
FLOWCHART:          [N]
DECISION_TREE:      [N]
TIMELINE:           [N]
HIERARCHY:          [N]
SPECTRUM:           [N]
KEY_DIFFERENTIATORS: [N]
----------------------------------------
TOTAL:              [N]

VISUAL SLIDES:
----------------------------------------
Slide [N]: [TYPE] - Spec: [YES/NO]
Slide [N]: [TYPE] - Spec: [YES/NO]
[...more visuals...]

RECOMMENDATIONS:
----------------------------------------
[List of recommendations]

ACTION REQUIRED:
----------------------------------------
[If FAIL]
Return to Step 9 (Visual Identifier) to add [N] more visual(s).
Suggested opportunities based on content analysis.

[If PASS]
Proceed to Step 10 for visual integration.
```

---

## Proactive Trigger Reference

When below quota, suggest visuals based on content patterns:

| Content Pattern | Suggested Visual |
|-----------------|------------------|
| 4+ bullet points | TABLE |
| Comparing 2+ items | TABLE, KEY_DIFFERENTIATORS |
| Process/sequence | FLOWCHART |
| Diagnostic criteria | DECISION_TREE, TABLE |
| Similar disorders | KEY_DIFFERENTIATORS |
| Severity/progression | SPECTRUM |
| Historical/developmental | TIMELINE |
| Classification/organization | HIERARCHY |

---

## Integration Points

| Upstream | Downstream |
|----------|------------|
| char_limit_checker | brand_compliance_checker |
| visual_identifier | error_reporter |
| visual_integrator | score_calculator |

---

**Agent Version:** 1.0
**Last Updated:** 2026-01-04
