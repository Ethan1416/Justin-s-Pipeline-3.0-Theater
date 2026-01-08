# AGENTS.md - Theater Lecture Generation Pipeline

## Master Instructions for Claude Code Agent System

**Version:** 1.0
**Pipeline:** Theater Lecture Generation
**Architecture:** Multi-Agent Orchestration

---

## System Overview

This pipeline uses a hierarchical agent architecture to generate theater education lectures. The system consists of:

- **Orchestrators** - Coordinate multi-step workflows
- **Agents** - Execute specific tasks with defined inputs/outputs
- **Skills** - Python utilities for parsing, generation, and validation
- **Schemas** - Input/output contracts ensuring consistency

---

## Pipeline Framework

### The 5 Phases (Process Framework)
**Purpose:** HOW to analyze content in Step 2
**Used in:** `step2_lecture_mapping.txt`
**These are sequential analysis steps:**

| Phase | Name | What It Does |
|-------|------|--------------|
| Phase 1 | Content Survey | Inventory the anchor landscape |
| Phase 2 | Cluster Discovery | Group related anchors |
| Phase 3 | Relationship Mapping | Map prerequisite dependencies |
| Phase 4 | Section Formation | Form lecture sections |
| Phase 5 | Arc Planning | Generate sequence iterations |

### Simplified Content Organization

Unlike domain-based pipelines, this theater pipeline uses a **flat topic structure**:
- Content is organized by topic (e.g., "Acting Techniques", "Stagecraft")
- No enforced domain categorization
- Flexible section organization based on content

### Reserved Terminology

| Term | Means | Context |
|------|-------|---------|
| **Phase** | Process step (1-5) | Step 2 analysis workflow |
| **Topic** | Content area | Theater subject being taught |
| **Section** | Lecture division | Output structure within a topic |

---

## Agent Architecture

```
                    ┌─────────────────────────────────┐
                    │     MASTER ORCHESTRATOR         │
                    │   orchestrators/lecture_pipeline.md   │
                    └─────────────────┬───────────────┘
                                      │
        ┌─────────────────────────────┼─────────────────────────────┐
        │                             │                             │
        ▼                             ▼                             ▼
┌───────────────┐           ┌───────────────┐           ┌───────────────┐
│  PREPARATION  │           │   BLUEPRINT   │           │  GENERATION   │
│  ORCHESTRATOR │           │  ORCHESTRATOR │           │  ORCHESTRATOR │
└───────┬───────┘           └───────┬───────┘           └───────┬───────┘
        │                           │                           │
        ▼                           ▼                           ▼
   ┌─────────┐                 ┌─────────┐                 ┌─────────┐
   │ Agents  │                 │ Agents  │                 │ Agents  │
   │ 1-5     │                 │ 6-10    │                 │ 11-12   │
   └─────────┘                 └─────────┘                 └─────────┘
```

---

## Orchestrators

### 1. Master Pipeline Orchestrator
**File:** `orchestrators/lecture_pipeline.md`
**Purpose:** Coordinates entire lecture generation from anchor to PowerPoint
**Invokes:** All sub-orchestrators in sequence

### 2. Preparation Orchestrator
**File:** `orchestrators/preparation_pipeline.md`
**Purpose:** Handles initial content processing (Steps 1-5)
**Agents:**
- `anchor_uploader` → `lecture_mapper` → `content_sorter` → `outline_generator` → `standards_loader`

### 3. Blueprint Orchestrator
**File:** `orchestrators/blueprint_pipeline.md`
**Purpose:** Per-section blueprint creation and refinement (Steps 6-10)
**Agents:**
- `blueprint_generator` → `formatting_reviser` → `quality_reviewer` → `visual_identifier` → `visual_integrator`

