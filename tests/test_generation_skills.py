"""
Test Suite for Theater Generation Skills
Tests monologue_scripter, warmup_bank_selector, and activity_type_selector.
"""

import pytest
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from skills.generation import (
    # Monologue Scripter
    generate_presenter_notes,
    generate_slide_notes,
    validate_presenter_notes,
    estimate_duration,
    count_words,
    insert_markers,
    SPEAKING_RATE_WPM,
    TARGET_DURATION_MINUTES,
    MIN_WORDS,
    MAX_WORDS,
    TARGET_WORDS,
    # Warmup Bank Selector
    select_warmup,
    get_warmups_by_type,
    get_warmups_for_unit,
    validate_warmup_connection,
    format_warmup_for_output,
    WARMUP_TYPES,
    WARMUP_BANK,
    # Activity Type Selector
    select_activity,
    get_activities_by_type,
    get_activities_for_unit,
    validate_activity_structure,
    format_activity_for_output,
    ACTIVITY_TYPES,
    ACTIVITY_BANK,
    ACTIVITY_STRUCTURE,
)


# =============================================================================
# MONOLOGUE SCRIPTER TESTS
# =============================================================================

class TestMonologueScripter:
    """Tests for presenter notes generation."""

    def test_count_words_basic(self):
        """Test basic word counting."""
        text = "This is a simple test sentence."
        assert count_words(text) == 6

    def test_count_words_with_markers(self):
        """Test word counting excludes markers."""
        text = "This is [PAUSE] a test [EMPHASIS: word] sentence."
        # Should count: This, is, a, test, sentence = 5 words
        assert count_words(text) == 5

    def test_count_words_empty(self):
        """Test empty string returns 0."""
        assert count_words("") == 0
        assert count_words(None) == 0

    def test_estimate_duration(self):
        """Test duration estimation."""
        # 140 words at 140 WPM = 1 minute
        text = " ".join(["word"] * 140)
        duration = estimate_duration(text)
        assert 0.9 <= duration <= 1.1  # Allow some tolerance

    def test_estimate_duration_with_markers(self):
        """Test duration includes marker time."""
        text = "Test sentence. [PAUSE] Another sentence."
        duration_with = estimate_duration(text, include_markers=True)
        duration_without = estimate_duration(text, include_markers=False)
        # With markers should be longer due to pause time
        assert duration_with >= duration_without

    def test_insert_markers_adds_pause(self):
        """Test marker insertion adds [PAUSE]."""
        text = "First sentence. Second sentence. Third sentence."
        result = insert_markers(text)
        assert "[PAUSE]" in result

    def test_generate_slide_notes_returns_string(self):
        """Test slide notes generation returns string."""
        slide = {
            'slide_number': 5,
            'type': 'content',
            'header': 'Greek Theater Architecture',
            'body': '- The theatron\n- The orchestra\n- The skene'
        }
        notes = generate_slide_notes(slide, unit_number=1)
        assert isinstance(notes, str)
        assert len(notes) > 0

    def test_generate_slide_notes_includes_content(self):
        """Test slide notes reference slide content."""
        slide = {
            'slide_number': 5,
            'type': 'content',
            'header': 'The Theatron',
            'body': '- Seating area\n- Could hold 17000 spectators'
        }
        notes = generate_slide_notes(slide, unit_number=1)
        # Should mention theatron or seating
        assert 'theatron' in notes.lower() or 'seat' in notes.lower()

    def test_validate_presenter_notes_valid(self):
        """Test validation passes for valid notes."""
        # Generate enough words for valid notes
        notes = " ".join(["word"] * 2100)  # Target is 2100
        result = validate_presenter_notes(notes)
        assert result['valid'] == True

    def test_validate_presenter_notes_too_short(self):
        """Test validation fails for too short notes."""
        notes = "This is way too short."
        result = validate_presenter_notes(notes)
        assert result['valid'] == False
        assert any('short' in issue['type'] or 'under' in issue['type']
                   for issue in result.get('issues', []))

    def test_constants_defined(self):
        """Test required constants are defined."""
        assert SPEAKING_RATE_WPM == 140
        assert TARGET_DURATION_MINUTES == 15
        assert MIN_WORDS == 1950
        assert MAX_WORDS == 2250
        assert TARGET_WORDS == 2100


# =============================================================================
# WARMUP BANK SELECTOR TESTS
# =============================================================================

