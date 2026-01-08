# Sub-Orchestrator: Preparation Pipeline

**Version:** 1.2
**Purpose:** Handle Steps 1-5 - Initial content processing and outline generation
**Parent:** `lecture_pipeline.md`

---

## Overview

The Preparation Pipeline orchestrates the initial phase of lecture generation, from loading anchor documents through generating section outlines. This phase runs once per domain and produces the outline that drives all subsequent per-section processing.

---

## Agents Managed

| Agent | Step | Purpose | Input Schema | Output Schema |
|-------|------|---------|--------------|---------------|
| anchor_uploader | 1 | Load and validate anchor documents | anchor_input.schema.json | anchor_output.schema.json |
| lecture_mapper | 2 | Map anchors using 5-Phase analysis | mapping_input.schema.json | mapping_output.schema.json |
| content_sorter | 3 | Sort content into 6 NCLEX domains | sorting_input.schema.json | sorting_output.schema.json |
| outline_generator | 4 | Generate section outlines | outline_input.schema.json | outline_output.schema.json |
| standards_loader | 5 | Load presentation standards | standards_input.schema.json | standards_output.schema.json |
| ├─ standards_parser | 5A | Parse standards files (deterministic) | file paths | ParsedStandards |
| └─ standards_applier | 5B | Apply standards to outline (inference) | ParsedStandards + outline | standards_output.schema.json |

---

## Skill Assignments

```yaml
agents:
  anchor_uploader:
    skills:
      - skill: file_parser
        path: skills/utilities/file_parser.py
        purpose: Parse .docx anchor documents
      - skill: anchor_validator
        path: skills/validation/anchor_validator.py
        purpose: Validate anchor structure and content

  lecture_mapper:
    skills:
      - skill: phase_analyzer
        path: skills/generation/phase_analyzer.py
        purpose: Execute 5-Phase content analysis
      - skill: cluster_detector
        path: skills/generation/cluster_detector.py
        purpose: Identify related anchor clusters
      - skill: dependency_mapper
        path: skills/generation/dependency_mapper.py
        purpose: Map prerequisite relationships

  content_sorter:
    skills:
      - skill: domain_classifier
        path: skills/generation/domain_classifier.py
        purpose: Classify content into NCLEX domains
      - skill: priority_ranker
        path: skills/generation/priority_ranker.py
        purpose: Rank content by exam relevance

  outline_generator:
    skills:
      - skill: section_calculator
        path: skills/utilities/section_calculator.py
        purpose: Calculate section count (total_anchors / 15-20)
      - skill: outline_builder
        path: skills/generation/outline_builder.py
        purpose: Build section outline structure

  standards_loader:
    # Parent agent orchestrating sub-agents
    sub_agents:
      - agent: standards_parser
        step: 5A
        type: deterministic
        purpose: Parse standards files (markdown/YAML)
      - agent: standards_applier
        step: 5B
        type: inference
        purpose: Apply mode logic to outline
    skills:
      - skill: yaml_parser
        path: skills/utilities/yaml_parser.py
        purpose: Parse YAML config files
      - skill: standards_validator
        path: skills/validation/standards_validator.py
        purpose: Validate standards completeness
      - skill: standards_parser
        path: skills/parsing/standards_parser.py
        purpose: Parse markdown/YAML standards (deterministic)
      - skill: standards_applier
        path: skills/parsing/standards_applier.py
        purpose: Apply mode logic to outline (inference)
```

---

## Step 5 Sub-Agent Architecture

Step 5 uses a **split architecture** to separate parsing (deterministic) from application (inference):

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         STEP 5: STANDARDS LOADING                            │
│                    (Sub-Agent Architecture v1.2)                             │
└─────────────────────────────────────────────────────────────────────────────┘

                    ┌─────────────────────────────────┐
                    │     standards/                   │
                    │     ├── presenting_standards.md  │
                    │     config/                      │
                    │     └── constraints.yaml         │
                    └──────────────┬──────────────────┘
                                   │
                                   ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  SUB-AGENT 5A: STANDARDS_PARSER (Deterministic)                              │
