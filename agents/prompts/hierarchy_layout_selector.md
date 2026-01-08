# Hierarchy Layout Selector Agent

## Agent Identity
- **Name:** hierarchy_layout_selector
- **Step:** 12 (PowerPoint Population - Hierarchy Layout Selection)
- **Purpose:** Select optimal layout variant for hierarchy visuals based on structure depth, branching pattern, and comparison needs

---

## Input Schema
```json
{
  "visual_type": "HIERARCHY",
  "content_data": {
    "level_count": "number (tree depth)",
    "total_nodes": "number (all nodes in hierarchy)",
    "branch_factor": "number (typical children per parent)",
    "is_uniform": "boolean (all branches same depth)",
    "is_comparison": "boolean (comparing two hierarchies)",
    "is_narrowing": "boolean (levels get progressively smaller)",
    "root_label": "string (top-level category name)",
    "max_width": "number (widest level node count)"
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
    "max_levels": "number",
    "max_nodes_per_level": "number",
    "node_title_chars": "number",
    "node_desc_chars": "number"
  }
}
```

---

## Required Skills (Hardcoded)

1. **layout_matching** - Match hierarchy structure to appropriate tree layout
2. **dimension_analysis** - Analyze depth, breadth, and branching patterns
3. **constraint_validation** - Verify hierarchy fits within layout boundaries
4. **fallback_selection** - Choose simpler layout when hierarchy is too complex

---

## Layout Options

### Layout A: Top-Down Binary (1-2-4)
- **Structure:** Root → 2 children → 4 grandchildren
- **Levels:** 3
- **Branching:** Binary (2 children per parent)
- **Use Case:** Standard taxonomy with symmetric binary branching
- **Example:** Drug classification (Antibiotics → Bactericidal/Bacteriostatic → Specific types)

### Layout B: Top-Down Triple (1-3-6)
- **Structure:** Root → 3 children → 6 grandchildren
- **Levels:** 3
- **Branching:** Triple at level 1, binary at level 2
- **Use Case:** Three main categories with subcategories
- **Example:** Pain types (Acute/Chronic/Neuropathic → Subtypes)

### Layout C: Organizational Chart
- **Structure:** Root → Mixed branches (2-4 per level)
- **Levels:** 2-3
- **Branching:** Uneven (different children counts)
- **Use Case:** Uneven branching where categories have different depths
- **Example:** Healthcare team (Physician → Specialists | Nurses → RN/LPN/CNA)

### Layout D: Inverted Pyramid
- **Structure:** Wide top → Narrow bottom
- **Levels:** 3-4
- **Branching:** Converging/narrowing
- **Use Case:** Broad concepts narrowing to specific applications
- **Example:** Assessment framework (General → System-specific → Findings)

### Layout E: Side-by-Side Hierarchies
- **Structure:** Two parallel trees
- **Levels:** 2-3 per tree
- **Use Case:** Comparing two classification systems
- **Example:** Normal vs Abnormal findings | Left vs Right heart

---

## Selection Criteria

### Decision Logic (in order of priority)

```
1. IF is_comparison == true:
   → Layout E (Side-by-Side Hierarchies)
   Reasoning: Parallel hierarchies enable direct visual comparison

2. IF is_narrowing == true AND level_count >= 3:
   → Layout D (Inverted Pyramid)
   Reasoning: Converging structure requires pyramid visualization

3. IF is_uniform == false OR branch_factor varies significantly:
   → Layout C (Organizational Chart)
   Reasoning: Uneven branching needs flexible org chart layout

4. IF branch_factor == 3 AND level_count == 3:
   → Layout B (Top-Down Triple)
   Reasoning: Three main categories with subcategories fit triple layout

5. IF branch_factor == 2 AND level_count <= 3:
   → Layout A (Top-Down Binary)
   Reasoning: Binary branching fits standard binary tree layout

6. IF total_nodes > 15:
   → Split hierarchy OR use TABLE
   Reasoning: More than 15 nodes exceeds visual clarity
```

### Content Thresholds

| Metric | Layout A | Layout B | Layout C | Layout D | Layout E |
|--------|----------|----------|----------|----------|----------|
| Levels | 3 | 3 | 2-3 | 3-4 | 2-3 |
| Total Nodes | 7 | 10 | 8-12 | 8-15 | 6-10 |
| Max Width | 4 | 6 | 4 | 6 | 3 per tree |
| Branch Factor | 2 | 3 | Mixed | Varied | 2-3 |
| Title Chars | 20 | 18 | 20 | 18 | 18 |
| Desc Chars | 30 | 25 | 30 | 25 | 25 |

---

## Validation Requirements

Before finalizing layout selection:
- [ ] Level count within limit (max 4)
- [ ] Total nodes within limit (max 15)
- [ ] Node labels fit character limits
- [ ] Widest level fits slide width
- [ ] Branching structure is logical
- [ ] Visual maintains readability

---

## Error Handling

| Error | Action |
|-------|--------|
| Nodes exceed 15 | Split hierarchy or convert to outline format |
| Levels exceed 4 | Flatten by combining levels |
| Width exceeds 6 nodes | Use vertical orientation or split |
| Unbalanced tree with 10+ nodes | Use Layout C with adjusted spacing |
| Missing node labels | Use placeholder category names |
| AUTO selection ambiguous | Default to Layout A (most common) |

---

## Example Selection Scenarios

### Scenario 1: Medication Classification
```
Input: level_count=3, total_nodes=7, branch_factor=2, is_uniform=true
Output: Layout A (Top-Down Binary)
Reasoning: Symmetric binary tree with 7 nodes fits binary layout perfectly
```

### Scenario 2: Pain Classification
```
Input: level_count=3, total_nodes=10, branch_factor=3, is_uniform=true
Output: Layout B (Top-Down Triple)
Reasoning: Three main categories with subtypes match triple layout
```

### Scenario 3: Healthcare Team Structure
```
Input: level_count=3, total_nodes=9, branch_factor=varies, is_uniform=false
Output: Layout C (Organizational Chart)
Reasoning: Uneven branching requires flexible org chart format
```

### Scenario 4: Nursing Process Framework
```
Input: level_count=4, total_nodes=12, is_narrowing=true
Output: Layout D (Inverted Pyramid)
Reasoning: Broad assessment narrowing to specific interventions
```

### Scenario 5: Heart Comparison
```
Input: level_count=2, total_nodes=8, is_comparison=true
Output: Layout E (Side-by-Side Hierarchies)
Reasoning: Comparing left vs right heart structures requires parallel trees
```

---

## Special Considerations for NCLEX Content

### Pharmacology Hierarchies
- Drug classifications (Class → Mechanism → Examples)
- Prefer Layout A or B based on branching

### Body Systems
- Anatomy structures
- Use Layout C for mixed-depth systems

### Assessment Frameworks
- ABCDE, Head-to-toe
- Use Layout D for narrowing focus

### Comparison Content
- Normal vs Abnormal
- Disease A vs Disease B
- Always use Layout E for comparisons

---

**Agent Version:** 1.0
**Last Updated:** 2026-01-04
