# Consistency Checker Agent

## Agent Identity
- **Name:** consistency_checker
- **Step:** 8 (Quality Assurance - Terminology Consistency)
- **Purpose:** Verify terminology consistency across blueprints, ensuring no conflicting definitions or inconsistent style usage

---

## Input Schema
```json
{
  "blueprint": "string (blueprint content to validate)",
  "section_name": "string (current section name)",
  "domain": "string (theater unit)",
  "glossary_reference": "reference to terminology glossary (optional)",
  "previous_sections": "array of previous section blueprints (optional)"
}
```

## Output Schema
```json
{
  "validation_status": "string (PASS/FAIL)",
  "section_name": "string",
  "domain": "string",
  "terminology_consistency": {
    "status": "string (PASS/FAIL)",
    "terms_analyzed": "number",
    "inconsistencies_found": "number",
    "inconsistencies": [
      {
        "term": "string",
        "variations_found": "array of strings",
        "occurrences": "object mapping variation to count",
        "recommended_term": "string",
        "severity": "string (ERROR/WARNING)"
      }
    ]
  },
  "style_consistency": {
    "status": "string (PASS/FAIL)",
    "issues": [
      {
        "type": "string (CAPITALIZATION/ABBREVIATION/FORMATTING/PUNCTUATION)",
        "description": "string",
        "examples": "array of strings",
        "recommendation": "string",
        "severity": "string (ERROR/WARNING)"
      }
    ]
  },
  "definition_conflicts": {
    "status": "string (PASS/FAIL)",
    "conflicts": [
      {
        "term": "string",
        "definition_1": "string",
        "location_1": "string (slide number)",
        "definition_2": "string",
        "location_2": "string (slide number)",
        "severity": "string (ERROR/WARNING)"
      }
    ]
  },
  "cross_section_consistency": {
    "status": "string (PASS/FAIL/N/A)",
    "issues": "array of cross-section inconsistencies"
  },
  "total_issues": "number",
  "recommendations": "array of strings"
}
```

---

## Required Skills (Hardcoded)

1. **terminology_validation** - Identify and track terminology usage across content
2. **style_consistency** - Check for consistent capitalization, abbreviations, formatting
3. **definition_tracking** - Detect conflicting definitions of the same term
4. **cross_reference_check** - Compare terminology across multiple sections

---

## Validation Rules

### Terminology Standards

1. **Medical Terminology:**
   - Use standard medical abbreviations
   - Spell out abbreviations on first use
   - Maintain consistent spelling (American English)

2. **Theater-Specific Terms:**
   - Use official theater terminology
   - Consistent use of "performer" vs "actor"
   - Standardized theater terminology

3. **Nursing Process Terms:**
   - Assessment (not Assess, Assessing in isolation)
   - Diagnosis (Nursing Diagnosis)
   - Planning
   - Implementation
   - Evaluation

### Style Consistency Rules

1. **Capitalization:**
   - Proper nouns capitalized
   - Medical conditions: lowercase unless proper noun
   - Drug names: Generic (lowercase), Brand (capitalized)
   - Nursing diagnoses: Capitalized per NANDA format

2. **Abbreviations:**
   - Standard medical abbreviations only
   - Spell out on first use
   - Consistent throughout section

3. **Formatting:**
   - Consistent bullet point style
   - Consistent numbering format
   - Consistent emphasis (bold, italic)

4. **Punctuation:**
   - Consistent list punctuation (periods or no periods)
   - Consistent use of serial comma
   - Proper use of colons and semicolons

---

## Step-by-Step Instructions

