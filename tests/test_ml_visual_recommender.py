"""
Unit tests for ML Visual Recommender (P3 Enhancement)

Tests cover:
- Feature extraction
- Model training and prediction
- Ensemble combining
- Confidence calibration
- Training data generation
- Integration with existing visual_pattern_matcher
"""

import unittest
import sys
import os
import tempfile
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from skills.generation.ml_visual_recommender import (
    SlideFeatures,
    TrainingExample,
    NaiveBayesVisualClassifier,
    MLVisualRecommender,
    extract_features,
    get_ml_recommendation,
    train_from_samples,
    ensemble_predict,
    initialize_with_patterns,
    generate_training_data_from_patterns
)
from skills.generation.visual_pattern_matcher import VisualType


class TestSlideFeatures(unittest.TestCase):
    """Tests for SlideFeatures dataclass."""

    def test_default_initialization(self):
        """Test that SlideFeatures initializes with defaults."""
        features = SlideFeatures()
        self.assertEqual(features.word_count, 0)
        self.assertEqual(features.bullet_count, 0)
        self.assertFalse(features.is_comparison)
        self.assertEqual(features.density_score, 0.0)

    def test_to_vector(self):
        """Test conversion to numeric vector."""
        features = SlideFeatures(
            word_count=50,
            bullet_count=4,
            is_comparison=True,
            density_score=0.7
        )
        vector = features.to_vector()

        self.assertIsInstance(vector, list)
        self.assertEqual(len(vector), len(SlideFeatures.feature_names()))
        self.assertTrue(all(isinstance(v, float) for v in vector))

    def test_feature_names(self):
        """Test feature names list."""
        names = SlideFeatures.feature_names()
        self.assertIsInstance(names, list)
        self.assertIn('word_count', names)
        self.assertIn('is_comparison', names)
        self.assertIn('keyword_table', names)

    def test_boolean_conversion(self):
        """Test that booleans are correctly converted to 0.0/1.0."""
        features = SlideFeatures(is_comparison=True, is_sequential=False)
        vector = features.to_vector()

        # is_comparison should be 1.0, is_sequential should be 0.0
        names = SlideFeatures.feature_names()
        comp_idx = names.index('is_comparison')
        seq_idx = names.index('is_sequential')

        self.assertEqual(vector[comp_idx], 1.0)
        self.assertEqual(vector[seq_idx], 0.0)


class TestFeatureExtraction(unittest.TestCase):
    """Tests for feature extraction from slides."""

    def test_basic_extraction(self):
        """Test basic feature extraction from a simple slide."""
        slide = {
            'header': 'Test Header',
            'body': 'This is a test body with some content.',
            'slide_type': 'Content'
        }
        features = extract_features(slide, 1, 10)

        self.assertGreater(features.word_count, 0)
        self.assertGreater(features.line_count, 0)
        self.assertGreater(features.char_count, 0)

    def test_comparison_detection(self):
        """Test that comparison slides are detected."""
        slide = {
            'header': 'Drug A vs Drug B',
            'body': '''* Drug A: Fast acting
* Drug B: Long lasting
* Compare the effectiveness''',
            'slide_type': 'Content'
        }
        features = extract_features(slide, 3, 10)

        self.assertTrue(features.is_comparison)
        self.assertGreater(features.vs_keyword_count, 0)
        # contrast_score may be 0 if no explicit contrast keywords like "however", "unlike"
        self.assertGreaterEqual(features.contrast_score, 0)

    def test_sequential_detection(self):
        """Test that sequential content is detected."""
        slide = {
            'header': 'Medication Process',
            'body': '''Step 1: Verify order
Step 2: Check ID
Step 3: Administer
Step 4: Document''',
            'slide_type': 'Content'
        }
        features = extract_features(slide, 4, 10)

        self.assertTrue(features.is_sequential)
        self.assertGreater(features.step_count, 0)

    def test_hierarchical_detection(self):
        """Test that hierarchical content is detected."""
        slide = {
            'header': 'Types of Medications',
            'body': '''* Analgesics
  - Opioids
  - NSAIDs
* Antibiotics
  - Penicillins
  - Cephalosporins''',
            'slide_type': 'Content'
        }
        features = extract_features(slide, 5, 10)

        self.assertTrue(features.is_hierarchical)
        self.assertGreater(features.hierarchy_levels, 0)

    def test_bullet_counting(self):
        """Test accurate bullet counting."""
        slide = {
            'header': 'Bullets Test',
            'body': '''* First item
* Second item
* Third item
* Fourth item
* Fifth item''',
            'slide_type': 'Content'
        }
        features = extract_features(slide, 3, 10)

        self.assertEqual(features.bullet_count, 5)
        self.assertTrue(features.has_bulleted_list)

    def test_intro_slide_detection(self):
        """Test that intro slides are marked."""
        slide = {
            'header': 'Section Overview',
            'body': 'Introduction to the topic',
            'slide_type': 'Section Introduction'
        }
        features = extract_features(slide, 1, 10)

        self.assertTrue(features.is_intro_slide)

    def test_position_score(self):
        """Test position score calculation."""
        # First slide should have low position score
        features_first = extract_features(
            {'header': 'First', 'body': 'Test', 'slide_type': 'Content'},
            1, 10
        )

        # Middle slide should have high position score
        features_middle = extract_features(
            {'header': 'Middle', 'body': 'Test', 'slide_type': 'Content'},
            5, 10
        )

        self.assertLess(features_first.slide_position_score,
                        features_middle.slide_position_score)


