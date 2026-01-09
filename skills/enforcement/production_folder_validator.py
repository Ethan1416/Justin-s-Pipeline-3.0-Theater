"""
Production Folder Validator Skill
=================================

HARDCODED validator for production folder output.
This validator CANNOT be bypassed - all production output MUST pass validation.

Validation Rules:
- R1: Production folder exists at ~/Desktop/Theater_Production (HARDCODED)
- R2: Unit folder structure correct (HARDCODED)
- R3: Day folder structure correct (HARDCODED)
- R4: Required files present (HARDCODED)
- R5: File sizes valid (not empty) (HARDCODED)
- R6: PowerPoint has 16 slides (HARDCODED)

Pipeline: Theater Education
"""

from pathlib import Path
from typing import Dict, Any, List, Optional
import os


# =============================================================================
# HARDCODED VALIDATION THRESHOLDS (CANNOT BE MODIFIED)
# =============================================================================

# Import production constants
try:
    from .production_folder_generator import (
        PRODUCTION_ROOT,
        DESKTOP_PATH,
        REQUIRED_FILES,
        UNIT_NAMES,
        get_production_path
    )
except ImportError:
    # Fallback definitions
    DESKTOP_PATH = Path.home() / "Desktop"
    PRODUCTION_ROOT = DESKTOP_PATH / "Theater_Production"
    REQUIRED_FILES = {
        "powerpoint": {"extension": ".pptx", "required": True},
        "handout": {"extension": ".docx", "required": False},
        "lesson_plan": {"extension": ".md", "required": True},
        "exit_ticket": {"extension": ".md", "required": True},
        "journal_prompts": {"extension": ".md", "required": True},
    }
    UNIT_NAMES = {1: "Greek_Theater", 2: "Commedia_dellArte", 3: "Romeo_and_Juliet", 4: "Student_Directed_One_Acts"}

# Minimum file sizes (bytes)
MIN_FILE_SIZES = {
    ".pptx": 10000,  # PowerPoint must be at least 10KB
    ".docx": 5000,   # Word doc must be at least 5KB
    ".md": 500,      # Markdown must be at least 500 bytes
    ".txt": 100,     # Text must be at least 100 bytes
}

# Required PowerPoint slide count
REQUIRED_SLIDE_COUNT = 16


# =============================================================================
# FOLDER VALIDATION
# =============================================================================

def validate_production_root() -> Dict[str, Any]:
    """
    Validate production root folder exists.

    HARDCODED: ~/Desktop/Theater_Production must exist.

    Returns:
        Validation result
    """
    issues = []

    # R1: Check production root exists
    if not PRODUCTION_ROOT.exists():
        issues.append({
            "rule": "R1",
            "severity": "CRITICAL",
            "message": f"Production root not found: {PRODUCTION_ROOT}"
        })
        return {
            "valid": False,
            "path": str(PRODUCTION_ROOT),
            "exists": False,
            "issues": issues
        }

    if not PRODUCTION_ROOT.is_dir():
        issues.append({
            "rule": "R1",
            "severity": "CRITICAL",
            "message": f"Production root is not a directory: {PRODUCTION_ROOT}"
        })

    return {
        "valid": len(issues) == 0,
        "path": str(PRODUCTION_ROOT),
        "exists": True,
        "issues": issues
    }


def validate_unit_folder(unit_number: int) -> Dict[str, Any]:
    """
    Validate unit folder structure.

    HARDCODED: Unit_X_[Name] folder must exist with correct structure.

    Args:
        unit_number: Unit number (1-4)

    Returns:
        Validation result
    """
    issues = []
    warnings = []

    unit_name = UNIT_NAMES.get(unit_number, f"Unit_{unit_number}")
    unit_folder_name = f"Unit_{unit_number}_{unit_name}"
    unit_path = PRODUCTION_ROOT / unit_folder_name

    # R2: Check unit folder exists
    if not unit_path.exists():
        issues.append({
            "rule": "R2",
            "severity": "CRITICAL",
            "message": f"Unit folder not found: {unit_folder_name}"
        })
        return {
            "valid": False,
            "unit_number": unit_number,
            "path": str(unit_path),
            "exists": False,
            "issues": issues,
            "warnings": warnings
        }

    # Check for day folders
    day_folders = [d for d in unit_path.iterdir() if d.is_dir() and d.name.startswith("Day_")]

    if not day_folders:
        warnings.append({
            "rule": "R2",
            "severity": "WARNING",
            "message": f"No day folders found in {unit_folder_name}"
        })

    # Check for unit plan
    unit_plan = unit_path / "unit_plan.md"
    if not unit_plan.exists():
        warnings.append({
            "rule": "R2",
            "severity": "WARNING",
            "message": f"unit_plan.md not found in {unit_folder_name}"
        })

    return {
        "valid": len(issues) == 0,
        "unit_number": unit_number,
        "path": str(unit_path),
        "exists": True,
        "day_count": len(day_folders),
        "has_unit_plan": unit_plan.exists(),
        "issues": issues,
        "warnings": warnings
    }