│                                                                              │
│  Responsibilities:                                                           │
│  • Read markdown and YAML files from disk                                    │
│  • Extract structured data using regex/YAML parsing                          │
│  • Apply hardcoded defaults when files are missing                           │
│  • Output ParsedStandards object                                             │
│                                                                              │
│  Prompt: agents/prompts/standards_parser.md                                  │
│  Skill:  skills/parsing/standards_parser.py                                  │
│                                                                              │
│  KEY PRINCIPLE: No business logic or mode inference. Pure file I/O.         │
└─────────────────────────────────────────────────────────────────────────────┘
                                   │
                                   │ ParsedStandards Object
                                   │   - delivery_modes: Dict
                                   │   - fixed_slides: Dict
                                   │   - timing_guidance: TimingGuidance
                                   │   - character_limits: CharacterLimits
                                   │   - presenter_notes: PresenterNotesRequirements
                                   ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  SUB-AGENT 5B: STANDARDS_APPLIER (Inference-Based)                           │
│                                                                              │
│  Inputs:                                                                     │
│  • ParsedStandards object (from 5A)                                          │
│  • Step 4 outline (sections/subsections)                                     │
│                                                                              │
│  Responsibilities:                                                           │
│  • Determine delivery mode for each subsection                               │
│  • Build anchor delivery specifications                                      │
│  • Build active learning specifications                                      │
│  • Build presenter notes requirements                                        │
│  • Validate mode distribution                                                │
│  • Generate Step 5 output JSON                                               │
│                                                                              │
│  Prompt: agents/prompts/standards_applier.md                                 │
│  Skill:  skills/parsing/standards_applier.py                                 │
│                                                                              │
│  KEY PRINCIPLE: No file I/O. Pure inference and transformation.             │
└─────────────────────────────────────────────────────────────────────────────┘
                                   │
                                   ▼
                    ┌─────────────────────────────────┐
                    │     Step 5 Output JSON           │
                    │     (standards_output.schema)    │
                    └─────────────────────────────────┘
```

### Sub-Agent Execution Sequence

```yaml
step_5_execution:
  phase_2a:  # Part of PHASE 2: STANDARDS PARSING
    agent: standards_parser
    type: deterministic
    input:
      - standards/presenting_standards.md
      - config/constraints.yaml
    output: ParsedStandards object
    error_codes: [S5_004, S5_005, S5_006]

  phase_3:  # PHASE 3: OUTLINE TRANSFORMATION
    agent: standards_applier
    type: inference
    input:
      - ParsedStandards (from phase_2a)
      - Step 4 outline
    output: Step 5 JSON
    error_codes: [S5_007, S5_008]
```

### Benefits of Split Architecture

| Benefit | Description |
|---------|-------------|
| **Testability** | Parser can be tested with mock files; applier can be tested with mock ParsedStandards |
| **Reusability** | Parser can be reused for other purposes (e.g., standards validation tools) |
| **Maintainability** | Parsing logic changes don't affect mode selection; mode rules can evolve independently |
| **Debugging** | Easier to isolate issues: file not found vs. wrong mode assigned |
| **Performance** | Parser runs once; applier can be cached/memoized for same outline |

---

## Execution Order

```
Step 1: ANCHOR UPLOAD
    ├── Input: anchor_document path
    ├── Agent: anchor_uploader
    ├── Skills: file_parser, anchor_validator
    └── Output: Parsed anchor content

Step 2: LECTURE MAPPING (5-Phase Analysis)
    ├── Input: Step 1 output
    ├── Agent: lecture_mapper
    ├── Skills: phase_analyzer, cluster_detector, dependency_mapper
    ├── Phases:
    │   ├── Phase 1: Content Survey
    │   ├── Phase 2: Cluster Discovery
    │   ├── Phase 3: Relationship Mapping
    │   ├── Phase 4: Section Formation
    │   └── Phase 5: Arc Planning
    └── Output: Mapped anchor structure

Step 3: OFFICIAL SORTING (6-Domain Classification)
    ├── Input: Step 2 output
    ├── Agent: content_sorter
    ├── Skills: domain_classifier, priority_ranker
    ├── Domains:
    │   ├── 1. Fundamentals of Nursing
    │   ├── 2. Pharmacology
    │   ├── 3. Medical-Surgical Nursing
    │   ├── 4. OB/Maternity Nursing
    │   ├── 5. Pediatric Nursing
    │   └── 6. Mental Health Nursing
    └── Output: Domain-sorted content

