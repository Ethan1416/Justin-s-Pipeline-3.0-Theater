"""
Agenda Slide Generator - HARDCODED Skill
Generates structured agenda slide content for theater education lessons.

This skill is HARDCODED and cannot be bypassed during pipeline execution.
"""

from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from enum import Enum


# =============================================================================
# HARDCODED CONSTANTS - DO NOT MODIFY
# =============================================================================

# Class period configurations
CLASS_PERIODS = {
    "standard": 56,      # Default 56-minute period
    "block": 90,         # Block schedule
    "shortened": 45,     # Assembly/shortened schedule
    "extended": 75,      # Extended period
}

# Component timing for standard 56-minute period (HARDCODED)
STANDARD_COMPONENTS = {
    "agenda": {"duration": 5, "start": 0, "end": 5},
    "warmup": {"duration": 5, "start": 5, "end": 10},
    "lecture": {"duration": 15, "start": 10, "end": 25},
    "activity": {"duration": 15, "start": 25, "end": 40},
    "reflection": {"duration": 10, "start": 40, "end": 50},
    "buffer": {"duration": 6, "start": 50, "end": 56},
}

# Component display names
COMPONENT_DISPLAY_NAMES = {
    "agenda": "Agenda & Objectives",
    "warmup": "Warmup",
    "lecture": "Lecture",
    "activity": "Activity",
    "reflection": "Reflection & Exit Ticket",
    "buffer": "Buffer/Transition",
}

# Warmup type prefixes
WARMUP_TYPE_PREFIXES = {
    "physical": "Physical warmup",
    "vocal": "Vocal warmup",
    "mental": "Mental warmup",
    "ensemble": "Ensemble warmup",
    "character": "Character warmup",
}

# Activity type formats
ACTIVITY_TYPE_FORMATS = {
    "gallery_walk": "Gallery walk",
    "jigsaw": "Jigsaw activity",
    "partner_work": "Partner work",
    "group_discussion": "Group discussion",
    "scene_work": "Scene work",
    "tableau": "Tableau activity",
    "hot_seat": "Hot seat",
    "fishbowl": "Fishbowl discussion",
    "stations": "Station rotation",
    "performance": "Performance practice",
}

# Validation limits
MAX_OBJECTIVES = 3
MIN_OBJECTIVES = 1
MAX_OBJECTIVE_CHARS = 50
MAX_DESCRIPTION_CHARS = 60
MIN_MATERIALS = 3
MAX_MATERIALS = 5

# Required materials (always included)
REQUIRED_MATERIALS = [
    "PowerPoint presentation",
    "Journal/notebook",
]


# =============================================================================
# DATA CLASSES
# =============================================================================

class ComponentType(Enum):
    """Lesson component types."""
    AGENDA = "agenda"
    WARMUP = "warmup"
    LECTURE = "lecture"
    ACTIVITY = "activity"
    REFLECTION = "reflection"
    BUFFER = "buffer"


@dataclass
class AgendaComponent:
    """Single agenda component with timing."""
    sequence: int
    component_type: ComponentType
    display_name: str
    duration_minutes: int
    time_marker: str
    description: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "sequence": self.sequence,
            "component": self.display_name,
            "duration_minutes": self.duration_minutes,
            "time_marker": self.time_marker,
            "description": self.description,
        }


@dataclass
class AgendaSlide:
    """Complete agenda slide content."""
    unit_number: int
    unit_name: str
    day_number: int
    total_days: int
    lesson_title: str
    date_placeholder: str
    total_duration: int
    components: List[AgendaComponent]
    learning_objectives: List[str]
    materials: List[str]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "agenda": {
                "unit_info": f"Unit {self.unit_number}: {self.unit_name} - Day {self.day_number}/{self.total_days}",
                "date_placeholder": self.date_placeholder,
                "lesson_title": self.lesson_title,
                "total_duration": self.total_duration,
                "components": [c.to_dict() for c in self.components],
                "learning_objectives_display": [
                    f"{i+1}. {obj}" for i, obj in enumerate(self.learning_objectives)
                ],
                "materials_preview": self.materials,
            }
        }


@dataclass
class AgendaSlideVisual:
    """Visual layout specification for Slide 1."""
    header: str
    lesson_title: str
    agenda_items: List[str]
    objectives_display: List[str]

    def to_markdown(self) -> str:
        """Generate markdown representation of slide layout."""
        lines = [
            "┌─────────────────────────────────────────┐",
            f"│  {self.header:<39}│",
            f"│  \"{self.lesson_title}\"" + " " * (38 - len(self.lesson_title) - 2) + "│",
            "├─────────────────────────────────────────┤",
            "│  TODAY'S AGENDA                         │",
        ]
        for item in self.agenda_items:
            lines.append(f"│  ☐ {item:<36}│")
        lines.append("├─────────────────────────────────────────┤")
        lines.append("│  OBJECTIVES                             │")
        for obj in self.objectives_display:
            lines.append(f"│  {obj:<39}│")
        lines.append("└─────────────────────────────────────────┘")
        return "\n".join(lines)


