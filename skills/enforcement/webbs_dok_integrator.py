"""
Webb's Depth of Knowledge (DOK) Integrator (HARDCODED)
=====================================================

Integrates Webb's Depth of Knowledge framework into lesson planning.
DOK focuses on the complexity of thinking required, not difficulty.

HARDCODED RULES:
- R1: Each lesson must address at least 2 DOK levels
- R2: DOK Level 1 foundations required before Level 3-4 tasks
- R3: Activities must specify DOK level and justification
- R4: Assessment complexity must match instruction complexity
- R5: Extended thinking (DOK 4) should be included when time allows
"""

from typing import Any, Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from enum import IntEnum


# =============================================================================
# CONSTANTS (HARDCODED - DO NOT MODIFY)
# =============================================================================

MIN_DOK_LEVELS_PER_LESSON = 2
MAX_DOK_LEVELS_PER_LESSON = 4
REQUIRED_DOK_FOUNDATION = True  # Must have DOK 1 or 2 before 3-4


class DOKLevel(IntEnum):
    """Webb's Depth of Knowledge Levels."""
    RECALL = 1           # Recall and Reproduction
    SKILL_CONCEPT = 2    # Skills and Concepts
    STRATEGIC = 3        # Strategic Thinking
    EXTENDED = 4         # Extended Thinking


# DOK level definitions
DOK_DEFINITIONS = {
    DOKLevel.RECALL: {
        "name": "Recall and Reproduction",
        "description": "Recall a fact, information, or procedure",
        "complexity": "Low",
        "time_typical": "Less than a class period",
        "keywords": [
            "recall", "recognize", "identify", "locate", "list", "define",
            "memorize", "repeat", "state", "quote", "name", "label"
        ],
        "characteristics": [
            "Automatic response",
            "One correct answer",
            "No decision making",
            "Simple recall of information"
        ]
    },
    DOKLevel.SKILL_CONCEPT: {
        "name": "Skills and Concepts",
        "description": "Use information or conceptual knowledge; requires two or more steps",
        "complexity": "Moderate",
        "time_typical": "Lesson to few days",
        "keywords": [
            "summarize", "interpret", "classify", "organize", "compare",
            "contrast", "infer", "predict", "categorize", "identify patterns",
            "estimate", "observe", "collect", "display"
        ],
        "characteristics": [
            "Requires some mental processing",
            "May involve multiple steps",
            "Requires deciding how to approach",
            "Some flexibility in process"
        ]
    },
    DOKLevel.STRATEGIC: {
        "name": "Strategic Thinking",
        "description": "Requires reasoning, developing a plan, and more complex thinking",
        "complexity": "High",
        "time_typical": "Days to weeks",
        "keywords": [
            "analyze", "critique", "differentiate", "assess", "investigate",
            "develop argument", "draw conclusions", "construct meaning",
            "formulate", "synthesize", "evaluate", "hypothesize", "revise"
        ],
        "characteristics": [
            "Requires reasoning and justification",
            "Abstract thinking required",
            "Multiple valid approaches",
            "Requires evidence and explanation"
        ]
    },
    DOKLevel.EXTENDED: {
        "name": "Extended Thinking",
        "description": "Requires complex reasoning over time; synthesis across content areas",
        "complexity": "Very High",
        "time_typical": "Weeks to months",
        "keywords": [
            "design", "create", "synthesize", "apply concepts in new context",
            "critique", "prove", "connect", "transfer", "research", "investigate",
            "develop", "produce"
        ],
        "characteristics": [
            "Requires investigation over time",
            "Makes connections across ideas",
            "Selects and uses multiple approaches",
            "Self-directed learning"
        ]
    }
}

