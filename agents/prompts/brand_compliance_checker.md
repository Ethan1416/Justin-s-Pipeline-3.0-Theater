# Brand Compliance Checker Agent

## Agent Identity
- **Name:** brand_compliance_checker
- **Step:** 8 (Quality Assurance - Brand Standards Verification)
- **Purpose:** Verify that blueprints conform to theater brand standards including fonts, colors, and styling from theater.yaml

---

## Input Schema
```json
{
  "blueprint": "string (blueprint content to validate)",
  "section_name": "string (current section name)",
  "unit": "string (Theater unit: greek_theater/commedia/shakespeare/one_acts)",
  "brand_config": "reference to config/theater.yaml"
}
```

## Output Schema
```json
{
  "validation_status": "string (PASS/FAIL)",
  "section_name": "string",
  "domain": "string",
  "font_compliance": {
    "status": "string (PASS/FAIL)",
    "expected_font": "string",
    "violations": "array of violations"
  },
  "color_compliance": {
    "status": "string (PASS/FAIL)",
    "expected_primary_rgb": "array [R, G, B]",
    "expected_secondary_rgb": "array [R, G, B]",
    "violations": "array of violations"
  },
  "style_compliance": {
    "status": "string (PASS/FAIL)",
    "tip_prefix_correct": "boolean",
    "teaching_style_aligned": "boolean",
    "violations": "array of violations"
  },
  "total_violations": "number",
  "recommendations": "array of strings"
}
```

---

## Required Skills (Hardcoded)

1. **font_checking** - Verify font specifications match brand standards
2. **color_checking** - Verify color RGB values match domain-specific colors
3. **style_verification** - Verify styling conventions and content format

---

## Validation Rules

### Font Standards

| Element | Expected Font | Size Range | Weight |
|---------|---------------|------------|--------|
| Title/Header | Aptos | 28-36pt | Bold |
| Body Text | Aptos | 18-24pt | Regular |
| Bullet Points | Aptos | 18-22pt | Regular |
| Tips | Aptos | 16-20pt | Italic |
| Presenter Notes | Aptos | 12-14pt | Regular |

### Unit Color Standards (from theater.yaml)

| Unit | Primary RGB | Secondary RGB |
|------|-------------|---------------|
| greek_theater | [139, 90, 43] Bronze | [245, 235, 220] |
| commedia | [220, 53, 69] Red | [255, 235, 238] |
| shakespeare | [75, 0, 130] Indigo | [238, 232, 245] |
| one_acts | [0, 102, 68] Green | [232, 245, 233] |

### Style Standards

1. **Performance Tip Format:**
   - Prefix: "PERFORMANCE TIP:" (exact)
   - Focus areas: Technique application, Common pitfalls, Rehearsal strategies, Performance insight

2. **Teaching Style:**
   - Style: "performance_focused"
   - Emphasis: Physical technique, Vocal technique, Character work, Ensemble collaboration, Historical context

3. **Performance Patterns to Support:**
   - "How would you approach this scene?"
   - "What technique applies here?"
   - "How does this connect to historical context?"
   - "What should you focus on in rehearsal?"
   - "What is the character's objective?"

---

## Step-by-Step Instructions

### Step 1: Extract Style Specifications from Blueprint
```python
def extract_style_specs(blueprint_content):
    """Extract any explicit style specifications from blueprint."""

    style_specs = {
        'fonts_mentioned': [],
        'colors_mentioned': [],
        'tip_formats': [],
        'teaching_elements': []
    }

    for line in blueprint_content.split('\n'):
        # Check for font specifications
        if 'font:' in line.lower() or 'Font:' in line:
            style_specs['fonts_mentioned'].append(line)

        # Check for color specifications (RGB patterns)
        if 'rgb' in line.lower() or 'RGB' in line:
            style_specs['colors_mentioned'].append(line)
        if 'color:' in line.lower() or 'Color:' in line:
            style_specs['colors_mentioned'].append(line)

        # Check tip format
        if 'PERFORMANCE TIP' in line or 'performance tip' in line.lower():
            style_specs['tip_formats'].append(line)

        # Check for teaching elements
        teaching_keywords = ['technique', 'vocal', 'physical', 'character',
                            'ensemble', 'historical context']
        for keyword in teaching_keywords:
            if keyword.lower() in line.lower():
                style_specs['teaching_elements'].append(line)

    return style_specs
```

