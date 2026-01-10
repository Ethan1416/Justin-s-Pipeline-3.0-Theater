"""
Activity Instructions Generator (HARDCODED)
============================================

Generates step-by-step student-facing activity instructions.
Separate from lecture slides for easy projection during facilitation.

HARDCODED RULES (from COMPONENT_GENERATION_INSTRUCTIONS.txt):
- R1: Instructions must be student-facing (imperative verbs)
- R2: Each step must have time allocation
- R3: Must include success criteria
- R4: Must include early finisher instructions
- R5: Must include sharing/debrief protocol
"""

from typing import Any, Dict, List, Optional
from dataclasses import dataclass, field
from enum import Enum


# =============================================================================
# CONSTANTS (HARDCODED - DO NOT MODIFY)
# =============================================================================

ACTIVITY_DURATION_MINUTES = 15
MIN_STEPS = 3
MAX_STEPS = 6
REQUIRED_SECTIONS = ["objective", "steps", "success_criteria", "sharing", "early_finisher"]


class ActivityType(Enum):
    """Types of instructional activities."""
    ANALYSIS = "analysis"
    PERFORMANCE = "performance"
    DISCUSSION = "discussion"
    WRITING = "writing"
    VISUAL = "visual"
    COLLABORATIVE = "collaborative"


