"""
Warmup Bank Selector Skill
Selects appropriate theater warmups based on unit, lesson content, and activity type.

All warmups are 5 minutes and MUST connect to lesson content.

Usage:
    from skills.generation.warmup_bank_selector import (
        select_warmup,
        get_warmups_by_type,
        get_warmups_for_unit,
        validate_warmup_connection
    )
"""

from typing import Dict, Any, List, Optional
import random


# Warmup types from config/constraints.yaml
WARMUP_TYPES = {
    'physical': ['voice', 'body', 'movement'],
    'mental': ['focus', 'observation', 'concentration'],
    'social': ['partner', 'group', 'ensemble'],
    'creative': ['improvisation', 'imagination'],
    'content': ['skill_practice', 'vocabulary']
}

# Complete warmup bank organized by type and unit suitability
WARMUP_BANK = {
    # =========================================================================
    # PHYSICAL WARMUPS (voice, body, movement)
    # =========================================================================
    'physical': [
        {
            'id': 'PH001',
            'name': 'Tongue Twisters and Projection',
            'type': 'physical',
            'subtype': 'voice',
            'duration_minutes': 5,
            'suitable_units': ['all'],
            'instructions': """Students practice three tongue twisters: 1) 'She sells seashells by the seashore' 2) 'Unique New York' 3) 'Red leather, yellow leather'. Start quietly, then project to the back of the room. Focus on clear articulation at volume.""",
            'phases': {
                'setup': 'Explain the three tongue twisters and demonstrate each one.',
                'demonstration': 'Model quiet version first, then projected version.',
                'execution': 'Students practice individually, then as a group. Increase volume gradually.',
                'wrapup': 'Remind students why articulation matters for performance.',
                'transition': 'Our voices are now warmed up and ready to explore today\'s content.'
            },
            'connection_templates': {
                'greek_theater': 'Greek actors needed to project in massive outdoor theaters without microphones.',
                'commedia_dellarte': 'Commedia performers had to be heard in noisy marketplaces.',
                'shakespeare': 'Shakespeare\'s language demands clear articulation to be understood.',
                'student_directed_one_acts': 'Directors must be able to project when giving notes to actors.',
                'default': 'Clear vocal production is essential for any theater performance.'
            },
            'modifications': {
                'space_limited': 'Students can remain seated; focus on articulation over volume.',
                'large_class': 'Divide into sections; alternate which section is projecting.',
                'energy_level': 'high'
            }
        },
        {
            'id': 'PH002',
            'name': 'Exaggerated Walks',
            'type': 'physical',
            'subtype': 'body',
            'duration_minutes': 5,
            'suitable_units': ['commedia_dellarte', 'greek_theater'],
            'instructions': """Students walk around the room normally. Teacher calls out emotions (happy, sad, angry, tired, excited). Students exaggerate their walk to show that emotion with their whole body—posture, speed, and gestures.""",
            'phases': {
                'setup': 'Clear the space. Students spread out around the room.',
                'demonstration': 'Model an exaggerated "angry" walk to show full body commitment.',
                'execution': 'Call emotions every 20-30 seconds. Encourage bigger choices.',
                'wrapup': 'Freeze on final emotion. Discuss what made some walks more readable.',
                'transition': 'This physical expressiveness is exactly what we\'ll explore today.'
            },
            'connection_templates': {
                'greek_theater': 'Greek actors in masks communicated emotion entirely through body.',
                'commedia_dellarte': 'Commedia characters are defined by their physical characterization.',
                'shakespeare': 'Elizabethan actors used bold physical choices for large audiences.',
                'student_directed_one_acts': 'Directors must understand how actors use their bodies to communicate.',
                'default': 'Physical expression is fundamental to theatrical communication.'
            },
            'modifications': {
                'space_limited': 'Walk in place; focus on upper body and posture changes.',
                'large_class': 'Create traffic patterns; have students walk in a large circle.',
                'energy_level': 'high'
            }
        },
        {
            'id': 'PH003',
            'name': 'Breath and Center',
            'type': 'physical',
            'subtype': 'body',
            'duration_minutes': 5,
            'suitable_units': ['all'],
            'instructions': """Students stand in neutral. Guide them through diaphragmatic breathing: inhale for 4 counts, hold for 4, exhale for 8. Then shake out tension starting from hands, up arms, through shoulders, down the spine.""",
            'phases': {
                'setup': 'Students find their own space, feet hip-width apart.',
                'demonstration': 'Model proper diaphragmatic breathing with hand on belly.',
                'execution': 'Lead 4 cycles of breathing, then progressive shake-out.',
                'wrapup': 'Return to stillness. Notice how the body feels different.',
                'transition': 'With centered bodies and calm minds, let\'s begin today\'s work.'
            },
            'connection_templates': {
                'greek_theater': 'Greek performers needed centered breath for the demands of tragedy.',
                'commedia_dellarte': 'Physical comedy requires a relaxed, responsive body.',
                'shakespeare': 'Breath control is essential for speaking verse.',
                'student_directed_one_acts': 'Directors need calm focus to lead a rehearsal room.',
                'default': 'A centered body and focused mind prepare us for creative work.'
            },
            'modifications': {
                'space_limited': 'Can be done seated; skip shake-out if no room.',
                'large_class': 'Works well with any size; all can participate simultaneously.',
                'energy_level': 'low'
            }
        },
        {
            'id': 'PH004',
            'name': 'Mirror Movement',
            'type': 'physical',
            'subtype': 'movement',
            'duration_minutes': 5,
            'suitable_units': ['all'],
            'instructions': """Partners face each other. One leads slow movements, the other mirrors exactly. Switch leaders halfway. Goal: Move so smoothly an observer can't tell who's leading.""",
            'phases': {
                'setup': 'Find a partner. Decide who leads first. Stand arm\'s length apart.',
                'demonstration': 'Model with a student; show slow, controlled movements.',
                'execution': '2 minutes each leader. Remind: slow and smooth wins.',
                'wrapup': 'Discuss: What made mirroring easier? Harder?',
                'transition': 'This attention to your partner is key to ensemble work.'
            },
            'connection_templates': {
                'greek_theater': 'The Greek chorus moved as one unit, like one body.',
                'commedia_dellarte': 'Commedia partners must be in constant awareness of each other.',
                'shakespeare': 'Scene partners must listen and respond to each other.',
                'student_directed_one_acts': 'Directors must watch actors closely, noting every choice.',
                'default': 'Theater requires deep awareness of others on stage.'
            },
            'modifications': {
                'space_limited': 'Seated mirroring with upper body only.',
                'large_class': 'Some pairs may need to work in hallway or corners.',
                'energy_level': 'medium'
            }
        },
    ],

    # =========================================================================
    # MENTAL WARMUPS (focus, observation, concentration)
    # =========================================================================
    'mental': [
        {
            'id': 'ME001',
            'name': 'Director\'s Eye',
            'type': 'mental',
            'subtype': 'observation',
            'duration_minutes': 5,
            'suitable_units': ['student_directed_one_acts', 'all'],
            'instructions': """Show a 30-second video clip twice. First viewing: watch as an audience member (emotional response). Second viewing: watch as a director (technical observations—blocking, pacing, actor choices). Share observations with partner.""",
            'phases': {
                'setup': 'Explain the two different viewing modes: audience vs. director.',
                'demonstration': 'N/A - clip does the work.',
                'execution': 'Play clip. Pause. Ask for emotional responses. Play again. Discuss technical observations.',
                'wrapup': 'Highlight the shift in perspective between viewer types.',
                'transition': 'This analytical lens is what we\'ll develop today.'
            },
            'connection_templates': {
                'greek_theater': 'Audiences in Athens were sophisticated critics of performance.',
                'commedia_dellarte': 'Watch for physical characterization and comic timing.',
                'shakespeare': 'Notice how actors handle the verse and emotional beats.',
                'student_directed_one_acts': 'A director sees every choice an actor makes.',
                'default': 'Learning to watch theater analytically deepens our work.'
            },
            'modifications': {
                'space_limited': 'Works in any space with projector/screen.',
                'large_class': 'Partner discussions can happen with neighbors.',
                'energy_level': 'low'
            },
            'materials': ['30-second theater clip', 'projector']
        },
        {
            'id': 'ME002',
            'name': 'Zip Zap Zop',
            'type': 'mental',
            'subtype': 'focus',
            'duration_minutes': 5,
            'suitable_units': ['all'],
            'instructions': """Circle game. Person says "Zip" and points to someone. That person says "Zap" and points to another. Third person says "Zop" and points to start new round. Mistakes = funny celebration, then continue.""",
            'phases': {
                'setup': 'Form a circle. Explain the pattern: Zip, Zap, Zop.',
                'demonstration': 'Walk through one slow round with volunteers.',
                'execution': 'Begin slowly, increase speed. Celebrate mistakes with a cheer.',
                'wrapup': 'Reflect: What helped you stay focused? What broke your concentration?',
                'transition': 'That focused energy is what we need for today\'s work.'
            },
            'connection_templates': {
                'greek_theater': 'The chorus required perfect ensemble focus.',
                'commedia_dellarte': 'Improvisers must maintain sharp focus to respond instantly.',
                'shakespeare': 'Actors must stay alert for their cues.',
                'student_directed_one_acts': 'Directors need focused attention throughout rehearsal.',
                'default': 'Focus is the foundation of all theater work.'
            },
            'modifications': {
                'space_limited': 'Can be done seated in a circle or clustered group.',
                'large_class': 'Multiple circles of 10-12 each.',
                'energy_level': 'high'
            }
        },
        {
            'id': 'ME003',
            'name': 'What\'s Different?',
            'type': 'mental',
            'subtype': 'observation',
            'duration_minutes': 5,
            'suitable_units': ['all'],
            'instructions': """Partners face each other. Both observe for 30 seconds. One turns away while the other makes 3 changes (hair, accessories, posture, etc.). First partner turns back and identifies changes.""",
            'phases': {
                'setup': 'Find a partner. Face each other.',
                'demonstration': 'Model with a volunteer.',
                'execution': 'Round 1: Partner A observes, B changes. Round 2: Switch.',
                'wrapup': 'Discuss: What details did you notice? Miss?',
                'transition': 'This attention to detail will help us in today\'s lesson.'
            },
            'connection_templates': {
                'greek_theater': 'Greek audiences noticed every detail of mask and costume.',
                'commedia_dellarte': 'Each stock character has specific visual markers to observe.',
                'shakespeare': 'Directors must notice subtle changes in actor choices.',
                'student_directed_one_acts': 'A good director notices everything.',
                'default': 'Observation skills are essential for theater artists.'
            },
            'modifications': {
                'space_limited': 'Works in any space.',
                'large_class': 'Works fine with any number of pairs.',
                'energy_level': 'medium'
            }
        },
    ],

    # =========================================================================
    # SOCIAL WARMUPS (partner, group, ensemble)
    # =========================================================================
    'social': [
        {
            'id': 'SO001',
            'name': 'The Story Circle',
            'type': 'social',
            'subtype': 'ensemble',
            'duration_minutes': 5,
            'suitable_units': ['greek_theater', 'all'],
            'instructions': """Students stand in a circle. One person starts telling a story with one sentence. Each person adds one sentence, building the story collaboratively. Go around at least twice.""",
            'phases': {
                'setup': 'Form a standing circle. Explain the one-sentence-at-a-time rule.',
                'demonstration': 'Start the story yourself to model sentence length.',
                'execution': 'Go around the circle. Encourage "Yes, and..." thinking.',
                'wrapup': 'Reflect on how the story took unexpected turns.',
                'transition': 'This collaborative storytelling connects to our lesson today.'
            },
            'connection_templates': {
                'greek_theater': 'The Greek chorus told stories collectively, each voice contributing.',
                'commedia_dellarte': 'Commedia troupes built scenarios together through improvisation.',
                'shakespeare': 'Theater is collaborative storytelling between actors.',
                'student_directed_one_acts': 'Directors and actors build the story together.',
                'default': 'Theater is fundamentally collaborative.'
            },
            'modifications': {
                'space_limited': 'Seated circle works fine.',
                'large_class': 'Multiple circles of 8-10 each.',
                'energy_level': 'medium'
            }
        },
        {
            'id': 'SO002',
            'name': 'Group Count',
            'type': 'social',
            'subtype': 'group',
            'duration_minutes': 5,
            'suitable_units': ['all'],
            'instructions': """Group stands in a circle, eyes closed. Goal: count from 1 to 20 as a group. Anyone can say the next number, but if two people speak at once, restart from 1. No patterns or going in order.""",
            'phases': {
                'setup': 'Circle formation. Eyes closed. Explain rules.',
                'demonstration': 'N/A - jump right in.',
                'execution': 'Begin. Celebrate restarts. Try to reach higher each time.',
                'wrapup': 'Discuss: What helped the group succeed?',
                'transition': 'That ensemble awareness is exactly what we need today.'
            },
            'connection_templates': {
                'greek_theater': 'The chorus moved and spoke with unified timing.',
                'commedia_dellarte': 'Improv requires sensing when to speak and when to wait.',
                'shakespeare': 'Actors must feel the rhythm of the scene together.',
                'student_directed_one_acts': 'Rehearsals require everyone to be tuned in.',
                'default': 'Ensemble sensitivity is at the heart of theater.'
            },
            'modifications': {
                'space_limited': 'Eyes closed can be done anywhere.',
                'large_class': 'Larger groups make it harder—that\'s okay! Celebrate progress.',
                'energy_level': 'medium'
            }
        },
        {
            'id': 'SO003',
            'name': 'Yes, And...',
            'type': 'social',
            'subtype': 'partner',
            'duration_minutes': 5,
            'suitable_units': ['commedia_dellarte', 'all'],
            'instructions': """Partners plan an imaginary event using only "Yes, and..." Every statement must accept partner's idea and add to it. Example: "Let's have a pizza party." "Yes, and let's have it on the moon!" """,
            'phases': {
                'setup': 'Find a partner. Explain "Yes, and..." rule.',
                'demonstration': 'Model a short exchange with a volunteer.',
                'execution': 'Partners have 2 minutes. Switch to new partner and new topic.',
                'wrapup': 'Share the wildest ideas that emerged.',
                'transition': 'This acceptance mindset is essential for our work today.'
            },
            'connection_templates': {
                'greek_theater': 'Even Greek tragedy required actors to accept and build on each other.',
                'commedia_dellarte': '"Yes, and" is the foundation of Commedia improvisation.',
                'shakespeare': 'Scene partners must accept each other\'s offers.',
                'student_directed_one_acts': 'Directors must "yes, and" actor ideas to build trust.',
                'default': 'Collaboration requires accepting and building on offers.'
            },
            'modifications': {
                'space_limited': 'Works seated with desk partners.',
                'large_class': 'Works fine—everyone works simultaneously.',
                'energy_level': 'high'
            }
        },
    ],

    # =========================================================================
    # CREATIVE WARMUPS (improvisation, imagination)
    # =========================================================================
    'creative': [
        {
            'id': 'CR001',
            'name': 'Object Transformation',
            'type': 'creative',
            'subtype': 'imagination',
            'duration_minutes': 5,
            'suitable_units': ['all'],
            'instructions': """Pass an ordinary object (water bottle, pencil) around the circle. Each person uses it as something OTHER than what it is—a telescope, a sword, a baby, etc. No repeats.""",
            'phases': {
                'setup': 'Circle formation. Hold up the object.',
                'demonstration': 'Transform it yourself first (e.g., bottle becomes microphone).',
                'execution': 'Pass around. Encourage bold, physical transformations.',
                'wrapup': 'Discuss: What made some transformations more believable?',
                'transition': 'This imaginative transformation is what theater asks of us.'
            },
            'connection_templates': {
                'greek_theater': 'Greek theater used minimal props—imagination filled the gaps.',
                'commedia_dellarte': 'Commedia performers created entire worlds with simple objects.',
                'shakespeare': 'The Elizabethan stage relied on audience imagination.',
                'student_directed_one_acts': 'Directors must imagine how props will be used.',
                'default': 'Theater transforms the ordinary into the extraordinary.'
            },
            'modifications': {
                'space_limited': 'Works seated; pass object across desks.',
                'large_class': 'Multiple objects circulating simultaneously.',
                'energy_level': 'medium'
            },
            'materials': ['Simple object (water bottle, pencil, scarf)']
        },
        {
            'id': 'CR002',
            'name': 'Emotion Landscapes',
            'type': 'creative',
            'subtype': 'imagination',
            'duration_minutes': 5,
            'suitable_units': ['greek_theater', 'shakespeare'],
            'instructions': """Students close eyes. Teacher narrates walking through an emotion-based landscape: "You're walking through anger... the ground is hot... the sky is red..." Students physically respond to the imagery.""",
            'phases': {
                'setup': 'Spread out in the space. Close eyes or soft focus.',
                'demonstration': 'N/A - guided experience.',
                'execution': 'Guide through 2-3 contrasting emotions (joy, fear, grief).',
                'wrapup': 'Open eyes. Notice where you are in space. Discuss responses.',
                'transition': 'This emotional imagination connects to our character work today.'
            },
            'connection_templates': {
                'greek_theater': 'Greek tragedy requires full emotional commitment.',
                'commedia_dellarte': 'Commedia characters embody emotions fully and physically.',
                'shakespeare': 'Shakespeare\'s characters experience extreme emotions.',
                'student_directed_one_acts': 'Directors must help actors access emotional truth.',
                'default': 'Actors must imagine themselves into emotional states.'
            },
            'modifications': {
                'space_limited': 'Seated; focus on facial expressions and breathing.',
                'large_class': 'Works with any size; all participate simultaneously.',
                'energy_level': 'medium'
            }
        },
    ],

    # =========================================================================
    # CONTENT WARMUPS (skill_practice, vocabulary)
    # =========================================================================
    'content': [
        {
            'id': 'CO001',
            'name': 'Vocabulary Embodiment',
            'type': 'content',
            'subtype': 'vocabulary',
            'duration_minutes': 5,
            'suitable_units': ['all'],
            'instructions': """Teacher calls out a vocabulary term from today's lesson. Students create a frozen pose that represents that term. Share poses with partners, then volunteers share with class.""",
            'phases': {
                'setup': 'List 3-4 key vocabulary terms on board.',
                'demonstration': 'Model a pose for one term.',
                'execution': 'Call terms one at a time. 20 seconds per pose.',
                'wrapup': 'Volunteers share; class guesses which term.',
                'transition': 'We\'ll explore these terms in depth today.'
            },
            'connection_templates': {
                'greek_theater': 'Greek theater terms like "theatron" describe physical spaces.',
                'commedia_dellarte': 'Commedia vocabulary is deeply physical—embody it!',
                'shakespeare': 'Shakespeare\'s terms like "soliloquy" have physical implications.',
                'student_directed_one_acts': 'Directing terms like "blocking" are inherently physical.',
                'default': 'Embodying vocabulary helps it stick.'
            },
            'modifications': {
                'space_limited': 'Upper body poses only; stay at desks.',
                'large_class': 'Partner sharing only; skip full-class demonstrations.',
                'energy_level': 'medium'
            }
        },
        {
            'id': 'CO002',
            'name': 'Status Shuffle',
            'type': 'content',
            'subtype': 'skill_practice',
            'duration_minutes': 5,
            'suitable_units': ['commedia_dellarte', 'shakespeare'],
            'instructions': """Students walk around the room. Teacher assigns a number 1-10 representing social status (1=lowest, 10=highest). Students adjust their walk, posture, and eye contact to match their status.""",
            'phases': {
                'setup': 'Explain the status scale. Clear space for walking.',
                'demonstration': 'Model a "1" walk and a "10" walk.',
                'execution': 'Call different numbers. Let students explore each for 45 seconds.',
                'wrapup': 'Discuss: What physical changes did you make? How did you feel at each level?',
                'transition': 'This understanding of status will help us with today\'s characters.'
            },
            'connection_templates': {
                'greek_theater': 'Status was central to Greek society and its theater.',
                'commedia_dellarte': 'Commedia characters have clear, fixed social status.',
                'shakespeare': 'Shakespeare\'s plays are full of status relationships.',
                'student_directed_one_acts': 'Directors must understand character status to stage scenes.',
                'default': 'Status is expressed through body and behavior.'
            },
            'modifications': {
                'space_limited': 'Seated; adjust posture, eye contact, breathing.',
                'large_class': 'Works well; students focus on their own work.',
                'energy_level': 'medium'
            }
        },
    ]
}


