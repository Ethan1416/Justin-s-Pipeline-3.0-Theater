# Theater Pipeline Architecture v2.0

## High School Theater Education Pipeline
**Target:** Grades 9-12 Mixed Levels
**Duration:** 80 instructional days, 56 minutes each
**Units:** 4 units × 18-25 days

---

## Units Overview

| Unit | Name | Days | Focus |
|------|------|------|-------|
| 1 | Greek Theater | 20 | Origins, tragedy, comedy, chorus, masks |
| 2 | Commedia dell'Arte | 18 | Stock characters, lazzi, improvisation, physicality |
| 3 | Shakespeare | 25 | Language, verse, staging, character analysis |
| 4 | Student-Directed One Acts | 17 | Directing fundamentals, blocking, rehearsal process |

---

## Daily Structure (56 minutes)

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
- **RL.9-10.9**: Transformation of source material

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
        ┌─────────────────────────────┼─────────────────────────────────────┐
        │                             │                                     │
        ▼                             ▼                                     ▼
┌───────────────────┐     ┌───────────────────────┐     ┌───────────────────────┐
│   UNIT PLANNING   │     │   DAILY GENERATION    │     │   VALIDATION GATE     │
│   ORCHESTRATOR    │     │    ORCHESTRATOR       │     │    ORCHESTRATOR       │
└─────────┬─────────┘     └───────────┬───────────┘     └───────────┬───────────┘
          │                           │                             │
          ▼                           ▼                             ▼
    ┌──────────┐               ┌──────────────┐              ┌──────────────┐
    │ Unit     │               │ Lesson Plan  │              │ Truncation   │
    │ Planner  │               │ Generator    │              │ Validator    │
    │          │               ├──────────────┤              │ (HARDCODED)  │
    │ Standards│               │ PowerPoint   │              ├──────────────┤
    │ Mapper   │               │ Generator    │              │ Elaboration  │
    │          │               ├──────────────┤              │ Validator    │
    │ Scope    │               │ Warmup       │              │ (HARDCODED)  │
    │ Validator│               │ Generator    │              ├──────────────┤
    └──────────┘               ├──────────────┤              │ Timing       │
                               │ Activity     │              │ Validator    │
                               │ Generator    │              │ (HARDCODED)  │
                               ├──────────────┤              ├──────────────┤
                               │ Handout      │              │ Structure    │
                               │ Generator    │              │ Validator    │
                               ├──────────────┤              │ (HARDCODED)  │
                               │ Journal/Exit │              └──────────────┘
                               │ Generator    │
                               └──────────────┘