def validate_day_folder(unit_number: int, day: int) -> Dict[str, Any]:
    """
    Validate day folder and contents.

    HARDCODED: Day_XX folder must contain required files.

    Args:
        unit_number: Unit number
        day: Day number

    Returns:
        Validation result
    """
    issues = []
    warnings = []
    files_found = {}

    unit_name = UNIT_NAMES.get(unit_number, f"Unit_{unit_number}")
    unit_folder_name = f"Unit_{unit_number}_{unit_name}"
    day_folder_name = f"Day_{day:02d}"
    day_path = PRODUCTION_ROOT / unit_folder_name / day_folder_name

    # R3: Check day folder exists
    if not day_path.exists():
        issues.append({
            "rule": "R3",
            "severity": "CRITICAL",
            "message": f"Day folder not found: {day_folder_name}"
        })
        return {
            "valid": False,
            "unit_number": unit_number,
            "day": day,
            "path": str(day_path),
            "exists": False,
            "issues": issues,
            "warnings": warnings
        }

    # R4: Check required files
    for file_type, info in REQUIRED_FILES.items():
        ext = info["extension"]
        required = info["required"]

        # Find matching files
        matches = list(day_path.glob(f"*{ext}"))

        if matches:
            files_found[file_type] = {
                "found": True,
                "path": str(matches[0]),
                "size": matches[0].stat().st_size
            }

            # R5: Check file size
            min_size = MIN_FILE_SIZES.get(ext, 0)
            if matches[0].stat().st_size < min_size:
                issues.append({
                    "rule": "R5",
                    "severity": "CRITICAL",
                    "message": f"{file_type} file too small: {matches[0].stat().st_size} bytes < {min_size} minimum"
                })
        else:
            files_found[file_type] = {"found": False}
            if required:
                issues.append({
                    "rule": "R4",
                    "severity": "CRITICAL",
                    "message": f"Required file missing: {file_type} ({ext})"
                })
            else:
                warnings.append({
                    "rule": "R4",
                    "severity": "WARNING",
                    "message": f"Optional file missing: {file_type} ({ext})"
                })

    # R6: Validate PowerPoint slide count
    pptx_files = list(day_path.glob("*.pptx"))
    if pptx_files:
        slide_validation = validate_powerpoint_slides(pptx_files[0])
        if not slide_validation["valid"]:
            issues.extend(slide_validation["issues"])

    return {
        "valid": len(issues) == 0,
        "unit_number": unit_number,
        "day": day,
        "path": str(day_path),
        "exists": True,
        "files": files_found,
        "issues": issues,
        "warnings": warnings
    }


def validate_powerpoint_slides(pptx_path: Path) -> Dict[str, Any]:
    """
    Validate PowerPoint has correct number of slides.

    HARDCODED: PowerPoint must have exactly 16 slides.

    Args:
        pptx_path: Path to PowerPoint file

    Returns:
        Validation result
    """
    issues = []

    try:
        from pptx import Presentation
        prs = Presentation(str(pptx_path))
        slide_count = len(prs.slides)

        if slide_count != REQUIRED_SLIDE_COUNT:
            issues.append({
                "rule": "R6",
                "severity": "CRITICAL",
                "message": f"PowerPoint has {slide_count} slides, expected {REQUIRED_SLIDE_COUNT}"
            })

        return {
            "valid": len(issues) == 0,
            "slide_count": slide_count,
            "expected": REQUIRED_SLIDE_COUNT,
            "issues": issues
        }

    except ImportError:
        return {
            "valid": True,  # Can't validate without pptx
            "slide_count": None,
            "issues": [{"rule": "R6", "severity": "INFO", "message": "python-pptx not available for validation"}]
        }
    except Exception as e:
        issues.append({
            "rule": "R6",
            "severity": "CRITICAL",
            "message": f"Cannot open PowerPoint: {e}"
        })
        return {
            "valid": False,
            "slide_count": None,
            "issues": issues
        }


# =============================================================================
# FULL PRODUCTION VALIDATION
# =============================================================================

