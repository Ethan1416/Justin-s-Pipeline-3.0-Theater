"""
Bloom's Taxonomy Verb Selector Skill
Select appropriate action verbs for learning objectives based on Bloom's taxonomy levels.

Theater Pipeline Requirements:
- Learning objectives must use measurable verbs
- Verbs should match desired cognitive level
- Theater-specific verbs included

Usage:
    from skills.utilities.blooms_verb_selector import (
        select_verb,
        get_verbs_for_level,
        classify_verb,
        validate_objective,
        generate_objective
    )
"""

from typing import Dict, Any, List, Optional, Tuple
import random


# Bloom's Taxonomy Levels (Revised)
BLOOMS_LEVELS = [
    'remember',      # Level 1: Recall facts and basic concepts
    'understand',    # Level 2: Explain ideas or concepts
    'apply',         # Level 3: Use information in new situations
    'analyze',       # Level 4: Draw connections among ideas
    'evaluate',      # Level 5: Justify a decision or course of action
    'create',        # Level 6: Produce new or original work
]

# Verbs by Bloom's level
BLOOMS_VERBS = {
    'remember': [
        'define', 'describe', 'identify', 'label', 'list', 'match', 'name',
        'outline', 'recall', 'recognize', 'reproduce', 'select', 'state',
        'locate', 'memorize', 'quote', 'recite', 'record', 'repeat'
    ],
    'understand': [
        'classify', 'compare', 'contrast', 'demonstrate', 'explain', 'extend',
        'illustrate', 'infer', 'interpret', 'paraphrase', 'predict', 'summarize',
        'translate', 'associate', 'differentiate', 'discuss', 'distinguish',
        'estimate', 'express', 'generalize', 'give examples'
    ],
    'apply': [
        'apply', 'change', 'compute', 'construct', 'demonstrate', 'discover',
        'manipulate', 'modify', 'operate', 'predict', 'prepare', 'produce',
        'relate', 'show', 'solve', 'use', 'choose', 'dramatize', 'employ',
        'execute', 'implement', 'interpret', 'practice', 'schedule', 'sketch'
    ],
    'analyze': [
        'analyze', 'break down', 'compare', 'contrast', 'diagram', 'differentiate',
        'discriminate', 'distinguish', 'examine', 'experiment', 'identify',
        'illustrate', 'infer', 'outline', 'relate', 'select', 'separate',
        'categorize', 'classify', 'deconstruct', 'detect', 'inspect', 'investigate'
    ],
    'evaluate': [
        'appraise', 'argue', 'assess', 'choose', 'compare', 'conclude',
        'critique', 'decide', 'defend', 'evaluate', 'judge', 'justify',
        'prioritize', 'rank', 'rate', 'recommend', 'select', 'support',
        'value', 'weigh', 'check', 'criticize', 'determine', 'measure', 'test'
    ],
    'create': [
        'arrange', 'assemble', 'collect', 'compose', 'construct', 'create',
        'design', 'develop', 'devise', 'formulate', 'generate', 'hypothesize',
        'invent', 'make', 'organize', 'plan', 'prepare', 'produce', 'propose',
        'rearrange', 'reconstruct', 'revise', 'set up', 'synthesize', 'write'
    ]
}

# Theater-specific verbs by level
THEATER_VERBS = {
    'remember': [
        'identify', 'name', 'label', 'list', 'define', 'recall',
        'recognize', 'locate', 'describe'
    ],
    'understand': [
        'explain', 'describe', 'compare', 'contrast', 'summarize',
        'interpret', 'discuss', 'illustrate', 'distinguish'
    ],
    'apply': [
        'demonstrate', 'perform', 'execute', 'practice', 'use',
        'apply', 'dramatize', 'implement', 'show', 'portray'
    ],
    'analyze': [
        'analyze', 'examine', 'compare', 'contrast', 'investigate',
        'break down', 'differentiate', 'deconstruct', 'critique'
    ],
    'evaluate': [
        'evaluate', 'critique', 'assess', 'judge', 'justify',
        'defend', 'argue', 'support', 'recommend', 'appraise'
    ],
    'create': [
        'create', 'design', 'compose', 'develop', 'devise',
        'construct', 'produce', 'direct', 'choreograph', 'stage',
        'block', 'improvise', 'write', 'adapt', 'interpret'
    ]
}

# Level descriptions
LEVEL_DESCRIPTIONS = {
    'remember': 'Recall facts, terms, basic concepts, or answers',
    'understand': 'Demonstrate understanding of facts and ideas',
    'apply': 'Solve problems by applying knowledge to new situations',
    'analyze': 'Draw connections among ideas, break down into parts',
    'evaluate': 'Justify a stand or decision through criteria',
    'create': 'Produce new or original work'
}

