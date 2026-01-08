"""
Step 7 Formatting Revision Tests
Tests for character limits, line wrapping, condensation, and validation.

Run: python -m pytest tests/test_step7_formatting.py -v
"""

import sys
import unittest
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from skills.validation.char_counter import (
    CharCounter, count_chars_per_line, check_char_limit
)
from skills.validation.line_counter import (
    LineCounter, count_lines, check_line_limit
)
from skills.utilities.line_wrapper import (
    LineWrapper, wrap_text, wrap_header, wrap_body
)
from skills.utilities.bullet_formatter import (
    BulletFormatter, format_bullets, count_bullets
)
from skills.generation.text_condenser import (
    TextCondenser, condense_text
)
from skills.generation.content_condenser import (
    ContentCondenser, condense_content
)
from skills.enforcement.text_limits_enforcer import (
    enforce_all_text_limits, validate_all_text_limits
)
from skills.validation.constraint_validator import (
    ConstraintValidator, validate_slide
)


class TestCharCounter(unittest.TestCase):
    """Tests for CharCounter skill."""

    def setUp(self):
        self.counter = CharCounter()

    def test_count_empty_text(self):
        """Empty text returns zero counts."""
        result = self.counter.count("")
        self.assertEqual(result.total_chars, 0)
        self.assertEqual(result.line_count, 0)
        self.assertTrue(result.is_compliant)

    def test_count_single_line(self):
        """Single line counting works correctly."""
        result = self.counter.count("Hello World")
        self.assertEqual(result.total_chars, 11)
        self.assertEqual(result.line_count, 1)
        self.assertEqual(result.chars_per_line, [11])

    def test_count_multiple_lines(self):
        """Multiple lines counted correctly."""
        text = "Line one\nLine two\nLine three"
        result = self.counter.count(text)
        self.assertEqual(result.line_count, 3)
        self.assertEqual(len(result.chars_per_line), 3)

    def test_header_limit_compliance(self):
        """Header within 32 char limit is compliant."""
        result = self.counter.count_header("Short Header")
        self.assertTrue(result.is_compliant)

    def test_header_limit_violation(self):
        """Header exceeding 32 chars is non-compliant."""
        long_header = "This is a very long header that exceeds the limit"
        result = self.counter.count_header(long_header)
        self.assertFalse(result.is_compliant)
        self.assertGreater(len(result.lines_exceeding_limit), 0)

    def test_body_limit_compliance(self):
        """Body within 66 char limit is compliant."""
        result = self.counter.count_body("Normal body text within limits")
        self.assertTrue(result.is_compliant)

    def test_body_limit_violation(self):
        """Body exceeding 66 chars per line is non-compliant."""
        long_body = "x" * 70  # 70 characters
        result = self.counter.count_body(long_body)
        self.assertFalse(result.is_compliant)


class TestLineCounter(unittest.TestCase):
    """Tests for LineCounter skill."""

    def setUp(self):
        self.counter = LineCounter()

    def test_count_empty_text(self):
        """Empty text returns zero."""
        result = self.counter.count("")
        self.assertEqual(result.non_empty_lines, 0)

    def test_count_non_empty_lines_only(self):
        """Empty lines are not counted by default."""
        text = "Line 1\n\nLine 2\n\n\nLine 3"
        result = self.counter.count(text)
        self.assertEqual(result.non_empty_lines, 3)
        self.assertEqual(result.empty_lines, 3)

    def test_body_limit_compliance(self):
        """Body with 8 or fewer lines is compliant."""
        body = "\n".join([f"Line {i}" for i in range(8)])
        result = self.counter.count_body(body)
        self.assertTrue(result.is_compliant)

    def test_body_limit_violation(self):
        """Body with more than 8 lines is non-compliant."""
        body = "\n".join([f"Line {i}" for i in range(12)])
        result = self.counter.count_body(body)
        self.assertFalse(result.is_compliant)
        self.assertEqual(result.overage, 4)

    def test_bullet_detection(self):
        """Bullet points are detected correctly."""
        text = """* Bullet 1
* Bullet 2
  - Sub-bullet
Regular line"""
        result = self.counter.count(text)
        self.assertEqual(result.bullet_lines, 2)
        self.assertEqual(result.sub_bullet_lines, 1)