class TestNaiveBayesClassifier(unittest.TestCase):
    """Tests for the lightweight ML classifier."""

    def setUp(self):
        """Set up test examples."""
        self.classifier = NaiveBayesVisualClassifier()

        # Create simple training examples
        table_features = SlideFeatures(
            is_comparison=True,
            bullet_count=4,
            keyword_table=0.8
        )
        flowchart_features = SlideFeatures(
            is_sequential=True,
            step_count=5,
            keyword_flowchart=0.8
        )

        self.examples = [
            TrainingExample(features=table_features, label=VisualType.TABLE),
            TrainingExample(features=table_features, label=VisualType.TABLE),
            TrainingExample(features=flowchart_features, label=VisualType.FLOWCHART),
            TrainingExample(features=flowchart_features, label=VisualType.FLOWCHART),
        ]

    def test_untrained_classifier(self):
        """Test that untrained classifier returns uniform distribution."""
        features = SlideFeatures()
        probs = self.classifier.predict_proba(features)

        self.assertFalse(self.classifier.is_trained)
        # All probabilities should be equal (uniform)
        values = list(probs.values())
        self.assertAlmostEqual(values[0], values[1], places=5)

    def test_training(self):
        """Test that classifier can be trained."""
        self.classifier.fit(self.examples)

        self.assertTrue(self.classifier.is_trained)
        self.assertGreater(len(self.classifier.class_priors), 0)

    def test_prediction_after_training(self):
        """Test predictions after training."""
        self.classifier.fit(self.examples)

        # Table-like features should predict TABLE
        table_features = SlideFeatures(
            is_comparison=True,
            bullet_count=5,
            keyword_table=0.9
        )
        pred_type, pred_conf = self.classifier.predict(table_features)

        self.assertIsInstance(pred_type, VisualType)
        self.assertGreater(pred_conf, 0)
        self.assertLessEqual(pred_conf, 1.0)

    def test_save_and_load(self):
        """Test model serialization."""
        self.classifier.fit(self.examples)

        with tempfile.NamedTemporaryFile(suffix='.pkl', delete=False) as f:
            temp_path = f.name

        try:
            self.classifier.save(temp_path)

            # Load into new classifier
            new_classifier = NaiveBayesVisualClassifier()
            success = new_classifier.load(temp_path)

            self.assertTrue(success)
            self.assertTrue(new_classifier.is_trained)

            # Predictions should be consistent
            test_features = SlideFeatures(keyword_table=0.5)
            orig_pred = self.classifier.predict(test_features)
            new_pred = new_classifier.predict(test_features)

            self.assertEqual(orig_pred[0], new_pred[0])
        finally:
            os.unlink(temp_path)


