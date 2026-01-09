"""
English Standards Integrator Skill
==================================

HARDCODED skill for integrating California Common Core English/Language Arts
standards citations into lesson materials.

This skill CANNOT be bypassed - all lessons MUST cite relevant standards.

Integration Points:
- Lesson plan header (all standards listed)
- Activity instructions (relevant standards cited)
- Exit tickets (standards alignment noted)
- Assessment connections

Requirements (HARDCODED):
- Each lesson must have 1-3 English standards
- Standards must be cited in lesson plan
- Standards must be referenced in activities where applicable
- Exit tickets must align with at least one standard

Pipeline: Theater Education
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass


# =============================================================================
# HARDCODED CONSTANTS (CANNOT BE MODIFIED)
# =============================================================================

# Minimum and maximum standards per lesson
MIN_STANDARDS_PER_LESSON = 1
MAX_STANDARDS_PER_LESSON = 3

# California Common Core ELA Standards relevant to Theater Education
CA_ELA_STANDARDS = {
    # Reading Literature Standards (RL)
    "RL.9-10.1": "Cite strong and thorough textual evidence to support analysis of what the text says explicitly as well as inferences drawn from the text.",
    "RL.9-10.2": "Determine a theme or central idea of a text and analyze in detail its development over the course of the text, including how it emerges and is shaped and refined by specific details; provide an objective summary of the text.",
    "RL.9-10.3": "Analyze how complex characters (e.g., those with multiple or conflicting motivations) develop over the course of a text, interact with other characters, and advance the plot or develop the theme.",
    "RL.9-10.4": "Determine the meaning of words and phrases as they are used in the text, including figurative and connotative meanings; analyze the impact of specific word choices on meaning and tone.",
    "RL.9-10.5": "Analyze how an author's choices concerning how to structure a text, order events within it (e.g., parallel plots), and manipulate time (e.g., pacing, flashbacks) create such effects as mystery, tension, or surprise.",
    "RL.9-10.6": "Analyze a particular point of view or cultural experience reflected in a work of literature from outside the United States, drawing on a wide reading of world literature.",
    "RL.9-10.7": "Analyze the representation of a subject or a key scene in two different artistic mediums, including what is emphasized or absent in each treatment.",
    "RL.9-10.9": "Analyze how an author draws on and transforms source material in a specific work.",
    "RL.9-10.10": "By the end of grade 10, read and comprehend literature, including stories, dramas, and poems, at the high end of the grades 9-10 text complexity band independently and proficiently.",

    # Speaking and Listening Standards (SL)
    "SL.9-10.1": "Initiate and participate effectively in a range of collaborative discussions with diverse partners on grades 9-10 topics, texts, and issues, building on others' ideas and expressing their own clearly and persuasively.",
    "SL.9-10.1a": "Come to discussions prepared, having read and researched material under study; explicitly draw on that preparation by referring to evidence from texts and other research on the topic or issue to stimulate a thoughtful, well-reasoned exchange of ideas.",
    "SL.9-10.1b": "Work with peers to set rules for collegial discussions and decision-making, clear goals and deadlines, and individual roles as needed.",
    "SL.9-10.1c": "Propel conversations by posing and responding to questions that relate the current discussion to broader themes or larger ideas; actively incorporate others into the discussion; and clarify, verify, or challenge ideas and conclusions.",
    "SL.9-10.1d": "Respond thoughtfully to diverse perspectives, summarize points of agreement and disagreement, and, when warranted, qualify or justify their own views and understanding and make new connections in light of the evidence and reasoning presented.",
    "SL.9-10.2": "Integrate multiple sources of information presented in diverse media or formats evaluating the credibility and accuracy of each source.",
    "SL.9-10.3": "Evaluate a speaker's point of view, reasoning, and use of evidence and rhetoric, identifying any fallacious reasoning or exaggerated or distorted evidence.",
    "SL.9-10.4": "Present information, findings, and supporting evidence clearly, concisely, and logically such that listeners can follow the line of reasoning and the organization, development, substance, and style are appropriate to purpose, audience, and task.",
    "SL.9-10.5": "Make strategic use of digital media in presentations to enhance understanding of findings, reasoning, and evidence and to add interest.",
    "SL.9-10.6": "Adapt speech to a variety of contexts and tasks, demonstrating command of formal English when indicated or appropriate.",

    # Writing Standards (W)
    "W.9-10.1": "Write arguments to support claims in an analysis of substantive topics or texts, using valid reasoning and relevant and sufficient evidence.",
    "W.9-10.2": "Write informative/explanatory texts to examine and convey complex ideas, concepts, and information clearly and accurately through the effective selection, organization, and analysis of content.",
    "W.9-10.3": "Write narratives to develop real or imagined experiences or events using effective technique, well-chosen details, and well-structured event sequences.",
    "W.9-10.4": "Produce clear and coherent writing in which the development, organization, and style are appropriate to task, purpose, and audience.",
    "W.9-10.9": "Draw evidence from literary or informational texts to support analysis, reflection, and research.",
    "W.9-10.10": "Write routinely over extended time frames and shorter time frames for a range of tasks, purposes, and audiences.",

    # Language Standards (L)
    "L.9-10.1": "Demonstrate command of the conventions of standard English grammar and usage when writing or speaking.",
    "L.9-10.3": "Apply knowledge of language to understand how language functions in different contexts, to make effective choices for meaning or style, and to comprehend more fully when reading or listening.",
    "L.9-10.4": "Determine or clarify the meaning of unknown and multiple-meaning words and phrases based on grades 9-10 reading and content.",
    "L.9-10.5": "Demonstrate understanding of figurative language, word relationships, and nuances in word meanings.",
    "L.9-10.6": "Acquire and use accurately general academic and domain-specific words and phrases.",
}

# Activity type to relevant standards mapping
ACTIVITY_STANDARDS_MAP = {
    "discussion": ["SL.9-10.1", "SL.9-10.1c", "SL.9-10.1d"],
    "collaborative": ["SL.9-10.1", "SL.9-10.1b"],
    "critical_thinking": ["RL.9-10.1", "SL.9-10.1c"],
    "writing": ["W.9-10.4", "W.9-10.10"],
    "performance": ["SL.9-10.4", "SL.9-10.6"],
    "annotation": ["RL.9-10.1", "RL.9-10.4"],
    "analysis": ["RL.9-10.2", "RL.9-10.3", "RL.9-10.5"],
    "vocabulary": ["L.9-10.4", "L.9-10.5", "L.9-10.6"],
    "creative": ["W.9-10.3", "SL.9-10.5"],
    "presentation": ["SL.9-10.4", "SL.9-10.5", "SL.9-10.6"],
    "vocal": ["SL.9-10.6"],
    "physical": ["SL.9-10.1b"],
}


# =============================================================================
# DATA CLASSES
# =============================================================================

@dataclass
class StandardsCitation:
    """A standards citation with context."""
    code: str
    full_text: str
    context: str  # Where/how it applies
    component: str  # Which lesson component it applies to


@dataclass
class IntegrationResult:
    """Result of standards integration."""
    success: bool
    standards_integrated: List[StandardsCitation]
    lesson_plan_text: str
    activity_text: str
    exit_ticket_alignment: Dict[str, str]
    issues: List[str]
    warnings: List[str]


# =============================================================================
# STANDARDS INTEGRATION FUNCTIONS
# =============================================================================

def get_standard_text(code: str) -> Optional[str]:
    """
    Get the full text of a standard by its code.

    Args:
        code: Standard code (e.g., "RL.9-10.4")

    Returns:
        Full text of the standard, or None if not found
    """
    return CA_ELA_STANDARDS.get(code)


def suggest_standards_for_activity(activity_type: str) -> List[str]:
    """
    Suggest relevant standards based on activity type.

    Args:
        activity_type: Type of activity (e.g., "discussion", "writing")

    Returns:
        List of suggested standard codes
    """
    return ACTIVITY_STANDARDS_MAP.get(activity_type.lower(), ["SL.9-10.1"])


def format_standards_citation(
    standards: List[Dict[str, str]],
    include_full_text: bool = True
) -> str:
    """
    Format standards for citation in lesson materials.

    HARDCODED format for consistency across all lessons.

    Args:
        standards: List of standards with 'code' and 'full_text' keys
        include_full_text: Whether to include full standard text

    Returns:
        Formatted standards citation string
    """
    if not standards:
        return "**Standards:** None specified"

    lines = ["**Standards Addressed:**"]
    for std in standards:
        code = std.get("code", "")
        full_text = std.get("full_text", CA_ELA_STANDARDS.get(code, ""))

        if include_full_text and full_text:
            lines.append(f"- **{code}**: {full_text}")
        else:
            lines.append(f"- {code}")

    return "\n".join(lines)


def format_activity_standards_citation(
    activity: Dict[str, Any],
    lesson_standards: List[Dict[str, str]]
) -> str:
    """
    Format standards citation for an activity.

    HARDCODED: Activities must cite relevant standards.

    Args:
        activity: Activity data with 'type' key
        lesson_standards: Standards for the lesson

    Returns:
        Formatted standards citation for the activity
    """
    activity_type = activity.get("type", "").lower()

    # Find which lesson standards apply to this activity type
    relevant_standard_codes = suggest_standards_for_activity(activity_type)

    applicable_standards = []
    for std in lesson_standards:
        code = std.get("code", "")
        # Check if any part of the code matches suggested standards
        for suggested in relevant_standard_codes:
            if code.startswith(suggested.split(".")[0]):  # Match strand (RL, SL, etc.)
                applicable_standards.append(std)
                break

    # If no exact match, use all lesson standards
    if not applicable_standards:
        applicable_standards = lesson_standards

    if not applicable_standards:
        return ""

    codes = [std.get("code", "") for std in applicable_standards]
    return f"*Standards: {', '.join(codes)}*"


def integrate_standards_into_lesson_plan(
    lesson_data: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Integrate standards citations into lesson plan output.

    HARDCODED: All lesson plans must include standards section.

    Args:
        lesson_data: Complete lesson data

    Returns:
        Enhanced lesson plan with standards integration
    """
    standards = lesson_data.get("standards", [])

    # Build standards section
    standards_section = {
        "header": "Standards Addressed",
        "standards": []
    }

    for std in standards:
        code = std.get("code", "")
        full_text = std.get("full_text", CA_ELA_STANDARDS.get(code, ""))

        standards_section["standards"].append({
            "code": code,
            "full_text": full_text,
            "strand": code.split(".")[0] if "." in code else code
        })

    return standards_section


