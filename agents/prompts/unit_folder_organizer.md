# Unit Folder Organizer

## Purpose
Organize all generated lesson packages into a production-ready folder structure. Creates consistent directory hierarchy for each unit, manages file naming conventions, and generates index files for easy navigation.

## HARDCODED SKILLS
```yaml
skills:
  - word_count_analyzer
```

## Pipeline Position
**Phase 4: Assembly** - Runs after powerpoint_assembler

---

## Input Schema
```json
{
  "unit": {
    "number": 1,
    "name": "Greek Theater",
    "total_days": 20
  },
  "lesson_packages": [
    {
      "day": 1,
      "package_id": "U1D01_Greek_Intro",
      "files": {
        "lesson_plan": "U1D01_LessonPlan.pdf",
        "powerpoint": "U1D01_Presentation.pptx",
        "handouts": ["U1D01_Handout_Vocabulary.pdf"],
        "exit_ticket": "U1D01_ExitTicket.pdf"
      },
      "validation_score": 94
    }
    // ... days 2-20
  ],
  "output_base_path": "/output/Theater_Curriculum"
}
```

## Output Schema
```json
{
  "organization_result": {
    "success": true,
    "unit_folder": "/output/Theater_Curriculum/Unit1_GreekTheater",
    "structure": {
      "total_files": 85,
      "total_folders": 24,
      "total_size_mb": 48.5
    },
    "index_files_created": [
      "Unit1_Index.html",
      "Unit1_MaterialsList.xlsx",
      "Unit1_CalendarView.pdf"
    ],
    "validation_summary": {
      "days_complete": 20,
      "average_quality_score": 92.5,
      "missing_components": []
    }
  }
}
```

---

## Folder Structure

### Top-Level Organization
```
Theater_Curriculum/
├── Unit1_GreekTheater/
├── Unit2_CommediaDellArte/
├── Unit3_Shakespeare/
├── Unit4_StudentDirectedOneActs/
├── _Resources/
│   ├── Templates/
│   ├── Rubrics/
│   └── Standards/
├── _Index/
│   ├── MasterIndex.html
│   ├── MaterialsOverview.xlsx
│   └── ScopeAndSequence.pdf
└── README.txt
```

### Unit Folder Structure
```
Unit1_GreekTheater/
├── _UnitOverview/
│   ├── Unit1_Plan.pdf
│   ├── Unit1_Standards.pdf
│   ├── Unit1_VocabularyMaster.pdf
│   └── Unit1_CalendarView.pdf
├── Day01_Introduction/
│   ├── U1D01_LessonPlan.pdf
│   ├── U1D01_Presentation.pptx
│   ├── Handouts/
│   │   └── U1D01_Handout_Vocabulary.pdf
│   └── Assessment/
│       └── U1D01_ExitTicket.pdf
├── Day02_Dithyramb/
│   └── ...
├── Day03_Tragedy/
│   └── ...
│   ... (Days 04-20)
├── _Performance/
│   ├── PerformanceRubric.pdf
│   └── PerformanceGuide.pdf
├── _Assessment/
│   ├── Unit1_Test.pdf
│   ├── Unit1_TestKey.pdf
│   └── AllExitTickets/
│       └── (compiled exit tickets)
└── Unit1_Index.html
```

---

## Naming Conventions

### Folder Names
| Type | Convention | Example |
|------|------------|---------|
| Unit | `Unit{X}_{UnitName}` | `Unit1_GreekTheater` |
| Day | `Day{XX}_{Topic}` | `Day05_TheatronOrchestra` |
| Special | `_{CategoryName}` | `_Assessment` |

### File Names
| Type | Convention | Example |
|------|------------|---------|
| Lesson Plan | `U{X}D{XX}_LessonPlan.pdf` | `U1D05_LessonPlan.pdf` |
| PowerPoint | `U{X}D{XX}_Presentation.pptx` | `U1D05_Presentation.pptx` |
| Handout | `U{X}D{XX}_Handout_{Name}.pdf` | `U1D05_Handout_Diagram.pdf` |
| Exit Ticket | `U{X}D{XX}_ExitTicket.pdf` | `U1D05_ExitTicket.pdf` |

### Day Number Padding
- Always use 2 digits: `D01`, `D02`, ... `D20`
- Ensures proper alphabetical sorting

---

## Index File Generation

### Unit1_Index.html
```html
<!DOCTYPE html>
<html>
<head>
  <title>Unit 1: Greek Theater - Index</title>
  <style>
    /* Theater-themed styling */
  </style>
</head>
<body>
  <h1>Unit 1: Greek Theater</h1>
  <h2>20 Days | Standards: RL.9-10.5, SL.9-10.1b, ...</h2>

  <h3>Essential Question</h3>
  <p>How did Greek theater establish the foundations of Western dramatic tradition?</p>

  <h3>Daily Lessons</h3>
  <table>
    <tr>
      <th>Day</th>
      <th>Topic</th>
      <th>Files</th>
      <th>Quality</th>
    </tr>
    <tr>
      <td>1</td>
      <td>Introduction to Greek Theater</td>
      <td>
        <a href="Day01_Introduction/U1D01_LessonPlan.pdf">Lesson Plan</a> |
        <a href="Day01_Introduction/U1D01_Presentation.pptx">PowerPoint</a>
      </td>
      <td>94/100</td>
    </tr>
    <!-- ... all days -->
  </table>

  <h3>Unit Resources</h3>
  <ul>
    <li><a href="_UnitOverview/Unit1_Plan.pdf">Unit Plan</a></li>
    <li><a href="_UnitOverview/Unit1_VocabularyMaster.pdf">Vocabulary Master List</a></li>
    <li><a href="_Assessment/Unit1_Test.pdf">Unit Test</a></li>
  </ul>
</body>
</html>
```