# =============================================================================
# CORE GENERATION FUNCTIONS
# =============================================================================

def generate_time_marker(start: int, end: int) -> str:
    """Generate time marker in MM:SS format."""
    return f"{start}:00-{end}:00"


def generate_component_description(
    component_type: ComponentType,
    topic: str,
    warmup_type: Optional[str] = None,
    activity_type: Optional[str] = None,
) -> str:
    """Generate component description under 60 characters."""
    if component_type == ComponentType.AGENDA:
        desc = "Review daily agenda and learning objectives"
    elif component_type == ComponentType.WARMUP:
        prefix = WARMUP_TYPE_PREFIXES.get(warmup_type, "Warmup")
        desc = f"{prefix} - {topic}"
    elif component_type == ComponentType.LECTURE:
        desc = f"{topic} - verbatim script"
    elif component_type == ComponentType.ACTIVITY:
        format_name = ACTIVITY_TYPE_FORMATS.get(activity_type, "Activity")
        desc = f"{format_name} - {topic}"
    elif component_type == ComponentType.REFLECTION:
        desc = "Journal prompt and exit ticket"
    elif component_type == ComponentType.BUFFER:
        desc = "Transition time and cleanup"
    else:
        desc = topic

    # Enforce character limit
    if len(desc) > MAX_DESCRIPTION_CHARS:
        desc = desc[:MAX_DESCRIPTION_CHARS - 3] + "..."

    return desc


def generate_agenda_slide(
    unit_number: int,
    unit_name: str,
    day_number: int,
    total_days: int,
    lesson_topic: str,
    learning_objectives: List[str],
    warmup_type: str = "physical",
    warmup_connection: str = "",
    activity_type: str = "discussion",
    activity_topic: str = "",
    additional_materials: Optional[List[str]] = None,
    class_period: str = "standard",
) -> AgendaSlide:
    """
    Generate complete agenda slide content.

    HARDCODED: This function enforces all timing and content rules.

    Args:
        unit_number: Unit number (1-4)
        unit_name: Unit name (e.g., "Greek Theater")
        day_number: Day within unit
        total_days: Total days in unit
        lesson_topic: Main topic for the day
        learning_objectives: List of 1-3 measurable objectives
        warmup_type: Type of warmup (physical, vocal, mental, ensemble, character)
        warmup_connection: How warmup connects to lesson
        activity_type: Type of activity
        activity_topic: Specific activity focus
        additional_materials: Extra materials beyond required
        class_period: Period type (standard, block, shortened, extended)

    Returns:
        AgendaSlide with complete content
    """
    # Validate objectives
    if len(learning_objectives) > MAX_OBJECTIVES:
        learning_objectives = learning_objectives[:MAX_OBJECTIVES]
    if len(learning_objectives) < MIN_OBJECTIVES:
        learning_objectives = [f"Understand {lesson_topic}"]

    # Truncate long objectives at word boundaries (smart truncation)
    def smart_truncate_objective(obj: str, max_chars: int = MAX_OBJECTIVE_CHARS) -> str:
        if len(obj) <= max_chars:
            return obj
        # Find last space before limit
        truncated = obj[:max_chars]
        last_space = truncated.rfind(' ')
        if last_space > max_chars // 2:  # Only truncate at word if reasonable
            return truncated[:last_space]
        return truncated  # Fall back to hard truncate if no good word boundary

    learning_objectives = [
        smart_truncate_objective(obj) for obj in learning_objectives
    ]

    # Get timing configuration
    total_duration = CLASS_PERIODS.get(class_period, CLASS_PERIODS["standard"])

    # Build components with timing
    components = []
    timing = STANDARD_COMPONENTS.copy()

    # Adjust timing for non-standard periods
    if class_period == "block":
        timing = _adjust_timing_for_block()
    elif class_period == "shortened":
        timing = _adjust_timing_for_shortened()
    elif class_period == "extended":
        timing = _adjust_timing_for_extended()

    # Generate each component
    warmup_desc = warmup_connection if warmup_connection else lesson_topic
    activity_desc = activity_topic if activity_topic else lesson_topic

    component_configs = [
        (ComponentType.AGENDA, "agenda", lesson_topic, None, None),
        (ComponentType.WARMUP, "warmup", warmup_desc, warmup_type, None),
        (ComponentType.LECTURE, "lecture", lesson_topic, None, None),
        (ComponentType.ACTIVITY, "activity", activity_desc, None, activity_type),
        (ComponentType.REFLECTION, "reflection", lesson_topic, None, None),
        (ComponentType.BUFFER, "buffer", lesson_topic, None, None),
    ]

    for seq, (comp_type, key, topic, w_type, a_type) in enumerate(component_configs, 1):
        t = timing[key]
        components.append(AgendaComponent(
            sequence=seq,
            component_type=comp_type,
            display_name=COMPONENT_DISPLAY_NAMES[key],
            duration_minutes=t["duration"],
            time_marker=generate_time_marker(t["start"], t["end"]),
            description=generate_component_description(comp_type, topic, w_type, a_type),
        ))

    # Build materials list
    materials = REQUIRED_MATERIALS.copy()
    if additional_materials:
        for mat in additional_materials:
            if len(materials) < MAX_MATERIALS and mat not in materials:
                materials.append(mat)

    # Ensure minimum materials
    default_extras = ["Writing utensil", "Handout"]
    for extra in default_extras:
        if len(materials) < MIN_MATERIALS:
            materials.append(extra)

    return AgendaSlide(
        unit_number=unit_number,
        unit_name=unit_name,
        day_number=day_number,
        total_days=total_days,
        lesson_title=lesson_topic,
        date_placeholder="[DATE]",
        total_duration=total_duration,
        components=components,
        learning_objectives=learning_objectives,
        materials=materials[:MAX_MATERIALS],
    )