# Recommended levels by lesson type
LESSON_TYPE_LEVELS = {
    'introduction': ['remember', 'understand'],
    'content': ['understand', 'apply', 'analyze'],
    'workshop': ['apply', 'create'],
    'rehearsal': ['apply', 'create'],
    'performance': ['apply', 'create', 'evaluate'],
    'review': ['remember', 'understand', 'analyze'],
    'assessment': ['remember', 'understand', 'apply', 'analyze', 'evaluate']
}


def get_verbs_for_level(
    level: str,
    include_theater: bool = True,
    count: int = None
) -> List[str]:
    """
    Get verbs for a specific Bloom's level.

    Args:
        level: Bloom's taxonomy level
        include_theater: Include theater-specific verbs
        count: Limit number of verbs returned

    Returns:
        List of appropriate verbs
    """
    level = level.lower()
    if level not in BLOOMS_LEVELS:
        raise ValueError(f"Invalid level: {level}. Must be one of {BLOOMS_LEVELS}")

    verbs = list(BLOOMS_VERBS[level])

    if include_theater and level in THEATER_VERBS:
        # Add theater verbs, avoiding duplicates
        for v in THEATER_VERBS[level]:
            if v not in verbs:
                verbs.append(v)

    if count:
        return verbs[:count]
    return verbs


def select_verb(
    level: str,
    prefer_theater: bool = True,
    exclude: List[str] = None
) -> str:
    """
    Select a random appropriate verb for a level.

    Args:
        level: Bloom's taxonomy level
        prefer_theater: Prefer theater-specific verbs
        exclude: Verbs to exclude from selection

    Returns:
        Selected verb
    """
    level = level.lower()
    exclude = exclude or []

    if prefer_theater and level in THEATER_VERBS:
        candidates = [v for v in THEATER_VERBS[level] if v not in exclude]
        if candidates:
            return random.choice(candidates)

    candidates = [v for v in BLOOMS_VERBS.get(level, []) if v not in exclude]
    if candidates:
        return random.choice(candidates)

    raise ValueError(f"No verbs available for level {level} with given exclusions")


def classify_verb(verb: str) -> Dict[str, Any]:
    """
    Classify a verb by its Bloom's level(s).

    Args:
        verb: Verb to classify

    Returns:
        Classification result
    """
    verb_lower = verb.lower().strip()
    found_levels = []

    for level, verbs in BLOOMS_VERBS.items():
        if verb_lower in verbs:
            found_levels.append(level)

    # Check theater verbs too
    is_theater_verb = False
    for level, verbs in THEATER_VERBS.items():
        if verb_lower in verbs:
            is_theater_verb = True
            if level not in found_levels:
                found_levels.append(level)

    if not found_levels:
        return {
            'verb': verb,
            'found': False,
            'levels': [],
            'is_theater_verb': False,
            'recommendation': 'Consider using a standard Bloom\'s taxonomy verb'
        }

    # Primary level is the first (lowest/foundational)
    level_order = {l: i for i, l in enumerate(BLOOMS_LEVELS)}
    found_levels.sort(key=lambda x: level_order.get(x, 99))

    return {
        'verb': verb,
        'found': True,
        'levels': found_levels,
        'primary_level': found_levels[0],
        'is_theater_verb': is_theater_verb,
        'level_description': LEVEL_DESCRIPTIONS.get(found_levels[0], '')
    }


def validate_objective(
    objective: str,
    expected_level: str = None
) -> Dict[str, Any]:
    """
    Validate a learning objective for Bloom's compliance.

    Args:
        objective: Learning objective text
        expected_level: Expected Bloom's level (optional)

    Returns:
        Validation result
    """
    # Extract the first word (assumed to be the verb)
    words = objective.strip().split()
    if not words:
        return {
            'valid': False,
            'error': 'Empty objective'
        }

    # Handle common patterns
    verb = words[0].lower().rstrip('.,;:')

    # Check for "Students will..." pattern
    if verb in ['students', 'learners', 'the']:
        if len(words) > 2 and words[1].lower() == 'will':
            verb = words[2].lower().rstrip('.,;:')
        elif len(words) > 1:
            verb = words[1].lower().rstrip('.,;:')

    classification = classify_verb(verb)

    issues = []

    if not classification['found']:
        issues.append({
            'type': 'unknown_verb',
            'message': f'"{verb}" is not a recognized Bloom\'s taxonomy verb',
            'suggestion': 'Use a verb from the Bloom\'s taxonomy list'
        })

    if expected_level and classification['found']:
        if expected_level.lower() not in classification['levels']:
            issues.append({
                'type': 'level_mismatch',
                'message': f'Verb "{verb}" is level {classification["primary_level"]}, expected {expected_level}',
                'suggestion': f'Use a {expected_level}-level verb like: {", ".join(get_verbs_for_level(expected_level)[:5])}'
            })

    # Check for measurability
    vague_words = ['know', 'learn', 'appreciate', 'be aware', 'become familiar']
    if verb in vague_words:
        issues.append({
            'type': 'not_measurable',
            'message': f'"{verb}" is not measurable',
            'suggestion': 'Use a specific, observable verb'
        })

    return {
        'valid': len(issues) == 0,
        'objective': objective,
        'extracted_verb': verb,
        'classification': classification,
        'issues': issues,
        'is_measurable': verb not in vague_words and classification['found']
    }


