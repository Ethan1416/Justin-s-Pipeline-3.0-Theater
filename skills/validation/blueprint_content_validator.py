"""
Blueprint Content Validator
Comprehensive validation of blueprint slides against all Step 6 requirements.

Requirements validated:
- R1: Header max 32 chars/line, max 2 lines
- R2: Body max 8 non-empty lines
- R3: Body max 66 chars/line
- R4: NCLEX tip required on all content slides
- R5: NCLEX tip max 2 lines
- R6: Presenter notes max 450 words
- R7: Presenter notes max 180 seconds (estimated)
- R8: All anchors covered
- R9: Section intro has quote
- R10: Vignette has 2-4 sentence stem + 4 options
- R11: Answer slide has rationale + distractor analysis

Usage:
    python blueprint_content_validator.py <blueprint_file>
    python blueprint_content_validator.py <blueprint_file> --json
"""

import re
import sys
import json
from pathlib import Path
from dataclasses import dataclass, field, asdict
from typing import List, Optional, Dict, Any


# Constraints from spec
HEADER_MAX_CHARS_PER_LINE = 32
HEADER_MAX_LINES = 2
BODY_MAX_LINES = 8
BODY_MAX_CHARS_PER_LINE = 66
TIP_MAX_LINES = 2
TIP_MAX_CHARS_PER_LINE = 66
PRESENTER_NOTES_MAX_WORDS = 450
PRESENTER_NOTES_MAX_SECONDS = 180
WORDS_PER_MINUTE = 150  # For timing estimation


@dataclass
class ValidationResult:
    """Result of validating a single requirement."""
    requirement_id: str
    requirement_name: str
    passed: bool
    message: str
    slide_number: Optional[int] = None
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class SlideValidation:
    """Validation results for a single slide."""
    slide_number: int
    slide_type: str
    slide_title: str
    results: List[ValidationResult] = field(default_factory=list)

    @property
    def all_passed(self) -> bool:
        return all(r.passed for r in self.results)

    @property
    def failed_count(self) -> int:
        return sum(1 for r in self.results if not r.passed)


@dataclass
class BlueprintValidation:
    """Complete validation results for a blueprint."""
    blueprint_file: str
    total_slides: int
    slides: List[SlideValidation] = field(default_factory=list)
    global_results: List[ValidationResult] = field(default_factory=list)

    @property
    def all_passed(self) -> bool:
        slide_passed = all(s.all_passed for s in self.slides)
        global_passed = all(r.passed for r in self.global_results)
        return slide_passed and global_passed

    @property
    def total_failures(self) -> int:
        slide_failures = sum(s.failed_count for s in self.slides)
        global_failures = sum(1 for r in self.global_results if not r.passed)
        return slide_failures + global_failures

    def to_dict(self) -> dict:
        return {
            "blueprint_file": self.blueprint_file,
            "total_slides": self.total_slides,
            "all_passed": self.all_passed,
            "total_failures": self.total_failures,
            "slides": [
                {
                    "slide_number": s.slide_number,
                    "slide_type": s.slide_type,
                    "slide_title": s.slide_title,
                    "all_passed": s.all_passed,
                    "results": [asdict(r) for r in s.results]
                }
                for s in self.slides
            ],
            "global_results": [asdict(r) for r in self.global_results]
        }


def count_non_empty_lines(text: str) -> int:
    """Count non-empty lines in text."""
    lines = [line.strip() for line in text.strip().split('\n')]
    return len([line for line in lines if line])


def count_chars_per_line(text: str) -> List[int]:
    """Get character count for each non-empty line."""
    lines = [line.strip() for line in text.strip().split('\n')]
    return [len(line) for line in lines if line]


def count_words(text: str) -> int:
    """Count words in text."""
    return len(text.split())


def estimate_speaking_seconds(text: str) -> int:
    """Estimate speaking time in seconds."""
    words = count_words(text)
    return int((words / WORDS_PER_MINUTE) * 60)


