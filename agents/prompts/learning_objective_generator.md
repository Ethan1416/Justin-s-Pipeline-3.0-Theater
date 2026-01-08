# Learning Objective Generator Agent

## Agent Identity
- **Name:** learning_objective_generator
- **Phase:** 1 (Unit Planning)
- **Purpose:** Generate measurable learning objectives using Bloom's Taxonomy verbs aligned to California ELA standards
- **Invocation:** Called during lesson planning to create standards-aligned objectives

---

## Required Skills (Hardcoded)

### Skill 1: Bloom's Taxonomy Classifier
```python
def classify_bloom_level(verb):
    """Classify a verb according to Bloom's Taxonomy."""
    BLOOM_LEVELS = {
        'remember': ['identify', 'list', 'name', 'recall', 'recognize', 'state', 'define'],
        'understand': ['describe', 'explain', 'summarize', 'interpret', 'paraphrase', 'discuss'],
        'apply': ['demonstrate', 'perform', 'use', 'execute', 'implement', 'practice'],
        'analyze': ['analyze', 'compare', 'contrast', 'examine', 'differentiate', 'distinguish'],
        'evaluate': ['evaluate', 'assess', 'critique', 'judge', 'justify', 'defend'],
        'create': ['create', 'design', 'develop', 'compose', 'construct', 'produce']
    }

    verb_lower = verb.lower()
    for level, verbs in BLOOM_LEVELS.items():
        if verb_lower in verbs:
            return level
    return 'understand'  # Default
```

### Skill 2: Objective Formatter
```python
def format_objective(verb, content, condition=None, criterion=None):
    """Format a measurable learning objective."""
    objective = f"{verb.capitalize()} {content}"

    if condition:
        objective = f"Given {condition}, {objective.lower()}"

    if criterion:
        objective += f" {criterion}"

    return objective
```

---

## Input Schema
```json
{
  "lesson_context": {
    "unit_name": "string",
    "unit_number": "integer (1-4)",
    "day": "integer",
    "topic": "string",
    "vocabulary": ["array of key terms"],
    "prior_knowledge": "string (what students should already know)"
  },
  "standards": ["array of standard codes (e.g., 'RL.9-10.3', 'SL.9-10.1')"],
  "objective_count": "integer (default: 3)",
  "bloom_distribution": {
    "lower_order": "integer (remember, understand - default: 1)",
    "higher_order": "integer (apply, analyze, evaluate, create - default: 2)"
  }
}
```

## Output Schema
```json
{
  "objectives": [
    {
      "objective_text": "string (the complete objective)",
      "bloom_level": "string (remember|understand|apply|analyze|evaluate|create)",
      "verb": "string (action verb used)",
      "aligned_standards": ["array of standard codes"],
      "assessment_suggestion": "string (how to measure this objective)"
    }
  ],
  "summary": {
    "total_objectives": "integer",
    "bloom_distribution": {
      "remember": "integer",
      "understand": "integer",
      "apply": "integer",
      "analyze": "integer",
      "evaluate": "integer",
      "create": "integer"
    },
    "standards_coverage": ["array of all standards addressed"]
  }
}
```

---

## Bloom's Taxonomy Verb Bank (Theater-Focused)

### Level 1: Remember
```yaml
verbs:
  - identify
  - list
  - name
  - recall
  - recognize
  - state
  - define
  - label
  - match

theater_examples:
  - "Identify the three parts of a Greek theater"
  - "List the five stock characters of Commedia dell'Arte"
  - "Name the elements of iambic pentameter"
  - "Define the term 'lazzi'"
```

### Level 2: Understand
```yaml
verbs:
  - describe
  - explain
  - summarize
  - interpret
  - paraphrase
  - discuss
  - classify
  - compare

theater_examples:
  - "Explain the purpose of the Greek chorus"
  - "Describe the physicality of Arlecchino"
  - "Summarize the plot structure of a Shakespearean tragedy"
  - "Discuss the historical context of Commedia dell'Arte"
```

