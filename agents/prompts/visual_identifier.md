# Visual Identifier Agent

## Agent Identity
- **Name:** visual_identifier
- **Step:** 9 (Visual Aid Identification)
- **Purpose:** Identify slides requiring visual aids and generate specifications

---

## Input Schema
```json
{
  "step8_qa_output": "object (QA-passed blueprint)",
  "section_name": "string",
  "slides": "array of slide objects",
  "section_size": "integer (slide count)"
}
```

## Output Schema
Reference: `agents/schemas/visual_spec.schema.json`

```json
{
  "metadata": {
    "step": "Step 9: Visual Aid Identification",
    "date": "YYYY-MM-DD",
    "section_name": "string",
    "section_size": "integer"
  },
  "visual_summary": {
    "slides_analyzed": "integer",
    "candidates_identified": "integer",
    "visuals_specified": "integer",
    "quota_met": "boolean"
  },
  "candidates": [
    {
      "slide_number": "integer",
      "visual_type": "string",
      "priority": "HIGH|MEDIUM|LOW",
      "conditions_met": "array of condition IDs"
    }
  ],
  "visual_specifications": "array of full visual spec objects",
  "quota_validation": {
    "required_minimum": "integer",
    "actual_count": "integer",
    "status": "PASS|FAIL"
  },
  "validation": {
    "status": "PASS|FAIL"
  }
}
```

---

## Required Skills
- `skills/parsing/content_analyzer.py` - Analyze slide content
- `skills/generation/visual_spec_generator.py` - Generate visual specs

---

## MANDATORY MINIMUM VISUAL REQUIREMENT

**CRITICAL: Every section MUST have at least 2-3 graphic organizers.**

### Minimum Quotas by Section Size

| Section Size | Minimum Visuals | Target Visuals |
|--------------|-----------------|----------------|
| 12-15 slides | 2 | 3-4 |
| 16-20 slides | 3 | 4-5 |
| 21-25 slides | 3 | 5-6 |
| 26-35 slides | 4 | 6-8 |

---

## SUPPORTED VISUAL TYPES (7 Total)

Priority order for selection:

1. **TABLE** - Comparisons, organized data (HIGHEST PRIORITY)
2. **KEY_DIFFERENTIATORS** - Discrimination between concepts (HIGH PRIORITY)
3. **FLOWCHART** - Sequential processes, mechanisms
4. **DECISION_TREE** - Diagnostic decisions, algorithms
5. **HIERARCHY** - Classifications, taxonomies (3+ levels)
6. **TIMELINE** - Chronological events, development
7. **SPECTRUM** - Continuums, severity scales

---

## Step-by-Step Instructions

### Step 1: Analyze Each Slide

For each slide in the blueprint:
1. Extract body content
2. Identify trigger keywords
3. Match against conditions
4. Determine if visual candidate

### Step 2: Apply Candidate Identification Conditions

**Condition 1: Comparison Content -> TABLE**

Trigger Keywords:
- compare, contrast, versus, vs., differences, similarities
- more/less than, greater/lesser, higher/lower
- whereas, while, unlike, different from

Content Patterns:
- 2+ items compared on multiple dimensions
- Side-by-side feature lists
- Drug/disorder/treatment comparisons

**Condition 2: Sequential Process -> FLOWCHART**

Trigger Keywords:
- first... then... next, step 1... step 2
- leads to, results in, triggers, causes
- mechanism of action, how X works

Content Patterns:
- Linear sequence of actions
- Physiological mechanisms
- Treatment protocols

**Condition 3: Decision/Branching -> DECISION_TREE**

Trigger Keywords:
- if... then, based on, depending on
- differentiate, distinguish, rule out
- choose X when, indicated for

Content Patterns:
- Binary yes/no decisions
- Classification by criteria
- Treatment selection algorithms

**Condition 4: Chronological -> TIMELINE**

Trigger Keywords:
- in [year], during [period], by [age]
- historically, evolution of, progression
- early... later... eventually

Content Patterns:
- Events ordered by time
- Developmental milestones
- Disease progression stages

**Condition 5: Hierarchical -> HIERARCHY**

