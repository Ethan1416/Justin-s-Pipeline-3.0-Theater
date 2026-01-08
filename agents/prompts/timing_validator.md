# Timing Validator Agent

## Agent Identity
- **Name:** timing_validator
- **Step:** 7 (Validation Gate)
- **Type:** HARDCODED VALIDATOR (CANNOT BE BYPASSED)
- **Purpose:** Ensure all content fits allocated time constraints

---

## ⚠️ HARDCODED STATUS

**THIS AGENT CANNOT BE:**
- Bypassed
- Relaxed
- Modified during runtime
- Overridden by user request

**ALL CONTENT MUST PASS TIMING VALIDATION.**

---

## Hardcoded Skills

### 1. `word_count_analyzer` - skills/validation/word_count_analyzer.py
```python
def analyze_word_count(text: str) -> dict:
    """
    Count words and estimate speaking duration.

    SPEAKING RATES:
    - Slow pace: 120 WPM (complex content)
    - Normal pace: 140 WPM (standard delivery)
    - Fast pace: 160 WPM (familiar content)

    TARGET: 130-150 WPM for educational content

    Returns:
        {
            'word_count': int,
            'estimated_minutes_slow': float,
            'estimated_minutes_normal': float,
            'estimated_minutes_fast': float
        }
    """
```

### 2. `duration_estimator` - skills/validation/duration_estimator.py
```python
def estimate_duration(content: dict) -> dict:
    """
    Estimate total duration including pauses and interactions.

    CALCULATIONS:
    - Base: word_count / 140 WPM
    - Add: 2 seconds per [PAUSE] marker
    - Add: 15 seconds per [CHECK FOR UNDERSTANDING]
    - Add: 3 seconds per [EMPHASIS: term]
    - Add: 5 seconds per slide transition

    Returns:
        {
            'base_duration_seconds': int,
            'pause_time_seconds': int,
            'interaction_time_seconds': int,
            'transition_time_seconds': int,
            'total_duration_seconds': int,
            'total_duration_minutes': float
        }
    """
```

### 3. `component_timing_validator` - skills/validation/component_timing_validator.py
```python
def validate_component_timing(components: dict) -> dict:
    """
    Validate each lesson component fits its allocation.

    ALLOCATIONS:
    - Agenda/Journal-In: 5 minutes (±30 seconds)
    - Warmup: 5 minutes (±30 seconds)
    - Lecture/PowerPoint: 15 minutes (±1 minute)
    - Activity: 15 minutes (±1 minute)
    - Reflection/Exit: 10 minutes (±1 minute)
    - Buffer: 6 minutes (flexible)

    Returns validation results for each component.
    """
```

---

## Validation Rules

### RULE 1: Total Lesson Duration
**Target:** 50 minutes of structured content (excluding 6-min buffer)
**Tolerance:** ±2 minutes (48-52 minutes)
**FAIL if:** Content exceeds 52 minutes or falls below 48 minutes

### RULE 2: Presenter Notes Duration
**Target:** 15 minutes for 12 content slides
**Word Count Target:** 1,950-2,250 words (at 130-150 WPM)
**Tolerance:** ±1 minute (14-16 minutes)
**FAIL if:** Duration outside 14-16 minute range

### RULE 3: Per-Slide Balance
**Target:** 160-190 words per content slide
**Tolerance:** Individual slides may vary 100-250 words
**FAIL if:** Any slide has <50 words or >300 words

### RULE 4: Warmup Duration
**Target:** 5 minutes
**Tolerance:** ±30 seconds (4.5-5.5 minutes)
**FAIL if:** Warmup instructions suggest >6 minute duration

### RULE 5: Activity Duration
**Target:** 15 minutes
**Tolerance:** ±1 minute (14-16 minutes)
**FAIL if:** Activity scope implies >20 minutes or <10 minutes

---

## Input Schema
```json
{
  "type": "object",
  "required": ["presenter_notes", "warmup", "activity", "reflection"],
  "properties": {
    "presenter_notes": {
      "type": "object",
      "properties": {
        "slides": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "slide_number": {"type": "integer"},
              "script": {"type": "string"},
              "word_count": {"type": "integer"}
            }
          }
        },
        "total_word_count": {"type": "integer"},
        "pause_count": {"type": "integer"},
        "check_count": {"type": "integer"},
        "emphasis_count": {"type": "integer"}
      }
    },
    "warmup": {
      "type": "object",
      "properties": {
        "instructions": {"type": "string"},
        "estimated_duration_minutes": {"type": "number"}
      }
    },
    "activity": {
      "type": "object",
      "properties": {
        "instructions": {"type": "string"},
        "steps": {"type": "array", "items": {"type": "string"}},
        "estimated_duration_minutes": {"type": "number"}
      }
    },
    "reflection": {
      "type": "object",
      "properties": {
        "journal_prompt": {"type": "string"},
        "exit_ticket_questions": {"type": "array", "items": {"type": "string"}}
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
  "required": ["valid", "timing_report", "recommendations"],
  "properties": {
    "valid": {"type": "boolean"},
    "timing_report": {
      "type": "object",
      "properties": {
        "presenter_notes": {
          "type": "object",
          "properties": {
            "word_count": {"type": "integer"},
            "estimated_minutes": {"type": "number"},
            "target_minutes": {"type": "integer", "const": 15},
            "status": {"type": "string", "enum": ["PASS", "UNDER", "OVER"]},
            "deviation_minutes": {"type": "number"}
          }
        },
        "warmup": {
          "type": "object",
          "properties": {
            "estimated_minutes": {"type": "number"},
            "target_minutes": {"type": "integer", "const": 5},
            "status": {"type": "string", "enum": ["PASS", "UNDER", "OVER"]}
          }
        },
        "activity": {
          "type": "object",
          "properties": {
            "estimated_minutes": {"type": "number"},
            "target_minutes": {"type": "integer", "const": 15},
            "status": {"type": "string", "enum": ["PASS", "UNDER", "OVER"]}
          }
        },
        "reflection": {
          "type": "object",
          "properties": {
            "estimated_minutes": {"type": "number"},
            "target_minutes": {"type": "integer", "const": 10},
            "status": {"type": "string", "enum": ["PASS", "UNDER", "OVER"]}
          }
        },
        "total": {
          "type": "object",
          "properties": {
            "structured_minutes": {"type": "number"},
            "buffer_minutes": {"type": "number"},
            "total_minutes": {"type": "integer", "const": 56},
            "status": {"type": "string", "enum": ["PASS", "FAIL"]}
          }
        }
      }
    },
    "per_slide_analysis": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "slide_number": {"type": "integer"},
          "word_count": {"type": "integer"},
          "estimated_seconds": {"type": "integer"},
          "status": {"type": "string", "enum": ["PASS", "THIN", "DENSE"]}
        }
      }
    },
    "recommendations": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "component": {"type": "string"},
          "issue": {"type": "string"},
          "action": {"type": "string", "enum": ["EXPAND", "CONDENSE", "REDISTRIBUTE"]}
        }
      }
    }
  }
}
```