def integrate_standards_into_exit_tickets(
    exit_tickets: List[str],
    standards: List[Dict[str, str]]
) -> List[Dict[str, Any]]:
    """
    Align exit tickets with standards.

    HARDCODED: Each exit ticket must reference at least one standard.

    Args:
        exit_tickets: List of exit ticket questions
        standards: Lesson standards

    Returns:
        Exit tickets with standards alignment
    """
    aligned_tickets = []

    for i, ticket in enumerate(exit_tickets):
        ticket_lower = ticket.lower()

        # Determine which standard best aligns with this question
        aligned_standard = None

        # Simple keyword matching for alignment
        if any(word in ticket_lower for word in ["analyze", "explain", "describe"]):
            # Likely RL standard
            for std in standards:
                if std.get("code", "").startswith("RL"):
                    aligned_standard = std
                    break

        if not aligned_standard and any(word in ticket_lower for word in ["discuss", "share", "explain"]):
            # Likely SL standard
            for std in standards:
                if std.get("code", "").startswith("SL"):
                    aligned_standard = std
                    break

        if not aligned_standard and any(word in ticket_lower for word in ["define", "vocabulary", "word"]):
            # Likely L standard
            for std in standards:
                if std.get("code", "").startswith("L"):
                    aligned_standard = std
                    break

        # Default to first standard if no match
        if not aligned_standard and standards:
            aligned_standard = standards[0]

        aligned_tickets.append({
            "question": ticket,
            "question_number": i + 1,
            "aligned_standard": aligned_standard.get("code") if aligned_standard else None,
            "standard_text": aligned_standard.get("full_text") if aligned_standard else None
        })

    return aligned_tickets


