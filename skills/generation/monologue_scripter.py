"""
Monologue Scripter Skill
Generates verbatim presenter notes for theater education lectures.

Targets: 15-minute presentation (1,950-2,250 words at 140 WPM)

Usage:
    from skills.generation.monologue_scripter import (
        generate_presenter_notes,
        generate_slide_notes,
        estimate_duration
    )
"""

import re
from typing import Dict, Any, List, Optional


# Constants from config/constraints.yaml
SPEAKING_RATE_WPM = 140
TARGET_DURATION_MINUTES = 15
MIN_WORDS = 1950
MAX_WORDS = 2250
TARGET_WORDS = 2100

# Per-slide word targets
SLIDE_WORD_TARGETS = {
    'title': {'min': 100, 'target': 125, 'max': 150},
    'intro': {'min': 100, 'target': 125, 'max': 150},
    'content': {'min': 160, 'target': 175, 'max': 190},
    'summary': {'min': 150, 'target': 175, 'max': 200},
    'auxiliary': {'min': 50, 'target': 75, 'max': 100},
}

# Marker requirements
MIN_PAUSE_PER_SLIDE = 2
MIN_EMPHASIS_PER_CONTENT_SLIDE = 1
MIN_CHECK_UNDERSTANDING_TOTAL = 3

# Transition phrases for natural flow
TRANSITION_PHRASES = [
    "Now, let's move on to",
    "Building on that idea,",
    "This connects directly to",
    "Next, we'll explore",
    "With that foundation in place,",
    "Let's take this further and look at",
    "Here's where it gets interesting:",
    "Now here's the key point:",
    "Think about this:",
    "Consider what this means for your performance:",
]

# Theater-specific engagement phrases
ENGAGEMENT_PHRASES = {
    'greek_theater': [
        "Imagine yourself in ancient Athens...",
        "Picture 17,000 people watching this unfold...",
        "When you perform Greek theater, remember...",
        "The Greeks understood something fundamental about performance...",
    ],
    'commedia_dellarte': [
        "Think about how your body tells the story...",
        "In Commedia, the mask leads everything...",
        "This is where physical comedy becomes art...",
        "The audience should know your character instantly...",
    ],
    'shakespeare': [
        "Listen to the rhythm of the language...",
        "Shakespeare wrote for speaking, not reading...",
        "Trust the verse—it tells you how to breathe...",
        "The groundlings needed to understand every word...",
    ],
    'student_directed_one_acts': [
        "As a director, your job is to...",
        "Think about what you want the audience to feel...",
        "Every choice you make should serve the story...",
        "Your actors are your collaborators, not your instruments...",
    ],
    'default': [
        "In performance, this translates to...",
        "When you're on stage, remember...",
        "Think about how this applies to your work...",
        "The key to making this work is...",
    ]
}


def count_words(text: str) -> int:
    """Count words in text."""
    if not text:
        return 0
    return len(text.split())


def estimate_duration(word_count: int, wpm: int = SPEAKING_RATE_WPM) -> float:
    """Estimate speaking duration in minutes."""
    return word_count / wpm


def get_unit_key(unit: str) -> str:
    """Normalize unit name to key."""
    unit_lower = unit.lower().replace(' ', '_').replace('-', '_').replace("'", '')

    mappings = {
        'greek': 'greek_theater',
        'greek_theater': 'greek_theater',
        'unit_1': 'greek_theater',
        'commedia': 'commedia_dellarte',
        'commedia_dellarte': 'commedia_dellarte',
        'commedia_dell_arte': 'commedia_dellarte',
        'unit_2': 'commedia_dellarte',
        'shakespeare': 'shakespeare',
        'unit_3': 'shakespeare',
        'one_acts': 'student_directed_one_acts',
        'student_directed': 'student_directed_one_acts',
        'student_directed_one_acts': 'student_directed_one_acts',
        'unit_4': 'student_directed_one_acts',
    }

    return mappings.get(unit_lower, 'default')


def insert_markers(notes: str, slide_type: str, unit: str = 'default') -> str:
    """
    Insert required markers into presenter notes.

    Markers:
    - [PAUSE]: Natural break points (min 2 per slide)
    - [EMPHASIS: term]: Key vocabulary (min 1 per content slide)
    - [CHECK FOR UNDERSTANDING]: Comprehension checks
    """
    result = notes

    # Split into sentences for marker insertion
    sentences = re.split(r'(?<=[.!?])\s+', result)

    if len(sentences) < 2:
        return result

    # Insert [PAUSE] after first sentence
    if '[PAUSE]' not in sentences[0]:
        sentences[0] = sentences[0] + ' [PAUSE]'

    # Insert [PAUSE] before last sentence if we don't have 2 yet
    pause_count = result.count('[PAUSE]')
    if pause_count < MIN_PAUSE_PER_SLIDE and len(sentences) >= 3:
        # Find a good spot in the middle
        mid = len(sentences) // 2
        if '[PAUSE]' not in sentences[mid]:
            sentences[mid] = '[PAUSE] ' + sentences[mid]

    result = ' '.join(sentences)

    return result


