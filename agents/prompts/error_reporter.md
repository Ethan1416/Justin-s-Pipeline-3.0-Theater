# Error Reporter Agent

## Agent Identity
- **Name:** error_reporter
- **Step:** 8 (Quality Assurance - Error Reporting)
- **Purpose:** Generate comprehensive, actionable error reports from validation and scoring results for pipeline corrections

---

## Input Schema
```json
{
  "validation_result": "object (from constraint_validator)",
  "score_result": "object (from score_calculator)",
  "blueprint_path": "string (path to blueprint file)",
  "section_name": "string (current section)",
  "pipeline_step": "number (which step generated the content)"
}
```

## Output Schema
```json
{
  "report": {
    "header": "object (report metadata)",
    "executive_summary": "string (brief overview)",
    "errors": "array of categorized errors",
    "warnings": "array of categorized warnings",
    "action_items": "array of prioritized fixes",
    "statistics": "object (error counts and distributions)"
  },
  "report_path": "string (path to saved report file)",
  "severity": "string (CRITICAL/HIGH/MEDIUM/LOW)",
  "requires_immediate_action": "boolean"
}
```

---

## Required Skills (Hardcoded)

1. **Error Categorization** - Classify errors by type, severity, and source
2. **Action Item Generation** - Create specific, actionable fix instructions
3. **Report Formatting** - Generate readable, structured reports
4. **Priority Assignment** - Rank issues by impact and urgency
5. **Trend Analysis** - Identify patterns across multiple errors

---

## Error Categories

### Category 1: Format Errors
```yaml
format_errors:
  subcategories:
    - character_limit_exceeded
    - missing_section
    - invalid_marker
    - malformed_structure
    - naming_convention_violation

  severity_rules:
    character_limit_exceeded:
      default: HIGH
      if_minor: MEDIUM
    missing_section:
      required_section: CRITICAL
      optional_section: LOW
```

### Category 2: Content Errors
```yaml
content_errors:
  subcategories:
    - clinical_inaccuracy
    - incomplete_content
    - unclear_language
    - missing_rationale
    - improper_question_format

  severity_rules:
    clinical_inaccuracy: CRITICAL
    missing_rationale: HIGH
    unclear_language: MEDIUM
```

### Category 3: NCLEX Alignment Errors
```yaml
nclex_errors:
  subcategories:
    - missing_nclex_tip
    - invalid_vignette_format
    - missing_client_needs_tag
    - weak_critical_thinking

  severity_rules:
    invalid_vignette_format: HIGH
    missing_nclex_tip: MEDIUM
    weak_critical_thinking: LOW
```

### Category 4: Presentation Errors
```yaml
presentation_errors:
  subcategories:
    - missing_presenter_notes
    - sparse_notes
    - missing_visual_spec
    - flow_discontinuity

  severity_rules:
    missing_presenter_notes: HIGH
    missing_visual_spec: MEDIUM
```

---

## Step-by-Step Instructions

### Step 1: Collect All Issues
```python
def collect_issues(validation_result, score_result):
    """Collect all errors and warnings from validation and scoring."""

    issues = {
        'errors': [],
        'warnings': []
    }

    # From validation result
    for violation in validation_result.get('violations', []):
        issue = {
            'source': 'validation',
            'slide': violation.get('slide'),
            'element': violation.get('element'),
            'type': violation.get('type'),
            'message': violation.get('message'),
            'original_severity': violation.get('severity', 'ERROR')
        }
        issues['errors'].append(issue)

    for warning in validation_result.get('warnings', []):
        issue = {
            'source': 'validation',
            'slide': warning.get('slide'),
            'element': warning.get('element'),
            'type': warning.get('type'),
            'message': warning.get('message'),
            'original_severity': 'WARN'
        }
        issues['warnings'].append(issue)

    # From score result - low scores indicate issues
    for category, data in score_result.get('score_breakdown', {}).items():
        ratio = data['earned'] / data['max'] if data['max'] > 0 else 0

        if ratio < 0.6:
            issues['errors'].append({
                'source': 'scoring',
                'category': category,
                'type': 'LOW_SCORE',
                'message': f"{category} score is {data['earned']}/{data['max']} ({ratio*100:.0f}%)",
                'original_severity': 'ERROR'
            })
        elif ratio < 0.8:
            issues['warnings'].append({
                'source': 'scoring',
                'category': category,
                'type': 'SUBOPTIMAL_SCORE',
                'message': f"{category} score is {data['earned']}/{data['max']} ({ratio*100:.0f}%)",
                'original_severity': 'WARN'
            })

    return issues
```