### Level 3: Apply
```yaml
verbs:
  - demonstrate
  - perform
  - use
  - execute
  - implement
  - practice
  - illustrate
  - apply

theater_examples:
  - "Demonstrate the physical characteristics of a stock character"
  - "Perform a short lazzi sequence"
  - "Apply blocking principles to a scene"
  - "Use iambic pentameter in original dialogue"
```

### Level 4: Analyze
```yaml
verbs:
  - analyze
  - compare
  - contrast
  - examine
  - differentiate
  - distinguish
  - investigate
  - deconstruct

theater_examples:
  - "Analyze the protagonist's motivation in Act 2"
  - "Compare Greek tragedy with Greek comedy"
  - "Contrast the physicality of zanni vs. vecchi characters"
  - "Examine how Shakespeare uses soliloquy to reveal character"
```

### Level 5: Evaluate
```yaml
verbs:
  - evaluate
  - assess
  - critique
  - judge
  - justify
  - defend
  - argue
  - recommend

theater_examples:
  - "Evaluate the effectiveness of the chorus in this scene"
  - "Critique a peer's blocking choices"
  - "Justify your interpretation of Hamlet's 'To be or not to be' soliloquy"
  - "Defend your directorial concept for the one-act"
```

### Level 6: Create
```yaml
verbs:
  - create
  - design
  - develop
  - compose
  - construct
  - produce
  - devise
  - formulate

theater_examples:
  - "Create original choreography for the chorus"
  - "Design a character mask for Pantalone"
  - "Compose a modern adaptation of a Greek myth"
  - "Develop a directorial concept for the production"
```

---

## Step-by-Step Instructions

### Step 1: Analyze Lesson Context
```python
def analyze_lesson_context(context):
    """Extract key elements for objective generation."""
    return {
        'key_concepts': extract_concepts(context['topic']),
        'vocabulary_terms': context.get('vocabulary', []),
        'prior_knowledge': context.get('prior_knowledge', ''),
        'unit_themes': get_unit_themes(context['unit_number']),
        'day_position': categorize_day_position(context['day'], context.get('total_days', 20))
    }
```

### Step 2: Select Appropriate Bloom Levels
```python
def select_bloom_levels(day_position, bloom_distribution):
    """Select Bloom levels based on day position and distribution."""
    levels = []

    lower = bloom_distribution.get('lower_order', 1)
    higher = bloom_distribution.get('higher_order', 2)

    # Early in unit: more lower-order
    if day_position == 'early':
        levels.extend(['remember'] * min(lower, 2))
        levels.extend(['understand'] * max(lower - 1, 0))
        levels.extend(['apply'] * higher)

    # Middle of unit: balanced
    elif day_position == 'middle':
        levels.append('understand')
        levels.extend(['apply', 'analyze'][:higher])

    # Late in unit: more higher-order
    else:  # 'late'
        levels.extend(['analyze', 'evaluate', 'create'][:higher + 1])
        if lower > 0:
            levels.append('understand')

    return levels[:bloom_distribution.get('lower_order', 1) + bloom_distribution.get('higher_order', 2)]
```

### Step 3: Generate Objectives for Each Bloom Level
```python
def generate_objective(bloom_level, context, standards):
    """Generate a single learning objective."""

    # Get appropriate verb
    verb = select_verb(bloom_level, context)

    # Get content focus
    content = generate_content_phrase(context, bloom_level)

    # Add condition if appropriate
    condition = generate_condition(context, bloom_level) if bloom_level in ['apply', 'analyze', 'evaluate'] else None

    # Add criterion if appropriate
    criterion = generate_criterion(bloom_level)

    # Format objective
    objective_text = format_objective(verb, content, condition, criterion)

    # Match to standards
    aligned = match_to_standards(objective_text, standards)

    # Suggest assessment
    assessment = suggest_assessment(bloom_level, verb)

    return {
        'objective_text': objective_text,
        'bloom_level': bloom_level,
        'verb': verb,
        'aligned_standards': aligned,
        'assessment_suggestion': assessment
    }
```

