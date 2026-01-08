# Theater Pipeline Master Orchestrator

**Version:** 1.0
**Purpose:** Entry point for the entire theater education pipeline
**Domain:** Theater Education (High School, Grades 9-12)

---

## Overview

The Theater Master Orchestrator coordinates the complete generation workflow for theater education lessons. It manages four major phases:

1. **Unit Planning** - Generate 18-25 day unit plans with standards mapping
2. **Daily Generation** - Create complete daily lesson packages (56-minute structure)
3. **Validation Gates** - Run HARDCODED validators to ensure quality
4. **Assembly** - Package deliverables for production use

---

## Pipeline Constants (from config/constraints.yaml)

### Daily Structure (56 minutes total)
| Component | Duration | Tolerance | Description |
|-----------|----------|-----------|-------------|
| Agenda/Journal-In | 5 min | ±30 sec | Agenda display and journal prompt |
| Warmup | 5 min | ±30 sec | Content-connected theater warmup |
| Lecture | 15 min | ±1 min | PowerPoint with verbatim presenter notes |
| Activity | 15 min | ±1 min | Structured hands-on activity |
| Reflection | 10 min | ±1 min | Journal reflection and exit ticket |
| Buffer | 6 min | N/A | Transition and flexibility time |

### Unit Structure
| Unit | Name | Days | Focus Areas |
|------|------|------|-------------|
| 1 | Greek Theater | 20 | Origins, tragedy, comedy, chorus, masks |
| 2 | Commedia dell'Arte | 18 | Stock characters, lazzi, improvisation, physicality |
| 3 | Shakespeare | 25 | Language, verse, staging, character analysis |
| 4 | Student-Directed One Acts | 17 | Directing, blocking, rehearsal, production |

### PowerPoint Structure (16 slides)
| Slide | Type | Content |
|-------|------|---------|
| 1 | Auxiliary | Agenda |
| 2 | Auxiliary | Warmup Instructions |
| 3-14 | Content | Learning Content (12 slides) |
| 15 | Auxiliary | Activity Instructions |
| 16 | Auxiliary | Journal & Exit Ticket |

---

## Agents Managed

### Phase 1: Unit Planning Agents
| Agent | Purpose | Input | Output |
|-------|---------|-------|--------|
| unit_planner | Generate 18-25 day unit scope | unit_request | unit_plan |
| unit_scope_validator | Validate scope fits days | unit_plan | validation_result |
| standards_mapper | Map CA ELA standards to objectives | unit_plan | standards_map |
| learning_objective_generator | Generate Bloom's-aligned objectives | content_outline | objectives |

### Phase 2: Daily Generation Agents
| Agent | Purpose | Input | Output |
|-------|---------|-------|--------|
| lesson_plan_generator | Generate admin-friendly lesson plan | daily_input | lesson_plan |
| warmup_generator | Generate 5-min content-connected warmup | daily_input | warmup |
| powerpoint_generator | Generate 16-slide PowerPoint | daily_input | powerpoint |
| presenter_notes_writer | Generate 15-min verbatim script | powerpoint | presenter_notes |
| activity_generator | Generate 15-min structured activity | daily_input | activity |
| journal_exit_generator | Generate reflection prompts and exit tickets | daily_input | journal_exit |
| handout_generator | Generate print-ready activity handouts | activity | handout |

### Phase 3: Validation Agents (HARDCODED - CANNOT BE BYPASSED)
| Agent | Purpose | Pass Criteria | Gate Type |
|-------|---------|---------------|-----------|
| truncation_validator | Ensure no truncated sentences | 100% complete sentences | MUST PASS |
| structure_validator | Validate all components present | 100% components | MUST PASS |
| elaboration_validator | Ensure content depth | Score ≥ 85/100 | QUALITY |
| timing_validator | Validate duration (14-16 min) | Within tolerance | QUALITY |
| coherence_validator | Validate internal consistency | Score ≥ 80/100 | QUALITY |

### Phase 4: Assembly Agents
| Agent | Purpose | Input | Output |
|-------|---------|-------|--------|
| lesson_assembler | Combine all daily components | all_daily_outputs | lesson_package |
| powerpoint_assembler | Build final .pptx file | powerpoint + notes | pptx_file |
| unit_folder_organizer | Organize into production folders | all_lessons | folder_structure |
| final_qa_reporter | Generate QA summary report | validation_results | qa_report |

---

## Skills Required

