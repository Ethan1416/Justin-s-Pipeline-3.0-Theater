"""
Formative Activities Generator (HARDCODED)
==========================================

Generates formative assessment activities that check for understanding
during instruction. These are low-stakes assessments used to monitor
student learning and adjust teaching in real-time.

HARDCODED RULES:
- R1: Each lesson must include at least 2 formative checks
- R2: Formative activities must be aligned to learning objectives
- R3: Each formative check must have clear success criteria
- R4: Formative activities must provide immediate feedback opportunity
- R5: Variety of formative types required (not all same type)
"""

from typing import Any, Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum


# =============================================================================
# CONSTANTS (HARDCODED - DO NOT MODIFY)
# =============================================================================

MIN_FORMATIVE_CHECKS_PER_LESSON = 2
MAX_FORMATIVE_CHECKS_PER_LESSON = 5
REQUIRED_FORMATIVE_COMPONENTS = ["prompt", "success_criteria", "feedback_method", "objective_alignment"]


class FormativeType(Enum):
    """Types of formative assessment."""
    QUICK_CHECK = "quick_check"           # 30-second understanding check
    EXIT_SLIP = "exit_slip"               # End-of-class check
    THINK_PAIR_SHARE = "think_pair_share" # Collaborative discussion
    THUMBS_CHECK = "thumbs_check"         # Visual understanding signal
    WHITEBOARD = "whiteboard"             # Written response
    GALLERY_WALK = "gallery_walk"         # Movement-based review
    TURN_AND_TALK = "turn_and_talk"       # Partner discussion
    FIST_TO_FIVE = "fist_to_five"         # Self-rating scale
    ONE_MINUTE_PAPER = "one_minute_paper" # Quick written reflection
    MUDDIEST_POINT = "muddiest_point"     # Confusion identification
    TICKET_OUT = "ticket_out"             # Exit verification
    COLD_CALL = "cold_call"               # Random selection response
    CHORAL_RESPONSE = "choral_response"   # Whole-class response


class FeedbackMethod(Enum):
    """Methods for providing feedback on formative assessment."""
    IMMEDIATE_VERBAL = "immediate_verbal"
    PEER_FEEDBACK = "peer_feedback"
    SELF_CHECK = "self_check"
    TEACHER_CIRCULATION = "teacher_circulation"
    CLASS_DISCUSSION = "class_discussion"
    VISUAL_DISPLAY = "visual_display"


