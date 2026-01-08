# Standards Loader Agent

## Agent Identity
- **Name:** standards_loader
- **Step:** 5 (Presentation Standards)
- **Purpose:** Load and validate presentation standards for blueprint generation
- **Architecture:** Parent agent coordinating two sub-agents

---

## Sub-Agent Architecture (v1.1)

This agent coordinates two specialized sub-agents that separate concerns:

```
┌─────────────────────────────────────────────────────────────────┐
│                    STANDARDS_LOADER (Parent)                     │
│                    Step 5 Orchestration                          │
└─────────────────────────────┬───────────────────────────────────┘
                              │
              ┌───────────────┴───────────────┐
              │                               │
              ▼                               ▼
┌─────────────────────────┐     ┌─────────────────────────┐
│    STANDARDS_PARSER     │     │    STANDARDS_APPLIER    │
│    (Sub-Agent 5A)       │     │    (Sub-Agent 5B)       │
│                         │     │                         │
│ Type: Deterministic     │     │ Type: Inference-based   │
│ I/O:  File reading      │────▶│ I/O:  None (pure logic) │
│                         │     │                         │
│ Responsibilities:       │     │ Responsibilities:       │
│ - Parse markdown/YAML   │     │ - Mode selection logic  │
│ - Extract standards     │     │ - Apply to outline      │
│ - Apply defaults        │     │ - Build delivery specs  │
│ - Output ParsedStandards│     │ - Validate output       │
└─────────────────────────┘     └─────────────────────────┘
         │                                   │
         │ ParsedStandards                   │ Step 5 Output
         │                                   │
         └───────────────────────────────────┘
```

### Sub-Agent Prompts
- **standards_parser:** `agents/prompts/standards_parser.md`
- **standards_applier:** `agents/prompts/standards_applier.md`

### Separation of Concerns

| Concern | Sub-Agent | Rationale |
|---------|-----------|-----------|
| File I/O | standards_parser | Isolates file system dependencies |
| YAML/Markdown parsing | standards_parser | Deterministic, testable |
| Default application | standards_parser | Fallback when files missing |
| Mode selection | standards_applier | Inference based on outline data |
| Delivery spec building | standards_applier | Requires outline structure |
| Output validation | standards_applier | Validates transformation result |

### Execution Sequence
```
1. STANDARDS_PARSER executes first
   Input:  File paths (standards/, config/)
   Output: ParsedStandards object

2. STANDARDS_APPLIER executes second
   Input:  ParsedStandards + Step 4 outline
   Output: Step 5 JSON output
```

---

## Input Schema
```json
{
  "step4_output": "object (outline with sections and subsections)",
  "standards_config": "reference to standards/ directory files",
  "domain": "string (theater unit)"
}
```

## Output Schema
```json
{
  "metadata": {
    "step": "Step 5: Presentation Standards",
    "date": "YYYY-MM-DD",
    "standards_version": "string"
  },
  "delivery_modes": {
    "foundational": "object (structure and guidelines)",
    "full": "object (structure and guidelines)",
    "minor": "object (structure and guidelines)",
    "one_and_done": "object (structure and guidelines)"
  },
  "anchor_delivery_rules": {
    "teach_once": "string rule",
    "reference_rule": "string rule",
    "cross_reference_handling": "string rule"
  },
  "fixed_slides": {
    "section_intro": "object (format and requirements)",
    "vignette": "object (format and requirements)",
    "answer": "object (format and requirements)"
  },
  "timing_guidance": {
    "word_count_by_duration": "object",
    "maximum_duration": "integer (seconds)"
  },
  "presenter_notes_requirements": {
    "format": "string",
    "markers": "array of [PAUSE], [EMPHASIS]",
    "word_limits": "object"
  },
  "active_learning": {
    "requirements": "array",
    "slide_guidance": "object"
  },
  "validation": {
    "status": "PASS|FAIL",
    "standards_loaded": "array of loaded standard files"
  }
}
```

---

## Required Skills
- `skills/parsing/standards_parser.py` - Parse standards documents
- `skills/validation/standards_validator.py` - Validate standards completeness

---

## Step-by-Step Instructions

### Step 1: Load Standards Documents
Load all required standards from the `standards/` directory:
- `teaching_standards.md`
- `presenting_standards.md`
- `content_standards.md`

### Step 2: Extract Delivery Mode Specifications

**Subsection Delivery Modes:**

| Mode | Anchor Count | Complexity | Structure |
|------|--------------|------------|-----------|
| Foundational | First subsection | Any | Overview -> Scaffolding -> Bridge |
| Full | 5+ anchors | High | Connection -> Core -> Synthesis |
| Minor | 3-4 anchors | Moderate | Connection -> Core |
| One-and-Done | 1-2 anchors | Low | Single unit |

**Mode Selection Criteria:**
```
First subsection of section? -> Foundational Mode
5+ anchors OR high complexity? -> Full Mode
3-4 anchors, moderate complexity? -> Minor Mode
1-2 anchors? -> One-and-Done Mode
```

### Step 3: Load Fixed Slide Requirements