### Step 1: Extract and Index Terms
```python
def extract_terms(blueprint_content):
    """Extract medical/nursing terms and track occurrences."""

    # Common medical/nursing term patterns
    TERM_PATTERNS = [
        r'\b[A-Z]{2,6}\b',  # Abbreviations
        r'\b\w+itis\b',      # Medical conditions
        r'\b\w+emia\b',
        r'\b\w+osis\b',
        r'\b\w+pathy\b',
        r'\b\w+ectomy\b',
        r'\b\w+plasty\b',
        r'\b\w+scopy\b'
    ]

    term_index = {}
    slides = parse_slides(blueprint_content)

    for slide_num, slide in enumerate(slides, 1):
        content = slide.get('body', '') + ' ' + slide.get('title', '')

        # Extract potential terms
        words = re.findall(r'\b[A-Za-z][A-Za-z-]+[A-Za-z]\b', content)

        for word in words:
            # Normalize for comparison
            normalized = word.lower()

            if normalized not in term_index:
                term_index[normalized] = {
                    'variations': {},
                    'locations': []
                }

            # Track variations (case differences)
            if word not in term_index[normalized]['variations']:
                term_index[normalized]['variations'][word] = 0
            term_index[normalized]['variations'][word] += 1

            term_index[normalized]['locations'].append(slide_num)

    return term_index
```

### Step 2: Check Terminology Consistency
```python
def check_terminology_consistency(term_index):
    """Check for inconsistent term usage."""

    inconsistencies = []

    for term, data in term_index.items():
        variations = data['variations']

        # Check if multiple variations exist
        if len(variations) > 1:
            # Determine recommended form
            most_common = max(variations, key=variations.get)

            inconsistencies.append({
                'term': term,
                'variations_found': list(variations.keys()),
                'occurrences': variations,
                'recommended_term': most_common,
                'severity': 'WARNING' if len(variations) == 2 else 'ERROR'
            })

    # Check specific known inconsistencies
    KNOWN_PAIRS = [
        ('patient', 'client'),
        ('healthcare', 'health care'),
        ('bp', 'blood pressure'),
        ('hr', 'heart rate'),
        ('prn', 'as needed')
    ]

    for term1, term2 in KNOWN_PAIRS:
        if term1 in term_index and term2 in term_index:
            inconsistencies.append({
                'term': f'{term1}/{term2}',
                'variations_found': [term1, term2],
                'occurrences': {
                    term1: sum(term_index[term1]['variations'].values()),
                    term2: sum(term_index[term2]['variations'].values())
                },
                'recommended_term': term2 if 'client' in (term1, term2) else term1,
                'severity': 'ERROR'
            })

    return {
        'status': 'PASS' if len([i for i in inconsistencies if i['severity'] == 'ERROR']) == 0 else 'FAIL',
        'terms_analyzed': len(term_index),
        'inconsistencies_found': len(inconsistencies),
        'inconsistencies': inconsistencies
    }
```