Step 4: OUTLINE GENERATION
    ├── Input: Step 3 output
    ├── Agent: outline_generator
    ├── Skills: section_calculator, outline_builder
    ├── Constraints:
    │   ├── Min sections: 4
    │   ├── Max sections: 12
    │   └── Formula: total_anchors / 15-20
    └── Output: Section outlines

Step 5: STANDARDS LOADING
    ├── Input: Standards path references
    ├── Agent: standards_loader
    ├── Skills: yaml_parser, standards_validator
    ├── Files loaded:
    │   ├── standards/presenting_standards.md
    │   ├── standards/VISUAL_LAYOUT_STANDARDS.md
    │   └── config/constraints.yaml
    └── Output: Loaded standards context
```

---

## Step 5: Standards Loading - Detailed Execution Protocol

### Purpose
Transform Step 4 outline into standards-enriched output with delivery modes, fixed slides, and presenter notes requirements for each subsection.

### Execution Protocol

```
STEP 5 EXECUTION PROTOCOL
═══════════════════════════════════════════════════════════════════════════════

┌─────────────────────────────────────────────────────────────────────────────┐
│ PHASE 1: PRE-EXECUTION VALIDATION                                           │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  1.1 VERIFY INPUTS                                                          │
│      ├── [ ] Step 4 output file exists at expected path                     │
│      ├── [ ] Step 4 output is valid JSON (parseable)                        │
│      ├── [ ] Step 4 output contains required metadata (step, date, domain)  │
│      ├── [ ] Step 4 output contains sessions array with sections            │
│      └── [ ] Step 4 output contains subsections with anchor data            │
│                                                                             │
│  1.2 VERIFY STANDARDS FILES                                                 │
│      ├── [ ] standards/presenting_standards.md exists and is readable       │
│      ├── [ ] config/constraints.yaml exists and is readable                 │
│      ├── [ ] agents/schemas/standards_input.schema.json available           │
│      └── [ ] agents/schemas/standards_output.schema.json available          │
│                                                                             │
│  1.3 VERIFY DOMAIN CONTEXT                                                  │
│      ├── [ ] Domain context provided (e.g., "NCLEX Fundamentals")           │
│      ├── [ ] Exam context specified (NCLEX)                                 │
│      └── [ ] Domain type identified (clinical/theoretical)                  │
│                                                                             │
│  → IF ANY CHECK FAILS: Abort with specific error code                       │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│ PHASE 2: STANDARDS PARSING                                                  │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  2.1 INITIALIZE PARSER                                                      │
│      ├── Instantiate StandardsParser with project base_path                 │
│      ├── Configure file paths for standards documents                       │
│      └── Initialize ParsedStandards result container                        │
│                                                                             │
│  2.2 PARSE PRESENTING STANDARDS                                             │
│      ├── Load standards/presenting_standards.md                             │
│      ├── Extract delivery mode definitions (foundational/full/minor/one_and_done) │
│      ├── Extract fixed slide specifications (intro/vignette/answer)         │
│      ├── Extract timing guidance (words_per_minute, max_duration)           │
│      └── Extract presenter notes requirements (markers, word counts)        │
│                                                                             │
│  2.3 PARSE CONSTRAINTS                                                      │
│      ├── Load config/constraints.yaml                                       │
│      ├── Extract character limits (header: 32, body: 66, tip: 66)           │
│      ├── Extract visual quotas                                              │
│      └── Merge with timing guidance from presenting_standards               │
│                                                                             │
│  2.4 APPLY DEFAULTS                                                         │
│      ├── If presenting_standards.md missing → use hardcoded DELIVERY_MODES  │
│      ├── If constraints.yaml missing → use CharacterLimits defaults         │
│      └── Ensure all ParsedStandards fields populated                        │
│                                                                             │
│  → OUTPUT: ParsedStandards object with success=True                         │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│ PHASE 3: OUTLINE TRANSFORMATION                                             │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  3.1 INITIALIZE OUTPUT STRUCTURE                                            │
│      ├── Create metadata (step, date, domain, exam_context)                 │
│      ├── Initialize sessions array                                          │
│      ├── Initialize delivery_summary with mode_distribution                 │
│      ├── Add character_limits from parsed standards                         │
│      └── Initialize validation block (status: PASS, checklist, errors)      │
│                                                                             │
│  3.2 PROCESS SESSIONS                                                       │
│      FOR each session in Step 4 outline:                                    │
│          ├── Create session_output with session_number                      │
│          ├── Initialize sections array                                      │
│          └── Add break specification                                        │
│                                                                             │
│  3.3 PROCESS SECTIONS                                                       │
│      FOR each section in session:                                           │
│          ├── Build fixed_slides_spec (intro, vignette, answer)              │
│          ├── Set include_prior_connection (False for first section)         │
│          ├── Initialize subsections array                                   │
│          ├── Initialize xref_callbacks array                                │
│          └── Update fixed_slides_total counters                             │
│                                                                             │
│  3.4 PROCESS SUBSECTIONS                                                    │
│      FOR each subsection in section:                                        │
│          ├── Determine is_first_subsection flag                             │
│          ├── Call determine_delivery_mode(subsection, is_first_subsection)  │
│          │   ├── First subsection → "foundational" mode                     │
│          │   ├── 5+ anchors OR complex → "full" mode                        │
│          │   ├── 3-4 anchors → "minor" mode                                 │
│          │   └── 1-2 anchors → "one_and_done" mode                          │
│          ├── Build anchor_delivery (primary_teaching, reference_callbacks)  │
│          ├── Build active_learning_spec based on complexity                 │
│          │   ├── complex → case_application (60s)                           │
│          │   ├── moderate → exam_style_question (45s)                       │
│          │   └── simple → concept_check (30s)                               │
│          ├── Build presenter_notes_requirements                             │
│          └── Update mode_distribution counters                              │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│ PHASE 4: POST-EXECUTION VALIDATION                                          │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  4.1 VALIDATE OUTPUT STRUCTURE                                              │
│      ├── [ ] All subsections have delivery_mode object                      │
│      ├── [ ] All sections have fixed_slides object                          │
│      ├── [ ] First subsections use "foundational" mode                      │
│      ├── [ ] Misc section exceptions applied correctly                      │
│      └── [ ] Culmination section exceptions applied correctly               │
│                                                                             │
│  4.2 VALIDATE DELIVERY MODES                                                │
│      ├── [ ] All 4 modes defined (foundational, full, minor, one_and_done)  │
│      ├── [ ] Mode distribution sums to total_subsections                    │
│      └── [ ] Each mode has structure and selection_rationale                │
│                                                                             │
│  4.3 VALIDATE FIXED SLIDES                                                  │
│      ├── [ ] intro with position="first"                                    │
│      ├── [ ] vignette with position="near_end"                              │
│      ├── [ ] answer with position="after_vignette"                          │
│      └── [ ] All have content_spec and presenter_notes_spec                 │
│                                                                             │
│  4.4 SET VALIDATION STATUS                                                  │
│      ├── IF all checks pass → status = "PASS", errors = []                  │
│      └── IF any check fails → status = "FAIL", errors = [error_list]        │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│ PHASE 5: OUTPUT GENERATION                                                  │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  5.1 CALCULATE SUMMARY                                                      │
│      ├── Calculate total_fixed_slides (intro + vignette + answer + break)   │
│      ├── Count active_learning_points                                       │
│      └── Count exam_pattern_callouts                                        │
│                                                                             │
│  5.2 WRITE OUTPUT FILE                                                      │
│      ├── Format: step5_output_{domain}_{date}.json                          │
│      ├── Location: outputs/standards/                                       │
│      └── Validate against standards_output.schema.json                      │
│                                                                             │
│  5.3 SAVE STATE CHECKPOINT                                                  │
│      ├── Save checkpoint to checkpoints/step5_complete_{run_id}.json        │
│      ├── Include full output for recovery                                   │
│      └── Log completion timestamp                                           │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Skill Reference

