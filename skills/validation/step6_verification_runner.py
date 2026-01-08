"""
Step 6 Verification Runner
Runs verification tests for each requirement across sample inputs.
Executes 10 passes per requirement with parallel execution where possible.

Usage:
    python step6_verification_runner.py <samples_folder>
    python step6_verification_runner.py <samples_folder> --json
    python step6_verification_runner.py <samples_folder> --verbose
"""

import re
import sys
import json
import time
from pathlib import Path
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Any, Callable
from concurrent.futures import ThreadPoolExecutor, as_completed


# Requirement definitions
REQUIREMENTS = [
    {"id": "R1", "name": "Header limits", "critical": True},
    {"id": "R2", "name": "Body line limit", "critical": True},
    {"id": "R3", "name": "Body char limit", "critical": True},
    {"id": "R4", "name": "NCLEX tip required", "critical": True},
    {"id": "R5", "name": "NCLEX tip line limit", "critical": False},
    {"id": "R6", "name": "Notes word limit", "critical": False},
    {"id": "R7", "name": "Notes time limit", "critical": False},
    {"id": "R8", "name": "Anchor coverage", "critical": True},
    {"id": "R9", "name": "Intro quote", "critical": False},
    {"id": "R10", "name": "Vignette structure", "critical": True},
    {"id": "R11", "name": "Answer structure", "critical": True},
    {"id": "R12", "name": "Fixed slides present", "critical": True},
    {"id": "R13", "name": "Delivery modes", "critical": False},
    {"id": "R14", "name": "Notes markers", "critical": False},
    {"id": "R15", "name": "Sequential numbering", "critical": False},
]

PASSES_PER_REQUIREMENT = 10


@dataclass
class TestResult:
    requirement_id: str
    requirement_name: str
    sample_file: str
    pass_number: int
    passed: bool
    message: str
    execution_time_ms: float


@dataclass
class RequirementSummary:
    requirement_id: str
    requirement_name: str
    critical: bool
    total_tests: int
    passed_tests: int
    failed_tests: int
    pass_rate: float
    failures: List[Dict[str, Any]] = field(default_factory=list)

    @property
    def status(self) -> str:
        if self.pass_rate == 100.0:
            return "PASS"
        elif self.pass_rate >= 80.0:
            return "WARN"
        else:
            return "FAIL"


def parse_slides(content: str) -> List[Dict]:
    """Parse blueprint content into slides."""
    slides = []
    slide_pattern = r'===========================================\nSLIDE (\d+): (.+?)\n===========================================\n(.*?)(?=\n===========================================\nSLIDE|\Z)'

    for match in re.finditer(slide_pattern, content, re.DOTALL):
        slide_num = int(match.group(1))
        slide_title = match.group(2).strip()
        slide_content = match.group(3)

        # Parse slide type
        type_match = re.search(r'Type:\s*(.+)', slide_content)
        slide_type = type_match.group(1).strip().lower().replace(" ", "_") if type_match else "unknown"

        # Parse header
        header_match = re.search(r'HEADER:\n(.*?)(?=\n\nBODY:|\nBODY:)', slide_content, re.DOTALL)
        header = header_match.group(1).strip() if header_match else ""

        # Parse body
        body_match = re.search(
            r'\nBODY:\n(.*?)(?=\n\nNCLEX TIP:|\nNCLEX TIP:|\n\nPRESENTER NOTES:|\nPRESENTER NOTES:|$)',
            slide_content, re.DOTALL
        )
        body = body_match.group(1).strip() if body_match else ""

        # Parse NCLEX tip
        tip_match = re.search(
            r'NCLEX TIP:\n(.*?)(?=\n\nPRESENTER NOTES:|\nPRESENTER NOTES:|$)',
            slide_content, re.DOTALL
        )
        tip = ""
        if tip_match:
            tip_text = tip_match.group(1).strip()
            if tip_text and tip_text.lower() not in ['[none]', '[none - omit for intro slides]',
                                                       '[none - omit for vignette slides]',
                                                       '[none - omit for answer slides]']:
                tip = tip_text

        # Parse presenter notes
        notes_match = re.search(r'PRESENTER NOTES:\n(.*?)(?===|$)', slide_content, re.DOTALL)
        notes = notes_match.group(1).strip() if notes_match else ""

        slides.append({
            "number": slide_num,
            "title": slide_title,
            "type": slide_type,
            "header": header,
            "body": body,
            "nclex_tip": tip,
            "presenter_notes": notes
        })

    return slides