def get_warmups_by_type(warmup_type: str) -> List[Dict[str, Any]]:
    """Get all warmups of a specific type."""
    return WARMUP_BANK.get(warmup_type, [])


def get_warmups_for_unit(unit: str) -> List[Dict[str, Any]]:
    """Get all warmups suitable for a specific unit."""
    unit_key = unit.lower().replace(' ', '_').replace('-', '_').replace("'", '')

    # Map unit names to keys
    unit_mapping = {
        'greek': 'greek_theater',
        'greek_theater': 'greek_theater',
        'unit_1': 'greek_theater',
        'commedia': 'commedia_dellarte',
        'commedia_dellarte': 'commedia_dellarte',
        'unit_2': 'commedia_dellarte',
        'shakespeare': 'shakespeare',
        'unit_3': 'shakespeare',
        'one_acts': 'student_directed_one_acts',
        'student_directed': 'student_directed_one_acts',
        'student_directed_one_acts': 'student_directed_one_acts',
        'unit_4': 'student_directed_one_acts',
    }

    unit_key = unit_mapping.get(unit_key, unit_key)

    suitable = []
    for warmup_type, warmups in WARMUP_BANK.items():
        for warmup in warmups:
            units = warmup.get('suitable_units', [])
            if 'all' in units or unit_key in units:
                suitable.append(warmup)

    return suitable


