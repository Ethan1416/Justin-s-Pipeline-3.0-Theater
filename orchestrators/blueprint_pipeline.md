# Sub-Orchestrator: Blueprint Pipeline

**Version:** 1.7
**Purpose:** Handle Steps 6-11 - Per-section blueprint creation and refinement
**Parent:** `lecture_pipeline.md`

---

## Overview

The Blueprint Pipeline orchestrates the creation and refinement of slide blueprints for each section. This phase runs once per section and produces integrated blueprints with visual markers ready for PowerPoint generation.

---

## Agents Managed

| Agent | Step | Purpose | Input Schema | Output Schema |
|-------|------|---------|--------------|---------------|
| blueprint_generator | 6 | Generate initial slide blueprints | blueprint_input.schema.json | blueprint_output.schema.json |
| line_enforcer | 6.5 | Enforce line limits | enforce_input.schema.json | enforce_output.schema.json |
| formatting_reviser | 7 | Apply formatting constraints | format_input.schema.json | format_output.schema.json |
| quality_reviewer | 8 | Validate against all standards | qa_input.schema.json | qa_output.schema.json |
| visual_identifier | 9 | Identify visual aid opportunities | visual_id_input.schema.json | visual_id_output.schema.json |
| visual_integrator | 10 | Merge visuals into blueprints | integrate_input.schema.json | integrate_output.schema.json |
| blueprint_organizer | 11 | Organize final blueprint structure | org_input.schema.json | org_output.schema.json |

### Supporting Agents

| Agent | Purpose | Used By Step |
|-------|---------|--------------|
| constraint_validator | Validate character/line limits | 7, 8 |
| presenter_notes_writer | Generate presenter notes | 6 |
| tip_generator | Generate NCLEX exam tips | 6 |

---

## Skill Assignments (Implementation Status)

### Generation Skills

| Skill | Path | Status | Purpose |
|-------|------|--------|---------|
| slide_builder | skills/generation/slide_builder.py | ✓ IMPLEMENTED | Build slide structure from outline |
| content_expander | skills/generation/content_expander.py | ✓ IMPLEMENTED | Expand anchor content to slide format |
| visual_pattern_matcher | skills/generation/visual_pattern_matcher.py | ✓ IMPLEMENTED | Match content to visual types |
| ml_visual_recommender | skills/generation/ml_visual_recommender.py | ✓ IMPLEMENTED | ML-based visual type recommendation (P3) |
| presenter_notes_generator | skills/generation/presenter_notes_generator.py | TODO | Generate presenter notes |
| layout_selector | skills/generation/layout_selector.py | TODO | Select optimal layout variant |
| visual_merger | skills/generation/visual_merger.py | TODO | Merge visual specs into blueprint |
| sequence_optimizer | skills/generation/sequence_optimizer.py | TODO | Optimize slide sequence |

### Validation Skills

| Skill | Path | Status | Purpose |
|-------|------|--------|---------|
| anchor_coverage_tracker | skills/validation/anchor_coverage_tracker.py | ✓ IMPLEMENTED | Track anchor coverage (R8) |
| visual_quota_tracker | skills/validation/visual_quota_tracker.py | ✓ IMPLEMENTED | Track visual quota compliance |
| pipeline_validator | skills/validation/pipeline_validator.py | TODO | Full constraint validation |
| blueprint_line_validator | skills/validation/blueprint_line_validator.py | TODO | Validate line limits |
| score_calculator | skills/validation/score_calculator.py | TODO | Calculate QA score (0-100) |
| error_reporter | skills/validation/error_reporter.py | TODO | Generate detailed error reports |
| structure_validator | skills/validation/structure_validator.py | TODO | Validate final blueprint structure |

### Enforcement Skills