def generate_standards_summary(
    lesson_data: Dict[str, Any]
) -> str:
    """
    Generate a summary of how standards are addressed in the lesson.

    HARDCODED: All lessons must include this summary in teacher notes.

    Args:
        lesson_data: Complete lesson data

    Returns:
        Standards summary text
    """
    standards = lesson_data.get("standards", [])
    activity = lesson_data.get("activity", {})
    exit_tickets = lesson_data.get("exit_tickets", [])

    lines = [
        "## Standards Integration Summary",
        ""
    ]

    for std in standards:
        code = std.get("code", "")
        full_text = std.get("full_text", "")

        lines.append(f"### {code}")
        lines.append(f"*{full_text}*")
        lines.append("")
        lines.append("**Addressed through:**")

        # Determine where this standard is addressed
        addressed = []

        # Check activity alignment
        activity_type = activity.get("type", "").lower()
        relevant_codes = suggest_standards_for_activity(activity_type)
        if any(code.startswith(r.split(".")[0]) for r in relevant_codes):
            addressed.append(f"- Activity: {activity.get('name', 'Main Activity')}")

        # Check if reading-related standard
        if code.startswith("RL"):
            addressed.append("- Direct instruction on text analysis")
            addressed.append("- Close reading exercises")

        # Check if speaking/listening standard
        if code.startswith("SL"):
            addressed.append("- Class discussion")
            addressed.append("- Collaborative group work")

        # Check if writing standard
        if code.startswith("W"):
            addressed.append("- Journal writing")
            addressed.append("- Written responses")

        # Check if language standard
        if code.startswith("L"):
            addressed.append("- Vocabulary instruction")
            addressed.append("- Language analysis")

        # Exit tickets
        addressed.append("- Exit ticket assessment")

        lines.extend(addressed)
        lines.append("")

    return "\n".join(lines)