# Theater-specific DOK activities
THEATER_DOK_ACTIVITIES = {
    DOKLevel.RECALL: [
        "Define stage areas (upstage, downstage, etc.)",
        "List the elements of a monologue",
        "Name the stock characters in Commedia",
        "Identify Shakespeare's use of verse vs. prose",
        "Recall blocking symbols"
    ],
    DOKLevel.SKILL_CONCEPT: [
        "Summarize a scene in your own words",
        "Compare two characters' motivations",
        "Categorize characters by their function in the plot",
        "Organize the plot structure of a play",
        "Interpret the subtext of a line"
    ],
    DOKLevel.STRATEGIC: [
        "Analyze how staging choices affect audience interpretation",
        "Develop a character's backstory based on textual evidence",
        "Evaluate the effectiveness of a directorial choice",
        "Construct an argument for a specific interpretation",
        "Synthesize research into a director's concept"
    ],
    DOKLevel.EXTENDED: [
        "Design and direct a scene with full justification",
        "Create an original one-act play",
        "Research and present on a theater movement's historical context",
        "Develop a full production concept with multiple elements",
        "Connect a classical play to contemporary issues through adaptation"
    ]
}

# DOK level descriptors for theater
THEATER_DOK_DESCRIPTORS = {
    DOKLevel.RECALL: "Students recall or locate theater terminology, facts, or procedures",
    DOKLevel.SKILL_CONCEPT: "Students demonstrate understanding of theater concepts through application",
    DOKLevel.STRATEGIC: "Students analyze, evaluate, or create theater work requiring justification",
    DOKLevel.EXTENDED: "Students synthesize theater learning across extended time with original work"
}


@dataclass
class DOKActivity:
    """An activity classified by DOK level."""
    activity_description: str
    dok_level: DOKLevel
    justification: str
    time_required_minutes: int
    complexity_indicators: List[str]
    prerequisite_skills: List[str] = field(default_factory=list)


@dataclass
class DOKIntegrationPlan:
    """Complete DOK integration for a lesson."""
    lesson_topic: str
    activities_by_level: Dict[DOKLevel, List[DOKActivity]]
    level_coverage: List[DOKLevel]
    foundation_present: bool  # Has DOK 1 or 2
    strategic_present: bool   # Has DOK 3 or 4
    total_activities: int
    complexity_progression: bool


# =============================================================================
# GENERATOR FUNCTIONS
# =============================================================================

def classify_activity_dok(
    activity_description: str,
    time_minutes: int = 15
) -> Tuple[DOKLevel, str]:
    """
    Classify an activity by its DOK level.

    Args:
        activity_description: Description of the activity
        time_minutes: Time allocated for activity

    Returns:
        Tuple of (DOKLevel, justification)
    """
    description_lower = activity_description.lower()

    # Check for extended thinking indicators
    if time_minutes >= 45 or any(kw in description_lower for kw in ["design", "create", "research", "develop concept"]):
        if any(kw in description_lower for kw in DOK_DEFINITIONS[DOKLevel.EXTENDED]["keywords"]):
            return DOKLevel.EXTENDED, "Requires extended time and synthesis across concepts"

    # Check for strategic thinking
    for keyword in DOK_DEFINITIONS[DOKLevel.STRATEGIC]["keywords"]:
        if keyword in description_lower:
            return DOKLevel.STRATEGIC, f"Requires strategic thinking: {keyword}"

    # Check for skill/concept
    for keyword in DOK_DEFINITIONS[DOKLevel.SKILL_CONCEPT]["keywords"]:
        if keyword in description_lower:
            return DOKLevel.SKILL_CONCEPT, f"Applies skills and concepts: {keyword}"

    # Check for recall
    for keyword in DOK_DEFINITIONS[DOKLevel.RECALL]["keywords"]:
        if keyword in description_lower:
            return DOKLevel.RECALL, f"Recalls information: {keyword}"

    # Default based on time
    if time_minutes <= 5:
        return DOKLevel.RECALL, "Brief activity suggests recall level"
    elif time_minutes <= 15:
        return DOKLevel.SKILL_CONCEPT, "Moderate time suggests skill application"
    else:
        return DOKLevel.STRATEGIC, "Extended time suggests strategic thinking required"


def generate_dok_activities(
    topic: str,
    target_levels: List[DOKLevel] = None,
    total_time_minutes: int = 45
) -> List[DOKActivity]:
    """
    Generate DOK-aligned activities for a lesson.

    Args:
        topic: Lesson topic
        target_levels: Specific DOK levels to include
        total_time_minutes: Total activity time available

    Returns:
        List of DOKActivity objects
    """
    if target_levels is None:
        # Default: include at least DOK 1, 2, and 3
        target_levels = [DOKLevel.RECALL, DOKLevel.SKILL_CONCEPT, DOKLevel.STRATEGIC]

    activities = []
    time_per_level = total_time_minutes // len(target_levels)

    for level in sorted(target_levels):
        activity = generate_dok_activity(topic, level, time_per_level)
        activities.append(activity)

    return activities