| Skill | Path | Status | Purpose |
|-------|------|--------|---------|
| header_enforcer | skills/enforcement/header_enforcer.py | ✓ IMPLEMENTED | R1: Header limits |
| body_line_enforcer | skills/enforcement/body_line_enforcer.py | ✓ IMPLEMENTED | R2: Body line limits |
| body_char_enforcer | skills/enforcement/body_char_enforcer.py | ✓ IMPLEMENTED | R3: Body char limits |
| text_limits_enforcer | skills/enforcement/text_limits_enforcer.py | ✓ IMPLEMENTED | Unified text limits |
| marker_insertion | skills/enforcement/marker_insertion.py | ✓ IMPLEMENTED | R14: Presenter notes markers |
| anchor_coverage_enforcer | skills/enforcement/anchor_coverage_enforcer.py | ✓ IMPLEMENTED | R8: Anchor coverage |
| slide_numbering | skills/enforcement/slide_numbering.py | ✓ IMPLEMENTED | R15: Sequential numbering |
| nclex_tip_fallback | skills/enforcement/nclex_tip_fallback.py | ✓ IMPLEMENTED | R4: NCLEX tips |

### Template Skills

| Skill | Path | Status | Purpose |
|-------|------|--------|---------|
| vignette_template | skills/templates/vignette_template.py | ✓ IMPLEMENTED | R10: Vignette structure |
| answer_template | skills/templates/answer_template.py | ✓ IMPLEMENTED | R11: Answer structure |

### Utility Skills

| Skill | Path | Status | Purpose |
|-------|------|--------|---------|
| text_splitter | skills/utilities/text_splitter.py | ✓ IMPLEMENTED | Smart text splitting |
| smart_retry_controller | skills/utilities/smart_retry_controller.py | ✓ IMPLEMENTED | Intelligent retry loops with context |
| step_state_manager | skills/utilities/step_state_manager.py | ✓ IMPLEMENTED | Inter-step state persistence |
| error_recovery | skills/utilities/error_recovery.py | ✓ IMPLEMENTED | Unified error handling |
| char_counter | skills/utilities/char_counter.py | TODO | Count characters per line |
| line_wrapper | skills/utilities/line_wrapper.py | TODO | Wrap text to character limits |
| bullet_formatter | skills/utilities/bullet_formatter.py | TODO | Format bullet points consistently |
| word_count | skills/utilities/word_count.py | TODO | Word counting for notes |
| marker_inserter | skills/utilities/marker_inserter.py | TODO | Insert Visual: Yes/No markers |

---

## Execution Order