def generate_objective(
    topic: str,
    level: str,
    prefer_theater: bool = True
) -> str:
    """
    Generate a sample learning objective.

    Args:
        topic: Topic for the objective
        level: Bloom's taxonomy level
        prefer_theater: Prefer theater-specific verbs

    Returns:
        Generated objective
    """
    verb = select_verb(level, prefer_theater=prefer_theater)

    # Capitalize first letter of verb
    verb_capitalized = verb.capitalize()

    # Generate based on level
    templates = {
        'remember': [
            f"{verb_capitalized} the key {topic}",
            f"{verb_capitalized} at least three {topic}",
            f"{verb_capitalized} the main components of {topic}"
        ],
        'understand': [
            f"{verb_capitalized} the relationship between {topic}",
            f"{verb_capitalized} how {topic} affects performance",
            f"{verb_capitalized} the significance of {topic}"
        ],
        'apply': [
            f"{verb_capitalized} {topic} in a performance context",
            f"{verb_capitalized} {topic} techniques in scene work",
            f"{verb_capitalized} understanding of {topic} through practice"
        ],
        'analyze': [
            f"{verb_capitalized} the elements of {topic}",
            f"{verb_capitalized} how {topic} contributes to theatrical effect",
            f"{verb_capitalized} the structure of {topic}"
        ],
        'evaluate': [
            f"{verb_capitalized} the effectiveness of {topic}",
            f"{verb_capitalized} different approaches to {topic}",
            f"{verb_capitalized} peer performances using {topic} criteria"
        ],
        'create': [
            f"{verb_capitalized} original work incorporating {topic}",
            f"{verb_capitalized} a scene that demonstrates {topic}",
            f"{verb_capitalized} blocking that reflects {topic} principles"
        ]
    }

    level_templates = templates.get(level.lower(), templates['understand'])
    return random.choice(level_templates)


def suggest_objectives_for_lesson(
    lesson_type: str,
    topic: str,
    count: int = 2
) -> List[Dict[str, Any]]:
    """
    Suggest learning objectives for a lesson type.

    Args:
        lesson_type: Type of lesson (introduction, content, workshop, etc.)
        topic: Lesson topic
        count: Number of objectives to generate

    Returns:
        List of suggested objectives with metadata
    """
    recommended_levels = LESSON_TYPE_LEVELS.get(
        lesson_type.lower(),
        ['understand', 'apply']
    )

    suggestions = []
    used_verbs = []

    for i in range(count):
        # Rotate through recommended levels
        level = recommended_levels[i % len(recommended_levels)]

        verb = select_verb(level, prefer_theater=True, exclude=used_verbs)
        used_verbs.append(verb)

        objective = generate_objective(topic, level)

        suggestions.append({
            'objective': objective,
            'level': level,
            'verb': verb,
            'is_theater_specific': verb in THEATER_VERBS.get(level, [])
        })

    return suggestions


def get_level_info(level: str) -> Dict[str, Any]:
    """
    Get detailed information about a Bloom's level.

    Args:
        level: Bloom's level name

    Returns:
        Level information
    """
    level = level.lower()
    if level not in BLOOMS_LEVELS:
        raise ValueError(f"Invalid level: {level}")

    level_index = BLOOMS_LEVELS.index(level)

    return {
        'level': level,
        'order': level_index + 1,
        'description': LEVEL_DESCRIPTIONS[level],
        'verbs': get_verbs_for_level(level, include_theater=False),
        'theater_verbs': THEATER_VERBS.get(level, []),
        'is_lower_order': level_index < 3,
        'is_higher_order': level_index >= 3
    }


if __name__ == "__main__":
    # Test
    print("Bloom's Verb Selector Test")
    print("=" * 50)

    # Test verb classification
    test_verbs = ['analyze', 'perform', 'choreograph', 'know', 'wiggle']
    print("\nVerb Classification:")
    for v in test_verbs:
        result = classify_verb(v)
        if result['found']:
            print(f"  '{v}': {result['primary_level']} (theater: {result['is_theater_verb']})")
        else:
            print(f"  '{v}': NOT FOUND")

    # Test objective validation
    print("\nObjective Validation:")
    test_objectives = [
        "Identify the parts of a Greek theater",
        "Know about Shakespeare",
        "Students will analyze the use of masks in Commedia"
    ]
    for obj in test_objectives:
        result = validate_objective(obj)
        status = "✓" if result['valid'] else "✗"
        print(f"  {status} {obj}")
        if not result['valid']:
            for issue in result['issues']:
                print(f"      - {issue['message']}")

    # Test objective generation
    print("\nGenerated Objectives for 'Greek theater masks':")
    for level in ['understand', 'apply', 'analyze']:
        obj = generate_objective('Greek theater masks', level)
        print(f"  [{level}] {obj}")
