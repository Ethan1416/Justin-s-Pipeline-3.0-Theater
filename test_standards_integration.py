#!/usr/bin/env python3
"""
Integration Test Script - Standards Parser Module
Tests the standards_parser.py module across 5 test categories, 10 rounds each
"""

import json
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from skills.parsing.standards_parser import StandardsParser, parse_standards, ParsedStandards


def test_1_module_import():
    """Test 1: Module imports without error"""
    try:
        from skills.parsing.standards_parser import StandardsParser, parse_standards
        return True, "Module imported successfully"
    except Exception as e:
        return False, f"Import failed: {e}"


def test_2_parse_all_standards():
    """Test 2: parse_all_standards() returns success=True"""
    try:
        parser = StandardsParser()
        result = parser.parse_all_standards()

        if not isinstance(result, ParsedStandards):
            return False, f"Expected ParsedStandards, got {type(result)}"

        if result.success:
            return True, f"Parse successful. Found {len(result.delivery_modes)} delivery modes"
        else:
            return False, f"Parse failed: {result.errors}"
    except Exception as e:
        return False, f"Exception: {e}"


def test_3_apply_standards_output():
    """Test 3: apply_standards_to_outline() produces valid output structure"""
    try:
        # Load sample input
        input_file = project_root / "inputs" / "sample_nclex" / "sample_standards_input.json"
        if not input_file.exists():
            return False, f"Sample input file not found: {input_file}"

        with open(input_file, 'r') as f:
            outline = json.load(f)

        parser = StandardsParser()
        output = parser.apply_standards_to_outline(outline)

        # Validate structure
        required_keys = ["metadata", "sessions", "delivery_summary", "character_limits", "validation"]
        for key in required_keys:
            if key not in output:
                return False, f"Missing key '{key}' in output"

        # Validate metadata
        if "step" not in output["metadata"]:
            return False, "Missing metadata.step"

        # Validate sessions
        if not isinstance(output["sessions"], list):
            return False, "sessions is not a list"

        # Validate subsections have required fields
        for session in output["sessions"]:
            for section in session.get("sections", []):
                for subsection in section.get("subsections", []):
                    required_sub_keys = ["delivery_mode", "anchor_delivery", "active_learning", "presenter_notes_requirements"]
                    for key in required_sub_keys:
                        if key not in subsection:
                            return False, f"Missing key '{key}' in subsection {subsection.get('subsection_id')}"

        return True, "Output structure valid with all required fields"
    except Exception as e:
        return False, f"Exception: {e}"


def test_4_output_validation():
    """Test 4: Output passes validation (status=PASS)"""
    try:
        # Load sample input
        input_file = project_root / "inputs" / "sample_nclex" / "sample_standards_input.json"
        if not input_file.exists():
            return False, f"Sample input file not found: {input_file}"

        with open(input_file, 'r') as f:
            outline = json.load(f)

        parser = StandardsParser()
        output = parser.apply_standards_to_outline(outline)

        validation = output.get("validation", {})
        status = validation.get("status")

        if status == "PASS":
            checklist = validation.get("checklist", {})
            errors = validation.get("errors", [])
            return True, f"Validation PASS. Checklist items: {len(checklist)}, Errors: {len(errors)}"
        else:
            errors = validation.get("errors", [])
            return False, f"Validation status: {status}, Errors: {errors}"
    except Exception as e:
        return False, f"Exception: {e}"


def test_5_methods_callable():
    """Test 5: All required methods callable"""
    try:
        parser = StandardsParser()

        # Check methods exist and are callable
        required_methods = [
            'parse_all_standards',
            'determine_delivery_mode',
            'build_fixed_slides_spec',
            'build_presenter_notes_requirements',
            'build_anchor_delivery',
            'build_active_learning_spec',
            'apply_standards_to_outline',
            'format_report'
        ]

        for method_name in required_methods:
            if not hasattr(parser, method_name):
                return False, f"Method '{method_name}' not found"
            method = getattr(parser, method_name)
            if not callable(method):
                return False, f"'{method_name}' is not callable"

        # Test parse_standards function
        if not callable(parse_standards):
            return False, "parse_standards function not callable"

        return True, f"All {len(required_methods)} required methods callable, plus standalone function"
    except Exception as e:
        return False, f"Exception: {e}"


def run_tests():
    """Run all 5 tests, 10 times each"""
    test_functions = [
        ("20.1 Module imports without error", test_1_module_import),
        ("20.2 parse_all_standards() returns success=True", test_2_parse_all_standards),
        ("20.3 apply_standards_to_outline() produces valid output", test_3_apply_standards_output),
        ("20.4 Output passes validation (status=PASS)", test_4_output_validation),
        ("20.5 All required methods callable", test_5_methods_callable),
    ]

    results = {}
    rounds = 10

    print("\n" + "=" * 80)
    print("TASK 20: Integration Test - Standards Parser Module")
    print("=" * 80)

    for test_name, test_func in test_functions:
        passed = 0
        failed = 0

        print(f"\nRunning {test_name}...")
        print("-" * 80)

        for round_num in range(1, rounds + 1):
            success, message = test_func()
            if success:
                passed += 1
                status = "PASS"
            else:
                failed += 1
                status = "FAIL"

            print(f"  Round {round_num:2d}: [{status}] {message}")

        results[test_name] = {
            "passed": passed,
            "failed": failed,
            "total": rounds,
            "status": "PASS" if failed == 0 else "FAIL"
        }

    # Print summary
    print("\n" + "=" * 80)
    print("TASK 20: Integration Test Summary")
    print("=" * 80)
    print("\nItems Verified:")

    all_passed = True
    for test_name, result in results.items():
        status = result["status"]
        passed = result["passed"]
        total = result["total"]

        if status == "FAIL":
            all_passed = False

        print(f"  [{status}] {test_name} ({passed}/{total} rounds)")

    print("\n" + "=" * 80)
    print(f"TASK 20 STATUS: {'PASS' if all_passed else 'FAIL'}")
    print("=" * 80)

    return all_passed


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
