"""
Timing Pacer Skill
Pace content to fit within time allocation constraints.

Theater Pipeline Requirements:
- Lecture component: 15 minutes (1,950-2,250 words at 140 WPM)
- Per-slide targets vary by type
- Must not truncate - adjust content depth instead

Usage:
    from skills.utilities.timing_pacer import (
        pace_content,
        calculate_target_words,
        suggest_content_adjustments,
        validate_pacing
    )
"""

import re
from typing import Dict, Any, List, Optional, Tuple


# Speaking rate constants
SPEAKING_RATE_WPM = 140
SPEAKING_RATE_MIN = 130
SPEAKING_RATE_MAX = 150

# Duration targets (in minutes)
LECTURE_DURATION_TARGET = 15
LECTURE_DURATION_MIN = 14
LECTURE_DURATION_MAX = 16

# Word count targets
TOTAL_WORDS_MIN = 1950
TOTAL_WORDS_TARGET = 2100
TOTAL_WORDS_MAX = 2250

# Per-slide word targets by type
SLIDE_WORD_TARGETS = {
    'auxiliary': {'min': 50, 'target': 75, 'max': 100},
    'title': {'min': 100, 'target': 125, 'max': 150},
    'content': {'min': 160, 'target': 175, 'max': 190},
    'summary': {'min': 150, 'target': 175, 'max': 200},
}

# Marker time adjustments (seconds)
MARKER_TIMES = {
    'pause': 2.0,
    'emphasis': 0.5,
    'check_understanding': 5.0,
}


def count_words(text: str) -> int:
    """Count words excluding markers."""
    if not text:
        return 0
    cleaned = re.sub(r'\[[^\]]+\]', '', text)
    return len([w for w in cleaned.split() if w.strip()])


def count_markers(text: str) -> Dict[str, int]:
    """Count markers in text."""
    if not text:
        return {'pause': 0, 'emphasis': 0, 'check_understanding': 0}

    return {
        'pause': len(re.findall(r'\[PAUSE[^\]]*\]', text, re.IGNORECASE)),
        'emphasis': len(re.findall(r'\[EMPHASIS[:\s][^\]]+\]', text, re.IGNORECASE)),
        'check_understanding': len(re.findall(r'\[CHECK FOR UNDERSTANDING\]', text, re.IGNORECASE)),
    }


def estimate_duration(text: str, wpm: int = SPEAKING_RATE_WPM) -> float:
    """
    Estimate speaking duration in minutes.

    Args:
        text: Text to estimate
        wpm: Words per minute

    Returns:
        Duration in minutes
    """
    word_count = count_words(text)
    markers = count_markers(text)

    # Base speaking time
    speaking_minutes = word_count / wpm

    # Add marker time
    marker_seconds = (
        markers['pause'] * MARKER_TIMES['pause'] +
        markers['emphasis'] * MARKER_TIMES['emphasis'] +
        markers['check_understanding'] * MARKER_TIMES['check_understanding']
    )

    total_minutes = speaking_minutes + (marker_seconds / 60)
    return round(total_minutes, 2)


def calculate_target_words(
    duration_minutes: float,
    wpm: int = SPEAKING_RATE_WPM,
    marker_count: int = 0
) -> int:
    """
    Calculate target word count for a duration.

    Args:
        duration_minutes: Target duration
        wpm: Speaking rate
        marker_count: Expected number of markers (for time adjustment)

    Returns:
        Target word count
    """
    # Subtract marker time
    marker_seconds = marker_count * MARKER_TIMES['pause']
    available_minutes = duration_minutes - (marker_seconds / 60)

    return int(available_minutes * wpm)


def get_slide_target(slide_type: str) -> Dict[str, int]:
    """Get word count targets for a slide type."""
    return SLIDE_WORD_TARGETS.get(slide_type.lower(), SLIDE_WORD_TARGETS['content'])


def pace_content(
    content: str,
    target_words: int,
    slide_type: str = 'content'
) -> Dict[str, Any]:
    """
    Analyze content pacing against target.

    Args:
        content: Text content
        target_words: Target word count
        slide_type: Type of slide

    Returns:
        Pacing analysis with recommendations
    """
    current_words = count_words(content)
    targets = get_slide_target(slide_type)
    duration = estimate_duration(content)

    # Calculate deviation
    deviation = current_words - target_words
    deviation_pct = (deviation / target_words * 100) if target_words > 0 else 0

    # Determine status
    if current_words < targets['min']:
        status = 'under'
        action = 'expand'
    elif current_words > targets['max']:
        status = 'over'
        action = 'condense'
    else:
        status = 'ok'
        action = 'none'

    return {
        'current_words': current_words,
        'target_words': target_words,
        'deviation': deviation,
        'deviation_pct': round(deviation_pct, 1),
        'status': status,
        'action': action,
        'estimated_duration_minutes': duration,
        'slide_type': slide_type,
        'targets': targets
    }


