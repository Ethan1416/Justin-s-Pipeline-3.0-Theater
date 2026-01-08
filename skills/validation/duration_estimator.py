"""
Duration Estimator Skill
Estimates speaking duration for presenter notes and validates timing requirements.

Theater Pipeline Requirements:
- Target duration: 15 minutes (lecture component)
- Acceptable range: 14-16 minutes
- Speaking rate: 140 WPM (average)
- Pause markers add ~2 seconds each

Usage:
    from skills.validation.duration_estimator import (
        estimate_duration,
        estimate_slide_duration,
        validate_timing,
        get_pacing_analysis
    )
"""

import re
from typing import Dict, Any, List, Optional, Tuple


# Speaking rate constants
SPEAKING_RATE_WPM = 140  # Average speaking rate
SPEAKING_RATE_MIN = 130  # Slower delivery
SPEAKING_RATE_MAX = 150  # Faster delivery

# Duration requirements
TARGET_DURATION_MINUTES = 15
MIN_DURATION_MINUTES = 14
MAX_DURATION_MINUTES = 16

# Marker timing adjustments (in seconds)
MARKER_DURATIONS = {
    'pause': 2.0,           # [PAUSE]
    'pause_short': 1.5,     # [PAUSE - 1 second]
    'pause_long': 4.0,      # [PAUSE - 3 seconds]
    'emphasis': 0.5,        # [EMPHASIS: term] - slight pause
    'check_understanding': 5.0,  # [CHECK FOR UNDERSTANDING] - time for response
}

# Per-slide duration targets (in seconds)
SLIDE_DURATION_TARGETS = {
    'title': {'min': 45, 'target': 55, 'max': 65},
    'intro': {'min': 45, 'target': 55, 'max': 65},
    'section_intro': {'min': 45, 'target': 55, 'max': 65},
    'content': {'min': 70, 'target': 80, 'max': 90},
    'summary': {'min': 60, 'target': 75, 'max': 90},
    'auxiliary': {'min': 30, 'target': 40, 'max': 50},
}

DEFAULT_SLIDE_DURATION = {'min': 60, 'target': 75, 'max': 90}


def count_words(text: str) -> int:
    """Count words in text, excluding markers."""
    if not text:
        return 0
    cleaned = re.sub(r'\[[^\]]+\]', '', text)
    return len([w for w in cleaned.split() if w.strip()])


def count_markers(text: str) -> Dict[str, int]:
    """
    Count different types of markers in text.

    Returns:
        Dictionary with counts for each marker type
    """
    if not text:
        return {'pause': 0, 'emphasis': 0, 'check_understanding': 0}

    pause_count = len(re.findall(r'\[PAUSE[^\]]*\]', text, re.IGNORECASE))
    emphasis_count = len(re.findall(r'\[EMPHASIS[:\s][^\]]+\]', text, re.IGNORECASE))
    check_count = len(re.findall(r'\[CHECK FOR UNDERSTANDING\]', text, re.IGNORECASE))

    return {
        'pause': pause_count,
        'emphasis': emphasis_count,
        'check_understanding': check_count
    }


def calculate_marker_time(markers: Dict[str, int]) -> float:
    """
    Calculate total time added by markers (in seconds).

    Args:
        markers: Dictionary of marker counts

    Returns:
        Total seconds added by markers
    """
    total = 0.0
    total += markers.get('pause', 0) * MARKER_DURATIONS['pause']
    total += markers.get('emphasis', 0) * MARKER_DURATIONS['emphasis']
    total += markers.get('check_understanding', 0) * MARKER_DURATIONS['check_understanding']
    return total


def estimate_duration(
    text: str,
    wpm: int = SPEAKING_RATE_WPM,
    include_markers: bool = True
) -> float:
    """
    Estimate speaking duration for text.

    Args:
        text: Text to estimate
        wpm: Words per minute speaking rate
        include_markers: Whether to add time for markers

    Returns:
        Estimated duration in minutes
    """
    word_count = count_words(text)
    base_minutes = word_count / wpm

    if include_markers:
        markers = count_markers(text)
        marker_seconds = calculate_marker_time(markers)
        base_minutes += marker_seconds / 60

    return round(base_minutes, 2)


def estimate_slide_duration(
    notes: str,
    slide_type: str = 'content',
    wpm: int = SPEAKING_RATE_WPM
) -> Dict[str, Any]:
    """
    Estimate duration for a single slide.

    Args:
        notes: Presenter notes for the slide
        slide_type: Type of slide
        wpm: Speaking rate

    Returns:
        Duration analysis for the slide
    """
    word_count = count_words(notes)
    markers = count_markers(notes)

    # Base speaking time
    speaking_seconds = (word_count / wpm) * 60

    # Marker time
    marker_seconds = calculate_marker_time(markers)

    # Total time
    total_seconds = speaking_seconds + marker_seconds

    # Get targets
    targets = SLIDE_DURATION_TARGETS.get(slide_type.lower(), DEFAULT_SLIDE_DURATION)

    # Determine status
    if total_seconds < targets['min']:
        status = 'short'
    elif total_seconds > targets['max']:
        status = 'long'
    else:
        status = 'ok'

    return {
        'word_count': word_count,
        'markers': markers,
        'speaking_seconds': round(speaking_seconds, 1),
        'marker_seconds': round(marker_seconds, 1),
        'total_seconds': round(total_seconds, 1),
        'total_minutes': round(total_seconds / 60, 2),
        'targets': targets,
        'status': status,
        'slide_type': slide_type
    }


