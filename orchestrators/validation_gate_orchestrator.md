# Sub-Orchestrator: Validation Gate Pipeline

**Version:** 1.0
**Purpose:** Run HARDCODED validators to ensure quality before assembly
**Parent:** `theater_master_orchestrator.md`

---

## Overview

The Validation Gate Orchestrator manages the HARDCODED validation gates that ALL generated content must pass before proceeding to assembly. These validators cannot be bypassed, skipped, or have their thresholds lowered. Failed content is routed back to generation with specific fix instructions.

---

## CRITICAL: HARDCODED VALIDATORS

These validators are NON-NEGOTIABLE. The pipeline CANNOT produce output that fails any MUST PASS gate.

| Gate | Validator | Type | Pass Criteria | Bypass Allowed |
|------|-----------|------|---------------|----------------|
| 1 | truncation_validator | MUST PASS | 100% complete sentences | **NO** |
| 2 | structure_validator | MUST PASS | 100% components present | **NO** |
| 3 | elaboration_validator | QUALITY | Score ≥ 85/100 | **NO** |
| 4 | timing_validator | QUALITY | 14-16 min duration | **NO** |

---

## Agents Managed

| Agent | Gate | Purpose | Input | Output |
|-------|------|---------|-------|--------|
| truncation_validator | 1 | Ensure no truncated content | daily_output | truncation_result |
| structure_validator | 2 | Validate all components present | daily_output | structure_result |
| elaboration_validator | 3 | Score content depth | daily_output | elaboration_result |
| timing_validator | 4 | Validate 15-min duration | presenter_notes | timing_result |

---

## Execution Flow

