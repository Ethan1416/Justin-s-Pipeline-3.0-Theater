# Unit Planner Agent

## Purpose
Generate comprehensive unit plans for 18-25 day theater education units, including day-by-day topic breakdown, standards alignment, and learning progression.

---

## Hardcoded Skills

### 1. `scope_calculator`
Calculates appropriate content scope for given number of days.

### 2. `standards_mapper`
Maps unit content to California ELA/Literacy standards (RL, SL, W.9-12).

### 3. `scaffolding_sequencer`
Ensures learning builds progressively from foundational to complex.

### 4. `assessment_distributor`
Distributes formative and summative assessments across unit.

---

## Input Schema

```json
{
  "type": "object",
  "required": ["unit_name", "total_days", "grade_levels", "prior_units"],
  "properties": {
    "unit_name": {
      "type": "string",
      "enum": ["Greek Theater", "Commedia dell'Arte", "Shakespeare", "Student-Directed One Acts"]
    },
    "total_days": {
      "type": "integer",
      "minimum": 18,
      "maximum": 25
    },
    "grade_levels": {
      "type": "array",
      "items": {"type": "integer", "minimum": 9, "maximum": 12}
    },
    "prior_units": {
      "type": "array",
      "items": {"type": "string"},
      "description": "Units completed before this one"
    },
    "available_resources": {
      "type": "array",
      "items": {"type": "string"},
      "description": "Scripts, props, spaces available"
    }
  }
}
```

---

## Output Schema

```json
{
  "type": "object",
  "required": ["unit_overview", "essential_questions", "standards", "vocabulary", "daily_breakdown", "assessments"],
  "properties": {
    "unit_overview": {
      "type": "object",
      "properties": {
        "unit_name": {"type": "string"},
        "total_days": {"type": "integer"},
        "unit_summary": {"type": "string", "minLength": 200},
        "big_ideas": {"type": "array", "items": {"type": "string"}, "minItems": 3}
      }
    },
    "essential_questions": {
      "type": "array",
      "items": {"type": "string"},
      "minItems": 3,
      "maxItems": 5
    },
    "standards": {
      "type": "object",
      "properties": {
        "reading_literature": {"type": "array", "items": {"type": "string"}},
        "speaking_listening": {"type": "array", "items": {"type": "string"}},
        "writing": {"type": "array", "items": {"type": "string"}}
      }
    },
    "vocabulary": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "term": {"type": "string"},
          "definition": {"type": "string"},
          "introduced_day": {"type": "integer"}
        }
      }
    },
    "daily_breakdown": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "day": {"type": "integer"},
          "topic": {"type": "string"},
          "learning_objectives": {"type": "array", "items": {"type": "string"}},
          "standards_addressed": {"type": "array", "items": {"type": "string"}},
          "activity_type": {"type": "string"},
          "materials_needed": {"type": "array", "items": {"type": "string"}},
          "assessment_type": {"type": "string", "enum": ["none", "formative", "summative", "performance"]}
        }
      }
    },
    "assessments": {
      "type": "object",
      "properties": {
        "formative": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "day": {"type": "integer"},
              "type": {"type": "string"},
              "description": {"type": "string"}
            }
          }
        },
        "summative": {
          "type": "object",
          "properties": {
            "type": {"type": "string"},
            "day": {"type": "integer"},
            "description": {"type": "string"},
            "rubric_categories": {"type": "array", "items": {"type": "string"}}
          }
        }
      }
    }
  }
}
```

---

## Unit-Specific Content Guidelines

### Unit 1: Greek Theater (20 days)

**Scope:**
- Days 1-4: Historical context and origins
- Days 5-8: Theater architecture and production elements
- Days 9-12: Tragedy (structure, themes, chorus)
- Days 13-16: Comedy (Old Comedy, Aristophanes)
- Days 17-19: Performance and application
- Day 20: Unit assessment

**Key Content:**
- Festival of Dionysus
- Theater architecture (orchestra, theatron, skene)
- Tragedy elements (hamartia, catharsis, hubris)
- Role of the chorus
- Masks and costumes
- Major playwrights (Aeschylus, Sophocles, Euripides, Aristophanes)

**Standards Focus:**
- RL.9-10.5 / RL.11-12.5 (structure)
- SL.9-10.1 / SL.11-12.1 (discussion)
- SL.9-10.6 / SL.11-12.6 (adapt speech)

---

### Unit 2: Commedia dell'Arte (18 days)

**Scope:**
- Days 1-3: Historical context (Renaissance Italy)
- Days 4-7: Stock characters (masters, servants, lovers)
- Days 8-11: Physical comedy and lazzi
- Days 12-15: Improvisation within structure
- Days 16-17: Performance preparation
- Day 18: Unit assessment

**Key Content:**
- Historical context (traveling troupes, marketplace theater)
- Stock characters (Pantalone, Il Dottore, Arlecchino, Colombina, etc.)
- Masks and physicality
- Lazzi (comic bits)
- Scenario vs. script
- Improvisation techniques