```yaml
step_5_skills:
  primary_skill:
    name: standards_parser
    path: skills/parsing/standards_parser.py
    class: StandardsParser
    methods:
      - parse_all_standards()      # Parse presenting_standards.md and constraints.yaml
      - determine_delivery_mode()  # Select mode based on anchor count and complexity
      - build_fixed_slides_spec()  # Generate intro/vignette/answer specs
      - build_presenter_notes_requirements()  # Generate presenter notes requirements
      - build_anchor_delivery()    # Build primary_teaching and reference_callbacks
      - build_active_learning_spec()  # Build retrieval practice specs
      - apply_standards_to_outline()  # Main transformation: Step 4 → Step 5
      - _validate_output()         # Validate output structure

  supporting_skills:
    - name: yaml_parser
      path: skills/utilities/yaml_parser.py
      purpose: Parse config/constraints.yaml
    - name: standards_validator
      path: skills/validation/standards_validator.py
      purpose: Validate standards completeness
```

---

## Step 5: Error Recovery Procedures

### Standards Loading Specific Errors

```yaml
step_5_error_codes:
  S5_001:
    error: STEP4_OUTPUT_NOT_FOUND
    severity: CRITICAL
    description: Step 4 output file does not exist
    recovery:
      - action: Check expected path outputs/outlines/step4_output_{domain}_{date}.json
      - action: Verify Step 4 completed successfully
      - action: If Step 4 incomplete, re-run preparation pipeline from Step 4
      - fallback: HALT - Cannot proceed without Step 4 output

  S5_002:
    error: STEP4_OUTPUT_INVALID_JSON
    severity: CRITICAL
    description: Step 4 output is not valid JSON
    recovery:
      - action: Log parsing error with line/column number
      - action: Check for file corruption or truncation
      - action: Re-run Step 4 to regenerate output
      - fallback: HALT - Cannot parse invalid JSON

  S5_003:
    error: STEP4_OUTPUT_MISSING_FIELDS
    severity: HIGH
    description: Step 4 output missing required fields (sessions, metadata, etc.)
    recovery:
      - action: Log which fields are missing
      - action: Check schema compliance
      - action: Re-run Step 4 with schema validation enabled
      - fallback: HALT - Incomplete Step 4 output

  S5_004:
    error: PRESENTING_STANDARDS_NOT_FOUND
    severity: MEDIUM
    description: standards/presenting_standards.md not found
    recovery:
      - action: Log warning about missing file
      - action: Use hardcoded DELIVERY_MODES from StandardsParser class
      - action: Use hardcoded FIXED_SLIDES from StandardsParser class
      - fallback: CONTINUE with defaults - standards_parser.py has built-in fallbacks

  S5_005:
    error: CONSTRAINTS_YAML_NOT_FOUND
    severity: MEDIUM
    description: config/constraints.yaml not found
    recovery:
      - action: Log warning about missing file
      - action: Use CharacterLimits dataclass defaults (header: 32, body: 66, tip: 66)
      - action: Use TimingGuidance dataclass defaults (130-150 wpm, 450 max words)
      - fallback: CONTINUE with defaults - CharacterLimits has built-in fallbacks

  S5_006:
    error: CONSTRAINTS_YAML_PARSE_ERROR
    severity: MEDIUM
    description: config/constraints.yaml exists but cannot be parsed
    recovery:
      - action: Log YAML parsing error with details
      - action: Check for syntax errors in YAML file
      - action: Use CharacterLimits defaults
      - fallback: CONTINUE with defaults

  S5_007:
    error: DELIVERY_MODE_ASSIGNMENT_FAILED
    severity: HIGH
    description: Could not determine delivery mode for a subsection
    recovery:
      - action: Log subsection_id and available data
      - action: Check anchor_count and complexity fields
      - action: Default to "one_and_done" mode if data insufficient
      - fallback: CONTINUE with default mode - flag for review

  S5_008:
    error: VALIDATION_FAILED
    severity: HIGH
    description: Output validation failed (missing delivery_modes, fixed_slides, etc.)
    recovery:
      - action: Log specific validation failures
      - action: Set validation.status = "FAIL"
      - action: Populate validation.errors array
      - action: Write output file with FAIL status for debugging
      - fallback: HALT - Output does not meet quality requirements

  S5_009:
    error: OUTPUT_WRITE_FAILED
    severity: CRITICAL
    description: Could not write output file to outputs/standards/
    recovery:
      - action: Check directory exists (create if missing)
      - action: Check write permissions
      - action: Check disk space
      - action: Retry write operation
      - fallback: HALT - Cannot save output

  S5_010:
    error: CHECKPOINT_SAVE_FAILED
    severity: LOW
    description: Could not save state checkpoint
    recovery:
      - action: Log warning
      - action: Retry checkpoint save
      - action: Continue without checkpoint (output file is primary artifact)
      - fallback: CONTINUE - Checkpoint is optional recovery aid
```

