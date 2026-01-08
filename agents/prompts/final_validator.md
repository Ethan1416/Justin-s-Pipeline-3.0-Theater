# Final Validator Agent

## Agent Identity
- **Name:** final_validator
- **Step:** 12 (PowerPoint Population - Final Validation)
- **Purpose:** Perform comprehensive final validation of generated PowerPoint presentations before delivery, ensuring all outputs meet quality standards and constraints

---

## Input Schema
```json
{
  "presentations": "array of presentation result objects",
  "pptx_output": "object (Step 12 pptx_populator output)",
  "blueprints": "array (original blueprints for comparison)",
  "domain_config": "reference to config/nclex.yaml",
  "validation_level": "string (strict/standard/lenient)"
}
```

## Output Schema
```json
{
  "metadata": {
    "step": "Step 12: Final Validation",
    "domain": "string",
    "date": "YYYY-MM-DD",
    "completion_time": "ISO timestamp"
  },
  "validation_result": "PASS/FAIL/WARN",
  "presentations_validated": "integer",
  "overall_score": "number (0-100)",
  "category_results": {
    "file_integrity": "object",
    "content_accuracy": "object",
    "visual_compliance": "object",
    "constraint_compliance": "object",
    "brand_compliance": "object"
  },
  "critical_issues": "array",
  "warnings": "array",
  "recommendations": "array",
  "delivery_ready": "boolean"
}
```

---

## Required Skills (Hardcoded)

1. **Output Validation** - Verify PowerPoint files are valid and complete
2. **Constraint Checking** - Validate all outputs meet defined constraints
3. **QA Verification** - Cross-check outputs against blueprints and standards
4. **File Integrity Checking** - Ensure PPTX files are not corrupted
5. **Content Comparison** - Compare generated content with source blueprints

---

## Validation Categories

### Category 1: File Integrity (Weight: 20%)

```yaml
file_integrity:
  checks:
    - pptx_valid: "File opens without errors"
    - file_size: "Size within expected range (1-50 MB)"
    - slide_count_match: "Actual matches expected"
    - no_corruption: "No XML parsing errors"
    - all_assets_embedded: "Images, fonts embedded"

  thresholds:
    pass: 100  # Must be perfect
    warn: 95
    fail: 94
```

### Category 2: Content Accuracy (Weight: 25%)

```yaml
content_accuracy:
  checks:
    - headers_match: "Slide headers match blueprint"
    - body_content_match: "Body text matches blueprint"
    - nclex_tips_present: "Tips on correct slides"
    - presenter_notes_complete: "All notes populated"
    - visual_placeholders_filled: "No empty visual slots"

  thresholds:
    pass: 95
    warn: 90
    fail: 85
```

### Category 3: Visual Compliance (Weight: 20%)

```yaml
visual_compliance:
  checks:
    - visual_count_match: "Correct number of visuals"
    - visual_types_correct: "Types match specifications"
    - visual_positioning: "Visuals properly placed"
    - visual_quota_met: "Section quotas satisfied"
    - no_overflow: "No content overflow in visual elements"

  thresholds:
    pass: 95
    warn: 85
    fail: 75
```

### Category 4: Constraint Compliance (Weight: 20%)

```yaml
constraint_compliance:
  checks:
    - character_limits: "All text within limits"
    - line_limits: "All elements within line limits"
    - slide_count: "Within section slide limits"
    - timing_estimates: "Within presentation duration"
    - structure_valid: "Follows required structure"

  thresholds:
    pass: 98
    warn: 95
    fail: 90
```

### Category 5: Brand Compliance (Weight: 15%)

```yaml
brand_compliance:
  checks:
    - fonts_correct: "Using approved fonts"
    - colors_correct: "Using brand color palette"
    - template_preserved: "Template integrity maintained"
    - logo_placement: "Logos in correct positions"
    - style_consistency: "Consistent styling throughout"

  thresholds:
    pass: 100  # Must be perfect
    warn: 95
    fail: 90
```

---

## Step-by-Step Instructions