# Formative activity templates by type
FORMATIVE_TEMPLATES = {
    FormativeType.QUICK_CHECK: {
        "description": "Quick understanding check requiring immediate response",
        "duration_seconds": 30,
        "ideal_for": ["vocabulary", "concept recall", "procedure steps"],
        "example_prompts": [
            "What is the term for...?",
            "True or false: ...",
            "Which of these is an example of...?"
        ]
    },
    FormativeType.THINK_PAIR_SHARE: {
        "description": "Individual thinking, partner discussion, class share",
        "duration_seconds": 180,
        "ideal_for": ["analysis", "interpretation", "application"],
        "example_prompts": [
            "How would you apply this to...?",
            "What connections do you see between...?",
            "Why do you think the character...?"
        ]
    },
    FormativeType.THUMBS_CHECK: {
        "description": "Visual signal of understanding level",
        "duration_seconds": 15,
        "ideal_for": ["pacing check", "concept clarity", "ready to move on"],
        "example_prompts": [
            "Thumbs up if you can explain..., sideways if you need clarification, down if you need help",
            "Show me your confidence level for..."
        ]
    },
    FormativeType.WHITEBOARD: {
        "description": "Written response on individual whiteboards",
        "duration_seconds": 60,
        "ideal_for": ["vocabulary", "short answers", "problem solving"],
        "example_prompts": [
            "Write the definition of...",
            "List three examples of...",
            "Draw a quick diagram showing..."
        ]
    },
    FormativeType.TURN_AND_TALK: {
        "description": "Brief partner discussion on focused question",
        "duration_seconds": 90,
        "ideal_for": ["processing", "clarification", "prediction"],
        "example_prompts": [
            "Tell your partner one thing you learned about...",
            "Discuss with your neighbor: What might happen if...?",
            "Explain to your partner the difference between..."
        ]
    },
    FormativeType.FIST_TO_FIVE: {
        "description": "Self-rating scale from 0 (fist) to 5 (five fingers)",
        "duration_seconds": 15,
        "ideal_for": ["confidence check", "self-assessment", "readiness"],
        "example_prompts": [
            "Rate your understanding of... from fist to five",
            "How confident are you that you can...?"
        ]
    },
    FormativeType.ONE_MINUTE_PAPER: {
        "description": "Brief written response to focused prompt",
        "duration_seconds": 60,
        "ideal_for": ["synthesis", "reflection", "key takeaways"],
        "example_prompts": [
            "What was the most important thing you learned today?",
            "Summarize today's concept in one sentence",
            "What question do you still have?"
        ]
    },
    FormativeType.MUDDIEST_POINT: {
        "description": "Identify most confusing aspect of lesson",
        "duration_seconds": 45,
        "ideal_for": ["confusion identification", "lesson adjustment", "clarity check"],
        "example_prompts": [
            "What is still unclear about...?",
            "What part of today's lesson confused you most?"
        ]
    },
    FormativeType.GALLERY_WALK: {
        "description": "Movement-based review of displayed work",
        "duration_seconds": 300,
        "ideal_for": ["peer learning", "example analysis", "comparison"],
        "example_prompts": [
            "As you walk, note one thing you learned from others",
            "Find an example that shows... and be ready to share why"
        ]
    },
    FormativeType.COLD_CALL: {
        "description": "Random selection of student to respond",
        "duration_seconds": 30,
        "ideal_for": ["accountability", "attention check", "individual thinking"],
        "example_prompts": [
            "Student name, can you tell us...?",
            "I'm going to randomly select someone to explain..."
        ]
    },
    FormativeType.CHORAL_RESPONSE: {
        "description": "Whole class responds simultaneously",
        "duration_seconds": 10,
        "ideal_for": ["vocabulary", "definitions", "quick facts"],
        "example_prompts": [
            "Everyone, what do we call...?",
            "On three, tell me the name for..."
        ]
    }
}

# Theater-specific formative activities
THEATER_FORMATIVE_ACTIVITIES = {
    "character_check": {
        "type": FormativeType.QUICK_CHECK,
        "prompt_template": "What is {character}'s motivation in this scene?",
        "theater_application": "Character analysis understanding"
    },
    "blocking_thumbs": {
        "type": FormativeType.THUMBS_CHECK,
        "prompt_template": "Do you understand why the character moves {direction}?",
        "theater_application": "Blocking comprehension"
    },
    "term_whiteboard": {
        "type": FormativeType.WHITEBOARD,
        "prompt_template": "Write the definition of '{term}' in theater terms",
        "theater_application": "Vocabulary reinforcement"
    },
    "scene_analysis_tps": {
        "type": FormativeType.THINK_PAIR_SHARE,
        "prompt_template": "How does the playwright use {technique} in this scene?",
        "theater_application": "Script analysis skills"
    },
    "performance_fist_to_five": {
        "type": FormativeType.FIST_TO_FIVE,
        "prompt_template": "Rate your confidence in performing {skill}",
        "theater_application": "Performance readiness"
    }
}


@dataclass
class FormativeActivity:
    """A single formative assessment activity."""
    formative_type: FormativeType
    prompt: str
    success_criteria: List[str]
    feedback_method: FeedbackMethod
    duration_seconds: int
    objective_alignment: str
    when_to_use: str  # "during_lecture", "after_activity", "end_of_class"
    materials_needed: List[str] = field(default_factory=list)
    teacher_script: str = ""
    follow_up_if_low: str = ""


@dataclass
class FormativeAssessmentPlan:
    """Complete formative assessment plan for a lesson."""
    lesson_topic: str
    learning_objectives: List[str]
    formative_activities: List[FormativeActivity]
    timing_distribution: Dict[str, int]  # When formatives occur
    variety_check: bool  # Different types used


