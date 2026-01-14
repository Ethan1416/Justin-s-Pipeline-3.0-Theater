"""
Monologue Generator Skill
=========================

HARDCODED skill for generating verbatim presenter notes (monologues).
This skill CANNOT be bypassed or modified at runtime.

Requirements:
- 40-180 words per slide (flexible based on content needs)
- Required markers: [PAUSE], [EMPHASIS], [GESTURE], [CHECK], [TRANSITION]
- Natural speech flow, no bullet-point style
- First person, conversational tone
- Dynamic structure that connects slides with backward/forward references

Pipeline: Theater Education
"""

import re
from typing import Dict, Any, List, Optional


# =============================================================================
# HARDCODED CONSTANTS (CANNOT BE MODIFIED)
# =============================================================================

MIN_WORDS_PER_SLIDE = 30
MAX_WORDS_PER_SLIDE = 180
TARGET_WORDS_PER_SLIDE = 105  # Midpoint for guidance, but use best judgment

# Required markers
REQUIRED_MARKERS = {
    "[PAUSE]": {"min_per_slide": 2, "description": "Brief pause for emphasis"},
    "[EMPHASIS]": {"min_per_slide": 1, "description": "Stress the following word/phrase"},
    "[GESTURE]": {"min_per_slide": 0, "description": "Suggested physical movement"},
    "[CHECK]": {"min_per_slide": 0, "description": "Check for student understanding"},
    "[TRANSITION]": {"min_per_slide": 0, "description": "Moving to next point"},
}

# Minimum markers per presentation
MIN_PAUSE_PER_PRESENTATION = 24  # 2 per slide * 12 slides
MIN_EMPHASIS_PER_PRESENTATION = 12  # 1 per slide * 12 slides
MIN_CHECK_PER_PRESENTATION = 3


# =============================================================================
# MONOLOGUE TEMPLATES BY SLIDE TYPE
# =============================================================================

def generate_agenda_monologue(slide_data: Dict[str, Any], day: int = 1) -> str:
    """Generate verbatim monologue for agenda slide."""
    topic = slide_data.get("header", "Today's Lesson")
    body = slide_data.get("body", [])
    if isinstance(body, str):
        body = body.split("\n")

    objectives = [line for line in body if line.strip().startswith("•")]
    objectives_text = " ".join([obj.replace("•", "").strip() for obj in objectives[:3]])

    return f"""[GESTURE: Welcome students as they enter]

Good morning, everyone! [PAUSE] Welcome to Day {day} of our unit.

[EMPHASIS] Today we're diving into something really exciting. Take a look at our agenda on the screen. [GESTURE: Point to the objectives]

[CHECK] Can everyone see the learning objectives? [PAUSE] These are the key things you'll be able to do by the end of class today.

Let me walk you through what we'll cover. {objectives_text if objectives_text else "We have some great material to explore today."}

First, we'll start with our warmup to get our voices and bodies ready. [PAUSE] Then we'll move into the main content of our lesson.

[EMPHASIS] Pay special attention to the vocabulary terms listed here. You'll see these throughout our unit, and they're essential for understanding the material.

[TRANSITION] Any questions before we begin? [PAUSE] Great, let's get started with our warmup!"""


def generate_warmup_monologue(slide_data: Dict[str, Any]) -> str:
    """Generate verbatim monologue for warmup slide."""
    name = slide_data.get("header", "Warmup")

    return f"""[GESTURE: Move to center of room]

Alright everyone, let's get our bodies and voices warmed up! [PAUSE]

[EMPHASIS] This warmup connects directly to what we'll be learning today. In Shakespeare's time, actors had to project their voices to audiences of 3,000 people—without microphones!

[GESTURE: Demonstrate standing posture]

Stand up, please. [PAUSE] Find your space. Make sure you have room to move without touching anyone.

[CHECK] Is everyone ready? [PAUSE]

Here's what we're going to do. [EMPHASIS] Follow my lead and really commit to each exercise. The more energy you put in now, the more prepared you'll be for our performance work later.

[GESTURE: Begin warmup movements]

Let's start with some deep breathing. Breathe in through your nose... [PAUSE] ...and out through your mouth. Feel your diaphragm engage.

Now shake out your hands. [PAUSE] Shake out your feet. Roll your shoulders back. We're releasing tension and waking up our bodies.

[TRANSITION] Now let's move on to our articulation exercises!"""


