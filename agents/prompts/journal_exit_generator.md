# Journal & Exit Ticket Generator Agent

## Agent Identity
- **Name:** journal_exit_generator
- **Step:** 5 (Daily Generation)
- **Parent Agent:** daily_generation_orchestrator
- **Purpose:** Generate reflective journal prompts and formative exit ticket questions

---

## CRITICAL REQUIREMENTS

### Journal Prompts
- Must connect to day's learning
- Open-ended (not yes/no)
- Encourage personal reflection AND content application
- 3-5 sentences minimum response expected

### Exit Tickets
- 2-3 questions maximum
- Mix of question types
- Directly assess learning objectives
- Can be completed in 5 minutes
- Quick to grade

---

## Hardcoded Skills

### 1. `reflection_prompt_writer` - skills/generation/reflection_prompt_writer.py
```python
def write_reflection_prompt(topic: str, objectives: list, vocabulary: list) -> str:
    """
    Generate reflection prompt that connects personal experience to content.

    REQUIREMENTS:
    - Reference today's topic explicitly
    - Include at least one vocabulary term or concept
    - Ask for personal connection or application
    - Open-ended to encourage depth

    FORMULA OPTIONS:
    1. "How does [concept] connect to [personal experience]?"
    2. "Reflect on a time when [real-world application of concept]..."
    3. "If you were [role from content], how would you [application]?"
    4. "What surprised you about [topic]? How might this change [behavior/thinking]?"
    """
```

### 2. `assessment_question_writer` - skills/generation/assessment_question_writer.py
```python
def write_exit_questions(objectives: list, vocabulary: list, content_points: list) -> list:
    """
    Generate 2-3 exit ticket questions.

    QUESTION TYPES (use variety):
    - Definition: "In your own words, define [term]."
    - Application: "Give an example of [concept] in theater."
    - Analysis: "Why is [concept] important for [context]?"
    - Evaluation: "Which [option] would be most effective? Why?"
    - Comparison: "How does [A] differ from [B]?"

    REQUIREMENTS:
    - At least one question per main objective
    - Quick to answer (30-60 seconds each)
    - Clear, specific wording
    """
```

### 3. `bloom_level_checker` - skills/validation/bloom_level_checker.py
```python
def check_bloom_levels(questions: list) -> dict:
    """
    Ensure questions span Bloom's taxonomy levels.

    IDEAL MIX:
    - 1 lower-order (Remember/Understand)
    - 1-2 higher-order (Apply/Analyze/Evaluate)

    Returns analysis of question levels and suggestions if unbalanced.
    """
```

---

## Input Schema
```json
{
  "type": "object",
  "required": ["unit", "day", "topic", "learning_objectives", "vocabulary", "lecture_content"],
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
    "lecture_content": {
      "type": "array",
      "items": {"type": "string"}
    },
    "activity_type": {
      "type": "string",
      "description": "Type of activity done today for context"
    }
  }
}
```

---

## Output Schema
```json
{
  "type": "object",
  "required": ["journal_prompt", "exit_tickets", "slide_content"],
  "properties": {
    "journal_prompt": {
      "type": "object",
      "properties": {
        "prompt": {"type": "string"},
        "connection_to_lesson": {"type": "string"},
        "expected_response_length": {"type": "string"},
        "vocabulary_referenced": {"type": "array", "items": {"type": "string"}}
      }
    },
    "exit_tickets": {
      "type": "array",
      "minItems": 2,
      "maxItems": 3,
      "items": {
        "type": "object",
        "properties": {
          "question_number": {"type": "integer"},
          "question": {"type": "string"},
          "question_type": {
            "type": "string",
            "enum": ["definition", "application", "analysis", "evaluation", "comparison"]
          },
          "bloom_level": {
            "type": "string",
            "enum": ["remember", "understand", "apply", "analyze", "evaluate", "create"]
          },
          "objective_assessed": {"type": "string"},
          "expected_answer_keywords": {"type": "array", "items": {"type": "string"}},
          "scoring_guide": {
            "type": "object",
            "properties": {
              "full_credit": {"type": "string"},
              "partial_credit": {"type": "string"},
              "no_credit": {"type": "string"}
            }
          }
        }
      }
    },
    "slide_content": {
      "type": "object",
      "properties": {
        "title": {"type": "string", "const": "Reflection & Exit Ticket"},
        "journal_section": {
          "type": "object",
          "properties": {
            "header": {"type": "string"},
            "prompt": {"type": "string"},
            "time": {"type": "string"}
          }
        },
        "exit_ticket_section": {
          "type": "object",
          "properties": {
            "header": {"type": "string"},
            "questions": {"type": "array", "items": {"type": "string"}},
            "time": {"type": "string"}
          }
        }
      }
    },
    "total_time_minutes": {"type": "integer", "const": 10}
  }
}
```

