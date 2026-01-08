# Score Calculator Agent

## Agent Identity
- **Name:** score_calculator
- **Step:** 8 (Quality Assurance - Score Calculation)
- **Purpose:** Calculate quality scores for blueprints based on weighted criteria across multiple dimensions

---

## Input Schema
```json
{
  "blueprint": "string (Step 7 revised blueprint content)",
  "validation_result": "object (from constraint_validator)",
  "domain_config": "reference to config/theater.yaml",
  "section_name": "string (current section)"
}
```

## Output Schema
```json
{
  "total_score": "number (0-100)",
  "category_scores": {
    "format_compliance": "number (0-25)",
    "content_quality": "number (0-25)",
    "standards_alignment": "number (0-25)",
    "presentation_readiness": "number (0-25)"
  },
  "score_breakdown": "array of detailed score items",
  "grade": "string (A/B/C/D/F)",
  "pass_threshold": "number",
  "passed": "boolean",
  "improvement_areas": "array of areas needing work"
}
```

---

## Required Skills (Hardcoded)

1. **Multi-Dimensional Scoring** - Score across format, content, alignment, readiness
2. **Weight Application** - Apply configurable weights to criteria
3. **Threshold Evaluation** - Compare scores against pass thresholds
4. **Grade Assignment** - Map scores to letter grades
5. **Improvement Identification** - Identify areas for score improvement

---

## Scoring Rubric

### Category 1: Format Compliance (25 points)

```yaml
format_compliance:
  max_points: 25
  criteria:
    character_limits:
      weight: 8
      scoring:
        all_pass: 8
        minor_violations: 5
        major_violations: 2
        severe_violations: 0

    structure_completeness:
      weight: 7
      scoring:
        all_sections_present: 7
        missing_optional: 5
        missing_required: 2
        severely_incomplete: 0

    visual_markers:
      weight: 5
      scoring:
        all_marked: 5
        some_missing: 3
        none_marked: 0

    naming_conventions:
      weight: 5
      scoring:
        fully_compliant: 5
        minor_deviations: 3
        non_compliant: 0
```

### Category 2: Content Quality (25 points)

```yaml
content_quality:
  max_points: 25
  criteria:
    clinical_accuracy:
      weight: 10
      scoring:
        verified_accurate: 10
        minor_concerns: 7
        errors_present: 3
        inaccurate: 0

    completeness:
      weight: 8
      scoring:
        comprehensive: 8
        adequate: 6
        gaps_present: 3
        incomplete: 0

    clarity:
      weight: 7
      scoring:
        crystal_clear: 7
        mostly_clear: 5
        some_confusion: 3
        unclear: 0
```

### Category 3: Standards Alignment (25 points)

```yaml
standards_alignment:
  max_points: 25
  criteria:
    ela_standards_coverage:
      weight: 8
      scoring:
        tagged_and_relevant: 8
        tagged_only: 5
        partially_tagged: 3
        not_tagged: 0

    performance_tips:
      weight: 7
      scoring:
        helpful_specific: 7
        helpful_general: 5
        present_not_helpful: 2
        missing: 0

    activity_quality:
      weight: 5
      scoring:
        engaging_relevant: 5
        acceptable: 3
        weak: 1
        none: 0

    critical_thinking:
      weight: 5
      scoring:
        promotes_analysis: 5
        some_analysis: 3
        memorization_only: 1
```

### Category 4: Presentation Readiness (25 points)

```yaml
presentation_readiness:
  max_points: 25
  criteria:
    presenter_notes:
      weight: 10
      scoring:
        full_monologue: 10
        adequate_notes: 7
        sparse_notes: 4
        no_notes: 0

    visual_specifications:
      weight: 8
      scoring:
        complete_specs: 8
        partial_specs: 5
        vague_specs: 2
        no_specs: 0

    flow_coherence:
      weight: 7
      scoring:
        logical_flow: 7
        mostly_logical: 5
        some_gaps: 3
        disjointed: 0
```

