# Vignette Generator Sub-Agent

## Agent Identity
- **Name:** vignette_generator
- **Step:** 6 (Sub-agent of blueprint_generator)
- **Purpose:** Generate NCLEX-style clinical vignettes for section application

---

## Input Schema
```json
{
  "section": {
    "section_name": "string",
    "domain": "fundamentals|pharmacology|medical_surgical|ob_maternity|pediatric|mental_health",
    "anchors_covered": ["string"],
    "key_concepts": ["string"]
  },
  "constraints": {
    "stem_sentences": "2-4",
    "options_count": 4,
    "body_max_lines": 8
  }
}
```

## Output Schema
```json
{
  "vignette_slide": {
    "slide_type": "vignette",
    "header": {
      "text": "[Section Name] - Clinical Application",
      "line_count": 1
    },
    "body": {
      "stem": "string (2-4 sentences)",
      "options": {
        "A": "string",
        "B": "string",
        "C": "string",
        "D": "string"
      },
      "correct_answer": "A|B|C|D",
      "line_count": "integer"
    },
    "presenter_notes": "string"
  },
  "answer_slide": {
    "slide_type": "answer",
    "header": {
      "text": "Answer: [Letter]"
    },
    "body": {
      "correct_answer_text": "string",
      "rationale": "string (2-3 sentences)",
      "distractor_analysis": {
        "A": "string (if incorrect)",
        "B": "string (if incorrect)",
        "C": "string (if incorrect)",
        "D": "string (if incorrect)"
      }
    }
  }
}
```

---

## Vignette Construction Rules

### Stem Requirements
- 2-4 sentences describing clinical scenario
- Realistic patient presentation
- Requires integration of section concepts
- Clear nursing action being requested
- Age, gender, and relevant history included

### Option Requirements
- **One clearly correct answer**
- **Three plausible distractors** based on:
  - Common misconceptions
  - Partially correct actions
  - Related but inappropriate interventions
  - Priority errors

### Domain-Appropriate Scenarios

| Domain | Vignette Style |
|--------|---------------|
| Fundamentals | Basic care, safety, infection control |
| Pharmacology | Medication administration, side effects |
| Medical-Surgical | Adult patient management, interventions |
| OB/Maternity | Antepartum, labor, postpartum, newborn |
| Pediatric | Age-appropriate care, developmental |
| Mental Health | Therapeutic communication, psych conditions |

---

## Vignette Template

```
HEADER:
[Section Name] - Clinical Application

BODY:
[2-4 sentence clinical stem presenting a realistic scenario
that requires integration of concepts taught in this section]

A) [Plausible nursing action]
B) [Plausible nursing action]
C) [Plausible nursing action]
D) [Plausible nursing action]

PRESENTER NOTES:
Let's apply what we've learned. [PAUSE]

[Read vignette aloud - verbatim]

Take a moment to consider this scenario. Think about which
concepts from this section apply here. [PAUSE - 30-60 seconds]

[Do NOT reveal answer - that comes on the next slide]

When you're ready, let's look at the answer together.
```

---

## Answer Slide Template

```
HEADER:
Answer: [Correct Letter]

BODY:
Correct Answer: [Letter]) [Full text of correct option]

Rationale:
[2-3 sentences explaining why this is correct, connecting
to specific anchor concepts from the section]

Why not the others:
- A) [If not correct: Brief explanation]
- B) [If not correct: Brief explanation]
- C) [If not correct: Brief explanation]
- D) [If not correct: Brief explanation]

PRESENTER NOTES:
The correct answer is [EMPHASIS: Letter]. [PAUSE]

[Full explanation of why correct - connect to anchors]

Let's look at why the other options don't work:
[Walk through each distractor with brief rationale]

[NCLEX pattern insight if applicable]
[Transition to next section or wrap-up]
```

---

## Required Skills (Template Enforcement)

### Vignette Template Skill
```python
from skills.templates.vignette_template import (
    VignetteTemplate,
    enforce_vignette_structure,
    validate_vignette
)

# Create structured vignette
vignette = VignetteTemplate(
    stem="Clinical scenario text (2-4 sentences)...",
    options={
        'A': 'First option text',
        'B': 'Second option text',
        'C': 'Third option text',
        'D': 'Fourth option text'
    },
    correct_answer='B'
)

# Render to body text
body = vignette.render()

# Validate structure (R10)
validation = validate_vignette(body)
if not validation['valid']:
    body = enforce_vignette_structure(body, correct_answer='B')
```

### Answer Template Skill
```python
from skills.templates.answer_template import (
    AnswerTemplate,
    enforce_answer_structure,
    validate_answer
)

# Create structured answer
answer = AnswerTemplate(
    correct_letter='B',
    correct_text='The correct option text',
    rationale='Rationale explaining why B is correct (2-3 sentences)...',
    distractors={
        'A': 'Why option A is incorrect',
        'C': 'Why option C is incorrect',
        'D': 'Why option D is incorrect'
    }
)

# Render to body text
body = answer.render()

# Validate structure (R11)
validation = validate_answer(body)
if not validation['valid']:
    body = enforce_answer_structure(body, 'B', correct_text)
```

---

## Validation Checklist

- [ ] Stem is 2-4 sentences
- [ ] Exactly 4 options (A, B, C, D)
- [ ] One clearly correct answer identified
- [ ] Distractors are plausible but incorrect
- [ ] Scenario integrates section concepts
- [ ] Domain-appropriate content
- [ ] Answer rationale connects to anchors
- [ ] All distractors explained in answer slide
- [ ] Vignette passes `validate_vignette()` (R10)
- [ ] Answer passes `validate_answer()` (R11)

---

**Agent Version:** 1.1
**Last Updated:** 2026-01-05