### Step 3: Check Style Consistency
```python
def check_style_consistency(blueprint_content):
    """Check for consistent styling across content."""

    issues = []
    slides = parse_slides(blueprint_content)

    # Check capitalization patterns
    cap_patterns = analyze_capitalization(slides)
    if cap_patterns['inconsistent']:
        issues.append({
            'type': 'CAPITALIZATION',
            'description': 'Inconsistent capitalization of terms',
            'examples': cap_patterns['examples'][:3],
            'recommendation': 'Standardize capitalization',
            'severity': 'WARNING'
        })

    # Check abbreviation consistency
    abbrev_issues = check_abbreviation_usage(blueprint_content)
    for issue in abbrev_issues:
        issues.append({
            'type': 'ABBREVIATION',
            'description': issue['description'],
            'examples': issue['examples'],
            'recommendation': issue['fix'],
            'severity': 'WARNING'
        })

    # Check bullet point consistency
    bullet_styles = analyze_bullet_styles(slides)
    if bullet_styles['inconsistent']:
        issues.append({
            'type': 'FORMATTING',
            'description': 'Inconsistent bullet point styles',
            'examples': bullet_styles['examples'][:3],
            'recommendation': 'Use consistent bullet markers (-,*,)',
            'severity': 'WARNING'
        })

    # Check list punctuation
    punct_issues = analyze_list_punctuation(slides)
    if punct_issues['inconsistent']:
        issues.append({
            'type': 'PUNCTUATION',
            'description': 'Inconsistent list item punctuation',
            'examples': punct_issues['examples'][:3],
            'recommendation': 'Either use periods on all list items or none',
            'severity': 'WARNING'
        })

    return {
        'status': 'PASS' if len([i for i in issues if i['severity'] == 'ERROR']) == 0 else 'FAIL',
        'issues': issues
    }

def analyze_capitalization(slides):
    """Analyze capitalization patterns."""
    # Track condition/disease capitalization
    conditions = []
    for slide in slides:
        content = slide.get('body', '')
        # Find potential medical conditions
        matches = re.findall(r'\b(diabetes|hypertension|pneumonia|asthma|copd)\b', content, re.I)
        conditions.extend(matches)

    if not conditions:
        return {'inconsistent': False, 'examples': []}

    # Check if mix of capitalized and lowercase
    caps = [c for c in conditions if c[0].isupper()]
    lower = [c for c in conditions if c[0].islower()]

    return {
        'inconsistent': len(caps) > 0 and len(lower) > 0,
        'examples': list(set(conditions))
    }

def check_abbreviation_usage(content):
    """Check abbreviation usage patterns."""
    issues = []

    # Common nursing abbreviations
    ABBREVS = {
        'BP': 'blood pressure',
        'HR': 'heart rate',
        'RR': 'respiratory rate',
        'I&O': 'intake and output',
        'PRN': 'as needed',
        'NPO': 'nothing by mouth',
        'ADL': 'activities of daily living',
        'ROM': 'range of motion'
    }

    for abbrev, full in ABBREVS.items():
        abbrev_count = len(re.findall(rf'\b{abbrev}\b', content))
        full_count = len(re.findall(rf'\b{full}\b', content, re.I))

        if abbrev_count > 0 and full_count > 0:
            issues.append({
                'description': f'Mixed use of "{abbrev}" and "{full}"',
                'examples': [abbrev, full],
                'fix': f'Spell out "{full}" on first use, then use "{abbrev}"'
            })

    return issues

def analyze_bullet_styles(slides):
    """Analyze bullet point consistency."""
    bullet_chars = []
    for slide in slides:
        content = slide.get('body', '')
        for line in content.split('\n'):
            if line.strip():
                first_char = line.strip()[0] if line.strip() else ''
                if first_char in '-*':
                    bullet_chars.append(first_char)

    unique_bullets = set(bullet_chars)
    return {
        'inconsistent': len(unique_bullets) > 1,
        'examples': list(unique_bullets)
    }

def analyze_list_punctuation(slides):
    """Analyze list item punctuation."""
    with_period = 0
    without_period = 0

    for slide in slides:
        content = slide.get('body', '')
        for line in content.split('\n'):
            if line.strip().startswith(('-', '*', '')):
                if line.strip().endswith('.'):
                    with_period += 1
                elif len(line.strip()) > 5:
                    without_period += 1

    return {
        'inconsistent': with_period > 0 and without_period > 0,
        'examples': [f'{with_period} items with periods', f'{without_period} without']
    }
```