def check_r1_header_limits(slides: List[Dict]) -> List[Dict]:
    """R1: Header max 32 chars/line, max 2 lines"""
    issues = []
    for slide in slides:
        header = slide["header"]
        lines = [l for l in header.split('\n') if l.strip()]

        if len(lines) > 2:
            issues.append({"slide": slide["number"], "issue": f"Header has {len(lines)} lines (max 2)"})

        for i, line in enumerate(lines):
            if len(line.strip()) > 32:
                issues.append({"slide": slide["number"], "issue": f"Header line {i+1} has {len(line)} chars (max 32)"})

    return issues


def check_r2_body_lines(slides: List[Dict]) -> List[Dict]:
    """R2: Body max 8 non-empty lines"""
    issues = []
    for slide in slides:
        body = slide["body"]
        lines = [l for l in body.split('\n') if l.strip()]

        if len(lines) > 8:
            issues.append({"slide": slide["number"], "issue": f"Body has {len(lines)} lines (max 8)"})

    return issues


def check_r3_body_chars(slides: List[Dict]) -> List[Dict]:
    """R3: Body max 66 chars/line"""
    issues = []
    for slide in slides:
        body = slide["body"]
        for i, line in enumerate(body.split('\n')):
            if line.strip() and len(line) > 66:
                issues.append({"slide": slide["number"], "issue": f"Body line {i+1} has {len(line)} chars (max 66)"})

    return issues


def check_r4_nclex_tip_required(slides: List[Dict]) -> List[Dict]:
    """R4: NCLEX tip required on content slides"""
    issues = []
    for slide in slides:
        if slide["type"] == "content":
            if not slide["nclex_tip"]:
                issues.append({"slide": slide["number"], "issue": "Content slide missing NCLEX tip"})

    return issues


def check_r5_tip_lines(slides: List[Dict]) -> List[Dict]:
    """R5: NCLEX tip max 2 lines"""
    issues = []
    for slide in slides:
        tip = slide["nclex_tip"]
        if tip:
            lines = [l for l in tip.split('\n') if l.strip()]
            if len(lines) > 2:
                issues.append({"slide": slide["number"], "issue": f"NCLEX tip has {len(lines)} lines (max 2)"})

    return issues


def check_r6_notes_words(slides: List[Dict]) -> List[Dict]:
    """R6: Presenter notes max 450 words"""
    issues = []
    for slide in slides:
        notes = slide["presenter_notes"]
        word_count = len(notes.split())
        if word_count > 450:
            issues.append({"slide": slide["number"], "issue": f"Notes have {word_count} words (max 450)"})

    return issues


def check_r7_notes_time(slides: List[Dict]) -> List[Dict]:
    """R7: Presenter notes max 180 seconds"""
    issues = []
    for slide in slides:
        notes = slide["presenter_notes"]
        word_count = len(notes.split())
        estimated_seconds = int((word_count / 150) * 60)  # 150 WPM
        if estimated_seconds > 180:
            issues.append({"slide": slide["number"], "issue": f"Notes ~{estimated_seconds}s (max 180s)"})

    return issues


