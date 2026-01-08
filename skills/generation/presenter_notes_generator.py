"""
Presenter Notes Generator Skill
Standards-compliant presenter notes generation for NCLEX lecture pipeline.

Requirements (from standards):
- config/constraints.yaml: max_words: 450, max_duration: 180s
- standards/presenting_standards.md: 130-150 words per minute
- agents/prompts/presenter_notes_writer.md: slide type targets

Word Count Targets by Slide Type:
- Title/Intro: 200-450 words (target 350)
- Content: 250-450 words (target 380)
- Summary: 250-450 words (target 380)
- Vignette: 150-350 words (target 250)
- Answer: 250-450 words (target 400)

Marker Requirements:
- [PAUSE]: minimum 2 per slide
- [EMPHASIS: term]: minimum 1 for content slides
- NCLEX pattern callouts where relevant
"""

from typing import Dict, List, Any, Optional


def generate_presenter_notes(
    slide_type: str,
    topic: str,
    anchors: List[Any],
    section_name: str,
    nclex_tip: str = "",
    slide_num: int = 1,
    total_slides: int = 10,
    domain: str = "NCLEX"
) -> str:
    """
    Generate comprehensive presenter notes following standards/presenting_standards.md

    Args:
        slide_type: Type of slide ('title', 'content', 'summary', 'vignette', 'answer')
        topic: Main topic/header of the slide
        anchors: List of anchor points or subsections (dicts with 'text' key, or strings)
        section_name: Name of the section
        nclex_tip: NCLEX tip text (optional)
        slide_num: Current slide number
        total_slides: Total slides in section
        domain: Domain name for context

    Returns:
        Standards-compliant presenter notes string
    """
    slide_type = slide_type.lower()

    if slide_type == "title":
        return _generate_title_notes(topic, section_name, anchors, domain)
    elif slide_type == "summary":
        return _generate_summary_notes(topic, section_name, anchors, domain)
    elif slide_type == "vignette":
        return _generate_vignette_notes(topic, anchors, section_name)
    elif slide_type == "answer":
        return _generate_answer_notes(topic, anchors, section_name, nclex_tip)
    else:
        return _generate_content_notes(topic, anchors, section_name, nclex_tip, slide_num, total_slides)


def _generate_title_notes(
    topic: str,
    section_name: str,
    subsections: List[Any],
    domain: str = "NCLEX"
) -> str:
    """Generate presenter notes for title/intro slides (target: 350 words)."""

    # Build subsection list - handle both string lists and dict lists
    subsection_text = ""
    if subsections:
        if isinstance(subsections[0], dict):
            items = [s.get('text', str(s)) for s in subsections[:4]]
        else:
            items = [str(s) for s in subsections[:4]]
        subsection_text = ", ".join(items)
        if len(subsections) > 4:
            subsection_text += f", and {len(subsections) - 4} more essential topics"

    notes = f"""Welcome to {section_name}. [PAUSE]

This section is one of the most heavily tested areas on the NCLEX, and for good reason. Understanding these concepts is absolutely critical for safe nursing practice. As you work through this material, I want you to think about how each concept connects to patient safety and clinical decision-making.

[PAUSE]

In this section, we'll cover {subsection_text}. Each of these topics builds on the others, so pay close attention to how they interconnect. The NCLEX loves to test your ability to integrate multiple concepts into a single clinical scenario.

Before we dive in, let me share something important. [EMPHASIS: {domain}] content isn't just about memorizing facts and procedures. It's about understanding the underlying principles that help you predict outcomes and make safe clinical decisions. When you understand the "why" behind nursing interventions, you'll be able to answer NCLEX questions even when you encounter an unfamiliar scenario.

On the NCLEX, you'll see questions from this content area presented in various formats. Some will be straightforward knowledge questions, but many will be scenario-based, asking you to apply your knowledge to a specific patient situation. The key is to focus on safety first. When in doubt, think about what could harm the patient and what actions would protect them.

[PAUSE]

As we work through this content, I'll highlight specific NCLEX testing patterns and common "trap" answers to watch out for. Take notes on these patterns because recognizing them during the exam can be the difference between choosing the correct answer and falling for a well-crafted distractor.

Let's begin with our first topic and build a strong foundation for everything that follows."""

    return notes


