# Coherence Validator

## Purpose
Validate internal consistency across all lesson components. Ensures warmups connect to content, activities reinforce learning, assessments measure objectives, and all elements work together as a unified lesson.

## HARDCODED SKILLS
```yaml
skills:
  - word_count_analyzer
  - sentence_completeness_checker
```

## Validation Type
**QUALITY GATE** - Score must be ≥ 80/100 to pass

---

## Input Schema
```json
{
  "lesson": {
    "unit": "Greek Theater",
    "day": 5,
    "topic": "The Theatron and Orchestra",
    "learning_objectives": [
      "Identify the parts of a Greek theater",
      "Explain the function of the orchestra"
    ]
  },
  "components": {
    "warmup": {
      "name": "Greek Chorus Walk",
      "connection": "Prepares bodies for understanding how performers used the orchestra space"
    },
    "lecture": {
      "slides": [...],
      "vocabulary": ["theatron", "orchestra", "skene"],
      "key_concepts": ["audience-performer relationship", "acoustics", "sightlines"]
    },
    "activity": {
      "name": "Theater Blueprint Analysis",
      "instructions": "Rotate through stations analyzing Greek theater components",
      "learning_focus": "Spatial understanding of theater architecture"
    },
    "journal_prompt": "How might the design of the Greek theater have affected the performance style of actors?",
    "exit_ticket": "Label the three main parts of a Greek theater on a blank diagram."
  }
}
```

## Output Schema
```json
{
  "validation_result": {
    "valid": true,
    "score": 88,
    "pass_threshold": 80,
    "coherence_checks": [
      {
        "check": "warmup_to_content",
        "score": 90,
        "evidence": "Warmup physically prepares for orchestra space discussion",
        "status": "pass"
      },
      {
        "check": "objectives_to_content",
        "score": 95,
        "evidence": "All objectives directly addressed in lecture slides",
        "status": "pass"
      },
      {
        "check": "activity_to_objectives",
        "score": 85,
        "evidence": "Activity reinforces identification objective",
        "status": "pass"
      },
      {
        "check": "assessment_to_objectives",
        "score": 80,
        "evidence": "Exit ticket measures objective 1, journal addresses objective 2",
        "status": "pass"
      },
      {
        "check": "vocabulary_integration",
        "score": 90,
        "evidence": "All vocabulary terms appear in lecture and activity",
        "status": "pass"
      }
    ],
    "overall_coherence": "strong",
    "issues": [],
    "recommendations": []
  }
}
```

---

## Coherence Dimensions

### 1. Warmup-to-Content Connection (20 points)

**Strong Connection (18-20 points)**
- Warmup explicitly prepares for lesson topic
- Physical/mental state created supports learning
- Connection is stated and obvious

**Moderate Connection (12-17 points)**
- Warmup relates to general unit theme
- Some preparation for lesson content
- Connection exists but not explicit

**Weak Connection (6-11 points)**
- Warmup is generic theater exercise
- Minimal preparation for specific content
- Connection is forced or unclear

**No Connection (0-5 points)**
- Warmup unrelated to lesson
- Could be any random activity
- No preparation value for content

### 2. Objectives-to-Content Alignment (25 points)

**Full Alignment (23-25 points)**
- Every objective explicitly taught in lecture
- Content depth matches objective verb level
- No objectives left unaddressed

**Strong Alignment (17-22 points)**
- Most objectives addressed in lecture
- Some objectives only partially covered
- Minor gaps in coverage

**Partial Alignment (10-16 points)**
- Some objectives addressed, others missing
- Content doesn't match objective depth
- Significant coverage gaps

**Poor Alignment (0-9 points)**
- Objectives not reflected in content
- Lecture covers different topics
- Major disconnect between goals and teaching

### 3. Activity-to-Objectives Connection (20 points)

**Strong Reinforcement (18-20 points)**
- Activity directly practices objective skills
- Students demonstrate learning through activity
- Clear connection between doing and learning

**Moderate Reinforcement (12-17 points)**
- Activity supports objectives indirectly
- Some practice of target skills
- Connection present but not optimal

**Weak Reinforcement (6-11 points)**
- Activity tangentially related
- Limited skill practice
- Connection is unclear

**No Reinforcement (0-5 points)**
- Activity unrelated to objectives
- No skill practice
- Complete disconnect

### 4. Assessment-to-Objectives Match (25 points)

**Direct Measurement (23-25 points)**
- Exit ticket directly measures stated objectives
- Journal prompt deepens objective understanding
- Assessment verbs match objective verbs

**Strong Measurement (17-22 points)**
- Exit ticket measures most objectives
- Journal prompt relates to objectives
- Minor gaps in measurement

