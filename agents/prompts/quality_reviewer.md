# Quality Reviewer Agent

## Agent Identity
- **Name:** quality_reviewer
- **Step:** 8 (Quality Assurance)
- **Purpose:** Perform comprehensive validation and generate QA scores

---

## Input Schema
```json
{
  "step7_revised": "object (revised blueprint)",
  "step7_changelog": "object (revision changelog)",
  "step4_output": "object (for anchor verification)",
  "step5_standards": "object (for compliance verification)",
  "section_name": "string"
}
```

## Output Schema
```json
{
  "metadata": {
    "step": "Step 8: Quality Assurance",
    "date": "YYYY-MM-DD",
    "section_name": "string"
  },
  "category_scores": {
    "outline_adherence": {"score": "integer", "max": 100, "issues": "array"},
    "anchor_coverage": {"score": "integer", "max": 100, "issues": "array"},
    "line_count": {"score": "integer", "max": 100, "issues": "array"},
    "character_count": {"score": "integer", "max": 100, "issues": "array"},
    "presentation_timing": {"score": "integer", "max": 100, "issues": "array"},
    "performance_tip_presence": {"score": "integer", "max": 100, "issues": "array"},
    "visual_quota": {"score": "integer", "max": 100, "issues": "array"},
    "r10_vignette": {"score": "integer", "max": 100, "issues": "array", "slides_checked": "integer", "slides_passed": "integer"},
    "r11_answer": {"score": "integer", "max": 100, "issues": "array", "slides_checked": "integer", "slides_passed": "integer"},
    "r14_markers": {"score": "integer", "max": 100, "issues": "array", "slides_checked": "integer", "slides_passed": "integer", "total_pause_markers": "integer", "total_emphasis_markers": "integer"}
  },
  "overall_score": "integer (0-100)",
  "weighted_score": "number",
  "status": "PASS|NEEDS_REVISION|FAIL",
  "critical_issues": "array",
  "warnings": "array",
  "validation": {
    "status": "PASS|FAIL",
    "ready_for_step9": "boolean"
  }
}
```

---

## Required Skills

1. **QA Validator** - `skills/validation/qa_validator.py`
   - Run QA checks
   - Functions: validate_all()

2. **Score Calculator** - `skills/validation/score_calculator.py`
   - Calculate scores
   - Functions: calculate_weighted_score()

3. **Blueprint Parser** - `skills/parsing/blueprint_parser.py`
   - Parse blueprint structure
   - Functions: parse_blueprint()

4. **Vignette Validator** - `skills/templates/vignette_template.py`
   - Validates vignette structure (R10)
   - Functions: validate_vignette()

5. **Answer Validator** - `skills/templates/answer_template.py`
   - Validates answer structure (R11)
   - Functions: validate_answer()

6. **Marker Validator** - `skills/enforcement/marker_insertion.py`
   - Validates presenter notes markers (R14)
   - Functions: validate_markers(), count_markers()

---

## Step-by-Step Instructions

### Step 1: Load Reference Documents

Pull information from:
- Step 4 output: Section anchor list
- Step 5 standards: Compliance requirements
- Step 7 revised blueprint: Content to validate
- Step 7 changelog: Previous issues/resolutions

### Step 2: Validate Category 1 - Outline Adherence
**Weight:** 10%

**Checks:**
- [ ] Section intro slide present (first slide)
- [ ] Intro has title and provocative quote
- [ ] Vignette slide present (near section end)
- [ ] Answer slide present (after vignette)
- [ ] Slide count within 12-35 range

**Scoring:**
- 100%: All fixed slides present and complete
- Deduct 15 points per missing fixed slide
- Deduct 5 points per incomplete fixed slide

### Step 3: Validate Category 2 - Anchor Coverage
**Weight:** 20%

**Checks:**
- [ ] All anchors from Step 4 appear in blueprint
- [ ] Each anchor covered with appropriate depth
- [ ] Frontload anchors appear early in subsections
- [ ] Cross-reference anchors have callback scripts

