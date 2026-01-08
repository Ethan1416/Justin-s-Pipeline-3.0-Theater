# Unit Scope Validator Agent

## Agent Identity
- **Name:** unit_scope_validator
- **Phase:** 1 (Unit Planning)
- **Purpose:** Validate that unit plan fits within time constraints and content density requirements
- **Invocation:** Called after unit_planner to validate scope

---

## Required Skills (Hardcoded)

### Skill 1: Day Counter
```python
def count_unit_days(unit_plan):
    """Count total instructional days in unit."""
    return len(unit_plan.get('days', []))
```

### Skill 2: Content Density Checker
```python
def check_content_density(unit_plan, constraints):
    """Verify content density is appropriate for each day."""
    issues = []
    for day in unit_plan.get('days', []):
        objectives = len(day.get('learning_objectives', []))
        vocabulary = len(day.get('vocabulary', []))

        if objectives > constraints['max_objectives_per_day']:
            issues.append(f"Day {day['day']}: Too many objectives ({objectives})")
        if vocabulary > constraints['max_vocabulary_per_day']:
            issues.append(f"Day {day['day']}: Too much vocabulary ({vocabulary})")

    return issues
```

---

## Input Schema
```json
{
  "unit_plan": {
    "unit_name": "string",
    "unit_number": "integer (1-4)",
    "total_days": "integer",
    "days": [
      {
        "day": "integer",
        "topic": "string",
        "learning_objectives": ["array of objectives"],
        "vocabulary": ["array of terms"],
        "standards": ["array of standard codes"]
      }
    ]
  },
  "constraints": {
    "min_days": "integer (default: 17)",
    "max_days": "integer (default: 25)",
    "max_objectives_per_day": "integer (default: 4)",
    "max_vocabulary_per_day": "integer (default: 8)"
  }
}
```

## Output Schema
```json
{
  "validation_status": "PASS | FAIL | WARN",
  "unit_name": "string",
  "metrics": {
    "total_days": "integer",
    "day_range_status": "PASS | FAIL",
    "average_objectives_per_day": "number",
    "average_vocabulary_per_day": "number",
    "content_density_status": "PASS | WARN | FAIL"
  },
  "issues": [
    {
      "severity": "ERROR | WARNING | INFO",
      "day": "integer (optional)",
      "message": "string",
      "recommendation": "string"
    }
  ],
  "recommendations": ["array of improvement suggestions"]
}
```

---

## Unit Day Ranges (Theater Pipeline)

| Unit | Name | Min Days | Max Days | Target |
|------|------|----------|----------|--------|
| 1 | Greek Theater | 18 | 22 | 20 |
| 2 | Commedia dell'Arte | 16 | 20 | 18 |
| 3 | Shakespeare | 22 | 27 | 25 |
| 4 | Student-Directed One Acts | 15 | 19 | 17 |

**Total Course:** 80 instructional days

---

## Step-by-Step Instructions

### Step 1: Count Total Days
```python
def validate_day_count(unit_plan, constraints):
    """Validate unit fits within day constraints."""
    total_days = count_unit_days(unit_plan)
    min_days = constraints.get('min_days', 17)
    max_days = constraints.get('max_days', 25)

    if total_days < min_days:
        return {
            'status': 'FAIL',
            'message': f'Unit has {total_days} days, minimum is {min_days}',
            'recommendation': f'Add {min_days - total_days} more days of content'
        }
    elif total_days > max_days:
        return {
            'status': 'FAIL',
            'message': f'Unit has {total_days} days, maximum is {max_days}',
            'recommendation': f'Remove or consolidate {total_days - max_days} days'
        }
    else:
        return {
            'status': 'PASS',
            'message': f'Unit has {total_days} days (within {min_days}-{max_days} range)'
        }
```

### Step 2: Check Content Density Per Day
```python
def validate_content_density(unit_plan, constraints):
    """Validate each day has appropriate content density."""
    issues = []
    max_objectives = constraints.get('max_objectives_per_day', 4)
    max_vocab = constraints.get('max_vocabulary_per_day', 8)

    for day in unit_plan.get('days', []):
        day_num = day.get('day', 0)
        objectives = len(day.get('learning_objectives', []))
        vocabulary = len(day.get('vocabulary', []))

        # Check objectives
        if objectives > max_objectives:
            issues.append({
                'severity': 'WARNING',
                'day': day_num,
                'message': f'Day {day_num} has {objectives} objectives (max {max_objectives})',
                'recommendation': 'Consider splitting into multiple days or reducing scope'
            })
        elif objectives < 2:
            issues.append({
                'severity': 'INFO',
                'day': day_num,
                'message': f'Day {day_num} has only {objectives} objective(s)',
                'recommendation': 'Consider adding more objectives or merging with adjacent day'
            })

        # Check vocabulary
        if vocabulary > max_vocab:
            issues.append({
                'severity': 'WARNING',
                'day': day_num,
                'message': f'Day {day_num} has {vocabulary} vocabulary terms (max {max_vocab})',
                'recommendation': 'Reduce vocabulary or spread across multiple days'
            })

    return issues
```

