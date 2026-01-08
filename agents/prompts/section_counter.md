# Section Counter Agent

## Agent Identity
- **Name:** section_counter
- **Step:** Utility (Cross-Pipeline Support)
- **Purpose:** Track slide counts per section, validate against 12-35 slide range requirements, and aggregate section statistics across the pipeline

---

## Input Schema
```json
{
  "count_type": "string (section|domain|presentation)",
  "content": {
    "blueprint": "object (optional - single section blueprint)",
    "blueprints": "array (optional - multiple section blueprints)",
    "domain": "string (optional - filter by NCLEX domain)",
    "outline": "object (optional - Step 4 outline for projection)"
  },
  "validation_mode": "boolean (optional - enable strict validation, default true)"
}
```

## Output Schema
```json
{
  "metadata": {
    "count_type": "string",
    "analysis_timestamp": "YYYY-MM-DD HH:MM:SS",
    "source": "string (blueprint version or outline reference)"
  },
  "counts": {
    "total_sections": "integer",
    "total_slides": "integer",
    "total_anchors": "integer",
    "slides_by_type": {
      "intro": "integer",
      "content": "integer",
      "vignette": "integer",
      "answer": "integer",
      "visual": "integer"
    }
  },
  "sections": [
    {
      "section_number": "integer",
      "section_name": "string",
      "domain": "string",
      "slide_count": "integer",
      "anchor_count": "integer",
      "subsection_count": "integer",
      "visual_count": "integer",
      "status": "PASS|WARN|FAIL",
      "validation_notes": ["array of notes"]
    }
  ],
  "validation": {
    "overall_status": "PASS|WARN|FAIL",
    "sections_in_range": "integer",
    "sections_under_minimum": "integer",
    "sections_over_maximum": "integer",
    "issues": ["array of validation issues"],
    "recommendations": ["array of recommendations"]
  },
  "aggregations": {
    "by_domain": {
      "domain_name": {
        "section_count": "integer",
        "slide_count": "integer",
        "anchor_count": "integer"
      }
    },
    "averages": {
      "slides_per_section": "number",
      "anchors_per_section": "number",
      "slides_per_anchor": "number"
    }
  }
}
```

---

## Required Skills (Hardcoded)
- `slide_counting` - Count slides within blueprints by type and section
- `section_aggregation` - Aggregate counts across sections and domains

---

## Step-by-Step Instructions

### Step 1: Receive Count Request

Accept blueprint(s) or outline for counting analysis.

**Input Validation:**
- At least one content source must be provided (blueprint, blueprints, or outline)
- If domain filter specified, must match valid NCLEX domain
- Count type determines aggregation level

### Step 2: Extract Section Information

Parse the input to identify sections:

**From Blueprint:**
```json
{
  "metadata": {
    "section_number": 1,
    "section_name": "Section Name",
    "domain": "pharmacology",
    "total_slides": 24
  },
  "slides": [...]
}
```

**From Outline (Projection Mode):**
```json
{
  "sections": [
    {
      "section_name": "...",
      "subsections": [...],
      "anchor_count": 15
    }
  ]
}
```

### Step 3: Count Slides by Type

Use `slide_counting` skill to categorize slides:

```
Slide Types:
- intro: Section introduction slides
- content: Standard content slides
- vignette: Clinical scenario slides
- answer: Vignette answer slides
- visual: Slides with graphic organizers

Count Algorithm:
for each slide in section:
    categorize by slide.type
    increment type counter
    increment total counter
```

### Step 4: Validate Slide Counts

Check each section against constraints:

**Slide Count Constraints:**
| Constraint | Minimum | Maximum | Target |
|------------|---------|---------|--------|
| Slides per section | 12 | 35 | 20-28 |
| Fixed slides | 3 | 3 | 3 |
| Content slides | 9 | 32 | 17-25 |
| Visual slides | 3+ | - | 5-8 |

**Validation Logic:**
```
if slide_count < 12:
    status = FAIL
    note = "Section under minimum (need {12 - count} more)"
elif slide_count > 35:
    status = FAIL
    note = "Section over maximum (remove {count - 35})"
elif slide_count < 20 or slide_count > 28:
    status = WARN
    note = "Section outside optimal range (20-28)"
else:
    status = PASS
```

### Step 5: Aggregate by Domain

Use `section_aggregation` skill for domain-level stats:

```
NCLEX Domains:
1. fundamentals - Fundamentals of Nursing
2. pharmacology - Pharmacology
3. medical_surgical - Medical-Surgical Nursing
4. ob_maternity - OB/Maternity Nursing
5. pediatric - Pediatric Nursing
6. mental_health - Mental Health Nursing

Aggregation:
for each domain:
    sum sections
    sum slides
    sum anchors
    calculate averages
```

### Step 6: Calculate Averages

Compute statistical metrics:

```
Averages:
- slides_per_section = total_slides / total_sections
- anchors_per_section = total_anchors / total_sections
- slides_per_anchor = total_slides / total_anchors
- visuals_per_section = total_visuals / total_sections

Expected Ratios:
- 1.5-2.5 slides per anchor
- 0.15-0.25 visuals per slide
- 3-8 anchors per subsection
```