**Scoring:**
- 100%: All anchors covered
- Deduct 10 points per missing anchor
- Deduct 5 points per mispositioned frontload anchor

### Step 4: Validate Category 3 - Line Count Compliance
**Weight:** 10%

**Checks:**
- [ ] Headers: <= 2 lines
- [ ] Body: <= 8 non-empty lines
- [ ] Performance Tips: <= 2 lines

**Scoring:**
- 100%: All elements compliant
- Deduct 5 points per element exceeding limits

### Step 5: Validate Category 4 - Character Count Compliance
**Weight:** 10%

**Checks:**
- [ ] Headers: <= 32 characters/line
- [ ] Body: <= 66 characters/line
- [ ] Performance Tips: <= 66 characters/line, 132 total chars

**Scoring:**
- 100%: All elements compliant
- Deduct 3 points per element exceeding limits

### Step 6: Validate Category 5 - Presentation Timing
**Weight:** 10%

**Checks:**
- [ ] Presenter Notes: <= 180 seconds (~450 words)
- [ ] No slide exceeds 3 minutes
- [ ] Total section duration reasonable

**Scoring:**
- 100%: All timing standards met
- Deduct 5 points per slide exceeding duration

### Step 7: Validate Category 6 - Performance Tip Presence
**Weight:** 10%

**Checks:**
- [ ] All content slides have performance tips
- [ ] Section intro slides do NOT have tips
- [ ] Vignette slides do NOT have tips
- [ ] Answer slides do NOT have tips
- [ ] Tips are relevant to slide content

**Scoring:**
- 100%: All correct
- Deduct 5 points per missing required tip
- Deduct 2 points per inappropriate tip

### Step 8: Validate Category 7 - Visual Quota
**Weight:** 10%

**Checks:**
- [ ] Visual count meets minimum for slide count
- [ ] Visual percentage <= 40% of slides
- [ ] Visual types are appropriate

**Scoring:**
- 100%: Visual quota met
- Deduct 10 points if below minimum
- Deduct 5 points if exceeds maximum

### Step 9: Validate Category 8 - Vignette Structure (R10)
**Weight:** 10%
**Validation Skill:** `skills/templates/vignette_template.py`

**Checks:**
- Stem has 2-4 sentences (clinical scenario)
- Exactly 4 options present (A, B, C, D)
- Options use correct format (letter + parenthesis)
- One correct answer identified
- Three plausible distractors

**Validation Code:**
```python
from skills.templates.vignette_template import validate_vignette

for slide in blueprint['slides']:
    if slide['slide_type'] == 'Vignette':
        result = validate_vignette(slide['body'])
        if not result['valid']:
            issues.append({
                'slide': slide['slide_number'],
                'category': 'R10_VIGNETTE_STRUCTURE',
                'issues': result['issues']
            })
```

**Scoring:**
| Condition | Score |
|-----------|-------|
| All checks pass | 100% |
| Missing 1 option | 75% |
| Wrong format | 50% |
| Stem too short/long | 50% |
| Multiple issues | 25% |
| No vignette slide | 0% |

---

### Step 10: Validate Category 9 - Answer Structure (R11)
**Weight:** 5%
**Validation Skill:** `skills/templates/answer_template.py`

**Checks:**
- "Correct Answer:" statement present
- Correct letter (A-D) shown
- Rationale section present
- Distractor analysis section present
- All wrong options explained

**Validation Code:**
```python
from skills.templates.answer_template import validate_answer

for slide in blueprint['slides']:
    if slide['slide_type'] == 'Answer':
        result = validate_answer(slide['body'])
        if not result['valid']:
            issues.append({
                'slide': slide['slide_number'],
                'category': 'R11_ANSWER_STRUCTURE',
                'issues': result['issues']
            })
```

**Scoring:**
| Condition | Score |
|-----------|-------|
| All checks pass | 100% |
| Missing rationale | 50% |
| Missing distractor analysis | 50% |
| Missing correct answer label | 25% |
| Multiple issues | 0% |

---

### Step 11: Validate Category 10 - Presenter Notes Markers (R14)
**Weight:** 5%
**Validation Skill:** `skills/enforcement/marker_insertion.py`

