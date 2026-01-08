#!/usr/bin/env python3
"""
Theater PowerPoint Generator
============================

Creates PowerPoint presentations for Theater Education lessons using
the template_theater.pptx template.

This skill properly:
1. Loads the template_theater.pptx file
2. Duplicates the template slide for each new slide
3. Finds and populates existing shapes by name
4. Preserves all template styling and formatting

Shape Mappings (from template inspection):
- TextBox 6:    Title/Header
- TextBox Body: Body content
- TextBox 20:   "PERFORMANCE TIP" label (static)
- TextBox 24:   Performance tip content
- TextBox 30:   Footer

16-Slide Structure for Theater Lessons:
- Slide 1:     Agenda (auxiliary)
- Slide 2:     Warmup Instructions (auxiliary)
- Slides 3-14: Learning Content (12 content slides)
- Slide 15:    Activity Instructions (auxiliary)
- Slide 16:    Journal & Exit Ticket (auxiliary)

Created: 2026-01-08
Pipeline: Theater Education
"""

import copy
from pathlib import Path
from typing import Any, Dict, List, Optional
from datetime import datetime

try:
    from pptx import Presentation
    from pptx.util import Inches, Pt
    PPTX_AVAILABLE = True
except ImportError:
    PPTX_AVAILABLE = False


# =============================================================================
# SHAPE NAME CONSTANTS (from template_theater.pptx inspection)
# =============================================================================

SHAPE_TITLE = "TextBox 6"
SHAPE_BODY = "TextBox Body"
SHAPE_TIP_LABEL = "TextBox 20"  # Static label "PERFORMANCE TIP"
SHAPE_TIP_CONTENT = "TextBox 24"  # Actual tip text
SHAPE_FOOTER = "TextBox 30"

# Performance tip integration
PERFORMANCE_TIP_SEPARATOR = "\n\n---\nPERFORMANCE TIP: "


# =============================================================================
# SLIDE TYPES
# =============================================================================

class SlideType:
    """Enumeration of slide types in Theater lessons."""
    AGENDA = "agenda"
    WARMUP = "warmup"
    CONTENT = "content"
    ACTIVITY = "activity"
    JOURNAL = "journal"
    SUMMARY = "summary"
    TITLE = "title"


# Standard 16-slide structure
SLIDE_STRUCTURE = [
    {"slide_num": 1, "type": SlideType.AGENDA, "name": "Agenda"},
    {"slide_num": 2, "type": SlideType.WARMUP, "name": "Warmup"},
    {"slide_num": 3, "type": SlideType.CONTENT, "name": "Content 1"},
    {"slide_num": 4, "type": SlideType.CONTENT, "name": "Content 2"},
    {"slide_num": 5, "type": SlideType.CONTENT, "name": "Content 3"},
    {"slide_num": 6, "type": SlideType.CONTENT, "name": "Content 4"},
    {"slide_num": 7, "type": SlideType.CONTENT, "name": "Content 5"},
    {"slide_num": 8, "type": SlideType.CONTENT, "name": "Content 6"},
    {"slide_num": 9, "type": SlideType.CONTENT, "name": "Content 7"},
    {"slide_num": 10, "type": SlideType.CONTENT, "name": "Content 8"},
    {"slide_num": 11, "type": SlideType.CONTENT, "name": "Content 9"},
    {"slide_num": 12, "type": SlideType.CONTENT, "name": "Content 10"},
    {"slide_num": 13, "type": SlideType.CONTENT, "name": "Content 11"},
    {"slide_num": 14, "type": SlideType.CONTENT, "name": "Content 12"},
    {"slide_num": 15, "type": SlideType.ACTIVITY, "name": "Activity"},
    {"slide_num": 16, "type": SlideType.JOURNAL, "name": "Journal & Exit"},
]


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def get_template_path() -> Path:
    """Get the absolute path to the theater template."""
    current = Path(__file__).resolve()
    while current.parent != current:
        if (current / "templates" / "template_theater.pptx").exists():
            return current / "templates" / "template_theater.pptx"
        current = current.parent
    raise FileNotFoundError("Could not find templates/template_theater.pptx")