```
Step 6: BLUEPRINT GENERATION
    ├── Input: Section outline from Step 4
    ├── Agent: blueprint_generator
    ├── Skills: slide_builder, content_expander, presenter_notes_generator
    ├── Output: Initial blueprint (may exceed limits)
    └── Save: outputs/blueprints/step6_blueprint_{domain}_{section}_{date}.txt

Step 6.5: LINE LIMIT ENFORCEMENT
    ├── Input: Step 6 output
    ├── Agent: line_enforcer
    ├── Skills: blueprint_line_validator, text_splitter
    ├── Constraints:
    │   ├── Title: 32 chars/line, max 2 lines
    │   ├── Body: 66 chars/line, max 8 lines
    │   └── Tip: 66 chars/line, max 2 lines
    └── Output: Line-enforced blueprint

Step 7: FORMATTING REVISION
    ├── Input: Step 6.5 output
    ├── Agent: formatting_reviser
    ├── Skills: char_counter, line_wrapper, bullet_formatter
    ├── Validation:
    │   ├── Agent: constraint_validator
    │   └── Check: All limits respected
    └── Output: Formatted blueprint
    └── Save: outputs/revisions/step7_revised_{domain}_{section}_{date}.txt
    └── Save: outputs/revisions/step7_changelog_{domain}_{section}_{date}.txt

Step 8: QUALITY ASSURANCE
    ├── Input: Step 7 output
    ├── Agent: quality_reviewer
    ├── Skills: pipeline_validator, score_calculator, error_reporter
    ├── Quality Gate:
    │   ├── Required score: >= 90/100
    │   ├── On PASS: Continue to Step 9
    │   └── On FAIL: Return to Step 7 with error context
    └── Output: QA report with score
    └── Save: outputs/qa_reports/step8_qa_report_{domain}_{section}_{date}.txt
    └── Save: outputs/qa_reports/step8_score_{domain}_{section}_{date}.txt

Step 9: VISUAL AID IDENTIFICATION
    ├── Input: Step 8 output (passed blueprint)
    ├── Agent: visual_identifier
    ├── Skills: visual_pattern_matcher, visual_quota_tracker, layout_selector
    ├── Visual Quotas (from config/constraints.yaml):
    │   ├── 12-15 slides: min 2, target 3-4
    │   ├── 16-20 slides: min 3, target 4-5
    │   ├── 21-25 slides: min 3, target 5-6
    │   └── 26-35 slides: min 4, target 6-8
    ├── Visual Types:
    │   ├── TABLE
    │   ├── FLOWCHART
    │   ├── DECISION_TREE
    │   ├── TIMELINE
    │   ├── HIERARCHY
    │   ├── SPECTRUM
    │   └── KEY_DIFFERENTIATORS
    └── Output: Visual specifications
    └── Save: outputs/visual_specs/step9_visual_specs_{domain}_{section}_{date}.txt

Step 10: VISUAL INTEGRATION REVISION
    ├── Input: Step 9 output + visual specs
    ├── Agent: visual_integrator
    ├── Skills: visual_merger, marker_inserter
    ├── Requirements:
    │   └── EVERY slide must have Visual: Yes or Visual: No marker
    └── Output: Integrated blueprint with visual markers
    └── Save: outputs/integrated/step10_integrated_{domain}_{section}_{date}.txt
    └── Save: outputs/integrated/step10_changelog_{domain}_{section}_{date}.txt

Step 11: BLUEPRINT ORGANIZATION
    ├── Input: Step 10 output
    ├── Agent: blueprint_organizer
    ├── Skills: structure_validator, sequence_optimizer
    └── Output: Final organized blueprint ready for PowerPoint
    └── Save: outputs/organized/step11_final_{domain}_{section}_{date}.txt
```

---

## Data Transformation Between Steps

### Step 6 → Step 6.5 Transformation

**Input (Step 6 Output):**
```json
{
  "metadata": {
    "section_number": 1,
    "section_name": "string",
    "generated_at": "timestamp"
  },
  "slides": [
    {
      "slide_number": 1,
      "slide_type": "Section Intro | Content | Vignette | Answer",
      "header": "string",
      "body": "string",
      "anchors_covered": ["anchor_ids"],
      "nclex_tip": "string",
      "presenter_notes": "string"
    }
  ],
  "anchor_coverage": {
    "total_anchors": "integer",
    "covered_anchors": ["anchor_ids"],
    "coverage_rate": "float"
  }
}
```

**Transformation:**
1. Slides array is passed directly
2. Metadata is preserved
3. Anchor coverage tracking continues

**Output (Step 6.5 Input):**
```json
{
  "step6_blueprint": "reference to above",
  "section_name": "string",
  "slides": "array (same structure)"
}
```

### Slide Renumbering After Splits

When a slide is split (body exceeds 8 lines):

1. Original slide becomes first part with original number
2. Continuation slide(s) get new sequential numbers
3. All subsequent slides are renumbered
4. Header gets "(cont.)" suffix for continuations
5. Anchors remain on original slide only
6. tip_generator and presenter_notes_writer called for new slides

**Example:**
```
Before split: Slides 1, 2, 3, 4, 5
Slide 3 splits into 2 parts
After split: Slides 1, 2, 3, 3a (or 4), 4 (or 5), 5 (or 6)
```

### Changelog Merge Strategy

Each step produces a changelog. Merge strategy:

1. Step 6.5 changelog: Line enforcement changes
2. Step 7 changelog: Formatting changes
3. Step 8 changelog: QA-driven fixes

**Merged changelog structure:**
```json
{
  "changes": [
    {
      "step": "6.5",
      "slide_number": 3,
      "change_type": "LINE_SPLIT",
      "before": "original content",
      "after": "modified content"
    }
  ],
  "total_changes": "integer",
  "slides_modified": ["slide_numbers"]
}
```

