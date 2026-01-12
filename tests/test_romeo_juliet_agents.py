"""
Romeo and Juliet Agent Verification Tests
==========================================

Runs parallel verification tests for all R&J unit agents.
- 1 agent per requirement
- 10 passes each
- Parallel execution
- Outputs pass rates and flags failures
"""

import sys
import yaml
import json
import time
import traceback
from pathlib import Path
from typing import Any, Dict, List, Tuple
from dataclasses import dataclass, field
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from agents import (
    SceneCutterAgent,
    SceneSummaryGeneratorAgent,
    ReadingDayGeneratorAgent,
    ActivityDayGeneratorAgent,
    DifferentiationSelectorAgent,
    WeekPlannerAgent,
    TextExcerptSelectorAgent,
    RJUnitValidatorAgent,
)


# =============================================================================
# TEST CONFIGURATION
# =============================================================================

PASSES_PER_TEST = 10
MAX_WORKERS = 8  # Parallel execution threads


@dataclass
class TestResult:
    """Result of a single test execution."""
    agent_name: str
    sample_id: str
    pass_number: int
    passed: bool
    duration_ms: float
    error_message: str = ""
    output: Dict = field(default_factory=dict)


@dataclass
class AgentTestSummary:
    """Summary of all tests for an agent."""
    agent_name: str
    total_tests: int = 0
    passed_tests: int = 0
    failed_tests: int = 0
    pass_rate: float = 0.0
    avg_duration_ms: float = 0.0
    failures: List[TestResult] = field(default_factory=list)


# =============================================================================
# AGENT MAPPING
# =============================================================================

AGENT_MAP = {
    "SceneCutterAgent": SceneCutterAgent,
    "SceneSummaryGeneratorAgent": SceneSummaryGeneratorAgent,
    "ReadingDayGeneratorAgent": ReadingDayGeneratorAgent,
    "ActivityDayGeneratorAgent": ActivityDayGeneratorAgent,
    "DifferentiationSelectorAgent": DifferentiationSelectorAgent,
    "WeekPlannerAgent": WeekPlannerAgent,
    "TextExcerptSelectorAgent": TextExcerptSelectorAgent,
    "RJUnitValidatorAgent": RJUnitValidatorAgent,
}


# =============================================================================
# TEST VALIDATION HELPERS
# =============================================================================

def validate_output(output: Dict, expected: Dict) -> Tuple[bool, str]:
    """
    Validate agent output against expected values.

    Supports special validation syntax:
    - "length >= N" - checks list/dict length
    - "length == N" - checks exact length
    - "contains: text" - checks if text is in value
    - "has keys: key1, key2" - checks dict has keys
    - "not empty" - checks value is truthy
    - true/false - boolean comparison
    - Direct value comparison otherwise
    """
    errors = []

    for key, expected_value in expected.items():
        if key not in output:
            # Try nested access
            actual_value = get_nested_value(output, key)
            if actual_value is None:
                errors.append(f"Missing key: {key}")
                continue
        else:
            actual_value = output[key]

        # Handle special validation syntax
        if isinstance(expected_value, str):
            if expected_value.startswith("length "):
                if not validate_length(actual_value, expected_value):
                    errors.append(f"{key}: {expected_value} failed (got {len(actual_value) if hasattr(actual_value, '__len__') else 'N/A'})")
            elif expected_value.startswith("contains:"):
                search_text = expected_value.replace("contains:", "").strip()
                if not contains_text(actual_value, search_text):
                    errors.append(f"{key}: should contain '{search_text}'")
            elif expected_value.startswith("has keys:"):
                required_keys = [k.strip() for k in expected_value.replace("has keys:", "").split(",")]
                if not all(k in actual_value for k in required_keys):
                    errors.append(f"{key}: missing required keys")
            elif expected_value == "not empty":
                if not actual_value:
                    errors.append(f"{key}: should not be empty")
            elif expected_value.startswith("not "):
                forbidden = expected_value.replace("not ", "")
                if actual_value == forbidden:
                    errors.append(f"{key}: should not be '{forbidden}'")
            else:
                # Direct comparison
                if str(actual_value) != expected_value:
                    errors.append(f"{key}: expected '{expected_value}', got '{actual_value}'")
        elif isinstance(expected_value, bool):
            if actual_value != expected_value:
                errors.append(f"{key}: expected {expected_value}, got {actual_value}")
        elif isinstance(expected_value, (int, float)):
            if actual_value != expected_value:
                errors.append(f"{key}: expected {expected_value}, got {actual_value}")
        elif isinstance(expected_value, list):
            for item in expected_value:
                if isinstance(item, dict) and "contains" in str(item):
                    # Check if any item in actual list contains the expected text
                    pass  # Complex validation - skip for now
        elif isinstance(expected_value, dict):
            # Recursive validation
            nested_valid, nested_errors = validate_output(actual_value, expected_value)
            if not nested_valid:
                errors.extend([f"{key}.{e}" for e in nested_errors.split("; ")])

    return len(errors) == 0, "; ".join(errors)


