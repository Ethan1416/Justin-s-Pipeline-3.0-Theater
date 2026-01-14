# PowerPoint Generator

## Purpose
Generate complete 16-slide PowerPoint blueprints for theater education lessons with 4 auxiliary slides and 12 content slides.

## HARDCODED SKILLS
```yaml
skills:
  - monologue_scripter
  - word_count_analyzer
  - duration_estimator
  - sentence_completeness_checker
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
  "learning_objectives": [
    "Identify the parts of a Greek theater",
    "Explain the function of the orchestra"
  ],
  "vocabulary": [
    {
      "term": "theatron",
      "definition": "The seating area for the audience in a Greek theater",
      "usage_example": "The theatron could hold up to 17,000 spectators."
    }
  ],
  "content_outline": [
    "Introduction to Greek theater architecture",
    "The theatron - audience seating",
    "The orchestra - performance space",
    "The skene - scenic building"
  ],
  "warmup": {
    "name": "Greek Chorus Walk",
    "duration": 5,
    "connection_to_lesson": "Prepares bodies for understanding how performers used the orchestra space"
  },
  "activity": {
    "name": "Theater Blueprint Analysis",
    "type": "gallery_walk",
    "duration": 15
  }
}
```

## Output Schema
```json
{
  "blueprint": {
    "metadata": {
      "unit": "Unit 1: Greek Theater",
      "day": 5,
      "topic": "The Theatron and Orchestra",
      "total_slides": 16,
      "auxiliary_slides": 4,
      "content_slides": 12
    },
    "slides": [
      {
        "slide_number": 1,
        "type": "auxiliary",
        "subtype": "agenda",
        "header": "Today's Agenda",
        "body": "1. Warmup: Greek Chorus Walk (5 min)\n2. Lecture: The Theatron and Orchestra (15 min)\n3. Activity: Theater Blueprint Analysis (15 min)\n4. Reflection: Journal + Exit Ticket (10 min)",
        "presenter_notes": "Welcome students as they enter...",
        "performance_tip": "Make eye contact with different sections of the room as you review the agenda."
      }
    ]
  }
}
```

## Slide Structure

### Auxiliary Slides (1-4)
| Slide | Type | Purpose |
|-------|------|---------|
| 1 | Agenda | Daily schedule with time markers |
| 2 | Warmup | Warmup instructions and connection |
| 3 | Activity | Activity overview and instructions |
| 4 | Journal/Exit | Reflection prompt and exit ticket |

### Content Slides (5-16)
| Slide | Type | Purpose |
|-------|------|---------|
| 5 | Title | Lesson title and learning objectives |
| 6-15 | Content | Core lesson content (10 slides) |
| 16 | Summary | Key takeaways and vocabulary review |

## Text Limits (from config/constraints.yaml)

### Header
- Maximum characters per line: 32
- Maximum lines: 2
- Total maximum characters: 64

### Body
- Maximum lines: 8
- Maximum characters per line: 66
- Word wrap: enabled (no truncation)

### Performance Tip
- Maximum characters: 132
- Must be actionable teaching advice

### Presenter Notes
- Target words: 1,950-2,250 (total across all slides)
- Per slide (ALL types): 30-180 words (use best judgment based on content needs)
- Markers required: [PAUSE], [EMPHASIS: term], [CHECK FOR UNDERSTANDING]

## Slide Templates

### Slide 1: Agenda (Auxiliary)
```
Header: Today's Agenda
Body:
1. Warmup: [Name] (5 min)
2. Lecture: [Topic] (15 min)
3. Activity: [Name] (15 min)
4. Reflection: Journal + Exit Ticket (10 min)

Performance Tip: Review agenda items while making eye contact with different sections of the room.
```

### Slide 2: Warmup (Auxiliary)
```
Header: Warmup: [Name]
Body:
Purpose: [Connection to lesson]

Instructions:
- Step 1
- Step 2
- Step 3

Time: 5 minutes

Performance Tip: [Warmup-specific guidance]
```

### Slide 3: Activity (Auxiliary)
```
Header: Activity: [Name]
Body:
Setup (1.5 min): [Brief setup]
Work Time (11 min): [Main instructions]
Sharing (2.5 min): [Share-out format]

Materials: [List]

Performance Tip: [Activity-specific guidance]
```

### Slide 4: Journal/Exit (Auxiliary)
```
Header: Reflection Time
Body:
Journal Prompt:
[Thought-provoking question]

Exit Ticket:
[Quick assessment question]

Performance Tip: Circulate while students write to encourage deeper thinking.
```

### Slide 5: Title (Content)
```
Header: [Lesson Title]
Body:
Unit [X]: [Unit Name] - Day [Y]

Learning Objectives:
1. [Objective 1]
2. [Objective 2]

Essential Question: [Driving question]

Performance Tip: State objectives clearly - students should know what they're working toward.
```

### Slides 6-15: Content (10 slides)
```
Header: [Topic/Subtopic]
Body:
[Key points in bullet form]
- Point 1
- Point 2
- Point 3

[Optional vocabulary callout]

Performance Tip: [Delivery guidance for this specific content]
```

### Slide 16: Summary (Content)
```
Header: Today's Key Takeaways
Body:
We learned:
- [Takeaway 1]
- [Takeaway 2]
- [Takeaway 3]

Vocabulary Review:
[Term 1], [Term 2], [Term 3]

Performance Tip: Ask students to share one thing they learned before dismissing.
```

## Presenter Notes Requirements

### Word Count Distribution
| Slide Type | Word Range | Guidance |
|------------|------------|----------|
| ALL slides | 30-180 words | Use best judgment based on content needs |

**Judgment Factors:**
- Complexity of content (more complex = more words)
- Need for examples or elaboration
- Natural pacing and flow
- Connection to previous/next slides
- Student engagement moments
- Vocabulary introduction needs

**No rigid per-slide-type targets.** Let the content drive the length.

### Marker Requirements
- `[PAUSE]` - Minimum 2 per content slide
- `[EMPHASIS: term]` - At least 1 per vocabulary introduction
- `[CHECK FOR UNDERSTANDING]` - At least 3 throughout presentation

### No Truncation Policy
- Every sentence must be complete
- No trailing ellipsis (...)
- No mid-word cuts
- No orphaned phrases

## Error Handling
- If word count is below minimum, expand with examples and context
- If word count exceeds maximum, prioritize essential content
- If performance tip exceeds 132 characters, condense to key action

## Validation Checklist
- [ ] Exactly 16 slides (4 auxiliary + 12 content)
- [ ] Total presenter notes: 1,950-2,250 words
- [ ] Each slide: 30-180 words (flexible based on content)
- [ ] All headers under 64 characters
- [ ] All body text under 8 lines
- [ ] Performance tips under 132 characters
- [ ] [PAUSE] markers: minimum 24 total
- [ ] [EMPHASIS] markers: at least 1 per vocabulary term
- [ ] [CHECK FOR UNDERSTANDING]: minimum 3
- [ ] No truncated sentences
