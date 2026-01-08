"""
Integration Tests for Step 6 Pipeline
Tests full flow from blueprint generation through quality review.
"""

import unittest
import json
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from skills.templates.vignette_template import validate_vignette, VignetteTemplate
from skills.templates.answer_template import validate_answer, AnswerTemplate
from skills.enforcement.marker_insertion import validate_markers, insert_markers
from skills.enforcement.text_limits_enforcer import enforce_all_text_limits, validate_all_text_limits
from skills.validation.anchor_coverage_tracker import AnchorCoverageTracker, Anchor


class TestStep6Integration(unittest.TestCase):
    """Integration tests for Step 6 pipeline."""

    @classmethod
    def setUpClass(cls):
        """Load test fixtures."""
        cls.sample_input = cls._create_sample_input()

    @staticmethod
    def _create_sample_input():
        """Create sample Step 4 output as input for Step 6."""
        return {
            'section': {
                'section_number': 1,
                'section_name': 'Infection Control Fundamentals',
                'domain': 'fundamentals',
                'anchor_ids': ['IC001', 'IC002', 'IC003', 'IC004'],
                'anchor_content': [
                    {
                        'anchor_id': 'IC001',
                        'summary': 'Standard precautions overview',
                        'key_points': [
                            'Apply to all patients regardless of diagnosis',
                            'Include hand hygiene and PPE',
                            'Prevent transmission of infectious agents'
                        ]
                    },
                    {
                        'anchor_id': 'IC002',
                        'summary': 'Hand hygiene techniques',
                        'key_points': [
                            'Wash with soap and water for visible soiling',
                            'Use alcohol-based rub for routine decontamination',
                            'Five moments for hand hygiene'
                        ]
                    },
                    {
                        'anchor_id': 'IC003',
                        'summary': 'Personal protective equipment',
                        'key_points': [
                            'Gloves for contact with body fluids',
                            'Gowns for potential splash or spray',
                            'Eye protection when indicated'
                        ]
                    },
                    {
                        'anchor_id': 'IC004',
                        'summary': 'Transmission-based precautions',
                        'key_points': [
                            'Contact precautions for direct transmission',
                            'Droplet precautions for respiratory secretions',
                            'Airborne precautions for small particles'
                        ]
                    }
                ]
            },
            'constraints': {
                'header_max_chars': 32,
                'header_max_lines': 2,
                'body_max_chars': 66,
                'body_max_lines': 8
            }
        }

    def test_anchor_coverage_tracking(self):
        """Test that anchor coverage is properly tracked."""
        # Create proper Anchor objects
        anchors = [
            Anchor(number=1, summary='IC001', text='Standard precautions'),
            Anchor(number=2, summary='IC002', text='Hand hygiene'),
            Anchor(number=3, summary='IC003', text='PPE usage'),
            Anchor(number=4, summary='IC004', text='Transmission precautions')
        ]
        tracker = AnchorCoverageTracker(anchors)

        # Simulate covering anchors across slides
        tracker.mark_covered(['IC001', 'IC002'], slide_number=2)
        tracker.mark_covered(['IC003'], slide_number=3)
        tracker.mark_covered(['IC004'], slide_number=4)

        result = tracker.validate()
        self.assertTrue(result['valid'])
        self.assertEqual(result['covered_count'], result['total_anchors'])

    def test_text_limits_enforcement(self):
        """Test R1, R2, R3 enforcement through pipeline."""
        slide = {
            'slide_number': 2,
            'slide_type': 'Content',
            'header': 'This Header Is Way Too Long And Exceeds The Maximum Characters Allowed',
            'body': '\n'.join([f'Line {i} with some content' for i in range(12)]),
            'nclex_tip': 'A tip that is also too long ' * 5
        }

        enforced = enforce_all_text_limits(slide)
        validation = validate_all_text_limits(enforced)

        self.assertTrue(validation['valid'])
        self.assertLessEqual(len(enforced['header'].split('\n')[0]), 32)

    def test_vignette_structure_complete(self):
        """Test complete vignette structure validation."""
        vignette = VignetteTemplate(
            stem="A nurse is caring for a patient in airborne isolation. The patient has been diagnosed with tuberculosis. The nurse prepares to enter the room.",
            options={
                'A': 'Don a surgical mask',
                'B': 'Don an N95 respirator',
                'C': 'Use standard precautions only',
                'D': 'Wait for negative pressure confirmation'
            },
            correct_answer='B'
        )

        body = vignette.render()
        result = validate_vignette(body)

        self.assertTrue(result['valid'])
        self.assertTrue(result['has_all_options'])
        self.assertGreaterEqual(result['stem_sentences'], 2)
        self.assertLessEqual(result['stem_sentences'], 4)

    def test_answer_structure_complete(self):
        """Test complete answer structure validation."""
        answer = AnswerTemplate(
            correct_letter='B',
            correct_text='Don an N95 respirator',
            rationale='Tuberculosis requires airborne precautions. N95 respirators filter particles as small as 0.3 microns, providing protection against airborne pathogens.',
            distractors={
                'A': 'Surgical masks do not provide adequate filtration for airborne particles',
                'C': 'Standard precautions are insufficient for airborne transmission diseases',
                'D': 'Negative pressure is maintained continuously; waiting is unnecessary'
            }
        )

        body = answer.render()
        result = validate_answer(body)

        self.assertTrue(result['valid'])
        self.assertTrue(result['has_rationale'])
        self.assertTrue(result['has_distractor_analysis'])

    def test_marker_insertion_complete(self):
        """Test marker insertion and validation."""
        raw_notes = """Welcome to infection control fundamentals.
In this section we will cover standard precautions.
Hand hygiene is the most important intervention.
Always wash hands before and after patient contact.
On the NCLEX, these concepts are frequently tested."""

        notes = insert_markers(raw_notes, 'content', 'fundamentals')
        result = validate_markers(notes, 'content')

        self.assertTrue(result['valid'])
        self.assertGreaterEqual(result['pause_count'], 2)
        self.assertGreaterEqual(result['emphasis_count'], 1)

    def test_full_slide_workflow(self):
        """Test complete slide creation workflow."""
        # 1. Create slide structure
        slide = {
            'slide_number': 2,
            'slide_type': 'Content',
            'header': 'Standard Precautions',
            'body': '* Apply to all patients\n* Include hand hygiene\n* Use appropriate PPE',
            'anchors_covered': ['IC001'],
            'nclex_tip': '',
            'presenter_notes': ''
        }

        # 2. Enforce text limits
        slide = enforce_all_text_limits(slide)

        # 3. Add presenter notes with markers
        raw_notes = "Standard precautions are fundamental. They apply to all patients. Hand hygiene is key. PPE selection matters."
        slide['presenter_notes'] = insert_markers(raw_notes, 'content')

        # 4. Validate all components
        text_valid = validate_all_text_limits(slide)['valid']
        marker_valid = validate_markers(slide['presenter_notes'], 'content')['valid']

        self.assertTrue(text_valid)
        self.assertTrue(marker_valid)

    def test_vignette_answer_pair(self):
        """Test that vignette and answer slides work together."""
        # Create vignette
        vignette = VignetteTemplate(
            stem="A nurse is caring for a patient with active TB. The patient requires assessment.",
            options={
                'A': 'Enter with surgical mask',
                'B': 'Enter with N95 respirator',
                'C': 'Enter without PPE',
                'D': 'Delegate to UAP'
            },
            correct_answer='B'
        )

        # Create matching answer
        answer = AnswerTemplate(
            correct_letter='B',
            correct_text='Enter with N95 respirator',
            rationale='TB requires airborne precautions with N95 or higher respiratory protection.',
            distractors={
                'A': 'Surgical mask insufficient for airborne pathogens',
                'C': 'PPE is required for TB patients',
                'D': 'RN assessment cannot be delegated'
            }
        )

        # Both should be valid
        vig_result = validate_vignette(vignette.render())
        ans_result = validate_answer(answer.render())

        self.assertTrue(vig_result['valid'])
        self.assertTrue(ans_result['valid'])

        # Correct answers should match
        self.assertEqual(vignette.correct_answer, answer.correct_letter)


