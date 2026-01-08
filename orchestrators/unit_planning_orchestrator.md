# Unit Planning Orchestrator

**Version:** 1.0
**Purpose:** Generate comprehensive unit plans for theater education units
**Parent:** theater_master_orchestrator.md

---

## Overview

The Unit Planning Orchestrator manages Phase 1 of the theater pipeline, generating 18-25 day unit plans with CA ELA/Literacy standards mapping, learning objectives, and day-by-day topic sequencing.

This orchestrator runs ONCE per unit before daily generation begins.

---

## Pipeline Position

```
┌─────────────────────────────────────────────────────────────────┐
│                    THEATER MASTER ORCHESTRATOR                   │
├─────────────────────────────────────────────────────────────────┤
│  ╔═══════════════════════╗                                      │
│  ║   PHASE 1: UNIT       ║  ← YOU ARE HERE                      │
│  ║   PLANNING            ║                                      │
│  ╚═══════════════════════╝                                      │
│           ↓                                                     │
│  ┌───────────────────────┐                                      │
│  │ PHASE 2: DAILY        │                                      │
│  │ GENERATION            │                                      │
│  └───────────────────────┘                                      │
│           ↓                                                     │
│  ┌───────────────────────┐                                      │
│  │ PHASE 3: VALIDATION   │                                      │
│  │ GATES                 │                                      │
│  └───────────────────────┘                                      │
│           ↓                                                     │
│  ┌───────────────────────┐                                      │
│  │ PHASE 4: ASSEMBLY     │                                      │
│  └───────────────────────┘                                      │
└─────────────────────────────────────────────────────────────────┘
```

---

## Unit Overview

| Unit | Name | Total Days | Key Themes |
|------|------|------------|------------|
| 1 | Greek Theater | 20 | Origins, Dionysus, tragedy, comedy, chorus, masks, staging |
| 2 | Commedia dell'Arte | 18 | Stock characters, lazzi, scenarios, physicality, improvisation |
| 3 | Shakespeare | 25 | Language, verse, staging, character, Elizabethan context |
| 4 | Student-Directed One Acts | 17 | Directing, blocking, ensemble, rehearsal, production |

---

## Agents Managed

### Sequential Agent Flow

```
unit_request
     │
     ▼
┌─────────────────────────┐
│    unit_planner         │  Generate unit scope and topic sequence
│    (Main Generator)     │
└─────────────────────────┘
     │
     ▼
┌─────────────────────────┐
│  standards_mapper       │  Map CA ELA/Literacy standards
│  (Enrichment)           │
└─────────────────────────┘
     │
     ▼
┌─────────────────────────┐
│ learning_objective_     │  Generate Bloom's-aligned objectives
│ generator (Enrichment)  │
└─────────────────────────┘
     │
     ▼
┌─────────────────────────┐
│  unit_scope_validator   │  Validate scope fits available days
│  (GATE - MUST PASS)     │
└─────────────────────────┘
     │
     ▼
unit_plan (complete)
```

### Agent Specifications

#### 1. unit_planner
**Purpose:** Generate the master unit plan with day-by-day topic sequence

**Input:**
```json
{
  "unit_number": 1,
  "unit_name": "Greek Theater",
  "total_days": 20,
  "performance_day": 18,
  "review_day": 19,
  "assessment_day": 20
}
```

**Output:**
```json
{
  "unit_plan": {
    "unit_number": 1,
    "unit_name": "Greek Theater",
    "total_days": 20,
    "essential_question": "How did Greek theater establish the foundations of Western dramatic tradition?",
    "unit_objectives": [
      "Analyze the origins and development of Greek theater",
      "Demonstrate understanding of Greek theatrical conventions",
      "Apply Greek theatrical techniques in performance"
    ],
    "day_sequence": [
      {
        "day": 1,
        "topic": "Introduction to Greek Theater",
        "focus": "Origins and the Festival of Dionysus",
        "type": "intro"
      },
      {
        "day": 2,
        "topic": "The Dithyramb and Chorus",
        "focus": "Evolution from religious ritual to theater",
        "type": "content"
      }
      // ... days 3-20
    ],
    "vocabulary_bank": [
      "dithyramb", "chorus", "theatron", "orchestra", "skene",
      "tragedy", "comedy", "satyr play", "protagonist", "antagonist",
      "mask", "cothornus", "chiton", "chorus leader", "strophê"
    ],
    "assessment_types": ["performance", "written", "exit_tickets"]
  }
}
```

#### 2. standards_mapper
**Purpose:** Map CA ELA/Literacy standards to unit objectives and daily topics

**Input:** `unit_plan` from unit_planner

