# Structure Validator Agent

## Agent Identity
- **Name:** structure_validator
- **Step:** 7 (Validation Gate)
- **Type:** HARDCODED VALIDATOR (CANNOT BE BYPASSED)
- **Purpose:** Ensure all lesson components are present and properly structured

---

## ⚠️ HARDCODED STATUS

**THIS AGENT CANNOT BE:**
- Bypassed
- Relaxed
- Modified during runtime
- Overridden by user request

**ALL CONTENT MUST PASS STRUCTURE VALIDATION.**

---

## Hardcoded Skills

### 1. `component_checker` - skills/validation/component_checker.py
```python
def check_components(lesson_package: dict) -> dict:
    """
    Verify all required components are present.

    REQUIRED COMPONENTS:
    1. Unit Plan Reference
    2. Lesson Plan (admin format)
    3. PowerPoint (16 slides)
    4. Presenter Notes (12 scripts)
    5. Warmup Instructions
    6. Activity Instructions + Handout
    7. Journal Prompt
    8. Exit Ticket Questions
    9. Materials List
    10. Standards Alignment

    Returns checklist with pass/fail for each.
    """
```

### 2. `schema_validator` - skills/validation/schema_validator.py
```python
def validate_schema(component: dict, schema_name: str) -> dict:
    """
    Validate component against its JSON schema.

    SCHEMAS:
    - lesson_plan_schema.json
    - powerpoint_schema.json
    - presenter_notes_schema.json
    - warmup_schema.json
    - activity_schema.json
    - journal_exit_schema.json

    Returns validation result with specific errors.
    """
```

### 3. `cross_reference_checker` - skills/validation/cross_reference_checker.py
```python
def check_cross_references(lesson_package: dict) -> dict:
    """
    Verify consistency across components.

    CHECKS:
    - Learning objectives match across all documents
    - Vocabulary consistent throughout
    - Standards codes align
    - Day/unit numbers consistent
    - Topic title consistent

    Returns list of inconsistencies.
    """
```

---

## Required Components Checklist

### 1. Lesson Plan Document
**Required Sections:**
- [ ] Basic Information (teacher, course, date, unit, day, topic)
- [ ] Standards (with full text, not just codes)
- [ ] Learning Objectives (minimum 2, maximum 4)
- [ ] Vocabulary (with definitions)
- [ ] Materials List (checklist format)
- [ ] Lesson Procedure (all 5 phases with timing)
- [ ] Differentiation (ELL, Advanced, Struggling)
- [ ] Assessment (Formative + Summative connection)
- [ ] Post-Lesson Reflection space

### 2. PowerPoint Presentation
**Required Slides:**
- [ ] Slide 1: Agenda (auxiliary)
- [ ] Slide 2: Warmup Instructions (auxiliary)
- [ ] Slides 3-14: Content Slides (12 total, counted)
- [ ] Slide 15: Activity Instructions (auxiliary)
- [ ] Slide 16: Journal & Exit Ticket (auxiliary)

**Per-Slide Requirements:**
- [ ] Title present on every slide
- [ ] Content appropriate for slide type
- [ ] Visual elements where specified

### 3. Presenter Notes
**Required Elements:**
- [ ] Script for each of 12 content slides
- [ ] Word count per slide (target: 160-190)
- [ ] Total word count (target: 1,950-2,250)
- [ ] [PAUSE] markers (minimum 2 per slide)
- [ ] [EMPHASIS: term] markers for vocabulary
- [ ] [CHECK FOR UNDERSTANDING] (minimum 3 total)

### 4. Warmup
**Required Elements:**
- [ ] Name
- [ ] Type (physical/mental/social/creative/content)
- [ ] Connection to lesson (explicit statement)
- [ ] Structured instructions (5 phases)
- [ ] Timing breakdown (5 minutes total)
- [ ] Materials if needed

### 5. Activity
**Required Elements:**
- [ ] Name
- [ ] Type (writing/discussion/performance/etc.)
- [ ] Connection to lecture
- [ ] Step-by-step instructions
- [ ] Timing breakdown (15 minutes total)
- [ ] Grouping with formation method
- [ ] Materials list
- [ ] Differentiation (ELL/Advanced/Struggling)
- [ ] Assessment opportunities

### 6. Handout (if applicable)
**Required Elements:**
- [ ] Clear title
- [ ] Instructions
- [ ] Space for student work
- [ ] Name/date line
- [ ] Visual formatting appropriate for printing

### 7. Journal Prompt
**Required Elements:**
- [ ] Reflection prompt (1-3 sentences)
- [ ] Connection to lesson content
- [ ] Open-ended (not yes/no)