def generate_slide_notes(
    slide: Dict[str, Any],
    slide_index: int,
    total_slides: int,
    unit: str,
    vocabulary: List[Dict[str, str]] = None,
    learning_objectives: List[str] = None,
    content_points: List[str] = None
) -> str:
    """
    Generate presenter notes for a single slide.

    Args:
        slide: Slide dictionary with header, body, type
        slide_index: 0-based index of this slide
        total_slides: Total number of slides
        unit: Unit name for context
        vocabulary: List of vocabulary terms
        learning_objectives: Learning objectives
        content_points: Key content points

    Returns:
        Verbatim presenter notes for this slide
    """
    slide_type = slide.get('type', slide.get('slide_type', 'content')).lower()
    header = slide.get('header', slide.get('title', ''))
    body = slide.get('body', '')

    unit_key = get_unit_key(unit)
    engagement = ENGAGEMENT_PHRASES.get(unit_key, ENGAGEMENT_PHRASES['default'])

    # Determine word target based on slide type
    if slide_type in ['title', 'intro', 'section_intro']:
        targets = SLIDE_WORD_TARGETS['title']
    elif slide_type in ['summary', 'conclusion']:
        targets = SLIDE_WORD_TARGETS['summary']
    elif slide_type in ['auxiliary', 'agenda', 'warmup', 'activity', 'journal']:
        targets = SLIDE_WORD_TARGETS['auxiliary']
    else:
        targets = SLIDE_WORD_TARGETS['content']

    notes_parts = []

    # Opening based on slide position
    if slide_index == 0:
        notes_parts.append(f"Welcome everyone. Today we're diving into {header}.")
        notes_parts.append("[PAUSE]")
    elif slide_index == total_slides - 1:
        notes_parts.append(f"Let's wrap up what we've learned today about {header}.")
    else:
        # Use transition phrase
        transition = TRANSITION_PHRASES[slide_index % len(TRANSITION_PHRASES)]
        notes_parts.append(f"{transition} {header}.")

    notes_parts.append("[PAUSE]")

    # Main content expansion
    if body:
        # Split body into points
        body_points = [p.strip() for p in body.split('\n') if p.strip()]

        for i, point in enumerate(body_points):
            # Clean bullet markers
            clean_point = re.sub(r'^[-•]\s*', '', point)

            # Expand the point with explanation
            notes_parts.append(f"Let's look at this: {clean_point}")

            # Add elaboration
            if slide_type == 'content':
                notes_parts.append("This is important because it directly affects how you'll approach your performance work.")

                # Add engagement phrase occasionally
                if i == 0 and engagement:
                    notes_parts.append(engagement[slide_index % len(engagement)])

    # Add vocabulary emphasis if applicable
    if vocabulary and slide_type == 'content':
        vocab_terms = [v.get('term', '') for v in vocabulary]
        for term in vocab_terms:
            if term.lower() in body.lower() or term.lower() in header.lower():
                notes_parts.append(f"[EMPHASIS: {term}]")
                notes_parts.append(f"Remember, {term} is a key concept you'll use throughout this unit.")
                break

    # Add check for understanding at strategic points
    if slide_index > 0 and slide_index % 4 == 0 and slide_type == 'content':
        notes_parts.append("[CHECK FOR UNDERSTANDING]")
        notes_parts.append("Quick check—can someone tell me what we just covered?")
        notes_parts.append("[PAUSE]")

    # Closing for slide
    if slide_index < total_slides - 1:
        notes_parts.append("[PAUSE]")
        notes_parts.append("Let's continue.")
    else:
        notes_parts.append("[PAUSE]")
        notes_parts.append("Great work today, everyone.")

    # Join and verify word count
    notes = ' '.join(notes_parts)
    current_words = count_words(notes)

    # Pad if too short
    while current_words < targets['min']:
        padding = "Take a moment to let this sink in. This concept will come up again as we progress through the unit."
        notes += f" [PAUSE] {padding}"
        current_words = count_words(notes)

    return notes