### Step 2: Validate Font Compliance
```python
def check_font_compliance(style_specs, brand_config):
    """Verify font specifications match brand standards."""

    EXPECTED_FONT = "Aptos"
    violations = []

    for font_line in style_specs['fonts_mentioned']:
        # Check if non-Aptos font is specified
        if EXPECTED_FONT.lower() not in font_line.lower():
            # Extract the font name mentioned
            violations.append({
                'type': 'FONT_MISMATCH',
                'expected': EXPECTED_FONT,
                'found': font_line,
                'severity': 'ERROR',
                'message': f"Non-standard font specified. Expected {EXPECTED_FONT}."
            })

    # If no fonts mentioned, assume compliance (fonts set at template level)
    status = 'PASS' if len(violations) == 0 else 'FAIL'

    return {
        'status': status,
        'expected_font': EXPECTED_FONT,
        'violations': violations
    }
```

### Step 3: Validate Color Compliance
```python
def check_color_compliance(style_specs, unit, brand_config):
    """Verify color specifications match unit colors."""

    unit_colors = brand_config['content']['units'].get(unit, {})
    expected_primary = unit_colors.get('color_primary_rgb', [0, 0, 0])
    expected_secondary = unit_colors.get('color_secondary_rgb', [255, 255, 255])

    violations = []

    for color_line in style_specs['colors_mentioned']:
        # Parse RGB values if present
        import re
        rgb_pattern = r'\[?\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*\]?'
        matches = re.findall(rgb_pattern, color_line)

        for match in matches:
            found_rgb = [int(match[0]), int(match[1]), int(match[2])]

            # Check if it matches expected primary or secondary
            if found_rgb != expected_primary and found_rgb != expected_secondary:
                # Allow some tolerance (within 5 units per channel)
                if not colors_close(found_rgb, expected_primary, 5) and \
                   not colors_close(found_rgb, expected_secondary, 5):
                    violations.append({
                        'type': 'COLOR_MISMATCH',
                        'expected_primary': expected_primary,
                        'expected_secondary': expected_secondary,
                        'found': found_rgb,
                        'severity': 'WARNING',
                        'message': f"Color {found_rgb} does not match {unit} unit colors"
                    })

    status = 'PASS' if len(violations) == 0 else 'FAIL'

    return {
        'status': status,
        'expected_primary_rgb': expected_primary,
        'expected_secondary_rgb': expected_secondary,
        'violations': violations
    }

def colors_close(color1, color2, tolerance):
    """Check if two RGB colors are within tolerance."""
    return all(abs(c1 - c2) <= tolerance for c1, c2 in zip(color1, color2))
```

### Step 4: Validate Style Compliance
```python
def check_style_compliance(style_specs, blueprint_content, brand_config):
    """Verify styling conventions match brand standards."""

    violations = []

    # Check tip prefix format
    TIP_PREFIX = "PERFORMANCE TIP:"
    tip_prefix_correct = True

    for tip_line in style_specs['tip_formats']:
        if TIP_PREFIX not in tip_line:
            # Check for variations that should be corrected
            variations = ['Performance Tip:', 'performance tip:', 'TIP:']
            for var in variations:
                if var in tip_line and var != TIP_PREFIX:
                    violations.append({
                        'type': 'TIP_FORMAT',
                        'expected': TIP_PREFIX,
                        'found': var,
                        'severity': 'WARNING',
                        'message': f"Tip prefix should be '{TIP_PREFIX}' not '{var}'"
                    })
                    tip_prefix_correct = False

    # Check teaching style alignment
    teaching_emphasis = brand_config['teaching']['emphasis']
    teaching_style_aligned = len(style_specs['teaching_elements']) > 0

    if not teaching_style_aligned:
        violations.append({
            'type': 'TEACHING_STYLE',
            'expected': teaching_emphasis,
            'found': 'No teaching elements detected',
            'severity': 'INFO',
            'message': 'Consider incorporating more exam-focused teaching elements'
        })

    # Check for question pattern support
    question_patterns = brand_config['teaching']['question_patterns']
    scenario_found = 'scenario' in blueprint_content.lower() or 'activity' in blueprint_content.lower()

    if not scenario_found:
        violations.append({
            'type': 'SCENARIO_PATTERNS',
            'severity': 'INFO',
            'message': 'No theater-style scenario patterns detected in content'
        })

    status = 'PASS' if len([v for v in violations if v['severity'] == 'ERROR']) == 0 else 'FAIL'

    return {
        'status': status,
        'tip_prefix_correct': tip_prefix_correct,
        'teaching_style_aligned': teaching_style_aligned,
        'violations': violations
    }
```

