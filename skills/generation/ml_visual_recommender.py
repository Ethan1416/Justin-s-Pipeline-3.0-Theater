"""
ML-Based Visual Type Recommender
Provides machine learning-enhanced visual type recommendations for NCLEX slides.

This module implements P3 enhancement from the diagnostic assessment:
- Feature extraction from slide content
- Lightweight ML model using scikit-learn compatible patterns
- Calibrated confidence scores
- Training data generation from historical patterns
- Seamless integration with existing visual_pattern_matcher

The ML approach supplements (not replaces) the rule-based system, providing
ensemble predictions that combine both methods.

Usage:
    from skills.generation.ml_visual_recommender import (
        MLVisualRecommender,
        extract_features,
        get_ml_recommendation,
        train_from_samples,
        ensemble_predict
    )
"""

import re
import json
import math
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass, field, asdict
from enum import Enum
from pathlib import Path
import pickle
from collections import Counter

# Import existing modules
from .visual_pattern_matcher import (
    VisualType,
    score_visual_opportunity_multifactor,
    get_all_visual_scores,
    NCLEX_DOMAIN_KEYWORDS
)
from .content_structure_analyzer import (
    count_bullet_points,
    detect_list_patterns,
    identify_comparison_structure,
    detect_sequential_markers,
    analyze_information_density,
    detect_hierarchical_structure
)


# =============================================================================
# FEATURE EXTRACTION
# =============================================================================

@dataclass
class SlideFeatures:
    """Feature vector for a slide, used as input to ML model."""

    # Basic content metrics (5 features)
    word_count: int = 0
    line_count: int = 0
    avg_words_per_line: float = 0.0
    char_count: int = 0
    unique_word_ratio: float = 0.0

    # Structure features (8 features)
    bullet_count: int = 0
    has_numbered_list: bool = False
    has_bulleted_list: bool = False
    list_depth: int = 0
    nested_item_count: int = 0
    colon_count: int = 0
    has_parallel_structure: bool = False
    structure_complexity: float = 0.0

    # Comparison features (5 features)
    is_comparison: bool = False
    comparison_item_count: int = 0
    is_binary_comparison: bool = False
    vs_keyword_count: int = 0
    contrast_score: float = 0.0

    # Sequential features (5 features)
    is_sequential: bool = False
    sequence_type_process: bool = False
    sequence_type_timeline: bool = False
    sequence_type_steps: bool = False
    step_count: int = 0

    # Hierarchical features (4 features)
    is_hierarchical: bool = False
    hierarchy_levels: int = 0
    has_root_concept: bool = False
    classification_score: float = 0.0

    # Density features (4 features)
    density_score: float = 0.0
    unique_concepts: int = 0
    information_richness: float = 0.0
    technical_term_density: float = 0.0

    # Domain features (6 features - one per NCLEX domain)
    domain_pharmacology: float = 0.0
    domain_medical_surgical: float = 0.0
    domain_fundamentals: float = 0.0
    domain_mental_health: float = 0.0
    domain_maternal_child: float = 0.0
    domain_max_score: float = 0.0

    # Visual keyword features (7 features - one per visual type)
    keyword_table: float = 0.0
    keyword_flowchart: float = 0.0
    keyword_decision_tree: float = 0.0
    keyword_timeline: float = 0.0
    keyword_hierarchy: float = 0.0
    keyword_spectrum: float = 0.0
    keyword_key_diff: float = 0.0

    # Slide context features (3 features)
    slide_position_score: float = 0.0
    is_intro_slide: bool = False
    is_summary_slide: bool = False

    def to_vector(self) -> List[float]:
        """Convert features to a numeric vector for ML model."""
        return [
            # Basic (5)
            float(self.word_count),
            float(self.line_count),
            self.avg_words_per_line,
            float(self.char_count),
            self.unique_word_ratio,
            # Structure (8)
            float(self.bullet_count),
            1.0 if self.has_numbered_list else 0.0,
            1.0 if self.has_bulleted_list else 0.0,
            float(self.list_depth),
            float(self.nested_item_count),
            float(self.colon_count),
            1.0 if self.has_parallel_structure else 0.0,
            self.structure_complexity,
            # Comparison (5)
            1.0 if self.is_comparison else 0.0,
            float(self.comparison_item_count),
            1.0 if self.is_binary_comparison else 0.0,
            float(self.vs_keyword_count),
            self.contrast_score,
            # Sequential (5)
            1.0 if self.is_sequential else 0.0,
            1.0 if self.sequence_type_process else 0.0,
            1.0 if self.sequence_type_timeline else 0.0,
            1.0 if self.sequence_type_steps else 0.0,
            float(self.step_count),
            # Hierarchical (4)
            1.0 if self.is_hierarchical else 0.0,
            float(self.hierarchy_levels),
            1.0 if self.has_root_concept else 0.0,
            self.classification_score,
            # Density (4)
            self.density_score,
            float(self.unique_concepts),
            self.information_richness,
            self.technical_term_density,
            # Domain (6)
            self.domain_pharmacology,
            self.domain_medical_surgical,
            self.domain_fundamentals,
            self.domain_mental_health,
            self.domain_maternal_child,
            self.domain_max_score,
            # Visual keywords (7)
            self.keyword_table,
            self.keyword_flowchart,
            self.keyword_decision_tree,
            self.keyword_timeline,
            self.keyword_hierarchy,
            self.keyword_spectrum,
            self.keyword_key_diff,
            # Context (3)
            self.slide_position_score,
            1.0 if self.is_intro_slide else 0.0,
            1.0 if self.is_summary_slide else 0.0,
        ]

    @classmethod
    def feature_names(cls) -> List[str]:
        """Get ordered list of feature names."""
        return [
            'word_count', 'line_count', 'avg_words_per_line', 'char_count', 'unique_word_ratio',
            'bullet_count', 'has_numbered_list', 'has_bulleted_list', 'list_depth',
            'nested_item_count', 'colon_count', 'has_parallel_structure', 'structure_complexity',
            'is_comparison', 'comparison_item_count', 'is_binary_comparison',
            'vs_keyword_count', 'contrast_score',
            'is_sequential', 'sequence_type_process', 'sequence_type_timeline',
            'sequence_type_steps', 'step_count',
            'is_hierarchical', 'hierarchy_levels', 'has_root_concept', 'classification_score',
            'density_score', 'unique_concepts', 'information_richness', 'technical_term_density',
            'domain_pharmacology', 'domain_medical_surgical', 'domain_fundamentals',
            'domain_mental_health', 'domain_maternal_child', 'domain_max_score',
            'keyword_table', 'keyword_flowchart', 'keyword_decision_tree',
            'keyword_timeline', 'keyword_hierarchy', 'keyword_spectrum', 'keyword_key_diff',
            'slide_position_score', 'is_intro_slide', 'is_summary_slide'
        ]


