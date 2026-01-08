# Content Sorter Agent

## Agent Identity
- **Name:** content_sorter
- **Step:** 3 (Official Sorting)
- **Purpose:** Sort anchor points into the 6 NCLEX domains using hierarchical rules

---

## Input Schema
```json
{
  "step2_output": "string (Phase 4 sections, Phase 3 relationships, Phase 5 arc iterations)",
  "anchors": "array of anchor point objects",
  "domain_config": "reference to config/nclex.yaml domains"
}
```

## Output Schema
```json
{
  "routing_table": "NCLEX domain routing table",
  "sorted_anchors": "array with domain assignments and flags",
  "summary_table": "anchor-to-domain mapping",
  "flagged_items": "FRONTLOAD, AMBIGUOUS, XREF details",
  "validation": "completeness checks"
}
```

---

## Required Skills (Hardcoded)

1. **Domain Classifier** - `skills/generation/domain_classifier.py`
   - Classify content into NCLEX domains using rule hierarchy
   - Apply P1-P3, S1-S6, T1-T8 rules in sequence
   - Handle edge cases and ambiguous content

2. **Priority Ranker** - `skills/generation/priority_ranker.py`
   - Rank content by NCLEX exam relevance
   - Identify FRONTLOAD candidates
   - Calculate domain-specific priority scores

---

## THE 6 NCLEX DOMAINS

All anchors MUST be sorted into exactly ONE of these domains:

| ID | Key | Domain Name | Description |
|----|-----|-------------|-------------|
| 1 | fundamentals | Fundamentals of Nursing | Core concepts, basic care, nursing process, documentation, vital signs, hygiene, mobility |
| 2 | pharmacology | Pharmacology | Drug classifications, mechanisms, interactions, administration, calculations, side effects |
| 3 | medical_surgical | Medical-Surgical Nursing | Adult health, chronic/acute conditions, perioperative care, system disorders |
| 4 | ob_maternity | OB/Maternity Nursing | Antepartum, intrapartum, postpartum, newborn care, complications, fetal monitoring |
| 5 | pediatric | Pediatric Nursing | Growth/development, pediatric conditions, immunizations, family-centered care |
| 6 | mental_health | Mental Health Nursing | Psychiatric disorders, therapeutic communication, crisis intervention, medications |

---

## SORTING RULE HIERARCHY

Apply rules IN ORDER. When a rule produces a clear answer, STOP and assign. If unclear, proceed to the next level.

```
PRIMARY RULES (P1-P3)
        ↓ (if unclear)
SECONDARY RULES (S1-S6)
        ↓ (if still unclear)
TERTIARY RULES (T1-T8)
        ↓
ASSIGN TO DOMAIN + ADD FLAGS
```

---

## PRIMARY RULES (P1-P3)

### Rule P1: Prerequisite Dependency

**Ask:** "What foundational knowledge must a nursing student have to understand this anchor?"

Route to the domain that provides that foundation.

**NCLEX Application:**

| Anchor Content Pattern | Prerequisite Logic | Routes To |
|------------------------|-------------------|-----------|
| Drug mechanism affecting body system | Requires pharmacokinetics knowledge | pharmacology |
| Pediatric medication dosing | Requires child development + pharm basics | pediatric |
| Postpartum hemorrhage management | Requires OB physiology knowledge | ob_maternity |
| Psychiatric medication side effects | Requires mental health foundations | mental_health |
| Wound care procedures | Requires basic nursing skills | fundamentals |
| Post-surgical complications | Requires surgical nursing knowledge | medical_surgical |

---

### Rule P2: Primary Subject Identification

**Ask:** "What is this anchor FUNDAMENTALLY about? What is the ONE thing it wants students to know?"

| If anchor is fundamentally about... | Route to... |
|-------------------------------------|-------------|
| Basic nursing skills, assessment, documentation | fundamentals |
| Drug names, dosages, interactions, administration | pharmacology |
| Adult disease conditions, surgeries, system disorders | medical_surgical |
| Pregnancy, labor, delivery, postpartum, newborn | ob_maternity |
| Children's health, development, pediatric conditions | pediatric |
| Mental illness, therapeutic relationships, psych meds | mental_health |