### Step 4: Check for Definition Conflicts
```python
def check_definition_conflicts(blueprint_content):
    """Check for conflicting definitions of the same term."""

    conflicts = []
    slides = parse_slides(blueprint_content)

    # Track definitions (look for "X is Y" or "X: Y" patterns)
    definitions = {}

    for slide_num, slide in enumerate(slides, 1):
        content = slide.get('body', '')

        # Pattern: "Term is definition"
        is_patterns = re.findall(r'(\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s+is\s+(.+?)(?:\.|$)', content)

        # Pattern: "Term: definition"
        colon_patterns = re.findall(r'(\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*):\s*(.+?)(?:\.|$)', content)

        for term, definition in is_patterns + colon_patterns:
            term_lower = term.lower()
            def_normalized = definition.strip().lower()[:100]

            if term_lower in definitions:
                existing = definitions[term_lower]
                if existing['definition'] != def_normalized:
                    # Check similarity - might just be rephrasing
                    if not definitions_similar(existing['definition'], def_normalized):
                        conflicts.append({
                            'term': term,
                            'definition_1': existing['definition'],
                            'location_1': f"Slide {existing['location']}",
                            'definition_2': def_normalized,
                            'location_2': f"Slide {slide_num}",
                            'severity': 'ERROR'
                        })
            else:
                definitions[term_lower] = {
                    'definition': def_normalized,
                    'location': slide_num
                }

    return {
        'status': 'PASS' if len(conflicts) == 0 else 'FAIL',
        'conflicts': conflicts
    }

def definitions_similar(def1, def2, threshold=0.7):
    """Check if two definitions are similar (simple word overlap)."""
    words1 = set(def1.split())
    words2 = set(def2.split())

    if not words1 or not words2:
        return True

    overlap = len(words1 & words2)
    similarity = overlap / max(len(words1), len(words2))

    return similarity >= threshold
```

### Step 5: Generate Consistency Report
```python
def generate_consistency_report(blueprint_content, section_name, domain, previous_sections=None):
    """Generate comprehensive consistency report."""

    # Extract terms
    term_index = extract_terms(blueprint_content)

    # Run all checks
    terminology_result = check_terminology_consistency(term_index)
    style_result = check_style_consistency(blueprint_content)
    definition_result = check_definition_conflicts(blueprint_content)

    # Cross-section check (if previous sections provided)
    cross_section_result = {'status': 'N/A', 'issues': []}
    if previous_sections:
        cross_section_result = check_cross_section_consistency(
            blueprint_content, previous_sections, term_index
        )

    # Calculate totals
    total_issues = (
        terminology_result['inconsistencies_found'] +
        len(style_result['issues']) +
        len(definition_result['conflicts']) +
        len(cross_section_result.get('issues', []))
    )

    # Count errors vs warnings
    error_count = (
        len([i for i in terminology_result['inconsistencies'] if i['severity'] == 'ERROR']) +
        len([i for i in style_result['issues'] if i['severity'] == 'ERROR']) +
        len([c for c in definition_result['conflicts'] if c['severity'] == 'ERROR'])
    )

    # Generate recommendations
    recommendations = []
    if terminology_result['inconsistencies_found'] > 0:
        recommendations.append('Standardize terminology - use recommended terms consistently')
    if len(style_result['issues']) > 0:
        recommendations.append('Review and standardize formatting, capitalization, abbreviations')
    if len(definition_result['conflicts']) > 0:
        recommendations.append('Resolve conflicting definitions - ensure single definition per term')
    if cross_section_result.get('issues'):
        recommendations.append('Align terminology with previous sections for lecture consistency')

    # Determine overall status
    overall_status = 'PASS' if error_count == 0 else 'FAIL'

    return {
        'validation_status': overall_status,
        'section_name': section_name,
        'domain': domain,
        'terminology_consistency': terminology_result,
        'style_consistency': style_result,
        'definition_conflicts': definition_result,
        'cross_section_consistency': cross_section_result,
        'total_issues': total_issues,
        'recommendations': recommendations
    }

def check_cross_section_consistency(current_blueprint, previous_sections, current_terms):
    """Check terminology consistency across sections."""
    issues = []

    for prev_section in previous_sections:
        prev_terms = extract_terms(prev_section.get('content', ''))

        for term, current_data in current_terms.items():
            if term in prev_terms:
                prev_variations = set(prev_terms[term]['variations'].keys())
                curr_variations = set(current_data['variations'].keys())

                if prev_variations != curr_variations:
                    issues.append({
                        'term': term,
                        'previous_usage': list(prev_variations),
                        'current_usage': list(curr_variations),
                        'severity': 'WARNING'
                    })

    return {
        'status': 'PASS' if len(issues) == 0 else 'FAIL',
        'issues': issues
    }
```

