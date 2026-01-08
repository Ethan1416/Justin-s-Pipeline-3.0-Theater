# Outline Generator Agent

## Agent Identity
- **Name:** outline_generator
- **Step:** 4 (Outline Generation)
- **Purpose:** Generate final lecture structure with sessions, sections, and slide counts

---

## Input Schema
```json
{
  "step3_output": "object (sorting output with domain assignments)",
  "step2_output": "object (arc planning iterations, relationship mapping)",
  "domain": "string (NCLEX domain)",
  "sorted_anchors": "array of anchors with domain assignments and flags"
}
```

## Output Schema
```json
{
  "metadata": {
    "step": "Step 4: Outline Generation",
    "date": "YYYY-MM-DD",
    "domain": "string",
    "total_anchors": "integer",
    "total_sections": "integer",
    "total_slides": "integer"
  },
  "session1": {
    "estimated_slides": "integer (72-90)",
    "sections": "array of section objects with subsections",
    "break_placement": "object"
  },
  "session2": {
    "estimated_slides": "integer (72-90)",
    "sections": "array of section objects with subsections",
    "break_placement": "object",
    "culmination_section": "object (if applicable)"
  },
  "grand_summary": {
    "statistics": "object with totals by session",
    "section_flow": "string diagram",
    "prerequisite_chain": "string diagram",
    "constraint_validation": "object"
  },
  "flagged_content": {
    "frontload_by_section": "object",
    "cross_references": "array"
  },
  "validation": {
    "status": "PASS|FAIL",
    "checks": "object with all constraint checks"
  }
}
```

---

## Required Skills
- `skills/generation/outline_builder.py` - Generate outline structure
- `skills/validation/constraint_validator.py` - Validate slide/section limits

---

## Step-by-Step Instructions

### Step 1: Review Arc Iterations from Step 2
Examine arc planning iterations and select optimal sequence based on:
- Strongest prerequisite integrity
- Best session balance
- Most logical learning flow

### Step 2: Apply Distribution Logic

**Prerequisite Rule:** Foundational sections precede dependent sections
**Balance Rule:** 72-90 slides per session
**Frontloading Rule:** Distribute scaffolding appropriately
**Culmination Rule:** Integration section at end of Session 2

### Step 3: Calculate Slide Counts

**Anchor-to-Slide Formula:**
```
Content Slides = Anchor Count x Complexity Multiplier
Section Total = Content Slides + 3 (fixed slides: intro, vignette, answer)
```

**Complexity Multipliers:**
| Content Type | Multiplier |
|--------------|------------|
| Simple (definitions, single concepts) | x 1.0 |
| Moderate (mechanisms, relationships) | x 1.15 (default) |
| Complex (differentials, integrative) | x 1.3 |

### Step 4: Create Subsections

**Subsection Guidelines:**
- Group by conceptual similarity
- 3-8 anchors per subsection typical
- Name descriptively
- Sequence: Foundation -> Core -> Application -> Integration

**Domain-Specific Patterns:**
| Domain | Typical Subsection Flow |
|--------|------------------------|
| fundamentals | Concept -> Process -> Application -> Safety |
| pharmacology | Drug Class -> Mechanism -> Administration -> Side Effects |
| medical_surgical | Pathophysiology -> Assessment -> Intervention -> Evaluation |
| ob_maternity | Normal Process -> Complications -> Nursing Care |
| pediatric | Development -> Condition -> Family-Centered Care |
| mental_health | Disorder -> Symptoms -> Therapeutic Approach -> Safety |

### Step 5: Validate Constraints

**Hard Constraints:**
- 2 sessions, 150 minutes each
- 72-90 slides per session
- 10-35 slides per section
- 3 fixed slides per section

### Step 6: Generate Output

---

## Validation Requirements

### Slide Constraints
- [ ] Session 1: 72-90 slides
- [ ] Session 2: 72-90 slides
- [ ] Total: 144-180 slides
- [ ] Each section: 10-35 slides (10 min if 5+ sections, 12 min if ≤4 sections)

### Content Constraints
- [ ] Every anchor assigned to one section
- [ ] Every anchor in one subsection
- [ ] No orphaned anchors
- [ ] No duplicate assignments

### Structural Constraints
- [ ] Prerequisites respected
- [ ] Culmination at end (if applicable)
- [ ] Break placement at ~75 min
- [ ] Frontload anchors positioned early

---

## Output Format

```
========================================
STEP 4: OUTLINE - FINAL
========================================
Domain: [Domain Name]
Total Anchors: [X]
Total Sections: [X]
Total Estimated Slides: [X]
Date: [Date]

========================================
SESSION 1 (150 minutes)
========================================
Estimated Slides: [XX] (target: 72-90)
Sections: [X]
Anchors: [X]

---

### SECTION 1: [SECTION NAME]
**Anchor Count:** [XX]
**Estimated Slides:** [XX]
**Prerequisites:** [None / List]

#### Subsections:

**1.1 [Subsection Name]** ([X] anchors)
Anchors: #[list]
Focus: [description]

**1.2 [Subsection Name]** ([X] anchors)
Anchors: #[list]
Focus: [description]

**Frontload Anchors:** #[list]
**Cross-References:** [list]

---

[Continue for all sections...]

### --- SESSION 1 BREAK (10 minutes) ---
Slide Count: 1
Placement: After Section [X]

---

### SESSION 1 SUMMARY
| Section | Anchors | Slides | Subsections |
|---------|---------|--------|-------------|
| [Name]  | [X]     | [X]    | [X]         |
| Break   | -       | 1      | -           |
| TOTAL   | [X]     | [X]    |             |

Constraint Check:
- Slides: [X] (target: 72-90) [PASS/FAIL]
- All sections 12-35 slides: [PASS/FAIL]
- Prerequisites respected: [PASS/FAIL]

========================================
SESSION 2 (150 minutes)
========================================
[Same format as Session 1]

========================================
OUTLINE GRAND SUMMARY
========================================

| Metric      | Session 1 | Session 2 | Total |
|-------------|-----------|-----------|-------|
| Sections    | [X]       | [X]       | [X]   |
| Anchors     | [X]       | [X]       | [X]   |
| Slides      | [X]       | [X]       | [X]   |

CONSTRAINT VALIDATION:
| Constraint | Requirement | Actual | Status |
|------------|-------------|--------|--------|
| Session 1 slides | 72-90 | [X] | [PASS/FAIL] |
| Session 2 slides | 72-90 | [X] | [PASS/FAIL] |
| Total slides | 144-180 | [X] | [PASS/FAIL] |
| Min slides/section | 10-12 | [X] | [PASS/FAIL] |
| Max slides/section | 35 | [X] | [PASS/FAIL] |

========================================
READY FOR STEP 5: PRESENTATION STANDARDS
========================================
```

---

## Error Handling

| Error Condition | Action |
|-----------------|--------|
| Session exceeds 90 slides | Move section to other session OR split section |
| Session below 72 slides | Move section from other session OR expand coverage |
| Section exceeds 35 slides | Split into two sections |
| Section below 10-12 slides | Merge with related section (10 min if 5+ sections, 12 min if ≤4 sections) |
| Missing Step 2/3 input | HALT, request required outputs |

---

## Quality Gates

Before proceeding to Step 5:
- [ ] All constraint checks PASS
- [ ] All anchors assigned to sections and subsections
- [ ] Session distribution balanced
- [ ] Prerequisites properly sequenced
- [ ] Validation status: PASS

---

**Agent Version:** 1.0
**Last Updated:** 2026-01-04
