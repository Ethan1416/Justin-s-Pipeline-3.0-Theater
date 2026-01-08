"""
Unit tests for Smart Retry Controller.

Tests cover:
- Basic retry execution
- Context tracking and persistence
- Strategy determination
- Incremental scoring
- Termination conditions
- Slide locking
"""

import pytest
import sys
import json
import shutil
from pathlib import Path
from typing import Dict, Any, Tuple, List

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from skills.utilities.smart_retry_controller import (
    SmartRetryController,
    IncrementalScorer,
    RetryStrategy,
    TerminationReason,
    RetryResult,
    RetryContext,
    RetryIteration,
    create_retry_controller,
    execute_step_with_retry
)


# =============================================================================
# TEST FIXTURES
# =============================================================================

@pytest.fixture
def controller():
    """Create a controller with test output directory."""
    return SmartRetryController(output_dir="outputs/test_retry")


@pytest.fixture
def mock_slides():
    """Sample slides for testing."""
    return [
        {'slide_number': i, 'header': f'Slide {i}', 'body': f'Content for slide {i}'}
        for i in range(1, 11)
    ]


@pytest.fixture
def cleanup():
    """Cleanup test outputs after tests."""
    yield
    shutil.rmtree("outputs/test_retry", ignore_errors=True)


# =============================================================================
# MOCK FUNCTIONS FOR TESTING
# =============================================================================

class MockExecutor:
    """Mock executor that simulates improving scores."""

    def __init__(self, base_score: float = 70, improvement: float = 8):
        self.iteration = 0
        self.base_score = base_score
        self.improvement = improvement

    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        self.iteration += 1
        return {
            'slides': [
                {'slide_number': i, 'header': f'Slide {i}'}
                for i in range(1, 11)
            ],
            'iteration': self.iteration,
            'base_score': min(self.base_score + (self.iteration * self.improvement), 100)
        }

    def validate(self, output: Dict[str, Any]) -> Tuple[float, Dict[str, Any]]:
        score = output.get('base_score', 0)
        failing_cats = []
        failing_slides = []

        if score < 80:
            failing_cats.append('char_limits')
            failing_slides = [1, 3, 5]
        if score < 85:
            failing_cats.append('markers')
            failing_slides.extend([2, 4])
        if score < 90:
            failing_cats.append('nclex_tip')

        return score, {
            'category_scores': {
                'char_limits': {'raw_score': min(score + 5, 100)},
                'markers': {'raw_score': min(score, 100)},
                'nclex_tip': {'raw_score': min(score - 2, 100)}
            },
            'failing_slides': list(set(failing_slides)),
            'issues': [{'slide_number': s} for s in failing_slides]
        }


class FailingExecutor:
    """Mock executor that always fails to improve."""

    def __init__(self, fixed_score: float = 75):
        self.fixed_score = fixed_score

    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        return {
            'slides': [{'slide_number': i} for i in range(1, 11)],
            'base_score': self.fixed_score
        }

    def validate(self, output: Dict[str, Any]) -> Tuple[float, Dict[str, Any]]:
        return self.fixed_score, {
            'category_scores': {'char_limits': {'raw_score': 70}},
            'failing_slides': [1, 2, 3],
            'issues': []
        }


# =============================================================================
# BASIC RETRY EXECUTION TESTS
# =============================================================================

class TestBasicRetryExecution:
    """Tests for basic retry execution flow."""

    def test_successful_retry_reaches_target(self, controller, cleanup):
        """Test that retry succeeds when score reaches target."""
        executor = MockExecutor(base_score=70, improvement=10)

        result = controller.execute_with_retry(
            step=8,
            execute_fn=executor.execute,
            validate_fn=executor.validate,
            initial_input={'blueprint': {}},
            target_score=90.0,
            max_iterations=3
        )

        assert result.success is True
        assert result.final_score >= 90.0
        assert result.termination_reason == TerminationReason.SUCCESS

    def test_retry_respects_max_iterations(self, controller, cleanup):
        """Test that retry stops at max iterations."""
        executor = MockExecutor(base_score=70, improvement=5)

        result = controller.execute_with_retry(
            step=8,
            execute_fn=executor.execute,
            validate_fn=executor.validate,
            initial_input={'blueprint': {}},
            target_score=95.0,  # Unreachable with improvement=5
            max_iterations=3
        )

        assert result.success is False
        assert result.iterations_used == 3
        assert result.termination_reason == TerminationReason.MAX_ITERATIONS

    def test_retry_stops_when_no_improvement(self, controller, cleanup):
        """Test that retry stops when scores plateau."""
        executor = FailingExecutor(fixed_score=75)

        result = controller.execute_with_retry(
            step=8,
            execute_fn=executor.execute,
            validate_fn=executor.validate,
            initial_input={'blueprint': {}},
            target_score=90.0,
            max_iterations=5
        )

        assert result.success is False
        assert result.termination_reason == TerminationReason.NO_IMPROVEMENT

    def test_retry_returns_final_blueprint(self, controller, cleanup):
        """Test that final blueprint is returned."""
        executor = MockExecutor(base_score=85, improvement=10)

        result = controller.execute_with_retry(
            step=8,
            execute_fn=executor.execute,
            validate_fn=executor.validate,
            initial_input={'blueprint': {}},
            target_score=90.0,
            max_iterations=3
        )

        assert result.final_blueprint is not None
        assert 'slides' in result.final_blueprint