def find_shape_by_name(slide, shape_name: str):
    """Find a shape in a slide by its name."""
    for shape in slide.shapes:
        if shape.name == shape_name:
            return shape
    return None


def set_shape_text(shape, text: str) -> bool:
    """
    Set text in a shape's text frame, preserving formatting.

    Args:
        shape: PowerPoint shape object
        text: Text to set

    Returns:
        True if successful, False otherwise
    """
    if not shape or not shape.has_text_frame:
        return False

    text_frame = shape.text_frame

    # Clear existing text while preserving paragraph formatting
    for paragraph in text_frame.paragraphs:
        paragraph.clear()

    # Set new text in first paragraph
    if text_frame.paragraphs:
        text_frame.paragraphs[0].text = str(text) if text else ""

    return True


def duplicate_slide(prs, slide_index: int = 0):
    """
    Duplicate a slide by copying its XML element.

    This method properly copies all shapes, including custom TextBoxes
    that are not part of the slide layout.

    Args:
        prs: Presentation object
        slide_index: Index of the slide to duplicate

    Returns:
        The duplicated slide
    """
    from lxml import etree

    source_slide = prs.slides[slide_index]

    # Use the same layout
    slide_layout = source_slide.slide_layout
    new_slide = prs.slides.add_slide(slide_layout)

    # Clear the new slide's shapes (except placeholders from layout)
    shapes_to_remove = []
    for shape in new_slide.shapes:
        # Keep only shapes that came from the layout
        if not shape.is_placeholder:
            shapes_to_remove.append(shape)

    for shape in shapes_to_remove:
        sp = shape.element
        sp.getparent().remove(sp)

    # Copy all shapes from source slide
    for shape in source_slide.shapes:
        # Deep copy the shape's XML element
        new_el = copy.deepcopy(shape.element)
        # Add to new slide's shape tree
        new_slide.shapes._spTree.append(new_el)

    return new_slide


# =============================================================================
# SLIDE POPULATION
# =============================================================================

def populate_slide(
    slide,
    slide_data: Dict[str, Any],
    slide_num: int,
    total_slides: int,
    unit_name: str = "Theater",
    program_name: str = "THEATER EDUCATION",
    year: str = "2026"
) -> None:
    """
    Populate a slide's shapes with content from slide_data.

    Args:
        slide: The PowerPoint slide object
        slide_data: Dictionary containing:
            - header: Title text (max 36 chars)
            - body: Body content (list of lines or single string, max 12 lines)
            - performance_tip: Optional performance tip text (max 132 chars)
            - presenter_notes: Optional presenter notes
            - slide_type: Type of slide (content, agenda, warmup, etc.)
        slide_num: Current slide number (1-indexed)
        total_slides: Total number of slides
        unit_name: Unit name for subtitle
        program_name: Program name for footer
        year: Year for footer
    """
    # 1. Populate title (TextBox 6)
    title_shape = find_shape_by_name(slide, SHAPE_TITLE)
    if title_shape:
        header = slide_data.get("header", f"Slide {slide_num}")
        # Enforce 36-char limit
        if len(header) > 36:
            header = header[:33] + "..."
        set_shape_text(title_shape, header)

    # 2. Populate body (TextBox Body)
    body_shape = find_shape_by_name(slide, SHAPE_BODY)
    if body_shape:
        body = slide_data.get("body", "")
        if isinstance(body, list):
            # Enforce 12-line limit
            body = "\n".join(body[:12])
        set_shape_text(body_shape, body)

    # 3. Update tip label to "PERFORMANCE TIP" (TextBox 20)
    tip_label = find_shape_by_name(slide, SHAPE_TIP_LABEL)
    if tip_label:
        set_shape_text(tip_label, "PERFORMANCE TIP")

    # 4. Populate performance tip content (TextBox 24)
    tip_content = find_shape_by_name(slide, SHAPE_TIP_CONTENT)
    if tip_content:
        performance_tip = slide_data.get("performance_tip", "")
        # Only show tip on content slides
        slide_type = slide_data.get("slide_type", "content")
        if slide_type == SlideType.CONTENT and performance_tip:
            # Enforce 132-char limit
            if len(performance_tip) > 132:
                performance_tip = performance_tip[:129] + "..."
            set_shape_text(tip_content, performance_tip)
        else:
            # Clear tip for non-content slides
            set_shape_text(tip_content, "")

    # 5. Populate footer (TextBox 30)
    footer_shape = find_shape_by_name(slide, SHAPE_FOOTER)
    if footer_shape:
        footer = f"© {year} {program_name} | {unit_name}"
        set_shape_text(footer_shape, footer)

    # 6. Add presenter notes if provided
    if "presenter_notes" in slide_data and slide_data["presenter_notes"]:
        notes_slide = slide.notes_slide
        notes_frame = notes_slide.notes_text_frame
        notes_frame.text = slide_data["presenter_notes"]