**Standards Focus:**
- RL.9-10.3 / RL.11-12.3 (character analysis)
- SL.9-10.6 / SL.11-12.6 (adapt speech)
- W.9-10.3 / W.11-12.3 (narrative writing)

---

### Unit 3: Shakespeare (25 days)

**Scope:**
- Days 1-4: Shakespeare's world (Elizabethan England, Globe Theatre)
- Days 5-8: Language tools (iambic pentameter, verse vs. prose)
- Days 9-14: Tragedy study (selected play)
- Days 15-20: Comedy study (selected play)
- Days 21-24: Scene work and performance
- Day 25: Unit assessment

**Key Content:**
- Historical context (Elizabethan era, Globe Theatre)
- Iambic pentameter and scansion
- Verse vs. prose (status implications)
- Soliloquy and aside
- Character analysis through text
- Staging conventions
- Selected plays for study

**Standards Focus:**
- RL.9-10.4 / RL.11-12.4 (language analysis - Shakespeare explicitly mentioned)
- RL.9-10.9 (source transformation)
- SL.9-10.4 / SL.11-12.4 (presentation)

---

### Unit 4: Student-Directed One Acts (17 days)

**Scope:**
- Days 1-3: Director's role and responsibilities
- Days 4-6: Script analysis for directing
- Days 7-9: Blocking and staging fundamentals
- Days 10-12: Working with actors
- Days 13-16: Rehearsal process (students direct)
- Day 17: Showcase and assessment

**Key Content:**
- Director's vision and concept
- Script analysis (given circumstances, objectives, obstacles)
- Blocking notation and stage geography
- Giving effective notes
- Rehearsal structure
- Technical coordination basics

**Standards Focus:**
- SL.9-10.1 / SL.11-12.1 (collaborative discussion)
- SL.9-10.4 / SL.11-12.4 (present information)
- W.9-10.2 / W.11-12.2 (informative writing - director's notes)

---

## Learning Progression Requirements

### Scaffolding Principles
1. **Introduce → Practice → Apply → Assess**
2. **Concrete → Abstract** (physical activities before theoretical discussion)
3. **Individual → Group → Performance**
4. **Receptive → Productive** (watching/reading before creating)

### Day-by-Day Progression Pattern
- **Days 1-3:** Foundation (history, context, key concepts)
- **Days 4-7:** Skill introduction (core techniques)
- **Days 8-12:** Skill development (practice, refinement)
- **Days 13-16:** Application (projects, performance prep)
- **Days 17+:** Assessment and synthesis

---

## Quality Requirements

### Unit Plan Must Include:
- [ ] Clear learning progression from day 1 to final day
- [ ] All learning objectives linked to standards
- [ ] Vocabulary introduced before concepts requiring it
- [ ] Balance of activity types (lecture, practice, performance)
- [ ] Multiple formative assessments throughout
- [ ] Summative assessment aligned to essential questions
- [ ] Differentiation considerations noted

### Validation Checks:
1. **Coverage Check:** All standards mapped to at least 2 days
2. **Vocabulary Check:** All terms defined and introduction day specified
3. **Assessment Check:** At least 3 formative assessments before summative
4. **Balance Check:** No more than 3 consecutive lecture-heavy days
5. **Progression Check:** Complexity increases across unit

---

## Example Output (Partial)

```json
{
  "unit_overview": {
    "unit_name": "Greek Theater",
    "total_days": 20,
    "unit_summary": "This unit explores the origins of Western theater in ancient Greece, examining how religious festivals dedicated to Dionysus evolved into the dramatic traditions that influence theater today. Students will study the physical theater space, understand the conventions of tragedy and comedy, and experience Greek theatrical techniques through performance activities.",
    "big_ideas": [
      "Theater originated as religious ritual and maintains ceremonial qualities",
      "Greek theater established structural conventions still used today",
      "The chorus served as bridge between audience and action"
    ]
  },
  "essential_questions": [
    "How did religious practice give birth to theatrical performance?",
    "What makes Greek tragedy 'tragic' and how do we see its influence today?",
    "How does physical space shape theatrical storytelling?",
    "What role does community play in theatrical performance?"
  ],
  "daily_breakdown": [
    {
      "day": 1,
      "topic": "Introduction to Greek Theater: Origins and the Festival of Dionysus",
      "learning_objectives": [
        "Explain the religious origins of Greek theater",
        "Describe the Festival of Dionysus and its role in theater history",
        "Identify key vocabulary: dithyramb, Thespis, Dionysus"
      ],
      "standards_addressed": ["RL.9-10.5", "SL.9-10.1"],
      "activity_type": "collaborative_discussion",
      "materials_needed": ["PowerPoint", "Map of ancient Greece", "Journal"],
      "assessment_type": "none"
    }
  ]
}
```

---

## Post-Generation Validation

After generating, this unit plan passes through:
1. **Truncation Validator** - Ensure no incomplete content
2. **Elaboration Validator** - Ensure sufficient detail
3. **Standards Coverage Validator** - Verify all standards addressed

---

**Agent Version:** 2.0
**Last Updated:** 2026-01-08
