"""
Bloom's Taxonomy Integrator (HARDCODED)
=======================================

Integrates Bloom's Taxonomy cognitive levels into lesson planning.
Ensures lessons address multiple cognitive levels for deeper learning.

HARDCODED RULES:
- R1: Each lesson must address at least 3 Bloom's levels
- R2: Lower levels (Remember, Understand) must precede higher levels
- R3: Learning objectives must use Bloom's action verbs
- R4: Assessment must align with objective Bloom's level
- R5: Activities must scaffold from lower to higher order thinking
"""

from typing import Any, Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum, IntEnum


# =============================================================================
# CONSTANTS (HARDCODED - DO NOT MODIFY)
# =============================================================================

MIN_BLOOM_LEVELS_PER_LESSON = 3
MAX_BLOOM_LEVELS_PER_LESSON = 6
REQUIRED_LOWER_LEVELS = 1  # Must have at least 1 lower-order thinking skill
REQUIRED_HIGHER_LEVELS = 1  # Must have at least 1 higher-order thinking skill


class BloomLevel(IntEnum):
    """Bloom's Taxonomy cognitive levels (revised)."""
    REMEMBER = 1     # Retrieve knowledge from memory
    UNDERSTAND = 2   # Construct meaning from information
    APPLY = 3        # Use procedures in a given situation
    ANALYZE = 4      # Break material into parts, determine relationships
    EVALUATE = 5     # Make judgments based on criteria
    CREATE = 6       # Put elements together to form new pattern


# Bloom's level descriptions and keywords
BLOOM_DEFINITIONS = {
    BloomLevel.REMEMBER: {
        "description": "Retrieve, recognize, and recall relevant knowledge from long-term memory",
        "question_stems": ["What is...?", "Who was...?", "When did...?", "List the...", "Define..."],
        "assessment_types": ["Quiz", "Matching", "Fill-in-blank", "Labeling", "Recall test"]
    },
    BloomLevel.UNDERSTAND: {
        "description": "Construct meaning from oral, written, and graphic messages",
        "question_stems": ["Explain why...", "Describe how...", "Summarize...", "What is the main idea?", "Compare..."],
        "assessment_types": ["Summary", "Paraphrase", "Classification", "Comparison chart", "Discussion"]
    },
    BloomLevel.APPLY: {
        "description": "Carry out or use a procedure in a given situation",
        "question_stems": ["How would you use...?", "Demonstrate...", "Apply... to...", "Show how..."],
        "assessment_types": ["Demonstration", "Role play", "Practice", "Simulation", "Performance"]
    },
    BloomLevel.ANALYZE: {
        "description": "Break material into constituent parts and determine relationships",
        "question_stems": ["What are the parts of...?", "How does... relate to...?", "What evidence...?", "Compare and contrast..."],
        "assessment_types": ["Analysis essay", "Graphic organizer", "Comparison", "Case study", "Investigation"]
    },
    BloomLevel.EVALUATE: {
        "description": "Make judgments based on criteria and standards",
        "question_stems": ["Do you agree...?", "What is your opinion...?", "Evaluate...", "Judge the value of...", "Critique..."],
        "assessment_types": ["Critique", "Review", "Debate", "Rubric-based assessment", "Peer evaluation"]
    },
    BloomLevel.CREATE: {
        "description": "Put elements together to form a coherent or functional whole; reorganize into a new pattern",
        "question_stems": ["Design a...", "Create...", "What would happen if...?", "Devise...", "Compose..."],
        "assessment_types": ["Original creation", "Design project", "Composition", "Production", "Portfolio"]
    }
}


