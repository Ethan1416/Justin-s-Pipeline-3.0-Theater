"""
Instruction Integration Agent (HARDCODED)
==========================================

Integrates all instructional components to ensure coherent lesson flow.
Combines scaffolding, formative assessment, Bloom's, and DOK frameworks
into a unified instructional sequence.

HARDCODED RULES:
- R1: Lecture must frontload content before activities
- R2: Activities must apply concepts introduced in lecture
- R3: Scaffolding must progress from high to low support
- R4: Formative checks must align with learning objectives
- R5: Reading activities must be included for text-based lessons
- R6: Lesson must follow I Do, We Do, You Do structure
"""

from typing import Any, Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum

from .scaffolding_generator import (
    ScaffoldingPlan, Scaffold, SupportLevel,
    generate_scaffolding_plan, validate_scaffolding_plan
)
from .formative_activities_generator import (
    FormativeAssessmentPlan, FormativeActivity,
    generate_formative_plan, validate_formative_plan
)
from .blooms_taxonomy_integrator import (
    BloomIntegrationPlan, BloomLevel,
    generate_bloom_integration_plan, validate_bloom_integration
)
from .webbs_dok_integrator import (
    DOKIntegrationPlan, DOKLevel,
    generate_dok_integration_plan, validate_dok_integration
)


# =============================================================================
# CONSTANTS (HARDCODED - DO NOT MODIFY)
# =============================================================================

# Lecture duration range (in minutes)
MIN_LECTURE_DURATION = 5
MAX_LECTURE_DURATION = 20
DEFAULT_LECTURE_DURATION = 15

# Activity requirements
MIN_ACTIVITIES_PER_LESSON = 1
READING_REQUIRED_FOR_SHAKESPEARE = True

# Instructional phases
REQUIRED_PHASES = ["frontload", "guided_practice", "independent_practice", "assessment"]


class InstructionalPhase(Enum):
    """Phases of instruction."""
    FRONTLOAD = "frontload"           # Lecture introduces concepts
    MODELING = "modeling"             # Teacher demonstrates
    GUIDED_PRACTICE = "guided"        # We do together
    COLLABORATIVE = "collaborative"   # You do together
    INDEPENDENT = "independent"       # You do alone
    ASSESSMENT = "assessment"         # Check for mastery


class ActivityType(Enum):
    """Types of instructional activities."""
    READING = "reading"
    DISCUSSION = "discussion"
    PERFORMANCE = "performance"
    WRITING = "writing"
    ANALYSIS = "analysis"
    CREATIVE = "creative"
    PHYSICAL = "physical"


# Romeo and Juliet 6-week coverage structure
ROMEO_AND_JULIET_STRUCTURE = {
    "total_weeks": 6,
    "total_days": 30,  # 5 days per week
    "acts": {
        1: {"days": 5, "focus": ["Prologue", "Scene 1-5"], "reading_required": True},
        2: {"days": 5, "focus": ["Scene 1-6", "Balcony Scene"], "reading_required": True},
        3: {"days": 6, "focus": ["Scene 1-5", "Fight Scene", "Banishment"], "reading_required": True},
        4: {"days": 5, "focus": ["Scene 1-5", "Potion Plan"], "reading_required": True},
        5: {"days": 5, "focus": ["Scene 1-3", "Tomb Scene", "Resolution"], "reading_required": True},
        "performance": {"days": 4, "focus": ["Scene Performance", "Final Project"], "reading_required": False}
    },
    "reading_activities": [
        "Shared reading with annotation",
        "Close reading with discussion",
        "Partner reading with roles",
        "Independent reading with response",
        "Choral reading for verse",
        "Readers theater performance"
    ]
}


@dataclass
class ReadingActivity:
    """A reading activity component."""
    reading_type: str
    text_reference: str
    duration_minutes: int
    purpose: str
    supports: List[str]
    follow_up: str


@dataclass
class LectureComponent:
    """Lecture component with frontloading."""
    topic: str
    duration_minutes: int
    key_concepts: List[str]
    vocabulary_frontload: List[str]
    connects_to_activity: str
    frontloading_strategy: str


