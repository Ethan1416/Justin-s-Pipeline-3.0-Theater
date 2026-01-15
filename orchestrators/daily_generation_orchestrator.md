# Sub-Orchestrator: Daily Generation Pipeline

**Version:** 1.0
**Purpose:** Generate all components for a single day's lesson (56-minute structure)
**Parent:** `theater_master_orchestrator.md`

---

## Overview

The Daily Generation Orchestrator coordinates the creation of all lesson components for a single day. It runs the generation agents in sequence, ensuring each component builds on previous outputs and maintains coherence across the lesson.

---

## Agents Managed

| Agent | Order | Purpose | Duration Target | Output | HARDCODED |
|-------|-------|---------|-----------------|--------|-----------|
| **agenda_generator** | **0** | **Slide 1 agenda with timing structure** | **N/A** | **agenda.json** | **YES** |
| lesson_plan_generator | 1 | Admin-friendly scripted lesson plan | N/A | lesson_plan.json | No |
| warmup_generator | 2 | Content-connected theater warmup | 5 min | warmup.json | No |
| powerpoint_generator | 3 | 16-slide PowerPoint structure | 15 min | powerpoint.json | No |
| presenter_notes_writer | 4 | Verbatim presenter script | 15 min | presenter_notes.json | No |
| activity_generator | 5 | Structured hands-on activity | 15 min | activity.json | No |
| journal_exit_generator | 6 | Reflection prompts and assessments | 10 min | journal_exit.json | No |
| handout_generator | 7 | Print-ready activity handouts | N/A | handout.json | No |

### HARDCODED Agents

The following agents use hardcoded skills that CANNOT be bypassed:

| Agent | Skill | Rules Enforced |
|-------|-------|----------------|
| agenda_generator | `agenda_slide_generator.py` | R1: 6 components, R2: 1-3 objectives, R3: 3-5 materials, R4: Total time = class period |
| agenda_validator | `agenda_slide_validator.py` | R5: Sequential time markers, R6: Descriptions under 60 chars |

---

## Daily Structure Reference (56 minutes)

```
┌────────────────────────────────────────────────────────────────┐
│  DAILY CLASS STRUCTURE (56 minutes total)                      │
├────────────────────────────────────────────────────────────────┤
│                                                                │
│  ┌─────────┐ ┌─────────┐ ┌───────────────┐                    │
│  │ Agenda  │ │ Warmup  │ │   Lecture     │                    │
│  │   5m    │ │   5m    │ │    15m        │                    │
│  └─────────┘ └─────────┘ └───────────────┘                    │
│      ↓           ↓              ↓                              │
│  Slide 1     Slide 2      Slides 3-14                         │
│                                                                │
│  ┌───────────────┐ ┌──────────────────┐ ┌─────────┐           │
│  │   Activity    │ │   Reflection     │ │ Buffer  │           │
│  │     15m       │ │      10m         │ │   6m    │           │
│  └───────────────┘ └──────────────────┘ └─────────┘           │
│         ↓                   ↓                                  │
│     Slide 15           Slide 16                                │
│                                                                │
└────────────────────────────────────────────────────────────────┘
```

---

## Execution Order

