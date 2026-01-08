# Lecture Mapper Agent

## Agent Identity
- **Name:** lecture_mapper
- **Step:** 2 (Lecture Mapping)
- **Purpose:** Analyze anchor content through 5 sequential phases to prepare for sorting

---

## Input Schema
```json
{
  "step1_output": "object (anchor upload output)",
  "anchors": "array of anchor point objects with text and numbers",
  "domain": "string (detected domain from Step 1)"
}
```

## Output Schema
```json
{
  "metadata": {
    "step": "Step 2: Lecture Mapping",
    "date": "YYYY-MM-DD",
    "domain": "string",
    "total_anchors": "integer"
  },
  "phase1_content_survey": {
    "categories": "array of category inventories",
    "key_observations": "array of pattern notes"
  },
  "phase2_cluster_discovery": {
    "clusters": "array of cluster objects with anchors",
    "multi_fit_anchors": "array of ambiguous anchor notes"
  },
  "phase3_relationship_mapping": {
    "prerequisite_analysis": "string narrative",
    "dependency_summary": "object with foundational/dependent/culminating",
    "frontloading_requirements": "array"
  },
  "phase4_section_formation": {
    "section_count": "integer",
    "sections": "array of section objects",
    "special_sections": "object (misc, culmination if applicable)"
  },
  "phase5_arc_planning": {
    "iterations": "array of 3-5 sequence iterations",
    "comparison_summary": "object comparing iterations",
    "implications_for_sorting": "array of insights"
  },
  "handoff": {
    "proposed_sections": "array",
    "arc_iterations_count": "integer",
    "multi_fit_anchors": "array"
  }
}
```

---

## Required Skills
- `skills/parsing/content_analyzer.py` - Analyze anchor content
- `skills/generation/cluster_generator.py` - Form clusters from anchors

---

## Step-by-Step Instructions

### PHASE 1: CONTENT SURVEY
**Purpose:** Familiarize with the anchor landscape

**Task:** Read ALL anchors and create detailed inventory.

**Identify and catalog using domain-appropriate categories:**
- Anatomical structures, body systems, disorders
- Drugs, medications, pharmacological agents
- Nursing processes, procedures, interventions
- Populations (adult, pediatric, maternal, psych)

**Output Format:**
```
===== PHASE 1: CONTENT SURVEY =====
Domain: [extracted from document]
Total Anchors: [count]

CATEGORY 1: [Category Name] ([X] unique items, [Y] total mentions)
[Subcategory A]:
- [Item]: Anchors #[list] ([X] mentions)
- [Item]: Anchors #[list] ([X] mentions)

KEY OBSERVATIONS:
- [Notable patterns, heavily represented topics, gaps]
```

---

### PHASE 2: CLUSTER DISCOVERY
**Purpose:** Identify natural groupings of related anchors

**Clustering Principles:**
- Group by conceptual similarity
- Cluster = coherent teaching unit
- Minimum 5 anchors per cluster (may merge)
- Each anchor in exactly ONE cluster

**Output Format:**
```
===== PHASE 2: CLUSTER DISCOVERY =====
PROVISIONAL CLUSTERS IDENTIFIED: [X]

CLUSTER: [Cluster Name]
Anchor Count: [X]
Anchors: #[list all anchor numbers]
Core Theme: [1-2 sentence description]
Key Concepts: [main elements]

MULTI-FIT ANCHORS:
- Anchor #[X]: Currently in [Cluster A], could also fit [Cluster B]
  - Reason for current placement: [rationale]
```

---

### PHASE 3: RELATIONSHIP MAPPING
**Purpose:** Understand prerequisite dependencies between clusters

**Key Questions:**
- Which clusters provide foundational knowledge?
- What must be taught BEFORE other content?
- Which clusters are independent vs. dependent?
- How much frontloading is needed?

**Output Format:**
```
===== PHASE 3: RELATIONSHIP MAPPING =====

PREREQUISITE ANALYSIS (Narrative)
[Cluster A] serves as foundational because [explanation]...

DEPENDENCY SUMMARY:
Foundational Clusters: [list with rationale]
Dependent Clusters: [list with required prerequisites]
Culminating Clusters: [list requiring most prior content]

FRONTLOADING REQUIREMENTS:
| Cluster | Frontloading Needed | Must Come After |
```

---

### PHASE 4: SECTION FORMATION
**Purpose:** Convert clusters into proposed lecture sections

**Section Formation Rules:**
- Total Anchors / 15-20 = Target section count
- Valid range: 4-12 sections total
- Section size: 10-35 slides (based on anchor count)

**Output Format:**
```
===== PHASE 4: SECTION FORMATION =====

SECTION COUNT CALCULATION:
- Total anchors: [X]
- Formula: [X] / 17 = [Y] sections (target)

PROPOSED SECTIONS:
SECTION: [Section Name]
Formed From: [Cluster(s)]
Anchor Count: [X]
Anchors: #[list]
Foundational Status: [Foundational / Dependent / Culminating]
Prerequisites: [None / List required prior sections]
```

---

### PHASE 5: ARC PLANNING
**Purpose:** Generate multiple section sequencing iterations

**Generate 3-5 iterations considering:**
- 2 sessions, 150 minutes each
- 72-90 slides per session
- Prerequisite relationships
- Culmination content at end of Session 2

**Evaluation Criteria:**
1. Prerequisite Integrity
2. Session Balance
3. Learning Flow
4. Culmination Setup
5. Logical Coherence
6. Frontloading Efficiency

**Output Format:**
```
===== PHASE 5: ARC PLANNING =====

ITERATION 1: [Label]
Session 1:
1. [Section Name] ([X] anchors, [Y] slides) - [rationale]
...
Session 1 Totals: [X] anchors, [Y] estimated slides

Session 2:
1. [Section Name] ([X] anchors, [Y] slides) - [rationale]
...
Session 2 Totals: [X] anchors, [Y] estimated slides

Evaluation:
- Prerequisite Integrity: [Strong/Moderate/Weak]
- Session Balance: [Balanced/Uneven]
...

ITERATION COMPARISON SUMMARY:
[Table comparing all iterations across criteria]

IMPLICATIONS FOR SORTING (Step 3):
- [Insights for sorting decisions]
```

---

## Validation Requirements

### Phase Completion Checks
- [ ] Phase 1: All anchors inventoried
- [ ] Phase 2: All anchors assigned to exactly one cluster
- [ ] Phase 3: Dependency relationships documented
- [ ] Phase 4: Sections formed within size constraints
- [ ] Phase 5: 3-5 iterations generated with evaluations

### Output Validation
- [ ] Total anchors in sections = input anchor count
- [ ] No duplicate anchor assignments
- [ ] All multi-fit anchors documented with rationale

---

## Error Handling

| Error Condition | Action |
|-----------------|--------|
| Missing Step 1 input | HALT, request Step 1 output |
| Fewer than 20 anchors | WARN, proceed with adjusted section count |
| Cluster too small (<5) | FLAG for merge consideration |
| Cluster too large (>30) | FLAG for split consideration |
| Phase output incomplete | HALT phase, complete before proceeding |

---

## Quality Gates

Before proceeding to Step 3:
- [ ] All 5 phases completed
- [ ] All anchors assigned to clusters
- [ ] Section proposals generated
- [ ] 3-5 arc iterations created
- [ ] Handoff summary prepared

---

**Agent Version:** 1.0
**Last Updated:** 2026-01-04
