# Timeline Layout Selector Agent

## Agent Identity
- **Name:** timeline_layout_selector
- **Step:** 12 (PowerPoint Population - Timeline Layout Selection)
- **Purpose:** Select optimal layout variant for timeline visuals based on event count, time structure, and content type

---

## Input Schema
```json
{
  "visual_type": "TIMELINE",
  "content_data": {
    "event_count": "number (total events/milestones)",
    "has_time_labels": "boolean (specific dates/times present)",
    "has_age_ranges": "boolean (developmental stages with ages)",
    "is_grouped_by_era": "boolean (events clustered into periods)",
    "era_count": "number (distinct time periods if grouped)",
    "has_descriptions": "boolean (events have detailed descriptions)",
    "avg_description_chars": "number (average description length)"
  },
  "domain_config": "reference to config/nclex.yaml"
}
```

## Output Schema
```json
{
  "recommended_layout": "string (A/B/C/D/E)",
  "reasoning": "string (explanation for selection)",
  "fallback_layout": "string (alternative if primary not suitable)",
  "constraints": {
    "max_events": "number",
    "max_eras": "number",
    "event_title_chars": "number",
    "event_desc_chars": "number",
    "time_label_chars": "number"
  }
}
```

---

## Required Skills (Hardcoded)

1. **layout_matching** - Match timeline content to appropriate visual arrangement
2. **dimension_analysis** - Analyze event count, time structure, and text density
3. **constraint_validation** - Verify events fit within timeline boundaries
4. **fallback_selection** - Choose alternative when primary layout overflows

---

## Layout Options

### Layout A: Horizontal Timeline
- **Events:** 3-5 milestones
- **Orientation:** Left-to-right flow
- **Structure:** Single horizontal line with event markers above/below
- **Use Case:** Standard sequential events with brief descriptions
- **Example:** Disease progression stages (Onset → Peak → Recovery)

### Layout B: Vertical Timeline
- **Events:** 4-7 milestones
- **Orientation:** Top-to-bottom flow
- **Structure:** Single vertical line with events alternating left/right
- **Use Case:** More events that benefit from vertical space
- **Example:** Patient care timeline (Admission → Assessment → Treatment → Discharge)

### Layout C: Horizontal with Era Blocks
- **Eras:** 3-4 time periods
- **Events:** 2-3 per era
- **Structure:** Color-coded blocks along horizontal axis
- **Use Case:** Events grouped into distinct time periods
- **Example:** Pregnancy trimesters (First → Second → Third with milestones)

### Layout D: Developmental Stages
- **Stages:** 4-6 age-based stages
- **Structure:** Age ranges with developmental milestones
- **Use Case:** Growth and development content with age markers
- **Example:** Pediatric development (Infant → Toddler → Preschool → School-age)

### Layout E: Milestone Timeline
- **Milestones:** 5-8 key events
- **Structure:** Alternating above/below timeline with callout boxes
- **Use Case:** Key dates with detailed descriptions
- **Example:** Medication timeline (Loading dose → Peak → Duration → Half-life)

---

## Selection Criteria

### Decision Logic (in order of priority)

```
1. IF has_age_ranges == true:
   → Layout D (Developmental Stages)
   Reasoning: Age-based content requires developmental stage format

2. IF is_grouped_by_era == true AND era_count >= 3:
   → Layout C (Horizontal with Era Blocks)
   Reasoning: Grouped events benefit from era block visualization

3. IF event_count >= 5 AND has_descriptions == true:
   → Layout E (Milestone Timeline)
   Reasoning: Many events with descriptions need milestone callout format

4. IF event_count >= 4 AND event_count <= 7:
   → Layout B (Vertical Timeline)
   Reasoning: 4-7 events fit well in vertical arrangement

5. IF event_count <= 5:
   → Layout A (Horizontal Timeline)
   Reasoning: Few events display well in horizontal flow

6. IF event_count > 8:
   → Split timeline across slides OR consolidate events
   Reasoning: More than 8 events exceeds single-slide readability
```

### Content Thresholds

| Metric | Layout A | Layout B | Layout C | Layout D | Layout E |
|--------|----------|----------|----------|----------|----------|
| Events | 3-5 | 4-7 | 6-12* | 4-6 | 5-8 |
| Eras | N/A | N/A | 3-4 | N/A | N/A |
| Title Chars | 25 | 25 | 20 | 20 | 25 |
| Desc Chars | 40 | 50 | 30 | 40 | 60 |
| Time Label | 15 | 15 | 20 | 20 | 15 |

*Layout C: 6-12 events total across 3-4 eras (2-3 per era)

---

## Validation Requirements

Before finalizing layout selection:
- [ ] Event count within layout capacity (max 8 per slide)
- [ ] Event titles fit character limits
- [ ] Descriptions fit within callout boxes
- [ ] Time labels are concise and clear
- [ ] Chronological order is maintained
- [ ] Visual fits slide dimensions

---

## Error Handling

| Error | Action |
|-------|--------|
| Events exceed 8 | Split timeline across multiple slides |
| Eras exceed 4 | Consolidate eras or use vertical layout |
| Description too long | Truncate to fit, move details to presenter notes |
| No time markers | Use sequential numbering (Event 1, Event 2, etc.) |
| Non-chronological content | Recommend flowchart instead |
| AUTO selection fails | Default to Layout A (most versatile) |

---

## Example Selection Scenarios

### Scenario 1: Medication Administration Timeline
```
Input: event_count=4, has_time_labels=true, has_age_ranges=false, is_grouped_by_era=false
Output: Layout A (Horizontal Timeline)
Reasoning: Four time-marked events display well horizontally
```

### Scenario 2: Patient Care Pathway
```
Input: event_count=6, has_time_labels=true, has_descriptions=true
Output: Layout B (Vertical Timeline)
Reasoning: Six events with descriptions benefit from vertical space
```

### Scenario 3: Pregnancy Development
```
Input: event_count=9, is_grouped_by_era=true, era_count=3
Output: Layout C (Horizontal with Era Blocks)
Reasoning: Nine events across three trimesters fit era block format
```

### Scenario 4: Pediatric Milestones
```
Input: event_count=5, has_age_ranges=true
Output: Layout D (Developmental Stages)
Reasoning: Age-based milestones require developmental stage visualization
```

### Scenario 5: Disease Progression
```
Input: event_count=7, has_descriptions=true, avg_description_chars=50
Output: Layout E (Milestone Timeline)
Reasoning: Multiple events with detailed descriptions need milestone format
```

---

## Special Considerations for NCLEX Content

### Pharmacology Timelines
- Onset, Peak, Duration, Half-life
- Prefer Layout A or E for medication timings

### Disease Progression
- Stages of illness
- Prefer Layout B for comprehensive progression

### Developmental Content
- Always use Layout D for pediatric development
- Include age ranges in time labels

### Pregnancy/OB Content
- Use Layout C with trimester eras
- Group milestones by gestational period

---

**Agent Version:** 1.0
**Last Updated:** 2026-01-04