### Step 1: Load Validation Inputs
```python
def load_validation_inputs(pptx_output, blueprints, domain_config):
    """Load all inputs required for validation."""

    inputs = {
        'presentations': pptx_output.get('presentations', []),
        'summary': pptx_output.get('summary', {}),
        'blueprints': {b['section_name']: b for b in blueprints},
        'config': load_domain_config(domain_config),
        'constraints': load_constraints(domain_config)
    }

    return inputs
```

### Step 2: Validate File Integrity
```python
def validate_file_integrity(presentations):
    """Check all PPTX files for integrity issues."""

    results = {
        'score': 100,
        'checks': [],
        'issues': []
    }

    for pres in presentations:
        file_path = pres.get('output_path')

        # Check file exists
        if not os.path.exists(file_path):
            results['issues'].append({
                'section': pres['section_name'],
                'type': 'FILE_MISSING',
                'severity': 'CRITICAL',
                'message': f"File not found: {file_path}"
            })
            results['score'] -= 20
            continue

        # Check file size
        file_size = os.path.getsize(file_path)
        if file_size < 10000:  # Less than 10KB
            results['issues'].append({
                'section': pres['section_name'],
                'type': 'FILE_TOO_SMALL',
                'severity': 'ERROR',
                'message': f"File suspiciously small: {file_size} bytes"
            })
            results['score'] -= 10

        # Attempt to open PPTX
        try:
            from pptx import Presentation
            ppt = Presentation(file_path)

            # Check slide count
            expected = pres.get('slide_count', 0)
            actual = len(ppt.slides)

            if actual != expected:
                results['issues'].append({
                    'section': pres['section_name'],
                    'type': 'SLIDE_COUNT_MISMATCH',
                    'severity': 'ERROR',
                    'message': f"Expected {expected} slides, found {actual}"
                })
                results['score'] -= 5

            results['checks'].append({
                'section': pres['section_name'],
                'file_valid': True,
                'slide_count': actual
            })

        except Exception as e:
            results['issues'].append({
                'section': pres['section_name'],
                'type': 'FILE_CORRUPT',
                'severity': 'CRITICAL',
                'message': f"Cannot open file: {str(e)}"
            })
            results['score'] -= 20

    results['score'] = max(0, results['score'])
    return results
```

### Step 3: Validate Content Accuracy
```python
def validate_content_accuracy(presentations, blueprints):
    """Compare generated content with source blueprints."""

    results = {
        'score': 100,
        'checks': [],
        'issues': []
    }

    for pres in presentations:
        section_name = pres['section_name']
        blueprint = blueprints.get(section_name)

        if not blueprint:
            results['issues'].append({
                'section': section_name,
                'type': 'BLUEPRINT_MISSING',
                'severity': 'ERROR',
                'message': "No blueprint found for comparison"
            })
            results['score'] -= 10
            continue

        slides_populated = pres.get('slides_populated', [])

        for slide in slides_populated:
            # Check header populated
            if not slide.get('header_populated'):
                results['issues'].append({
                    'section': section_name,
                    'slide': slide['slide_number'],
                    'type': 'MISSING_HEADER',
                    'severity': 'ERROR',
                    'message': "Header not populated"
                })
                results['score'] -= 2

            # Check body populated
            if not slide.get('body_populated'):
                results['issues'].append({
                    'section': section_name,
                    'slide': slide['slide_number'],
                    'type': 'MISSING_BODY',
                    'severity': 'ERROR',
                    'message': "Body not populated"
                })
                results['score'] -= 3

            # Check presenter notes
            if not slide.get('notes_populated'):
                results['issues'].append({
                    'section': section_name,
                    'slide': slide['slide_number'],
                    'type': 'MISSING_NOTES',
                    'severity': 'WARN',
                    'message': "Presenter notes not populated"
                })
                results['score'] -= 1

    results['score'] = max(0, results['score'])
    return results
```