def extract_features(
    slide: Dict[str, Any],
    slide_number: int = 0,
    total_slides: int = 0
) -> SlideFeatures:
    """
    Extract comprehensive feature vector from slide content.

    Combines features from multiple analyzers to create a rich
    representation suitable for ML classification.

    Args:
        slide: Slide dictionary with header, body, slide_type
        slide_number: Position in section (1-indexed)
        total_slides: Total slides in section

    Returns:
        SlideFeatures dataclass with all extracted features
    """
    header = slide.get('header', '')
    body = slide.get('body', '')
    slide_type = slide.get('slide_type', '').lower()
    content = f"{header}\n{body}"
    content_lower = content.lower()

    features = SlideFeatures()

    # =========================
    # Basic Content Metrics
    # =========================
    words = re.findall(r'\b\w+\b', content)
    lines = [l for l in content.split('\n') if l.strip()]

    features.word_count = len(words)
    features.line_count = len(lines)
    features.avg_words_per_line = len(words) / max(1, len(lines))
    features.char_count = len(content)

    unique_words = set(w.lower() for w in words)
    features.unique_word_ratio = len(unique_words) / max(1, len(words))

    # =========================
    # Structure Features
    # =========================
    features.bullet_count = count_bullet_points(body)

    list_patterns = detect_list_patterns(body)
    features.has_numbered_list = list_patterns['has_numbered_list']
    features.has_bulleted_list = list_patterns['has_bulleted_list']
    features.list_depth = list_patterns['list_depth']

    # Nested items (items at depth > 1)
    if list_patterns['items_per_level']:
        features.nested_item_count = sum(list_patterns['items_per_level'][1:])

    features.colon_count = body.count(':')

    # Parallel structure detection (items with similar patterns)
    features.has_parallel_structure = _detect_parallel_structure(body)

    # Structure complexity score
    features.structure_complexity = _calculate_structure_complexity(
        features.bullet_count,
        features.list_depth,
        features.nested_item_count,
        features.colon_count
    )

    # =========================
    # Comparison Features
    # =========================
    comparison = identify_comparison_structure(body)
    features.is_comparison = comparison['is_comparison']
    features.comparison_item_count = len(comparison['comparison_items'])
    features.is_binary_comparison = comparison['comparison_type'] == 'binary'

    features.vs_keyword_count = len(re.findall(r'\bvs\.?\b|\bversus\b', content_lower))

    # Contrast score based on contrast keywords
    contrast_keywords = ['however', 'unlike', 'whereas', 'contrast', 'different']
    features.contrast_score = min(1.0, sum(1 for kw in contrast_keywords if kw in content_lower) / 3)

    # =========================
    # Sequential Features
    # =========================
    sequential = detect_sequential_markers(body)
    features.is_sequential = sequential['is_sequential']
    features.sequence_type_process = sequential['sequence_type'] == 'process'
    features.sequence_type_timeline = sequential['sequence_type'] == 'timeline'
    features.sequence_type_steps = sequential['sequence_type'] == 'steps'
    features.step_count = sequential['step_count']

    # =========================
    # Hierarchical Features
    # =========================
    hierarchical = detect_hierarchical_structure(body)
    features.is_hierarchical = hierarchical['is_hierarchical']
    features.hierarchy_levels = hierarchical['levels_detected']
    features.has_root_concept = hierarchical['root_concept'] is not None

    # Classification score based on classification keywords
    class_keywords = ['types of', 'categories', 'classification', 'classes', 'subdivided']
    features.classification_score = min(1.0, sum(1 for kw in class_keywords if kw in content_lower) / 2)

    # =========================
    # Density Features
    # =========================
    density = analyze_information_density(body)
    features.density_score = density['density_score']
    features.unique_concepts = density['unique_concepts']

    # Information richness (combination of concepts and density)
    features.information_richness = (features.density_score +
                                     min(1.0, features.unique_concepts / 8)) / 2

    # Technical term density
    features.technical_term_density = _calculate_technical_term_density(content)

    # =========================
    # Domain Features
    # =========================
    for domain, keywords in NCLEX_DOMAIN_KEYWORDS.items():
        domain_score = sum(1 for kw in keywords if kw in content_lower) / len(keywords)

        if domain == 'pharmacology':
            features.domain_pharmacology = domain_score
        elif domain == 'medical_surgical':
            features.domain_medical_surgical = domain_score
        elif domain == 'fundamentals':
            features.domain_fundamentals = domain_score
        elif domain == 'mental_health':
            features.domain_mental_health = domain_score
        elif domain == 'maternal_child':
            features.domain_maternal_child = domain_score

    features.domain_max_score = max(
        features.domain_pharmacology,
        features.domain_medical_surgical,
        features.domain_fundamentals,
        features.domain_mental_health,
        features.domain_maternal_child
    )

    # =========================
    # Visual Keyword Features
    # =========================
    keyword_scores = get_all_visual_scores(content)
    features.keyword_table = keyword_scores.get(VisualType.TABLE, 0.0)
    features.keyword_flowchart = keyword_scores.get(VisualType.FLOWCHART, 0.0)
    features.keyword_decision_tree = keyword_scores.get(VisualType.DECISION_TREE, 0.0)
    features.keyword_timeline = keyword_scores.get(VisualType.TIMELINE, 0.0)
    features.keyword_hierarchy = keyword_scores.get(VisualType.HIERARCHY, 0.0)
    features.keyword_spectrum = keyword_scores.get(VisualType.SPECTRUM, 0.0)
    features.keyword_key_diff = keyword_scores.get(VisualType.KEY_DIFFERENTIATORS, 0.0)

    # =========================
    # Slide Context Features
    # =========================
    if total_slides > 0:
        # Position score: middle slides get higher scores
        relative_pos = slide_number / total_slides
        if relative_pos < 0.2 or relative_pos > 0.9:
            features.slide_position_score = 0.3
        elif relative_pos < 0.35 or relative_pos > 0.75:
            features.slide_position_score = 0.6
        else:
            features.slide_position_score = 0.8
    else:
        features.slide_position_score = 0.5

    features.is_intro_slide = any(t in slide_type for t in ['intro', 'introduction', 'overview'])
    features.is_summary_slide = any(t in slide_type for t in ['summary', 'conclusion', 'review'])

    return features