```
VALIDATION GATE PIPELINE
========================

INPUT: daily_output.json (from daily_generation_orchestrator)
OUTPUT: validated_output.json OR rejection with fix instructions

┌─────────────────────────────────────────────────────────────────┐
│               GATE 1: TRUNCATION VALIDATOR                      │
│               ════════════════════════════                      │
│               TYPE: MUST PASS (NO BYPASS)                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Agent: truncation_validator                                    │
│  Skill: sentence_completeness_checker, fragment_detector        │
│                                                                 │
│  CHECKS PERFORMED:                                              │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │ □ Every sentence ends with terminal punctuation (. ! ? :) │ │
│  │ □ No trailing ellipsis (...)                              │ │
│  │ □ No mid-word cuts                                        │ │
│  │ □ No incomplete thoughts                                  │ │
│  │ □ No orphaned phrases                                     │ │
│  │ □ All bullet points are complete sentences               │ │
│  │ □ Headers are complete phrases (not truncated)           │ │
│  └───────────────────────────────────────────────────────────┘ │
│                                                                 │
│  COMPONENTS VALIDATED:                                          │
│  • powerpoint.slides[].header                                   │
│  • powerpoint.slides[].body                                     │
│  • powerpoint.slides[].performance_tip                          │
│  • presenter_notes.slides[].notes                               │
│  • warmup.instructions                                          │
│  • activity.instructions                                        │
│  • journal_exit.journal_prompt                                  │
│  • handout.instructions (if present)                            │
│                                                                 │
│  AUTO-FIX CAPABILITY: YES                                       │
│  • Add missing terminal punctuation                             │
│  • Complete obviously truncated sentences                       │
│  • Flag ambiguous cases for regeneration                        │
│                                                                 │
│  ON FAIL:                                                       │
│  → Return to daily_generation_orchestrator                      │
│  → Include: specific locations, suggested completions           │
│  → Retry count: max 3 attempts                                  │
│                                                                 │
│  ON PASS: → Continue to Gate 2                                  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│               GATE 2: STRUCTURE VALIDATOR                       │
│               ═══════════════════════════                       │
│               TYPE: MUST PASS (NO BYPASS)                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Agent: structure_validator                                     │
│  Skill: component_checker, schema_validator                     │
│                                                                 │
│  REQUIRED COMPONENTS (ALL must be present):                     │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │ □ lesson_plan                                             │ │
│  │   □ basic_information                                     │ │
│  │   □ standards (with full text)                           │ │
│  │   □ learning_objectives (2-4)                            │ │
│  │   □ vocabulary                                           │ │
│  │   □ materials_list                                       │ │
│  │   □ procedure (teacher + student actions)                │ │
│  │   □ differentiation (ell, advanced, struggling)          │ │
│  │   □ assessment_strategy                                  │ │
│  │                                                           │ │
│  │ □ powerpoint                                              │ │
│  │   □ 16 slides total                                      │ │
│  │   □ 4 auxiliary slides (1, 2, 15, 16)                   │ │
│  │   □ 12 content slides (3-14)                            │ │
│  │   □ Each content slide has performance_tip              │ │
│  │                                                           │ │
│  │ □ presenter_notes                                         │ │
│  │   □ Notes for all 16 slides                             │ │
│  │   □ Markers present ([PAUSE], [EMPHASIS])               │ │
│  │                                                           │ │
│  │ □ warmup                                                  │ │
│  │   □ type specified                                       │ │
│  │   □ connection_to_lesson present                        │ │
│  │   □ All instruction phases present                      │ │
│  │                                                           │ │
│  │ □ activity                                                │ │
│  │   □ type specified                                       │ │
│  │   □ duration = 15                                        │ │
│  │   □ structure (setup, work, sharing)                    │ │
│  │   □ differentiation present                             │ │
│  │                                                           │ │
│  │ □ journal_exit                                            │ │
│  │   □ journal_prompt present                               │ │
│  │   □ exit_tickets (2-3)                                  │ │
│  │                                                           │ │
│  │ □ handout (if activity.requires_handout = true)          │ │
│  │                                                           │ │
│  │ □ standards linked to objectives                         │ │
│  │ □ materials_list complete                                │ │
│  └───────────────────────────────────────────────────────────┘ │
│                                                                 │
│  ON FAIL:                                                       │
│  → Return to daily_generation_orchestrator                      │
│  → Include: list of missing components                          │
│  → Include: which agent should regenerate                       │
│  → Retry count: max 3 attempts                                  │
│                                                                 │
│  ON PASS: → Continue to Gate 3                                  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│             GATE 3: ELABORATION VALIDATOR                       │
│             ═════════════════════════════                       │
│             TYPE: QUALITY (Score ≥ 85/100)                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Agent: elaboration_validator                                   │
│  Skill: depth_analyzer, example_counter, procedure_validator    │
│                                                                 │
│  SCORING RUBRIC (Total: 100 points):                           │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │                                                           │ │
│  │  DEPTH (30 points)                                        │ │
│  │  ├── Concepts explained, not just stated                 │ │
│  │  ├── "Why" and "how" provided, not just "what"          │ │
│  │  ├── Historical/theatrical context included             │ │
│  │  └── Connections to broader theater concepts            │ │
│  │                                                           │ │
│  │  EXAMPLES (20 points)                                     │ │
│  │  ├── Concrete examples for abstract concepts            │ │
│  │  ├── Unit-specific examples (Greek, Commedia, etc.)     │ │
│  │  ├── Student-relatable comparisons                      │ │
│  │  └── Visual/physical demonstrations described           │ │
│  │                                                           │ │
│  │  PROCEDURE (20 points)                                    │ │
│  │  ├── Step-by-step instructions clear                    │ │
│  │  ├── Timing included for each step                      │ │
│  │  ├── Teacher actions explicit                           │ │
│  │  └── Student expectations clear                         │ │
│  │                                                           │ │
│  │  TONE (15 points)                                         │ │
│  │  ├── Engaging, not academic/dry                         │ │
│  │  ├── Direct address ("you", "we", "let's")              │ │
│  │  ├── Enthusiasm conveyed                                │ │
│  │  └── Performance-focused language                       │ │
│  │                                                           │ │
│  │  CONNECTIONS (15 points)                                  │ │
│  │  ├── Warmup connects to lesson                          │ │
│  │  ├── Activity reinforces lecture                        │ │
│  │  ├── Exit tickets assess objectives                     │ │
│  │  └── Cross-unit connections (when applicable)           │ │
│  │                                                           │ │
│  └───────────────────────────────────────────────────────────┘ │
│                                                                 │
│  PASS THRESHOLD: ≥ 85 points                                   │
│                                                                 │
│  ON FAIL (score < 85):                                         │
│  → Return to daily_generation_orchestrator                      │
│  → Include: per-category scores                                │
│  → Include: specific areas needing enrichment                  │
│  → Include: example suggestions for improvement                │
│  → Retry count: max 3 attempts                                  │
│                                                                 │
│  ON PASS: → Continue to Gate 4                                  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│               GATE 4: TIMING VALIDATOR                          │
│               ════════════════════════                          │
│               TYPE: QUALITY (14-16 min)                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Agent: timing_validator                                        │
│  Skill: word_count_analyzer, duration_estimator                 │
│                                                                 │
│  TIMING REQUIREMENTS:                                           │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │                                                           │ │
│  │  PRESENTER NOTES (Lecture Component = 15 min target)      │ │
│  │  ├── Total words: 1,950 - 2,250                          │ │
│  │  ├── Speaking rate: 140 WPM (average)                    │ │
│  │  ├── Estimated duration: 14-16 minutes                   │ │
│  │  │                                                        │ │
│  │  │  Calculation: words / 140 WPM = duration              │ │
│  │  │  1,950 / 140 = 13.9 min → FAIL (too short)           │ │
│  │  │  2,100 / 140 = 15.0 min → PASS (target)              │ │
│  │  │  2,250 / 140 = 16.1 min → PASS (upper bound)         │ │
│  │  │                                                        │ │
│  │  └── Per-slide targets:                                  │ │
│  │      ├── Title/intro slides: 100-150 words              │ │
│  │      ├── Content slides: 160-190 words                  │ │
│  │      └── Summary slides: 150-200 words                  │ │
│  │                                                           │ │
│  │  MARKER VALIDATION                                        │ │
│  │  ├── [PAUSE]: minimum 2 per slide                       │ │
│  │  ├── [EMPHASIS: term]: minimum 1 per content slide      │ │
│  │  └── [CHECK FOR UNDERSTANDING]: minimum 3 per pres.     │ │
│  │                                                           │ │
│  │  PACING CHECK                                             │ │
│  │  ├── No single slide > 300 words                        │ │
│  │  ├── No single slide < 50 words (content)               │ │
│  │  └── Variation across slides (not robotic)              │ │
│  │                                                           │ │
│  └───────────────────────────────────────────────────────────┘ │
│                                                                 │
│  ON FAIL (too short):                                          │
│  → Return to presenter_notes_writer                            │
│  → Include: current word count, needed words                   │
│  → Include: which slides are under-elaborated                  │
│  → Instruction: "Elaborate, don't pad"                         │
│                                                                 │
│  ON FAIL (too long):                                           │
│  → Return to presenter_notes_writer                            │
│  → Include: current word count, target reduction               │
│  → Include: which slides are verbose                           │
│  → Instruction: "Condense, don't truncate"                     │
│                                                                 │
│  ON FAIL (markers missing):                                    │
│  → Auto-fix via marker_insertion skill                         │
│  → Re-validate after auto-fix                                  │
│                                                                 │
│  ON PASS: → Proceed to assembly_orchestrator                   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
                    ┌─────────────────┐
                    │  ALL GATES      │
                    │    PASSED       │
                    └────────┬────────┘
                             │
                             ▼
                    validated_output.json
                    → assembly_orchestrator
```

