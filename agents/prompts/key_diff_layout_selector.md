# Key Differentiators Layout Selector Agent

## Agent Identity
- **Name:** key_diff_layout_selector
- **Step:** 12 (PowerPoint Population - Key Differentiators Layout Selection)
- **Purpose:** Select optimal layout variant for key differentiators visuals based on concept count, differentiator count, and comparison structure

---

## Input Schema
```json
{
  "visual_type": "KEY_DIFFERENTIATORS",
  "content_data": {
    "concept_count": "number (items being compared)",
    "differentiator_count": "number (key differences highlighted)",
    "feature_count": "number (comparison attributes)",
    "has_single_critical_diff": "boolean (one main distinguishing factor)",
    "is_matrix_format": "boolean (features across multiple concepts)",
    "concept_labels": "array of strings",
    "differentiator_labels": "array of strings"
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
    "max_concepts": "number",
    "max_differentiators": "number",
    "max_features": "number",
    "concept_label_chars": "number",
    "diff_label_chars": "number"
  }
}
```

---

## Required Skills (Hardcoded)

1. **layout_matching** - Match differentiator structure to appropriate visual layout
2. **dimension_analysis** - Analyze concept count, differentiators, and features
3. **constraint_validation** - Verify comparison fits layout boundaries
4. **fallback_selection** - Choose alternative when content exceeds layout capacity

---

## Layout Options

### Layout A: Side-by-Side Comparison
- **Concepts:** 2 items
- **Features:** 3-5 comparison points
- **Structure:** Two columns with shared feature rows
- **Use Case:** Standard VS comparison with multiple attributes
- **Example:** Type 1 vs Type 2 Diabetes (Onset | Insulin | Ketosis | Age)

### Layout B: Centered Key Differentiator
- **Concepts:** 2 items
- **Key Diff:** 1 critical distinction
- **Structure:** Two sides with large central differentiator highlighted
- **Use Case:** Single most important distinguishing factor
- **Example:** Crohn's vs UC with "Skip Lesions" as central differentiator

### Layout C: Multiple Differentiators
- **Concepts:** 2 items
- **Key Diffs:** 2-4 highlighted differences
- **Structure:** Two sides with multiple emphasized differences
- **Use Case:** Several key differences need equal emphasis
- **Example:** STEMI vs NSTEMI (ST Elevation | Troponin | Treatment | Urgency)

### Layout D: Three-Way Discrimination
- **Concepts:** 3 items
- **Structure:** Triangle arrangement with differences on edges
- **Use Case:** Distinguishing three similar conditions
- **Example:** MI vs Angina vs Pericarditis (triangular comparison)

### Layout E: Feature Matrix
- **Concepts:** 2-4 items
- **Features:** 4-6 comparison attributes
- **Structure:** Matrix grid with checkmarks/icons
- **Use Case:** Comprehensive multi-concept comparison
- **Example:** Anemia types (Iron | B12 | Folate | Chronic Disease comparison)

---

## Selection Criteria

### Decision Logic (in order of priority)

```
1. IF concept_count == 3:
   → Layout D (Three-Way Discrimination)
   Reasoning: Three concepts require triangle arrangement

2. IF concept_count >= 3 OR feature_count >= 5:
   → Layout E (Feature Matrix)
   Reasoning: Multiple concepts or many features need matrix format

3. IF differentiator_count >= 2 AND differentiator_count <= 4:
   → Layout C (Multiple Differentiators)
   Reasoning: Several key differences need equal visual emphasis

4. IF has_single_critical_diff == true:
   → Layout B (Centered Key Differentiator)
   Reasoning: Single critical distinction needs central emphasis

5. IF concept_count == 2 AND feature_count <= 5:
   → Layout A (Side-by-Side Comparison)
   Reasoning: Standard two-concept comparison with moderate features

6. IF concept_count > 4:
   → Use TABLE format instead
   Reasoning: More than 4 concepts exceeds key diff visual capacity
```

### Content Thresholds