---

## Step-by-Step Instructions

### Step 1: Initialize Score Tracker
```python
def initialize_score_tracker():
    """Initialize scoring structure."""

    return {
        'format_compliance': {
            'max': 25,
            'earned': 0,
            'items': []
        },
        'content_quality': {
            'max': 25,
            'earned': 0,
            'items': []
        },
        'standards_alignment': {
            'max': 25,
            'earned': 0,
            'items': []
        },
        'presentation_readiness': {
            'max': 25,
            'earned': 0,
            'items': []
        }
    }
```

### Step 2: Score Format Compliance
```python
def score_format_compliance(slides, validation_result, rubric):
    """Score format compliance category."""

    scores = []
    criteria = rubric['format_compliance']['criteria']

    # Character limits
    char_violations = [v for v in validation_result.get('violations', [])
                       if v['type'] == 'CHARACTER_LIMIT']
    char_weight = criteria['character_limits']['weight']

    if len(char_violations) == 0:
        char_score = char_weight  # Full points
        char_level = 'all_pass'
    elif len(char_violations) <= 3:
        char_score = criteria['character_limits']['scoring']['minor_violations']
        char_level = 'minor_violations'
    elif len(char_violations) <= 8:
        char_score = criteria['character_limits']['scoring']['major_violations']
        char_level = 'major_violations'
    else:
        char_score = 0
        char_level = 'severe_violations'

    scores.append({
        'criterion': 'character_limits',
        'earned': char_score,
        'max': char_weight,
        'level': char_level,
        'details': f"{len(char_violations)} violations found"
    })

    # Structure completeness
    struct_violations = [v for v in validation_result.get('violations', [])
                         if v['type'] == 'MISSING_SECTION']
    struct_weight = criteria['structure_completeness']['weight']

    if len(struct_violations) == 0:
        struct_score = struct_weight
        struct_level = 'all_sections_present'
    elif len(struct_violations) <= 2:
        struct_score = criteria['structure_completeness']['scoring']['missing_optional']
        struct_level = 'missing_optional'
    else:
        struct_score = criteria['structure_completeness']['scoring']['missing_required']
        struct_level = 'missing_required'

    scores.append({
        'criterion': 'structure_completeness',
        'earned': struct_score,
        'max': struct_weight,
        'level': struct_level
    })

    # Visual markers
    marker_violations = [v for v in validation_result.get('violations', [])
                         if 'MARKER' in v['type']]
    marker_weight = criteria['visual_markers']['weight']

    if len(marker_violations) == 0:
        marker_score = marker_weight
    elif len(marker_violations) <= len(slides) / 2:
        marker_score = criteria['visual_markers']['scoring']['some_missing']
    else:
        marker_score = 0

    scores.append({
        'criterion': 'visual_markers',
        'earned': marker_score,
        'max': marker_weight
    })

    # Naming conventions (simplified check)
    naming_score = criteria['naming_conventions']['weight']  # Assume compliant
    scores.append({
        'criterion': 'naming_conventions',
        'earned': naming_score,
        'max': criteria['naming_conventions']['weight']
    })

    total_earned = sum(s['earned'] for s in scores)
    return total_earned, scores
```