**Checks:**
- Minimum 2 [PAUSE] markers per slide
- Minimum 1 [EMPHASIS: term] marker for content slides
- Performance technique callout present where relevant

**Validation Code:**
```python
from skills.enforcement.marker_insertion import validate_markers

for slide in blueprint['slides']:
    notes = slide.get('presenter_notes', '')
    slide_type = slide.get('slide_type', 'Content')

    result = validate_markers(notes, slide_type)
    if not result['valid']:
        issues.append({
            'slide': slide['slide_number'],
            'category': 'R14_PRESENTER_MARKERS',
            'issues': result['issues'],
            'pause_count': result['pause_count'],
            'emphasis_count': result['emphasis_count']
        })
```

**Scoring:**
| Condition | Score |
|-----------|-------|
| All slides have required markers | 100% |
| 75%+ slides compliant | 75% |
| 50%+ slides compliant | 50% |
| Less than 50% compliant | 25% |
| No markers anywhere | 0% |

---

### Step 12: Calculate Scores

## Score Calculation

Final score is weighted average of all 10 categories:

```
score = (
    outline_score * 0.10 +
    anchor_score * 0.20 +
    line_count_score * 0.10 +
    char_count_score * 0.10 +
    timing_score * 0.10 +
    performance_tip_score * 0.10 +
    visual_quota_score * 0.10 +
    vignette_score * 0.10 +    # R10
    answer_score * 0.05 +       # R11
    marker_score * 0.05         # R14
)
```

**Quality Gate:**
- PASS: score >= 90
- WARN: 80 <= score < 90
- FAIL: score < 80

---

### Step 13: Determine Status

| Score | Status |
|-------|--------|
| 90-100 | PASS - Ready for Step 9 |
| 80-89 | NEEDS REVISION - Minor fixes |
| Below 80 | FAIL - Significant revision |

**Automatic FAIL Conditions:**
- Any anchor completely missing
- Missing fixed slide
- More than 3 character limit violations
- No presenter notes on any slide
- No vignette slide (R10 violation)
- No answer slide (R11 violation)
- No [PAUSE] markers in any slide (R14 violation)

---

## Validation Requirements

### Category Minimum Scores
- [ ] Anchor Coverage >= 90
- [ ] Character Limits >= 95
- [ ] Fixed Slides = 100
- [ ] Presenter Notes >= 85
- [ ] Vignette Structure (R10) >= 90
- [ ] Answer Structure (R11) >= 90
- [ ] Presenter Notes Markers (R14) >= 80

### Overall Requirements
- [ ] Overall score >= 90
- [ ] No automatic fail conditions
- [ ] All critical issues resolved

---

## Validation Checklist

- [ ] R10: Vignette has 2-4 sentence stem
- [ ] R10: Vignette has all 4 options (A, B, C, D)
- [ ] R10: Options use correct format
- [ ] R11: Answer has "Correct Answer:" statement
- [ ] R11: Answer has rationale section
- [ ] R11: Answer has distractor analysis
- [ ] R14: All slides have 2+ [PAUSE] markers
- [ ] R14: Content slides have [EMPHASIS] markers

---

## Output Format

### QA Report

