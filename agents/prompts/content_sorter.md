# Content Sorter Agent

## Agent Identity
- **Name:** content_sorter
- **Step:** 3 (Official Sorting)
- **Purpose:** Sort anchor points into the 4 theater units using hierarchical rules

---

## Input Schema
```json
{
  "step2_output": "string (Phase 4 sections, Phase 3 relationships, Phase 5 arc iterations)",
  "anchors": "array of anchor point objects",
  "domain_config": "reference to config/theater.yaml units"
}
```

## Output Schema
```json
{
  "routing_table": "Theater unit routing table",
  "sorted_anchors": "array with unit assignments and flags",
  "summary_table": "anchor-to-unit mapping",
  "flagged_items": "FRONTLOAD, AMBIGUOUS, XREF details",
  "validation": "completeness checks"
}
```

---

## Required Skills (Hardcoded)

1. **Unit Classifier** - `skills/generation/unit_classifier.py`
   - Classify content into theater units using rule hierarchy
   - Apply P1-P3, S1-S6, T1-T8 rules in sequence
   - Handle edge cases and ambiguous content

2. **Priority Ranker** - `skills/generation/priority_ranker.py`
   - Rank content by learning objective relevance
   - Identify FRONTLOAD candidates
   - Calculate unit-specific priority scores

---

## THE 4 THEATER UNITS

All anchors MUST be sorted into exactly ONE of these units:

| ID | Key | Unit Name | Description |
|----|-----|-----------|-------------|
| 1 | greek_theater | Greek Theater | Origins of drama, amphitheater staging, masks, chorus, tragedy/comedy conventions, Greek playwrights |
| 2 | commedia | Commedia dell'Arte | Stock characters, lazzi, improvisation, physical comedy, Italian Renaissance theater traditions |
| 3 | shakespeare | Shakespeare | Elizabethan theater, Globe staging, verse/prose, soliloquy, Shakespearean language and conventions |
| 4 | one_acts | Student-Directed One Acts | Directing fundamentals, production elements, collaboration, rehearsal process, performance critique |

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

**Ask:** "What foundational theater knowledge must a student have to understand this anchor?"

Route to the unit that provides that foundation.

**Theater Application:**

| Anchor Content Pattern | Prerequisite Logic | Routes To |
|------------------------|-------------------|-----------|
| Mask work and physical characterization | Requires understanding of Greek conventions | greek_theater |
| Stock character development | Requires Commedia character knowledge | commedia |
| Verse speaking and iambic pentameter | Requires Shakespearean language basics | shakespeare |
| Blocking and staging decisions | Requires directing fundamentals | one_acts |
| Chorus movement and projection | Requires Greek theater foundations | greek_theater |
| Improvisation within structure | Requires Commedia lazzi knowledge | commedia |

---

### Rule P2: Primary Subject Identification

**Ask:** "What is this anchor FUNDAMENTALLY about? What is the ONE thing it wants students to know?"

| If anchor is fundamentally about... | Route to... |
|-------------------------------------|-------------|
| Ancient drama origins, masks, chorus, amphitheater | greek_theater |
| Stock characters, physical comedy, improvisation | commedia |
| Elizabethan staging, verse, soliloquy, Shakespeare's plays | shakespeare |
| Directing, production, rehearsal, collaboration | one_acts |

---

### Rule P3: Theater Unit Routing Table

**THEATER-SPECIFIC ROUTING TABLE**