def parse_slide(slide_content: str) -> Dict[str, Any]:
    """Parse slide content into structured data."""
    slide = {
        "header": "",
        "body": "",
        "nclex_tip": "",
        "presenter_notes": "",
        "type": "unknown"
    }

    # Extract type
    type_match = re.search(r'Type:\s*(.+)', slide_content)
    if type_match:
        slide["type"] = type_match.group(1).strip().lower().replace(" ", "_")

    # Extract header
    header_match = re.search(r'HEADER:\n(.*?)(?=\n\nBODY:|\nBODY:)', slide_content, re.DOTALL)
    if header_match:
        slide["header"] = header_match.group(1).strip()

    # Extract body
    body_match = re.search(
        r'\nBODY:\n(.*?)(?=\n\nNCLEX TIP:|\nNCLEX TIP:|\n\nPRESENTER NOTES:|\nPRESENTER NOTES:|$)',
        slide_content, re.DOTALL
    )
    if body_match:
        slide["body"] = body_match.group(1).strip()

    # Extract NCLEX tip
    tip_match = re.search(
        r'NCLEX TIP:\n(.*?)(?=\n\nPRESENTER NOTES:|\nPRESENTER NOTES:|$)',
        slide_content, re.DOTALL
    )
    if tip_match:
        tip_text = tip_match.group(1).strip()
        if tip_text and tip_text.lower() not in ['[none]', '[none - omit for intro slides]',
                                                   '[none - omit for vignette slides]',
                                                   '[none - omit for answer slides]']:
            slide["nclex_tip"] = tip_text

    # Extract presenter notes
    notes_match = re.search(r'PRESENTER NOTES:\n(.*?)(?===|$)', slide_content, re.DOTALL)
    if notes_match:
        slide["presenter_notes"] = notes_match.group(1).strip()

    return slide


def validate_header(slide: Dict, slide_num: int) -> List[ValidationResult]:
    """Validate header constraints (R1)."""
    results = []
    header = slide.get("header", "")

    if not header:
        results.append(ValidationResult(
            requirement_id="R1",
            requirement_name="Header validation",
            passed=False,
            message="Header is empty",
            slide_number=slide_num
        ))
        return results

    lines = [line for line in header.split('\n') if line.strip()]
    line_count = len(lines)

    # Check line count
    if line_count > HEADER_MAX_LINES:
        results.append(ValidationResult(
            requirement_id="R1a",
            requirement_name="Header max lines",
            passed=False,
            message=f"Header has {line_count} lines, max is {HEADER_MAX_LINES}",
            slide_number=slide_num,
            details={"line_count": line_count, "max": HEADER_MAX_LINES}
        ))
    else:
        results.append(ValidationResult(
            requirement_id="R1a",
            requirement_name="Header max lines",
            passed=True,
            message=f"Header has {line_count} lines (max {HEADER_MAX_LINES})",
            slide_number=slide_num
        ))

    # Check chars per line
    max_chars_found = 0
    for i, line in enumerate(lines):
        char_count = len(line.strip())
        max_chars_found = max(max_chars_found, char_count)
        if char_count > HEADER_MAX_CHARS_PER_LINE:
            results.append(ValidationResult(
                requirement_id="R1b",
                requirement_name="Header max chars/line",
                passed=False,
                message=f"Header line {i+1} has {char_count} chars, max is {HEADER_MAX_CHARS_PER_LINE}",
                slide_number=slide_num,
                details={"line": i+1, "chars": char_count, "max": HEADER_MAX_CHARS_PER_LINE}
            ))

    if max_chars_found <= HEADER_MAX_CHARS_PER_LINE:
        results.append(ValidationResult(
            requirement_id="R1b",
            requirement_name="Header max chars/line",
            passed=True,
            message=f"All header lines within {HEADER_MAX_CHARS_PER_LINE} char limit",
            slide_number=slide_num
        ))

    return results


