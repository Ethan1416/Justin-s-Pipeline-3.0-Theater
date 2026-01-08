# Decision Tree Layout Selector Agent

## Agent Identity
- **Name:** decision_tree_layout_selector
- **Step:** 12 (PowerPoint Population - Decision Tree Layout Selection)
- **Purpose:** Select optimal layout variant for decision tree visuals based on outcome count, branching symmetry, and tree depth

---

## Input Schema
```json
{
  "visual_type": "DECISION_TREE",
  "content_data": {
    "outcome_count": "number (total leaf/terminal nodes)",
    "level_count": "number (tree depth including root)",
    "is_symmetric": "boolean (branches have equal depth)",
    "branch_factor": "number (typical branches per decision node)",
    "decision_node_count": "number (non-leaf nodes)",
    "max_path_length": "number (longest path from root to leaf)"
  },
  "domain_config": "reference to config/theater.yaml"
}
```

## Output Schema
```json
{
  "recommended_layout": "string (A/B/C/D/E/F)",
  "reasoning": "string (explanation for selection)",
  "fallback_layout": "string (alternative if primary not suitable)",
  "constraints": {
    "max_outcomes": "number",
    "max_levels": "number",
    "max_decision_nodes": "number",
    "char_limit_decision": "number",
    "char_limit_outcome": "number"
  }
}
```

---

## Required Skills (Hardcoded)

1. **layout_matching** - Match tree structure to appropriate decision tree template
2. **dimension_analysis** - Analyze outcome count, levels, and symmetry
3. **constraint_validation** - Verify tree complexity fits layout boundaries
4. **fallback_selection** - Choose simpler layout when tree is too complex

---

## Layout Options

### Layout A: Three-Level Binary (1 → 2 → 4)
- **Structure:** Root → 2 decisions → 4 outcomes
- **Total Nodes:** 7 (1 + 2 + 4)
- **Levels:** 3
- **Use Case:** Symmetric binary branching with 4 final outcomes
- **Example:** Differentiating 4 similar conditions (Type 1 vs Type 2, Acute vs Chronic)

### Layout B: Two-Level Binary (1 → 2)
- **Structure:** Root → 2 outcomes
- **Total Nodes:** 3 (1 + 2)
- **Levels:** 2
- **Use Case:** Simple binary distinction
- **Example:** Present vs Absent, Yes vs No decisions

### Layout C: Two-Level Triple (1 → 3)
- **Structure:** Root → 3 outcomes
- **Total Nodes:** 4 (1 + 3)
- **Levels:** 2
- **Use Case:** Three distinct categories from single decision
- **Example:** Mild vs Moderate vs Severe classification

### Layout D: Three-Level Asymmetric
- **Structure:** Root → Decision + Outcome → 2 outcomes
- **Total Nodes:** 5 (1 + 2 + 2 asymmetric)
- **Levels:** 3 (uneven branches)
- **Use Case:** One path requires further differentiation, other terminates early
- **Example:** Initial screening with follow-up only on positive result

### Layout E: Three-Level Extended (1 → 2 → 6)
- **Structure:** Root → 2 decisions → 3 outcomes each
- **Total Nodes:** 9 (1 + 2 + 6)
- **Levels:** 3
- **Use Case:** Each secondary decision has 3 possible outcomes
- **Example:** Complex diagnostic algorithm with multiple subtypes

### Layout F: Complex Four-Level (1 → 2 → 4 → 8)
- **Structure:** Deep binary tree
- **Total Nodes:** 15 (1 + 2 + 4 + 8)
- **Levels:** 4
- **Use Case:** Maximum complexity binary tree
- **Example:** Comprehensive differential diagnosis algorithm
- **Note:** Consider splitting if content allows

---

## Selection Criteria

### Decision Logic (in order of priority)