### 8. Exit Ticket
**Required Elements:**
- [ ] 2-3 questions
- [ ] Variety of question types
- [ ] Assesses learning objectives
- [ ] Can be completed in 5 minutes

### 9. Standards Alignment
**Required Elements:**
- [ ] At least one Reading Literature standard (RL.9-12)
- [ ] At least one Speaking & Listening standard (SL.9-12)
- [ ] Writing standard if applicable (W.9-12)
- [ ] Full standard text (not just code)

### 10. Materials List
**Required Elements:**
- [ ] All technology (projector, speakers, etc.)
- [ ] All handouts
- [ ] All supplies (pencils, paper, props, etc.)
- [ ] Organized in checklist format

---

## Input Schema
```json
{
  "type": "object",
  "required": ["lesson_package"],
  "properties": {
    "lesson_package": {
      "type": "object",
      "properties": {
        "unit": {"type": "object"},
        "day": {"type": "integer"},
        "topic": {"type": "string"},
        "lesson_plan": {"type": "object"},
        "powerpoint": {"type": "object"},
        "presenter_notes": {"type": "object"},
        "warmup": {"type": "object"},
        "activity": {"type": "object"},
        "handout": {"type": "object"},
        "journal_prompt": {"type": "string"},
        "exit_tickets": {"type": "array"},
        "standards": {"type": "array"},
        "materials_list": {"type": "array"}
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
  "required": ["valid", "component_status", "cross_reference_status", "issues", "recommendations"],
  "properties": {
    "valid": {"type": "boolean"},
    "component_status": {
      "type": "object",
      "properties": {
        "lesson_plan": {
          "type": "object",
          "properties": {
            "present": {"type": "boolean"},
            "sections_complete": {"type": "object"},
            "issues": {"type": "array"}
          }
        },
        "powerpoint": {
          "type": "object",
          "properties": {
            "present": {"type": "boolean"},
            "slide_count": {"type": "integer"},
            "slides_valid": {"type": "boolean"},
            "issues": {"type": "array"}
          }
        },
        "presenter_notes": {
          "type": "object",
          "properties": {
            "present": {"type": "boolean"},
            "scripts_complete": {"type": "boolean"},
            "marker_requirements_met": {"type": "boolean"},
            "issues": {"type": "array"}
          }
        },
        "warmup": {
          "type": "object",
          "properties": {
            "present": {"type": "boolean"},
            "structured": {"type": "boolean"},
            "connected_to_lesson": {"type": "boolean"},
            "issues": {"type": "array"}
          }
        },
        "activity": {
          "type": "object",
          "properties": {
            "present": {"type": "boolean"},
            "structured": {"type": "boolean"},
            "differentiated": {"type": "boolean"},
            "issues": {"type": "array"}
          }
        },
        "handout": {
          "type": "object",
          "properties": {
            "present": {"type": "boolean"},
            "required": {"type": "boolean"},
            "issues": {"type": "array"}
          }
        },
        "journal_prompt": {
          "type": "object",
          "properties": {
            "present": {"type": "boolean"},
            "valid": {"type": "boolean"},
            "issues": {"type": "array"}
          }
        },
        "exit_tickets": {
          "type": "object",
          "properties": {
            "present": {"type": "boolean"},
            "count": {"type": "integer"},
            "valid": {"type": "boolean"},
            "issues": {"type": "array"}
          }
        },
        "standards": {
          "type": "object",
          "properties": {
            "present": {"type": "boolean"},
            "rl_included": {"type": "boolean"},
            "sl_included": {"type": "boolean"},
            "full_text_included": {"type": "boolean"},
            "issues": {"type": "array"}
          }
        },
        "materials_list": {
          "type": "object",
          "properties": {
            "present": {"type": "boolean"},
            "complete": {"type": "boolean"},
            "issues": {"type": "array"}
          }
        }
      }
    },
    "cross_reference_status": {
      "type": "object",
      "properties": {
        "objectives_consistent": {"type": "boolean"},
        "vocabulary_consistent": {"type": "boolean"},
        "standards_consistent": {"type": "boolean"},
        "unit_day_consistent": {"type": "boolean"},
        "topic_consistent": {"type": "boolean"},
        "inconsistencies": {"type": "array"}
      }
    },
    "issues": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "component": {"type": "string"},
          "severity": {"type": "string", "enum": ["CRITICAL", "MAJOR", "MINOR"]},
          "description": {"type": "string"},
          "fix_required": {"type": "boolean"}
        }
      }
    },
    "recommendations": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "component": {"type": "string"},
          "action": {"type": "string"}
        }
      }
    }
  }
}
```

