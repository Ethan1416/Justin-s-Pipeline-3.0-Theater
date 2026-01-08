# Lesson Assembler

## Purpose
Combine all daily lesson components into a complete, production-ready lesson package. Merges lesson plan, warmup, PowerPoint blueprint, presenter notes, activity, handouts, journal prompts, and exit tickets into a unified deliverable.

## HARDCODED SKILLS
```yaml
skills:
  - word_count_analyzer
  - sentence_completeness_checker
```

## Pipeline Position
**Phase 4: Assembly** - Runs after all validation gates pass

```
┌─────────────────────────────────────────────────────────────────┐
│                       ASSEMBLY PHASE                             │
├─────────────────────────────────────────────────────────────────┤
│  ╔═══════════════════════╗                                      │
│  ║   LESSON ASSEMBLER    ║  ← YOU ARE HERE                      │
│  ╚═══════════════════════╝                                      │
│           ↓                                                     │
│  ┌───────────────────────┐                                      │
│  │ POWERPOINT ASSEMBLER  │                                      │
│  └───────────────────────┘                                      │
│           ↓                                                     │
│  ┌───────────────────────┐                                      │
│  │ UNIT FOLDER ORGANIZER │                                      │
│  └───────────────────────┘                                      │
│           ↓                                                     │
│  ┌───────────────────────┐                                      │
│  │ FINAL QA REPORTER     │                                      │
│  └───────────────────────┘                                      │
└─────────────────────────────────────────────────────────────────┘
```

---

## Input Schema
```json
{
  "lesson_metadata": {
    "unit_number": 1,
    "unit_name": "Greek Theater",
    "day": 5,
    "topic": "The Theatron and Orchestra",
    "date_generated": "2026-01-08"
  },
  "components": {
    "lesson_plan": {
      "admin_format": {...},
      "timing_breakdown": {...}
    },
    "warmup": {
      "name": "Greek Chorus Walk",
      "type": "physical",
      "duration": 5,
      "instructions": [...],
      "connection": "..."
    },
    "powerpoint_blueprint": {
      "slides": [...],
      "total_slides": 16
    },
    "presenter_notes": {
      "per_slide": [...],
      "total_words": 2100,
      "duration_minutes": 15
    },
    "activity": {
      "name": "Theater Blueprint Analysis",
      "type": "gallery_walk",
      "duration": 15,
      "instructions": {...},
      "materials": [...]
    },
    "handouts": [
      {
        "name": "Greek Theater Diagram",
        "type": "worksheet",
        "content": "..."
      }
    ],
    "journal_prompt": "How might the design of the Greek theater have affected the performance style of actors?",
    "exit_ticket": {
      "question": "Label the three main parts of a Greek theater on a blank diagram.",
      "format": "diagram_labeling"
    }
  },
  "validation_results": {
    "truncation": {"passed": true, "score": 100},
    "structure": {"passed": true, "score": 100},
    "elaboration": {"passed": true, "score": 88},
    "timing": {"passed": true, "score": 95}
  }
}
```

## Output Schema
```json
{
  "lesson_package": {
    "metadata": {
      "package_id": "U1D05_Greek_Theatron",
      "unit": "Unit 1: Greek Theater",
      "day": 5,
      "topic": "The Theatron and Orchestra",
      "generated": "2026-01-08T10:30:00Z",
      "version": "1.0"
    },
    "deliverables": {
      "lesson_plan": {
        "filename": "U1D05_LessonPlan.pdf",
        "format": "admin_template",
        "pages": 2
      },
      "powerpoint": {
        "filename": "U1D05_Presentation.pptx",
        "slides": 16,
        "includes_notes": true
      },
      "handouts": [
        {
          "filename": "U1D05_Handout_TheaterDiagram.pdf",
          "copies_needed": "1 per student"
        }
      ],
      "exit_ticket": {
        "filename": "U1D05_ExitTicket.pdf",
        "copies_needed": "1 per student"
      }
    },
    "quick_reference": {
      "timing_summary": {
        "agenda": "5 min",
        "warmup": "5 min",
        "lecture": "15 min",
        "activity": "15 min",
        "reflection": "10 min",
        "buffer": "6 min"
      },
      "materials_checklist": [
        "Computer with presentation",
        "Projector/screen",
        "Greek theater diagrams (6 copies for stations)",
        "Sticky notes and markers",
        "Exit tickets (class set)",
        "Student journals"
      ],
      "vocabulary": ["theatron", "orchestra", "skene"],
      "learning_objectives": [
        "Identify the parts of a Greek theater",
        "Explain the function of the orchestra"
      ]
    },
    "validation_summary": {
      "all_gates_passed": true,
      "quality_score": 94
    }
  }
}
```

---

## Assembly Process

### Step 1: Validate All Components Present
```
Required Components:
□ lesson_plan
□ warmup
□ powerpoint_blueprint (16 slides)
□ presenter_notes (1,950-2,250 words)
□ activity
□ handouts (at least 1)
□ journal_prompt
□ exit_ticket
□ validation_results (all passed)
```

### Step 2: Generate Package ID
Format: `U{unit}D{day}_{TopicAbbrev}`
- `U1D05_Greek_Theatron`
- `U2D03_Commedia_StockChars`
- `U3D10_Shakespeare_Soliloquy`
- `U4D07_OneActs_Blocking`

