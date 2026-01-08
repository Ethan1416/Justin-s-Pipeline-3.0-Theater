# Sub-Orchestrator: Visual Generation

**Version:** 1.0
**Purpose:** Handle Step 12 visual generation - Generate all graphic organizers
**Parent:** `lecture_pipeline.md`

---

## Overview

The Visual Generation orchestrator handles the creation of all graphic organizer content for slides marked with `Visual: Yes`. It routes each visual specification to the appropriate generator agent based on visual type and manages parallel execution for efficiency.

---

## Agents Managed

### Visual Generator Agents (7)

| Agent | Visual Type | Purpose | Input Schema | Output Schema |
|-------|-------------|---------|--------------|---------------|
| table_generator | TABLE | Generate comparison tables | table_input.schema.json | table_output.schema.json |
| flowchart_generator | FLOWCHART | Generate process flowcharts | flowchart_input.schema.json | flowchart_output.schema.json |
| decision_tree_generator | DECISION_TREE | Generate decision trees | dtree_input.schema.json | dtree_output.schema.json |
| timeline_generator | TIMELINE | Generate timelines | timeline_input.schema.json | timeline_output.schema.json |
| hierarchy_generator | HIERARCHY | Generate hierarchy diagrams | hierarchy_input.schema.json | hierarchy_output.schema.json |
| spectrum_generator | SPECTRUM | Generate spectrum visuals | spectrum_input.schema.json | spectrum_output.schema.json |
| key_diff_generator | KEY_DIFFERENTIATORS | Generate key differentiators | keydiff_input.schema.json | keydiff_output.schema.json |

### Layout Selector Agents (7)

| Agent | Visual Type | Purpose |
|-------|-------------|---------|
| table_layout_selector | TABLE | Select optimal table layout (A-E) |
| flowchart_layout_selector | FLOWCHART | Select optimal flowchart layout (A-E) |
| decision_tree_layout_selector | DECISION_TREE | Select optimal decision tree layout (A-E) |
| timeline_layout_selector | TIMELINE | Select optimal timeline layout (A-E) |
| hierarchy_layout_selector | HIERARCHY | Select optimal hierarchy layout (A-E) |
| spectrum_layout_selector | SPECTRUM | Select optimal spectrum layout (A-E) |
| key_diff_layout_selector | KEY_DIFFERENTIATORS | Select optimal key diff layout (A-E) |

---

## Skill Assignments

```yaml
agents:
  table_generator:
    skills:
      - skill: table_builder
        path: skills/generation/table_builder.py
        purpose: Build table structure with headers and rows
      - skill: table_cell_formatter
        path: skills/generation/table_cell_formatter.py
        purpose: Format cell content within char limits
      - skill: table_validator
        path: skills/validation/table_validator.py
        purpose: Validate table against constraints

  flowchart_generator:
    skills:
      - skill: flowchart_builder
        path: skills/generation/flowchart_builder.py
        purpose: Build flowchart step structure
      - skill: step_formatter
        path: skills/generation/step_formatter.py
        purpose: Format step headers and bodies
      - skill: flowchart_validator
        path: skills/validation/flowchart_validator.py
        purpose: Validate flowchart constraints

  decision_tree_generator:
    skills:
      - skill: dtree_builder
        path: skills/generation/dtree_builder.py
        purpose: Build decision tree node structure
      - skill: outcome_formatter
        path: skills/generation/outcome_formatter.py
        purpose: Format outcome nodes
      - skill: dtree_validator
        path: skills/validation/dtree_validator.py
        purpose: Validate tree depth and node count

  timeline_generator:
    skills:
      - skill: timeline_builder
        path: skills/generation/timeline_builder.py
        purpose: Build timeline event structure
      - skill: event_formatter
        path: skills/generation/event_formatter.py
        purpose: Format event cards
      - skill: timeline_validator
        path: skills/validation/timeline_validator.py
        purpose: Validate timeline constraints

  hierarchy_generator:
    skills:
      - skill: hierarchy_builder
        path: skills/generation/hierarchy_builder.py
        purpose: Build hierarchy node tree
      - skill: level_formatter
        path: skills/generation/level_formatter.py
        purpose: Format nodes by level
      - skill: hierarchy_validator
        path: skills/validation/hierarchy_validator.py
        purpose: Validate levels and node count

  spectrum_generator:
    skills:
      - skill: spectrum_builder
        path: skills/generation/spectrum_builder.py
        purpose: Build spectrum segments
      - skill: gradient_selector
        path: skills/generation/gradient_selector.py
        purpose: Select appropriate gradient type
      - skill: spectrum_validator
        path: skills/validation/spectrum_validator.py
        purpose: Validate segment count

  key_diff_generator:
    skills:
      - skill: keydiff_builder
        path: skills/generation/keydiff_builder.py
        purpose: Build concept comparison structure
      - skill: differentiator_formatter
        path: skills/generation/differentiator_formatter.py
        purpose: Format key differentiator emphasis
      - skill: keydiff_validator
        path: skills/validation/keydiff_validator.py
        purpose: Validate concept/feature counts

  # Layout selectors share common skills
  "*_layout_selector":
    skills:
      - skill: content_analyzer
        path: skills/generation/content_analyzer.py
        purpose: Analyze content for layout requirements
      - skill: layout_matcher
        path: skills/generation/layout_matcher.py
        purpose: Match content to optimal layout
```

