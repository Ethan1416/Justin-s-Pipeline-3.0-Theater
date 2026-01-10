"""
Warm-Up Instruction Card Generator (HARDCODED)
==============================================

Generates ready-to-project warm-up instruction cards for each lesson.
Teacher can display and facilitate without additional prep.

HARDCODED RULES (from COMPONENT_GENERATION_INSTRUCTIONS.txt):
- R1: Warm-up must connect to day's topic (not generic)
- R2: Must include timing cues
- R3: Must include at least one variation
- R4: Instructions must be student-facing (not teacher notes)
- R5: Must fit on one page when projected
"""

from typing import Any, Dict, List, Optional
from dataclasses import dataclass, field


# =============================================================================
# CONSTANTS (HARDCODED - DO NOT MODIFY)
# =============================================================================

WARMUP_DURATION_MINUTES = 5
MIN_STEPS = 3
MAX_STEPS = 5
REQUIRED_SECTIONS = ["setup", "instructions", "teacher_cues", "variations", "connection"]

# Warm-up types by category
WARMUP_TYPES = {
    "physical": {
        "name": "Physical Warm-Up",
        "examples": ["Body shake-out", "Stretch sequence", "Movement exploration", "Stage crosses"]
    },
    "vocal": {
        "name": "Vocal Warm-Up",
        "examples": ["Tongue twisters", "Resonance exercises", "Projection practice", "Breath work"]
    },
    "focus": {
        "name": "Focus/Concentration",
        "examples": ["Zip-zap-zop", "Count to 20", "Mirror exercise", "Observation game"]
    },
    "ensemble": {
        "name": "Ensemble Building",
        "examples": ["Group shape", "Collective story", "Trust circle", "Rhythm pass"]
    },
    "content": {
        "name": "Content-Connected",
        "examples": ["Vocabulary charades", "Quote delivery", "Character walk", "Status exercise"]
    }
}