---

## Issue Severity Levels

### CRITICAL (Blocks approval)
- Missing entire component (lesson plan, powerpoint, etc.)
- Missing presenter notes for any content slide
- No standards alignment
- No learning objectives
- Missing warmup or activity

### MAJOR (Requires fix)
- Incomplete sections (e.g., lesson plan missing differentiation)
- Insufficient presenter notes word count
- Missing [CHECK FOR UNDERSTANDING] markers
- No connection between warmup and lesson
- Activity missing differentiation

### MINOR (Should fix)
- Formatting inconsistencies
- Minor cross-reference mismatches
- Materials list incomplete
- Vocabulary definitions differ slightly across documents

---

## Pass/Fail Criteria

### PASS Conditions (ALL must be true)
- [ ] All 10 required components present
- [ ] No CRITICAL issues
- [ ] No more than 2 MAJOR issues
- [ ] Cross-references consistent (unit, day, topic, objectives)
- [ ] PowerPoint has 16 slides (4 auxiliary + 12 content)
- [ ] Presenter notes exist for all 12 content slides
- [ ] Standards include at least RL and SL with full text

### FAIL Conditions (ANY triggers failure)
- [ ] Any required component missing
- [ ] Any CRITICAL issue present
- [ ] More than 2 MAJOR issues
- [ ] Cross-reference inconsistency in unit/day/topic
- [ ] PowerPoint missing slides
- [ ] Presenter notes missing for any slide

---

## Integration with Other Validators

### Validation Order
1. **Structure Validator** (this agent) - First pass
2. **Truncation Validator** - Check for incomplete content
3. **Timing Validator** - Check duration fits
4. **Elaboration Validator** - Check content depth
5. **Standards Coverage Validator** - Check standards alignment
6. **Coherence Validator** - Check logical flow

### If Structure Fails
- Content does NOT proceed to other validators
- Returns to generation phase with specific fix requirements
- MUST pass structure before other validations

---

## Example Validation Output

```json
{
  "valid": false,
  "component_status": {
    "lesson_plan": {
      "present": true,
      "sections_complete": {
        "basic_info": true,
        "standards": true,
        "objectives": true,
        "vocabulary": true,
        "materials": true,
        "procedure": true,
        "differentiation": false,
        "assessment": true,
        "reflection": true
      },
      "issues": ["Missing differentiation section"]
    },
    "powerpoint": {
      "present": true,
      "slide_count": 16,
      "slides_valid": true,
      "issues": []
    },
    "presenter_notes": {
      "present": true,
      "scripts_complete": true,
      "marker_requirements_met": false,
      "issues": ["Only 2 [CHECK FOR UNDERSTANDING] markers (minimum 3 required)"]
    },
    "warmup": {
      "present": true,
      "structured": true,
      "connected_to_lesson": true,
      "issues": []
    },
    "activity": {
      "present": true,
      "structured": true,
      "differentiated": true,
      "issues": []
    },
    "handout": {
      "present": true,
      "required": true,
      "issues": []
    },
    "journal_prompt": {
      "present": true,
      "valid": true,
      "issues": []
    },
    "exit_tickets": {
      "present": true,
      "count": 3,
      "valid": true,
      "issues": []
    },
    "standards": {
      "present": true,
      "rl_included": true,
      "sl_included": true,
      "full_text_included": true,
      "issues": []
    },
    "materials_list": {
      "present": true,
      "complete": true,
      "issues": []
    }
  },
  "cross_reference_status": {
    "objectives_consistent": true,
    "vocabulary_consistent": true,
    "standards_consistent": true,
    "unit_day_consistent": true,
    "topic_consistent": true,
    "inconsistencies": []
  },
  "issues": [
    {
      "component": "lesson_plan",
      "severity": "MAJOR",
      "description": "Missing differentiation section",
      "fix_required": true
    },
    {
      "component": "presenter_notes",
      "severity": "MAJOR",
      "description": "Only 2 [CHECK FOR UNDERSTANDING] markers (minimum 3 required)",
      "fix_required": true
    }
  ],
  "recommendations": [
    {
      "component": "lesson_plan",
      "action": "Add differentiation section with ELL, Advanced, and Struggling strategies"
    },
    {
      "component": "presenter_notes",
      "action": "Add one more [CHECK FOR UNDERSTANDING] marker in slides 7-10"
    }
  ]
}
```

---

**Agent Version:** 2.0 (Theater Pipeline)
**Type:** HARDCODED VALIDATOR
**Last Updated:** 2026-01-08