@dataclass
class IntegratedLesson:
    """Fully integrated lesson plan."""
    lesson_topic: str
    unit_name: str
    day_number: int
    learning_objectives: List[str]

    # Lecture (frontloads activity)
    lecture: LectureComponent

    # Scaffolding plan
    scaffolding: ScaffoldingPlan

    # Formative assessment plan
    formatives: FormativeAssessmentPlan

    # Bloom's integration
    blooms: BloomIntegrationPlan

    # DOK integration
    dok: DOKIntegrationPlan

    # Reading activity (if applicable)
    reading_activity: Optional[ReadingActivity]

    # Activity details
    main_activity: Dict[str, Any]

    # Phase sequence
    phase_sequence: List[InstructionalPhase]

    # Validation status
    integration_valid: bool


# =============================================================================
# GENERATOR FUNCTIONS
# =============================================================================

def generate_integrated_lesson(
    lesson_topic: str,
    unit_name: str,
    day_number: int,
    learning_objectives: List[str],
    activity_description: str,
    lecture_duration_minutes: int = DEFAULT_LECTURE_DURATION,
    include_reading: bool = True,
    text_reference: str = ""
) -> IntegratedLesson:
    """
    Generate a fully integrated lesson with all instructional components.

    Args:
        lesson_topic: The topic of the lesson
        unit_name: Name of the unit (e.g., "Shakespeare")
        day_number: Day number within unit
        learning_objectives: List of learning objectives
        activity_description: Description of the main activity
        lecture_duration_minutes: Duration of lecture (5-20 minutes)
        include_reading: Whether to include a reading activity
        text_reference: Text being studied (e.g., "Romeo and Juliet Act 2 Scene 2")

    Returns:
        IntegratedLesson with all components
    """
    # Validate lecture duration
    lecture_duration = max(MIN_LECTURE_DURATION, min(MAX_LECTURE_DURATION, lecture_duration_minutes))

    # Generate lecture component with frontloading
    lecture = generate_lecture_component(
        topic=lesson_topic,
        duration=lecture_duration,
        activity_to_frontload=activity_description,
        objectives=learning_objectives
    )

    # Generate scaffolding plan
    scaffolding = generate_scaffolding_plan(
        lesson_topic=lesson_topic,
        content_type=_determine_content_type(activity_description),
        learning_objectives=learning_objectives,
        total_duration_minutes=lecture_duration + 15  # Include activity time
    )

    # Generate formative plan
    formatives = generate_formative_plan(
        lesson_topic=lesson_topic,
        learning_objectives=learning_objectives,
        lecture_duration_minutes=lecture_duration
    )

    # Generate Bloom's integration
    blooms = generate_bloom_integration_plan(
        lesson_topic=lesson_topic,
        learning_objectives=learning_objectives
    )

    # Generate DOK integration
    dok_activities = [{"description": activity_description, "duration_minutes": 15}]
    dok = generate_dok_integration_plan(
        lesson_topic=lesson_topic,
        activities=dok_activities
    )

    # Generate reading activity if needed
    reading_activity = None
    if include_reading and text_reference:
        reading_activity = generate_reading_activity(
            text_reference=text_reference,
            lesson_topic=lesson_topic,
            duration_minutes=10
        )

    # Build phase sequence
    phase_sequence = build_phase_sequence(
        has_reading=reading_activity is not None,
        scaffolding=scaffolding
    )

    # Build main activity dict
    main_activity = {
        "description": activity_description,
        "duration_minutes": 15,
        "type": _determine_content_type(activity_description),
        "frontloaded_by_lecture": True
    }

    # Create integrated lesson
    lesson = IntegratedLesson(
        lesson_topic=lesson_topic,
        unit_name=unit_name,
        day_number=day_number,
        learning_objectives=learning_objectives,
        lecture=lecture,
        scaffolding=scaffolding,
        formatives=formatives,
        blooms=blooms,
        dok=dok,
        reading_activity=reading_activity,
        main_activity=main_activity,
        phase_sequence=phase_sequence,
        integration_valid=True  # Will be validated
    )

    # Validate integration
    validation = validate_integrated_lesson(lesson)
    lesson.integration_valid = validation["valid"]

    return lesson


