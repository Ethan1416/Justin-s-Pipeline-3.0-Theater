"""
Test Suite for Theater Utility Skills
Tests timing_pacer, blooms_verb_selector, and timing_allocator.
"""

import pytest
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from skills.utilities import (
    # Timing Pacer
    pace_content,
    pace_presentation,
    calculate_target_words,
    suggest_content_adjustments,
    validate_pacing,
    distribute_words,
    pacer_estimate_duration,
    pacer_count_words,
    SPEAKING_RATE_WPM,
    TOTAL_WORDS_MIN,
    TOTAL_WORDS_MAX,
    TOTAL_WORDS_TARGET,
    SLIDE_WORD_TARGETS,
    # Bloom's Verb Selector
    select_verb,
    get_verbs_for_level,
    classify_verb,
    validate_objective,
    generate_objective,
    suggest_objectives_for_lesson,
    get_level_info,
    BLOOMS_LEVELS,
    BLOOMS_VERBS,
    THEATER_VERBS,
    LEVEL_DESCRIPTIONS,
    # Timing Allocator
    allocate_lesson_time,
    allocate_activity_time,
    allocate_reflection_time,
    validate_timing,
    suggest_adjustments,
    generate_timing_script,
    format_time_marker,
    get_time_markers,
    LESSON_STRUCTURE,
    ACTIVITY_STRUCTURE,
    REFLECTION_STRUCTURE,
    ACTIVITY_TYPE_TIMING,
)


# =============================================================================
# TIMING PACER TESTS
# =============================================================================

class TestTimingPacer:
    """Tests for content pacing."""

    def test_count_words_basic(self):
        """Test basic word counting."""
        text = "This is a test sentence."
        assert pacer_count_words(text) == 5

    def test_count_words_with_markers(self):
        """Test markers excluded from count."""
        text = "This [PAUSE] is a test."
        assert pacer_count_words(text) == 4

    def test_estimate_duration(self):
        """Test duration estimation."""
        # 140 words at 140 WPM = 1 minute
        text = " ".join(["word"] * 140)
        duration = pacer_estimate_duration(text)
        assert 0.95 <= duration <= 1.05

    def test_calculate_target_words(self):
        """Test target word calculation."""
        # 15 minutes at 140 WPM = 2100 words
        target = calculate_target_words(15, 140, 0)
        assert target == 2100

    def test_calculate_target_words_with_markers(self):
        """Test target words accounts for markers."""
        # Markers take time, so fewer words needed
        target_with = calculate_target_words(15, 140, 10)
        target_without = calculate_target_words(15, 140, 0)
        assert target_with < target_without

    def test_pace_content_ok(self):
        """Test pacing for content at target."""
        text = " ".join(["word"] * 175)
        result = pace_content(text, 175, 'content')
        assert result['status'] == 'ok'
        assert result['action'] == 'none'

    def test_pace_content_under(self):
        """Test pacing detects under-target."""
        text = "Too short."
        result = pace_content(text, 175, 'content')
        assert result['status'] == 'under'
        assert result['action'] == 'expand'

    def test_pace_content_over(self):
        """Test pacing detects over-target."""
        text = " ".join(["word"] * 300)
        result = pace_content(text, 175, 'content')
        assert result['status'] == 'over'
        assert result['action'] == 'condense'

    def test_suggest_content_adjustments_expand(self):
        """Test suggestions for expanding content."""
        pacing = {'action': 'expand', 'deviation': -50}
        suggestions = suggest_content_adjustments(pacing)
        assert len(suggestions) > 0
        assert any(s['type'] == 'add_example' for s in suggestions)

    def test_suggest_content_adjustments_condense(self):
        """Test suggestions for condensing content."""
        pacing = {'action': 'condense', 'deviation': 50}
        suggestions = suggest_content_adjustments(pacing)
        assert len(suggestions) > 0
        assert any(s['type'] == 'remove_redundancy' for s in suggestions)

    def test_distribute_words(self):
        """Test word distribution across slides."""
        result = distribute_words(2100, 16, 4)
        assert result['auxiliary_per_slide'] > 0
        assert result['content_per_slide'] > 0
        assert result['title_slide'] > 0
        assert result['summary_slide'] > 0
        # Total should approximately equal input
        total = result['distribution']['grand_total']
        assert abs(total - 2100) < 50  # Allow some rounding

    def test_validate_pacing_valid(self):
        """Test pacing validation for valid presentation."""
        slides = [
            {'slide_number': i, 'type': 'content',
             'notes': " ".join(["word"] * 175)}
            for i in range(1, 13)
        ]
        result = validate_pacing(slides)
        assert result['valid'] == True

    def test_constants_defined(self):
        """Test constants are properly defined."""
        assert SPEAKING_RATE_WPM == 140
        assert TOTAL_WORDS_MIN == 1950
        assert TOTAL_WORDS_MAX == 2250
        assert TOTAL_WORDS_TARGET == 2100