def suggest_content_adjustments(
    pacing_result: Dict[str, Any]
) -> List[Dict[str, Any]]:
    """
    Suggest specific adjustments to meet pacing targets.

    Args:
        pacing_result: Result from pace_content()

    Returns:
        List of suggested adjustments
    """
    suggestions = []
    action = pacing_result['action']
    deviation = abs(pacing_result['deviation'])

    if action == 'expand':
        # Content needs to be longer
        suggestions.append({
            'type': 'add_example',
            'description': f'Add a concrete example (+20-30 words)',
            'words_impact': 25,
            'priority': 'high' if deviation > 50 else 'medium'
        })

        suggestions.append({
            'type': 'add_context',
            'description': f'Add historical/cultural context (+15-25 words)',
            'words_impact': 20,
            'priority': 'medium'
        })

        suggestions.append({
            'type': 'add_connection',
            'description': f'Add connection to prior learning (+10-15 words)',
            'words_impact': 12,
            'priority': 'low'
        })

        if deviation > 30:
            suggestions.append({
                'type': 'add_elaboration',
                'description': f'Elaborate on key concept (+25-40 words)',
                'words_impact': 32,
                'priority': 'high'
            })

    elif action == 'condense':
        # Content needs to be shorter
        suggestions.append({
            'type': 'remove_redundancy',
            'description': f'Remove redundant phrases (-15-25 words)',
            'words_impact': -20,
            'priority': 'high' if deviation > 50 else 'medium'
        })

        suggestions.append({
            'type': 'simplify_sentences',
            'description': f'Simplify complex sentences (-10-20 words)',
            'words_impact': -15,
            'priority': 'medium'
        })

        suggestions.append({
            'type': 'move_to_handout',
            'description': f'Move detailed info to handout (-20-40 words)',
            'words_impact': -30,
            'priority': 'low'
        })

    return suggestions


def pace_presentation(
    slides: List[Dict[str, Any]],
    total_duration_target: float = LECTURE_DURATION_TARGET
) -> Dict[str, Any]:
    """
    Analyze pacing for entire presentation.

    Args:
        slides: List of slide dictionaries with 'notes' and 'type'
        total_duration_target: Target total duration in minutes

    Returns:
        Complete pacing analysis
    """
    per_slide = []
    total_words = 0
    total_duration = 0

    for i, slide in enumerate(slides):
        notes = slide.get('notes', slide.get('presenter_notes', ''))
        slide_type = slide.get('type', slide.get('slide_type', 'content'))
        slide_num = slide.get('slide_number', i + 1)

        targets = get_slide_target(slide_type)
        word_count = count_words(notes)
        duration = estimate_duration(notes)

        total_words += word_count
        total_duration += duration

        # Determine per-slide target based on proportion
        # Content slides get more, auxiliary less
        if slide_type == 'auxiliary':
            proportion = 0.04  # 4% each for 4 auxiliary slides = 16%
        elif slide_type == 'title':
            proportion = 0.05  # 5% for title
        elif slide_type == 'summary':
            proportion = 0.07  # 7% for summary
        else:
            proportion = 0.06  # ~6% each for 10 content slides = 60%

        target_words_for_slide = int(TOTAL_WORDS_TARGET * proportion)

        status = 'ok'
        if word_count < targets['min']:
            status = 'under'
        elif word_count > targets['max']:
            status = 'over'

        per_slide.append({
            'slide_number': slide_num,
            'slide_type': slide_type,
            'word_count': word_count,
            'target_words': target_words_for_slide,
            'duration_minutes': duration,
            'status': status,
            'targets': targets
        })

    # Calculate overall status
    if total_words < TOTAL_WORDS_MIN:
        overall_status = 'under'
        words_needed = TOTAL_WORDS_MIN - total_words
    elif total_words > TOTAL_WORDS_MAX:
        overall_status = 'over'
        words_needed = total_words - TOTAL_WORDS_MAX
    else:
        overall_status = 'ok'
        words_needed = 0

    # Duration check
    if total_duration < LECTURE_DURATION_MIN:
        duration_status = 'short'
    elif total_duration > LECTURE_DURATION_MAX:
        duration_status = 'long'
    else:
        duration_status = 'ok'

    return {
        'total_words': total_words,
        'total_duration_minutes': round(total_duration, 2),
        'target_duration': total_duration_target,
        'word_count_status': overall_status,
        'duration_status': duration_status,
        'words_adjustment_needed': words_needed,
        'per_slide': per_slide,
        'summary': {
            'slides_under': sum(1 for s in per_slide if s['status'] == 'under'),
            'slides_over': sum(1 for s in per_slide if s['status'] == 'over'),
            'slides_ok': sum(1 for s in per_slide if s['status'] == 'ok'),
        }
    }