### Step 2: Categorize and Prioritize
```python
def categorize_issues(issues):
    """Categorize issues and assign final severity."""

    CATEGORY_MAP = {
        'CHARACTER_LIMIT': 'format',
        'MISSING_SECTION': 'format',
        'INVALID_MARKER': 'format',
        'MISSING_MARKER': 'format',
        'LINE_LIMIT': 'format',
        'CONTENT_RULE': 'content',
        'WORD_COUNT': 'presentation',
        'LOW_SCORE': 'scoring',
        'SUBOPTIMAL_SCORE': 'scoring'
    }

    SEVERITY_OVERRIDE = {
        ('format', 'MISSING_SECTION', 'HEADER'): 'CRITICAL',
        ('format', 'MISSING_SECTION', 'BODY'): 'CRITICAL',
        ('format', 'MISSING_MARKER', None): 'HIGH',
        ('content', 'CONTENT_RULE', 'Vignette'): 'HIGH',
        ('content', 'CONTENT_RULE', 'Answer'): 'HIGH',
    }

    categorized = {
        'critical': [],
        'high': [],
        'medium': [],
        'low': []
    }

    for issue in issues['errors'] + issues['warnings']:
        issue_type = issue.get('type', 'UNKNOWN')
        category = CATEGORY_MAP.get(issue_type, 'other')
        element = issue.get('element')

        # Check for severity override
        override_key = (category, issue_type, element)
        if override_key in SEVERITY_OVERRIDE:
            severity = SEVERITY_OVERRIDE[override_key]
        elif override_key[:2] + (None,) in SEVERITY_OVERRIDE:
            severity = SEVERITY_OVERRIDE[override_key[:2] + (None,)]
        else:
            # Default based on original severity
            orig = issue.get('original_severity', 'WARN')
            severity = 'HIGH' if orig == 'ERROR' else 'MEDIUM'

        issue['category'] = category
        issue['severity'] = severity

        categorized[severity.lower()].append(issue)

    return categorized
```

### Step 3: Generate Action Items
```python
def generate_action_items(categorized_issues):
    """Generate specific action items for fixing issues."""

    action_items = []

    # Group issues by type for consolidated actions
    by_type = {}
    for severity_level in ['critical', 'high', 'medium', 'low']:
        for issue in categorized_issues[severity_level]:
            issue_type = issue.get('type')
            if issue_type not in by_type:
                by_type[issue_type] = {
                    'issues': [],
                    'severity': severity_level,
                    'affected_slides': set()
                }
            by_type[issue_type]['issues'].append(issue)
            if issue.get('slide'):
                by_type[issue_type]['affected_slides'].add(issue['slide'])

    # Generate action item for each type
    ACTION_TEMPLATES = {
        'CHARACTER_LIMIT': {
            'action': 'Reduce text length',
            'details': 'Review and condense text in affected slides to meet character limits',
            'how_to_fix': [
                'Remove redundant words and phrases',
                'Use abbreviations where appropriate',
                'Split content across multiple slides if needed',
                'Focus on key points only'
            ]
        },
        'MISSING_SECTION': {
            'action': 'Add missing sections',
            'details': 'Ensure all required sections are present in blueprint',
            'how_to_fix': [
                'Add HEADER section with slide title',
                'Add BODY section with content',
                'Add NCLEX TIP section (can be "None" if not applicable)',
                'Add PRESENTER NOTES section with monologue'
            ]
        },
        'MISSING_MARKER': {
            'action': 'Add Visual markers',
            'details': 'Add Visual: Yes or Visual: No to each slide',
            'how_to_fix': [
                'Add "Visual: No" for content slides',
                'Add "Visual: Yes - [TYPE]" for visual slides',
                'Valid types: TABLE, FLOWCHART, DECISION_TREE, TIMELINE, HIERARCHY, SPECTRUM, KEY_DIFFERENTIATORS'
            ]
        },
        'CONTENT_RULE': {
            'action': 'Fix content compliance',
            'details': 'Ensure content meets NCLEX requirements',
            'how_to_fix': [
                'Add proper question format for vignettes',
                'Include 4 answer options labeled A, B, C, D',
                'Identify correct answer in Answer slides',
                'Provide rationale for correct answer'
            ]
        },
        'WORD_COUNT': {
            'action': 'Adjust presenter notes length',
            'details': 'Ensure notes are 130-450 words (from config/constraints.yaml)',
            'how_to_fix': [
                'Expand sparse notes with more detail (min 130 words)',
                'Add context and examples',
                'Include speaking cues and emphasis points',
                'Condense overly long notes (max 450 words / 180 seconds)'
            ]
        },
        'LOW_SCORE': {
            'action': 'Improve category score',
            'details': 'Review and enhance content in low-scoring category',
            'how_to_fix': [
                'Review scoring rubric for category',
                'Address specific criteria that scored low',
                'Consider restructuring content',
                'Add missing elements'
            ]
        }
    }

    for issue_type, data in by_type.items():
        template = ACTION_TEMPLATES.get(issue_type, {
            'action': f'Fix {issue_type} issues',
            'details': 'Review and correct affected slides',
            'how_to_fix': ['Review error details', 'Make necessary corrections']
        })

        action_items.append({
            'id': len(action_items) + 1,
            'priority': data['severity'].upper(),
            'action': template['action'],
            'details': template['details'],
            'affected_slides': sorted(list(data['affected_slides'])),
            'issue_count': len(data['issues']),
            'how_to_fix': template['how_to_fix']
        })

    # Sort by priority
    priority_order = {'CRITICAL': 0, 'HIGH': 1, 'MEDIUM': 2, 'LOW': 3}
    action_items.sort(key=lambda x: priority_order.get(x['priority'], 4))

    return action_items
```