# =============================================================================
# BLOOM'S VERB SELECTOR TESTS
# =============================================================================

class TestBloomsVerbSelector:
    """Tests for Bloom's taxonomy verb selection."""

    def test_blooms_levels_defined(self):
        """Test all Bloom's levels are defined."""
        assert len(BLOOMS_LEVELS) == 6
        assert 'remember' in BLOOMS_LEVELS
        assert 'understand' in BLOOMS_LEVELS
        assert 'apply' in BLOOMS_LEVELS
        assert 'analyze' in BLOOMS_LEVELS
        assert 'evaluate' in BLOOMS_LEVELS
        assert 'create' in BLOOMS_LEVELS

    def test_blooms_verbs_populated(self):
        """Test verbs exist for each level."""
        for level in BLOOMS_LEVELS:
            assert len(BLOOMS_VERBS[level]) >= 10

    def test_theater_verbs_defined(self):
        """Test theater-specific verbs are defined."""
        assert len(THEATER_VERBS) > 0
        # Check for theater-specific verbs
        all_theater = []
        for verbs in THEATER_VERBS.values():
            all_theater.extend(verbs)
        assert 'perform' in all_theater or 'demonstrate' in all_theater

    def test_get_verbs_for_level(self):
        """Test getting verbs for a specific level."""
        verbs = get_verbs_for_level('analyze')
        assert len(verbs) >= 10
        assert 'analyze' in verbs

    def test_get_verbs_for_level_with_theater(self):
        """Test including theater verbs."""
        verbs_with = get_verbs_for_level('create', include_theater=True)
        verbs_without = get_verbs_for_level('create', include_theater=False)
        assert len(verbs_with) >= len(verbs_without)

    def test_select_verb(self):
        """Test verb selection."""
        verb = select_verb('understand')
        assert isinstance(verb, str)
        assert len(verb) > 0

    def test_select_verb_excludes(self):
        """Test verb selection with exclusions."""
        verb = select_verb('remember', exclude=['identify', 'name', 'list'])
        assert verb not in ['identify', 'name', 'list']

    def test_classify_verb_found(self):
        """Test verb classification for known verb."""
        result = classify_verb('analyze')
        assert result['found'] == True
        assert 'analyze' in result['levels']

    def test_classify_verb_not_found(self):
        """Test verb classification for unknown verb."""
        result = classify_verb('wiggle')
        assert result['found'] == False

    def test_classify_verb_theater(self):
        """Test classification identifies theater verbs."""
        result = classify_verb('perform')
        assert result['found'] == True
        assert result['is_theater_verb'] == True

    def test_validate_objective_valid(self):
        """Test validation of valid objective."""
        result = validate_objective("Identify the parts of a Greek theater")
        assert result['valid'] == True
        assert result['is_measurable'] == True

    def test_validate_objective_invalid_verb(self):
        """Test validation catches invalid verb."""
        result = validate_objective("Know about theater history")
        assert result['valid'] == False
        assert any(i['type'] == 'not_measurable' for i in result['issues'])

    def test_validate_objective_with_students_will(self):
        """Test parsing 'Students will...' pattern."""
        result = validate_objective("Students will analyze the use of masks")
        assert result['valid'] == True
        assert result['extracted_verb'] == 'analyze'

    def test_generate_objective(self):
        """Test objective generation."""
        objective = generate_objective('Greek masks', 'analyze')
        assert isinstance(objective, str)
        assert len(objective) > 10

    def test_suggest_objectives_for_lesson(self):
        """Test objective suggestions for lesson type."""
        suggestions = suggest_objectives_for_lesson('content', 'Greek theater', 2)
        assert len(suggestions) == 2
        for s in suggestions:
            assert 'objective' in s
            assert 'level' in s
            assert 'verb' in s

    def test_get_level_info(self):
        """Test getting level information."""
        info = get_level_info('analyze')
        assert info['level'] == 'analyze'
        assert info['order'] == 4  # 4th level
        assert 'description' in info
        assert info['is_higher_order'] == True