def generate_agenda_slide_visual(agenda: AgendaSlide) -> AgendaSlideVisual:
    """
    Generate visual layout specification for Slide 1.

    HARDCODED: This produces the exact visual format for PowerPoint.
    """
    header = f"Unit {agenda.unit_number}: {agenda.unit_name} - Day {agenda.day_number}/{agenda.total_days}"

    agenda_items = []
    for comp in agenda.components:
        if comp.component_type != ComponentType.BUFFER:
            item = f"{comp.display_name} ({comp.duration_minutes} min)"
            agenda_items.append(item)

    objectives_display = [
        f"{i+1}. {obj}" for i, obj in enumerate(agenda.learning_objectives)
    ]

    return AgendaSlideVisual(
        header=header,
        lesson_title=agenda.lesson_title,
        agenda_items=agenda_items,
        objectives_display=objectives_display,
    )


# =============================================================================
# TIMING ADJUSTMENT FUNCTIONS (HARDCODED)
# =============================================================================

def _adjust_timing_for_block() -> Dict[str, Dict[str, int]]:
    """Adjust timing for 90-minute block schedule."""
    return {
        "agenda": {"duration": 5, "start": 0, "end": 5},
        "warmup": {"duration": 10, "start": 5, "end": 15},
        "lecture": {"duration": 25, "start": 15, "end": 40},
        "activity": {"duration": 30, "start": 40, "end": 70},
        "reflection": {"duration": 15, "start": 70, "end": 85},
        "buffer": {"duration": 5, "start": 85, "end": 90},
    }


def _adjust_timing_for_shortened() -> Dict[str, Dict[str, int]]:
    """Adjust timing for 45-minute shortened schedule."""
    return {
        "agenda": {"duration": 3, "start": 0, "end": 3},
        "warmup": {"duration": 5, "start": 3, "end": 8},
        "lecture": {"duration": 12, "start": 8, "end": 20},
        "activity": {"duration": 12, "start": 20, "end": 32},
        "reflection": {"duration": 8, "start": 32, "end": 40},
        "buffer": {"duration": 5, "start": 40, "end": 45},
    }


def _adjust_timing_for_extended() -> Dict[str, Dict[str, int]]:
    """Adjust timing for 75-minute extended period."""
    return {
        "agenda": {"duration": 5, "start": 0, "end": 5},
        "warmup": {"duration": 7, "start": 5, "end": 12},
        "lecture": {"duration": 20, "start": 12, "end": 32},
        "activity": {"duration": 22, "start": 32, "end": 54},
        "reflection": {"duration": 13, "start": 54, "end": 67},
        "buffer": {"duration": 8, "start": 67, "end": 75},
    }


# =============================================================================
# VALIDATION FUNCTIONS
# =============================================================================

