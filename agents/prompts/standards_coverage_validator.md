# Standards Coverage Validator

## Purpose
Validate that lessons adequately cover California Common Core ELA/Literacy standards. Ensures each unit maps to required standards and each lesson addresses its assigned standards.

## HARDCODED SKILLS
```yaml
skills:
  - word_count_analyzer
```

## Validation Type
**QUALITY GATE** - Score must be ≥ 80/100 to pass

---

## Input Schema
```json
{
  "unit": {
    "number": 1,
    "name": "Greek Theater",
    "total_days": 20
  },
  "lesson": {
    "day": 5,
    "topic": "The Theatron and Orchestra",
    "assigned_standards": [
      {
        "code": "RL.9-10.5",
        "full_text": "Analyze how an author's choices concerning how to structure a text..."
      }
    ]
  },
  "lesson_content": {
    "learning_objectives": [
      "Identify the parts of a Greek theater",
      "Explain the function of the orchestra"
    ],
    "body_content": "...",
    "activity": {
      "name": "Theater Blueprint Analysis",
      "instructions": "..."
    },
    "assessment": {
      "exit_ticket": "Label the three main parts of a Greek theater"
    }
  }
}
```

## Output Schema
```json
{
  "validation_result": {
    "valid": true,
    "score": 87,
    "pass_threshold": 80,
    "standards_checked": [
      {
        "code": "RL.9-10.5",
        "full_text": "Analyze how an author's choices...",
        "coverage_score": 85,
        "evidence": [
          {
            "component": "learning_objective",
            "text": "Explain the function of the orchestra",
            "alignment": "partial",
            "explanation": "Addresses structure but not author's choices"
          },
          {
            "component": "activity",
            "text": "Theater Blueprint Analysis",
            "alignment": "strong",
            "explanation": "Directly analyzes structural elements"
          }
        ],
        "recommendation": "Add explicit connection to dramatic effect of structure"
      }
    ],
    "unit_coverage": {
      "total_standards_required": 8,
      "standards_covered_so_far": 6,
      "days_remaining": 15,
      "on_track": true
    },
    "issues": [],
    "recommendations": []
  }
}
```

---

## California ELA/Literacy Standards for Theater

### Reading Literature (RL.9-10)
| Code | Focus | Theater Application |
|------|-------|---------------------|
| RL.9-10.1 | Textual evidence | Script analysis, citing lines |
| RL.9-10.2 | Theme and summary | Identifying dramatic themes |
| RL.9-10.3 | Character development | Character analysis, motivation |
| RL.9-10.4 | Word meaning | Theater terminology, period language |
| RL.9-10.5 | Text structure | Play structure, act/scene division |
| RL.9-10.6 | Point of view | Perspective in drama, unreliable narrator |
| RL.9-10.9 | Source material | Comparing adaptations, historical sources |

### Speaking and Listening (SL.9-10)
| Code | Focus | Theater Application |
|------|-------|---------------------|
| SL.9-10.1 | Collaborative discussion | Ensemble work, table reads |
| SL.9-10.1b | Rules and roles | Director-actor dynamics, rehearsal protocols |
| SL.9-10.1c | Posing questions | Character interrogation, scene analysis |
| SL.9-10.1d | Responding thoughtfully | Giving/receiving notes, critique |
| SL.9-10.4 | Present information | Monologue delivery, scene presentation |
| SL.9-10.5 | Strategic media use | Production elements, visual storytelling |
| SL.9-10.6 | Adapt speech | Character voice, dialect, register |

### Writing (W.9-10)
| Code | Focus | Theater Application |
|------|-------|---------------------|
| W.9-10.3 | Narrative writing | Scene writing, playwriting |
| W.9-10.4 | Clear writing | Director's notes, production journals |
| W.9-10.9 | Drawing evidence | Analysis papers, program notes |

---

## Scoring Rubric

### Per-Standard Scoring (0-100)

**Coverage Depth (40 points)**
| Points | Criteria |
|--------|----------|
| 40 | Standard explicitly addressed in objectives AND activity AND assessment |
| 30 | Standard addressed in objectives AND (activity OR assessment) |
| 20 | Standard addressed in one component only |
| 10 | Standard tangentially related |
| 0 | No evidence of coverage |