# Action verbs by Bloom's level
BLOOM_VERBS = {
    BloomLevel.REMEMBER: [
        "define", "describe", "identify", "label", "list", "match", "name",
        "outline", "recall", "recognize", "reproduce", "select", "state"
    ],
    BloomLevel.UNDERSTAND: [
        "classify", "compare", "contrast", "demonstrate", "discuss", "distinguish",
        "explain", "express", "illustrate", "interpret", "paraphrase", "predict",
        "summarize", "translate"
    ],
    BloomLevel.APPLY: [
        "apply", "calculate", "change", "complete", "construct", "demonstrate",
        "discover", "dramatize", "employ", "examine", "experiment", "illustrate",
        "interpret", "manipulate", "modify", "operate", "practice", "relate",
        "schedule", "show", "sketch", "solve", "use", "write"
    ],
    BloomLevel.ANALYZE: [
        "analyze", "appraise", "break down", "calculate", "categorize", "classify",
        "compare", "contrast", "criticize", "diagram", "differentiate", "discriminate",
        "distinguish", "examine", "experiment", "identify", "infer", "investigate",
        "model", "outline", "question", "relate", "select", "separate", "subdivide"
    ],
    BloomLevel.EVALUATE: [
        "appraise", "argue", "assess", "choose", "compare", "conclude", "contrast",
        "criticize", "critique", "decide", "defend", "discriminate", "estimate",
        "evaluate", "explain", "grade", "interpret", "judge", "justify", "measure",
        "rank", "rate", "recommend", "relate", "select", "summarize", "support",
        "test", "value"
    ],
    BloomLevel.CREATE: [
        "arrange", "assemble", "build", "categorize", "combine", "compile", "compose",
        "construct", "create", "design", "develop", "devise", "establish", "formulate",
        "generate", "hypothesize", "imagine", "integrate", "invent", "make", "manage",
        "modify", "organize", "originate", "plan", "prepare", "produce", "propose",
        "rearrange", "reconstruct", "relate", "reorganize", "revise", "rewrite",
        "set up", "synthesize", "write"
    ]
}

# Theater-specific activities by Bloom's level
THEATER_BLOOM_ACTIVITIES = {
    BloomLevel.REMEMBER: [
        "Identify theater terminology",
        "List character names and relationships",
        "Recall plot sequence",
        "Define genre characteristics",
        "Name historical theater periods"
    ],
    BloomLevel.UNDERSTAND: [
        "Explain character motivation",
        "Summarize scene content",
        "Paraphrase Shakespeare to modern English",
        "Interpret stage directions",
        "Describe theatrical conventions"
    ],
    BloomLevel.APPLY: [
        "Demonstrate blocking techniques",
        "Practice vocal exercises",
        "Perform monologue with direction",
        "Apply character analysis to performance",
        "Use stage geography correctly"
    ],
    BloomLevel.ANALYZE: [
        "Analyze character development across scenes",
        "Compare directorial approaches",
        "Examine playwright's use of dramatic irony",
        "Investigate historical context effects on production",
        "Differentiate between theatrical styles"
    ],
    BloomLevel.EVALUATE: [
        "Critique a performance",
        "Evaluate blocking choices",
        "Judge effectiveness of directorial concept",
        "Assess peer performances using rubric",
        "Defend interpretation choices"
    ],
    BloomLevel.CREATE: [
        "Create original blocking",
        "Design character backstory",
        "Compose original monologue",
        "Develop directorial concept",
        "Devise ensemble scene"
    ]
}


@dataclass
class BloomObjective:
    """A learning objective classified by Bloom's level."""
    objective_text: str
    bloom_level: BloomLevel
    action_verb: str
    assessment_aligned: bool
    suggested_assessment: str


@dataclass
class BloomIntegrationPlan:
    """Complete Bloom's integration for a lesson."""
    lesson_topic: str
    objectives_by_level: Dict[BloomLevel, List[BloomObjective]]
    level_coverage: List[BloomLevel]
    progression_valid: bool
    total_objectives: int
    lower_order_count: int
    higher_order_count: int


# =============================================================================
# GENERATOR FUNCTIONS
# =============================================================================

def classify_objective(objective_text: str) -> Tuple[BloomLevel, str]:
    """
    Classify a learning objective by its Bloom's level.

    Args:
        objective_text: The learning objective text

    Returns:
        Tuple of (BloomLevel, action_verb found)
    """
    objective_lower = objective_text.lower()

    # Check each level starting from highest (most specific)
    for level in reversed(list(BloomLevel)):
        verbs = BLOOM_VERBS[level]
        for verb in verbs:
            if objective_lower.startswith(verb) or f" {verb} " in objective_lower:
                return level, verb

    # Default to Understand if no clear verb found
    return BloomLevel.UNDERSTAND, "understand"


