"""
Activity Type Selector Skill
Selects appropriate 15-minute activities based on unit, lesson content, and learning objectives.

Activity Structure: 1.5 min setup, 11 min work, 2.5 min sharing

Usage:
    from skills.generation.activity_type_selector import (
        select_activity,
        get_activities_by_type,
        get_activities_for_unit,
        validate_activity_structure
    )
"""

from typing import Dict, Any, List, Optional
import random


# Activity types from config/constraints.yaml
ACTIVITY_TYPES = [
    'writing',
    'discussion',
    'performance',
    'annotation',
    'creative',
    'physical',
    'collaborative'
]

# Activity timing structure
ACTIVITY_STRUCTURE = {
    'setup_minutes': 1.5,
    'work_minutes': 11,
    'sharing_minutes': 2.5,
    'total_minutes': 15
}

# Time warnings
TIME_WARNINGS = [
    {'at_minute': 10, 'message': 'Five minutes remaining. Start wrapping up your work.'},
    {'at_minute': 13, 'message': 'Two minutes remaining. Prepare to share.'}
]

# Complete activity bank
ACTIVITY_BANK = {
    # =========================================================================
    # WRITING ACTIVITIES
    # =========================================================================
    'writing': [
        {
            'id': 'WR001',
            'name': 'Directorial Vision Statement Draft',
            'type': 'writing',
            'duration_minutes': 15,
            'suitable_units': ['student_directed_one_acts'],
            'description': 'Students draft their personal directorial vision for their one-act project.',
            'instructions': """Using the provided one-act script options:
1) Select one script that interests you (2 min)
2) Read the one-page synopsis provided (2 min)
3) Answer three guiding questions in your journal:
   - What themes resonate with you?
   - What visual or staging ideas come to mind?
   - What would you want the audience to feel leaving the theater?
4) Write a 3-5 sentence Directorial Vision Statement draft (5 min)
5) Share your vision with a partner and give feedback (2 min)""",
            'materials_needed': [
                'One-act script options handout',
                'Directorial Vision Statement template',
                'Student journals'
            ],
            'grouping': 'individual',
            'learning_objective_connection': 'Begin developing a personal directorial vision statement',
            'differentiation': {
                'ell': "Provide sentence frames: 'I want to direct [title] because... My vision focuses on... I want the audience to...'",
                'advanced': 'Additional prompt: How might your concept differ from a "traditional" interpretation?',
                'struggling': 'One-on-one conference to talk through ideas verbally before writing.'
            },
            'success_criteria': [
                'Vision statement is 3-5 sentences',
                'Statement addresses themes, staging, and audience impact',
                'Statement shows personal perspective'
            ],
            'requires_handout': True
        },
        {
            'id': 'WR002',
            'name': 'Character Analysis Journal',
            'type': 'writing',
            'duration_minutes': 15,
            'suitable_units': ['shakespeare', 'commedia_dellarte', 'greek_theater'],
            'description': 'Students analyze a character through guided journal prompts.',
            'instructions': """Focus on the character we discussed today:
1) Write the character's name at the top of your page (1 min)
2) Answer these questions in complete sentences:
   - What does this character want most? (objective)
   - What stands in their way? (obstacle)
   - What tactics do they use to get what they want?
   - What moment shows us who they really are?
3) Write a 2-3 sentence "character essence" statement (3 min)
4) Share with a partner—do they see the character the same way? (2 min)""",
            'materials_needed': [
                'Student journals',
                'Character analysis guiding questions handout'
            ],
            'grouping': 'individual',
            'learning_objective_connection': 'Analyze character motivation and development',
            'differentiation': {
                'ell': 'Provide vocabulary list for theatrical terms; allow bullet points instead of sentences.',
                'advanced': 'Add: How does this character connect to characters in other plays you know?',
                'struggling': 'Provide sentence starters for each question.'
            },
            'success_criteria': [
                'All four questions answered',
                'Character essence statement is clear and specific',
                'Analysis goes beyond surface observations'
            ],
            'requires_handout': True
        },
        {
            'id': 'WR003',
            'name': 'Blocking Notation Practice',
            'type': 'writing',
            'duration_minutes': 15,
            'suitable_units': ['student_directed_one_acts'],
            'description': 'Students learn and practice standard blocking notation.',
            'instructions': """Using the blocking key provided:
1) Review the standard abbreviations (CS, US, DS, SL, SR, X) (2 min)
2) Watch the short scene clip and note the blocking you observe (3 min)
3) Transcribe the blocking using standard notation (5 min)
4) Compare your notation with a partner—did you catch the same moves? (3 min)
5) Discuss: What was hardest to notate? (2 min)""",
            'materials_needed': [
                'Blocking notation key handout',
                'Blank blocking grid',
                'Short scene clip (1-2 min)',
                'Projector'
            ],
            'grouping': 'individual then pairs',
            'learning_objective_connection': 'Learn standard blocking notation used by directors',
            'differentiation': {
                'ell': 'Provide completed example; allow partner work throughout.',
                'advanced': 'Add motivation notes—WHY does the character move?',
                'struggling': 'Pause video frequently; provide partially completed notation.'
            },
            'success_criteria': [
                'Correct use of abbreviations',
                'Major movements captured',
                'Notation is readable to others'
            ],
            'requires_handout': True
        }
    ],

    # =========================================================================
    # DISCUSSION ACTIVITIES
    # =========================================================================
    'discussion': [
        {
            'id': 'DI001',
            'name': 'Socratic Seminar: The Role of Fate',
            'type': 'discussion',
            'duration_minutes': 15,
            'suitable_units': ['greek_theater', 'shakespeare'],
            'description': 'Structured discussion on the role of fate vs. free will in theater.',
            'instructions': """Socratic Seminar Protocol:
1) Review discussion norms: listen, respond to ideas not people, use evidence (1 min)
2) Opening question (posed by teacher): "To what extent are the characters in control of their fate?"
3) Inner circle discusses (6 min), outer circle observes and takes notes
4) Switch circles (6 min)
5) Whole class: What was the strongest argument you heard? (2 min)""",
            'materials_needed': [
                'Discussion norms poster',
                'Note-taking sheet for observers',
                'Text excerpts for evidence'
            ],
            'grouping': 'inner/outer circle',
            'learning_objective_connection': 'Analyze thematic elements through collaborative discussion',
            'differentiation': {
                'ell': 'Provide sentence starters; allow preparation time with partner.',
                'advanced': 'Lead with follow-up questions; serve as discussion facilitator.',
                'struggling': 'Start in outer circle; provide key quotes to reference.'
            },
            'success_criteria': [
                'All students contribute at least once',
                'Evidence from text is cited',
                'Students respond to each other, not just teacher'
            ],
            'requires_handout': True
        },
        {
            'id': 'DI002',
            'name': 'Think-Pair-Share: Performance Choices',
            'type': 'discussion',
            'duration_minutes': 15,
            'suitable_units': ['all'],
            'description': 'Structured discussion analyzing performance choices in a clip.',
            'instructions': """After watching the scene clip:
1) THINK: Write 3 observations about the actor's choices (3 min)
   - Voice, body, staging, relationships
2) PAIR: Share observations with a partner. What did they notice that you missed? (4 min)
3) SHARE: Each pair contributes one insight to class discussion (5 min)
4) Synthesis: What makes these choices effective or ineffective? (3 min)""",
            'materials_needed': [
                'Scene clip (2-3 min)',
                'Observation worksheet',
                'Projector'
            ],
            'grouping': 'individual → pairs → whole class',
            'learning_objective_connection': 'Analyze how performance choices communicate meaning',
            'differentiation': {
                'ell': 'Provide observation categories; allow partner support throughout.',
                'advanced': 'Compare to another production of the same scene.',
                'struggling': 'Focus on one category (voice OR body); provide sentence frames.'
            },
            'success_criteria': [
                'Observations are specific and detailed',
                'Partner discussion adds new insights',
                'Class discussion connects to learning objectives'
            ],
            'requires_handout': True
        }
    ],

    # =========================================================================
    # PERFORMANCE ACTIVITIES
    # =========================================================================
    'performance': [
        {
            'id': 'PE001',
            'name': 'Tableau Vivant',
            'type': 'performance',
            'duration_minutes': 15,
            'suitable_units': ['greek_theater', 'shakespeare', 'commedia_dellarte'],
            'description': 'Groups create frozen images representing key moments.',
            'instructions': """In groups of 4-5:
1) Receive your assigned moment from today's text (1 min)
2) Discuss: What's the most important element to show? (2 min)
3) Create your tableau—frozen image showing the moment (4 min)
   - Consider: levels, focus, spatial relationships, facial expressions
4) Present to class. Audience guesses the moment and analyzes choices (6 min)
5) Debrief: What made tableaux effective? (2 min)""",
            'materials_needed': [
                'Moment cards (one per group)',
                'Open performance space'
            ],
            'grouping': 'groups of 4-5',
            'learning_objective_connection': 'Communicate narrative through visual storytelling',
            'differentiation': {
                'ell': 'Pair with supportive group; focus on physical, not verbal.',
                'advanced': 'Add "before" and "after" tableaux for context.',
                'struggling': 'Provide image examples; allow more planning time.'
            },
            'success_criteria': [
                'Moment is recognizable to audience',
                'All group members are engaged',
                'Staging shows understanding of relationships'
            ],
            'requires_handout': False
        },
        {
            'id': 'PE002',
            'name': 'Status Improvisation',
            'type': 'performance',
            'duration_minutes': 15,
            'suitable_units': ['commedia_dellarte', 'shakespeare'],
            'description': 'Partners improvise scenes exploring status relationships.',
            'instructions': """In pairs:
1) Each partner secretly draws a number 1-10 (status level) (1 min)
2) Given scenario: "You're waiting for the bus"
3) Improvise the scene for 2 minutes, playing your status
4) Audience guesses each person's number (2 min)
5) New partners, new scenario: "You're at a job interview" (5 min)
6) Debrief: How did you show status physically? Vocally? (3 min)""",
            'materials_needed': [
                'Number cards 1-10 (multiple sets)',
                'Scenario cards',
                'Open performance space'
            ],
            'grouping': 'pairs, rotating',
            'learning_objective_connection': 'Explore how status is communicated through performance',
            'differentiation': {
                'ell': 'Minimal dialogue required—focus on physical status.',
                'advanced': 'Switch status mid-scene; make the shift visible.',
                'struggling': 'Limit to extreme status (1 or 10 only).'
            },
            'success_criteria': [
                'Status is readable to audience',
                'Status is consistent throughout scene',
                'Physical and vocal choices support status'
            ],
            'requires_handout': False
        },
        {
            'id': 'PE003',
            'name': 'Choral Speaking',
            'type': 'performance',
            'duration_minutes': 15,
            'suitable_units': ['greek_theater'],
            'description': 'Groups perform choral text with unified movement and voice.',
            'instructions': """In groups of 6-8:
1) Receive your assigned choral passage (1 min)
2) Read through together—find the rhythm (2 min)
3) Add movement that supports the text's meaning (4 min)
   - Consider: unison, echo, call-response, levels
4) Rehearse and refine (3 min)
5) Perform for class (3 min)
6) Feedback: What created the strongest moments of unity? (2 min)""",
            'materials_needed': [
                'Choral text excerpts (one per group)',
                'Open performance space'
            ],
            'grouping': 'groups of 6-8',
            'learning_objective_connection': 'Experience the power of the Greek chorus through performance',
            'differentiation': {
                'ell': 'Shorter text; allow some unison with gesture only.',
                'advanced': 'Add contrasting solo voices within the chorus.',
                'struggling': 'Focus on movement; minimize text complexity.'
            },
            'success_criteria': [
                'Voices are unified in rhythm and volume',
                'Movement supports textual meaning',
                'Group functions as one unit'
            ],
            'requires_handout': True
        }
    ],

    # =========================================================================
    # ANNOTATION ACTIVITIES
    # =========================================================================
    'annotation': [
        {
            'id': 'AN001',
            'name': 'Script Markup',
            'type': 'annotation',
            'duration_minutes': 15,
            'suitable_units': ['shakespeare', 'student_directed_one_acts'],
            'description': 'Students annotate a script page with performance notes.',
            'instructions': """Using the annotation key provided:
1) Read through your assigned page silently (2 min)
2) Mark the following using the color code:
   - Blue: beats/shifts in intention
   - Green: key words to emphasize
   - Red: tactical shifts (what the character tries)
   - Pencil: questions for discussion (6 min)
3) Compare annotations with a partner—discuss differences (4 min)
4) Class share: What were the most debated moments? (3 min)""",
            'materials_needed': [
                'Script pages (one per student)',
                'Annotation key handout',
                'Colored pencils (blue, green, red)',
                'Regular pencils'
            ],
            'grouping': 'individual → pairs',
            'learning_objective_connection': 'Analyze script for performance choices',
            'differentiation': {
                'ell': 'Pre-highlight key passages; provide glossary.',
                'advanced': 'Add notations for subtext—what character is NOT saying.',
                'struggling': 'Focus on one color only (beats); model examples.'
            },
            'success_criteria': [
                'All annotation categories addressed',
                'Annotations show thoughtful analysis',
                'Partner discussion reveals different interpretations'
            ],
            'requires_handout': True
        },
        {
            'id': 'AN002',
            'name': 'Visual Analysis Gallery Walk',
            'type': 'annotation',
            'duration_minutes': 15,
            'suitable_units': ['greek_theater', 'commedia_dellarte'],
            'description': 'Students annotate and analyze production images.',
            'instructions': """6 images are posted around the room:
1) Rotate in pairs, spending 2 min at each station (12 min total)
2) At each station, write on the posted chart paper:
   - What do you notice? (describe)
   - What does this tell you? (analyze)
   - What questions do you have?
3) Return to seats. Discuss: What patterns emerged across images? (3 min)""",
            'materials_needed': [
                '6 production images (posted)',
                'Chart paper (one per image)',
                'Markers',
                'Observation worksheet'
            ],
            'grouping': 'pairs',
            'learning_objective_connection': 'Analyze visual elements of theatrical production',
            'differentiation': {
                'ell': 'Provide sentence frames for observations.',
                'advanced': 'Compare to modern productions - what is similar/different?',
                'struggling': 'Reduce to 4 stations; provide guiding questions.'
            },
            'success_criteria': [
                'Written observations at each station',
                'Analysis goes beyond surface description',
                'Participation in final discussion'
            ],
            'requires_handout': True
        }
    ],

    # =========================================================================
    # CREATIVE ACTIVITIES
    # =========================================================================
    'creative': [
        {
            'id': 'CR001',
            'name': 'Theater Origins Mind Map',
            'type': 'creative',
            'duration_minutes': 15,
            'suitable_units': ['greek_theater'],
            'description': 'Groups create visual mind maps connecting concepts.',
            'instructions': """In groups of 4:
1) Get your poster paper and markers (1 min)
2) Create a mind map showing:
   - Center: Today's main topic
   - Branch 1: What you knew before today
   - Branch 2: What you learned today
   - Branch 3: Connections to theater today
3) Use color, images, and keywords (10 min)
4) Gallery walk: view other groups' maps (2 min)
5) One insight from another group's map (2 min)""",
            'materials_needed': [
                'Poster paper (one per group)',
                'Markers (multiple colors)',
                'Tape for posting'
            ],
            'grouping': 'groups of 4',
            'learning_objective_connection': 'Synthesize learning and make connections',
            'differentiation': {
                'ell': 'Provide word bank; encourage visual over text.',
                'advanced': 'Add fourth branch: Questions that remain.',
                'struggling': 'Provide partially completed template.'
            },
            'success_criteria': [
                'All three branches addressed',
                'Connections between ideas shown',
                'All group members contributed'
            ],
            'requires_handout': False
        },
        {
            'id': 'CR002',
            'name': 'Stock Character Design',
            'type': 'creative',
            'duration_minutes': 15,
            'suitable_units': ['commedia_dellarte'],
            'description': 'Students design a modern stock character.',
            'instructions': """Create a modern stock character:
1) Review the characteristics of traditional stock characters (2 min)
2) Brainstorm modern "types" in your world (student, influencer, etc.) (2 min)
3) Choose one and design:
   - Name and social status
   - Signature posture and walk
   - Voice quality and catchphrase
   - What they want (objective)
   - What makes them funny or tragic (5 min)
4) Present your character in 30 seconds—in character! (4 min)
5) Discuss: What makes a stock character work? (2 min)""",
            'materials_needed': [
                'Character design worksheet',
                'Examples of traditional stock characters',
                'Open performance space'
            ],
            'grouping': 'individual',
            'learning_objective_connection': 'Apply understanding of stock characters to original creation',
            'differentiation': {
                'ell': 'Allow partner collaboration; focus on physical over verbal.',
                'advanced': 'Create a relationship between two stock characters.',
                'struggling': 'Provide character template with prompts.'
            },
            'success_criteria': [
                'Character is clearly defined',
                'Physical characteristics are distinctive',
                'Character connects to Commedia principles'
            ],
            'requires_handout': True
        }
    ],

    # =========================================================================
    # PHYSICAL ACTIVITIES
    # =========================================================================
    'physical': [
        {
            'id': 'PH001',
            'name': 'Mask Exploration',
            'type': 'physical',
            'duration_minutes': 15,
            'suitable_units': ['greek_theater', 'commedia_dellarte'],
            'description': 'Students explore character through mask work.',
            'instructions': """Working with neutral or character masks:
1) Receive your mask. DO NOT put it on yet. (1 min)
2) Study the mask: What does it suggest? What does it want? (2 min)
3) Put on the mask. Let it change your body. (2 min)
4) Move around the space as the mask. No speaking. (3 min)
5) Find a partner (still in mask). Relate silently. (3 min)
6) Remove mask. Debrief: How did the mask change you? (4 min)""",
            'materials_needed': [
                'Neutral or character masks (one per student)',
                'Mirror (optional)',
                'Open performance space'
            ],
            'grouping': 'individual → pairs',
            'learning_objective_connection': 'Experience how masks transform the performer',
            'differentiation': {
                'ell': 'Non-verbal activity works well; follow-up discussion can be in L1.',
                'advanced': 'Try multiple masks; compare how each transforms you.',
                'struggling': 'Spend more time in observation phase; partner throughout.'
            },
            'success_criteria': [
                'Physical transformation is visible',
                'Commitment to mask\'s qualities',
                'Reflection shows understanding'
            ],
            'requires_handout': False
        },
        {
            'id': 'PH002',
            'name': 'Lazzi Creation',
            'type': 'physical',
            'duration_minutes': 15,
            'suitable_units': ['commedia_dellarte'],
            'description': 'Groups create and perform original lazzi.',
            'instructions': """In groups of 3:
1) Review examples of traditional lazzi (1 min)
2) Choose a simple scenario: character tries to [action] but fails (1 min)
3) Create a 30-second physical comedy routine (7 min)
   - Must be repeatable
   - Must build in three stages
   - Must have a clear ending
4) Perform for class (4 min)
5) Discuss: What made the funniest moments work? (2 min)""",
            'materials_needed': [
                'Lazzi examples handout',
                'Simple props (scarves, hats)',
                'Open performance space'
            ],
            'grouping': 'groups of 3',
            'learning_objective_connection': 'Create original physical comedy using Commedia techniques',
            'differentiation': {
                'ell': 'Physical activity requires minimal language.',
                'advanced': 'Add status reversals within the lazzi.',
                'struggling': 'Provide scenario; focus on physical execution.'
            },
            'success_criteria': [
                'Clear three-part structure',
                'Physical comedy is readable',
                'All group members participate'
            ],
            'requires_handout': True
        }
    ],

    # =========================================================================
    # COLLABORATIVE ACTIVITIES
    # =========================================================================
    'collaborative': [
        {
            'id': 'CO001',
            'name': 'Myth vs. Reality Sorting',
            'type': 'collaborative',
            'duration_minutes': 15,
            'suitable_units': ['shakespeare', 'greek_theater'],
            'description': 'Groups sort facts from myths about the topic.',
            'instructions': """In groups of 3-4:
1) Open your envelope—you have 10 statements (1 min)
2) Sort them into FACT and MYTH piles (5 min)
3) For each, write a brief justification for your choice (4 min)
4) Teacher reveals answers—track your accuracy (2 min)
5) Discuss: What surprised you? Why do myths persist? (3 min)""",
            'materials_needed': [
                'Envelopes with statement cards (one set per group)',
                'Sorting mat (FACT/MYTH)',
                'Answer key for teacher'
            ],
            'grouping': 'groups of 3-4',
            'learning_objective_connection': 'Distinguish historical fact from popular misconception',
            'differentiation': {
                'ell': 'Provide glossary; allow discussion in L1.',
                'advanced': 'Create one new myth and one new fact to share.',
                'struggling': 'Reduce to 6 statements; provide hint sheet.'
            },
            'success_criteria': [
                'All statements sorted',
                'Justifications provided',
                'Group collaboration evident'
            ],
            'requires_handout': True
        },
        {
            'id': 'CO002',
            'name': 'Production Concept Pitch',
            'type': 'collaborative',
            'duration_minutes': 15,
            'suitable_units': ['shakespeare', 'student_directed_one_acts'],
            'description': 'Groups develop and pitch a production concept.',
            'instructions': """Your group is pitching a production concept to a theater company:
1) Assign roles: Director, Designer, Marketing (1 min)
2) Develop your concept for assigned play:
   - Setting (when/where)
   - Visual style (colors, textures)
   - Big idea (what's this production ABOUT?)
   - Target audience (4 min)
3) Prepare 1-minute pitch—everyone speaks (4 min)
4) Deliver pitches to class (4 min)
5) Class votes on most compelling concept (2 min)""",
            'materials_needed': [
                'Play assignment cards',
                'Concept planning worksheet',
                'Timer for pitches'
            ],
            'grouping': 'groups of 3',
            'learning_objective_connection': 'Apply directorial concept thinking to production planning',
            'differentiation': {
                'ell': 'Visual presentation option; allow partner support.',
                'advanced': 'Include budget considerations and casting ideas.',
                'struggling': 'Provide concept templates; focus on one element.'
            },
            'success_criteria': [
                'Concept is clear and unified',
                'All elements support the big idea',
                'All group members contribute to pitch'
            ],
            'requires_handout': True
        }
    ]
}