**Output:**
```json
{
  "standards_map": {
    "unit_standards": [
      {
        "code": "RL.9-10.5",
        "full_text": "Analyze how an author's choices concerning how to structure a text, order events within it, and manipulate time create such effects as mystery, tension, or surprise.",
        "applicable_days": [3, 7, 12, 15],
        "learning_objectives": [
          "Analyze the three-part structure of Greek tragedy",
          "Explain how dramatic irony creates tension"
        ]
      },
      {
        "code": "SL.9-10.1b",
        "full_text": "Work with peers to set rules for collegial discussions and decision-making, clear goals and deadlines, and individual roles as needed.",
        "applicable_days": [4, 8, 11, 16],
        "learning_objectives": [
          "Collaborate effectively in ensemble performance",
          "Apply director's notes in group staging"
        ]
      }
    ],
    "coverage_summary": {
      "reading_literature": 4,
      "speaking_listening": 6,
      "writing": 2
    }
  }
}
```

#### 3. learning_objective_generator
**Purpose:** Generate Bloom's taxonomy-aligned objectives for each day

**Input:** `unit_plan` + `standards_map`

**Output:**
```json
{
  "daily_objectives": [
    {
      "day": 1,
      "topic": "Introduction to Greek Theater",
      "objectives": [
        {
          "text": "Identify the key characteristics of Greek theater",
          "blooms_level": "remember",
          "verb": "identify",
          "assessable": true
        },
        {
          "text": "Explain the role of the Festival of Dionysus in theater development",
          "blooms_level": "understand",
          "verb": "explain",
          "assessable": true
        }
      ],
      "standards_addressed": ["RL.9-10.9"]
    }
    // ... all days
  ]
}
```

#### 4. unit_scope_validator
**Purpose:** Validate that scope fits within available days

**Input:** Complete unit plan with standards and objectives

**Output:**
```json
{
  "validation_result": {
    "valid": true,
    "checks": [
      {
        "check": "day_count_match",
        "expected": 20,
        "actual": 20,
        "passed": true
      },
      {
        "check": "performance_day_exists",
        "day": 18,
        "passed": true
      },
      {
        "check": "assessment_day_exists",
        "day": 20,
        "passed": true
      },
      {
        "check": "standards_coverage",
        "minimum_required": 8,
        "actual": 12,
        "passed": true
      },
      {
        "check": "objectives_per_day",
        "minimum": 2,
        "maximum": 3,
        "all_days_pass": true
      },
      {
        "check": "vocabulary_distribution",
        "total_terms": 15,
        "terms_per_day_avg": 1.5,
        "passed": true
      }
    ],
    "overall_pass": true,
    "recommendations": []
  }
}
```

---

## Unit-Specific Configurations

### Unit 1: Greek Theater (20 days)

**Day Types:**
| Days | Type | Focus |
|------|------|-------|
| 1 | Intro | Course overview, Greek theater intro |
| 2-6 | Content | History, structure, tragedy |
| 7 | Review | Mid-unit review |
| 8-13 | Content | Comedy, chorus, masks |
| 14 | Workshop | Mask making/performance prep |
| 15-17 | Rehearsal | Chorus performance preparation |
| 18 | Performance | Chorus performance |
| 19 | Review | Unit review |
| 20 | Assessment | Unit test + reflection |

**Key Vocabulary (15 terms):**
- dithyramb, chorus, theatron, orchestra, skene
- tragedy, comedy, satyr play, protagonist, antagonist
- mask, cothornus, catharsis, hamartia, hubris

**Standards Focus:**
- RL.9-10.5 (text structure)
- RL.9-10.9 (source material analysis)
- SL.9-10.1b (collaboration)
- SL.9-10.4 (presentation)

### Unit 2: Commedia dell'Arte (18 days)

**Day Types:**
| Days | Type | Focus |
|------|------|-------|
| 1 | Intro | Commedia origins, Italian Renaissance |
| 2-5 | Content | Stock characters, physicality |
| 6 | Workshop | Character development |
| 7-10 | Content | Lazzi, scenarios, improvisation |
| 11 | Review | Mid-unit check |
| 12-14 | Rehearsal | Scenario development |
| 15-16 | Rehearsal | Performance preparation |
| 17 | Performance | Commedia scenarios |
| 18 | Assessment | Unit test + reflection |

**Key Vocabulary (12 terms):**
- zanni, lazzi, scenario, canovaccio
- Pantalone, Dottore, Capitano, Arlecchino
- Colombina, Brighella, Pulcinella, mask

**Standards Focus:**
- RL.9-10.3 (character analysis)
- SL.9-10.1 (collaborative discussion)
- SL.9-10.6 (formal/informal speech)

### Unit 3: Shakespeare (25 days)

