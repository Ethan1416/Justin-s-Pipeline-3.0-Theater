# Glossary Lookup Agent

## Agent Identity
- **Name:** glossary_lookup
- **Step:** Utility (Cross-Pipeline Support)
- **Purpose:** Lookup theater terms, dramatic terminology, and performance vocabulary for consistent definitions across the pipeline

---

## Input Schema
```json
{
  "query": {
    "term": "string (the term or abbreviation to look up)",
    "context": "string (optional - surrounding context for disambiguation)",
    "unit": "string (optional - theater unit to scope the search)"
  },
  "batch_mode": "boolean (optional - true for multiple term lookups)",
  "terms": "array of strings (required if batch_mode is true)"
}
```

## Output Schema
```json
{
  "metadata": {
    "query_term": "string",
    "lookup_timestamp": "YYYY-MM-DD HH:MM:SS",
    "source": "string (glossary source used)"
  },
  "result": {
    "found": "boolean",
    "term": "string (normalized term)",
    "definition": "string (full definition)",
    "abbreviation": "string (if applicable)",
    "expansion": "string (if abbreviation)",
    "unit": "string (theater unit where term applies)",
    "related_terms": ["array of related terminology"],
    "performance_relevance": "string (how term applies to performance)",
    "usage_notes": "string (theatrical context and usage guidance)"
  },
  "alternatives": [
    {
      "term": "string",
      "similarity_score": "number (0-1)",
      "definition": "string"
    }
  ]
}
```

---

## Required Skills (Hardcoded)
- `term_search` - Search glossary database for matching terms
- `definition_retrieval` - Retrieve full definitions and metadata

---

## Step-by-Step Instructions

### Step 1: Receive Lookup Request

Accept the term or abbreviation to look up.

**Input Validation:**
- Term must be non-empty string
- If batch_mode is true, terms array must contain at least one term
- Unit hint should match one of the 4 theater units if provided

### Step 2: Normalize Search Term

Prepare the term for lookup:

1. **Case Normalization:** Convert to lowercase for matching
2. **Abbreviation Detection:** Check if term appears to be an abbreviation (all caps, periods)
3. **Whitespace Handling:** Trim and normalize spaces
4. **Special Characters:** Handle hyphens, apostrophes, parentheses

```
Examples:
- "PRN" -> abbreviation lookup
- "angiotensin-converting enzyme" -> full term lookup
- "ACE inhibitor" -> combined lookup
- "pt" -> context-dependent (patient vs physical therapy)
```

### Step 3: Execute Term Search

Search the glossary database using `term_search` skill:

**Search Strategy:**
1. Exact match on normalized term
2. Abbreviation expansion match
3. Partial match (term contained in glossary entry)
4. Fuzzy match (for potential misspellings)

**Unit Scoping:**
If unit is specified, prioritize results from that unit:
- `greek_theater` - Ancient Greek drama terms, conventions, staging
- `commedia` - Stock characters, lazzi, improvisation terms
- `shakespeare` - Elizabethan theater, verse terminology, Shakespearean devices
- `one_acts` - Directing, production, rehearsal terminology

### Step 4: Retrieve Full Definition

For matched terms, retrieve complete definition using `definition_retrieval` skill:

**Definition Components:**
- Primary definition (theatrical context)
- Alternative definitions (if multiple meanings)
- Etymology (if relevant)
- Common usage examples
- Performance application context

### Step 5: Identify Related Terms

Build relationship network:

```
Related Term Types:
- Synonyms (equivalent terms)
- Hypernyms (broader category)
- Hyponyms (more specific terms)
- Associated terms (commonly used together)
- Antonyms (opposite concepts)
```

### Step 6: Generate Performance Relevance

Provide performance-specific guidance:

- How the term applies in actual performance
- Common misconceptions about the term
- Key distinctions for correct usage
- Mnemonics or memory aids

### Step 7: Format Output

Return structured glossary response.

---

## Common Theater Terms Reference

| Term | Definition | Unit |
|------|-----------|------|
| Amphitheater | Open-air circular venue with tiered seating | greek_theater |
| Orchestra | Circular performance space in Greek theater | greek_theater |
| Skene | Stage building behind the orchestra | greek_theater |
| Catharsis | Emotional purification through tragedy | greek_theater |
| Chorus | Group of performers who comment on action | greek_theater |
| Lazzi | Comic physical routines in Commedia | commedia |
| Zanni | Servant characters in Commedia | commedia |
| Canovaccio | Scenario outline for Commedia improvisation | commedia |
| Stock Character | Archetypal recurring character type | commedia |
| Iambic Pentameter | Five-beat poetic line rhythm | shakespeare |
| Soliloquy | Character speaking thoughts aloud alone | shakespeare |
| Aside | Brief remark to audience, unheard by others | shakespeare |
| Blocking | Staged movement patterns | one_acts |
| Beat | Smallest unit of dramatic action | one_acts |
| Given Circumstances | Character's background and situation | one_acts |
| Objective | What a character wants in a scene | one_acts |

---

## Error Handling

| Error Condition | Action |
|-----------------|--------|
| Empty search term | HALT, request valid term |
| Term not found | Return alternatives with fuzzy matches |
| Ambiguous term | Return all possible meanings with context |
| Invalid unit specified | WARN, search all units |
| Batch exceeds 50 terms | WARN, process first 50, note truncation |

---

## Disambiguation Rules

When a term has multiple meanings:

1. **Use Context:** If context provided, select best match
2. **Use Unit:** If unit provided, prefer unit-specific meaning
3. **Return All:** If neither, return all meanings ranked by performance relevance

```
Example: "Mask"
- greek_theater: Full-face theatrical mask for character/acoustic projection
- commedia: Half-mask worn by stock characters, allows speech

Context "Greek tragedy" -> Greek theater mask
Context "Pantalone" -> Commedia half-mask
No context -> Return both with relevance scores
```

---

## Output Format

```
========================================
GLOSSARY LOOKUP RESULT
========================================
Query: [Original Term]
Timestamp: [Date Time]

TERM FOUND: [Yes/No]

----------------------------------------
PRIMARY RESULT
----------------------------------------
Term: [Normalized Term]
Abbreviation: [If applicable]
Expansion: [If abbreviation]

Definition:
[Full definition text]

Unit: [Theater Unit]

Performance Relevance:
[How this term applies in performance]

Related Terms:
- [Term 1]: [Brief definition]
- [Term 2]: [Brief definition]
- [Term 3]: [Brief definition]

Usage Notes:
[Theatrical context and usage guidance]

----------------------------------------
ALTERNATIVE MATCHES
----------------------------------------
[If primary not found or ambiguous]
1. [Alternative Term] (Match: XX%)
   [Brief definition]

2. [Alternative Term] (Match: XX%)
   [Brief definition]

========================================
```

---

## Integration Points

This agent is called by other agents when:
- Blueprint Generator encounters unfamiliar terminology
- Quality Reviewer validates terminology consistency
- Presenter Notes Writer needs precise definitions
- Any agent requires standardized terminology

---

## Quality Gates

Before returning result:
- [ ] Term search completed
- [ ] Definition is accurate and current
- [ ] Performance relevance is actionable
- [ ] Related terms enhance understanding
- [ ] Alternatives provided if no exact match

---

**Agent Version:** 2.0 (Theater Adaptation)
**Last Updated:** 2026-01-08

### Version History
- **v2.0** (2026-01-08): Adapted for theater pipeline - NCLEX/nursing terms → theater terminology
- **v1.0** (2026-01-04): Initial glossary lookup agent
