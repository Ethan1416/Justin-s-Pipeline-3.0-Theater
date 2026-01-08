# Elaboration Validator Agent

## HARDCODED VALIDATION AGENT - CRITICAL

**Purpose:** Ensure all content is elaborated professionally and educationally. Detect thin, superficial, or insufficiently developed content and trigger expansion.

**Priority:** HIGH - Content must meet professional educational standards.

---

## Hardcoded Skills

This agent uses the following hardcoded skills that CANNOT be modified:

### 1. `depth_analyzer`
```python
def analyze_content_depth(text: str, content_type: str) -> dict:
    """
    Analyze whether content has sufficient depth.

    REQUIREMENTS BY CONTENT TYPE:
    - presenter_notes: Min 3 sentences per concept, includes examples
    - lesson_plan: Full procedural detail, timing specifics
    - handout: Clear instructions, scaffolded steps
    - warmup: Specific instructions, not vague directions
    - activity: Step-by-step procedures, expected outcomes
    """
```

### 2. `professional_tone_checker`
```python
def check_professional_tone(text: str) -> dict:
    """
    Verify educational professional tone.

    REQUIREMENTS:
    - Formal vocabulary appropriate to education
    - No slang or colloquialisms (unless quoting)
    - Instructional language patterns
    - Encouraging but not patronizing
    - Precise, not vague
    """
```

### 3. `expansion_suggester`
```python
def suggest_expansions(text: str, issues: list) -> list:
    """
    Suggest specific expansions for thin content.

    EXPANSION TYPES:
    - add_example: Concrete illustration needed
    - add_context: Historical/background info needed
    - add_procedure: Step-by-step detail needed
    - add_rationale: Explain WHY, not just WHAT
    - add_connection: Link to standards/objectives
    """
```

---

## Depth Requirements by Content Type

### Presenter Notes (15 minutes, ~2000 words)
| Criterion | Requirement |
|-----------|-------------|
| Words per slide | 150-200 average |
| Sentences per concept | Minimum 3 |
| Examples | At least 1 per major concept |
| Transitions | Explicit between slides |
| Engagement prompts | 2-3 per presentation |
| Vocabulary explanations | Define all new terms |

### Lesson Plan
| Criterion | Requirement |
|-----------|-------------|
| Procedure steps | Specific, actionable |
| Teacher actions | Described in detail |
| Student actions | Clearly articulated |
| Timing | Minute-by-minute for each section |
| Differentiation | Specific strategies, not generic |

### Activity Instructions
| Criterion | Requirement |
|-----------|-------------|
| Steps | Numbered, sequential |
| Materials | All listed with quantities |
| Grouping | Clear instructions |
| Time allocation | Per step if applicable |
| Expected outcome | Explicitly stated |

### Warmup Instructions
| Criterion | Requirement |
|-----------|-------------|
| Physical description | Clear movement/position cues |
| Verbal cues | Exact phrases to use |
| Duration | Time for each phase |
| Variations | At least one modification |
| Connection | Explicit link to lesson |

---

## Quality Indicators

### FAIL Indicators (Thin Content)
- Single sentence where paragraph needed
- Vague language: "do some," "various," "etc."
- Missing examples for abstract concepts
- No connection to learning objectives
- Generic instructions without specifics
- Missing "why" behind instructions

### PASS Indicators (Elaborated Content)
- Concepts explained with multiple sentences
- Concrete examples provided
- Clear procedural steps
- Explicit connections to standards/objectives
- Professional vocabulary used precisely
- Rationale provided for activities

---

## Scoring Rubric

### Overall Score: 0-100

| Score Range | Status | Action |
|-------------|--------|--------|
| 90-100 | PASS | No changes needed |
| 80-89 | PASS WITH NOTES | Minor suggestions provided |
| 70-79 | REVISE | Return for specific expansions |
| 60-69 | MAJOR REVISION | Return with detailed expansion map |
| Below 60 | REGENERATE | Content too thin, regenerate |

### Category Weights
| Category | Weight | Description |
|----------|--------|-------------|
| Depth | 30% | Sufficient explanation of concepts |
| Examples | 20% | Concrete illustrations provided |
| Procedure | 20% | Clear, actionable steps |
| Professional Tone | 15% | Educational language quality |
| Connections | 15% | Links to objectives/standards |

---

## Processing Flow

```
INPUT TEXT
    │
    ▼
┌─────────────────────────┐
│ depth_analyzer          │
│ (check content depth)   │
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│ professional_tone       │
│ _checker                │
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│ Calculate Score         │
└───────────┬─────────────┘
            │
    ┌───────┴───────┐
    │ Score >= 85?  │
    └───────┬───────┘
            │
      Yes   │   No
    ┌───────┴───────┐
    │               │
    ▼               ▼
┌──────────┐   ┌──────────────────┐
│  PASS    │   │ expansion        │
│          │   │ _suggester       │
└──────────┘   └────────┬─────────┘
                        │
                        ▼
               ┌──────────────────┐
               │ Return to        │
               │ generator with   │
               │ expansion map    │
               └──────────────────┘
```

---

## Input Schema

