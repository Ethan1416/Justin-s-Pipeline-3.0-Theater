# Pedagogy Validator

## Purpose
Validate that lessons follow best practices in theater education pedagogy. Ensures appropriate use of active learning, differentiation, scaffolding, and engagement strategies suitable for high school theater students.

## HARDCODED SKILLS
```yaml
skills:
  - word_count_analyzer
  - duration_estimator
```

## Validation Type
**QUALITY GATE** - Score must be ≥ 75/100 to pass

---

## Input Schema
```json
{
  "lesson": {
    "unit": "Greek Theater",
    "day": 5,
    "topic": "The Theatron and Orchestra",
    "grade_level": "9-12"
  },
  "components": {
    "warmup": {
      "name": "Greek Chorus Walk",
      "type": "physical",
      "duration": 5,
      "student_participation": "whole_class"
    },
    "lecture": {
      "duration": 15,
      "interaction_points": 3,
      "check_understanding_count": 2,
      "visual_supports": true
    },
    "activity": {
      "name": "Theater Blueprint Analysis",
      "type": "gallery_walk",
      "duration": 15,
      "grouping": "small_groups",
      "differentiation": {
        "ell": "Sentence frames provided",
        "advanced": "Compare to modern theaters",
        "struggling": "Graphic organizer"
      }
    },
    "reflection": {
      "journal_prompt": "How might the design affect performance style?",
      "exit_ticket": "Label the three main parts",
      "duration": 10
    }
  },
  "presenter_notes": {
    "word_count": 2100,
    "pause_markers": 24,
    "emphasis_markers": 8,
    "check_understanding_markers": 3
  }
}
```

## Output Schema
```json
{
  "validation_result": {
    "valid": true,
    "score": 82,
    "pass_threshold": 75,
    "pedagogy_checks": [
      {
        "category": "active_learning",
        "score": 85,
        "indicators": ["warmup", "gallery_walk", "journal"],
        "status": "pass"
      },
      {
        "category": "differentiation",
        "score": 80,
        "indicators": ["ell_support", "advanced_extension", "struggling_support"],
        "status": "pass"
      },
      {
        "category": "engagement",
        "score": 78,
        "indicators": ["interaction_points", "varied_activities"],
        "status": "pass"
      },
      {
        "category": "scaffolding",
        "score": 85,
        "indicators": ["building_complexity", "supports_provided"],
        "status": "pass"
      }
    ],
    "strengths": [
      "Good variety of activity types",
      "Differentiation for all learner groups",
      "Appropriate pacing for 15-minute lecture"
    ],
    "areas_for_improvement": [
      "Add one more check for understanding in lecture"
    ],
    "issues": [],
    "recommendations": []
  }
}
```

---

## Pedagogy Dimensions

### 1. Active Learning (25 points)

Theater education should be experiential. Validate presence of:

**Physical Engagement (10 points)**
| Points | Criteria |
|--------|----------|
| 10 | Physical warmup + physical activity component |
| 7 | Either warmup OR activity involves movement |
| 4 | Limited physical engagement |
| 0 | No physical engagement |

**Student Participation (10 points)**
| Points | Criteria |
|--------|----------|
| 10 | Multiple participation modalities (individual, pair, group, whole class) |
| 7 | At least 2 participation modalities |
| 4 | Single participation modality |
| 0 | Passive observation only |

**Practice Opportunity (5 points)**
| Points | Criteria |
|--------|----------|
| 5 | Students practice target skills during activity |
| 3 | Limited practice opportunity |
| 0 | No practice opportunity |

### 2. Differentiation (20 points)

**ELL Support (7 points)**
| Points | Criteria |
|--------|----------|
| 7 | Visual supports + sentence frames + strategic pairing |
| 5 | Two of the above |
| 3 | One support type |
| 0 | No ELL support |

**Advanced Learner Extension (7 points)**
| Points | Criteria |
|--------|----------|
| 7 | Explicit extension task + leadership opportunity |
| 5 | Extension task provided |
| 3 | Implied extension |
| 0 | No advanced differentiation |

**Struggling Learner Support (6 points)**
| Points | Criteria |
|--------|----------|
| 6 | Scaffolds + modified requirements + peer support |
| 4 | Two of the above |
| 2 | One support type |
| 0 | No struggling learner support |

### 3. Engagement Strategies (20 points)

**Interaction Frequency (8 points)**
| Points | Criteria |
|--------|----------|
| 8 | Interaction every 3-5 minutes of lecture |
| 6 | Interaction every 5-7 minutes |
| 4 | 1-2 interactions in 15-minute lecture |
| 0 | No planned interactions |

**Variety of Activities (7 points)**
| Points | Criteria |
|--------|----------|
| 7 | 4+ distinct activity types across lesson |
| 5 | 3 distinct activity types |
| 3 | 2 activity types |
| 0 | Single activity type |

**Student Voice (5 points)**
| Points | Criteria |
|--------|----------|
| 5 | Multiple opportunities for student input/choice |
| 3 | Some student voice opportunity |
| 0 | No student voice |

### 4. Scaffolding (15 points)

**Building Complexity (8 points)**
| Points | Criteria |
|--------|----------|
| 8 | Clear progression from simple to complex |
| 6 | Some complexity progression |
| 3 | Flat difficulty level |
| 0 | No scaffolding evident |