### Recovery Decision Tree

```
Step 5 Error Recovery Flow
═══════════════════════════

                    ┌─────────────────┐
                    │   Error Occurs  │
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │ Identify Error  │
                    │     Code        │
                    └────────┬────────┘
                             │
        ┌────────────────────┼────────────────────┐
        │                    │                    │
   ┌────▼────┐          ┌────▼────┐          ┌────▼────┐
   │CRITICAL │          │  HIGH   │          │ MEDIUM  │
   │ S5_001  │          │ S5_003  │          │ S5_004  │
   │ S5_002  │          │ S5_007  │          │ S5_005  │
   │ S5_009  │          │ S5_008  │          │ S5_006  │
   └────┬────┘          └────┬────┘          └────┬────┘
        │                    │                    │
   ┌────▼────┐          ┌────▼────┐          ┌────▼────┐
   │  HALT   │          │  RETRY  │          │CONTINUE │
   │ Cannot  │          │   or    │          │  with   │
   │Proceed  │          │  HALT   │          │defaults │
   └─────────┘          └─────────┘          └─────────┘
```

### Retry Configuration

```yaml
step_5_retry_config:
  max_retries: 3
  retry_delay_ms: 1000
  exponential_backoff: true

  retryable_errors:
    - S5_006  # YAML parse error (might be transient file lock)
    - S5_009  # Output write failed (might be transient)
    - S5_010  # Checkpoint save failed

  non_retryable_errors:
    - S5_001  # Step 4 output not found
    - S5_002  # Invalid JSON (needs regeneration)
    - S5_003  # Missing fields (needs regeneration)
    - S5_007  # Mode assignment (use default instead)
    - S5_008  # Validation failed (logical error)
```