def _generate_summary_notes(
    topic: str,
    section_name: str,
    key_points: List[Any],
    domain: str = "NCLEX"
) -> str:
    """Generate presenter notes for summary slides (target: 380 words)."""

    notes = f"""Let's take a moment to consolidate what we've learned in {section_name}. [PAUSE]

This has been a content-rich section, and I want to make sure you're walking away with the key concepts firmly in mind. Remember, the NCLEX doesn't just test whether you know facts. It tests whether you can apply those facts to make safe clinical decisions.

[EMPHASIS: The most critical takeaway] from this section is understanding the underlying principles, not just memorizing individual items. When you understand why something works the way it does, you can reason through unfamiliar scenarios on the exam.

[PAUSE]

Let me highlight the highest-yield concepts from this section. First, always think about patient safety. Before performing any intervention or administering any treatment, ask yourself: What could go wrong? What assessments do I need to perform first? What monitoring is required afterward?

Second, remember the connections between concepts. The NCLEX often tests your ability to integrate knowledge across topics. A question might combine assessment findings with intervention selection, or pathophysiology with patient teaching. Look for these connections as you review.

Third, pay attention to the "red flag" situations we discussed. These are the scenarios where something could go seriously wrong if you don't intervene appropriately. The NCLEX loves to test your ability to recognize when a situation requires immediate action versus when you can continue with routine care.

[PAUSE]

For your study approach, I recommend using active recall rather than passive re-reading. Quiz yourself on the key concepts, practice applying them to case scenarios, and explain the material out loud as if you were teaching someone else. This type of deep processing will help the information stick and make it accessible during the high-pressure exam environment.

On the NCLEX, if you encounter a question from this content area and feel uncertain, fall back on the fundamental principles we discussed. Think about safety, prioritization, and the nursing process. These frameworks will guide you to the correct answer even when the specific details are fuzzy.

[PAUSE]

Now let's move forward and continue building your knowledge base."""

    return notes


def _generate_content_notes(
    topic: str,
    anchors: List[Any],
    section_name: str,
    nclex_tip: str,
    slide_num: int,
    total_slides: int
) -> str:
    """Generate presenter notes for content slides (target: 380 words)."""

    # Extract key terms for emphasis
    key_terms = []
    for anchor in anchors:
        text = anchor.get('text', str(anchor)) if isinstance(anchor, dict) else str(anchor)
        # Find terms in quotes, parentheses, or specific patterns
        if '"' in text:
            parts = text.split('"')
            if len(parts) > 1:
                key_terms.append(parts[1])
        if '(' in text and ')' in text:
            term = text.split('(')[1].split(')')[0]
            if len(term) < 30:
                key_terms.append(term)
        # Look for drug suffixes or medical terms
        for suffix in ['-olol', '-pril', '-sartan', '-statin', '-prazole', '-dipine', '-mycin', '-cillin']:
            if suffix in text.lower():
                key_terms.append(suffix)
                break

    # Pick first valid key term or use topic
    emphasis_term = key_terms[0] if key_terms else topic.split()[0]

    # Build anchor explanations
    anchor_explanations = []
    for anchor in anchors:
        text = anchor.get('text', str(anchor)) if isinstance(anchor, dict) else str(anchor)
        explanation = f"Let's talk about this key point: {text}. "

        # Add clinical context based on content keywords
        text_lower = text.lower()
        if any(kw in text_lower for kw in ['monitor', 'check', 'assess', 'evaluate']):
            explanation += "This monitoring requirement exists because early detection of problems allows for timely intervention. In clinical practice, you'll need to establish baseline values and track changes over time. "
        elif any(kw in text_lower for kw in ['never', 'avoid', 'contraindicated', 'do not']):
            explanation += "This is a critical safety point that you must remember. Violating this guideline could result in serious patient harm. On the NCLEX, watch for questions that tempt you to choose an unsafe option. "
        elif any(kw in text_lower for kw in ['before', 'first', 'priority', 'initial']):
            explanation += "The sequencing here is essential. Performing steps in the wrong order can compromise patient safety or treatment effectiveness. "
        elif any(kw in text_lower for kw in ['sign', 'symptom', 'finding', 'present']):
            explanation += "Recognizing these clinical findings is crucial for accurate assessment. The NCLEX frequently tests your ability to identify abnormal findings and respond appropriately. "
        else:
            explanation += "Understanding this concept will help you provide safe, effective care and answer related NCLEX questions with confidence. "

        anchor_explanations.append(explanation)

    # Determine transition based on slide position
    if slide_num < total_slides - 2:
        transition = "Now let's continue to our next important topic."
    else:
        transition = "We're approaching the end of this section. Let's make sure these concepts are clear."

    # Process NCLEX tip
    nclex_callout = nclex_tip.replace('NCLEX TIP:', 'On the NCLEX,') if nclex_tip else f"On the NCLEX, {topic.lower()} is frequently tested."

    # Build the full notes
    notes = f"""Now we're going to focus on {topic}. [PAUSE]

This is essential knowledge for the NCLEX, and you'll apply it frequently in clinical practice. Pay close attention to the specific details here because the exam often tests the nuances that distinguish safe practice from potentially harmful actions.

[EMPHASIS: {emphasis_term}] is the key concept to anchor your understanding here. When you see questions related to this topic on the NCLEX, start by recalling this foundational principle and work from there.

[PAUSE]

{' '.join(anchor_explanations)}

Let me connect this to clinical practice. When you're caring for patients, you'll use this knowledge to make real-time decisions about their care. The ability to quickly recall and apply these concepts can make the difference between catching a problem early and missing a critical warning sign.

{nclex_callout} Watch for questions that present similar but distinct scenarios. The test writers know the common mistakes students make, and they craft distractors specifically to catch those errors.

[PAUSE]

Before we move on, make sure you can explain why each of these points matters, not just what the correct action is. This deeper understanding will serve you well on scenario-based questions where the correct answer isn't immediately obvious.

{transition}"""

    return notes