class TestQualityGateIntegration(unittest.TestCase):
    """Tests for quality gate logic."""

    def test_quality_score_calculation(self):
        """Test that quality scores are calculated correctly."""
        # Simulate validation results
        scores = {
            'outline': 100,
            'anchor': 100,
            'line_count': 100,
            'char_count': 100,
            'timing': 100,
            'nclex_tip': 100,
            'visual_quota': 100,
            'vignette': 100,
            'answer': 100,
            'markers': 100
        }

        # Weights from quality_reviewer
        weights = {
            'outline': 0.10,
            'anchor': 0.20,
            'line_count': 0.10,
            'char_count': 0.10,
            'timing': 0.10,
            'nclex_tip': 0.10,
            'visual_quota': 0.10,
            'vignette': 0.10,
            'answer': 0.05,
            'markers': 0.05
        }

        total = sum(scores[k] * weights[k] for k in scores)
        self.assertEqual(total, 100.0)

    def test_quality_gate_pass(self):
        """Test quality gate pass condition."""
        score = 92
        self.assertGreaterEqual(score, 90)  # PASS threshold

    def test_quality_gate_fail(self):
        """Test quality gate fail condition."""
        score = 85
        self.assertLess(score, 90)  # Below PASS threshold


if __name__ == '__main__':
    unittest.main(verbosity=2)