---

## Execution Order

```
VISUAL GENERATION (parallel by default)
│
├── FOR EACH visual_spec in integrated_blueprints:
│   │
│   ├── 1. LAYOUT SELECTION
│   │   ├── Agent: {type}_layout_selector
│   │   ├── Input: Visual spec + content analysis
│   │   └── Output: Selected layout (A, B, C, D, or E)
│   │
│   └── 2. CONTENT GENERATION
│       ├── Agent: {type}_generator
│       ├── Input: Visual spec + selected layout
│       └── Output: Complete visual data
│
└── OUTPUT: All visual specifications with data
```

### Parallel Execution Strategy

```yaml
parallel_execution:
  enabled: true  # From config/pipeline.yaml
  max_concurrent: 7  # One per visual type

  batching:
    strategy: "by_type"
    description: |
      Group all visuals by type and process each type in parallel.
      Within a type, process sequentially to share context.

  example:
    - batch_1: [all TABLE visuals]
    - batch_2: [all FLOWCHART visuals]
    - batch_3: [all DECISION_TREE visuals]
    # ... etc, all running in parallel
```

---

## Input Schema Contract

```yaml
input:
  type: object
  required:
    - run_id
    - visual_specs
  properties:
    run_id:
      type: string
    visual_specs:
      type: array
      items:
        type: object
        required:
          - section_number
          - slide_number
          - type
          - layout
          - title
          - source_content
        properties:
          section_number:
            type: integer
          slide_number:
            type: integer
          type:
            type: string
            enum: [TABLE, FLOWCHART, DECISION_TREE, TIMELINE, HIERARCHY, SPECTRUM, KEY_DIFFERENTIATORS]
          layout:
            type: string
            enum: [A, B, C, D, E]
          title:
            type: string
            maxLength: 50
          source_content:
            type: object
            description: Slide body content to visualize
          rationale:
            type: string
```

---

## Output Schema Contract

```yaml
output:
  type: object
  required:
    - run_id
    - visuals
    - statistics
  properties:
    run_id:
      type: string
    visuals:
      type: array
      items:
        $ref: agents/schemas/visual_spec.schema.json
    statistics:
      type: object
      properties:
        total_visuals:
          type: integer
        by_type:
          type: object
          additionalProperties:
            type: integer
        generation_time_seconds:
          type: number
    errors:
      type: array
      items:
        type: object
        properties:
          section:
            type: integer
          slide:
            type: integer
          type:
            type: string
          error:
            type: string
```

---

## Visual Type Specifications

### TABLE