def get_nested_value(data: Dict, key_path: str) -> Any:
    """Get value from nested dict using dot notation."""
    keys = key_path.split(".")
    value = data
    for key in keys:
        if isinstance(value, dict) and key in value:
            value = value[key]
        else:
            return None
    return value


def validate_length(value: Any, condition: str) -> bool:
    """Validate length conditions like 'length >= 3'."""
    if not hasattr(value, '__len__'):
        return False

    actual_len = len(value)

    if ">=" in condition:
        expected = int(condition.split(">=")[1].strip())
        return actual_len >= expected
    elif "==" in condition:
        expected = int(condition.split("==")[1].strip())
        return actual_len == expected
    elif "<=" in condition:
        expected = int(condition.split("<=")[1].strip())
        return actual_len <= expected
    elif ">" in condition:
        expected = int(condition.split(">")[1].strip())
        return actual_len > expected
    elif "<" in condition:
        expected = int(condition.split("<")[1].strip())
        return actual_len < expected

    return False


def contains_text(value: Any, search: str) -> bool:
    """Check if value contains search text."""
    if isinstance(value, str):
        return search.lower() in value.lower()
    elif isinstance(value, list):
        return any(contains_text(item, search) for item in value)
    elif isinstance(value, dict):
        return any(contains_text(v, search) for v in value.values())
    return False


# =============================================================================
# TEST EXECUTION
# =============================================================================

def run_single_test(
    agent_class: type,
    sample: Dict,
    pass_number: int
) -> TestResult:
    """Run a single test pass for an agent."""
    agent_name = agent_class.__name__
    sample_id = sample.get("id", "unknown")

    start_time = time.time()

    try:
        # Create agent instance
        agent = agent_class()

        # Execute agent with sample input
        result = agent.execute(sample.get("input", {}))

        duration_ms = (time.time() - start_time) * 1000

        # Validate output against expected
        expected = sample.get("expected_output", {})
        if expected:
            valid, error_msg = validate_output(result.output, expected)
        else:
            valid = result.status.value == "completed"
            error_msg = "" if valid else "Agent did not complete successfully"

        return TestResult(
            agent_name=agent_name,
            sample_id=sample_id,
            pass_number=pass_number,
            passed=valid,
            duration_ms=duration_ms,
            error_message=error_msg if not valid else "",
            output=result.output
        )

    except Exception as e:
        duration_ms = (time.time() - start_time) * 1000
        return TestResult(
            agent_name=agent_name,
            sample_id=sample_id,
            pass_number=pass_number,
            passed=False,
            duration_ms=duration_ms,
            error_message=f"Exception: {str(e)}\n{traceback.format_exc()}"
        )


def run_agent_tests(
    agent_name: str,
    samples: List[Dict],
    passes: int = PASSES_PER_TEST
) -> AgentTestSummary:
    """Run all tests for a single agent."""
    agent_class = AGENT_MAP.get(agent_name)
    if not agent_class:
        return AgentTestSummary(
            agent_name=agent_name,
            failures=[TestResult(
                agent_name=agent_name,
                sample_id="N/A",
                pass_number=0,
                passed=False,
                duration_ms=0,
                error_message=f"Unknown agent: {agent_name}"
            )]
        )

    results: List[TestResult] = []

    # Run tests in parallel for each sample
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = []
        for sample in samples:
            for pass_num in range(1, passes + 1):
                future = executor.submit(
                    run_single_test,
                    agent_class,
                    sample,
                    pass_num
                )
                futures.append(future)

        for future in as_completed(futures):
            results.append(future.result())

    # Calculate summary
    total = len(results)
    passed = sum(1 for r in results if r.passed)
    failed = total - passed
    durations = [r.duration_ms for r in results]

    summary = AgentTestSummary(
        agent_name=agent_name,
        total_tests=total,
        passed_tests=passed,
        failed_tests=failed,
        pass_rate=(passed / total * 100) if total > 0 else 0,
        avg_duration_ms=sum(durations) / len(durations) if durations else 0,
        failures=[r for r in results if not r.passed]
    )

    return summary


# =============================================================================
# MAIN TEST RUNNER
# =============================================================================

def load_test_samples() -> Dict[str, List[Dict]]:
    """Load test samples from YAML file."""
    samples_path = Path(__file__).parent.parent / "samples" / "romeo_juliet_test_samples.yaml"

    if not samples_path.exists():
        print(f"ERROR: Test samples file not found: {samples_path}")
        return {}

    with open(samples_path, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)

    # Extract samples by agent
    samples_by_agent = {}

    for key, value in data.items():
        if key.endswith("_agent") and isinstance(value, dict):
            agent_name = value.get("agent_name", "")
            test_samples = value.get("test_samples", [])
            if agent_name and test_samples:
                samples_by_agent[agent_name] = test_samples

    return samples_by_agent