---

## Input Schema Contract

```yaml
input:
  type: object
  required:
    - section
    - outline
    - standards
    - run_id
  properties:
    section:
      type: object
      required:
        - section_number
        - section_name
        - anchor_ids
      properties:
        section_number:
          type: integer
        section_name:
          type: string
        anchor_ids:
          type: array
          items:
            type: string
        anchor_content:
          type: array
          items:
            type: object
    outline:
      type: object
      description: Full outline from Step 4
    standards:
      type: object
      description: Loaded standards from Step 5
    run_id:
      type: string
    domain:
      type: string
```

---

## Output Schema Contract

```yaml
output:
  type: object
  required:
    - section_number
    - section_name
    - blueprint
    - qa_score
    - visual_quota_status
  properties:
    section_number:
      type: integer
    section_name:
      type: string
    blueprint:
      $ref: agents/schemas/blueprint.schema.json
    qa_score:
      type: integer
      minimum: 90
      maximum: 100
    visual_quota_status:
      type: string
      enum: [PASS, FAIL]
    visual_count:
      type: integer
    slide_count:
      type: integer
    output_files:
      type: object
      properties:
        blueprint:
          type: string
        revised:
          type: string
        qa_report:
          type: string
        visual_specs:
          type: string
        integrated:
          type: string
        final:
          type: string
```

---

## Inter-Agent Data Flow

```
blueprint_generator
    │
    ├─── initial_blueprint: {
    │        metadata: {...},
    │        slides: Array<Slide>,
    │        presenter_notes: Array<Notes>
    │    }
    │
    ▼
line_enforcer
    │
    ├─── enforced_blueprint: {
    │        slides: Array<Slide>,  // All lines within limits
    │        changes: Array<Change>
    │    }
    │
    ▼
formatting_reviser
    │
    ├─── formatted_blueprint: {
    │        slides: Array<FormattedSlide>,
    │        changelog: Array<Revision>
    │    }
    │
    ▼
quality_reviewer
    │
    ├─── qa_result: {
    │        score: 94,
    │        status: "PASS",
    │        issues: [],
    │        passed_blueprint: {...}
    │    }
    │
    ▼
visual_identifier
    │
    ├─── visual_specs: {
    │        quota_status: "PASS",
    │        visuals: Array<VisualSpec>,
    │        rationale: Map<SlideNum, String>
    │    }
    │
    ▼
visual_integrator
    │
    ├─── integrated_blueprint: {
    │        slides: Array<SlideWithVisualMarker>,
    │        visual_index: Map<SlideNum, VisualSpec>
    │    }
    │
    ▼
blueprint_organizer
    │
    └─── final_blueprint: {
             metadata: { qa_score: 94, visual_count: 4, ... },
             slides: Array<FinalSlide>,
             ready_for_powerpoint: true
         }
```

---

## Error Handling Procedures

### Step-Specific Errors

```yaml
step_6_errors:
  - error: ANCHOR_NOT_FOUND
    action: Skip anchor with warning, continue
  - error: SLIDE_OVERFLOW
    action: Split slide, log change
  - error: CONTENT_INSUFFICIENT
    action: Flag for manual review

step_6_5_errors:
  - error: LINE_TOO_LONG
    action: Auto-split at word boundary
  - error: CANNOT_SPLIT
    action: Truncate with ellipsis, flag

step_7_errors:
  - error: CHAR_LIMIT_EXCEEDED
    action: Re-wrap text
  - error: FORMAT_INCONSISTENT
    action: Apply standard format

step_8_errors:
  - error: QA_SCORE_LOW
    action: Return to Step 7 with specific issues
    max_retries: 3
  - error: CRITICAL_VIOLATION
    action: Halt section processing

step_9_errors:
  - error: QUOTA_NOT_MET
    action: Identify additional visual opportunities
    max_retries: 2
  - error: NO_VALID_VISUAL_CONTENT
    action: Use TABLE as fallback

step_10_errors:
  - error: MISSING_MARKER
    action: Add Visual: No as default
  - error: SPEC_MISMATCH
    action: Regenerate visual spec

step_11_errors:
  - error: STRUCTURE_INVALID
    action: Rebuild structure
  - error: SEQUENCE_ISSUE
    action: Reorder slides
```