```

---

## Agent Registry

### Phase 1: Unit Planning Agents (5)

| Agent | File | Hardcoded Skills | Purpose |
|-------|------|------------------|---------|
| unit_planner | `agents/prompts/unit_planner.md` | `scope_calculator`, `standards_mapper` | Generate 18-25 day unit plan |
| unit_scope_validator | `agents/prompts/unit_scope_validator.md` | `day_counter`, `content_density_checker` | Validate unit fits time constraints |
| standards_mapper | `agents/prompts/standards_mapper.md` | `standards_lookup`, `alignment_scorer` | Map content to CA standards |
| unit_sequence_optimizer | `agents/prompts/unit_sequence_optimizer.md` | `prerequisite_checker`, `scaffolding_analyzer` | Optimize lesson sequence |
| learning_objective_generator | `agents/prompts/learning_objective_generator.md` | `blooms_taxonomy_classifier`, `objective_formatter` | Generate measurable objectives |

### Phase 2: Daily Generation Agents (12)

| Agent | File | Hardcoded Skills | Purpose |
|-------|------|------------------|---------|
| daily_agenda_generator | `agents/prompts/daily_agenda_generator.md` | `time_allocator`, `component_formatter` | Create 56-min daily agenda |
| lesson_plan_generator | `agents/prompts/lesson_plan_generator.md` | `admin_template_formatter`, `timing_calculator` | Generate scripted lesson plan |
| warmup_generator | `agents/prompts/warmup_generator.md` | `warmup_bank_selector`, `content_connector` | Generate content-connected warmup |
| powerpoint_generator | `agents/prompts/powerpoint_generator.md` | `slide_builder`, `content_distributor` | Generate 12 content slides |
| presenter_notes_writer | `agents/prompts/presenter_notes_writer.md` | `monologue_scripter`, `timing_pacer` | Write 15-min verbatim script (~2000 words) |
| activity_generator | `agents/prompts/activity_generator.md` | `activity_type_selector`, `instruction_writer` | Generate structured activities |
| handout_generator | `agents/prompts/handout_generator.md` | `handout_formatter`, `print_optimizer` | Create activity handouts |
| journal_prompt_generator | `agents/prompts/journal_prompt_generator.md` | `reflection_prompt_writer`, `depth_calibrator` | Generate reflection prompts |
| exit_ticket_generator | `agents/prompts/exit_ticket_generator.md` | `assessment_writer`, `quick_check_formatter` | Generate exit ticket questions |
| auxiliary_slide_generator | `agents/prompts/auxiliary_slide_generator.md` | `non_content_slide_builder` | Generate agenda/warmup/activity/journal slides |
| differentiation_annotator | `agents/prompts/differentiation_annotator.md` | `ell_support_adder`, `accommodation_suggester` | Add differentiation notes |
| materials_list_generator | `agents/prompts/materials_list_generator.md` | `resource_identifier`, `prep_checker` | Generate materials/prep list |

### Phase 3: Validation Agents - HARDCODED (8)

| Agent | File | Hardcoded Skills | Validation Focus |
|-------|------|------------------|------------------|
| **truncation_validator** | `agents/prompts/truncation_validator.md` | `sentence_completeness_checker`, `fragment_detector`, `auto_completion_fixer` | **CRITICAL**: Detect and FIX truncated sentences |
| **elaboration_validator** | `agents/prompts/elaboration_validator.md` | `depth_analyzer`, `professional_tone_checker`, `expansion_suggester` | Ensure professional elaboration |
| **timing_validator** | `agents/prompts/timing_validator.md` | `word_count_analyzer`, `speaking_pace_calculator`, `duration_estimator` | Ensure 15-min content fits |
| **structure_validator** | `agents/prompts/structure_validator.md` | `component_checker`, `required_element_scanner` | Ensure all components present |
| **standards_coverage_validator** | `agents/prompts/standards_coverage_validator.md` | `standards_tracker`, `coverage_calculator` | Track standards addressed |
| **coherence_validator** | `agents/prompts/coherence_validator.md` | `flow_analyzer`, `transition_checker` | Ensure logical lesson flow |
| **pedagogy_validator** | `agents/prompts/pedagogy_validator.md` | `engagement_scorer`, `active_learning_checker` | Ensure sound teaching practices |
| **content_accuracy_validator** | `agents/prompts/content_accuracy_validator.md` | `fact_checker`, `historical_accuracy_verifier` | Verify theater content accuracy |

### Phase 4: Assembly Agents (4)

| Agent | File | Hardcoded Skills | Purpose |
|-------|------|------------------|---------|
| lesson_assembler | `agents/prompts/lesson_assembler.md` | `component_merger`, `format_standardizer` | Assemble complete lesson package |
| powerpoint_assembler | `agents/prompts/powerpoint_assembler.md` | `slide_orderer`, `notes_attacher` | Assemble final PowerPoint |
| unit_folder_organizer | `agents/prompts/unit_folder_organizer.md` | `file_namer`, `folder_structurer` | Organize output into folders |
| final_qa_reporter | `agents/prompts/final_qa_reporter.md` | `validation_summarizer`, `issue_reporter` | Generate QA summary report |

---

## Hardcoded Skill Definitions

### Truncation Detection & Fixing Skills

```yaml
sentence_completeness_checker:
  description: "Detect incomplete sentences"
  checks:
    - ends_with_punctuation: ['.', '!', '?', ':']
    - has_subject_and_verb: true
    - no_trailing_ellipsis: true
    - no_cut_off_mid_word: true
  action_on_fail: "FLAG_FOR_COMPLETION"

fragment_detector:
  description: "Identify sentence fragments"
  patterns:
    - dependent_clause_only: "Although..., Because..., When..."
    - missing_main_verb: true
    - dangling_modifier: true
  action_on_fail: "FLAG_FOR_REPAIR"

auto_completion_fixer:
  description: "Automatically complete truncated content"
  strategies:
    - complete_sentence_grammatically: true
    - maintain_original_intent: true
    - add_concluding_thought: true
    - never_truncate_mid_thought: true
```

### Elaboration & Professional Tone Skills

```yaml
depth_analyzer:
  description: "Ensure content has sufficient depth"
  requirements:
    - min_explanation_sentences: 3
    - includes_example: true
    - connects_to_prior_knowledge: true
    - provides_context: true

professional_tone_checker:
  description: "Ensure educational professional tone"
  checks:
    - formal_vocabulary: true
    - no_slang: true
    - instructional_language: true
    - encouraging_but_not_patronizing: true

expansion_suggester:
  description: "Suggest expansions for thin content"
  triggers:
    - section_under_word_minimum: true
    - missing_examples: true
    - missing_connection_to_standards: true
