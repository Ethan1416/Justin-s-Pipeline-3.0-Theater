# AGENTS.md - Theater Lecture Generation Pipeline

## Master Instructions for Claude Code Agent System

**Version:** 2.0
**Pipeline:** High School Theater Education
**Architecture:** Multi-Agent Orchestration with Hardcoded Validators
**Target:** Grades 9-12, Mixed Levels

---

## System Overview

This pipeline generates complete theater education lesson packages for high school students. Each lesson includes unit plans, daily lesson plans, PowerPoints with 15-minute verbatim presenter notes, warmups, activities, handouts, and journal/exit ticket prompts.

**Key Features:**
- **Hardcoded Validation Agents** - Truncation and elaboration validators that cannot be bypassed
- **Standards Alignment** - California ELA/Literacy standards (RL, SL, W.9-12)
- **Structured Activities** - No abstract warmups; all content-connected
- **Verbatim Scripts** - 15 minutes of word-for-word presenter notes per lesson

---

## Course Structure

### Units (4 total, 80 instructional days)

| Unit | Name | Days | Focus |
|------|------|------|-------|
| 1 | Greek Theater | 20 | Origins, tragedy, comedy, chorus, masks |
| 2 | Commedia dell'Arte | 18 | Stock characters, lazzi, improvisation, physicality |
| 3 | Shakespeare | 25 | Language, verse, staging, character analysis |
| 4 | Student-Directed One Acts | 17 | Directing fundamentals, blocking, rehearsal |

### Daily Structure (56 minutes)

| Time | Component | Duration | Pipeline Output |
|------|-----------|----------|-----------------|
| 0:00-0:05 | Agenda & Journal-In | 5 min | Agenda Slide |
| 0:05-0:10 | Warmup | 5 min | Warmup Instructions Slide |
| 0:10-0:25 | Lecture/PowerPoint | 15 min | 12 Content Slides + Presenter Notes |
| 0:25-0:40 | Activity | 15 min | Activity Slide + Handout |
| 0:40-0:50 | Reflection & Exit Ticket | 10 min | Journal Slide + Exit Ticket |
| 0:50-0:56 | Transition/Buffer | 6 min | - |

---

## California Standards Alignment

### Reading Literature (RL.9-12)
- **RL.9-10.3 / RL.11-12.3**: Character analysis, plot development
- **RL.9-10.4 / RL.11-12.4**: Language analysis (especially Shakespeare)
- **RL.9-10.5 / RL.11-12.5**: Structure and aesthetic impact
- **RL.9-10.6 / RL.11-12.6**: Point of view, satire, irony

### Speaking & Listening (SL.9-12)
- **SL.9-10.1 / SL.11-12.1**: Collaborative discussions
- **SL.9-10.4 / SL.11-12.4**: Present information clearly
- **SL.9-10.6 / SL.11-12.6**: Adapt speech to context

### Writing (W.9-12)
- **W.9-10.1 / W.11-12.1**: Argumentative writing
- **W.9-10.2 / W.11-12.2**: Informative/explanatory writing
- **W.9-10.3 / W.11-12.3**: Narrative writing

---

## Pipeline Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         MASTER ORCHESTRATOR                                  │
│                    orchestrators/theater_pipeline.md                        │
└─────────────────────────────────────┬───────────────────────────────────────┘
                                      │
        ┌─────────────────────────────┼─────────────────────────────┐
        │                             │                             │
        ▼                             ▼                             ▼
┌───────────────────┐     ┌───────────────────────┐     ┌───────────────────────┐
│   UNIT PLANNING   │     │   DAILY GENERATION    │     │   VALIDATION GATE     │
│   ORCHESTRATOR    │     │    ORCHESTRATOR       │     │    ORCHESTRATOR       │
└─────────┬─────────┘     └───────────┬───────────┘     └───────────┬───────────┘
          │                           │                             │
          ▼                           ▼                             ▼
    ┌──────────┐               ┌──────────────┐              ┌──────────────┐
    │ Unit     │               │ Lesson Plan  │              │ TRUNCATION   │
    │ Planner  │               │ Generator    │              │ VALIDATOR    │
    │          │               ├──────────────┤              │ (HARDCODED)  │
    │ Standards│               │ PowerPoint   │              ├──────────────┤
    │ Mapper   │               │ Generator    │              │ ELABORATION  │
    │          │               ├──────────────┤              │ VALIDATOR    │
    │ Scope    │               │ Presenter    │              │ (HARDCODED)  │
    │ Validator│               │ Notes Writer │              ├──────────────┤
    └──────────┘               ├──────────────┤              │ TIMING       │
                               │ Warmup       │              │ VALIDATOR    │
                               │ Generator    │              │ (HARDCODED)  │
                               ├──────────────┤              └──────────────┘
                               │ Activity     │
                               │ Generator    │
                               ├──────────────┤
                               │ Handout      │
                               │ Generator    │
                               ├──────────────┤
                               │ Journal/Exit │
                               │ Generator    │
                               └──────────────┘
