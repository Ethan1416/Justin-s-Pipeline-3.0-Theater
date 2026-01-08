"""
Timing Allocator Skill
Allocate time across lesson components within the 56-minute structure.

Theater Pipeline Requirements:
- 56-minute total class period
- Fixed allocations: Agenda (5), Warmup (5), Lecture (15), Activity (15), Reflection (10), Buffer (6)
- Sub-component timing for activities and reflection

Usage:
    from skills.utilities.timing_allocator import (
        allocate_lesson_time,
        allocate_activity_time,
        allocate_reflection_time,
        validate_timing,
        suggest_adjustments
    )
"""

from typing import Dict, Any, List, Optional, Tuple


# Standard lesson structure (56 minutes)
LESSON_STRUCTURE = {
    'total_minutes': 56,
    'components': {
        'agenda': {'minutes': 5, 'tolerance': 0.5, 'required': True},
        'warmup': {'minutes': 5, 'tolerance': 0.5, 'required': True},
        'lecture': {'minutes': 15, 'tolerance': 1.0, 'required': True},
        'activity': {'minutes': 15, 'tolerance': 1.0, 'required': True},
        'reflection': {'minutes': 10, 'tolerance': 1.0, 'required': True},
        'buffer': {'minutes': 6, 'tolerance': 0, 'required': True},
    }
}

# Activity sub-component timing
ACTIVITY_STRUCTURE = {
    'total_minutes': 15,
    'setup': {'minutes': 1.5, 'tolerance': 0.5},
    'work': {'minutes': 11, 'tolerance': 1.0},
    'sharing': {'minutes': 2.5, 'tolerance': 0.5},
}

# Reflection sub-component timing
REFLECTION_STRUCTURE = {
    'total_minutes': 10,
    'journal': {'minutes': 7, 'tolerance': 1.0},
    'exit_ticket': {'minutes': 3, 'tolerance': 0.5},
}

# Activity type timing variations
ACTIVITY_TYPE_TIMING = {
    'discussion': {'setup': 1.0, 'work': 12.0, 'sharing': 2.0},
    'gallery_walk': {'setup': 2.0, 'work': 10.0, 'sharing': 3.0},
    'small_group': {'setup': 1.5, 'work': 11.0, 'sharing': 2.5},
    'pair_work': {'setup': 1.0, 'work': 11.5, 'sharing': 2.5},
    'individual': {'setup': 1.0, 'work': 12.0, 'sharing': 2.0},
    'performance': {'setup': 2.0, 'work': 10.0, 'sharing': 3.0},
    'tableaux': {'setup': 1.5, 'work': 10.5, 'sharing': 3.0},
    'improvisation': {'setup': 2.0, 'work': 10.0, 'sharing': 3.0},
    'scene_work': {'setup': 2.0, 'work': 10.0, 'sharing': 3.0},
    'blocking': {'setup': 2.0, 'work': 11.0, 'sharing': 2.0},
    'text_analysis': {'setup': 1.0, 'work': 11.5, 'sharing': 2.5},
    'writing': {'setup': 1.0, 'work': 12.0, 'sharing': 2.0},
}


def allocate_lesson_time(
    adjustments: Dict[str, float] = None
) -> Dict[str, Any]:
    """
    Allocate time across main lesson components.

    Args:
        adjustments: Optional timing adjustments by component name

    Returns:
        Time allocation with cumulative markers
    """
    adjustments = adjustments or {}
    allocation = {}
    cumulative = 0

    for component, config in LESSON_STRUCTURE['components'].items():
        minutes = config['minutes']

        # Apply adjustment if provided
        if component in adjustments:
            adj = adjustments[component]
            # Respect tolerance
            max_adj = config['tolerance']
            adj = max(-max_adj, min(max_adj, adj))
            minutes += adj

        start_time = cumulative
        end_time = cumulative + minutes

        allocation[component] = {
            'minutes': minutes,
            'start': start_time,
            'end': end_time,
            'time_marker': f"{int(start_time)}:{int((start_time % 1) * 60):02d}-{int(end_time)}:{int((end_time % 1) * 60):02d}",
            'tolerance': config['tolerance']
        }

        cumulative = end_time

    # Verify total
    total = sum(a['minutes'] for a in allocation.values())

    return {
        'allocation': allocation,
        'total_minutes': total,
        'target_total': LESSON_STRUCTURE['total_minutes'],
        'valid': abs(total - LESSON_STRUCTURE['total_minutes']) < 0.1
    }