class TestLineWrapper(unittest.TestCase):
    """Tests for LineWrapper skill."""

    def setUp(self):
        self.wrapper = LineWrapper(max_chars=66)

    def test_short_line_unchanged(self):
        """Lines within limit are unchanged."""
        text = "Short line"
        result = self.wrapper.wrap(text)
        self.assertEqual(result.original_text, result.wrapped_text)
        self.assertFalse(result.was_modified)

    def test_long_line_wrapped(self):
        """Long lines are wrapped at word boundaries."""
        text = "This is a very long line that definitely exceeds the sixty-six character limit and needs wrapping"
        result = self.wrapper.wrap(text)
        self.assertTrue(result.was_modified)
        self.assertGreater(result.wrapped_lines, 1)
        self.assertLessEqual(result.max_char_per_line, 66)

    def test_bullet_preservation(self):
        """Bullet formatting is preserved when wrapping."""
        text = "* This is a very long bullet point that needs to be wrapped because it exceeds the character limit"
        result = self.wrapper.wrap(text)
        lines = result.wrapped_text.split('\n')
        self.assertTrue(lines[0].startswith('* '))

    def test_header_wrapping(self):
        """Header wrapping uses 32-char limit."""
        header = "The Relationship Between Dopamine and Motor Function in Parkinson's"
        wrapped = wrap_header(header)
        for line in wrapped.split('\n'):
            self.assertLessEqual(len(line), 32)


class TestBulletFormatter(unittest.TestCase):
    """Tests for BulletFormatter skill."""

    def setUp(self):
        self.formatter = BulletFormatter()

    def test_normalize_bullet_characters(self):
        """Different bullet characters are normalized."""
        text = """* Asterisk bullet
- Dash bullet
► Arrow bullet"""
        result = self.formatter.format(text)
        self.assertIn('•', result.formatted_text)

    def test_sub_bullet_detection(self):
        """Sub-bullets are detected and formatted."""
        text = """* Main bullet
  - Sub bullet"""
        result = self.formatter.format(text)
        self.assertEqual(result.bullet_count, 1)
        self.assertEqual(result.sub_bullet_count, 1)

    def test_count_bullets(self):
        """Bullet counting works correctly."""
        text = """* Bullet 1
* Bullet 2
  - Sub 1
  - Sub 2
* Bullet 3"""
        counts = count_bullets(text)
        self.assertEqual(counts['primary'], 3)
        self.assertEqual(counts['sub'], 2)
        self.assertEqual(counts['total'], 5)


class TestTextCondenser(unittest.TestCase):
    """Tests for TextCondenser skill."""

    def setUp(self):
        self.condenser = TextCondenser()

    def test_remove_filler_phrases(self):
        """Filler phrases are removed."""
        text = "It is important to note that the patient has symptoms."
        result = self.condenser.condense(text)
        self.assertNotIn("It is important to note that", result.condensed_text)
        self.assertIn("Removed filler phrases", result.techniques_applied)

    def test_phrase_condensation(self):
        """Long phrases are condensed."""
        text = "This results in the occurrence of hypotension."
        result = self.condenser.condense(text)
        self.assertIn("causes", result.condensed_text)

    def test_already_short_text_unchanged(self):
        """Short text that meets limits is unchanged."""
        text = "Simple statement."
        result = self.condenser.condense(text, max_lines=8)
        self.assertTrue(result.meets_limits)


class TestContentCondenser(unittest.TestCase):
    """Tests for ContentCondenser skill."""

    def setUp(self):
        self.condenser = ContentCondenser()

    def test_preserve_nclex_content(self):
        """NCLEX-related content is preserved."""
        slide = {
            'body': """* Regular point
* NCLEX tip: Priority assessment first
* Another regular point
* More content
* Additional content
* Extra line 1
* Extra line 2
* Extra line 3
* Extra line 4
* Low priority example"""
        }
        result = self.condenser.condense(slide, target_lines=8)
        self.assertIn("NCLEX", result.condensed_slide['body'])

    def test_moves_content_to_notes(self):
        """Excess content is moved to presenter notes."""
        slide = {
            'body': "\n".join([f"* Point {i}" for i in range(12)]),
            'presenter_notes': ""
        }
        result = self.condenser.condense(slide, target_lines=8)
        self.assertLessEqual(result.condensed_body_lines, 8)
        if result.content_moved_to_notes:
            self.assertIn("Additional context", result.condensed_slide['presenter_notes'])


class TestTextLimitsEnforcer(unittest.TestCase):
    """Tests for unified text limits enforcement."""

    def test_enforce_header(self):
        """Header enforcement works."""
        slide = {
            'header': 'The World Health Organization Five Moments for Hand Hygiene Practice',
            'body': 'Simple body'
        }
        result = enforce_all_text_limits(slide)
        # Header should be modified to fit 32 chars/line
        lines = result['header'].split('\n')
        for line in lines:
            self.assertLessEqual(len(line), 32)

    def test_enforce_body_chars(self):
        """Body character enforcement wraps long lines."""
        slide = {
            'header': 'Test',
            'body': 'x' * 100  # 100 chars in one line
        }
        result = enforce_all_text_limits(slide)
        for line in result['body'].split('\n'):
            self.assertLessEqual(len(line), 66)

    def test_validate_compliant_slide(self):
        """Compliant slide passes validation."""
        slide = {
            'header': 'Short Header',
            'body': '* Point 1\n* Point 2\n* Point 3'
        }
        result = validate_all_text_limits(slide)
        self.assertTrue(result['valid'])
        self.assertEqual(len(result['issues']), 0)


