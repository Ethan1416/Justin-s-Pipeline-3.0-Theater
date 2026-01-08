# Blueprint Generator Agent

## Agent Identity
- **Name:** blueprint_generator
- **Step:** 6 (Blueprint Generation)
- **Purpose:** Orchestrate slide-by-slide content specifications for one section at a time

---

## Sub-Agent Architecture

This agent orchestrates the following sub-agents:

| Sub-Agent | Purpose | Input | Output |
|-----------|---------|-------|--------|
| `slide_planner` | Plan slide sequence and assignments | Section outline | Slide plan with sequence |
| `content_slide_generator` | Generate content slide body | Slide plan + anchors | Content slides |
| `vignette_generator` | Generate NCLEX vignette | Section concepts | Vignette + answer slides |
| `tip_generator` | Generate NCLEX tips | Content slides | Tips per slide |
| `presenter_notes_writer` | Generate presenter monologues | All slides | Notes per slide |

### Execution Flow
```
slide_planner
    |
    +--> content_slide_generator (parallel per subsection)
    |         |
    |         +--> tip_generator (per content slide)
    |         |
    |         +--> presenter_notes_writer (per slide)
    |
    +--> vignette_generator
              |
              +--> presenter_notes_writer (for vignette + answer)
```

---

## Input Schema
```json
{
  "step4_output": "object (outline with sections and subsections)",
  "step5_standards": "object (presentation standards)",
  "section_name": "string (target section to generate)",
  "section_number": "integer",
  "anchors": "array of anchors assigned to this section"
}
```

## Output Schema
Reference: `agents/schemas/blueprint.schema.json`

```json
{
  "metadata": {
    "section_number": "integer",
    "section_name": "string",
    "domain": "string",
    "date": "YYYY-MM-DD",
    "version": "string",
    "total_slides": "integer"
  },
  "subsection_modes": "array of {subsection, mode, anchor_count}",
  "slides": "array of slide objects",
  "anchor_coverage": {
    "subsections": "array of coverage by subsection",
    "total_anchors": "integer",
    "covered": "integer",
    "missing": "array"
  }
}
```

---

## Required Skills
- `skills/generation/slide_generator.py` - Generate slide content
- `skills/parsing/outline_parser.py` - Parse outline structure
- `skills/validation/blueprint_validator.py` - Validate blueprint
- `skills/validation/anchor_coverage_tracker.py` - Track anchor coverage (R8)
- `skills/enforcement/anchor_coverage_enforcer.py` - Enforce anchor coverage (R8)

---

## Step-by-Step Instructions

### Step 1: Analyze Section Structure

From Step 4 output, extract for target section:
- Subsection names and anchor assignments
- Anchor summaries
- Frontload flags
- Cross-reference flags
- Prerequisite sections

### Step 2: Determine Slide Sequence

```
Slide 1: Section Intro (fixed)
Slides 2-N: Subsection 1 content (mode-based)
Slides N+1-M: Subsection 2 content (mode-based)
[Continue for all subsections...]
Slide X: Vignette (fixed)
Slide X+1: Answer (fixed)
```

### Step 3: Apply Delivery Modes

**Foundational Mode (first subsection):**
- Overview slide(s)
- Scaffolding slides
- Bridge slide

**Full Mode (5+ anchors):**
- Connection slide
- Core content slides
- Synthesis slide

**Minor Mode (3-4 anchors):**
- Connection (brief, may combine with first content)
- Core content slides

**One-and-Done Mode (1-2 anchors):**
- Single presentation unit (1-2 slides)

### Step 4: Generate Each Slide

For each slide, produce:
1. Slide number
2. Slide type
3. Header text (max 32 chars/line, 2 lines)
4. Body text (max 66 chars/line, 8 lines)
5. NCLEX Tip (content slides only)
6. Presenter notes (verbatim monologue)

### Step 5: Validate Anchor Coverage (CRITICAL - R8)

Verify ALL anchors from Step 4 are covered in the blueprint.