# Activity templates with step structures
ACTIVITY_TEMPLATES = {
    "Close Reading with Annotation": {
        "type": ActivityType.ANALYSIS,
        "group_size": "Individual or pairs",
        "objective": "Analyze the text closely by marking key elements and writing observations",
        "steps": [
            {"step": "Read through the passage once silently", "time": 2},
            {"step": "Underline or highlight key words and phrases", "time": 3},
            {"step": "Write margin notes explaining WHY these words matter", "time": 5},
            {"step": "Star your most important discovery", "time": 1},
            {"step": "Be ready to share your starred discovery with a partner", "time": 2}
        ],
        "success_criteria": [
            "You have at least 5 annotations marked",
            "Each annotation has a margin note explaining its significance",
            "You can explain your starred discovery in 30 seconds"
        ],
        "early_finisher": "Find a second passage in the scene that connects to your starred discovery"
    },
    "Character Motivation Chart": {
        "type": ActivityType.ANALYSIS,
        "group_size": "Individual",
        "objective": "Map what your character wants, what's in their way, and what they do about it",
        "steps": [
            {"step": "Write your character's name at the top", "time": 1},
            {"step": "In the WANT column, write what the character desires most", "time": 3},
            {"step": "In the OBSTACLE column, write what stands in their way", "time": 3},
            {"step": "In the ACTION column, write what the character does about it", "time": 3},
            {"step": "At the bottom, predict what will happen next", "time": 2}
        ],
        "success_criteria": [
            "All three columns are filled with specific details from the text",
            "You can point to a line in the scene as evidence",
            "Your prediction connects to what you wrote"
        ],
        "early_finisher": "Complete the chart for a second character and compare their motivations"
    },
    "Blocking Exploration": {
        "type": ActivityType.PERFORMANCE,
        "group_size": "Groups of 3-4",
        "objective": "Create staging for a key moment that shows the relationships between characters",
        "steps": [
            {"step": "Read through your assigned section as a group", "time": 2},
            {"step": "Discuss: Where should each character stand? Why?", "time": 3},
            {"step": "Get on your feet and try your first idea", "time": 3},
            {"step": "Adjust based on what feels right - try at least 2 versions", "time": 4},
            {"step": "Choose your best version and rehearse it once", "time": 2}
        ],
        "success_criteria": [
            "Every character has a clear position that shows their relationship to others",
            "You tried more than one version before deciding",
            "You can explain WHY you made your staging choices"
        ],
        "early_finisher": "Add one specific gesture or movement that reveals character"
    },
    "Tableaux Creation": {
        "type": ActivityType.PERFORMANCE,
        "group_size": "Groups of 4-5",
        "objective": "Create frozen images that capture key moments from the scene",
        "steps": [
            {"step": "As a group, identify 3 key moments from the scene", "time": 2},
            {"step": "For each moment, decide: Who is in the image? What are they doing?", "time": 3},
            {"step": "Physically create your first tableau - everyone freezes", "time": 3},
            {"step": "Create your second and third tableaux", "time": 4},
            {"step": "Practice transitioning between all three", "time": 2}
        ],
        "success_criteria": [
            "You have exactly 3 clear, frozen images",
            "Every person in the group is in each tableau",
            "A viewer could understand the story from your images alone"
        ],
        "early_finisher": "Add a title for each tableau that could be displayed"
    },
    "Fishbowl Discussion": {
        "type": ActivityType.DISCUSSION,
        "group_size": "Inner circle (5-6) + outer circle (rest of class)",
        "objective": "Engage in deep discussion while practicing active listening and evidence use",
        "steps": [
            {"step": "Inner circle: Review the discussion question", "time": 1},
            {"step": "Inner circle: Share your initial response with evidence", "time": 4},
            {"step": "Inner circle: Respond to and build on each other's ideas", "time": 5},
            {"step": "Outer circle: Listen actively and take notes on key points", "time": 0},
            {"step": "Outer circle: Prepare one question or comment for debrief", "time": 2}
        ],
        "success_criteria": [
            "Inner circle: You cited textual evidence at least once",
            "Inner circle: You responded to another person's idea",
            "Outer circle: You have notes on 3 key points made"
        ],
        "early_finisher": "Write a summary statement that captures the group's consensus"
    },
    "Think-Pair-Share": {
        "type": ActivityType.DISCUSSION,
        "group_size": "Individual → Pairs → Whole class",
        "objective": "Develop your thinking through reflection, discussion, and sharing",
        "steps": [
            {"step": "THINK: Silently consider the question for 1 minute", "time": 2},
            {"step": "THINK: Write down your initial thoughts", "time": 2},
            {"step": "PAIR: Turn to a partner and share your ideas", "time": 4},
            {"step": "PAIR: Listen to your partner's ideas and find connections", "time": 3},
            {"step": "SHARE: Be ready to share with the class what you discussed", "time": 2}
        ],
        "success_criteria": [
            "You wrote something during the THINK phase",
            "You spoke AND listened during the PAIR phase",
            "You can summarize your partner's main point"
        ],
        "early_finisher": "Write one new question that emerged from your discussion"
    },
    "Modern Translation": {
        "type": ActivityType.WRITING,
        "group_size": "Individual or pairs",
        "objective": "Translate Shakespeare's language into contemporary speech while keeping the meaning",
        "steps": [
            {"step": "Read the original passage aloud", "time": 2},
            {"step": "Identify words or phrases you don't understand", "time": 2},
            {"step": "Use context clues and your glossary to figure out meanings", "time": 3},
            {"step": "Rewrite the passage in modern language", "time": 5},
            {"step": "Read your translation aloud - does it still make sense?", "time": 2}
        ],
        "success_criteria": [
            "Your translation is in modern, natural-sounding language",
            "The meaning matches the original (check key ideas)",
            "Someone unfamiliar with Shakespeare could understand it"
        ],
        "early_finisher": "Now translate it into text message style - what would be lost?"
    },
    "Character Journal": {
        "type": ActivityType.WRITING,
        "group_size": "Individual",
        "objective": "Write a diary entry from your character's perspective after today's scene",
        "steps": [
            {"step": "Review what happened to your character in today's scene", "time": 2},
            {"step": "Think: What is your character feeling right now?", "time": 1},
            {"step": "Write the date and 'Dear Diary' or your own opening", "time": 1},
            {"step": "Write your character's thoughts and feelings (minimum 8 sentences)", "time": 8},
            {"step": "End with what your character hopes or fears will happen next", "time": 2}
        ],
        "success_criteria": [
            "You write in first person as the character (I, me, my)",
            "You reference specific events from the scene",
            "Your character's emotions are clear and specific"
        ],
        "early_finisher": "Add a second entry from a different character's perspective"
    },
    "Language Analysis": {
        "type": ActivityType.ANALYSIS,
        "group_size": "Pairs",
        "objective": "Examine how Shakespeare uses language to create meaning",
        "steps": [
            {"step": "Read the assigned passage together", "time": 2},
            {"step": "Identify: Is this verse or prose? How do you know?", "time": 2},
            {"step": "Find and list all figurative language (metaphors, similes, personification)", "time": 4},
            {"step": "For each example, explain what it reveals about character or theme", "time": 4},
            {"step": "Choose your best example to share with the class", "time": 2}
        ],
        "success_criteria": [
            "You correctly identified verse vs. prose",
            "You found at least 3 examples of figurative language",
            "You explained what each example reveals (not just named it)"
        ],
        "early_finisher": "Find a passage in modern media that uses similar techniques"
    },
    "Scene Performance Prep": {
        "type": ActivityType.PERFORMANCE,
        "group_size": "Pairs or small groups",
        "objective": "Rehearse your scene with attention to blocking, delivery, and character",
        "steps": [
            {"step": "Read through the scene once for understanding", "time": 2},
            {"step": "Discuss basic blocking: entrances, exits, key movements", "time": 3},
            {"step": "Run the scene on your feet - don't worry about perfection", "time": 4},
            {"step": "Identify one moment to improve and work on it specifically", "time": 3},
            {"step": "Run the scene one more time with your improvement", "time": 2}
        ],
        "success_criteria": [
            "You are off-book OR using script minimally",
            "Your blocking tells the story (not random movement)",
            "You made a specific improvement between runs"
        ],
        "early_finisher": "Add one prop or gesture that deepens the scene"
    },
    "Monologue Coaching": {
        "type": ActivityType.PERFORMANCE,
        "group_size": "Individual with partner feedback",
        "objective": "Work your monologue for performance, focusing on beats and builds",
        "steps": [
            {"step": "Speak through your monologue once for a partner", "time": 2},
            {"step": "Partner gives one piece of feedback: 'I wanted more of...'", "time": 1},
            {"step": "Mark the 'beats' - where does the thought change?", "time": 3},
            {"step": "Work the build - where is the climax? How do you get there?", "time": 4},
            {"step": "Perform again with your adjustments", "time": 3}
        ],
        "success_criteria": [
            "You can identify at least 3 beats in your monologue",
            "Your build to climax is clear to a listener",
            "You incorporated your partner's feedback"
        ],
        "early_finisher": "Try a completely different interpretation and compare"
    },
    "Hot Seat": {
        "type": ActivityType.DISCUSSION,
        "group_size": "1 in seat + class as questioners",
        "objective": "Answer questions as your character, deepening your understanding of their perspective",
        "steps": [
            {"step": "Volunteer (or assigned student) takes the 'hot seat'", "time": 1},
            {"step": "Class asks questions - the character answers in first person", "time": 8},
            {"step": "Character must stay true to what they know at this point in the play", "time": 0},
            {"step": "If stuck, say 'Let me think...' and consider what the character would say", "time": 0},
            {"step": "Class may challenge: 'Where in the text does it say that?'", "time": 4}
        ],
        "success_criteria": [
            "You answered in character (I, me, my) the entire time",
            "Your answers were supported by textual evidence",
            "You revealed something about the character we might have missed"
        ],
        "early_finisher": "Write one question you wish someone had asked"
    },
    "Theme Tracking": {
        "type": ActivityType.ANALYSIS,
        "group_size": "Individual or pairs",
        "objective": "Trace how a major theme develops through specific evidence in the scene",
        "steps": [
            {"step": "Identify the theme you're tracking (love, fate, conflict, family, etc.)", "time": 1},
            {"step": "Read through the scene looking for moments that connect to your theme", "time": 3},
            {"step": "Record at least 3 quotes with line numbers", "time": 4},
            {"step": "For each quote, explain how it develops or complicates the theme", "time": 4},
            {"step": "Write one sentence summarizing what this scene says about your theme", "time": 2}
        ],
        "success_criteria": [
            "You have at least 3 quotes with accurate line numbers",
            "Your explanations go beyond summary to interpretation",
            "Your summary sentence makes a claim about the theme"
        ],
        "early_finisher": "Compare to how this theme appeared in an earlier scene"
    }
}


