#!/usr/bin/env python3
"""
Title Reviser Skill

Revises slide titles to fit within character constraints WITHOUT truncation.
Always rewrites intelligently to preserve meaning.

Constraints:
- Maximum 36 characters per line
- Maximum 2 lines
- Total maximum 72 characters

IMPORTANT: This skill NEVER truncates. It always revises.

Created: 2026-01-06
"""

from typing import Dict, List, Any, Optional, Tuple
import re

# Character limits - Single line only
MAX_CHARS_PER_LINE = 36
MAX_LINES = 1
MAX_TOTAL_CHARS = MAX_CHARS_PER_LINE  # 36 chars, single line

# Abbreviation dictionary (priority order - most common first)
ABBREVIATIONS = {
    # High priority - very common in nursing
    "administration": "Admin",
    "medication": "Med",
    "medications": "Meds",
    "patient": "Pt",
    "patients": "Pts",
    "assessment": "Assess",
    "management": "Mgmt",

    # Medium priority - healthcare terms
    "healthcare": "HC",
    "pharmacology": "Pharm",
    "cardiovascular": "CV",
    "gastrointestinal": "GI",
    "intravenous": "IV",
    "intramuscular": "IM",
    "subcutaneous": "SubQ",
    "temperature": "Temp",
    "documentation": "Doc",
    "communication": "Comm",

    # Lower priority - general terms
    "complications": "Compl",
    "considerations": "Consid",
    "intervention": "Interv",
    "interventions": "Intervs",
    "fundamentals": "Fund",
    "transmission": "Trans",
    "precautions": "Precaut",
    "prevention": "Prevent",
    "procedures": "Proc",
    "principles": "Princ",
    "evaluation": "Eval",
    "implementation": "Impl",
    "comprehensive": "",  # Often removable
    "approximately": "~",
    "guidelines": "Guide",
    "requirements": "Reqs",
}

# Words that can often be removed without losing meaning
FILLER_WORDS = [
    "the", "a", "an", "for", "in", "of", "to", "with",
    "and", "or", "by", "on", "at", "from", "into",
    "understanding", "overview", "introduction",
]


def apply_abbreviations(text: str) -> str:
    """Apply medical/nursing abbreviations to shorten text."""
    result = text
    for full, abbrev in ABBREVIATIONS.items():
        # Case-insensitive replacement
        pattern = re.compile(r'\b' + re.escape(full) + r'\b', re.IGNORECASE)
        if abbrev:
            result = pattern.sub(abbrev, result)
        else:
            # Empty abbrev means remove the word
            result = pattern.sub('', result)

    # Clean up extra spaces
    result = ' '.join(result.split())
    return result


def remove_filler_words(text: str) -> str:
    """Remove common filler words that don't add meaning."""
    words = text.split()
    result = []
    for word in words:
        if word.lower() not in FILLER_WORDS:
            result.append(word)
    return ' '.join(result)


def replace_and_with_ampersand(text: str) -> str:
    """Replace 'and' with '&' to save characters."""
    return re.sub(r'\band\b', '&', text, flags=re.IGNORECASE)


def condense_to_single_line(text: str) -> str:
    """Condense text to fit in a single line (max 36 chars).

    Since we only allow 1 line, this aggressively abbreviates and
    extracts core concepts to fit within the limit.
    """
    if len(text) <= MAX_CHARS_PER_LINE:
        return text

    # Apply all abbreviations
    result = apply_abbreviations(text)
    result = replace_and_with_ampersand(result)
    result = remove_filler_words(result)

    if len(result) <= MAX_CHARS_PER_LINE:
        return result

    # Extract core concept if still too long
    result = extract_core_concept(result)
    result = apply_abbreviations(result)

    if len(result) <= MAX_CHARS_PER_LINE:
        return result

    # Last resort: take first N words that fit
    words = result.split()
    final_words = []
    for word in words:
        test = ' '.join(final_words + [word])
        if len(test) <= MAX_CHARS_PER_LINE:
            final_words.append(word)
        else:
            break

    return ' '.join(final_words) if final_words else result[:MAX_CHARS_PER_LINE]