def integrate_all_standards(
    lesson_data: Dict[str, Any]
) -> IntegrationResult:
    """
    Full integration of standards into all lesson components.

    HARDCODED: This function must be called for every lesson.

    Args:
        lesson_data: Complete lesson data

    Returns:
        IntegrationResult with all integrated content
    """
    standards = lesson_data.get("standards", [])
    activity = lesson_data.get("activity", {})
    exit_tickets = lesson_data.get("exit_tickets", [])

    issues = []
    warnings = []
    citations = []

    # Validate standards count
    if len(standards) < MIN_STANDARDS_PER_LESSON:
        issues.append(f"Lesson has {len(standards)} standards (minimum {MIN_STANDARDS_PER_LESSON} required)")
    elif len(standards) > MAX_STANDARDS_PER_LESSON:
        warnings.append(f"Lesson has {len(standards)} standards (maximum {MAX_STANDARDS_PER_LESSON} recommended)")

    # Generate lesson plan standards section
    lesson_plan_text = format_standards_citation(standards, include_full_text=True)

    # Generate activity standards citation
    activity_text = format_activity_standards_citation(activity, standards)

    # Align exit tickets with standards
    aligned_exit_tickets = integrate_standards_into_exit_tickets(exit_tickets, standards)
    exit_ticket_alignment = {
        f"Q{et['question_number']}": et['aligned_standard']
        for et in aligned_exit_tickets
    }

    # Build citations list
    for std in standards:
        code = std.get("code", "")
        citations.append(StandardsCitation(
            code=code,
            full_text=std.get("full_text", CA_ELA_STANDARDS.get(code, "")),
            context="Lesson-wide standard",
            component="lesson_plan"
        ))

    return IntegrationResult(
        success=len(issues) == 0,
        standards_integrated=citations,
        lesson_plan_text=lesson_plan_text,
        activity_text=activity_text,
        exit_ticket_alignment=exit_ticket_alignment,
        issues=issues,
        warnings=warnings
    )


# =============================================================================
# LESSON PLAN FORMATTING WITH STANDARDS
# =============================================================================