# Theater-specific warm-ups for Romeo and Juliet
ROMEO_JULIET_WARMUPS = {
    "status_walk": {
        "name": "Status Walk",
        "type": "content",
        "instructions": [
            "Walk around the space at a neutral pace",
            "When I call a number 1-10, adjust your status (1=lowest, 10=highest)",
            "Let your posture, pace, and eye contact reflect your status",
            "Notice how status affects how you interact with others",
            "Freeze when called and observe the room"
        ],
        "connection": "Explore the status differences between Montagues, Capulets, and servants",
        "variations": {
            "simplified": "Use only 3 levels: low, medium, high",
            "advanced": "Add a character name to embody at each status",
            "seated": "Show status through seated posture and gestures only"
        }
    },
    "emotion_spectrum": {
        "name": "Emotion Spectrum",
        "type": "physical",
        "instructions": [
            "Stand in a neutral position",
            "I'll call out an emotion from today's scene",
            "Physically embody that emotion from 0% to 100%",
            "Start at 0, then build to 25%, 50%, 75%, 100%",
            "Reset to neutral between each emotion"
        ],
        "connection": "Practice the emotional range needed for today's scene work",
        "variations": {
            "simplified": "Use only 3 levels: mild, medium, intense",
            "advanced": "Transition smoothly between contrasting emotions",
            "seated": "Express emotion through face and upper body only"
        }
    },
    "verse_rhythm": {
        "name": "Verse Rhythm Walk",
        "type": "vocal",
        "instructions": [
            "Walk around the space at a steady pace",
            "As you walk, tap the iambic rhythm on your thigh: da-DUM, da-DUM",
            "Now speak a line from today's scene in rhythm with your steps",
            "Let the rhythm drive your movement",
            "Freeze on the final stressed syllable"
        ],
        "connection": "Feel Shakespeare's iambic pentameter in your body",
        "variations": {
            "simplified": "Just tap the rhythm, no speaking",
            "advanced": "Add gestures on stressed syllables",
            "seated": "Tap rhythm on desk while speaking"
        }
    },
    "mirror_emotions": {
        "name": "Mirror with Emotion",
        "type": "focus",
        "instructions": [
            "Find a partner and face each other",
            "One person leads with slow movements",
            "The follower mirrors exactly",
            "When I call an emotion, both add that feeling to the movement",
            "Switch leaders on my signal"
        ],
        "connection": "Practice responding to a scene partner's emotional cues",
        "variations": {
            "simplified": "Leader moves only hands and arms",
            "advanced": "Add sounds that match the emotion",
            "seated": "Mirror facial expressions and gestures only"
        }
    },
    "character_walk": {
        "name": "Character Physicality Walk",
        "type": "content",
        "instructions": [
            "Walk around the space as yourself",
            "When I call a character name, transform into them",
            "How do they walk? What leads their movement?",
            "How do they hold their arms? Where do they look?",
            "Be ready to explain your choices"
        ],
        "connection": "Explore physical characterization for today's scene",
        "variations": {
            "simplified": "Focus on one character only",
            "advanced": "Interact briefly with other characters as you pass",
            "seated": "Show character through seated posture and gesture"
        }
    },
    "vocal_projection": {
        "name": "Projection Ladder",
        "type": "vocal",
        "instructions": [
            "Stand facing the back wall",
            "Speak a line from today's scene at whisper level (1)",
            "Repeat at conversational level (3)",
            "Repeat at stage projection (5)",
            "Repeat as if the back row is deaf (7)",
            "Always maintain clarity - loud is not yelling"
        ],
        "connection": "Build the vocal power needed for Shakespeare's language",
        "variations": {
            "simplified": "Use only 3 levels",
            "advanced": "Add emotional intensity as volume increases",
            "seated": "Focus on resonance rather than volume"
        }
    },
    "ensemble_breath": {
        "name": "Ensemble Breath",
        "type": "ensemble",
        "instructions": [
            "Form a circle and hold hands",
            "Close your eyes",
            "Begin breathing naturally",
            "Without forcing, try to sync your breath with the group",
            "When we're breathing together, open your eyes slowly"
        ],
        "connection": "Build the ensemble focus needed for today's group work",
        "variations": {
            "simplified": "Keep eyes open, follow a designated leader",
            "advanced": "Add a group hum on the exhale",
            "seated": "Hands on own knees, eyes closed, listen for group rhythm"
        }
    },
    "fight_choreography_basics": {
        "name": "Stage Combat Basics",
        "type": "physical",
        "instructions": [
            "Find a partner and stand at arm's length",
            "Practice the 'knap' - clapping your own hands to create sound",
            "Leader throws a slow-motion punch (never touch partner)",
            "Follower reacts and creates the 'knap' sound",
            "Switch roles after 3 attempts"
        ],
        "connection": "Learn safe stage combat techniques for fight scenes",
        "variations": {
            "simplified": "Practice only the reaction, no punch",
            "advanced": "Add a slow-motion fall after the hit",
            "seated": "Practice just the 'knap' timing in pairs"
        }
    },
    "death_freeze": {
        "name": "Death Tableau",
        "type": "content",
        "instructions": [
            "Walk around the space",
            "When I clap, freeze in a death pose from the play",
            "Hold for 5 seconds - complete stillness",
            "When I clap again, resume walking",
            "Each freeze should be different"
        ],
        "connection": "Explore the physical vocabulary of tragedy",
        "variations": {
            "simplified": "Freeze in any dramatic pose",
            "advanced": "Create a tableau with a partner",
            "seated": "Freeze in seated death pose"
        }
    },
    "text_toss": {
        "name": "Text Toss",
        "type": "content",
        "instructions": [
            "Form a circle",
            "One person has an imaginary ball and a line from today's scene",
            "Speak the line and 'toss' the ball to someone",
            "Receiver catches, repeats the line, then says a new line and tosses",
            "Keep energy up - no long pauses"
        ],
        "connection": "Get today's key quotes into your mouth and body",
        "variations": {
            "simplified": "Everyone uses the same line",
            "advanced": "Respond with the next line in the scene",
            "seated": "Point to pass instead of toss"
        }
    }
}