# =============================================================================
# SLIDE BUILDERS
# =============================================================================

def build_agenda_slide(
    learning_objectives: List[str],
    vocabulary: List[Dict[str, str]],
    topic: str,
    day: int
) -> Dict[str, Any]:
    """
    Build the agenda slide (Slide 1).

    Args:
        learning_objectives: List of learning objectives
        vocabulary: List of vocabulary dictionaries with 'term' key
        topic: Lesson topic
        day: Day number

    Returns:
        Slide data dictionary
    """
    body_lines = [
        f"Day {day}: {topic}",
        "",
        "Today's Learning Objectives:",
    ]

    for obj in learning_objectives[:3]:  # Max 3 objectives
        body_lines.append(f"• {obj}")

    body_lines.append("")
    body_lines.append("Key Vocabulary:")

    vocab_terms = [v.get("term", "") for v in vocabulary[:4]]
    body_lines.append("• " + " • ".join(vocab_terms))

    return {
        "header": f"Today's Agenda - Day {day}",
        "body": body_lines,
        "slide_type": SlideType.AGENDA,
        "performance_tip": ""
    }


def build_warmup_slide(warmup_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Build the warmup slide (Slide 2).

    Args:
        warmup_data: Warmup dictionary with name, instructions, connection

    Returns:
        Slide data dictionary
    """
    name = warmup_data.get("name", "Theater Warmup")
    instructions = warmup_data.get("instructions", "Follow teacher directions.")
    connection = warmup_data.get("connection_to_lesson", "")

    body_lines = [
        f"Activity: {name}",
        "",
        "Instructions:",
        instructions[:200] if len(instructions) > 200 else instructions,
        "",
        f"Connection: {connection[:100]}" if connection else ""
    ]

    return {
        "header": "Warmup (5 minutes)",
        "body": body_lines,
        "slide_type": SlideType.WARMUP,
        "performance_tip": ""
    }


def build_content_slide(
    content_point: str,
    slide_index: int,
    performance_tip: str = "",
    vocabulary_terms: List[str] = None
) -> Dict[str, Any]:
    """
    Build a content slide (Slides 3-14).

    Args:
        content_point: Main content for this slide
        slide_index: Which content slide (1-12)
        performance_tip: Optional performance tip
        vocabulary_terms: Optional vocabulary to highlight

    Returns:
        Slide data dictionary
    """
    body_lines = [content_point]

    if vocabulary_terms:
        body_lines.append("")
        body_lines.append("Key Terms: " + ", ".join(vocabulary_terms[:3]))

    return {
        "header": f"Learning Point {slide_index}",
        "body": body_lines,
        "slide_type": SlideType.CONTENT,
        "performance_tip": performance_tip or "Focus on understanding the key concept before moving on."
    }


def build_activity_slide(activity_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Build the activity slide (Slide 15).

    Args:
        activity_data: Activity dictionary with name, instructions, materials

    Returns:
        Slide data dictionary
    """
    name = activity_data.get("name", "Practice Activity")
    instructions = activity_data.get("instructions", "")
    materials = activity_data.get("materials", [])
    grouping = activity_data.get("grouping", "individual")

    body_lines = [
        f"Activity: {name}",
        f"Format: {grouping.capitalize()}",
        "",
        "Instructions:",
    ]

    if isinstance(instructions, str):
        body_lines.append(instructions[:300])
    elif isinstance(instructions, list):
        for i, step in enumerate(instructions[:5], 1):
            body_lines.append(f"{i}. {step[:60]}")

    if materials:
        body_lines.append("")
        body_lines.append(f"Materials: {', '.join(materials[:3])}")

    return {
        "header": "Activity (15 minutes)",
        "body": body_lines,
        "slide_type": SlideType.ACTIVITY,
        "performance_tip": ""
    }


def build_journal_slide(
    journal_prompt: str,
    exit_tickets: List[str]
) -> Dict[str, Any]:
    """
    Build the journal & exit ticket slide (Slide 16).

    Args:
        journal_prompt: Reflection prompt
        exit_tickets: List of exit ticket questions

    Returns:
        Slide data dictionary
    """
    body_lines = [
        "Journal Reflection:",
        journal_prompt[:150] if len(journal_prompt) > 150 else journal_prompt,
        "",
        "Exit Ticket:",
    ]

    for i, question in enumerate(exit_tickets[:3], 1):
        body_lines.append(f"{i}. {question[:80]}")

    return {
        "header": "Reflection & Exit (10 min)",
        "body": body_lines,
        "slide_type": SlideType.JOURNAL,
        "performance_tip": ""
    }


# =============================================================================
# MAIN GENERATION FUNCTIONS
# =============================================================================

def generate_slides_from_lesson(lesson_data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Generate 16 slide data dictionaries from lesson data.

    Args:
        lesson_data: Complete lesson data including:
            - topic, day, learning_objectives, vocabulary
            - warmup, activity, journal_prompt, exit_tickets
            - content_points, presenter_notes

    Returns:
        List of 16 slide data dictionaries
    """
    slides = []

    # Extract lesson components
    topic = lesson_data.get("topic", "Theater Lesson")
    day = lesson_data.get("day", 1)
    learning_objectives = lesson_data.get("learning_objectives", [])
    vocabulary = lesson_data.get("vocabulary", [])
    warmup = lesson_data.get("warmup", {})
    activity = lesson_data.get("activity", {})
    journal_prompt = lesson_data.get("journal_prompt", "")
    exit_tickets = lesson_data.get("exit_tickets", [])
    content_points = lesson_data.get("content_points", [])
    presenter_notes = lesson_data.get("presenter_notes", {})

    # Ensure we have 12 content points
    while len(content_points) < 12:
        content_points.append(f"Additional content point {len(content_points) + 1}")

    # Slide 1: Agenda
    agenda = build_agenda_slide(learning_objectives, vocabulary, topic, day)
    agenda["presenter_notes"] = presenter_notes.get("slide_1", "")
    slides.append(agenda)

    # Slide 2: Warmup
    warmup_slide = build_warmup_slide(warmup)
    warmup_slide["presenter_notes"] = presenter_notes.get("slide_2", "")
    slides.append(warmup_slide)

    # Slides 3-14: Content (12 slides)
    vocab_terms = [v.get("term", "") for v in vocabulary]
    for i in range(12):
        content = build_content_slide(
            content_point=content_points[i],
            slide_index=i + 1,
            performance_tip=f"Theater practice: Apply this concept in your performance work.",
            vocabulary_terms=vocab_terms[i:i+2] if i < len(vocab_terms) else []
        )
        content["presenter_notes"] = presenter_notes.get(f"slide_{i+3}", "")
        slides.append(content)

    # Slide 15: Activity
    activity_slide = build_activity_slide(activity)
    activity_slide["presenter_notes"] = presenter_notes.get("slide_15", "")
    slides.append(activity_slide)

    # Slide 16: Journal & Exit
    journal_slide = build_journal_slide(journal_prompt, exit_tickets)
    journal_slide["presenter_notes"] = presenter_notes.get("slide_16", "")
    slides.append(journal_slide)

    return slides


def create_theater_presentation(
    lesson_data: Dict[str, Any],
    output_path: Path,
    unit_name: str = "Theater",
    program_name: str = "THEATER EDUCATION",
    year: str = "2026"
) -> Path:
    """
    Create a complete Theater PowerPoint presentation.

    Args:
        lesson_data: Complete lesson data dictionary
        output_path: Where to save the .pptx file
        unit_name: Unit name for branding
        program_name: Program name for footer
        year: Year for footer

    Returns:
        Path to the created .pptx file
    """
    if not PPTX_AVAILABLE:
        raise ImportError("python-pptx is required. Install with: pip install python-pptx")

    # Get template
    template_path = get_template_path()

    # Load template
    prs = Presentation(str(template_path))

    if len(prs.slides) == 0:
        raise ValueError("Template has no slides")

    # Generate slide data
    slides_data = generate_slides_from_lesson(lesson_data)
    total_slides = len(slides_data)

    # Duplicate template slide for each additional slide needed
    for i in range(1, total_slides):
        duplicate_slide(prs, 0)

    # Populate all slides
    for i, slide_data in enumerate(slides_data):
        slide = prs.slides[i]
        populate_slide(
            slide=slide,
            slide_data=slide_data,
            slide_num=i + 1,
            total_slides=total_slides,
            unit_name=unit_name,
            program_name=program_name,
            year=year
        )

    # Ensure output directory exists
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Save presentation
    prs.save(str(output_path))

    return output_path


def generate_pptx(
    lesson_data: Dict[str, Any],
    output_dir: Path,
    unit_number: int,
    day: int
) -> Dict[str, Any]:
    """
    Main entry point for PowerPoint generation.

    Args:
        lesson_data: Complete lesson data
        output_dir: Output directory
        unit_number: Unit number (1-4)
        day: Day number

    Returns:
        Result dictionary with status and file path
    """
    unit_names = {
        1: "Greek Theater",
        2: "Commedia dell'Arte",
        3: "Shakespeare",
        4: "Student-Directed One Acts"
    }

    unit_name = unit_names.get(unit_number, "Theater")

    # Generate filename
    filename = f"Unit{unit_number}_Day{day:02d}_{unit_name.replace(' ', '_')}.pptx"
    output_path = Path(output_dir) / filename

    try:
        result_path = create_theater_presentation(
            lesson_data=lesson_data,
            output_path=output_path,
            unit_name=unit_name,
            program_name="THEATER EDUCATION",
            year=str(datetime.now().year)
        )

        return {
            "status": "success",
            "file_path": str(result_path),
            "slides_count": 16,
            "unit": unit_name,
            "day": day
        }

    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "unit": unit_name,
            "day": day
        }


# =============================================================================
# VALIDATION
# =============================================================================

def validate_slide_content(slide_data: Dict[str, Any]) -> List[str]:
    """
    Validate slide content against constraints.

    Args:
        slide_data: Slide data dictionary

    Returns:
        List of validation issues (empty if valid)
    """
    issues = []

    # Check header length (max 36 chars)
    header = slide_data.get("header", "")
    if len(header) > 36:
        issues.append(f"Header exceeds 36 chars: {len(header)} chars")

    # Check body line count (max 12 lines)
    body = slide_data.get("body", "")
    if isinstance(body, list):
        if len(body) > 12:
            issues.append(f"Body exceeds 12 lines: {len(body)} lines")
    elif isinstance(body, str):
        lines = body.split("\n")
        if len(lines) > 12:
            issues.append(f"Body exceeds 12 lines: {len(lines)} lines")

    # Check performance tip (max 132 chars)
    tip = slide_data.get("performance_tip", "")
    if len(tip) > 132:
        issues.append(f"Performance tip exceeds 132 chars: {len(tip)} chars")

    return issues


def validate_presentation(slides_data: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Validate entire presentation.

    Args:
        slides_data: List of slide data dictionaries

    Returns:
        Validation result dictionary
    """
    all_issues = []

    # Check slide count
    if len(slides_data) != 16:
        all_issues.append(f"Expected 16 slides, found {len(slides_data)}")

    # Validate each slide
    for i, slide in enumerate(slides_data):
        slide_issues = validate_slide_content(slide)
        for issue in slide_issues:
            all_issues.append(f"Slide {i+1}: {issue}")

    return {
        "valid": len(all_issues) == 0,
        "issues": all_issues,
        "slides_checked": len(slides_data)
    }


# =============================================================================
# EXPORTS
# =============================================================================

__all__ = [
    "create_theater_presentation",
    "generate_pptx",
    "generate_slides_from_lesson",
    "validate_presentation",
    "validate_slide_content",
    "SlideType",
    "SLIDE_STRUCTURE",
]


# =============================================================================
# CLI TESTING
# =============================================================================

if __name__ == "__main__":
    # Test with sample data
    sample_lesson = {
        "topic": "Introduction to Greek Theater",
        "day": 1,
        "learning_objectives": [
            "Identify key characteristics of Greek theater",
            "Explain the role of the Festival of Dionysus",
            "Demonstrate understanding of theatrical origins"
        ],
        "vocabulary": [
            {"term": "dithyramb", "definition": "A choral hymn sung to Dionysus"},
            {"term": "theatron", "definition": "The seating area in Greek theater"},
            {"term": "orchestra", "definition": "The circular performance space"}
        ],
        "warmup": {
            "name": "Chorus Movement",
            "instructions": "Stand in a circle. Follow the leader's movements.",
            "connection_to_lesson": "Introduces ensemble movement like Greek chorus"
        },
        "activity": {
            "name": "Dionysus Festival Role Play",
            "instructions": ["Form groups of 4", "Create a short dithyramb", "Present to class"],
            "grouping": "small groups",
            "materials": ["Percussion instruments", "Movement space"]
        },
        "journal_prompt": "How might participating in a religious festival have influenced the development of theater?",
        "exit_tickets": [
            "Name two elements of Greek theater",
            "Why was the Festival of Dionysus important?"
        ],
        "content_points": [
            "Greek theater originated in ancient Athens around 534 BCE",
            "The Festival of Dionysus was a religious celebration honoring the god of wine",
            "Early performances featured a single actor and a chorus of 12-15 performers",
            "The theatron (seating area) could hold up to 17,000 spectators",
            "The orchestra was a circular space where the chorus performed",
            "Greek theater explored themes of fate, hubris, and divine justice",
            "Tragedy and comedy were the two main dramatic forms",
            "Masks allowed actors to play multiple roles",
            "The chorus provided commentary and emotional response",
            "Theater was a civic duty - attendance was considered important",
            "Competition between playwrights was a key feature of festivals",
            "The legacy of Greek theater continues to influence drama today"
        ]
    }

    # Test generation
    print("Testing Theater PowerPoint Generator...")
    print("=" * 50)

    # Generate slides
    slides = generate_slides_from_lesson(sample_lesson)
    print(f"Generated {len(slides)} slides")

    # Validate
    validation = validate_presentation(slides)
    print(f"Validation: {'PASS' if validation['valid'] else 'FAIL'}")
    if validation['issues']:
        for issue in validation['issues']:
            print(f"  - {issue}")

    # Create presentation
    output_path = Path("test_output/test_theater_presentation.pptx")
    try:
        result = generate_pptx(sample_lesson, output_path.parent, unit_number=1, day=1)
        print(f"\nResult: {result['status']}")
        if result['status'] == 'success':
            print(f"Created: {result['file_path']}")
    except Exception as e:
        print(f"Error: {e}")