def validate_pacing(
    slides: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """
    Validate presentation meets all pacing requirements.

    Args:
        slides: List of slide dictionaries

    Returns:
        Validation result
    """
    analysis = pace_presentation(slides)

    issues = []

    # Check total word count
    if analysis['word_count_status'] == 'under':
        issues.append({
            'type': 'total_words_under',
            'severity': 'error',
            'message': f"Total words ({analysis['total_words']}) below minimum ({TOTAL_WORDS_MIN})",
            'adjustment': f"Add {TOTAL_WORDS_MIN - analysis['total_words']} words"
        })
    elif analysis['word_count_status'] == 'over':
        issues.append({
            'type': 'total_words_over',
            'severity': 'warning',
            'message': f"Total words ({analysis['total_words']}) above maximum ({TOTAL_WORDS_MAX})",
            'adjustment': f"Remove {analysis['total_words'] - TOTAL_WORDS_MAX} words"
        })

    # Check duration
    if analysis['duration_status'] == 'short':
        issues.append({
            'type': 'duration_short',
            'severity': 'error',
            'message': f"Duration ({analysis['total_duration_minutes']} min) below minimum ({LECTURE_DURATION_MIN} min)"
        })
    elif analysis['duration_status'] == 'long':
        issues.append({
            'type': 'duration_long',
            'severity': 'warning',
            'message': f"Duration ({analysis['total_duration_minutes']} min) above maximum ({LECTURE_DURATION_MAX} min)"
        })

    # Check individual slides
    for slide in analysis['per_slide']:
        if slide['status'] == 'under':
            issues.append({
                'type': 'slide_under',
                'severity': 'warning',
                'slide_number': slide['slide_number'],
                'message': f"Slide {slide['slide_number']} under target ({slide['word_count']} words)"
            })

    error_count = sum(1 for i in issues if i.get('severity') == 'error')

    return {
        'valid': error_count == 0,
        'analysis': analysis,
        'issues': issues,
        'error_count': error_count,
        'warning_count': len(issues) - error_count
    }


def distribute_words(
    total_words: int,
    slide_count: int = 16,
    auxiliary_count: int = 4
) -> Dict[str, int]:
    """
    Suggest word distribution across slides.

    Args:
        total_words: Total words to distribute
        slide_count: Total number of slides
        auxiliary_count: Number of auxiliary slides

    Returns:
        Suggested distribution
    """
    content_count = slide_count - auxiliary_count - 2  # -2 for title and summary

    # Auxiliary slides get less
    auxiliary_per = int(total_words * 0.04)  # 4% each
    title_words = int(total_words * 0.05)  # 5%
    summary_words = int(total_words * 0.08)  # 8%

    remaining = total_words - (auxiliary_per * auxiliary_count) - title_words - summary_words
    content_per = remaining // content_count

    return {
        'auxiliary_per_slide': auxiliary_per,
        'title_slide': title_words,
        'summary_slide': summary_words,
        'content_per_slide': content_per,
        'distribution': {
            'auxiliary_total': auxiliary_per * auxiliary_count,
            'title': title_words,
            'content_total': content_per * content_count,
            'summary': summary_words,
            'grand_total': (auxiliary_per * auxiliary_count) + title_words + (content_per * content_count) + summary_words
        }
    }


if __name__ == "__main__":
    # Test
    print("Timing Pacer Test")
    print("=" * 50)

    # Test word distribution
    dist = distribute_words(2100, 16, 4)
    print(f"\nWord distribution for 2100 words across 16 slides:")
    print(f"  Auxiliary (4): {dist['auxiliary_per_slide']} each")
    print(f"  Title: {dist['title_slide']}")
    print(f"  Content (10): {dist['content_per_slide']} each")
    print(f"  Summary: {dist['summary_slide']}")
    print(f"  Total: {dist['distribution']['grand_total']}")

    # Test pacing
    test_text = "This is a test sentence. " * 30 + "[PAUSE] More content here. [EMPHASIS: test]"
    result = pace_content(test_text, 175, 'content')
    print(f"\nPacing analysis:")
    print(f"  Words: {result['current_words']}")
    print(f"  Target: {result['target_words']}")
    print(f"  Status: {result['status']}")
    print(f"  Duration: {result['estimated_duration_minutes']} min")