def generate_dok_activity(
    topic: str,
    level: DOKLevel,
    time_minutes: int
) -> DOKActivity:
    """
    Generate a single DOK-aligned activity.

    Args:
        topic: Lesson topic
        level: Target DOK level
        time_minutes: Time allocated

    Returns:
        DOKActivity object
    """
    # Get sample activities for level
    theater_activities = THEATER_DOK_ACTIVITIES.get(level, [])

    # Generate description
    description = _generate_activity_description(topic, level, theater_activities)

    # Get complexity indicators
    complexity = DOK_DEFINITIONS[level]["characteristics"]

    # Determine prerequisites
    prerequisites = []
    if level >= DOKLevel.SKILL_CONCEPT:
        prerequisites.append(f"Understanding of basic {topic} terminology")
    if level >= DOKLevel.STRATEGIC:
        prerequisites.append(f"Ability to apply {topic} concepts")
    if level == DOKLevel.EXTENDED:
        prerequisites.append(f"Experience analyzing {topic} in context")

    return DOKActivity(
        activity_description=description,
        dok_level=level,
        justification=THEATER_DOK_DESCRIPTORS[level],
        time_required_minutes=time_minutes,
        complexity_indicators=complexity,
        prerequisite_skills=prerequisites
    )


def _generate_activity_description(
    topic: str,
    level: DOKLevel,
    sample_activities: List[str]
) -> str:
    """Generate an activity description for a DOK level."""
    templates = {
        DOKLevel.RECALL: f"Identify and define key terms related to {topic}",
        DOKLevel.SKILL_CONCEPT: f"Compare and contrast different approaches to {topic}",
        DOKLevel.STRATEGIC: f"Analyze the effectiveness of {topic} techniques and justify your conclusions",
        DOKLevel.EXTENDED: f"Design and develop an original work applying principles of {topic}"
    }
    return templates.get(level, f"Explore {topic}")


def generate_dok_integration_plan(
    lesson_topic: str,
    activities: List[Dict[str, Any]],
    include_extended: bool = False
) -> DOKIntegrationPlan:
    """
    Generate a complete DOK integration plan.

    Args:
        lesson_topic: The lesson topic
        activities: List of activity dictionaries
        include_extended: Whether to include DOK 4 activities

    Returns:
        DOKIntegrationPlan with level analysis
    """
    dok_activities = []

    # Classify existing activities
    for activity in activities:
        description = activity.get("description", activity.get("name", ""))
        time_mins = activity.get("duration_minutes", 15)
        level, justification = classify_activity_dok(description, time_mins)

        dok_activities.append(DOKActivity(
            activity_description=description,
            dok_level=level,
            justification=justification,
            time_required_minutes=time_mins,
            complexity_indicators=DOK_DEFINITIONS[level]["characteristics"],
            prerequisite_skills=[]
        ))

    # Organize by level
    by_level: Dict[DOKLevel, List[DOKActivity]] = {level: [] for level in DOKLevel}
    for activity in dok_activities:
        by_level[activity.dok_level].append(activity)

    # Calculate coverage
    levels_covered = [level for level in DOKLevel if by_level[level]]
    foundation_present = any(l <= DOKLevel.SKILL_CONCEPT for l in levels_covered)
    strategic_present = any(l >= DOKLevel.STRATEGIC for l in levels_covered)

    # Check progression
    complexity_progression = _check_dok_progression(dok_activities)

    return DOKIntegrationPlan(
        lesson_topic=lesson_topic,
        activities_by_level=by_level,
        level_coverage=levels_covered,
        foundation_present=foundation_present,
        strategic_present=strategic_present,
        total_activities=len(dok_activities),
        complexity_progression=complexity_progression
    )