@dataclass
class ActivityInstructions:
    """Complete activity instruction set."""
    day_number: int
    activity_name: str
    activity_type: ActivityType
    group_size: str
    duration_minutes: int
    objective: str
    steps: List[Dict[str, Any]]
    success_criteria: List[str]
    early_finisher: str
    sharing_protocol: str = ""
    materials_needed: List[str] = field(default_factory=list)


# =============================================================================
# GENERATOR FUNCTIONS
# =============================================================================

def generate_activity_instructions(
    day_number: int,
    activity_name: str,
    lesson_topic: str = "",
    custom_objective: str = ""
) -> ActivityInstructions:
    """
    Generate activity instructions for a lesson.

    Args:
        day_number: Day number in the unit
        activity_name: Name of the activity from templates
        lesson_topic: Topic of today's lesson (for customization)
        custom_objective: Override the default objective if provided

    Returns:
        ActivityInstructions with complete step-by-step guide
    """
    # Get template or use default
    template = ACTIVITY_TEMPLATES.get(activity_name)

    if not template:
        # Create generic template for unknown activities
        template = _create_generic_template(activity_name)

    # Customize objective if provided
    objective = custom_objective if custom_objective else template["objective"]
    if lesson_topic and lesson_topic not in objective:
        objective = f"{objective} (focusing on {lesson_topic})"

    # Generate sharing protocol based on activity type
    sharing = _generate_sharing_protocol(template["type"])

    # Determine materials needed
    materials = _determine_materials(activity_name, template["type"])

    return ActivityInstructions(
        day_number=day_number,
        activity_name=activity_name,
        activity_type=template["type"],
        group_size=template["group_size"],
        duration_minutes=ACTIVITY_DURATION_MINUTES,
        objective=objective,
        steps=template["steps"],
        success_criteria=template["success_criteria"],
        early_finisher=template["early_finisher"],
        sharing_protocol=sharing,
        materials_needed=materials
    )


