"""
Unit Tests for Phase 4: Template Enforcement (R10, R11, R14)

Tests:
- VignetteTemplate creation and validation
- AnswerTemplate creation and validation
- Marker insertion and validation
"""

import unittest
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from skills.templates.vignette_template import (
    VignetteTemplate, validate_vignette, enforce_vignette_structure,
    parse_vignette_body
)
from skills.templates.answer_template import (
    AnswerTemplate, validate_answer, enforce_answer_structure,
    parse_answer_body
)
from skills.enforcement.marker_insertion import (
    insert_markers, validate_markers, count_markers,
    insert_pause_markers, insert_emphasis_markers, find_key_terms
)


class TestVignetteTemplate(unittest.TestCase):
    """Tests for R10: Vignette Structure"""

    def test_valid_vignette_creation(self):
        """Test creating a valid vignette with all required components."""
        template = VignetteTemplate(
            stem="A nurse is caring for a patient with pneumonia. The patient has a fever and decreased breath sounds.",
            options={
                'A': 'Administer prescribed antipyretic',
                'B': 'Position patient on right side',
                'C': 'Encourage deep breathing exercises',
                'D': 'Notify the healthcare provider immediately'
            },
            correct_answer='C'
        )
        result = template.validate()
        self.assertTrue(result['valid'])
        self.assertEqual(result['sentence_count'], 2)
        self.assertEqual(result['option_count'], 4)

    def test_vignette_missing_options_filled(self):
        """Test that missing options are auto-filled with placeholders."""
        template = VignetteTemplate(
            stem="A nurse assesses a patient. The patient reports chest pain.",
            options={
                'A': 'Option A',
                'B': 'Option B'
            },
            correct_answer='A'
        )
        # Missing C and D should be auto-filled
        self.assertIn('C', template.options)
        self.assertIn('D', template.options)
        self.assertTrue(template.options['C'].startswith('[Option'))

    def test_vignette_invalid_correct_answer(self):
        """Test that invalid correct answer raises error."""
        with self.assertRaises(ValueError):
            VignetteTemplate(
                stem="A nurse cares for a patient.",
                options={'A': 'A', 'B': 'B', 'C': 'C', 'D': 'D'},
                correct_answer='E'  # Invalid!
            )

    def test_vignette_render(self):
        """Test rendering vignette to body text."""
        template = VignetteTemplate(
            stem="A nurse is caring for a patient. The patient has symptoms.",
            options={
                'A': 'Option A text',
                'B': 'Option B text',
                'C': 'Option C text',
                'D': 'Option D text'
            },
            correct_answer='B'
        )
        body = template.render()
        self.assertIn('A nurse is caring', body)
        self.assertIn('A) Option A text', body)
        self.assertIn('B) Option B text', body)
        self.assertIn('C) Option C text', body)
        self.assertIn('D) Option D text', body)

    def test_validate_vignette_missing_option(self):
        """Test validation catches missing options."""
        body = """A nurse cares for a patient. The patient is sick.

A) Option A
B) Option B
C) Option C"""  # Missing D!

        result = validate_vignette(body)
        self.assertFalse(result['valid'])
        self.assertIn('D', result['missing_options'])

    def test_validate_vignette_short_stem(self):
        """Test validation catches too-short stem."""
        body = """Short stem.

A) Option A
B) Option B
C) Option C
D) Option D"""

        result = validate_vignette(body)
        self.assertFalse(result['valid'])
        self.assertEqual(result['stem_sentences'], 1)

    def test_enforce_vignette_adds_missing(self):
        """Test enforcement adds missing option D."""
        body = """A nurse cares for a patient. The patient is in the hospital.

A) Option A
B) Option B
C) Option C"""

        fixed = enforce_vignette_structure(body, 'A')
        self.assertIn('D)', fixed)
        result = validate_vignette(fixed)
        self.assertTrue(result['has_all_options'])

    def test_parse_vignette_body(self):
        """Test parsing raw vignette body."""
        body = """A nurse is caring for a patient with TB. The patient is in isolation. The nurse must wear proper PPE.

A) Surgical mask
B) N95 respirator
C) Face shield only
D) No PPE needed"""

        parsed = parse_vignette_body(body)
        self.assertIsNotNone(parsed)
        self.assertEqual(len(parsed.options), 4)
        self.assertIn('N95 respirator', parsed.options['B'])