def generate_lecture_component(
    topic: str,
    duration: int,
    activity_to_frontload: str,
    objectives: List[str]
) -> LectureComponent:
    """
    Generate a lecture component that frontloads the activity.

    Args:
        topic: Lecture topic
        duration: Duration in minutes (5-20)
        activity_to_frontload: Activity that follows the lecture
        objectives: Learning objectives

    Returns:
        LectureComponent with frontloading strategy
    """
    # Extract key concepts from objectives
    key_concepts = [_extract_concept(obj) for obj in objectives[:3]]

    # Determine vocabulary to frontload
    vocabulary = _extract_vocabulary(topic, activity_to_frontload)

    # Determine frontloading strategy
    strategy = _determine_frontloading_strategy(activity_to_frontload)

    return LectureComponent(
        topic=topic,
        duration_minutes=duration,
        key_concepts=key_concepts,
        vocabulary_frontload=vocabulary,
        connects_to_activity=activity_to_frontload,
        frontloading_strategy=strategy
    )


def generate_reading_activity(
    text_reference: str,
    lesson_topic: str,
    duration_minutes: int = 10
) -> ReadingActivity:
    """
    Generate a reading activity for text-based lessons.

    Args:
        text_reference: Text being read (e.g., "Romeo and Juliet Act 2 Scene 2")
        lesson_topic: Topic of the lesson
        duration_minutes: Time allocated for reading

    Returns:
        ReadingActivity object
    """
    # Determine reading type based on text
    if "shakespeare" in lesson_topic.lower() or "romeo" in text_reference.lower():
        reading_type = "Shared reading with modern translation support"
        supports = [
            "Side-by-side modern translation",
            "Vocabulary glossary",
            "Character tracking chart",
            "Line-by-line annotation guide"
        ]
    else:
        reading_type = "Close reading with annotation"
        supports = [
            "Annotation guide",
            "Vocabulary support",
            "Discussion questions"
        ]

    return ReadingActivity(
        reading_type=reading_type,
        text_reference=text_reference,
        duration_minutes=duration_minutes,
        purpose=f"Build understanding of {lesson_topic} through textual analysis",
        supports=supports,
        follow_up="Discussion and application of reading content"
    )


def generate_romeo_juliet_unit_plan(
    start_day: int = 1
) -> List[Dict[str, Any]]:
    """
    Generate a 6-week unit plan for Romeo and Juliet.

    Args:
        start_day: Starting day number

    Returns:
        List of lesson plans for 30 days
    """
    lessons = []
    current_day = start_day

    for act_num, act_info in ROMEO_AND_JULIET_STRUCTURE["acts"].items():
        if act_num == "performance":
            continue

        for i in range(act_info["days"]):
            focus = act_info["focus"][min(i, len(act_info["focus"])-1)]

            lesson = {
                "day": current_day,
                "week": (current_day - 1) // 5 + 1,
                "act": act_num,
                "focus": focus,
                "text_reference": f"Romeo and Juliet Act {act_num}",
                "reading_required": act_info["reading_required"],
                "reading_activity": ROMEO_AND_JULIET_STRUCTURE["reading_activities"][i % len(ROMEO_AND_JULIET_STRUCTURE["reading_activities"])],
                "suggested_activity": _get_shakespeare_activity(act_num, i)
            }
            lessons.append(lesson)
            current_day += 1

    # Add performance days
    perf_info = ROMEO_AND_JULIET_STRUCTURE["acts"]["performance"]
    for i in range(perf_info["days"]):
        lesson = {
            "day": current_day,
            "week": 6,
            "act": "performance",
            "focus": perf_info["focus"][min(i, len(perf_info["focus"])-1)],
            "text_reference": "Selected scenes",
            "reading_required": False,
            "reading_activity": None,
            "suggested_activity": "Scene performance and feedback"
        }
        lessons.append(lesson)
        current_day += 1

    return lessons


def _get_shakespeare_activity(act: int, day_in_act: int) -> str:
    """Get suggested activity for Shakespeare unit."""
    activities = [
        "Close reading with annotation",
        "Character motivation analysis",
        "Blocking and staging exploration",
        "Language analysis (verse/prose)",
        "Scene performance preparation"
    ]
    return activities[day_in_act % len(activities)]


