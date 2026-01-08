# Constraint Validator Agent

## Agent Identity
- **Name:** constraint_validator
- **Step:** 8 (Quality Assurance - Constraint Validation)
- **Purpose:** Validate blueprint content against domain-specific constraints including character limits, formatting rules, and content requirements

---

## Input Schema
```json
{
  "blueprint": "string (Step 7 revised blueprint content)",
  "domain_config": "reference to config/theater.yaml",
  "section_name": "string (current section)",
  "validation_mode": "string (strict/lenient)"
}
```

## Output Schema
```json
{
  "validation_result": "PASS/FAIL/WARN",
  "violations": "array of violation objects",
  "warnings": "array of warning objects",
  "statistics": {
    "slides_checked": "number",
    "violations_found": "number",
    "warnings_found": "number",
    "pass_rate": "number (percentage)"
  },
  "recommendations": "array of fix suggestions"
}
```

---

## Required Skills (Hardcoded)

1. **Character Limit Checking** - Validate text against per-element limits
2. **Format Compliance** - Verify blueprint structure matches spec
3. **Content Rules** - Check theater-specific content requirements
4. **Constraint Configuration** - Load and apply domain-specific constraints
5. **Violation Reporting** - Generate actionable violation reports

---

## Constraint Categories

### Category 1: Character Limits

**Reference:** `config/constraints.yaml` (canonical source)

```yaml
character_limits:
  # R1: Header constraints
  slide_header:
    chars_per_line: 32      # From config/constraints.yaml
    max_lines: 2
    total_max_chars: 64     # 32 * 2
    severity: ERROR

  # R2/R3: Body constraints
  slide_body:
    chars_per_line: 66      # From config/constraints.yaml
    max_lines: 8            # From config/constraints.yaml
    severity: ERROR

  # R4: Performance tip constraints
  performance_tip:
    chars_per_line: 66      # From config/constraints.yaml
    max_lines: 2
    total_max_chars: 132    # CANONICAL VALUE
    severity: WARN

  # Presenter notes constraints (15-minute verbatim scripts)
  presenter_notes:
    min_words: 1950         # ~14 minutes at 140 WPM
    max_words: 2250         # ~16 minutes at 140 WPM
    target_words: 2100      # ~15 minutes at 140 WPM
    max_duration_seconds: 960  # 16 minutes max
    severity: ERROR

  visual_elements:
    table_cell: 60
    decision_node_header: 20
    decision_node_body: 50
    flowchart_step_header: 20
    flowchart_step_body: 50
    timeline_event: 30
    hierarchy_node: 25
```

### Category 2: Structural Requirements

```yaml
structural_requirements:
  required_sections:
    - HEADER
    - BODY
    - PERFORMANCE TIP  # Can be "None"
    - PRESENTER NOTES

  slide_types:
    valid:
      - Section Intro
      - Content
      - Visual
      - Activity
      - Summary

  visual_marker:
    required: true
    format: "Visual: Yes - [TYPE]" or "Visual: No"
    valid_types:
      - TABLE
      - FLOWCHART
      - DECISION_TREE
      - TIMELINE
      - HIERARCHY
      - SPECTRUM
      - KEY_DIFFERENTIATORS
```

### Category 3: Content Rules

```yaml
content_rules:
  performance_tip:
    must_be_actionable: true
    keywords:
      - PERFORMANCE TIP
      - stage
      - blocking
      - character
      - rehearsal
      - technique

  presenter_notes:
    must_include_monologue: true
    must_be_verbatim: true    # Full script, not bullet points
    should_expand_bullets: true
    min_sentences: 10         # Complete 15-minute script
    required_markers:
      - "[PAUSE]"             # At least 2 per slide
      - "[EMPHASIS]"          # At least 1 for content slides

  activity_slides:
    must_have_instructions: true
    must_have_duration: true
    must_have_setup: true
```

### Category 4: Theater-Specific Requirements