### 4. Visual Generation Orchestrator
**File:** `orchestrators/visual_generation.md`
**Purpose:** Generates all visual types for Step 12
**Agents:**
- `table_generator`, `flowchart_generator`, `decision_tree_generator`, `timeline_generator`, `hierarchy_generator`, `spectrum_generator`, `key_diff_generator`

### 5. PowerPoint Orchestrator
**File:** `orchestrators/powerpoint_pipeline.md`
**Purpose:** Final PowerPoint assembly
**Agents:**
- `pptx_populator`, `slide_assembler`, `quality_validator`

---

## Agents (50 Total)

### Preparation Phase Agents (5)

| Agent | File | Input Schema | Output Schema | Purpose |
|-------|------|--------------|---------------|---------|
| anchor_uploader | `agents/prompts/anchor_uploader.md` | anchor_input.schema.json | anchor_output.schema.json | Load and validate anchor documents |
| lecture_mapper | `agents/prompts/lecture_mapper.md` | mapping_input.schema.json | mapping_output.schema.json | Map anchors to lecture structure |
| content_sorter | `agents/prompts/content_sorter.md` | sorting_input.schema.json | sorting_output.schema.json | Sort content by priority/relevance |
| outline_generator | `agents/prompts/outline_generator.md` | outline_input.schema.json | outline_output.schema.json | Generate section outlines |
| standards_loader | `agents/prompts/standards_loader.md` | standards_input.schema.json | standards_output.schema.json | Load presentation standards |

### Blueprint Phase Agents (10)

| Agent | File | Input Schema | Output Schema | Purpose |
|-------|------|--------------|---------------|---------|
| blueprint_generator | `agents/prompts/blueprint_generator.md` | blueprint_input.schema.json | blueprint_output.schema.json | Generate initial slide blueprints |
| line_enforcer | `agents/prompts/line_enforcer.md` | enforce_input.schema.json | enforce_output.schema.json | Enforce line limits (Step 6.5) |
| formatting_reviser | `agents/prompts/formatting_reviser.md` | format_input.schema.json | format_output.schema.json | Apply formatting constraints |
| quality_reviewer | `agents/prompts/quality_reviewer.md` | qa_input.schema.json | qa_output.schema.json | Validate against all standards |
| visual_identifier | `agents/prompts/visual_identifier.md` | visual_id_input.schema.json | visual_id_output.schema.json | Identify visual aid opportunities |
| visual_integrator | `agents/prompts/visual_integrator.md` | integrate_input.schema.json | integrate_output.schema.json | Merge visuals into blueprints |
| blueprint_organizer | `agents/prompts/blueprint_organizer.md` | org_input.schema.json | org_output.schema.json | Organize blueprint structure |
| constraint_validator | `agents/prompts/constraint_validator.md` | constraint_input.schema.json | constraint_output.schema.json | Validate character/line limits |
| presenter_notes_writer | `agents/prompts/presenter_notes_writer.md` | notes_input.schema.json | notes_output.schema.json | Generate presenter notes |
| tip_generator | `agents/prompts/tip_generator.md` | tip_input.schema.json | tip_output.schema.json | Generate performance tips |

### Visual Generation Agents (14)