---

## Retry Logic

### Gate Failure Handling

```python
MAX_RETRIES = 3
RETRY_STRATEGIES = {
    'truncation': 'TARGETED_FIX',      # Fix specific truncated items
    'structure': 'COMPONENT_REGEN',     # Regenerate missing components
    'elaboration': 'ENRICHMENT_PASS',   # Add depth to weak areas
    'timing': 'ADJUSTMENT_PASS'         # Expand or condense
}

def handle_gate_failure(gate_name, failure_details, attempt):
    """Handle validation gate failure with progressive strategies."""

    if attempt >= MAX_RETRIES:
        return {
            'action': 'ESCALATE',
            'reason': f'Max retries ({MAX_RETRIES}) exceeded for {gate_name}',
            'details': failure_details
        }

    strategy = RETRY_STRATEGIES[gate_name]

    if strategy == 'TARGETED_FIX':
        # Attempt 1-2: Fix specific issues
        return {
            'action': 'FIX_SPECIFIC',
            'targets': failure_details['truncated_items'],
            'instruction': 'Complete these specific sentences'
        }

    elif strategy == 'COMPONENT_REGEN':
        # Regenerate only missing components
        return {
            'action': 'REGENERATE_COMPONENTS',
            'components': failure_details['missing_components'],
            'preserve': failure_details['valid_components']
        }

    elif strategy == 'ENRICHMENT_PASS':
        # Add elaboration to weak areas
        return {
            'action': 'ENRICH',
            'weak_areas': failure_details['low_scoring_categories'],
            'suggestions': failure_details['enrichment_suggestions']
        }

    elif strategy == 'ADJUSTMENT_PASS':
        if failure_details['issue'] == 'too_short':
            return {
                'action': 'ELABORATE',
                'target_words': failure_details['needed_words'],
                'focus_slides': failure_details['under_elaborated_slides']
            }
        else:
            return {
                'action': 'CONDENSE',
                'target_words': failure_details['excess_words'],
                'focus_slides': failure_details['verbose_slides']
            }
```