---

## State Checkpoint: Standards Loaded

### Checkpoint Specification

```yaml
checkpoint:
  name: STEP5_STANDARDS_LOADED
  trigger: After successful Step 5 completion
  location: checkpoints/step5_complete_{run_id}.json

  contents:
    metadata:
      checkpoint_type: "STEP5_STANDARDS_LOADED"
      timestamp: "2026-01-05T12:00:00Z"
      run_id: "{run_id}"
      domain: "{domain}"
      step: 5
      status: "COMPLETE"

    step_4_reference:
      file: "outputs/outlines/step4_output_{domain}_{date}.json"
      hash: "{sha256_hash}"

    step_5_output:
      file: "outputs/standards/step5_output_{domain}_{date}.json"
      hash: "{sha256_hash}"
      validation_status: "PASS"

    summary:
      total_sections: 5
      total_subsections: 10
      mode_distribution:
        foundational: 5
        full: 0
        minor: 4
        one_and_done: 1
      fixed_slides_total: 17
      active_learning_points: 10

    recovery_info:
      can_resume_from: "STEP6_BLUEPRINT_GENERATION"
      required_files:
        - "outputs/standards/step5_output_{domain}_{date}.json"
        - "standards/presenting_standards.md"
        - "config/constraints.yaml"
```

### Checkpoint Operations