**Support Structures (7 points)**
| Points | Criteria |
|--------|----------|
| 7 | Graphic organizers + models + guided practice |
| 5 | Two support types |
| 3 | One support type |
| 0 | No support structures |

### 5. Assessment for Learning (20 points)

**Formative Checks (10 points)**
| Points | Criteria |
|--------|----------|
| 10 | 3+ checks for understanding during lecture |
| 7 | 2 checks for understanding |
| 4 | 1 check for understanding |
| 0 | No formative assessment |

**Exit Ticket Quality (5 points)**
| Points | Criteria |
|--------|----------|
| 5 | Directly measures learning objectives |
| 3 | Partially measures objectives |
| 0 | Doesn't measure objectives |

**Reflection Depth (5 points)**
| Points | Criteria |
|--------|----------|
| 5 | Journal prompt requires synthesis/evaluation |
| 3 | Journal prompt requires analysis/application |
| 1 | Journal prompt requires recall only |
| 0 | No reflection component |

---

## Theater-Specific Pedagogy

### Warmup Best Practices
- [ ] Connects to lesson content (not random)
- [ ] Appropriate for classroom space
- [ ] Includes safety considerations if physical
- [ ] Builds ensemble/community
- [ ] 5 minutes maximum

### Lecture Best Practices
- [ ] 15 minutes maximum (high school attention span)
- [ ] Visual supports for key concepts
- [ ] Vocabulary explicitly defined with [EMPHASIS]
- [ ] [PAUSE] markers every 2-3 minutes
- [ ] [CHECK FOR UNDERSTANDING] at least twice

### Activity Best Practices
- [ ] Clear instructions (under 2 minutes to explain)
- [ ] Defined time structure (setup, work, share)
- [ ] Student movement/interaction
- [ ] Connects to learning objectives
- [ ] Includes sharing/reflection component

### Reflection Best Practices
- [ ] Journal prompt is open-ended
- [ ] Requires personal connection or synthesis
- [ ] Exit ticket is quick (2-3 minutes)
- [ ] Exit ticket is assessable

---

## Presenter Notes Pedagogy

### Pacing Indicators
| Indicator | Target | Validation |
|-----------|--------|------------|
| Words per minute | 140 WPM | Check duration estimate |
| [PAUSE] frequency | Every 2-3 min | Minimum 6 per 15-min lecture |
| [EMPHASIS] usage | Key terms | At least 1 per vocabulary word |
| [CHECK FOR UNDERSTANDING] | 2-3 per lecture | Minimum 2 |

### Language Accessibility
- [ ] Sentences average 15-20 words
- [ ] Technical terms defined before use
- [ ] Examples are relatable to high schoolers
- [ ] No jargon without explanation

### Engagement Cues
- [ ] Questions posed to students
- [ ] Invitations to participate
- [ ] Acknowledgment of student responses
- [ ] Transitions clearly marked

---

## Grade-Level Appropriateness (9-12)

### Content Complexity
- [ ] Concepts appropriate for high school
- [ ] Vocabulary at grade-level reading
- [ ] Historical context explained
- [ ] Connections to student experience

### Autonomy Level
- [ ] Some student choice in activity
- [ ] Self-directed work time
- [ ] Peer collaboration opportunities
- [ ] Independent reflection

### Social-Emotional Considerations
- [ ] Safe space for performance/risk-taking
- [ ] Inclusive language and examples
- [ ] Growth mindset language in feedback
- [ ] Community building elements

---

## Common Pedagogy Issues

### Red Flags (Automatic -10 points each)
| Issue | Impact |
|-------|--------|
| Lecture > 20 minutes | Attention loss |
| No warmup | Missed engagement |
| No differentiation | Excludes learners |
| No formative assessment | Unknown learning |
| Activity without instructions | Confusion |

### Yellow Flags (Warning, -5 points each)
| Issue | Impact |
|-------|--------|
| Weak warmup connection | Missed opportunity |
| Single activity type | Limited engagement |
| No [CHECK FOR UNDERSTANDING] | Missed feedback |
| Exit ticket too complex | Time overflow |

---

## Scoring Calculation

```
Total Score =
  Active Learning (25) +
  Differentiation (20) +
  Engagement (20) +
  Scaffolding (15) +
  Assessment for Learning (20)
  - Red Flag Deductions
  - Yellow Flag Deductions

Maximum: 100 points
Pass Threshold: 75 points
```

---

## Recommendations Generation

For scores below 75, generate pedagogical improvements:

```json
{
  "category": "engagement",
  "current_score": 60,
  "gap": 15,
  "issues": [
    "Only 1 interaction point in 15-minute lecture"
  ],
  "recommendations": [
    {
      "action": "Add [CHECK FOR UNDERSTANDING] after slide 8",
      "example": "Turn to a partner and share one thing you've learned so far",
      "improvement": "+4 points"
    },
    {
      "action": "Add think-pair-share before activity",
      "example": "What do you predict you'll discover about Greek theaters?",
      "improvement": "+4 points"
    }
  ]
}
```

---

## Validation Checklist

- [ ] Active learning: Physical + participation + practice
- [ ] Differentiation: ELL + advanced + struggling supports
- [ ] Engagement: Regular interaction + variety + student voice
- [ ] Scaffolding: Progressive complexity + support structures
- [ ] Assessment: Formative checks + exit ticket + reflection
- [ ] No red flags (lecture length, missing components)
- [ ] Overall score ≥ 75/100