def _create_generic_template(activity_name: str) -> Dict[str, Any]:
    """Create a generic template for unknown activities."""
    return {
        "type": ActivityType.COLLABORATIVE,
        "group_size": "Pairs or small groups",
        "objective": f"Complete the {activity_name} activity with your group",
        "steps": [
            {"step": "Read and understand the task", "time": 2},
            {"step": "Work with your group on the main task", "time": 8},
            {"step": "Prepare to share your results", "time": 3},
            {"step": "Be ready to present to the class", "time": 2}
        ],
        "success_criteria": [
            "Your group completed the task",
            "Everyone contributed",
            "You can explain your process"
        ],
        "early_finisher": "Help another group or extend your work with additional details"
    }


def _generate_sharing_protocol(activity_type: ActivityType) -> str:
    """Generate sharing/debrief protocol based on activity type."""
    protocols = {
        ActivityType.ANALYSIS: "Share your key discovery with a partner, then volunteers share with class",
        ActivityType.PERFORMANCE: "Each group performs for the class, audience gives one positive note",
        ActivityType.DISCUSSION: "Summarize key points as a class, note areas of agreement/disagreement",
        ActivityType.WRITING: "Volunteers read their work aloud, class responds with observations",
        ActivityType.VISUAL: "Gallery walk to view all work, note observations on sticky notes",
        ActivityType.COLLABORATIVE: "One spokesperson per group shares with class"
    }
    return protocols.get(activity_type, "Share with a partner, then whole class discussion")


def _determine_materials(activity_name: str, activity_type: ActivityType) -> List[str]:
    """Determine materials needed for activity."""
    base_materials = {
        ActivityType.ANALYSIS: ["Handout or text", "Pen/pencil", "Highlighters"],
        ActivityType.PERFORMANCE: ["Open space", "Script excerpts"],
        ActivityType.DISCUSSION: ["Discussion questions visible", "Notes paper"],
        ActivityType.WRITING: ["Paper or journal", "Pen/pencil"],
        ActivityType.VISUAL: ["Chart paper", "Markers", "Tape"]
    }

    materials = base_materials.get(activity_type, ["Handout", "Pen/pencil"])

    # Add specific materials for certain activities
    if "Chart" in activity_name:
        materials.append("Graphic organizer handout")
    if "Tableau" in activity_name:
        materials.append("Camera for capturing (optional)")

    return materials


def activity_instructions_to_markdown(instructions: ActivityInstructions) -> str:
    """Convert ActivityInstructions to markdown format for projection."""
    lines = []

    # Slide 1: Title
    lines.append(f"# {instructions.activity_name}")
    lines.append(f"**Time:** {instructions.duration_minutes} minutes | **Grouping:** {instructions.group_size}")
    lines.append("")

    # Slide 2: Objective
    lines.append("## Your Objective")
    lines.append(f"*By the end of this activity, you will:*")
    lines.append(f"> {instructions.objective}")
    lines.append("")

    # Slides 3-N: Steps
    lines.append("## Steps")
    total_time = 0
    for i, step in enumerate(instructions.steps, 1):
        time_str = f"({step['time']} min)" if step['time'] > 0 else ""
        lines.append(f"### Step {i} {time_str}")
        lines.append(f"{step['step']}")
        lines.append("")
        total_time += step['time']

    # Success Criteria
    lines.append("## You're Successful When...")
    for criterion in instructions.success_criteria:
        lines.append(f"- [ ] {criterion}")
    lines.append("")

    # Early Finisher
    lines.append("## Finished Early?")
    lines.append(f"{instructions.early_finisher}")
    lines.append("")

    # Sharing
    lines.append("## Sharing")
    lines.append(f"{instructions.sharing_protocol}")

    return "\n".join(lines)


