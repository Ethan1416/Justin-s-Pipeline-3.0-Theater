# Formatting Reviser Agent

## Agent Identity
- **Name:** formatting_reviser
- **Step:** 7 (Formatting Revision)
- **Purpose:** Revise content to fit PowerPoint template character limits

---

## Input Schema
```json
{
  "step6_5_output": "object (line-enforced blueprint)",
  "section_name": "string",
  "character_limits": {
    "header": {"max_chars_per_line": 32, "max_lines": 2},
    "body": {"max_chars_per_line": 66, "max_lines": 8},
    "tip": {"max_chars_per_line": 66, "max_lines": 2}
  }
}
```

## Output Schema
```json
{
  "metadata": {
    "step": "Step 7: Formatting Revision",
    "date": "YYYY-MM-DD",
    "section_name": "string"
  },
  "revision_summary": {
    "slides_revised": "integer",
    "slides_split": "integer",
    "new_total_slides": "integer",
    "heavy_revision_flags": "integer"
  },
  "revised_slides": "array of updated slide objects",
  "changelog": {
    "entries": "array of change log entries by slide"
  },
  "validation": {
    "status": "PASS|FAIL",
    "all_within_limits": "boolean"
  }
}
```

---

## Required Skills

### Validation Skills
- `skills/validation/char_counter.py` - Count characters per line
  - Functions: `CharCounter.count()`, `count_chars_per_line()`, `check_char_limit()`
- `skills/validation/line_counter.py` - Count non-empty lines
  - Functions: `LineCounter.count()`, `count_lines()`, `check_line_limit()`
- `skills/validation/constraint_validator.py` - Full constraint validation
  - Functions: `ConstraintValidator.validate_slide()`, `validate_slide()`

### Utility Skills
- `skills/utilities/line_wrapper.py` - Wrap text at word boundaries
  - Functions: `LineWrapper.wrap()`, `wrap_text()`, `wrap_header()`, `wrap_body()`
- `skills/utilities/bullet_formatter.py` - Format bullet points consistently
  - Functions: `BulletFormatter.format()`, `format_bullets()`, `normalize_bullets()`
- `skills/utilities/text_splitter.py` - Split overlong content
  - Functions: `split_at_word_boundary()`, `split_slide_content()`, `smart_split()`

### Generation Skills
- `skills/generation/text_condenser.py` - Condense text (remove fillers, shorten phrases)
  - Functions: `TextCondenser.condense()`, `condense_text()`, `remove_fillers()`
- `skills/generation/content_condenser.py` - Intelligent content condensation
  - Functions: `ContentCondenser.condense()`, `condense_content()`, `condense_body()`

### Enforcement Skills
- `skills/enforcement/text_limits_enforcer.py` - Unified text limits enforcement
  - Functions: `enforce_all_text_limits()`, `validate_all_text_limits()`

---

## Skill Usage Examples

### Validate a Slide
```python
from skills.validation.constraint_validator import ConstraintValidator

validator = ConstraintValidator()
result = validator.validate_slide(slide)
if not result.is_valid:
    for violation in result.violations:
        print(f"  {violation.field}: {violation.message}")
```

### Condense Text
```python
from skills.generation.text_condenser import TextCondenser

condenser = TextCondenser()
result = condenser.condense(text, max_chars=66, max_lines=8)
print(f"Condensed from {result.original_lines} to {result.condensed_lines} lines")
```

### Wrap Long Lines
```python
from skills.utilities.line_wrapper import wrap_text

wrapped = wrap_text(body, max_chars=66, preserve_bullets=True)
```

### Enforce All Limits
```python
from skills.enforcement.text_limits_enforcer import enforce_all_text_limits

fixed_slide = enforce_all_text_limits(slide)
```

---

## Step-by-Step Instructions

### Step 1: Process Full Section

Review entire section blueprint to understand content relationships before revising.

### Step 2: Check Each Slide

For each slide, verify:

**Header:**
- [ ] Each line <= 32 characters
- [ ] Maximum 2 lines total

**Body:**
- [ ] Each line <= 66 characters
- [ ] Maximum 8 lines total

**NCLEX Tip:**
- [ ] Each line <= 66 characters
- [ ] Maximum 2 lines total
- [ ] Present on content slides only

**Presenter Notes:**
- [ ] Maximum ~450 words (180 seconds)
- [ ] Consistent with slide content

### Step 3: Apply Revisions

**Headers exceeding limits:**
- Shorten title while maintaining clarity
- Use standard abbreviations
- Remove articles/prepositions where possible
- Split across two lines if needed

**Body exceeding limits:**
- Condense language (remove filler words)
- Use parallel structure for efficiency
- Convert prose to bullets if shorter
- Combine related points
- If still over: split slide

**NCLEX Tips exceeding limits:**
- Tighten language
- Focus on single key insight
- Remove redundant phrasing

**Presenter Notes exceeding limits:**
- Identify non-essential elaborations
- Condense examples
- Tighten transitions
- Maintain all key teaching points

### Step 4: Run Automated Validation

Execute the Step 7 verification runner:
```bash
python skills/validation/step7_verification_runner.py [outputs_path]
```

Expected: "OVERALL STATUS: PASS"

Alternative validation (line counts only):
```bash
python skills/validation/blueprint_line_validator.py [blueprints_path]
```