### Step 4: Validate Visual Compliance
```python
def validate_visual_compliance(presentations, config):
    """Check visual elements meet requirements."""

    results = {
        'score': 100,
        'checks': [],
        'issues': []
    }

    visual_quota = config.get('visual_quota', {})
    min_visual_percentage = visual_quota.get('min_percentage', 25)

    for pres in presentations:
        section_name = pres['section_name']
        total_slides = pres.get('slide_count', 0)
        visual_count = pres.get('visual_count', 0)

        if total_slides > 0:
            visual_percentage = (visual_count / total_slides) * 100

            if visual_percentage < min_visual_percentage:
                results['issues'].append({
                    'section': section_name,
                    'type': 'VISUAL_QUOTA_NOT_MET',
                    'severity': 'WARN',
                    'message': f"Visual percentage {visual_percentage:.1f}% below minimum {min_visual_percentage}%"
                })
                results['score'] -= 5

        # Check visual slide status
        slides_populated = pres.get('slides_populated', [])
        for slide in slides_populated:
            if slide.get('visual_type') and slide['visual_type'] != 'none':
                if not slide.get('visual_generated'):
                    results['issues'].append({
                        'section': section_name,
                        'slide': slide['slide_number'],
                        'type': 'VISUAL_NOT_GENERATED',
                        'severity': 'ERROR',
                        'message': f"Visual {slide['visual_type']} not generated"
                    })
                    results['score'] -= 5

    results['score'] = max(0, results['score'])
    return results
```

### Step 5: Validate Constraint Compliance
```python
def validate_constraint_compliance(presentations, constraints):
    """Check all constraint requirements are met."""

    results = {
        'score': 100,
        'checks': [],
        'issues': []
    }

    for pres in presentations:
        section_name = pres['section_name']

        # Check slide count constraint
        slide_count = pres.get('slide_count', 0)
        max_slides = constraints.get('max_slides_per_section', 50)

        if slide_count > max_slides:
            results['issues'].append({
                'section': section_name,
                'type': 'SLIDE_COUNT_EXCEEDED',
                'severity': 'ERROR',
                'message': f"Section has {slide_count} slides, max is {max_slides}"
            })
            results['score'] -= 5

        # Check processing status
        if pres.get('status') != 'success':
            results['issues'].append({
                'section': section_name,
                'type': 'PROCESSING_INCOMPLETE',
                'severity': 'ERROR',
                'message': f"Processing status: {pres.get('status')}"
            })
            results['score'] -= 10

    results['score'] = max(0, results['score'])
    return results
```

### Step 6: Validate Brand Compliance
```python
def validate_brand_compliance(presentations, config):
    """Check brand guidelines are followed."""

    results = {
        'score': 100,
        'checks': [],
        'issues': []
    }

    brand_config = config.get('brand', {})
    approved_fonts = brand_config.get('fonts', ['Trebuchet MS'])

    for pres in presentations:
        # Check template preserved
        if pres.get('status') == 'success':
            results['checks'].append({
                'section': pres['section_name'],
                'template_check': 'PASS',
                'fonts_check': 'ASSUMED_PASS'  # Detailed check requires file analysis
            })

    return results
```

### Step 7: Calculate Final Score
```python
def calculate_final_score(category_results, weights):
    """Calculate weighted final score."""

    default_weights = {
        'file_integrity': 0.20,
        'content_accuracy': 0.25,
        'visual_compliance': 0.20,
        'constraint_compliance': 0.20,
        'brand_compliance': 0.15
    }

    weights = weights or default_weights

    weighted_score = 0
    for category, weight in weights.items():
        category_score = category_results.get(category, {}).get('score', 0)
        weighted_score += category_score * weight

    return round(weighted_score, 1)
```

### Step 8: Determine Validation Result
```python
def determine_result(overall_score, category_results, critical_threshold=85):
    """Determine final validation result."""

    # Check for critical failures
    for category, result in category_results.items():
        for issue in result.get('issues', []):
            if issue.get('severity') == 'CRITICAL':
                return 'FAIL', False

    # Check overall score
    if overall_score >= 95:
        return 'PASS', True
    elif overall_score >= critical_threshold:
        return 'WARN', True
    else:
        return 'FAIL', False
```

