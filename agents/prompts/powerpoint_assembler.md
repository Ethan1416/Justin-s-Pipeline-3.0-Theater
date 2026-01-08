# PowerPoint Assembler

## Purpose
Build the final .pptx file from the PowerPoint blueprint and presenter notes. Populates theater template with content, embeds presenter notes, and ensures all slides meet formatting requirements.

## HARDCODED SKILLS
```yaml
skills:
  - sentence_completeness_checker
  - word_count_analyzer
```

## Pipeline Position
**Phase 4: Assembly** - Runs after lesson_assembler

---

## Input Schema
```json
{
  "blueprint": {
    "metadata": {
      "unit": "Unit 1: Greek Theater",
      "day": 5,
      "topic": "The Theatron and Orchestra",
      "total_slides": 16
    },
    "slides": [
      {
        "slide_number": 1,
        "type": "auxiliary",
        "subtype": "agenda",
        "header": "Today's Agenda",
        "body": "1. Warmup: Greek Chorus Walk (5 min)\n2. Lecture: The Theatron and Orchestra (15 min)\n3. Activity: Theater Blueprint Analysis (15 min)\n4. Reflection: Journal + Exit Ticket (10 min)",
        "presenter_notes": "Welcome everyone! As you can see...",
        "performance_tip": "Review each agenda item while making eye contact with different sections of the room."
      }
      // ... slides 2-16
    ]
  },
  "template_path": "templates/template_theater.pptx",
  "output_path": "output/U1D05_Presentation.pptx"
}
```

## Output Schema
```json
{
  "assembly_result": {
    "success": true,
    "output_file": "output/U1D05_Presentation.pptx",
    "file_size_kb": 2450,
    "slides_populated": 16,
    "notes_embedded": 16,
    "assembly_log": [
      {"slide": 1, "status": "success", "notes_words": 87},
      {"slide": 2, "status": "success", "notes_words": 92}
      // ... all slides
    ],
    "quality_metrics": {
      "total_notes_words": 2100,
      "avg_words_per_content_slide": 175,
      "markers_preserved": {
        "pause": 24,
        "emphasis": 12,
        "check_understanding": 3
      }
    },
    "warnings": [],
    "errors": []
  }
}
```

---

## Theater Template Structure

### Template: template_theater.pptx

**Slide Layout Configuration:**
| Layout Index | Name | Use |
|--------------|------|-----|
| 0 | Title | Auxiliary slides (agenda, warmup, activity, journal) |
| 1 | Content | Content slides with header + body |
| 2 | Section | Unit/day intro |
| 3 | Blank | Custom layouts |

**Shape Mappings:**
| Shape Name | Purpose | Character Limit |
|------------|---------|-----------------|
| Title | Header text | 64 (32 x 2 lines) |
| Subtitle | Subheading | 100 |
| Body | Main content | 528 (66 x 8 lines) |
| Footer | Slide info | 50 |
| Slide Number | Auto | N/A |

**Color Scheme (from config/theater.yaml):**
| Element | Color | Hex |
|---------|-------|-----|
| Primary | Dark Red | #8B0000 |
| Secondary | Seashell | #FFF5EE |
| Accent | Goldenrod | #DAA520 |
| Text | Dark Gray | #333333 |

---

## Assembly Process

### Step 1: Load Template
```python
# Pseudocode
template = load_template("templates/template_theater.pptx")
validate_template_shapes(template)
```

### Step 2: Process Each Slide
For each slide in blueprint:

#### 2a. Select Layout
| Slide Type | Layout |
|------------|--------|
| auxiliary/agenda | Title |
| auxiliary/warmup | Title |
| auxiliary/activity | Title |
| auxiliary/journal | Title |
| content/title | Section |
| content/body | Content |
| content/summary | Content |

#### 2b. Populate Header
```
Input: "The Theatron and Orchestra"
Process:
1. Check length ≤ 64 characters
2. Split to 2 lines if needed (at word boundary)
3. Apply title formatting
4. Insert into Title shape
```

#### 2c. Populate Body
```
Input: "- Point 1\n- Point 2\n- Point 3..."
Process:
1. Verify ≤ 8 lines
2. Verify each line ≤ 66 characters
3. Apply body formatting
4. Insert into Body shape
```

#### 2d. Embed Presenter Notes
```
Input: "Welcome everyone! [PAUSE] Today we explore..."
Process:
1. Preserve all markers ([PAUSE], [EMPHASIS], [CHECK FOR UNDERSTANDING])
2. Verify word count within range
3. Insert into notes panel
```

#### 2e. Add Performance Tip
```
Input: "Review agenda items while making eye contact..."
Process:
1. Verify ≤ 132 characters
2. Format as callout box or footer note
3. Insert at designated position
```

### Step 3: Finalize Presentation
```
1. Update slide numbers
2. Verify all slides populated
3. Run final validation
4. Save to output path
```

---

## Text Formatting Rules

