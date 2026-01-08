"""
Word Count Analyzer Skill
Analyzes word counts for presenter notes and validates against timing requirements.

Theater Pipeline Requirements:
- Total presenter notes: 1,950-2,250 words
- Per-slide targets vary by type
- Speaking rate: 140 WPM

Usage:
    from skills.validation.word_count_analyzer import (
        count_words,
        analyze_word_count,
        validate_word_counts,
        get_per_slide_analysis
    )
"""

import re
from typing import Dict, Any, List, Optional, Tuple


# Constants from config/constraints.yaml
SPEAKING_RATE_WPM = 140

# Total word count requirements
TOTAL_REQUIREMENTS = {
    'minimum': 1950,
    'target': 2100,
    'maximum': 2250
}

# Per-slide word count targets by slide type
SLIDE_TARGETS = {
    'title': {'min': 100, 'target': 125, 'max': 150},
    'intro': {'min': 100, 'target': 125, 'max': 150},
    'section_intro': {'min': 100, 'target': 125, 'max': 150},
    'content': {'min': 160, 'target': 175, 'max': 190},
    'summary': {'min': 150, 'target': 175, 'max': 200},
    'conclusion': {'min': 150, 'target': 175, 'max': 200},
    'auxiliary': {'min': 50, 'target': 75, 'max': 100},
    'agenda': {'min': 50, 'target': 75, 'max': 100},
    'warmup': {'min': 75, 'target': 100, 'max': 125},
    'activity': {'min': 75, 'target': 100, 'max': 125},
    'journal': {'min': 50, 'target': 75, 'max': 100},
}

# Default for unknown slide types
DEFAULT_TARGETS = {'min': 100, 'target': 150, 'max': 200}


def count_words(text: str) -> int:
    """
    Count words in text.

    Args:
        text: Input text

    Returns:
        Word count (integer)
    """
    if not text:
        return 0

    # Remove markers like [PAUSE], [EMPHASIS: term], etc.
    cleaned = re.sub(r'\[[^\]]+\]', '', text)

    # Split on whitespace and count non-empty tokens
    words = [w for w in cleaned.split() if w.strip()]

    return len(words)


def count_words_detailed(text: str) -> Dict[str, Any]:
    """
    Count words with detailed breakdown.

    Returns:
        {
            'total': int,
            'without_markers': int,
            'marker_count': int,
            'sentence_count': int,
            'avg_words_per_sentence': float
        }
    """
    if not text:
        return {
            'total': 0,
            'without_markers': 0,
            'marker_count': 0,
            'sentence_count': 0,
            'avg_words_per_sentence': 0.0
        }

    # Count markers
    markers = re.findall(r'\[[^\]]+\]', text)
    marker_count = len(markers)

    # Remove markers for word count
    cleaned = re.sub(r'\[[^\]]+\]', '', text)
    words = [w for w in cleaned.split() if w.strip()]
    word_count = len(words)

    # Count sentences
    sentences = re.split(r'[.!?]+', cleaned)
    sentences = [s.strip() for s in sentences if s.strip()]
    sentence_count = len(sentences)

    avg_per_sentence = word_count / sentence_count if sentence_count > 0 else 0

    return {
        'total': word_count,
        'without_markers': word_count,
        'marker_count': marker_count,
        'sentence_count': sentence_count,
        'avg_words_per_sentence': round(avg_per_sentence, 1)
    }


def get_slide_targets(slide_type: str) -> Dict[str, int]:
    """
    Get word count targets for a slide type.

    Args:
        slide_type: Type of slide (content, title, auxiliary, etc.)

    Returns:
        Dictionary with min, target, max word counts
    """
    slide_type_lower = slide_type.lower().strip()
    return SLIDE_TARGETS.get(slide_type_lower, DEFAULT_TARGETS)