### Generation Skills
| Skill | Path | Purpose |
|-------|------|---------|
| monologue_scripter | skills/generation/monologue_scripter.py | Generate verbatim presenter notes |
| warmup_bank_selector | skills/generation/warmup_bank_selector.py | Select unit-appropriate warmups |
| content_connector | skills/generation/content_connector.py | Connect warmups to lesson content |
| activity_type_selector | skills/generation/activity_type_selector.py | Select appropriate activity types |
| instruction_scaffolder | skills/generation/instruction_scaffolder.py | Create scaffolded instructions |

### Validation Skills
| Skill | Path | Purpose |
|-------|------|---------|
| word_count_analyzer | skills/validation/word_count_analyzer.py | Count words for timing |
| duration_estimator | skills/validation/duration_estimator.py | Estimate speaking duration |
| sentence_completeness_checker | skills/validation/sentence_completeness_checker.py | Check for truncation |
| fragment_detector | skills/validation/fragment_detector.py | Detect incomplete fragments |
| depth_analyzer | skills/validation/depth_analyzer.py | Analyze elaboration depth |

### Enforcement Skills (Theater-adapted)
| Skill | Path | Purpose |
|-------|------|---------|
| header_enforcer | skills/enforcement/header_enforcer.py | 36 chars, 1 line max |
| body_overflow_enforcer | skills/enforcement/body_overflow_enforcer.py | 12 lines max, word wrap |
| marker_insertion | skills/enforcement/marker_insertion.py | [PAUSE], [EMPHASIS] markers |
| performance_tip_fallback | skills/enforcement/performance_tip_fallback.py | Ensure performance tips |
| slide_numbering | skills/enforcement/slide_numbering.py | Sequential numbering |

---

## Execution Flow