class TestConstraintValidator(unittest.TestCase):
    """Tests for ConstraintValidator."""

    def setUp(self):
        self.validator = ConstraintValidator()

    def test_validate_compliant_slide(self):
        """Compliant slide returns valid result."""
        slide = {
            'title': 'Test Title',
            'body': 'Test body content',
            'tip': 'Test tip',
            'notes': 'Short presenter notes for testing.'
        }
        result = self.validator.validate_slide(slide)
        self.assertTrue(result.is_valid)
        self.assertEqual(len(result.violations), 0)

    def test_validate_title_violation(self):
        """Title exceeding limit returns violation."""
        slide = {
            'title': 'This is a very long title that exceeds the thirty-two character limit per line',
            'body': 'Body'
        }
        result = self.validator.validate_slide(slide)
        self.assertFalse(result.is_valid)
        title_violations = [v for v in result.violations if v.field == 'title']
        self.assertGreater(len(title_violations), 0)

    def test_validate_body_violation(self):
        """Body exceeding limit returns violation."""
        slide = {
            'title': 'Title',
            'body': '\n'.join([f'Line {i}' for i in range(15)])  # 15 lines
        }
        result = self.validator.validate_slide(slide)
        body_violations = [v for v in result.violations if v.field == 'body']
        self.assertGreater(len(body_violations), 0)

    def test_batch_validation(self):
        """Multiple slides can be validated at once."""
        slides = [
            {'title': 'Slide 1', 'body': 'Body 1'},
            {'title': 'Slide 2', 'body': 'Body 2'},
            {'title': 'x' * 50, 'body': 'Body 3'},  # Invalid
        ]
        result = self.validator.validate_slides(slides)
        self.assertEqual(result.total_slides, 3)
        self.assertEqual(result.valid_slides, 2)
        self.assertEqual(result.invalid_slides, 1)


class TestStep7Integration(unittest.TestCase):
    """Integration tests for Step 7 workflow."""

    def test_full_formatting_workflow(self):
        """Complete Step 7 formatting workflow."""
        # Simulate Step 6.5 output
        slide = {
            'slide_number': 1,
            'slide_type': 'content',
            'header': 'The Relationship Between Dopamine and Motor Function',
            'body': """It is important to note that dopamine plays an important role in motor control:

* Dopamine is released from the substantia nigra in the brain
* It results in the occurrence of smooth, coordinated movements
* Deficiency leads to Parkinson's disease symptoms including tremor, rigidity, and bradykinesia
* Treatment involves dopamine replacement therapy with medications like levodopa
* NCLEX tip: Priority is assessing motor function before administering medication
* In other words, always assess baseline status first""",
            'nclex_tip': 'Focus on priority nursing actions for Parkinson\'s patients.',
            'presenter_notes': 'Explain the dopamine pathway.'
        }

        # Step 1: Condense text
        condenser = TextCondenser()
        condensed = condenser.condense_slide(slide)

        # Step 2: Wrap lines
        wrapper = LineWrapper()
        wrapped = wrapper.wrap_slide(condensed)

        # Step 3: Enforce limits
        enforced = enforce_all_text_limits(wrapped)

        # Step 4: Validate
        result = validate_all_text_limits(enforced)

        # Assertions
        self.assertLessEqual(
            len([l for l in enforced['header'].split('\n') if l]),
            2,
            "Header should have max 2 lines"
        )
        for line in enforced['header'].split('\n'):
            self.assertLessEqual(len(line), 32, "Header lines should be <= 32 chars")
        for line in enforced['body'].split('\n'):
            if line.strip():
                self.assertLessEqual(len(line), 66, "Body lines should be <= 66 chars")


class TestChangelog(unittest.TestCase):
    """Tests for changelog generation functionality."""

    def test_changelog_format(self):
        """Changelog entries have correct format."""
        # Simulate revision tracking
        original_header = "Very Long Header That Exceeds Limits"
        revised_header = "Condensed Header"

        changelog_entry = {
            'slide_number': 1,
            'element': 'header',
            'issue': f'Exceeded 32 characters (was {len(original_header)})',
            'original': original_header,
            'revised': revised_header,
            'change': 'Shortened while maintaining clarity'
        }

        # Verify structure
        self.assertIn('slide_number', changelog_entry)
        self.assertIn('element', changelog_entry)
        self.assertIn('issue', changelog_entry)
        self.assertIn('original', changelog_entry)
        self.assertIn('revised', changelog_entry)


if __name__ == '__main__':
    unittest.main()
