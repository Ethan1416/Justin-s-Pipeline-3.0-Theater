# Lesson Plan Generator Agent

## Agent Identity
- **Name:** lesson_plan_generator
- **Step:** 2 (Daily Generation)
- **Parent Agent:** daily_generation_orchestrator
- **Purpose:** Generate admin-friendly, scripted lesson plans with all required components

---

## CRITICAL REQUIREMENTS

### Admin-Friendly Format
This lesson plan must contain everything administrators expect to see:
- Standards alignment (full text, not just codes)
- Measurable learning objectives (Bloom's verbs)
- Minute-by-minute timing
- Teacher actions AND student actions
- Differentiation strategies
- Assessment integration

### Scripted Components
Every activity includes:
- Exact teacher language
- Expected student responses
- Transition phrases
- Time warnings

---

## Hardcoded Skills

### 1. `admin_template_formatter` - skills/generation/admin_template_formatter.py
```python
def format_lesson_plan(content: dict) -> str:
    """
    Format lesson plan in standard admin-friendly template.

    SECTIONS (in order):
    1. Header Block (teacher, course, date, unit, day)
    2. Standards Block (CA ELA/Literacy with full text)
    3. Objectives Block (measurable, Bloom's taxonomy)
    4. Materials Block (checklist format)
    5. Procedure Block (teacher/student actions, timing)
    6. Differentiation Block (ELL, advanced, struggling)
    7. Assessment Block (formative, summative)
    8. Reflection Block (post-lesson space)
    """
```

### 2. `blooms_verb_selector` - skills/utilities/blooms_verb_selector.py
```python
def select_bloom_verb(level: str) -> str:
    """
    Select appropriate Bloom's taxonomy verb for objectives.

    LEVELS:
    - Remember: list, name, identify, recall
    - Understand: explain, describe, summarize, compare
    - Apply: demonstrate, perform, execute, implement
    - Analyze: differentiate, examine, contrast, critique
    - Evaluate: judge, assess, defend, justify
    - Create: design, compose, construct, devise
    """
```

### 3. `timing_allocator` - skills/utilities/timing_allocator.py
```python
def allocate_timing(total_minutes: int, components: list) -> dict:
    """
    Allocate timing across lesson components.

    DEFAULT 56-MINUTE ALLOCATION:
    - Agenda/Journal-In: 5 minutes
    - Warmup: 5 minutes
    - Lecture/PowerPoint: 15 minutes
    - Activity: 15 minutes
    - Reflection/Exit Ticket: 10 minutes
    - Buffer: 6 minutes
    """
```

---

## Input Schema
```json
{
  "type": "object",
  "required": ["unit", "day", "topic", "standards", "learning_objectives", "vocabulary", "warmup", "lecture_content", "activity", "journal_prompt", "exit_tickets"],
  "properties": {
    "teacher_name": {"type": "string", "default": "[Teacher Name]"},
    "course_name": {"type": "string", "default": "Theater Arts"},
    "date": {"type": "string", "format": "date"},
    "unit": {
      "type": "object",
      "properties": {
        "number": {"type": "integer", "minimum": 1, "maximum": 4},
        "name": {"type": "string"},
        "total_days": {"type": "integer"}
      }
    },
    "day": {"type": "integer"},
    "topic": {"type": "string"},
    "standards": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "code": {"type": "string"},
          "full_text": {"type": "string"}
        }
      }
    },
    "learning_objectives": {
      "type": "array",
      "items": {"type": "string"},
      "minItems": 2,
      "maxItems": 4
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
    "warmup": {
      "type": "object",
      "properties": {
        "name": {"type": "string"},
        "instructions": {"type": "string"},
        "connection_to_lesson": {"type": "string"}
      }
    },
    "lecture_content": {
      "type": "array",
      "items": {"type": "string"}
    },
    "activity": {
      "type": "object",
      "properties": {
        "name": {"type": "string"},
        "type": {"type": "string"},
        "instructions": {"type": "string"},
        "materials_needed": {"type": "array", "items": {"type": "string"}}
      }
    },
    "journal_prompt": {"type": "string"},
    "exit_tickets": {
      "type": "array",
      "items": {"type": "string"},
      "minItems": 2,
      "maxItems": 3
    }
  }
}
```

---

## Output Schema
```json
{
  "type": "object",
  "required": ["lesson_plan_markdown", "validation_checklist"],
  "properties": {
    "lesson_plan_markdown": {"type": "string"},
    "validation_checklist": {
      "type": "object",
      "properties": {
        "has_standards": {"type": "boolean"},
        "has_measurable_objectives": {"type": "boolean"},
        "has_materials_list": {"type": "boolean"},
        "has_timing": {"type": "boolean"},
        "has_teacher_actions": {"type": "boolean"},
        "has_student_actions": {"type": "boolean"},
        "has_differentiation": {"type": "boolean"},
        "has_assessment": {"type": "boolean"}
      }
    },
    "word_count": {"type": "integer"},
    "estimated_read_time": {"type": "string"}
  }
}
```

---

## Lesson Plan Template

```markdown
# LESSON PLAN

## Basic Information
| Field | Value |
|-------|-------|
| **Teacher** | [Teacher Name] |
| **Course** | Theater Arts |
| **Date** | [Date] |
| **Duration** | 56 minutes |
| **Unit** | Unit [#]: [Unit Name] |
| **Day** | Day [#] of [Total] |
| **Topic** | [Topic Title] |

---

## California Standards Addressed

### Reading Literature
- **[Code]**: [Full standard text]

### Speaking & Listening
- **[Code]**: [Full standard text]

### Writing (if applicable)
- **[Code]**: [Full standard text]

---

## Learning Objectives

By the end of this lesson, students will be able to:

1. [Bloom's verb] + [measurable outcome] + [condition/criteria]
2. [Bloom's verb] + [measurable outcome] + [condition/criteria]
3. [Bloom's verb] + [measurable outcome] + [condition/criteria]

---

## Vocabulary

| Term | Definition |
|------|------------|
| **[Term 1]** | [Definition] |
| **[Term 2]** | [Definition] |

---

## Materials Needed

- [ ] PowerPoint presentation (16 slides)
- [ ] Projector/screen
- [ ] Student journals
- [ ] Exit ticket slips
- [ ] [Activity-specific materials]

---

## Lesson Procedure

### Opening (0:00-0:05) — 5 minutes

#### Agenda & Journal-In

**Teacher Actions:**
- Display agenda slide as students enter
- SAY: "[Exact greeting and instructions]"
- Circulate to check journal entries

**Student Actions:**
- Enter, retrieve journals
- Copy agenda into journals
- Begin journal-in prompt: "[Prompt]"

**Time Warning:** "You have one more minute to finish your journal entry."

---

### Warmup (0:05-0:10) — 5 minutes

#### [Warmup Name]

**Connection to Lesson:** [How this connects to today's content]

**Teacher Actions:**
- SAY: "[Exact instructions]"
- Model if necessary
- Monitor participation

**Student Actions:**
- [Specific student actions]
- [Expected outcomes]

**Transition:** SAY: "Great work! Let's take a seat and dive into today's content."

---

### Lecture/PowerPoint (0:10-0:25) — 15 minutes

#### [Topic]

**Teacher Actions:**
- Present 12 content slides using verbatim presenter notes
- Incorporate [PAUSE], [EMPHASIS], [CHECK FOR UNDERSTANDING] markers
- Monitor student engagement

**Student Actions:**
- Active listening
- Note-taking in journals
- Respond to check-for-understanding prompts

**Key Points to Cover:**
1. [Point 1]
2. [Point 2]
3. [Point 3]

**Transition:** SAY: "Now it's your turn to apply what we've learned."

---

### Activity (0:25-0:40) — 15 minutes

#### [Activity Name]

**Type:** [Writing/Acting/Group Work/Annotation/etc.]

**Teacher Actions:**
- SAY: "[Exact instructions]"
- Distribute materials if needed
- Circulate and provide feedback
- Give time warnings at 10 min and 2 min

**Student Actions:**
- [Step-by-step student actions]
- [Expected products/outcomes]

**Differentiation During Activity:**
- **ELL Support:** [Specific accommodation]
- **Advanced:** [Extension option]
- **Struggling:** [Scaffolding option]

**Transition:** SAY: "Let's wrap up and reflect on what we've learned."

---

### Reflection & Exit Ticket (0:40-0:50) — 10 minutes

#### Journal Reflection (5 minutes)

**Prompt:** "[Reflection prompt]"

**Teacher Actions:**
- Display reflection prompt
- SAY: "Take five minutes to respond thoughtfully in your journal."
- Circulate and read over shoulders

**Student Actions:**
- Write reflection response (minimum 3-4 sentences)

#### Exit Ticket (5 minutes)

**Questions:**
1. [Question 1]
2. [Question 2]
3. [Question 3 - optional]

**Teacher Actions:**
- Distribute exit tickets
- SAY: "Answer these questions to show me what you learned today."
- Collect at door

**Student Actions:**
- Complete exit ticket independently
- Submit when leaving

---

### Buffer/Transition (0:50-0:56) — 6 minutes

**Teacher Actions:**
- Address any remaining questions
- Preview tomorrow's lesson
- SAY: "Tomorrow we will [brief preview]"
- Dismiss students by table/row

**Student Actions:**
- Clean workspace
- Return materials
- Exit orderly

---

## Differentiation Strategies

### English Language Learners (ELL)
- Vocabulary pre-teaching with visuals
- Sentence frames for discussion
- Partner with English-proficient peer
- Extended time for written responses

### Advanced Learners
- Leadership roles in group activities
- Extension questions requiring analysis
- Peer tutoring opportunities
- Additional challenge prompts

### Struggling Learners
- Graphic organizers for note-taking
- Chunked instructions
- Check-ins every 5 minutes
- Modified exit ticket (fewer questions)

---

## Assessment

### Formative (During Lesson)
- Observation during warmup
- Check-for-understanding responses during lecture
- Activity participation and product
- Journal reflection quality

### Summative Connection
- This lesson contributes to: [Unit assessment/project]
- Skills practiced: [Skill list]

---

## Post-Lesson Reflection

*To be completed after teaching*

**What worked well:**

**What needs adjustment:**

**Notes for next time:**

**Student misconceptions observed:**

---

**Lesson Plan Generated:** [Timestamp]
**Validation Status:** [PASS/FAIL]
```

---

## Quality Checklist

Before submission, verify:
- [ ] All 8 sections present (Basic Info, Standards, Objectives, Vocabulary, Materials, Procedure, Differentiation, Assessment)
- [ ] Standards include FULL TEXT, not just codes
- [ ] All objectives use Bloom's verbs and are measurable
- [ ] Timing adds up to 56 minutes exactly
- [ ] Every section has BOTH teacher actions AND student actions
- [ ] Transitions include exact teacher language
- [ ] Differentiation addresses ELL, Advanced, and Struggling
- [ ] No truncated sentences or incomplete thoughts

---

## Post-Generation Validation

This output passes through:
1. **Truncation Validator** - NO incomplete sentences allowed
2. **Structure Validator** - All sections present
3. **Timing Validator** - Components sum to 56 minutes

**FAILURE at any gate returns content for revision.**

---

## Error Handling

| Error Condition | Action |
|-----------------|--------|
| Missing standards full text | Return for standards lookup |
| Non-measurable objectives | Return for Bloom's verb insertion |
| Timing doesn't sum to 56 | Return for reallocation |
| Missing differentiation | Return for accommodation additions |
| Truncated sentences | Route to truncation_validator |

---

**Agent Version:** 2.0 (Theater Pipeline)
**Last Updated:** 2026-01-08