# =============================================================================
# CONTEXT TRACKING TESTS
# =============================================================================

class TestContextTracking:
    """Tests for retry context tracking."""

    def test_context_tracks_iterations(self, controller, cleanup):
        """Test that context tracks all iterations."""
        executor = MockExecutor(base_score=80, improvement=5)

        result = controller.execute_with_retry(
            step=8,
            execute_fn=executor.execute,
            validate_fn=executor.validate,
            initial_input={'blueprint': {}},
            target_score=90.0,
            max_iterations=3
        )

        assert result.context is not None
        assert len(result.context.iterations) == result.iterations_used

    def test_context_tracks_score_trajectory(self, controller, cleanup):
        """Test score trajectory tracking."""
        executor = MockExecutor(base_score=70, improvement=8)

        result = controller.execute_with_retry(
            step=8,
            execute_fn=executor.execute,
            validate_fn=executor.validate,
            initial_input={'blueprint': {}},
            target_score=90.0,
            max_iterations=3
        )

        trajectory = result.context.get_score_trajectory()
        assert len(trajectory) > 0
        # Scores should be increasing
        for i in range(1, len(trajectory)):
            assert trajectory[i] > trajectory[i-1]

    def test_context_tracks_failing_categories(self, controller, cleanup):
        """Test failing category tracking."""
        executor = MockExecutor(base_score=75, improvement=5)

        result = controller.execute_with_retry(
            step=8,
            execute_fn=executor.execute,
            validate_fn=executor.validate,
            initial_input={'blueprint': {}},
            target_score=90.0,
            max_iterations=2
        )

        assert result.context.failing_categories is not None

    def test_context_serialization(self, controller, cleanup):
        """Test context can be serialized to dict."""
        executor = MockExecutor(base_score=85, improvement=10)

        result = controller.execute_with_retry(
            step=8,
            execute_fn=executor.execute,
            validate_fn=executor.validate,
            initial_input={'blueprint': {}},
            target_score=90.0,
            max_iterations=2
        )

        context_dict = result.context.to_dict()
        assert 'step' in context_dict
        assert 'iterations' in context_dict
        assert 'locked_slides' in context_dict


# =============================================================================
# STRATEGY DETERMINATION TESTS
# =============================================================================

class TestStrategyDetermination:
    """Tests for retry strategy selection."""

    def test_incremental_fix_for_char_limits(self, controller):
        """Test that char_limits gets incremental fix strategy."""
        strategy = controller._determine_strategy(['char_limits', 'markers'])
        assert strategy == RetryStrategy.INCREMENTAL_FIX

    def test_full_reprocess_for_anchor_coverage(self, controller):
        """Test that anchor_coverage triggers full reprocess."""
        strategy = controller._determine_strategy(['anchor_coverage', 'char_limits'])
        assert strategy == RetryStrategy.FULL_REPROCESS

    def test_targeted_for_mixed_categories(self, controller):
        """Test targeted reprocess for mixed categories."""
        strategy = controller._determine_strategy(['nclex_tip', 'vignette_structure'])
        assert strategy == RetryStrategy.TARGETED_REPROCESS

    def test_targeted_for_empty_categories(self, controller):
        """Test default strategy for no failing categories."""
        strategy = controller._determine_strategy([])
        assert strategy == RetryStrategy.TARGETED_REPROCESS


# =============================================================================
# SLIDE LOCKING TESTS
# =============================================================================

class TestSlideLocking:
    """Tests for slide locking functionality."""

    def test_passing_slides_get_locked(self, controller, cleanup):
        """Test that passing slides are locked after iteration."""
        executor = MockExecutor(base_score=80, improvement=5)

        result = controller.execute_with_retry(
            step=8,
            execute_fn=executor.execute,
            validate_fn=executor.validate,
            initial_input={'blueprint': {}},
            target_score=90.0,
            max_iterations=3
        )

        # Should have some locked slides
        assert len(result.context.locked_slides) > 0

    def test_locked_slides_persist_across_iterations(self, controller, cleanup):
        """Test that locked slides aren't unlocked."""
        executor = MockExecutor(base_score=75, improvement=8)

        result = controller.execute_with_retry(
            step=8,
            execute_fn=executor.execute,
            validate_fn=executor.validate,
            initial_input={'blueprint': {}},
            target_score=90.0,
            max_iterations=3
        )

        # Check that locked slides only grow across iterations
        if len(result.context.iterations) >= 2:
            iter1_locked = set(result.context.iterations[0].locked_slides)
            iter2_locked = set(result.context.iterations[-1].locked_slides)
            # Later iterations should have at least as many locked slides
            assert len(iter2_locked) >= len(iter1_locked)