# =============================================================================
# GENERATOR FUNCTIONS
# =============================================================================

def generate_formative_plan(
    lesson_topic: str,
    learning_objectives: List[str],
    lesson_duration_minutes: int = 56,
    lecture_duration_minutes: int = 15
) -> FormativeAssessmentPlan:
    """
    Generate a complete formative assessment plan for a lesson.

    Args:
        lesson_topic: The topic of the lesson
        learning_objectives: List of learning objectives
        lesson_duration_minutes: Total lesson duration
        lecture_duration_minutes: Duration of lecture portion

    Returns:
        FormativeAssessmentPlan with multiple formative checks
    """
    formatives = []
    types_used = set()

    # Formative 1: During lecture (quick check)
    during_lecture = generate_formative_activity(
        objective=learning_objectives[0] if learning_objectives else "Understand key concepts",
        context="during_lecture",
        topic=lesson_topic,
        excluded_types=types_used
    )
    formatives.append(during_lecture)
    types_used.add(during_lecture.formative_type)

    # Formative 2: After modeling (understanding check)
    if len(learning_objectives) > 1:
        obj = learning_objectives[1]
    else:
        obj = learning_objectives[0] if learning_objectives else "Apply concepts"

    after_modeling = generate_formative_activity(
        objective=obj,
        context="after_modeling",
        topic=lesson_topic,
        excluded_types=types_used
    )
    formatives.append(after_modeling)
    types_used.add(after_modeling.formative_type)

    # Formative 3: During activity (progress check)
    during_activity = generate_formative_activity(
        objective=obj,
        context="during_activity",
        topic=lesson_topic,
        excluded_types=types_used
    )
    formatives.append(during_activity)
    types_used.add(during_activity.formative_type)

    # Calculate timing distribution
    timing = {
        "during_lecture": sum(1 for f in formatives if f.when_to_use == "during_lecture"),
        "after_activity": sum(1 for f in formatives if f.when_to_use in ["after_modeling", "during_activity"]),
        "end_of_class": sum(1 for f in formatives if f.when_to_use == "end_of_class")
    }

    return FormativeAssessmentPlan(
        lesson_topic=lesson_topic,
        learning_objectives=learning_objectives,
        formative_activities=formatives,
        timing_distribution=timing,
        variety_check=len(types_used) >= 2
    )


def generate_formative_activity(
    objective: str,
    context: str,
    topic: str,
    excluded_types: set = None
) -> FormativeActivity:
    """
    Generate a single formative activity.

    Args:
        objective: Learning objective to assess
        context: When this will be used (during_lecture, after_modeling, etc.)
        topic: Lesson topic
        excluded_types: Types already used (for variety)

    Returns:
        FormativeActivity object
    """
    excluded_types = excluded_types or set()

    # Select appropriate type based on context
    if context == "during_lecture":
        preferred_types = [FormativeType.THUMBS_CHECK, FormativeType.QUICK_CHECK,
                         FormativeType.FIST_TO_FIVE, FormativeType.CHORAL_RESPONSE]
    elif context == "after_modeling":
        preferred_types = [FormativeType.THINK_PAIR_SHARE, FormativeType.TURN_AND_TALK,
                         FormativeType.WHITEBOARD]
    elif context == "during_activity":
        preferred_types = [FormativeType.TURN_AND_TALK, FormativeType.COLD_CALL,
                         FormativeType.QUICK_CHECK]
    else:
        preferred_types = [FormativeType.ONE_MINUTE_PAPER, FormativeType.MUDDIEST_POINT,
                         FormativeType.TICKET_OUT]

    # Select type not yet used
    selected_type = None
    for ft in preferred_types:
        if ft not in excluded_types:
            selected_type = ft
            break

    if selected_type is None:
        selected_type = preferred_types[0]  # Default to first preferred

    template = FORMATIVE_TEMPLATES[selected_type]

    # Generate prompt based on objective
    prompt = _generate_prompt(selected_type, objective, topic)

    # Generate success criteria
    success_criteria = _generate_success_criteria(selected_type, objective)

    # Select feedback method
    feedback_method = _select_feedback_method(selected_type)

    return FormativeActivity(
        formative_type=selected_type,
        prompt=prompt,
        success_criteria=success_criteria,
        feedback_method=feedback_method,
        duration_seconds=template["duration_seconds"],
        objective_alignment=objective,
        when_to_use=context,
        materials_needed=_get_materials(selected_type),
        teacher_script=_generate_teacher_script(selected_type, prompt),
        follow_up_if_low=_generate_follow_up(selected_type, topic)
    )