def _detect_parallel_structure(body: str) -> bool:
    """Detect if body has parallel structure (similar patterns repeated)."""
    if not body:
        return False

    lines = [l.strip() for l in body.split('\n') if l.strip()]
    if len(lines) < 2:
        return False

    # Check for colon-based parallel structure (X: ... Y: ...)
    colon_lines = [l for l in lines if ':' in l]
    if len(colon_lines) >= 2:
        return True

    # Check for similar line starts (same first word pattern)
    first_words = [l.split()[0] if l.split() else '' for l in lines]
    word_counts = Counter(first_words)
    # If any first word appears 3+ times, it's parallel
    if any(c >= 3 for c in word_counts.values()):
        return True

    return False


def _calculate_structure_complexity(
    bullet_count: int,
    list_depth: int,
    nested_count: int,
    colon_count: int
) -> float:
    """Calculate overall structure complexity score (0-1)."""
    score = 0.0

    # Bullet complexity (more bullets = more structure)
    score += min(0.25, bullet_count * 0.05)

    # Depth complexity (deeper nesting = more complex)
    score += min(0.25, list_depth * 0.1)

    # Nested complexity
    score += min(0.25, nested_count * 0.05)

    # Colon complexity (structured key:value pairs)
    score += min(0.25, colon_count * 0.05)

    return min(1.0, score)


def _calculate_technical_term_density(content: str) -> float:
    """Calculate density of technical/medical terms in content."""
    if not content:
        return 0.0

    # Technical term indicators
    technical_patterns = [
        r'\b[A-Z]{2,}s?\b',  # Abbreviations like ACE, ARB, COPD
        r'\b\w+emia\b',  # Medical terms ending in -emia
        r'\b\w+itis\b',  # -itis
        r'\b\w+osis\b',  # -osis
        r'\b\w+ectomy\b',  # -ectomy
        r'\b\w+plasty\b',  # -plasty
        r'\b\d+\s*(?:mg|mcg|mL|L|g|kg)\b',  # Dosage patterns
        r'\(\w+\)',  # Parenthetical terms
    ]

    words = re.findall(r'\b\w+\b', content)
    if not words:
        return 0.0

    technical_count = 0
    for pattern in technical_patterns:
        technical_count += len(re.findall(pattern, content))

    return min(1.0, technical_count / (len(words) / 5))