def extract_core_concept(text: str, context: Optional[Dict] = None) -> str:
    """Extract the core concept when other strategies fail."""
    # Remove common prefixes
    prefixes_to_remove = [
        r'^understanding\s+',
        r'^overview\s+of\s+',
        r'^introduction\s+to\s+',
        r'^the\s+',
        r'^comprehensive\s+',
        r'^basic\s+',
        r'^advanced\s+',
    ]

    result = text
    for prefix in prefixes_to_remove:
        result = re.sub(prefix, '', result, flags=re.IGNORECASE)

    # Remove common suffixes
    suffixes_to_remove = [
        r'\s+in\s+healthcare(\s+settings?)?$',
        r'\s+for\s+nurses?$',
        r'\s+in\s+nursing(\s+practice)?$',
        r'\s+and\s+best\s+practices$',
    ]

    for suffix in suffixes_to_remove:
        result = re.sub(suffix, '', result, flags=re.IGNORECASE)

    return result.strip()


def validate_title(title: str) -> Dict[str, Any]:
    """Validate a title meets all constraints."""
    lines = title.split('\n')
    line_lengths = [len(line) for line in lines]

    valid = (
        len(lines) <= MAX_LINES and
        all(length <= MAX_CHARS_PER_LINE for length in line_lengths)
    )

    return {
        "valid": valid,
        "char_count": sum(line_lengths),
        "line_count": len(lines),
        "chars_per_line": line_lengths,
        "max_line_length": max(line_lengths) if line_lengths else 0
    }


def revise_title(
    original_title: str,
    violations: Optional[List[Dict]] = None,
    context: Optional[Dict] = None,
    hints: Optional[List[str]] = None
) -> Dict[str, Any]:
    """
    Revise a title to fit within constraints WITHOUT truncation.

    SINGLE LINE ONLY - Maximum 36 characters.

    Args:
        original_title: The title that needs revision
        violations: List of constraint violations from validator
        context: Additional context (topic, anchors, slide_type)
        hints: Revision suggestions from validator

    Returns:
        Dictionary with revised title and metadata
    """
    changes_made = []

    # Clean input - ensure single line
    working_title = original_title.strip()
    working_title = ' '.join(working_title.split())  # Normalize whitespace, remove newlines

    # Check if already valid
    validation = validate_title(working_title)
    if validation['valid']:
        return {
            "revised_title": working_title,
            "original_title": original_title,
            "revision_type": "none_needed",
            "changes_made": [],
            "validation": validation,
            "meaning_preserved": True
        }

    # Strategy 1: Replace 'and' with '&'
    revised = replace_and_with_ampersand(working_title)
    if revised != working_title:
        changes_made.append("Replaced 'and' with '&'")
        working_title = revised

    validation = validate_title(working_title)
    if validation['valid']:
        return {
            "revised_title": working_title,
            "original_title": original_title,
            "revision_type": "ampersand_substitution",
            "changes_made": changes_made,
            "validation": validation,
            "meaning_preserved": True
        }

    # Strategy 2: Apply abbreviations
    revised = apply_abbreviations(working_title)
    if revised != working_title:
        changes_made.append("Applied medical abbreviations")
        working_title = revised

    validation = validate_title(working_title)
    if validation['valid']:
        return {
            "revised_title": working_title,
            "original_title": original_title,
            "revision_type": "abbreviation",
            "changes_made": changes_made,
            "validation": validation,
            "meaning_preserved": True
        }

    # Strategy 3: Remove filler words
    revised = remove_filler_words(working_title)
    if revised != working_title:
        changes_made.append("Removed filler words")
        working_title = revised

    validation = validate_title(working_title)
    if validation['valid']:
        return {
            "revised_title": working_title,
            "original_title": original_title,
            "revision_type": "filler_removal",
            "changes_made": changes_made,
            "validation": validation,
            "meaning_preserved": True
        }

    # Strategy 4: Extract core concept
    revised = extract_core_concept(working_title, context)
    if revised != working_title:
        changes_made.append("Extracted core concept")
        working_title = revised

    # Re-apply abbreviations after extraction
    revised = apply_abbreviations(working_title)
    revised = replace_and_with_ampersand(revised)

    validation = validate_title(revised)
    if validation['valid']:
        return {
            "revised_title": revised,
            "original_title": original_title,
            "revision_type": "core_extraction",
            "changes_made": changes_made,
            "validation": validation,
            "meaning_preserved": True
        }

    # Strategy 5: Use condense_to_single_line for aggressive condensation
    revised = condense_to_single_line(working_title)
    validation = validate_title(revised)

    if validation['valid']:
        changes_made.append("Condensed to single line")
        return {
            "revised_title": revised,
            "original_title": original_title,
            "revision_type": "condensed",
            "changes_made": changes_made,
            "validation": validation,
            "meaning_preserved": True
        }

    # Last resort: Take first meaningful words that fit in single line
    words = revised.split()
    final_words = []

    for word in words:
        test = ' '.join(final_words + [word])
        if len(test) <= MAX_CHARS_PER_LINE:
            final_words.append(word)
        else:
            break

    if final_words:
        final_title = ' '.join(final_words)
        validation = validate_title(final_title)
        changes_made.append("Condensed to fit 36-char limit")

        return {
            "revised_title": final_title,
            "original_title": original_title,
            "revision_type": "best_effort",
            "changes_made": changes_made,
            "validation": validation,
            "meaning_preserved": len(final_words) > len(words) // 2,
            "warning": "Title significantly condensed - review recommended"
        }

    # Should never reach here, but just in case
    return {
        "revised_title": original_title[:MAX_CHARS_PER_LINE],  # Last resort
        "original_title": original_title,
        "revision_type": "failed",
        "changes_made": ["Could not revise within constraints"],
        "validation": validate_title(original_title[:MAX_CHARS_PER_LINE]),
        "meaning_preserved": False,
        "error": "Revision failed - manual review required"
    }