# =============================================================================
# TIMING ALLOCATOR TESTS
# =============================================================================

class TestTimingAllocator:
    """Tests for 56-minute timing allocation."""

    def test_lesson_structure_defined(self):
        """Test lesson structure is defined."""
        assert LESSON_STRUCTURE['total_minutes'] == 56
        assert 'agenda' in LESSON_STRUCTURE['components']
        assert 'warmup' in LESSON_STRUCTURE['components']
        assert 'lecture' in LESSON_STRUCTURE['components']
        assert 'activity' in LESSON_STRUCTURE['components']
        assert 'reflection' in LESSON_STRUCTURE['components']
        assert 'buffer' in LESSON_STRUCTURE['components']

    def test_activity_structure_defined(self):
        """Test activity structure sums to 15 minutes."""
        total = (ACTIVITY_STRUCTURE['setup']['minutes'] +
                 ACTIVITY_STRUCTURE['work']['minutes'] +
                 ACTIVITY_STRUCTURE['sharing']['minutes'])
        assert total == 15

    def test_reflection_structure_defined(self):
        """Test reflection structure sums to 10 minutes."""
        total = (REFLECTION_STRUCTURE['journal']['minutes'] +
                 REFLECTION_STRUCTURE['exit_ticket']['minutes'])
        assert total == 10

    def test_allocate_lesson_time(self):
        """Test basic lesson time allocation."""
        result = allocate_lesson_time()
        assert result['valid'] == True
        assert result['total_minutes'] == 56

    def test_allocate_lesson_time_components(self):
        """Test all components are allocated."""
        result = allocate_lesson_time()
        expected = ['agenda', 'warmup', 'lecture', 'activity', 'reflection', 'buffer']
        for comp in expected:
            assert comp in result['allocation']
            assert result['allocation'][comp]['minutes'] > 0

    def test_allocate_lesson_time_markers(self):
        """Test time markers are sequential."""
        result = allocate_lesson_time()
        prev_end = 0
        for comp in ['agenda', 'warmup', 'lecture', 'activity', 'reflection', 'buffer']:
            assert result['allocation'][comp]['start'] == prev_end
            prev_end = result['allocation'][comp]['end']

    def test_allocate_activity_time_default(self):
        """Test default activity allocation."""
        result = allocate_activity_time()
        assert result['total_minutes'] == 15
        total = sum(v['minutes'] for v in result['allocation'].values())
        assert abs(total - 15) < 0.1

    def test_allocate_activity_time_gallery_walk(self):
        """Test gallery walk activity timing."""
        result = allocate_activity_time('gallery_walk')
        assert result['activity_type'] == 'gallery_walk'
        # Gallery walk has more setup and sharing time
        assert result['allocation']['setup']['minutes'] >= 2.0

    def test_allocate_reflection_time(self):
        """Test reflection time allocation."""
        result = allocate_reflection_time()
        assert result['total_minutes'] == 10
        assert result['allocation']['journal']['minutes'] == 7
        assert result['allocation']['exit_ticket']['minutes'] == 3

    def test_allocate_reflection_extended(self):
        """Test extended reflection allocation."""
        result = allocate_reflection_time('extended')
        assert result['allocation']['journal']['minutes'] > 7

    def test_format_time_marker(self):
        """Test time marker formatting."""
        assert format_time_marker(5) == "5:00"
        assert format_time_marker(5.5) == "5:30"
        assert format_time_marker(10.75) == "10:45"

    def test_get_time_markers(self):
        """Test getting all time markers."""
        markers = get_time_markers()
        assert 'agenda' in markers
        assert markers['agenda'] == "0:00-5:00"
        assert markers['warmup'] == "5:00-10:00"

    def test_validate_timing_valid(self):
        """Test validation of valid timing."""
        timing = {
            'agenda': 5,
            'warmup': 5,
            'lecture': 15,
            'activity': 15,
            'reflection': 10,
            'buffer': 6
        }
        result = validate_timing(timing)
        assert result['valid'] == True
        assert result['total_minutes'] == 56

    def test_validate_timing_invalid_total(self):
        """Test validation catches wrong total."""
        timing = {
            'agenda': 5,
            'warmup': 5,
            'lecture': 15,
            'activity': 15,
            'reflection': 10,
            'buffer': 10  # Too much buffer
        }
        result = validate_timing(timing)
        assert result['valid'] == False
        assert any(i['type'] == 'total_mismatch' for i in result['issues'])

    def test_suggest_adjustments_needed(self):
        """Test adjustment suggestions when needed."""
        timing = {
            'agenda': 5,
            'warmup': 5,
            'lecture': 15,
            'activity': 15,
            'reflection': 10,
            'buffer': 4  # 2 minutes short
        }
        result = suggest_adjustments(timing)
        assert result['needed'] == True
        assert len(result['suggestions']) > 0

    def test_suggest_adjustments_not_needed(self):
        """Test no suggestions when timing is correct."""
        timing = {
            'agenda': 5,
            'warmup': 5,
            'lecture': 15,
            'activity': 15,
            'reflection': 10,
            'buffer': 6
        }
        result = suggest_adjustments(timing)
        assert result['needed'] == False

    def test_generate_timing_script(self):
        """Test timing script generation."""
        script = generate_timing_script('gallery_walk', 25)
        assert 'cues' in script
        assert len(script['cues']) >= 4
        # Check cues have required fields
        for cue in script['cues']:
            assert 'time' in cue
            assert 'action' in cue

    def test_activity_type_timing_defined(self):
        """Test activity type timings are defined."""
        assert len(ACTIVITY_TYPE_TIMING) >= 5
        assert 'gallery_walk' in ACTIVITY_TYPE_TIMING
        assert 'discussion' in ACTIVITY_TYPE_TIMING