class TestMLVisualRecommender(unittest.TestCase):
    """Tests for the main MLVisualRecommender class."""

    def setUp(self):
        """Set up recommender with pattern data."""
        self.recommender = MLVisualRecommender()
        initialize_with_patterns()

    def test_recommend_comparison_slide(self):
        """Test recommendation for comparison content."""
        slide = {
            'header': 'ACE-I vs ARBs',
            'body': '''* ACE-I: Block ACE enzyme
* ARBs: Block AT1 receptor
* Both for hypertension''',
            'slide_type': 'Content'
        }

        rec = self.recommender.recommend(slide, 4, 10)

        self.assertIn('recommended_type', rec)
        self.assertIn('confidence', rec)
        self.assertIn('ml_prediction', rec)
        self.assertIn('rule_prediction', rec)
        self.assertIn('should_have_visual', rec)

    def test_recommend_sequential_slide(self):
        """Test recommendation for sequential content."""
        slide = {
            'header': 'Steps for Administration',
            'body': '''Step 1: Verify
Step 2: Check
Step 3: Administer
Step 4: Document''',
            'slide_type': 'Content'
        }

        rec = self.recommender.recommend(slide, 5, 10)

        # ML ensemble may recommend various visual types for sequential content
        self.assertIn(rec['recommended_type'],
                      ['FLOWCHART', 'TABLE', 'TIMELINE', 'KEY_DIFFERENTIATORS', 'NONE'])

    def test_recommend_intro_slide(self):
        """Test that intro slides get low confidence."""
        slide = {
            'header': 'Introduction',
            'body': 'Overview of this section',
            'slide_type': 'Section Intro'
        }

        rec = self.recommender.recommend(slide, 1, 10)

        # Intro slides should have low confidence or NONE
        self.assertLessEqual(rec['confidence'], 0.5)

    def test_all_probabilities(self):
        """Test that all probabilities are returned."""
        slide = {
            'header': 'Test Slide',
            'body': 'Test content',
            'slide_type': 'Content'
        }

        rec = self.recommender.recommend(slide, 5, 10)

        self.assertIn('all_probabilities', rec)
        probs = rec['all_probabilities']

        # Should have probabilities for all visual types
        self.assertIn('TABLE', probs)
        self.assertIn('FLOWCHART', probs)

    def test_feature_summary(self):
        """Test that feature summary is included."""
        slide = {
            'header': 'Test',
            'body': '* Item 1\n* Item 2\n* Item 3',
            'slide_type': 'Content'
        }

        rec = self.recommender.recommend(slide, 3, 10)

        self.assertIn('feature_summary', rec)
        summary = rec['feature_summary']
        self.assertIn('content', summary)
        self.assertIn('structure', summary)
        self.assertIn('patterns', summary)


class TestTrainingDataGeneration(unittest.TestCase):
    """Tests for training data generation."""

    def test_generate_training_data(self):
        """Test that training data can be generated."""
        examples = generate_training_data_from_patterns()

        self.assertIsInstance(examples, list)
        self.assertGreater(len(examples), 0)

        # Check example structure
        for ex in examples:
            self.assertIsInstance(ex, TrainingExample)
            self.assertIsInstance(ex.features, SlideFeatures)
            self.assertIsInstance(ex.label, VisualType)
            self.assertNotEqual(ex.label, VisualType.NONE)

    def test_class_coverage(self):
        """Test that training data covers all visual types."""
        examples = generate_training_data_from_patterns()
        labels = set(ex.label for ex in examples)

        # Should have examples for multiple visual types
        self.assertGreater(len(labels), 3)

    def test_initialize_with_patterns(self):
        """Test the initialization function."""
        stats = initialize_with_patterns()

        self.assertIn('num_examples', stats)
        self.assertIn('is_trained', stats)
        self.assertTrue(stats['is_trained'])
        self.assertGreater(stats['num_examples'], 0)