### Step 3: Score Content Quality
```python
def score_content_quality(slides, rubric):
    """Score content quality category."""

    scores = []
    criteria = rubric['content_quality']['criteria']

    # Clinical accuracy (simplified - would need NLP/manual review)
    # For now, assume adequate unless flagged
    accuracy_weight = criteria['clinical_accuracy']['weight']
    accuracy_score = accuracy_weight * 0.8  # Default to 80%
    scores.append({
        'criterion': 'clinical_accuracy',
        'earned': accuracy_score,
        'max': accuracy_weight,
        'note': 'Manual review recommended'
    })

    # Completeness
    complete_weight = criteria['completeness']['weight']
    slides_with_body = sum(1 for s in slides if s.get('body') and len(s['body']) > 50)
    completeness_ratio = slides_with_body / len(slides) if slides else 0

    if completeness_ratio >= 0.95:
        complete_score = complete_weight
    elif completeness_ratio >= 0.8:
        complete_score = criteria['completeness']['scoring']['adequate']
    elif completeness_ratio >= 0.6:
        complete_score = criteria['completeness']['scoring']['gaps_present']
    else:
        complete_score = 0

    scores.append({
        'criterion': 'completeness',
        'earned': complete_score,
        'max': complete_weight,
        'ratio': completeness_ratio
    })

    # Clarity (based on sentence structure)
    clarity_weight = criteria['clarity']['weight']
    avg_sentence_length = calculate_avg_sentence_length(slides)

    if 15 <= avg_sentence_length <= 25:
        clarity_score = clarity_weight
    elif 10 <= avg_sentence_length <= 30:
        clarity_score = criteria['clarity']['scoring']['mostly_clear']
    else:
        clarity_score = criteria['clarity']['scoring']['some_confusion']

    scores.append({
        'criterion': 'clarity',
        'earned': clarity_score,
        'max': clarity_weight,
        'avg_sentence_length': avg_sentence_length
    })

    total_earned = sum(s['earned'] for s in scores)
    return total_earned, scores

def calculate_avg_sentence_length(slides):
    """Calculate average sentence length across slides."""
    all_text = ' '.join(s.get('body', '') for s in slides)
    sentences = re.split(r'[.!?]+', all_text)
    sentences = [s.strip() for s in sentences if s.strip()]

    if not sentences:
        return 0

    total_words = sum(len(s.split()) for s in sentences)
    return total_words / len(sentences)
```

### Step 4: Score Standards Alignment
```python
def score_standards_alignment(slides, rubric):
    """Score standards alignment category."""

    scores = []
    criteria = rubric['standards_alignment']['criteria']

    # ELA standards coverage
    ela_weight = criteria['ela_standards_coverage']['weight']
    # Check for ELA standard tags in content
    ela_keywords = ['RL', 'SL', 'W', 'reading', 'speaking', 'listening',
                    'writing', 'interpret', 'collaborate', 'present']
    tagged_slides = sum(1 for s in slides
                        if any(kw in (s.get('body', '') + s.get('notes', '')).lower()
                               for kw in ela_keywords))
    tag_ratio = tagged_slides / len(slides) if slides else 0

    if tag_ratio >= 0.8:
        ela_score = ela_weight
    elif tag_ratio >= 0.5:
        ela_score = criteria['ela_standards_coverage']['scoring']['tagged_only']
    else:
        ela_score = criteria['ela_standards_coverage']['scoring']['partially_tagged']

    scores.append({
        'criterion': 'ela_standards_coverage',
        'earned': ela_score,
        'max': ela_weight
    })

    # Performance tips
    tips_weight = criteria['performance_tips']['weight']
    slides_with_tips = sum(1 for s in slides
                           if s.get('tip') and s['tip'].lower() not in ['none', 'n/a'])
    tip_ratio = slides_with_tips / len(slides) if slides else 0

    if tip_ratio >= 0.7:
        tips_score = tips_weight
    elif tip_ratio >= 0.4:
        tips_score = criteria['performance_tips']['scoring']['helpful_general']
    elif tip_ratio > 0:
        tips_score = criteria['performance_tips']['scoring']['present_not_helpful']
    else:
        tips_score = 0

    scores.append({
        'criterion': 'performance_tips',
        'earned': tips_score,
        'max': tips_weight,
        'tip_ratio': tip_ratio
    })

    # Activity quality
    activity_weight = criteria['activity_quality']['weight']
    activity_slides = [s for s in slides if s.get('type') == 'Activity']

    if activity_slides:
        well_formed = sum(1 for a in activity_slides
                          if 'instruction' in a.get('body', '').lower()
                          or 'step' in a.get('body', '').lower())
        activity_score = (well_formed / len(activity_slides)) * activity_weight
    else:
        activity_score = activity_weight * 0.5  # No activities, partial credit

    scores.append({
        'criterion': 'activity_quality',
        'earned': activity_score,
        'max': activity_weight
    })

    # Critical thinking
    thinking_weight = criteria['critical_thinking']['weight']
    # Check for analysis-promoting language
    analysis_terms = ['analyze', 'evaluate', 'interpret', 'critique',
                      'assess', 'compare', 'perform', 'demonstrate', 'create']
    analysis_count = sum(1 for s in slides
                         if any(term in (s.get('body', '')).lower()
                                for term in analysis_terms))
    analysis_ratio = analysis_count / len(slides) if slides else 0

    if analysis_ratio >= 0.6:
        thinking_score = thinking_weight
    elif analysis_ratio >= 0.3:
        thinking_score = criteria['critical_thinking']['scoring']['some_analysis']
    else:
        thinking_score = criteria['critical_thinking']['scoring']['memorization_only']

    scores.append({
        'criterion': 'critical_thinking',
        'earned': thinking_score,
        'max': thinking_weight
    })

    total_earned = sum(s['earned'] for s in scores)
    return total_earned, scores
```