# =============================================================================
# INCREMENTAL SCORING TESTS
# =============================================================================

class TestIncrementalScoring:
    """Tests for incremental scoring functionality."""

    def test_cache_stores_results(self):
        """Test that scorer caches validation results."""
        scorer = IncrementalScorer()

        slide = {'slide_number': 1, 'header': 'Test', 'body': 'Content'}
        result = {'score': 85, 'valid': True}

        scorer.cache_result(slide, result)
        cached = scorer.get_cached_result(slide)

        assert cached == result

    def test_cache_invalidation(self):
        """Test cache invalidation by slide number."""
        scorer = IncrementalScorer()

        slide = {'slide_number': 1, 'header': 'Test', 'body': 'Content'}
        scorer.cache_result(slide, {'score': 85})

        scorer.invalidate(1)
        cached = scorer.get_cached_result(slide)

        assert cached is None

    def test_incremental_scoring_uses_cache(self):
        """Test that incremental scoring uses cached results."""
        scorer = IncrementalScorer()

        slides = [
            {'slide_number': 1, 'header': 'Test 1', 'body': 'Content 1'},
            {'slide_number': 2, 'header': 'Test 2', 'body': 'Content 2'},
        ]

        validation_count = [0]

        def validate_slide(slide):
            validation_count[0] += 1
            return {'score': 85, 'slide_number': slide['slide_number']}

        # First pass - both slides validated
        score, details = scorer.score_incrementally(
            slides=slides,
            locked_slides=set(),
            validate_slide_fn=validate_slide
        )
        assert details['slides_validated'] == 2
        assert details['slides_from_cache'] == 0

        # Second pass with slide 1 locked - should use cache
        score, details = scorer.score_incrementally(
            slides=slides,
            locked_slides={1},
            validate_slide_fn=validate_slide
        )
        assert details['slides_from_cache'] == 1

    def test_incremental_scoring_average(self):
        """Test that incremental scoring computes correct average."""
        scorer = IncrementalScorer()

        slides = [
            {'slide_number': 1, 'header': 'Test 1', 'body': 'A'},
            {'slide_number': 2, 'header': 'Test 2', 'body': 'B'},
        ]

        def validate_slide(slide):
            # Slide 1 gets 80, slide 2 gets 100
            score = 80 if slide['slide_number'] == 1 else 100
            return {'score': score}

        score, _ = scorer.score_incrementally(
            slides=slides,
            locked_slides=set(),
            validate_slide_fn=validate_slide
        )

        assert score == 90.0  # Average of 80 and 100


# =============================================================================
# CATEGORY GUIDANCE TESTS
# =============================================================================

class TestCategoryGuidance:
    """Tests for category-specific guidance generation."""

    def test_guidance_for_char_limits(self, controller):
        """Test guidance generated for char_limits."""
        guidance = controller._get_category_guidance(['char_limits'])
        assert 'char_limits' in guidance
        assert '66' in guidance['char_limits']  # Character limit mentioned

    def test_guidance_for_multiple_categories(self, controller):
        """Test guidance for multiple failing categories."""
        guidance = controller._get_category_guidance(['char_limits', 'markers', 'nclex_tip'])
        assert len(guidance) == 3
        assert all(k in guidance for k in ['char_limits', 'markers', 'nclex_tip'])

    def test_guidance_includes_actionable_info(self, controller):
        """Test that guidance includes actionable information."""
        guidance = controller._get_category_guidance(['markers'])
        assert '[PAUSE]' in guidance['markers'] or 'markers' in guidance['markers'].lower()


# =============================================================================
# TERMINATION CONDITION TESTS
# =============================================================================

class TestTerminationConditions:
    """Tests for retry termination logic."""

    def test_success_terminates_loop(self, controller, cleanup):
        """Test that hitting target score terminates successfully."""
        executor = MockExecutor(base_score=90, improvement=0)

        result = controller.execute_with_retry(
            step=8,
            execute_fn=executor.execute,
            validate_fn=executor.validate,
            initial_input={},
            target_score=90.0,
            max_iterations=5
        )

        assert result.iterations_used == 1
        assert result.termination_reason == TerminationReason.SUCCESS

    def test_improvement_rate_triggers_early_stop(self, controller, cleanup):
        """Test that low improvement rate causes early termination."""
        # Executor that improves very slowly
        executor = MockExecutor(base_score=75, improvement=1)

        result = controller.execute_with_retry(
            step=8,
            execute_fn=executor.execute,
            validate_fn=executor.validate,
            initial_input={},
            target_score=95.0,
            max_iterations=10
        )

        # Should stop before max iterations due to low improvement
        assert result.iterations_used < 10