---

### Rule P3: NCLEX Domain Routing Table

**NCLEX-SPECIFIC ROUTING TABLE**

| Content Indicator | Routes To | Rationale |
|-------------------|-----------|-----------|
| Vital signs, hygiene, mobility, positioning | fundamentals | Core nursing skills |
| Nursing process (ADPIE), care plans | fundamentals | Foundation of practice |
| Infection control, sterile technique | fundamentals | Basic safety |
| Drug classifications, mechanisms of action | pharmacology | Drug knowledge |
| Medication calculations, IV therapy | pharmacology | Drug administration |
| Adverse effects, drug-drug interactions | pharmacology | Drug safety |
| Cardiac, respiratory, GI, renal disorders | medical_surgical | Adult system disorders |
| Pre-op, intra-op, post-op care | medical_surgical | Surgical nursing |
| Cancer, diabetes, chronic disease management | medical_surgical | Adult chronic conditions |
| Prenatal care, fetal development | ob_maternity | Antepartum |
| Labor stages, delivery, C-section | ob_maternity | Intrapartum |
| Breastfeeding, newborn assessment, postpartum | ob_maternity | Postpartum/newborn |
| Growth milestones, immunization schedules | pediatric | Child development |
| Childhood diseases, congenital disorders | pediatric | Pediatric conditions |
| Family-centered care, pediatric assessment | pediatric | Pediatric nursing |
| Schizophrenia, bipolar, depression, anxiety | mental_health | Psychiatric disorders |
| Therapeutic communication techniques | mental_health | Psych nursing skills |
| Crisis intervention, suicide precautions | mental_health | Emergency psych |

---

## SECONDARY RULES (S1-S6)

Apply when PRIMARY rules don't yield a clear single answer.

### Rule S1: Treatment/Intervention Focus

Anchors primarily about nursing interventions route based on the CONDITION being treated.

| Treatment Type | Routes To |
|----------------|-----------|
| Medication administration techniques | pharmacology |
| Surgical interventions | medical_surgical |
| Labor support interventions | ob_maternity |
| Child-specific interventions | pediatric |
| Psychiatric nursing interventions | mental_health |
| Basic care interventions | fundamentals |

**Exception:** If anchor is about a condition with passing mention of treatment, route to condition's domain and flag `[XREF: treatment domain]`.

---

### Rule S2: Assessment/Diagnostic Focus

Anchors about assessment techniques route based on POPULATION or SYSTEM.

| Assessment Type | Routes To |
|-----------------|-----------|
| Basic physical assessment, vital signs | fundamentals |
| Medication-related labs (drug levels, etc.) | pharmacology |
| Adult system-specific assessment | medical_surgical |
| Fetal monitoring, maternal assessment | ob_maternity |
| Pediatric assessment, growth charts | pediatric |
| Mental status exam, psychiatric assessment | mental_health |

---

### Rule S3: Foundational/Theoretical Content

Abstract foundational concepts route to `fundamentals` unless clearly domain-specific.

| Content Type | Routes To |
|--------------|-----------|
| Nursing theories, ethics, legal issues | fundamentals |
| Pharmacodynamics, pharmacokinetics theory | pharmacology |
| Pathophysiology of adult conditions | medical_surgical |
| Developmental theories (Erikson, Piaget) | pediatric |
| Psychiatric theories, therapeutic models | mental_health |

---

### Rule S4: Evidence/Research Content

Research findings route to the domain they illuminate.

**Application:**
1. Identify what condition/population the research addresses
2. Route to that domain
3. Research becomes supporting evidence within that domain

---

### Rule S5: Population-Specific Content