```yaml
theater_requirements:
  content_accuracy:
    check_theater_terminology: true
    check_historical_accuracy: true
    check_technique_names: true

  lesson_format:
    56_minute_structure: true
    components:
      - agenda (5 min)
      - warmup (5 min)
      - lecture (15 min)
      - activity (15 min)
      - reflection (10 min)
      - buffer (6 min)

  content_coverage:
    must_tag_unit: true
    valid_units:
      - Unit 1: Greek Theater
      - Unit 2: Commedia dell'Arte
      - Unit 3: Shakespeare
      - Unit 4: Student-Directed One Acts
```

---

## Step-by-Step Instructions

### Step 1: Load Constraints
```python
def load_constraints(domain_config_path):
    """Load domain-specific constraints."""

    with open(domain_config_path, 'r') as f:
        config = yaml.safe_load(f)

    constraints = {
        'character_limits': config.get('character_limits', {}),
        'structural_requirements': config.get('structural_requirements', {}),
        'content_rules': config.get('content_rules', {}),
        'theater_requirements': config.get('theater_requirements', {})
    }

    return constraints
```

### Step 2: Parse Blueprint for Validation
```python
def parse_blueprint_for_validation(blueprint_content):
    """Parse blueprint into validatable components."""

    slides = []
    slide_pattern = r'={40,}\s*SLIDE\s+(\d+[AB]?):\s*(.+?)\s*={40,}'
    slide_blocks = re.split(slide_pattern, blueprint_content)

    i = 1
    while i < len(slide_blocks) - 2:
        slide_num = slide_blocks[i].strip()
        slide_title = slide_blocks[i + 1].strip()
        slide_content = slide_blocks[i + 2]

        slides.append({
            'number': slide_num,
            'title': slide_title,
            'header': extract_section(slide_content, 'HEADER'),
            'body': extract_section(slide_content, 'BODY'),
            'tip': extract_section(slide_content, 'PERFORMANCE TIP'),
            'notes': extract_section(slide_content, 'PRESENTER NOTES'),
            'type': extract_field(slide_content, 'Type'),
            'visual_marker': extract_field(slide_content, 'Visual'),
            'raw_content': slide_content
        })

        i += 3

    return slides
```