def allocate_activity_time(
    activity_type: str = 'small_group',
    total_minutes: float = 15
) -> Dict[str, Any]:
    """
    Allocate time within activity component.

    Args:
        activity_type: Type of activity
        total_minutes: Total activity time (default 15)

    Returns:
        Sub-component time allocation
    """
    # Get timing for activity type or use default
    timing = ACTIVITY_TYPE_TIMING.get(
        activity_type.lower(),
        ACTIVITY_STRUCTURE
    )

    if isinstance(timing, dict) and 'setup' in timing:
        setup = timing['setup']
        work = timing['work']
        sharing = timing['sharing']
    else:
        setup = ACTIVITY_STRUCTURE['setup']['minutes']
        work = ACTIVITY_STRUCTURE['work']['minutes']
        sharing = ACTIVITY_STRUCTURE['sharing']['minutes']

    # Scale if total is different from 15
    scale = total_minutes / 15
    setup *= scale
    work *= scale
    sharing *= scale

    return {
        'activity_type': activity_type,
        'total_minutes': total_minutes,
        'allocation': {
            'setup': {
                'minutes': round(setup, 1),
                'description': 'Explain instructions, distribute materials'
            },
            'work': {
                'minutes': round(work, 1),
                'description': 'Main activity time'
            },
            'sharing': {
                'minutes': round(sharing, 1),
                'description': 'Share out, discussion, debrief'
            }
        },
        'teacher_notes': {
            'setup': f"Keep instructions to {round(setup, 1)} minutes maximum",
            'work': f"Give time warnings at {round(work/2, 1)} min and 1 min remaining",
            'sharing': f"Allow {round(sharing, 1)} minutes for share-out"
        }
    }


def allocate_reflection_time(
    journal_focus: str = 'standard',
    total_minutes: float = 10
) -> Dict[str, Any]:
    """
    Allocate time within reflection component.

    Args:
        journal_focus: Type of journal activity (standard, extended, brief)
        total_minutes: Total reflection time (default 10)

    Returns:
        Sub-component time allocation
    """
    # Adjust based on journal focus
    journal_allocations = {
        'standard': {'journal': 7, 'exit_ticket': 3},
        'extended': {'journal': 8, 'exit_ticket': 2},
        'brief': {'journal': 5, 'exit_ticket': 5},
        'exit_only': {'journal': 2, 'exit_ticket': 8},
    }

    base = journal_allocations.get(journal_focus.lower(), journal_allocations['standard'])

    # Scale if total is different from 10
    scale = total_minutes / 10
    journal = base['journal'] * scale
    exit_ticket = base['exit_ticket'] * scale

    return {
        'journal_focus': journal_focus,
        'total_minutes': total_minutes,
        'allocation': {
            'journal': {
                'minutes': round(journal, 1),
                'description': 'Written reflection time'
            },
            'exit_ticket': {
                'minutes': round(exit_ticket, 1),
                'description': 'Complete and submit exit ticket'
            }
        },
        'teacher_notes': {
            'journal': f"Silent writing time, circulate to encourage depth",
            'exit_ticket': f"Quick assessment, collect before dismissal"
        }
    }


def format_time_marker(minutes: float) -> str:
    """
    Format minutes as MM:SS time marker.

    Args:
        minutes: Time in minutes

    Returns:
        Formatted time string (e.g., "5:30")
    """
    whole_minutes = int(minutes)
    seconds = int((minutes % 1) * 60)
    return f"{whole_minutes}:{seconds:02d}"


def generate_timing_script(
    activity_type: str = 'small_group',
    start_minute: float = 25
) -> Dict[str, Any]:
    """
    Generate a timing script for the teacher.

    Args:
        activity_type: Type of activity
        start_minute: When the activity starts in the class period

    Returns:
        Timing script with cues
    """
    activity_timing = allocate_activity_time(activity_type)

    setup_end = start_minute + activity_timing['allocation']['setup']['minutes']
    work_end = setup_end + activity_timing['allocation']['work']['minutes']
    sharing_end = work_end + activity_timing['allocation']['sharing']['minutes']

    work_halfway = setup_end + (activity_timing['allocation']['work']['minutes'] / 2)
    work_warning = work_end - 1  # 1 minute warning

    script = {
        'cues': [
            {
                'time': format_time_marker(start_minute),
                'action': 'Begin activity instructions',
                'script': 'Now it\'s time for your activity...'
            },
            {
                'time': format_time_marker(setup_end),
                'action': 'Start work time',
                'script': 'Go ahead and begin!'
            },
            {
                'time': format_time_marker(work_halfway),
                'action': 'Halfway check',
                'script': f'You\'re halfway through - about {round(activity_timing["allocation"]["work"]["minutes"]/2)} minutes remaining.'
            },
            {
                'time': format_time_marker(work_warning),
                'action': 'One minute warning',
                'script': 'One minute remaining!'
            },
            {
                'time': format_time_marker(work_end),
                'action': 'Transition to sharing',
                'script': 'Time! Let\'s come together to share...'
            },
            {
                'time': format_time_marker(sharing_end),
                'action': 'Activity complete',
                'script': 'Great work everyone!'
            }
        ],
        'timing': activity_timing
    }

    return script