def select_warmup(
    unit: str,
    warmup_type: str = None,
    topic: str = None,
    vocabulary: List[str] = None,
    energy_preference: str = None,
    exclude_ids: List[str] = None
) -> Dict[str, Any]:
    """
    Select the best warmup for given parameters.

    Args:
        unit: Unit name
        warmup_type: Preferred type (physical, mental, social, creative, content)
        topic: Lesson topic for connection matching
        vocabulary: Key vocabulary terms
        energy_preference: low, medium, high
        exclude_ids: IDs of warmups to exclude (already used)

    Returns:
        Selected warmup dictionary with connection filled in
    """
    exclude_ids = exclude_ids or []

    # Get unit-appropriate warmups
    candidates = get_warmups_for_unit(unit)

    # Filter by type if specified
    if warmup_type:
        candidates = [w for w in candidates if w.get('type') == warmup_type]

    # Filter by energy if specified
    if energy_preference:
        candidates = [w for w in candidates
                      if w.get('modifications', {}).get('energy_level') == energy_preference]

    # Exclude already-used warmups
    candidates = [w for w in candidates if w.get('id') not in exclude_ids]

    if not candidates:
        # Fallback to any warmup for the unit
        candidates = get_warmups_for_unit(unit)
        candidates = [w for w in candidates if w.get('id') not in exclude_ids]

    if not candidates:
        # Last resort: return first physical warmup
        candidates = WARMUP_BANK.get('physical', [])

    # Select randomly from candidates (could be made smarter)
    selected = random.choice(candidates)

    # Fill in the connection for this specific unit
    unit_key = unit.lower().replace(' ', '_').replace('-', '_').replace("'", '')
    unit_mapping = {
        'greek': 'greek_theater',
        'greek_theater': 'greek_theater',
        'commedia': 'commedia_dellarte',
        'commedia_dellarte': 'commedia_dellarte',
        'shakespeare': 'shakespeare',
        'one_acts': 'student_directed_one_acts',
        'student_directed_one_acts': 'student_directed_one_acts',
    }
    unit_key = unit_mapping.get(unit_key, 'default')

    connection_templates = selected.get('connection_templates', {})
    connection = connection_templates.get(unit_key, connection_templates.get('default', ''))

    # Create output with connection filled in
    result = dict(selected)
    result['connection_to_lesson'] = connection

    return result