# Map scenes to appropriate warm-ups
SCENE_WARMUP_MAP = {
    "Prologue": ["verse_rhythm", "ensemble_breath", "text_toss"],
    "brawl": ["status_walk", "fight_choreography_basics", "emotion_spectrum"],
    "ball": ["status_walk", "character_walk", "mirror_emotions"],
    "balcony": ["emotion_spectrum", "vocal_projection", "mirror_emotions"],
    "fight": ["fight_choreography_basics", "emotion_spectrum", "ensemble_breath"],
    "death": ["death_freeze", "emotion_spectrum", "ensemble_breath"],
    "Mercutio": ["character_walk", "vocal_projection", "verse_rhythm"],
    "Nurse": ["character_walk", "status_walk", "vocal_projection"],
    "Friar": ["character_walk", "status_walk", "ensemble_breath"],
    "potion": ["emotion_spectrum", "death_freeze", "vocal_projection"],
    "tomb": ["death_freeze", "emotion_spectrum", "ensemble_breath"],
    "default": ["ensemble_breath", "vocal_projection", "character_walk"]
}


@dataclass
class WarmupCard:
    """A complete warm-up instruction card."""
    day_number: int
    warmup_name: str
    warmup_type: str
    duration_minutes: int
    connection_to_lesson: str
    setup: Dict[str, Any]
    instructions: List[str]
    teacher_cues: Dict[str, str]
    variations: Dict[str, str]
    safety_notes: List[str] = field(default_factory=list)


# =============================================================================
# GENERATOR FUNCTIONS
# =============================================================================

def generate_warmup_card(
    day_number: int,
    lesson_topic: str,
    scene_focus: str,
    vocabulary: List[str] = None
) -> WarmupCard:
    """
    Generate a warm-up instruction card for a lesson.

    Args:
        day_number: Day number in the unit
        lesson_topic: Topic of today's lesson
        scene_focus: Scene being studied (for warmup selection)
        vocabulary: Key vocabulary for the day

    Returns:
        WarmupCard with complete instructions
    """
    vocabulary = vocabulary or []

    # Select appropriate warm-up based on scene
    warmup_key = _select_warmup_for_scene(scene_focus)
    warmup_template = ROMEO_JULIET_WARMUPS.get(warmup_key, ROMEO_JULIET_WARMUPS["ensemble_breath"])

    # Build setup section
    setup = _generate_setup(warmup_template, warmup_key)

    # Build teacher cues
    teacher_cues = _generate_teacher_cues(warmup_template)

    # Customize connection to specific lesson
    connection = _customize_connection(warmup_template["connection"], lesson_topic, vocabulary)

    # Add safety notes if physical
    safety_notes = _get_safety_notes(warmup_template["type"])

    return WarmupCard(
        day_number=day_number,
        warmup_name=warmup_template["name"],
        warmup_type=warmup_template["type"],
        duration_minutes=WARMUP_DURATION_MINUTES,
        connection_to_lesson=connection,
        setup=setup,
        instructions=warmup_template["instructions"],
        teacher_cues=teacher_cues,
        variations=warmup_template["variations"],
        safety_notes=safety_notes
    )


def _select_warmup_for_scene(scene_focus: str) -> str:
    """Select an appropriate warm-up based on scene content."""
    scene_lower = scene_focus.lower()

    for key, warmups in SCENE_WARMUP_MAP.items():
        if key.lower() in scene_lower:
            return warmups[0]  # Return first recommended warm-up

    return SCENE_WARMUP_MAP["default"][0]


