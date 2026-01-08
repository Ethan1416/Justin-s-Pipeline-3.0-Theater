# Line Limit Checker Agent

## Agent Identity
- **Name:** line_limit_checker
- **Step:** 8 (Quality Assurance - Line Limit Verification)
- **Purpose:** Verify that all slide sections conform to line limit constraints from constraints.yaml

---

## Input Schema
```json
{
  "blueprint": "string (blueprint content to validate)",
  "section_name": "string (current section name)",
  "constraints_config": "reference to config/constraints.yaml"
}
```

## Output Schema
```json
{
  "validation_status": "string (PASS/FAIL)",
  "total_slides": "number",
  "slides_checked": "number",
  "violations": [
    {
      "slide_number": "number",
      "slide_title": "string",
      "element": "string (HEADER/BODY/TIP)",
      "line_count": "number",
      "max_allowed": "number",
      "excess_lines": "number",
      "severity": "string (ERROR/WARNING)",
      "content_preview": "string (first 50 chars)"
    }
  ],
  "summary": {
    "header_violations": "number",
    "body_violations": "number",
    "tip_violations": "number",
    "total_violations": "number"
  },
  "pass_rate": "number (percentage)"
}
```

---

## Required Skills (Hardcoded)

1. **line_counting** - Count lines in each slide element accurately
2. **limit_comparison** - Compare counted lines against configured limits
3. **error_flagging** - Flag violations with appropriate severity levels

---

## Validation Rules

### Line Limit Constraints (from constraints.yaml)

| Element | Max Lines | Reference |
|---------|-----------|-----------|
| HEADER (Title) | 2 | character_limits.title.max_lines |
| BODY | **8** | character_limits.body.max_lines (R2 requirement) |
| TIP (PERFORMANCE TIP) | 2 | character_limits.tip.max_lines |

### Counting Rules

1. **Line Definition:**
   - A line is any text followed by a newline character OR end of element
   - Empty lines count if between content
   - Trailing empty lines do not count

2. **Element Boundaries:**
   - HEADER: From "HEADER:" to next section marker
   - BODY: From "BODY:" to next section marker
   - TIP: From "PERFORMANCE TIP:" to next section marker or slide boundary

3. **Special Cases:**
   - Bullet points count as separate lines
   - Sub-bullets (indented) count as separate lines
   - Visual specifications within BODY do not count toward line limit

---

## Step-by-Step Instructions

### Step 1: Parse Blueprint
```python
def parse_blueprint_for_lines(blueprint_content):
    """Parse blueprint into slides with elements."""

    slides = []
    current_slide = None

    for line in blueprint_content.split('\n'):
        # Detect slide boundary
        if line.startswith('---SLIDE ') or line.startswith('SLIDE '):
            if current_slide:
                slides.append(current_slide)
            current_slide = {
                'number': extract_slide_number(line),
                'title': '',
                'header_lines': [],
                'body_lines': [],
                'tip_lines': [],
                'current_element': None
            }

        # Detect element markers
        elif 'HEADER:' in line:
            current_slide['current_element'] = 'header'
        elif 'BODY:' in line:
            current_slide['current_element'] = 'body'
        elif 'PERFORMANCE TIP:' in line or 'TIP:' in line:
            current_slide['current_element'] = 'tip'
        elif 'PRESENTER NOTES:' in line:
            current_slide['current_element'] = 'notes'  # Skip
        elif 'Visual:' in line:
            pass  # Visual markers don't count

        # Accumulate content
        elif current_slide and current_slide['current_element']:
            element = current_slide['current_element']
            if element == 'header':
                current_slide['header_lines'].append(line)
            elif element == 'body':
                if not line.strip().startswith('VISUAL SPECIFICATION'):
                    current_slide['body_lines'].append(line)
            elif element == 'tip':
                current_slide['tip_lines'].append(line)

    if current_slide:
        slides.append(current_slide)

    return slides
```

### Step 2: Count Lines Per Element
```python
def count_element_lines(lines):
    """Count non-empty lines in element."""

    # Remove leading/trailing empty lines
    content_lines = []
    started = False

    for line in lines:
        if line.strip():
            started = True
            content_lines.append(line)
        elif started:
            content_lines.append(line)  # Keep internal empty lines

    # Remove trailing empty lines
    while content_lines and not content_lines[-1].strip():
        content_lines.pop()

    return len(content_lines), content_lines
```