def estimate_presentation_duration(
    slides: List[Dict[str, Any]],
    wpm: int = SPEAKING_RATE_WPM
) -> Dict[str, Any]:
    """
    Estimate total presentation duration.

    Args:
        slides: List of slide dictionaries with 'notes' and optional 'type'
        wpm: Speaking rate

    Returns:
        Complete duration analysis
    """
    per_slide = []
    total_words = 0
    total_speaking_seconds = 0
    total_marker_seconds = 0

    for i, slide in enumerate(slides):
        notes = slide.get('notes', slide.get('presenter_notes', ''))
        slide_type = slide.get('type', slide.get('slide_type', 'content'))
        slide_num = slide.get('slide_number', i + 1)

        analysis = estimate_slide_duration(notes, slide_type, wpm)
        analysis['slide_number'] = slide_num

        total_words += analysis['word_count']
        total_speaking_seconds += analysis['speaking_seconds']
        total_marker_seconds += analysis['marker_seconds']

        per_slide.append(analysis)

    total_seconds = total_speaking_seconds + total_marker_seconds
    total_minutes = total_seconds / 60

    return {
        'total_words': total_words,
        'total_speaking_seconds': round(total_speaking_seconds, 1),
        'total_marker_seconds': round(total_marker_seconds, 1),
        'total_seconds': round(total_seconds, 1),
        'total_minutes': round(total_minutes, 2),
        'speaking_rate_wpm': wpm,
        'per_slide': per_slide,
        'slide_count': len(slides)
    }


def validate_timing(
    slides: List[Dict[str, Any]],
    wpm: int = SPEAKING_RATE_WPM
) -> Dict[str, Any]:
    """
    Validate presentation timing meets requirements.

    Args:
        slides: List of slide dictionaries
        wpm: Speaking rate

    Returns:
        Validation result with pass/fail and issues
    """
    analysis = estimate_presentation_duration(slides, wpm)

    issues = []
    duration = analysis['total_minutes']

    # Check overall duration
    if duration < MIN_DURATION_MINUTES:
        issues.append({
            'type': 'duration_short',
            'severity': 'error',
            'message': f"Duration ({duration:.1f} min) below minimum ({MIN_DURATION_MINUTES} min)",
            'current': duration,
            'required': MIN_DURATION_MINUTES,
            'gap': MIN_DURATION_MINUTES - duration
        })
    elif duration > MAX_DURATION_MINUTES:
        issues.append({
            'type': 'duration_long',
            'severity': 'error',
            'message': f"Duration ({duration:.1f} min) above maximum ({MAX_DURATION_MINUTES} min)",
            'current': duration,
            'required': MAX_DURATION_MINUTES,
            'excess': duration - MAX_DURATION_MINUTES
        })

    # Check individual slides
    for slide in analysis['per_slide']:
        if slide['status'] == 'short':
            issues.append({
                'type': 'slide_short',
                'severity': 'warning',
                'slide_number': slide['slide_number'],
                'message': f"Slide {slide['slide_number']} too short ({slide['total_seconds']:.0f}s, min {slide['targets']['min']}s)"
            })
        elif slide['status'] == 'long':
            issues.append({
                'type': 'slide_long',
                'severity': 'warning',
                'slide_number': slide['slide_number'],
                'message': f"Slide {slide['slide_number']} too long ({slide['total_seconds']:.0f}s, max {slide['targets']['max']}s)"
            })

    # Count errors and warnings
    error_count = sum(1 for i in issues if i.get('severity') == 'error')
    warning_count = sum(1 for i in issues if i.get('severity') == 'warning')

    return {
        'valid': error_count == 0,
        'duration_minutes': duration,
        'target_range': f"{MIN_DURATION_MINUTES}-{MAX_DURATION_MINUTES} min",
        'target_minutes': TARGET_DURATION_MINUTES,
        'within_range': MIN_DURATION_MINUTES <= duration <= MAX_DURATION_MINUTES,
        'issues': issues,
        'error_count': error_count,
        'warning_count': warning_count,
        'analysis': analysis
    }