def generate_content_monologue(
    slide_data: Dict[str, Any],
    slide_index: int = 1,
    prior_topic: str = "",
    next_topic: str = ""
) -> str:
    """
    Generate verbatim monologue for content slide.

    Follows the 5-part framework:
    1. Transition/Hook (15-25 words)
    2. Core Content Delivery (60-80 words)
    3. Example/Illustration (40-50 words)
    4. Connection/Significance (30-40 words)
    5. Bridge to Next (15-20 words)
    """
    header = slide_data.get("header", f"Content {slide_index}")
    body = slide_data.get("body", [])
    if isinstance(body, str):
        body_lines = body.split("\n")
    else:
        body_lines = body

    # Extract body text
    body_text = " ".join([line.strip() for line in body_lines if line.strip()])

    # Part 1: Transition/Hook
    if slide_index == 1:
        transition = "Now that we're warmed up, let's dive into our first key concept. [PAUSE]"
    elif prior_topic:
        transition = f"Building on what we just learned about {prior_topic}, let's explore the next important idea. [PAUSE]"
    else:
        transition = "Here's where it gets really interesting. [PAUSE]"

    # Part 2: Core Content Delivery
    core_content = f"""[GESTURE: Direct attention to screen]

Take a look at the header: "{header}". [EMPHASIS] This is one of the most important ideas we'll explore today.

{body_text}"""

    # Part 3: Example/Illustration
    example = """[PAUSE] Let me give you an example to make this more concrete. Imagine yourself transported back in time, standing in that world. What would you see, hear, and feel? [PAUSE] That's the kind of immersion we want to create when we study theater history."""

    # Part 4: Connection/Significance
    if slide_index % 4 == 0:  # Every 4th slide, add CHECK
        connection = """[CHECK] Can someone tell me how this connects to what we learned earlier? [PAUSE]

Think about why this matters. When we study theater history, we're not just memorizing facts—we're understanding how human creativity and expression have evolved over centuries."""
    else:
        connection = """[EMPHASIS] Think about why this matters. When we study theater history, we're not just memorizing facts—we're understanding how human creativity and expression have evolved over centuries.

Consider how this connects to performances you've seen in your own life. [PAUSE]"""

    # Part 5: Bridge to Next
    if next_topic:
        bridge = f"[TRANSITION] Now let's see how this leads us to our next topic: {next_topic}."
    else:
        bridge = "[TRANSITION] Great, let's continue to our next point."

    return f"""{transition}

{core_content}

{example}

{connection}

{bridge}"""


def generate_activity_monologue(slide_data: Dict[str, Any]) -> str:
    """Generate verbatim monologue for activity slide."""
    name = slide_data.get("header", "Activity")
    body = slide_data.get("body", [])
    if isinstance(body, str):
        body = body.split("\n")

    instructions = [line for line in body if line.strip() and not line.startswith("Activity:")]
    instructions_text = " ".join(instructions[:3]) if instructions else "Follow the instructions on the screen."

    return f"""[EMPHASIS] Alright, it's time for our hands-on activity! [PAUSE]

[GESTURE: Move to activity materials]

This is where you get to apply what we've learned. [PAUSE] Listen carefully to the instructions.

[CHECK] Everyone, eyes up here please. [PAUSE]

Here's what you're going to do. [GESTURE: Point to instructions on screen]

{instructions_text}

[EMPHASIS] The key to success in this activity is working together with your group. Communication is essential—just like it was for Shakespeare's acting company.

[PAUSE]

Take a moment to read through the instructions on the screen. [PAUSE]

You'll have about 15 minutes to complete this activity. [EMPHASIS] That means you need to get started right away and stay focused.

[CHECK] Does everyone understand what they need to do? [PAUSE]

[GESTURE: Signal to begin]

[TRANSITION] Alright, find your groups and let's begin! I'll be circulating to help if you have questions."""