### Step 3: Create File Manifest
| Component | Filename Pattern | Format |
|-----------|------------------|--------|
| Lesson Plan | `U{X}D{YY}_LessonPlan.pdf` | PDF |
| PowerPoint | `U{X}D{YY}_Presentation.pptx` | PPTX |
| Handout | `U{X}D{YY}_Handout_{Name}.pdf` | PDF |
| Exit Ticket | `U{X}D{YY}_ExitTicket.pdf` | PDF |
| Materials List | `U{X}D{YY}_Materials.txt` | TXT |

### Step 4: Generate Quick Reference
One-page summary for teacher:
- Timing at a glance
- Materials checklist
- Vocabulary list
- Learning objectives
- Warmup connection
- Activity overview

### Step 5: Compile Validation Summary
```json
{
  "gates_passed": 4,
  "gates_total": 4,
  "scores": {
    "truncation": 100,
    "structure": 100,
    "elaboration": 88,
    "timing": 95
  },
  "average_quality": 95.75,
  "warnings": [],
  "ready_for_production": true
}
```

---

## Lesson Plan Format (Admin Template)

### Page 1: Overview
```
╔══════════════════════════════════════════════════════════════════╗
║  LESSON PLAN                                                      ║
║  Unit 1: Greek Theater | Day 5 of 20                             ║
║  Topic: The Theatron and Orchestra                               ║
╠══════════════════════════════════════════════════════════════════╣
║  DATE: ____________    PERIOD: ____________                      ║
╠══════════════════════════════════════════════════════════════════╣
║  LEARNING OBJECTIVES:                                            ║
║  □ Identify the parts of a Greek theater                         ║
║  □ Explain the function of the orchestra                         ║
╠══════════════════════════════════════════════════════════════════╣
║  STANDARDS:                                                      ║
║  RL.9-10.5, SL.9-10.1b                                          ║
╠══════════════════════════════════════════════════════════════════╣
║  VOCABULARY:                                                     ║
║  theatron, orchestra, skene                                      ║
╠══════════════════════════════════════════════════════════════════╣
║  MATERIALS:                                                      ║
║  □ PowerPoint presentation                                       ║
║  □ Greek theater diagrams (6 for stations)                       ║
║  □ Sticky notes and markers                                      ║
║  □ Exit tickets                                                  ║
║  □ Student journals                                              ║
╚══════════════════════════════════════════════════════════════════╝
```

### Page 2: Timing and Procedures
```
╔══════════════════════════════════════════════════════════════════╗
║  LESSON TIMING (56 minutes)                                      ║
╠══════════════════════════════════════════════════════════════════╣
║  0:00-5:00   AGENDA & OBJECTIVES                                 ║
║              Display agenda, review objectives                    ║
║                                                                  ║
║  5:00-10:00  WARMUP: Greek Chorus Walk                          ║
║              Connection: Prepares for orchestra space discussion  ║
║                                                                  ║
║  10:00-25:00 LECTURE: The Theatron and Orchestra                ║
║              Slides 5-16, verbatim presenter notes               ║
║                                                                  ║
║  25:00-40:00 ACTIVITY: Theater Blueprint Analysis               ║
║              Setup (1.5 min) | Work (11 min) | Share (2.5 min)  ║
║                                                                  ║
║  40:00-50:00 REFLECTION                                         ║
║              Journal (7 min) | Exit Ticket (3 min)              ║
║                                                                  ║
║  50:00-56:00 BUFFER                                             ║
║              Transition, cleanup, dismissal                      ║
╠══════════════════════════════════════════════════════════════════╣
║  DIFFERENTIATION:                                                ║
║  ELL: Sentence frames, visual supports, strategic pairing        ║
║  Advanced: Compare to modern theaters extension                  ║
║  Struggling: Graphic organizer, word bank                        ║
╠══════════════════════════════════════════════════════════════════╣
║  ASSESSMENT:                                                     ║
║  Exit Ticket: Label three main parts of Greek theater           ║
╠══════════════════════════════════════════════════════════════════╣
║  NOTES:                                                          ║
║  _______________________________________________________________║
║  _______________________________________________________________║
╚══════════════════════════════════════════════════════════════════╝
```

---

## Component Integration Rules

### Rule 1: Presenter Notes Integration
- Notes must be embedded in PowerPoint file
- Notes panel for each slide
- Markers ([PAUSE], [EMPHASIS]) preserved

### Rule 2: Handout Formatting
- All handouts print-ready (no color required)
- Clear headings and instructions
- Student name/date line at top
- Consistent formatting across unit

### Rule 3: Exit Ticket Formatting
- Half-page format (2 per sheet)
- Clear question and answer space
- Name line at top
- Matches learning objectives

### Rule 4: Materials Cross-Reference
- All materials in lesson plan appear in materials list
- All materials in activity appear in lesson plan
- No orphaned material references

---

## Error Handling

### Missing Component
If any required component missing:
1. Flag ERROR - cannot assemble
2. Identify missing component
3. Return to generation phase for that component
4. Re-validate before assembly

### Validation Failure
If any validation gate not passed:
1. Flag ERROR - cannot assemble
2. Identify failing gate
3. Return to generation with failure context
4. Cannot proceed until all gates pass

### Word Count Mismatch
If presenter notes not within 1,950-2,250:
1. Flag WARNING
2. Note in validation summary
3. Recommend adjustment in QA report
4. Can proceed if within 10% tolerance

---

## Quality Checks Before Output

- [ ] All 8 components present
- [ ] All validation gates passed
- [ ] Package ID generated correctly
- [ ] All filenames follow convention
- [ ] Materials list complete
- [ ] Quick reference accurate
- [ ] Lesson plan formatted correctly
- [ ] No truncation in any text field
- [ ] Presenter notes word count verified
- [ ] Exit ticket matches objectives