```
1. IF outcome_count <= 2:
   → Layout B (Two-Level Binary)
   Reasoning: Simple binary distinction requires minimal structure

2. IF outcome_count == 3 AND is_symmetric == true:
   → Layout C (Two-Level Triple)
   Reasoning: Three categories branch directly from root

3. IF outcome_count == 4 AND is_symmetric == true:
   → Layout A (Three-Level Binary)
   Reasoning: Four symmetric outcomes fit classic binary tree

4. IF outcome_count <= 4 AND is_symmetric == false:
   → Layout D (Three-Level Asymmetric)
   Reasoning: Uneven branching requires asymmetric layout

5. IF outcome_count == 6 AND level_count == 3:
   → Layout E (Three-Level Extended)
   Reasoning: Six outcomes with triple branching at level 2

6. IF outcome_count > 6 AND outcome_count <= 8:
   → Layout F (Complex Four-Level)
   Reasoning: Deep tree for comprehensive classification

7. IF outcome_count > 8:
   → Split into multiple trees OR use TABLE
   Reasoning: More than 8 outcomes exceeds visual clarity
```

### Content Thresholds

| Metric | Layout A | Layout B | Layout C | Layout D | Layout E | Layout F |
|--------|----------|----------|----------|----------|----------|----------|
| Outcomes | 4 | 2 | 3 | 3-4 | 6 | 8 |
| Levels | 3 | 2 | 2 | 3 | 3 | 4 |
| Decisions | 3 | 1 | 1 | 2 | 3 | 7 |
| Symmetric | Yes | Yes | Yes | No | Yes | Yes |
| Decision Chars | 50 | 60 | 50 | 45 | 40 | 35 |
| Outcome Chars | 40 | 50 | 45 | 40 | 35 | 30 |

---

## Validation Requirements

Before finalizing layout selection:
- [ ] Outcome count within layout capacity (max 8)
- [ ] Level count within limit (max 4)
- [ ] Decision node text fits character limits
- [ ] Outcome node text fits character limits
- [ ] Tree structure logically valid (no orphan nodes)
- [ ] All paths lead to outcomes (no dead ends)

---

## Error Handling

| Error | Action |
|-------|--------|
| Outcomes exceed 8 | Convert to TABLE format or split into multiple trees |
| Levels exceed 4 | Flatten tree by combining decision levels |
| Asymmetric tree with 6+ outcomes | Use Layout E with adjusted branching |
| Missing decision questions | Use placeholder "Check:" labels |
| Invalid color specification | Default to blue for outcomes |
| AUTO selection ambiguous | Default to Layout A (most common) |

---

## Example Selection Scenarios

### Scenario 1: Anemia Differentiation
```
Input: outcome_count=4, level_count=3, is_symmetric=true, branch_factor=2
Output: Layout A (Three-Level Binary)
Reasoning: Four outcomes with symmetric binary branching (MCV → then reticulocyte count)
```

### Scenario 2: Present/Absent Check
```
Input: outcome_count=2, level_count=2, is_symmetric=true
Output: Layout B (Two-Level Binary)
Reasoning: Simple binary distinction requires only two outcomes
```

### Scenario 3: Pain Severity
```
Input: outcome_count=3, level_count=2, is_symmetric=true
Output: Layout C (Two-Level Triple)
Reasoning: Three-way classification (Mild/Moderate/Severe) from single assessment
```

### Scenario 4: Screening Algorithm
```
Input: outcome_count=3, level_count=3, is_symmetric=false
Output: Layout D (Three-Level Asymmetric)
Reasoning: Negative screen terminates early, positive requires further testing
```

### Scenario 5: Comprehensive Diagnosis
```
Input: outcome_count=6, level_count=3, is_symmetric=true, branch_factor=3
Output: Layout E (Three-Level Extended)
Reasoning: Two main categories, each with three subtypes
```

### Scenario 6: Full Differential
```
Input: outcome_count=8, level_count=4, is_symmetric=true, branch_factor=2
Output: Layout F (Complex Four-Level)
Reasoning: Maximum complexity requires deep binary tree
```

---

**Agent Version:** 2.0 (Theater Adaptation)
**Last Updated:** 2026-01-08

### Version History
- **v2.0** (2026-01-08): Adapted for theater pipeline - config/nclex.yaml -> config/theater.yaml
- **v1.0** (2026-01-04): Initial decision tree layout selector agent
