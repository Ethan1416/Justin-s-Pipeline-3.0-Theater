"""
Scaffolding Generator (HARDCODED)
=================================

Generates scaffolding strategies for lesson content.
Scaffolding breaks down complex learning into manageable steps,
providing temporary supports that are gradually removed.

HARDCODED RULES:
- R1: Each lesson must have 2-4 scaffolding levels
- R2: Scaffolds must progress from high-support to low-support
- R3: Each scaffold must include teacher actions and student actions
- R4: Scaffolds must align with learning objectives
- R5: Gradual release model required (I do, We do, You do)
"""

from typing import Any, Dict, List, Optional
from dataclasses import dataclass, field
from enum import Enum


# =============================================================================
# CONSTANTS (HARDCODED - DO NOT MODIFY)
# =============================================================================

MIN_SCAFFOLDS_PER_LESSON = 2
MAX_SCAFFOLDS_PER_LESSON = 4
REQUIRED_SCAFFOLD_COMPONENTS = ["teacher_action", "student_action", "support_level", "transition_cue"]

class SupportLevel(Enum):
    """Support levels from highest to lowest."""
    MODELED = "modeled"           # Teacher demonstrates fully (I do)
    GUIDED = "guided"             # Teacher leads, students follow (We do together)
    COLLABORATIVE = "collaborative"  # Students work together with teacher support
    INDEPENDENT = "independent"   # Students work alone (You do)


# Gradual Release Model Phases
GRADUAL_RELEASE_PHASES = {
    SupportLevel.MODELED: {
        "name": "I Do",
        "description": "Teacher models the skill or concept explicitly",
        "teacher_role": "Demonstrator",
        "student_role": "Observer/Active listener",
        "typical_duration_percent": 20
    },
    SupportLevel.GUIDED: {
        "name": "We Do Together",
        "description": "Teacher and students work through examples together",
        "teacher_role": "Guide/Facilitator",
        "student_role": "Participator",
        "typical_duration_percent": 30
    },
    SupportLevel.COLLABORATIVE: {
        "name": "You Do Together",
        "description": "Students work collaboratively with peer support",
        "teacher_role": "Monitor/Coach",
        "student_role": "Collaborator",
        "typical_duration_percent": 25
    },
    SupportLevel.INDEPENDENT: {
        "name": "You Do Alone",
        "description": "Students demonstrate mastery independently",
        "teacher_role": "Assessor",
        "student_role": "Independent practitioner",
        "typical_duration_percent": 25
    }
}

# Scaffold templates by content type
SCAFFOLD_TEMPLATES = {
    "reading": {
        SupportLevel.MODELED: "Teacher reads aloud with think-aloud annotations",
        SupportLevel.GUIDED: "Shared reading with student participation in analysis",
        SupportLevel.COLLABORATIVE: "Partner reading with discussion protocol",
        SupportLevel.INDEPENDENT: "Independent reading with annotation task"
    },
    "performance": {
        SupportLevel.MODELED: "Teacher demonstrates technique with explanation",
        SupportLevel.GUIDED: "Class rehearses technique with teacher coaching",
        SupportLevel.COLLABORATIVE: "Small groups practice with peer feedback",
        SupportLevel.INDEPENDENT: "Individual performance with self-assessment"
    },
    "analysis": {
        SupportLevel.MODELED: "Teacher models analytical process step-by-step",
        SupportLevel.GUIDED: "Class analyzes together with guided questions",
        SupportLevel.COLLABORATIVE: "Groups complete analysis with graphic organizer",
        SupportLevel.INDEPENDENT: "Independent analysis with written response"
    },
    "writing": {
        SupportLevel.MODELED: "Teacher composes while thinking aloud",
        SupportLevel.GUIDED: "Collaborative drafting with sentence starters",
        SupportLevel.COLLABORATIVE: "Peer writing and revision partners",
        SupportLevel.INDEPENDENT: "Independent composition"
    },
    "discussion": {
        SupportLevel.MODELED: "Teacher models discussion protocol",
        SupportLevel.GUIDED: "Fishbowl discussion with teacher facilitation",
        SupportLevel.COLLABORATIVE: "Small group discussions with roles",
        SupportLevel.INDEPENDENT: "Student-led discussions"
    }
}