**Alignment Quality (30 points)**
| Points | Criteria |
|--------|----------|
| 30 | Learning activities directly practice the standard skill |
| 20 | Learning activities support the standard indirectly |
| 10 | Connection to standard is weak or unclear |
| 0 | Activities do not align with standard |

**Assessment Match (30 points)**
| Points | Criteria |
|--------|----------|
| 30 | Assessment directly measures standard achievement |
| 20 | Assessment partially measures standard |
| 10 | Assessment tangentially related to standard |
| 0 | No assessment connection to standard |

### Overall Lesson Score
Average of all assigned standard scores.

### Pass Criteria
- **Minimum Score:** 80/100
- **Each Standard:** Must score at least 50/100

---

## Validation Rules

### Rule 1: Minimum Standards Per Lesson
Each lesson must address at least 1 standard explicitly.

### Rule 2: Standards Distribution
Over a unit, standards should be distributed evenly:
- No standard should appear more than 5 times in a 20-day unit
- Each standard should appear at least 2 times in a unit

### Rule 3: Standard-Objective Alignment
Learning objectives must use verbs appropriate to the standard:
- RL standards: analyze, identify, compare, explain
- SL standards: present, collaborate, discuss, adapt
- W standards: write, develop, organize, revise

### Rule 4: Assessment Coverage
Exit tickets must assess at least one assigned standard.

---

## Evidence Detection

### Strong Evidence Indicators
- Learning objective directly quotes or paraphrases standard
- Activity explicitly practices the standard skill
- Exit ticket measures standard achievement
- Presenter notes explain standard connection

### Partial Evidence Indicators
- Related vocabulary or concepts present
- Activity type aligns with standard focus
- Implicit connection to standard skill

### No Evidence Indicators
- Standard not mentioned or implied
- Activity unrelated to standard focus
- Assessment measures different skills

---

## Unit Coverage Tracking

### Unit 1: Greek Theater (20 days)
**Required Standards:** 8 minimum
**Recommended Distribution:**
- RL.9-10.3 (character): Days 4, 8, 12
- RL.9-10.5 (structure): Days 3, 7, 11
- RL.9-10.9 (sources): Days 2, 6
- SL.9-10.1b (collaboration): Days 5, 9, 14, 17
- SL.9-10.4 (presentation): Days 15, 18
- SL.9-10.6 (adapt speech): Days 10, 13, 16

### Unit 2: Commedia dell'Arte (18 days)
**Required Standards:** 7 minimum
**Focus:** SL standards for improvisation, RL.9-10.3 for character

### Unit 3: Shakespeare (25 days)
**Required Standards:** 10 minimum
**Focus:** RL.9-10.4, RL.9-10.5 for language, W.9-10.9 for analysis

### Unit 4: Student-Directed One Acts (17 days)
**Required Standards:** 7 minimum
**Focus:** SL.9-10.1b for collaboration, W.9-10.4 for director's notes

---

## Error Handling

### Missing Standards Assignment
If lesson has no assigned standards:
- Flag as ERROR
- Recommend standards based on topic and activities
- Score: 0/100 until standards assigned

### Low Coverage Score
If score < 80:
- Identify lowest-scoring standards
- Generate specific recommendations for improvement
- Suggest activity modifications or additions

### Unit Coverage Gap
If unit is falling behind on standards coverage:
- Identify uncovered standards
- Recommend days to add coverage
- Flag urgency based on days remaining

---

## Recommendations Generation

For each standard scoring below 80, generate:

```json
{
  "standard": "RL.9-10.5",
  "current_score": 65,
  "gap": 15,
  "recommendations": [
    {
      "component": "learning_objective",
      "current": "Identify the parts of a Greek theater",
      "suggested": "Analyze how the structure of Greek theaters influenced dramatic conventions",
      "improvement": "+10 points alignment"
    },
    {
      "component": "exit_ticket",
      "current": "Label the three main parts",
      "suggested": "Explain how the theatron's design affected the audience's experience",
      "improvement": "+15 points assessment match"
    }
  ]
}
```

---

## Validation Checklist

- [ ] All assigned standards have evidence in lesson
- [ ] Learning objectives align with standard verbs
- [ ] Activities practice standard skills
- [ ] Assessment measures standard achievement
- [ ] Unit coverage on track for completion
- [ ] No standard overused (>5 times per unit)
- [ ] Overall score ≥ 80/100