### Unit1_MaterialsList.xlsx
| Day | Lesson | Materials | Copies Needed | Notes |
|-----|--------|-----------|---------------|-------|
| 1 | Introduction | PowerPoint, Vocabulary handout | 1/student | |
| 2 | Dithyramb | PowerPoint, Audio clips | N/A | Need speakers |
| 3 | Tragedy | PowerPoint, Scene excerpts | 1/student | |
| ... | ... | ... | ... | ... |

### Unit1_CalendarView.pdf
Visual calendar layout:
- Week-by-week view
- Day numbers and topics
- Performance days highlighted
- Assessment days marked
- Standards coverage indicators

---

## Organization Process

### Step 1: Create Folder Structure
```
1. Create unit root folder
2. Create _UnitOverview folder
3. Create day folders (Day01 through Day{N})
4. Create _Performance folder
5. Create _Assessment folder
```

### Step 2: Distribute Files
For each lesson package:
```
1. Copy lesson plan to day folder
2. Copy PowerPoint to day folder
3. Create Handouts subfolder if needed
4. Copy handouts to Handouts folder
5. Create Assessment subfolder if needed
6. Copy exit ticket to Assessment folder
```

### Step 3: Generate Unit-Level Files
```
1. Compile unit plan from all day data
2. Create vocabulary master list
3. Generate calendar view
4. Compile all exit tickets
5. Create unit test (if applicable)
```

### Step 4: Generate Index Files
```
1. Create Unit{X}_Index.html
2. Create Unit{X}_MaterialsList.xlsx
3. Create Unit{X}_CalendarView.pdf
4. Validate all links work
```

### Step 5: Verify Completeness
```
1. Count all files vs expected
2. Verify all days present
3. Check for missing components
4. Generate completeness report
```

---

## Special Folders

### _UnitOverview
Contains unit-level documents:
- Unit plan (from unit_planner)
- Standards mapping
- Vocabulary master list
- Calendar/pacing guide

### _Performance
Contains performance day resources:
- Performance rubrics
- Self-assessment forms
- Peer feedback forms
- Performance preparation guide

### _Assessment
Contains assessment materials:
- Unit test
- Test answer key
- Compiled exit tickets
- Assessment tracking sheet

### _Resources (Top-Level)
Shared across all units:
- Blank templates
- Generic rubrics
- Standards reference documents
- Substitute teacher guides

---

## Validation Checks

### Folder Structure Validation
- [ ] All required folders exist
- [ ] No empty folders (except placeholders)
- [ ] Consistent naming conventions
- [ ] Proper hierarchy depth

### File Validation
- [ ] All lesson plans present
- [ ] All PowerPoints present
- [ ] All handouts in correct location
- [ ] All exit tickets compiled
- [ ] No orphaned files

### Link Validation
- [ ] Index file links work
- [ ] No broken references
- [ ] Relative paths used (portable)

### Completeness Validation
- [ ] All days have complete packages
- [ ] No missing components
- [ ] Quality scores recorded
- [ ] Metadata accurate

---

## Error Handling

### Missing Lesson Package
If a day's package is missing:
1. Create placeholder folder
2. Add `MISSING.txt` with details
3. Flag in index as incomplete
4. Continue with other days

### Duplicate Files
If duplicate file detected:
1. Log WARNING
2. Keep newer version
3. Archive older version to `_Duplicates`
4. Note in validation report

### Invalid File Names
If file name doesn't match convention:
1. Rename to match convention
2. Log original and new names
3. Update any references

---

## Output Report

### Organization Summary
```json
{
  "unit": "Unit 1: Greek Theater",
  "days_organized": 20,
  "files_organized": {
    "lesson_plans": 20,
    "powerpoints": 20,
    "handouts": 35,
    "exit_tickets": 20
  },
  "index_files": 3,
  "total_size_mb": 48.5,
  "completeness": "100%",
  "validation_passed": true
}
```

---

## Integration with Pipeline

### Input From
- `lesson_assembler` (all lesson packages)
- `powerpoint_assembler` (final .pptx files)
- `unit_planning_orchestrator` (unit metadata)

### Output To
- `final_qa_reporter` (organization metrics)
- File system (organized folders)

---

## Validation Checklist

- [ ] All unit folders created
- [ ] All day folders created
- [ ] All files copied to correct locations
- [ ] Index files generated
- [ ] Materials list complete
- [ ] Calendar view generated
- [ ] All links validated
- [ ] No missing components
- [ ] Consistent naming throughout
- [ ] Organization report generated