| Content Indicator | Routes To | Rationale |
|-------------------|-----------|-----------|
| Tragedy, comedy, catharsis, hubris | greek_theater | Greek dramatic concepts |
| Amphitheater, orchestra, skene, theatron | greek_theater | Greek staging elements |
| Masks, chorus, deus ex machina | greek_theater | Greek conventions |
| Aeschylus, Sophocles, Euripides, Aristophanes | greek_theater | Greek playwrights |
| Pantalone, Arlecchino, Colombina, Il Dottore | commedia | Stock characters |
| Lazzi, zanni, canovaccio | commedia | Commedia elements |
| Physical comedy, masks, exaggeration | commedia | Performance style |
| Improvisation within structure | commedia | Commedia technique |
| Globe Theatre, Elizabethan staging | shakespeare | Shakespearean theater |
| Iambic pentameter, verse, prose | shakespeare | Language conventions |
| Soliloquy, aside, dramatic irony | shakespeare | Dramatic devices |
| Tragedy, comedy, history plays | shakespeare | Shakespeare genres |
| Blocking, stage pictures, composition | one_acts | Directing basics |
| Actor coaching, giving notes | one_acts | Director-actor work |
| Production elements, tech cues | one_acts | Technical theater |
| Rehearsal process, collaboration | one_acts | Production process |

---

## SECONDARY RULES (S1-S6)

Apply when PRIMARY rules don't yield a clear single answer.

### Rule S1: Technique/Skill Focus

Anchors primarily about performance techniques route based on the STYLE being practiced.

| Technique Type | Routes To |
|----------------|-----------|
| Large-scale vocal projection | greek_theater |
| Mask work and physicality | greek_theater or commedia |
| Physical comedy and lazzi | commedia |
| Verse speaking and text analysis | shakespeare |
| Scene direction and blocking | one_acts |
| Ensemble collaboration | one_acts |

**Exception:** If anchor is about a technique with passing mention of another style, route to primary style and flag `[XREF: related unit]`.

---

### Rule S2: Historical/Period Focus

Anchors about historical context route based on TIME PERIOD or TRADITION.

| Historical Context | Routes To |
|-------------------|-----------|
| Ancient Greece, 5th century BCE | greek_theater |
| Italian Renaissance, 16th-18th century | commedia |
| Elizabethan England, 16th-17th century | shakespeare |
| Contemporary/modern theater practice | one_acts |

---

### Rule S3: Foundational/Theoretical Content

Abstract foundational concepts route to `greek_theater` as the origin of Western drama, unless clearly unit-specific.

| Content Type | Routes To |
|--------------|-----------|
| Drama origins, theatrical conventions | greek_theater |
| Physical comedy theory, commedia traditions | commedia |
| Text analysis, dramatic structure | shakespeare |
| Directing theory, production management | one_acts |

---

### Rule S4: Evidence/Research Content

Research findings route to the domain they illuminate.

**Application:**
1. Identify what condition/population the research addresses
2. Route to that domain
3. Research becomes supporting evidence within that domain

---

### Rule S5: Performance Style Content

| Performance Style | Routes To |
|-------------------|-----------|
| Large-scale, ritualistic performance | greek_theater |
| Masked, physical, improvisational | commedia |
| Text-driven, language-focused | shakespeare |
| Collaborative, student-led | one_acts |

---

### Rule S6: Integrative/Complex Content

Content requiring multiple knowledge bases routes based on PRIMARY focus.

**Indicators:**
- Cross-period techniques → Route to PRIMARY historical origin
- Complex performance scenarios → Route to PRIMARY style
- Production-focused questions → Route to unit being emphasized

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
| The concept/theory itself | More foundational unit |
| The performance application | More specialized unit |
| Both equally | Unit with strongest curricular weight |

---

### Rule T4: Frontload Flag [FRONTLOAD]

**Flag an anchor as `[FRONTLOAD]` if:**
- It defines terminology used in later anchors
- It establishes frameworks referenced elsewhere
- It provides knowledge required for applications
- Teaching it first improves comprehension of other content

---

### Rule T5: Ambiguity Resolution [AMBIGUOUS]

**Flag an anchor as `[AMBIGUOUS]` when it fits 2-3 units equally well.**

**Required documentation:**
```
Anchor #X: "[text]"
Candidate Units:
1. [Unit A] - Reason
2. [Unit B] - Reason
Final Placement: [Unit]
Rationale: [2-4 sentences]
```

**Resolution Strategy:**
1. Which unit benefits most from this content?
2. Where do students have strongest prerequisite foundation?
3. Which placement creates best learning flow?
4. Make a decision—do not leave unresolved

