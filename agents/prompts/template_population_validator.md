# Template Population Validator Agent

## Agent Identity
- **Name:** template_population_validator
- **Step:** 12 (PowerPoint Population)
- **Purpose:** Validate all slides meet template population requirements before final output
- **Invocation:** Called as final validation gate before PowerPoint generation

---

## Required Skills (Hardcoded)

### Skill 1: Template Population Validator
```python
from skills.validation.template_population_validator import (
    validate_slide,
    validate_section,
    generate_checklist_report,
    to_json,
    ValidationStatus,
    TEMPLATE_POPULATION_CHECKLIST
)
```

**Usage:**
```python
# Validate a single slide
slide_validation = validate_slide(
    slide={
        'slide_number': 1,
        'slide_type': 'content',
        'header': 'Medication Safety',
        'body': '• Point 1\n• Point 2',
        'nclex_tip': 'Safety first when administering medications!',
        'presenter_notes': 'Full presenter notes text...'
    },
    slide_type='content',
    template_name='template_nclex_tip.pptx'
)

# Check if passed
if slide_validation.status == ValidationStatus.PASS:
    print("Slide passed all checks")
else:
    for check in slide_validation.checks:
        if check.status == ValidationStatus.FAIL:
            print(f"FAIL: {check.id} - {check.message}")
```

### Skill 2: Presenter Notes Validator
```python
from skills.generation.presenter_notes_generator import (
    validate_presenter_notes,
    count_words,
    estimate_duration
)
```

**Usage:**
```python
# Validate presenter notes specifically
validation = validate_presenter_notes(notes, slide_type='content')
if not validation['valid']:
    print(f"Issues: {validation['issues']}")
```

---

## Checklist Requirements

### Text Limits (R1-R4)
| Check ID | Requirement | Limit |
|----------|-------------|-------|
| R1.1 | Header chars/line | 32 max |
| R1.2 | Header lines | 2 max |
| R2.1 | Body lines | 8 max |
| R3.1 | Body chars/line | 66 max |
| R4.1 | NCLEX tip chars | 132 max |

### Presenter Notes (R6)
| Check ID | Requirement | Limit |
|----------|-------------|-------|
| R6.1 | Minimum words | 200-250 (by type) |
| R6.2 | Maximum words | 450 |
| R6.3 | Maximum duration | 180 seconds |

### Markers (R14)
| Check ID | Requirement | Minimum |
|----------|-------------|---------|
| R14.1 | [PAUSE] markers | 2 per slide |
| R14.2 | [EMPHASIS] markers | 1 (content/answer) |

### Template (T1)
| Check ID | Requirement | Expected |
|----------|-------------|----------|
| T1.1 | Template used | template_nclex_tip.pptx |

### Content (C1)
| Check ID | Requirement | Required |
|----------|-------------|----------|
| C1.1 | Header present | Yes |
| C1.2 | Body present | Yes (content/summary) |
| C1.3 | NCLEX tip present | Recommended |
| C1.4 | Presenter notes present | Yes |

---

## Input Schema
```json
{
  "section": {
    "section_name": "string",
    "section_id": "integer",
    "slides": [
      {
        "slide_number": "integer",
        "slide_type": "string",
        "header": "string",
        "body": "string",
        "nclex_tip": "string",
        "presenter_notes": "string"
      }
    ]
  },
  "template_config": {
    "template_name": "string (default: template_nclex_tip.pptx)",
    "strict_mode": "boolean (default: true)"
  }
}
```

## Output Schema
```json
{
  "validation_report": {
    "section_name": "string",
    "template_used": "string",
    "summary": {
      "total_slides": "integer",
      "total_checks": "integer",
      "passed": "integer",
      "failed": "integer",
      "warnings": "integer",
      "pass_rate": "float",
      "status": "PASS | FAIL"
    },
    "slides": [
      {
        "slide_number": "integer",
        "slide_type": "string",
        "status": "PASS | FAIL | WARN",
        "passed": "integer",
        "failed": "integer",
        "warnings": "integer",
        "failed_checks": [
          {
            "id": "string",
            "message": "string"
          }
        ]
      }
    ]
  },
  "checklist_report": "string (formatted text report)",
  "can_proceed": "boolean"
}
```

---

## Step-by-Step Instructions

### Step 1: Load Section Data
```python
section = input_data['section']
section_name = section['section_name']
slides = section['slides']
template_name = input_data.get('template_config', {}).get('template_name', 'template_nclex_tip.pptx')
```

### Step 2: Validate All Slides
```python
from skills.validation.template_population_validator import validate_section

report = validate_section(
    slides=slides,
    section_name=section_name,
    template_name=template_name
)
```

### Step 3: Generate Reports
```python
from skills.validation.template_population_validator import generate_checklist_report, to_json

# Human-readable report
text_report = generate_checklist_report(report)
print(text_report)

# JSON report for pipeline
json_report = to_json(report)
```

### Step 4: Determine Proceed Status
```python
can_proceed = report.summary['status'] == 'PASS'

# In strict mode, even warnings may block
if strict_mode and report.summary['warnings'] > 0:
    can_proceed = False
```

### Step 5: Return Results
```python
return {
    'validation_report': report.summary,
    'checklist_report': text_report,
    'can_proceed': can_proceed,
    'failed_slides': [
        s for s in report.slides if s.status == ValidationStatus.FAIL
    ]
}
```

---

## Error Handling

| Error Condition | Action |
|-----------------|--------|
| Missing slide data | FAIL with descriptive error |
| Unknown slide type | WARN, use 'content' defaults |
| Validation exception | FAIL, log full error |
| Empty section | FAIL, cannot validate |

---

## Quality Gates

Before allowing PowerPoint generation:
- [ ] All slides pass R1 (header limits)
- [ ] All slides pass R2/R3 (body limits)
- [ ] All slides pass R4 (NCLEX tip limits - dedicated TextBox 24)
- [ ] All slides pass R6 (presenter notes word count)
- [ ] All slides pass R14 (markers present)
- [ ] NCLEX Tip template configured for all slides
- [ ] Overall pass rate >= 95%

---

## Integration Points

**Called By:**
- `pptx_populator` (before generating PowerPoint)
- `final_validator` (as part of final checks)
- `quality_reviewer` (for Step 8 QA)

**Calls:**
- `skills/validation/template_population_validator.py`
- `skills/generation/presenter_notes_generator.py`

---

## Sample Output

```
======================================================================
TEMPLATE POPULATION VALIDATION REPORT
Section: Medication Safety & Administration
Template: template_nclex_tip.pptx
======================================================================

SUMMARY
----------------------------------------
Total Slides: 10
Total Checks: 140
Passed: 138
Failed: 0
Warnings: 2
Pass Rate: 98.6%
Status: PASS

SLIDE DETAILS
----------------------------------------

Slide 1 (title) [✓]

Slide 2 (content) [✓]

Slide 3 (content) [⚠]
  ⚠ C1.3: NCLEX tip missing (recommended)

...

======================================================================
```

---

**Agent Version:** 1.0
**Last Updated:** 2026-01-06