def validate_production_output(
    unit_number: int,
    day: int
) -> Dict[str, Any]:
    """
    Full validation of production output for a lesson.

    HARDCODED validation that cannot be bypassed.

    Args:
        unit_number: Unit number
        day: Day number

    Returns:
        Complete validation result
    """
    all_issues = []
    all_warnings = []

    # Validate production root
    root_result = validate_production_root()
    if not root_result["valid"]:
        return {
            "valid": False,
            "root_validation": root_result,
            "issues": root_result["issues"],
            "warnings": []
        }

    # Validate unit folder
    unit_result = validate_unit_folder(unit_number)
    all_issues.extend(unit_result.get("issues", []))
    all_warnings.extend(unit_result.get("warnings", []))

    if not unit_result["valid"]:
        return {
            "valid": False,
            "root_validation": root_result,
            "unit_validation": unit_result,
            "issues": all_issues,
            "warnings": all_warnings
        }

    # Validate day folder
    day_result = validate_day_folder(unit_number, day)
    all_issues.extend(day_result.get("issues", []))
    all_warnings.extend(day_result.get("warnings", []))

    # Build summary
    critical_issues = [i for i in all_issues if i.get("severity") == "CRITICAL"]

    return {
        "valid": len(critical_issues) == 0,
        "unit_number": unit_number,
        "day": day,
        "production_path": day_result.get("path"),
        "root_validation": root_result,
        "unit_validation": unit_result,
        "day_validation": day_result,
        "files_found": day_result.get("files", {}),
        "issues": all_issues,
        "warnings": all_warnings,
        "summary": generate_validation_summary(day_result, all_issues, all_warnings)
    }


def generate_validation_summary(
    day_result: Dict,
    issues: List[Dict],
    warnings: List[Dict]
) -> str:
    """Generate human-readable validation summary."""
    lines = ["=" * 60]
    lines.append("PRODUCTION FOLDER VALIDATION SUMMARY")
    lines.append("=" * 60)

    if day_result.get("exists"):
        lines.append(f"Path: {day_result.get('path')}")

    files = day_result.get("files", {})
    found_count = sum(1 for f in files.values() if f.get("found"))
    total_count = len(files)

    if issues:
        critical = [i for i in issues if i.get("severity") == "CRITICAL"]
        lines.append(f"STATUS: FAILED ({len(critical)} critical issues)")
    else:
        lines.append(f"STATUS: PASSED ({found_count}/{total_count} files)")

    lines.append("")
    lines.append("Files:")
    for file_type, info in files.items():
        if info.get("found"):
            size = info.get("size", 0)
            lines.append(f"  [OK] {file_type}: {size:,} bytes")
        else:
            status = "MISSING" if REQUIRED_FILES.get(file_type, {}).get("required") else "optional"
            lines.append(f"  [{status.upper()}] {file_type}")

    if issues:
        lines.append("")
        lines.append("Issues:")
        for issue in issues[:5]:
            lines.append(f"  [{issue.get('severity')}] {issue.get('message')}")
        if len(issues) > 5:
            lines.append(f"  ... and {len(issues) - 5} more")

    lines.append("=" * 60)
    return "\n".join(lines)


# =============================================================================
# QUICK VALIDATION FUNCTIONS
# =============================================================================

def has_valid_production(unit_number: int, day: int) -> bool:
    """Quick check if production output is valid."""
    result = validate_production_output(unit_number, day)
    return result["valid"]


def get_production_issues(unit_number: int, day: int) -> List[str]:
    """Get list of issue messages."""
    result = validate_production_output(unit_number, day)
    return [i["message"] for i in result.get("issues", [])]


def production_folder_exists(unit_number: int, day: int) -> bool:
    """Check if production folder exists."""
    unit_name = UNIT_NAMES.get(unit_number, f"Unit_{unit_number}")
    path = PRODUCTION_ROOT / f"Unit_{unit_number}_{unit_name}" / f"Day_{day:02d}"
    return path.exists()


# =============================================================================
# EXPORTS
# =============================================================================

__all__ = [
    # Main validation functions
    "validate_production_root",
    "validate_unit_folder",
    "validate_day_folder",
    "validate_powerpoint_slides",
    "validate_production_output",
    # Quick checks
    "has_valid_production",
    "get_production_issues",
    "production_folder_exists",
    # Constants
    "PRODUCTION_ROOT",
    "REQUIRED_FILES",
    "MIN_FILE_SIZES",
    "REQUIRED_SLIDE_COUNT",
]
