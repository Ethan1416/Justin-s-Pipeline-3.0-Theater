# Unit Sequence Optimizer Agent

## Agent Identity
- **Name:** unit_sequence_optimizer
- **Phase:** 1 (Unit Planning)
- **Purpose:** Optimize the sequence of lessons within a unit for optimal learning progression
- **Invocation:** Called after unit_scope_validator to optimize lesson order

---

## Required Skills (Hardcoded)

### Skill 1: Prerequisite Checker
```python
def check_prerequisites(lesson, previous_lessons):
    """Verify lesson prerequisites are covered by previous lessons."""
    required_knowledge = lesson.get('prerequisites', [])
    covered_topics = set()

    for prev in previous_lessons:
        covered_topics.update(prev.get('topics_covered', []))
        covered_topics.update(prev.get('vocabulary', []))

    missing = [req for req in required_knowledge if req not in covered_topics]
    return {'satisfied': len(missing) == 0, 'missing': missing}
```

### Skill 2: Scaffolding Analyzer
```python
def analyze_scaffolding(lessons):
    """Analyze if lessons build appropriately on each other."""
    issues = []
    for i, lesson in enumerate(lessons[1:], 1):
        complexity = lesson.get('complexity', 1)
        prev_complexity = lessons[i-1].get('complexity', 1)

        if complexity > prev_complexity + 2:
            issues.append(f"Day {lesson['day']}: Complexity jump too large")

    return issues
```

---

## Input Schema
```json
{
  "unit_plan": {
    "unit_name": "string",
    "unit_number": "integer (1-4)",
    "days": [
      {
        "day": "integer",
        "topic": "string",
        "learning_objectives": ["array"],
        "vocabulary": ["array"],
        "prerequisites": ["array of required prior knowledge"],
        "complexity": "integer (1-5)",
        "lesson_type": "string (intro|core|practice|assessment|culminating)"
      }
    ]
  },
  "optimization_mode": "string ('suggest' | 'auto')"
}
```

## Output Schema
```json
{
  "optimization_status": "OPTIMIZED | SUGGESTIONS | NO_CHANGES",
  "original_sequence": ["array of day numbers in original order"],
  "optimized_sequence": ["array of day numbers in optimized order"],
  "changes_made": [
    {
      "change_type": "MOVE | SWAP | MERGE | SPLIT",
      "original_position": "integer",
      "new_position": "integer",
      "rationale": "string"
    }
  ],
  "scaffolding_analysis": {
    "complexity_progression": "SMOOTH | JUMPY | FLAT",
    "prerequisite_coverage": "COMPLETE | GAPS",
    "lesson_type_distribution": "BALANCED | UNBALANCED"
  },
  "recommendations": ["array of suggestions if not auto-optimizing"]
}
```

---

## Sequencing Principles

### 1. Lesson Type Progression
```
INTRODUCTION -> CORE CONTENT -> PRACTICE -> SYNTHESIS -> ASSESSMENT
     Day 1    |   Days 2-70%   | Days 15%  |  Days 10%  |  Final 5%
```

### 2. Complexity Curve
```
Complexity
    5 |                    ●●●   Assessment
    4 |              ●●●●●      Practice/Synthesis
    3 |        ●●●●●            Core Content
    2 |    ●●●                  Foundation
    1 | ●●                      Introduction
      +----------------------------->
        Day 1      Mid-Unit      Final Day
```

### 3. Prerequisites Must Precede Dependents
- Vocabulary introduced before it's used
- Concepts explained before they're applied
- Skills modeled before they're practiced

---

## Step-by-Step Instructions

### Step 1: Analyze Current Sequence
```python
def analyze_current_sequence(unit_plan):
    """Analyze the current lesson sequence for issues."""
    days = unit_plan.get('days', [])
    analysis = {
        'prerequisite_issues': [],
        'complexity_issues': [],
        'type_distribution': {},
        'vocabulary_flow': []
    }

    # Track what's been covered
    covered_topics = set()
    covered_vocabulary = set()

    for i, day in enumerate(days):
        # Check prerequisites
        prereqs = day.get('prerequisites', [])
        for prereq in prereqs:
            if prereq not in covered_topics and prereq not in covered_vocabulary:
                analysis['prerequisite_issues'].append({
                    'day': day['day'],
                    'missing_prereq': prereq,
                    'severity': 'ERROR'
                })

        # Check complexity progression
        if i > 0:
            curr_complexity = day.get('complexity', 3)
            prev_complexity = days[i-1].get('complexity', 3)
            if curr_complexity > prev_complexity + 1:
                analysis['complexity_issues'].append({
                    'day': day['day'],
                    'jump': curr_complexity - prev_complexity,
                    'severity': 'WARNING'
                })
            elif curr_complexity < prev_complexity - 1 and day.get('lesson_type') != 'practice':
                analysis['complexity_issues'].append({
                    'day': day['day'],
                    'drop': prev_complexity - curr_complexity,
                    'severity': 'INFO'
                })

        # Track lesson type distribution
        lesson_type = day.get('lesson_type', 'core')
        analysis['type_distribution'][lesson_type] = analysis['type_distribution'].get(lesson_type, 0) + 1

        # Update covered content
        covered_topics.update(day.get('topics_covered', [day.get('topic', '')]))
        covered_vocabulary.update(day.get('vocabulary', []))

    return analysis
```