```python
# Checkpoint save (after successful Step 5)
def save_step5_checkpoint(run_id: str, domain: str, step5_output: dict) -> bool:
    checkpoint = {
        "metadata": {
            "checkpoint_type": "STEP5_STANDARDS_LOADED",
            "timestamp": datetime.now().isoformat(),
            "run_id": run_id,
            "domain": domain,
            "step": 5,
            "status": "COMPLETE"
        },
        "step_5_output": step5_output,
        "summary": {
            "total_sections": step5_output["metadata"]["total_sections"],
            "total_subsections": step5_output["metadata"]["total_subsections"],
            "mode_distribution": step5_output["delivery_summary"]["mode_distribution"],
            "validation_status": step5_output["validation"]["status"]
        },
        "recovery_info": {
            "can_resume_from": "STEP6_BLUEPRINT_GENERATION",
            "step5_output_file": f"outputs/standards/step5_output_{domain}_{datetime.now().strftime('%Y%m%d')}.json"
        }
    }

    checkpoint_path = f"checkpoints/step5_complete_{run_id}.json"
    return write_json(checkpoint_path, checkpoint)

# Checkpoint recovery (for pipeline restart)
def recover_from_step5_checkpoint(run_id: str) -> Optional[dict]:
    checkpoint_path = f"checkpoints/step5_complete_{run_id}.json"
    if not exists(checkpoint_path):
        return None

    checkpoint = read_json(checkpoint_path)

    # Verify referenced files still exist
    step5_file = checkpoint["recovery_info"]["step5_output_file"]
    if not exists(step5_file):
        log_warning(f"Step 5 output file missing: {step5_file}")
        return None

    return checkpoint
```

### Recovery from Checkpoint

```
Pipeline Recovery Protocol (from Step 5 Checkpoint)
═══════════════════════════════════════════════════

1. DETECT CHECKPOINT
   └── Check for checkpoints/step5_complete_{run_id}.json

2. VALIDATE CHECKPOINT
   ├── Verify checkpoint file is valid JSON
   ├── Verify checkpoint.status == "COMPLETE"
   ├── Verify referenced Step 5 output file exists
   └── Verify Step 5 output passes validation

3. RESUME OPTIONS
   ├── OPTION A: Continue to Step 6 (Blueprint Generation)
   │   └── Use Step 5 output from checkpoint
   │
   ├── OPTION B: Re-run Step 5 (if standards changed)
   │   ├── Delete checkpoint
   │   └── Re-execute Step 5 with new standards
   │
   └── OPTION C: Full pipeline restart
       ├── Delete all checkpoints
       └── Start from Step 1

4. CHECKPOINT CLEANUP
   └── Delete checkpoint after successful Step 6 completion
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
      description: Path to anchor document
      example: inputs/revised_standards.docx
    domain:
      type: string
      enum: [fundamentals, pharmacology, medical_surgical, ob_maternity, pediatric, mental_health]
    run_id:
      type: string
    config:
      type: object
      properties:
        target_sections:
          type: integer
          minimum: 4
          maximum: 12
        slides_per_section:
          type: integer
          minimum: 10
          maximum: 35
```

---

## Output Schema Contract

```yaml
output:
  type: object
  required:
    - run_id
    - domain
    - sections
    - standards
  properties:
    run_id:
      type: string
    domain:
      type: string
    total_anchors:
      type: integer
    sections:
      type: array
      minItems: 4
      maxItems: 12
      items:
        type: object
        required:
          - section_number
          - section_name
          - anchor_count
          - anchor_ids
        properties:
          section_number:
            type: integer
          section_name:
            type: string
          anchor_count:
            type: integer
          anchor_ids:
            type: array
            items:
              type: string
          target_slides:
            type: integer
    standards:
      type: object
      properties:
        character_limits:
          $ref: config/constraints.yaml#/character_limits
        visual_quotas:
          $ref: config/constraints.yaml#/visual_quotas
        presentation_style:
          type: string
    output_files:
      type: object
      properties:
        step2_mapping:
          type: string
        step3_sorting:
          type: string
        step4_outline:
          type: string
```

---

## Inter-Agent Data Flow

