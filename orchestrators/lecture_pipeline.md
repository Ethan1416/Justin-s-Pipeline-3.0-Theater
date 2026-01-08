# Master Orchestrator: Lecture Pipeline

**Version:** 1.0
**Purpose:** Coordinate all sub-orchestrators for complete NCLEX lecture generation
**Role:** Master workflow controller

---

## Overview

This is the master orchestrator that coordinates the entire NCLEX lecture generation pipeline from anchor document upload through final PowerPoint generation. It invokes sub-orchestrators in sequence and manages cross-phase state.

---

## Sub-Orchestrators Managed

| Orchestrator | File | Steps | Purpose |
|--------------|------|-------|---------|
| Preparation | `preparation_pipeline.md` | 1-5 | Initial content processing |
| Blueprint | `blueprint_pipeline.md` | 6-11 | Per-section blueprint creation |
| Visual Generation | `visual_generation.md` | 12 (visuals) | Generate graphic organizers |
| PowerPoint | `powerpoint_pipeline.md` | 12 (assembly) | Final PowerPoint assembly |

---

## Execution Order

```
Phase 1: PREPARATION (Steps 1-5)
    └── Run preparation_pipeline.md
    └── Output: Outlines for all sections

Phase 2: BLUEPRINT (Steps 6-11) - Per Section Loop
    └── FOR EACH section:
        └── Run blueprint_pipeline.md
        └── Output: Integrated blueprint with visual markers

Phase 3: VISUAL GENERATION (Step 12 - Part A)
    └── FOR EACH visual marked in blueprints:
        └── Run visual_generation.md
        └── Output: Visual specifications

Phase 4: POWERPOINT (Step 12 - Part B)
    └── Run powerpoint_pipeline.md
    └── Output: Final PowerPoint files
```

---

## Input Schema Contract

```yaml
input:
  type: object
  required:
    - anchor_document
    - domain
    - run_id
  properties:
    anchor_document:
      type: string
      description: Path to anchor document (e.g., revised_standards.docx)
    domain:
      type: string
      enum: [fundamentals, pharmacology, medical_surgical, ob_maternity, pediatric, mental_health]
    run_id:
      type: string
      description: Unique identifier for this pipeline run
    options:
      type: object
      properties:
        parallel_visuals:
          type: boolean
          default: true
        strict_validation:
          type: boolean
          default: true
```

---

## Output Schema Contract

```yaml
output:
  type: object
  required:
    - run_id
    - status
    - outputs
  properties:
    run_id:
      type: string
    status:
      type: string
      enum: [success, failed, partial]
    outputs:
      type: object
      properties:
        powerpoints:
          type: array
          items:
            type: string
            description: Paths to generated PowerPoint files
        total_sections:
          type: integer
        total_slides:
          type: integer
        total_visuals:
          type: integer
    errors:
      type: array
      items:
        type: object
        properties:
          phase:
            type: string
          step:
            type: integer
          message:
            type: string
```

---

## Skill Registry Dependencies

```yaml
skills_required:
  # State management
  - skill: state_manager
    path: skills/utilities/pipeline_state_manager.py
    purpose: Persist state between orchestrator phases

  # Validation
  - skill: pipeline_validator
    path: skills/validation/pipeline_validator.py
    purpose: Cross-phase validation
```

---

## Quality Gates

### Between Phases

| Transition | Gate | Requirement | Fail Action |
|------------|------|-------------|-------------|
| Prep -> Blueprint | Section Count | 4-12 sections defined | Return to Step 4 |
| Blueprint -> Visual | QA Score | All sections score >= 90/100 | Return to Step 7 |
| Blueprint -> Visual | Visual Markers | All slides have Visual: Yes/No | Return to Step 10 |
| Visual -> PowerPoint | Visual Specs | All Visual: Yes slides have specs | Return to Visual Gen |

---

## Error Handling Procedures

### Phase Failure Protocol

```
1. ON_ERROR in any sub-orchestrator:
   a. Capture error context (step, agent, message)
   b. Log to outputs/logs/pipeline_errors.log
   c. Save current state to pipeline_state.json
   d. Evaluate retry eligibility

2. RETRY_LOGIC:
   - Max retries: 3 (from config/pipeline.yaml)
   - Retry delay: 5 seconds
   - Retry scope: Individual agent, not full phase

3. HALT_CONDITIONS (no retry):
   - Schema validation failure
   - Missing required resource
   - Quality gate failure after 3 attempts
   - Manual halt requested

4. RECOVERY:
   - Pipeline can be resumed from last saved state
   - Use: python -m skills.utilities.pipeline_state_manager --resume
```

---

## Invocation Protocol

### Starting Fresh

```bash
# Initialize new pipeline run
python -m orchestrators.lecture_pipeline \
  --anchor inputs/revised_standards.docx \
  --domain medical_surgical \
  --run-id "run_$(date +%Y%m%d_%H%M%S)"
```

### Resuming

```bash
# Resume from saved state
python -m orchestrators.lecture_pipeline \
  --resume \
  --state-file pipeline_state.json
```

---

## State Persistence

State is saved after each sub-orchestrator completes:

```json
{
  "run_id": "run_20260104_143000",
  "current_phase": "blueprint",
  "current_step": 8,
  "current_section": 3,
  "completed_phases": ["preparation"],
  "section_states": {
    "1": { "status": "complete", "qa_score": 94 },
    "2": { "status": "complete", "qa_score": 92 },
    "3": { "status": "in_progress", "current_step": 8 }
  },
  "timestamp": "2026-01-04T14:30:00Z"
}
```

---

## Configuration References

| Config File | Purpose |
|-------------|---------|
| `config/pipeline.yaml` | Pipeline settings, timeouts, paths |
| `config/nclex.yaml` | Domain definitions, brand config |
| `config/constraints.yaml` | Character/line limits, visual quotas |
| `config/visuals.yaml` | Visual type settings, layouts |

---

## Logging

All orchestrator activity is logged to:
- `outputs/logs/lecture_pipeline_{run_id}.log`
- `outputs/logs/errors_{run_id}.log` (errors only)

Log format:
```
[TIMESTAMP] [LEVEL] [ORCHESTRATOR] [STEP] Message
```

---

## Version History

- **v1.0** (2026-01-04): Initial orchestrator configuration