# =============================================================================
# LIGHTWEIGHT ML MODEL
# =============================================================================

@dataclass
class TrainingExample:
    """A single training example for the ML model."""
    features: SlideFeatures
    label: VisualType
    confidence: float = 1.0  # How confident we are in this label


class NaiveBayesVisualClassifier:
    """
    Lightweight Naive Bayes classifier for visual type prediction.

    Uses Gaussian Naive Bayes with calibrated probability outputs.
    No external dependencies - implements from scratch using numpy-compatible
    operations with Python's built-in math module.
    """

    def __init__(self):
        self.classes = [vt for vt in VisualType if vt != VisualType.NONE]
        self.class_priors: Dict[VisualType, float] = {}
        self.feature_means: Dict[VisualType, List[float]] = {}
        self.feature_stds: Dict[VisualType, List[float]] = {}
        self.is_trained = False
        self.n_features = len(SlideFeatures.feature_names())

        # Calibration parameters
        self.calibration_temp = 1.0  # Temperature for probability calibration

    def fit(self, examples: List[TrainingExample]) -> None:
        """
        Train the classifier on labeled examples.

        Args:
            examples: List of TrainingExample objects
        """
        if not examples:
            return

        # Group examples by class
        class_examples: Dict[VisualType, List[List[float]]] = {
            c: [] for c in self.classes
        }

        for ex in examples:
            if ex.label in self.classes:
                class_examples[ex.label].append(ex.features.to_vector())

        # Calculate class priors
        total = len(examples)
        for c in self.classes:
            self.class_priors[c] = max(0.01, len(class_examples[c]) / total)

        # Calculate feature statistics per class
        for c in self.classes:
            if class_examples[c]:
                vectors = class_examples[c]
                n = len(vectors)

                # Calculate means
                means = [0.0] * self.n_features
                for v in vectors:
                    for i, val in enumerate(v):
                        means[i] += val / n
                self.feature_means[c] = means

                # Calculate standard deviations
                stds = [0.0] * self.n_features
                for v in vectors:
                    for i, val in enumerate(v):
                        stds[i] += (val - means[i]) ** 2 / n
                stds = [max(0.01, math.sqrt(s)) for s in stds]  # Min std to avoid division by zero
                self.feature_stds[c] = stds
            else:
                # Default for classes with no examples
                self.feature_means[c] = [0.0] * self.n_features
                self.feature_stds[c] = [1.0] * self.n_features

        self.is_trained = True

    def predict_proba(self, features: SlideFeatures) -> Dict[VisualType, float]:
        """
        Predict probability distribution over visual types.

        Args:
            features: SlideFeatures for a slide

        Returns:
            Dictionary mapping VisualType to probability
        """
        if not self.is_trained:
            # Return uniform distribution if not trained
            uniform = 1.0 / len(self.classes)
            return {c: uniform for c in self.classes}

        vector = features.to_vector()
        log_probs: Dict[VisualType, float] = {}

        for c in self.classes:
            # Start with log prior
            log_prob = math.log(self.class_priors[c])

            # Add log likelihood of each feature
            means = self.feature_means[c]
            stds = self.feature_stds[c]

            for i, val in enumerate(vector):
                # Gaussian log likelihood
                z = (val - means[i]) / stds[i]
                log_prob -= 0.5 * z * z
                log_prob -= math.log(stds[i])

            log_probs[c] = log_prob

        # Convert to probabilities with temperature scaling
        max_log = max(log_probs.values())
        probs = {}
        total = 0.0

        for c, lp in log_probs.items():
            p = math.exp((lp - max_log) / self.calibration_temp)
            probs[c] = p
            total += p

        # Normalize
        return {c: p / total for c, p in probs.items()}

    def predict(self, features: SlideFeatures) -> Tuple[VisualType, float]:
        """
        Predict the most likely visual type.

        Args:
            features: SlideFeatures for a slide

        Returns:
            Tuple of (predicted VisualType, confidence score)
        """
        probs = self.predict_proba(features)
        best_class = max(probs, key=probs.get)
        return (best_class, probs[best_class])

    def save(self, path: str) -> None:
        """Save model to disk."""
        state = {
            'class_priors': {k.value: v for k, v in self.class_priors.items()},
            'feature_means': {k.value: v for k, v in self.feature_means.items()},
            'feature_stds': {k.value: v for k, v in self.feature_stds.items()},
            'is_trained': self.is_trained,
            'calibration_temp': self.calibration_temp
        }
        with open(path, 'wb') as f:
            pickle.dump(state, f)

    def load(self, path: str) -> bool:
        """Load model from disk. Returns True if successful."""
        try:
            with open(path, 'rb') as f:
                state = pickle.load(f)

            self.class_priors = {VisualType(k): v for k, v in state['class_priors'].items()}
            self.feature_means = {VisualType(k): v for k, v in state['feature_means'].items()}
            self.feature_stds = {VisualType(k): v for k, v in state['feature_stds'].items()}
            self.is_trained = state['is_trained']
            self.calibration_temp = state.get('calibration_temp', 1.0)
            return True
        except (FileNotFoundError, KeyError, pickle.PickleError):
            return False