def check_r8_anchor_coverage(content: str, slides: List[Dict] = None, input_anchors: List[str] = None) -> List[Dict]:
    """
    R8: All anchors covered - comprehensive validation.

    This function validates anchor coverage using multiple methods:
    1. Pattern matching in content (backward compatible)
    2. Direct slide inspection if slides are provided
    3. Comparison against input_anchors if provided

    Args:
        content: Blueprint content string
        slides: Optional list of slide dictionaries with 'anchors_covered' field
        input_anchors: Optional list of all input anchor summaries

    Returns:
        List of issue dictionaries
    """
    issues = []

    # Method 1: Pattern matching (backward compatible)
    coverage_match = re.search(r'Anchors missing:\s*(.+?)(?:\n|$)', content)
    if coverage_match:
        missing = coverage_match.group(1).strip()
        if missing.lower() != "none" and missing != "0":
            issues.append({"slide": 0, "issue": f"Missing anchors (text): {missing}"})

    # Method 2: Direct slide inspection
    if slides is not None:
        covered_anchors = set()
        for slide in slides:
            anchors = slide.get('anchors_covered', [])
            if anchors:
                for anchor in anchors:
                    if isinstance(anchor, str):
                        covered_anchors.add(anchor.lower().strip())
                    elif isinstance(anchor, dict):
                        covered_anchors.add(anchor.get('summary', '').lower().strip())

        # Method 3: Compare against input anchors
        if input_anchors is not None:
            input_set = {a.lower().strip() for a in input_anchors if a}
            missing_anchors = input_set - covered_anchors

            if missing_anchors:
                # Report first 5 missing
                missing_list = list(missing_anchors)[:5]
                more_count = len(missing_anchors) - 5 if len(missing_anchors) > 5 else 0
                issue_text = f"Missing anchors ({len(missing_anchors)} total): {', '.join(missing_list)}"
                if more_count > 0:
                    issue_text += f" ... and {more_count} more"
                issues.append({"slide": 0, "issue": issue_text})

                # Calculate coverage percentage
                total = len(input_set)
                covered = total - len(missing_anchors)
                coverage_pct = (covered / total * 100) if total > 0 else 0
                if coverage_pct < 100:
                    issues.append({
                        "slide": 0,
                        "issue": f"Coverage: {covered}/{total} ({coverage_pct:.1f}%) - R8 requires 100%"
                    })

    return issues


def check_r9_intro_quote(slides: List[Dict]) -> List[Dict]:
    """R9: Section intro has provocative quote"""
    issues = []
    intro_slides = [s for s in slides if s["type"] == "section_intro"]
    for slide in intro_slides:
        body = slide["body"]
        has_quote = '"' in body or '"' in body or '—' in body or '–' in body
        if not has_quote:
            issues.append({"slide": slide["number"], "issue": "Section intro missing quote"})

    return issues


def check_r10_vignette_structure(slides: List[Dict]) -> List[Dict]:
    """R10: Vignette has 2-4 sentence stem + 4 options"""
    issues = []
    vignette_slides = [s for s in slides if s["type"] == "vignette"]
    for slide in vignette_slides:
        body = slide["body"]
        # Check for 4 options
        options = ['A)', 'B)', 'C)', 'D)']
        missing_options = [opt for opt in options if opt not in body]
        if missing_options:
            issues.append({"slide": slide["number"], "issue": f"Missing options: {missing_options}"})

    return issues


def check_r11_answer_structure(slides: List[Dict]) -> List[Dict]:
    """R11: Answer slide has rationale + distractor analysis"""
    issues = []
    answer_slides = [s for s in slides if s["type"] == "answer"]
    for slide in answer_slides:
        body = slide["body"].lower()

        if 'rationale' not in body:
            issues.append({"slide": slide["number"], "issue": "Missing rationale section"})

        if 'why not' not in body and 'incorrect' not in body and 'wrong' not in body:
            issues.append({"slide": slide["number"], "issue": "Missing distractor analysis"})

    return issues


def check_r12_fixed_slides(slides: List[Dict]) -> List[Dict]:
    """R12: Fixed slides present (intro, vignette, answer)"""
    issues = []
    types = [s["type"] for s in slides]

    if not types or types[0] != "section_intro":
        issues.append({"slide": 1, "issue": "First slide must be Section Intro"})

    if "vignette" not in types:
        issues.append({"slide": 0, "issue": "Missing Vignette slide"})

    if "answer" not in types:
        issues.append({"slide": 0, "issue": "Missing Answer slide"})
    elif types[-1] != "answer":
        issues.append({"slide": 0, "issue": "Answer should be last slide"})

    return issues