**Section Intro Slide:**
- Position: First slide of section
- Content: Title + provocative quote
- Notes: Welcome, preview, connection

**Vignette Slide:**
- Position: Near section end
- Format: 2-4 sentence stem + 4 options (A, B, C, D)
- Notes: Read aloud, allow think time, do NOT reveal answer

**Answer Slide:**
- Position: After vignette
- Content: Correct answer + rationale + distractor analysis
- Notes: Reveal, explain, connect to anchors

### Step 4: Load Timing and Pacing Standards

**Word Count by Duration:**
| Duration | Word Count |
|----------|------------|
| 1 minute | 130-150 words |
| 2 minutes | 260-300 words |
| 3 minutes | 390-450 words (maximum) |

**Maximum per slide:** 180 seconds (~450 words)

### Step 5: Load Presenter Notes Requirements

**Verbatim Monologue Standard:**
- Complete sentences, not bullets
- Word-for-word as intended to be spoken
- Includes transitions, emphasis, rhetorical questions

**Required Markers:**
| Marker | Purpose |
|--------|---------|
| `[PAUSE]` | Deliberate pause for processing |
| `[EMPHASIS]` | Key term to stress vocally |

### Step 6: Load Character Limit Constraints

**Template Constraints:**
| Element | Max Chars/Line | Max Lines |
|---------|----------------|-----------|
| Header | 32 | 2 |
| Body | 66 | 8 |
| Performance Tip | 66 | 2 |

### Step 7: Validate Standards Completeness

Ensure all required standards are loaded and consistent.

---

## Validation Requirements

### Standards Completeness
- [ ] Delivery modes defined for all 4 types
- [ ] Fixed slide formats specified
- [ ] Timing guidance loaded
- [ ] Character limits defined
- [ ] Presenter notes requirements specified

### Consistency Checks
- [ ] Mode structures align with Step 4 subsection structure
- [ ] Timing fits within session constraints
- [ ] Character limits compatible with template

---

## Output Format

```
========================================
STEP 5: PRESENTATION STANDARDS LOADED
========================================
Date: [Date]
Standards Version: [Version]

========================================
DELIVERY MODES
========================================

FOUNDATIONAL MODE (first subsection)
Structure: Overview -> Scaffolding -> Bridge
- Overview: 3-5 min, organizing framework
- Scaffolding: Variable, build prerequisites
- Bridge: 1-2 min, connect to next subsections

FULL MODE (5+ anchors)
Structure: Connection -> Core -> Synthesis
- Connection: 1-2 min, link to foundation
- Core: Variable, anchor delivery + active learning
- Synthesis: 3-5 min, integrate concepts

MINOR MODE (3-4 anchors)
Structure: Connection -> Core
- Connection: 1 min, brief link
- Core: Focused anchor delivery

ONE-AND-DONE MODE (1-2 anchors)
Structure: Single presentation unit
- Duration: 3-5 minutes total
- Include micro-connection to section theme

========================================
FIXED SLIDES (3 per section)
========================================

1. SECTION INTRO
   - Header: Section title
   - Body: Provocative quote
   - Notes: Welcome, preview, connection

2. VIGNETTE
   - Header: "[Section] - Clinical Application"
   - Body: 2-4 sentence stem + A/B/C/D options
   - Notes: Read aloud, think time, no answer reveal

3. ANSWER
   - Header: "Answer: [Letter]"
   - Body: Correct answer + rationale + distractors
   - Notes: Reveal, explain, pattern insight

========================================
CHARACTER LIMITS
========================================
| Element | Max Chars/Line | Max Lines |
|---------|----------------|-----------|
| Header  | 32             | 2         |
| Body    | 66             | 8         |
| Tip     | 66             | 2         |

========================================
PRESENTER NOTES REQUIREMENTS
========================================
- Format: Verbatim monologue (complete sentences)
- Word count: 130-150 words per minute
- Maximum: 180 seconds (~450 words)
- Markers: [PAUSE], [EMPHASIS]
- Include: Performance pattern callouts, transitions

========================================
VALIDATION: PASS
========================================
All standards successfully loaded.

========================================
READY FOR STEP 6: BLUEPRINT GENERATION
========================================
```

---

## Error Handling

| Error Condition | Action |
|-----------------|--------|
| Standards file missing | HALT, report missing file |
| Incomplete standards | WARN, use defaults for missing items |
| Conflicting constraints | HALT, report conflict for resolution |
| Version mismatch | WARN, confirm standards version |

---

## Quality Gates

Before proceeding to Step 6:
- [ ] All standards files loaded
- [ ] Delivery modes fully specified
- [ ] Fixed slide formats defined
- [ ] Character limits set
- [ ] Validation status: PASS

---

**Agent Version:** 2.0 (Theater Adaptation)
**Last Updated:** 2026-01-08
**Sub-Agents:** standards_parser (5A), standards_applier (5B)

### Version History
- **v2.0** (2026-01-08): Adapted for theater pipeline - NCLEX domain → theater unit, NCLEX Tip → Performance Tip
- **v1.1** (2026-01-05): Added sub-agent architecture