def build_phase_sequence(
    has_reading: bool,
    scaffolding: ScaffoldingPlan
) -> List[InstructionalPhase]:
    """Build the instructional phase sequence."""
    phases = [InstructionalPhase.FRONTLOAD]

    if has_reading:
        phases.append(InstructionalPhase.MODELING)

    for scaffold in scaffolding.scaffolds:
        if scaffold.level == SupportLevel.MODELED:
            if InstructionalPhase.MODELING not in phases:
                phases.append(InstructionalPhase.MODELING)
        elif scaffold.level == SupportLevel.GUIDED:
            phases.append(InstructionalPhase.GUIDED_PRACTICE)
        elif scaffold.level == SupportLevel.COLLABORATIVE:
            phases.append(InstructionalPhase.COLLABORATIVE)
        elif scaffold.level == SupportLevel.INDEPENDENT:
            phases.append(InstructionalPhase.INDEPENDENT)

    phases.append(InstructionalPhase.ASSESSMENT)

    return phases


def _determine_content_type(activity_description: str) -> str:
    """Determine content type from activity description."""
    desc_lower = activity_description.lower()

    if any(w in desc_lower for w in ["read", "annotate", "text"]):
        return "reading"
    elif any(w in desc_lower for w in ["discuss", "debate", "conversation"]):
        return "discussion"
    elif any(w in desc_lower for w in ["perform", "scene", "monologue"]):
        return "performance"
    elif any(w in desc_lower for w in ["write", "compose", "draft"]):
        return "writing"
    elif any(w in desc_lower for w in ["analyze", "examine", "compare"]):
        return "analysis"
    else:
        return "analysis"


def _extract_concept(objective: str) -> str:
    """Extract key concept from objective."""
    # Remove common objective starters
    starters = ["students will", "learners will", "swbat", "the student will"]
    obj_lower = objective.lower()
    for starter in starters:
        if obj_lower.startswith(starter):
            return objective[len(starter):].strip().capitalize()
    return objective


def _extract_vocabulary(topic: str, activity: str) -> List[str]:
    """Extract vocabulary to frontload based on topic and activity."""
    # Theater-specific vocabulary by topic area
    vocab_bank = {
        "shakespeare": ["iambic pentameter", "soliloquy", "aside", "verse", "prose"],
        "character": ["motivation", "objective", "subtext", "given circumstances"],
        "blocking": ["upstage", "downstage", "stage left", "stage right", "cross"],
        "performance": ["projection", "articulation", "physicality", "presence"],
        "analysis": ["theme", "conflict", "dramatic irony", "foreshadowing"]
    }

    vocab = []
    combined = (topic + " " + activity).lower()

    for category, words in vocab_bank.items():
        if category in combined:
            vocab.extend(words[:3])

    return vocab[:5] if vocab else ["key term 1", "key term 2", "key term 3"]


def _determine_frontloading_strategy(activity: str) -> str:
    """Determine frontloading strategy based on activity type."""
    strategies = {
        "reading": "Introduce vocabulary and context before reading",
        "discussion": "Present key concepts and discussion framework",
        "performance": "Demonstrate techniques before practice",
        "writing": "Model writing process with examples",
        "analysis": "Explain analytical framework with guided example"
    }

    content_type = _determine_content_type(activity)
    return strategies.get(content_type, "Present key concepts before application")


# =============================================================================
# VALIDATION FUNCTIONS
# =============================================================================