def generate_bloom_objectives(
    topic: str,
    existing_objectives: List[str],
    target_levels: List[BloomLevel] = None
) -> List[BloomObjective]:
    """
    Generate or enhance objectives to meet Bloom's requirements.

    Args:
        topic: Lesson topic
        existing_objectives: Existing learning objectives
        target_levels: Specific Bloom's levels to target

    Returns:
        List of BloomObjective with level classifications
    """
    objectives = []

    # Classify existing objectives
    for obj_text in existing_objectives:
        level, verb = classify_objective(obj_text)
        assessment = _suggest_assessment(level)

        objectives.append(BloomObjective(
            objective_text=obj_text,
            bloom_level=level,
            action_verb=verb,
            assessment_aligned=True,
            suggested_assessment=assessment
        ))

    # Check level coverage
    levels_covered = {obj.bloom_level for obj in objectives}

    # Ensure minimum levels are covered
    if target_levels:
        needed_levels = set(target_levels) - levels_covered
    else:
        # Default: ensure at least one lower and one higher order
        needed_levels = set()
        if not any(l <= BloomLevel.APPLY for l in levels_covered):
            needed_levels.add(BloomLevel.UNDERSTAND)
        if not any(l >= BloomLevel.ANALYZE for l in levels_covered):
            needed_levels.add(BloomLevel.ANALYZE)

    # Generate objectives for needed levels
    for level in needed_levels:
        verb = BLOOM_VERBS[level][0]
        obj_text = _generate_objective_for_level(topic, level, verb)
        assessment = _suggest_assessment(level)

        objectives.append(BloomObjective(
            objective_text=obj_text,
            bloom_level=level,
            action_verb=verb,
            assessment_aligned=True,
            suggested_assessment=assessment
        ))

    return sorted(objectives, key=lambda x: x.bloom_level)


def generate_bloom_integration_plan(
    lesson_topic: str,
    learning_objectives: List[str]
) -> BloomIntegrationPlan:
    """
    Generate a complete Bloom's integration plan for a lesson.

    Args:
        lesson_topic: The lesson topic
        learning_objectives: List of learning objectives

    Returns:
        BloomIntegrationPlan with level analysis
    """
    # Generate enhanced objectives
    bloom_objectives = generate_bloom_objectives(lesson_topic, learning_objectives)

    # Organize by level
    by_level: Dict[BloomLevel, List[BloomObjective]] = {level: [] for level in BloomLevel}
    for obj in bloom_objectives:
        by_level[obj.bloom_level].append(obj)

    # Calculate coverage
    levels_covered = [level for level in BloomLevel if by_level[level]]
    lower_count = sum(1 for obj in bloom_objectives if obj.bloom_level <= BloomLevel.APPLY)
    higher_count = sum(1 for obj in bloom_objectives if obj.bloom_level >= BloomLevel.ANALYZE)

    # Check progression validity
    progression_valid = _check_progression(bloom_objectives)

    return BloomIntegrationPlan(
        lesson_topic=lesson_topic,
        objectives_by_level=by_level,
        level_coverage=levels_covered,
        progression_valid=progression_valid,
        total_objectives=len(bloom_objectives),
        lower_order_count=lower_count,
        higher_order_count=higher_count
    )


def _generate_objective_for_level(topic: str, level: BloomLevel, verb: str) -> str:
    """Generate an objective for a specific Bloom's level."""
    templates = {
        BloomLevel.REMEMBER: f"{verb.capitalize()} key terms and concepts related to {topic}",
        BloomLevel.UNDERSTAND: f"{verb.capitalize()} the significance of {topic} in theatrical context",
        BloomLevel.APPLY: f"{verb.capitalize()} techniques of {topic} in practical exercises",
        BloomLevel.ANALYZE: f"{verb.capitalize()} the components and relationships within {topic}",
        BloomLevel.EVALUATE: f"{verb.capitalize()} the effectiveness of {topic} using established criteria",
        BloomLevel.CREATE: f"{verb.capitalize()} original work incorporating principles of {topic}"
    }
    return templates.get(level, f"{verb.capitalize()} {topic}")