| Agent | File | Input Schema | Output Schema | Purpose |
|-------|------|--------------|---------------|---------|
| table_generator | `agents/prompts/table_generator.md` | table_input.schema.json | table_output.schema.json | Generate comparison tables |
| table_layout_selector | `agents/prompts/table_layout_selector.md` | layout_input.schema.json | layout_output.schema.json | Select optimal table layout |
| flowchart_generator | `agents/prompts/flowchart_generator.md` | flowchart_input.schema.json | flowchart_output.schema.json | Generate process flowcharts |
| flowchart_layout_selector | `agents/prompts/flowchart_layout_selector.md` | layout_input.schema.json | layout_output.schema.json | Select optimal flowchart layout |
| decision_tree_generator | `agents/prompts/decision_tree_generator.md` | dtree_input.schema.json | dtree_output.schema.json | Generate decision trees |
| decision_tree_layout_selector | `agents/prompts/decision_tree_layout_selector.md` | layout_input.schema.json | layout_output.schema.json | Select optimal decision tree layout |
| timeline_generator | `agents/prompts/timeline_generator.md` | timeline_input.schema.json | timeline_output.schema.json | Generate timelines |
| timeline_layout_selector | `agents/prompts/timeline_layout_selector.md` | layout_input.schema.json | layout_output.schema.json | Select optimal timeline layout |
| hierarchy_generator | `agents/prompts/hierarchy_generator.md` | hierarchy_input.schema.json | hierarchy_output.schema.json | Generate hierarchy diagrams |
| hierarchy_layout_selector | `agents/prompts/hierarchy_layout_selector.md` | layout_input.schema.json | layout_output.schema.json | Select optimal hierarchy layout |
| spectrum_generator | `agents/prompts/spectrum_generator.md` | spectrum_input.schema.json | spectrum_output.schema.json | Generate spectrum visuals |
| spectrum_layout_selector | `agents/prompts/spectrum_layout_selector.md` | layout_input.schema.json | layout_output.schema.json | Select optimal spectrum layout |
| key_diff_generator | `agents/prompts/key_diff_generator.md` | keydiff_input.schema.json | keydiff_output.schema.json | Generate key differentiators |
| key_diff_layout_selector | `agents/prompts/key_diff_layout_selector.md` | layout_input.schema.json | layout_output.schema.json | Select optimal key diff layout |

### PowerPoint Generation Agents (8)

| Agent | File | Input Schema | Output Schema | Purpose |
|-------|------|--------------|---------------|---------|
| pptx_populator | `agents/prompts/pptx_populator.md` | pptx_input.schema.json | pptx_output.schema.json | Populate PowerPoint templates |
| slide_assembler | `agents/prompts/slide_assembler.md` | assemble_input.schema.json | assemble_output.schema.json | Assemble final slides |
| shape_renderer | `agents/prompts/shape_renderer.md` | shape_input.schema.json | shape_output.schema.json | Render shapes/visuals |
| text_formatter | `agents/prompts/text_formatter.md` | text_input.schema.json | text_output.schema.json | Format text content |
| color_applier | `agents/prompts/color_applier.md` | color_input.schema.json | color_output.schema.json | Apply color schemes |
| position_calculator | `agents/prompts/position_calculator.md` | position_input.schema.json | position_output.schema.json | Calculate element positions |
| connector_drawer | `agents/prompts/connector_drawer.md` | connector_input.schema.json | connector_output.schema.json | Draw connectors/arrows |
| final_validator | `agents/prompts/final_validator.md` | final_input.schema.json | final_output.schema.json | Final output validation |

### Quality Assurance Agents (8)

| Agent | File | Input Schema | Output Schema | Purpose |
|-------|------|--------------|---------------|---------|
| line_limit_checker | `agents/prompts/line_limit_checker.md` | check_input.schema.json | check_output.schema.json | Verify line limits |
| char_limit_checker | `agents/prompts/char_limit_checker.md` | check_input.schema.json | check_output.schema.json | Verify character limits |
| visual_quota_checker | `agents/prompts/visual_quota_checker.md` | quota_input.schema.json | quota_output.schema.json | Verify visual minimums |
| brand_compliance_checker | `agents/prompts/brand_compliance_checker.md` | brand_input.schema.json | brand_output.schema.json | Check brand standards |
| pedagogy_checker | `agents/prompts/pedagogy_checker.md` | pedagogy_input.schema.json | pedagogy_output.schema.json | Check learning objectives |
| consistency_checker | `agents/prompts/consistency_checker.md` | consistency_input.schema.json | consistency_output.schema.json | Check terminology consistency |
| score_calculator | `agents/prompts/score_calculator.md` | score_input.schema.json | score_output.schema.json | Calculate QA scores |
| error_reporter | `agents/prompts/error_reporter.md` | error_input.schema.json | error_output.schema.json | Generate error reports |