# =============================================================================
# INTEGRATION TESTS
# =============================================================================

class TestUtilityIntegration:
    """Integration tests for utility skills working together."""

    def test_pacing_with_allocation(self):
        """Test pacing integrates with timing allocation."""
        # Get target words for lecture duration
        lecture_minutes = LESSON_STRUCTURE['components']['lecture']['minutes']
        target_words = calculate_target_words(lecture_minutes, SPEAKING_RATE_WPM, 0)

        # Should be close to our standard target
        assert abs(target_words - TOTAL_WORDS_TARGET) < 100

    def test_objectives_for_all_lesson_types(self):
        """Test objectives can be generated for all lesson types."""
        lesson_types = ['introduction', 'content', 'workshop', 'review']
        for lt in lesson_types:
            suggestions = suggest_objectives_for_lesson(lt, 'Greek theater', 2)
            assert len(suggestions) == 2

    def test_complete_lesson_timing(self):
        """Test complete lesson timing workflow."""
        # Allocate main timing
        lesson = allocate_lesson_time()

        # Allocate activity sub-timing
        activity = allocate_activity_time('gallery_walk', 15)

        # Allocate reflection sub-timing
        reflection = allocate_reflection_time('standard', 10)

        # Validate
        timing = {k: v['minutes'] for k, v in lesson['allocation'].items()}
        result = validate_timing(timing)

        assert result['valid'] == True
        assert activity['total_minutes'] == 15
        assert reflection['total_minutes'] == 10


# =============================================================================
# RUN TESTS
# =============================================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
