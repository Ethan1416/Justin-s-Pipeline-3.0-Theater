"""
Phase 2: Text Limits Enforcement Tests
Tests for R1, R2, R3 requirements.
"""

import unittest
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from skills.enforcement.header_enforcer import (
    enforce_header_limits, validate_header, abbreviate_text
)
from skills.enforcement.body_line_enforcer import (
    enforce_body_lines, validate_body_lines, count_non_empty_lines
)
from skills.enforcement.body_char_enforcer import (
    enforce_body_chars, validate_body_chars, wrap_line
)
from skills.enforcement.text_limits_enforcer import (
    enforce_all_text_limits, validate_all_text_limits
)


class TestHeaderEnforcer(unittest.TestCase):
    """Test R1: Header character limits (32 chars/line, 2 lines max)."""

    def test_short_header_unchanged(self):
        """Short headers should remain unchanged."""
        header = "Simple Header"
        result = enforce_header_limits(header)
        self.assertEqual(result, header)

    def test_long_header_truncated(self):
        """Long headers should be truncated to fit limits."""
        header = "This is a very long header that exceeds the limit"
        result = enforce_header_limits(header)
        lines = result.split('\n')
        self.assertTrue(all(len(l) <= 32 for l in lines))
        self.assertTrue(len(lines) <= 2)

    def test_abbreviation_applied(self):
        """Abbreviations should reduce text length."""
        text = "infection control fundamentals"
        abbreviated = abbreviate_text(text)
        self.assertLess(len(abbreviated), len(text))

    def test_validation_passes_for_valid_header(self):
        """Validation should pass for valid headers."""
        header = "Valid Header"
        result = validate_header(header)
        self.assertTrue(result['valid'])
        self.assertEqual(len(result['issues']), 0)

    def test_validation_fails_for_long_line(self):
        """Validation should fail for lines exceeding 32 chars."""
        header = "This header line is much too long to be valid"
        result = validate_header(header)
        self.assertFalse(result['valid'])
        self.assertGreater(len(result['issues']), 0)

    def test_two_line_header_allowed(self):
        """Two-line headers should be allowed if within char limits."""
        header = "Line One\nLine Two"
        result = validate_header(header)
        self.assertTrue(result['valid'])
        self.assertEqual(result['line_count'], 2)

    def test_three_line_header_rejected(self):
        """Three-line headers should fail validation."""
        header = "Line One\nLine Two\nLine Three"
        result = validate_header(header)
        self.assertFalse(result['valid'])

    def test_header_enforcement_real_example(self):
        """Test with realistic NCLEX header."""
        header = "The World Health Organization Five Moments for Hand Hygiene Practice"
        result = enforce_header_limits(header)
        validation = validate_header(result)
        self.assertTrue(validation['valid'])


class TestBodyLineEnforcer(unittest.TestCase):
    """Test R2: Body line limits (8 non-empty lines max)."""

    def test_under_limit_unchanged(self):
        """Content under limit should remain unchanged."""
        body = "Line 1\nLine 2\nLine 3"
        result = enforce_body_lines(body)
        self.assertEqual(result['action'], 'none')

    def test_over_limit_condensed(self):
        """Content over limit should be condensed."""
        body = '\n'.join([f"Line {i}" for i in range(12)])
        result = enforce_body_lines(body, strategy='condense')
        self.assertEqual(result['action'], 'condensed')
        self.assertEqual(result['final_lines'], 8)

    def test_over_limit_split(self):
        """Content over limit should be split when using split strategy."""
        body = '\n'.join([f"Line {i}" for i in range(12)])
        result = enforce_body_lines(body, strategy='split')
        self.assertEqual(result['action'], 'split')
        self.assertEqual(result['split_count'], 2)

    def test_count_non_empty_lines(self):
        """Should correctly count non-empty lines."""
        body = "Line 1\n\nLine 2\n\n\nLine 3"
        count = count_non_empty_lines(body)
        self.assertEqual(count, 3)

    def test_validation_passes_for_valid_body(self):
        """Validation should pass for body within limits."""
        body = '\n'.join([f"Line {i}" for i in range(5)])
        result = validate_body_lines(body)
        self.assertTrue(result['valid'])

    def test_validation_fails_for_excess_lines(self):
        """Validation should fail for body exceeding 8 lines."""
        body = '\n'.join([f"Line {i}" for i in range(12)])
        result = validate_body_lines(body)
        self.assertFalse(result['valid'])

    def test_blank_lines_not_counted(self):
        """Blank lines should not count toward the limit."""
        body = "Line 1\n\n\nLine 2\n\n\n\nLine 3"
        result = validate_body_lines(body)
        self.assertEqual(result['line_count'], 3)
        self.assertTrue(result['valid'])