def generate_presenter_notes(
    slides: List[Dict[str, Any]],
    unit: str,
    vocabulary: List[Dict[str, str]] = None,
    learning_objectives: List[str] = None,
    content_points: List[str] = None,
    topic: str = None
) -> Dict[str, Any]:
    """
    Generate complete presenter notes for all slides.

    Args:
        slides: List of slide dictionaries
        unit: Unit name
        vocabulary: Vocabulary terms
        learning_objectives: Learning objectives
        content_points: Key content points
        topic: Lesson topic

    Returns:
        {
            'slides': list of {slide_number, notes, word_count},
            'total_word_count': int,
            'estimated_duration_minutes': float,
            'markers': {pause_count, emphasis_count, check_understanding_count},
            'within_target': bool,
            'issues': list
        }
    """
    result_slides = []
    total_words = 0
    total_pauses = 0
    total_emphasis = 0
    total_checks = 0
    issues = []

    for i, slide in enumerate(slides):
        notes = generate_slide_notes(
            slide=slide,
            slide_index=i,
            total_slides=len(slides),
            unit=unit,
            vocabulary=vocabulary,
            learning_objectives=learning_objectives,
            content_points=content_points
        )

        # Insert markers
        slide_type = slide.get('type', slide.get('slide_type', 'content')).lower()
        notes = insert_markers(notes, slide_type, unit)

        word_count = count_words(notes)
        total_words += word_count

        # Count markers
        pause_count = notes.count('[PAUSE]')
        emphasis_count = len(re.findall(r'\[EMPHASIS[:\s][^\]]+\]', notes))
        check_count = notes.count('[CHECK FOR UNDERSTANDING]')

        total_pauses += pause_count
        total_emphasis += emphasis_count
        total_checks += check_count

        # Check per-slide requirements
        if pause_count < MIN_PAUSE_PER_SLIDE:
            issues.append(f"Slide {i+1}: Only {pause_count} [PAUSE] markers, need {MIN_PAUSE_PER_SLIDE}")

        if slide_type == 'content' and emphasis_count < MIN_EMPHASIS_PER_CONTENT_SLIDE:
            issues.append(f"Slide {i+1}: No [EMPHASIS] marker on content slide")

        result_slides.append({
            'slide_number': slide.get('slide_number', i + 1),
            'notes': notes,
            'word_count': word_count,
            'markers': {
                'pause': pause_count,
                'emphasis': emphasis_count,
                'check_understanding': check_count
            }
        })

    # Check total requirements
    duration = estimate_duration(total_words)

    if total_words < MIN_WORDS:
        issues.append(f"Total word count {total_words} below minimum {MIN_WORDS}")
    elif total_words > MAX_WORDS:
        issues.append(f"Total word count {total_words} above maximum {MAX_WORDS}")

    if total_checks < MIN_CHECK_UNDERSTANDING_TOTAL:
        issues.append(f"Only {total_checks} [CHECK FOR UNDERSTANDING] markers, need {MIN_CHECK_UNDERSTANDING_TOTAL}")

    return {
        'slides': result_slides,
        'total_word_count': total_words,
        'estimated_duration_minutes': round(duration, 1),
        'target_duration_minutes': TARGET_DURATION_MINUTES,
        'markers': {
            'pause_count': total_pauses,
            'emphasis_count': total_emphasis,
            'check_understanding_count': total_checks
        },
        'within_target': MIN_WORDS <= total_words <= MAX_WORDS,
        'issues': issues
    }


def validate_presenter_notes(notes_result: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate presenter notes meet all requirements.

    Returns:
        {
            'valid': bool,
            'word_count_valid': bool,
            'duration_valid': bool,
            'markers_valid': bool,
            'issues': list
        }
    """
    issues = list(notes_result.get('issues', []))

    word_count = notes_result.get('total_word_count', 0)
    duration = notes_result.get('estimated_duration_minutes', 0)
    markers = notes_result.get('markers', {})

    word_count_valid = MIN_WORDS <= word_count <= MAX_WORDS
    duration_valid = 14 <= duration <= 16
    markers_valid = (
        markers.get('check_understanding_count', 0) >= MIN_CHECK_UNDERSTANDING_TOTAL
    )

    return {
        'valid': word_count_valid and duration_valid and markers_valid and len(issues) == 0,
        'word_count_valid': word_count_valid,
        'duration_valid': duration_valid,
        'markers_valid': markers_valid,
        'issues': issues
    }


if __name__ == "__main__":
    # Test with sample slides
    test_slides = [
        {'slide_number': 1, 'type': 'title', 'header': 'Introduction to Greek Theater', 'body': ''},
        {'slide_number': 2, 'type': 'content', 'header': 'Origins of Theater',
         'body': '- Theater originated from religious rituals\n- Festival of Dionysus was central\n- Dithyrambs were the first performances'},
        {'slide_number': 3, 'type': 'content', 'header': 'The Greek Theater Space',
         'body': '- Orchestra: circular dancing space\n- Theatron: audience seating\n- Skene: stage building'},
        {'slide_number': 4, 'type': 'summary', 'header': 'Key Takeaways', 'body': '- Religious origins\n- Physical structure\n- Performance traditions'},
    ]

    test_vocab = [
        {'term': 'Dionysus', 'definition': 'Greek god of wine and theater'},
        {'term': 'orchestra', 'definition': 'Circular dancing space'},
        {'term': 'theatron', 'definition': 'Audience seating area'},
    ]

    result = generate_presenter_notes(
        slides=test_slides,
        unit='greek_theater',
        vocabulary=test_vocab
    )

    print(f"Total words: {result['total_word_count']}")
    print(f"Estimated duration: {result['estimated_duration_minutes']} minutes")
    print(f"Within target: {result['within_target']}")
    print(f"Markers: {result['markers']}")

    if result['issues']:
        print(f"\nIssues:")
        for issue in result['issues']:
            print(f"  - {issue}")

    print(f"\nSample notes (Slide 2):")
    print(result['slides'][1]['notes'][:500] + "...")