**Using Anchor Coverage Tracker:**
```python
from skills.validation.anchor_coverage_tracker import AnchorCoverageTracker

# Initialize tracker from Step 4 input
tracker = AnchorCoverageTracker.from_input(step4_output)

# After generating each slide, mark anchors as covered
for slide in generated_slides:
    tracker.mark_covered(
        slide['anchors_covered'],
        slide_number=slide['slide_number'],
        slide_type=slide['type']
    )

# Validate coverage
result = tracker.validate()
if not result['valid']:
    # Handle missing anchors
    from skills.enforcement.anchor_coverage_enforcer import ensure_anchor_coverage
    coverage_result = ensure_anchor_coverage(slides, step4_output)
    slides = coverage_result['slides']
```

**Coverage Requirements:**
- ALL anchors from input MUST appear on at least one slide
- FRONTLOAD anchors MUST appear in first 3 slides of their subsection
- XREF anchors can have abbreviated treatment (1 slide max)
- Missing anchors = VALIDATION FAILURE

---

## Slide Templates

### Section Intro Slide
```
===========================================
SLIDE 1: SECTION INTRO
===========================================
Type: Section Intro

HEADER:
[Section Title from Step 4]

BODY:
"[Poetic or provocative quote that relates to section content
and primes the audience]"

- [Attribution]

NCLEX TIP:
[None - omit for intro slides]

PRESENTER NOTES:
Welcome to [Section Name]. [PAUSE]

In this section, we'll explore [brief overview].
[Connection to prior section if applicable]

[Preview subsections]: We'll begin by [first], then [second],
and conclude with [final].

[Provocative hook or question]

Let's begin with [transition to first content].
```

### Content Slide Template
```
===========================================
SLIDE [#]: [DESCRIPTIVE TITLE]
===========================================
Type: Content
Subsection: [Subsection Name]
Anchors Covered: [List anchor summaries]

HEADER:
[Clear, descriptive title - 1-2 lines max]

BODY:
[Main content - 3-8 lines maximum]
- Use bullet points, numbered lists, or prose
- Mixed format acceptable
- Prioritize clarity over density

NCLEX TIP:
[1-2 line insight about NCLEX testing patterns]

PRESENTER NOTES:
[Opening statement]

[Full explanation - verbatim script]

[EMPHASIS: key terms] where needed
[PAUSE] where appropriate

[Applied relevance]
[NCLEX pattern callout if applicable]
[Transition to next slide]

[Target: 130-150 words per minute, max 180 seconds]
```

### Vignette Slide Template
```
===========================================
SLIDE [#]: VIGNETTE
===========================================
Type: Vignette

HEADER:
[Section Name] - Clinical Application

BODY:
[2-4 sentence NCLEX-style vignette stem]

A) [Plausible option]
B) [Plausible option]
C) [Plausible option]
D) [Plausible option]

NCLEX TIP:
[None - omit for vignette slides]

PRESENTER NOTES:
Let's apply what we've learned. [PAUSE]

[Read vignette aloud - verbatim]

Take a moment to consider this scenario. Think about which
concepts apply here. [PAUSE - 30-60 seconds]

When you're ready, let's look at the answer.
```

### Answer Slide Template
```
===========================================
SLIDE [#]: ANSWER
===========================================
Type: Answer

HEADER:
Answer: [Correct Letter]

BODY:
Correct Answer: [Letter]) [Full text]

Rationale:
[2-3 sentences explaining correctness]

Why not the others:
- A) [If wrong: explanation]
- B) [If wrong: explanation]
- C) [If wrong: explanation]
- D) [If wrong: explanation]

NCLEX TIP:
[None - omit for answer slides]

PRESENTER NOTES:
The correct answer is [EMPHASIS: Letter]. [PAUSE]

[Full explanation connecting to anchor concepts]

Let's look at why the other options don't work:
[Walk through each distractor]

[NCLEX pattern insight]
[Transition to next section or wrap-up]
```

---

## Content Generation Guidelines