### Step 3: Validate Character Limits
```python
def validate_character_limits(slides, limits):
    """
    Check all text elements against character limits.

    CANONICAL VALUES from config/constraints.yaml:
    - Header: 32 chars/line, 2 lines max (64 total)
    - Body: 66 chars/line, 8 lines max
    - Performance Tip: 66 chars/line, 2 lines max (132 total)
    - Presenter Notes: 1,950-2,250 words (15-min verbatim script)
    """

    violations = []
    warnings = []

    for slide in slides:
        slide_num = slide['number']

        # R1: Header limit (32 chars/line, 2 lines max)
        if slide['header']:
            header_lines = slide['header'].split('\n')
            chars_per_line = limits.get('slide_header', {}).get('chars_per_line', 32)
            max_lines = limits.get('slide_header', {}).get('max_lines', 2)

            if len(header_lines) > max_lines:
                violations.append({
                    'slide': slide_num,
                    'element': 'HEADER',
                    'type': 'LINE_LIMIT',
                    'severity': 'ERROR',
                    'message': f"Header exceeds {max_lines} lines ({len(header_lines)} lines)"
                })

            for i, line in enumerate(header_lines):
                if len(line) > chars_per_line:
                    violations.append({
                        'slide': slide_num,
                        'element': 'HEADER',
                        'type': 'CHARACTER_LIMIT',
                        'severity': 'ERROR',
                        'message': f"Header line {i+1} exceeds {chars_per_line} chars ({len(line)} chars)",
                        'current': len(line),
                        'limit': chars_per_line
                    })

        # R2/R3: Body limit (66 chars/line, 8 lines max)
        if slide['body']:
            body_lines = [l for l in slide['body'].split('\n') if l.strip()]  # Non-empty lines
            chars_per_line = limits.get('slide_body', {}).get('chars_per_line', 66)
            max_lines = limits.get('slide_body', {}).get('max_lines', 8)

            # R2: Line count (8 non-empty lines max)
            if len(body_lines) > max_lines:
                violations.append({
                    'slide': slide_num,
                    'element': 'BODY',
                    'type': 'LINE_LIMIT',
                    'severity': 'ERROR',
                    'message': f"Body exceeds {max_lines} lines ({len(body_lines)} lines)"
                })

            # R3: Character count per line (66 chars max)
            for i, line in enumerate(body_lines):
                if len(line) > chars_per_line:
                    violations.append({
                        'slide': slide_num,
                        'element': 'BODY',
                        'type': 'CHARACTER_LIMIT',
                        'severity': 'ERROR',
                        'message': f"Body line {i+1} exceeds {chars_per_line} chars ({len(line)} chars)",
                        'current': len(line),
                        'limit': chars_per_line
                    })

        # R4: Performance tip limit (132 chars total)
        if slide['tip'] and slide['tip'].lower() not in ['none', 'n/a']:
            tip_len = len(slide['tip'])
            tip_limit = limits.get('performance_tip', {}).get('total_max_chars', 132)
            if tip_len > tip_limit:
                warnings.append({
                    'slide': slide_num,
                    'element': 'PERFORMANCE TIP',
                    'type': 'CHARACTER_LIMIT',
                    'severity': 'WARN',
                    'message': f"Tip exceeds {tip_limit} chars ({tip_len} chars)"
                })

        # Presenter notes limits (15-minute verbatim script: 1,950-2,250 words)
        if slide['notes']:
            words = len(slide['notes'].split())
            min_words = limits.get('presenter_notes', {}).get('min_words', 1950)
            max_words = limits.get('presenter_notes', {}).get('max_words', 2250)

            if words < min_words:
                warnings.append({
                    'slide': slide_num,
                    'element': 'PRESENTER NOTES',
                    'type': 'WORD_COUNT',
                    'severity': 'WARN',
                    'message': f"Notes under minimum ({words} words, min {min_words})"
                })
            elif words > max_words:
                warnings.append({
                    'slide': slide_num,
                    'element': 'PRESENTER NOTES',
                    'type': 'WORD_COUNT',
                    'severity': 'WARN',
                    'message': f"Notes over maximum ({words} words, max {max_words})"
                })

    return violations, warnings
```

### Step 4: Validate Structure
```python
def validate_structure(slides, requirements):
    """Check blueprint structure against requirements."""

    violations = []

    required_sections = requirements.get('required_sections', [])
    valid_types = requirements.get('slide_types', {}).get('valid', [])

    for slide in slides:
        slide_num = slide['number']

        # Check required sections
        for section in required_sections:
            section_key = section.lower().replace(' ', '_').replace('performance_tip', 'tip')
            if section_key == 'performance_tip':
                section_key = 'tip'

            if not slide.get(section_key):
                violations.append({
                    'slide': slide_num,
                    'element': section,
                    'type': 'MISSING_SECTION',
                    'severity': 'ERROR',
                    'message': f"Missing required section: {section}"
                })

        # Check slide type
        if slide.get('type') and slide['type'] not in valid_types:
            violations.append({
                'slide': slide_num,
                'element': 'Type',
                'type': 'INVALID_TYPE',
                'severity': 'ERROR',
                'message': f"Invalid slide type: {slide['type']}"
            })

        # Check visual marker
        visual_marker = slide.get('visual_marker', '')
        if not visual_marker:
            violations.append({
                'slide': slide_num,
                'element': 'Visual',
                'type': 'MISSING_MARKER',
                'severity': 'ERROR',
                'message': "Missing Visual: Yes/No marker"
            })
        elif not (visual_marker.startswith('Yes') or visual_marker.lower() == 'no'):
            violations.append({
                'slide': slide_num,
                'element': 'Visual',
                'type': 'INVALID_MARKER',
                'severity': 'ERROR',
                'message': f"Invalid visual marker format: {visual_marker}"
            })

    return violations
```