```
THEATER PIPELINE MASTER FLOW
============================

INPUT: Unit selection (1-4) OR Specific day request
OUTPUT: Complete lesson package(s) for production use

┌─────────────────────────────────────────────────────────────────┐
│                    PHASE 1: UNIT PLANNING                       │
│  (Run once per unit, or load existing unit plan)                │
├─────────────────────────────────────────────────────────────────┤
│  1.1 unit_planner                                               │
│      └── Generate scope: 18-25 day outline                      │
│  1.2 standards_mapper                                           │
│      └── Map CA ELA standards (RL.9-12, SL.9-12, W.9-12)        │
│  1.3 learning_objective_generator                               │
│      └── Create 2-4 objectives per day (Bloom's verbs)          │
│  1.4 unit_scope_validator                                       │
│      └── VALIDATE: Content fits allocated days                  │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                PHASE 2: DAILY GENERATION                        │
│  (Run for each day in unit, parallelizable)                     │
├─────────────────────────────────────────────────────────────────┤
│  2.1 lesson_plan_generator                                      │
│      └── Admin-friendly scripted lesson plan                    │
│                                                                 │
│  2.2 warmup_generator                                           │
│      ├── Type: physical, mental, social, creative, content      │
│      ├── Duration: 5 minutes                                    │
│      └── REQUIREMENT: Must connect to lesson content            │
│                                                                 │
│  2.3 powerpoint_generator                                       │
│      ├── 4 auxiliary slides (agenda, warmup, activity, journal) │
│      ├── 12 content slides                                      │
│      └── Text Limits: 36-char header, 12-line body              │
│                                                                 │
│  2.4 presenter_notes_writer                                     │
│      ├── Target: 1,950-2,250 words (15 min at 140 WPM)          │
│      ├── Style: Verbatim script, natural spoken language        │
│      ├── Markers: [PAUSE] ×2+, [EMPHASIS: term] ×1+             │
│      └── [CHECK FOR UNDERSTANDING] ×3+ per presentation         │
│                                                                 │
│  2.5 activity_generator                                         │
│      ├── Duration: 15 minutes (1.5 setup, 11 work, 2.5 share)   │
│      ├── Types: writing, discussion, performance, annotation    │
│      └── Differentiation: ELL, advanced, struggling             │
│                                                                 │
│  2.6 journal_exit_generator                                     │
│      ├── Journal: Open-ended reflection (10 min)                │
│      └── Exit Tickets: 2-3 quick assessments                    │
│                                                                 │
│  2.7 handout_generator                                          │
│      └── Print-ready activity handout (if applicable)           │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│           PHASE 3: VALIDATION GATES (HARDCODED)                 │
│  (Must pass ALL gates before assembly)                          │
├─────────────────────────────────────────────────────────────────┤
│  GATE 1: TRUNCATION VALIDATOR (MUST PASS - NO BYPASS)           │
│  ├── Check: Every sentence ends with . ! ? or :                 │
│  ├── Check: No trailing ellipsis (...)                          │
│  ├── Check: No mid-word cuts                                    │
│  ├── Check: No incomplete thoughts                              │
│  ├── On FAIL: Return to Phase 2 with specific fix instructions  │
│  └── On PASS: Continue to Gate 2                                │
│                                                                 │
│  GATE 2: STRUCTURE VALIDATOR (MUST PASS - NO BYPASS)            │
│  ├── Check: lesson_plan present                                 │
│  ├── Check: powerpoint has 16 slides                            │
│  ├── Check: presenter_notes exist for all content slides        │
│  ├── Check: warmup present with all required fields             │
│  ├── Check: activity present with all required fields           │
│  ├── Check: handout generated (if activity requires one)        │
│  ├── Check: journal_prompt present                              │
│  ├── Check: exit_tickets present (2-3)                          │
│  ├── Check: standards linked                                    │
│  ├── Check: materials_list complete                             │
│  ├── On FAIL: Return to Phase 2 with missing component list     │
│  └── On PASS: Continue to Gate 3                                │
│                                                                 │
│  GATE 3: ELABORATION VALIDATOR (Score ≥ 85/100)                 │
│  ├── Scoring:                                                   │
│  │   ├── depth: 30%                                             │
│  │   ├── examples: 20%                                          │
│  │   ├── procedure: 20%                                         │
│  │   ├── tone: 15%                                              │
│  │   └── connections: 15%                                       │
│  ├── On FAIL (score < 85): Return to Phase 2 for enrichment     │
│  └── On PASS: Continue to Gate 4                                │
│                                                                 │
│  GATE 4: TIMING VALIDATOR (14-16 minutes)                       │
│  ├── Check: presenter_notes word count (1,950-2,250 words)      │
│  ├── Check: per-slide word count (100-250 words)                │
│  ├── Check: estimated duration at 140 WPM                       │
│  ├── On FAIL (too short): Return for elaboration                │
│  ├── On FAIL (too long): Return for condensation                │
│  └── On PASS: Proceed to Phase 4                                │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    PHASE 4: ASSEMBLY                            │
│  (Package all components for production use)                    │
├─────────────────────────────────────────────────────────────────┤
│  4.1 lesson_assembler                                           │
│      └── Combine: lesson_plan + warmup + activity + journal     │
│                                                                 │
│  4.2 powerpoint_assembler                                       │
│      ├── Populate template with content                         │
│      ├── Insert presenter notes                                 │
│      └── Generate .pptx file                                    │
│                                                                 │
│  4.3 unit_folder_organizer                                      │
│      └── Structure:                                             │
│          Unit_{N}_{Name}/                                       │
│          ├── Day_{DD}/                                          │
│          │   ├── Lesson_Plan.docx                               │
│          │   ├── PowerPoint.pptx                                │
│          │   ├── Handout.pdf (if applicable)                    │
│          │   └── Teacher_Notes.md                               │
│          └── Unit_Resources/                                    │
│              ├── Standards_Map.csv                              │
│              ├── Vocabulary_Master.csv                          │
│              └── Assessment_Bank.json                           │
│                                                                 │
│  4.4 final_qa_reporter                                          │
│      └── Generate: QA_Report_{unit}_{date}.md                   │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
                        OUTPUT: Complete
                        lesson package(s)
```

---

## Sub-Orchestrators

### 1. unit_planning_orchestrator.md
- Manages Phase 1 agents
- Input: Unit number (1-4)
- Output: Complete unit plan with standards mapping

### 2. daily_generation_orchestrator.md
- Manages Phase 2 agents for a single day
- Input: Unit plan + day number
- Output: All daily components (before validation)

### 3. validation_gate_orchestrator.md
- Manages Phase 3 HARDCODED validators
- Input: Daily components from Phase 2
- Output: Validated components OR rejection with fix instructions

### 4. assembly_orchestrator.md
- Manages Phase 4 assembly agents
- Input: Validated daily components
- Output: Production-ready files

---

## Error Recovery Strategy

### Validation Failure Handling