```

---

## HARDCODED VALIDATION AGENTS (CRITICAL)

These agents CANNOT be bypassed, modified, or relaxed during pipeline execution.

### 1. Truncation Validator
**File:** `agents/prompts/truncation_validator.md`
**Purpose:** Detect and AUTO-FIX truncated sentences
**Skills:**
- `sentence_completeness_checker`
- `fragment_detector`
- `auto_completion_fixer`

**Rules:**
- Every sentence MUST end with `.` `!` `?` `:`
- No trailing ellipsis (`...`)
- No mid-word cuts
- No incomplete thoughts

### 2. Elaboration Validator
**File:** `agents/prompts/elaboration_validator.md`
**Purpose:** Ensure professional educational content depth
**Skills:**
- `depth_analyzer`
- `professional_tone_checker`
- `expansion_suggester`

**Scoring:**
- Pass threshold: ≥85/100
- Categories: Depth (30%), Examples (20%), Procedure (20%), Tone (15%), Connections (15%)

### 3. Timing Validator
**File:** `agents/prompts/timing_validator.md`
**Purpose:** Ensure content fits time allocations
**Skills:**
- `word_count_analyzer`
- `speaking_pace_calculator`
- `duration_estimator`

**Targets:**
- Presenter notes: 1,950-2,250 words (15 minutes at 130-150 WPM)
- Warmup: 5 minutes
- Activity: 15 minutes

### 4. Structure Validator
**File:** `agents/prompts/structure_validator.md`
**Purpose:** Ensure all lesson components are present and properly structured
**Skills:**
- `component_checker`
- `schema_validator`
- `cross_reference_checker`

**Checks:**
- All 10 required components present
- No CRITICAL issues
- Cross-references consistent (unit, day, topic, objectives)
- PowerPoint has correct slide count

---

## Agent Registry

### Phase 1: Unit Planning Agents (5)

| Agent | File | Hardcoded Skills | Purpose |
|-------|------|------------------|---------|
| unit_planner | `agents/prompts/unit_planner.md` | `scope_calculator`, `standards_mapper` | Generate 18-25 day unit plan |
| unit_scope_validator | `agents/prompts/unit_scope_validator.md` | `day_counter`, `content_density_checker` | Validate unit fits time |
| standards_mapper | `agents/prompts/standards_mapper.md` | `standards_lookup`, `alignment_scorer` | Map content to CA standards |
| unit_sequence_optimizer | `agents/prompts/unit_sequence_optimizer.md` | `prerequisite_checker` | Optimize lesson sequence |
| learning_objective_generator | `agents/prompts/learning_objective_generator.md` | `blooms_taxonomy_classifier` | Generate measurable objectives |

### Phase 2: Daily Generation Agents (12)

| Agent | File | Hardcoded Skills | Purpose |
|-------|------|------------------|---------|
| daily_agenda_generator | `agents/prompts/daily_agenda_generator.md` | `time_allocator` | Create 56-min daily agenda |
| lesson_plan_generator | `agents/prompts/lesson_plan_generator.md` | `admin_template_formatter` | Generate scripted lesson plan |
| warmup_generator | `agents/prompts/warmup_generator.md` | `warmup_bank_selector`, `content_connector` | Generate content-connected warmup |
| powerpoint_generator | `agents/prompts/powerpoint_generator.md` | `slide_builder` | Generate 12 content slides |
| presenter_notes_writer | `agents/prompts/presenter_notes_writer.md` | `monologue_scripter`, `timing_pacer` | Write 15-min verbatim script |
| activity_generator | `agents/prompts/activity_generator.md` | `activity_type_selector` | Generate structured activities |
| handout_generator | `agents/prompts/handout_generator.md` | `handout_formatter` | Create activity handouts |
| journal_prompt_generator | `agents/prompts/journal_prompt_generator.md` | `reflection_prompt_writer` | Generate reflection prompts |
| exit_ticket_generator | `agents/prompts/exit_ticket_generator.md` | `assessment_writer` | Generate exit ticket questions |
| auxiliary_slide_generator | `agents/prompts/auxiliary_slide_generator.md` | `non_content_slide_builder` | Generate agenda/warmup/activity slides |
| differentiation_annotator | `agents/prompts/differentiation_annotator.md` | `ell_support_adder` | Add differentiation notes |
| materials_list_generator | `agents/prompts/materials_list_generator.md` | `resource_identifier` | Generate materials list |

### Phase 3: Validation Agents - HARDCODED (8)

| Agent | File | Hardcoded Skills | Validation Focus |
|-------|------|------------------|------------------|
| **truncation_validator** | `agents/prompts/truncation_validator.md` | `sentence_completeness_checker`, `auto_completion_fixer` | **CRITICAL**: No truncated sentences |
| **elaboration_validator** | `agents/prompts/elaboration_validator.md` | `depth_analyzer`, `professional_tone_checker` | Professional elaboration |
| **timing_validator** | `agents/prompts/timing_validator.md` | `word_count_analyzer`, `duration_estimator` | 15-min content fits |
| **structure_validator** | `agents/prompts/structure_validator.md` | `component_checker` | All components present |
| **standards_coverage_validator** | `agents/prompts/standards_coverage_validator.md` | `standards_tracker` | Standards addressed |
| **coherence_validator** | `agents/prompts/coherence_validator.md` | `flow_analyzer` | Logical lesson flow |
| **pedagogy_validator** | `agents/prompts/pedagogy_validator.md` | `engagement_scorer` | Sound teaching practices |
| **content_accuracy_validator** | `agents/prompts/content_accuracy_validator.md` | `fact_checker` | Theater content accuracy |

### Phase 4: Assembly Agents (4)

| Agent | File | Purpose |
|-------|------|---------|
| lesson_assembler | `agents/prompts/lesson_assembler.md` | Assemble complete lesson package |
| powerpoint_assembler | `agents/prompts/powerpoint_assembler.md` | Assemble final PowerPoint |
| unit_folder_organizer | `agents/prompts/unit_folder_organizer.md` | Organize output folders |
| final_qa_reporter | `agents/prompts/final_qa_reporter.md` | Generate QA summary |

---

## Output Folder Structure

```
production/
├── Unit_1_Greek_Theater/
│   ├── unit_plan.md
│   ├── standards_map.json
│   ├── Day_01/
│   │   ├── lesson_plan.md
│   │   ├── powerpoint.pptx
│   │   ├── handout.pdf
│   │   ├── journal_prompts.md
│   │   └── exit_ticket.md
│   ├── Day_02/
│   │   └── ...
│   └── Day_20/
├── Unit_2_Commedia_dellArte/
├── Unit_3_Shakespeare/
└── Unit_4_Student_Directed_One_Acts/
```

---

## Lesson Plan Template (Admin-Friendly)

Standard template includes:
- Basic Information (teacher, course, date, duration, unit, day)
- Standards Addressed (RL, SL, W codes with full text)
- Learning Objectives (measurable, Bloom's verbs)
- Materials Needed (checklist)
- Lesson Procedure (teacher actions, student actions, timing)
- Differentiation (ELL support, advanced, struggling)
- Assessment (formative, summative connections)
- Post-Lesson Reflection space

---

## PowerPoint Structure

### Slide Count: 12 Content + 4 Auxiliary = 16 Total

| Slide # | Type | Content | Counted |
|---------|------|---------|---------|
| 1 | Auxiliary | Agenda | No |
| 2 | Auxiliary | Warmup Instructions | No |
| 3-14 | Content | Learning Content (12 slides) | Yes |
| 15 | Auxiliary | Activity Instructions | No |
| 16 | Auxiliary | Journal & Exit Ticket | No |

### Presenter Notes Requirements

- **Total Words:** 1,950-2,250 (15 minutes at 130-150 WPM)
- **Per Content Slide:** ~160-190 words average
- **Format:** VERBATIM script (word-for-word)
- **Markers:** [PAUSE], [EMPHASIS: term], [CHECK FOR UNDERSTANDING]

---

## Validation Gates

### Gate 1: Post-Generation (MANDATORY)
1. **Truncation Validator** - MUST PASS (auto-fixes)
2. **Structure Validator** - MUST PASS

### Gate 2: Quality (Score-Based)
1. **Elaboration Validator** - Score ≥ 85/100
2. **Timing Validator** - Within ±10% of target
3. **Coherence Validator** - Score ≥ 80/100

### Gate 3: Standards (Coverage)
1. **Standards Coverage Validator** - All objectives linked
2. **Pedagogy Validator** - Score ≥ 80/100

---

## Configuration Files

| File | Purpose |
|------|---------|
| `config/pipeline.yaml` | Pipeline settings, timeouts |
| `config/theater.yaml` | Theater-specific brand config |
| `config/constraints.yaml` | Text limits, timing constraints |
| `config/theater_template.yaml` | PowerPoint shape mappings |

---

## Sample Inputs

Located in `inputs/sample_theater/`:
- `sample_unit1_greek_day1.json` - Greek Theater Day 1
- `sample_unit2_commedia_day1.json` - Commedia dell'Arte Day 1
- `sample_unit3_shakespeare_day1.json` - Shakespeare Day 1
- `sample_unit4_oneacts_day1.json` - Student-Directed One Acts Day 1

These can be run in parallel for testing validation agents.

---

## Quick Start

1. **Load Config:** `config/pipeline.yaml`
2. **Generate Unit Plan:** Run unit_planner for selected unit
3. **Generate Daily Lessons:** For each day, run daily generation orchestrator
4. **Validate:** All content passes through hardcoded validators
5. **Assemble:** Organize into production folder structure

---

## Architecture Documentation

See `THEATER_PIPELINE_ARCHITECTURE.md` for:
- Complete agent specifications
- Skill definitions
- Validation rules
- Sample outputs

---

## Created Agent Files

### Implemented Agents (with full specifications):
| Agent | File | Status |
|-------|------|--------|
| truncation_validator | `agents/prompts/truncation_validator.md` | ✅ Complete |
| elaboration_validator | `agents/prompts/elaboration_validator.md` | ✅ Complete |
| timing_validator | `agents/prompts/timing_validator.md` | ✅ Complete |
| structure_validator | `agents/prompts/structure_validator.md` | ✅ Complete |
| unit_planner | `agents/prompts/unit_planner.md` | ✅ Complete |
| lesson_plan_generator | `agents/prompts/lesson_plan_generator.md` | ✅ Complete |
| presenter_notes_writer | `agents/prompts/presenter_notes_writer.md` | ✅ Complete |
| warmup_generator | `agents/prompts/warmup_generator.md` | ✅ Complete |
| activity_generator | `agents/prompts/activity_generator.md` | ✅ Complete |
| journal_exit_generator | `agents/prompts/journal_exit_generator.md` | ✅ Complete |
| handout_generator | `agents/prompts/handout_generator.md` | ✅ Complete |

### Phase 1 Unit Planning Agents - COMPLETE:
| Agent | File | Status |
|-------|------|--------|
| unit_scope_validator | `agents/prompts/unit_scope_validator.md` | ✅ Complete |
| standards_mapper | `agents/prompts/standards_mapper.md` | ✅ Complete |
| unit_sequence_optimizer | `agents/prompts/unit_sequence_optimizer.md` | ✅ Complete |
| learning_objective_generator | `agents/prompts/learning_objective_generator.md` | ✅ Complete |

### Phase 2-4 Agents (inherited from NCLEX pipeline, theater-adapted):
| Agent | File | Status |
|-------|------|--------|
| daily_agenda_generator | `agents/prompts/daily_agenda_generator.md` | ✅ Inherited |
| powerpoint_generator | `agents/prompts/powerpoint_generator.md` | ✅ Inherited |
| auxiliary_slide_generator | `agents/prompts/auxiliary_slide_generator.md` | ✅ Inherited |
| differentiation_annotator | `agents/prompts/differentiation_annotator.md` | ✅ Inherited |
| materials_list_generator | `agents/prompts/materials_list_generator.md` | ✅ Inherited |
| standards_coverage_validator | `agents/prompts/standards_coverage_validator.md` | ✅ Inherited |
| coherence_validator | `agents/prompts/coherence_validator.md` | ✅ Inherited |
| pedagogy_validator | `agents/prompts/pedagogy_validator.md` | ✅ Inherited |
| content_accuracy_validator | `agents/prompts/content_accuracy_validator.md` | ✅ Inherited |
| lesson_assembler | `agents/prompts/lesson_assembler.md` | ✅ Inherited |
| powerpoint_assembler | `agents/prompts/powerpoint_assembler.md` | ✅ Inherited |
| unit_folder_organizer | `agents/prompts/unit_folder_organizer.md` | ✅ Inherited |
| final_qa_reporter | `agents/prompts/final_qa_reporter.md` | ✅ Inherited |

---

## HARDCODED Lesson Generation Agents (NEW)

These agents are hardcoded and cannot be bypassed:

### Instructional Framework Agents

| Agent | File | Purpose | Hardcoded Rules |
|-------|------|---------|-----------------|
| scaffolding_generator | `skills/enforcement/scaffolding_generator.py` | Generate scaffolding (I Do/We Do/You Do) | R1: 2-4 scaffolds per lesson |
| formative_activities | `skills/enforcement/formative_activities_generator.py` | Generate formative checks | R1: 2+ checks per lesson |
| blooms_taxonomy | `skills/enforcement/blooms_taxonomy_integrator.py` | Bloom's level integration | R1: 3+ levels per lesson |
| webbs_dok | `skills/enforcement/webbs_dok_integrator.py` | Webb's DOK integration | R1: 2+ levels per lesson |
| instruction_integrator | `skills/enforcement/instruction_integrator.py` | Full lesson integration | R1: Lecture frontloads activity |

### Component Orchestrators

| Orchestrator | File | Purpose |
|--------------|------|---------|
| ScaffoldingOrchestrator | `orchestrators/component_orchestrators.py` | Manages scaffolding generation |
| FormativeAssessmentOrchestrator | `orchestrators/component_orchestrators.py` | Manages formative assessment |
| CognitiveFrameworkOrchestrator | `orchestrators/component_orchestrators.py` | Integrates Bloom's and DOK |
| ReadingActivityOrchestrator | `orchestrators/component_orchestrators.py` | Generates reading activities |
| LectureFrontloadOrchestrator | `orchestrators/component_orchestrators.py` | Ensures lecture frontloading |
| LessonGenerationOrchestrator | `orchestrators/component_orchestrators.py` | Master lesson orchestrator |

---

## Romeo and Juliet 6-Week Unit (HARDCODED)

The Shakespeare unit includes complete Romeo and Juliet coverage:

| Week | Act | Days | Focus |
|------|-----|------|-------|
| 1 | 1 | 5 | Prologue through ball scene |
| 2 | 2 | 5 | Balcony scene and marriage |
| 3 | 3 | 6 | Fight scene and banishment |
| 4 | 4 | 5 | Friar's plan and potion |
| 5 | 5 | 5 | Tomb scene and resolution |
| 6 | Performance | 4 | Scene performances |

**Required Reading Activities:** Every lesson includes reading (shared, close, partner, independent, or choral).

---

## Lecture Duration Configuration

| Setting | Value | Notes |
|---------|-------|-------|
| Minimum | 5 minutes | Hardcoded minimum |
| Default | 15 minutes | Standard lecture length |
| Maximum | 20 minutes | Hardcoded maximum |
| Frontloading | Required | Lecture MUST frontload activity content |

---

## Version History

- **v2.3** (2026-01-09): Instructional Framework Integration
  - Added scaffolding generator with gradual release model
  - Added formative activities generator with objective alignment
  - Added Bloom's Taxonomy integrator (action verbs, 6 levels)
  - Added Webb's DOK integrator (4 levels with theater activities)
  - Added instruction integrator for full lesson integration
  - Added component orchestrators for each pipeline element
  - Updated lecture duration to 5-20 minutes range
  - Added Romeo and Juliet 6-week unit plan (30 days)
  - Added reading activities as required component
  - Implemented lecture frontloading for activities
- **v2.2** (2026-01-08): Phase 1 Unit Planning complete
  - Created unit_scope_validator agent
  - Created standards_mapper agent (CA ELA standards)
  - Created unit_sequence_optimizer agent
  - Created learning_objective_generator agent (Bloom's Taxonomy)
  - All Phase 1 Unit Planning agents now implemented
  - Cleaned all NCLEX references from 50+ agent files
- **v2.1** (2026-01-08): Agent implementation phase
  - Created 11 full agent specification files
  - Added 4th sample input (Unit 4: One Acts)
  - All 4 hardcoded validators implemented
  - Core generation agents implemented
- **v2.0** (2026-01-08): Complete overhaul for high school theater education
  - Added hardcoded validation agents
  - 56-minute daily structure
  - 4 units (Greek, Commedia, Shakespeare, One Acts)
  - 15-minute verbatim presenter notes
  - California standards alignment
- **v1.0** (2026-01-08): Initial theater pipeline (adapted from NCLEX)

---

**Last Updated:** 2026-01-09
**Pipeline Owner:** Theater Education Department