def _generate_prompt(
    formative_type: FormativeType,
    objective: str,
    topic: str
) -> str:
    """Generate a prompt for the formative activity."""
    templates = {
        FormativeType.QUICK_CHECK: f"Based on what we just learned about {topic}, {objective.lower().replace('students will', 'can you')}?",
        FormativeType.THUMBS_CHECK: f"Show me thumbs up if you understand how to {objective.lower().replace('students will', '').strip()}, sideways if you need clarification.",
        FormativeType.THINK_PAIR_SHARE: f"Think about how you would {objective.lower().replace('students will', '').strip()}. Share your thinking with a partner.",
        FormativeType.TURN_AND_TALK: f"Turn to your neighbor and explain one key thing about {topic}.",
        FormativeType.WHITEBOARD: f"On your whiteboard, write one example of {topic}.",
        FormativeType.FIST_TO_FIVE: f"Rate your confidence: How ready are you to {objective.lower().replace('students will', '').strip()}?",
        FormativeType.ONE_MINUTE_PAPER: f"In one minute, write what you learned about {topic} today.",
        FormativeType.MUDDIEST_POINT: f"What is still confusing about {topic}?",
        FormativeType.CHORAL_RESPONSE: f"Everyone, tell me: What is the term for {topic}?",
        FormativeType.COLD_CALL: f"[Name], can you tell us about {topic}?"
    }
    return templates.get(formative_type, f"Check understanding of {topic}")


def _generate_success_criteria(formative_type: FormativeType, objective: str) -> List[str]:
    """Generate success criteria for the formative activity."""
    base_criteria = [
        "Students demonstrate understanding of the concept",
        "Responses align with learning objective"
    ]

    type_specific = {
        FormativeType.THUMBS_CHECK: ["80%+ show thumbs up"],
        FormativeType.THINK_PAIR_SHARE: ["Partners actively discuss", "Students can explain to class"],
        FormativeType.WHITEBOARD: ["Written responses are accurate", "All students participate"],
        FormativeType.FIST_TO_FIVE: ["Average rating is 3 or higher"]
    }

    return base_criteria + type_specific.get(formative_type, [])


def _select_feedback_method(formative_type: FormativeType) -> FeedbackMethod:
    """Select appropriate feedback method for formative type."""
    method_mapping = {
        FormativeType.QUICK_CHECK: FeedbackMethod.IMMEDIATE_VERBAL,
        FormativeType.THUMBS_CHECK: FeedbackMethod.VISUAL_DISPLAY,
        FormativeType.THINK_PAIR_SHARE: FeedbackMethod.CLASS_DISCUSSION,
        FormativeType.TURN_AND_TALK: FeedbackMethod.TEACHER_CIRCULATION,
        FormativeType.WHITEBOARD: FeedbackMethod.VISUAL_DISPLAY,
        FormativeType.FIST_TO_FIVE: FeedbackMethod.IMMEDIATE_VERBAL,
        FormativeType.ONE_MINUTE_PAPER: FeedbackMethod.TEACHER_CIRCULATION,
        FormativeType.GALLERY_WALK: FeedbackMethod.PEER_FEEDBACK
    }
    return method_mapping.get(formative_type, FeedbackMethod.IMMEDIATE_VERBAL)


def _get_materials(formative_type: FormativeType) -> List[str]:
    """Get materials needed for formative activity."""
    materials = {
        FormativeType.WHITEBOARD: ["Individual whiteboards", "Markers", "Erasers"],
        FormativeType.ONE_MINUTE_PAPER: ["Paper/index cards", "Pencils"],
        FormativeType.GALLERY_WALK: ["Posted work", "Sticky notes for feedback"]
    }
    return materials.get(formative_type, [])


