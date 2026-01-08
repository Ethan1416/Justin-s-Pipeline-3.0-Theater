# Spectrum Layout Selector Agent

## Agent Identity
- **Name:** spectrum_layout_selector
- **Step:** 12 (PowerPoint Population - Spectrum Layout Selection)
- **Purpose:** Select optimal layout variant for spectrum visuals based on segment count, polarity, and dimensional requirements

---

## Input Schema
```json
{
  "visual_type": "SPECTRUM",
  "content_data": {
    "segment_count": "number (distinct levels/segments)",
    "is_bipolar": "boolean (has opposite poles)",
    "has_neutral_center": "boolean (middle/neutral point emphasized)",
    "is_discrete": "boolean (distinct segments vs continuous)",
    "has_second_dimension": "boolean (two-axis spectrum)",
    "left_pole_label": "string (low end label)",
    "right_pole_label": "string (high end label)",
    "segment_labels": "array of strings"
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
    "max_segments": "number",
    "segment_label_chars": "number",
    "pole_label_chars": "number",
    "requires_gradient": "boolean"
  }
}
```

---

## Required Skills (Hardcoded)

1. **layout_matching** - Match spectrum type to appropriate visual layout
2. **dimension_analysis** - Analyze segment count, polarity, and dimensionality
3. **constraint_validation** - Verify spectrum content fits layout boundaries
4. **fallback_selection** - Choose alternative when primary layout insufficient

---

## Layout Options

### Layout A: Horizontal Bar Spectrum
- **Segments:** 3-5 levels
- **Orientation:** Left-to-right gradient
- **Structure:** Single horizontal bar with color gradient
- **Use Case:** Standard gradient bar showing progression
- **Example:** Pain scale (None → Mild → Moderate → Severe)

### Layout B: Vertical Bar Spectrum
- **Segments:** 4-7 levels
- **Orientation:** Bottom-to-top gradient
- **Structure:** Single vertical bar with color gradient
- **Use Case:** More segments requiring vertical space
- **Example:** Glasgow Coma Scale (3 → 15 with descriptors)

### Layout C: Bipolar Spectrum with Center
- **Segments:** 3-5 levels
- **Structure:** Opposite poles with emphasized neutral center
- **Use Case:** Concepts with true opposites and a middle ground
- **Example:** Fluid balance (Dehydrated ← Euvolemic → Overloaded)

### Layout D: Segmented Spectrum
- **Segments:** 3-6 discrete levels
- **Structure:** Distinct color-coded segments (not gradient)
- **Use Case:** Discrete categories along a continuum
- **Example:** Risk levels (Low | Moderate | High | Critical)

### Layout E: Dual-Axis Spectrum
- **Axes:** 2 perpendicular dimensions
- **Quadrants:** 4 resulting categories
- **Structure:** Two intersecting spectrums creating quadrants
- **Use Case:** Two independent dimensions creating four outcomes
- **Example:** Urgency vs Severity (4-quadrant triage)

---

## Selection Criteria

### Decision Logic (in order of priority)

```
1. IF has_second_dimension == true:
   → Layout E (Dual-Axis Spectrum)
   Reasoning: Two dimensions require quadrant visualization

2. IF is_bipolar == true AND has_neutral_center == true:
   → Layout C (Bipolar Spectrum with Center)
   Reasoning: Opposite poles with neutral center need specialized layout

3. IF is_discrete == true AND segment_count >= 3:
   → Layout D (Segmented Spectrum)
   Reasoning: Discrete categories benefit from distinct segment blocks

4. IF segment_count >= 5:
   → Layout B (Vertical Bar Spectrum)
   Reasoning: Many segments fit better vertically

5. IF segment_count <= 5:
   → Layout A (Horizontal Bar Spectrum)
   Reasoning: Standard gradient bar for typical spectrum

6. IF segment_count > 7:
   → Consider TABLE or split spectrum
   Reasoning: More than 7 segments exceeds visual clarity
```

### Content Thresholds

| Metric | Layout A | Layout B | Layout C | Layout D | Layout E |
|--------|----------|----------|----------|----------|----------|
| Segments | 3-5 | 4-7 | 3-5 | 3-6 | 2 per axis |
| Orientation | Horizontal | Vertical | Horizontal | Horizontal | Both |
| Gradient | Yes | Yes | Yes (bipolar) | No | Optional |
| Center Emphasis | No | No | Yes | No | Yes |
| Pole Label Chars | 20 | 20 | 20 | 15 | 15 |
| Segment Chars | 15 | 20 | 15 | 20 | 15 |

---

## Validation Requirements

Before finalizing layout selection:
- [ ] Segment count within layout capacity (max 7)
- [ ] Pole labels fit character limits
- [ ] Segment labels fit within segment width
- [ ] Color gradient is appropriate for content type
- [ ] Center point is logical (for bipolar)
- [ ] Two dimensions are truly independent (for dual-axis)

---

## Error Handling

| Error | Action |
|-------|--------|
| Segments exceed 7 | Convert to TABLE or categorized list |
| Missing pole labels | Use generic "Low"/"High" labels |
| Segment labels too long | Abbreviate or use legend |
| Non-continuous data | Use Layout D (discrete segments) |
| More than 2 dimensions | Split into multiple spectrums |
| AUTO selection fails | Default to Layout A (most versatile) |

---

## Example Selection Scenarios

### Scenario 1: Pain Assessment Scale
```
Input: segment_count=5, is_bipolar=false, is_discrete=false
Output: Layout A (Horizontal Bar Spectrum)
Reasoning: Five-level continuous pain scale fits horizontal gradient
```

### Scenario 2: Glasgow Coma Scale
```
Input: segment_count=6, is_discrete=true
Output: Layout B (Vertical Bar Spectrum)
Reasoning: Six GCS categories with scores benefit from vertical layout
```

### Scenario 3: Fluid Balance
```
Input: segment_count=3, is_bipolar=true, has_neutral_center=true
Output: Layout C (Bipolar Spectrum with Center)
Reasoning: Dehydration-Euvolemic-Overload requires bipolar visualization
```

### Scenario 4: Risk Stratification
```
Input: segment_count=4, is_discrete=true, is_bipolar=false
Output: Layout D (Segmented Spectrum)
Reasoning: Discrete risk levels need distinct segment blocks
```

### Scenario 5: Triage Assessment
```
Input: has_second_dimension=true, segment_count=2 per axis
Output: Layout E (Dual-Axis Spectrum)
Reasoning: Urgency vs Severity creates four-quadrant triage system
```

---

## Color Recommendations by Content Type

### Pain/Severity Scales
- Green (low) → Yellow → Orange → Red (high)
- Layout A or D recommended

### Balance/Equilibrium
- Blue (deficit) → Green (normal) → Purple (excess)
- Layout C recommended for bipolar

### Risk Assessment
- Green (low) → Yellow (moderate) → Orange (high) → Red (critical)
- Layout D recommended for discrete levels

### Lab Values
- Blue (low) → Green (normal) → Red (high)
- Layout C recommended with normal center emphasis

### Dual-Axis Content
- Use contrasting color pairs for each axis
- Layout E with clear quadrant coloring

---

## Special Considerations for NCLEX Content

### Vital Signs
- Normal ranges with abnormal poles
- Use Layout C with normal range emphasized

### Lab Interpretations
- Reference range spectrums
- Use Layout D for distinct categories

### Assessment Scores
- GCS, Apgar, etc.
- Use Layout B for multi-level scoring

### Priority/Triage
- Urgency classifications
- Use Layout D or E based on dimensions

---

**Agent Version:** 1.0
**Last Updated:** 2026-01-04