| Metric | Layout A | Layout B | Layout C | Layout D | Layout E |
|--------|----------|----------|----------|----------|----------|
| Concepts | 2 | 2 | 2 | 3 | 2-4 |
| Features | 3-5 | 2-3 | 3-4 | 3 | 4-6 |
| Key Diffs | N/A | 1 | 2-4 | 3 | N/A |
| Concept Chars | 25 | 25 | 20 | 20 | 20 |
| Feature Chars | 30 | 20 | 25 | 25 | 20 |
| Diff Chars | N/A | 30 | 20 | 20 | N/A |

---

## Validation Requirements

Before finalizing layout selection:
- [ ] Concept count within layout capacity (max 4)
- [ ] Feature/differentiator count within limits
- [ ] Concept labels fit character limits
- [ ] Feature labels fit within cells
- [ ] Differentiators are truly distinguishing (not shared traits)
- [ ] Visual maintains focus on key differences

---

## Error Handling

| Error | Action |
|-------|--------|
| Concepts exceed 4 | Convert to TABLE format |
| Features exceed 6 | Prioritize top features, move others to notes |
| Differentiators exceed 4 | Use Layout E matrix or split comparison |
| No true differentiators | Recommend TABLE instead (items too similar) |
| Concepts too similar for visual | Add distinguishing features |
| AUTO selection ambiguous | Default to Layout A (most common) |

---

## Example Selection Scenarios

### Scenario 1: Diabetes Type Comparison
```
Input: concept_count=2, feature_count=4, differentiator_count=0
Output: Layout A (Side-by-Side Comparison)
Reasoning: Two concepts with four features fits standard comparison
```

### Scenario 2: IBD Differentiation
```
Input: concept_count=2, has_single_critical_diff=true, feature_count=3
Output: Layout B (Centered Key Differentiator)
Reasoning: "Skip lesions" as single critical differentiator needs central emphasis
```

### Scenario 3: STEMI vs NSTEMI
```
Input: concept_count=2, differentiator_count=3, feature_count=4
Output: Layout C (Multiple Differentiators)
Reasoning: Three key differences (ST elevation, enzyme timing, treatment) need equal emphasis
```

### Scenario 4: Chest Pain Differential
```
Input: concept_count=3, feature_count=3
Output: Layout D (Three-Way Discrimination)
Reasoning: Three similar conditions require triangle arrangement
```

### Scenario 5: Anemia Classification
```
Input: concept_count=4, feature_count=5
Output: Layout E (Feature Matrix)
Reasoning: Four anemia types with five features requires matrix format
```

---

## Key Differentiator Identification Guidelines

### What Makes a Good Key Differentiator
1. **Mutually Exclusive** - Only present in one concept, not both
2. **Clinically Significant** - Impacts diagnosis or treatment
3. **Memorable** - Easy to recall on exam
4. **Observable** - Can be assessed or measured

### Common NCLEX Key Differentiators
- **Lab Values:** Specific markers unique to condition
- **Timing:** Acute vs chronic, onset patterns
- **Location:** Anatomical differences
- **Appearance:** Visual characteristics
- **Response:** Treatment responses

### Red Flags (NOT Key Differentiators)
- Features present in both conditions
- Vague or subjective descriptions
- Non-diagnostic characteristics
- Common symptoms (pain, fever, etc.)

---

## Special Considerations for NCLEX Content

### Disease Differentiation
- Focus on "NCLEX-likely" distinguishing features
- Prioritize actionable differences
- Use Layout B or C for similar disease pairs

### Medication Comparison
- Drug class differentiators
- Side effect profiles
- Use Layout A or E based on drug count

### Assessment Findings
- Normal vs Abnormal
- Expected vs Unexpected
- Use Layout A for two-way, Layout D for three-way

### Emergency Conditions
- Time-sensitive differentiators
- Treatment pathway differences
- Use Layout C for critical distinctions

---

**Agent Version:** 1.0
**Last Updated:** 2026-01-04