### Quality Gate Loop

```
IF step_8_score < 90:
    iteration_count++
    IF iteration_count <= 3:
        RETURN to Step 7 with:
            - Current blueprint
            - QA issues list
            - Previous changelog
        REPROCESS Steps 7-8
    ELSE:
        LOG "Max iterations reached"
        HALT section with error
```

---

## Error Recovery Details

### Smart Retry Controller Integration

**Location:** `skills/utilities/smart_retry_controller.py`

The Smart Retry Controller provides intelligent retry logic with:
- Context-aware retry with failing category targeting
- Slide locking to avoid re-processing passing slides
- Incremental scoring (only revalidate changed slides)
- Score trajectory tracking for early termination

**Usage:**
```python
from skills.utilities.smart_retry_controller import (
    SmartRetryController, create_retry_controller
)

controller = create_retry_controller()

result = controller.execute_with_retry(
    step=8,
    execute_fn=run_quality_review,
    validate_fn=check_qa_score,
    initial_input={'blueprint': blueprint},
    target_score=90.0,
    max_iterations=3
)

if result.success:
    # Continue to Step 9
    pass
elif result.termination_reason == TerminationReason.NO_IMPROVEMENT:
    # Scores plateaued - human review needed
    pass
```

### Quality Gate Loop (Step 8)

**Trigger:** QA score < 90

**Retry Context (SmartRetryContext):**
```json
{
  "step": 8,
  "target_score": 90.0,
  "current_iteration": 2,
  "iterations": [
    {
      "iteration": 1,
      "score": 78.5,
      "failing_categories": ["char_limits", "markers"],
      "failing_slides": [3, 5, 7],
      "locked_slides": [1, 2, 4, 6, 8, 9, 10],
      "modifications": []
    }
  ],
  "locked_slides": [1, 2, 4, 6, 8, 9, 10],
  "failing_categories": ["char_limits", "markers"],
  "strategy": "TARGETED_REPROCESS",
  "category_weights": {
    "anchor_coverage": 20,
    "char_limits": 15,
    "line_limits": 15
  }
}
```

**Category-Specific Guidance:**
The controller provides targeted guidance for each failing category:
```python
{
  "char_limits": "Apply body_char_enforcer to wrap lines at 66 characters.",
  "markers": "Insert [PAUSE] (min 2) and [EMPHASIS: term] markers.",
  "nclex_tip": "Ensure NCLEX tip is present (max 132 chars, 2 lines)."
}
```

**Retry Strategies:**
| Strategy | When Used | Description |
|----------|-----------|-------------|
| FULL_REPROCESS | anchor_coverage fails | Reprocess all slides |
| TARGETED_REPROCESS | Mixed failures | Only reprocess failing slides |
| INCREMENTAL_FIX | char_limits, markers, numbering | Apply minimal fixes |
| ESCALATE | Max iterations or no improvement | Stop and report to user |

**Termination Conditions:**
- SUCCESS: Score >= target (90)
- MAX_ITERATIONS: 3 attempts exhausted
- NO_IMPROVEMENT: Score not improving for 2+ iterations
- CRITICAL_ERROR: Unrecoverable exception

**After Max Retries (3):**
- If score >= 80: WARN status, continue with warnings
- If score < 80: HALT section processing
- Log all unresolved issues via retry log
- Human review required for HALT cases

### Incremental Scoring

**Location:** `skills/utilities/smart_retry_controller.py` → `IncrementalScorer`

