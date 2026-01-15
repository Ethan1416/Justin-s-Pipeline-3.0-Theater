# Daily Agenda Generator

## Purpose
Generate structured daily agendas for theater education lessons with precise timing, clear objectives, and PowerPoint Slide 1 visual layout.

## HARDCODED SKILLS
```yaml
skills:
  - agenda_slide_generator      # skills/enforcement/agenda_slide_generator.py
  - agenda_slide_validator      # skills/enforcement/agenda_slide_validator.py
  - timing_allocator
  - word_count_analyzer
```

## Slide 1 Visual Layout (HARDCODED)

The agenda slide (Slide 1) MUST follow this exact visual layout:

```
┌─────────────────────────────────────────┐
│  Unit 3: Shakespeare - Day 12/25        │  ← Header (unit info)
│  "The Balcony Scene"                    │  ← Lesson Title (in quotes)
├─────────────────────────────────────────┤
│  TODAY'S AGENDA                         │  ← Section header
│  ☐ Agenda & Objectives (5 min)          │  ← Checkbox format
│  ☐ Warmup (5 min)                       │
│  ☐ Lecture (15 min)                     │
│  ☐ Activity (15 min)                    │
│  ☐ Reflection & Exit Ticket (10 min)    │
├─────────────────────────────────────────┤
│  OBJECTIVES                             │  ← Section header
│  1. Analyze Romeo's use of metaphor     │  ← Numbered, measurable
│  2. Perform 10 lines with partner       │
└─────────────────────────────────────────┘
```

### Slide 1 Content Requirements

| Element | Format | Max Length |
|---------|--------|------------|
| Header | "Unit X: [Name] - Day Y/Z" | 45 chars |
| Lesson Title | In quotes, title case | 40 chars |
| Agenda Items | "☐ [Component] (X min)" | 35 chars |
| Objectives | "N. [Measurable verb]..." | 50 chars |

### Buffer Component
The buffer/transition time (6 min) is NOT displayed on the agenda slide but IS included in timing calculations.

## Input Schema
```json
{
  "unit": {
    "number": 1,
    "name": "Greek Theater",
    "day": 5,
    "total_days": 20
  },
  "lesson_topic": "The Theatron and Orchestra",
  "learning_objectives": [
    "Identify the parts of a Greek theater",
    "Explain the function of the orchestra"
  ],
  "warmup_type": "physical",
  "activity_type": "discussion"
}
```

## Output Schema
```json
{
  "agenda": {
    "unit_info": "Unit 1: Greek Theater - Day 5/20",
    "date_placeholder": "[DATE]",
    "lesson_title": "The Theatron and Orchestra",
    "total_duration": 56,
    "components": [
      {
        "sequence": 1,
        "component": "Agenda & Objectives",
        "duration_minutes": 5,
        "time_marker": "0:00-5:00",
        "description": "Review daily agenda and learning objectives"
      },
      {
        "sequence": 2,
        "component": "Warmup",
        "duration_minutes": 5,
        "time_marker": "5:00-10:00",
        "description": "Physical warmup - Greek chorus movement"
      },
      {
        "sequence": 3,
        "component": "Lecture",
        "duration_minutes": 15,
        "time_marker": "10:00-25:00",
        "description": "The Theatron and Orchestra - verbatim script"
      },
      {
        "sequence": 4,
        "component": "Activity",
        "duration_minutes": 15,
        "time_marker": "25:00-40:00",
        "description": "Gallery walk - Greek theater diagram analysis"
      },
      {
        "sequence": 5,
        "component": "Reflection",
        "duration_minutes": 10,
        "time_marker": "40:00-50:00",
        "description": "Journal prompt and exit ticket"
      },
      {
        "sequence": 6,
        "component": "Buffer",
        "duration_minutes": 6,
        "time_marker": "50:00-56:00",
        "description": "Transition time and cleanup"
      }
    ],
    "learning_objectives_display": [
      "1. Identify the parts of a Greek theater",
      "2. Explain the function of the orchestra"
    ],
    "materials_preview": [
      "PowerPoint presentation",
      "Theater diagram handout",
      "Journal/notebook"
    ]
  }
}
```

## Class Period Configurations (HARDCODED)

The pipeline supports multiple class period types:

| Schedule | Duration | Use Case |
|----------|----------|----------|
| **standard** | 56 min | Default daily schedule |
| **block** | 90 min | Block schedule days |
| **shortened** | 45 min | Assembly/pep rally days |
| **extended** | 75 min | Extended period days |

## Timing Requirements

### Standard 56-Minute Period (Default)

| Component | Duration | Start | End | Purpose |
|-----------|----------|-------|-----|---------|
| Agenda & Objectives | 5 min | 0:00 | 5:00 | Set expectations, review goals |
| Warmup | 5 min | 5:00 | 10:00 | Physical/vocal/mental preparation |
| Lecture | 15 min | 10:00 | 25:00 | Verbatim presenter notes delivery |
| Activity | 15 min | 25:00 | 40:00 | Hands-on application |
| Reflection | 10 min | 40:00 | 50:00 | Journal + exit ticket |
| Buffer | 6 min | 50:00 | 56:00 | Transitions, cleanup, flexibility |
| **TOTAL** | **56 min** | | | |

### Block 90-Minute Period

| Component | Duration | Start | End |
|-----------|----------|-------|-----|
| Agenda & Objectives | 5 min | 0:00 | 5:00 |
| Warmup | 10 min | 5:00 | 15:00 |
| Lecture | 25 min | 15:00 | 40:00 |
| Activity | 30 min | 40:00 | 70:00 |
| Reflection | 15 min | 70:00 | 85:00 |
| Buffer | 5 min | 85:00 | 90:00 |

### Shortened 45-Minute Period

| Component | Duration | Start | End |
|-----------|----------|-------|-----|
| Agenda & Objectives | 3 min | 0:00 | 3:00 |
| Warmup | 5 min | 3:00 | 8:00 |
| Lecture | 12 min | 8:00 | 20:00 |
| Activity | 12 min | 20:00 | 32:00 |
| Reflection | 8 min | 32:00 | 40:00 |
| Buffer | 5 min | 40:00 | 45:00 |

## Generation Rules

### 1. Time Marker Format
Always use `MM:SS-MM:SS` format:
- `0:00-5:00` for Agenda
- `5:00-10:00` for Warmup
- `10:00-25:00` for Lecture
- `25:00-40:00` for Activity
- `40:00-50:00` for Reflection
- `50:00-56:00` for Buffer

### 2. Component Descriptions
Keep descriptions concise (under 60 characters):
- Include component type and specific topic
- Use action verbs (Review, Analyze, Practice, Discuss)
- Connect to lesson content

### 3. Learning Objectives Display
- Maximum 3 objectives per lesson
- Number each objective (1., 2., 3.)
- Use measurable verbs (Identify, Explain, Compare, Demonstrate)
- Keep each under 50 characters

### 4. Materials Preview
List 3-5 essential materials:
- PowerPoint presentation (always included)
- Specific handouts for the day
- Props or special equipment
- Journal/notebook (always included)

## Unit-Specific Context

### Unit 1: Greek Theater
- Warmups connect to Greek chorus traditions
- Activities focus on physical staging and mask work
- Vocabulary: theatron, orchestra, skene, chorus, dithyramb

### Unit 2: Commedia dell'Arte
- Warmups include stock character physicality
- Activities focus on improvisation and lazzi
- Vocabulary: zanni, lazzi, scenario, stock characters

### Unit 3: Shakespeare
- Warmups include verse speaking and breath work
- Activities focus on text analysis and staging
- Vocabulary: iambic pentameter, soliloquy, aside, groundlings

### Unit 4: Student-Directed One Acts
- Warmups focus on ensemble building
- Activities focus on blocking and directing
- Vocabulary: blocking, staging, director's vision, ensemble

## Error Handling
- If duration doesn't sum to 56 minutes, adjust buffer time
- If fewer than 3 materials, add "Journal/notebook" and "Writing utensil"
- If objectives exceed 3, prioritize by measurability

## Validation Checklist
- [ ] Total duration equals 56 minutes
- [ ] All 6 components present
- [ ] Time markers are sequential and non-overlapping
- [ ] Learning objectives are numbered and measurable
- [ ] Materials list has 3-5 items
- [ ] Descriptions are under 60 characters