### Header Text
- Clear, descriptive titles
- 1-2 lines maximum
- Max 32 characters per line

### Body Text

**CRITICAL: Maximum 8 non-empty lines per slide**

| Content Type | Recommended Format |
|--------------|-------------------|
| Definitions/concepts | Bullet points |
| Processes/sequences | Numbered list |
| Comparisons | Side-by-side or table |
| Single complex idea | Prose paragraph |

### NCLEX Tips
- Present on ALL content slides
- Omit for Intro/Vignette/Answer slides
- 1-2 lines maximum
- Focus on testing patterns

### Presenter Notes
- Verbatim monologue (complete sentences)
- 130-150 words per minute
- Maximum 180 seconds per slide
- Include [PAUSE] and [EMPHASIS] markers
- Include NCLEX pattern callouts
- Include transitions

---

## Validation Requirements

### Line Count Validation
- [ ] ALL BODY sections have <= 8 non-empty lines
- [ ] Headers <= 2 lines, 32 chars/line
- [ ] NCLEX Tips <= 2 lines

### Content Validation
- [ ] All anchors from Step 4 covered (R8 - use anchor_coverage_tracker)
- [ ] FRONTLOAD anchors appear early (within first 3 slides of subsection)
- [ ] NCLEX tips on all content slides
- [ ] Fixed slides present (intro, vignette, answer)
- [ ] Presenter notes complete on all slides

### Structure Validation
- [ ] Delivery modes correctly applied
- [ ] Subsection boundaries clear
- [ ] Slide sequence logical

---

## Output Format

```
========================================
STEP 6: BLUEPRINT
========================================
Domain: [Domain Name]
Section: [Section Name]
Section Number: [X of Y]
Date: [Date]

Source: step4_output_[domain]_[date].txt

SECTION OVERVIEW:
- Subsections: [count]
- Total Anchors: [count]
- Estimated Content Slides: [count]
- Fixed Slides: 3 (intro, vignette, answer)
- Total Slides: [count]

SUBSECTION DELIVERY MODES:
1. [Subsection Name]: [Mode] ([X] anchors)
2. [Subsection Name]: [Mode] ([X] anchors)
...

========================================
BEGIN SLIDE-BY-SLIDE BLUEPRINT
========================================

[All slides using templates above]

========================================
END SLIDE-BY-SLIDE BLUEPRINT
========================================

VALIDATION: ANCHORS COVERED

Subsection 1: [Subsection Name]
[checkmark] [Anchor summary 1] - Slide(s) [#]
[checkmark] [Anchor summary 2] - Slide(s) [#]
...

COVERAGE STATUS:
- Total anchors in section: [X]
- Anchors covered: [X]
- Anchors missing: [None / List]

========================================
READY FOR STEP 6.5: LINE ENFORCEMENT
========================================
```

---

## Error Handling

| Error Condition | Action |
|-----------------|--------|
| Missing Step 4 outline | HALT, request Step 4 output |
| Missing Step 5 standards | HALT, request Step 5 output |
| Section not in outline | HALT, verify section name |
| Anchor not found | FLAG, document in coverage report |
| Body exceeds 8 lines | FLAG for Step 6.5 enforcement |

---

## Quality Gates

Before proceeding to Step 6.5:
- [ ] All subsections addressed
- [ ] Delivery modes correctly applied
- [ ] Section intro includes quote
- [ ] All content slides have NCLEX tips
- [ ] Vignette is NCLEX-style
- [ ] Answer slide includes distractor analysis
- [ ] Presenter notes complete
- [ ] All anchors covered

---

## CRITICAL WARNING

```
DO NOT SKIP TO STEP 12 (PowerPoint Generation) FROM HERE!

Steps 6.5, 7, 8, 9, 10, and 11 are MANDATORY.

Required sequence:
Step 6 -> Step 6.5 -> Step 7 -> Step 8 -> Step 9 -> Step 10 -> Step 11 -> Step 12
```

---

**Agent Version:** 1.1
**Last Updated:** 2026-01-05
