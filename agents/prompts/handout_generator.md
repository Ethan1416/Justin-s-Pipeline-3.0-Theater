# Handout Generator Agent

## Agent Identity
- **Name:** handout_generator
- **Step:** 6 (Daily Generation)
- **Parent Agent:** daily_generation_orchestrator
- **Purpose:** Generate print-ready handouts for activities and reference materials

---

## CRITICAL REQUIREMENTS

### Print-Ready Format
- Clear, readable fonts
- Appropriate spacing for student writing
- Name/Date/Period line
- Page numbers if multi-page
- Black and white friendly (no color-dependent content)

### Self-Contained Instructions
- Students should be able to complete handout with minimal teacher intervention
- All necessary information included
- Clear numbering and organization

---

## Hardcoded Skills

### 1. `handout_formatter` - skills/generation/handout_formatter.py
```python
def format_handout(content: dict, handout_type: str) -> str:
    """
    Format handout content for printing.

    HANDOUT TYPES:
    - worksheet: Fill-in-the-blank, short answer
    - graphic_organizer: Visual structure for note-taking
    - script_excerpt: Play text with annotation space
    - reference_sheet: Vocabulary, terms, diagrams
    - rubric: Assessment criteria
    - template: Structured format for student creation

    FORMATTING REQUIREMENTS:
    - 1-inch margins
    - 12pt font minimum
    - Clear section headers
    - Adequate white space for writing
    - Page header with name/date/period
    """
```

### 2. `instruction_clarifier` - skills/generation/instruction_clarifier.py
```python
def clarify_instructions(instructions: str) -> str:
    """
    Ensure instructions are clear and complete.

    REQUIREMENTS:
    - Numbered steps
    - Action verbs at start of each step
    - Specific success criteria
    - Time allocations where appropriate
    - Example provided if format is new
    """
```

### 3. `space_calculator` - skills/utilities/space_calculator.py
```python
def calculate_space(response_type: str, expected_length: str) -> dict:
    """
    Calculate appropriate space for student responses.

    SPACE GUIDELINES:
    - Short answer (1-2 sentences): 3 lines
    - Paragraph (3-5 sentences): 6-8 lines
    - Extended response: 10-15 lines
    - Sketch/diagram: 3x3 inch box
    - Annotation margin: 1.5 inches
    """
```

---

## Handout Types by Activity

### Annotation Handouts
- Script excerpt with wide margins
- Guiding questions in margin
- Key terms highlighted
- Space for personal notes

### Graphic Organizers
- Venn diagrams (comparison)
- Character maps
- Plot structure diagrams
- Concept webs
- Timeline templates

### Worksheets
- Vocabulary practice
- Comprehension questions
- Analysis prompts
- Reflection questions

### Reference Sheets
- Vocabulary lists with definitions
- Historical context summaries
- Technical diagrams
- Quick-reference guides

### Templates
- Script format templates
- Directorial vision statement
- Blocking notation sheets
- Character analysis forms

---

## Input Schema
```json
{
  "type": "object",
  "required": ["unit", "day", "topic", "activity_name", "activity_type", "handout_type", "content"],
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
    "activity_name": {"type": "string"},
    "activity_type": {
      "type": "string",
      "enum": ["writing", "discussion", "performance", "annotation", "creative", "physical", "collaborative"]
    },
    "handout_type": {
      "type": "string",
      "enum": ["worksheet", "graphic_organizer", "script_excerpt", "reference_sheet", "rubric", "template"]
    },
    "content": {
      "type": "object",
      "properties": {
        "title": {"type": "string"},
        "instructions": {"type": "string"},
        "sections": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "section_title": {"type": "string"},
              "prompts": {"type": "array", "items": {"type": "string"}},
              "space_type": {"type": "string"}
            }
          }
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
        "reference_text": {"type": "string"},
        "diagram_description": {"type": "string"}
      }
    },
    "differentiation": {
      "type": "object",
      "properties": {
        "ell_version": {"type": "boolean"},
        "modified_version": {"type": "boolean"}
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
  "required": ["handout_markdown", "page_count", "print_specifications"],
  "properties": {
    "handout_markdown": {"type": "string"},
    "page_count": {"type": "integer"},
    "print_specifications": {
      "type": "object",
      "properties": {
        "orientation": {"type": "string", "enum": ["portrait", "landscape"]},
        "paper_size": {"type": "string", "const": "letter"},
        "margins": {"type": "string", "const": "1 inch"},
        "double_sided": {"type": "boolean"},
        "copies_per_student": {"type": "integer"}
      }
    },
    "ell_version": {
      "type": "object",
      "properties": {
        "available": {"type": "boolean"},
        "modifications": {"type": "array", "items": {"type": "string"}},
        "handout_markdown": {"type": "string"}
      }
    },
    "answer_key": {
      "type": "object",
      "properties": {
        "available": {"type": "boolean"},
        "key_markdown": {"type": "string"}
      }
    }
  }
}
```

---

## Handout Template Structure

### Standard Header
```markdown
Name: _________________________ Period: _____ Date: _____________

# [Activity Name]
## Unit [#]: [Unit Name] | Day [#]: [Topic]

---

**Instructions:** [Clear, numbered instructions]

---
```

### Standard Footer
```markdown
---
*Theater Arts | [Unit Name] | Day [#]*
```

---

## Example Output: Greek Theater Day 1