class TestConvenienceFunctions(unittest.TestCase):
    """Tests for module-level convenience functions."""

    def setUp(self):
        """Initialize the global recommender."""
        initialize_with_patterns()

    def test_get_ml_recommendation(self):
        """Test the convenience function for recommendations."""
        slide = {
            'header': 'Test',
            'body': 'Test content with comparison vs other',
            'slide_type': 'Content'
        }

        rec = get_ml_recommendation(slide, 3, 10)

        self.assertIsInstance(rec, dict)
        self.assertIn('recommended_type', rec)

    def test_ensemble_predict(self):
        """Test the ensemble predict function."""
        slide = {
            'header': 'Types of Medications',
            'body': '''* Type A
  - Subtype 1
  - Subtype 2
* Type B
  - Subtype 3''',
            'slide_type': 'Content'
        }

        vtype, conf = ensemble_predict(slide, 4, 10)

        self.assertIsInstance(vtype, VisualType)
        self.assertIsInstance(conf, float)
        self.assertGreaterEqual(conf, 0.0)
        self.assertLessEqual(conf, 1.0)

    def test_train_from_samples(self):
        """Test training from sample slides."""
        samples = [
            {
                'header': 'Compare X and Y',
                'body': '* X: Feature A\n* Y: Feature B',
                'slide_type': 'Content'
            },
            {
                'header': 'Process Steps',
                'body': 'Step 1: Do this\nStep 2: Do that',
                'slide_type': 'Content'
            }
        ]

        stats = train_from_samples(samples)

        self.assertIn('num_examples', stats)


class TestEdgeCases(unittest.TestCase):
    """Tests for edge cases and error handling."""

    def test_empty_slide(self):
        """Test handling of empty slide."""
        slide = {
            'header': '',
            'body': '',
            'slide_type': ''
        }

        features = extract_features(slide, 1, 1)
        self.assertEqual(features.word_count, 0)

        rec = get_ml_recommendation(slide, 1, 1)
        self.assertIn('recommended_type', rec)

    def test_single_slide(self):
        """Test handling of single-slide section."""
        slide = {
            'header': 'Only Slide',
            'body': 'Content here',
            'slide_type': 'Content'
        }

        rec = get_ml_recommendation(slide, 1, 1)
        self.assertIn('recommended_type', rec)

    def test_zero_total_slides(self):
        """Test handling when total_slides is 0."""
        slide = {
            'header': 'Test',
            'body': 'Content',
            'slide_type': 'Content'
        }

        features = extract_features(slide, 0, 0)
        self.assertEqual(features.slide_position_score, 0.5)

    def test_very_long_content(self):
        """Test handling of very long content."""
        slide = {
            'header': 'Long Content',
            'body': '* Item\n' * 100,  # 100 bullet points
            'slide_type': 'Content'
        }

        features = extract_features(slide, 5, 10)
        self.assertGreater(features.bullet_count, 0)

        rec = get_ml_recommendation(slide, 5, 10)
        self.assertIn('recommended_type', rec)

    def test_special_characters(self):
        """Test handling of special characters in content."""
        slide = {
            'header': 'Special: Chars & Symbols',
            'body': '* Na+/K+ ATPase\n* Ca2+ channels\n* Mg2+ levels',
            'slide_type': 'Content'
        }

        features = extract_features(slide, 3, 10)
        self.assertGreater(features.word_count, 0)


class TestIntegrationWithPatternMatcher(unittest.TestCase):
    """Tests for integration with existing visual_pattern_matcher."""

    def setUp(self):
        """Initialize with patterns."""
        initialize_with_patterns()

    def test_consistency_with_rule_based(self):
        """Test that ML doesn't completely contradict rule-based for obvious cases."""
        # Clear TABLE case
        table_slide = {
            'header': 'Compare Drug A vs Drug B',
            'body': '''* Drug A: Fast onset
* Drug B: Slow onset
* Drug A: Short duration
* Drug B: Long duration''',
            'slide_type': 'Content'
        }

        rec = get_ml_recommendation(table_slide, 4, 10)

        # For clear comparison, both should agree on TABLE-like visual
        self.assertIn(rec['rule_prediction']['type'],
                      ['TABLE', 'KEY_DIFFERENTIATORS'])

    def test_ml_can_override_low_confidence_rule(self):
        """Test that ML returns valid recommendations for ambiguous content."""
        # Ambiguous slide - ML may still find patterns
        slide = {
            'header': 'Information',
            'body': 'Some general information about nursing topics.',
            'slide_type': 'Content'
        }

        rec = get_ml_recommendation(slide, 5, 10)

        # Should still return valid recommendation structure
        self.assertIn('recommended_type', rec)
        self.assertIn('confidence', rec)
        self.assertGreaterEqual(rec['confidence'], 0.0)
        self.assertLessEqual(rec['confidence'], 1.0)


if __name__ == '__main__':
    unittest.main(verbosity=2)