### Step 2: Identify Optimization Opportunities
```python
def identify_optimizations(days, analysis):
    """Identify potential sequence optimizations."""
    optimizations = []

    # Fix prerequisite issues by reordering
    for issue in analysis['prerequisite_issues']:
        day_num = issue['day']
        missing = issue['missing_prereq']

        # Find which day covers this prerequisite
        provider_day = None
        for d in days:
            if missing in d.get('vocabulary', []) or missing in d.get('topics_covered', []):
                provider_day = d['day']
                break

        if provider_day and provider_day > day_num:
            optimizations.append({
                'change_type': 'MOVE',
                'day': provider_day,
                'new_position': day_num - 1,
                'rationale': f"Day {provider_day} covers '{missing}' needed by Day {day_num}"
            })

    # Smooth complexity jumps
    for issue in analysis['complexity_issues']:
        if issue['severity'] == 'WARNING':
            optimizations.append({
                'change_type': 'SUGGEST',
                'day': issue['day'],
                'rationale': f"Consider adding scaffolding before Day {issue['day']} (complexity jump of {issue['jump']})"
            })

    return optimizations
```

### Step 3: Apply Optimizations (Auto Mode)
```python
def apply_optimizations(days, optimizations, mode):
    """Apply optimizations to the sequence."""
    if mode != 'auto':
        return days, []

    optimized = days.copy()
    changes_made = []

    for opt in optimizations:
        if opt['change_type'] == 'MOVE':
            # Find and move the day
            day_to_move = None
            move_idx = None
            for i, d in enumerate(optimized):
                if d['day'] == opt['day']:
                    day_to_move = d
                    move_idx = i
                    break

            if day_to_move and move_idx is not None:
                optimized.pop(move_idx)
                new_idx = opt['new_position']
                optimized.insert(new_idx, day_to_move)
                changes_made.append({
                    'change_type': 'MOVE',
                    'original_position': move_idx + 1,
                    'new_position': new_idx + 1,
                    'rationale': opt['rationale']
                })

    # Renumber days after optimization
    for i, day in enumerate(optimized):
        day['original_day'] = day.get('day', i + 1)
        day['day'] = i + 1

    return optimized, changes_made
```

### Step 4: Validate Optimized Sequence
```python
def validate_optimized_sequence(optimized_days):
    """Ensure optimized sequence is valid."""
    # Re-run prerequisite check
    analysis = analyze_current_sequence({'days': optimized_days})

    # Check lesson type boundaries
    first_day = optimized_days[0] if optimized_days else {}
    last_day = optimized_days[-1] if optimized_days else {}

    validation = {
        'prerequisite_check': len(analysis['prerequisite_issues']) == 0,
        'intro_first': first_day.get('lesson_type') == 'intro',
        'culminating_last': last_day.get('lesson_type') in ['assessment', 'culminating'],
        'smooth_complexity': len([i for i in analysis['complexity_issues'] if i['severity'] == 'WARNING']) == 0
    }

    return validation
```