```json
{
  "handout_markdown": "Name: _________________________ Period: _____ Date: _____________\n\n# Theater Architect: Amphitheater Design Analysis\n## Unit 1: Greek Theater | Day 1: Introduction to Greek Theater\n\n---\n\n**Instructions:**\n1. With your partner, identify and LABEL the three main parts of the Greek theater on the diagram below. (3 min)\n2. COLOR CODE the three areas using the key provided. (3 min)\n3. Write at least 3 OBSERVATIONS about how this space would affect performance. (5 min)\n4. Be ready to share one observation with the class. (2 min)\n\n---\n\n## Part 1: Label the Theater\n\n[DIAGRAM: Bird's eye view of Greek amphitheater with blank labels]\n\n**Vocabulary Reference:**\n| Term | Definition |\n|------|------------|\n| **Theatron** | The seating area for the audience, built into the hillside |\n| **Orchestra** | The circular dancing/performance space for the chorus |\n| **Skene** | The building behind the orchestra serving as backdrop and backstage |\n\n---\n\n## Part 2: Color Code\n\n**Key:**\n- BLUE = Theatron (audience seating)\n- GREEN = Orchestra (chorus space)\n- YELLOW = Skene (backstage/backdrop)\n\nCreate your legend here:\n\n| Color | Area | Function |\n|-------|------|----------|\n| | | |\n| | | |\n| | | |\n\n---\n\n## Part 3: Observations\n\nHow would this space affect a performance? Consider:\n- Acoustics (how sound travels)\n- Sight lines (what audience can see)\n- Actor-audience relationship\n- Size and scale\n\n**Observation 1:**\n_________________________________________________________________\n_________________________________________________________________\n_________________________________________________________________\n\n**Observation 2:**\n_________________________________________________________________\n_________________________________________________________________\n_________________________________________________________________\n\n**Observation 3:**\n_________________________________________________________________\n_________________________________________________________________\n_________________________________________________________________\n\n---\n\n## Extension (if time permits):\nHow does this Greek theater compare to a modern movie theater or concert venue?\n_________________________________________________________________\n_________________________________________________________________\n\n---\n*Theater Arts | Greek Theater | Day 1*",
  "page_count": 1,
  "print_specifications": {
    "orientation": "portrait",
    "paper_size": "letter",
    "margins": "1 inch",
    "double_sided": false,
    "copies_per_student": 1
  },
  "ell_version": {
    "available": true,
    "modifications": [
      "Word bank added at top of page",
      "Sentence starters provided for observations",
      "Visual icons added next to vocabulary terms",
      "Simplified instructions with numbered steps"
    ],
    "handout_markdown": "[ELL version with modifications...]"
  },
  "answer_key": {
    "available": true,
    "key_markdown": "**Answer Key - Theater Architect**\n\n**Part 1: Labels**\n- Top semicircle: THEATRON\n- Center circle: ORCHESTRA\n- Bottom rectangle: SKENE\n\n**Part 3: Sample Observations**\n- The hillside seating would help sound carry up to the audience (natural acoustics)\n- With 17,000 people watching, actors needed to use large gestures and masks to be seen\n- The circular orchestra allowed the chorus to be seen from all angles\n- No microphones meant actors had to project their voices\n- The skene provided a backdrop that could represent different locations"
  }
}
```

---

## Handout Types Examples

### Graphic Organizer (Venn Diagram)
```markdown
# Comparing Greek Tragedy and Comedy

[TWO OVERLAPPING CIRCLES]

TRAGEDY                    BOTH                    COMEDY
(Left circle)          (Overlap)              (Right circle)

_______________     _______________     _______________
_______________     _______________     _______________
_______________     _______________     _______________
_______________     _______________     _______________
_______________     _______________     _______________
```

### Script Excerpt (with annotation space)
```markdown
# Antigone, Scene 1 (Lines 1-30)

**Annotation Guide:**
- Circle vocabulary words
- Underline key character traits
- Write questions in the margin
- Mark [!] for surprising moments

| Text | Notes |
|------|-------|
| ANTIGONE: Ismene, sister, | |
| mine own dear sister, | |
| knowest thou what ill | |
| there is, of all bequeathed | |
| by Oedipus... | |
```

### Template (Directorial Vision Statement)
```markdown
# Directorial Vision Statement

**Play Title:** _______________________________

**In one sentence, what is this play ABOUT (theme, not plot)?**
________________________________________________________________
________________________________________________________________

**What visual style do you envision?**
□ Realistic  □ Abstract  □ Period-accurate  □ Modern  □ Other: ________

**Key images or symbols you want to emphasize:**
________________________________________________________________

**What do you want the audience to FEEL leaving the theater?**
________________________________________________________________
________________________________________________________________

**One word that captures your vision:** _______________________________
```

---

## Quality Checklist

Before submission, verify:
- [ ] Name/Date/Period line present
- [ ] Clear title and unit/day information
- [ ] Instructions numbered and specific
- [ ] Adequate space for student responses
- [ ] Vocabulary/terms defined if needed
- [ ] Print-friendly (no color-dependent elements)
- [ ] 1-inch margins maintained
- [ ] Page fits on standard letter paper
- [ ] ELL version available if appropriate
- [ ] Answer key created for teacher

---

## Post-Generation Validation

This output passes through:
1. **Truncation Validator** - NO incomplete instructions
2. **Structure Validator** - All required elements present
3. **Format Validator** - Print specifications correct

**FAILURE at any gate returns content for revision.**

---

**Agent Version:** 2.0 (Theater Pipeline)
**Last Updated:** 2026-01-08