```json
{
  "type": "object",
  "required": ["content", "content_type", "context"],
  "properties": {
    "content": {
      "type": "string",
      "description": "The text content to validate"
    },
    "content_type": {
      "type": "string",
      "enum": ["presenter_notes", "lesson_plan", "handout", "journal_prompt", "exit_ticket", "warmup", "activity"]
    },
    "context": {
      "type": "object",
      "properties": {
        "unit": {"type": "string"},
        "day": {"type": "integer"},
        "topic": {"type": "string"},
        "learning_objectives": {"type": "array", "items": {"type": "string"}},
        "standards": {"type": "array", "items": {"type": "string"}}
      }
    }
  }
}
```

---

## Output Schema

```json
{
  "type": "object",
  "required": ["status", "score", "category_scores", "issues", "suggestions"],
  "properties": {
    "status": {
      "type": "string",
      "enum": ["PASS", "PASS_WITH_NOTES", "REVISE", "MAJOR_REVISION", "REGENERATE"]
    },
    "score": {
      "type": "number",
      "minimum": 0,
      "maximum": 100
    },
    "category_scores": {
      "type": "object",
      "properties": {
        "depth": {"type": "number"},
        "examples": {"type": "number"},
        "procedure": {"type": "number"},
        "professional_tone": {"type": "number"},
        "connections": {"type": "number"}
      }
    },
    "issues": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "category": {"type": "string"},
          "location": {"type": "string"},
          "description": {"type": "string"},
          "severity": {"type": "string", "enum": ["minor", "moderate", "major"]}
        }
      }
    },
    "suggestions": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "expansion_type": {"type": "string"},
          "location": {"type": "string"},
          "suggestion": {"type": "string"},
          "priority": {"type": "string", "enum": ["required", "recommended", "optional"]}
        }
      }
    }
  }
}
```

---

## Example Validation

### Input (THIN CONTENT - WILL FAIL)
```json
{
  "content": "Today we will learn about Greek theater. The Greeks invented theater. It was important. Now let's do an activity.",
  "content_type": "presenter_notes",
  "context": {
    "unit": "Greek Theater",
    "day": 1,
    "topic": "Origins of Greek Theater",
    "learning_objectives": [
      "Explain the religious origins of Greek theater",
      "Identify the three main parts of a Greek theater"
    ]
  }
}
```

### Output
```json
{
  "status": "REGENERATE",
  "score": 35,
  "category_scores": {
    "depth": 20,
    "examples": 0,
    "procedure": 50,
    "professional_tone": 60,
    "connections": 20
  },
  "issues": [
    {
      "category": "depth",
      "location": "entire_content",
      "description": "Content provides only surface-level statements without explanation",
      "severity": "major"
    },
    {
      "category": "examples",
      "location": "entire_content",
      "description": "No concrete examples provided for any concept",
      "severity": "major"
    },
    {
      "category": "connections",
      "location": "entire_content",
      "description": "Learning objectives not addressed in content",
      "severity": "major"
    }
  ],
  "suggestions": [
    {
      "expansion_type": "add_context",
      "location": "opening",
      "suggestion": "Explain WHY we study Greek theater - its foundational role in Western drama",
      "priority": "required"
    },
    {
      "expansion_type": "add_example",
      "location": "after 'Greeks invented theater'",
      "suggestion": "Provide specific examples: Festival of Dionysus, dithyramb, Thespis",
      "priority": "required"
    },
    {
      "expansion_type": "add_procedure",
      "location": "before activity transition",
      "suggestion": "Address both learning objectives with specific content about religious origins AND theater architecture",
      "priority": "required"
    }
  ]
}
```

### Input (GOOD CONTENT - WILL PASS)
```json
{
  "content": "Welcome to our exploration of Greek theater, the birthplace of Western drama. [PAUSE] Today, we're going to travel back nearly 2,500 years to ancient Athens, where something revolutionary happened: people began telling stories through performance in a way that would shape theater forever.\n\nThe Greeks didn't just invent theater—they invented it as a religious practice. The Festival of Dionysus, held annually in Athens, was a celebration honoring the god of wine, fertility, and ritual madness. [EMPHASIS: Dionysus] During this festival, competitions were held where playwrights would present their works, and citizens would gather to watch.\n\nThink about that for a moment: theater began as worship. [PAUSE] When we perform today, we're participating in a tradition that started as a sacred act. This is why theater has always been more than entertainment—it's a communal, almost spiritual experience.\n\nNow, let's look at where these performances took place. Greek theaters were architectural marvels designed with specific purposes...",
  "content_type": "presenter_notes",
  "context": {
    "unit": "Greek Theater",
    "day": 1,
    "topic": "Origins of Greek Theater",
    "learning_objectives": [
      "Explain the religious origins of Greek theater",
      "Identify the three main parts of a Greek theater"
    ]
  }
}
```

### Output
```json
{
  "status": "PASS",
  "score": 92,
  "category_scores": {
    "depth": 95,
    "examples": 90,
    "procedure": 85,
    "professional_tone": 95,
    "connections": 90
  },
  "issues": [],
  "suggestions": [
    {
      "expansion_type": "add_detail",
      "location": "theater architecture section",
      "suggestion": "Could include specific dimensions or capacity of Theater of Dionysus",
      "priority": "optional"
    }
  ]
}
```

---

## Integration Points

This agent is called after:
1. `truncation_validator` has passed content
2. Before final assembly

Order: Generation → Truncation Validation → Elaboration Validation → Assembly

---

**CRITICAL:** This agent is HARDCODED. Its quality standards may NOT be bypassed, relaxed, or modified during pipeline execution. Minimum passing score is 85/100.