def format_lesson_plan_with_standards(
    lesson_data: Dict[str, Any]
) -> str:
    """
    Format complete lesson plan with integrated standards citations.

    HARDCODED format for consistent output.

    Args:
        lesson_data: Complete lesson data

    Returns:
        Formatted lesson plan markdown
    """
    unit = lesson_data.get("unit", {})
    standards = lesson_data.get("standards", [])
    objectives = lesson_data.get("learning_objectives", [])
    vocabulary = lesson_data.get("vocabulary", [])
    warmup = lesson_data.get("warmup", {})
    activity = lesson_data.get("activity", {})
    exit_tickets = lesson_data.get("exit_tickets", [])
    materials = lesson_data.get("materials_list", [])

    lines = [
        f"# Lesson Plan: {unit.get('name', 'Theater')} - Day {lesson_data.get('day', 1)}",
        f"## {lesson_data.get('topic', '')}",
        "",
        "---",
        "",
        "## Basic Information",
        f"| Field | Value |",
        f"|-------|-------|",
        f"| Unit | {unit.get('name', '')} |",
        f"| Day | {lesson_data.get('day', '')} |",
        f"| Duration | 56 minutes |",
        "",
    ]

    # Standards Section (HARDCODED - must appear prominently)
    lines.append("## Standards Addressed")
    lines.append("")
    for std in standards:
        code = std.get("code", "")
        full_text = std.get("full_text", CA_ELA_STANDARDS.get(code, ""))
        lines.append(f"### {code}")
        lines.append(f"> {full_text}")
        lines.append("")

    # Learning Objectives
    lines.append("## Learning Objectives")
    lines.append("By the end of this lesson, students will be able to:")
    for i, obj in enumerate(objectives, 1):
        lines.append(f"{i}. {obj}")
    lines.append("")

    # Vocabulary
    lines.append("## Vocabulary")
    for vocab in vocabulary:
        lines.append(f"- **{vocab.get('term', '')}**: {vocab.get('definition', '')}")
    lines.append("")

    # Warmup with standards citation
    lines.append("## Warmup (5 minutes)")
    lines.append(f"**{warmup.get('name', '')}**")
    lines.append(warmup.get('instructions', ''))
    lines.append(f"*Connection to lesson: {warmup.get('connection_to_lesson', '')}*")
    # Cite relevant standards for warmup
    warmup_standards = format_activity_standards_citation({"type": warmup.get("type", "")}, standards)
    if warmup_standards:
        lines.append(warmup_standards)
    lines.append("")

    # Main Activity with standards citation
    lines.append("## Main Activity (15 minutes)")
    lines.append(f"**{activity.get('name', '')}**")
    lines.append(activity.get('instructions', ''))
    # Cite standards for activity
    activity_standards = format_activity_standards_citation(activity, standards)
    if activity_standards:
        lines.append("")
        lines.append(activity_standards)
    lines.append("")

    # Exit Tickets with standards alignment
    lines.append("## Exit Tickets")
    aligned = integrate_standards_into_exit_tickets(exit_tickets, standards)
    for et in aligned:
        std_ref = f" *(Assesses: {et['aligned_standard']})*" if et['aligned_standard'] else ""
        lines.append(f"{et['question_number']}. {et['question']}{std_ref}")
    lines.append("")

    # Materials
    lines.append("## Materials")
    for material in materials:
        lines.append(f"- [ ] {material}")
    lines.append("")

    # Standards Integration Summary
    lines.append(generate_standards_summary(lesson_data))

    lines.append("---")
    lines.append("*Generated by Theater Education Pipeline - Standards Integrated*")

    return "\n".join(lines)


# =============================================================================
# EXPORTS
# =============================================================================

__all__ = [
    # Constants
    "MIN_STANDARDS_PER_LESSON",
    "MAX_STANDARDS_PER_LESSON",
    "CA_ELA_STANDARDS",
    "ACTIVITY_STANDARDS_MAP",
    # Functions
    "get_standard_text",
    "suggest_standards_for_activity",
    "format_standards_citation",
    "format_activity_standards_citation",
    "integrate_standards_into_lesson_plan",
    "integrate_standards_into_exit_tickets",
    "generate_standards_summary",
    "integrate_all_standards",
    "format_lesson_plan_with_standards",
    # Data classes
    "StandardsCitation",
    "IntegrationResult",
]