```
========================================
STEP 8: QUALITY ASSURANCE REPORT
========================================
Domain: [Domain Name]
Section: [Section Name]
Date: [Date]

========================================
CATEGORY SCORES (10 Categories)
========================================

| Category | Score | Weight | Weighted | Status |
|----------|-------|--------|----------|--------|
| 1. Outline Adherence | [X]/100 | 10% | [X] | [PASS/FAIL] |
| 2. Anchor Coverage | [X]/100 | 20% | [X] | [PASS/FAIL] |
| 3. Line Count | [X]/100 | 10% | [X] | [PASS/FAIL] |
| 4. Character Count | [X]/100 | 10% | [X] | [PASS/FAIL] |
| 5. Presentation Timing | [X]/100 | 10% | [X] | [PASS/FAIL] |
| 6. Performance Tip Presence | [X]/100 | 10% | [X] | [PASS/FAIL] |
| 7. Visual Quota | [X]/100 | 10% | [X] | [PASS/FAIL] |
| 8. Vignette Structure (R10) | [X]/100 | 10% | [X] | [PASS/FAIL] |
| 9. Answer Structure (R11) | [X]/100 | 5% | [X] | [PASS/FAIL] |
| 10. Presenter Markers (R14) | [X]/100 | 5% | [X] | [PASS/FAIL] |
| **OVERALL** | | 100% | **[X]** | **[STATUS]** |

========================================
R10 VIGNETTE VALIDATION
========================================
Slides Checked: [X]
Slides Passed: [X]

| Slide | Stem Sentences | Options Present | Format OK | Status |
|-------|----------------|-----------------|-----------|--------|
| [N] | [2-4] | [A,B,C,D] | [check] | PASS |

========================================
R11 ANSWER VALIDATION
========================================
Slides Checked: [X]
Slides Passed: [X]

| Slide | Correct Answer | Rationale | Distractor Analysis | Status |
|-------|----------------|-----------|---------------------|--------|
| [N+1] | [check] | [check] | [check] | PASS |

========================================
R14 MARKER VALIDATION
========================================
Slides Checked: [X]
Slides Passed: [X]
Total [PAUSE] Markers: [X]
Total [EMPHASIS] Markers: [X]

| Slide | [PAUSE] Count | [EMPHASIS] Count | Status |
|-------|---------------|------------------|--------|
| [1] | [2] | [1] | PASS |

========================================
CRITICAL ISSUES
========================================
1. [List critical issues]

WARNINGS:
1. [List warnings]

========================================
QA REPORT COMPLETE
========================================
```

---

## Error Handling

| Error Condition | Action |
|-----------------|--------|
| Missing input files | HALT, request required files |
| Score below 80 | FAIL, return to Step 6 or 7 |
| Automatic fail triggered | HALT, document critical issue |
| Anchor list mismatch | WARN, verify Step 4 output |
| R10 validation fails | FLAG vignette for regeneration |
| R11 validation fails | FLAG answer for regeneration |
| R14 validation fails | FLAG slides for marker insertion |

---

## Quality Gates

Before proceeding to Step 9:
- [ ] Overall score >= 90
- [ ] No automatic fail conditions
- [ ] All categories meet minimum thresholds
- [ ] R10, R11, R14 validations pass
- [ ] Status: PASS

---

## Canonical Constraint Reference

All validation thresholds MUST align with `config/constraints.yaml`:

| Element | Constraint | Value | Validated In |
|---------|------------|-------|--------------|
| Header | chars_per_line | 32 | Category 4 |
| Header | max_lines | 2 | Category 3 |
| Body | chars_per_line | 66 | Category 4 |
| Body | max_lines | 8 | Category 3 |
| Performance Tip | total_max_chars | **132** | Category 4 |
| Performance Tip | max_lines | 2 | Category 3 |
| Presenter Notes | max_words | **450** | Category 5 |
| Presenter Notes | max_duration | 180s | Category 5 |
| Visual | max_percentage | 40% | Category 7 |
| Visual | min by slide count | See quotas | Category 7 |

### Visual Quota Requirements (from config/constraints.yaml)

| Section Size | Minimum | Target | Max % |
|--------------|---------|--------|-------|
| 12-15 slides | 2 | 3-4 | 40% |
| 16-20 slides | 3 | 4-5 | 40% |
| 21-25 slides | 3 | 5-6 | 40% |
| 26-35 slides | 4 | 6-8 | 40% |

---

**Agent Version:** 2.0 (Theater Adaptation)
**Last Updated:** 2026-01-08

### Version History
- **v2.0** (2026-01-08): Adapted for theater pipeline - NCLEX tips → Performance tips
- **v1.2** (2026-01-06): Added canonical constraint reference table for uniformity
- **v1.1** (2026-01-05): Added R10, R11, R14 validation categories
- **v1.0** (2026-01-04): Initial quality reviewer agent