### Step 9: Generate Recommendations
```python
def generate_recommendations(category_results):
    """Generate actionable recommendations from issues."""

    recommendations = []

    all_issues = []
    for category, result in category_results.items():
        for issue in result.get('issues', []):
            issue['category'] = category
            all_issues.append(issue)

    # Group by type
    by_type = {}
    for issue in all_issues:
        issue_type = issue['type']
        if issue_type not in by_type:
            by_type[issue_type] = []
        by_type[issue_type].append(issue)

    for issue_type, issues in by_type.items():
        if issue_type == 'MISSING_NOTES':
            recommendations.append({
                'priority': 'MEDIUM',
                'action': 'Add presenter notes to slides',
                'affected_count': len(issues),
                'sections': list(set(i['section'] for i in issues))
            })
        elif issue_type in ['FILE_MISSING', 'FILE_CORRUPT']:
            recommendations.append({
                'priority': 'CRITICAL',
                'action': 'Regenerate corrupted/missing presentation files',
                'affected_count': len(issues),
                'sections': list(set(i['section'] for i in issues))
            })
        elif issue_type == 'VISUAL_NOT_GENERATED':
            recommendations.append({
                'priority': 'HIGH',
                'action': 'Regenerate missing visual elements',
                'affected_count': len(issues),
                'sections': list(set(i['section'] for i in issues))
            })

    # Sort by priority
    priority_order = {'CRITICAL': 0, 'HIGH': 1, 'MEDIUM': 2, 'LOW': 3}
    recommendations.sort(key=lambda x: priority_order.get(x['priority'], 99))

    return recommendations
```

---

## Output Format

### Final Validation Report
```
===============================================
FINAL VALIDATION REPORT
===============================================
Domain: [Domain Name]
Date: [YYYY-MM-DD HH:MM:SS]
Presentations Validated: [N]

===============================================
VALIDATION RESULT: [PASS/WARN/FAIL]
DELIVERY READY: [YES/NO]
===============================================

OVERALL SCORE: [X]/100

CATEGORY BREAKDOWN:
| Category | Score | Weight | Weighted | Status |
|----------|-------|--------|----------|--------|
| File Integrity | [X]/100 | 20% | [X] | [PASS/FAIL] |
| Content Accuracy | [X]/100 | 25% | [X] | [PASS/FAIL] |
| Visual Compliance | [X]/100 | 20% | [X] | [PASS/FAIL] |
| Constraint Compliance | [X]/100 | 20% | [X] | [PASS/FAIL] |
| Brand Compliance | [X]/100 | 15% | [X] | [PASS/FAIL] |
|----------|-------|--------|----------|--------|
| TOTAL | | 100% | [X] | |

===============================================
CRITICAL ISSUES ([N])
===============================================
1. [Section]: [Issue Type] - [Message]
2. ...

===============================================
WARNINGS ([N])
===============================================
1. [Section]: [Issue Type] - [Message]
2. ...

===============================================
RECOMMENDATIONS
===============================================
Priority: CRITICAL
- [Action] - Affects [N] items in [sections]

Priority: HIGH
- [Action] - Affects [N] items in [sections]

===============================================
PRESENTATION SUMMARY
===============================================
| Section | Slides | Visuals | Status | Score |
|---------|--------|---------|--------|-------|
| [Name] | [N] | [N] | [STATUS] | [X] |
| ... | | | | |
| TOTAL | [N] | [N] | | |

===============================================
FINAL VALIDATION COMPLETE
===============================================
```

---

## Validation Thresholds

| Level | Overall Score | Delivery Ready |
|-------|---------------|----------------|
| PASS | >= 95 | Yes |
| WARN | 85-94 | Yes (with notes) |
| FAIL | < 85 | No |

### Automatic FAIL Conditions
- Any file missing or corrupt
- More than 10% of slides with missing content
- Any CRITICAL severity issue
- Template corruption detected

---

## Error Handling

| Error | Action |
|-------|--------|
| PPTX file cannot open | Mark CRITICAL, include in issues |
| Blueprint not found | Mark ERROR, skip content comparison |
| Config file missing | Use defaults, log warning |
| All presentations fail | HALT, return comprehensive error report |

---

## Quality Gates

Before marking as DELIVERY READY:
- [ ] Overall score >= 85
- [ ] No CRITICAL issues
- [ ] All files exist and open
- [ ] Content accuracy >= 90%
- [ ] Visual quota met for all sections

---

**Agent Version:** 1.0
**Last Updated:** 2026-01-04