**Partial Measurement (10-16 points)**
- Some objectives measured, others not
- Assessment partially aligned
- Significant measurement gaps

**Poor Measurement (0-9 points)**
- Assessment doesn't measure objectives
- Different skills assessed
- Major disconnect

### 5. Vocabulary Integration (10 points)

**Full Integration (9-10 points)**
- All vocabulary introduced in lecture
- Terms used in activity instructions
- Terms appear in assessment

**Partial Integration (5-8 points)**
- Most vocabulary introduced
- Some terms missing from components
- Inconsistent usage

**Poor Integration (0-4 points)**
- Vocabulary disconnected from lesson
- Terms introduced but not used
- Assessment uses undefined terms

---

## Cross-Component Checks

### Check 1: Topic Threading
The lesson topic should appear in:
- [ ] Warmup connection statement
- [ ] At least 50% of lecture slides
- [ ] Activity name or instructions
- [ ] Journal prompt or exit ticket

### Check 2: Vocabulary Consistency
Each vocabulary term should:
- [ ] Be introduced with definition in lecture
- [ ] Appear in presenter notes with [EMPHASIS]
- [ ] Be used in activity context
- [ ] Appear in assessment (journal or exit ticket)

### Check 3: Objective Verb Alignment
| Objective Verb | Required Evidence |
|----------------|-------------------|
| Identify | Content presents items to identify; assessment asks for identification |
| Explain | Content provides explanation; assessment asks for explanation |
| Compare | Content presents multiple items; assessment asks for comparison |
| Demonstrate | Activity requires demonstration; assessment observes demonstration |
| Analyze | Content models analysis; assessment requires analysis |
| Create | Activity includes creation; assessment evaluates creation |

### Check 4: Time Allocation Logic
Components should have logical time distribution:
- More complex objectives need more lecture time
- Higher Bloom's activities need more work time
- Deeper assessments need more reflection time

### Check 5: Difficulty Progression
Within the lesson:
- Warmup: Low cognitive demand (preparation)
- Lecture: Building knowledge (present)
- Activity: Application (practice)
- Journal: Synthesis/reflection (deepen)
- Exit Ticket: Verification (assess)

---

## Issue Detection

### Critical Coherence Issues
| Issue | Impact | Resolution |
|-------|--------|------------|
| Objective not taught | Students can't achieve goal | Add content for objective |
| Assessment mismatch | Invalid measurement | Align assessment to objectives |
| Vocabulary undefined | Student confusion | Add definitions to lecture |

### Warning-Level Issues
| Issue | Impact | Resolution |
|-------|--------|------------|
| Weak warmup connection | Missed engagement opportunity | Strengthen connection |
| Activity doesn't reinforce | Limited practice | Modify activity focus |
| Journal too simple | Shallow reflection | Deepen prompt |

### Minor Issues
| Issue | Impact | Resolution |
|-------|--------|------------|
| Vocabulary underused | Missed reinforcement | Add usage instances |
| Topic not in all components | Slight disconnect | Add topic references |

---

## Scoring Calculation

```
Total Score =
  Warmup-to-Content (20) +
  Objectives-to-Content (25) +
  Activity-to-Objectives (20) +
  Assessment-to-Objectives (25) +
  Vocabulary Integration (10)

Maximum: 100 points
Pass Threshold: 80 points
```

---

## Recommendations Generation

For scores below 80, generate specific fixes:

```json
{
  "dimension": "activity_to_objectives",
  "current_score": 65,
  "gap": 15,
  "issue": "Activity focuses on identification but objective includes explanation",
  "recommendation": {
    "component": "activity",
    "current": "Label theater parts on diagram",
    "suggested": "Label theater parts AND explain the function of each to a partner",
    "improvement": "+15 points"
  }
}
```

---

## Unit-Level Coherence

Beyond single lessons, check unit coherence:

### Progressive Learning
- Day N content builds on Day N-1
- Vocabulary accumulated appropriately
- Skills developed in logical sequence

### Theme Consistency
- All lessons connect to unit essential question
- Unit vocabulary used consistently
- Performance day connects to all prior lessons

### Assessment Spiral
- Exit tickets progressively complex
- Journal prompts deepen over unit
- Final assessment covers unit scope

---

## Validation Checklist

- [ ] Warmup explicitly connects to lesson topic
- [ ] All learning objectives addressed in lecture
- [ ] Activity reinforces at least one objective
- [ ] Exit ticket measures at least one objective
- [ ] Journal prompt promotes deeper thinking
- [ ] All vocabulary terms defined and used
- [ ] Topic appears in all major components
- [ ] Overall score ≥ 80/100