def validate_warmup_connection(warmup: Dict[str, Any], lesson_topic: str) -> Dict[str, Any]:
    """
    Validate that a warmup has a proper connection to lesson content.

    Returns:
        {
            'valid': bool,
            'has_connection': bool,
            'connection_text': str,
            'issues': list
        }
    """
    issues = []

    connection = warmup.get('connection_to_lesson', '')
    if not connection or not connection.strip():
        issues.append("Warmup missing connection to lesson content")

    if connection and len(connection) < 20:
        issues.append("Connection to lesson is too brief")

    return {
        'valid': len(issues) == 0,
        'has_connection': bool(connection and connection.strip()),
        'connection_text': connection,
        'issues': issues
    }


def format_warmup_for_output(warmup: Dict[str, Any]) -> Dict[str, Any]:
    """Format warmup for pipeline output schema."""
    return {
        'name': warmup.get('name', ''),
        'type': warmup.get('type', ''),
        'subtype': warmup.get('subtype', ''),
        'duration_minutes': warmup.get('duration_minutes', 5),
        'instructions': warmup.get('instructions', ''),
        'connection_to_lesson': warmup.get('connection_to_lesson', ''),
        'phases': warmup.get('phases', {}),
        'modifications': warmup.get('modifications', {}),
        'materials': warmup.get('materials', [])
    }


if __name__ == "__main__":
    # Test warmup selection
    print("Testing warmup selection...\n")

    for unit in ['greek_theater', 'commedia_dellarte', 'shakespeare', 'student_directed_one_acts']:
        warmup = select_warmup(unit=unit)
        print(f"Unit: {unit}")
        print(f"  Selected: {warmup['name']}")
        print(f"  Type: {warmup['type']}")
        print(f"  Connection: {warmup['connection_to_lesson'][:80]}...")
        print()

    # Test type filtering
    print("Physical warmups only:")
    warmup = select_warmup(unit='shakespeare', warmup_type='physical')
    print(f"  {warmup['name']}")

    # Test validation
    print("\nValidation test:")
    result = validate_warmup_connection(warmup, "Introduction to Shakespeare")
    print(f"  Valid: {result['valid']}")
    print(f"  Connection: {result['connection_text'][:60]}...")