def get_pacing_analysis(
    slides: List[Dict[str, Any]],
    wpm: int = SPEAKING_RATE_WPM
) -> Dict[str, Any]:
    """
    Analyze pacing across the presentation.

    Returns insights about pacing variation and consistency.
    """
    analysis = estimate_presentation_duration(slides, wpm)

    durations = [s['total_seconds'] for s in analysis['per_slide']]

    if not durations:
        return {
            'average_seconds': 0,
            'min_seconds': 0,
            'max_seconds': 0,
            'variation': 0,
            'consistency': 'unknown',
            'recommendations': []
        }

    avg_duration = sum(durations) / len(durations)
    min_duration = min(durations)
    max_duration = max(durations)
    variation = max_duration - min_duration

    # Calculate standard deviation
    variance = sum((d - avg_duration) ** 2 for d in durations) / len(durations)
    std_dev = variance ** 0.5

    # Determine consistency
    if std_dev < 10:
        consistency = 'very_consistent'
    elif std_dev < 20:
        consistency = 'consistent'
    elif std_dev < 30:
        consistency = 'moderate'
    else:
        consistency = 'inconsistent'

    # Generate recommendations
    recommendations = []

    if consistency == 'inconsistent':
        recommendations.append("Consider balancing content across slides for more even pacing")

    # Find outliers
    short_slides = [s for s in analysis['per_slide'] if s['total_seconds'] < avg_duration - std_dev * 1.5]
    long_slides = [s for s in analysis['per_slide'] if s['total_seconds'] > avg_duration + std_dev * 1.5]

    if short_slides:
        nums = [s['slide_number'] for s in short_slides]
        recommendations.append(f"Slides {nums} are significantly shorter than average - consider elaborating")

    if long_slides:
        nums = [s['slide_number'] for s in long_slides]
        recommendations.append(f"Slides {nums} are significantly longer than average - consider condensing")

    return {
        'average_seconds': round(avg_duration, 1),
        'average_minutes': round(avg_duration / 60, 2),
        'min_seconds': round(min_duration, 1),
        'max_seconds': round(max_duration, 1),
        'variation_seconds': round(variation, 1),
        'std_deviation': round(std_dev, 1),
        'consistency': consistency,
        'short_outliers': [s['slide_number'] for s in short_slides],
        'long_outliers': [s['slide_number'] for s in long_slides],
        'recommendations': recommendations
    }


def calculate_time_adjustment(
    current_duration: float,
    target_duration: float = TARGET_DURATION_MINUTES
) -> Dict[str, Any]:
    """
    Calculate how much to add/remove to reach target duration.

    Args:
        current_duration: Current duration in minutes
        target_duration: Target duration in minutes

    Returns:
        Adjustment recommendation
    """
    diff_minutes = target_duration - current_duration
    diff_seconds = diff_minutes * 60
    diff_words = int(diff_minutes * SPEAKING_RATE_WPM)

    if diff_minutes > 0:
        action = 'add'
        message = f"Add approximately {abs(diff_words)} words ({abs(diff_minutes):.1f} min)"
    elif diff_minutes < 0:
        action = 'remove'
        message = f"Remove approximately {abs(diff_words)} words ({abs(diff_minutes):.1f} min)"
    else:
        action = 'none'
        message = "Duration is at target"

    return {
        'action': action,
        'difference_minutes': round(diff_minutes, 2),
        'difference_seconds': round(diff_seconds, 0),
        'difference_words': diff_words,
        'message': message
    }


if __name__ == "__main__":
    # Test
    test_slides = [
        {'slide_number': 1, 'type': 'title',
         'notes': 'Welcome everyone. [PAUSE] Today we explore Greek theater. This will be an exciting journey. ' * 6},
        {'slide_number': 2, 'type': 'content',
         'notes': 'The origins of theater trace back to ancient Greece. [PAUSE] Religious rituals formed the basis. [EMPHASIS: Dionysus] ' * 8},
        {'slide_number': 3, 'type': 'content',
         'notes': 'The theatron could hold 17000 spectators. [PAUSE] Imagine the scale. [CHECK FOR UNDERSTANDING] ' * 8},
        {'slide_number': 4, 'type': 'summary',
         'notes': 'In summary, Greek theater emerged from religious celebration. [PAUSE] Remember the key terms. ' * 7},
    ]

    print("Duration Estimation Test")
    print("=" * 50)

    result = validate_timing(test_slides)

    print(f"Total duration: {result['duration_minutes']:.2f} minutes")
    print(f"Target range: {result['target_range']}")
    print(f"Valid: {result['valid']}")

    if result['issues']:
        print("\nIssues:")
        for issue in result['issues']:
            print(f"  [{issue['severity']}] {issue['message']}")

    print("\nPer-slide durations:")
    for slide in result['analysis']['per_slide']:
        print(f"  Slide {slide['slide_number']}: {slide['total_seconds']:.0f}s ({slide['total_minutes']:.2f} min) - {slide['status']}")

    print("\nPacing analysis:")
    pacing = get_pacing_analysis(test_slides)
    print(f"  Average: {pacing['average_seconds']:.0f}s per slide")
    print(f"  Consistency: {pacing['consistency']}")
    if pacing['recommendations']:
        print("  Recommendations:")
        for rec in pacing['recommendations']:
            print(f"    - {rec}")