```
DAILY GENERATION PIPELINE
=========================

INPUT: {unit_plan, day_number, daily_input}
OUTPUT: Complete daily lesson components (pre-validation)

Step 0: AGENDA GENERATION (HARDCODED)
=====================================
Agent: agenda_generator
Orchestrator: AgendaOrchestrator
Skill: skills/enforcement/agenda_slide_generator.py (HARDCODED)
Validator: skills/enforcement/agenda_slide_validator.py (HARDCODED)

Input:
  - unit_number: from unit_plan
  - unit_name: from unit_plan
  - day_number: day_number
  - total_days: from unit_plan
  - lesson_topic: from daily_input.topic
  - learning_objectives: from daily_input.learning_objectives
  - warmup_type: from daily_input.warmup.type OR auto-select
  - activity_type: from daily_input.activity.type OR auto-select
  - class_period: "standard" | "block" | "shortened" | "extended"

Output: agenda.json
  - agenda_data:
    - unit_info: "Unit X: [Name] - Day Y/Z"
    - lesson_title: topic
    - total_duration: 56 | 90 | 45 | 75
    - components: [6 items with timing]
    - learning_objectives_display: ["1. ...", "2. ...", "3. ..."]
    - materials_preview: [3-5 items]
  - slide_content:
    - slide_number: 1
    - slide_type: "agenda"
    - title: unit_info
    - body_sections: [agenda_items, objectives]
    - presenter_notes: verbatim script
  - validation:
    - valid: true | false
    - score: 0-100
    - issues: []
    - warnings: []

HARDCODED Rules (CANNOT BE BYPASSED):
  R1: Total duration must equal class period
  R2: Exactly 6 components required
  R3: 1-3 learning objectives required
  R4: 3-5 materials required
  R5: Time markers must be sequential
  R6: Descriptions must be under 60 characters

Visual Layout (Slide 1):
┌─────────────────────────────────────────┐
│  Unit X: [Name] - Day Y/Z               │
│  "[Lesson Title]"                       │
├─────────────────────────────────────────┤
│  TODAY'S AGENDA                         │
│  ☐ Agenda & Objectives (5 min)          │
│  ☐ Warmup (5 min)                       │
│  ☐ Lecture (15 min)                     │
│  ☐ Activity (15 min)                    │
│  ☐ Reflection & Exit Ticket (10 min)    │
├─────────────────────────────────────────┤
│  OBJECTIVES                             │
│  1. [Measurable objective]              │
│  2. [Measurable objective]              │
└─────────────────────────────────────────┘


Step 1: LESSON PLAN GENERATION
==============================
Agent: lesson_plan_generator
Input:
  - unit: {number, name, total_days}
  - day: day_number
  - topic: from daily_input
  - learning_objectives: from daily_input
  - standards: from daily_input
  - vocabulary: from daily_input
  - prior_knowledge: from daily_input

Output: lesson_plan.json
  - basic_information (title, unit, day, duration)
  - standards (full text, not just codes)
  - learning_objectives (2-4, Bloom's verbs)
  - vocabulary (term, definition, usage_example)
  - materials_list
  - procedure (teacher_actions, student_actions, timing)
  - differentiation (ell, advanced, struggling)
  - assessment_strategy
  - reflection_space

Skill: admin_template_formatter


Step 2: WARMUP GENERATION
=========================
Agent: warmup_generator
Input:
  - lesson_plan (from Step 1)
  - warmup_type: from daily_input OR auto-select
  - content_connection: from lesson topic

Output: warmup.json
  - type: physical | mental | social | creative | content
  - title: descriptive name
  - duration: 5 (fixed)
  - connection_to_lesson: explicit statement
  - setup_instructions: 30 seconds
  - demonstration_notes: 30 seconds (if needed)
  - execution_instructions: 3 minutes (numbered steps)
  - wrapup_instructions: 30 seconds
  - transition_to_lecture: 30 seconds
  - modifications:
    - space_limited: adaptation
    - large_class: adaptation
    - energy_level: low/medium/high

Skills: warmup_bank_selector, content_connector

WARMUP REQUIREMENTS:
- MUST connect to lesson content (not abstract)
- Connection types: vocabulary_reference, skill_practice, concept_preview
- Physical warmups: voice, body, movement
- Mental warmups: focus, observation, concentration
- Social warmups: partner, group, ensemble
- Creative warmups: improvisation, imagination
- Content warmups: skill_practice, vocabulary


Step 3: POWERPOINT GENERATION
=============================
Agent: powerpoint_generator
Input:
  - lesson_plan (from Step 1)
  - warmup (from Step 2)
  - content_points: from daily_input
  - learning_objectives: from lesson_plan

Output: powerpoint.json
  - slides: array of 16 slides
    - slide_number: 1-16
    - type: auxiliary | content
    - header: max 36 chars, 1 line
    - body: max 12 lines, word wrap enabled
    - performance_tip: for content slides (66 chars, 2 lines max)
    - visual_marker: Yes | No
    - anchors_covered: array of learning points

Slide Structure:
  - Slide 1: Agenda (auxiliary)
  - Slide 2: Warmup Instructions (auxiliary)
  - Slides 3-14: Learning Content (12 content slides)
  - Slide 15: Activity Instructions (auxiliary)
  - Slide 16: Journal & Exit Ticket (auxiliary)

TEXT LIMITS (from config/constraints.yaml):
  - Header: 36 chars max, 1 line, NEVER truncate (revise instead)
  - Body: 12 lines max, word wrap enabled, NEVER truncate
  - Performance Tip: 132 chars max (66 × 2 lines)

Skills: header_enforcer, body_overflow_enforcer, performance_tip_fallback


Step 4: PRESENTER NOTES GENERATION
==================================
Agent: presenter_notes_writer
Input:
  - powerpoint (from Step 3)
  - lesson_plan (from Step 1)
  - speaking_rate: 140 WPM (target)

Output: presenter_notes.json
  - total_word_count: 1,950-2,250
  - estimated_duration_minutes: 14-16
  - slides: array matching powerpoint slides
    - slide_number: 1-16
    - notes: verbatim script
    - word_count: per slide
    - markers: [PAUSE], [EMPHASIS], [CHECK FOR UNDERSTANDING]

PRESENTER NOTES REQUIREMENTS:
  - Style: Verbatim script (word-for-word what to say)
  - Language: Natural, spoken, contractions allowed
  - Address: Direct ("you", "we", "let's")
  - Per-slide targets:
    - Title/intro slides: 100-150 words
    - Content slides: 160-190 words
    - Summary slides: 150-200 words
  - Total: 1,950-2,250 words (15 min at 140 WPM)

MARKER REQUIREMENTS:
  - [PAUSE]: minimum 2 per slide
  - [EMPHASIS: term]: minimum 1 per content slide
  - [CHECK FOR UNDERSTANDING]: minimum 3 per presentation

Skills: monologue_scripter, marker_insertion, word_count_analyzer


Step 5: ACTIVITY GENERATION
===========================
Agent: activity_generator
Input:
  - lesson_plan (from Step 1)
  - powerpoint (from Step 3)
  - activity_type: from daily_input OR auto-select

Output: activity.json
  - type: writing | discussion | performance | annotation | creative | physical | collaborative
  - title: descriptive name
  - duration: 15 (fixed)
  - structure:
    - setup_minutes: 1.5
    - work_minutes: 11
    - sharing_minutes: 2.5
  - instructions:
    - numbered_steps: array
    - time_allocations: per step
    - expected_outcomes: array
    - teacher_actions: array
    - student_actions: array
  - materials_needed: array
  - grouping: individual | pairs | small_groups | whole_class
  - time_warnings:
    - at_minute_10: warning text
    - at_minute_13: warning text
  - differentiation:
    - ell_supports: adaptations
    - advanced_extensions: enrichment
    - struggling_modifications: scaffolds
  - success_criteria: observable indicators
  - requires_handout: boolean

Skills: activity_type_selector, instruction_scaffolder, timing_allocator


Step 6: JOURNAL & EXIT TICKET GENERATION
========================================
Agent: journal_exit_generator
Input:
  - lesson_plan (from Step 1)
  - activity (from Step 5)
  - learning_objectives: from lesson_plan

Output: journal_exit.json
  - journal_prompt:
    - prompt_text: open-ended reflection question
    - connection_to_lesson: explicit link
    - suggested_length: sentence count or word range
    - duration_minutes: 5-7
  - exit_tickets: array (2-3 items)
    - ticket_number: 1-3
    - question: assessment question
    - format: multiple_choice | short_answer | rating_scale
    - objective_assessed: which learning objective
    - correct_answer: for auto-check (if applicable)

Skills: reflection_prompt_writer, assessment_question_writer


Step 7: HANDOUT GENERATION (Conditional)
========================================
Agent: handout_generator
Condition: activity.requires_handout == true
Input:
  - activity (from Step 5)
  - lesson_plan (from Step 1)

Output: handout.json
  - title: activity title
  - instructions: student-facing (simplified from activity)
  - workspace: structured space for student work
  - name_date_period: header fields
  - page_count: 1-2 (target: 1)
  - print_format: portrait | landscape

Skills: instruction_scaffolder, admin_template_formatter
```

