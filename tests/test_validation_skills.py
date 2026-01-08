"""
Test Suite for Theater Validation Skills
Tests word_count_analyzer, duration_estimator, and sentence_completeness_checker.
"""

import pytest
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from skills.validation import (
    # Word Count Analyzer
    count_words,
    count_words_detailed,
    get_slide_targets,
    analyze_slide_word_count,
    get_per_slide_analysis,
    analyze_word_count,
    validate_word_counts,
    calculate_words_needed,
    suggest_distribution,
    SPEAKING_RATE_WPM,
    TOTAL_REQUIREMENTS,
    SLIDE_TARGETS,
    DEFAULT_TARGETS,
    # Duration Estimator
    estimate_duration,
    estimate_slide_duration,
    estimate_presentation_duration,
    validate_timing,
    get_pacing_analysis,
    calculate_time_adjustment,
    count_markers,
    calculate_marker_time,
    TARGET_DURATION_MINUTES,
    MIN_DURATION_MINUTES,
    MAX_DURATION_MINUTES,
    MARKER_DURATIONS,
    SLIDE_DURATION_TARGETS,
    # Sentence Completeness Checker
    is_complete_sentence,
    check_bullet_point,
    find_truncations,
    validate_text,
    check_sentence_completeness,
    auto_fix_truncations,
    fix_slide_truncations,
    TERMINAL_PUNCTUATION,
    TRUNCATION_PATTERNS,
    FRAGMENT_STARTERS,
)


# =============================================================================
# WORD COUNT ANALYZER TESTS
# =============================================================================

class TestWordCountAnalyzer:
    """Tests for word count analysis."""

    def test_count_words_basic(self):
        """Test basic word counting."""
        text = "This is a test sentence."
        assert count_words(text) == 5

    def test_count_words_excludes_markers(self):
        """Test markers are excluded from count."""
        text = "This [PAUSE] is a [EMPHASIS: test] sentence."
        assert count_words(text) == 4  # This, is, a, sentence

    def test_count_words_empty(self):
        """Test empty input returns 0."""
        assert count_words("") == 0
        assert count_words(None) == 0

    def test_count_words_detailed(self):
        """Test detailed word count."""
        text = "First sentence. Second sentence! [PAUSE] Third?"
        result = count_words_detailed(text)
        assert result['total'] > 0
        assert result['sentence_count'] == 3
        assert result['marker_count'] == 1

    def test_total_requirements_defined(self):
        """Test total word requirements are defined."""
        assert TOTAL_REQUIREMENTS['minimum'] == 1950
        assert TOTAL_REQUIREMENTS['target'] == 2100
        assert TOTAL_REQUIREMENTS['maximum'] == 2250

    def test_get_slide_targets(self):
        """Test getting targets for slide types."""
        content_targets = get_slide_targets('content')
        assert content_targets['min'] > 0
        assert content_targets['target'] > content_targets['min']
        assert content_targets['max'] > content_targets['target']

    def test_analyze_slide_word_count(self):
        """Test per-slide analysis."""
        notes = " ".join(["word"] * 175)  # Target for content slide
        result = analyze_slide_word_count(notes, 'content')
        assert result['word_count'] == 175
        assert result['status'] == 'ok'

    def test_analyze_slide_under_target(self):
        """Test detection of under-target slides."""
        notes = "Too short."
        result = analyze_slide_word_count(notes, 'content')
        assert result['status'] == 'under'
        assert result['recommendation'] is not None

    def test_analyze_slide_over_target(self):
        """Test detection of over-target slides."""
        notes = " ".join(["word"] * 300)  # Well over max
        result = analyze_slide_word_count(notes, 'content')
        assert result['status'] == 'over'

    def test_validate_word_counts_valid(self):
        """Test validation passes for valid counts."""
        # Create slides with appropriate word counts
        slides = [
            {'slide_number': i, 'type': 'content', 'notes': " ".join(["word"] * 175)}
            for i in range(1, 13)
        ]
        result = validate_word_counts(slides)
        assert result['valid'] == True

    def test_validate_word_counts_invalid(self):
        """Test validation fails for invalid counts."""
        slides = [
            {'slide_number': 1, 'type': 'content', 'notes': "Too short."}
        ]
        result = validate_word_counts(slides)
        assert result['valid'] == False

    def test_calculate_words_needed(self):
        """Test words needed calculation."""
        needed = calculate_words_needed(1500, 'minimum')
        assert needed == 450  # 1950 - 1500

    def test_suggest_distribution(self):
        """Test word distribution suggestion."""
        result = suggest_distribution(300, 10)  # 300 words over 10 slides
        assert result['per_slide_average'] == 30


# =============================================================================
# DURATION ESTIMATOR TESTS
# =============================================================================