def _generate_teacher_script(formative_type: FormativeType, prompt: str) -> str:
    """Generate teacher script for administering the formative."""
    intro = {
        FormativeType.THUMBS_CHECK: "I'm going to check for understanding. When I count to three, show me...",
        FormativeType.THINK_PAIR_SHARE: "Take 30 seconds to think on your own, then turn to a partner...",
        FormativeType.WHITEBOARD: "Get your whiteboards ready. On my signal, show me...",
        FormativeType.FIST_TO_FIVE: "Using fist to five, show me..."
    }
    return f"{intro.get(formative_type, 'Let me check your understanding.')}\n{prompt}"


def _generate_follow_up(formative_type: FormativeType, topic: str) -> str:
    """Generate follow-up action if formative shows low understanding."""
    return f"If understanding is low, pause and reteach the concept of {topic} using a different example or approach."


# =============================================================================
# VALIDATION FUNCTIONS
# =============================================================================

def validate_formative_plan(plan: FormativeAssessmentPlan) -> Dict[str, Any]:
    """
    Validate a formative assessment plan against hardcoded rules.

    Returns:
        Dictionary with validation status and any issues
    """
    issues = []
    warnings = []

    # R1: Check formative count
    count = len(plan.formative_activities)
    if count < MIN_FORMATIVE_CHECKS_PER_LESSON:
        issues.append({
            "rule": "R1",
            "message": f"Insufficient formative checks: {count} (minimum: {MIN_FORMATIVE_CHECKS_PER_LESSON})"
        })
    if count > MAX_FORMATIVE_CHECKS_PER_LESSON:
        warnings.append({
            "rule": "R1",
            "message": f"Many formative checks: {count} (recommended max: {MAX_FORMATIVE_CHECKS_PER_LESSON})"
        })

    # R2: Check objective alignment
    for i, activity in enumerate(plan.formative_activities):
        if not activity.objective_alignment:
            issues.append({
                "rule": "R2",
                "message": f"Formative {i+1} not aligned to an objective"
            })

    # R3: Check success criteria
    for i, activity in enumerate(plan.formative_activities):
        if not activity.success_criteria:
            issues.append({
                "rule": "R3",
                "message": f"Formative {i+1} missing success criteria"
            })

    # R4: Check feedback method
    for i, activity in enumerate(plan.formative_activities):
        if not activity.feedback_method:
            issues.append({
                "rule": "R4",
                "message": f"Formative {i+1} missing feedback method"
            })

    # R5: Check variety
    if not plan.variety_check:
        warnings.append({
            "rule": "R5",
            "message": "Limited variety in formative types - consider using different types"
        })

    return {
        "valid": len(issues) == 0,
        "issues": issues,
        "warnings": warnings,
        "formative_count": count,
        "variety_achieved": plan.variety_check
    }


def has_valid_formatives(plan: FormativeAssessmentPlan) -> bool:
    """Quick check if formative plan is valid."""
    result = validate_formative_plan(plan)
    return result["valid"]


def formative_plan_to_dict(plan: FormativeAssessmentPlan) -> Dict[str, Any]:
    """Convert a formative plan to dictionary for JSON serialization."""
    return {
        "lesson_topic": plan.lesson_topic,
        "learning_objectives": plan.learning_objectives,
        "timing_distribution": plan.timing_distribution,
        "variety_check": plan.variety_check,
        "formative_activities": [
            {
                "type": f.formative_type.value,
                "prompt": f.prompt,
                "success_criteria": f.success_criteria,
                "feedback_method": f.feedback_method.value,
                "duration_seconds": f.duration_seconds,
                "objective_alignment": f.objective_alignment,
                "when_to_use": f.when_to_use,
                "materials_needed": f.materials_needed,
                "teacher_script": f.teacher_script,
                "follow_up_if_low": f.follow_up_if_low
            }
            for f in plan.formative_activities
        ]
    }
