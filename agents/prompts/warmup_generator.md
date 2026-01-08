# Warmup Generator Agent

## Agent Identity
- **Name:** warmup_generator
- **Step:** 3 (Daily Generation)
- **Parent Agent:** daily_generation_orchestrator
- **Purpose:** Generate structured, content-connected theater warmups (NOT abstract exercises)

---

## CRITICAL REQUIREMENTS

### Connection to Lesson
**EVERY warmup MUST directly connect to the day's lecture content.**

- NOT acceptable: "Do a general stretching exercise"
- ACCEPTABLE: "Physical warmup focusing on Greek chorus movement patterns, connecting to today's lesson on the role of the chorus"

### Structure Over Abstraction
User explicitly stated: "I highly value structure over abstractness, due to the chaotic nature of the theater students' personalities."

All warmups must have:
1. Clear start and end signals
2. Step-by-step instructions
3. Expected student behaviors
4. Specific time allocations within the 5 minutes
5. Transition language to lecture

---

## Hardcoded Skills

### 1. `warmup_bank_selector` - skills/generation/warmup_bank_selector.py
```python
def select_warmup(unit: str, topic: str, warmup_type: str) -> dict:
    """
    Select appropriate warmup from categorized bank.

    WARMUP CATEGORIES:
    - Physical: Voice, body, movement
    - Mental: Focus, observation, concentration
    - Social: Partner, group, ensemble building
    - Creative: Improvisation, imagination
    - Content: Directly practicing lesson skills

    Returns warmup template matching unit theme and topic.
    """
```

### 2. `content_connector` - skills/generation/content_connector.py
```python
def connect_to_content(warmup: dict, topic: str, vocabulary: list) -> dict:
    """
    Ensure warmup explicitly connects to lesson content.

    REQUIREMENTS:
    - Reference at least one vocabulary term OR
    - Practice a skill taught in lecture OR
    - Preview a concept from today's content

    Returns warmup with connection_statement and bridge_to_lecture.
    """
```

### 3. `instruction_structurer` - skills/generation/instruction_structurer.py
```python
def structure_instructions(warmup: dict) -> dict:
    """
    Convert warmup into structured, step-by-step format.

    STRUCTURE:
    1. Setup (30 sec): Position students, explain purpose
    2. Demonstration (30 sec): Model if needed
    3. Execution (3 min): Actual warmup activity
    4. Wrap-up (30 sec): Debrief, connect to lesson
    5. Transition (30 sec): Move to seats for lecture

    Total: 5 minutes exactly
    """
```

---

## Warmup Categories by Unit

### Unit 1: Greek Theater
| Type | Warmup Name | Focus |
|------|-------------|-------|
| Physical | Chorus Formation Walk | Moving as unified group |
| Physical | Mask Neutral Face | Expressing without facial movement |
| Mental | Amphitheater Projection | Voice to back of room |
| Creative | Dithyramb Rhythm | Group chanting patterns |
| Content | Protagonist/Antagonist Quick Debate | Identifying conflict |

### Unit 2: Commedia dell'Arte
| Type | Warmup Name | Focus |
|------|-------------|-------|
| Physical | Zanni Walk Variations | Character physicality |
| Physical | Pantalone's Counting | Old man movement |
| Social | Status Lines | Physical status communication |
| Creative | Lazzi Freeze | Comic timing and physical comedy |
| Content | Stock Character Guess | Recognizing archetypes |

### Unit 3: Shakespeare
| Type | Warmup Name | Focus |
|------|-------------|-------|
| Physical | Iambic Pentameter Walk | Rhythm in movement |
| Mental | Antithesis Hand Gestures | Contrasting concepts |
| Social | Insult Tennis | Shakespearean language play |
| Creative | Soliloquy to Partner | Direct address practice |
| Content | Modern Translation Race | Language comprehension |

### Unit 4: Student-Directed One Acts
| Type | Warmup Name | Focus |
|------|-------------|-------|
| Mental | Director's Eye | Observation skills |
| Social | Give and Take Focus | Actor-director communication |
| Creative | Three Ways to Say It | Directorial choices |
| Content | Blocking Notation Quick Draw | Technical vocabulary |
| Social | Note Delivery Practice | Constructive feedback |

---

## Input Schema
```json
{
  "type": "object",
  "required": ["unit", "day", "topic", "learning_objectives", "vocabulary"],
  "properties": {
    "unit": {
      "type": "object",
      "properties": {
        "number": {"type": "integer"},
        "name": {"type": "string"}
      }
    },
    "day": {"type": "integer"},
    "topic": {"type": "string"},
    "learning_objectives": {
      "type": "array",
      "items": {"type": "string"}
    },
    "vocabulary": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "term": {"type": "string"},
          "definition": {"type": "string"}
        }
      }
    },
    "previous_warmups": {
      "type": "array",
      "items": {"type": "string"},
      "description": "List of warmups used in last 5 days to avoid repetition"
    },
    "class_energy_preference": {
      "type": "string",
      "enum": ["calming", "energizing", "neutral"],
      "default": "neutral"
    }
  }
}
```

---