@dataclass
class Scaffold:
    """A single scaffolding step."""
    level: SupportLevel
    description: str
    teacher_action: str
    student_action: str
    duration_minutes: int
    supports_provided: List[str] = field(default_factory=list)
    transition_cue: str = ""
    materials_needed: List[str] = field(default_factory=list)
    differentiation_notes: str = ""


@dataclass
class ScaffoldingPlan:
    """Complete scaffolding plan for a lesson."""
    lesson_topic: str
    content_type: str
    scaffolds: List[Scaffold]
    total_duration_minutes: int
    objectives_addressed: List[str]
    gradual_release_complete: bool


# =============================================================================
# GENERATOR FUNCTIONS
# =============================================================================

def generate_scaffolding_plan(
    lesson_topic: str,
    content_type: str,
    learning_objectives: List[str],
    total_duration_minutes: int,
    activity_description: str = ""
) -> ScaffoldingPlan:
    """
    Generate a complete scaffolding plan for a lesson.

    Args:
        lesson_topic: The topic of the lesson
        content_type: Type of content (reading, performance, analysis, writing, discussion)
        learning_objectives: List of learning objectives to address
        total_duration_minutes: Total time available for scaffolded instruction
        activity_description: Optional description of the main activity

    Returns:
        ScaffoldingPlan with 2-4 scaffolds following gradual release model
    """
    # Validate content type
    if content_type not in SCAFFOLD_TEMPLATES:
        content_type = "analysis"  # Default to analysis template

    # Determine number of scaffolds based on duration
    if total_duration_minutes <= 10:
        num_scaffolds = 2
    elif total_duration_minutes <= 15:
        num_scaffolds = 3
    else:
        num_scaffolds = 4

    # Ensure within bounds
    num_scaffolds = max(MIN_SCAFFOLDS_PER_LESSON, min(MAX_SCAFFOLDS_PER_LESSON, num_scaffolds))

    # Select scaffold levels based on count
    if num_scaffolds == 2:
        levels = [SupportLevel.MODELED, SupportLevel.INDEPENDENT]
    elif num_scaffolds == 3:
        levels = [SupportLevel.MODELED, SupportLevel.GUIDED, SupportLevel.INDEPENDENT]
    else:
        levels = [SupportLevel.MODELED, SupportLevel.GUIDED, SupportLevel.COLLABORATIVE, SupportLevel.INDEPENDENT]

    # Generate scaffolds
    scaffolds = []
    templates = SCAFFOLD_TEMPLATES[content_type]

    for i, level in enumerate(levels):
        phase_info = GRADUAL_RELEASE_PHASES[level]
        template = templates[level]

        # Calculate duration for this scaffold
        duration = int(total_duration_minutes * phase_info["typical_duration_percent"] / 100)
        duration = max(2, duration)  # Minimum 2 minutes per scaffold

        # Determine transition cue
        if i < len(levels) - 1:
            next_level = levels[i + 1]
            next_phase = GRADUAL_RELEASE_PHASES[next_level]
            transition_cue = f"Now we'll move to {next_phase['name']}"
        else:
            transition_cue = "Now let's see what you've learned"

        scaffold = Scaffold(
            level=level,
            description=f"{phase_info['name']}: {template}",
            teacher_action=f"{phase_info['teacher_role']}: {_generate_teacher_action(level, content_type, lesson_topic)}",
            student_action=f"{phase_info['student_role']}: {_generate_student_action(level, content_type)}",
            duration_minutes=duration,
            supports_provided=_get_supports_for_level(level, content_type),
            transition_cue=transition_cue,
            materials_needed=_get_materials_for_level(level, content_type),
            differentiation_notes=_get_differentiation_for_level(level)
        )
        scaffolds.append(scaffold)

    # Adjust durations to match total
    total_calculated = sum(s.duration_minutes for s in scaffolds)
    if total_calculated != total_duration_minutes:
        diff = total_duration_minutes - total_calculated
        # Add difference to middle scaffolds
        middle_idx = len(scaffolds) // 2
        scaffolds[middle_idx].duration_minutes += diff

    return ScaffoldingPlan(
        lesson_topic=lesson_topic,
        content_type=content_type,
        scaffolds=scaffolds,
        total_duration_minutes=total_duration_minutes,
        objectives_addressed=learning_objectives,
        gradual_release_complete=len(scaffolds) >= 3
    )