def _suggest_assessment(level: BloomLevel) -> str:
    """Suggest an assessment type for a Bloom's level."""
    assessments = BLOOM_DEFINITIONS[level]["assessment_types"]
    return assessments[0] if assessments else "Observation"


def _check_progression(objectives: List[BloomObjective]) -> bool:
    """Check if objectives follow appropriate progression."""
    if not objectives:
        return True

    # Should have lower levels before introducing higher levels
    levels = [obj.bloom_level for obj in objectives]
    has_foundation = any(l <= BloomLevel.UNDERSTAND for l in levels)
    return has_foundation


def get_bloom_verbs_for_level(level: BloomLevel) -> List[str]:
    """Get action verbs for a specific Bloom's level."""
    return BLOOM_VERBS.get(level, [])


def get_theater_activities_for_level(level: BloomLevel) -> List[str]:
    """Get theater-specific activities for a Bloom's level."""
    return THEATER_BLOOM_ACTIVITIES.get(level, [])


def suggest_activity_for_objective(objective: BloomObjective) -> str:
    """Suggest a theater activity based on objective's Bloom's level."""
    activities = THEATER_BLOOM_ACTIVITIES.get(objective.bloom_level, [])
    return activities[0] if activities else "Guided practice activity"


# =============================================================================
# VALIDATION FUNCTIONS
# =============================================================================

def validate_bloom_integration(plan: BloomIntegrationPlan) -> Dict[str, Any]:
    """
    Validate Bloom's integration against hardcoded rules.

    Returns:
        Dictionary with validation status and any issues
    """
    issues = []
    warnings = []

    # R1: Check level coverage
    if len(plan.level_coverage) < MIN_BLOOM_LEVELS_PER_LESSON:
        issues.append({
            "rule": "R1",
            "message": f"Insufficient Bloom's levels: {len(plan.level_coverage)} (minimum: {MIN_BLOOM_LEVELS_PER_LESSON})"
        })

    # R2: Check lower levels precede higher
    if not plan.progression_valid:
        issues.append({
            "rule": "R2",
            "message": "Objectives don't follow Remember/Understand foundation before higher-order skills"
        })

    # R3: Check action verbs
    for level, objs in plan.objectives_by_level.items():
        for obj in objs:
            if obj.action_verb not in BLOOM_VERBS.get(level, []):
                warnings.append({
                    "rule": "R3",
                    "message": f"Verb '{obj.action_verb}' may not align with {level.name} level"
                })

    # R5: Check lower and higher order balance
    if plan.lower_order_count < REQUIRED_LOWER_LEVELS:
        issues.append({
            "rule": "R5",
            "message": f"Need at least {REQUIRED_LOWER_LEVELS} lower-order objective (Remember/Understand/Apply)"
        })
    if plan.higher_order_count < REQUIRED_HIGHER_LEVELS:
        issues.append({
            "rule": "R5",
            "message": f"Need at least {REQUIRED_HIGHER_LEVELS} higher-order objective (Analyze/Evaluate/Create)"
        })

    return {
        "valid": len(issues) == 0,
        "issues": issues,
        "warnings": warnings,
        "levels_covered": [l.name for l in plan.level_coverage],
        "total_objectives": plan.total_objectives,
        "lower_order_count": plan.lower_order_count,
        "higher_order_count": plan.higher_order_count
    }


def has_valid_bloom_integration(plan: BloomIntegrationPlan) -> bool:
    """Quick check if Bloom's integration is valid."""
    result = validate_bloom_integration(plan)
    return result["valid"]


def bloom_plan_to_dict(plan: BloomIntegrationPlan) -> Dict[str, Any]:
    """Convert Bloom's plan to dictionary for JSON serialization."""
    return {
        "lesson_topic": plan.lesson_topic,
        "level_coverage": [l.name for l in plan.level_coverage],
        "progression_valid": plan.progression_valid,
        "total_objectives": plan.total_objectives,
        "lower_order_count": plan.lower_order_count,
        "higher_order_count": plan.higher_order_count,
        "objectives_by_level": {
            level.name: [
                {
                    "text": obj.objective_text,
                    "verb": obj.action_verb,
                    "assessment": obj.suggested_assessment
                }
                for obj in objs
            ]
            for level, objs in plan.objectives_by_level.items()
            if objs
        }
    }