def validate_timing(
    components: Dict[str, float]
) -> Dict[str, Any]:
    """
    Validate that component timing sums to 56 minutes.

    Args:
        components: Dictionary of component names to minutes

    Returns:
        Validation result
    """
    total = sum(components.values())
    expected = LESSON_STRUCTURE['total_minutes']

    issues = []

    # Check total
    if abs(total - expected) > 0.5:
        issues.append({
            'type': 'total_mismatch',
            'severity': 'error',
            'message': f'Total time ({total} min) does not equal {expected} min',
            'difference': total - expected
        })

    # Check individual components
    for component, config in LESSON_STRUCTURE['components'].items():
        if component in components:
            actual = components[component]
            expected_min = config['minutes']
            tolerance = config['tolerance']

            if abs(actual - expected_min) > tolerance:
                issues.append({
                    'type': 'component_out_of_range',
                    'severity': 'warning',
                    'component': component,
                    'message': f'{component} time ({actual} min) outside tolerance (±{tolerance}) of {expected_min} min'
                })
        elif config['required']:
            issues.append({
                'type': 'missing_component',
                'severity': 'error',
                'component': component,
                'message': f'Required component {component} is missing'
            })

    return {
        'valid': not any(i['severity'] == 'error' for i in issues),
        'total_minutes': total,
        'target_minutes': expected,
        'issues': issues
    }


def suggest_adjustments(
    current_timing: Dict[str, float],
    target_total: float = 56
) -> Dict[str, Any]:
    """
    Suggest timing adjustments to reach target total.

    Args:
        current_timing: Current component timing
        target_total: Target total minutes

    Returns:
        Suggested adjustments
    """
    current_total = sum(current_timing.values())
    difference = target_total - current_total

    if abs(difference) < 0.5:
        return {
            'needed': False,
            'current_total': current_total,
            'target_total': target_total,
            'suggestions': []
        }

    suggestions = []

    if difference > 0:
        # Need to add time
        # First try buffer
        if 'buffer' in current_timing:
            add_to_buffer = min(difference, 2)  # Max 2 min to buffer
            suggestions.append({
                'component': 'buffer',
                'action': 'add',
                'minutes': add_to_buffer,
                'reason': 'Buffer can absorb additional time'
            })
            difference -= add_to_buffer

        # Then try reflection
        if difference > 0 and 'reflection' in current_timing:
            add_to_reflection = min(difference, 1)
            suggestions.append({
                'component': 'reflection',
                'action': 'add',
                'minutes': add_to_reflection,
                'reason': 'Extended journal time supports deeper thinking'
            })
            difference -= add_to_reflection
    else:
        # Need to remove time
        difference = abs(difference)

        # First try buffer
        if 'buffer' in current_timing and current_timing['buffer'] > 4:
            remove_from_buffer = min(difference, current_timing['buffer'] - 4)
            suggestions.append({
                'component': 'buffer',
                'action': 'remove',
                'minutes': remove_from_buffer,
                'reason': 'Buffer can be reduced while maintaining minimum'
            })
            difference -= remove_from_buffer

        # Then try agenda
        if difference > 0 and 'agenda' in current_timing and current_timing['agenda'] > 4:
            remove_from_agenda = min(difference, 1)
            suggestions.append({
                'component': 'agenda',
                'action': 'remove',
                'minutes': remove_from_agenda,
                'reason': 'Agenda review can be streamlined'
            })

    return {
        'needed': True,
        'current_total': current_total,
        'target_total': target_total,
        'difference': target_total - current_total,
        'suggestions': suggestions
    }


def get_time_markers(
    allocation: Dict[str, float] = None
) -> Dict[str, str]:
    """
    Generate time markers for each component.

    Args:
        allocation: Component timing (uses default if None)

    Returns:
        Dictionary of component to time range strings
    """
    if allocation is None:
        result = allocate_lesson_time()
        allocation = {k: v['minutes'] for k, v in result['allocation'].items()}

    markers = {}
    current = 0

    for component in ['agenda', 'warmup', 'lecture', 'activity', 'reflection', 'buffer']:
        if component in allocation:
            start = current
            end = current + allocation[component]
            markers[component] = f"{format_time_marker(start)}-{format_time_marker(end)}"
            current = end

    return markers


if __name__ == "__main__":
    # Test
    print("Timing Allocator Test")
    print("=" * 50)

    # Test lesson allocation
    lesson = allocate_lesson_time()
    print("\nLesson Time Allocation:")
    for component, data in lesson['allocation'].items():
        print(f"  {component}: {data['minutes']} min ({data['time_marker']})")
    print(f"  Total: {lesson['total_minutes']} min")

    # Test activity allocation
    print("\nActivity Allocation (gallery_walk):")
    activity = allocate_activity_time('gallery_walk')
    for sub, data in activity['allocation'].items():
        print(f"  {sub}: {data['minutes']} min")

    # Test timing script
    print("\nTiming Script:")
    script = generate_timing_script('gallery_walk', 25)
    for cue in script['cues']:
        print(f"  {cue['time']}: {cue['action']}")

    # Test validation
    print("\nValidation Test:")
    test_timing = {'agenda': 5, 'warmup': 5, 'lecture': 15, 'activity': 15, 'reflection': 10, 'buffer': 6}
    result = validate_timing(test_timing)
    print(f"  Valid: {result['valid']}")
    print(f"  Total: {result['total_minutes']} min")
