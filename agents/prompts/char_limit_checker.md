# Character Limit Checker Agent

## Agent Identity
- **Name:** char_limit_checker
- **Step:** 8 (Quality Assurance - Character Limit Verification)
- **Purpose:** Verify that all slide text content conforms to character-per-line limits from constraints.yaml

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
  "total_lines_checked": "number",
  "violations": [
    {
      "slide_number": "number",
      "slide_title": "string",
      "element": "string (HEADER/BODY/TIP)",
      "line_number": "number (within element)",
      "char_count": "number",
      "max_allowed": "number",
      "excess_chars": "number",
      "severity": "string (ERROR/WARNING)",
      "line_content": "string (the violating line)",
      "suggested_break": "string (suggested line break point)"
    }
  ],
  "summary": {
    "header_violations": "number",
    "body_violations": "number",
    "tip_violations": "number",
    "total_violations": "number",
    "worst_violation_chars": "number"
  },
  "pass_rate": "number (percentage)"
}
```

---

## Required Skills (Hardcoded)

1. **char_counting** - Count characters per line accurately (excluding whitespace at line ends)
2. **limit_comparison** - Compare character counts against element-specific limits
3. **error_flagging** - Flag violations with severity and suggested fixes

---

## Validation Rules

### Character Limits (from constraints.yaml)

| Element | Chars Per Line | Reference |
|---------|----------------|-----------|
| HEADER (Title) | 32 | character_limits.title.chars_per_line |
| BODY | 66 | character_limits.body.chars_per_line |
| TIP (NCLEX TIP) | 66 | character_limits.tip.chars_per_line |

### Total Character Limits

| Element | Total Max Chars | Reference |
|---------|-----------------|-----------|
| HEADER (Title) | 64 | character_limits.title.total_max_chars |
| BODY | 660 | character_limits.body.total_max_chars |
| TIP | 132 | character_limits.tip.total_max_chars |

### Counting Rules

1. **Character Counting:**
   - Count all visible characters including punctuation and spaces
   - Exclude trailing whitespace
   - Include bullet point characters in count

2. **Line Breaks:**
   - Each newline creates a new line to check
   - Continuation lines (wrapped in display) each count separately

3. **Special Characters:**
   - Unicode characters count as 1 character each
   - Tabs count as 1 character (should be converted to spaces)

---

## Step-by-Step Instructions

### Step 1: Parse Blueprint Into Lines
```python
def parse_blueprint_for_chars(blueprint_content):
    """Parse blueprint and extract lines per element."""

    slides = []
    current_slide = None
    current_element = None

    for line in blueprint_content.split('\n'):
        # Detect slide boundary
        if line.startswith('---SLIDE ') or line.startswith('SLIDE '):
            if current_slide:
                slides.append(current_slide)
            current_slide = {
                'number': extract_slide_number(line),
                'title': '',
                'elements': {
                    'header': [],
                    'body': [],
                    'tip': []
                }
            }
            current_element = None

        # Detect element markers
        elif 'HEADER:' in line:
            current_element = 'header'
        elif 'BODY:' in line:
            current_element = 'body'
        elif 'NCLEX TIP:' in line or 'TIP:' in line:
            current_element = 'tip'
        elif 'PRESENTER NOTES:' in line or 'Visual:' in line:
            current_element = None  # Skip these

        # Accumulate content lines
        elif current_slide and current_element and line.strip():
            # Skip visual specification blocks
            if 'VISUAL SPECIFICATION' in line:
                current_element = None
                continue
            current_slide['elements'][current_element].append(line.rstrip())

    if current_slide:
        slides.append(current_slide)

    return slides
```

### Step 2: Check Character Limits
```python
def check_char_limits(slides, constraints):
    """Check each line against character limits."""

    CHAR_LIMITS = {
        'header': constraints['character_limits']['title']['chars_per_line'],  # 32
        'body': constraints['character_limits']['body']['chars_per_line'],     # 66
        'tip': constraints['character_limits']['tip']['chars_per_line']        # 66
    }

    TOTAL_LIMITS = {
        'header': constraints['character_limits']['title']['total_max_chars'],  # 64
        'body': constraints['character_limits']['body']['total_max_chars'],     # 660
        'tip': constraints['character_limits']['tip']['total_max_chars']        # 132
    }

    violations = []
    total_lines = 0

    for slide in slides:
        for element_name, lines in slide['elements'].items():
            char_limit = CHAR_LIMITS[element_name]
            total_chars = 0

            for line_num, line in enumerate(lines, 1):
                total_lines += 1
                char_count = len(line.rstrip())
                total_chars += char_count

                if char_count > char_limit:
                    violations.append({
                        'slide_number': slide['number'],
                        'slide_title': slide.get('title', 'Unknown'),
                        'element': element_name.upper(),
                        'line_number': line_num,
                        'char_count': char_count,
                        'max_allowed': char_limit,
                        'excess_chars': char_count - char_limit,
                        'severity': classify_severity(char_count, char_limit),
                        'line_content': line,
                        'suggested_break': suggest_line_break(line, char_limit)
                    })

            # Check total character limit
            if total_chars > TOTAL_LIMITS[element_name]:
                violations.append({
                    'slide_number': slide['number'],
                    'slide_title': slide.get('title', 'Unknown'),
                    'element': element_name.upper(),
                    'line_number': 0,  # Indicates total violation
                    'char_count': total_chars,
                    'max_allowed': TOTAL_LIMITS[element_name],
                    'excess_chars': total_chars - TOTAL_LIMITS[element_name],
                    'severity': 'ERROR',
                    'line_content': f'[TOTAL: {total_chars} chars across {len(lines)} lines]',
                    'suggested_break': 'Reduce overall content length'
                })

    return violations, total_lines