### Header Formatting
| Property | Value |
|----------|-------|
| Font | Georgia |
| Size | 36pt |
| Color | Dark Red (#8B0000) |
| Alignment | Left |
| Bold | Yes |

### Body Formatting
| Property | Value |
|----------|-------|
| Font | Arial |
| Size | 24pt |
| Color | Dark Gray (#333333) |
| Alignment | Left |
| Bullet Style | Em dash (—) |
| Line Spacing | 1.2 |

### Presenter Notes Formatting
| Property | Value |
|----------|-------|
| Font | Arial |
| Size | 12pt |
| Color | Black |
| Markers | Bold + Color (e.g., [PAUSE] in blue) |

---

## Slide-by-Slide Assembly

### Slides 1-4: Auxiliary Slides

#### Slide 1: Agenda
```
Layout: Title
Header: "Today's Agenda"
Body:
1. Warmup: [Name] (5 min)
2. Lecture: [Topic] (15 min)
3. Activity: [Name] (15 min)
4. Reflection: Journal + Exit Ticket (10 min)

Notes: Welcome script (75-100 words)
```

#### Slide 2: Warmup
```
Layout: Title
Header: "Warmup: [Name]"
Body:
Purpose: [Connection]
Instructions: [Steps]
Time: 5 minutes

Notes: Warmup facilitation script (75-100 words)
```

#### Slide 3: Activity
```
Layout: Title
Header: "Activity: [Name]"
Body:
Setup (1.5 min): [Instructions]
Work Time (11 min): [Instructions]
Sharing (2.5 min): [Format]

Notes: Activity facilitation script (75-100 words)
```

#### Slide 4: Journal/Exit
```
Layout: Title
Header: "Reflection Time"
Body:
Journal Prompt (7 min): [Prompt]
Exit Ticket (3 min): [Question]

Notes: Reflection facilitation script (50-75 words)
```

### Slide 5: Title Slide
```
Layout: Section
Header: [Lesson Topic]
Body:
Unit [X]: [Unit Name] - Day [Y]
Learning Objectives:
1. [Objective 1]
2. [Objective 2]

Notes: Hook and context script (100-125 words)
```

### Slides 6-15: Content Slides
```
Layout: Content
Header: [Subtopic]
Body: [Key points as bullets]

Notes: Full delivery script (160-190 words each)
```

### Slide 16: Summary
```
Layout: Content
Header: "Today's Key Takeaways"
Body:
We learned:
- [Takeaway 1]
- [Takeaway 2]
- [Takeaway 3]

Vocabulary: [Terms]

Notes: Wrap-up script (150-175 words)
```

---

## Marker Handling

### [PAUSE] Markers
- Preserve in notes text
- Format: Bold, Blue (#0066CC)
- Minimum 2 per content slide

### [EMPHASIS: term] Markers
- Preserve in notes text
- Format: Bold, Green (#006600)
- At least 1 per vocabulary introduction

### [CHECK FOR UNDERSTANDING] Markers
- Preserve in notes text
- Format: Bold, Orange (#FF6600)
- Minimum 3 throughout presentation

---

## Error Handling

### Text Overflow
If content exceeds limits:
1. Log WARNING with overflow amount
2. Do NOT truncate (violates hardcoded rule)
3. Flag for manual review
4. Continue assembly with warning

### Missing Content
If slide blueprint incomplete:
1. Log ERROR
2. Skip slide with placeholder
3. Flag for regeneration
4. Prevent finalization until resolved

### Template Mismatch
If template shapes don't match expected:
1. Log ERROR
2. Attempt shape name fallback
3. Report mapping failures
4. May require template update

---

## Quality Verification

### Post-Assembly Checks
- [ ] All 16 slides present
- [ ] All headers populated
- [ ] All bodies populated
- [ ] All presenter notes embedded
- [ ] Total notes word count: 1,950-2,250
- [ ] [PAUSE] markers: ≥24
- [ ] [EMPHASIS] markers: ≥8
- [ ] [CHECK FOR UNDERSTANDING]: ≥3
- [ ] No text truncation
- [ ] File saves successfully

### Output Metrics
```json
{
  "slides_total": 16,
  "slides_auxiliary": 4,
  "slides_content": 12,
  "notes_total_words": 2100,
  "notes_per_slide_avg": 131,
  "markers": {
    "pause": 26,
    "emphasis": 12,
    "check_understanding": 3
  },
  "file_size_kb": 2450,
  "assembly_time_seconds": 3.2
}
```

---

## Integration with Pipeline

### Input From
- `powerpoint_generator` (blueprint)
- `presenter_notes_writer` (notes content)
- `lesson_assembler` (metadata)

### Output To
- `unit_folder_organizer` (final .pptx file)
- `final_qa_reporter` (assembly metrics)

---

## Validation Checklist

- [ ] Template loaded successfully
- [ ] All 16 slides assembled
- [ ] Headers within character limits
- [ ] Bodies within line/character limits
- [ ] Presenter notes embedded with markers
- [ ] Performance tips included
- [ ] Word count verified
- [ ] No truncation in any field
- [ ] File saved to correct path
- [ ] Assembly log complete