class TestDurationEstimator:
    """Tests for duration estimation."""

    def test_estimate_duration_basic(self):
        """Test basic duration estimation."""
        # 140 words at 140 WPM = 1 minute
        text = " ".join(["word"] * 140)
        duration = estimate_duration(text)
        assert 0.95 <= duration <= 1.05

    def test_estimate_duration_with_markers(self):
        """Test markers add time."""
        text = "Test. [PAUSE] More test."
        duration = estimate_duration(text)
        # Should include ~2 seconds for PAUSE
        assert duration > estimate_duration("Test. More test.")

    def test_count_markers(self):
        """Test marker counting."""
        text = "[PAUSE] test [PAUSE] more [EMPHASIS: word] [CHECK FOR UNDERSTANDING]"
        markers = count_markers(text)
        assert markers['pause'] == 2
        assert markers['emphasis'] == 1
        assert markers['check_understanding'] == 1

    def test_calculate_marker_time(self):
        """Test marker time calculation."""
        markers = {'pause': 2, 'emphasis': 1, 'check_understanding': 1}
        time = calculate_marker_time(markers)
        expected = (2 * MARKER_DURATIONS['pause'] +
                   1 * MARKER_DURATIONS['emphasis'] +
                   1 * MARKER_DURATIONS['check_understanding'])
        assert time == expected

    def test_estimate_slide_duration(self):
        """Test per-slide duration estimation."""
        notes = " ".join(["word"] * 175)  # ~1.25 minutes
        result = estimate_slide_duration(notes, 'content')
        assert result['word_count'] == 175
        assert result['total_minutes'] > 0
        assert 'status' in result

    def test_validate_timing_valid(self):
        """Test timing validation for valid presentation."""
        # Create slides totaling ~15 minutes (2100 words)
        slides = [
            {'slide_number': i, 'type': 'content',
             'notes': " ".join(["word"] * 175)}
            for i in range(1, 13)  # 12 slides * 175 = 2100 words
        ]
        result = validate_timing(slides)
        assert result['within_range'] == True

    def test_validate_timing_too_short(self):
        """Test timing validation fails for too short."""
        slides = [
            {'slide_number': 1, 'type': 'content', 'notes': "Too short."}
        ]
        result = validate_timing(slides)
        assert result['valid'] == False
        assert any(i['type'] == 'duration_short' for i in result['issues'])

    def test_get_pacing_analysis(self):
        """Test pacing analysis."""
        slides = [
            {'slide_number': i, 'type': 'content',
             'notes': " ".join(["word"] * (150 + i * 5))}
            for i in range(1, 6)
        ]
        result = get_pacing_analysis(slides)
        assert 'average_seconds' in result
        assert 'consistency' in result

    def test_calculate_time_adjustment(self):
        """Test time adjustment calculation."""
        result = calculate_time_adjustment(12, 15)  # 12 min current, 15 target
        assert result['action'] == 'add'
        assert result['difference_minutes'] == 3

    def test_duration_constants_defined(self):
        """Test duration constants are defined."""
        assert TARGET_DURATION_MINUTES == 15
        assert MIN_DURATION_MINUTES == 14
        assert MAX_DURATION_MINUTES == 16


# =============================================================================
# SENTENCE COMPLETENESS CHECKER TESTS
# =============================================================================

