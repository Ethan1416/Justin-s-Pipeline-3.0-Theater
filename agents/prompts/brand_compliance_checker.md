# Brand Compliance Checker Agent

## Agent Identity
- **Name:** brand_compliance_checker
- **Step:** 8 (Quality Assurance - Brand Standards Verification)
- **Purpose:** Verify that blueprints conform to NCLEX brand standards including fonts, colors, and styling from nclex.yaml

---

## Input Schema
```json
{
  "blueprint": "string (blueprint content to validate)",
  "section_name": "string (current section name)",
  "domain": "string (NCLEX domain: fundamentals/pharmacology/medical_surgical/ob_maternity/pediatric/mental_health)",
  "brand_config": "reference to config/nclex.yaml"
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

### Domain Color Standards (from nclex.yaml)

| Domain | Primary RGB | Secondary RGB |
|--------|-------------|---------------|
| fundamentals | [0, 102, 68] Green | [232, 245, 233] |
| pharmacology | [25, 118, 210] Blue | [227, 242, 253] |
| medical_surgical | [198, 40, 40] Red | [255, 235, 238] |
| ob_maternity | [255, 143, 0] Orange | [255, 243, 224] |
| pediatric | [0, 150, 136] Teal | [224, 242, 241] |
| mental_health | [106, 27, 154] Purple | [243, 229, 245] |

### Style Standards

1. **NCLEX Tip Format:**
   - Prefix: "NCLEX TIP:" (exact)
   - Focus areas: Test-taking strategy, Priority identification, Key discriminators, Common distractors

2. **Teaching Style:**
   - Style: "exam_focused"
   - Emphasis: Clinical judgment, Priority setting, Delegation principles, Safety first, ADPIE nursing process

3. **Question Patterns to Support:**
   - "Which action should the nurse take FIRST?"
   - "Which finding requires IMMEDIATE intervention?"
   - "Which client should the nurse see FIRST?"
   - "Which task can be delegated to the UAP?"
   - "Which statement indicates understanding?"

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
        if 'NCLEX TIP' in line or 'nclex tip' in line.lower():
            style_specs['tip_formats'].append(line)

        # Check for teaching elements
        teaching_keywords = ['clinical judgment', 'priority', 'delegation',
                            'safety', 'ADPIE', 'nursing process']
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
def check_color_compliance(style_specs, domain, brand_config):
    """Verify color specifications match domain colors."""

    domain_colors = brand_config['content']['domains'].get(domain, {})
    expected_primary = domain_colors.get('color_primary_rgb', [0, 0, 0])
    expected_secondary = domain_colors.get('color_secondary_rgb', [255, 255, 255])

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
                        'message': f"Color {found_rgb} does not match {domain} domain colors"
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
    TIP_PREFIX = "NCLEX TIP:"
    tip_prefix_correct = True

    for tip_line in style_specs['tip_formats']:
        if TIP_PREFIX not in tip_line:
            # Check for variations that should be corrected
            variations = ['NCLEX Tip:', 'Nclex Tip:', 'nclex tip:', 'TIP:']
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
    vignette_found = 'vignette' in blueprint_content.lower() or 'question' in blueprint_content.lower()

    if not vignette_found:
        violations.append({
            'type': 'QUESTION_PATTERNS',
            'severity': 'INFO',
            'message': 'No NCLEX-style question patterns detected in content'
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
def generate_brand_compliance_report(blueprint_content, section_name, domain, brand_config):
    """Generate comprehensive brand compliance report."""

    style_specs = extract_style_specs(blueprint_content)

    font_result = check_font_compliance(style_specs, brand_config)
    color_result = check_color_compliance(style_specs, domain, brand_config)
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
        recommendations.append(f"Apply {domain} domain colors: Primary {color_result['expected_primary_rgb']}")
    if not style_result['tip_prefix_correct']:
        recommendations.append("Standardize all tip prefixes to 'NCLEX TIP:'")
    if not style_result['teaching_style_aligned']:
        recommendations.append("Incorporate more exam-focused teaching elements")

    return {
        'validation_status': overall_status,
        'section_name': section_name,
        'domain': domain,
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
| BRAND_003 | WARNING | Incorrect tip prefix format | Use "NCLEX TIP:" prefix |
| BRAND_004 | INFO | No teaching elements detected | Add exam-focused content |
| BRAND_005 | INFO | No question patterns found | Consider adding vignettes |
| BRAND_006 | ERROR | Critical brand violation | Immediate correction required |

---

## Output Format

### Text Report
```
===== BRAND COMPLIANCE VALIDATION REPORT =====
Section: [Section Name]
Domain: [Domain Name]
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
Domain: [Domain Name]
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

## Domain Color Quick Reference

| Domain | Primary | Hex | Use For |
|--------|---------|-----|---------|
| fundamentals | Green | #006644 | Headers, accents |
| pharmacology | Blue | #1976D2 | Headers, accents |
| medical_surgical | Red | #C62828 | Headers, accents |
| ob_maternity | Orange | #FF8F00 | Headers, accents |
| pediatric | Teal | #009688 | Headers, accents |
| mental_health | Purple | #6A1B9A | Headers, accents |

---

## Integration Points

| Upstream | Downstream |
|----------|------------|
| visual_quota_checker | pedagogy_checker |
| blueprint_generator | error_reporter |
| formatting_reviser | score_calculator |

---

**Agent Version:** 1.0
**Last Updated:** 2026-01-04