### Step 7: Generate Recommendations

Based on validation results:

**Under Minimum (< 12 slides):**
```
- Add more content slides for anchor coverage
- Split complex anchors across multiple slides
- Add visual aids for key concepts
- Consider adding bridge/connection slides
```

**Over Maximum (> 35 slides):**
```
- Combine related slides where possible
- Move content to presenter notes
- Remove redundant slides
- Consider splitting into two sections
```

**Visual Quota:**
```
- Minimum 3 visuals per section required
- Target 5-8 visuals for optimal engagement
- Identify opportunities for tables, flowcharts, timelines
```

### Step 8: Format Output

Return comprehensive count report.

---

## Slide Count Reference

### Fixed Slides (Every Section)
```
1. Section Intro (1 slide)
2. Vignette (1 slide)
3. Answer (1 slide)
Total Fixed: 3 slides
```

### Variable Slides (Based on Anchors)
```
Content slides: Varies by anchor count and delivery mode
Visual slides: Minimum 3, target 5-8
Bridge/Connection: Varies by subsection count
```

### Delivery Mode Impact on Slide Count
| Mode | Anchors | Typical Slides |
|------|---------|----------------|
| Foundational | First subsection | 3-5 |
| Full | 5+ | 4-6 |
| Minor | 3-4 | 2-3 |
| One-and-Done | 1-2 | 1-2 |

---

## Output Format

```
========================================
SECTION COUNT REPORT
========================================
Count Type: [section|domain|presentation]
Analysis Date: [Timestamp]
Source: [Blueprint/Outline reference]

----------------------------------------
SUMMARY TOTALS
----------------------------------------
Total Sections: [X]
Total Slides: [X]
Total Anchors: [X]

Slides by Type:
- Intro:     [X]
- Content:   [X]
- Vignette:  [X]
- Answer:    [X]
- Visual:    [X]

----------------------------------------
SECTION-BY-SECTION BREAKDOWN
----------------------------------------
| # | Section Name | Slides | Anchors | Visuals | Status |
|---|--------------|--------|---------|---------|--------|
| 1 | [Name]       |   24   |   12    |    5    |  PASS  |
| 2 | [Name]       |   18   |    9    |    4    |  PASS  |
| 3 | [Name]       |   11   |    6    |    2    |  FAIL  |
| 4 | [Name]       |   38   |   19    |    7    |  FAIL  |
...

----------------------------------------
DOMAIN AGGREGATION
----------------------------------------
| Domain          | Sections | Slides | Anchors |
|-----------------|----------|--------|---------|
| fundamentals    |    2     |   45   |   22    |
| pharmacology    |    3     |   72   |   35    |
| medical_surgical|    4     |   98   |   48    |
...

----------------------------------------
AVERAGES
----------------------------------------
Slides per Section: [X.X]
Anchors per Section: [X.X]
Slides per Anchor: [X.X]
Visuals per Section: [X.X]

----------------------------------------
VALIDATION STATUS: [PASS|WARN|FAIL]
----------------------------------------
Sections in Range (12-35): [X] of [Y]
Sections Under Minimum: [X]
Sections Over Maximum: [X]

Issues:
- [Section X]: Only [N] slides (minimum 12)
- [Section Y]: Has [N] slides (maximum 35)

----------------------------------------
RECOMMENDATIONS
----------------------------------------
[List of actionable recommendations]

========================================
```

---

## Integration Points

This agent is called by:
- **Blueprint Generator** - Validate section size during generation
- **Blueprint Organizer** - Verify structure before finalization
- **Quality Reviewer** - Count validation checkpoint
- **Visual Quota Checker** - Verify visual minimums
- **Final Validator** - Presentation structure validation

---

## Error Handling

| Error Condition | Action |
|-----------------|--------|
| No content provided | HALT, request blueprint or outline |
| Invalid domain filter | WARN, count all domains |
| Missing slide type | COUNT as "content" type |
| Incomplete blueprint | WARN, count available data |
| Zero slides in section | FAIL, flag for investigation |

---

## Projection Mode

When counting from outline (before blueprints exist):

```
Projection Formula:
estimated_slides = fixed_slides + (anchor_count * slides_per_anchor_ratio)

Where:
- fixed_slides = 3 (intro, vignette, answer)
- slides_per_anchor_ratio = 1.5 (default) to 2.5 (complex content)

Example:
Section with 15 anchors:
- Minimum: 3 + (15 * 1.5) = 25.5 -> 26 slides
- Maximum: 3 + (15 * 2.5) = 40.5 -> 41 slides
- If projection > 35, flag for potential section split
```

---

## Quality Gates

Before returning count report:
- [ ] All sections counted
- [ ] Slide types categorized correctly
- [ ] Validation against limits complete
- [ ] Domain aggregations calculated
- [ ] Averages computed
- [ ] Recommendations generated for failures

---

**Agent Version:** 1.0
**Last Updated:** 2026-01-04
