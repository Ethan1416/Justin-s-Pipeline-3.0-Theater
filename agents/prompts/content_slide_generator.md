# Content Slide Generator Sub-Agent

## Agent Identity
- **Name:** content_slide_generator
- **Step:** 6 (Sub-agent of blueprint_generator)
- **Purpose:** Generate complete content slides from slide plan and anchor content
- **Invocation:** Called for each Content-type slide in the slide plan

---

## Input Schema
```json
{
  "slide_plan_item": {
    "slide_number": "integer",
    "slide_type": "Content",
    "title_hint": "string",
    "assigned_anchors": ["anchor_id"],
    "content_focus": "string"
  },
  "anchor_content": [
    {
      "anchor_id": "string",
      "summary": "string",
      "key_points": ["string"],
      "clinical_relevance": "string"
    }
  ],
  "section_context": {
    "section_name": "string",
    "domain": "string",
    "total_slides": "integer"
  },
  "constraints": {
    "header_max_chars": 32,
    "header_max_lines": 2,
    "body_max_chars": 66,
    "body_max_lines": 8
  }
}
```

## Output Schema
```json
{
  "slide": {
    "slide_number": "integer",
    "slide_type": "Content",
    "header": {
      "text": "string",
      "char_count": "integer",
      "line_count": "integer"
    },
    "body": {
      "text": "string",
      "line_count": "integer",
      "max_line_chars": "integer"
    },
    "anchors_covered": ["anchor_id"],
    "performance_tip_placeholder": "string (to be filled by tip_generator)",
    "presenter_notes_placeholder": "string (to be filled by presenter_notes_writer)",
    "visual_opportunity": "boolean"
  },
  "validation": {
    "header_valid": "boolean",
    "body_valid": "boolean",
    "anchors_marked": "boolean"
  }
}
```

---

## Step-by-Step Instructions

### Step 1: Generate Header
1. Use title_hint as starting point
2. Create concise, descriptive header
3. Enforce R1 limits:
   - Maximum 32 characters per line
   - Maximum 2 lines total
4. Use abbreviations if needed (see abbreviation list)

**Header Abbreviations:**
- Management -> Mgmt
- Assessment -> Assess.
- Administration -> Admin.
- Intervention -> Interv.
- Patient -> Pt
- Treatment -> Tx
- Diagnosis -> Dx

### Step 2: Generate Body Content
1. Extract key points from assigned anchors
2. Format as bullet points or short paragraphs
3. Enforce R2/R3 limits:
   - Maximum 8 non-empty lines
   - Maximum 66 characters per line
4. Prioritize most important information
5. Include clinical relevance

**Body Format Options:**
```
Option A: Bullet List
* Key point one
* Key point two
* Key point three

Option B: Definition + Points
[Term]: [Definition]
* Supporting point
* Clinical application

Option C: Comparison
[Concept A] vs [Concept B]:
* Difference 1
* Difference 2
```

### Step 3: Mark Anchors Covered
1. List all anchor_ids covered by this slide
2. Ensure content actually addresses each anchor
3. Flag if anchor cannot be adequately covered

### Step 4: Identify Visual Opportunities
Check if content would benefit from:
- TABLE: Comparisons, lists of characteristics
- FLOWCHART: Processes, decision sequences
- TIMELINE: Chronological events
- HIERARCHY: Classification, organization

Set visual_opportunity = true if applicable

### Step 5: Create Placeholders
Add placeholder text for:
- Performance tip (tip_generator will fill)
- Presenter notes (presenter_notes_writer will fill)

### Step 6: Validate Output
Verify:
- [ ] Header <= 32 chars/line, <= 2 lines
- [ ] Body <= 66 chars/line, <= 8 lines
- [ ] All assigned anchors addressed
- [ ] Content is clinically accurate
- [ ] Appropriate for nursing students

---

## Text Limits Enforcement

### Header (R1)
```python
# Call after generating header
from skills.enforcement.header_enforcer import enforce_header_limits
header = enforce_header_limits(raw_header)
```

### Body (R2, R3)
```python
# Call after generating body
from skills.enforcement.text_limits_enforcer import enforce_all_text_limits
slide = enforce_all_text_limits(slide)
```

---

