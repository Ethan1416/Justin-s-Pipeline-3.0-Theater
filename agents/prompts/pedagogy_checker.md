# Pedagogy Checker Agent

## Agent Identity
- **Name:** pedagogy_checker
- **Step:** 8 (Quality Assurance - Learning Objectives Verification)
- **Purpose:** Verify that blueprints contain proper learning objectives, logical flow, and theater education standards alignment

---

## Input Schema
```json
{
  "blueprint": "string (blueprint content to validate)",
  "section_name": "string (current section name)",
  "unit": "string (theater unit: Greek Theater, Commedia dell'Arte, Shakespeare, One Acts)",
  "theater_config": "reference to config/theater.yaml"
}
```

## Output Schema
```json
{
  "validation_status": "string (PASS/FAIL)",
  "section_name": "string",
  "unit": "string",
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
    "has_practice_activities": "boolean",
    "flow_issues": "array of strings"
  },
  "standards_alignment": {
    "status": "string (PASS/FAIL)",
    "ca_ela_standards_covered": "array of strings",
    "theater_skills_present": "number",
    "performance_elements": "number",
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
3. **standards_alignment_check** - Verify alignment with CA ELA/Literacy standards

---

## Validation Rules

### Learning Objectives Standards

1. **Presence Requirements:**
   - At least 2-4 learning objectives per lesson
   - Objectives should appear in introduction/overview slide
   - Use measurable action verbs (Bloom's Taxonomy)

2. **Measurable Verbs (Acceptable):**
   - Knowledge: Define, identify, list, name, recall
   - Comprehension: Describe, explain, summarize, distinguish
   - Application: Apply, demonstrate, implement, perform
   - Analysis: Analyze, compare, differentiate, critique
   - Synthesis: Create, design, develop, compose, improvise
   - Evaluation: Evaluate, assess, determine, judge, defend

3. **Non-Measurable Verbs (Avoid):**
   - Understand, know, learn, appreciate, be aware of

4. **Theater-Specific Action Verbs:**
   - Perform, demonstrate, rehearse, block, characterize
   - Direct, improvise, interpret, project, articulate
   - Collaborate, critique, revise, reflect

### Learning Flow Standards

1. **Introduction Requirements:**
   - Title slide
   - Learning objectives slide
   - Overview/agenda (required for 56-minute structure)

2. **Content Progression:**
   - Concepts build on previous slides
   - Complexity increases appropriately
   - Related topics grouped together
   - Performance skills scaffolded

3. **56-Minute Structure:**
   - Agenda (5 min): Daily learning objectives
   - Warmup (5 min): Physical/vocal preparation
   - Lecture (15 min): Content delivery
   - Activity (15 min): Practical application
   - Reflection (10 min): Journal + exit ticket
   - Buffer (6 min): Transitions

### Standards Alignment Standards

1. **CA ELA/Literacy Standards (RL, SL, W.9-12):**
   - Reading Literature (RL.9-12.1-10)
   - Speaking and Listening (SL.9-12.1-6)
   - Writing (W.9-12.1-10)

2. **Theater Skills Categories:**
   - Acting techniques
   - Movement and blocking
   - Voice and diction
   - Character analysis
   - Script interpretation
   - Ensemble collaboration
   - Performance critique

3. **Performance Elements:**
   - Physical demonstration
   - Vocal exercises
   - Improvisation activities
   - Scene work
   - Reflection and journaling

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
        'learner will', 'upon completion', 'swbat'
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
        'apply', 'demonstrate', 'implement', 'use', 'perform',
        'analyze', 'compare', 'prioritize', 'assess', 'evaluate', 'critique',
        'determine', 'select', 'recognize', 'classify',
        # Theater-specific verbs
        'rehearse', 'block', 'characterize', 'direct', 'improvise',
        'interpret', 'project', 'articulate', 'collaborate', 'revise'
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
        'has_practice_activities': False,
        'flow_issues': []
    }

    # Check for introduction elements
    intro_keywords = ['introduction', 'overview', 'objective', 'agenda', 'welcome', 'today']
    for i, slide in enumerate(slides[:3]):  # Check first 3 slides
        slide_text = (slide.get('title', '') + slide.get('body', '')).lower()
        if any(kw in slide_text for kw in intro_keywords):
            flow_analysis['has_introduction'] = True
            break

    if not flow_analysis['has_introduction']:
        flow_analysis['flow_issues'].append('Missing introduction/overview section')

    # Check for summary elements
    summary_keywords = ['summary', 'review', 'key points', 'takeaway', 'conclusion', 'reflection']
    for slide in slides[-3:]:  # Check last 3 slides
        slide_text = (slide.get('title', '') + slide.get('body', '')).lower()
        if any(kw in slide_text for kw in summary_keywords):
            flow_analysis['has_summary'] = True
            break

    if not flow_analysis['has_summary']:
        flow_analysis['flow_issues'].append('Missing summary/key takeaways section')

    # Check for practice activities
    activity_keywords = ['activity', 'practice', 'exercise', 'rehearse', 'perform',
                        'improvise', 'scene', 'tableaux', 'blocking', 'partner work']
    for slide in slides:
        slide_text = (slide.get('title', '') + slide.get('body', '')).lower()
        if any(kw in slide_text for kw in activity_keywords):
            flow_analysis['has_practice_activities'] = True
            break

    if not flow_analysis['has_practice_activities']:
        flow_analysis['flow_issues'].append('No performance activities found')

    return flow_analysis
```