### Step 4: Calculate Statistics
```python
def calculate_statistics(categorized_issues, validation_result, score_result):
    """Calculate error statistics and distributions."""

    total_errors = sum(len(categorized_issues[s]) for s in ['critical', 'high'])
    total_warnings = sum(len(categorized_issues[s]) for s in ['medium', 'low'])

    # Distribution by category
    category_dist = {}
    for severity_level in categorized_issues:
        for issue in categorized_issues[severity_level]:
            cat = issue.get('category', 'other')
            if cat not in category_dist:
                category_dist[cat] = 0
            category_dist[cat] += 1

    # Distribution by slide
    slide_dist = {}
    for severity_level in categorized_issues:
        for issue in categorized_issues[severity_level]:
            slide = issue.get('slide')
            if slide:
                if slide not in slide_dist:
                    slide_dist[slide] = 0
                slide_dist[slide] += 1

    # Most problematic slides
    problematic_slides = sorted(slide_dist.items(), key=lambda x: -x[1])[:5]

    return {
        'total_issues': total_errors + total_warnings,
        'total_errors': total_errors,
        'total_warnings': total_warnings,
        'by_severity': {
            'critical': len(categorized_issues['critical']),
            'high': len(categorized_issues['high']),
            'medium': len(categorized_issues['medium']),
            'low': len(categorized_issues['low'])
        },
        'by_category': category_dist,
        'by_slide': slide_dist,
        'most_problematic_slides': problematic_slides,
        'overall_score': score_result.get('total_score', 0),
        'pass_status': score_result.get('passed', False)
    }
```

### Step 5: Generate Report
```python
def generate_error_report(validation_result, score_result, section_name, blueprint_path):
    """Generate comprehensive error report."""

    # Collect issues
    issues = collect_issues(validation_result, score_result)

    # Categorize
    categorized = categorize_issues(issues)

    # Generate action items
    action_items = generate_action_items(categorized)

    # Calculate statistics
    stats = calculate_statistics(categorized, validation_result, score_result)

    # Determine overall severity
    if categorized['critical']:
        overall_severity = 'CRITICAL'
        requires_action = True
    elif categorized['high']:
        overall_severity = 'HIGH'
        requires_action = True
    elif categorized['medium']:
        overall_severity = 'MEDIUM'
        requires_action = False
    else:
        overall_severity = 'LOW'
        requires_action = False

    # Generate executive summary
    exec_summary = generate_executive_summary(stats, overall_severity)

    report = {
        'header': {
            'section': section_name,
            'blueprint': blueprint_path,
            'generated': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'overall_severity': overall_severity
        },
        'executive_summary': exec_summary,
        'errors': categorized['critical'] + categorized['high'],
        'warnings': categorized['medium'] + categorized['low'],
        'action_items': action_items,
        'statistics': stats
    }

    return {
        'report': report,
        'severity': overall_severity,
        'requires_immediate_action': requires_action
    }

def generate_executive_summary(stats, severity):
    """Generate brief executive summary."""

    if stats['total_issues'] == 0:
        return "Blueprint passes all validation checks with no issues found."

    if severity == 'CRITICAL':
        return (f"CRITICAL: Blueprint has {stats['by_severity']['critical']} critical issues "
                f"that must be resolved before proceeding. Total {stats['total_errors']} errors "
                f"and {stats['total_warnings']} warnings found.")

    if severity == 'HIGH':
        return (f"Blueprint has {stats['total_errors']} errors requiring attention. "
                f"Score: {stats['overall_score']}/100. Review action items below.")

    if severity == 'MEDIUM':
        return (f"Blueprint is acceptable with {stats['total_warnings']} minor issues. "
                f"Score: {stats['overall_score']}/100. Consider addressing warnings for improvement.")

    return f"Blueprint passes validation. Score: {stats['overall_score']}/100."
```