### Step 3: Check Against Limits
```python
def check_line_limits(slides, constraints):
    """Check each slide against line limits."""

    # CANONICAL VALUES from config/constraints.yaml
    LIMITS = {
        'header': constraints['character_limits']['title']['max_lines'],  # 2
        'body': constraints['character_limits']['body']['max_lines'],     # 8 (R2 requirement)
        'tip': constraints['character_limits']['tip']['max_lines']        # 2
    }

    violations = []

    for slide in slides:
        # Check header
        header_count, header_content = count_element_lines(slide['header_lines'])
        if header_count > LIMITS['header']:
            violations.append({
                'slide_number': slide['number'],
                'slide_title': slide.get('title', 'Unknown'),
                'element': 'HEADER',
                'line_count': header_count,
                'max_allowed': LIMITS['header'],
                'excess_lines': header_count - LIMITS['header'],
                'severity': 'ERROR',
                'content_preview': ' '.join(header_content)[:50]
            })

        # Check body
        body_count, body_content = count_element_lines(slide['body_lines'])
        if body_count > LIMITS['body']:
            violations.append({
                'slide_number': slide['number'],
                'slide_title': slide.get('title', 'Unknown'),
                'element': 'BODY',
                'line_count': body_count,
                'max_allowed': LIMITS['body'],
                'excess_lines': body_count - LIMITS['body'],
                'severity': 'ERROR' if body_count > LIMITS['body'] + 2 else 'WARNING',
                'content_preview': ' '.join(body_content)[:50]
            })

        # Check tip
        tip_count, tip_content = count_element_lines(slide['tip_lines'])
        if tip_count > LIMITS['tip']:
            violations.append({
                'slide_number': slide['number'],
                'slide_title': slide.get('title', 'Unknown'),
                'element': 'TIP',
                'line_count': tip_count,
                'max_allowed': LIMITS['tip'],
                'excess_lines': tip_count - LIMITS['tip'],
                'severity': 'ERROR',
                'content_preview': ' '.join(tip_content)[:50]
            })

    return violations
```

### Step 4: Generate Report
```python
def generate_line_limit_report(slides, violations):
    """Generate comprehensive line limit report."""

    header_violations = [v for v in violations if v['element'] == 'HEADER']
    body_violations = [v for v in violations if v['element'] == 'BODY']
    tip_violations = [v for v in violations if v['element'] == 'TIP']

    total_checks = len(slides) * 3  # 3 elements per slide
    pass_rate = ((total_checks - len(violations)) / total_checks) * 100 if total_checks > 0 else 100

    return {
        'validation_status': 'PASS' if len(violations) == 0 else 'FAIL',
        'total_slides': len(slides),
        'slides_checked': len(slides),
        'violations': violations,
        'summary': {
            'header_violations': len(header_violations),
            'body_violations': len(body_violations),
            'tip_violations': len(tip_violations),
            'total_violations': len(violations)
        },
        'pass_rate': round(pass_rate, 1)
    }
```

---

## Error Codes

| Code | Severity | Description | Action |
|------|----------|-------------|--------|
| LINE_001 | ERROR | Header exceeds 2 lines | Condense title to 2 lines max |
| LINE_002 | ERROR | Body exceeds 8 lines (R2) | Split content or reduce bullet points |
| LINE_003 | WARNING | Body at 7-8 lines | Consider reducing for readability |
| LINE_004 | ERROR | Tip exceeds 2 lines | Condense tip to 2 lines max |
| LINE_005 | WARNING | Slide has no content | Check for parsing errors |

---

## Output Format

### Text Report
```
===== LINE LIMIT VALIDATION REPORT =====
Section: [Section Name]
Date: [YYYY-MM-DD HH:MM:SS]

STATUS: [PASS/FAIL]

SUMMARY:
----------------------------------------
Total Slides: [N]
Header Violations: [N]
Body Violations: [N]
Tip Violations: [N]
Total Violations: [N]
Pass Rate: [XX]%

VIOLATIONS:
----------------------------------------
[If any]
Slide [N]: [Element] - [X] lines (max [Y])
  Preview: "[first 50 chars...]"
  Severity: [ERROR/WARNING]

[...more violations...]

RECOMMENDATION:
----------------------------------------
[If FAIL]
Return to Step 7 for content revision.
Focus on slides: [list of slide numbers]

[If PASS]
Proceed to next validation check.
```

---

## Integration Points

| Upstream | Downstream |
|----------|------------|
| formatting_reviser | char_limit_checker |
| quality_reviewer | error_reporter |
| blueprint_generator | score_calculator |

---

**Agent Version:** 2.0 (Theater Adaptation)
**Last Updated:** 2026-01-08

### Version History
- **v2.0** (2026-01-08): Adapted for theater pipeline - NCLEX TIP → PERFORMANCE TIP
- **v1.0** (2026-01-04): Initial line limit checker agent