```
RETRY LOGIC FOR VALIDATION FAILURES
===================================

MAX_RETRIES = 3

For each failed validation gate:

Attempt 1: TARGETED FIX
  ├── Pass specific failure context to generating agent
  ├── Request targeted fixes only
  └── Re-validate failed gate only

Attempt 2: SECTION REGENERATION
  ├── If targeted fix fails
  ├── Regenerate entire failing component
  └── Re-validate from Gate 1

Attempt 3: FULL REGENERATION
  ├── If section regeneration fails
  ├── Regenerate all Phase 2 outputs
  └── Full validation from Gate 1

On 3 failures: ESCALATE
  └── Flag for human review with detailed error log
```

### Context Preservation

All validation failures preserve:
- Original input
- Generated content
- Specific failure reasons
- Suggested fixes
- Retry iteration count

---

## Input Schema

```json
{
  "$schema": "theater_pipeline_input.schema.json",
  "type": "object",
  "required": ["request_type"],
  "properties": {
    "request_type": {
      "enum": ["unit", "day", "range"]
    },
    "unit_number": {
      "type": "integer",
      "minimum": 1,
      "maximum": 4
    },
    "day_number": {
      "type": "integer",
      "minimum": 1,
      "maximum": 25
    },
    "day_range": {
      "type": "object",
      "properties": {
        "start": {"type": "integer"},
        "end": {"type": "integer"}
      }
    },
    "options": {
      "type": "object",
      "properties": {
        "skip_existing": {"type": "boolean", "default": true},
        "parallel_generation": {"type": "boolean", "default": true},
        "output_format": {"enum": ["production", "draft", "review"]}
      }
    }
  }
}
```

---

## Output Schema

```json
{
  "$schema": "theater_pipeline_output.schema.json",
  "type": "object",
  "properties": {
    "status": {
      "enum": ["success", "partial", "failed"]
    },
    "unit": {
      "type": "object",
      "properties": {
        "number": {"type": "integer"},
        "name": {"type": "string"},
        "days_generated": {"type": "integer"},
        "days_total": {"type": "integer"}
      }
    },
    "validation_results": {
      "type": "object",
      "properties": {
        "truncation": {"type": "boolean"},
        "structure": {"type": "boolean"},
        "elaboration_score": {"type": "number"},
        "timing_minutes": {"type": "number"}
      }
    },
    "outputs": {
      "type": "object",
      "properties": {
        "lesson_plans": {"type": "array"},
        "powerpoints": {"type": "array"},
        "handouts": {"type": "array"},
        "qa_report": {"type": "string"}
      }
    },
    "errors": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "day": {"type": "integer"},
          "component": {"type": "string"},
          "error": {"type": "string"},
          "resolution": {"type": "string"}
        }
      }
    }
  }
}
```

---

## Integration Points

### Config Files Referenced
- `config/constraints.yaml` - All text limits and timing requirements
- `config/theater.yaml` - Brand, colors, teaching style
- `config/theater_template.yaml` - PowerPoint shape mappings

### Sample Inputs
- `inputs/sample_theater/sample_unit1_greek_day1.json`
- `inputs/sample_theater/sample_unit2_commedia_day1.json`
- `inputs/sample_theater/sample_unit3_shakespeare_day1.json`
- `inputs/sample_theater/sample_unit4_oneacts_day1.json`

### Output Locations
- `outputs/unit_plans/` - Unit planning outputs
- `outputs/daily/` - Daily generation outputs (pre-validation)
- `outputs/validated/` - Post-validation outputs
- `outputs/production/` - Final assembled outputs
- `outputs/qa_reports/` - QA validation reports

---

## Usage Examples

### Generate Full Unit
```python
from orchestrators import theater_master_orchestrator

result = theater_master_orchestrator.run({
    "request_type": "unit",
    "unit_number": 1,
    "options": {
        "parallel_generation": True,
        "output_format": "production"
    }
})
```

### Generate Single Day
```python
result = theater_master_orchestrator.run({
    "request_type": "day",
    "unit_number": 3,
    "day_number": 5,
    "options": {
        "output_format": "draft"
    }
})
```

### Generate Day Range
```python
result = theater_master_orchestrator.run({
    "request_type": "range",
    "unit_number": 2,
    "day_range": {"start": 1, "end": 5},
    "options": {
        "skip_existing": True,
        "parallel_generation": True
    }
})
```

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-01-08 | Initial theater-specific master orchestrator |

---

## Related Documents

- `AGENTS.md` - Complete agent specifications
- `THEATER_PIPELINE_ARCHITECTURE.md` - Architecture overview
- `config/constraints.yaml` - All pipeline constraints
- `config/theater.yaml` - Theater-specific configuration