### Utility Agents (5)

| Agent | File | Input Schema | Output Schema | Purpose |
|-------|------|--------------|---------------|---------|
| glossary_lookup | `agents/prompts/glossary_lookup.md` | glossary_input.schema.json | glossary_output.schema.json | Terminology lookup |
| timing_estimator | `agents/prompts/timing_estimator.md` | timing_input.schema.json | timing_output.schema.json | Estimate presentation timing |
| section_counter | `agents/prompts/section_counter.md` | count_input.schema.json | count_output.schema.json | Count sections/slides |
| state_manager | `agents/prompts/state_manager.md` | state_input.schema.json | state_output.schema.json | Manage pipeline state |
| changelog_writer | `agents/prompts/changelog_writer.md` | changelog_input.schema.json | changelog_output.schema.json | Write revision changelogs |

---

## Execution Rules

### 1. Sequential Dependency
Steps MUST run in order. Each agent's output is the next agent's input.

### 2. Schema Validation
Every agent input/output MUST validate against its schema before proceeding.

### 3. Quality Gates
- Step 8 QA must score ≥90/100 to proceed
- Step 9 visual quota must show PASS
- Step 10 must have Visual: Yes/No on every slide

### 4. Error Handling
- On validation failure: Return to previous agent with error context
- On schema mismatch: Halt and report
- On resource missing: Halt and report

### 5. State Persistence
Pipeline state is saved after each agent completes to `pipeline_state.json`

---

## Configuration Files

| File | Purpose |
|------|---------|
| `config/pipeline.yaml` | Pipeline settings, timeouts, defaults |
| `config/theater.yaml` | Theater-specific brand config |
| `config/visuals.yaml` | Visual type definitions |
| `config/constraints.yaml` | Character/line limits |

---

## Directory Structure

```
theater-pipeline/
├── AGENTS.md                    # This file
├── CLAUDE.md                    # Alias for Claude Code
│
├── config/
│   ├── pipeline.yaml            # Pipeline settings
│   ├── theater.yaml             # Brand config
│   └── constraints.yaml         # Limits and quotas
│
├── orchestrators/
│   ├── lecture_pipeline.md      # Master workflow
│   ├── preparation_pipeline.md  # Steps 1-5
│   ├── blueprint_pipeline.md    # Steps 6-10
│   ├── visual_generation.md     # Visual type routing
│   └── powerpoint_pipeline.md   # Final assembly
│
├── agents/
│   ├── prompts/                 # Agent instruction files (50)
│   └── schemas/                 # Input/output contracts
│
├── skills/
│   ├── parsing/                 # Template parsing utilities
│   ├── generation/              # Content generation utilities
│   ├── validation/              # Constraint validation utilities
│   └── utilities/               # Helper utilities
│
├── standards/
│   ├── teaching_standards.md
│   ├── presenting_standards.md
│   ├── content_standards.md
│   └── visual_formats/
│
├── templates/
│   ├── template_theater.pptx    # Theater template for ALL slides
│   ├── template_canvas.pptx     # Legacy canvas template (fallback)
│   └── archive/                 # Archived legacy templates
│
├── inputs/
├── outputs/
└── tests/
```

---

## Quick Start

1. **Initialize:** Load `config/pipeline.yaml`
2. **Prepare:** Run preparation orchestrator (Steps 1-5)
3. **Blueprint:** For each section, run blueprint orchestrator (Steps 6-10)
4. **Generate:** Run PowerPoint orchestrator (Step 12)
5. **Validate:** Run final QA agents

---

## Version History

- **v1.0** (2026-01-08): Initial theater pipeline - adapted from NCLEX v4.3

---

**Last Updated:** 2026-01-08
**Maintainer:** ethangrucza@gmail.com