### Step 3: Validate Pacing
```python
def validate_pacing(unit_plan):
    """Check that content builds appropriately across days."""
    issues = []
    days = unit_plan.get('days', [])

    # Check for foundation day (Day 1 should be introductory)
    if days and days[0].get('day') == 1:
        first_day_topic = days[0].get('topic', '').lower()
        if 'introduction' not in first_day_topic and 'overview' not in first_day_topic:
            issues.append({
                'severity': 'INFO',
                'day': 1,
                'message': 'Day 1 does not appear to be an introduction',
                'recommendation': 'Consider starting with an introductory/overview lesson'
            })

    # Check for culminating activity (final days should be synthesis/performance)
    if days:
        last_day = days[-1]
        last_topic = last_day.get('topic', '').lower()
        synthesis_keywords = ['performance', 'presentation', 'assessment', 'review', 'showcase']
        if not any(kw in last_topic for kw in synthesis_keywords):
            issues.append({
                'severity': 'INFO',
                'day': last_day.get('day'),
                'message': 'Final day may not be a culminating activity',
                'recommendation': 'Consider ending with performance, presentation, or assessment'
            })

    return issues
```

### Step 4: Calculate Metrics
```python
def calculate_metrics(unit_plan):
    """Calculate unit metrics for reporting."""
    days = unit_plan.get('days', [])
    total_days = len(days)

    total_objectives = sum(len(d.get('learning_objectives', [])) for d in days)
    total_vocabulary = sum(len(d.get('vocabulary', [])) for d in days)

    return {
        'total_days': total_days,
        'average_objectives_per_day': round(total_objectives / max(total_days, 1), 2),
        'average_vocabulary_per_day': round(total_vocabulary / max(total_days, 1), 2),
        'total_objectives': total_objectives,
        'total_vocabulary': total_vocabulary
    }
```

### Step 5: Generate Final Report
```python
def validate_unit_scope(unit_plan, constraints):
    """Generate complete scope validation report."""

    # Day count validation
    day_result = validate_day_count(unit_plan, constraints)

    # Content density validation
    density_issues = validate_content_density(unit_plan, constraints)

    # Pacing validation
    pacing_issues = validate_pacing(unit_plan)

    # Calculate metrics
    metrics = calculate_metrics(unit_plan)
    metrics['day_range_status'] = day_result['status']

    # Combine issues
    all_issues = [day_result] if day_result['status'] != 'PASS' else []
    all_issues.extend(density_issues)
    all_issues.extend(pacing_issues)

    # Determine overall status
    error_count = len([i for i in all_issues if i.get('severity') == 'ERROR'])
    warning_count = len([i for i in all_issues if i.get('severity') == 'WARNING'])

    if error_count > 0 or day_result['status'] == 'FAIL':
        overall_status = 'FAIL'
    elif warning_count > 0:
        overall_status = 'WARN'
    else:
        overall_status = 'PASS'

    metrics['content_density_status'] = 'FAIL' if error_count > 0 else ('WARN' if warning_count > 0 else 'PASS')

    # Generate recommendations
    recommendations = list(set(i.get('recommendation', '') for i in all_issues if i.get('recommendation')))

    return {
        'validation_status': overall_status,
        'unit_name': unit_plan.get('unit_name', 'Unknown'),
        'metrics': metrics,
        'issues': all_issues,
        'recommendations': recommendations
    }
```

---

## Output Format

```
============================================================
UNIT SCOPE VALIDATION REPORT
============================================================
Unit: [Unit Name]
Date: [YYYY-MM-DD HH:MM:SS]

STATUS: [PASS | WARN | FAIL]

------------------------------------------------------------
METRICS
------------------------------------------------------------
Total Days: [X] (Range: [min]-[max]) [PASS/FAIL]
Average Objectives/Day: [X.X]
Average Vocabulary/Day: [X.X]
Total Objectives: [X]
Total Vocabulary Terms: [X]

------------------------------------------------------------
ISSUES
------------------------------------------------------------
[If any]
[SEVERITY] Day [X]: [Message]
  Recommendation: [Action]

------------------------------------------------------------
RECOMMENDATIONS
------------------------------------------------------------
1. [Recommendation 1]
2. [Recommendation 2]

============================================================
```

---

## Error Handling

| Error Condition | Action |
|-----------------|--------|
| Missing unit_plan | HALT, request unit plan input |
| Empty days array | FAIL, "Unit has no days defined" |
| Missing day numbers | WARN, assume sequential numbering |
| Invalid constraints | Use defaults, log warning |

---

## Quality Gates

Before allowing unit to proceed to daily generation:
- [ ] Total days within range (17-25 typical)
- [ ] No day exceeds 4 objectives
- [ ] No day exceeds 8 vocabulary terms
- [ ] Day 1 is introductory
- [ ] Final day is culminating activity
- [ ] Validation status is PASS or WARN (not FAIL)

---

## Integration Points

**Called By:**
- `unit_planner` (after generating unit plan)
- `unit_sequence_optimizer` (before optimization)

**Calls:**
- None (standalone validation)

**Outputs To:**
- `unit_sequence_optimizer` (if adjustments needed)
- `daily_agenda_generator` (if PASS)

---

**Agent Version:** 1.0 (Theater Pipeline)
**Last Updated:** 2026-01-08
