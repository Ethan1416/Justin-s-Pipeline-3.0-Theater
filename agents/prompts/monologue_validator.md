# Monologue Validator Agent

## Purpose
Validate that all presenter notes (monologues) meet HARDCODED requirements. This validator CANNOT be bypassed - every slide MUST pass validation before the presentation is considered complete.

---

## HARDCODED VALIDATION RULES (CANNOT BE BYPASSED)

### R1: Word Count Requirements
| Slide Type | Minimum | Maximum | Target |
|------------|---------|---------|--------|
| Content (3-14) | 150 | 200 | 175 |
| Auxiliary (1,2,15,16) | 100 | 200 | 150 |

**CRITICAL:** Any content slide with fewer than 150 words FAILS validation.

### R2: [PAUSE] Marker Requirements
- **Minimum per slide:** 2
- **Minimum per presentation:** 24 (2 x 12 content slides)
- **Purpose:** Allow information absorption, emphasize key points

**CRITICAL:** Any slide with fewer than 2 [PAUSE] markers FAILS validation.

### R3: [EMPHASIS] Marker Requirements
- **Minimum per content slide:** 1
- **Minimum per presentation:** 12
- **Purpose:** Highlight vocabulary terms and key concepts

**CRITICAL:** Any content slide without [EMPHASIS] markers FAILS validation.

### R4: No Bullet-Point Style
The following patterns are FORBIDDEN:
- `• ` or `- ` at line start (bullet points)
- `1. ` `2. ` `3. ` at line start (numbered lists)
- `TODO`, `PLACEHOLDER`, `INSERT HERE`
- `[CONTENT]` placeholder markers

**CRITICAL:** Any slide with bullet-point style FAILS validation.

### R5: Natural Speech Flow
- No excessive blank lines (3+ consecutive newlines)
- Complete sentences only
- Conversational tone
- First-person address

### R6: Presentation-Level Requirements
| Marker | Minimum Total |
|--------|---------------|
| [PAUSE] | 24 |
| [EMPHASIS] | 12 |
| [CHECK] | 3 |

**CRITICAL:** Presentation FAILS if totals are below minimums.

---

## Input Schema

```json
{
  "type": "object",
  "required": ["monologues"],
  "properties": {
    "monologues": {
      "type": "array",
      "items": {"type": "string"},
      "minItems": 16,
      "maxItems": 16,
      "description": "Array of 16 presenter notes strings"
    },
    "slide_types": {
      "type": "array",
      "items": {"type": "string"},
      "description": "Optional array of slide types (agenda, warmup, content, activity, journal)"
    }
  }
}
```

---

## Output Schema

```json
{
  "type": "object",
  "required": ["valid", "slides_passed", "total_words", "total_markers", "issues"],
  "properties": {
    "valid": {
      "type": "boolean",
      "description": "TRUE only if ALL slides pass ALL validation rules"
    },
    "slides_checked": {"type": "integer"},
    "slides_passed": {"type": "integer"},
    "slides_failed": {"type": "integer"},
    "total_words": {"type": "integer"},
    "total_markers": {
      "type": "object",
      "properties": {
        "PAUSE": {"type": "integer"},
        "EMPHASIS": {"type": "integer"},
        "CHECK": {"type": "integer"},
        "GESTURE": {"type": "integer"},
        "TRANSITION": {"type": "integer"}
      }
    },
    "estimated_duration_minutes": {"type": "number"},
    "slide_results": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "slide_index": {"type": "integer"},
          "valid": {"type": "boolean"},
          "word_count": {"type": "integer"},
          "markers": {"type": "object"},
          "issues": {"type": "array"}
        }
      }
    },
    "issues": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "rule": {"type": "string"},
          "severity": {"enum": ["CRITICAL", "WARNING", "INFO"]},
          "message": {"type": "string"},
          "slide": {"type": "integer"}
        }
      }
    }
  }
}
```

---

## Validation Process

### Step 1: Per-Slide Validation
For each of the 16 slides:

```python
def validate_slide(monologue, slide_index, slide_type):
    issues = []

    # R1: Word count
    word_count = count_words(monologue)
    if slide_type == "content" and word_count < 150:
        issues.append(CRITICAL("R1", f"Slide {slide_index}: {word_count} words < 150 minimum"))

    # R2: [PAUSE] markers
    pause_count = count_marker(monologue, "[PAUSE]")
    if pause_count < 2:
        issues.append(CRITICAL("R2", f"Slide {slide_index}: {pause_count} [PAUSE] < 2 minimum"))

    # R3: [EMPHASIS] markers (content slides)
    if slide_type == "content":
        emphasis_count = count_marker(monologue, "[EMPHASIS")
        if emphasis_count < 1:
            issues.append(CRITICAL("R3", f"Slide {slide_index}: No [EMPHASIS] marker"))

    # R4: Bullet-point check
    if has_bullet_style(monologue):
        issues.append(CRITICAL("R4", f"Slide {slide_index}: Bullet-point style detected"))

    return {
        "valid": len([i for i in issues if i.severity == "CRITICAL"]) == 0,
        "issues": issues
    }
```

### Step 2: Presentation-Level Validation

```python
def validate_presentation(all_results):
    total_pause = sum(r.markers["PAUSE"] for r in all_results)
    total_emphasis = sum(r.markers["EMPHASIS"] for r in all_results)
    total_check = sum(r.markers["CHECK"] for r in all_results)

    issues = []
    if total_pause < 24:
        issues.append(CRITICAL("R6", f"Total [PAUSE] ({total_pause}) < 24 minimum"))
    if total_emphasis < 12:
        issues.append(CRITICAL("R6", f"Total [EMPHASIS] ({total_emphasis}) < 12 minimum"))
    if total_check < 3:
        issues.append(CRITICAL("R6", f"Total [CHECK] ({total_check}) < 3 minimum"))

    return issues
```

---

## Example Validation Report

```
============================================================
MONOLOGUE VALIDATION SUMMARY
============================================================
STATUS: PASSED (16/16 slides)

Total Words: 2,847
Estimated Duration: 19.0 minutes

Marker Totals:
  [PAUSE]: 38 (min: 24) ✓
  [EMPHASIS]: 14 (min: 12) ✓
  [CHECK]: 5 (min: 3) ✓
  [GESTURE]: 22
  [TRANSITION]: 15

Per-Slide Results:
  Slide 1 (agenda): 142 words, 3 [PAUSE], 1 [EMPHASIS] ✓
  Slide 2 (warmup): 156 words, 4 [PAUSE], 2 [EMPHASIS] ✓
  Slide 3 (content): 178 words, 3 [PAUSE], 1 [EMPHASIS] ✓
  ... (all passing)
  Slide 16 (journal): 161 words, 3 [PAUSE], 1 [EMPHASIS] ✓

============================================================
VALIDATION: PASSED
============================================================
```

---

## Failure Report Example

```
============================================================
MONOLOGUE VALIDATION SUMMARY
============================================================
STATUS: FAILED (14/16 slides passed)

Issues Found:
  [CRITICAL] R1: Slide 7 - Only 98 words. MINIMUM is 150.
  [CRITICAL] R2: Slide 7 - Only 1 [PAUSE] marker. MINIMUM is 2.
  [CRITICAL] R3: Slide 12 - No [EMPHASIS] markers. MINIMUM is 1.

============================================================
VALIDATION: FAILED - 3 critical issues must be resolved
============================================================
```

---

## Integration with Pipeline

The monologue validator runs:
1. **After monologue generation** - Validates generated content
2. **Before PPTX export** - Final gate check
3. **Cannot be skipped** - Part of hardcoded enforcement

```python
# In pipeline
from skills.enforcement import validate_presentation_monologues

result = validate_presentation_monologues(monologues)
if not result["valid"]:
    raise ValidationError(f"Monologue validation failed: {result['issues']}")
```

---

## Remediation Actions

When validation fails, the pipeline MUST:

1. **R1 Failures (word count):** Regenerate monologue with expanded content
2. **R2 Failures ([PAUSE]):** Insert additional pause markers at natural break points
3. **R3 Failures ([EMPHASIS]):** Add emphasis markers around vocabulary terms
4. **R4 Failures (bullet style):** Rewrite in conversational prose
5. **R6 Failures (totals):** Regenerate affected slides to meet minimums

---

**Agent Version:** 1.0
**Last Updated:** 2026-01-09
**Pipeline:** Theater Education
**Type:** HARDCODED VALIDATOR (cannot be bypassed)