```

### Timing & Pacing Skills

```yaml
word_count_analyzer:
  description: "Count words for timing estimation"
  parameters:
    target_speaking_rate_wpm: 130-150
    fifteen_minute_target: 1950-2250 words
    buffer_percentage: 10

speaking_pace_calculator:
  description: "Calculate delivery time"
  includes:
    - pause_markers: "[PAUSE]"
    - emphasis_markers: "[EMPHASIS]"
    - transition_time: 2-3 seconds per slide
```

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
│       └── ...
├── Unit_2_Commedia_dellArte/
│   └── ...
├── Unit_3_Shakespeare/
│   └── ...
└── Unit_4_Student_Directed_One_Acts/
    └── ...
```

---

## Lesson Plan Template (Admin-Friendly)

```markdown
# Lesson Plan: [Unit Name] - Day [X]

## Basic Information
| Field | Value |
|-------|-------|
| Teacher | [Name] |
| Course | Theater (Grades 9-12) |
| Date | [Date] |
| Duration | 56 minutes |
| Unit | [Unit Name] |
| Day | [X] of [Total] |

## Standards Addressed
- **RL.9-12.X**: [Standard text]
- **SL.9-12.X**: [Standard text]
- **W.9-12.X**: [Standard text]

## Learning Objectives
By the end of this lesson, students will be able to:
1. [Measurable objective using Bloom's verb]
2. [Measurable objective using Bloom's verb]
3. [Measurable objective using Bloom's verb]

## Materials Needed
- [ ] PowerPoint presentation
- [ ] Handouts (X copies)
- [ ] [Other materials]

## Lesson Procedure

### Opening (5 minutes) - Agenda & Journal
| Time | Teacher Actions | Student Actions |
|------|-----------------|-----------------|
| 0:00-0:02 | Display agenda, greet students | Enter, get journals |
| 0:02-0:05 | Circulate, prompt journaling | Write journal response |

**Journal Prompt:** [Prompt text]

### Warmup (5 minutes)
| Time | Teacher Actions | Student Actions |
|------|-----------------|-----------------|
| 0:05-0:10 | Lead warmup, model as needed | Participate actively |

**Warmup:** [Specific warmup with instructions]

### Direct Instruction (15 minutes)
| Time | Teacher Actions | Student Actions |
|------|-----------------|-----------------|
| 0:10-0:25 | Deliver lecture using PowerPoint | Take notes, respond to prompts |

**Key Points:**
1. [Point 1]
2. [Point 2]
3. [Point 3]

### Guided Practice / Activity (15 minutes)
| Time | Teacher Actions | Student Actions |
|------|-----------------|-----------------|
| 0:25-0:40 | Facilitate activity, provide feedback | Complete activity |

**Activity:** [Activity name and detailed instructions]

### Closure (10 minutes) - Reflection & Exit Ticket
| Time | Teacher Actions | Student Actions |
|------|-----------------|-----------------|
| 0:40-0:47 | Prompt reflection, circulate | Write reflection |
| 0:47-0:50 | Collect exit tickets | Complete exit ticket |

**Reflection Prompt:** [Prompt text]
**Exit Ticket Questions:**
1. [Question 1]
2. [Question 2]

## Differentiation
- **ELL Support:** [Specific accommodations]
- **Advanced:** [Extension activities]
- **Struggling:** [Scaffolding strategies]

## Assessment
- **Formative:** Exit ticket, observation during activity
- **Summative:** [Connection to unit assessment]

## Notes/Reflection (Post-Lesson)
[Space for teacher notes]
```

---

## PowerPoint Structure

### Slide Count: 12 Content + 4 Auxiliary = 16 Total

| Slide # | Type | Content | Counted |
|---------|------|---------|---------|
| 1 | Auxiliary | Agenda | No |
| 2 | Auxiliary | Warmup Instructions | No |
| 3 | Content | Title/Learning Objectives | Yes (1) |
| 4 | Content | Introduction/Hook | Yes (2) |
| 5-12 | Content | Main Content (8 slides) | Yes (3-10) |
| 13 | Content | Key Takeaways | Yes (11) |
| 14 | Content | Bridge to Activity | Yes (12) |
| 15 | Auxiliary | Activity Instructions | No |
| 16 | Auxiliary | Journal & Exit Ticket | No |

### Presenter Notes Requirements

- **Total Words:** 1,950-2,250 (15 minutes at 130-150 WPM)
- **Per Content Slide:** ~160-190 words average
- **Format:** Verbatim script (word-for-word)
- **Markers:** [PAUSE], [EMPHASIS: term], [CHECK FOR UNDERSTANDING]
- **Transitions:** Clear bridges between slides

---

## Validation Gates