### Step 4: Ensure Standards Coverage
```python
def ensure_standards_coverage(objectives, required_standards):
    """Adjust objectives to ensure all required standards are addressed."""
    covered = set()
    for obj in objectives:
        covered.update(obj['aligned_standards'])

    missing = set(required_standards) - covered

    for standard in missing:
        # Generate additional objective targeting this standard
        new_obj = generate_standard_specific_objective(standard)
        objectives.append(new_obj)

    return objectives
```

### Step 5: Generate Complete Objective Set
```python
def generate_learning_objectives(lesson_context, standards, objective_count, bloom_distribution):
    """Generate complete set of learning objectives."""

    # Analyze context
    context = analyze_lesson_context(lesson_context)

    # Select Bloom levels
    bloom_levels = select_bloom_levels(context['day_position'], bloom_distribution)

    # Ensure we have the right count
    while len(bloom_levels) < objective_count:
        bloom_levels.append('apply')  # Default to application level

    # Generate objectives
    objectives = []
    for level in bloom_levels[:objective_count]:
        obj = generate_objective(level, context, standards)
        objectives.append(obj)

    # Ensure standards coverage
    objectives = ensure_standards_coverage(objectives, standards)

    # Calculate summary
    summary = calculate_summary(objectives, standards)

    return {
        'objectives': objectives,
        'summary': summary
    }
```

---

## Unit-Specific Objective Templates

### Unit 1: Greek Theater
```yaml
remember:
  - "Identify the [component] of Greek theater"
  - "Define the term '[vocabulary_term]'"
  - "List the characteristics of Greek [tragedy/comedy]"

understand:
  - "Explain the purpose of the [chorus/mask/orchestra]"
  - "Describe the structure of Greek [tragedy/comedy]"
  - "Discuss the role of [element] in Greek theater"

apply:
  - "Demonstrate choral movement techniques"
  - "Perform a short Greek-style monologue with mask"
  - "Apply the concept of [catharsis/hubris] to a scene analysis"

analyze:
  - "Analyze the protagonist's hamartia in [play excerpt]"
  - "Compare Greek tragedy with Greek comedy"
  - "Examine how the chorus functions in this scene"

evaluate:
  - "Evaluate the effectiveness of this mask design"
  - "Critique the use of the orchestra space in this staging"

create:
  - "Create original movement for a chorus scene"
  - "Design a mask that represents [character/emotion]"
```

### Unit 2: Commedia dell'Arte
```yaml
remember:
  - "Identify the stock character [name]"
  - "List the physical characteristics of [character]"
  - "Name the categories of Commedia characters"

understand:
  - "Explain the purpose of lazzi in Commedia"
  - "Describe the relationship between [character1] and [character2]"
  - "Summarize the typical scenario structure"

apply:
  - "Demonstrate the walk and posture of [character]"
  - "Perform a lazzi sequence"
  - "Use improvisation within a structured scenario"

analyze:
  - "Analyze how status affects character interactions"
  - "Compare the physicality of zanni vs. vecchi characters"
  - "Examine how Commedia influenced modern comedy"

evaluate:
  - "Evaluate the comedic timing in this lazzi"
  - "Critique a peer's character physicality"

create:
  - "Create an original lazzi routine"
  - "Design a character mask"
  - "Develop a modern Commedia scenario"
```