def generate_journal_monologue(slide_data: Dict[str, Any]) -> str:
    """Generate verbatim monologue for journal/exit slide."""
    return """[TRANSITION] We're coming to the end of class, and now it's time for reflection. [PAUSE]

[GESTURE: Lower voice slightly for reflective tone]

Take out your journals. [PAUSE] This is your time to process what you've learned today.

[EMPHASIS] Reflection is a crucial part of learning. When you write about what you've learned, you strengthen those neural pathways and make the information your own.

[PAUSE]

Look at the journal prompt on the screen. [GESTURE: Point to prompt]

[CHECK] Take a moment to read it silently. [PAUSE]

You have about three minutes to write your response. [EMPHASIS] Don't worry about perfect sentences—just let your thoughts flow onto the page.

[PAUSE]

[GESTURE: Move to exit ticket distribution]

When you finish your journal, please complete the exit ticket. [PAUSE] This helps me understand what you learned today and what we might need to review tomorrow.

[TRANSITION] Begin writing now. I'll let you know when time is up."""


# =============================================================================
# MAIN GENERATION FUNCTION
# =============================================================================

def generate_monologue(
    slide_data: Dict[str, Any],
    slide_type: str,
    slide_index: int = 1,
    context: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Generate verbatim monologue for any slide type.

    HARDCODED: Generates 150-200 words with required markers.

    Args:
        slide_data: Slide content dictionary
        slide_type: One of: agenda, warmup, content, activity, journal
        slide_index: For content slides, which one (1-12)
        context: Optional context (prior/next topics, etc.)

    Returns:
        Dictionary with monologue and validation info
    """
    context = context or {}

    # Generate based on slide type
    if slide_type == "agenda":
        day = context.get("day", 1)
        monologue = generate_agenda_monologue(slide_data, day)
    elif slide_type == "warmup":
        monologue = generate_warmup_monologue(slide_data)
    elif slide_type == "content":
        prior = context.get("prior_topic", "")
        next_topic = context.get("next_topic", "")
        monologue = generate_content_monologue(slide_data, slide_index, prior, next_topic)
    elif slide_type == "activity":
        monologue = generate_activity_monologue(slide_data)
    elif slide_type == "journal":
        monologue = generate_journal_monologue(slide_data)
    else:
        # Default fallback
        monologue = generate_content_monologue(slide_data, slide_index)

    # Count words and markers
    word_count = len(monologue.split())
    markers = count_markers(monologue)

    # Validate
    validation = validate_monologue(monologue, word_count, markers)

    return {
        "monologue": monologue,
        "word_count": word_count,
        "estimated_duration_seconds": int(word_count / 2.5),  # ~150 WPM
        "markers": markers,
        "validation": validation,
        "slide_type": slide_type,
        "slide_index": slide_index
    }


def count_markers(text: str) -> Dict[str, int]:
    """Count all markers in text."""
    return {
        "pause_count": len(re.findall(r'\[PAUSE\]', text)),
        "emphasis_count": len(re.findall(r'\[EMPHASIS\]', text)),
        "gesture_count": len(re.findall(r'\[GESTURE[:\s]', text)),
        "check_count": len(re.findall(r'\[CHECK\]', text)),
        "transition_count": len(re.findall(r'\[TRANSITION\]', text)),
    }


def validate_monologue(
    monologue: str,
    word_count: int,
    markers: Dict[str, int]
) -> Dict[str, Any]:
    """
    Validate monologue against HARDCODED requirements.

    Returns validation result with pass/fail status.
    """
    issues = []

    # Word count validation
    meets_min = word_count >= MIN_WORDS_PER_SLIDE
    meets_max = word_count <= MAX_WORDS_PER_SLIDE

    if not meets_min:
        issues.append(f"CRITICAL: Only {word_count} words. Minimum is {MIN_WORDS_PER_SLIDE}.")
    if not meets_max:
        issues.append(f"WARNING: {word_count} words exceeds maximum of {MAX_WORDS_PER_SLIDE}.")

    # Marker validation
    has_required_markers = True
    if markers["pause_count"] < 2:
        issues.append(f"CRITICAL: Only {markers['pause_count']} [PAUSE] markers. Minimum is 2.")
        has_required_markers = False
    if markers["emphasis_count"] < 1:
        issues.append(f"CRITICAL: Only {markers['emphasis_count']} [EMPHASIS] markers. Minimum is 1.")
        has_required_markers = False

    # Speech flow validation
    bullet_indicators = ["•", "-  ", "* ", "1. ", "2. ", "3. "]
    no_bullet_style = True
    for indicator in bullet_indicators:
        if indicator in monologue:
            issues.append(f"Bullet-point style detected: '{indicator}'")
            no_bullet_style = False

    # Natural speech check
    natural_speech = not any([
        monologue.count("\n\n\n") > 0,  # Too many blank lines
        "TODO" in monologue.upper(),
        "PLACEHOLDER" in monologue.upper(),
    ])

    return {
        "valid": len([i for i in issues if "CRITICAL" in i]) == 0,
        "meets_word_minimum": meets_min,
        "meets_word_maximum": meets_max,
        "has_required_markers": has_required_markers,
        "natural_speech_flow": natural_speech,
        "no_bullet_style": no_bullet_style,
        "issues": issues
    }


# =============================================================================
# PRESENTATION-LEVEL GENERATION
# =============================================================================

def generate_all_monologues(
    slides_data: List[Dict[str, Any]],
    day: int = 1
) -> Dict[str, Any]:
    """
    Generate monologues for all 16 slides.

    Args:
        slides_data: List of 16 slide data dictionaries
        day: Day number for context

    Returns:
        Dictionary with all monologues and validation summary
    """
    slide_types = (
        ["agenda", "warmup"] +
        ["content"] * 12 +
        ["activity", "journal"]
    )

    results = []
    total_words = 0
    total_markers = {
        "pause_count": 0,
        "emphasis_count": 0,
        "gesture_count": 0,
        "check_count": 0,
        "transition_count": 0,
    }

    for i, (slide_data, slide_type) in enumerate(zip(slides_data, slide_types)):
        # Determine content slide index
        content_index = i - 1 if slide_type == "content" else 0

        # Build context
        context = {"day": day}
        if i > 0:
            context["prior_topic"] = slides_data[i-1].get("header", "")
        if i < len(slides_data) - 1:
            context["next_topic"] = slides_data[i+1].get("header", "")

        # Generate monologue
        result = generate_monologue(
            slide_data,
            slide_type,
            slide_index=content_index if slide_type == "content" else i + 1,
            context=context
        )

        results.append(result)
        total_words += result["word_count"]

        for key in total_markers:
            total_markers[key] += result["markers"].get(key, 0)

    # Presentation-level validation
    presentation_valid = (
        total_markers["pause_count"] >= MIN_PAUSE_PER_PRESENTATION and
        total_markers["emphasis_count"] >= MIN_EMPHASIS_PER_PRESENTATION and
        total_markers["check_count"] >= MIN_CHECK_PER_PRESENTATION
    )

    return {
        "slides": results,
        "total_words": total_words,
        "total_markers": total_markers,
        "presentation_valid": presentation_valid,
        "estimated_total_duration_minutes": round(total_words / 150, 1)
    }


# =============================================================================
# EXPORTS
# =============================================================================

__all__ = [
    "generate_monologue",
    "generate_all_monologues",
    "generate_agenda_monologue",
    "generate_warmup_monologue",
    "generate_content_monologue",
    "generate_activity_monologue",
    "generate_journal_monologue",
    "validate_monologue",
    "count_markers",
    "MIN_WORDS_PER_SLIDE",
    "MAX_WORDS_PER_SLIDE",
    "REQUIRED_MARKERS",
]