def get_activities_by_type(activity_type: str) -> List[Dict[str, Any]]:
    """Get all activities of a specific type."""
    return ACTIVITY_BANK.get(activity_type, [])


def get_activities_for_unit(unit: str) -> List[Dict[str, Any]]:
    """Get all activities suitable for a specific unit."""
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
    unit_key = unit_mapping.get(unit_key, unit_key)

    suitable = []
    for activity_type, activities in ACTIVITY_BANK.items():
        for activity in activities:
            units = activity.get('suitable_units', [])
            if 'all' in units or unit_key in units:
                suitable.append(activity)

    return suitable


def select_activity(
    unit: str,
    activity_type: str = None,
    learning_objectives: List[str] = None,
    exclude_ids: List[str] = None,
    requires_performance: bool = None
) -> Dict[str, Any]:
    """
    Select the best activity for given parameters.

    Args:
        unit: Unit name
        activity_type: Preferred type
        learning_objectives: Learning objectives to connect to
        exclude_ids: IDs of activities to exclude
        requires_performance: If True, prioritize performance activities

    Returns:
        Selected activity dictionary
    """
    exclude_ids = exclude_ids or []

    # Get unit-appropriate activities
    candidates = get_activities_for_unit(unit)

    # Filter by type if specified
    if activity_type:
        candidates = [a for a in candidates if a.get('type') == activity_type]

    # Filter for performance if required
    if requires_performance:
        perf_types = ['performance', 'physical']
        candidates = [a for a in candidates if a.get('type') in perf_types]

    # Exclude already-used activities
    candidates = [a for a in candidates if a.get('id') not in exclude_ids]

    if not candidates:
        # Fallback to any unit activity
        candidates = get_activities_for_unit(unit)
        candidates = [a for a in candidates if a.get('id') not in exclude_ids]

    if not candidates:
        # Last resort
        candidates = ACTIVITY_BANK.get('collaborative', [])

    selected = random.choice(candidates)

    # Add standard structure
    selected['structure'] = ACTIVITY_STRUCTURE
    selected['time_warnings'] = TIME_WARNINGS

    return selected