def run_all_tests() -> Dict[str, AgentTestSummary]:
    """Run all verification tests in parallel."""
    print("=" * 70)
    print("ROMEO AND JULIET AGENT VERIFICATION TESTS")
    print(f"Started: {datetime.now().isoformat()}")
    print(f"Passes per test: {PASSES_PER_TEST}")
    print(f"Max parallel workers: {MAX_WORKERS}")
    print("=" * 70)
    print()

    # Load samples
    samples_by_agent = load_test_samples()

    if not samples_by_agent:
        print("ERROR: No test samples found!")
        return {}

    print(f"Loaded samples for {len(samples_by_agent)} agents")
    for agent, samples in samples_by_agent.items():
        print(f"  - {agent}: {len(samples)} samples")
    print()

    # Run all agent tests in parallel
    all_summaries: Dict[str, AgentTestSummary] = {}

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = {
            executor.submit(run_agent_tests, agent_name, samples): agent_name
            for agent_name, samples in samples_by_agent.items()
        }

        for future in as_completed(futures):
            agent_name = futures[future]
            try:
                summary = future.result()
                all_summaries[agent_name] = summary
                print(f"Completed: {agent_name}")
            except Exception as e:
                print(f"ERROR testing {agent_name}: {e}")

    return all_summaries


def print_results(summaries: Dict[str, AgentTestSummary]) -> int:
    """Print test results and return exit code."""
    print()
    print("=" * 70)
    print("TEST RESULTS")
    print("=" * 70)
    print()

    total_tests = 0
    total_passed = 0
    total_failed = 0
    all_failures = []

    # Print per-agent results
    for agent_name, summary in sorted(summaries.items()):
        total_tests += summary.total_tests
        total_passed += summary.passed_tests
        total_failed += summary.failed_tests

        status = "PASS" if summary.failed_tests == 0 else "FAIL"
        status_icon = "[OK]" if status == "PASS" else "[XX]"

        print(f"{status_icon} {agent_name}")
        print(f"    Tests: {summary.total_tests} | Passed: {summary.passed_tests} | Failed: {summary.failed_tests}")
        print(f"    Pass Rate: {summary.pass_rate:.1f}% | Avg Duration: {summary.avg_duration_ms:.2f}ms")

        if summary.failures:
            all_failures.extend(summary.failures)
            # Show first 2 failures per agent
            for failure in summary.failures[:2]:
                print(f"    FAILURE [{failure.sample_id}]: {failure.error_message[:80]}")
        print()

    # Print overall summary
    print("=" * 70)
    print("OVERALL SUMMARY")
    print("=" * 70)
    overall_pass_rate = (total_passed / total_tests * 100) if total_tests > 0 else 0

    print(f"Total Tests:  {total_tests}")
    print(f"Passed:       {total_passed}")
    print(f"Failed:       {total_failed}")
    print(f"Pass Rate:    {overall_pass_rate:.1f}%")
    print()

    if total_failed > 0:
        print("=" * 70)
        print("FAILURE DETAILS")
        print("=" * 70)
        for i, failure in enumerate(all_failures[:10]):  # Show first 10 failures
            print(f"\n[{i+1}] {failure.agent_name} - {failure.sample_id} (Pass {failure.pass_number})")
            print(f"    Error: {failure.error_message}")

        if len(all_failures) > 10:
            print(f"\n... and {len(all_failures) - 10} more failures")

    # Return exit code
    return 0 if total_failed == 0 else 1


def save_results(summaries: Dict[str, AgentTestSummary]):
    """Save detailed results to JSON file."""
    output_path = Path(__file__).parent.parent / "test_output" / "rj_verification_results.json"
    output_path.parent.mkdir(exist_ok=True)

    results = {
        "timestamp": datetime.now().isoformat(),
        "config": {
            "passes_per_test": PASSES_PER_TEST,
            "max_workers": MAX_WORKERS
        },
        "summaries": {}
    }

    for agent_name, summary in summaries.items():
        results["summaries"][agent_name] = {
            "total_tests": summary.total_tests,
            "passed_tests": summary.passed_tests,
            "failed_tests": summary.failed_tests,
            "pass_rate": summary.pass_rate,
            "avg_duration_ms": summary.avg_duration_ms,
            "failures": [
                {
                    "sample_id": f.sample_id,
                    "pass_number": f.pass_number,
                    "error_message": f.error_message
                }
                for f in summary.failures
            ]
        }

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2)

    print(f"\nDetailed results saved to: {output_path}")


# =============================================================================
# ENTRY POINT
# =============================================================================

if __name__ == "__main__":
    summaries = run_all_tests()
    save_results(summaries)
    exit_code = print_results(summaries)
    sys.exit(exit_code)