def analyze_slide_word_count(
    notes: str,
    slide_type: str
) -> Dict[str, Any]:
    """
    Analyze word count for a single slide.

    Args:
        notes: Presenter notes text
        slide_type: Type of slide

    Returns:
        Analysis result with status and recommendations
    """
    word_count = count_words(notes)
    targets = get_slide_targets(slide_type)

    # Determine status
    if word_count < targets['min']:
        status = 'under'
        deviation = targets['min'] - word_count
        recommendation = f"Add {deviation} more words to reach minimum"
    elif word_count > targets['max']:
        status = 'over'
        deviation = word_count - targets['max']
        recommendation = f"Remove {deviation} words to reach maximum"
    else:
        status = 'ok'
        deviation = 0
        recommendation = None

    # Calculate percentage of target
    pct_of_target = (word_count / targets['target']) * 100 if targets['target'] > 0 else 0

    return {
        'word_count': word_count,
        'slide_type': slide_type,
        'targets': targets,
        'status': status,
        'deviation': deviation,
        'pct_of_target': round(pct_of_target, 1),
        'recommendation': recommendation
    }


def get_per_slide_analysis(
    slides: List[Dict[str, Any]]
) -> List[Dict[str, Any]]:
    """
    Analyze word counts for all slides.

    Args:
        slides: List of slide dictionaries with 'notes' and 'type' keys

    Returns:
        List of analysis results per slide
    """
    results = []

    for i, slide in enumerate(slides):
        notes = slide.get('notes', slide.get('presenter_notes', ''))
        slide_type = slide.get('type', slide.get('slide_type', 'content'))
        slide_num = slide.get('slide_number', i + 1)

        analysis = analyze_slide_word_count(notes, slide_type)
        analysis['slide_number'] = slide_num

        results.append(analysis)

    return results


