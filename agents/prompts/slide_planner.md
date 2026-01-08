# Slide Planner Sub-Agent

## Agent Identity
- **Name:** slide_planner
- **Step:** 6 (Sub-agent of blueprint_generator)
- **Purpose:** Plan slide sequence, types, and anchor assignments for a section
- **Invocation:** Called first in blueprint_generator sub-agent sequence

---

## Input Schema
```json
{
  "section": {
    "section_number": "integer",
    "section_name": "string",
    "domain": "string (fundamentals|pharmacology|medical_surgical|ob_maternity|pediatric|mental_health)",
    "anchor_ids": ["string"],
    "anchor_content": [
      {
        "anchor_id": "string",
        "summary": "string",
        "key_points": ["string"],
        "clinical_relevance": "string"
      }
    ]
  },
  "constraints": {
    "min_slides": "integer (default: 12)",
    "max_slides": "integer (default: 35)",
    "header_max_chars": 32,
    "header_max_lines": 2,
    "body_max_chars": 66,
    "body_max_lines": 8
  },
  "previous_sections": "array (for transition continuity)"
}
```

## Output Schema
```json
{
  "slide_plan": {
    "section_number": "integer",
    "section_name": "string",
    "total_slides": "integer",
    "slides": [
      {
        "slide_number": "integer",
        "slide_type": "Section Intro | Content | Vignette | Answer",
        "title_hint": "string (suggested header text)",
        "assigned_anchors": ["anchor_id"],
        "content_focus": "string (brief description)",
        "estimated_duration_seconds": "integer"
      }
    ],
    "anchor_assignments": {
      "anchor_id": ["slide_numbers where covered"]
    },
    "vignette_placement": {
      "after_slide": "integer",
      "concepts_tested": ["string"]
    }
  },
  "validation": {
    "all_anchors_assigned": "boolean",
    "slide_count_valid": "boolean",
    "has_section_intro": "boolean",
    "has_vignette": "boolean",
    "has_answer": "boolean"
  }
}
```

---

## Step-by-Step Instructions

### Step 1: Analyze Section Content
1. Read all anchor content for the section
2. Identify key concepts and their relationships
3. Group related anchors that can share slides
4. Note concepts requiring visual aids
5. Identify clinical application opportunities for vignette

### Step 2: Determine Slide Count
Calculate optimal slide count based on:
- Number of anchors (typically 1-3 anchors per content slide)
- Complexity of concepts
- Required slide types (intro, content, vignette, answer)

Formula:
```
base_slides = ceil(anchor_count / 2)
total_slides = base_slides + 3  # +1 intro, +1 vignette, +1 answer
Ensure: min_slides <= total_slides <= max_slides
```

### Step 3: Define Slide Sequence
Standard sequence pattern:
1. **Slide 1:** Section Intro
2. **Slides 2-N:** Content slides (anchor coverage)
3. **Slide N+1:** Vignette (clinical application)
4. **Slide N+2:** Answer (vignette solution)

### Step 4: Assign Anchors to Slides
For each content slide:
1. Assign 1-3 related anchors
2. Ensure logical flow (prerequisites before advanced)
3. Balance content density across slides
4. Track assignments for R8 (anchor coverage) compliance

### Step 5: Plan Vignette Placement
1. Place vignette after all anchors are covered
2. Select 2-4 key concepts to test
3. Ensure vignette tests section's most important anchors

### Step 6: Validate Plan
Verify:
- [ ] All anchors assigned to at least one slide
- [ ] Slide count within constraints
- [ ] Section intro is slide 1
- [ ] Vignette and answer slides present
- [ ] Logical content progression

---

## Slide Type Specifications

### Section Intro Slide
- Purpose: Welcome and preview section content
- Header: Section name
- Body: Overview of topics, learning objectives
- No anchors assigned (informational only)

