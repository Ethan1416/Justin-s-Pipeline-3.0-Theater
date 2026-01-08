"""
Pipeline State Manager - Track and Update Pipeline Progress
============================================================

This script manages the pipeline_state.json file to track progress
of each section through the pipeline steps.

Usage:
    # View current state
    python pipeline_state_manager.py status

    # Update a section's step status
    python pipeline_state_manager.py update "Section_Name" step7 completed

    # Add a new section
    python pipeline_state_manager.py add "New_Section_Name"

    # Generate progress report
    python pipeline_state_manager.py report
"""

import json
import sys
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, Any

STATE_FILE = Path(__file__).parent / "pipeline_state.json"

# Import singleton for pre-validation (lazy import to avoid circular deps)
_standards_loader = None

VALID_STATUSES = ["pending", "in_progress", "completed", "failed", "skipped"]

SECTION_STEPS = [
    "step6_blueprint",
    "step7_revision",
    "step8_qa",
    "step9_visual",
    "step10_integration",
    "step11_organization",
    "step12_population"
]


def load_state() -> dict:
    """Load pipeline state from JSON file."""
    if not STATE_FILE.exists():
        return create_default_state()

    with open(STATE_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_state(state: dict):
    """Save pipeline state to JSON file."""
    state['pipeline_info']['last_updated'] = datetime.now().strftime('%Y-%m-%d')

    with open(STATE_FILE, 'w', encoding='utf-8') as f:
        json.dump(state, f, indent=2)

    print(f"State saved to {STATE_FILE}")


def create_default_state() -> dict:
    """Create default state structure."""
    return {
        "pipeline_info": {
            "domain": "Unknown",
            "created": datetime.now().strftime('%Y-%m-%d'),
            "last_updated": datetime.now().strftime('%Y-%m-%d')
        },
        "sections": {},
        "global_steps": {
            "step0_standards_prevalidation": "pending",
            "step1_anchor_upload": "pending",
            "step2_lecture_mapping": "pending",
            "step3_official_sorting": "pending",
            "step4_outline_generation": "pending",
            "step5_presentation_standards": "reference_document"
        },
        "notes": []
    }


def prevalidate_standards() -> Dict[str, Any]:
    """
    Pre-validate all standards at pipeline initialization (Step 0).

    This function:
    1. Loads and caches all standards via singleton
    2. Validates standards completeness
    3. Reports any errors before pipeline processing begins
    4. Updates pipeline state with validation status

    Returns:
        Dictionary with validation status and details
    """
    global _standards_loader

    result = {
        "status": "UNKNOWN",
        "step": "step0_standards_prevalidation",
        "standards_valid": False,
        "cached": False,
        "errors": [],
        "warnings": [],
        "report": ""
    }

    try:
        # Lazy import to avoid circular dependencies
        if _standards_loader is None:
            from skills.parsing.standards_loader_singleton import (
                prevalidate_pipeline,
                StandardsLoaderSingleton
            )
            _standards_loader = {
                "prevalidate": prevalidate_pipeline,
                "singleton": StandardsLoaderSingleton
            }

        # Run pre-validation
        validation_result = _standards_loader["prevalidate"]()

        result["standards_valid"] = validation_result.get("standards_valid", False)
        result["cached"] = validation_result.get("cached", False)
        result["errors"] = validation_result.get("errors", [])
        result["warnings"] = validation_result.get("warnings", [])
        result["report"] = validation_result.get("report", "")
        result["status"] = validation_result.get("status", "UNKNOWN")

        # Update pipeline state
        state = load_state()
        if result["standards_valid"]:
            state["global_steps"]["step0_standards_prevalidation"] = "completed"
            state["pipeline_info"]["standards_prevalidation"] = {
                "status": "PASS",
                "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                "cached": True
            }
        else:
            state["global_steps"]["step0_standards_prevalidation"] = "failed"
            state["pipeline_info"]["standards_prevalidation"] = {
                "status": "FAIL",
                "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                "errors": result["errors"]
            }

        save_state(state)

    except ImportError as e:
        result["status"] = "ERROR"
        result["errors"].append(f"Import error: {str(e)}")
    except Exception as e:
        result["status"] = "ERROR"
        result["errors"].append(f"Pre-validation error: {str(e)}")

    return result


def get_cached_standards():
    """
    Get cached standards from singleton.

    Returns:
        ParsedStandards object or None if not available
    """
    global _standards_loader

    try:
        if _standards_loader is None:
            from skills.parsing.standards_loader_singleton import get_cached_standards
            return get_cached_standards()
        return None
    except ImportError:
        return None


def add_section(section_name: str):
    """Add a new section to track."""
    state = load_state()

    if section_name in state['sections']:
        print(f"Section '{section_name}' already exists")
        return

    state['sections'][section_name] = {step: "pending" for step in SECTION_STEPS}
    save_state(state)
    print(f"Added section: {section_name}")


def update_status(section_name: str, step: str, status: str):
    """Update the status of a step for a section."""
    state = load_state()

    # Normalize step name
    if not step.startswith("step"):
        step = f"step{step}"
    if "_" not in step:
        # Map short names to full names
        step_mapping = {
            "step6": "step6_blueprint",
            "step7": "step7_revision",
            "step8": "step8_qa",
            "step9": "step9_visual",
            "step10": "step10_integration",
            "step11": "step11_organization",
            "step12": "step12_population"
        }
        step = step_mapping.get(step, step)

    # Validate status
    if status not in VALID_STATUSES:
        print(f"Invalid status: {status}")
        print(f"Valid statuses: {', '.join(VALID_STATUSES)}")
        return

    # Check if section exists
    if section_name not in state['sections']:
        print(f"Section '{section_name}' not found. Adding it...")
        state['sections'][section_name] = {s: "pending" for s in SECTION_STEPS}

    # Check if step is valid
    if step not in state['sections'][section_name]:
        print(f"Invalid step: {step}")
        print(f"Valid steps: {', '.join(SECTION_STEPS)}")
        return

    old_status = state['sections'][section_name][step]
    state['sections'][section_name][step] = status
    save_state(state)
    print(f"Updated {section_name}/{step}: {old_status} -> {status}")


def show_status():
    """Display current pipeline status."""
    state = load_state()

    print("=" * 70)
    print("PIPELINE STATUS")
    print("=" * 70)
    print(f"Domain: {state['pipeline_info'].get('domain', 'Unknown')}")
    print(f"Last Updated: {state['pipeline_info'].get('last_updated', 'Unknown')}")
    print()

    # Global steps
    print("GLOBAL STEPS:")
    print("-" * 40)
    for step, status in state.get('global_steps', {}).items():
        status_icon = get_status_icon(status)
        print(f"  {status_icon} {step}: {status}")
    print()

    # Section steps
    print("SECTION PROGRESS:")
    print("-" * 70)

    sections = state.get('sections', {})
    if not sections:
        print("  No sections tracked yet")
    else:
        # Header
        print(f"  {'Section':<30} | 6 | 7 | 8 | 9 | 10| 11| 12|")
        print("  " + "-" * 66)

        for section, steps in sections.items():
            icons = []
            for step in SECTION_STEPS:
                status = steps.get(step, "pending")
                icons.append(get_status_icon(status))

            print(f"  {section:<30} | {' | '.join(icons)} |")

    print()
    print("Legend: [x]=completed [~]=in_progress [ ]=pending [!]=failed [-]=skipped")
    print("=" * 70)


def get_status_icon(status: str) -> str:
    """Get single-character icon for status."""
    icons = {
        "completed": "x",
        "in_progress": "~",
        "pending": " ",
        "failed": "!",
        "skipped": "-",
        "reference_document": "R"
    }
    return icons.get(status, "?")


def generate_report():
    """Generate detailed progress report."""
    state = load_state()

    print("=" * 70)
    print("PIPELINE PROGRESS REPORT")
    print("=" * 70)
    print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Domain: {state['pipeline_info'].get('domain', 'Unknown')}")
    print()

    sections = state.get('sections', {})

    # Calculate statistics
    total_steps = len(sections) * len(SECTION_STEPS)
    completed_steps = 0
    in_progress_steps = 0
    failed_steps = 0

    for section, steps in sections.items():
        for step, status in steps.items():
            if status == "completed":
                completed_steps += 1
            elif status == "in_progress":
                in_progress_steps += 1
            elif status == "failed":
                failed_steps += 1

    if total_steps > 0:
        progress_pct = (completed_steps / total_steps) * 100
    else:
        progress_pct = 0

    print("SUMMARY:")
    print("-" * 40)
    print(f"  Sections: {len(sections)}")
    print(f"  Total Steps: {total_steps}")
    print(f"  Completed: {completed_steps} ({progress_pct:.1f}%)")
    print(f"  In Progress: {in_progress_steps}")
    print(f"  Failed: {failed_steps}")
    print()

    # Progress bar
    bar_width = 40
    filled = int(bar_width * progress_pct / 100)
    bar = "[" + "#" * filled + "-" * (bar_width - filled) + "]"
    print(f"  Progress: {bar} {progress_pct:.1f}%")
    print()

    # Section details
    print("SECTION DETAILS:")
    print("-" * 40)

    for section, steps in sections.items():
        section_completed = sum(1 for s in steps.values() if s == "completed")
        section_total = len(steps)
        section_pct = (section_completed / section_total * 100) if section_total > 0 else 0

        print(f"\n  {section}:")
        print(f"    Progress: {section_completed}/{section_total} ({section_pct:.0f}%)")

        # Find next pending step
        for step in SECTION_STEPS:
            if steps.get(step) == "pending":
                print(f"    Next Step: {step}")
                break
        else:
            if section_completed == section_total:
                print("    Status: COMPLETE")

    print()
    print("=" * 70)


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python pipeline_state_manager.py status")
        print("  python pipeline_state_manager.py update <section> <step> <status>")
        print("  python pipeline_state_manager.py add <section>")
        print("  python pipeline_state_manager.py report")
        print("  python pipeline_state_manager.py prevalidate   # Run Step 0 standards pre-validation")
        return 1

    command = sys.argv[1].lower()

    if command == "status":
        show_status()
    elif command == "report":
        generate_report()
    elif command == "add" and len(sys.argv) >= 3:
        add_section(sys.argv[2])
    elif command == "update" and len(sys.argv) >= 5:
        update_status(sys.argv[2], sys.argv[3], sys.argv[4])
    elif command == "prevalidate":
        # Run Step 0: Standards Pre-validation
        print("=" * 60)
        print("STEP 0: STANDARDS PRE-VALIDATION")
        print("=" * 60)

        result = prevalidate_standards()

        print(f"\nStatus: {result['status']}")
        print(f"Standards Valid: {result['standards_valid']}")
        print(f"Cached: {result['cached']}")

        if result['errors']:
            print("\nErrors:")
            for error in result['errors']:
                print(f"  - {error}")

        if result['warnings']:
            print("\nWarnings:")
            for warning in result['warnings']:
                print(f"  - {warning}")

        if result['standards_valid']:
            print("\nStandards pre-validation PASSED. Pipeline ready to proceed.")
        else:
            print("\nStandards pre-validation FAILED. Fix errors before continuing.")
            return 1

        print("=" * 60)
    else:
        print(f"Unknown command or missing arguments: {command}")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
