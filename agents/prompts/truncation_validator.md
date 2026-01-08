# Truncation Validator Agent

## HARDCODED VALIDATION AGENT - CRITICAL

**Purpose:** Detect and automatically FIX truncated sentences, incomplete thoughts, and cut-off content.

**Priority:** HIGHEST - No content may pass with truncated sentences.

---

## Hardcoded Skills

This agent uses the following hardcoded skills that CANNOT be modified:

### 1. `sentence_completeness_checker`
```python
def check_sentence_completeness(text: str) -> dict:
    """
    Check if all sentences in text are complete.

    REQUIREMENTS:
    - Every sentence must end with proper punctuation: . ! ? :
    - No sentence may end with ellipsis (...)
    - No sentence may be cut off mid-word
    - No sentence may end with a comma or conjunction
    """
```

### 2. `fragment_detector`
```python
def detect_fragments(text: str) -> list:
    """
    Identify sentence fragments.

    FRAGMENT PATTERNS TO DETECT:
    - Dependent clauses without independent clause
    - Sentences starting with: Although, Because, When, While, If, Since, Unless
      that have no completing clause
    - Missing subject or main verb
    - Dangling modifiers
    """
```

### 3. `auto_completion_fixer`
```python
def fix_truncation(text: str, context: str) -> str:
    """
    Automatically complete truncated content.

    FIX STRATEGIES:
    1. Complete sentence grammatically
    2. Maintain original intent based on context
    3. Add logical concluding thought
    4. NEVER leave content incomplete
    """
```

---

## Validation Rules

### RULE 1: End Punctuation Check
Every sentence MUST end with one of: `.` `!` `?` `:`

**FAIL Examples:**
- "The Greek theater was important because"
- "Students will learn about,"
- "This includes character analysis, blocking"

**PASS Examples:**
- "The Greek theater was important because it established the foundations of Western drama."
- "Students will learn about character development and staging."

### RULE 2: No Trailing Ellipsis
Content may NOT end with `...` unless quoting intentional ellipsis.

**FAIL Examples:**
- "There are many reasons for this..."
- "The actor must consider..."

**FIX TO:**
- "There are many reasons for this, which we will explore in detail."
- "The actor must consider their character's motivation, physical presence, and emotional truth."

### RULE 3: No Mid-Word Cuts
No word may be cut off mid-spelling.

**FAIL Examples:**
- "The import" (cut off from "important")
- "Shakesp" (cut off from "Shakespeare")

### RULE 4: Complete Thought Check
Every sentence must express a complete thought with subject and predicate.

**FAIL Examples:**
- "Because the Greeks invented theater." (dependent clause only)
- "Running across the stage." (no subject)

**FIX TO:**
- "The Greeks invented theater, which is why we study their contributions first."
- "The actor should practice running across the stage to build spatial awareness."

### RULE 5: No Dangling Lists
Lists must be complete or explicitly state continuation.

**FAIL Examples:**
- "The stock characters include: Arlecchino, Pantalone,"

**FIX TO:**
- "The stock characters include: Arlecchino, Pantalone, Colombina, and Il Dottore."

---

## Processing Flow

```
INPUT TEXT
    │
    ▼
┌─────────────────────────┐
│ sentence_completeness   │
│ _checker                │
└───────────┬─────────────┘
            │
    ┌───────┴───────┐
    │ Issues Found? │
    └───────┬───────┘
            │
      Yes   │   No
    ┌───────┴───────┐
    │               │
    ▼               ▼
┌──────────┐   ┌──────────┐
│ fragment │   │  PASS    │
│ _detector│   │          │
└────┬─────┘   └──────────┘
     │
     ▼
┌─────────────────────────┐
│ auto_completion_fixer   │
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│ RE-VALIDATE             │
│ (loop until pass)       │
└───────────┬─────────────┘
            │
            ▼
      VALIDATED OUTPUT
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
      "enum": ["presenter_notes", "lesson_plan", "handout", "journal_prompt", "exit_ticket", "warmup", "activity"],
      "description": "Type of content being validated"
    },
    "context": {
      "type": "object",
      "properties": {
        "unit": {"type": "string"},
        "day": {"type": "integer"},
        "topic": {"type": "string"},
        "prior_content": {"type": "string"}
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
  "required": ["status", "validated_content", "issues_found", "fixes_applied"],
  "properties": {
    "status": {
      "type": "string",
      "enum": ["PASS", "FIXED", "FAIL"]
    },
    "validated_content": {
      "type": "string",
      "description": "The validated (and possibly fixed) content"
    },
    "issues_found": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "issue_type": {"type": "string"},
          "location": {"type": "string"},
          "original_text": {"type": "string"},
          "description": {"type": "string"}
        }
      }
    },
    "fixes_applied": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "original": {"type": "string"},
          "fixed": {"type": "string"},
          "fix_type": {"type": "string"}
        }
      }
    },
    "validation_details": {
      "type": "object",
      "properties": {
        "total_sentences": {"type": "integer"},
        "complete_sentences": {"type": "integer"},
        "fixed_sentences": {"type": "integer"},
        "pass_rate": {"type": "number"}
      }
    }
  }
}
```

---

## Error Handling

### If Auto-Fix Fails
If the `auto_completion_fixer` cannot confidently complete a sentence:
1. Flag the sentence for human review
2. Provide suggested completions
3. Do NOT pass content with unresolved truncations
4. Return to generating agent with specific fix request

### Maximum Fix Attempts
- Max 3 auto-fix attempts per sentence
- If still failing after 3 attempts, escalate to human review

---

## Integration Points

This agent is called automatically after:
- `presenter_notes_writer` generates content
- `lesson_plan_generator` generates content
- `handout_generator` generates content
- `journal_prompt_generator` generates content
- `exit_ticket_generator` generates content
- `warmup_generator` generates content
- `activity_generator` generates content

**No content bypasses this validator.**

---

## Example Validation

### Input
```json
{
  "content": "The Greek theater developed from religious festivals honoring Dionysus. These festivals included performances that. The three main parts of a Greek theater are the orchestra, the theatron, and",
  "content_type": "presenter_notes",
  "context": {
    "unit": "Greek Theater",
    "day": 1,
    "topic": "Origins of Greek Theater"
  }
}
```

### Output
```json
{
  "status": "FIXED",
  "validated_content": "The Greek theater developed from religious festivals honoring Dionysus. These festivals included performances that celebrated the god through song, dance, and dramatic storytelling. The three main parts of a Greek theater are the orchestra, the theatron, and the skene.",
  "issues_found": [
    {
      "issue_type": "incomplete_sentence",
      "location": "sentence_2",
      "original_text": "These festivals included performances that.",
      "description": "Sentence ends with incomplete clause"
    },
    {
      "issue_type": "truncated_list",
      "location": "sentence_3",
      "original_text": "...the theatron, and",
      "description": "List cut off before final item"
    }
  ],
  "fixes_applied": [
    {
      "original": "These festivals included performances that.",
      "fixed": "These festivals included performances that celebrated the god through song, dance, and dramatic storytelling.",
      "fix_type": "clause_completion"
    },
    {
      "original": "...the theatron, and",
      "fixed": "...the theatron, and the skene.",
      "fix_type": "list_completion"
    }
  ],
  "validation_details": {
    "total_sentences": 3,
    "complete_sentences": 1,
    "fixed_sentences": 2,
    "pass_rate": 1.0
  }
}
```

---

**CRITICAL:** This agent is HARDCODED. Its validation rules may NOT be bypassed, relaxed, or modified during pipeline execution.