```yaml
table:
  reference: step12_table_generation.txt
  constraints:
    header_chars: 25
    cell_chars_per_line: 30
    cell_max_lines: 2
    columns: { min: 2, max: 6 }
    rows: { min: 2, max: 10 }

  layouts:
    A: "Standard Comparison (2-4 cols, 3-6 rows)"
    B: "Wide Comparison (2 cols, 4-8 rows)"
    C: "Category List (3 cols, 4-6 rows)"
    D: "Compact Reference (4-6 cols, 4-5 rows)"
    E: "Tall Comparison (2 cols, 6-10 rows)"

  use_cases:
    - Drug comparisons
    - Lab value references
    - Assessment findings
    - Intervention comparisons
```

### FLOWCHART

```yaml
flowchart:
  reference: step12_flowchart_generation.txt
  constraints:
    step_header_chars: 20
    step_body_chars_per_line: 25
    step_body_max_lines: 2
    max_steps: 7

  layouts:
    A: "Linear Horizontal (3-4 steps)"
    B: "Linear Vertical (4-6 steps)"
    C: "Horizontal with Substeps"
    D: "Snake/Zigzag (5-7 steps)"
    E: "Branching Linear"

  use_cases:
    - Clinical pathways
    - Nursing process steps
    - Assessment sequences
    - Procedure protocols
```

### DECISION_TREE

```yaml
decision_tree:
  reference: step12_decision_tree_generation.txt
  constraints:
    decision_header_chars: 20
    decision_body_chars_per_line: 25
    decision_body_max_lines: 2
    outcome_header_chars: 20
    outcome_body_chars_per_line: 20
    outcome_body_max_lines: 2
    path_label_chars: 12
    max_nodes: 15
    max_depth: 4

  layouts:
    A: "Three-level Binary (1-2-4)"
    B: "Two-level Binary (1-2)"
    C: "Two-level Triple (1-3)"
    D: "Three-level Asymmetric"
    E: "Three-level Extended (1-2-6)"

  use_cases:
    - Diagnostic criteria
    - Triage decisions
    - Treatment selection
    - Priority determination
```

### TIMELINE

```yaml
timeline:
  reference: step12_timeline_generation.txt
  constraints:
    event_header_chars: 20
    event_body_chars_per_line: 25
    event_body_max_lines: 2
    date_chars: 15
    max_events: 8

  layouts:
    A: "Horizontal Timeline (3-5 events)"
    B: "Vertical Timeline (4-7 events)"
    C: "Horizontal Era Blocks"
    D: "Developmental Stages"
    E: "Milestone Timeline (5-8)"

  use_cases:
    - Disease progression
    - Developmental milestones
    - Treatment phases
    - Recovery timeline
```

### HIERARCHY

```yaml
hierarchy:
  reference: step12_hierarchy_diagram_generation.txt
  constraints:
    node_header_chars: 25
    node_body_chars_per_line: 20
    node_body_max_lines: 2
    max_levels: 4
    max_nodes: 15

  layouts:
    A: "Top-Down Tree (1-2-4)"
    B: "Top-Down Tree Wide (1-3-6)"
    C: "Organizational Chart"
    D: "Inverted Pyramid"
    E: "Side-by-Side Hierarchies"

  use_cases:
    - Body system organization
    - Classification systems
    - Care team structure
    - Delegation hierarchy
```

### SPECTRUM

```yaml
spectrum:
  reference: step12_spectrum_generation.txt
  constraints:
    segment_label_chars: 20
    description_chars_per_line: 25
    description_max_lines: 2
    max_segments: 6

  layouts:
    A: "Horizontal Bar Spectrum (3-5 segments)"
    B: "Vertical Bar Spectrum (4-6 segments)"
    C: "Bipolar Spectrum with Center"
    D: "Segmented Spectrum"
    E: "Dual-Axis Spectrum"

  gradients:
    blue: "Low to high intensity"
    alert: "Green (normal) to red (critical)"
    bipolar: "Two opposite states"

  use_cases:
    - Pain scales
    - Severity levels
    - Medication dosing ranges
    - Assessment scores
```