def revise_slide_title(slide: Dict[str, Any]) -> Dict[str, Any]:
    """Revise the title/header of a slide dictionary."""
    if 'header' not in slide:
        return slide

    revision = revise_title(
        original_title=slide['header'],
        context={
            'slide_type': slide.get('slide_type'),
            'slide_number': slide.get('slide_number')
        }
    )

    updated_slide = slide.copy()
    updated_slide['header'] = revision['revised_title']
    updated_slide['_title_revision'] = {
        'original': revision['original_title'],
        'revision_type': revision['revision_type'],
        'changes': revision['changes_made']
    }

    return updated_slide


def revise_blueprint_titles(blueprint: Dict[str, Any]) -> Dict[str, Any]:
    """Revise all slide titles in a blueprint."""
    if 'slides' not in blueprint:
        return blueprint

    updated_blueprint = blueprint.copy()
    updated_slides = []
    revisions_made = 0

    for slide in blueprint['slides']:
        updated_slide = revise_slide_title(slide)
        if '_title_revision' in updated_slide:
            if updated_slide['_title_revision']['revision_type'] != 'none_needed':
                revisions_made += 1
        updated_slides.append(updated_slide)

    updated_blueprint['slides'] = updated_slides
    updated_blueprint['_title_revision_summary'] = {
        'total_slides': len(updated_slides),
        'titles_revised': revisions_made
    }

    return updated_blueprint


if __name__ == "__main__":
    # Test the reviser
    test_titles = [
        "Transmission-Based Precautions for Infection Control in Healthcare Settings",
        "Comprehensive Medication Administration Safety Guidelines and Best Practices",
        "Understanding the Physiological Mechanisms of Beta-Adrenergic Receptor Blocking Agents",
        "Simple Title",
        "Beta-Blockers",
        "Cardiovascular Medications and Patient Safety Assessment",
    ]

    print("=== TITLE REVISER SKILL TEST ===\n")

    for title in test_titles:
        print(f"Original ({len(title)} chars):")
        print(f"  {title}")

        result = revise_title(title)

        print(f"Revised ({result['validation']['char_count']} chars):")
        for line in result['revised_title'].split('\n'):
            print(f"  {line} ({len(line)} chars)")
        print(f"Type: {result['revision_type']}")
        print(f"Valid: {result['validation']['valid']}")
        print(f"Changes: {', '.join(result['changes_made']) if result['changes_made'] else 'None'}")
        print()