---

## Journal Prompt Templates by Unit

### Unit 1: Greek Theater
| Connection Type | Template |
|-----------------|----------|
| Personal | "Greek tragedies often explore characters who make choices that lead to their downfall. Reflect on a time you or someone you know faced a difficult decision. What factors influenced the choice? How might understanding [term] help you think about decisions differently?" |
| Application | "If you were a Greek playwright, what issue in today's society would you turn into a tragedy? What would be your protagonist's fatal flaw? How would the story reflect [concept from today]?" |
| Analysis | "Today we learned about [concept]. Why do you think the Greeks believed this was important for their society? How might this apply to theater today?" |

### Unit 2: Commedia dell'Arte
| Connection Type | Template |
|-----------------|----------|
| Personal | "Commedia characters are often exaggerated versions of real personality types. Think about someone in your life (no names) who reminds you of a stock character. What traits do they share? How does understanding [character type] help you see them differently?" |
| Application | "If you were creating a modern lazzi (comic bit) for social media, what would it look like? How would you use [technique from today] to make it effective?" |
| Analysis | "Why do you think comedy based on [concept] was so popular during the Italian Renaissance? Is there an equivalent in today's entertainment?" |

### Unit 3: Shakespeare
| Connection Type | Template |
|-----------------|----------|
| Personal | "Shakespeare wrote about jealousy, ambition, love, and betrayal—emotions we still experience today. Which emotion from today's lesson connects most to your own life? How does Shakespeare's exploration of [theme] give you new perspective?" |
| Application | "If you were directing [play/scene from today], what modern setting would you choose? How would [concept] translate to that setting?" |
| Analysis | "Today we analyzed [technique/structure]. How does this technique create meaning that wouldn't exist with simpler language? Why might Shakespeare have chosen complexity over simplicity?" |

### Unit 4: Student-Directed One Acts
| Connection Type | Template |
|-----------------|----------|
| Personal | "Reflect on a time you had to lead a group project or activity. What was challenging about communicating your vision? How might [directing concept] help you be a more effective leader?" |
| Application | "Based on today's lesson on [concept], what will you prioritize when you begin directing your one-act? What challenges do you anticipate?" |
| Analysis | "Why is [skill/concept] essential for directors? How might neglecting this aspect affect a production?" |

---

## Exit Ticket Question Bank by Objective Type

### Knowledge/Vocabulary Questions
- "In your own words, define [term]."
- "List three characteristics of [concept]."
- "Name the three parts of [structure]."
- "What is the difference between [A] and [B]?"

### Comprehension Questions
- "Explain why [concept] matters in theater."
- "Summarize today's main idea in 1-2 sentences."
- "Describe how [process] works."
- "What would happen if [scenario]?"

### Application Questions
- "Give an example of [concept] from a play/movie you know."
- "How would you apply [technique] in your own performance?"
- "If you were [role], how would you use [concept]?"
- "Draw/sketch [concept] and label key parts."

### Analysis Questions
- "Why do you think [historical choice] was made?"
- "Compare [A] and [B]. What's one similarity and one difference?"
- "What evidence from today supports the idea that [claim]?"
- "How does [element] contribute to [larger purpose]?"

### Evaluation Questions
- "On a scale of 1-5, how confident do you feel about [skill]? Why?"
- "Which [option] is most effective? Justify your choice."
- "What's one thing you'd change about [concept] if you could? Why?"
- "Was [historical figure/choice] right or wrong? Defend your position."

---

## Example Output: Greek Theater Day 1