def analyze_word_count(
    presenter_notes: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """
    Comprehensive word count analysis for all presenter notes.

    Args:
        presenter_notes: List of {slide_number, notes, type} dictionaries

    Returns:
        Complete analysis with totals, per-slide, and recommendations
    """
    per_slide = get_per_slide_analysis(presenter_notes)

    # Calculate totals
    total_words = sum(s['word_count'] for s in per_slide)

    # Count statuses
    under_count = sum(1 for s in per_slide if s['status'] == 'under')
    over_count = sum(1 for s in per_slide if s['status'] == 'over')
    ok_count = sum(1 for s in per_slide if s['status'] == 'ok')

    # Overall status
    if total_words < TOTAL_REQUIREMENTS['minimum']:
        overall_status = 'under'
        overall_deviation = TOTAL_REQUIREMENTS['minimum'] - total_words
        overall_recommendation = f"Add {overall_deviation} words total to reach minimum"
    elif total_words > TOTAL_REQUIREMENTS['maximum']:
        overall_status = 'over'
        overall_deviation = total_words - TOTAL_REQUIREMENTS['maximum']
        overall_recommendation = f"Remove {overall_deviation} words total to reach maximum"
    else:
        overall_status = 'ok'
        overall_deviation = 0
        overall_recommendation = None

    # Estimated duration
    estimated_minutes = total_words / SPEAKING_RATE_WPM

    # Find problem slides
    problem_slides = [s for s in per_slide if s['status'] != 'ok']

    return {
        'total_word_count': total_words,
        'requirements': TOTAL_REQUIREMENTS,
        'estimated_duration_minutes': round(estimated_minutes, 1),
        'speaking_rate_wpm': SPEAKING_RATE_WPM,
        'overall_status': overall_status,
        'overall_deviation': overall_deviation,
        'overall_recommendation': overall_recommendation,
        'per_slide_analysis': per_slide,
        'summary': {
            'slides_under': under_count,
            'slides_over': over_count,
            'slides_ok': ok_count,
            'total_slides': len(per_slide)
        },
        'problem_slides': problem_slides
    }


def validate_word_counts(
    presenter_notes: List[Dict[str, Any]],
    strict: bool = False
) -> Dict[str, Any]:
    """
    Validate word counts meet requirements.

    Args:
        presenter_notes: List of slide notes
        strict: If True, all slides must meet targets; if False, only total matters

    Returns:
        Validation result with pass/fail and issues
    """
    analysis = analyze_word_count(presenter_notes)

    issues = []

    # Check total
    total = analysis['total_word_count']
    if total < TOTAL_REQUIREMENTS['minimum']:
        issues.append({
            'type': 'total_under',
            'message': f"Total word count ({total}) below minimum ({TOTAL_REQUIREMENTS['minimum']})",
            'severity': 'error',
            'words_needed': TOTAL_REQUIREMENTS['minimum'] - total
        })
    elif total > TOTAL_REQUIREMENTS['maximum']:
        issues.append({
            'type': 'total_over',
            'message': f"Total word count ({total}) above maximum ({TOTAL_REQUIREMENTS['maximum']})",
            'severity': 'error',
            'words_excess': total - TOTAL_REQUIREMENTS['maximum']
        })

    # Check duration
    duration = analysis['estimated_duration_minutes']
    if duration < 14:
        issues.append({
            'type': 'duration_short',
            'message': f"Estimated duration ({duration} min) below 14 minutes",
            'severity': 'error'
        })
    elif duration > 16:
        issues.append({
            'type': 'duration_long',
            'message': f"Estimated duration ({duration} min) above 16 minutes",
            'severity': 'error'
        })

    # Check per-slide if strict mode
    if strict:
        for slide in analysis['problem_slides']:
            issues.append({
                'type': f"slide_{slide['status']}",
                'slide_number': slide['slide_number'],
                'message': f"Slide {slide['slide_number']} ({slide['slide_type']}): {slide['word_count']} words ({slide['status']})",
                'severity': 'warning',
                'recommendation': slide['recommendation']
            })

    # Determine pass/fail
    error_count = sum(1 for i in issues if i.get('severity') == 'error')

    return {
        'valid': error_count == 0,
        'total_word_count': total,
        'estimated_duration': duration,
        'target_range': f"{TOTAL_REQUIREMENTS['minimum']}-{TOTAL_REQUIREMENTS['maximum']}",
        'issues': issues,
        'error_count': error_count,
        'warning_count': len(issues) - error_count,
        'analysis': analysis
    }


def calculate_words_needed(
    current_total: int,
    target: str = 'minimum'
) -> int:
    """
    Calculate words needed to reach target.

    Args:
        current_total: Current word count
        target: 'minimum', 'target', or 'maximum'

    Returns:
        Words needed (positive) or excess (negative)
    """
    target_value = TOTAL_REQUIREMENTS.get(target, TOTAL_REQUIREMENTS['target'])
    return target_value - current_total


def suggest_distribution(
    total_words_needed: int,
    slide_count: int = 12
) -> Dict[str, Any]:
    """
    Suggest how to distribute additional words across slides.

    Args:
        total_words_needed: Total words to add
        slide_count: Number of content slides

    Returns:
        Distribution suggestion
    """
    if total_words_needed <= 0:
        return {
            'action': 'none',
            'message': 'Word count is sufficient'
        }

    per_slide = total_words_needed // slide_count
    remainder = total_words_needed % slide_count

    return {
        'action': 'add',
        'total_needed': total_words_needed,
        'per_slide_average': per_slide,
        'remainder': remainder,
        'suggestion': f"Add approximately {per_slide} words to each of {slide_count} content slides"
    }


if __name__ == "__main__":
    # Test
    test_slides = [
        {'slide_number': 1, 'type': 'title', 'notes': 'Welcome everyone. Today we explore Greek theater. ' * 8},
        {'slide_number': 2, 'type': 'content', 'notes': 'The origins of theater trace back to ancient Greece. ' * 12},
        {'slide_number': 3, 'type': 'content', 'notes': 'Religious rituals honoring Dionysus formed the basis. ' * 12},
        {'slide_number': 4, 'type': 'summary', 'notes': 'In summary, Greek theater emerged from religious celebration. ' * 10},
    ]

    print("Word Count Analysis Test")
    print("=" * 50)

    result = validate_word_counts(test_slides)

    print(f"Total words: {result['total_word_count']}")
    print(f"Estimated duration: {result['estimated_duration']} min")
    print(f"Valid: {result['valid']}")

    if result['issues']:
        print("\nIssues:")
        for issue in result['issues']:
            print(f"  [{issue['severity']}] {issue['message']}")

    print("\nPer-slide breakdown:")
    for slide in result['analysis']['per_slide_analysis']:
        print(f"  Slide {slide['slide_number']} ({slide['slide_type']}): {slide['word_count']} words - {slide['status']}")