Incremental scoring avoids redundant validation:
```python
from skills.utilities.smart_retry_controller import IncrementalScorer

scorer = IncrementalScorer()

# Only validate slides not in cache
score, details = scorer.score_incrementally(
    slides=blueprint['slides'],
    locked_slides={1, 2, 4, 6},  # From retry context
    validate_slide_fn=validate_single_slide
)

# details includes:
# - slides_validated: 4 (new validations)
# - slides_from_cache: 6 (reused results)
```

### Partial Failure Handling

**Scenario:** Some slides pass, others fail

**Approach (Automated by SmartRetryController):**
1. After each iteration, extract passing slides
2. Mark passing slides as LOCKED in retry context
3. Prepare retry input with only failing slides
4. Merge fixes into existing blueprint
5. Preserve slide numbers (no renumbering during retry)

**Locked Slide Protection (Automatic):**
```python
# Controller handles this internally
context.locked_slides.update(passing_slides)

# Retry input only includes failing slides
retry_input['slides_to_process'] = [
    s for s in blueprint['slides']
    if s.get('slide_number') not in context.locked_slides
]
```

---

## Output Files Generated

| Step | Output Pattern | Example |
|------|----------------|---------|
| 6 | `outputs/blueprints/step6_blueprint_{domain}_{section}_{date}.txt` | step6_blueprint_medical_surgical_01_20260104.txt |
| 7 | `outputs/revisions/step7_revised_{domain}_{section}_{date}.txt` | step7_revised_medical_surgical_01_20260104.txt |
| 7 | `outputs/revisions/step7_changelog_{domain}_{section}_{date}.txt` | step7_changelog_medical_surgical_01_20260104.txt |
| 8 | `outputs/qa_reports/step8_qa_report_{domain}_{section}_{date}.txt` | step8_qa_report_medical_surgical_01_20260104.txt |
| 8 | `outputs/qa_reports/step8_score_{domain}_{section}_{date}.txt` | step8_score_medical_surgical_01_20260104.txt |
| 9 | `outputs/visual_specs/step9_visual_specs_{domain}_{section}_{date}.txt` | step9_visual_specs_medical_surgical_01_20260104.txt |
| 10 | `outputs/integrated/step10_integrated_{domain}_{section}_{date}.txt` | step10_integrated_medical_surgical_01_20260104.txt |
| 10 | `outputs/integrated/step10_changelog_{domain}_{section}_{date}.txt` | step10_changelog_medical_surgical_01_20260104.txt |
| 11 | `outputs/organized/step11_final_{domain}_{section}_{date}.txt` | step11_final_medical_surgical_01_20260104.txt |

---

## Quality Gates

| Gate | Location | Requirement | On Fail |
|------|----------|-------------|---------|
| Line Limits | Step 6.5 | All lines within char limits | Auto-fix |
| Format | Step 7 | Consistent formatting | Auto-fix |
| QA Score | Step 8 | Score >= 90/100 | Return to Step 7 |
| Visual Quota | Step 9 | QUOTA STATUS: PASS | Identify more visuals |
| Visual Markers | Step 10 | All slides have markers | Add default markers |
| Structure | Step 11 | Valid schema | Rebuild |

---

## Constraint Reference

From `config/constraints.yaml`:

```yaml
# Text limits
character_limits:
  title:
    chars_per_line: 32
    max_lines: 2
  body:
    chars_per_line: 66
    max_lines: 8
  tip:
    chars_per_line: 66
    max_lines: 2
    total_max_chars: 132  # IMPORTANT: Use 132, not 120
  presenter_notes:
    max_words: 450
    max_seconds: 180
    # No per-line char limit (intentional - speaker notes)

# Visual quotas
visual_quotas:
  max_percentage: 0.40  # Maximum 40% of slides can have visuals
  by_section_size:
    "12-15": { minimum: 2, target_min: 3, target_max: 4 }
    "16-20": { minimum: 3, target_min: 4, target_max: 5 }
    "21-25": { minimum: 3, target_min: 5, target_max: 6 }
    "26-35": { minimum: 4, target_min: 6, target_max: 8 }
```

**IMPORTANT**: Visual slides cannot exceed 40% of total section slides.

---

