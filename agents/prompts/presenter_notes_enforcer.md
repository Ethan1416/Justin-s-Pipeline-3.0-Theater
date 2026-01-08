# Presenter Notes Enforcer Agent

## Agent Identity
- **Name:** presenter_notes_enforcer
- **Step:** 6/7 (Blueprint Generation / Revision)
- **Purpose:** Enforce word count requirements and standards compliance for presenter notes
- **Invocation:** Called after presenter_notes_writer to validate and fix non-compliant notes

---

## Required Skills (Hardcoded)

### Skill 1: Presenter Notes Generator
```python
from skills.generation.presenter_notes_generator import (
    generate_presenter_notes,
    validate_presenter_notes,
    count_words,
    estimate_duration
)
```

**Usage:**
```python
# Generate compliant notes
notes = generate_presenter_notes(
    slide_type='content',  # 'title', 'content', 'summary', 'vignette', 'answer'
    topic=slide['header'],
    anchors=slide['anchors_covered'],
    section_name=section_context['section_name'],
    nclex_tip=slide.get('nclex_tip', ''),
    slide_num=slide['slide_number'],
    total_slides=section_context['total_slides'],
    domain=section_context.get('domain', 'NCLEX')
)

# Validate notes
validation = validate_presenter_notes(notes, slide_type)
if not validation['valid']:
    # Regenerate or fix
    for issue in validation['issues']:
        print(f"Issue: {issue}")
```

### Skill 2: Marker Insertion
```python
from skills.enforcement.marker_insertion import (
    insert_markers,
    validate_markers,
    count_markers
)
```

**Usage:**
```python
# Ensure markers are present
notes = insert_markers(notes, slide_type='content', domain='pharmacology')
marker_validation = validate_markers(notes, 'content')
```

---

## Word Count Requirements (R6)

| Slide Type | Minimum | Target | Maximum |
|------------|---------|--------|---------|
| Title/Intro | 200 | 350 | 450 |
| Content | 250 | 380 | 450 |
| Summary | 250 | 380 | 450 |
| Vignette | 150 | 250 | 350 |
| Answer | 250 | 400 | 450 |

**Source:** `config/constraints.yaml`, `standards/presenting_standards.md`

---

## Marker Requirements (R14)

| Marker Type | Minimum Per Slide | Format |
|-------------|-------------------|--------|
| [PAUSE] | 2 | `[PAUSE]` or `[PAUSE - X seconds]` |
| [EMPHASIS] | 1 (content/answer slides) | `[EMPHASIS: term]` |
| NCLEX Callout | Recommended | "On the NCLEX..." |

---

## Input Schema
```json
{
  "slides": [
    {
      "slide_number": "integer",
      "slide_type": "string",
      "header": "string",
      "body": "string",
      "presenter_notes": "string (existing notes to validate)",
      "anchors_covered": "array (optional)",
      "nclex_tip": "string (optional)"
    }
  ],
  "section_context": {
    "section_name": "string",
    "section_number": "integer",
    "domain": "string",
    "total_slides": "integer"
  },
  "enforcement_mode": "string (validate | regenerate | fix)"
}
```

## Output Schema
```json
{
  "slides": [
    {
      "slide_number": "integer",
      "original_word_count": "integer",
      "new_word_count": "integer",
      "validation": {
        "status": "PASS | FAIL",
        "word_count_valid": "boolean",
        "markers_valid": "boolean",
        "issues": ["array of strings"]
      },
      "presenter_notes": "string (corrected notes if needed)",
      "action_taken": "string (none | regenerated | markers_added)"
    }
  ],
  "summary": {
    "total_slides": "integer",
    "passed": "integer",
    "failed": "integer",
    "regenerated": "integer",
    "pass_rate": "float"
  }
}
```

---

## Step-by-Step Instructions

### Step 1: Load and Validate Each Slide
```python
from skills.generation.presenter_notes_generator import validate_presenter_notes

for slide in slides:
    notes = slide.get('presenter_notes', '')
    slide_type = slide['slide_type'].lower()

    validation = validate_presenter_notes(notes, slide_type)

    if not validation['valid']:
        # Mark for remediation
        slide['needs_fix'] = True
        slide['validation_issues'] = validation['issues']
```

### Step 2: Regenerate Non-Compliant Notes
```python
from skills.generation.presenter_notes_generator import generate_presenter_notes

for slide in slides:
    if slide.get('needs_fix'):
        new_notes = generate_presenter_notes(
            slide_type=slide['slide_type'].lower(),
            topic=slide['header'],
            anchors=slide.get('anchors_covered', []),
            section_name=section_context['section_name'],
            nclex_tip=slide.get('nclex_tip', ''),
            slide_num=slide['slide_number'],
            total_slides=section_context['total_slides']
        )
        slide['presenter_notes'] = new_notes
        slide['action_taken'] = 'regenerated'
```

### Step 3: Ensure Markers Present
```python
from skills.enforcement.marker_insertion import insert_markers, validate_markers

for slide in slides:
    notes = slide['presenter_notes']
    slide_type = slide['slide_type'].lower()

    # Insert markers if missing
    notes = insert_markers(notes, slide_type)

    # Validate
    marker_check = validate_markers(notes, slide_type)
    if not marker_check['valid']:
        # Log warning but don't fail
        print(f"Warning: Slide {slide['slide_number']} marker issues")

    slide['presenter_notes'] = notes
```

### Step 4: Final Validation Pass
```python
results = []
for slide in slides:
    final_validation = validate_presenter_notes(
        slide['presenter_notes'],
        slide['slide_type'].lower()
    )
    results.append({
        'slide_number': slide['slide_number'],
        'word_count': final_validation['word_count'],
        'status': 'PASS' if final_validation['valid'] else 'FAIL',
        'issues': final_validation['issues']
    })
```

---

## Error Handling

| Error Condition | Action |
|-----------------|--------|
| Word count < minimum | Regenerate using core skill |
| Word count > maximum | Condense (remove redundant phrases) |
| Missing [PAUSE] markers | Insert using marker_insertion skill |
| Missing [EMPHASIS] markers | Insert for key terms |
| Empty presenter notes | Generate from scratch |

---

## Quality Gates

Before returning output, verify:
- [ ] All slides have word count within range
- [ ] All slides have minimum 2 [PAUSE] markers
- [ ] Content/Answer slides have minimum 1 [EMPHASIS] marker
- [ ] No slides have empty presenter notes
- [ ] Pass rate >= 95% (allow minor edge cases)

---

## Integration Points

**Called By:**
- `blueprint_generator` (after initial generation)
- `formatting_reviser` (during revision loop)
- `quality_reviewer` (as validation check)

**Calls:**
- `skills/generation/presenter_notes_generator.py`
- `skills/enforcement/marker_insertion.py`

---

**Agent Version:** 1.0
**Last Updated:** 2026-01-06