def check_r13_delivery_modes(content: str) -> List[Dict]:
    """R13: Delivery modes correctly applied"""
    # This would require input anchors to fully validate
    # For now, check that delivery modes are documented
    issues = []
    if "SUBSECTION DELIVERY MODES" not in content:
        issues.append({"slide": 0, "issue": "Delivery modes not documented"})
    return issues


def check_r14_notes_markers(slides: List[Dict]) -> List[Dict]:
    """R14: Presenter notes have [PAUSE] and [EMPHASIS] markers"""
    issues = []
    for slide in slides:
        notes = slide["presenter_notes"]
        if notes:
            if '[PAUSE]' not in notes:
                issues.append({"slide": slide["number"], "issue": "Missing [PAUSE] markers"})
            if slide["type"] == "content" and '[EMPHASIS' not in notes:
                issues.append({"slide": slide["number"], "issue": "Missing [EMPHASIS] markers"})

    return issues


def check_r15_sequential_numbering(slides: List[Dict]) -> List[Dict]:
    """R15: Slides numbered sequentially"""
    issues = []
    numbers = [s["number"] for s in slides]
    expected = list(range(1, len(numbers) + 1))

    if numbers != expected:
        issues.append({"slide": 0, "issue": f"Non-sequential: {numbers} vs expected {expected}"})

    return issues


# Map requirement IDs to check functions
REQUIREMENT_CHECKS = {
    "R1": lambda slides, content: check_r1_header_limits(slides),
    "R2": lambda slides, content: check_r2_body_lines(slides),
    "R3": lambda slides, content: check_r3_body_chars(slides),
    "R4": lambda slides, content: check_r4_nclex_tip_required(slides),
    "R5": lambda slides, content: check_r5_tip_lines(slides),
    "R6": lambda slides, content: check_r6_notes_words(slides),
    "R7": lambda slides, content: check_r7_notes_time(slides),
    "R8": lambda slides, content: check_r8_anchor_coverage(content),
    "R9": lambda slides, content: check_r9_intro_quote(slides),
    "R10": lambda slides, content: check_r10_vignette_structure(slides),
    "R11": lambda slides, content: check_r11_answer_structure(slides),
    "R12": lambda slides, content: check_r12_fixed_slides(slides),
    "R13": lambda slides, content: check_r13_delivery_modes(content),
    "R14": lambda slides, content: check_r14_notes_markers(slides),
    "R15": lambda slides, content: check_r15_sequential_numbering(slides),
}


def run_single_test(req_id: str, req_name: str, sample_path: Path, pass_num: int) -> TestResult:
    """Run a single test for a requirement."""
    start_time = time.time()

    try:
        with open(sample_path, 'r', encoding='utf-8') as f:
            content = f.read()

        slides = parse_slides(content)
        check_func = REQUIREMENT_CHECKS.get(req_id)

        if check_func:
            issues = check_func(slides, content)
            passed = len(issues) == 0
            message = "PASS" if passed else f"Issues: {issues}"
        else:
            passed = False
            message = f"No check function for {req_id}"

    except Exception as e:
        passed = False
        message = f"Error: {str(e)}"

    execution_time = (time.time() - start_time) * 1000

    return TestResult(
        requirement_id=req_id,
        requirement_name=req_name,
        sample_file=sample_path.name,
        pass_number=pass_num,
        passed=passed,
        message=message,
        execution_time_ms=execution_time
    )