### Unit 3: Shakespeare
```yaml
remember:
  - "Identify examples of [literary device] in the text"
  - "Define the term '[soliloquy/aside/iambic pentameter]'"
  - "List the elements of [tragedy/comedy] in this play"

understand:
  - "Explain what Shakespeare reveals through this soliloquy"
  - "Paraphrase the meaning of this passage"
  - "Discuss the historical context of [play]"

apply:
  - "Perform a monologue with attention to verse structure"
  - "Apply scansion to mark the iambic pentameter"
  - "Use staging conventions of the Globe Theatre"

analyze:
  - "Analyze the character's motivation in this scene"
  - "Compare the use of prose vs. verse"
  - "Examine how Shakespeare creates dramatic irony"

evaluate:
  - "Evaluate different interpretations of [character]"
  - "Justify your interpretation of this passage"
  - "Critique the effectiveness of this soliloquy"

create:
  - "Create blocking for this scene"
  - "Compose a modern adaptation of this scene"
  - "Develop a character analysis presentation"
```

### Unit 4: Student-Directed One Acts
```yaml
remember:
  - "Identify the elements of a director's concept"
  - "List the responsibilities of a director"
  - "Define key directing terminology"

understand:
  - "Explain your vision for this production"
  - "Describe effective blocking principles"
  - "Discuss how to give constructive notes to actors"

apply:
  - "Demonstrate effective blocking techniques"
  - "Use staging to reveal character relationships"
  - "Apply rehearsal management strategies"

analyze:
  - "Analyze the playwright's intentions"
  - "Compare different directorial approaches"
  - "Examine how technical elements support the story"

evaluate:
  - "Evaluate the pacing of this scene"
  - "Critique blocking choices for clarity"
  - "Assess ensemble collaboration"

create:
  - "Create a director's concept document"
  - "Design the blocking for Act 1"
  - "Develop a rehearsal schedule"
```

---

## Assessment Alignment

| Bloom Level | Assessment Type | Example |
|-------------|-----------------|---------|
| Remember | Quiz, matching, labeling | "Match terms to definitions" |
| Understand | Short answer, discussion | "Explain the purpose of..." |
| Apply | Performance, demonstration | "Perform the character walk" |
| Analyze | Written analysis, comparison | "Compare these two interpretations" |
| Evaluate | Critique, peer review | "Evaluate the effectiveness of..." |
| Create | Project, performance, design | "Create original blocking for..." |

---

## Output Format

```
============================================================
LEARNING OBJECTIVES
============================================================
Unit: [Unit Name]
Day: [Day Number]
Topic: [Topic]

------------------------------------------------------------
OBJECTIVES (By the end of this lesson, students will be able to:)
------------------------------------------------------------

1. [APPLY] Demonstrate the physicality of Arlecchino through
   movement and gesture.
   - Standards: SL.9-10.6
   - Assessment: Performance observation, peer feedback

2. [ANALYZE] Compare the physical characteristics of zanni
   characters with vecchi characters.
   - Standards: RL.9-10.3
   - Assessment: Venn diagram worksheet, class discussion

3. [UNDERSTAND] Explain how Commedia stock characters
   influenced modern comedy archetypes.
   - Standards: RL.9-10.9
   - Assessment: Exit ticket, written response

------------------------------------------------------------
SUMMARY
------------------------------------------------------------
Total Objectives: 3
Bloom Distribution:
  - Remember: 0
  - Understand: 1
  - Apply: 1
  - Analyze: 1
  - Evaluate: 0
  - Create: 0

Standards Addressed: RL.9-10.3, RL.9-10.9, SL.9-10.6

============================================================
```

---

## Quality Gates

Before finalizing objectives:
- [ ] 2-4 objectives per lesson (typically 3)
- [ ] At least one higher-order objective (analyze, evaluate, create)
- [ ] All objectives begin with measurable verb
- [ ] All objectives align to at least one standard
- [ ] Assessment method identified for each objective
- [ ] Objectives appropriate for lesson position in unit

---

## Integration Points

**Called By:**
- `unit_planner` (for unit-level objectives)
- `lesson_plan_generator` (for daily objectives)

**Outputs To:**
- `lesson_plan_generator` (objectives for lesson plan)
- `exit_ticket_generator` (assessment questions)
- `standards_coverage_validator` (for verification)

---

**Agent Version:** 1.0 (Theater Pipeline)
**Last Updated:** 2026-01-08