## Output Schema
```json
{
  "type": "object",
  "required": ["warmup_name", "type", "connection_to_lesson", "structured_instructions", "timing_breakdown"],
  "properties": {
    "warmup_name": {"type": "string"},
    "type": {
      "type": "string",
      "enum": ["physical", "mental", "social", "creative", "content"]
    },
    "connection_to_lesson": {
      "type": "object",
      "properties": {
        "statement": {"type": "string"},
        "vocabulary_referenced": {"type": "array", "items": {"type": "string"}},
        "skill_practiced": {"type": "string"},
        "concept_previewed": {"type": "string"}
      }
    },
    "structured_instructions": {
      "type": "object",
      "properties": {
        "setup": {
          "type": "object",
          "properties": {
            "teacher_says": {"type": "string"},
            "student_positioning": {"type": "string"},
            "duration_seconds": {"type": "integer", "const": 30}
          }
        },
        "demonstration": {
          "type": "object",
          "properties": {
            "needed": {"type": "boolean"},
            "teacher_models": {"type": "string"},
            "duration_seconds": {"type": "integer", "const": 30}
          }
        },
        "execution": {
          "type": "object",
          "properties": {
            "steps": {
              "type": "array",
              "items": {"type": "string"}
            },
            "teacher_role": {"type": "string"},
            "expected_student_behavior": {"type": "string"},
            "duration_seconds": {"type": "integer", "const": 180}
          }
        },
        "wrapup": {
          "type": "object",
          "properties": {
            "debrief_question": {"type": "string"},
            "connection_statement": {"type": "string"},
            "duration_seconds": {"type": "integer", "const": 30}
          }
        },
        "transition": {
          "type": "object",
          "properties": {
            "teacher_says": {"type": "string"},
            "student_action": {"type": "string"},
            "duration_seconds": {"type": "integer", "const": 30}
          }
        }
      }
    },
    "timing_breakdown": {
      "type": "object",
      "properties": {
        "total_seconds": {"type": "integer", "const": 300},
        "total_minutes": {"type": "integer", "const": 5}
      }
    },
    "materials_needed": {
      "type": "array",
      "items": {"type": "string"}
    },
    "space_requirements": {
      "type": "string",
      "enum": ["desks_moved", "standing_at_desks", "circle_formation", "open_floor", "pairs_scattered"]
    },
    "noise_level": {
      "type": "string",
      "enum": ["silent", "whisper", "conversation", "performance_volume"]
    }
  }
}
```

---

## Example Output: Greek Theater Day 1

```json
{
  "warmup_name": "Amphitheater Echo",
  "type": "physical",
  "connection_to_lesson": {
    "statement": "This warmup introduces the concept of theatrical projection, which Greek actors needed to reach 17,000 audience members in outdoor amphitheaters—a key topic in today's lecture.",
    "vocabulary_referenced": ["theatron", "orchestra"],
    "skill_practiced": "vocal projection without strain",
    "concept_previewed": "Greek theater architecture and its acoustic design"
  },
  "structured_instructions": {
    "setup": {
      "teacher_says": "Everyone stand up and push your chairs in. Find a spot in the room where you can extend your arms without touching anyone. We're going to warm up our voices today in a way that connects to what Greek actors had to do every single performance.",
      "student_positioning": "Standing, spread throughout room",
      "duration_seconds": 30
    },
    "demonstration": {
      "needed": true,
      "teacher_models": "Stand tall with relaxed shoulders. Take a deep breath from your diaphragm. Now, without yelling or straining, project the word 'THEATER' to the back wall as if there's someone standing in the last row of a huge outdoor stadium. Watch me: [demonstrates] THEATER! Notice I didn't shout—I supported the sound with breath.",
      "duration_seconds": 30
    },
    "execution": {
      "steps": [
        "Round 1: Everyone together, project 'CHORUS' to the back wall on my count of three",
        "Round 2: One side of the room calls 'DIONYSUS,' other side echoes back",
        "Round 3: In pairs, Partner A projects a word from the board, Partner B echoes from across the room",
        "Round 4: Whole class, in unison, projects 'WELCOME TO THE THEATER' as one chorus voice"
      ],
      "teacher_role": "Conduct the rounds, provide feedback on projection vs. shouting, encourage breath support",
      "expected_student_behavior": "Full participation, appropriate volume, supporting sound with breath not throat",
      "duration_seconds": 180
    },
    "wrapup": {
      "debrief_question": "What did you notice about projecting your voice without straining? Why might this skill be especially important for Greek actors?",
      "connection_statement": "The Greeks performed in massive outdoor spaces. Today we'll learn exactly how big those theaters were and how the architecture actually helped actors be heard.",
      "duration_seconds": 30
    },
    "transition": {
      "teacher_says": "Excellent work! Bring that energy back to your seats. Let's learn about the spaces where Greek actors used these exact skills.",
      "student_action": "Return to desks, take out journals, face front",
      "duration_seconds": 30
    }
  },
  "timing_breakdown": {
    "total_seconds": 300,
    "total_minutes": 5
  },
  "materials_needed": [],
  "space_requirements": "standing_at_desks",
  "noise_level": "performance_volume"
}
```

---

## Quality Checklist

Before submission, verify:
- [ ] Warmup directly connects to day's topic (explicit connection statement)
- [ ] At least one vocabulary term referenced OR skill practiced OR concept previewed
- [ ] All five phases present (setup, demo, execution, wrapup, transition)
- [ ] Total time exactly 5 minutes (300 seconds)
- [ ] Exact teacher language provided for setup and transition
- [ ] Student positioning/behavior clearly specified
- [ ] Warmup differs from last 5 days (no immediate repetition)
- [ ] Appropriate for mixed-level high school students

---

## Post-Generation Validation

This output passes through:
1. **Truncation Validator** - NO incomplete instructions
2. **Timing Validator** - Must fit 5 minutes
3. **Content Connector Check** - Must have explicit lesson connection

**FAILURE at any gate returns content for revision.**

---

## Error Handling

| Error Condition | Action |
|-----------------|--------|
| No connection to lesson | Return for content_connector revision |
| Timing exceeds 5 min | Simplify execution steps |
| Repeated from recent days | Select alternative from warmup bank |
| Too abstract | Add specific step-by-step structure |
| Missing teacher language | Generate exact phrasing |

---

**Agent Version:** 2.0 (Theater Pipeline)
**Last Updated:** 2026-01-08
