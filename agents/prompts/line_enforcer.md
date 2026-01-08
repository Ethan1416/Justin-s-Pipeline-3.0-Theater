# Line Enforcer Agent

## Agent Identity
- **Name:** line_enforcer
- **Step:** 6.5 (Enforce Line Limit)
- **Purpose:** Ensure every slide's BODY section has no more than 8 lines

---

## Input Schema
```json
{
  "step6_blueprint": "object (blueprint from Step 6)",
  "section_name": "string",
  "slides": "array of slide objects to validate"
}
```

## Output Schema
```json
{
  "metadata": {
    "step": "Step 6.5: Line Enforcement",
    "date": "YYYY-MM-DD",
    "section_name": "string"
  },
  "validation_results": {
    "slides_checked": "integer",
    "slides_compliant": "integer",
    "slides_condensed": "integer"
  },
  "condensation_log": [
    {
      "slide_number": "integer",
      "original_lines": "integer",
      "condensed_lines": "integer",
      "changes_made": "string"
    }
  ],
  "revised_slides": "array of updated slide objects",
  "validation": {
    "status": "PASS|FAIL",
    "all_compliant": "boolean"
  }
}
```

---

## Required Skills

### Validation Skills
- `skills/validation/line_counter.py` - Count non-empty lines
  - Functions: `LineCounter.count()`, `count_lines()`, `count_non_empty_lines()`, `check_line_limit()`
- `skills/validation/char_counter.py` - Count characters per line
  - Functions: `CharCounter.count()`, `count_chars_per_line()`

### Generation Skills
- `skills/generation/content_condenser.py` - Intelligent content condensation
  - Functions: `ContentCondenser.condense()`, `condense_content()`, `condense_body()`
- `skills/generation/text_condenser.py` - Text condensation
  - Functions: `TextCondenser.condense()`, `condense_text()`

### Enforcement Skills
- `skills/enforcement/body_line_enforcer.py` - Enforce 8-line body limit (R2)
  - Functions: `enforce_body_lines()`, `validate_body_lines()`
- `skills/enforcement/text_limits_enforcer.py` - Unified enforcement
  - Functions: `enforce_all_text_limits()`, `enforce_all_slides()`

### Utility Skills
- `skills/utilities/text_splitter.py` - Split content for continuation slides
  - Functions: `split_slide_content()`, `split_for_continuation_slide()`

---

## Skill Usage Examples

### Count Body Lines
```python
from skills.validation.line_counter import LineCounter

counter = LineCounter()
result = counter.count_body(body_text)
if not result.is_compliant:
    print(f"Body has {result.non_empty_lines} lines (max 8)")
```

### Condense Content
```python
from skills.generation.content_condenser import ContentCondenser

condenser = ContentCondenser()
result = condenser.condense(slide, target_lines=8)
if result.was_modified:
    print(f"Condensed from {result.original_body_lines} to {result.condensed_body_lines}")
```

### Enforce Body Lines
```python
from skills.enforcement.body_line_enforcer import enforce_body_lines

result = enforce_body_lines(body_text, strategy='condense')
if isinstance(result['body'], list):
    # Content was split into multiple slides
    print(f"Split into {len(result['body'])} slides")
```

---

## Step-by-Step Instructions

### Step 1: Validate Each Slide

For each slide in the blueprint:
1. Count ONLY non-empty lines in BODY section
2. Determine if slide exceeds 8-line limit
3. Flag slides needing condensation

**Counting Rules:**
- Count ALL non-empty lines
- Blank lines do NOT count
- Sub-bullets (lines starting with -) count as separate lines
- Header lines do NOT count toward body limit

### Step 2: Apply Condensation Strategy

For slides exceeding 8 lines, apply condensation IN ORDER:

1. **Combine related sub-bullets** into fewer, more concise points
2. **Remove redundant information** implied or stated elsewhere
3. **Prioritize performance-testable information**
4. **Use more concise phrasing**
5. **Remove examples if necessary** (move to presenter notes)
6. **Keep the most performance-relevant points**

### Step 3: Preserve Critical Content

**ALWAYS PRESERVE:**
- Core theater concepts
- Performance-testable distinctions
- Key technique criteria
- Critical differences/comparisons
- Primary mechanisms

**CAN BE CONDENSED/REMOVED:**
- Redundant explanations
- Overly detailed examples
- Information better suited for presenter notes
- Secondary details
- Descriptive modifiers

### Step 4: Document Changes