def _generate_setup(warmup_template: Dict, warmup_key: str) -> Dict[str, Any]:
    """Generate setup section for warm-up."""
    space_requirements = {
        "status_walk": "Open space, scattered formation",
        "emotion_spectrum": "Open space, scattered formation",
        "verse_rhythm": "Open space for walking",
        "mirror_emotions": "Pairs facing each other, arm's length apart",
        "character_walk": "Open space, scattered formation",
        "vocal_projection": "Facing back wall, scattered",
        "ensemble_breath": "Standing circle, holding hands",
        "fight_choreography_basics": "Pairs at arm's length, scattered",
        "death_freeze": "Open space for movement",
        "text_toss": "Standing circle"
    }

    props = {
        "text_toss": ["Imaginary ball (or soft ball)"],
        "verse_rhythm": ["Line from today's scene on board"],
        "vocal_projection": ["Line from today's scene on board"]
    }

    return {
        "space_requirements": space_requirements.get(warmup_key, "Flexible formation"),
        "props_needed": props.get(warmup_key, []),
        "time_to_setup": "30 seconds"
    }


def _generate_teacher_cues(warmup_template: Dict) -> Dict[str, str]:
    """Generate teacher cues for warm-up facilitation."""
    return {
        "begin_signal": "Let's begin. Find your starting position.",
        "midpoint_check": "Check in with yourself - are you fully committed?",
        "thirty_seconds": "30 seconds remaining - bring it to a close.",
        "end_signal": "And freeze. Take a breath.",
        "transition": "Great work. Let's carry that energy into today's lesson."
    }


def _customize_connection(base_connection: str, lesson_topic: str, vocabulary: List[str]) -> str:
    """Customize the warm-up connection to specific lesson content."""
    connection = base_connection

    if vocabulary:
        vocab_note = f" Today's key terms: {', '.join(vocabulary[:3])}."
        connection += vocab_note

    connection += f" This connects to our focus on {lesson_topic}."

    return connection


def _get_safety_notes(warmup_type: str) -> List[str]:
    """Get safety notes based on warm-up type."""
    safety = {
        "physical": [
            "Move at your own pace",
            "Stop if anything hurts",
            "Be aware of others around you"
        ],
        "vocal": [
            "Never strain your voice",
            "Stay hydrated"
        ],
        "content": [
            "This is exploration, not performance",
            "There are no wrong choices"
        ]
    }
    return safety.get(warmup_type, [])


def warmup_card_to_markdown(card: WarmupCard) -> str:
    """Convert a WarmupCard to markdown format for projection/printing."""
    lines = []

    # Header
    lines.append(f"# Day {card.day_number}: {card.warmup_name}")
    lines.append(f"**Duration:** {card.duration_minutes} minutes | **Type:** {card.warmup_type.title()}")
    lines.append("")
    lines.append(f"*{card.connection_to_lesson}*")
    lines.append("")

    # Setup
    lines.append("## Setup (30 seconds)")
    lines.append(f"- **Space:** {card.setup['space_requirements']}")
    if card.setup.get('props_needed'):
        lines.append(f"- **Props:** {', '.join(card.setup['props_needed'])}")
    if card.safety_notes:
        lines.append(f"- **Safety:** {'; '.join(card.safety_notes)}")
    lines.append("")

    # Instructions
    lines.append("## Instructions")
    for i, instruction in enumerate(card.instructions, 1):
        lines.append(f"{i}. {instruction}")
    lines.append("")

    # Teacher Cues
    lines.append("## Teacher Cues")
    lines.append(f"- **Begin:** \"{card.teacher_cues['begin_signal']}\"")
    lines.append(f"- **Midpoint:** \"{card.teacher_cues['midpoint_check']}\"")
    lines.append(f"- **30 sec warning:** \"{card.teacher_cues['thirty_seconds']}\"")
    lines.append(f"- **End:** \"{card.teacher_cues['end_signal']}\"")
    lines.append(f"- **Transition:** \"{card.teacher_cues['transition']}\"")
    lines.append("")

    # Variations
    lines.append("## Variations")
    lines.append(f"- **Simplified:** {card.variations['simplified']}")
    lines.append(f"- **Advanced:** {card.variations['advanced']}")
    lines.append(f"- **Seated:** {card.variations['seated']}")

    return "\n".join(lines)


