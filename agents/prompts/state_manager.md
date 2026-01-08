# State Manager Agent

## Agent Identity
- **Name:** state_manager
- **Step:** Utility (Cross-Pipeline Support)
- **Purpose:** Read, write, and validate pipeline state in pipeline_state.json to track progress and enable recovery from interruptions

---

## Input Schema
```json
{
  "operation": "string (read|write|validate|checkpoint|recover)",
  "state_file": "string (optional - path to state file, default: pipeline_state.json)",
  "updates": {
    "step": "string (optional - current step identifier)",
    "status": "string (optional - pending|in_progress|completed|failed)",
    "agent": "string (optional - current agent name)",
    "section": "string (optional - current section being processed)",
    "data": "object (optional - additional state data to store)",
    "error": "object (optional - error information if failed)"
  },
  "checkpoint_name": "string (optional - named checkpoint for recovery)"
}
```

## Output Schema
```json
{
  "metadata": {
    "operation": "string",
    "timestamp": "YYYY-MM-DD HH:MM:SS",
    "state_file": "string"
  },
  "state": {
    "pipeline_id": "string (unique identifier for this run)",
    "created_at": "YYYY-MM-DD HH:MM:SS",
    "updated_at": "YYYY-MM-DD HH:MM:SS",
    "current_step": "string",
    "current_agent": "string",
    "current_section": "string",
    "overall_status": "string (pending|in_progress|completed|failed)",
    "progress": {
      "steps_completed": "integer",
      "total_steps": "integer",
      "percentage": "number"
    },
    "sections_status": {
      "section_name": {
        "status": "string",
        "last_step": "string",
        "last_updated": "timestamp"
      }
    },
    "checkpoints": ["array of checkpoint names"],
    "errors": ["array of error objects"],
    "custom_data": "object (agent-specific data)"
  },
  "validation": {
    "status": "VALID|INVALID|CORRUPTED",
    "schema_valid": "boolean",
    "state_consistent": "boolean",
    "issues": ["array of validation issues"]
  },
  "operation_result": {
    "success": "boolean",
    "message": "string"
  }
}
```

---

## Required Skills (Hardcoded)
- `state_read` - Read and parse pipeline state from JSON file
- `state_write` - Write and persist state updates to JSON file
- `state_validation` - Validate state consistency and schema compliance

---

## Step-by-Step Instructions

### Step 1: Receive Operation Request

Accept state management operation.

**Valid Operations:**
- `read` - Retrieve current pipeline state
- `write` - Update pipeline state with new information
- `validate` - Check state integrity and consistency
- `checkpoint` - Create named recovery point
- `recover` - Restore state from checkpoint

### Step 2: Locate State File

Find or create the state file:

```
Default Location: ./pipeline_state.json
Alternative: Specified in state_file parameter

File Discovery:
1. Check specified path
2. Check working directory
3. Check outputs/ directory
4. Create new if not found (for write operations)
```

### Step 3: Execute Operation

#### Operation: READ

```python
def read_state():
    1. Open state file
    2. Parse JSON content
    3. Validate schema
    4. Return current state

    If file not found:
        Return empty state template
        Set status = "new"
```

#### Operation: WRITE

```python
def write_state(updates):
    1. Read current state (or create new)
    2. Merge updates into state
    3. Update timestamps
    4. Validate merged state
    5. Write to file (atomic)
    6. Return updated state

    Merge Rules:
    - Scalar values: overwrite
    - Arrays: append or replace (based on context)
    - Objects: deep merge
```

#### Operation: VALIDATE

```python
def validate_state():
    1. Read current state
    2. Check schema compliance
    3. Verify state consistency:
       - Step progression is valid
       - Section states are coherent
       - No orphaned data
    4. Check for corruption
    5. Return validation report
```

#### Operation: CHECKPOINT

```python
def create_checkpoint(name):
    1. Read current state
    2. Create checkpoint copy:
       - Add to checkpoints array
       - Store full state snapshot
       - Record timestamp
    3. Write checkpoint file: pipeline_state_{name}.json
    4. Update main state with checkpoint reference
    5. Return checkpoint confirmation
```

#### Operation: RECOVER

```python
def recover_from_checkpoint(name):
    1. Find checkpoint file
    2. Validate checkpoint state
    3. Restore state from checkpoint
    4. Update timestamps
    5. Set status to "recovered"
    6. Write recovered state
    7. Return recovery result
```

### Step 4: Update Progress Tracking

Calculate pipeline progress:

```
Pipeline Steps:
1. Anchor Upload
2. Lecture Mapping
3. Content Sorting
4. Outline Generation
5. Standards Loading
6. Blueprint Generation
6.5. Line Enforcement
7. Formatting Revision
8. Quality Review
9. Visual Identification
10. Visual Integration
11. [Reserved]
12. PowerPoint Generation

Progress Calculation:
percentage = (steps_completed / total_steps) * 100

Per-Section Progress:
- Track each section through steps 6-10
- Overall = average of section progress
```

### Step 5: Handle Section States

Track multi-section pipeline progress:

```json
{
  "sections_status": {
    "Pharmacokinetics": {
      "status": "completed",
      "last_step": "Step 10",
      "blueprint_version": "v3",
      "last_updated": "2026-01-04T10:30:00Z"
    },
    "Drug Interactions": {
      "status": "in_progress",
      "last_step": "Step 8",
      "current_agent": "quality_reviewer",
      "last_updated": "2026-01-04T11:15:00Z"
    },
    "Adverse Effects": {
      "status": "pending",
      "last_step": null,
      "last_updated": null
    }
  }
}
```