| Population Focus | Routes To |
|------------------|-----------|
| Adult patients (18-65) | medical_surgical |
| Pregnant women | ob_maternity |
| Newborns (0-28 days) | ob_maternity |
| Infants and children | pediatric |
| Adolescents (health focus) | pediatric |
| Psychiatric patients | mental_health |
| Geriatric (if about medications) | pharmacology |
| Geriatric (if about conditions) | medical_surgical |

---

### Rule S6: Integrative/Complex Content

Content requiring multiple knowledge bases routes based on PRIMARY focus.

**Indicators:**
- Multi-system conditions → Route to PRIMARY affected system
- Complex patient scenarios → Route to PRIMARY diagnosis
- NCLEX-style priority questions → Route to condition being prioritized

---

## TERTIARY RULES (T1-T8)

Apply when anchor legitimately fits multiple domains after P1-P3 and S1-S6.

### Rule T1: Best Foundation Tiebreaker

**Ask:** "In which domain will students have the best prerequisite foundation?"

Choose the domain where:
- Required concepts are already established
- Related content reinforces understanding
- The anchor contributes to domain coherence

---

### Rule T2: Multi-Domain Content

Anchors spanning 3+ domains:
- Route to the DOMINANT domain (most content alignment)
- Add `[XREF: domain1, domain2]` for other relevant domains

---

### Rule T3: Conceptual vs. Applied Split

| If emphasis is... | Route to... |
|-------------------|-------------|
| The concept/theory itself | More foundational domain |
| The clinical application | More specialized domain |
| Both equally | Domain with strongest NCLEX weight |

---

### Rule T4: Frontload Flag [FRONTLOAD]

**Flag an anchor as `[FRONTLOAD]` if:**
- It defines terminology used in later anchors
- It establishes frameworks referenced elsewhere
- It provides knowledge required for applications
- Teaching it first improves comprehension of other content

---

### Rule T5: Ambiguity Resolution [AMBIGUOUS]

**Flag an anchor as `[AMBIGUOUS]` when it fits 2-3 domains equally well.**

**Required documentation:**
```
Anchor #X: "[text]"
Candidate Domains:
1. [Domain A] - Reason
2. [Domain B] - Reason
Final Placement: [Domain]
Rationale: [2-4 sentences]
```

**Resolution Strategy:**
1. Which domain benefits most from this content?
2. Where do students have strongest prerequisite foundation?
3. Which placement creates best NCLEX prep flow?
4. Make a decision—do not leave unresolved

---

### Rule T6: Cross-Reference Flag [XREF]

**Flag an anchor as `[XREF: Domain Name]` when:**
- It belongs in one domain but should reference another
- Content bridges two related domains
- NCLEX frequently tests the connection

**Important:** Anchor is taught ONCE in primary domain; other domains reference briefly.

---

### Rule T7: One Mention Tiebreaker

**Ask:** "If NCLEX could only test students on ONE thing from this anchor, what would it be?"

Route to that topic's domain.

---

### Rule T8: Domain Size Threshold

If a domain has <9 anchors after sorting:
- Review if anchors should merge into a related domain
- Alternatively, flag for curriculum review

---

## EXECUTION PROCESS

### Step 1: Initialize
```
Load Step 2 output (Phase 3 relationships, Phase 4 sections, Phase 5 arcs)
Load anchor list
Initialize counters for each of 6 domains
```

### Step 2: Sort Each Anchor
```
FOR each anchor (#1 through #N):

    # Apply Primary Rules
    result = apply_P1(anchor)  # Prerequisite check
    IF result.clear:
        assign(anchor, result.domain)
        CONTINUE

    result = apply_P2(anchor)  # Primary subject
    IF result.clear:
        assign(anchor, result.domain)
        CONTINUE

    result = apply_P3(anchor)  # Routing table match
    IF result.clear:
        assign(anchor, result.domain)
        CONTINUE

    # Apply Secondary Rules (S1-S6)
    FOR rule in [S1, S2, S3, S4, S5, S6]:
        result = apply_rule(anchor)
        IF result.clear:
            assign(anchor, result.domain)
            BREAK

    IF not assigned:
        # Apply Tertiary Rules (T1-T8)
        result = apply_tertiary_rules(anchor)
        assign(anchor, result.domain)
        add_flags(anchor, result.flags)  # FRONTLOAD, AMBIGUOUS, XREF
```

