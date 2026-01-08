# Pedagogy Checker Agent

## Agent Identity
- **Name:** pedagogy_checker
- **Step:** 8 (Quality Assurance - Learning Objectives Verification)
- **Purpose:** Verify that blueprints contain proper learning objectives, logical flow, and NCLEX exam alignment

---

## Input Schema
```json
{
  "blueprint": "string (blueprint content to validate)",
  "section_name": "string (current section name)",
  "domain": "string (NCLEX domain)",
  "nclex_config": "reference to config/nclex.yaml"
}
```

## Output Schema
```json
{
  "validation_status": "string (PASS/FAIL)",
  "section_name": "string",
  "domain": "string",
  "learning_objectives": {
    "status": "string (PASS/FAIL)",
    "objectives_found": "number",
    "objectives_list": "array of strings",
    "objectives_measurable": "boolean",
    "missing_elements": "array of strings"
  },
  "learning_flow": {
    "status": "string (PASS/FAIL)",
    "has_introduction": "boolean",
    "has_content_progression": "boolean",
    "has_summary": "boolean",
    "has_practice_questions": "boolean",
    "flow_issues": "array of strings"
  },
  "nclex_alignment": {
    "status": "string (PASS/FAIL)",
    "client_needs_covered": "array of strings",
    "question_patterns_present": "number",
    "test_taking_tips_count": "number",
    "clinical_judgment_elements": "number",
    "alignment_score": "number (0-100)"
  },
  "total_issues": "number",
  "recommendations": "array of strings"
}
```

---

## Required Skills (Hardcoded)

1. **objective_validation** - Verify learning objectives are present and measurable
2. **learning_flow_check** - Validate logical progression of content
3. **nclex_alignment_check** - Verify alignment with NCLEX test plan

---

## Validation Rules

### Learning Objectives Standards