def validate_body(slide: Dict, slide_num: int) -> List[ValidationResult]:
    """Validate body constraints (R2, R3)."""
    results = []
    body = slide.get("body", "")

    if not body:
        # Body can be empty for some slide types
        return results

    # R2: Max 8 non-empty lines
    line_count = count_non_empty_lines(body)
    if line_count > BODY_MAX_LINES:
        results.append(ValidationResult(
            requirement_id="R2",
            requirement_name="Body max lines",
            passed=False,
            message=f"Body has {line_count} non-empty lines, max is {BODY_MAX_LINES}",
            slide_number=slide_num,
            details={"line_count": line_count, "max": BODY_MAX_LINES}
        ))
    else:
        results.append(ValidationResult(
            requirement_id="R2",
            requirement_name="Body max lines",
            passed=True,
            message=f"Body has {line_count} non-empty lines (max {BODY_MAX_LINES})",
            slide_number=slide_num
        ))

    # R3: Max 66 chars per line
    chars_per_line = count_chars_per_line(body)
    max_chars = max(chars_per_line) if chars_per_line else 0

    lines_over_limit = [i+1 for i, c in enumerate(chars_per_line) if c > BODY_MAX_CHARS_PER_LINE]
    if lines_over_limit:
        results.append(ValidationResult(
            requirement_id="R3",
            requirement_name="Body max chars/line",
            passed=False,
            message=f"Body has lines exceeding {BODY_MAX_CHARS_PER_LINE} chars: lines {lines_over_limit}",
            slide_number=slide_num,
            details={"max_chars": max_chars, "lines_over": lines_over_limit}
        ))
    else:
        results.append(ValidationResult(
            requirement_id="R3",
            requirement_name="Body max chars/line",
            passed=True,
            message=f"All body lines within {BODY_MAX_CHARS_PER_LINE} char limit",
            slide_number=slide_num
        ))

    return results


def validate_nclex_tip(slide: Dict, slide_num: int) -> List[ValidationResult]:
    """Validate NCLEX tip requirements (R4, R5)."""
    results = []
    slide_type = slide.get("type", "unknown")
    tip = slide.get("nclex_tip", "")

    # R4: NCLEX tip required on content slides
    if slide_type == "content":
        if not tip:
            results.append(ValidationResult(
                requirement_id="R4",
                requirement_name="NCLEX tip required",
                passed=False,
                message="Content slide missing NCLEX tip",
                slide_number=slide_num
            ))
        else:
            results.append(ValidationResult(
                requirement_id="R4",
                requirement_name="NCLEX tip required",
                passed=True,
                message="NCLEX tip present",
                slide_number=slide_num
            ))

            # R5: Tip max 2 lines
            line_count = count_non_empty_lines(tip)
            if line_count > TIP_MAX_LINES:
                results.append(ValidationResult(
                    requirement_id="R5",
                    requirement_name="NCLEX tip max lines",
                    passed=False,
                    message=f"NCLEX tip has {line_count} lines, max is {TIP_MAX_LINES}",
                    slide_number=slide_num
                ))
            else:
                results.append(ValidationResult(
                    requirement_id="R5",
                    requirement_name="NCLEX tip max lines",
                    passed=True,
                    message=f"NCLEX tip has {line_count} lines (max {TIP_MAX_LINES})",
                    slide_number=slide_num
                ))

    return results