### Step 5: Generate Optimization Report
```python
def optimize_unit_sequence(unit_plan, optimization_mode):
    """Generate complete sequence optimization report."""

    days = unit_plan.get('days', [])

    # Analyze current sequence
    analysis = analyze_current_sequence(unit_plan)

    # Identify optimizations
    optimizations = identify_optimizations(days, analysis)

    # Apply optimizations if auto mode
    optimized_days, changes = apply_optimizations(days, optimizations, optimization_mode)

    # Validate result
    validation = validate_optimized_sequence(optimized_days)

    # Determine status
    if not optimizations:
        status = 'NO_CHANGES'
    elif optimization_mode == 'auto' and changes:
        status = 'OPTIMIZED'
    else:
        status = 'SUGGESTIONS'

    # Analyze scaffolding
    scaffolding = {
        'complexity_progression': 'SMOOTH' if validation['smooth_complexity'] else 'JUMPY',
        'prerequisite_coverage': 'COMPLETE' if validation['prerequisite_check'] else 'GAPS',
        'lesson_type_distribution': 'BALANCED' if validation['intro_first'] and validation['culminating_last'] else 'UNBALANCED'
    }

    return {
        'optimization_status': status,
        'original_sequence': [d['day'] for d in days],
        'optimized_sequence': [d['day'] for d in optimized_days],
        'changes_made': changes,
        'scaffolding_analysis': scaffolding,
        'recommendations': [o['rationale'] for o in optimizations if o['change_type'] == 'SUGGEST']
    }
```

---

## Theater Unit Sequencing Guidelines

### Unit 1: Greek Theater (20 days)
```
Day 1: Introduction to Greek Theater
Days 2-4: Historical Context & the Festival of Dionysus
Days 5-8: Elements of Greek Theater (orchestra, theatron, skene)
Days 9-12: Tragedy - Structure & Themes
Days 13-15: Comedy - Structure & Themes
Days 16-17: The Chorus & Mask Work
Days 18-19: Scene Work / Practice
Day 20: Performance / Assessment
```

### Unit 2: Commedia dell'Arte (18 days)
```
Day 1: Introduction to Commedia
Days 2-4: Historical Context & Italian Renaissance
Days 5-10: Stock Characters (deep dive each type)
Days 11-13: Lazzi & Physical Comedy
Days 14-15: Improvisation Within Structure
Days 16-17: Scenario Creation & Practice
Day 18: Performance / Assessment
```

### Unit 3: Shakespeare (25 days)
```
Day 1: Introduction to Shakespeare
Days 2-4: Historical Context & the Globe
Days 5-8: Language - Verse, Prose, Iambic Pentameter
Days 9-13: Tragedy Study (Romeo & Juliet or Hamlet excerpts)
Days 14-18: Comedy Study (Midsummer or Much Ado excerpts)
Days 19-22: Scene Work & Monologue Preparation
Days 23-24: Rehearsal & Coaching
Day 25: Performance / Assessment
```

### Unit 4: Student-Directed One Acts (17 days)
```
Day 1: Introduction to Directing
Days 2-4: Director's Analysis & Concept Development
Days 5-7: Blocking Fundamentals
Days 8-10: Working with Actors
Days 11-14: Rehearsal Process
Days 15-16: Tech & Final Rehearsals
Day 17: Performance Showcase
```

---

## Output Format

```
============================================================
UNIT SEQUENCE OPTIMIZATION REPORT
============================================================
Unit: [Unit Name]
Mode: [suggest | auto]
Date: [YYYY-MM-DD HH:MM:SS]

STATUS: [OPTIMIZED | SUGGESTIONS | NO_CHANGES]

------------------------------------------------------------
SEQUENCE COMPARISON
------------------------------------------------------------
Original: 1 → 2 → 3 → 4 → 5 → ...
Optimized: 1 → 3 → 2 → 4 → 5 → ...
                ↑   ↑
              Swapped to fix prerequisites

------------------------------------------------------------
CHANGES MADE
------------------------------------------------------------
1. [MOVE] Day 3 moved from position 3 to position 2
   Rationale: Day 3 covers vocabulary needed by Day 2

2. [SUGGEST] Consider adding scaffolding before Day 7
   Rationale: Complexity jump of 3 levels

------------------------------------------------------------
SCAFFOLDING ANALYSIS
------------------------------------------------------------
Complexity Progression: [SMOOTH | JUMPY]
Prerequisite Coverage: [COMPLETE | GAPS]
Lesson Type Distribution: [BALANCED | UNBALANCED]

------------------------------------------------------------
RECOMMENDATIONS
------------------------------------------------------------
1. [Recommendation if any]

============================================================
```

---

## Quality Gates

Before finalizing sequence:
- [ ] All prerequisites satisfied
- [ ] No complexity jumps > 2 levels
- [ ] Introduction lesson is Day 1
- [ ] Culminating activity is final day
- [ ] Practice days distributed throughout (not clustered)

---

## Integration Points

**Called By:**
- `unit_planner` (after initial unit creation)
- `unit_scope_validator` (after scope validation)

**Outputs To:**
- `learning_objective_generator` (optimized sequence)
- `daily_agenda_generator` (final day order)

---

**Agent Version:** 1.0 (Theater Pipeline)
**Last Updated:** 2026-01-08
