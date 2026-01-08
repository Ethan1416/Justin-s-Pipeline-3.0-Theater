# Phase 2: Orchestrator Creation - Instructions

## Context

You are continuing the NCLEX Pipeline migration from Phase 1 (Foundation) to Phase 2 (Orchestrator Creation).

**Repository:** `/home/mcdanielmjustin/MyNewProjectPipeline3.0`
**Branch:** `nclex-adaptation`
**GitHub:** `https://github.com/Ethan1416/Justin-s-Pipeline-3.0-NCLEX.git`

---

## Phase 1 Completed Items

- [x] Directory structure created
- [x] `AGENTS.md` - 50 agents defined
- [x] `config/pipeline.yaml` - Execution settings
- [x] `config/constraints.yaml` - Character/line limits (body_max_lines=8)
- [x] `config/nclex.yaml` - NCLEX brand config
- [x] `config/visuals.yaml` - All colors, fonts, layouts from legacy
- [x] 3 core schemas in `agents/schemas/`
- [x] Standards migrated to `standards/`
- [x] Python files copied to `skills/` directories
- [x] `docs/MIGRATION_PLAN.md` updated with Phase 1.5

---

## Phase 2 Task: Create 5 Orchestrators

Create these orchestrator files in `/home/mcdanielmjustin/MyNewProjectPipeline3.0/orchestrators/`:

### 1. `lecture_pipeline.md` (Master Orchestrator)
**Source:** `PIPELINE_EXECUTION_ORDER.md`
**Purpose:** Coordinates entire lecture generation from anchor to PowerPoint
**Content should include:**
- Full workflow diagram
- Step sequencing (1-12)
- Quality gate checkpoints
- Error handling procedures
- Sub-orchestrator invocation order

### 2. `preparation_pipeline.md`
**Sources:** `step1_anchor_upload.txt`, `step2_lecture_mapping.txt`, `step3_official_sorting.txt`, `step4_outline_generation.txt`, `step5_presentation_standards.txt`
**Purpose:** Handle Steps 1-5 (Preparation Phase)
**Agents to coordinate:**
- anchor_uploader
- lecture_mapper
- content_sorter
- outline_generator
- standards_loader

### 3. `blueprint_pipeline.md`
**Sources:** `step6_blueprint_generation.txt`, `step6_5_enforce_line_limit.txt`, `step7_formatting_revision.txt`, `step8_quality_assurance.txt`, `step9_visual_aid_identification.txt`, `step10_visual_integration_revision.txt`, `step11_blueprint_organization.txt`
**Purpose:** Handle Steps 6-11 per section (Blueprint Phase)
**Agents to coordinate:**
- blueprint_generator
- line_enforcer
- formatting_reviser
- quality_reviewer
- visual_identifier
- visual_integrator
- blueprint_organizer
**Quality Gates:**
- Step 8: QA score >= 90/100
- Step 9: Visual quota PASS
- Step 10: All slides have Visual: Yes/No marker

### 4. `visual_generation.md`
**Sources:** `step12_table_generation.txt`, `step12_flowchart_generation.txt`, `step12_decision_tree_generation.txt`, `step12_timeline_generation.txt`, `step12_hierarchy_diagram_generation.txt`, `step12_spectrum_generation.txt`, `step12_key_differentiators_generation.txt`
**Purpose:** Generate all 7 visual types (can run in parallel)
**Agents to coordinate:**
- table_generator + table_layout_selector
- flowchart_generator + flowchart_layout_selector
- decision_tree_generator + decision_tree_layout_selector
- timeline_generator + timeline_layout_selector
- hierarchy_generator + hierarchy_layout_selector
- spectrum_generator + spectrum_layout_selector
- key_diff_generator + key_diff_layout_selector

### 5. `powerpoint_pipeline.md`
**Sources:** `step12_powerpoint_population.txt`, `step12_powerpoint_population.py`
**Purpose:** Final PowerPoint assembly
**Agents to coordinate:**
- pptx_populator
- slide_assembler
- final_validator

---

## Orchestrator Template

Each orchestrator should follow this structure:

```markdown
# [Orchestrator Name]

## Purpose
[One-line description]

## Scope
- Steps covered: [X-Y]
- Input: [What it receives]
- Output: [What it produces]

## Prerequisites
- [Required files/data]
- [Previous steps completed]

## Agent Sequence

### Step X: [Name]
**Agent:** `agent_name`
**Input:** [Schema or file]
**Output:** [Schema or file]
**Validation:** [Checks performed]

[Repeat for each step]

## Quality Gates
- [Gate 1]: [Condition] → [Action if fail]
- [Gate 2]: [Condition] → [Action if fail]

## Error Handling
- [Error type]: [Recovery action]

## Output Files
- [File pattern]: [Description]
```

---

## Key Reference Files

Read these before creating orchestrators:

1. **Pipeline flow:** `PIPELINE_EXECUTION_ORDER.md`
2. **Agent definitions:** `AGENTS.md`
3. **Execution order:** `config/pipeline.yaml` (lines 40-73)
4. **Quality gates:** `config/pipeline.yaml` (lines 25-38)
5. **Output patterns:** `config/pipeline.yaml` (lines 99-113)
6. **Constraints:** `config/constraints.yaml`

---

## Validation Checklist

After creating each orchestrator, verify:

- [ ] All agents from `AGENTS.md` for that phase are included
- [ ] Input/output schemas are referenced
- [ ] Quality gates match `config/pipeline.yaml`
- [ ] Error handling is defined
- [ ] Output file patterns match `config/pipeline.yaml`

---

## Commands to Start

```bash
cd /home/mcdanielmjustin/MyNewProjectPipeline3.0
git checkout nclex-adaptation
# Read the source files, then create orchestrators
```

---

## After Phase 2

Phase 3 will create the 50 agent prompt files in `agents/prompts/`.

---

**Last Updated:** 2026-01-03