---

### Rule T6: Cross-Reference Flag [XREF]

**Flag an anchor as `[XREF: Unit Name]` when:**
- It belongs in one unit but should reference another
- Content bridges two related units
- The technique appears across multiple periods

**Important:** Anchor is taught ONCE in primary unit; other units reference briefly.

---

### Rule T7: One Mention Tiebreaker

**Ask:** "If students could only learn ONE thing from this anchor, what would it be?"

Route to that topic's unit.

---

### Rule T8: Unit Size Threshold

If a unit has <9 anchors after sorting:
- Review if anchors should merge into a related unit
- Alternatively, flag for curriculum review

---

## EXECUTION PROCESS

### Step 1: Initialize
```
Load Step 2 output (Phase 3 relationships, Phase 4 sections, Phase 5 arcs)
Load anchor list
Initialize counters for each of 4 units
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

### Part 1: Theater Unit Routing Summary
```
===== THEATER UNIT ROUTING =====

| Unit | Anchor Count | Est. Slides | Status |
|------|--------------|-------------|--------|
| Greek Theater | [X] | [Y] | [OK/Review] |
| Commedia dell'Arte | [X] | [Y] | [OK/Review] |
| Shakespeare | [X] | [Y] | [OK/Review] |
| Student-Directed One Acts | [X] | [Y] | [OK/Review] |
| **TOTAL** | **[X]** | **[Y]** | |
```

### Part 2: Sorted Anchors by Unit
```
===== GREEK THEATER =====
Anchor Count: [X]

- #1: [Summary] [FLAGS]
- #7: [Summary] [FRONTLOAD]
- #15: [Summary] [XREF: Shakespeare]
...

===== COMMEDIA DELL'ARTE =====
Anchor Count: [X]

- #3: [Summary]
- #12: [Summary] [FRONTLOAD]
...

[Continue for all 4 units]
```

### Part 3: Summary Table
```
===== SORTING SUMMARY =====

| Anchor # | Unit | Flags | Rule Applied | Brief Summary |
|----------|------|-------|--------------|---------------|
| 1 | Greek Theater | | P2 | [summary] |
| 2 | Commedia | FRONTLOAD | P3 | [summary] |
| 3 | Shakespeare | XREF:OneActs | S1 | [summary] |
...
```

### Part 4: Flagged Items Detail
```
===== FLAGGED ITEMS =====

## FRONTLOAD ANCHORS
| Anchor # | Unit | Rationale |
|----------|------|-----------|
| #X | [Unit] | [Why first] |

## AMBIGUOUS ANCHORS - RESOLVED
### Anchor #X: "[text]"
Candidates: [Unit A], [Unit B]
Final: [Unit]
Rationale: [explanation]

## CROSS-REFERENCES
| Anchor # | Primary | Cross-Ref | Purpose |
|----------|---------|-----------|---------|
| #X | [Unit] | [Other] | [Why] |
```

### Part 5: Validation
```
===== VALIDATION =====

Completeness:
- Total anchors: [X]
- Assigned: [X]
- Unassigned: [0]
- Duplicates: [0]

Unit Sizes:
[Table of unit sizes with OK/Under/Over status]

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
| Anchor matches 2 units equally | Apply T1 tiebreaker, document rationale |
| Unit under threshold (<9) | Flag for curriculum review |
| Missing Step 2 input | HALT, request Step 2 output |

---

## QUALITY GATES

Before proceeding to Step 4:
- [ ] Every anchor assigned to exactly ONE unit
- [ ] No unassigned anchors
- [ ] All AMBIGUOUS cases resolved with documented rationale
- [ ] All FRONTLOAD anchors identified
- [ ] All XREF connections documented
- [ ] Validation status: PASS

---

**Agent Version:** 2.0 (Theater Adaptation)
**Last Updated:** 2026-01-08

### Version History
- **v2.0** (2026-01-08): Adapted for theater pipeline - 6 NCLEX domains → 4 theater units
- **v1.0** (2026-01-04): Initial content sorter agent