def validate_activity_structure(activity: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate activity has required structure.

    Returns validation result.
    """
    issues = []

    # Check required fields
    required = ['name', 'type', 'duration_minutes', 'instructions', 'grouping']
    for field in required:
        if not activity.get(field):
            issues.append(f"Missing required field: {field}")

    # Check duration
    if activity.get('duration_minutes') != 15:
        issues.append(f"Duration should be 15 minutes, got {activity.get('duration_minutes')}")

    # Check differentiation
    diff = activity.get('differentiation', {})
    if not diff.get('ell'):
        issues.append("Missing ELL differentiation")
    if not diff.get('advanced'):
        issues.append("Missing advanced differentiation")
    if not diff.get('struggling'):
        issues.append("Missing struggling learner differentiation")

    return {
        'valid': len(issues) == 0,
        'issues': issues
    }


def format_activity_for_output(activity: Dict[str, Any]) -> Dict[str, Any]:
    """Format activity for pipeline output schema."""
    return {
        'name': activity.get('name', ''),
        'type': activity.get('type', ''),
        'duration_minutes': activity.get('duration_minutes', 15),
        'description': activity.get('description', ''),
        'instructions': activity.get('instructions', ''),
        'materials_needed': activity.get('materials_needed', []),
        'grouping': activity.get('grouping', ''),
        'structure': activity.get('structure', ACTIVITY_STRUCTURE),
        'time_warnings': activity.get('time_warnings', TIME_WARNINGS),
        'differentiation': activity.get('differentiation', {}),
        'success_criteria': activity.get('success_criteria', []),
        'requires_handout': activity.get('requires_handout', False)
    }


if __name__ == "__main__":
    print("Testing activity selection...\n")

    for unit in ['greek_theater', 'commedia_dellarte', 'shakespeare', 'student_directed_one_acts']:
        activity = select_activity(unit=unit)
        print(f"Unit: {unit}")
        print(f"  Selected: {activity['name']}")
        print(f"  Type: {activity['type']}")
        print(f"  Requires handout: {activity.get('requires_handout', False)}")
        print()

    print("Type filtering test:")
    activity = select_activity(unit='commedia_dellarte', activity_type='performance')
    print(f"  Performance activity: {activity['name']}")

    print("\nValidation test:")
    result = validate_activity_structure(activity)
    print(f"  Valid: {result['valid']}")
    if result['issues']:
        for issue in result['issues']:
            print(f"  - {issue}")