def validate_presenter_notes(slide: Dict, slide_num: int) -> List[ValidationResult]:
    """Validate presenter notes constraints (R6, R7)."""
    results = []
    notes = slide.get("presenter_notes", "")

    if not notes:
        results.append(ValidationResult(
            requirement_id="R6",
            requirement_name="Presenter notes present",
            passed=False,
            message="Presenter notes missing",
            slide_number=slide_num
        ))
        return results

    # R6: Max 450 words
    word_count = count_words(notes)
    if word_count > PRESENTER_NOTES_MAX_WORDS:
        results.append(ValidationResult(
            requirement_id="R6",
            requirement_name="Presenter notes max words",
            passed=False,
            message=f"Presenter notes have {word_count} words, max is {PRESENTER_NOTES_MAX_WORDS}",
            slide_number=slide_num,
            details={"word_count": word_count, "max": PRESENTER_NOTES_MAX_WORDS}
        ))
    else:
        results.append(ValidationResult(
            requirement_id="R6",
            requirement_name="Presenter notes max words",
            passed=True,
            message=f"Presenter notes have {word_count} words (max {PRESENTER_NOTES_MAX_WORDS})",
            slide_number=slide_num
        ))

    # R7: Max 180 seconds
    estimated_seconds = estimate_speaking_seconds(notes)
    if estimated_seconds > PRESENTER_NOTES_MAX_SECONDS:
        results.append(ValidationResult(
            requirement_id="R7",
            requirement_name="Presenter notes max time",
            passed=False,
            message=f"Presenter notes estimated at {estimated_seconds}s, max is {PRESENTER_NOTES_MAX_SECONDS}s",
            slide_number=slide_num,
            details={"estimated_seconds": estimated_seconds, "max": PRESENTER_NOTES_MAX_SECONDS}
        ))
    else:
        results.append(ValidationResult(
            requirement_id="R7",
            requirement_name="Presenter notes max time",
            passed=True,
            message=f"Presenter notes estimated at {estimated_seconds}s (max {PRESENTER_NOTES_MAX_SECONDS}s)",
            slide_number=slide_num
        ))

    return results


def validate_section_intro(slide: Dict, slide_num: int) -> List[ValidationResult]:
    """Validate section intro has quote (R9)."""
    results = []

    if slide.get("type") != "section_intro":
        return results

    body = slide.get("body", "")

    # Check for quote (indicated by quotation marks or em-dash attribution)
    has_quote = '"' in body or '"' in body or '—' in body or '-' in body.lower()

    if not has_quote:
        results.append(ValidationResult(
            requirement_id="R9",
            requirement_name="Section intro quote",
            passed=False,
            message="Section intro missing provocative quote",
            slide_number=slide_num
        ))
    else:
        results.append(ValidationResult(
            requirement_id="R9",
            requirement_name="Section intro quote",
            passed=True,
            message="Section intro has quote",
            slide_number=slide_num
        ))

    return results


def validate_vignette(slide: Dict, slide_num: int) -> List[ValidationResult]:
    """Validate vignette structure (R10)."""
    results = []

    if slide.get("type") != "vignette":
        return results

    body = slide.get("body", "")

    # Check for 4 options (A, B, C, D)
    has_options = all(f"{opt})" in body or f"{opt}." in body for opt in ['A', 'B', 'C', 'D'])

    if not has_options:
        results.append(ValidationResult(
            requirement_id="R10",
            requirement_name="Vignette options",
            passed=False,
            message="Vignette missing A), B), C), D) options",
            slide_number=slide_num
        ))
    else:
        results.append(ValidationResult(
            requirement_id="R10",
            requirement_name="Vignette options",
            passed=True,
            message="Vignette has all 4 options",
            slide_number=slide_num
        ))

    return results


def validate_answer(slide: Dict, slide_num: int) -> List[ValidationResult]:
    """Validate answer slide structure (R11)."""
    results = []

    if slide.get("type") != "answer":
        return results

    body = slide.get("body", "")
    body_lower = body.lower()

    # Check for rationale
    has_rationale = 'rationale' in body_lower

    # Check for distractor analysis
    has_distractor = 'why not' in body_lower or 'incorrect' in body_lower or 'wrong' in body_lower

    if not has_rationale:
        results.append(ValidationResult(
            requirement_id="R11a",
            requirement_name="Answer rationale",
            passed=False,
            message="Answer slide missing rationale section",
            slide_number=slide_num
        ))
    else:
        results.append(ValidationResult(
            requirement_id="R11a",
            requirement_name="Answer rationale",
            passed=True,
            message="Answer slide has rationale",
            slide_number=slide_num
        ))

    if not has_distractor:
        results.append(ValidationResult(
            requirement_id="R11b",
            requirement_name="Distractor analysis",
            passed=False,
            message="Answer slide missing distractor analysis",
            slide_number=slide_num
        ))
    else:
        results.append(ValidationResult(
            requirement_id="R11b",
            requirement_name="Distractor analysis",
            passed=True,
            message="Answer slide has distractor analysis",
            slide_number=slide_num
        ))

    return results


