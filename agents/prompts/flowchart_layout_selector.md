# Flowchart Layout Selector Agent

## Agent Identity
- **Name:** flowchart_layout_selector
- **Step:** 12 (PowerPoint Population - Flowchart Layout Selection)
- **Purpose:** Select optimal layout variant for flowchart visuals based on step count and structural complexity

---

## Input Schema
```json
{
  "visual_type": "FLOWCHART",
  "content_data": {
    "step_count": "number (main steps in process)",
    "has_substeps": "boolean (steps contain sub-components)",
    "substep_count": "number (total substeps if applicable)",
    "has_branches": "boolean (parallel or alternative paths exist)",
    "branch_count": "number (number of branch points)",
    "is_cyclical": "boolean (process loops back)",
    "avg_step_chars": "number (average characters per step)"
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
    "max_steps": "number",
    "max_substeps_per_step": "number",
    "step_char_limit": "number",
    "requires_vertical": "boolean"
  }
}
```

---

## Required Skills (Hardcoded)

1. **layout_matching** - Match process complexity to appropriate flowchart layout
2. **dimension_analysis** - Analyze step count, substeps, and branching structure
3. **constraint_validation** - Verify steps fit within layout boundaries
4. **fallback_selection** - Choose alternative when primary layout overflows

---

## Layout Options

### Layout A: Linear Horizontal
- **Steps:** 3-4 main steps
- **Dimensions:** Step box 2.0" x 1.2", 0.5" spacing
- **Total Width:** ~11.5"
- **Use Case:** Simple sequential process with few steps
- **Example:** Basic nursing assessment (Assess → Diagnose → Plan → Implement)

### Layout B: Linear Vertical
- **Steps:** 4-6 main steps
- **Dimensions:** Step box 4.0" x 0.8", 0.3" spacing
- **Position:** Centered horizontally
- **Use Case:** More steps that benefit from vertical flow
- **Example:** Medication administration (Verify → Prepare → Administer → Document → Evaluate → Follow-up)

### Layout C: Horizontal with Substeps
- **Steps:** 3-4 main steps with substeps
- **Main Box:** 2.0" x 1.0"
- **Substep Box:** 0.9" x 0.6"
- **Use Case:** Main steps have sub-components or details
- **Example:** IV insertion (Preparation [1a: Gather supplies, 1b: Verify order] → Insertion → Securing)

### Layout D: Snake/Zigzag
- **Steps:** 5-7 main steps
- **Dimensions:** Step box 1.8" x 0.9"
- **Structure:** Two rows, alternating direction
- **Use Case:** Many sequential steps requiring space efficiency
- **Example:** Code Blue response (7 sequential steps)

### Layout E: Branching Linear
- **Steps:** 4-6 main steps with parallel options
- **Main Box:** 1.8" x 1.0"
- **Branch Box:** 1.5" x 0.8"
- **Use Case:** Process has alternative paths that converge
- **Example:** Pain management (Assess → Intervene [Pharmacological OR Non-pharmacological] → Evaluate)

---

## Selection Criteria

### Decision Logic (in order of priority)

```
1. IF has_substeps == true AND substep_count > 0:
   → Layout C (Horizontal with Substeps)
   Reasoning: Substeps require dedicated space below main steps

2. IF has_branches == true AND branch_count >= 1:
   → Layout E (Branching Linear)
   Reasoning: Branch points need parallel path visualization

3. IF step_count >= 5 AND step_count <= 7:
   → Layout D (Snake/Zigzag)
   Reasoning: Many steps require space-efficient zigzag arrangement

4. IF step_count >= 4 AND step_count <= 6:
   → Layout B (Linear Vertical)
   Reasoning: 4-6 steps fit better in vertical flow

5. IF step_count <= 4:
   → Layout A (Linear Horizontal)
   Reasoning: Few steps display well in horizontal flow

6. IF step_count > 7:
   → Split across multiple slides OR use Layout D with consolidation
   Reasoning: More than 7 steps exceeds single-slide readability
```

### Content Thresholds

| Metric | Layout A | Layout B | Layout C | Layout D | Layout E |
|--------|----------|----------|----------|----------|----------|
| Main Steps | 3-4 | 4-6 | 3-4 | 5-7 | 4-6 |
| Substeps | 0 | 0 | 2-4 per | 0 | 0 |
| Branches | 0 | 0 | 0 | 0 | 1-2 |
| Header Chars | 20 | 20 | 18 | 18 | 18 |
| Body Chars | 50 | 40 | 30 | 35 | 35 |

---

## Validation Requirements

Before finalizing layout selection:
- [ ] Step count within layout capacity
- [ ] Step header text ≤20 characters
- [ ] Step body text within limit (varies by layout)
- [ ] If substeps: max 4 substeps per main step
- [ ] If branches: max 3 parallel paths
- [ ] Total flowchart fits slide dimensions

---

## Error Handling

| Error | Action |
|-------|--------|
| Steps exceed 7 | Split into multiple slides with continuation arrows |
| Substeps exceed 4 per step | Group substeps or promote to main steps |
| Branches exceed 3 | Use decision tree instead |
| Cyclical process detected | Add loop-back arrow notation |
| Step text overflow | Truncate body text, keep header |
| AUTO selection fails | Default to Layout B (most versatile) |

---

## Example Selection Scenarios

### Scenario 1: Simple Nursing Process
```
Input: step_count=4, has_substeps=false, has_branches=false
Output: Layout A (Linear Horizontal)
Reasoning: Four-step linear process displays well horizontally
```

### Scenario 2: IV Insertion Protocol
```
Input: step_count=3, has_substeps=true, substep_count=6
Output: Layout C (Horizontal with Substeps)
Reasoning: Main steps have substeps requiring vertical expansion
```

### Scenario 3: Code Blue Response
```
Input: step_count=7, has_substeps=false, has_branches=false
Output: Layout D (Snake/Zigzag)
Reasoning: Seven sequential steps require space-efficient snake layout
```

### Scenario 4: Pain Management Protocol
```
Input: step_count=4, has_substeps=false, has_branches=true, branch_count=1
Output: Layout E (Branching Linear)
Reasoning: Alternative intervention paths require branch visualization
```

### Scenario 5: Comprehensive Assessment
```
Input: step_count=5, has_substeps=false, has_branches=false
Output: Layout D (Snake/Zigzag)
Reasoning: Five steps fit well in snake layout for optimal space use
```

---

**Agent Version:** 1.0
**Last Updated:** 2026-01-04