def _check_dok_progression(activities: List[DOKActivity]) -> bool:
    """Check if activities follow appropriate DOK progression."""
    if not activities:
        return True

    # Sort by when they appear (assuming order matters)
    levels = [a.dok_level for a in activities]

    # Should have foundation before strategic
    first_strategic_idx = next((i for i, l in enumerate(levels) if l >= DOKLevel.STRATEGIC), len(levels))
    has_foundation_before = any(l <= DOKLevel.SKILL_CONCEPT for l in levels[:first_strategic_idx])

    return has_foundation_before or first_strategic_idx == len(levels)


def get_dok_keywords(level: DOKLevel) -> List[str]:
    """Get keywords associated with a DOK level."""
    return DOK_DEFINITIONS[level]["keywords"]


def get_theater_activities_for_dok(level: DOKLevel) -> List[str]:
    """Get theater-specific activities for a DOK level."""
    return THEATER_DOK_ACTIVITIES.get(level, [])


def suggest_dok_level_for_time(time_minutes: int) -> DOKLevel:
    """Suggest appropriate DOK level based on available time."""
    if time_minutes < 10:
        return DOKLevel.RECALL
    elif time_minutes < 20:
        return DOKLevel.SKILL_CONCEPT
    elif time_minutes < 45:
        return DOKLevel.STRATEGIC
    else:
        return DOKLevel.EXTENDED


# =============================================================================
# VALIDATION FUNCTIONS
# =============================================================================

def validate_dok_integration(plan: DOKIntegrationPlan) -> Dict[str, Any]:
    """
    Validate DOK integration against hardcoded rules.

    Returns:
        Dictionary with validation status and any issues
    """
    issues = []
    warnings = []

    # R1: Check level coverage
    if len(plan.level_coverage) < MIN_DOK_LEVELS_PER_LESSON:
        issues.append({
            "rule": "R1",
            "message": f"Insufficient DOK levels: {len(plan.level_coverage)} (minimum: {MIN_DOK_LEVELS_PER_LESSON})"
        })

    # R2: Check foundation before strategic
    if plan.strategic_present and not plan.foundation_present:
        issues.append({
            "rule": "R2",
            "message": "DOK 3-4 activities present without DOK 1-2 foundation"
        })

    # R3: Check activity justifications
    for level, activities in plan.activities_by_level.items():
        for activity in activities:
            if not activity.justification:
                warnings.append({
                    "rule": "R3",
                    "message": f"Activity missing DOK justification: {activity.activity_description[:30]}..."
                })

    # R5: Check for extended thinking opportunity
    if DOKLevel.EXTENDED not in plan.level_coverage and plan.total_activities >= 3:
        warnings.append({
            "rule": "R5",
            "message": "Consider including DOK 4 (Extended Thinking) for deeper learning"
        })

    # Check complexity progression
    if not plan.complexity_progression:
        warnings.append({
            "rule": "R2",
            "message": "Activities may not follow optimal complexity progression"
        })

    return {
        "valid": len(issues) == 0,
        "issues": issues,
        "warnings": warnings,
        "levels_covered": [l.name for l in plan.level_coverage],
        "foundation_present": plan.foundation_present,
        "strategic_present": plan.strategic_present,
        "total_activities": plan.total_activities
    }


def has_valid_dok_integration(plan: DOKIntegrationPlan) -> bool:
    """Quick check if DOK integration is valid."""
    result = validate_dok_integration(plan)
    return result["valid"]


def dok_plan_to_dict(plan: DOKIntegrationPlan) -> Dict[str, Any]:
    """Convert DOK plan to dictionary for JSON serialization."""
    return {
        "lesson_topic": plan.lesson_topic,
        "level_coverage": [l.name for l in plan.level_coverage],
        "foundation_present": plan.foundation_present,
        "strategic_present": plan.strategic_present,
        "complexity_progression": plan.complexity_progression,
        "total_activities": plan.total_activities,
        "activities_by_level": {
            level.name: [
                {
                    "description": a.activity_description,
                    "justification": a.justification,
                    "time_minutes": a.time_required_minutes,
                    "complexity_indicators": a.complexity_indicators,
                    "prerequisites": a.prerequisite_skills
                }
                for a in activities
            ]
            for level, activities in plan.activities_by_level.items()
            if activities
        }
    }