## Text Limits Enforcement (After Content Generation)

After each slide is generated by content_slide_generator or vignette_generator:

1. **Apply Text Limits**
   - Call: `skills/enforcement/text_limits_enforcer.py`
   - Function: `enforce_all_text_limits(slide)`
   - Order: R1 (header) -> R3 (body chars) -> R2 (body lines)

2. **Handle Slide Splits**
   - If `slide._needs_split == True`:
     - Create continuation slides for overflow content
     - Re-number all slides sequentially
     - Call tip_generator and presenter_notes_writer for new slides

3. **Validation Gate**
   - Call: `validate_all_text_limits(slide)`
   - If not valid: LOG_WARNING and continue (best effort)

### Text Limit Skills Reference

| Skill | Path | Purpose |
|-------|------|---------|
| header_enforcer | skills/enforcement/header_enforcer.py | R1: Header limits (32 chars/line, 2 lines max) |
| body_line_enforcer | skills/enforcement/body_line_enforcer.py | R2: Body line limits (8 non-empty lines max) |
| body_char_enforcer | skills/enforcement/body_char_enforcer.py | R3: Body char limits (66 chars/line) |
| text_limits_enforcer | skills/enforcement/text_limits_enforcer.py | Unified interface for all text limits |

---

---

## Anchor Coverage Enforcement (R8)

### Pre-Generation: Anchor Assignment

Before content generation begins:

1. **Initialize Coverage Tracker**
   - Call: `skills/validation/anchor_coverage_tracker.py`
   - Function: `AnchorCoverageTracker.from_input(step4_output)`
   - Purpose: Load all required anchors from input

2. **Generate Assignment Plan**
   - Call: `skills/enforcement/anchor_coverage_enforcer.py`
   - Function: `get_anchor_assignment_plan(step4_output)`
   - Purpose: Pre-assign anchors to slide numbers
   - Pass plan to slide_planner

### During Generation: Track Coverage

For each slide generated:

1. **Mark Anchors Covered**
   - Call: `tracker.mark_covered(slide['anchors_covered'], slide_number)`
   - Update tracker state in real-time

### Post-Generation: Validate Coverage

After all slides generated:

1. **Validate Coverage**
   - Call: `tracker.validate()`
   - Check: All anchors covered

2. **Handle Missing Anchors**
   - If missing anchors:
     - Option A: Regenerate with explicit anchor assignment
     - Option B: Generate fallback slides (`ensure_anchor_coverage`)
   - Maximum 3 regeneration attempts

3. **Final Validation Gate**
   - If still missing after attempts: LOG_ERROR
   - Include coverage report in output

### Anchor Coverage Skills Reference

| Skill | Path | Purpose |
|-------|------|---------|
| AnchorCoverageTracker | skills/validation/anchor_coverage_tracker.py | Real-time coverage tracking |
| ensure_anchor_coverage | skills/enforcement/anchor_coverage_enforcer.py | Fallback slide generation |
| get_anchor_assignment_plan | skills/enforcement/anchor_coverage_enforcer.py | Pre-assignment planning |

---

## Template Enforcement (Vignette and Answer Slides)

### Vignette Generation (R10)

1. **Use Vignette Template**
   - Call: `skills/templates/vignette_template.py`
   - Function: `VignetteTemplate(stem, options, correct_answer)`
   - Ensures: 2-4 sentence stem, exactly 4 options (A, B, C, D)

2. **Validation Gate**
   - Call: `validate_vignette(body)`
   - If invalid: `enforce_vignette_structure(body, correct_answer)` to fix
   - Check: All 4 options present, stem is 2-4 sentences

### Answer Generation (R11)

1. **Use Answer Template**
   - Call: `skills/templates/answer_template.py`
   - Function: `AnswerTemplate(correct_letter, correct_text, rationale, distractors)`
   - Ensures: Rationale section + all distractors analyzed

2. **Validation Gate**
   - Call: `validate_answer(body)`
   - If invalid: `enforce_answer_structure(body, correct_letter, correct_text)` to fix
   - Check: Has rationale, has distractor analysis, has correct answer statement