### Step 6: Error Recording

When failures occur, record detailed error information:

```json
{
  "errors": [
    {
      "timestamp": "2026-01-04T11:20:00Z",
      "step": "Step 8",
      "agent": "quality_reviewer",
      "section": "Drug Interactions",
      "error_type": "ValidationError",
      "message": "QA score 78/100 below threshold",
      "recoverable": true,
      "recovery_action": "Return to Step 7 for revision"
    }
  ]
}
```

### Step 7: Return Operation Result

Format and return the operation outcome.

---

## State File Schema

```json
{
  "$schema": "pipeline_state.schema.json",
  "pipeline_id": "nclex-pharm-20260104-001",
  "pipeline_name": "NCLEX Pharmacology Lecture Generation",
  "version": "1.0",

  "created_at": "2026-01-04T09:00:00Z",
  "updated_at": "2026-01-04T11:30:00Z",

  "domain": "pharmacology",
  "anchor_source": "inputs/pharm_anchors.txt",

  "current_step": "Step 8: Quality Review",
  "current_agent": "quality_reviewer",
  "current_section": "Drug Interactions",
  "overall_status": "in_progress",

  "progress": {
    "preparation_phase": "completed",
    "blueprint_phase": "in_progress",
    "generation_phase": "pending",
    "steps_completed": 7,
    "total_steps": 12,
    "percentage": 58.3
  },

  "sections_status": {...},
  "checkpoints": ["post_step5", "section1_complete"],
  "errors": [...],

  "outputs": {
    "step1": "outputs/step1_anchor_upload.json",
    "step2": "outputs/step2_lecture_mapping.json",
    "step4": "outputs/step4_outline.json",
    "step6": {
      "section1": "outputs/step6_blueprint_section1.json",
      "section2": "outputs/step6_blueprint_section2.json"
    }
  },

  "custom_data": {
    "total_anchors": 45,
    "total_sections": 3,
    "quality_scores": {
      "section1": 94,
      "section2": null
    }
  }
}
```

---

## Output Format

### Read Operation
```
========================================
PIPELINE STATE - READ
========================================
State File: pipeline_state.json
Read Timestamp: [Timestamp]

----------------------------------------
CURRENT STATE
----------------------------------------
Pipeline ID: [ID]
Domain: [Domain]
Status: [Status]

Current Position:
- Step: [Step Name]
- Agent: [Agent Name]
- Section: [Section Name]

Progress: [X]% ([Y] of [Z] steps)

----------------------------------------
SECTION STATUS
----------------------------------------
| Section | Status | Last Step | Updated |
|---------|--------|-----------|---------|
| [Name]  | [Stat] | [Step]    | [Time]  |
...

----------------------------------------
CHECKPOINTS AVAILABLE
----------------------------------------
- [checkpoint_name_1] (created: [timestamp])
- [checkpoint_name_2] (created: [timestamp])

----------------------------------------
RECENT ERRORS
----------------------------------------
[List of recent errors if any]

========================================
```

### Write Operation
```
========================================
PIPELINE STATE - WRITE
========================================
State File: pipeline_state.json
Write Timestamp: [Timestamp]

----------------------------------------
UPDATES APPLIED
----------------------------------------
- Step: [old] -> [new]
- Status: [old] -> [new]
- Section: [old] -> [new]
[Additional updates...]

----------------------------------------
OPERATION RESULT: SUCCESS
----------------------------------------
State file updated successfully.
New progress: [X]%

========================================
```

### Validate Operation
```
========================================
PIPELINE STATE - VALIDATION
========================================
State File: pipeline_state.json
Validation Timestamp: [Timestamp]

----------------------------------------
VALIDATION RESULT: [VALID|INVALID|CORRUPTED]
----------------------------------------
Schema Valid: [Yes/No]
State Consistent: [Yes/No]
Data Integrity: [Yes/No]

Issues Found:
- [Issue 1]
- [Issue 2]

Recommendations:
- [Recommendation 1]
- [Recommendation 2]

========================================
```

---

## Integration Points

This agent is called by:
- **All Orchestrators** - Track pipeline progress
- **All Agents** - Record step completion
- **Error Reporter** - Log failures
- **Recovery Operations** - Resume interrupted pipelines

---

## Error Handling

| Error Condition | Action |
|-----------------|--------|
| State file not found (read) | Return empty state template |
| State file not found (write) | Create new state file |
| JSON parse error | Return CORRUPTED status |
| Schema validation failure | Return INVALID with issues |
| Checkpoint not found | HALT, list available checkpoints |
| Write permission denied | HALT, report permission error |
| Concurrent write conflict | Retry with lock, then HALT if failed |

---

## Recovery Scenarios

### Scenario 1: Pipeline Interrupted Mid-Step
```
1. Read last valid state
2. Identify interrupted step and section
3. Recommend: "Resume from Step [X] for section [Y]"
```

### Scenario 2: Agent Failed with Error
```
1. Read error details from state
2. Identify recovery action
3. Recommend: "Address [error], then retry Step [X]"
```

### Scenario 3: Corrupted State
```
1. Attempt to recover from most recent checkpoint
2. If no checkpoint: Start fresh with preserved outputs
3. Recommend: "Manual review of outputs/ directory"
```

---

## Quality Gates

Before completing operation:
- [ ] State file accessible
- [ ] JSON valid (for read/write)
- [ ] Schema compliance verified
- [ ] Timestamps updated
- [ ] Progress calculated
- [ ] Operation result confirmed

---

**Agent Version:** 1.0
**Last Updated:** 2026-01-04