### Context Preservation

Each retry preserves:
- Original input data
- Previous generation attempt
- Specific failure reasons
- Suggested fixes
- Attempt counter
- Time elapsed

---

## Validation Result Schema

```json
{
  "$schema": "validation_result.schema.json",
  "type": "object",
  "properties": {
    "overall_status": {
      "enum": ["PASSED", "FAILED", "ESCALATED"]
    },
    "gates": {
      "type": "object",
      "properties": {
        "truncation": {
          "type": "object",
          "properties": {
            "passed": {"type": "boolean"},
            "issues_found": {"type": "integer"},
            "issues_fixed": {"type": "integer"},
            "remaining_issues": {"type": "array"}
          }
        },
        "structure": {
          "type": "object",
          "properties": {
            "passed": {"type": "boolean"},
            "components_present": {"type": "array"},
            "components_missing": {"type": "array"},
            "component_details": {"type": "object"}
          }
        },
        "elaboration": {
          "type": "object",
          "properties": {
            "passed": {"type": "boolean"},
            "score": {"type": "number", "minimum": 0, "maximum": 100},
            "threshold": {"type": "number"},
            "breakdown": {
              "type": "object",
              "properties": {
                "depth": {"type": "number"},
                "examples": {"type": "number"},
                "procedure": {"type": "number"},
                "tone": {"type": "number"},
                "connections": {"type": "number"}
              }
            },
            "suggestions": {"type": "array"}
          }
        },
        "timing": {
          "type": "object",
          "properties": {
            "passed": {"type": "boolean"},
            "total_words": {"type": "integer"},
            "estimated_minutes": {"type": "number"},
            "target_range": {"type": "string"},
            "per_slide_analysis": {"type": "array"},
            "markers": {
              "type": "object",
              "properties": {
                "pause_count": {"type": "integer"},
                "emphasis_count": {"type": "integer"},
                "check_understanding_count": {"type": "integer"}
              }
            }
          }
        }
      }
    },
    "retry_info": {
      "type": "object",
      "properties": {
        "attempt_number": {"type": "integer"},
        "max_attempts": {"type": "integer"},
        "previous_failures": {"type": "array"}
      }
    },
    "validated_output": {
      "description": "Present only if overall_status == PASSED",
      "$ref": "daily_output.schema.json"
    },
    "rejection_details": {
      "description": "Present only if overall_status == FAILED",
      "type": "object",
      "properties": {
        "failed_gate": {"type": "string"},
        "reason": {"type": "string"},
        "fix_instructions": {"type": "string"},
        "context_for_retry": {"type": "object"}
      }
    }
  }
}
```

---

## Skills Integration

### Truncation Validator Skills
| Skill | Purpose |
|-------|---------|
| sentence_completeness_checker | Verify sentences have terminal punctuation |
| fragment_detector | Identify incomplete fragments |
| auto_completer | Attempt automatic sentence completion |