class TestSentenceCompletenessChecker:
    """Tests for truncation detection."""

    def test_complete_sentence_period(self):
        """Test complete sentence with period."""
        is_complete, reason = is_complete_sentence("This is complete.")
        assert is_complete == True
        assert reason is None

    def test_complete_sentence_exclamation(self):
        """Test complete sentence with exclamation."""
        is_complete, reason = is_complete_sentence("This is complete!")
        assert is_complete == True

    def test_complete_sentence_question(self):
        """Test complete sentence with question mark."""
        is_complete, reason = is_complete_sentence("Is this complete?")
        assert is_complete == True

    def test_complete_sentence_colon(self):
        """Test complete sentence with colon."""
        is_complete, reason = is_complete_sentence("Remember this:")
        assert is_complete == True

    def test_incomplete_trailing_ellipsis(self):
        """Test detection of trailing ellipsis."""
        is_complete, reason = is_complete_sentence("This is incomplete...")
        assert is_complete == False
        assert 'ellipsis' in reason.lower()

    def test_incomplete_missing_punctuation(self):
        """Test detection of missing punctuation."""
        is_complete, reason = is_complete_sentence("This has no punctuation")
        assert is_complete == False
        assert 'punctuation' in reason.lower()

    def test_incomplete_trailing_and(self):
        """Test detection of trailing 'and'."""
        is_complete, reason = is_complete_sentence("First item and")
        assert is_complete == False

    def test_incomplete_trailing_comma(self):
        """Test detection of trailing comma."""
        is_complete, reason = is_complete_sentence("This ends with,")
        assert is_complete == False

    def test_sentence_with_marker_at_end(self):
        """Test sentence ending with marker is OK."""
        is_complete, reason = is_complete_sentence("This has a pause. [PAUSE]")
        assert is_complete == True

    def test_check_bullet_point_complete(self):
        """Test complete bullet point."""
        is_complete, reason = check_bullet_point("- This is a complete bullet.")
        assert is_complete == True

    def test_check_bullet_point_phrase(self):
        """Test bullet point as phrase (OK without period)."""
        is_complete, reason = check_bullet_point("- Greek theater origins")
        assert is_complete == True  # Phrases are OK in bullets

    def test_find_truncations_none(self):
        """Test no truncations found in clean text."""
        text = "First sentence. Second sentence!"
        issues = find_truncations(text)
        assert len(issues) == 0

    def test_find_truncations_found(self):
        """Test truncations are found."""
        text = "Complete sentence.\nIncomplete sentence..."
        issues = find_truncations(text)
        assert len(issues) >= 1

    def test_validate_text(self):
        """Test text validation."""
        result = validate_text("This is complete.")
        assert result['valid'] == True
        assert result['issue_count'] == 0

    def test_check_sentence_completeness_slides(self):
        """Test slide-level completeness check."""
        slides = [
            {
                'slide_number': 1,
                'header': 'Complete Header.',
                'body': 'This is complete.',
                'notes': 'These notes are complete.'
            },
            {
                'slide_number': 2,
                'header': 'Also Complete.',
                'body': 'Body text here.',
                'notes': 'Notes here too.'
            }
        ]
        result = check_sentence_completeness(slides)
        assert result['valid'] == True

    def test_check_sentence_completeness_with_issues(self):
        """Test detection of issues across slides."""
        slides = [
            {
                'slide_number': 1,
                'header': 'Header',  # Missing punctuation
                'body': 'Body text...',  # Trailing ellipsis
                'notes': 'Notes here.'
            }
        ]
        result = check_sentence_completeness(slides)
        assert result['valid'] == False
        assert result['total_issues'] >= 1

    def test_auto_fix_truncations_ellipsis(self):
        """Test auto-fix removes ellipsis."""
        text = "This ends with..."
        fixed, fixes = auto_fix_truncations(text)
        assert fixed == "This ends with."
        assert len(fixes) > 0

    def test_auto_fix_truncations_comma(self):
        """Test auto-fix replaces trailing comma."""
        text = "This ends with,"
        fixed, fixes = auto_fix_truncations(text)
        assert fixed == "This ends with."

    def test_auto_fix_adds_period(self):
        """Test auto-fix adds missing period."""
        text = "No punctuation here"
        fixed, fixes = auto_fix_truncations(text)
        assert fixed.endswith(".")

    def test_fix_slide_truncations(self):
        """Test fixing truncations in a slide."""
        slide = {
            'header': 'Header...',
            'body': 'Body text,',
            'notes': 'Complete notes.'
        }
        fixed, fixes = fix_slide_truncations(slide)
        assert fixed['header'] == 'Header.'
        assert fixed['body'] == 'Body text.'
        assert len(fixes) >= 2

    def test_terminal_punctuation_defined(self):
        """Test terminal punctuation is defined."""
        assert '.' in TERMINAL_PUNCTUATION
        assert '!' in TERMINAL_PUNCTUATION
        assert '?' in TERMINAL_PUNCTUATION
        assert ':' in TERMINAL_PUNCTUATION


# =============================================================================
# INTEGRATION TESTS
# =============================================================================

class TestValidationIntegration:
    """Integration tests for validation skills working together."""

    def test_complete_slide_validation(self):
        """Test validating a complete slide through all validators."""
        # Create a slide with proper content
        notes = " ".join(["word"] * 175) + ". Complete sentence."
        slide = {
            'slide_number': 1,
            'type': 'content',
            'header': 'Test Header.',
            'body': 'Test body content.',
            'notes': notes
        }

        # Word count check
        word_result = analyze_slide_word_count(notes, 'content')

        # Duration check
        duration_result = estimate_slide_duration(notes, 'content')

        # Completeness check
        completeness_result = check_sentence_completeness([slide])

        # All should pass
        assert word_result['word_count'] > 100
        assert duration_result['total_minutes'] > 0
        assert completeness_result['valid'] == True

    def test_presentation_level_validation(self):
        """Test validating an entire presentation."""
        # Create 12 content slides
        slides = []
        for i in range(1, 13):
            notes = " ".join(["word"] * 175) + f". Slide {i} content."
            slides.append({
                'slide_number': i,
                'type': 'content',
                'header': f'Slide {i} Header.',
                'body': f'Slide {i} body.',
                'notes': notes
            })

        # Validate word counts
        word_result = validate_word_counts(slides)

        # Validate timing
        timing_result = validate_timing(slides)

        # Validate completeness
        complete_result = check_sentence_completeness(slides)

        # Check results
        assert word_result['total_word_count'] > 2000
        assert timing_result['duration_minutes'] > 10


# =============================================================================
# RUN TESTS
# =============================================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