**Day Types:**
| Days | Type | Focus |
|------|------|-------|
| 1-2 | Intro | Elizabethan context, Globe Theater |
| 3-8 | Content | Language, verse, iambic pentameter |
| 9 | Review | Language review |
| 10-15 | Content | Scene analysis, character study |
| 16 | Workshop | Monologue preparation |
| 17-20 | Rehearsal | Scene work |
| 21-23 | Performance | Scene performances |
| 24 | Review | Unit review |
| 25 | Assessment | Unit test + reflection |

**Key Vocabulary (20 terms):**
- iambic pentameter, blank verse, prose, soliloquy
- aside, monologue, dialogue, scene
- act, folio, quarto, groundling
- tragedy, comedy, history, romance
- Globe, tiring house, thrust stage, pit

**Standards Focus:**
- RL.9-10.4 (word meaning and impact)
- RL.9-10.5 (text structure)
- W.9-10.9 (drawing evidence from text)
- SL.9-10.1 (collaborative discussion)

### Unit 4: Student-Directed One Acts (17 days)

**Day Types:**
| Days | Type | Focus |
|------|------|-------|
| 1 | Intro | Directing overview, role of director |
| 2-4 | Content | Script analysis, casting, concept |
| 5 | Selection | Play selection, groups formed |
| 6-8 | Content | Blocking, staging, composition |
| 9-12 | Rehearsal | Table work, blocking rehearsals |
| 13 | Tech | Technical elements integration |
| 14-15 | Dress | Dress rehearsals |
| 16 | Performance | One act performances |
| 17 | Assessment | Director's reflection + peer feedback |

**Key Vocabulary (15 terms):**
- director, blocking, staging, composition
- proscenium, thrust, arena, traverse
- upstage, downstage, stage left, stage right
- action, objective, beat, tactic

**Standards Focus:**
- W.9-10.4 (clear, coherent writing)
- SL.9-10.1b (collaborative rules)
- SL.9-10.4 (presentation)
- SL.9-10.5 (strategic media use)

---

## Error Handling

### Scope Overflow
If content exceeds available days:
1. Identify lowest-priority topics
2. Combine related topics
3. Move advanced content to extension activities
4. Re-validate scope

### Standards Gap
If minimum standards not covered:
1. Identify uncovered standards
2. Map to existing days where applicable
3. Add explicit standards callouts to activities
4. Re-validate coverage

### Vocabulary Overload
If vocabulary exceeds 2 terms per day average:
1. Identify overlapping terms
2. Group related terms into single lessons
3. Move advanced vocabulary to enrichment
4. Re-validate distribution

---

## Output: Complete Unit Plan

The final output includes all components merged:

```json
{
  "unit_plan_complete": {
    "metadata": {
      "unit_number": 1,
      "unit_name": "Greek Theater",
      "total_days": 20,
      "generated_date": "2026-01-08",
      "version": "1.0"
    },
    "essential_question": "How did Greek theater establish the foundations of Western dramatic tradition?",
    "unit_objectives": [...],
    "standards_map": {...},
    "day_sequence": [
      {
        "day": 1,
        "topic": "Introduction to Greek Theater",
        "focus": "Origins and the Festival of Dionysus",
        "type": "intro",
        "objectives": [...],
        "vocabulary": ["dithyramb"],
        "standards": ["RL.9-10.9"],
        "warmup_type": "physical",
        "activity_type": "discussion"
      }
      // ... all days
    ],
    "vocabulary_bank": [...],
    "assessment_plan": {
      "formative": "Daily exit tickets",
      "summative": "Performance assessment + written test"
    },
    "validation_result": {...}
  }
}
```

---

## Integration with Daily Generation

The complete unit plan feeds into the Daily Generation Orchestrator:

```
unit_plan_complete
        │
        ▼
┌─────────────────────────────────────────────────────────────────┐
│            DAILY GENERATION ORCHESTRATOR                         │
│                                                                 │
│  For each day in day_sequence:                                  │
│    1. Extract day_input from unit_plan                          │
│    2. Generate all daily components                             │
│    3. Pass through validation gates                             │
│    4. Assemble lesson package                                   │
└─────────────────────────────────────────────────────────────────┘
```

---

## Validation Checklist

Before passing to Daily Generation:

- [ ] All days (1-N) have defined topics
- [ ] Performance days correctly positioned (not first or last week)
- [ ] Assessment day is final day of unit
- [ ] At least 8 CA ELA standards mapped
- [ ] Each day has 2-3 measurable objectives
- [ ] Vocabulary distributed (max 2 terms/day average)
- [ ] Warmup and activity types specified for each day
- [ ] Essential question is open-ended and unit-spanning
- [ ] Unit objectives use Bloom's action verbs