def _generate_teacher_action(level: SupportLevel, content_type: str, topic: str) -> str:
    """Generate teacher action for a scaffold level."""
    actions = {
        SupportLevel.MODELED: f"Explicitly demonstrate {content_type} techniques using {topic} examples",
        SupportLevel.GUIDED: f"Lead class through {content_type} process with questioning",
        SupportLevel.COLLABORATIVE: f"Monitor group work and provide targeted coaching",
        SupportLevel.INDEPENDENT: f"Assess individual understanding and provide feedback"
    }
    return actions.get(level, "Support student learning")


def _generate_student_action(level: SupportLevel, content_type: str) -> str:
    """Generate student action for a scaffold level."""
    actions = {
        SupportLevel.MODELED: "Watch, listen, and take notes on key steps",
        SupportLevel.GUIDED: "Participate by responding to questions and attempting alongside teacher",
        SupportLevel.COLLABORATIVE: "Work with partners/groups to practice skills",
        SupportLevel.INDEPENDENT: "Complete task independently demonstrating mastery"
    }
    return actions.get(level, "Engage with content")


def _get_supports_for_level(level: SupportLevel, content_type: str) -> List[str]:
    """Get scaffolding supports for a level."""
    base_supports = {
        SupportLevel.MODELED: [
            "Think-aloud modeling",
            "Visual demonstration",
            "Step-by-step breakdown",
            "Clear success criteria"
        ],
        SupportLevel.GUIDED: [
            "Sentence starters",
            "Graphic organizers",
            "Guiding questions",
            "Partially completed examples"
        ],
        SupportLevel.COLLABORATIVE: [
            "Peer support",
            "Group roles",
            "Collaboration protocols",
            "Check-in points"
        ],
        SupportLevel.INDEPENDENT: [
            "Reference materials",
            "Self-check rubric",
            "Exemplar samples",
            "Teacher availability for questions"
        ]
    }
    return base_supports.get(level, [])


def _get_materials_for_level(level: SupportLevel, content_type: str) -> List[str]:
    """Get materials needed for a scaffold level."""
    materials = {
        SupportLevel.MODELED: ["Projector/board", "Example text/script"],
        SupportLevel.GUIDED: ["Graphic organizer", "Whiteboard"],
        SupportLevel.COLLABORATIVE: ["Group task cards", "Timer"],
        SupportLevel.INDEPENDENT: ["Individual worksheets", "Rubric"]
    }
    return materials.get(level, [])


def _get_differentiation_for_level(level: SupportLevel) -> str:
    """Get differentiation notes for a scaffold level."""
    notes = {
        SupportLevel.MODELED: "ELL: Provide vocabulary preview. Advanced: Ask prediction questions",
        SupportLevel.GUIDED: "ELL: Use visual supports. Advanced: Assign leadership roles",
        SupportLevel.COLLABORATIVE: "ELL: Strategic grouping. Advanced: Extension questions",
        SupportLevel.INDEPENDENT: "ELL: Modified task. Advanced: Extension activity"
    }
    return notes.get(level, "")


def generate_scaffolds_for_activity(
    activity_type: str,
    activity_name: str,
    duration_minutes: int,
    complexity: str = "medium"
) -> List[Scaffold]:
    """
    Generate scaffolds specifically for an activity.

    Args:
        activity_type: Type of activity (discussion, performance, etc.)
        activity_name: Name of the specific activity
        duration_minutes: Time allocated for activity
        complexity: Complexity level (low, medium, high)

    Returns:
        List of scaffolds for the activity
    """
    # Map activity types to content types
    type_mapping = {
        "discussion": "discussion",
        "debate": "discussion",
        "tableaux": "performance",
        "scene_work": "performance",
        "annotation": "analysis",
        "character_analysis": "analysis",
        "script_writing": "writing",
        "journaling": "writing",
        "read_aloud": "reading",
        "close_reading": "reading"
    }

    content_type = type_mapping.get(activity_type, "analysis")

    plan = generate_scaffolding_plan(
        lesson_topic=activity_name,
        content_type=content_type,
        learning_objectives=[],
        total_duration_minutes=duration_minutes
    )

    return plan.scaffolds