# =============================================================================
# RETRY LOG TESTS
# =============================================================================

class TestRetryLogging:
    """Tests for retry log generation."""

    def test_retry_log_created(self, controller, cleanup):
        """Test that retry log file is created."""
        executor = MockExecutor(base_score=85, improvement=5)

        controller.execute_with_retry(
            step=8,
            execute_fn=executor.execute,
            validate_fn=executor.validate,
            initial_input={},
            target_score=90.0,
            max_iterations=2
        )

        log_files = list(Path("outputs/test_retry").glob("retry_step8_*.json"))
        assert len(log_files) >= 1

    def test_retry_log_contains_summary(self, controller, cleanup):
        """Test that retry log contains summary information."""
        executor = MockExecutor(base_score=85, improvement=5)

        controller.execute_with_retry(
            step=8,
            execute_fn=executor.execute,
            validate_fn=executor.validate,
            initial_input={},
            target_score=90.0,
            max_iterations=2
        )

        log_files = list(Path("outputs/test_retry").glob("retry_step8_*.json"))
        with open(log_files[0]) as f:
            log_data = json.load(f)

        assert 'summary' in log_data
        assert 'iterations_used' in log_data['summary']
        assert 'score_trajectory' in log_data['summary']


# =============================================================================
# CALLBACK TESTS
# =============================================================================

class TestCallbacks:
    """Tests for iteration callbacks."""

    def test_callback_called_each_iteration(self, controller, cleanup):
        """Test that callback is called for each iteration."""
        executor = MockExecutor(base_score=70, improvement=10)
        iterations_seen = []

        def on_iteration(iteration: RetryIteration):
            iterations_seen.append(iteration.iteration)

        result = controller.execute_with_retry(
            step=8,
            execute_fn=executor.execute,
            validate_fn=executor.validate,
            initial_input={},
            target_score=90.0,
            max_iterations=3,
            on_iteration=on_iteration
        )

        assert len(iterations_seen) == result.iterations_used


# =============================================================================
# CONVENIENCE FUNCTION TESTS
# =============================================================================

class TestConvenienceFunctions:
    """Tests for module-level convenience functions."""

    def test_create_retry_controller(self, cleanup):
        """Test controller factory function."""
        controller = create_retry_controller("outputs/test_retry")
        assert controller is not None
        assert isinstance(controller, SmartRetryController)

    def test_execute_step_with_retry(self, cleanup):
        """Test convenience execution function."""
        executor = MockExecutor(base_score=85, improvement=10)

        result = execute_step_with_retry(
            step=8,
            execute_fn=executor.execute,
            validate_fn=executor.validate,
            initial_input={},
            target_score=90.0,
            max_iterations=2
        )

        assert result is not None
        assert isinstance(result, RetryResult)


# =============================================================================
# EDGE CASE TESTS
# =============================================================================

class TestEdgeCases:
    """Tests for edge cases and error handling."""

    def test_handles_exception_in_execute(self, controller, cleanup):
        """Test handling of exceptions during execution."""
        def failing_execute(input_data):
            raise ValueError("Test error")

        def dummy_validate(output):
            return 0, {}

        result = controller.execute_with_retry(
            step=8,
            execute_fn=failing_execute,
            validate_fn=dummy_validate,
            initial_input={},
            target_score=90.0,
            max_iterations=3
        )

        assert result.success is False
        assert result.termination_reason == TerminationReason.CRITICAL_ERROR
        assert "Test error" in result.error_message

    def test_handles_empty_slides(self, controller, cleanup):
        """Test handling of empty slides list."""
        def empty_execute(input_data):
            return {'slides': [], 'base_score': 95}

        def validate(output):
            return 95, {'category_scores': {}, 'failing_slides': [], 'issues': []}

        result = controller.execute_with_retry(
            step=8,
            execute_fn=empty_execute,
            validate_fn=validate,
            initial_input={},
            target_score=90.0,
            max_iterations=2
        )

        assert result.success is True

    def test_first_iteration_succeeds(self, controller, cleanup):
        """Test when first iteration already meets target."""
        executor = MockExecutor(base_score=95, improvement=0)

        result = controller.execute_with_retry(
            step=8,
            execute_fn=executor.execute,
            validate_fn=executor.validate,
            initial_input={},
            target_score=90.0,
            max_iterations=5
        )

        assert result.success is True
        assert result.iterations_used == 1


# =============================================================================
# RUN TESTS
# =============================================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