### Template Skills Reference

| Skill | Path | Purpose |
|-------|------|---------|
| VignetteTemplate | skills/templates/vignette_template.py | R10: Structured vignette creation |
| validate_vignette | skills/templates/vignette_template.py | R10: Vignette validation |
| AnswerTemplate | skills/templates/answer_template.py | R11: Structured answer creation |
| validate_answer | skills/templates/answer_template.py | R11: Answer validation |

---

## Marker Insertion (All Slides - R14)

After presenter_notes_writer generates notes:

1. **Insert Required Markers**
   - Call: `skills/enforcement/marker_insertion.py`
   - Function: `insert_markers(notes, slide_type, domain)`
   - Ensures: [PAUSE] and [EMPHASIS] markers present

2. **Marker Requirements**
   - Minimum 2 [PAUSE] markers per slide
   - Minimum 1 [EMPHASIS: term] marker for content slides
   - NCLEX pattern callouts where relevant

3. **Validation**
   - Call: `validate_markers(notes, slide_type)`
   - Log warnings if still missing markers after insertion

### Marker Skills Reference

| Skill | Path | Purpose |
|-------|------|---------|
| insert_markers | skills/enforcement/marker_insertion.py | R14: Insert required markers |
| validate_markers | skills/enforcement/marker_insertion.py | R14: Validate marker presence |
| count_markers | skills/enforcement/marker_insertion.py | R14: Count existing markers |

---

## Validation Gate Summary

### Requirements by Step

| Step | Requirements Validated | Enforcement Skills Used |
|------|------------------------|------------------------|
| 6 | R8 (anchor assignment) | anchor_coverage_tracker |
| 6.5 | R1, R2, R3 (text limits) | header_enforcer, body_*_enforcer |
| 7 | R1, R2, R3 (formatting) | text_limits_enforcer |
| 8 | ALL (quality review) | All validation skills |
| 9 | Visual quota | visual_quota_tracker |
| 10 | Visual markers | marker_inserter |
| 11 | Structure | structure_validator |

### Requirement Ownership

| Requirement | Primary Step | Enforcement Step | Validation Step |
|-------------|--------------|------------------|-----------------|
| R1 (Header) | 6 | 6.5, 7 | 8 |
| R2 (Body lines) | 6 | 6.5, 7 | 8 |
| R3 (Body chars) | 6 | 6.5, 7 | 8 |
| R4 (NCLEX tip) | 6 | 6 | 8 |
| R8 (Anchor coverage) | 6 | 6 | 8 |
| R10 (Vignette) | 6 | 6 | 8 |
| R11 (Answer) | 6 | 6 | 8 |
| R14 (Markers) | 6 | 6 | 8 |
| R15 (Numbering) | 6, 6.5, 7 | 11 | 8, 11 |
| Visual quota | 9 | 9 | 8, 9 |

---

## Version History

- **v1.7** (2026-01-06): Added ML-based visual type recommendation (P3 enhancement)
  - New skill: `ml_visual_recommender.py` with 47-feature extraction
  - Naive Bayes classifier with calibrated probability outputs
  - Ensemble combining with rule-based `visual_pattern_matcher`
  - Pattern-based training data generation (16 examples, 7 visual types)
  - 33 unit tests, 41 validation requirements at 97%+ pass rate
- **v1.6** (2026-01-06): Added Smart Retry Controller integration with incremental scoring
- **v1.5** (2026-01-05): Added data transformation docs, skill status table, error recovery details, validation gate summary
- **v1.4** (2026-01-05): Added config/constraints.yaml reference, fixed NCLEX tip limit to 132
- **v1.3** (2026-01-05): Added template enforcement for R10, R11, R14
- **v1.2** (2026-01-05): Added anchor coverage tracking and enforcement (R8)
- **v1.1** (2026-01-05): Added text limits enforcement skills (R1, R2, R3)
- **v1.0** (2026-01-04): Initial blueprint orchestrator configuration