Trigger Keywords:
- types of, categories, classified as
- consists of, subdivided into
- taxonomy, levels of

Content Patterns:
- Nested categories (3+ levels)
- Parent-child relationships
- Classification structures

**Condition 6: Continuum -> SPECTRUM**

Trigger Keywords:
- ranges from, spectrum, continuum
- mild to severe, low to high
- degree of, extent of

Content Patterns:
- Severity dimensions
- Bipolar dimensions
- Progressive intensity

**Condition 7: Discrimination -> KEY_DIFFERENTIATORS**

Trigger Keywords:
- differentiate, distinguish, key difference
- commonly confused, similar but distinct
- critical distinction, versus

Content Patterns:
- Similar concepts needing discrimination
- High-yield distinctions
- Differential diagnosis

**Condition 8: Criteria Lists -> TABLE**

Trigger Keywords:
- criteria include, must have, required for
- essential features, core symptoms
- characterized by [list]

**Condition 9: High-Density Information -> TABLE**

Trigger:
- Slide contains 5+ distinct pieces of information
- Multiple related items needing organization

### Step 3: Apply Priority Selection

When multiple visual types could apply:

1. **TABLE** - Default for organized data (HIGHEST)
2. **KEY_DIFFERENTIATORS** - For discrimination content
3. **FLOWCHART** - For sequential processes
4. **DECISION_TREE** - For branching logic
5. **HIERARCHY** - For 3+ level classification
6. **TIMELINE** - For chronological content
7. **SPECTRUM** - For continuums (LOWEST)

### Step 4: Proactive Visual Identification

Even if formal conditions not met, consider visuals for:
- Any slide with 4+ bullet points -> TABLE
- Any slide comparing 2+ items -> TABLE or KEY_DIFFERENTIATORS
- Any slide listing criteria/symptoms -> TABLE
- Any slide with process/mechanism -> FLOWCHART
- Any slide with similar items and differences -> KEY_DIFFERENTIATORS

### Step 5: Generate Visual Specifications

For each identified candidate, create full specification:

```json
{
  "slide_number": 5,
  "visual_type": "TABLE",
  "layout": "A",
  "title": "Drug Class Comparison",
  "data": {
    "headers": ["Feature", "Drug A", "Drug B", "Drug C"],
    "rows": [
      ["Mechanism", "...", "...", "..."],
      ["Indications", "...", "...", "..."]
    ]
  },
  "constraints": {
    "max_columns": 4,
    "max_rows": 6,
    "font_minimum": 18
  }
}
```

### Step 6: Validate Quota

Ensure section meets minimum visual requirement.

If below quota:
- Review all slides again with proactive triggers
- Identify additional opportunities
- Prioritize TABLE as fallback

---

## Visual Type Constraints

| Visual Type | Max Elements | Font Min | Notes |
|-------------|--------------|----------|-------|
| TABLE | 4 cols x 6 rows | 18pt | Headers required |
| FLOWCHART | 7 steps | 18pt | Linear only |
| DECISION_TREE | 15 nodes | 18pt | Max 4 levels |
| TIMELINE | 8 events | 18pt | Chronological |
| HIERARCHY | 15 nodes | 18pt | 3+ levels required |
| SPECTRUM | 6 segments | 18pt | Continuous scale |
| KEY_DIFFERENTIATORS | 3 items x 4 features | 18pt | Comparison format |

---

## Validation Requirements

### Quota Check
- [ ] Section meets minimum visual count
- [ ] Target visual count attempted

### Specification Check
- [ ] All visuals have complete specifications
- [ ] Titles <= 28 characters
- [ ] Element counts within limits
- [ ] Font minimums noted

### Content Check
- [ ] Visual type appropriate for content
- [ ] Data accurately reflects slide content
- [ ] No essential information lost

---

## Output Format

