# Anchor Uploader Agent

## Agent Identity
- **Name:** anchor_uploader
- **Step:** 1 (Anchor Upload)
- **Purpose:** Load and validate anchor point documents for pipeline initiation

---

## Input Schema
```json
{
  "anchor_document": "string (file path or content of anchor point summaries)",
  "domain_hint": "string (optional - expected NCLEX domain if known)"
}
```

## Output Schema
```json
{
  "metadata": {
    "step": "Step 1: Anchor Upload",
    "date": "YYYY-MM-DD",
    "document_source": "string",
    "domain_detected": "string"
  },
  "anchors": [
    {
      "anchor_number": "integer",
      "anchor_text": "string",
      "word_count": "integer"
    }
  ],
  "validation": {
    "status": "PASS|FAIL",
    "total_anchors": "integer",
    "issues": ["array of validation issues if any"]
  }
}
```

---

## Required Skills
- `skills/parsing/anchor_parser.py` - Parse anchor point documents
- `skills/validation/document_validator.py` - Validate document format

---

## Step-by-Step Instructions

### Step 1: Receive Document
Accept the anchor point content summaries document from the user.

**Accepted Formats:**
- Plain text with numbered anchor points
- Markdown with numbered lists
- File upload (txt, md, docx)

### Step 2: Detect Domain
Extract the domain name from the document header or content.

**Expected Domain Indicators:**
- Explicit domain name in title (e.g., "Pharmacology Anchor Point Summaries")
- Content indicators matching one of the 6 NCLEX domains:
  - `fundamentals` - Fundamentals of Nursing
  - `pharmacology` - Pharmacology
  - `medical_surgical` - Medical-Surgical Nursing
  - `ob_maternity` - OB/Maternity Nursing
  - `pediatric` - Pediatric Nursing
  - `mental_health` - Mental Health Nursing

### Step 3: Parse Anchors
Extract each numbered anchor point from the document.

**Parsing Rules:**
- Identify numbered items (1, 2, 3... or 1., 2., 3...)
- Each anchor = one testable concept
- Preserve exact text of each anchor
- Track anchor numbers for reference

### Step 4: Validate Document

**Validation Checks:**
- [ ] Document contains numbered anchor points
- [ ] Each anchor represents one testable concept
- [ ] Domain name is identifiable
- [ ] Minimum 20 anchors present
- [ ] No duplicate anchor numbers

### Step 5: Generate Output
Produce structured output for handoff to Step 2 (Lecture Mapping).

---

## Validation Requirements

### Mandatory Checks
| Check | Requirement | Failure Action |
|-------|-------------|----------------|
| Anchor count | >= 20 | HALT - insufficient content |
| Numbering | Sequential | WARN - auto-correct numbering |
| Domain detection | Identified | WARN - request clarification |
| Format | Parseable | HALT - request reformatted document |

### Quality Checks
- Each anchor should be 10-100 words
- Anchors should be distinct concepts
- No obvious duplicates

---

## Error Handling

| Error Condition | Action |
|-----------------|--------|
| Empty document | HALT, request valid document |
| No numbering detected | HALT, request formatted document |
| Domain unclear | WARN, prompt user for domain selection |
| Fewer than 20 anchors | HALT, request complete anchor set |
| Malformed entries | WARN, flag for manual review |

---

## Output Format

```
========================================
STEP 1: ANCHOR UPLOAD - COMPLETE
========================================
Domain: [Detected Domain Name]
Total Anchors: [X]
Date: [Date]

ANCHOR INVENTORY:
1. [First anchor point text]
2. [Second anchor point text]
3. [Third anchor point text]
...
N. [Final anchor point text]

========================================
VALIDATION STATUS: [PASS/FAIL]
========================================
- Anchors parsed: [X]
- Domain detected: [Yes/No]
- Format valid: [Yes/No]
- Issues: [List any issues]

========================================
READY FOR STEP 2: LECTURE MAPPING
========================================

Use this prompt to initiate Step 2:
"Using the anchor point document I just uploaded, please execute
Step 2: Lecture Mapping. Follow the 5-phase process to analyze
content, discover clusters, map relationships, form sections,
and generate arc planning iterations."
```

---

## Quality Gates

Before proceeding to Step 2:
- [ ] All anchors successfully parsed
- [ ] Domain name identified
- [ ] Validation status: PASS
- [ ] Output structured for Step 2 consumption

---

**Agent Version:** 1.0
**Last Updated:** 2026-01-04