# =============================================================================
# ML VISUAL RECOMMENDER (Main Interface)
# =============================================================================

class MLVisualRecommender:
    """
    ML-enhanced visual type recommender.

    Combines a trained ML model with the existing rule-based system
    to provide improved visual type recommendations.

    Usage:
        recommender = MLVisualRecommender()

        # Load pre-trained model if available
        recommender.load_model('model.pkl')

        # Or train from samples
        recommender.train_from_samples(training_data)

        # Get recommendations
        result = recommender.recommend(slide, slide_num, total)
    """

    def __init__(self, model_path: Optional[str] = None):
        self.model = NaiveBayesVisualClassifier()
        self.rule_weight = 0.4  # Weight for rule-based predictions
        self.ml_weight = 0.6   # Weight for ML predictions

        if model_path:
            self.load_model(model_path)

    def train(self, examples: List[TrainingExample]) -> Dict[str, Any]:
        """
        Train the ML model on labeled examples.

        Args:
            examples: List of TrainingExample objects

        Returns:
            Training statistics
        """
        self.model.fit(examples)

        return {
            'num_examples': len(examples),
            'is_trained': self.model.is_trained,
            'classes': [c.value for c in self.model.classes],
            'class_distribution': {
                c.value: sum(1 for e in examples if e.label == c)
                for c in self.model.classes
            }
        }

    def train_from_samples(
        self,
        samples: List[Dict[str, Any]],
        labels: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Train from sample slides with optional labels.

        If labels not provided, uses rule-based predictions as pseudo-labels.

        Args:
            samples: List of slide dictionaries
            labels: Optional list of visual type labels (as strings)

        Returns:
            Training statistics
        """
        examples = []

        for i, slide in enumerate(samples):
            features = extract_features(
                slide,
                slide.get('slide_number', i + 1),
                len(samples)
            )

            if labels and i < len(labels):
                # Use provided label
                try:
                    label = VisualType(labels[i])
                except ValueError:
                    label = VisualType.NONE
            else:
                # Use rule-based prediction as pseudo-label
                score = score_visual_opportunity_multifactor(
                    slide,
                    slide.get('slide_number', i + 1),
                    len(samples)
                )
                label = score.visual_type

            if label != VisualType.NONE:
                examples.append(TrainingExample(features=features, label=label))

        return self.train(examples)

    def recommend(
        self,
        slide: Dict[str, Any],
        slide_number: int = 0,
        total_slides: int = 0
    ) -> Dict[str, Any]:
        """
        Get visual type recommendation using ensemble of rule-based and ML.

        Args:
            slide: Slide dictionary
            slide_number: Position in section
            total_slides: Total slides in section

        Returns:
            Recommendation dictionary with:
            - recommended_type: Best visual type
            - confidence: Combined confidence score
            - ml_prediction: ML model's prediction
            - rule_prediction: Rule-based prediction
            - all_probabilities: Distribution over all types
        """
        features = extract_features(slide, slide_number, total_slides)

        # Get ML prediction
        if self.model.is_trained:
            ml_type, ml_conf = self.model.predict(features)
            ml_probs = self.model.predict_proba(features)
        else:
            ml_type = VisualType.TABLE
            ml_conf = 0.0
            ml_probs = {c: 0.0 for c in self.model.classes}

        # Get rule-based prediction
        rule_score = score_visual_opportunity_multifactor(slide, slide_number, total_slides)
        rule_type = rule_score.visual_type
        rule_conf = rule_score.total_score

        # Ensemble combining
        combined_probs = self._ensemble_combine(
            ml_probs, ml_conf,
            rule_type, rule_conf
        )

        # Get best prediction
        best_type = max(combined_probs, key=combined_probs.get)
        best_conf = combined_probs[best_type]

        # If confidence too low, return NONE
        if best_conf < 0.3:
            best_type = VisualType.NONE
            best_conf = 0.0

        return {
            'recommended_type': best_type.value,
            'confidence': round(best_conf, 3),
            'should_have_visual': best_conf >= 0.4,
            'ml_prediction': {
                'type': ml_type.value,
                'confidence': round(ml_conf, 3)
            },
            'rule_prediction': {
                'type': rule_type.value if rule_type != VisualType.NONE else None,
                'confidence': round(rule_conf, 3),
                'proactive_trigger': rule_score.proactive_trigger
            },
            'all_probabilities': {
                k.value: round(v, 3) for k, v in combined_probs.items()
            },
            'feature_summary': self._summarize_features(features)
        }

    def _ensemble_combine(
        self,
        ml_probs: Dict[VisualType, float],
        ml_conf: float,
        rule_type: VisualType,
        rule_conf: float
    ) -> Dict[VisualType, float]:
        """
        Combine ML and rule-based predictions using weighted ensemble.

        When ML model is not trained or has low confidence, relies more
        on rule-based predictions. When both agree, boosts confidence.
        """
        combined = {}

        # Adjust weights based on ML confidence
        if not self.model.is_trained or ml_conf < 0.3:
            ml_w = 0.0
            rule_w = 1.0
        else:
            ml_w = self.ml_weight
            rule_w = self.rule_weight

        # Normalize weights
        total_w = ml_w + rule_w
        ml_w /= total_w
        rule_w /= total_w

        for c in self.model.classes:
            # ML contribution
            ml_contrib = ml_probs.get(c, 0.0) * ml_w

            # Rule contribution (spike at predicted type)
            if c == rule_type:
                rule_contrib = rule_conf * rule_w
            else:
                rule_contrib = 0.05 * rule_w  # Small contribution to others

            combined[c] = ml_contrib + rule_contrib

        # Agreement boost
        if rule_type in self.model.classes:
            # Check if ML and rule agree
            ml_best = max(ml_probs, key=ml_probs.get)
            if ml_best == rule_type:
                # Boost confidence when both agree
                combined[rule_type] *= 1.2

        # Normalize
        total = sum(combined.values())
        if total > 0:
            combined = {k: v / total for k, v in combined.items()}

        return combined

    def _summarize_features(self, features: SlideFeatures) -> Dict[str, Any]:
        """Create a human-readable feature summary."""
        return {
            'content': {
                'words': features.word_count,
                'lines': features.line_count,
                'bullets': features.bullet_count
            },
            'structure': {
                'complexity': round(features.structure_complexity, 2),
                'list_depth': features.list_depth,
                'is_parallel': features.has_parallel_structure
            },
            'patterns': {
                'is_comparison': features.is_comparison,
                'is_sequential': features.is_sequential,
                'is_hierarchical': features.is_hierarchical
            },
            'density': {
                'score': round(features.density_score, 2),
                'concepts': features.unique_concepts
            }
        }

    def save_model(self, path: str) -> None:
        """Save the trained model to disk."""
        self.model.save(path)

    def load_model(self, path: str) -> bool:
        """Load a trained model from disk."""
        return self.model.load(path)


# =============================================================================
# CONVENIENCE FUNCTIONS
# =============================================================================

# Global recommender instance (lazy-loaded)
_recommender: Optional[MLVisualRecommender] = None


def get_recommender() -> MLVisualRecommender:
    """Get or create the global recommender instance."""
    global _recommender
    if _recommender is None:
        _recommender = MLVisualRecommender()
    return _recommender


def get_ml_recommendation(
    slide: Dict[str, Any],
    slide_number: int = 0,
    total_slides: int = 0
) -> Dict[str, Any]:
    """
    Convenience function to get ML recommendation for a slide.

    Args:
        slide: Slide dictionary
        slide_number: Position in section
        total_slides: Total slides in section

    Returns:
        Recommendation dictionary
    """
    return get_recommender().recommend(slide, slide_number, total_slides)


def train_from_samples(
    samples: List[Dict[str, Any]],
    labels: Optional[List[str]] = None
) -> Dict[str, Any]:
    """
    Convenience function to train the global recommender.

    Args:
        samples: List of slide dictionaries
        labels: Optional list of visual type labels

    Returns:
        Training statistics
    """
    return get_recommender().train_from_samples(samples, labels)


def ensemble_predict(
    slide: Dict[str, Any],
    slide_number: int = 0,
    total_slides: int = 0
) -> Tuple[VisualType, float]:
    """
    Get ensemble prediction (combines ML and rule-based).

    Args:
        slide: Slide dictionary
        slide_number: Position in section
        total_slides: Total slides in section

    Returns:
        Tuple of (VisualType, confidence)
    """
    rec = get_recommender().recommend(slide, slide_number, total_slides)

    try:
        vtype = VisualType(rec['recommended_type'])
    except ValueError:
        vtype = VisualType.NONE

    return (vtype, rec['confidence'])


# =============================================================================
# TRAINING DATA GENERATION
# =============================================================================

def generate_training_data_from_patterns() -> List[TrainingExample]:
    """
    Generate training data from the built-in patterns in visual_pattern_matcher.

    Creates synthetic training examples based on the rule-based patterns,
    providing a starting point for the ML model.

    Returns:
        List of TrainingExample objects
    """
    examples = []

    # TABLE examples
    table_slides = [
        {
            'header': 'ACE Inhibitors vs ARBs',
            'body': '''* ACE-I: Block angiotensin converting enzyme
* ARBs: Block AT1 receptor directly
* ACE-I: May cause dry cough (10%)
* ARBs: No cough side effect
* Both: First-line for hypertension''',
            'slide_type': 'Content'
        },
        {
            'header': 'Comparison of Beta Blockers',
            'body': '''Metoprolol: Cardioselective, good for heart failure
Atenolol: Cardioselective, once daily dosing
Propranolol: Non-selective, crosses BBB
Carvedilol: Alpha/beta blocker, antioxidant properties''',
            'slide_type': 'Content'
        },
        {
            'header': 'Types of Insulin',
            'body': '''* Rapid-acting: Lispro, Aspart, Glulisine
* Short-acting: Regular insulin
* Intermediate: NPH
* Long-acting: Glargine, Detemir
* Ultra-long: Degludec''',
            'slide_type': 'Content'
        },
    ]

    for i, slide in enumerate(table_slides):
        features = extract_features(slide, i + 3, 12)
        examples.append(TrainingExample(features=features, label=VisualType.TABLE))

    # FLOWCHART examples
    flowchart_slides = [
        {
            'header': 'Medication Administration Process',
            'body': '''Step 1: Verify the medication order
Step 2: Check patient identification
Step 3: Review allergies and contraindications
Step 4: Prepare the medication
Step 5: Administer and document''',
            'slide_type': 'Content'
        },
        {
            'header': 'Blood Pressure Regulation Mechanism',
            'body': '''Low BP triggers baroreceptors
Then signals sent to medulla
This leads to sympathetic activation
Results in vasoconstriction
Finally BP returns to normal''',
            'slide_type': 'Content'
        },
        {
            'header': 'Nursing Process Steps',
            'body': '''* Assessment: Gather patient data
* Diagnosis: Identify nursing problems
* Planning: Set goals and outcomes
* Implementation: Execute interventions
* Evaluation: Measure effectiveness''',
            'slide_type': 'Content'
        },
    ]

    for i, slide in enumerate(flowchart_slides):
        features = extract_features(slide, i + 5, 12)
        examples.append(TrainingExample(features=features, label=VisualType.FLOWCHART))

    # DECISION_TREE examples
    decision_tree_slides = [
        {
            'header': 'Choosing Antihypertensive Therapy',
            'body': '''If patient has diabetes: Start with ACE-I or ARB
If patient has heart failure: Use beta-blocker + ACE-I
If patient has kidney disease: Prefer ACE-I
If patient is African American: Consider CCB + thiazide
If patient is pregnant: Use methyldopa or labetalol''',
            'slide_type': 'Content'
        },
        {
            'header': 'Pain Assessment Decision Path',
            'body': '''Assess pain intensity (0-10 scale)
If mild (1-3): Non-pharmacologic + PRN acetaminophen
If moderate (4-6): Scheduled NSAIDs or weak opioids
If severe (7-10): Strong opioids with adjuvants
Based on response: Adjust therapy accordingly''',
            'slide_type': 'Content'
        },
    ]

    for i, slide in enumerate(decision_tree_slides):
        features = extract_features(slide, i + 6, 12)
        examples.append(TrainingExample(features=features, label=VisualType.DECISION_TREE))

    # HIERARCHY examples
    hierarchy_slides = [
        {
            'header': 'Types of Heart Failure',
            'body': '''Heart Failure Types:
* Systolic HF (HFrEF)
  - Reduced ejection fraction
  - Weak contraction
* Diastolic HF (HFpEF)
  - Preserved ejection fraction
  - Impaired relaxation''',
            'slide_type': 'Content'
        },
        {
            'header': 'Classification of Antiarrhythmics',
            'body': '''Vaughan-Williams Classification:
* Class I: Sodium channel blockers
  - IA: Quinidine, Procainamide
  - IB: Lidocaine, Mexiletine
  - IC: Flecainide, Propafenone
* Class II: Beta blockers
* Class III: Potassium channel blockers
* Class IV: Calcium channel blockers''',
            'slide_type': 'Content'
        },
    ]

    for i, slide in enumerate(hierarchy_slides):
        features = extract_features(slide, i + 4, 12)
        examples.append(TrainingExample(features=features, label=VisualType.HIERARCHY))

    # TIMELINE examples
    timeline_slides = [
        {
            'header': 'Stages of Labor',
            'body': '''Early labor: 0-3 cm dilation
Active labor: 4-7 cm dilation
Transition: 8-10 cm dilation
Second stage: Pushing and delivery
Third stage: Placental delivery''',
            'slide_type': 'Content'
        },
        {
            'header': 'Wound Healing Phases',
            'body': '''Day 1-3: Inflammatory phase
Day 3-21: Proliferative phase
Day 21+: Maturation/Remodeling phase
Can take up to 2 years for full maturation''',
            'slide_type': 'Content'
        },
    ]

    for i, slide in enumerate(timeline_slides):
        features = extract_features(slide, i + 5, 12)
        examples.append(TrainingExample(features=features, label=VisualType.TIMELINE))

    # SPECTRUM examples
    spectrum_slides = [
        {
            'header': 'Pain Severity Scale',
            'body': '''Mild pain (1-3): Minimal interference
Moderate pain (4-6): Some activity limitation
Severe pain (7-9): Significant impairment
Worst possible (10): Debilitating''',
            'slide_type': 'Content'
        },
        {
            'header': 'Anxiety Spectrum',
            'body': '''Normal anxiety: Adaptive response
Mild anxiety: Heightened awareness
Moderate anxiety: Narrowed perception
Severe anxiety: Scattered thinking
Panic: Fight or flight activation''',
            'slide_type': 'Content'
        },
    ]

    for i, slide in enumerate(spectrum_slides):
        features = extract_features(slide, i + 6, 12)
        examples.append(TrainingExample(features=features, label=VisualType.SPECTRUM))

    # KEY_DIFFERENTIATORS examples
    keydiff_slides = [
        {
            'header': 'Distinguishing Type 1 vs Type 2 Diabetes',
            'body': '''Key difference: Type 1 has absolute insulin deficiency
Type 1: Autoimmune destruction of beta cells
Type 2: Insulin resistance with relative deficiency
Type 1: Usually presents in childhood
Type 2: Usually presents in adulthood with obesity''',
            'slide_type': 'Content'
        },
        {
            'header': 'Myocardial Infarction vs Angina',
            'body': '''Critical difference in duration:
Angina: Relief with rest or nitroglycerin
MI: No relief, lasting >20 minutes
Angina: Reversible ischemia
MI: Irreversible necrosis''',
            'slide_type': 'Content'
        },
    ]

    for i, slide in enumerate(keydiff_slides):
        features = extract_features(slide, i + 7, 12)
        examples.append(TrainingExample(features=features, label=VisualType.KEY_DIFFERENTIATORS))

    return examples


def initialize_with_patterns() -> Dict[str, Any]:
    """
    Initialize the global recommender with pattern-based training data.

    Call this function to bootstrap the ML model with built-in patterns.

    Returns:
        Training statistics
    """
    examples = generate_training_data_from_patterns()
    return get_recommender().train(examples)


# =============================================================================
# TEST RUNNER
# =============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("ML VISUAL RECOMMENDER - TEST SUITE")
    print("=" * 70)

    # Initialize with pattern-based training data
    print("\n1. Initializing model with pattern-based training data...")
    stats = initialize_with_patterns()
    print(f"   Training completed: {stats['num_examples']} examples")
    print(f"   Class distribution: {stats['class_distribution']}")

    # Test slides
    test_slides = [
        {
            'slide_number': 3,
            'header': 'ACE Inhibitors vs ARBs',
            'body': '''* ACE-I: Block angiotensin converting enzyme
* ARBs: Block AT1 receptor directly
* ACE-I: May cause dry cough (10%)
* ARBs: No cough side effect''',
            'slide_type': 'Content'
        },
        {
            'slide_number': 5,
            'header': 'Steps in Medication Administration',
            'body': '''Step 1: Verify the medication order
Step 2: Check patient identification
Step 3: Review allergies
Step 4: Prepare and administer''',
            'slide_type': 'Content'
        },
        {
            'slide_number': 7,
            'header': 'Types of Heart Failure',
            'body': '''* Systolic HF (HFrEF)
  - Reduced ejection fraction
  - Weak contraction
* Diastolic HF (HFpEF)
  - Preserved ejection fraction''',
            'slide_type': 'Content'
        },
        {
            'slide_number': 1,
            'header': 'Section Introduction',
            'body': 'Overview of cardiovascular medications',
            'slide_type': 'Section Intro'
        },
    ]

    print("\n2. Testing recommendations on sample slides...")
    print("-" * 70)

    for slide in test_slides:
        rec = get_ml_recommendation(slide, slide['slide_number'], len(test_slides))
        print(f"\nSlide {slide['slide_number']}: {slide['header'][:40]}...")
        print(f"  Recommended: {rec['recommended_type']} (conf: {rec['confidence']})")
        print(f"  ML prediction: {rec['ml_prediction']['type']} ({rec['ml_prediction']['confidence']})")
        print(f"  Rule prediction: {rec['rule_prediction']['type']} ({rec['rule_prediction']['confidence']})")
        print(f"  Should have visual: {rec['should_have_visual']}")
        if rec['rule_prediction'].get('proactive_trigger'):
            print(f"  Proactive trigger: {rec['rule_prediction']['proactive_trigger']}")

    print("\n3. Feature extraction test...")
    print("-" * 70)

    features = extract_features(test_slides[0], 3, 10)
    print(f"Sample features for slide 3:")
    print(f"  Word count: {features.word_count}")
    print(f"  Bullet count: {features.bullet_count}")
    print(f"  Is comparison: {features.is_comparison}")
    print(f"  Structure complexity: {features.structure_complexity:.2f}")
    print(f"  Keyword scores - Table: {features.keyword_table:.2f}, Flowchart: {features.keyword_flowchart:.2f}")

    print("\n4. All probabilities for slide 3...")
    print("-" * 70)

    rec = get_ml_recommendation(test_slides[0], 3, 10)
    for vtype, prob in sorted(rec['all_probabilities'].items(), key=lambda x: x[1], reverse=True):
        bar = "█" * int(prob * 30)
        print(f"  {vtype:20s} {prob:.3f} {bar}")

    print("\n" + "=" * 70)
    print("TEST COMPLETE")
    print("=" * 70)