def classify_severity(char_count, limit):
    """Classify violation severity based on excess."""
    excess = char_count - limit
    if excess <= 5:
        return 'WARNING'
    elif excess <= 15:
        return 'ERROR'
    else:
        return 'CRITICAL'

def suggest_line_break(line, limit):
    """Suggest a natural break point for the line."""
    if len(line) <= limit:
        return line

    # Find last space before limit
    break_point = line.rfind(' ', 0, limit)
    if break_point > limit * 0.5:  # Only if reasonable
        return f"{line[:break_point]}\\n{line[break_point+1:]}"
    else:
        return f"{line[:limit]}... [truncate/rewrite]"
```

### Step 3: Generate Detailed Report
```python
def generate_char_limit_report(slides, violations, total_lines):
    """Generate comprehensive character limit report."""

    header_violations = [v for v in violations if v['element'] == 'HEADER']
    body_violations = [v for v in violations if v['element'] == 'BODY']
    tip_violations = [v for v in violations if v['element'] == 'TIP']

    worst = max([v['excess_chars'] for v in violations], default=0)
    pass_rate = ((total_lines - len(violations)) / total_lines) * 100 if total_lines > 0 else 100

    return {
        'validation_status': 'PASS' if len(violations) == 0 else 'FAIL',
        'total_slides': len(slides),
        'total_lines_checked': total_lines,
        'violations': violations,
        'summary': {
            'header_violations': len(header_violations),
            'body_violations': len(body_violations),
            'tip_violations': len(tip_violations),
            'total_violations': len(violations),
            'worst_violation_chars': worst
        },
        'pass_rate': round(pass_rate, 1)
    }
```

---

## Error Codes

| Code | Severity | Description | Action |
|------|----------|-------------|--------|
| CHAR_001 | WARNING | Line exceeds limit by 1-5 chars | Minor edit needed |
| CHAR_002 | ERROR | Line exceeds limit by 6-15 chars | Rewrite line |
| CHAR_003 | CRITICAL | Line exceeds limit by 16+ chars | Split into multiple lines |
| CHAR_004 | ERROR | Header line > 32 chars | Shorten title |
| CHAR_005 | ERROR | Body line > 66 chars | Break or condense |
| CHAR_006 | ERROR | Tip line > 66 chars | Condense tip |
| CHAR_007 | ERROR | Total element chars exceeded | Reduce overall content |

---

## Output Format

### Text Report
```
===== CHARACTER LIMIT VALIDATION REPORT =====
Section: [Section Name]
Date: [YYYY-MM-DD HH:MM:SS]

STATUS: [PASS/FAIL]

LIMITS REFERENCE:
----------------------------------------
Header: 32 chars/line (max 64 total)
Body: 66 chars/line (max 660 total)
Tip: 66 chars/line (max 132 total)

SUMMARY:
----------------------------------------
Total Slides: [N]
Total Lines Checked: [N]
Header Violations: [N]
Body Violations: [N]
Tip Violations: [N]
Total Violations: [N]
Worst Excess: [N] characters
Pass Rate: [XX]%

VIOLATIONS:
----------------------------------------
[If any]
Slide [N], [Element], Line [N]:
  Count: [X] chars (max [Y], excess [Z])
  Severity: [WARNING/ERROR/CRITICAL]
  Content: "[line content]"
  Suggested: "[suggested break or edit]"

[...more violations...]

RECOMMENDATION:
----------------------------------------
[If FAIL]
Return to Step 7 for text condensation.
Priority fixes: [list of worst violations]

[If PASS]
Proceed to next validation check.
```

---

## Visual Element Character Limits (Reference)

For slides marked Visual: Yes, additional limits apply:

| Visual Type | Element | Chars/Line |
|-------------|---------|------------|
| TABLE | Header | 25 |
| TABLE | Cell | 30 |
| DECISION_TREE | Decision Header | 20 |
| DECISION_TREE | Decision Body | 25 |
| FLOWCHART | Step Header | 20 |
| FLOWCHART | Step Body | 25 |
| TIMELINE | Event Header | 20 |
| TIMELINE | Event Body | 25 |
| HIERARCHY | Node Header | 25 |
| HIERARCHY | Node Body | 20 |
| SPECTRUM | Segment Label | 20 |
| SPECTRUM | Description | 25 |
| KEY_DIFF | Concept Header | 25 |
| KEY_DIFF | Feature | 30 |

---

## Integration Points

| Upstream | Downstream |
|----------|------------|
| line_limit_checker | visual_quota_checker |
| formatting_reviser | error_reporter |
| blueprint_generator | score_calculator |

---

**Agent Version:** 1.0
**Last Updated:** 2026-01-04