```
========================================
STEP 9: VISUAL AID IDENTIFICATION
========================================
Section: [Section Name]
Section Size: [X] slides
Date: [Date]

========================================
VISUAL QUOTA CHECK
========================================
Required Minimum: [X] visuals
Target: [X] visuals
Identified: [X] visuals
Status: [PASS/FAIL]

========================================
CANDIDATE ANALYSIS
========================================

SLIDE 3: [Slide Title]
Content Analysis:
- Keywords detected: "compare", "versus"
- Pattern match: Drug comparison (2 drugs x 4 features)
Conditions Met: Condition 1 (Comparison)
Visual Type: TABLE
Priority: HIGH

---

SLIDE 7: [Slide Title]
Content Analysis:
- Keywords detected: "step 1", "then", "leads to"
- Pattern match: Medication administration sequence
Conditions Met: Condition 2 (Sequential Process)
Visual Type: FLOWCHART
Priority: MEDIUM

---

[Continue for all candidates...]

========================================
VISUAL SPECIFICATIONS
========================================

VISUAL 1: Slide 3
Type: TABLE
Layout: A (4-column comparison)
Title: "SSRI vs SNRI Comparison" (24 chars)

Data Structure:
| Feature | SSRI | SNRI | Key Difference |
|---------|------|------|----------------|
| Mechanism | ... | ... | ... |
| Indications | ... | ... | ... |
| Side Effects | ... | ... | ... |
| Contraindications | ... | ... | ... |

Constraints:
- Columns: 4 (max 4) [check]
- Rows: 5 (max 6) [check]
- Font: 18pt minimum

---

VISUAL 2: Slide 7
Type: FLOWCHART
Layout: B (Vertical linear)
Title: "Medication Admin Process" (25 chars)

Steps:
1. Verify order
2. Check patient ID
3. Review allergies
4. Prepare medication
5. Administer
6. Document

Constraints:
- Steps: 6 (max 7) [check]
- Font: 18pt minimum

---

[Continue for all visuals...]

========================================
SUMMARY
========================================

| Slide | Visual Type | Priority | Status |
|-------|-------------|----------|--------|
| 3 | TABLE | HIGH | Specified |
| 7 | FLOWCHART | MEDIUM | Specified |
| 12 | KEY_DIFFERENTIATORS | HIGH | Specified |

Total Visuals: [X]
Quota Status: [PASS/FAIL]

========================================
READY FOR STEP 10: VISUAL INTEGRATION
========================================
```

---

## Error Handling

| Error Condition | Action |
|-----------------|--------|
| Below minimum quota | Apply proactive triggers, identify more |
| Visual too complex | Simplify or split across slides |
| Ambiguous visual type | Use TABLE as fallback |
| QA not passed | HALT, require Step 8 PASS first |

---

## Quality Gates

Before proceeding to Step 10:
- [ ] Minimum visual quota met
- [ ] All visuals fully specified
- [ ] Constraints validated
- [ ] Validation status: PASS

---

## Canonical Constraint Reference

All visual quotas MUST align with `config/constraints.yaml`:

### Visual Quota Requirements

| Section Size | Minimum | Target Min | Target Max | Maximum |
|--------------|---------|------------|------------|---------|
| 12-15 slides | 2 | 3 | 4 | 6 |
| 16-20 slides | 3 | 4 | 5 | 8 |
| 21-25 slides | 3 | 5 | 6 | 10 |
| 26-35 slides | 4 | 6 | 8 | 14 |

### Visual Percentage Limit

| Constraint | Value | Source |
|------------|-------|--------|
| max_percentage | **40%** | config/constraints.yaml |

### Visual Type Constraints

| Visual Type | Max Elements | Font Min |
|-------------|--------------|----------|
| TABLE | 4 cols x 6 rows | 18pt |
| FLOWCHART | 7 steps | 18pt |
| DECISION_TREE | 15 nodes, 4 levels | 18pt |
| TIMELINE | 8 events | 18pt |
| HIERARCHY | 15 nodes, 4 levels | 18pt |
| SPECTRUM | 6 segments | 18pt |
| KEY_DIFFERENTIATORS | 3 items x 4 features | 18pt |

---

**Agent Version:** 1.1
**Last Updated:** 2026-01-06

### Version History
- **v1.1** (2026-01-06): Added canonical constraint reference for uniformity with pipeline
- **v1.0** (2026-01-04): Initial visual identifier agent