---

## Error Codes

| Code | Severity | Description | Action |
|------|----------|-------------|--------|
| CONS_001 | ERROR | Conflicting term definitions | Resolve to single definition |
| CONS_002 | ERROR | Critical terminology inconsistency | Standardize term usage |
| CONS_003 | WARNING | Minor term variation | Review and standardize |
| CONS_004 | WARNING | Capitalization inconsistency | Standardize capitalization |
| CONS_005 | WARNING | Abbreviation usage inconsistent | Spell out on first use |
| CONS_006 | WARNING | Formatting inconsistency | Standardize formatting |
| CONS_007 | WARNING | Cross-section term mismatch | Align with previous sections |
| CONS_008 | INFO | Style preference noted | Consider standardizing |

---

## Output Format

### Text Report
```
===== CONSISTENCY VALIDATION REPORT =====
Section: [Section Name]
Domain: [Domain Name]
Date: [YYYY-MM-DD HH:MM:SS]

STATUS: [PASS/FAIL]

TERMINOLOGY CONSISTENCY:
----------------------------------------
Status: [PASS/FAIL]
Terms Analyzed: [N]
Inconsistencies Found: [N]

[If inconsistencies]
Term: [term]
  Variations: [var1] ([count]), [var2] ([count])
  Recommended: [recommended]
  Severity: [ERROR/WARNING]

[...more inconsistencies...]

STYLE CONSISTENCY:
----------------------------------------
Status: [PASS/FAIL]
Issues Found: [N]

[If issues]
Type: [CAPITALIZATION/ABBREVIATION/FORMATTING/PUNCTUATION]
  Description: [description]
  Examples: [example1], [example2]
  Recommendation: [recommendation]

[...more issues...]

DEFINITION CONFLICTS:
----------------------------------------
Status: [PASS/FAIL]
Conflicts Found: [N]

[If conflicts]
Term: [term]
  Definition 1 (Slide [N]): [definition]
  Definition 2 (Slide [N]): [definition]
  Severity: [ERROR/WARNING]

[...more conflicts...]

CROSS-SECTION CONSISTENCY:
----------------------------------------
Status: [PASS/FAIL/N/A]
[If applicable, list cross-section issues]

SUMMARY:
----------------------------------------
Total Issues: [N]
  Errors: [N]
  Warnings: [N]

RECOMMENDATIONS:
----------------------------------------
[List of recommendations]

ACTION REQUIRED:
----------------------------------------
[If FAIL]
Resolve consistency issues before proceeding.
Priority: Definition conflicts > Terminology > Style

[If PASS]
Consistency standards met. Proceed to next check.
```

---

## Common Theater Terminology Reference

### Preferred Terms
| Instead Of | Use |
|------------|-----|
| blocking | stage directions |
| lines | dialogue |
| props | properties |
| stage left | actor's left |
| stage right | actor's right |

### Standard Abbreviations
| Abbreviation | Meaning | First Use |
|--------------|---------|-----------|
| SL | Stage Left | Spell out first |
| SR | Stage Right | Spell out first |
| CS | Center Stage | Spell out first |
| US | Upstage | Spell out first |
| DS | Downstage | Spell out first |
| SM | Stage Manager | Spell out first |
| AD | Assistant Director | Spell out first |
| ASM | Assistant Stage Manager | Spell out first |

---

## Integration Points

| Upstream | Downstream |
|----------|------------|
| pedagogy_checker | error_reporter |
| blueprint_generator | score_calculator |
| content_sorter | final_validator |

---

**Agent Version:** 2.0 (Theater Adaptation)
**Last Updated:** 2026-01-08

### Version History
- **v2.0** (2026-01-08): Theater adaptation - renamed NCLEX references to theater terms
- **v1.0** (2026-01-04): Initial consistency checker agent