### Step 3: Check Standards Alignment
```python
def check_standards_alignment(blueprint_content, theater_config):
    """Check alignment with CA ELA/Literacy standards and theater skills."""

    alignment = {
        'ca_ela_standards_covered': [],
        'theater_skills_present': 0,
        'performance_elements': 0,
        'alignment_score': 0
    }

    content_lower = blueprint_content.lower()

    # Check CA ELA/Literacy standards coverage
    ela_standards = {
        'RL': ['analyze', 'cite evidence', 'determine theme', 'interpret', 'compare'],
        'SL': ['participate', 'collaborate', 'present', 'adapt speech', 'evaluate'],
        'W': ['write', 'reflect', 'argue', 'journal', 'respond']
    }

    for standard_type, keywords in ela_standards.items():
        for kw in keywords:
            if kw in content_lower:
                if standard_type not in alignment['ca_ela_standards_covered']:
                    alignment['ca_ela_standards_covered'].append(standard_type)
                break

    # Check theater skills
    theater_skills = [
        'acting', 'blocking', 'movement', 'voice', 'diction',
        'character', 'script', 'ensemble', 'critique', 'rehearsal',
        'stage', 'audience', 'performance', 'improvisation', 'scene'
    ]

    for skill in theater_skills:
        if skill in content_lower:
            alignment['theater_skills_present'] += 1

    # Count performance elements
    performance_keywords = ['demonstrate', 'perform', 'rehearse', 'practice',
                           'present', 'show', 'act', 'improvise', 'scene work']
    for kw in performance_keywords:
        if kw in content_lower:
            alignment['performance_elements'] += 1

    # Calculate alignment score
    score = 0
    score += min(len(alignment['ca_ela_standards_covered']) * 15, 30)  # Max 30
    score += min(alignment['theater_skills_present'] * 5, 40)          # Max 40
    score += min(alignment['performance_elements'] * 5, 30)            # Max 30

    alignment['alignment_score'] = min(score, 100)

    return alignment
```