---

## Dependencies and Data Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                    DATA FLOW DIAGRAM                            │
└─────────────────────────────────────────────────────────────────┘

daily_input.json
       │
       ▼
┌─────────────────┐
│ lesson_plan_    │──────────────────────────────┐
│ generator       │                              │
└────────┬────────┘                              │
         │ lesson_plan.json                      │
         ▼                                       │
┌─────────────────┐                              │
│ warmup_         │                              │
│ generator       │                              │
└────────┬────────┘                              │
         │ warmup.json                           │
         ▼                                       ▼
┌─────────────────┐                    ┌─────────────────┐
│ powerpoint_     │◄───────────────────│ learning_       │
│ generator       │                    │ objectives      │
└────────┬────────┘                    └─────────────────┘
         │ powerpoint.json                       │
         ▼                                       │
┌─────────────────┐                              │
│ presenter_      │◄─────────────────────────────┤
│ notes_writer    │                              │
└────────┬────────┘                              │
         │ presenter_notes.json                  │
         │                                       │
         │ (parallel branch)                     │
         ▼                                       ▼
┌─────────────────┐                    ┌─────────────────┐
│ activity_       │◄───────────────────│ content_points  │
│ generator       │                    │ from lecture    │
└────────┬────────┘                    └─────────────────┘
         │ activity.json
         │
         ├────────────────────┬─────────────────┐
         ▼                    ▼                 ▼