### Structure Validator Skills
| Skill | Purpose |
|-------|---------|
| component_checker | Verify all required components present |
| schema_validator | Validate against JSON schemas |
| count_verifier | Check slide counts, exit ticket counts, etc. |

### Elaboration Validator Skills
| Skill | Purpose |
|-------|---------|
| depth_analyzer | Score depth of explanation |
| example_counter | Count and evaluate examples |
| procedure_validator | Validate step-by-step clarity |
| tone_analyzer | Evaluate engagement and directness |
| connection_validator | Check cross-component coherence |

### Timing Validator Skills
| Skill | Purpose |
|-------|---------|
| word_count_analyzer | Count words precisely |
| duration_estimator | Convert words to minutes at 140 WPM |
| pacing_analyzer | Check per-slide word distribution |
| marker_counter | Count [PAUSE], [EMPHASIS], etc. |
| marker_insertion | Auto-insert missing markers |

---

## Error Codes

| Code | Gate | Meaning | Auto-Fix |
|------|------|---------|----------|
| T001 | Truncation | Sentence missing terminal punctuation | Yes |
| T002 | Truncation | Trailing ellipsis found | Yes |
| T003 | Truncation | Mid-word cut detected | No |
| T004 | Truncation | Incomplete thought detected | No |
| S001 | Structure | Component missing | No |
| S002 | Structure | Slide count incorrect | No |
| S003 | Structure | Required field empty | No |
| E001 | Elaboration | Depth score below threshold | No |
| E002 | Elaboration | Examples insufficient | No |
| E003 | Elaboration | Procedure unclear | No |
| E004 | Elaboration | Tone too academic | No |
| E005 | Elaboration | Poor cross-component connection | No |
| TI001 | Timing | Word count too low | No |
| TI002 | Timing | Word count too high | No |
| TI003 | Timing | Slide word count out of range | No |
| TI004 | Timing | [PAUSE] markers insufficient | Yes |
| TI005 | Timing | [EMPHASIS] markers insufficient | Yes |
| TI006 | Timing | [CHECK FOR UNDERSTANDING] insufficient | Yes |

---

## Usage Example

```python
from orchestrators.validation_gate_orchestrator import ValidationGateOrchestrator

# Load generated daily output
with open('outputs/daily/unit1_day1_generated.json') as f:
    daily_output = json.load(f)

# Create orchestrator
validator = ValidationGateOrchestrator()

# Run validation
result = validator.run(daily_output)

if result['overall_status'] == 'PASSED':
    print(f"Validation passed!")
    print(f"Elaboration score: {result['gates']['elaboration']['score']}/100")
    print(f"Timing: {result['gates']['timing']['estimated_minutes']} min")

    # Proceed to assembly
    validated_output = result['validated_output']
    assembly_result = assembly_orchestrator.run(validated_output)

elif result['overall_status'] == 'FAILED':
    print(f"Validation failed at: {result['rejection_details']['failed_gate']}")
    print(f"Reason: {result['rejection_details']['reason']}")
    print(f"Fix instructions: {result['rejection_details']['fix_instructions']}")

    # Retry with context
    retry_result = daily_generation_orchestrator.retry(
        original_input=daily_input,
        failed_output=daily_output,
        fix_context=result['rejection_details']['context_for_retry']
    )

elif result['overall_status'] == 'ESCALATED':
    print(f"Max retries exceeded - requires human review")
    save_for_review(daily_output, result)
```

---

## Performance Metrics

Track validation performance:
- Average pass rate per gate
- Average elaboration scores
- Average word counts
- Most common failure modes
- Average retries needed

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-01-08 | Initial validation gate orchestrator |

---

## Related Documents

- `theater_master_orchestrator.md` - Parent orchestrator
- `daily_generation_orchestrator.md` - Generation phase
- `config/constraints.yaml` - All thresholds and limits
- `agents/prompts/truncation_validator.md` - Gate 1 agent
- `agents/prompts/structure_validator.md` - Gate 2 agent
- `agents/prompts/elaboration_validator.md` - Gate 3 agent
- `agents/prompts/timing_validator.md` - Gate 4 agent