### KEY_DIFFERENTIATORS

```yaml
key_differentiators:
  reference: step12_key_differentiators_generation.txt
  constraints:
    concept_header_chars: 25
    feature_chars_per_line: 30
    feature_max_lines: 2
    key_diff_chars_per_line: 35
    key_diff_max_lines: 3
    max_concepts: 4
    max_features: 6

  layouts:
    A: "Side-by-Side Comparison (2 concepts)"
    B: "Centered Key Differentiator"
    C: "Multiple Differentiators"
    D: "Three-Way Discrimination"
    E: "Feature Matrix (3-4 concepts)"

  use_cases:
    - Similar conditions discrimination
    - Medication comparison
    - Priority determination
    - Assessment differentiation
```

---

## Error Handling Procedures

### Type-Specific Errors

```yaml
common_errors:
  - error: CONTENT_TOO_LONG
    action: Truncate with validation, warn
  - error: LAYOUT_MISMATCH
    action: Select alternate layout
  - error: VALIDATION_FAILURE
    action: Regenerate with adjusted parameters

table_errors:
  - error: TOO_MANY_COLUMNS
    action: Split into multiple tables or use Layout D
  - error: TOO_MANY_ROWS
    action: Use Layout E or split
  - error: CELL_OVERFLOW
    action: Abbreviate, use multi-line

flowchart_errors:
  - error: TOO_MANY_STEPS
    action: Combine steps or use Layout D
  - error: STEP_CONTENT_OVERFLOW
    action: Use abbreviations

decision_tree_errors:
  - error: TOO_DEEP
    action: Flatten tree, max 4 levels
  - error: TOO_MANY_NODES
    action: Simplify branches

timeline_errors:
  - error: TOO_MANY_EVENTS
    action: Merge events or use Layout E
  - error: DATE_FORMAT_INVALID
    action: Standardize format

hierarchy_errors:
  - error: TOO_MANY_LEVELS
    action: Collapse levels
  - error: UNBALANCED_TREE
    action: Redistribute nodes

spectrum_errors:
  - error: TOO_MANY_SEGMENTS
    action: Merge adjacent segments
  - error: INVALID_GRADIENT
    action: Default to blue gradient

keydiff_errors:
  - error: TOO_MANY_CONCEPTS
    action: Use Layout E or split
  - error: NO_CLEAR_DIFFERENTIATOR
    action: Flag for manual review
```

### Recovery Protocol

```
1. ON_GENERATION_ERROR:
   a. Log error with visual spec context
   b. Attempt alternate layout
   c. If still failing, attempt simplified content
   d. If still failing, skip visual with warning

2. FALLBACK_CHAIN:
   - Try original layout with adjusted content
   - Try alternate layout
   - Try TABLE as universal fallback
   - Skip with manual review flag

3. BATCH_ERROR_HANDLING:
   - Individual visual failures don't halt batch
   - Collect all errors for summary report
   - Continue processing remaining visuals
```

---

## Output Files Generated

| Type | Output Pattern | Example |
|------|----------------|---------|
| Visual Data | `outputs/visuals/section_{num}_slide_{num}_{type}.json` | section_01_slide_05_TABLE.json |
| Generation Log | `outputs/logs/visual_generation_{run_id}.log` | visual_generation_run_20260104_143000.log |
| Error Report | `outputs/logs/visual_errors_{run_id}.json` | visual_errors_run_20260104_143000.json |

---

## Configuration References

From `config/visuals.yaml`:

```yaml
referenced_sections:
  - table
  - decision_tree
  - flowchart
  - timeline
  - hierarchy
  - spectrum
  - key_differentiators
  - reference_docs
```

From `config/constraints.yaml`:

```yaml
referenced_sections:
  - visual_limits
  - visual_elements
```

---

## Version History

- **v1.0** (2026-01-04): Initial visual generation orchestrator configuration