### Step 5: Validate Content Rules
```python
def validate_content_rules(slides, rules):
    """Check content against domain-specific rules."""

    violations = []
    warnings = []

    tip_rules = rules.get('performance_tip', {})
    notes_rules = rules.get('presenter_notes', {})
    activity_rules = rules.get('activity_slides', {})

    for slide in slides:
        slide_num = slide['number']
        slide_type = slide.get('type', 'Content')

        # Performance tip validation
        if slide['tip'] and slide['tip'].lower() not in ['none', 'n/a']:
            if tip_rules.get('must_be_actionable'):
                keywords = tip_rules.get('keywords', ['PERFORMANCE TIP'])
                if not any(kw.lower() in slide['tip'].lower() for kw in keywords):
                    warnings.append({
                        'slide': slide_num,
                        'element': 'PERFORMANCE TIP',
                        'type': 'CONTENT_RULE',
                        'severity': 'WARN',
                        'message': "Tip should include actionable theater guidance"
                    })

        # Presenter notes validation (15-minute verbatim script)
        if slide['notes']:
            if notes_rules.get('min_sentences'):
                sentences = len(re.findall(r'[.!?]+', slide['notes']))
                min_sent = notes_rules['min_sentences']
                if sentences < min_sent:
                    warnings.append({
                        'slide': slide_num,
                        'element': 'PRESENTER NOTES',
                        'type': 'CONTENT_RULE',
                        'severity': 'WARN',
                        'message': f"Notes have only {sentences} sentences (min {min_sent})"
                    })

            # Check for required markers
            required_markers = notes_rules.get('required_markers', ['[PAUSE]', '[EMPHASIS]'])
            for marker in required_markers:
                if marker not in slide['notes']:
                    warnings.append({
                        'slide': slide_num,
                        'element': 'PRESENTER NOTES',
                        'type': 'MISSING_MARKER',
                        'severity': 'WARN',
                        'message': f"Notes missing required marker: {marker}"
                    })

        # Activity slide validation
        if slide_type == 'Activity':
            body = slide.get('body', '')

            if activity_rules.get('must_have_instructions'):
                if 'instruction' not in body.lower() and 'step' not in body.lower():
                    violations.append({
                        'slide': slide_num,
                        'element': 'BODY',
                        'type': 'CONTENT_RULE',
                        'severity': 'ERROR',
                        'message': "Activity slide must contain instructions"
                    })

            if activity_rules.get('must_have_duration'):
                if 'minute' not in body.lower() and 'min' not in body.lower():
                    warnings.append({
                        'slide': slide_num,
                        'element': 'BODY',
                        'type': 'CONTENT_RULE',
                        'severity': 'WARN',
                        'message': "Activity slide should specify duration"
                    })

    return violations, warnings
```