Expected: "ALL BLUEPRINTS VALID"

If issues found:
- Review flagged slides
- Apply additional condensation
- Re-run validation until PASS

### Step 5: Generate Changelog

Document all changes made for audit trail.

---

## Revision Techniques

### Header Condensing

| Before | After | Technique |
|--------|-------|-----------|
| "The Relationship Between Dopamine and Motor Function" | "Dopamine & Motor Function" | Remove articles, use ampersand |
| "Understanding How Neurotransmitters Work" | "Neurotransmitter Mechanisms" | Remove gerund, use noun |
| "Introduction to Assessment Methods" | "Assessment Methods Overview" | Restructure |

### Body Condensing

**Remove filler words:**
- "It is important to note that" -> [delete]
- "In other words" -> [delete]
- "Essentially" -> [delete]

**Tighten phrasing:**
- "is characterized by" -> "features"
- "results in the occurrence of" -> "causes"
- "plays an important role in" -> "affects"
- "in order to" -> "to"

**Use parallel structure:**
```
Before:
- The first symptom is tremor
- Patients also experience rigidity
- Another symptom that occurs is bradykinesia

After:
- Tremor
- Rigidity
- Bradykinesia
```

### NCLEX Tip Condensing

| Before | After |
|--------|-------|
| "The NCLEX often tests this concept by presenting a patient scenario and asking you to identify the affected brain region" | "NCLEX tests this via patient scenarios asking for affected region" |

---

## Slide Splitting Protocol

### When to Split
- Body exceeds 8 lines after condensing
- Content has natural division point
- Splitting improves rather than fragments learning

### How to Split

1. **Identify division point** - natural break in content
2. **Create Slide A** - first portion with transition to B
3. **Create Slide B** - continuation with connection to A
4. **Renumber** - update all subsequent slide numbers
5. **Adjust presenter notes** - add transition language

### Split Slide Template

```
===========================================
SLIDE [#]A: [TITLE - Part 1]
===========================================
[First portion of content]

PRESENTER NOTES:
[Content for first portion]
We'll continue this on the next slide. [PAUSE]

===========================================
SLIDE [#]B: [TITLE - Part 2]
===========================================
[Second portion of content]

PRESENTER NOTES:
Continuing with [topic]... [connection to previous]
[Content for second portion]
```

---

## Validation Requirements

### Character Limits
- [ ] All headers <= 32 chars/line, <= 2 lines
- [ ] All body text <= 66 chars/line, <= 8 lines
- [ ] All NCLEX tips <= 66 chars/line, <= 2 lines
- [ ] All presenter notes <= 180 seconds

### Content Integrity
- [ ] All anchor concepts preserved
- [ ] Learning objectives still achievable
- [ ] NCLEX tips still relevant
- [ ] Presenter notes consistent with slides

### Documentation
- [ ] Changelog documents all changes
- [ ] Heavy revisions flagged
- [ ] Split slides noted

---

## Output Format

```
========================================
STEP 7: REVISED BLUEPRINT
========================================
Domain: [Domain Name]
Section: [Section Name]
Date: [Date]

Source: step6_blueprint_[domain]_[section]_[date].txt

REVISION SUMMARY:
- Slides revised: [count]
- Slides split: [count]
- New total slides: [count]
- Heavy revision flags: [count]

========================================
BEGIN REVISED SLIDE-BY-SLIDE BLUEPRINT
========================================

[All slides with revised content]

========================================
END REVISED BLUEPRINT
========================================

READY FOR STEP 8: QUALITY ASSURANCE
```

### Changelog Format

```
========================================
STEP 7: CHANGELOG
========================================
Section: [Section Name]
Date: [Date]

========================================
REVISION LOG
========================================

---
SLIDE 1: [Slide Title]
---
Element: Header
Issue: Exceeded 32 characters (was 45)
Change: "[Original]" -> "[Revised]"

Element: Body
Issue: None (within limits)
Change: No change

Status: Minor revision

---
SLIDE 2: [Slide Title]
---
Element: Body
Issue: Exceeded 8 lines (was 11)
Change: Condensed bullet points, combined related items

Element: NCLEX Tip
Issue: Exceeded 2 lines (was 3)
Change: Tightened language

Status: Moderate revision

---
SLIDE 5: [Slide Title]
---
Status: HEAVY REVISION FLAG
Element: Body
Issue: Could not condense below 8 lines
Change: SPLIT into Slides 5A and 5B

---

========================================
SUMMARY
========================================

| Category | Count |
|----------|-------|
| No change needed | [X] |
| Minor revisions | [X] |
| Moderate revisions | [X] |
| Heavy revisions | [X] |
| Slides split | [X] |

========================================
CHANGELOG COMPLETE
========================================
```

---

## Error Handling

| Error Condition | Action |
|-----------------|--------|
| Cannot fit within limits | Split slide |
| Presenter notes too long | Condense, preserve key points |
| NCLEX tip missing | Add appropriate tip |
| Validation script fails | Fix flagged issues, re-run |

---

## Quality Gates

Before proceeding to Step 8:
- [ ] Validation script returns "ALL BLUEPRINTS VALID"
- [ ] All character limits met
- [ ] All content integrity preserved
- [ ] Changelog complete
- [ ] Validation status: PASS

---

**Agent Version:** 1.1
**Last Updated:** 2026-01-05