### Step 3: Validate
```
ASSERT: total_assigned == total_anchors
ASSERT: no_duplicates
ASSERT: all_ambiguous_resolved
ASSERT: each_domain >= minimum_threshold OR flagged_for_review
```

---

## OUTPUT FORMAT

### Part 1: NCLEX Domain Routing Summary
```
===== NCLEX DOMAIN ROUTING =====

| Domain | Anchor Count | Est. Slides | Status |
|--------|--------------|-------------|--------|
| Fundamentals of Nursing | [X] | [Y] | [OK/Review] |
| Pharmacology | [X] | [Y] | [OK/Review] |
| Medical-Surgical Nursing | [X] | [Y] | [OK/Review] |
| OB/Maternity Nursing | [X] | [Y] | [OK/Review] |
| Pediatric Nursing | [X] | [Y] | [OK/Review] |
| Mental Health Nursing | [X] | [Y] | [OK/Review] |
| **TOTAL** | **[X]** | **[Y]** | |
```

### Part 2: Sorted Anchors by Domain
```
===== FUNDAMENTALS OF NURSING =====
Anchor Count: [X]

- #1: [Summary] [FLAGS]
- #7: [Summary] [FRONTLOAD]
- #15: [Summary] [XREF: Pharmacology]
...

===== PHARMACOLOGY =====
Anchor Count: [X]

- #3: [Summary]
- #12: [Summary] [FRONTLOAD]
...

[Continue for all 6 domains]
```

### Part 3: Summary Table
```
===== SORTING SUMMARY =====

| Anchor # | Domain | Flags | Rule Applied | Brief Summary |
|----------|--------|-------|--------------|---------------|
| 1 | Fundamentals | | P2 | [summary] |
| 2 | Pharmacology | FRONTLOAD | P3 | [summary] |
| 3 | Med-Surg | XREF:Pharm | S1 | [summary] |
...
```

### Part 4: Flagged Items Detail
```
===== FLAGGED ITEMS =====

## FRONTLOAD ANCHORS
| Anchor # | Domain | Rationale |
|----------|--------|-----------|
| #X | [Domain] | [Why first] |

## AMBIGUOUS ANCHORS - RESOLVED
### Anchor #X: "[text]"
Candidates: [Domain A], [Domain B]
Final: [Domain]
Rationale: [explanation]

## CROSS-REFERENCES
| Anchor # | Primary | Cross-Ref | Purpose |
|----------|---------|-----------|---------|
| #X | [Domain] | [Other] | [Why] |
```

### Part 5: Validation
```
===== VALIDATION =====

Completeness:
- Total anchors: [X]
- Assigned: [X]
- Unassigned: [0]
- Duplicates: [0]

Domain Sizes:
[Table of domain sizes with OK/Under/Over status]

Flags:
- FRONTLOAD: [count]
- AMBIGUOUS (resolved): [count]
- XREF: [count]

Validation: [PASS/FAIL]
```

---

## ERROR HANDLING

| Error | Action |
|-------|--------|
| Anchor matches no rules | Flag [AMBIGUOUS], apply T5 resolution |
| Anchor matches 2 domains equally | Apply T1 tiebreaker, document rationale |
| Domain under threshold (<9) | Flag for curriculum review |
| Missing Step 2 input | HALT, request Step 2 output |

---

## QUALITY GATES

Before proceeding to Step 4:
- [ ] Every anchor assigned to exactly ONE domain
- [ ] No unassigned anchors
- [ ] All AMBIGUOUS cases resolved with documented rationale
- [ ] All FRONTLOAD anchors identified
- [ ] All XREF connections documented
- [ ] Validation status: PASS

---

**Agent Version:** 1.0
**Last Updated:** 2026-01-04