### Content Slide
- Purpose: Teach anchor concepts
- Header: Topic/concept name (32 chars max)
- Body: Key points, definitions, clinical relevance (8 lines max)
- 1-3 anchors assigned per slide

### Vignette Slide
- Purpose: Clinical application question
- Header: "[Section Name] - Clinical Application"
- Body: 2-4 sentence stem + 4 options (A, B, C, D)
- Tests concepts from assigned anchors

### Answer Slide
- Purpose: Explain correct answer
- Header: "Answer: [Letter]"
- Body: Rationale + distractor analysis
- References anchors that explain the answer

---

## Slide Count Formulas

### By Delivery Mode

| Mode | Anchor Count | Slides Formula |
|------|--------------|----------------|
| Foundational | Any (first subsection) | ceil(anchors / 2) + 2 (overview + bridge) |
| Full | 5+ anchors | ceil(anchors / 2) + 2 (connection + synthesis) |
| Minor | 3-4 anchors | ceil(anchors / 2) + 1 (connection) |
| One-and-Done | 1-2 anchors | 1-2 slides |

### Fixed Slides (Always Present)
- Section Intro: 1
- Vignette: 1
- Answer: 1
- **Total Fixed:** 3

---

## Planning Rules

1. **First subsection** always uses Foundational mode
2. **Mode selection** based on anchor count:
   - 5+ anchors = Full mode
   - 3-4 anchors = Minor mode
   - 1-2 anchors = One-and-Done mode
3. **Slide splitting** when anchor content exceeds 8 lines
4. **FRONTLOAD anchors** positioned at start of subsection
5. **XREF anchors** get abbreviated treatment (1 slide max)

---

## Error Handling

| Error | Action |
|-------|--------|
| Too few anchors for min slides | Expand content, add examples |
| Too many anchors for max slides | Combine related anchors |
| Unassigned anchors | Force assignment to existing slides |
| No clear vignette concepts | Use most clinically relevant anchors |

---

## Integration Points

### Upstream
- Receives section outline from Step 4 (outline_generator)

### Downstream
- Passes slide plan to content_slide_generator
- Anchor assignments used by anchor_coverage_tracker (R8)

### Skills Used
- skills/enforcement/anchor_coverage_enforcer.py - get_anchor_assignment_plan()
- skills/validation/anchor_coverage_tracker.py - AnchorCoverageTracker

---

## Anchor Assignment (REQUIRED)

During slide planning, you MUST assign ALL anchors to slides:

### 1. Get Assignment Plan
- Input: Step 4 anchors
- Output: Anchor-to-slide mapping
- Skill: `skills/enforcement/anchor_coverage_enforcer.py::get_anchor_assignment_plan()`

### 2. Assignment Rules
- **FRONTLOAD anchors:** First slides of subsection (within slides 2-4)
- **XREF anchors:** Can share slide with other anchor (abbreviated treatment)
- **Regular anchors:** 1-2 per content slide

### 3. Output Format
Include in `slide_plan.slides`:
```json
{
  "slide_number": 2,
  "slide_type": "Content",
  "title_hint": "Hand Hygiene Principles",
  "assigned_anchors": ["Hand hygiene principles", "WHO five moments"],
  "content_focus": "Core hand hygiene concepts and WHO moments",
  "estimated_duration_seconds": 120
}
```

### 4. Validation Before Return
Before returning the plan, verify ALL input anchors are assigned:
```
Input anchor count == Sum of all assigned_anchors across slides
```

If any anchor is unassigned, add it to the nearest appropriate content slide
within its subsection.

---

## Validation Checklist
- [ ] All anchors assigned to slides
- [ ] Slide count: 12-35 range
- [ ] Slide 1 is Section Intro
- [ ] Has exactly 1 Vignette slide
- [ ] Has exactly 1 Answer slide
- [ ] Content slides have 1-3 anchors each
- [ ] Logical topic progression

---

**Agent Version:** 1.1
**Last Updated:** 2026-01-05