class TestWarmupBankSelector:
    """Tests for warmup selection."""

    def test_warmup_types_defined(self):
        """Test warmup types are defined."""
        assert len(WARMUP_TYPES) >= 5
        assert 'physical' in WARMUP_TYPES
        assert 'vocal' in WARMUP_TYPES or 'mental' in WARMUP_TYPES

    def test_warmup_bank_not_empty(self):
        """Test warmup bank has entries."""
        assert len(WARMUP_BANK) >= 10

    def test_get_warmups_by_type(self):
        """Test filtering warmups by type."""
        physical = get_warmups_by_type('physical')
        assert len(physical) >= 1
        for warmup in physical:
            assert warmup['type'] == 'physical'

    def test_get_warmups_for_unit(self):
        """Test getting warmups for a specific unit."""
        warmups = get_warmups_for_unit(1)  # Greek Theater
        assert len(warmups) >= 1

    def test_select_warmup_returns_dict(self):
        """Test warmup selection returns dictionary."""
        warmup = select_warmup(unit_number=1)
        assert isinstance(warmup, dict)
        assert 'name' in warmup
        assert 'type' in warmup

    def test_select_warmup_with_type(self):
        """Test warmup selection with type filter."""
        warmup = select_warmup(unit_number=1, warmup_type='physical')
        assert warmup['type'] == 'physical'

    def test_validate_warmup_connection(self):
        """Test warmup connection validation."""
        warmup = {
            'name': 'Greek Chorus Walk',
            'connection': 'Prepares bodies for understanding orchestra space'
        }
        result = validate_warmup_connection(warmup, 'Greek theater architecture')
        assert isinstance(result, dict)
        assert 'valid' in result

    def test_format_warmup_for_output(self):
        """Test warmup formatting for output."""
        warmup = select_warmup(unit_number=1)
        formatted = format_warmup_for_output(warmup, unit_number=1)
        assert isinstance(formatted, dict)
        assert 'name' in formatted
        assert 'instructions' in formatted or 'steps' in formatted or 'phases' in formatted

    def test_warmup_has_required_fields(self):
        """Test each warmup has required fields."""
        for warmup in WARMUP_BANK:
            assert 'name' in warmup, f"Warmup missing 'name'"
            assert 'type' in warmup, f"Warmup {warmup.get('name')} missing 'type'"
            assert 'duration' in warmup, f"Warmup {warmup.get('name')} missing 'duration'"


# =============================================================================
# ACTIVITY TYPE SELECTOR TESTS
# =============================================================================

class TestActivityTypeSelector:
    """Tests for activity selection."""

    def test_activity_types_defined(self):
        """Test activity types are defined."""
        assert len(ACTIVITY_TYPES) >= 5

    def test_activity_bank_not_empty(self):
        """Test activity bank has entries."""
        assert len(ACTIVITY_BANK) >= 10

    def test_activity_structure_defined(self):
        """Test activity structure timing is defined."""
        assert 'setup' in ACTIVITY_STRUCTURE
        assert 'work' in ACTIVITY_STRUCTURE
        assert 'sharing' in ACTIVITY_STRUCTURE
        # Total should be 15 minutes
        total = (ACTIVITY_STRUCTURE['setup'] +
                 ACTIVITY_STRUCTURE['work'] +
                 ACTIVITY_STRUCTURE['sharing'])
        assert total == 15

    def test_get_activities_by_type(self):
        """Test filtering activities by type."""
        discussions = get_activities_by_type('discussion')
        assert len(discussions) >= 1

    def test_get_activities_for_unit(self):
        """Test getting activities for a specific unit."""
        activities = get_activities_for_unit(1)  # Greek Theater
        assert len(activities) >= 1

    def test_select_activity_returns_dict(self):
        """Test activity selection returns dictionary."""
        activity = select_activity(unit_number=1)
        assert isinstance(activity, dict)
        assert 'name' in activity
        assert 'type' in activity

    def test_select_activity_with_type(self):
        """Test activity selection with type filter."""
        activity = select_activity(unit_number=1, activity_type='discussion')
        assert activity['type'] == 'discussion'

    def test_validate_activity_structure(self):
        """Test activity structure validation."""
        activity = {
            'name': 'Gallery Walk',
            'type': 'gallery_walk',
            'duration': 15,
            'setup': 'Post diagrams around room',
            'instructions': 'Rotate through stations'
        }
        result = validate_activity_structure(activity)
        assert isinstance(result, dict)
        assert 'valid' in result

    def test_format_activity_for_output(self):
        """Test activity formatting for output."""
        activity = select_activity(unit_number=1)
        formatted = format_activity_for_output(activity, unit_number=1)
        assert isinstance(formatted, dict)
        assert 'name' in formatted

    def test_activity_has_required_fields(self):
        """Test each activity has required fields."""
        for activity in ACTIVITY_BANK:
            assert 'name' in activity, f"Activity missing 'name'"
            assert 'type' in activity, f"Activity {activity.get('name')} missing 'type'"

    def test_activity_has_differentiation(self):
        """Test activities have differentiation options."""
        # At least some activities should have differentiation
        has_diff = sum(1 for a in ACTIVITY_BANK if 'differentiation' in a)
        assert has_diff >= len(ACTIVITY_BANK) // 2  # At least half


# =============================================================================
# INTEGRATION TESTS
# =============================================================================

class TestGenerationIntegration:
    """Integration tests for generation skills working together."""

    def test_generate_complete_lesson_components(self):
        """Test generating warmup, activity, and notes for a lesson."""
        unit = 1
        topic = "Greek Theater Architecture"

        # Select warmup
        warmup = select_warmup(unit_number=unit, warmup_type='physical')
        assert warmup is not None

        # Select activity
        activity = select_activity(unit_number=unit, activity_type='discussion')
        assert activity is not None

        # Generate notes for a slide
        slide = {
            'slide_number': 5,
            'type': 'content',
            'header': topic,
            'body': '- The theatron\n- The orchestra'
        }
        notes = generate_slide_notes(slide, unit_number=unit)
        assert len(notes) > 50  # Should have substantial content

    def test_warmup_activity_coherence(self):
        """Test warmup and activity can be coherently selected."""
        unit = 1  # Greek Theater

        warmup = select_warmup(unit_number=unit)
        activity = select_activity(unit_number=unit)

        # Both should have unit-appropriate content
        warmup_formatted = format_warmup_for_output(warmup, unit_number=unit)
        activity_formatted = format_activity_for_output(activity, unit_number=unit)

        assert warmup_formatted is not None
        assert activity_formatted is not None


# =============================================================================
# RUN TESTS
# =============================================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