def validate_agenda_slide(agenda: AgendaSlide) -> Dict[str, Any]:
    """
    Validate agenda slide against HARDCODED rules.

    Returns:
        Dictionary with 'valid' boolean and 'issues' list
    """
    issues = []

    # Check total duration
    total_component_time = sum(c.duration_minutes for c in agenda.components)
    if total_component_time != agenda.total_duration:
        issues.append(
            f"Duration mismatch: components sum to {total_component_time}, "
            f"expected {agenda.total_duration}"
        )

    # Check all components present
    required_types = {ct for ct in ComponentType}
    present_types = {c.component_type for c in agenda.components}
    missing = required_types - present_types
    if missing:
        issues.append(f"Missing components: {[m.value for m in missing]}")

    # Check component count
    if len(agenda.components) != 6:
        issues.append(f"Expected 6 components, found {len(agenda.components)}")

    # Check objectives
    if len(agenda.learning_objectives) < MIN_OBJECTIVES:
        issues.append(f"At least {MIN_OBJECTIVES} objective required")
    if len(agenda.learning_objectives) > MAX_OBJECTIVES:
        issues.append(f"Maximum {MAX_OBJECTIVES} objectives allowed")

    for i, obj in enumerate(agenda.learning_objectives):
        if len(obj) > MAX_OBJECTIVE_CHARS:
            issues.append(f"Objective {i+1} exceeds {MAX_OBJECTIVE_CHARS} chars")

    # Check materials
    if len(agenda.materials) < MIN_MATERIALS:
        issues.append(f"At least {MIN_MATERIALS} materials required")
    if len(agenda.materials) > MAX_MATERIALS:
        issues.append(f"Maximum {MAX_MATERIALS} materials allowed")

    # Check descriptions
    for comp in agenda.components:
        if len(comp.description) > MAX_DESCRIPTION_CHARS:
            issues.append(
                f"{comp.display_name} description exceeds {MAX_DESCRIPTION_CHARS} chars"
            )

    # Check time markers are sequential
    prev_end = 0
    for comp in sorted(agenda.components, key=lambda c: c.sequence):
        parts = comp.time_marker.replace(":00", "").split("-")
        start, end = int(parts[0]), int(parts[1])
        if start != prev_end:
            issues.append(f"Time gap before {comp.display_name}: expected {prev_end}:00")
        prev_end = end

    return {
        "valid": len(issues) == 0,
        "issues": issues,
        "component_count": len(agenda.components),
        "total_duration": total_component_time,
        "objective_count": len(agenda.learning_objectives),
        "materials_count": len(agenda.materials),
    }


def has_valid_agenda(agenda: AgendaSlide) -> bool:
    """Check if agenda passes all validation rules."""
    return validate_agenda_slide(agenda)["valid"]


def get_agenda_issues(agenda: AgendaSlide) -> List[str]:
    """Get list of validation issues for agenda."""
    return validate_agenda_slide(agenda)["issues"]


# =============================================================================
# CONVERSION FUNCTIONS
# =============================================================================

def agenda_to_dict(agenda: AgendaSlide) -> Dict[str, Any]:
    """Convert AgendaSlide to dictionary format."""
    return agenda.to_dict()


def agenda_to_markdown(agenda: AgendaSlide) -> str:
    """Convert agenda to markdown display format."""
    visual = generate_agenda_slide_visual(agenda)
    return visual.to_markdown()


def agenda_to_slide_content(agenda: AgendaSlide) -> Dict[str, Any]:
    """
    Convert agenda to PowerPoint slide content format.

    Returns content ready for pptx_populator agent.
    """
    visual = generate_agenda_slide_visual(agenda)

    return {
        "slide_number": 1,
        "slide_type": "agenda",
        "title": visual.header,
        "subtitle": f'"{visual.lesson_title}"',
        "body_sections": [
            {
                "header": "TODAY'S AGENDA",
                "items": [f"☐ {item}" for item in visual.agenda_items],
            },
            {
                "header": "OBJECTIVES",
                "items": visual.objectives_display,
            },
        ],
        "presenter_notes": _generate_agenda_presenter_notes(agenda),
    }


def _generate_agenda_presenter_notes(agenda: AgendaSlide) -> str:
    """Generate presenter notes for agenda slide."""
    notes = []
    notes.append("[PAUSE]")
    notes.append(f"Good morning/afternoon class. Today we're continuing Unit {agenda.unit_number}: {agenda.unit_name}.")
    notes.append(f"This is Day {agenda.day_number} of {agenda.total_days}.")
    notes.append("[PAUSE]")
    notes.append(f"Our topic today is: {agenda.lesson_title}.")
    notes.append("[CHECK FOR UNDERSTANDING]")
    notes.append("Let's review our agenda for today.")

    for comp in agenda.components:
        if comp.component_type != ComponentType.BUFFER:
            notes.append(f"[EMPHASIS: {comp.display_name}] - {comp.duration_minutes} minutes.")

    notes.append("[PAUSE]")
    notes.append("Our learning objectives for today are:")
    for i, obj in enumerate(agenda.learning_objectives, 1):
        notes.append(f"{i}. {obj}")

    notes.append("[CHECK FOR UNDERSTANDING]")
    notes.append("Any questions before we begin?")

    return "\n".join(notes)