def _generate_vignette_notes(
    topic: str,
    vignette_content: List[Any],
    section_name: str
) -> str:
    """Generate presenter notes for vignette slides (target: 250 words)."""

    notes = f"""Let's apply what we've learned with a clinical scenario. [PAUSE]

This vignette tests your ability to integrate the concepts we've covered in {section_name}. As I read through this scenario, pay attention to the key details that will help you identify the correct answer.

[PAUSE]

I'm going to read the vignette now. Listen carefully to the patient presentation, the relevant history, and what's being asked.

[Read the vignette stem aloud, emphasizing key clinical details]

[PAUSE]

Now, take a moment to think through each option carefully. Consider what you know about this topic and how it applies to this specific patient situation. Remember to use the nursing process: What assessments are relevant? What's the priority concern? What intervention would be most appropriate?

[EMPHASIS: Think before you answer]. Don't rush to select an option. The NCLEX rewards careful clinical reasoning, not quick guessing.

[PAUSE - Allow 30-60 seconds for thinking]

When you're ready, let's move on to review the answer and rationale."""

    return notes


def _generate_answer_notes(
    topic: str,
    answer_content: List[Any],
    section_name: str,
    nclex_tip: str = ""
) -> str:
    """Generate presenter notes for answer slides (target: 400 words)."""

    notes = f"""The correct answer is [EMPHASIS: revealed on slide]. [PAUSE]

Let me explain why this is the correct choice. This question tested your understanding of {topic} and your ability to apply it to a clinical scenario.

The correct answer demonstrates proper clinical reasoning because it addresses the priority concern for this patient while maintaining safety. When approaching similar questions on the NCLEX, always ask yourself: What is the most immediate threat to this patient? What action would best address that threat?

[PAUSE]

Now let's examine why the other options are incorrect. This distractor analysis is valuable because the NCLEX uses similar wrong answer patterns repeatedly.

The first incorrect option may have seemed appealing, but it fails because it either addresses a lower priority, could cause harm, or doesn't apply to this specific situation. Watch for options that are generally correct but not best for the specific scenario presented.

The second incorrect option represents a common misconception. Students often choose this because it sounds clinical or uses medical terminology, but it doesn't address the core issue in the vignette.

The third incorrect option might be appropriate in a different context, but for this particular patient presentation, it's not the priority action.

[PAUSE]

[EMPHASIS: The NCLEX testing pattern] here is asking you to prioritize. When you see questions asking for the "first," "priority," or "most important" action, remember your frameworks: ABCs, Maslow's hierarchy, and the nursing process. Safety always comes first.

This vignette exemplifies how the NCLEX integrates multiple concepts. You needed to recognize the clinical findings, understand their significance, and select the appropriate nursing response. Practice this type of integrated thinking as you study.

[PAUSE]

{nclex_tip if nclex_tip else "Remember this pattern for your exam preparation."}

Let's continue with our next topic."""

    return notes


def validate_presenter_notes(notes: str, slide_type: str = "content") -> Dict[str, Any]:
    """
    Validate presenter notes against requirements.

    Args:
        notes: The presenter notes text
        slide_type: Type of slide for word count targets

    Returns:
        Dictionary with validation results
    """
    word_count = len(notes.split())
    pause_count = notes.count("[PAUSE]")
    emphasis_count = notes.count("[EMPHASIS")

    # Word count targets by slide type
    targets = {
        "title": {"min": 200, "max": 450, "target": 350},
        "content": {"min": 250, "max": 450, "target": 380},
        "summary": {"min": 250, "max": 450, "target": 380},
        "vignette": {"min": 150, "max": 350, "target": 250},
        "answer": {"min": 250, "max": 450, "target": 400},
    }

    slide_type = slide_type.lower()
    target = targets.get(slide_type, targets["content"])

    # Validation checks
    word_count_valid = target["min"] <= word_count <= target["max"]
    pause_valid = pause_count >= 2
    emphasis_valid = emphasis_count >= 1 if slide_type in ["content", "answer"] else True

    issues = []
    if not word_count_valid:
        if word_count < target["min"]:
            issues.append(f"Word count {word_count} below minimum {target['min']}")
        else:
            issues.append(f"Word count {word_count} exceeds maximum {target['max']}")
    if not pause_valid:
        issues.append(f"Only {pause_count} [PAUSE] markers (need 2+)")
    if not emphasis_valid:
        issues.append(f"Missing [EMPHASIS] marker (need 1+)")

    return {
        "valid": word_count_valid and pause_valid and emphasis_valid,
        "word_count": word_count,
        "estimated_duration_seconds": int(word_count / 2.25),  # ~135 WPM
        "pause_count": pause_count,
        "emphasis_count": emphasis_count,
        "target": target,
        "issues": issues
    }


def count_words(text: str) -> int:
    """Count words in text."""
    return len(text.split())


def estimate_duration(word_count: int, wpm: int = 135) -> int:
    """Estimate speaking duration in seconds."""
    return int((word_count / wpm) * 60)