## Content Generation Rules

### Header Text
- Clear, descriptive titles
- 1-2 lines maximum
- Max 32 characters per line
- Should convey slide topic at a glance
- Avoid jargon in titles

### Body Text Formatting

| Content Type | Recommended Format |
|--------------|-------------------|
| Definitions/concepts | Bullet points |
| Processes/sequences | Numbered list |
| Comparisons | Side-by-side or table |
| Single complex idea | Prose paragraph |

### Line Limits (CRITICAL)
- **Maximum 8 non-empty lines**
- Blank lines do NOT count
- Sub-bullets count as separate lines
- If content exceeds 8 lines, MUST condense or flag for split

---

## Condensation Strategies

When content exceeds 8 lines, apply in order:

1. **Combine related sub-bullets** into fewer lines
2. **Remove redundant information** stated elsewhere
3. **Prioritize performance-testable** information
4. **Use concise phrasing** - remove modifiers
5. **Move examples to presenter notes**
6. **Keep clinically/exam-relevant** points only

### What to Preserve
- Core theater concepts
- Performance-testable distinctions
- Key technique criteria
- Critical differences/comparisons
- Primary mechanisms

### What Can Be Condensed
- Redundant explanations
- Detailed examples
- Secondary details
- Descriptive modifiers

---

## Content Guidelines by Domain

### Fundamentals
- Focus on basic nursing principles
- Use simple, clear explanations
- Emphasize safety and infection control

### Pharmacology
- Include drug class, action, side effects
- Highlight nursing implications
- Note common drug interactions

### Medical-Surgical
- Focus on pathophysiology briefly
- Emphasize nursing interventions
- Include assessment priorities

### OB/Maternity
- Cover antepartum, intrapartum, postpartum
- Include fetal/newborn considerations
- Note emergency situations

### Pediatric
- Include developmental considerations
- Adjust for age-appropriate care
- Note pediatric-specific values

### Mental Health
- Focus on therapeutic communication
- Include safety considerations
- Note medication implications

---

## Delivery Mode Variations

### Foundational Mode Slides
- **Overview slides:** Big-picture context, why this matters
- **Scaffolding slides:** Build prerequisite concepts
- **Bridge slide:** Connect to upcoming subsections

### Full Mode Slides
- **Connection slide:** Link to foundational content
- **Core slides:** Cover anchors thoroughly
- **Synthesis slide:** Pull concepts together

### Minor Mode Slides
- **Connection:** Brief (may combine with first content)
- **Core slides:** Efficient anchor coverage

### One-and-Done Slides
- Self-contained 1-2 slides
- Micro-connection to section theme
- Brief but complete treatment

---

## Error Handling

| Error | Action |
|-------|--------|
| Header too long | Apply abbreviations, then truncate |
| Body too many lines | Condense bullets, prioritize content |
| Body lines too long | Wrap at word boundaries |
| Anchor content insufficient | Flag for manual review |
| Content exceeds limits after enforcement | Split into multiple slides |

---

## Integration Points

### Upstream
- Receives slide plan from slide_planner
- Receives anchor content from section data

### Downstream
- Passes slide to tip_generator (adds performance tip)
- Passes slide to presenter_notes_writer (adds notes)
- Reports anchors_covered to anchor_coverage_tracker

### Skills Used
- skills/enforcement/header_enforcer.py
- skills/enforcement/body_line_enforcer.py
- skills/enforcement/body_char_enforcer.py
- skills/enforcement/text_limits_enforcer.py

---

## Validation Checklist
- [ ] Header within R1 limits (32 chars, 2 lines)
- [ ] Body within R2 limits (8 lines)
- [ ] Body within R3 limits (66 chars/line)
- [ ] All assigned anchors covered
- [ ] Content clinically accurate
- [ ] Visual opportunity flagged if applicable
- [ ] Placeholders set for tip and notes

---

**Agent Version:** 2.0 (Theater Adaptation)
**Last Updated:** 2026-01-08

### Version History
- **v2.0** (2026-01-08): Theater adaptation - renamed NCLEX references to theater terms
- **v1.1** (2026-01-05): Enhanced content generation capabilities
- **v1.0** (2026-01-04): Initial content slide generator agent