def activity_instructions_to_dict(instructions: ActivityInstructions) -> Dict[str, Any]:
    """Convert ActivityInstructions to dictionary for JSON serialization."""
    return {
        "day_number": instructions.day_number,
        "activity_name": instructions.activity_name,
        "activity_type": instructions.activity_type.value,
        "group_size": instructions.group_size,
        "duration_minutes": instructions.duration_minutes,
        "objective": instructions.objective,
        "steps": instructions.steps,
        "success_criteria": instructions.success_criteria,
        "early_finisher": instructions.early_finisher,
        "sharing_protocol": instructions.sharing_protocol,
        "materials_needed": instructions.materials_needed
    }


# =============================================================================
# VALIDATION FUNCTIONS
# =============================================================================

def validate_activity_instructions(instructions: ActivityInstructions) -> Dict[str, Any]:
    """
    Validate activity instructions against hardcoded rules.

    Returns:
        Dictionary with validation status and any issues
    """
    issues = []
    warnings = []

    # R1: Instructions must be student-facing (imperative verbs)
    imperative_starters = ["read", "write", "discuss", "identify", "create", "find",
                          "share", "work", "prepare", "review", "choose", "practice",
                          "perform", "listen", "think", "turn", "be", "get", "run",
                          "speak", "mark", "underline", "star", "add", "end", "use"]
    for step in instructions.steps:
        first_word = step["step"].split()[0].lower()
        if first_word not in imperative_starters:
            warnings.append({
                "rule": "R1",
                "message": f"Step may not be student-facing: '{step['step'][:30]}...'"
            })

    # R2: Each step must have time allocation
    for i, step in enumerate(instructions.steps):
        if "time" not in step:
            issues.append({
                "rule": "R2",
                "message": f"Step {i+1} missing time allocation"
            })

    # Check total time
    total_time = sum(s.get("time", 0) for s in instructions.steps)
    if total_time > instructions.duration_minutes:
        warnings.append({
            "rule": "R2",
            "message": f"Step times ({total_time} min) exceed activity duration ({instructions.duration_minutes} min)"
        })

    # R3: Must include success criteria
    if not instructions.success_criteria or len(instructions.success_criteria) < 2:
        issues.append({
            "rule": "R3",
            "message": "Must include at least 2 success criteria"
        })

    # R4: Must include early finisher instructions
    if not instructions.early_finisher or len(instructions.early_finisher) < 10:
        issues.append({
            "rule": "R4",
            "message": "Must include meaningful early finisher instructions"
        })

    # R5: Must include sharing/debrief protocol
    if not instructions.sharing_protocol:
        issues.append({
            "rule": "R5",
            "message": "Must include sharing/debrief protocol"
        })

    # Check step count
    if len(instructions.steps) < MIN_STEPS:
        issues.append({
            "rule": "Structure",
            "message": f"Too few steps: {len(instructions.steps)} (minimum: {MIN_STEPS})"
        })
    if len(instructions.steps) > MAX_STEPS:
        warnings.append({
            "rule": "Structure",
            "message": f"Many steps: {len(instructions.steps)} (recommended max: {MAX_STEPS})"
        })

    return {
        "valid": len(issues) == 0,
        "issues": issues,
        "warnings": warnings,
        "step_count": len(instructions.steps),
        "total_step_time": total_time,
        "has_success_criteria": len(instructions.success_criteria) >= 2,
        "has_early_finisher": bool(instructions.early_finisher)
    }


def has_valid_activity_instructions(instructions: ActivityInstructions) -> bool:
    """Quick check if activity instructions are valid."""
    result = validate_activity_instructions(instructions)
    return result["valid"]


# =============================================================================
# BATCH GENERATION
# =============================================================================

def generate_activity_instructions_for_unit(
    unit_lessons: List[Dict[str, Any]]
) -> List[ActivityInstructions]:
    """
    Generate activity instructions for an entire unit.

    Args:
        unit_lessons: List of lesson dictionaries with day, activity_name, topic

    Returns:
        List of ActivityInstructions objects
    """
    instructions_list = []

    for lesson in unit_lessons:
        activity_name = lesson.get("activity", lesson.get("activity_name", ""))
        if isinstance(activity_name, tuple):
            activity_name = activity_name[0]  # Handle (name, description) tuples

        instructions = generate_activity_instructions(
            day_number=lesson.get("day", 1),
            activity_name=activity_name,
            lesson_topic=lesson.get("topic", lesson.get("focus", ""))
        )
        instructions_list.append(instructions)

    return instructions_list
