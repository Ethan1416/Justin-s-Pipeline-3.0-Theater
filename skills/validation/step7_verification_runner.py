"""
Step 7 Verification Runner
Validates formatting revision output against character and line constraints.
Executes 10 passes per requirement with parallel execution.

Usage:
    python step7_verification_runner.py <samples_folder>
    python step7_verification_runner.py <samples_folder> --json
    python step7_verification_runner.py <samples_folder> --verbose
"""

import re
import sys
import json
import time
from pathlib import Path
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Any, Callable, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed


# Step 7 specific requirements
REQUIREMENTS = [
    {"id": "F1", "name": "Header char limit (32)", "critical": True},
    {"id": "F2", "name": "Header line limit (2)", "critical": True},
    {"id": "F3", "name": "Body char limit (66)", "critical": True},
    {"id": "F4", "name": "Body line limit (8)", "critical": True},
    {"id": "F5", "name": "Tip char limit (66)", "critical": True},
    {"id": "F6", "name": "Tip line limit (2)", "critical": True},
    {"id": "F7", "name": "Notes word limit (450)", "critical": False},
    {"id": "F8", "name": "Changelog present", "critical": False},
    {"id": "F9", "name": "Revision summary present", "critical": False},
    {"id": "F10", "name": "All slides validated", "critical": True},
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
    """Parse blueprint/revision content into slides."""
    slides = []
    slide_pattern = r'===========================================\nSLIDE (\d+[A-Z]?): (.+?)\n===========================================\n(.*?)(?=\n===========================================\nSLIDE|\Z)'

    for match in re.finditer(slide_pattern, content, re.DOTALL):
        slide_num = match.group(1)
        slide_title = match.group(2).strip()
        slide_content = match.group(3)

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
            if tip_text and tip_text.lower() not in ['[none]', 'none', 'n/a']:
                tip = tip_text

        # Parse presenter notes
        notes_match = re.search(r'PRESENTER NOTES:\n(.*?)(?===|$)', slide_content, re.DOTALL)
        notes = notes_match.group(1).strip() if notes_match else ""

        slides.append({
            "number": slide_num,
            "title": slide_title,
            "header": header,
            "body": body,
            "nclex_tip": tip,
            "presenter_notes": notes
        })

    return slides


def check_f1_header_chars(slides: List[Dict], content: str) -> List[Dict]:
    """F1: Header max 32 chars per line."""
    issues = []
    for slide in slides:
        header = slide["header"]
        for i, line in enumerate(header.split('\n')):
            if line.strip() and len(line) > 32:
                issues.append({
                    "slide": slide["number"],
                    "issue": f"Header line {i+1} has {len(line)} chars (max 32)"
                })
    return issues


def check_f2_header_lines(slides: List[Dict], content: str) -> List[Dict]:
    """F2: Header max 2 lines."""
    issues = []
    for slide in slides:
        header = slide["header"]
        lines = [l for l in header.split('\n') if l.strip()]
        if len(lines) > 2:
            issues.append({
                "slide": slide["number"],
                "issue": f"Header has {len(lines)} lines (max 2)"
            })
    return issues


def check_f3_body_chars(slides: List[Dict], content: str) -> List[Dict]:
    """F3: Body max 66 chars per line."""
    issues = []
    for slide in slides:
        body = slide["body"]
        for i, line in enumerate(body.split('\n')):
            if line.strip() and len(line) > 66:
                issues.append({
                    "slide": slide["number"],
                    "issue": f"Body line {i+1} has {len(line)} chars (max 66)"
                })
    return issues


def check_f4_body_lines(slides: List[Dict], content: str) -> List[Dict]:
    """F4: Body max 8 non-empty lines."""
    issues = []
    for slide in slides:
        body = slide["body"]
        lines = [l for l in body.split('\n') if l.strip()]
        if len(lines) > 8:
            issues.append({
                "slide": slide["number"],
                "issue": f"Body has {len(lines)} lines (max 8)"
            })
    return issues


def check_f5_tip_chars(slides: List[Dict], content: str) -> List[Dict]:
    """F5: NCLEX tip max 66 chars per line."""
    issues = []
    for slide in slides:
        tip = slide["nclex_tip"]
        if tip:
            for i, line in enumerate(tip.split('\n')):
                if line.strip() and len(line) > 66:
                    issues.append({
                        "slide": slide["number"],
                        "issue": f"Tip line {i+1} has {len(line)} chars (max 66)"
                    })
    return issues


def check_f6_tip_lines(slides: List[Dict], content: str) -> List[Dict]:
    """F6: NCLEX tip max 2 lines."""
    issues = []
    for slide in slides:
        tip = slide["nclex_tip"]
        if tip:
            lines = [l for l in tip.split('\n') if l.strip()]
            if len(lines) > 2:
                issues.append({
                    "slide": slide["number"],
                    "issue": f"Tip has {len(lines)} lines (max 2)"
                })
    return issues


def check_f7_notes_words(slides: List[Dict], content: str) -> List[Dict]:
    """F7: Presenter notes max 450 words."""
    issues = []
    for slide in slides:
        notes = slide["presenter_notes"]
        # Remove markers for word count
        clean_notes = re.sub(r'\[[^\]]+\]', '', notes)
        word_count = len(clean_notes.split())
        if word_count > 450:
            issues.append({
                "slide": slide["number"],
                "issue": f"Notes have {word_count} words (max 450)"
            })
    return issues


def check_f8_changelog_present(slides: List[Dict], content: str) -> List[Dict]:
    """F8: Changelog section present."""
    issues = []
    if "CHANGELOG" not in content.upper() and "REVISION LOG" not in content.upper():
        # Also accept JSON-style changelog
        if '"changelog"' not in content.lower():
            issues.append({
                "slide": 0,
                "issue": "Changelog/revision log not found"
            })
    return issues


def check_f9_revision_summary(slides: List[Dict], content: str) -> List[Dict]:
    """F9: Revision summary present."""
    issues = []
    patterns = [
        r'REVISION SUMMARY',
        r'revision_summary',
        r'Slides revised:',
        r'slides_revised',
    ]
    found = any(re.search(p, content, re.IGNORECASE) for p in patterns)
    if not found:
        issues.append({
            "slide": 0,
            "issue": "Revision summary not found"
        })
    return issues


def check_f10_all_validated(slides: List[Dict], content: str) -> List[Dict]:
    """F10: All slides pass validation."""
    issues = []

    for slide in slides:
        slide_issues = []

        # Check header chars
        for line in slide["header"].split('\n'):
            if line.strip() and len(line) > 32:
                slide_issues.append("header chars")
                break

        # Check header lines
        if len([l for l in slide["header"].split('\n') if l.strip()]) > 2:
            slide_issues.append("header lines")

        # Check body chars
        for line in slide["body"].split('\n'):
            if line.strip() and len(line) > 66:
                slide_issues.append("body chars")
                break

        # Check body lines
        if len([l for l in slide["body"].split('\n') if l.strip()]) > 8:
            slide_issues.append("body lines")

        if slide_issues:
            issues.append({
                "slide": slide["number"],
                "issue": f"Validation failed: {', '.join(slide_issues)}"
            })

    return issues


# Map requirement IDs to check functions
REQUIREMENT_CHECKS = {
    "F1": check_f1_header_chars,
    "F2": check_f2_header_lines,
    "F3": check_f3_body_chars,
    "F4": check_f4_body_lines,
    "F5": check_f5_tip_chars,
    "F6": check_f6_tip_lines,
    "F7": check_f7_notes_words,
    "F8": check_f8_changelog_present,
    "F9": check_f9_revision_summary,
    "F10": check_f10_all_validated,
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
    # Look for Step 7 output files
    sample_files = list(samples_folder.glob("step7*.txt"))
    sample_files.extend(samples_folder.glob("*revised*.txt"))
    sample_files.extend(samples_folder.glob("*format*.txt"))

    # Deduplicate
    sample_files = list(set(sample_files))

    if not sample_files:
        # Fall back to any txt files
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
    print("STEP 7 FORMATTING VERIFICATION RESULTS")
    print("=" * 80)
    print()

    # Summary table
    print(f"{'Req':<6} {'Name':<30} {'Critical':<10} {'Pass Rate':<12} {'Status':<8}")
    print("-" * 75)

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

        print(f"{summary.requirement_id:<6} {summary.requirement_name:<30} {critical_str:<10} {pass_rate_str:<12} {summary.status:<8}")

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
                msg = failure['message'][:60] if len(failure['message']) > 60 else failure['message']
                print(f"  - {failure['file']} (pass {failure['pass']}): {msg}...")
                failure_count += 1

    if failure_count == 0:
        print("  No failures!")

    print()
    print("=" * 80)


def validate_single_file(file_path: Path) -> Dict[str, Any]:
    """Validate a single Step 7 output file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    slides = parse_slides(content)

    results = {}
    for req in REQUIREMENTS:
        check_func = REQUIREMENT_CHECKS.get(req["id"])
        if check_func:
            issues = check_func(slides, content)
            results[req["id"]] = {
                "name": req["name"],
                "passed": len(issues) == 0,
                "issues": issues
            }

    return results


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