### Step 5: Score Presentation Readiness
```python
def score_presentation_readiness(slides, rubric):
    """Score presentation readiness category."""

    scores = []
    criteria = rubric['presentation_readiness']['criteria']

    # Presenter notes
    notes_weight = criteria['presenter_notes']['weight']
    slides_with_good_notes = sum(1 for s in slides
                                  if s.get('notes') and len(s['notes'].split()) >= 100)
    notes_ratio = slides_with_good_notes / len(slides) if slides else 0

    if notes_ratio >= 0.9:
        notes_score = notes_weight
    elif notes_ratio >= 0.7:
        notes_score = criteria['presenter_notes']['scoring']['adequate_notes']
    elif notes_ratio >= 0.4:
        notes_score = criteria['presenter_notes']['scoring']['sparse_notes']
    else:
        notes_score = 0

    scores.append({
        'criterion': 'presenter_notes',
        'earned': notes_score,
        'max': notes_weight,
        'notes_ratio': notes_ratio
    })

    # Visual specifications
    visual_weight = criteria['visual_specifications']['weight']
    visual_slides = [s for s in slides if 'Yes' in (s.get('visual_marker') or '')]
    if visual_slides:
        with_specs = sum(1 for v in visual_slides
                         if 'VISUAL SPECIFICATION' in (v.get('raw_content') or ''))
        spec_ratio = with_specs / len(visual_slides)
        visual_score = spec_ratio * visual_weight
    else:
        visual_score = visual_weight  # No visual slides = full credit

    scores.append({
        'criterion': 'visual_specifications',
        'earned': visual_score,
        'max': visual_weight
    })

    # Flow coherence (simplified check)
    flow_weight = criteria['flow_coherence']['weight']
    # Check for intro and logical progression
    has_intro = any('intro' in (s.get('type') or '').lower() for s in slides)
    flow_score = flow_weight if has_intro else flow_weight * 0.7

    scores.append({
        'criterion': 'flow_coherence',
        'earned': flow_score,
        'max': flow_weight
    })

    total_earned = sum(s['earned'] for s in scores)
    return total_earned, scores
```