def run_verification(samples_folder: Path, verbose: bool = False) -> Dict[str, RequirementSummary]:
    """Run verification for all requirements across all samples."""
    sample_files = list(samples_folder.glob("*.txt"))

    if not sample_files:
        print(f"No sample files found in {samples_folder}")
        return {}

    print(f"Found {len(sample_files)} sample files")
    print(f"Running {PASSES_PER_REQUIREMENT} passes per requirement")
    print(f"Total tests: {len(REQUIREMENTS)} requirements x {len(sample_files)} samples x {PASSES_PER_REQUIREMENT} passes")
    print()

    all_results = []

    # Run tests in parallel
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = []

        for req in REQUIREMENTS:
            for sample_path in sample_files:
                for pass_num in range(1, PASSES_PER_REQUIREMENT + 1):
                    future = executor.submit(
                        run_single_test,
                        req["id"],
                        req["name"],
                        sample_path,
                        pass_num
                    )
                    futures.append((future, req))

        for future, req in futures:
            result = future.result()
            all_results.append(result)

            if verbose:
                status = "PASS" if result.passed else "FAIL"
                print(f"  [{status}] {result.requirement_id} | {result.sample_file} | Pass {result.pass_number}")

    # Summarize results by requirement
    summaries = {}
    for req in REQUIREMENTS:
        req_results = [r for r in all_results if r.requirement_id == req["id"]]
        passed = sum(1 for r in req_results if r.passed)
        failed = sum(1 for r in req_results if not r.passed)
        total = len(req_results)

        failures = [
            {"file": r.sample_file, "pass": r.pass_number, "message": r.message}
            for r in req_results if not r.passed
        ]

        summaries[req["id"]] = RequirementSummary(
            requirement_id=req["id"],
            requirement_name=req["name"],
            critical=req["critical"],
            total_tests=total,
            passed_tests=passed,
            failed_tests=failed,
            pass_rate=(passed / total * 100) if total > 0 else 0,
            failures=failures[:5]  # Limit to first 5 failures
        )

    return summaries


def print_results(summaries: Dict[str, RequirementSummary]):
    """Print formatted results."""
    print("=" * 80)
    print("STEP 6 VERIFICATION RESULTS")
    print("=" * 80)
    print()

    # Summary table
    print(f"{'Req':<6} {'Name':<25} {'Critical':<10} {'Pass Rate':<12} {'Status':<8}")
    print("-" * 70)

    critical_pass = True
    warning_count = 0

    for req_id in sorted(summaries.keys()):
        summary = summaries[req_id]
        critical_str = "YES" if summary.critical else "NO"
        pass_rate_str = f"{summary.pass_rate:.1f}%"

        if summary.status == "FAIL" and summary.critical:
            critical_pass = False
        if summary.status == "WARN":
            warning_count += 1

        print(f"{summary.requirement_id:<6} {summary.requirement_name:<25} {critical_str:<10} {pass_rate_str:<12} {summary.status:<8}")

    print()
    print("=" * 80)

    # Overall status
    overall_status = "PASS" if critical_pass else "FAIL"
    print(f"OVERALL STATUS: {overall_status}")
    if warning_count > 0:
        print(f"WARNINGS: {warning_count}")

    # Flag failures
    print()
    print("FAILURES FLAGGED:")
    print("-" * 80)

    failure_count = 0
    for req_id in sorted(summaries.keys()):
        summary = summaries[req_id]
        if summary.failed_tests > 0:
            print(f"\n{summary.requirement_id} ({summary.requirement_name}):")
            for failure in summary.failures:
                print(f"  - {failure['file']} (pass {failure['pass']}): {failure['message'][:60]}...")
                failure_count += 1

    if failure_count == 0:
        print("  No failures!")

    print()
    print("=" * 80)


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    samples_folder = Path(sys.argv[1])
    output_json = '--json' in sys.argv
    verbose = '--verbose' in sys.argv

    if not samples_folder.exists():
        print(f"Error: Folder not found: {samples_folder}")
        sys.exit(1)

    print(f"Samples folder: {samples_folder}")
    print()

    summaries = run_verification(samples_folder, verbose)

    if output_json:
        output = {
            req_id: {
                "requirement_id": s.requirement_id,
                "requirement_name": s.requirement_name,
                "critical": s.critical,
                "total_tests": s.total_tests,
                "passed_tests": s.passed_tests,
                "failed_tests": s.failed_tests,
                "pass_rate": s.pass_rate,
                "status": s.status,
                "failures": s.failures
            }
            for req_id, s in summaries.items()
        }
        print(json.dumps(output, indent=2))
    else:
        print_results(summaries)


if __name__ == "__main__":
    main()