class TestAnswerTemplate(unittest.TestCase):
    """Tests for R11: Answer Structure"""

    def test_valid_answer_creation(self):
        """Test creating a valid answer with all components."""
        template = AnswerTemplate(
            correct_letter='B',
            correct_text='N95 respirator',
            rationale='TB requires airborne precautions. N95 respirators filter small particles effectively.',
            distractors={
                'A': 'Surgical masks do not filter airborne particles',
                'C': 'Face shields alone do not protect against airborne pathogens',
                'D': 'PPE is always required for TB patients in isolation'
            }
        )
        result = template.validate()
        self.assertTrue(result['valid'])
        self.assertTrue(result['has_rationale'])
        self.assertEqual(result['distractor_count'], 3)

    def test_answer_missing_rationale(self):
        """Test validation catches missing rationale."""
        template = AnswerTemplate(
            correct_letter='B',
            correct_text='N95 respirator',
            rationale='',  # Empty!
            distractors={
                'A': 'Why A is wrong',
                'C': 'Why C is wrong',
                'D': 'Why D is wrong'
            }
        )
        result = template.validate()
        self.assertFalse(result['valid'])
        self.assertIn('Rationale missing', str(result['issues']))

    def test_answer_missing_distractor(self):
        """Test validation catches missing distractor analysis."""
        template = AnswerTemplate(
            correct_letter='B',
            correct_text='N95 respirator',
            rationale='TB requires airborne precautions.',
            distractors={
                'A': 'Why A is wrong',
                # Missing C and D!
            }
        )
        result = template.validate()
        self.assertFalse(result['valid'])

    def test_answer_render(self):
        """Test rendering answer to body text."""
        template = AnswerTemplate(
            correct_letter='B',
            correct_text='N95 respirator',
            rationale='TB requires airborne precautions.',
            distractors={
                'A': 'Surgical masks insufficient',
                'C': 'Face shield alone inadequate',
                'D': 'PPE always required'
            }
        )
        body = template.render()
        self.assertIn('Correct Answer: B)', body)
        self.assertIn('Rationale:', body)
        self.assertIn('Why not the others:', body)
        self.assertIn('- A)', body)
        self.assertIn('- C)', body)
        self.assertIn('- D)', body)

    def test_validate_answer_structure(self):
        """Test validating answer body text."""
        body = """Correct Answer: B) N95 respirator

Rationale:
TB requires airborne precautions and N95 masks.

Why not the others:
- A) Surgical masks insufficient
- C) Face shield alone inadequate
- D) PPE is always required"""

        result = validate_answer(body)
        self.assertTrue(result['valid'])
        self.assertTrue(result['has_rationale'])
        self.assertTrue(result['has_distractor_analysis'])
        self.assertTrue(result['has_correct_answer'])

    def test_validate_answer_missing_rationale(self):
        """Test validation catches missing rationale section."""
        body = """Correct Answer: B) N95 respirator

TB requires airborne precautions."""  # No "Rationale:" label!

        result = validate_answer(body)
        self.assertFalse(result['valid'])
        self.assertFalse(result['has_rationale'])

    def test_enforce_answer_adds_sections(self):
        """Test enforcement adds missing sections."""
        body = """Correct Answer: B) N95 respirator

TB requires airborne precautions."""

        fixed = enforce_answer_structure(body, 'B', 'N95 respirator')
        self.assertIn('Rationale:', fixed)
        self.assertIn('Why not the others:', fixed)