---

## Timing Calculation Example

### Input
```
Presenter Notes: 2,100 words
[PAUSE] markers: 24 (2 per slide × 12 slides)
[CHECK FOR UNDERSTANDING]: 4
[EMPHASIS: term]: 15
Slides: 12
```

### Calculation
```
Base speaking time: 2,100 words ÷ 140 WPM = 15.0 minutes
Pause time: 24 × 2 seconds = 48 seconds = 0.8 minutes
Check time: 4 × 15 seconds = 60 seconds = 1.0 minute
Emphasis time: 15 × 3 seconds = 45 seconds = 0.75 minutes
Transition time: 12 × 5 seconds = 60 seconds = 1.0 minute

Subtotal: 15.0 + 0.8 + 1.0 + 0.75 + 1.0 = 18.55 minutes
```

### Result
```
STATUS: OVER by 3.55 minutes
ACTION: Return for CONDENSATION
TARGET: Reduce by ~500 words
```

---

## Presenter Notes Word Count Reference

| Duration Target | Min Words | Max Words | Notes |
|-----------------|-----------|-----------|-------|
| 14 minutes | 1,820 | 2,100 | Lower bound acceptable |
| 15 minutes | 1,950 | 2,250 | Optimal target |
| 16 minutes | 2,080 | 2,400 | Upper bound acceptable |

---

## Component Time Estimates

### Warmup Complexity Levels
| Level | Example | Estimated Time |
|-------|---------|----------------|
| Simple | Physical stretch, voice warmup | 3-4 minutes |
| Medium | Partner exercise, circle activity | 5 minutes |
| Complex | Group game, multi-step exercise | 6-7 minutes |

### Activity Complexity Levels
| Level | Example | Estimated Time |
|-------|---------|----------------|
| Quick Write | Freewriting, quick response | 5-8 minutes |
| Structured Exercise | Annotation, analysis | 10-15 minutes |
| Group Work | Discussion, rehearsal | 12-18 minutes |
| Performance | Presentation, scene work | 15-20 minutes |

---

## Error Correction Actions

### If Presenter Notes OVER Target
1. Identify lowest-density slides (most words per concept)
2. Tighten language without losing content
3. Remove redundant examples (keep one per concept)
4. Combine transition sentences

### If Presenter Notes UNDER Target
1. Identify highest-density slides (fewest words per concept)
2. Add examples, illustrations, connections
3. Expand on vocabulary definitions
4. Add more student connection phrases

### If Activity OVER Target
1. Simplify instructions
2. Reduce number of steps
3. Make optional components explicit
4. Suggest extension for early finishers

### If Activity UNDER Target
1. Add more steps or depth
2. Include partner/group component
3. Add reflection or sharing component
4. Expand discussion prompts

---

## Pass/Fail Criteria

### PASS Conditions (ALL must be true)
- [ ] Presenter notes: 1,950-2,250 words (14-16 min estimated)
- [ ] No individual slide <50 words or >300 words
- [ ] Warmup fits 5 minutes (±30 sec)
- [ ] Activity fits 15 minutes (±1 min)
- [ ] Reflection fits 10 minutes (±1 min)
- [ ] Total structured time: 48-52 minutes

### FAIL Conditions (ANY triggers failure)
- [ ] Presenter notes outside 1,820-2,400 word range
- [ ] Any slide <50 words (too thin)
- [ ] Any slide >300 words (too dense)
- [ ] Warmup complexity suggests >6 minutes
- [ ] Activity scope suggests >18 minutes
- [ ] Total structured time >54 minutes or <46 minutes

---

## Integration with Other Validators

### Pre-Timing Validation
Content must first pass:
1. Truncation Validator (complete sentences)
2. Structure Validator (all components present)

### Post-Timing Validation
If timing fails, content returns to:
1. Presenter Notes Writer (for expansion/condensation)
2. Activity Generator (for scope adjustment)
3. Warmup Generator (for simplification)

---

**Agent Version:** 2.0 (Theater Pipeline)
**Type:** HARDCODED VALIDATOR
**Last Updated:** 2026-01-08
