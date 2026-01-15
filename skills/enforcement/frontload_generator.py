"""
Frontload Generator - HARDCODED Skill
Generates frontloading content for lecture slides and presenter notes.

Frontloading prepares students for script reading by explaining:
- WHY content matters for understanding the play
- WHAT to watch for when reading
- HOW concepts connect to upcoming scenes

This skill is HARDCODED and cannot be bypassed during pipeline execution.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from enum import Enum


# =============================================================================
# HARDCODED CONSTANTS - DO NOT MODIFY
# =============================================================================

# Minimum requirements for frontloading
MIN_SIGNIFICANCE_SENTENCES = 2
MAX_SIGNIFICANCE_SENTENCES = 4
MIN_WATCH_FOR_ITEMS = 2
MAX_WATCH_FOR_ITEMS = 3
MIN_KEY_FACTS = 3
MAX_KEY_FACTS = 5

# Required sections in presenter notes
REQUIRED_PRESENTER_SECTIONS = [
    "introduction",
    "key_facts",
    "significance",
    "watch_for",
    "check_understanding"
]

# Presenter note markers
PRESENTER_MARKERS = {
    "pause": "[PAUSE]",
    "emphasis": "[EMPHASIS: {term}]",
    "check": "[CHECK FOR UNDERSTANDING]",
    "watch": "[WATCH FOR]",
    "significance": "[WHY THIS MATTERS]",
    "transition": "[TRANSITION]",
}

# Watch for prompt starters
WATCH_FOR_STARTERS = [
    "How does",
    "What does",
    "Why does",
    "Notice how",
    "Pay attention to",
    "Look for",
    "Compare",
    "Consider",
]

# Significance connectors
SIGNIFICANCE_CONNECTORS = [
    "This matters because",
    "This becomes important when",
    "Understanding this helps you see",
    "This sets up",
    "This contrast shows",
    "This reveals",
    "This foreshadows",
    "Keep this in mind when",
]


# =============================================================================
# DATA CLASSES
# =============================================================================

class FrontloadType(Enum):
    """Types of frontloading content."""
    CHARACTER = "character"
    THEME = "theme"
    PLOT = "plot"
    LANGUAGE = "language"
    STAGING = "staging"
    HISTORICAL = "historical"


@dataclass
class FrontloadContent:
    """Frontloading content for a single slide."""
    slide_title: str
    frontload_type: FrontloadType
    key_facts: List[str]
    significance: str
    watch_for: List[str]
    reading_connection: str
    scene_reference: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "slide_title": self.slide_title,
            "frontload_type": self.frontload_type.value,
            "key_facts": self.key_facts,
            "significance": self.significance,
            "watch_for": self.watch_for,
            "reading_connection": self.reading_connection,
            "scene_reference": self.scene_reference,
        }


@dataclass
class FrontloadedSlide:
    """Complete frontloaded slide with structured content."""
    title: str
    key_facts_section: List[str]
    significance_section: str
    watch_for_section: List[str]
    presenter_notes: str

    def to_slide_body(self) -> str:
        """Generate formatted slide body text."""
        lines = []

        # Key facts
        lines.append("KEY FACTS:")
        for fact in self.key_facts_section:
            lines.append(f"• {fact}")
        lines.append("")

        # Significance
        lines.append("WHY THIS MATTERS:")
        lines.append(self.significance_section)
        lines.append("")

        # Watch for
        lines.append("WATCH FOR WHEN READING:")
        for item in self.watch_for_section:
            lines.append(f"→ {item}")

        return "\n".join(lines)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "title": self.title,
            "key_facts": self.key_facts_section,
            "significance": self.significance_section,
            "watch_for": self.watch_for_section,
            "body": self.to_slide_body(),
            "presenter_notes": self.presenter_notes,
        }


@dataclass
class FrontloadedPresenterNotes:
    """Structured presenter notes with frontloading."""
    introduction: str
    key_facts_script: str
    significance_script: str
    watch_for_script: str
    check_understanding: str
    transition: str

    def to_full_script(self) -> str:
        """Generate complete presenter notes script."""
        sections = [
            self.introduction,
            "",
            self.key_facts_script,
            "",
            f"{PRESENTER_MARKERS['significance']}",
            self.significance_script,
            "",
            f"{PRESENTER_MARKERS['watch']}",
            self.watch_for_script,
            "",
            f"{PRESENTER_MARKERS['check']}",
            self.check_understanding,
            "",
            f"{PRESENTER_MARKERS['transition']}",
            self.transition,
        ]
        return "\n".join(sections)


# =============================================================================
# CORE GENERATION FUNCTIONS
# =============================================================================

def generate_frontload_content(
    slide_title: str,
    raw_bullets: List[str],
    raw_notes: str,
    frontload_type: FrontloadType,
    scene_reference: Optional[str] = None,
    upcoming_plot: Optional[str] = None,
) -> FrontloadContent:
    """
    Generate frontloading content from raw slide data.

    HARDCODED: Enforces minimum requirements for significance and watch_for.

    Args:
        slide_title: Title of the slide
        raw_bullets: Original bullet points
        raw_notes: Original presenter notes
        frontload_type: Type of content being frontloaded
        scene_reference: Scene being prepared for (e.g., "Act 2, Scene 2")
        upcoming_plot: Brief description of what happens next

    Returns:
        FrontloadContent with structured frontloading
    """
    # Extract or generate key facts (limit to MAX)
    key_facts = raw_bullets[:MAX_KEY_FACTS]
    if len(key_facts) < MIN_KEY_FACTS:
        # Pad with extracted facts from notes if needed
        key_facts = _extract_facts_from_notes(raw_notes, MIN_KEY_FACTS - len(key_facts))
        key_facts = raw_bullets + key_facts

    # Generate significance statement
    significance = _generate_significance(
        slide_title, frontload_type, raw_notes, upcoming_plot
    )

    # Generate watch_for items
    watch_for = _generate_watch_for(
        slide_title, frontload_type, raw_notes, scene_reference
    )

    # Generate reading connection
    reading_connection = _generate_reading_connection(
        frontload_type, scene_reference, upcoming_plot
    )

    return FrontloadContent(
        slide_title=slide_title,
        frontload_type=frontload_type,
        key_facts=key_facts[:MAX_KEY_FACTS],
        significance=significance,
        watch_for=watch_for[:MAX_WATCH_FOR_ITEMS],
        reading_connection=reading_connection,
        scene_reference=scene_reference,
    )


def generate_frontloaded_slide(
    frontload: FrontloadContent,
    raw_notes: str,
) -> FrontloadedSlide:
    """
    Generate a complete frontloaded slide with structured sections.

    Args:
        frontload: FrontloadContent with frontloading data
        raw_notes: Original presenter notes to enhance

    Returns:
        FrontloadedSlide with all sections
    """
    # Generate enhanced presenter notes
    presenter_notes = generate_frontloaded_presenter_notes(
        frontload, raw_notes
    )

    return FrontloadedSlide(
        title=frontload.slide_title,
        key_facts_section=frontload.key_facts,
        significance_section=frontload.significance,
        watch_for_section=frontload.watch_for,
        presenter_notes=presenter_notes.to_full_script(),
    )


def generate_frontloaded_presenter_notes(
    frontload: FrontloadContent,
    raw_notes: str,
) -> FrontloadedPresenterNotes:
    """
    Generate structured presenter notes with frontloading sections.

    HARDCODED: All required sections must be present.

    Args:
        frontload: FrontloadContent with frontloading data
        raw_notes: Original presenter notes

    Returns:
        FrontloadedPresenterNotes with all required sections
    """
    # Split raw notes into sentences for processing
    sentences = _split_into_sentences(raw_notes)

    # Introduction (first 2-3 sentences)
    introduction = " ".join(sentences[:3]) if len(sentences) >= 3 else raw_notes[:200]
    introduction = f"{PRESENTER_MARKERS['pause']}\n{introduction}"

    # Key facts script (middle section with emphasis markers)
    key_facts_script = _generate_key_facts_script(frontload.key_facts)

    # Significance script
    significance_script = _generate_significance_script(
        frontload.significance, frontload.frontload_type
    )

    # Watch for script
    watch_for_script = _generate_watch_for_script(
        frontload.watch_for, frontload.scene_reference
    )

    # Check understanding
    check_understanding = _generate_check_understanding(
        frontload.frontload_type, frontload.slide_title
    )

    # Transition
    transition = _generate_transition(frontload.reading_connection)

    return FrontloadedPresenterNotes(
        introduction=introduction,
        key_facts_script=key_facts_script,
        significance_script=significance_script,
        watch_for_script=watch_for_script,
        check_understanding=check_understanding,
        transition=transition,
    )


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def _extract_facts_from_notes(notes: str, count: int) -> List[str]:
    """Extract factual statements from presenter notes."""
    sentences = _split_into_sentences(notes)
    facts = []
    for s in sentences:
        if len(s) > 20 and len(s) < 100 and not s.startswith("["):
            facts.append(s.strip())
            if len(facts) >= count:
                break
    return facts


def _split_into_sentences(text: str) -> List[str]:
    """Split text into sentences."""
    import re
    # Remove markers first
    clean = re.sub(r'\[.*?\]', '', text)
    sentences = re.split(r'(?<=[.!?])\s+', clean)
    return [s.strip() for s in sentences if s.strip()]


def _generate_significance(
    title: str,
    frontload_type: FrontloadType,
    notes: str,
    upcoming_plot: Optional[str]
) -> str:
    """Generate significance statement based on frontload type."""
    type_templates = {
        FrontloadType.CHARACTER: "Understanding {title} helps you see how this character's choices drive the tragedy forward.",
        FrontloadType.THEME: "{title} introduces a theme that Shakespeare will develop throughout the play.",
        FrontloadType.PLOT: "This plot development sets up crucial events. {upcoming}",
        FrontloadType.LANGUAGE: "Shakespeare's language here reveals character and creates dramatic effect.",
        FrontloadType.STAGING: "These staging elements would have been meaningful to Shakespeare's original audience.",
        FrontloadType.HISTORICAL: "This historical context helps explain why characters behave as they do.",
    }

    template = type_templates.get(frontload_type, type_templates[FrontloadType.PLOT])
    upcoming = f"Watch how {upcoming_plot}" if upcoming_plot else "Pay attention to how events unfold."

    return template.format(title=title, upcoming=upcoming)


def _generate_watch_for(
    title: str,
    frontload_type: FrontloadType,
    notes: str,
    scene_reference: Optional[str]
) -> List[str]:
    """Generate watch_for items based on content type."""
    items = []

    # Type-specific watch items
    type_questions = {
        FrontloadType.CHARACTER: [
            f"How does this character speak differently than others?",
            f"What motivates this character's actions?",
            f"How do other characters react to them?",
        ],
        FrontloadType.THEME: [
            "How does Shakespeare introduce this theme?",
            "What images or words connect to this theme?",
            "How might this theme develop later?",
        ],
        FrontloadType.PLOT: [
            "What choices do characters make here?",
            "What could have happened differently?",
            "How does this scene connect to what comes next?",
        ],
        FrontloadType.LANGUAGE: [
            "What poetic devices does Shakespeare use?",
            "How does the language reveal emotion?",
            "What words or phrases are repeated?",
        ],
        FrontloadType.STAGING: [
            "How would this scene look on stage?",
            "What physical actions are implied?",
            "How does staging create meaning?",
        ],
        FrontloadType.HISTORICAL: [
            "How do historical attitudes appear in the text?",
            "What would the original audience understand?",
            "How might modern audiences see this differently?",
        ],
    }

    items = type_questions.get(frontload_type, type_questions[FrontloadType.PLOT])

    # Ensure minimum items
    while len(items) < MIN_WATCH_FOR_ITEMS:
        items.append(f"What surprises you about {title}?")

    return items[:MAX_WATCH_FOR_ITEMS]


def _generate_reading_connection(
    frontload_type: FrontloadType,
    scene_reference: Optional[str],
    upcoming_plot: Optional[str]
) -> str:
    """Generate connection to upcoming reading."""
    if scene_reference and upcoming_plot:
        return f"When you read {scene_reference}, look for how {upcoming_plot}."
    elif scene_reference:
        return f"Keep these ideas in mind as you read {scene_reference}."
    else:
        return "Keep these ideas in mind as you read the next scene."


def _generate_key_facts_script(facts: List[str]) -> str:
    """Generate presenter script for key facts."""
    lines = ["Let me walk you through the key facts you need to know."]
    for i, fact in enumerate(facts):
        if i == 0:
            lines.append(f"\n{PRESENTER_MARKERS['emphasis'].format(term='First')}, {fact}")
        elif i == len(facts) - 1:
            lines.append(f"\n{PRESENTER_MARKERS['emphasis'].format(term='Finally')}, {fact}")
        else:
            lines.append(f"\n{fact}")
        lines.append(PRESENTER_MARKERS['pause'])
    return "\n".join(lines)


def _generate_significance_script(significance: str, frontload_type: FrontloadType) -> str:
    """Generate presenter script for significance section."""
    intro = "Now, here's why this matters for understanding the play."
    return f"{intro}\n\n{PRESENTER_MARKERS['pause']}\n\n{significance}"


def _generate_watch_for_script(watch_items: List[str], scene_reference: Optional[str]) -> str:
    """Generate presenter script for watch_for section."""
    scene_text = f" {scene_reference}" if scene_reference else " the next scene"
    intro = f"As you read{scene_text}, I want you to watch for a few things."

    lines = [intro, PRESENTER_MARKERS['pause']]
    for item in watch_items:
        lines.append(f"\n{item}")
        lines.append(PRESENTER_MARKERS['pause'])

    return "\n".join(lines)


def _generate_check_understanding(frontload_type: FrontloadType, title: str) -> str:
    """Generate check for understanding question."""
    questions = {
        FrontloadType.CHARACTER: f"Can someone summarize what we learned about this character and why it matters?",
        FrontloadType.THEME: f"How would you explain this theme to someone who hasn't read the play?",
        FrontloadType.PLOT: f"What do you predict will happen next based on what we've discussed?",
        FrontloadType.LANGUAGE: f"What's one example of Shakespeare's language that stood out to you?",
        FrontloadType.STAGING: f"How would you stage this scene to emphasize its meaning?",
        FrontloadType.HISTORICAL: f"How does understanding the historical context change how you see this?",
    }
    return questions.get(frontload_type, f"What questions do you have about {title}?")


def _generate_transition(reading_connection: str) -> str:
    """Generate transition to reading activity."""
    return f"Alright, let's move into the text. {reading_connection}"


# =============================================================================
# VALIDATION FUNCTIONS
# =============================================================================

def validate_frontload_content(frontload: FrontloadContent) -> Dict[str, Any]:
    """
    Validate frontload content against HARDCODED rules.

    Returns:
        Dictionary with 'valid' boolean and 'issues' list
    """
    issues = []

    # R1: Check key facts count
    if len(frontload.key_facts) < MIN_KEY_FACTS:
        issues.append(f"Key facts below minimum ({MIN_KEY_FACTS}): has {len(frontload.key_facts)}")
    if len(frontload.key_facts) > MAX_KEY_FACTS:
        issues.append(f"Key facts above maximum ({MAX_KEY_FACTS}): has {len(frontload.key_facts)}")

    # R2: Check significance
    sig_sentences = len(_split_into_sentences(frontload.significance))
    if sig_sentences < MIN_SIGNIFICANCE_SENTENCES:
        issues.append(f"Significance too brief: {sig_sentences} sentences, need {MIN_SIGNIFICANCE_SENTENCES}")

    # R3: Check watch_for count
    if len(frontload.watch_for) < MIN_WATCH_FOR_ITEMS:
        issues.append(f"Watch-for items below minimum ({MIN_WATCH_FOR_ITEMS}): has {len(frontload.watch_for)}")
    if len(frontload.watch_for) > MAX_WATCH_FOR_ITEMS:
        issues.append(f"Watch-for items above maximum ({MAX_WATCH_FOR_ITEMS}): has {len(frontload.watch_for)}")

    # R4: Check reading connection exists
    if not frontload.reading_connection or len(frontload.reading_connection) < 20:
        issues.append("Reading connection missing or too brief")

    return {
        "valid": len(issues) == 0,
        "issues": issues,
        "key_facts_count": len(frontload.key_facts),
        "watch_for_count": len(frontload.watch_for),
        "significance_sentences": sig_sentences,
    }


def validate_frontloaded_slide(slide: FrontloadedSlide) -> Dict[str, Any]:
    """Validate complete frontloaded slide."""
    issues = []

    # Check all sections present
    if not slide.key_facts_section:
        issues.append("Missing key facts section")
    if not slide.significance_section:
        issues.append("Missing significance section")
    if not slide.watch_for_section:
        issues.append("Missing watch_for section")
    if not slide.presenter_notes:
        issues.append("Missing presenter notes")

    # Check presenter notes has required markers
    notes = slide.presenter_notes
    for section in ["WHY THIS MATTERS", "WATCH FOR", "CHECK FOR UNDERSTANDING"]:
        if section not in notes:
            issues.append(f"Presenter notes missing {section} section")

    return {
        "valid": len(issues) == 0,
        "issues": issues,
    }


# =============================================================================
# CONVENIENCE FUNCTIONS
# =============================================================================

def is_valid_frontload(frontload: FrontloadContent) -> bool:
    """Check if frontload content passes validation."""
    return validate_frontload_content(frontload)["valid"]


def get_frontload_issues(frontload: FrontloadContent) -> List[str]:
    """Get list of validation issues for frontload content."""
    return validate_frontload_content(frontload)["issues"]


def determine_frontload_type(topic: str, day_type: str) -> FrontloadType:
    """Determine frontload type based on topic and day type."""
    topic_lower = topic.lower()

    # Character-focused
    if any(name in topic_lower for name in ["nurse", "friar", "mercutio", "tybalt", "paris", "juliet", "romeo"]):
        return FrontloadType.CHARACTER

    # Theme-focused
    if any(theme in topic_lower for theme in ["love", "fate", "death", "feud", "family", "honor"]):
        return FrontloadType.THEME

    # Language-focused
    if any(lang in topic_lower for lang in ["sonnet", "soliloquy", "speech", "prologue", "poetry"]):
        return FrontloadType.LANGUAGE

    # Staging-focused
    if any(stage in topic_lower for stage in ["combat", "blocking", "staging", "performance"]):
        return FrontloadType.STAGING

    # Historical-focused
    if any(hist in topic_lower for hist in ["shakespeare", "elizabethan", "historical", "context"]):
        return FrontloadType.HISTORICAL

    # Default to plot
    return FrontloadType.PLOT