class TestBodyCharEnforcer(unittest.TestCase):
    """Test R3: Body character limits (66 chars/line)."""

    def test_short_lines_unchanged(self):
        """Short lines should remain unchanged."""
        body = "Short line\nAnother short line"
        result = enforce_body_chars(body)
        self.assertEqual(result, body)

    def test_long_line_wrapped(self):
        """Long lines should be wrapped at word boundaries."""
        body = "This is a very long line that definitely exceeds the sixty-six character limit and needs wrapping"
        result = enforce_body_chars(body)
        self.assertTrue(all(len(l) <= 66 for l in result.split('\n') if l.strip()))

    def test_bullet_preserved(self):
        """Bullet point markers should be preserved."""
        body = "- This is a bullet point that is longer than sixty-six characters and needs wrapping"
        result = enforce_body_chars(body)
        self.assertTrue(result.startswith('- '))

    def test_validation_passes_for_valid_body(self):
        """Validation should pass for body within char limits."""
        body = "Short line\nAnother short line"
        result = validate_body_chars(body)
        self.assertTrue(result['valid'])

    def test_validation_fails_for_long_line(self):
        """Validation should fail for lines exceeding 66 chars."""
        body = "This is a very long line that definitely exceeds the sixty-six character limit by quite a bit"
        result = validate_body_chars(body)
        self.assertFalse(result['valid'])

    def test_wrap_line_with_numbered_bullet(self):
        """Numbered bullets should be handled correctly."""
        line = "1. This is a numbered bullet point that is longer than sixty-six characters and needs proper wrapping"
        result = wrap_line(line)
        self.assertTrue(result[0].startswith('1. '))
        self.assertTrue(all(len(l) <= 66 for l in result))

    def test_blank_lines_preserved(self):
        """Blank lines should be preserved."""
        body = "Line 1\n\nLine 2"
        result = enforce_body_chars(body)
        self.assertEqual(result, body)


class TestUnifiedEnforcer(unittest.TestCase):
    """Test unified text limits enforcement."""

    def test_all_limits_enforced(self):
        """All text limits should be enforced correctly."""
        slide = {
            'header': 'Very Long Header That Exceeds The Character Limit',
            'body': 'A very long body line that exceeds sixty-six characters and needs to be wrapped properly'
        }
        result = enforce_all_text_limits(slide)
        validation = validate_all_text_limits(result)
        self.assertTrue(validation['valid'])

    def test_header_only_slide(self):
        """Slides with only header should be handled."""
        slide = {'header': 'Simple Header'}
        result = enforce_all_text_limits(slide)
        self.assertEqual(result['header'], 'Simple Header')

    def test_body_only_slide(self):
        """Slides with only body should be handled."""
        slide = {'body': 'Simple body text'}
        result = enforce_all_text_limits(slide)
        self.assertEqual(result['body'], 'Simple body text')

    def test_complex_slide(self):
        """Complex slides should be fully processed."""
        slide = {
            'header': 'The World Health Organization Five Moments for Hand Hygiene Practice',
            'body': """The WHO identifies five critical moments requiring hand hygiene in healthcare:

1. Before patient contact - to protect the patient from colonization with healthcare-associated microorganisms
2. Before aseptic procedure - such as inserting catheters, accessing IV lines
3. After body fluid exposure risk - including after removing gloves
4. After patient contact - to protect yourself and the healthcare environment
5. After touching patient surroundings - including bed rails, monitors
6. Additional considerations include proper technique and duration
7. Hand hygiene compliance should be monitored regularly
8. Education and reminders are essential for maintaining compliance
9. Extra line that exceeds the limit"""
        }
        result = enforce_all_text_limits(slide)
        validation = validate_all_text_limits(result)

        # Header should be valid
        self.assertTrue(validation['r1_header']['valid'])
        # Body chars should be valid
        self.assertTrue(validation['r3_body_chars']['valid'])
        # Body lines should be valid
        self.assertTrue(validation['r2_body_lines']['valid'])

    def test_validation_reports_all_issues(self):
        """Validation should report all issues across requirements."""
        slide = {
            'header': 'This header is way too long and will definitely exceed the maximum character limit per line',
            'body': '\n'.join([f"This is line {i} which is also quite long and may exceed the character limit" for i in range(12)])
        }
        validation = validate_all_text_limits(slide)
        self.assertFalse(validation['valid'])
        self.assertGreater(len(validation['issues']), 0)


class TestEdgeCases(unittest.TestCase):
    """Test edge cases and boundary conditions."""

    def test_empty_header(self):
        """Empty header should be handled."""
        result = validate_header('')
        self.assertTrue(result['valid'])
        self.assertEqual(result['line_count'], 0)

    def test_empty_body(self):
        """Empty body should be handled."""
        result = validate_body_lines('')
        self.assertTrue(result['valid'])
        self.assertEqual(result['line_count'], 0)

    def test_exactly_32_char_header(self):
        """Header with exactly 32 chars should pass."""
        header = "A" * 32
        result = validate_header(header)
        self.assertTrue(result['valid'])

    def test_exactly_33_char_header(self):
        """Header with 33 chars should fail."""
        header = "A" * 33
        result = validate_header(header)
        self.assertFalse(result['valid'])

    def test_exactly_66_char_line(self):
        """Body line with exactly 66 chars should pass."""
        body = "A" * 66
        result = validate_body_chars(body)
        self.assertTrue(result['valid'])

    def test_exactly_67_char_line(self):
        """Body line with 67 chars should fail."""
        body = "A" * 67
        result = validate_body_chars(body)
        self.assertFalse(result['valid'])

    def test_exactly_8_lines(self):
        """Body with exactly 8 lines should pass."""
        body = '\n'.join([f"Line {i}" for i in range(8)])
        result = validate_body_lines(body)
        self.assertTrue(result['valid'])

    def test_exactly_9_lines(self):
        """Body with 9 lines should fail."""
        body = '\n'.join([f"Line {i}" for i in range(9)])
        result = validate_body_lines(body)
        self.assertFalse(result['valid'])


if __name__ == '__main__':
    unittest.main()