### Gate 1: Post-Generation Validation
Every generated component passes through:
1. **Truncation Validator** - MUST PASS (no incomplete sentences)
2. **Structure Validator** - MUST PASS (all required elements)

### Gate 2: Quality Validation
1. **Elaboration Validator** - Score ≥ 85/100
2. **Timing Validator** - Within ±10% of target duration
3. **Coherence Validator** - Score ≥ 80/100

### Gate 3: Standards Validation
1. **Standards Coverage Validator** - All objectives have standards
2. **Pedagogy Validator** - Score ≥ 80/100

### Failure Handling
- **Truncation Failure:** Auto-fix, then re-validate
- **Elaboration Failure:** Return to generator with expansion prompt
- **Timing Failure:** Adjust content density
- **Structure Failure:** Return to generator with missing elements list

---

## Sample Inputs for Parallel Testing

### Unit 1: Greek Theater - Day 1 Sample Input

```json
{
  "unit": "Greek Theater",
  "day": 1,
  "unit_day_total": 20,
  "topic": "Introduction to Greek Theater: Origins and the Festival of Dionysus",
  "prior_knowledge": "None assumed",
  "vocabulary": ["orchestra", "theatron", "skene", "Dionysus", "dithyramb"],
  "standards": ["RL.9-10.5", "SL.9-10.1"],
  "learning_objectives": [
    "Explain the religious origins of Greek theater",
    "Identify the three main parts of a Greek theater",
    "Describe the role of the Festival of Dionysus in theater history"
  ]
}
```

### Unit 2: Commedia dell'Arte - Day 1 Sample Input

```json
{
  "unit": "Commedia dell'Arte",
  "day": 1,
  "unit_day_total": 18,
  "topic": "Introduction to Commedia dell'Arte: History and Stock Characters",
  "prior_knowledge": "Greek Theater unit completed",
  "vocabulary": ["lazzi", "stock character", "Arlecchino", "Pantalone", "scenario"],
  "standards": ["RL.9-10.3", "SL.9-10.6"],
  "learning_objectives": [
    "Explain the historical context of Commedia dell'Arte in Renaissance Italy",
    "Identify at least 5 stock characters and their defining traits",
    "Describe the improvisational nature of Commedia performances"
  ]
}
```

### Unit 3: Shakespeare - Day 1 Sample Input

```json
{
  "unit": "Shakespeare",
  "day": 1,
  "unit_day_total": 25,
  "topic": "Introduction to Shakespeare: The Man, the Myth, the Theater",
  "prior_knowledge": "Greek Theater and Commedia units completed",
  "vocabulary": ["iambic pentameter", "Globe Theatre", "groundlings", "soliloquy", "aside"],
  "standards": ["RL.11-12.4", "RL.9-10.9"],
  "learning_objectives": [
    "Describe Shakespeare's life and historical context",
    "Explain the structure and audience of the Globe Theatre",
    "Define key theatrical terms used in Shakespearean drama"
  ]
}
```

---

## Warmup Bank Categories

Connected to lesson content, NOT abstract:

1. **Physical Warmups** (connected to movement/blocking)
   - Character walks
   - Status exercises
   - Spatial awareness

2. **Vocal Warmups** (connected to text/language)
   - Articulation exercises
   - Projection practice
   - Rhythm and meter exercises

3. **Ensemble Warmups** (connected to collaboration)
   - Mirror exercises
   - Group counting
   - Focus games

4. **Character Warmups** (connected to character work)
   - Hot seating prep
   - Physicalization
   - Status games

5. **Text Warmups** (connected to script work)
   - Cold reading practice
   - Verse speaking
   - Paraphrasing exercises

---

## Activity Types (Structured, Not Abstract)

1. **Writing Exercises**
   - Character journals
   - Scene analysis worksheets
   - Playwriting prompts

2. **Essential Questions (Group)**
   - Structured discussion protocols
   - Fishbowl discussions
   - Think-pair-share

3. **Acting Exercises**
   - Blocking practice
   - Scene work
   - Monologue delivery

4. **Improv Exercises** (structured)
   - Scenario-based improvisation
   - Character improvisation
   - Yes-and exercises

5. **Annotation**
   - Script markup
   - Text analysis
   - Staging notation

6. **Interpretive Exercises**
   - Tableau creation
   - Scene reimagining
   - Cross-cultural adaptation

7. **Independent Reading**
   - Guided reading with questions
   - Annotation tasks
   - Summary writing

---

## Version History

- **v2.0** (2026-01-08): Complete overhaul for high school theater education
- **v1.0** (2026-01-08): Initial theater pipeline (adapted from NCLEX)

---

**Last Updated:** 2026-01-08
**Pipeline Owner:** Theater Education Department