# =============================================================================
# VALIDATION FUNCTIONS
# =============================================================================

def validate_scaffolding_plan(plan: ScaffoldingPlan) -> Dict[str, Any]:
    """
    Validate a scaffolding plan against hardcoded rules.

    Returns:
        Dictionary with validation status and any issues
    """
    issues = []
    warnings = []

    # R1: Check scaffold count
    scaffold_count = len(plan.scaffolds)
    if scaffold_count < MIN_SCAFFOLDS_PER_LESSON:
        issues.append({
            "rule": "R1",
            "message": f"Insufficient scaffolds: {scaffold_count} (minimum: {MIN_SCAFFOLDS_PER_LESSON})"
        })
    if scaffold_count > MAX_SCAFFOLDS_PER_LESSON:
        issues.append({
            "rule": "R1",
            "message": f"Too many scaffolds: {scaffold_count} (maximum: {MAX_SCAFFOLDS_PER_LESSON})"
        })

    # R2: Check progression from high to low support
    if plan.scaffolds:
        support_order = [SupportLevel.MODELED, SupportLevel.GUIDED, SupportLevel.COLLABORATIVE, SupportLevel.INDEPENDENT]
        prev_index = -1
        for scaffold in plan.scaffolds:
            current_index = support_order.index(scaffold.level)
            if current_index < prev_index:
                issues.append({
                    "rule": "R2",
                    "message": f"Scaffold progression out of order: {scaffold.level.value} after lower support level"
                })
            prev_index = current_index

    # R3: Check required components
    for i, scaffold in enumerate(plan.scaffolds):
        if not scaffold.teacher_action:
            issues.append({
                "rule": "R3",
                "message": f"Scaffold {i+1} missing teacher_action"
            })
        if not scaffold.student_action:
            issues.append({
                "rule": "R3",
                "message": f"Scaffold {i+1} missing student_action"
            })
        if not scaffold.transition_cue and i < len(plan.scaffolds) - 1:
            warnings.append({
                "rule": "R3",
                "message": f"Scaffold {i+1} missing transition_cue"
            })

    # R5: Check gradual release model
    levels_present = {s.level for s in plan.scaffolds}
    if SupportLevel.MODELED not in levels_present:
        warnings.append({
            "rule": "R5",
            "message": "Missing 'I Do' (modeled) phase in gradual release"
        })
    if SupportLevel.INDEPENDENT not in levels_present:
        warnings.append({
            "rule": "R5",
            "message": "Missing 'You Do' (independent) phase in gradual release"
        })

    return {
        "valid": len(issues) == 0,
        "issues": issues,
        "warnings": warnings,
        "scaffold_count": scaffold_count,
        "gradual_release_complete": plan.gradual_release_complete
    }


def has_valid_scaffolding(plan: ScaffoldingPlan) -> bool:
    """Quick check if scaffolding plan is valid."""
    result = validate_scaffolding_plan(plan)
    return result["valid"]


def scaffolding_plan_to_dict(plan: ScaffoldingPlan) -> Dict[str, Any]:
    """Convert a scaffolding plan to dictionary for JSON serialization."""
    return {
        "lesson_topic": plan.lesson_topic,
        "content_type": plan.content_type,
        "total_duration_minutes": plan.total_duration_minutes,
        "objectives_addressed": plan.objectives_addressed,
        "gradual_release_complete": plan.gradual_release_complete,
        "scaffolds": [
            {
                "level": s.level.value,
                "description": s.description,
                "teacher_action": s.teacher_action,
                "student_action": s.student_action,
                "duration_minutes": s.duration_minutes,
                "supports_provided": s.supports_provided,
                "transition_cue": s.transition_cue,
                "materials_needed": s.materials_needed,
                "differentiation_notes": s.differentiation_notes
            }
            for s in plan.scaffolds
        ]
    }