def warmup_card_to_dict(card: WarmupCard) -> Dict[str, Any]:
    """Convert WarmupCard to dictionary for JSON serialization."""
    return {
        "day_number": card.day_number,
        "warmup_name": card.warmup_name,
        "warmup_type": card.warmup_type,
        "duration_minutes": card.duration_minutes,
        "connection_to_lesson": card.connection_to_lesson,
        "setup": card.setup,
        "instructions": card.instructions,
        "teacher_cues": card.teacher_cues,
        "variations": card.variations,
        "safety_notes": card.safety_notes
    }


# =============================================================================
# VALIDATION FUNCTIONS
# =============================================================================

def validate_warmup_card(card: WarmupCard) -> Dict[str, Any]:
    """
    Validate a warm-up card against hardcoded rules.

    Returns:
        Dictionary with validation status and any issues
    """
    issues = []
    warnings = []

    # R1: Must connect to day's topic
    if not card.connection_to_lesson or len(card.connection_to_lesson) < 20:
        issues.append({
            "rule": "R1",
            "message": "Warm-up must have meaningful connection to day's topic"
        })

    # R2: Must include timing cues
    required_cues = ["begin_signal", "thirty_seconds", "end_signal"]
    for cue in required_cues:
        if cue not in card.teacher_cues:
            issues.append({
                "rule": "R2",
                "message": f"Missing timing cue: {cue}"
            })

    # R3: Must include at least one variation
    if not card.variations or len(card.variations) < 1:
        issues.append({
            "rule": "R3",
            "message": "Must include at least one variation"
        })

    # R4: Instructions must be student-facing
    for instruction in card.instructions:
        if instruction.lower().startswith("teacher") or "the students" in instruction.lower():
            warnings.append({
                "rule": "R4",
                "message": f"Instruction may not be student-facing: '{instruction[:30]}...'"
            })

    # R5: Check reasonable length (proxy for one-page)
    total_chars = len(warmup_card_to_markdown(card))
    if total_chars > 2000:
        warnings.append({
            "rule": "R5",
            "message": f"Content may exceed one page ({total_chars} chars)"
        })

    # Check instruction count
    if len(card.instructions) < MIN_STEPS:
        issues.append({
            "rule": "Structure",
            "message": f"Too few instructions: {len(card.instructions)} (minimum: {MIN_STEPS})"
        })
    if len(card.instructions) > MAX_STEPS:
        warnings.append({
            "rule": "Structure",
            "message": f"Many instructions: {len(card.instructions)} (recommended max: {MAX_STEPS})"
        })

    return {
        "valid": len(issues) == 0,
        "issues": issues,
        "warnings": warnings,
        "instruction_count": len(card.instructions),
        "has_variations": len(card.variations) >= 3,
        "has_connection": bool(card.connection_to_lesson)
    }


def has_valid_warmup_card(card: WarmupCard) -> bool:
    """Quick check if warm-up card is valid."""
    result = validate_warmup_card(card)
    return result["valid"]


# =============================================================================
# BATCH GENERATION
# =============================================================================

def generate_warmup_cards_for_unit(
    unit_lessons: List[Dict[str, Any]]
) -> List[WarmupCard]:
    """
    Generate warm-up cards for an entire unit.

    Args:
        unit_lessons: List of lesson dictionaries with day, topic, scene, vocabulary

    Returns:
        List of WarmupCard objects
    """
    cards = []

    for lesson in unit_lessons:
        card = generate_warmup_card(
            day_number=lesson.get("day", 1),
            lesson_topic=lesson.get("topic", lesson.get("focus", "")),
            scene_focus=lesson.get("scene", lesson.get("focus", "")),
            vocabulary=lesson.get("vocabulary", [])
        )
        cards.append(card)

    return cards