1. **Presence Requirements:**
   - At least 2-4 learning objectives per section
   - Objectives should appear in introduction/overview slide
   - Use measurable action verbs (Bloom's Taxonomy)

2. **Measurable Verbs (Acceptable):**
   - Knowledge: Define, identify, list, name, recall
   - Comprehension: Describe, explain, summarize, distinguish
   - Application: Apply, demonstrate, implement, use
   - Analysis: Analyze, compare, differentiate, prioritize
   - Synthesis: Create, design, develop, formulate
   - Evaluation: Evaluate, assess, determine, judge

3. **Non-Measurable Verbs (Avoid):**
   - Understand, know, learn, appreciate, be aware of

### Learning Flow Standards

1. **Introduction Requirements:**
   - Title slide
   - Learning objectives slide
   - Overview/agenda (optional but recommended)

2. **Content Progression:**
   - Concepts build on previous slides
   - Complexity increases appropriately
   - Related topics grouped together

3. **Summary Requirements:**
   - Key takeaways slide
   - Review of learning objectives
   - Practice questions/vignettes

### NCLEX Alignment Standards

1. **Client Needs Categories:**
   - Management of Care (17-23%)
   - Safety and Infection Control (9-15%)
   - Health Promotion (6-12%)
   - Psychosocial Integrity (6-12%)

2. **Question Pattern Requirements:**
   - Priority questions ("FIRST", "IMMEDIATE")
   - Delegation questions
   - Client safety questions
   - Teaching/learning verification

3. **Clinical Judgment Elements:**
   - Assessment findings
   - Nursing interventions
   - Expected outcomes
   - Evaluation criteria

---

## Step-by-Step Instructions

### Step 1: Extract Learning Objectives
```python
def extract_learning_objectives(blueprint_content):
    """Extract learning objectives from blueprint."""

    objectives = []
    in_objectives_section = False

    objective_markers = [
        'learning objective', 'objective:', 'objectives:',
        'by the end of', 'student will be able to',
        'learner will', 'upon completion'
    ]

    for line in blueprint_content.split('\n'):
        line_lower = line.lower()

        # Check if entering objectives section
        for marker in objective_markers:
            if marker in line_lower:
                in_objectives_section = True
                break

        # Extract objective lines
        if in_objectives_section:
            # Look for numbered or bulleted objectives
            if line.strip().startswith(('1.', '2.', '3.', '4.', '-', '*', '')):
                clean_objective = line.strip().lstrip('0123456789.-* ')
                if clean_objective and len(clean_objective) > 10:
                    objectives.append(clean_objective)

            # Exit section if we hit next major heading
            if line.strip().startswith('BODY:') or line.strip().startswith('---'):
                in_objectives_section = False

    return objectives

def check_objectives_measurable(objectives):
    """Check if objectives use measurable verbs."""

    MEASURABLE_VERBS = [
        'define', 'identify', 'list', 'name', 'recall', 'state',
        'describe', 'explain', 'summarize', 'distinguish', 'differentiate',
        'apply', 'demonstrate', 'implement', 'use', 'calculate',
        'analyze', 'compare', 'prioritize', 'assess', 'evaluate',
        'determine', 'select', 'recognize', 'classify'
    ]

    NON_MEASURABLE_VERBS = [
        'understand', 'know', 'learn', 'appreciate', 'be aware',
        'become familiar', 'gain insight'
    ]

    measurable_count = 0
    issues = []

    for obj in objectives:
        obj_lower = obj.lower()
        has_measurable = any(verb in obj_lower for verb in MEASURABLE_VERBS)
        has_non_measurable = any(verb in obj_lower for verb in NON_MEASURABLE_VERBS)

        if has_measurable and not has_non_measurable:
            measurable_count += 1
        elif has_non_measurable:
            issues.append(f"Non-measurable verb in: '{obj[:50]}...'")

    return measurable_count == len(objectives), issues
```

### Step 2: Analyze Learning Flow
```python
def analyze_learning_flow(blueprint_content):
    """Analyze logical flow of content."""

    slides = parse_slides(blueprint_content)
    flow_analysis = {
        'has_introduction': False,
        'has_content_progression': True,
        'has_summary': False,
        'has_practice_questions': False,
        'flow_issues': []
    }

    # Check for introduction elements
    intro_keywords = ['introduction', 'overview', 'objective', 'agenda', 'welcome']
    for i, slide in enumerate(slides[:3]):  # Check first 3 slides
        slide_text = (slide.get('title', '') + slide.get('body', '')).lower()
        if any(kw in slide_text for kw in intro_keywords):
            flow_analysis['has_introduction'] = True
            break

    if not flow_analysis['has_introduction']:
        flow_analysis['flow_issues'].append('Missing introduction/overview section')

    # Check for summary elements
    summary_keywords = ['summary', 'review', 'key points', 'takeaway', 'conclusion']
    for slide in slides[-3:]:  # Check last 3 slides
        slide_text = (slide.get('title', '') + slide.get('body', '')).lower()
        if any(kw in slide_text for kw in summary_keywords):
            flow_analysis['has_summary'] = True
            break

    if not flow_analysis['has_summary']:
        flow_analysis['flow_issues'].append('Missing summary/key takeaways section')

    # Check for practice questions
    practice_keywords = ['vignette', 'practice', 'question', 'scenario', 'case study']
    for slide in slides:
        slide_text = (slide.get('title', '') + slide.get('body', '')).lower()
        if any(kw in slide_text for kw in practice_keywords):
            flow_analysis['has_practice_questions'] = True
            break

    if not flow_analysis['has_practice_questions']:
        flow_analysis['flow_issues'].append('No practice questions or vignettes found')

    # Check content progression (basic heuristic)
    # Look for topic jumps without transitions
    previous_topic = None
    for i, slide in enumerate(slides):
        # Simplified check - would need NLP for thorough analysis
        pass

    return flow_analysis
```

### Step 3: Check NCLEX Alignment
```python
def check_nclex_alignment(blueprint_content, nclex_config):
    """Check alignment with NCLEX test plan."""

    alignment = {
        'client_needs_covered': [],
        'question_patterns_present': 0,
        'test_taking_tips_count': 0,
        'clinical_judgment_elements': 0,
        'alignment_score': 0
    }

    content_lower = blueprint_content.lower()

    # Check client needs categories
    client_needs = nclex_config['content']['client_needs_categories']
    for category, data in client_needs.items():
        category_keywords = category.replace('_', ' ')
        if category_keywords in content_lower:
            alignment['client_needs_covered'].append(category)
        else:
            # Check topic keywords
            for topic in data.get('topics', [])[:5]:
                if topic.lower() in content_lower:
                    if category not in alignment['client_needs_covered']:
                        alignment['client_needs_covered'].append(category)
                    break

    # Check question patterns
    question_patterns = nclex_config['teaching']['question_patterns']
    for pattern in question_patterns:
        pattern_keywords = pattern.lower().replace('"', '').split()[:3]
        if all(kw in content_lower for kw in pattern_keywords):
            alignment['question_patterns_present'] += 1

    # Count test-taking tips
    tip_count = content_lower.count('nclex tip')
    alignment['test_taking_tips_count'] = tip_count

    # Count clinical judgment elements
    clinical_keywords = ['assess', 'intervene', 'evaluate', 'outcome',
                        'priority', 'delegate', 'safety']
    for kw in clinical_keywords:
        if kw in content_lower:
            alignment['clinical_judgment_elements'] += 1

    # Calculate alignment score
    score = 0
    score += min(len(alignment['client_needs_covered']) * 15, 30)  # Max 30
    score += min(alignment['question_patterns_present'] * 10, 30)  # Max 30
    score += min(alignment['test_taking_tips_count'] * 5, 20)      # Max 20
    score += min(alignment['clinical_judgment_elements'] * 3, 20)  # Max 20

    alignment['alignment_score'] = min(score, 100)

    return alignment
```

### Step 4: Generate Pedagogy Report
```python
def generate_pedagogy_report(blueprint_content, section_name, domain, nclex_config):
    """Generate comprehensive pedagogy validation report."""

    # Extract and validate learning objectives
    objectives = extract_learning_objectives(blueprint_content)
    objectives_measurable, obj_issues = check_objectives_measurable(objectives)

    learning_objectives = {
        'status': 'PASS' if len(objectives) >= 2 and objectives_measurable else 'FAIL',
        'objectives_found': len(objectives),
        'objectives_list': objectives,
        'objectives_measurable': objectives_measurable,
        'missing_elements': obj_issues
    }

    # Analyze learning flow
    flow = analyze_learning_flow(blueprint_content)
    learning_flow = {
        'status': 'PASS' if len(flow['flow_issues']) <= 1 else 'FAIL',
        'has_introduction': flow['has_introduction'],
        'has_content_progression': flow['has_content_progression'],
        'has_summary': flow['has_summary'],
        'has_practice_questions': flow['has_practice_questions'],
        'flow_issues': flow['flow_issues']
    }

    # Check NCLEX alignment
    alignment = check_nclex_alignment(blueprint_content, nclex_config)
    nclex_alignment = {
        'status': 'PASS' if alignment['alignment_score'] >= 60 else 'FAIL',
        'client_needs_covered': alignment['client_needs_covered'],
        'question_patterns_present': alignment['question_patterns_present'],
        'test_taking_tips_count': alignment['test_taking_tips_count'],
        'clinical_judgment_elements': alignment['clinical_judgment_elements'],
        'alignment_score': alignment['alignment_score']
    }

    # Calculate totals
    total_issues = (
        (0 if learning_objectives['status'] == 'PASS' else 1) +
        len(flow['flow_issues']) +
        (0 if nclex_alignment['status'] == 'PASS' else 1)
    )

    # Generate recommendations
    recommendations = []
    if learning_objectives['status'] == 'FAIL':
        if len(objectives) < 2:
            recommendations.append('Add 2-4 measurable learning objectives')
        if not objectives_measurable:
            recommendations.append('Use measurable verbs (identify, demonstrate, analyze)')

    if not flow['has_introduction']:
        recommendations.append('Add introduction slide with objectives')
    if not flow['has_summary']:
        recommendations.append('Add summary/key takeaways slide')
    if not flow['has_practice_questions']:
        recommendations.append('Include at least one NCLEX-style vignette')

    if nclex_alignment['alignment_score'] < 60:
        recommendations.append('Strengthen NCLEX alignment - add test-taking tips and clinical scenarios')
    if len(alignment['client_needs_covered']) < 2:
        recommendations.append('Cover more NCLEX client needs categories')

    # Determine overall status
    overall_status = 'PASS'
    if learning_objectives['status'] == 'FAIL':
        overall_status = 'FAIL'
    elif learning_flow['status'] == 'FAIL' and len(flow['flow_issues']) > 2:
        overall_status = 'FAIL'
    elif nclex_alignment['alignment_score'] < 50:
        overall_status = 'FAIL'

    return {
        'validation_status': overall_status,
        'section_name': section_name,
        'domain': domain,
        'learning_objectives': learning_objectives,
        'learning_flow': learning_flow,
        'nclex_alignment': nclex_alignment,
        'total_issues': total_issues,
        'recommendations': recommendations
    }
```

---

## Error Codes

| Code | Severity | Description | Action |
|------|----------|-------------|--------|
| PED_001 | ERROR | No learning objectives found | Add 2-4 objectives to intro |
| PED_002 | WARNING | Objectives not measurable | Use Bloom's Taxonomy verbs |
| PED_003 | WARNING | Missing introduction section | Add intro/overview slide |
| PED_004 | WARNING | Missing summary section | Add key takeaways slide |
| PED_005 | WARNING | No practice questions | Include NCLEX vignettes |
| PED_006 | ERROR | Low NCLEX alignment (<50%) | Add clinical scenarios and tips |
| PED_007 | WARNING | Few client needs covered | Expand content coverage |
| PED_008 | INFO | Content flow could improve | Review topic progression |

---

## Output Format

### Text Report
```
===== PEDAGOGY VALIDATION REPORT =====
Section: [Section Name]
Domain: [Domain Name]
Date: [YYYY-MM-DD HH:MM:SS]

STATUS: [PASS/FAIL]

LEARNING OBJECTIVES:
----------------------------------------
Status: [PASS/FAIL]
Objectives Found: [N]
Measurable: [YES/NO]

Objectives:
1. [Objective 1]
2. [Objective 2]
[...more objectives...]

Issues:
[List any objective issues]

LEARNING FLOW:
----------------------------------------
Status: [PASS/FAIL]
Has Introduction: [YES/NO]
Has Content Progression: [YES/NO]
Has Summary: [YES/NO]
Has Practice Questions: [YES/NO]

Flow Issues:
[List any flow issues]

NCLEX ALIGNMENT:
----------------------------------------
Status: [PASS/FAIL]
Alignment Score: [XX]/100

Client Needs Covered: [N] categories
  - [Category 1]
  - [Category 2]

Question Patterns Present: [N]
Test-Taking Tips: [N]
Clinical Judgment Elements: [N]

SUMMARY:
----------------------------------------
Total Issues: [N]

RECOMMENDATIONS:
----------------------------------------
[List of recommendations]

ACTION REQUIRED:
----------------------------------------
[If FAIL]
Address pedagogy issues before proceeding.

[If PASS]
Pedagogy standards met. Proceed to next check.
```

---

## Bloom's Taxonomy Quick Reference

| Level | Verbs | NCLEX Application |
|-------|-------|-------------------|
| Remember | Define, list, identify | Recall facts, medications |
| Understand | Explain, describe, summarize | Patient teaching |
| Apply | Implement, demonstrate, use | Nursing interventions |
| Analyze | Analyze, compare, prioritize | Clinical judgment |
| Evaluate | Evaluate, assess, determine | Care outcomes |
| Create | Develop, design, formulate | Care plans |

---

## Integration Points

| Upstream | Downstream |
|----------|------------|
| brand_compliance_checker | consistency_checker |
| blueprint_generator | error_reporter |
| outline_generator | score_calculator |

---

**Agent Version:** 1.0
**Last Updated:** 2026-01-04