### Step 6: Generate Validation Report
```python
def generate_validation_report(slides, violations, warnings):
    """Generate comprehensive validation report."""

    total_slides = len(slides)
    total_violations = len(violations)
    total_warnings = len(warnings)

    # Calculate pass rate (slides without errors)
    slides_with_errors = len(set(v['slide'] for v in violations))
    pass_rate = ((total_slides - slides_with_errors) / total_slides * 100) if total_slides > 0 else 0

    # Determine overall result
    if total_violations == 0 and total_warnings == 0:
        result = 'PASS'
    elif total_violations == 0:
        result = 'WARN'
    else:
        result = 'FAIL'

    # Generate recommendations
    recommendations = generate_recommendations(violations, warnings)

    return {
        'validation_result': result,
        'violations': violations,
        'warnings': warnings,
        'statistics': {
            'slides_checked': total_slides,
            'violations_found': total_violations,
            'warnings_found': total_warnings,
            'pass_rate': round(pass_rate, 1)
        },
        'recommendations': recommendations
    }

def generate_recommendations(violations, warnings):
    """Generate actionable recommendations from violations."""

    recommendations = []

    # Group by type
    by_type = {}
    for v in violations + warnings:
        v_type = v['type']
        if v_type not in by_type:
            by_type[v_type] = []
        by_type[v_type].append(v)

    for v_type, items in by_type.items():
        if v_type == 'CHARACTER_LIMIT':
            recommendations.append({
                'type': 'CHARACTER_LIMIT',
                'count': len(items),
                'action': 'Reduce text length in affected elements',
                'affected_slides': list(set(i['slide'] for i in items))
            })
        elif v_type == 'MISSING_SECTION':
            recommendations.append({
                'type': 'MISSING_SECTION',
                'count': len(items),
                'action': 'Add missing sections to blueprint',
                'affected_slides': list(set(i['slide'] for i in items))
            })
        elif v_type == 'CONTENT_RULE':
            recommendations.append({
                'type': 'CONTENT_RULE',
                'count': len(items),
                'action': 'Review content for theater domain compliance',
                'affected_slides': list(set(i['slide'] for i in items))
            })

    return recommendations
```

---

## Output Format

### Validation Report
```
===== CONSTRAINT VALIDATION REPORT =====
Section: [Section Name]
Date: [YYYY-MM-DD HH:MM:SS]

RESULT: [PASS/WARN/FAIL]

STATISTICS:
- Slides Checked: [X]
- Violations Found: [Y]
- Warnings Found: [Z]
- Pass Rate: [N]%

VIOLATIONS (Errors):
-----------------------------------------
Slide [N]: [Element] - [Type]
  Message: [Description]
  Current: [Value], Limit: [Value]

WARNINGS:
-----------------------------------------
Slide [N]: [Element] - [Type]
  Message: [Description]

RECOMMENDATIONS:
-----------------------------------------
1. [Action] - Affects slides: [list]
2. [Action] - Affects slides: [list]

STATUS: [READY FOR STEP 9 / NEEDS REVISION]
```

---

## Validation Modes

### Strict Mode
- All violations cause FAIL
- All warnings reported
- Used for final validation

### Lenient Mode
- Only critical violations cause FAIL
- Minor warnings suppressed
- Used during development/iteration

---

## Error Handling

| Error | Action |
|-------|--------|
| Blueprint parse error | HALT, return parse error |
| Config file not found | Use defaults, log warning |
| Invalid constraint value | Skip constraint, log warning |
| Empty blueprint | Return FAIL with "empty content" |

---

## Canonical Constraint Reference

All constraint values MUST align with `config/constraints.yaml`:

| Element | Constraint | Value | Source |
|---------|------------|-------|--------|
| Header | chars_per_line | 32 | config/constraints.yaml |
| Header | max_lines | 2 | config/constraints.yaml |
| Body | chars_per_line | 66 | config/constraints.yaml |
| Body | max_lines | 8 | config/constraints.yaml |
| Performance Tip | total_max_chars | **132** | config/constraints.yaml |
| Performance Tip | max_lines | 2 | config/constraints.yaml |
| Presenter Notes | min_words | **1,950** | config/constraints.yaml |
| Presenter Notes | max_words | **2,250** | config/constraints.yaml |
| Presenter Notes | target_words | **2,100** | config/constraints.yaml |
| Visual | max_percentage | 40% | config/constraints.yaml |

---

**Agent Version:** 2.0 (Theater Adaptation)
**Last Updated:** 2026-01-08

### Version History
- **v2.0** (2026-01-08): Adapted for theater pipeline - replaced NCLEX with performance tips, updated presenter notes for 15-min verbatim scripts
- **v1.1** (2026-01-06): Fixed constraint conflicts - tip limit 120→132, presenter notes 300→450 words
- **v1.0** (2026-01-04): Initial constraint validator agent