┌─────────────────┐  ┌─────────────────┐ ┌─────────────────┐
│ journal_exit_   │  │ handout_        │ │ materials_      │
│ generator       │  │ generator       │ │ aggregator      │
└────────┬────────┘  └────────┬────────┘ └────────┬────────┘
         │                    │                   │
         │ journal_exit.json  │ handout.json     │ materials.json
         │                    │                   │
         └────────────────────┴───────────────────┘
                              │
                              ▼
                    daily_output.json
                    (sent to validation)
```

---

## Coherence Requirements

### Cross-Component Consistency

All generated components MUST maintain consistency:

| Element | Must Match Across |
|---------|-------------------|
| Vocabulary terms | lesson_plan → powerpoint → presenter_notes |
| Learning objectives | lesson_plan → powerpoint → exit_tickets |
| Activity type | lesson_plan → activity → handout |
| Warmup connection | warmup.connection → lesson content |
| Time allocations | lesson_plan → all components |
| Materials | lesson_plan → activity → handout |

### Coherence Checks (Pre-Validation)

Before sending to validation gates:
1. **Vocabulary alignment**: Terms in powerpoint appear in presenter_notes
2. **Objective coverage**: Each objective appears in lecture AND is assessed
3. **Activity coherence**: Activity reinforces lecture content
4. **Warmup relevance**: Warmup connects to day's topic (not generic)
5. **Exit ticket validity**: Each exit ticket maps to a learning objective

---

## Parallel vs Sequential Execution

### Sequential (Required Order)
1. `lesson_plan_generator` → provides foundation
2. `warmup_generator` → needs lesson topic
3. `powerpoint_generator` → needs objectives and warmup
4. `presenter_notes_writer` → needs slides

### Parallelizable (After Step 4)
- `activity_generator` ← can run parallel with notes finalization
- `journal_exit_generator` ← needs objectives only
- `handout_generator` ← needs activity output

```
Sequential:     1 → 2 → 3 → 4
                              ↘
Parallel:                      → 5 ─┐
                              ↘    │
                               → 6 ┼→ 7 → Output
```

---

## Input Schema

```json
{
  "$schema": "daily_generation_input.schema.json",
  "type": "object",
  "required": ["unit", "day", "topic", "learning_objectives", "standards"],
  "properties": {
    "unit": {
      "type": "object",
      "properties": {
        "number": {"type": "integer", "minimum": 1, "maximum": 4},
        "name": {"type": "string"},
        "total_days": {"type": "integer"}
      }
    },
    "day": {"type": "integer", "minimum": 1},
    "topic": {"type": "string"},
    "prior_knowledge": {"type": "string"},
    "vocabulary": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "term": {"type": "string"},
          "definition": {"type": "string"},
          "usage_example": {"type": "string"}
        }
      }
    },
    "learning_objectives": {
      "type": "array",
      "minItems": 2,
      "maxItems": 4,
      "items": {"type": "string"}
    },
    "standards": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "code": {"type": "string"},
          "text": {"type": "string"}
        }
      }
    },
    "content_points": {
      "type": "array",
      "items": {"type": "string"}
    },
    "warmup": {
      "type": "object",
      "properties": {
        "type": {"enum": ["physical", "mental", "social", "creative", "content"]},
        "suggested_activity": {"type": "string"}
      }
    },
    "activity": {
      "type": "object",
      "properties": {
        "type": {"enum": ["writing", "discussion", "performance", "annotation", "creative", "physical", "collaborative"]},
        "suggested_activity": {"type": "string"},
        "materials": {"type": "array", "items": {"type": "string"}}
      }
    },
    "journal_prompt": {"type": "string"},
    "exit_ticket_focus": {"type": "string"}
  }
}
```

---

## Output Schema

```json
{
  "$schema": "daily_generation_output.schema.json",
  "type": "object",
  "required": ["lesson_plan", "warmup", "powerpoint", "presenter_notes", "activity", "journal_exit"],
  "properties": {
    "metadata": {
      "type": "object",
      "properties": {
        "unit_number": {"type": "integer"},
        "unit_name": {"type": "string"},
        "day_number": {"type": "integer"},
        "generated_at": {"type": "string", "format": "date-time"},
        "pipeline_version": {"type": "string"}
      }
    },
    "lesson_plan": {"$ref": "lesson_plan.schema.json"},
    "warmup": {"$ref": "warmup.schema.json"},
    "powerpoint": {"$ref": "powerpoint.schema.json"},
    "presenter_notes": {"$ref": "presenter_notes.schema.json"},
    "activity": {"$ref": "activity.schema.json"},
    "journal_exit": {"$ref": "journal_exit.schema.json"},
    "handout": {"$ref": "handout.schema.json"},
    "coherence_check": {
      "type": "object",
      "properties": {
        "vocabulary_aligned": {"type": "boolean"},
        "objectives_covered": {"type": "boolean"},
        "activity_coherent": {"type": "boolean"},
        "warmup_relevant": {"type": "boolean"},
        "exit_tickets_valid": {"type": "boolean"}
      }
    },
    "timing_estimate": {
      "type": "object",
      "properties": {
        "total_minutes": {"type": "number"},
        "presenter_notes_words": {"type": "integer"},
        "speaking_duration_minutes": {"type": "number"}
      }
    }
  }
}
```

---

## Error Handling

### Generation Failures

```
ERROR HANDLING STRATEGY
=======================