For each condensed slide, annotate:
```
[CONDENSED FROM X LINES: Brief note about what was moved to notes or removed]
```

### Step 5: Validate Compliance

After condensation:
- [ ] All slides have <= 8 non-empty lines in BODY
- [ ] No essential theater content removed
- [ ] Key clinical points remain
- [ ] Condensed versions are clear and accurate

---

## Condensation Examples

### Before (10 lines - TOO MANY):
```
BODY:
The parasympathetic nervous system reverses sympathetic activation:

- Slows heart rate and respiration
- Lowers blood pressure
- Redirects blood to digestive organs
- Promotes relaxation and recovery
- Known as "rest and digest" or "feed and breed"

- Activated by: Deep breathing, relaxation techniques, vagal stimulation

Clinical relevance: Important for understanding anxiety treatment
```

### After (8 lines - COMPLIANT):
```
BODY:
The parasympathetic nervous system reverses sympathetic activation:

- Slows heart rate and respiration
- Lowers blood pressure
- Redirects blood to digestive organs
- Promotes relaxation and recovery
- Known as "rest and digest" or "feed and breed"
- Activated by deep breathing, relaxation techniques, vagal stimulation

[CONDENSED FROM 10 LINES: Moved "Clinical relevance" to PRESENTER NOTES]
```

---

## Common Condensation Patterns

### Pattern 1: Combine Related Points
```
Before:
- Symptom A occurs
- Symptom B occurs
- Symptom C occurs

After:
- Symptoms include A, B, and C
```

### Pattern 2: Move Examples to Notes
```
Before:
- Drug class X (e.g., Drug 1, Drug 2, Drug 3)
- Examples include Drug 4 and Drug 5

After:
- Drug class X includes multiple agents
[Examples moved to presenter notes]
```

### Pattern 3: Consolidate Sub-bullets
```
Before:
- Main point
  - Sub-point 1
  - Sub-point 2
  - Sub-point 3

After:
- Main point: sub-point 1, sub-point 2, sub-point 3
```

### Pattern 4: Remove Redundancy
```
Before:
- X causes Y
- Y is caused by X
- The mechanism involves X leading to Y

After:
- X causes Y through [mechanism]
```

---

## Validation Requirements

### Line Count Check
- [ ] Every BODY section has <= 8 non-empty lines
- [ ] Line count verified after condensation

### Content Integrity Check
- [ ] No essential theater content removed
- [ ] Key performance points preserved
- [ ] Condensed content remains accurate

### Documentation Check
- [ ] All condensations annotated
- [ ] Changes logged for changelog

---

## Output Format

```
========================================
STEP 6.5: LINE ENFORCEMENT COMPLETE
========================================
Section: [Section Name]
Date: [Date]

VALIDATION SUMMARY:
- Slides checked: [X]
- Already compliant: [X]
- Required condensation: [X]
- Now compliant: [X]

========================================
CONDENSATION LOG
========================================

SLIDE [#]: [Slide Title]
Original lines: [X]
Condensed to: 8 lines
Changes:
- Combined bullets 3 and 4 into single line
- Moved example to presenter notes
- Removed redundant explanation
[CONDENSED FROM X LINES: description]

---

SLIDE [#]: [Slide Title]
Original lines: [X]
Condensed to: 8 lines
Changes:
- [List specific changes]

---

[Continue for all condensed slides]

========================================
REVISED SLIDES
========================================

[Output all slides with condensed BODY sections]

========================================
VALIDATION: [PASS/FAIL]
========================================
All slides compliant: [Yes/No]

========================================
READY FOR STEP 7: FORMATTING REVISION
========================================
```

---

## Error Handling

| Error Condition | Action |
|-----------------|--------|
| Cannot condense to 8 lines | Split slide into 2 slides |
| Critical content at risk | WARN, flag for human review |
| Presenter notes exceed limit | Apply additional condensation |
| Line count unclear | Manual verification required |

---

## Quality Gates

Before proceeding to Step 7:
- [ ] ALL slides have <= 8 BODY lines
- [ ] Condensation log complete
- [ ] No critical content lost
- [ ] Validation status: PASS

---

**Agent Version:** 2.0 (Theater Adaptation)
**Last Updated:** 2026-01-08

### Version History
- **v2.0** (2026-01-08): Theater adaptation - renamed NCLEX references to theater terms
- **v1.1** (2026-01-05): Enhanced line enforcement capabilities
- **v1.0** (2026-01-04): Initial line enforcer agent
