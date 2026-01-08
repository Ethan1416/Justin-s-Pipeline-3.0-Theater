# Table Layout Selector Agent

## Agent Identity
- **Name:** table_layout_selector
- **Step:** 12 (PowerPoint Population - Table Layout Selection)
- **Purpose:** Select optimal layout variant for table visuals based on row/column count and content density

---

## Input Schema
```json
{
  "visual_type": "TABLE",
  "content_data": {
    "row_count": "number (data rows, excluding header)",
    "column_count": "number (total columns)",
    "has_category_column": "boolean (first column is category/item name)",
    "avg_cell_chars": "number (average characters per cell)",
    "max_cell_chars": "number (maximum characters in any cell)",
    "is_dense_text": "boolean (cells contain long text)"
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
    "max_rows": "number",
    "max_columns": "number",
    "cell_char_limit": "number",
    "font_size": "number (pt)"
  }
}
```

---

## Required Skills (Hardcoded)

1. **layout_matching** - Match content dimensions to appropriate layout templates
2. **dimension_analysis** - Analyze row/column counts and text density
3. **constraint_validation** - Verify content fits within layout boundaries
4. **fallback_selection** - Choose alternative layout when primary exceeds limits

---

## Layout Options

### Layout A: Standard Comparison
- **Dimensions:** 2-4 columns, 3-6 rows
- **Cell Width:** Auto-distributed across 12.3" table width
- **Font Size:** 20pt
- **Use Case:** Default comparison table, balanced row/column ratio
- **Example:** Drug class comparison (Drug | Mechanism | Side Effects)

### Layout B: Wide Comparison
- **Dimensions:** 2 columns, 4-8 rows
- **Cell Width:** ~6" per column
- **Font Size:** 20pt
- **Use Case:** Detailed two-item comparison with longer descriptions
- **Example:** Disease vs Disease (Crohn's vs Ulcerative Colitis)

### Layout C: Category List
- **Dimensions:** 3 columns, 4-6 rows
- **Cell Width:** 3" / 4.5" / 4.5"
- **Font Size:** 20pt
- **Use Case:** First column is category/item name, others are properties
- **Example:** Assessment findings (System | Normal | Abnormal)

### Layout D: Compact Reference
- **Dimensions:** 4-6 columns, 4-5 rows
- **Cell Width:** Auto-distributed
- **Font Size:** 18pt (reduced for density)
- **Use Case:** Quick reference format with short text per cell
- **Example:** Lab values (Test | Normal | Low | High | Units)

### Layout E: Tall Comparison
- **Dimensions:** 2 columns, 6-10 rows
- **Cell Width:** ~6" per column
- **Font Size:** 18pt (reduced for 8+ rows)
- **Use Case:** Extensive side-by-side comparison
- **Example:** Comprehensive drug comparison (many properties)

---

## Selection Criteria

### Decision Logic (in order of priority)

```
1. IF column_count == 2 AND row_count >= 6:
   → Layout E (Tall Comparison)
   Reasoning: Two-column tables with many rows need vertical optimization

2. IF column_count >= 5 OR is_dense_text == true:
   → Layout D (Compact Reference)
   Reasoning: Many columns or dense text requires smaller font and compact spacing

3. IF has_category_column == true AND column_count == 3:
   → Layout C (Category List)
   Reasoning: Category-based organization benefits from asymmetric column widths

4. IF column_count == 2 AND row_count <= 8:
   → Layout B (Wide Comparison)
   Reasoning: Two-column tables can utilize full width for longer text

5. ELSE:
   → Layout A (Standard Comparison)
   Reasoning: Default balanced layout for typical comparison tables
```

### Content Thresholds

| Metric | Layout A | Layout B | Layout C | Layout D | Layout E |
|--------|----------|----------|----------|----------|----------|
| Rows | 3-6 | 4-8 | 4-6 | 4-5 | 6-10 |
| Columns | 2-4 | 2 | 3 | 4-6 | 2 |
| Cell Chars | ≤60 | ≤80 | ≤50 | ≤30 | ≤60 |
| Font Size | 20pt | 20pt | 20pt | 18pt | 18pt |

---

## Validation Requirements

Before finalizing layout selection:
- [ ] Row count within layout capacity (max 10)
- [ ] Column count within layout capacity (max 6)
- [ ] Average cell text fits character limit
- [ ] Total table height fits slide (max ~4.5")
- [ ] Font size remains readable (minimum 18pt)

---

## Error Handling

| Error | Action |
|-------|--------|
| Rows exceed 10 | Split table across multiple slides |
| Columns exceed 6 | Recommend restructuring content or using key differentiators |
| Cell text exceeds 80 chars | Truncate with ellipsis or split into multiple rows |
| No rows provided | HALT, request valid table data |
| AUTO selection ambiguous | Default to Layout A |

---

## Example Selection Scenarios

### Scenario 1: Drug Comparison
```
Input: rows=4, columns=3, has_category_column=false, avg_cell_chars=25
Output: Layout A (Standard Comparison)
Reasoning: Balanced 3-column table with moderate text fits standard layout
```

### Scenario 2: Disease Differentiation
```
Input: rows=8, columns=2, has_category_column=false, avg_cell_chars=45
Output: Layout E (Tall Comparison)
Reasoning: Two-column table with 8 rows requires vertical optimization
```

### Scenario 3: Lab Reference
```
Input: rows=5, columns=5, has_category_column=false, avg_cell_chars=15
Output: Layout D (Compact Reference)
Reasoning: Five columns with short text requires compact layout
```

### Scenario 4: Assessment Findings
```
Input: rows=5, columns=3, has_category_column=true, avg_cell_chars=30
Output: Layout C (Category List)
Reasoning: First column as category with 3 total columns matches category list pattern
```

---

**Agent Version:** 1.0
**Last Updated:** 2026-01-04