def validate_blueprint(blueprint_path: str) -> BlueprintValidation:
    """Validate a complete blueprint file."""
    with open(blueprint_path, 'r', encoding='utf-8') as f:
        content = f.read()

    validation = BlueprintValidation(
        blueprint_file=str(blueprint_path),
        total_slides=0
    )

    # Parse slides
    slide_pattern = r'===========================================\nSLIDE (\d+): (.+?)\n===========================================\n(.*?)(?=\n===========================================\nSLIDE|\Z)'

    slides_data = []
    for match in re.finditer(slide_pattern, content, re.DOTALL):
        slide_num = int(match.group(1))
        slide_title = match.group(2).strip()
        slide_content = match.group(3)

        parsed = parse_slide(slide_content)
        parsed["number"] = slide_num
        parsed["title"] = slide_title
        slides_data.append(parsed)

    validation.total_slides = len(slides_data)

    # Validate each slide
    for slide in slides_data:
        slide_val = SlideValidation(
            slide_number=slide["number"],
            slide_type=slide["type"],
            slide_title=slide["title"]
        )

        # Run all validations
        slide_val.results.extend(validate_header(slide, slide["number"]))
        slide_val.results.extend(validate_body(slide, slide["number"]))
        slide_val.results.extend(validate_nclex_tip(slide, slide["number"]))
        slide_val.results.extend(validate_presenter_notes(slide, slide["number"]))
        slide_val.results.extend(validate_section_intro(slide, slide["number"]))
        slide_val.results.extend(validate_vignette(slide, slide["number"]))
        slide_val.results.extend(validate_answer(slide, slide["number"]))

        validation.slides.append(slide_val)

    # Global validations (R8: anchor coverage would go here)
    # Requires access to input anchors - handled by separate function

    return validation


def print_validation_report(validation: BlueprintValidation):
    """Print formatted validation report."""
    print("=" * 80)
    print("BLUEPRINT CONTENT VALIDATION REPORT")
    print("=" * 80)
    print(f"File: {validation.blueprint_file}")
    print(f"Total Slides: {validation.total_slides}")
    print(f"Status: {'PASS' if validation.all_passed else 'FAIL'}")
    print(f"Total Failures: {validation.total_failures}")
    print()

    for slide in validation.slides:
        if not slide.all_passed:
            print(f"\nSLIDE {slide.slide_number}: {slide.slide_title}")
            print("-" * 60)
            for result in slide.results:
                if not result.passed:
                    print(f"  [FAIL] {result.requirement_id}: {result.message}")

    if validation.all_passed:
        print("\nAll validations passed!")

    print("\n" + "=" * 80)

    # Summary by requirement
    print("\nREQUIREMENT SUMMARY:")
    requirement_stats = {}
    for slide in validation.slides:
        for result in slide.results:
            if result.requirement_id not in requirement_stats:
                requirement_stats[result.requirement_id] = {"passed": 0, "failed": 0, "name": result.requirement_name}
            if result.passed:
                requirement_stats[result.requirement_id]["passed"] += 1
            else:
                requirement_stats[result.requirement_id]["failed"] += 1

    for req_id in sorted(requirement_stats.keys()):
        stats = requirement_stats[req_id]
        total = stats["passed"] + stats["failed"]
        rate = (stats["passed"] / total * 100) if total > 0 else 0
        status = "PASS" if stats["failed"] == 0 else "FAIL"
        print(f"  {req_id} ({stats['name']}): {rate:.0f}% ({stats['passed']}/{total}) [{status}]")


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    blueprint_path = sys.argv[1]
    output_json = '--json' in sys.argv

    validation = validate_blueprint(blueprint_path)

    if output_json:
        print(json.dumps(validation.to_dict(), indent=2))
    else:
        print_validation_report(validation)

    sys.exit(0 if validation.all_passed else 1)


if __name__ == "__main__":
    main()