class TestMarkerInsertion(unittest.TestCase):
    """Tests for R14: Presenter Notes Markers"""

    def test_count_markers(self):
        """Test counting existing markers."""
        notes = "Text [PAUSE] more text [PAUSE] [EMPHASIS: key term] end."
        counts = count_markers(notes)
        self.assertEqual(counts['pause'], 2)
        self.assertEqual(counts['emphasis'], 1)

    def test_count_markers_empty(self):
        """Test counting when no markers present."""
        notes = "Plain text without any markers."
        counts = count_markers(notes)
        self.assertEqual(counts['pause'], 0)
        self.assertEqual(counts['emphasis'], 0)

    def test_find_key_terms(self):
        """Test finding key clinical terms."""
        text = "The nurse must assess the airway first. Safety is the priority."
        terms = find_key_terms(text)
        self.assertTrue(len(terms) > 0)
        # Should find terms like 'airway', 'safety', 'priority'

    def test_insert_pause_markers(self):
        """Test pause marker insertion."""
        notes = "First sentence here. Second sentence follows. Third is important. Final sentence concludes."
        fixed = insert_pause_markers(notes)
        counts = count_markers(fixed)
        self.assertGreaterEqual(counts['pause'], 2)

    def test_insert_pause_preserves_existing(self):
        """Test that existing pause markers are preserved."""
        notes = "Text [PAUSE] more text [PAUSE] end sentence."
        fixed = insert_pause_markers(notes)
        self.assertEqual(fixed, notes)  # Should be unchanged

    def test_insert_emphasis_markers(self):
        """Test emphasis marker insertion."""
        notes = "The nurse must assess the airway first. Safety is the priority in cardiac care."
        fixed = insert_emphasis_markers(notes)
        counts = count_markers(fixed)
        self.assertGreater(counts['emphasis'], 0)

    def test_insert_markers_content_slide(self):
        """Test full marker insertion for content slide."""
        notes = """Standard precautions are the foundation of infection control.
We treat every patient's body fluids as potentially infectious.
The components include hand hygiene and PPE.
Safe injection practices are also critical.
On the NCLEX, standard precautions questions are common."""

        fixed = insert_markers(notes, slide_type='content', domain='fundamentals')
        validation = validate_markers(fixed, 'content')
        self.assertTrue(validation['valid'])

    def test_insert_markers_vignette_slide(self):
        """Test marker insertion for vignette slide."""
        notes = "Let's apply what we've learned. Read the scenario carefully. Take time to think."
        fixed = insert_markers(notes, slide_type='vignette')
        counts = count_markers(fixed)
        self.assertGreaterEqual(counts['pause'], 2)

    def test_validate_markers_content(self):
        """Test validation for content slides."""
        notes = "Text [PAUSE] more text [PAUSE] [EMPHASIS: term] end."
        result = validate_markers(notes, 'content')
        self.assertTrue(result['valid'])

    def test_validate_markers_insufficient(self):
        """Test validation fails with insufficient markers."""
        notes = "Text with only [PAUSE] one pause marker."
        result = validate_markers(notes, 'content')
        self.assertFalse(result['valid'])
        self.assertIn('Only 1 [PAUSE] markers', str(result['issues']))

    def test_validate_markers_vignette_no_emphasis_needed(self):
        """Test that vignette slides don't require emphasis markers."""
        notes = "Text [PAUSE] more text [PAUSE] end."
        result = validate_markers(notes, 'vignette')
        self.assertTrue(result['valid'])


class TestIntegration(unittest.TestCase):
    """Integration tests combining multiple components."""

    def test_full_vignette_workflow(self):
        """Test complete vignette creation and validation workflow."""
        # Create vignette
        vignette = VignetteTemplate(
            stem="A nurse is caring for a patient in isolation. The patient has tuberculosis. The nurse prepares to enter the room.",
            options={
                'A': 'Put on surgical mask',
                'B': 'Put on N95 respirator',
                'C': 'Use standard precautions only',
                'D': 'Ask for physician clearance'
            },
            correct_answer='B'
        )

        # Validate structure
        body = vignette.render()
        validation = validate_vignette(body)
        self.assertTrue(validation['valid'])
        self.assertTrue(validation['has_all_options'])
        self.assertEqual(validation['stem_sentences'], 3)

    def test_full_answer_workflow(self):
        """Test complete answer creation and validation workflow."""
        # Create answer
        answer = AnswerTemplate(
            correct_letter='B',
            correct_text='Put on N95 respirator',
            rationale='Tuberculosis is transmitted via airborne droplet nuclei. N95 respirators filter particles as small as 0.3 microns with 95% efficiency.',
            distractors={
                'A': 'Surgical masks do not provide adequate protection against airborne pathogens',
                'C': 'Standard precautions are insufficient for airborne transmission',
                'D': 'Physician clearance is not required to follow isolation protocols'
            }
        )

        # Validate structure
        body = answer.render()
        validation = validate_answer(body)
        self.assertTrue(validation['valid'])

    def test_full_marker_workflow(self):
        """Test complete marker insertion workflow."""
        raw_notes = """Welcome to infection control fundamentals.
Today we'll discuss standard precautions and their importance.
Hand hygiene is the single most effective intervention.
Remember to wash hands before and after patient contact.
On the NCLEX, these concepts appear frequently."""

        # Insert markers
        notes = insert_markers(raw_notes, 'content', 'fundamentals')

        # Validate
        validation = validate_markers(notes, 'content')
        self.assertTrue(validation['valid'])
        self.assertGreaterEqual(validation['pause_count'], 2)
        self.assertGreaterEqual(validation['emphasis_count'], 1)


if __name__ == '__main__':
    unittest.main(verbosity=2)