### Step 5: Generate Compliance Report
```python
def generate_brand_compliance_report(blueprint_content, section_name, unit, brand_config):
    """Generate comprehensive brand compliance report."""

    style_specs = extract_style_specs(blueprint_content)

    font_result = check_font_compliance(style_specs, brand_config)
    color_result = check_color_compliance(style_specs, unit, brand_config)
    style_result = check_style_compliance(style_specs, blueprint_content, brand_config)

    # Calculate total violations
    all_violations = (font_result['violations'] +
                      color_result['violations'] +
                      style_result['violations'])
    error_count = len([v for v in all_violations if v.get('severity') == 'ERROR'])

    # Determine overall status
    overall_status = 'PASS'
    if error_count > 0:
        overall_status = 'FAIL'
    elif font_result['status'] == 'FAIL' or color_result['status'] == 'FAIL':
        overall_status = 'FAIL'

    # Generate recommendations
    recommendations = []
    if font_result['status'] == 'FAIL':
        recommendations.append(f"Use {font_result['expected_font']} font throughout presentation")
    if color_result['status'] == 'FAIL':
        recommendations.append(f"Apply {unit} unit colors: Primary {color_result['expected_primary_rgb']}")
    if not style_result['tip_prefix_correct']:
        recommendations.append("Standardize all tip prefixes to 'PERFORMANCE TIP:'")
    if not style_result['teaching_style_aligned']:
        recommendations.append("Incorporate more exam-focused teaching elements")

    return {
        'validation_status': overall_status,
        'section_name': section_name,
        'unit': unit,
        'font_compliance': font_result,
        'color_compliance': color_result,
        'style_compliance': style_result,
        'total_violations': len(all_violations),
        'recommendations': recommendations
    }
```

---

## Error Codes

| Code | Severity | Description | Action |
|------|----------|-------------|--------|
| BRAND_001 | ERROR | Non-Aptos font specified | Change to Aptos font |
| BRAND_002 | WARNING | Color does not match domain | Update to domain colors |
| BRAND_003 | WARNING | Incorrect tip prefix format | Use "PERFORMANCE TIP:" prefix |
| BRAND_004 | INFO | No teaching elements detected | Add exam-focused content |
| BRAND_005 | INFO | No question patterns found | Consider adding vignettes |
| BRAND_006 | ERROR | Critical brand violation | Immediate correction required |

---

## Output Format

### Text Report
```
===== BRAND COMPLIANCE VALIDATION REPORT =====
Section: [Section Name]
Unit: [Unit Name]
Date: [YYYY-MM-DD HH:MM:SS]

STATUS: [PASS/FAIL]

FONT COMPLIANCE:
----------------------------------------
Status: [PASS/FAIL]
Expected Font: Aptos
Violations: [N]
[List violations if any]

COLOR COMPLIANCE:
----------------------------------------
Status: [PASS/FAIL]
Unit: [Unit Name]
Expected Primary RGB: [R, G, B]
Expected Secondary RGB: [R, G, B]
Violations: [N]
[List violations if any]

STYLE COMPLIANCE:
----------------------------------------
Status: [PASS/FAIL]
Tip Prefix Correct: [YES/NO]
Teaching Style Aligned: [YES/NO]
Violations: [N]
[List violations if any]

SUMMARY:
----------------------------------------
Total Violations: [N]
  Errors: [N]
  Warnings: [N]
  Info: [N]

RECOMMENDATIONS:
----------------------------------------
[List of recommendations]

ACTION REQUIRED:
----------------------------------------
[If FAIL]
Correct brand violations before proceeding.

[If PASS]
Brand compliance verified. Proceed to next check.
```

---

## Unit Color Quick Reference

| Unit | Primary | Hex | Use For |
|------|---------|-----|---------|
| greek_theater | Bronze | #8B5A2B | Headers, accents |
| commedia | Red | #DC3545 | Headers, accents |
| shakespeare | Indigo | #4B0082 | Headers, accents |
| one_acts | Green | #006644 | Headers, accents |

---

## Integration Points

| Upstream | Downstream |
|----------|------------|
| visual_quota_checker | pedagogy_checker |
| blueprint_generator | error_reporter |
| formatting_reviser | score_calculator |

---

**Agent Version:** 2.0 (Theater Adaptation)
**Last Updated:** 2026-01-08

### Version History
- **v2.0** (2026-01-08): Adapted for theater pipeline - NCLEX domains → theater units, NCLEX TIP → PERFORMANCE TIP
- **v1.0** (2026-01-04): Initial brand compliance checker agent
