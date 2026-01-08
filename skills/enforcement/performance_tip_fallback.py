"""
Performance Tip Fallback Skill
Ensures every content slide has a Performance Tip.
Uses unit-specific fallback tips when generation fails.

Usage:
    from skills.enforcement.performance_tip_fallback import ensure_performance_tip
    slide = ensure_performance_tip(slide, unit='greek_theater')
"""

from typing import Dict, Any, Optional


# Unit-specific fallback performance tips for theater education
FALLBACK_TIPS = {
    'greek_theater': {
        'tips': [
            'Project your voice as if reaching the back row of an amphitheater.',
            'The chorus moves as one - practice synchronization with your ensemble.',
            'Masks require larger gestures; let your body tell the story.',
            'Greek tragedy demands emotional truth - find your character\'s fatal flaw.',
            'Remember: the audience is part of the ritual, not passive observers.',
        ],
        'index': 0
    },
    'commedia_dellarte': {
        'tips': [
            'Each stock character has a signature posture - find yours and commit.',
            'Lazzi are physical comedy gold - practice timing until it feels natural.',
            'Status is everything in Commedia - know where your character stands.',
            'Improvisation requires listening - react to your scene partners.',
            'The mask leads the body - let it inform your movement choices.',
        ],
        'index': 0
    },
    'shakespeare': {
        'tips': [
            'Iambic pentameter is your friend - let the rhythm guide your delivery.',
            'Antithesis reveals character - find the opposites in your lines.',
            'Shakespeare wrote for speaking, not reading - trust the language.',
            'Soliloquies are conversations with the audience - include them.',
            'The verse tells you when to breathe - don\'t fight the punctuation.',
        ],
        'index': 0
    },
    'student_directed_one_acts': {
        'tips': [
            'Directors: your vision must be clear before you can communicate it.',
            'Give actors playable directions - verbs, not adjectives.',
            'Blocking should serve the story, not just fill the space.',
            'The best note is specific, actionable, and kind.',
            'Trust your actors - collaboration creates better theater.',
        ],
        'index': 0
    },
    'default': {
        'tips': [
            'Theater is live - embrace the energy of the moment.',
            'Every choice on stage should serve the story.',
            'Acting is reacting - stay present with your scene partners.',
            'Rehearsal is for experimenting; performance is for committing.',
            'The audience completes the theatrical experience.',
        ],
        'index': 0
    }
}


def get_fallback_tip(unit: str) -> str:
    """
    Get next fallback tip for unit (rotates through available tips).

    Args:
        unit: Theater unit (greek_theater, commedia_dellarte, shakespeare, student_directed_one_acts)

    Returns:
        Fallback tip string
    """
    unit_lower = unit.lower().replace(' ', '_').replace('-', '_')

    # Handle variations of unit names
    unit_mapping = {
        'greek': 'greek_theater',
        'greek_theater': 'greek_theater',
        'unit_1': 'greek_theater',
        'unit1': 'greek_theater',
        'commedia': 'commedia_dellarte',
        'commedia_dellarte': 'commedia_dellarte',
        'commedia_dell_arte': 'commedia_dellarte',
        'unit_2': 'commedia_dellarte',
        'unit2': 'commedia_dellarte',
        'shakespeare': 'shakespeare',
        'unit_3': 'shakespeare',
        'unit3': 'shakespeare',
        'one_acts': 'student_directed_one_acts',
        'student_directed': 'student_directed_one_acts',
        'student_directed_one_acts': 'student_directed_one_acts',
        'unit_4': 'student_directed_one_acts',
        'unit4': 'student_directed_one_acts',
    }

    unit_key = unit_mapping.get(unit_lower, 'default')

    if unit_key not in FALLBACK_TIPS:
        unit_key = 'default'

    tips_data = FALLBACK_TIPS[unit_key]
    tip = tips_data['tips'][tips_data['index']]

    # Rotate to next tip for variety
    tips_data['index'] = (tips_data['index'] + 1) % len(tips_data['tips'])

    return tip


def ensure_performance_tip(slide: Dict[str, Any], unit: str) -> Dict[str, Any]:
    """
    Ensure slide has Performance Tip. Add fallback if missing.

    Args:
        slide: Slide dictionary
        unit: Theater unit for fallback selection

    Returns:
        Slide with guaranteed performance tip (for content slides)
    """
    # Only content slides require tips
    slide_type = slide.get('type', slide.get('slide_type', '')).lower()
    if slide_type != 'content':
        return slide

    # Check if tip exists and is non-empty
    tip = slide.get('performance_tip', '')
    if tip and tip.strip() and tip.lower() not in ['[none]', 'none', '']:
        return slide

    # Add fallback tip
    slide['performance_tip'] = get_fallback_tip(unit)
    slide['performance_tip_source'] = 'fallback'

    return slide


def ensure_all_tips(slides: list, unit: str) -> list:
    """
    Ensure all content slides have performance tips.

    Args:
        slides: List of slide dictionaries
        unit: Theater unit

    Returns:
        Slides with guaranteed tips on content slides
    """
    return [ensure_performance_tip(slide, unit) for slide in slides]


def validate_performance_tips(slides: list) -> Dict[str, Any]:
    """
    Validate all content slides have performance tips.

    Returns:
        Validation result with issues list
    """
    issues = []
    for slide in slides:
        slide_type = slide.get('type', slide.get('slide_type', '')).lower()
        if slide_type == 'content':
            tip = slide.get('performance_tip', '')
            if not tip or not tip.strip():
                issues.append({
                    'slide_number': slide.get('slide_number'),
                    'issue': 'Content slide missing performance tip'
                })

    return {
        'valid': len(issues) == 0,
        'issues': issues,
        'content_slides_checked': sum(1 for s in slides
            if s.get('type', s.get('slide_type', '')).lower() == 'content')
    }


# Backward compatibility aliases (for transition period)
ensure_nclex_tip = ensure_performance_tip
validate_nclex_tips = validate_performance_tips


if __name__ == "__main__":
    # Test
    test_slides = [
        {'slide_number': 1, 'type': 'section_intro'},
        {'slide_number': 2, 'type': 'content', 'performance_tip': ''},  # Missing!
        {'slide_number': 3, 'type': 'content', 'performance_tip': 'Good tip'},
        {'slide_number': 4, 'type': 'activity'},
    ]

    print("Before validation:", validate_performance_tips(test_slides))
    fixed = ensure_all_tips(test_slides, unit='greek_theater')
    print("After fix:", validate_performance_tips(fixed))
    print("Added tip:", fixed[1]['performance_tip'])
    print("Tip source:", fixed[1].get('performance_tip_source'))

    # Test all units
    print("\n--- Testing all units ---")
    for unit in ['greek_theater', 'commedia_dellarte', 'shakespeare', 'student_directed_one_acts']:
        print(f"{unit}: {get_fallback_tip(unit)}")
