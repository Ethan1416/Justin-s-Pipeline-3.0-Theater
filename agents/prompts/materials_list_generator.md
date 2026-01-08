# Materials List Generator

## Purpose
Generate comprehensive, organized materials lists for theater education lessons including classroom supplies, handouts, technology, and special theater equipment.

## HARDCODED SKILLS
```yaml
skills:
  - word_count_analyzer
```

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
  "components": {
    "warmup": {
      "name": "Greek Chorus Walk",
      "materials_needed": ["Open floor space", "Music (optional)"]
    },
    "lecture": {
      "topic": "The Theatron and Orchestra",
      "materials_needed": ["PowerPoint presentation", "Projector/screen"]
    },
    "activity": {
      "name": "Theater Blueprint Analysis",
      "type": "gallery_walk",
      "materials_needed": ["Printed diagrams", "Sticky notes", "Markers"]
    },
    "journal": {
      "materials_needed": ["Student journals", "Writing utensils"]
    }
  },
  "vocabulary": ["theatron", "orchestra", "skene"],
  "handouts": ["Greek theater diagram", "Exit ticket"]
}
```

## Output Schema
```json
{
  "materials_list": {
    "lesson_info": {
      "unit": "Unit 1: Greek Theater",
      "day": 5,
      "topic": "The Theatron and Orchestra"
    },
    "categories": {
      "technology": [
        {
          "item": "Computer/laptop with presentation software",
          "quantity": 1,
          "notes": "Loaded with lesson PowerPoint"
        },
        {
          "item": "Projector and screen",
          "quantity": 1,
          "notes": "Test before class"
        }
      ],
      "classroom_supplies": [
        {
          "item": "Sticky notes (3x3 inch)",
          "quantity": "1 pad per station",
          "notes": "Assorted colors recommended"
        }
      ],
      "handouts": [
        {
          "item": "Greek theater diagram",
          "quantity": "1 per student",
          "notes": "Print before class"
        }
      ],
      "theater_equipment": [],
      "special_items": []
    },
    "setup_checklist": [
      "Post 6 Greek theater diagrams around room",
      "Place sticky note pad and markers at each station",
      "Test projector and presentation",
      "Prepare exit tickets for distribution"
    ],
    "preparation_time": "10-15 minutes before class"
  }
}
```

## Material Categories

### 1. Technology
| Item | Typical Quantity | Notes |
|------|------------------|-------|
| Computer/laptop | 1 | With presentation software |
| Projector | 1 | Test before class |
| Screen or whiteboard | 1 | Clean surface for projection |
| Speakers | 1 set | For audio/video clips |
| Document camera | 1 | For demonstrating handouts |
| Timer/stopwatch | 1 | For activity timing |

### 2. Classroom Supplies
| Item | Typical Quantity | Notes |
|------|------------------|-------|
| Whiteboard markers | 3-4 colors | Check for ink |
| Chart paper | 1-3 sheets | For group work |
| Sticky notes | 1 pad per group | 3x3 inch |
| Markers (student use) | 1 per group | Fine tip recommended |
| Tape (masking) | 1 roll | For posting items |
| Index cards | 1 per student | For exit tickets |

### 3. Handouts
| Item | Typical Quantity | Notes |
|------|------------------|-------|
| Lesson handout | 1 per student | Print before class |
| Activity worksheet | 1 per student | Or 1 per group |
| Exit ticket | 1 per student | Half-sheet format |
| Vocabulary list | 1 per student | Optional - can be projected |
| Graphic organizer | 1 per student | For note-taking |

### 4. Theater Equipment
Unit-specific items needed for warmups and activities:

#### Unit 1: Greek Theater
- Open floor space for chorus movement
- Optional: fabric for simple costume draping
- Optional: images of Greek masks

#### Unit 2: Commedia dell'Arte
- Commedia masks (or mask templates)
- Open floor space for improvisation
- Props: hat, cane, fan (basic stock character items)

#### Unit 3: Shakespeare
- Script excerpts (copied)
- Optional: simple props for scene work
- Optional: fabric pieces for costuming

#### Unit 4: Student-Directed One Acts
- Script copies for each student
- Blocking tape for floor marking
- Director's notebook/clipboard
- Optional: basic props and costumes

### 5. Special Items
Items that may need advance ordering or preparation:

| Item | Lead Time | Source |
|------|-----------|--------|
| Printed posters | 2-3 days | School print shop |
| Guest speaker materials | 1 week | Coordinate with guest |
| Video clips | Same day | Pre-download/bookmark |
| Costumes/props | Varies | Theater department storage |

## Setup Checklist Generation

For each lesson, generate a step-by-step setup checklist:

```
SETUP CHECKLIST - [Lesson Title]

Before Class:
□ Print [quantity] copies of [handout name]
□ Print [quantity] copies of exit ticket
□ Test projector and load presentation
□ [Activity-specific setup step]
□ [Activity-specific setup step]

Room Setup:
□ Arrange desks for [activity type]
□ Post [items] around room
□ Place materials at [location]
□ Clear floor space for [warmup/activity]

Materials Ready:
□ Handouts stacked at distribution point
□ Markers/supplies at stations
□ Timer visible and set
□ Exit tickets ready for distribution
```

## Activity-Specific Materials

### Gallery Walk
- 4-6 posted items (diagrams, images, excerpts)
- Sticky notes (1 pad per station)
- Markers (1 per station)
- Timer

### Think-Pair-Share
- Handout or projected question
- Timer for each phase
- Optional: response cards

### Jigsaw
- Expert group materials (1 set per expert group)
- Home group worksheet
- Timer
- Clear station labels

### Tableau/Freeze Frame
- Open floor space
- Optional: fabric pieces
- Camera (for optional documentation)

### Improv Games
- Open floor space
- Props as needed
- Timer

### Text Analysis
- Script/text copies (1 per student or pair)
- Highlighters (2-3 colors)
- Annotation guide

### Scene Work
- Script copies
- Open floor space
- Basic props (as specified)
- Blocking tape

## Quantity Guidelines

### Per Student
- Handouts: 1 per student (+ 5 extras)
- Exit tickets: 1 per student (+ 5 extras)
- Writing utensils: assume students have, have 5 extras

### Per Group (4-5 students)
- Chart paper: 1 sheet per group
- Markers: 1 set per group
- Sticky notes: 1 pad per group

### Per Station (gallery walk)
- Posted item: 1 per station
- Sticky notes: 1 pad per station
- Writing utensil: 1 per station

## Error Handling
- If activity type unknown, include basic supplies (paper, writing utensils)
- If handout not specified, note "Create handout based on activity"
- If theater equipment unavailable, suggest alternatives

## Validation Checklist
- [ ] Technology section complete (computer, projector, speakers if needed)
- [ ] All handouts listed with quantities
- [ ] Activity-specific materials included
- [ ] Setup checklist has 5-10 actionable items
- [ ] Preparation time estimated
- [ ] Theater equipment appropriate for unit
- [ ] Quantities are realistic (include extras)
- [ ] No truncation in any field