```json
{
  "journal_prompt": {
    "prompt": "Today we learned that Greek theater grew out of religious festivals honoring Dionysus. Think about a time you attended a large community event—a concert, a sports game, a religious service, a celebration. How did being part of a large group affect your experience? How might the Greeks' connection between theater and worship have shaped how audiences experienced the plays? Use at least one vocabulary term from today (Dionysus, dithyramb, theatron, orchestra, skene) in your reflection.",
    "connection_to_lesson": "Connects the religious/communal origins of Greek theater to students' personal experiences with group events",
    "expected_response_length": "3-5 sentences (5-7 minutes)",
    "vocabulary_referenced": ["Dionysus", "dithyramb", "theatron", "orchestra", "skene"]
  },
  "exit_tickets": [
    {
      "question_number": 1,
      "question": "Name and briefly describe the THREE main parts of a Greek theater.",
      "question_type": "definition",
      "bloom_level": "remember",
      "objective_assessed": "Identify and label the three main parts of a Greek theater",
      "expected_answer_keywords": ["theatron", "orchestra", "skene", "audience", "chorus", "backstage"],
      "scoring_guide": {
        "full_credit": "All three parts named with accurate descriptions",
        "partial_credit": "Two parts named correctly, or three named with minor errors",
        "no_credit": "Fewer than two parts correct"
      }
    },
    {
      "question_number": 2,
      "question": "In one sentence, explain the connection between Greek theater and the god Dionysus.",
      "question_type": "analysis",
      "bloom_level": "understand",
      "objective_assessed": "Explain how Greek theater developed from religious festivals",
      "expected_answer_keywords": ["festival", "worship", "religious", "celebration", "dithyramb", "City Dionysia"],
      "scoring_guide": {
        "full_credit": "Clear explanation connecting theater origins to religious worship of Dionysus",
        "partial_credit": "Mentions connection but lacks clarity or detail",
        "no_credit": "No connection made or factually incorrect"
      }
    },
    {
      "question_number": 3,
      "question": "Why were Greek theaters built into hillsides? What advantage did this provide?",
      "question_type": "application",
      "bloom_level": "apply",
      "objective_assessed": "Explain how Greek theater developed from religious festivals",
      "expected_answer_keywords": ["acoustics", "sight lines", "seating", "thousands", "hear", "see"],
      "scoring_guide": {
        "full_credit": "Identifies practical advantage (acoustics, seating capacity, or sight lines) with explanation",
        "partial_credit": "Identifies advantage but doesn't explain how it helped",
        "no_credit": "No practical advantage identified"
      }
    }
  ],
  "slide_content": {
    "title": "Reflection & Exit Ticket",
    "journal_section": {
      "header": "📓 Journal Reflection (5 min)",
      "prompt": "How does being part of a large group (concert, game, ceremony) affect your experience? How might this connect to Greek theater's religious origins? Use one vocabulary term.",
      "time": "5 minutes"
    },
    "exit_ticket_section": {
      "header": "🎫 Exit Ticket (5 min)",
      "questions": [
        "1. Name & describe the THREE parts of a Greek theater.",
        "2. In one sentence: How is Greek theater connected to Dionysus?",
        "3. Why were theaters built into hillsides? What advantage?"
      ],
      "time": "5 minutes"
    }
  },
  "total_time_minutes": 10
}
```

---

## Quality Checklist

Before submission, verify:
- [ ] Journal prompt is open-ended (not yes/no)
- [ ] Journal prompt explicitly connects to today's content
- [ ] Journal prompt includes vocabulary reference opportunity
- [ ] Exit tickets number 2-3 questions
- [ ] Exit tickets assess stated learning objectives
- [ ] Exit tickets include variety of Bloom's levels
- [ ] Total time does not exceed 10 minutes
- [ ] Slide content is concise enough to display clearly

---

## Post-Generation Validation

This output passes through:
1. **Truncation Validator** - NO incomplete prompts/questions
2. **Structure Validator** - Required components present
3. **Timing Validator** - Fits 10-minute allocation

**FAILURE at any gate returns content for revision.**

---

**Agent Version:** 2.0 (Theater Pipeline)
**Last Updated:** 2026-01-08