def validate_integrated_lesson(lesson: IntegratedLesson) -> Dict[str, Any]:
    """
    Validate integrated lesson against hardcoded rules.

    Returns:
        Dictionary with validation status and any issues
    """
    issues = []
    warnings = []

    # R1: Check lecture frontloads activity
    if not lesson.lecture.frontloading_strategy:
        issues.append({
            "rule": "R1",
            "message": "Lecture must have frontloading strategy for activity"
        })

    # R2: Check activity applies lecture concepts
    if not lesson.lecture.connects_to_activity:
        issues.append({
            "rule": "R2",
            "message": "Activity must apply concepts from lecture"
        })

    # R3: Validate scaffolding progression
    scaff_result = validate_scaffolding_plan(lesson.scaffolding)
    if not scaff_result["valid"]:
        issues.extend([{"rule": "R3", "message": i["message"]} for i in scaff_result["issues"]])

    # R4: Validate formative alignment
    form_result = validate_formative_plan(lesson.formatives)
    if not form_result["valid"]:
        issues.extend([{"rule": "R4", "message": i["message"]} for i in form_result["issues"]])

    # R5: Check reading for Shakespeare
    if "shakespeare" in lesson.unit_name.lower() and not lesson.reading_activity:
        warnings.append({
            "rule": "R5",
            "message": "Shakespeare unit should include reading activity"
        })

    # R6: Check I Do, We Do, You Do structure
    required_phases = {InstructionalPhase.FRONTLOAD, InstructionalPhase.INDEPENDENT, InstructionalPhase.ASSESSMENT}
    if not required_phases.issubset(set(lesson.phase_sequence)):
        warnings.append({
            "rule": "R6",
            "message": "Lesson should include frontload, independent practice, and assessment phases"
        })

    # Validate Bloom's
    bloom_result = validate_bloom_integration(lesson.blooms)
    if not bloom_result["valid"]:
        warnings.extend([{"rule": "Bloom's", "message": i["message"]} for i in bloom_result["issues"]])

    # Validate DOK
    dok_result = validate_dok_integration(lesson.dok)
    if not dok_result["valid"]:
        warnings.extend([{"rule": "DOK", "message": i["message"]} for i in dok_result["issues"]])

    # Check lecture duration
    if lesson.lecture.duration_minutes < MIN_LECTURE_DURATION:
        issues.append({
            "rule": "Duration",
            "message": f"Lecture too short: {lesson.lecture.duration_minutes} min (minimum: {MIN_LECTURE_DURATION})"
        })
    if lesson.lecture.duration_minutes > MAX_LECTURE_DURATION:
        issues.append({
            "rule": "Duration",
            "message": f"Lecture too long: {lesson.lecture.duration_minutes} min (maximum: {MAX_LECTURE_DURATION})"
        })

    return {
        "valid": len(issues) == 0,
        "issues": issues,
        "warnings": warnings,
        "scaffolding_valid": scaff_result["valid"],
        "formatives_valid": form_result["valid"],
        "blooms_valid": bloom_result["valid"],
        "dok_valid": dok_result["valid"],
        "has_reading": lesson.reading_activity is not None,
        "lecture_duration": lesson.lecture.duration_minutes,
        "phase_count": len(lesson.phase_sequence)
    }


def has_valid_integration(lesson: IntegratedLesson) -> bool:
    """Quick check if lesson integration is valid."""
    result = validate_integrated_lesson(lesson)
    return result["valid"]


def integrated_lesson_to_dict(lesson: IntegratedLesson) -> Dict[str, Any]:
    """Convert integrated lesson to dictionary for JSON serialization."""
    from .scaffolding_generator import scaffolding_plan_to_dict
    from .formative_activities_generator import formative_plan_to_dict
    from .blooms_taxonomy_integrator import bloom_plan_to_dict
    from .webbs_dok_integrator import dok_plan_to_dict

    return {
        "lesson_topic": lesson.lesson_topic,
        "unit_name": lesson.unit_name,
        "day_number": lesson.day_number,
        "learning_objectives": lesson.learning_objectives,
        "lecture": {
            "topic": lesson.lecture.topic,
            "duration_minutes": lesson.lecture.duration_minutes,
            "key_concepts": lesson.lecture.key_concepts,
            "vocabulary_frontload": lesson.lecture.vocabulary_frontload,
            "connects_to_activity": lesson.lecture.connects_to_activity,
            "frontloading_strategy": lesson.lecture.frontloading_strategy
        },
        "scaffolding": scaffolding_plan_to_dict(lesson.scaffolding),
        "formatives": formative_plan_to_dict(lesson.formatives),
        "blooms": bloom_plan_to_dict(lesson.blooms),
        "dok": dok_plan_to_dict(lesson.dok),
        "reading_activity": {
            "type": lesson.reading_activity.reading_type,
            "text": lesson.reading_activity.text_reference,
            "duration": lesson.reading_activity.duration_minutes,
            "purpose": lesson.reading_activity.purpose,
            "supports": lesson.reading_activity.supports,
            "follow_up": lesson.reading_activity.follow_up
        } if lesson.reading_activity else None,
        "main_activity": lesson.main_activity,
        "phase_sequence": [p.value for p in lesson.phase_sequence],
        "integration_valid": lesson.integration_valid
    }