### Step 4: Generate Pedagogy Report
```python
def generate_pedagogy_report(blueprint_content, section_name, unit, theater_config):
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
        'has_practice_activities': flow['has_practice_activities'],
        'flow_issues': flow['flow_issues']
    }

    # Check standards alignment
    alignment = check_standards_alignment(blueprint_content, theater_config)
    standards_alignment = {
        'status': 'PASS' if alignment['alignment_score'] >= 60 else 'FAIL',
        'ca_ela_standards_covered': alignment['ca_ela_standards_covered'],
        'theater_skills_present': alignment['theater_skills_present'],
        'performance_elements': alignment['performance_elements'],
        'alignment_score': alignment['alignment_score']
    }

    # Calculate totals
    total_issues = (
        (0 if learning_objectives['status'] == 'PASS' else 1) +
        len(flow['flow_issues']) +
        (0 if standards_alignment['status'] == 'PASS' else 1)
    )

    # Generate recommendations
    recommendations = []
    if learning_objectives['status'] == 'FAIL':
        if len(objectives) < 2:
            recommendations.append('Add 2-4 measurable learning objectives')
        if not objectives_measurable:
            recommendations.append('Use measurable verbs (identify, demonstrate, analyze, perform)')

    if not flow['has_introduction']:
        recommendations.append('Add introduction slide with objectives')
    if not flow['has_summary']:
        recommendations.append('Add summary/reflection slide')
    if not flow['has_practice_activities']:
        recommendations.append('Include at least one performance activity')

    if standards_alignment['alignment_score'] < 60:
        recommendations.append('Strengthen standards alignment - add ELA connections and theater skills')
    if len(alignment['ca_ela_standards_covered']) < 2:
        recommendations.append('Cover more CA ELA/Literacy standards (RL, SL, W)')

    # Determine overall status
    overall_status = 'PASS'
    if learning_objectives['status'] == 'FAIL':
        overall_status = 'FAIL'
    elif learning_flow['status'] == 'FAIL' and len(flow['flow_issues']) > 2:
        overall_status = 'FAIL'
    elif standards_alignment['alignment_score'] < 50:
        overall_status = 'FAIL'

    return {
        'validation_status': overall_status,
        'section_name': section_name,
        'unit': unit,
        'learning_objectives': learning_objectives,
        'learning_flow': learning_flow,
        'standards_alignment': standards_alignment,
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
| PED_005 | WARNING | No performance activities | Include theater exercises |
| PED_006 | ERROR | Low standards alignment (<50%) | Add ELA connections and skills |
| PED_007 | WARNING | Few ELA standards covered | Expand standard coverage |
| PED_008 | INFO | Content flow could improve | Review topic progression |

---

## Output Format

### Text Report
```
===== PEDAGOGY VALIDATION REPORT =====
Section: [Section Name]
Unit: [Unit Name]
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
Has Performance Activities: [YES/NO]

Flow Issues:
[List any flow issues]

STANDARDS ALIGNMENT:
----------------------------------------
Status: [PASS/FAIL]
Alignment Score: [XX]/100

CA ELA Standards Covered: [N] categories
  - [RL/SL/W standards]

Theater Skills Present: [N]
Performance Elements: [N]

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

| Level | Verbs | Theater Application |
|-------|-------|---------------------|
| Remember | Define, list, identify | Recall facts, terminology |
| Understand | Explain, describe, summarize | Interpret scenes, themes |
| Apply | Implement, demonstrate, perform | Execute blocking, voice |
| Analyze | Analyze, compare, critique | Script analysis, character |
| Evaluate | Evaluate, assess, determine | Performance critique |
| Create | Develop, design, compose, improvise | Original scenes, characters |

---

## Unit-Specific Standards Reference

### Unit 1: Greek Theater
- RL.9-12.7: Analyze representation of subject in different mediums
- SL.9-12.1: Collaborative discussions
- Historical theater conventions

### Unit 2: Commedia dell'Arte
- RL.9-12.6: Point of view and cultural context
- SL.9-12.4: Present information clearly
- Stock characters and improvisation

### Unit 3: Shakespeare
- RL.9-12.4: Meaning of words and phrases
- RL.9-12.5: Text structure
- Iambic pentameter, soliloquy

### Unit 4: Student-Directed One Acts
- W.9-12.3: Narrative writing
- SL.9-12.5: Strategic use of digital media
- Directing, production elements

---

## Integration Points

| Upstream | Downstream |
|----------|------------|
| brand_compliance_checker | consistency_checker |
| blueprint_generator | error_reporter |
| outline_generator | score_calculator |

---

**Agent Version:** 2.0 (Theater Adaptation)
**Last Updated:** 2026-01-08

### Version History
- **v2.0** (2026-01-08): Adapted for theater pipeline - replaced NCLEX with CA ELA/Literacy standards, theater skills, and performance elements
- **v1.0** (2026-01-04): Initial pedagogy checker agent