For each agent in the pipeline:

ON AGENT FAILURE:
  1. Log error with full context
  2. Check if failure is recoverable:
     - Timeout → Retry with extended timeout
     - Validation → Pass to validation gate (may be fixable)
     - Fatal → Flag for human review
  3. If recoverable, retry up to 2 times
  4. If still failing, generate minimal valid output + flag
  5. Continue pipeline (don't block other components)

RECOVERABLE ERRORS:
  - Content too short → Request elaboration
  - Content too long → Request condensation
  - Missing markers → Auto-insert via skill
  - Invalid format → Restructure and retry

NON-RECOVERABLE ERRORS:
  - API failure → Escalate
  - Invalid input data → Reject with message
  - Schema violation (fundamental) → Escalate
```

### Partial Output Policy

If any agent fails after retries:
1. Generate what you can
2. Mark failed components as `"status": "failed"`
3. Include `"error": "description"`
4. Pass to validation (which will fail structure gate)
5. Validation will route back to regeneration

---

## Skill Integration Points

### Skills Called Per Agent

| Agent | Skills Used |
|-------|-------------|
| lesson_plan_generator | admin_template_formatter |
| warmup_generator | warmup_bank_selector, content_connector |
| powerpoint_generator | header_enforcer, body_overflow_enforcer, performance_tip_fallback |
| presenter_notes_writer | monologue_scripter, marker_insertion, word_count_analyzer |
| activity_generator | activity_type_selector, instruction_scaffolder, timing_allocator |
| journal_exit_generator | reflection_prompt_writer, assessment_question_writer |
| handout_generator | instruction_scaffolder, admin_template_formatter |

---

## Usage Example

```python
from orchestrators.daily_generation_orchestrator import DailyGenerationOrchestrator

# Load daily input
with open('inputs/sample_theater/sample_unit1_greek_day1.json') as f:
    daily_input = json.load(f)

# Create orchestrator instance
orchestrator = DailyGenerationOrchestrator()

# Run generation
result = orchestrator.run(
    unit={
        "number": 1,
        "name": "Greek Theater",
        "total_days": 20
    },
    day=1,
    daily_input=daily_input
)

# Check result
if result['coherence_check']['all_passed']:
    print(f"Generation complete: {result['timing_estimate']['total_minutes']} min")
else:
    print(f"Coherence issues: {result['coherence_check']}")

# Send to validation
validation_result = validation_gate_orchestrator.run(result)
```

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-01-08 | Initial daily generation orchestrator |

---

## Related Documents

- `theater_master_orchestrator.md` - Parent orchestrator
- `validation_gate_orchestrator.md` - Next phase
- `config/constraints.yaml` - All timing and text constraints
- `agents/prompts/*.md` - Individual agent specifications