```
anchor_uploader
    │
    ├─── anchor_content: {
    │        anchors: Array<Anchor>,
    │        metadata: {...},
    │        validation: { status: "valid" }
    │    }
    │
    ▼
lecture_mapper
    │
    ├─── mapping_result: {
    │        clusters: Array<Cluster>,
    │        dependencies: Graph<AnchorId, Dependency>,
    │        sections: Array<SectionDraft>,
    │        iterations: Array<ArcIteration>
    │    }
    │
    ▼
content_sorter
    │
    ├─── sorted_content: {
    │        domain: "medical_surgical",
    │        domain_id: 3,
    │        sorted_anchors: Array<SortedAnchor>,
    │        priority_rankings: Map<AnchorId, Priority>
    │    }
    │
    ▼
outline_generator
    │
    ├─── outline: {
    │        sections: Array<Section>,
    │        section_count: 6,
    │        total_slides_estimate: 84
    │    }
    │
    ▼
standards_loader
    │
    └─── standards_context: {
             constraints: {...},
             visual_quotas: {...},
             presentation_standards: {...}
         }
```

---

## Error Handling Procedures

### Step-Specific Errors

```yaml
step_1_errors:
  - error: FILE_NOT_FOUND
    action: Halt and report missing anchor document
  - error: INVALID_FORMAT
    action: Halt and report unsupported file format
  - error: PARSE_FAILURE
    action: Retry with alternate parser, then halt

step_2_errors:
  - error: INSUFFICIENT_ANCHORS
    action: Warn and continue with minimum viable mapping
  - error: CLUSTER_FAILURE
    action: Retry with relaxed clustering parameters
  - error: DEPENDENCY_CYCLE
    action: Break cycle and log warning

step_3_errors:
  - error: UNCLASSIFIABLE_CONTENT
    action: Assign to "fundamentals" with flag for review
  - error: DOMAIN_MISMATCH
    action: Warn if content doesn't match specified domain

step_4_errors:
  - error: TOO_FEW_SECTIONS
    action: Adjust section formula divisor
  - error: TOO_MANY_SECTIONS
    action: Merge smallest sections
  - error: IMBALANCED_SECTIONS
    action: Redistribute anchors

step_5_errors:
  - error: STANDARDS_NOT_FOUND
    action: Use default standards from config
  - error: INVALID_STANDARDS
    action: Halt and report validation failures
```

### Recovery Protocol

```
1. ON_STEP_ERROR:
   a. Log error with full context
   b. Save partial state
   c. Evaluate if step can be retried

2. RETRY_ELIGIBLE:
   - Parse failures (with alternate strategy)
   - Cluster failures (with relaxed parameters)
   - Balance failures (with adjusted formula)

3. NOT_RETRY_ELIGIBLE:
   - Missing files
   - Schema validation failures
   - Security/permission errors

4. RECOVERY:
   - Preparation phase can restart from Step 1
   - No partial recovery within phase (restart required)
```

---

## Output Files Generated

| Step | Output Pattern | Example |
|------|----------------|---------|
| 2 | `outputs/mapping/step2_output_{domain}_{date}.txt` | step2_output_medical_surgical_20260104.txt |
| 3 | `outputs/sorting/step3_output_{domain}_{date}.txt` | step3_output_medical_surgical_20260104.txt |
| 4 | `outputs/outlines/step4_output_{domain}_{date}.txt` | step4_output_medical_surgical_20260104.txt |

---

## Quality Checkpoints

### Post-Step Validation

| Step | Check | Requirement | On Fail |
|------|-------|-------------|---------|
| 1 | Anchor count | >= 20 anchors | Warn |
| 2 | Cluster coverage | 100% anchors assigned | Halt |
| 3 | Domain match | Primary domain >= 70% | Warn |
| 4 | Section count | 4-12 sections | Adjust |
| 4 | Slide estimate | 144-180 total | Adjust |
| 5 | Standards complete | All required fields | Halt |

---

## Configuration References

```yaml
configs_used:
  - file: config/pipeline.yaml
    sections:
      - execution_order.preparation
      - paths
      - output_patterns

  - file: config/nclex.yaml
    sections:
      - content.domains
      - teaching

  - file: config/constraints.yaml
    sections:
      - sections
      - slides
```

---

## Version History

- **v1.2** (2026-01-05): Added Step 5 sub-agent architecture (standards_parser + standards_applier split)
- **v1.1** (2026-01-05): Enhanced Step 5 with detailed execution protocol, error recovery procedures, and state checkpoint
- **v1.0** (2026-01-04): Initial preparation orchestrator configuration