### Step 6: Format and Save Report
```python
def format_report_text(report_data):
    """Format report as readable text."""

    report = report_data['report']
    lines = []

    # Header
    lines.append("=" * 70)
    lines.append("QUALITY ASSURANCE ERROR REPORT")
    lines.append("=" * 70)
    lines.append(f"Section: {report['header']['section']}")
    lines.append(f"Generated: {report['header']['generated']}")
    lines.append(f"Severity: {report['header']['overall_severity']}")
    lines.append("")

    # Executive Summary
    lines.append("EXECUTIVE SUMMARY")
    lines.append("-" * 70)
    lines.append(report['executive_summary'])
    lines.append("")

    # Statistics
    stats = report['statistics']
    lines.append("STATISTICS")
    lines.append("-" * 70)
    lines.append(f"Total Issues: {stats['total_issues']}")
    lines.append(f"  Errors: {stats['total_errors']}")
    lines.append(f"  Warnings: {stats['total_warnings']}")
    lines.append(f"Overall Score: {stats['overall_score']}/100")
    lines.append(f"Pass Status: {'PASSED' if stats['pass_status'] else 'FAILED'}")
    lines.append("")

    if stats['most_problematic_slides']:
        lines.append("Most Problematic Slides:")
        for slide, count in stats['most_problematic_slides']:
            lines.append(f"  Slide {slide}: {count} issues")
        lines.append("")

    # Errors
    if report['errors']:
        lines.append("ERRORS (Must Fix)")
        lines.append("-" * 70)
        for i, error in enumerate(report['errors'], 1):
            lines.append(f"{i}. [{error['severity']}] Slide {error.get('slide', 'N/A')}: "
                        f"{error.get('element', 'N/A')}")
            lines.append(f"   Type: {error['type']}")
            lines.append(f"   Message: {error['message']}")
            lines.append("")

    # Warnings
    if report['warnings']:
        lines.append("WARNINGS (Should Fix)")
        lines.append("-" * 70)
        for i, warn in enumerate(report['warnings'], 1):
            lines.append(f"{i}. [{warn['severity']}] Slide {warn.get('slide', 'N/A')}: "
                        f"{warn.get('element', 'N/A')}")
            lines.append(f"   Message: {warn['message']}")
            lines.append("")

    # Action Items
    lines.append("ACTION ITEMS")
    lines.append("-" * 70)
    for item in report['action_items']:
        lines.append(f"[{item['priority']}] {item['action']}")
        lines.append(f"  Details: {item['details']}")
        lines.append(f"  Affected Slides: {item['affected_slides']}")
        lines.append(f"  How to Fix:")
        for fix in item['how_to_fix']:
            lines.append(f"    - {fix}")
        lines.append("")

    # Footer
    lines.append("=" * 70)
    if report_data['requires_immediate_action']:
        lines.append("STATUS: REQUIRES IMMEDIATE ACTION")
    else:
        lines.append("STATUS: READY FOR NEXT STEP (with optional improvements)")
    lines.append("=" * 70)

    return '\n'.join(lines)

def save_report(report_data, output_folder):
    """Save report to file."""

    section = report_data['report']['header']['section']
    safe_name = re.sub(r'[^\w\-_]', '_', section)
    filename = f"qa_report_{safe_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"

    report_path = Path(output_folder) / filename

    formatted_report = format_report_text(report_data)

    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(formatted_report)

    return str(report_path)
```

---

## Output Format

### Error Report
```
======================================================================
QUALITY ASSURANCE ERROR REPORT
======================================================================
Section: [Section Name]
Generated: [YYYY-MM-DD HH:MM:SS]
Severity: [CRITICAL/HIGH/MEDIUM/LOW]

EXECUTIVE SUMMARY
----------------------------------------------------------------------
[Brief overview of issues and required actions]

STATISTICS
----------------------------------------------------------------------
Total Issues: [X]
  Errors: [Y]
  Warnings: [Z]
Overall Score: [XX]/100
Pass Status: [PASSED/FAILED]

Most Problematic Slides:
  Slide [N]: [X] issues
  Slide [N]: [X] issues

ERRORS (Must Fix)
----------------------------------------------------------------------
1. [CRITICAL] Slide [N]: [Element]
   Type: [Error Type]
   Message: [Description]

[...more errors...]

WARNINGS (Should Fix)
----------------------------------------------------------------------
1. [MEDIUM] Slide [N]: [Element]
   Message: [Description]

[...more warnings...]

ACTION ITEMS
----------------------------------------------------------------------
[HIGH] [Action Title]
  Details: [What needs to be done]
  Affected Slides: [list of slides]
  How to Fix:
    - [Step 1]
    - [Step 2]

[...more action items...]

======================================================================
STATUS: [REQUIRES IMMEDIATE ACTION / READY FOR NEXT STEP]
======================================================================
```

---

## Error Handling

| Error | Action |
|-------|--------|
| Missing validation result | Generate partial report |
| Missing score result | Generate validation-only report |
| File write error | Return report in memory |
| Invalid section name | Sanitize for filename |

---

**Agent Version:** 1.0
**Last Updated:** 2026-01-04