### Step 6: Calculate Final Score
```python
def calculate_final_score(blueprint_content, validation_result, rubric):
    """Calculate overall quality score."""

    # Parse slides
    slides = parse_blueprint_for_scoring(blueprint_content)

    # Initialize tracker
    tracker = initialize_score_tracker()

    # Score each category
    format_score, format_items = score_format_compliance(slides, validation_result, rubric)
    content_score, content_items = score_content_quality(slides, rubric)
    standards_score, standards_items = score_standards_alignment(slides, rubric)
    ready_score, ready_items = score_presentation_readiness(slides, rubric)

    # Update tracker
    tracker['format_compliance']['earned'] = format_score
    tracker['format_compliance']['items'] = format_items
    tracker['content_quality']['earned'] = content_score
    tracker['content_quality']['items'] = content_items
    tracker['standards_alignment']['earned'] = standards_score
    tracker['standards_alignment']['items'] = standards_items
    tracker['presentation_readiness']['earned'] = ready_score
    tracker['presentation_readiness']['items'] = ready_items

    # Calculate total
    total_score = format_score + content_score + standards_score + ready_score

    # Assign grade
    grade = assign_grade(total_score)

    # Check pass threshold
    pass_threshold = 90
    passed = total_score >= pass_threshold

    # Identify improvement areas
    improvement_areas = identify_improvements(tracker)

    return {
        'total_score': round(total_score, 1),
        'category_scores': {
            'format_compliance': round(format_score, 1),
            'content_quality': round(content_score, 1),
            'standards_alignment': round(standards_score, 1),
            'presentation_readiness': round(ready_score, 1)
        },
        'score_breakdown': tracker,
        'grade': grade,
        'pass_threshold': pass_threshold,
        'passed': passed,
        'improvement_areas': improvement_areas
    }

def assign_grade(score):
    """Assign letter grade based on score."""
    if score >= 93:
        return 'A'
    elif score >= 85:
        return 'B'
    elif score >= 77:
        return 'C'
    elif score >= 70:
        return 'D'
    else:
        return 'F'

def identify_improvements(tracker):
    """Identify areas needing improvement."""
    improvements = []

    for category, data in tracker.items():
        ratio = data['earned'] / data['max'] if data['max'] > 0 else 0
        if ratio < 0.8:
            improvements.append({
                'category': category,
                'current': data['earned'],
                'max': data['max'],
                'percentage': round(ratio * 100, 1),
                'priority': 'HIGH' if ratio < 0.6 else 'MEDIUM'
            })

    return sorted(improvements, key=lambda x: x['percentage'])
```

---

## Output Format

### Score Report
```
===== QUALITY SCORE REPORT =====
Section: [Section Name]
Date: [YYYY-MM-DD HH:MM:SS]

OVERALL SCORE: [XX]/100 (Grade: [A/B/C/D/F])
Pass Threshold: 90
Status: [PASSED/NEEDS IMPROVEMENT]

CATEGORY BREAKDOWN:
----------------------------------------
Format Compliance:      [XX]/25
Content Quality:        [XX]/25
Standards Alignment:    [XX]/25
Presentation Readiness: [XX]/25

DETAILED SCORES:
----------------------------------------
Format Compliance:
  - Character Limits: [X]/8
  - Structure: [X]/7
  - Visual Markers: [X]/5
  - Naming: [X]/5

[...other categories...]

IMPROVEMENT AREAS:
----------------------------------------
1. [Category] - [XX]% (Priority: [HIGH/MEDIUM])
2. [Category] - [XX]% (Priority: [HIGH/MEDIUM])

STATUS: [READY FOR STEP 9 / NEEDS REVISION]
```

---

## Pass Thresholds

```yaml
thresholds:
  overall_pass: 90
  category_minimum: 18  # Out of 25 (72%)

  grade_requirements:
    A: 93-100 (Excellent - production ready)
    B: 85-92 (Good - minor revisions)
    C: 77-84 (Acceptable - needs work)
    D: 70-76 (Poor - significant revision)
    F: 0-69 (Failing - major overhaul)
```

---

## Error Handling

| Error | Action |
|-------|--------|
| Empty blueprint | Return score 0 with "empty content" |
| Missing validation result | Run validation first |
| Parse error | Return partial score with error noted |
| Invalid rubric | Use defaults |

---

**Agent Version:** 1.0
**Last Updated:** 2026-01-04
