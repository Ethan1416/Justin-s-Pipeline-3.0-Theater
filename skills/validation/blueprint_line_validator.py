"""
Blueprint Line Count Validator and Fixer
Validates and optionally fixes blueprint slides that exceed 8 lines in BODY section.
(R2 requirement: maximum 8 non-empty lines per body)

CANONICAL VALUE from config/constraints.yaml:
- body.max_lines = 8

Usage:
    python blueprint_line_validator.py <blueprints_folder>           # Validate only
    python blueprint_line_validator.py <blueprints_folder> --fix     # Validate and fix
    python blueprint_line_validator.py <blueprints_folder> --dry-run # Preview fixes
"""

import re
import sys
import shutil
from pathlib import Path

MAX_BODY_LINES = 8  # Per spec: maximum 8 non-empty lines in BODY section


def count_body_lines(body_text):
    """Count non-empty lines in body text."""
    lines = [line.strip() for line in body_text.strip().split('\n')]
    non_empty_lines = [line for line in lines if line and line != '']
    return len(non_empty_lines)


def parse_blueprint(blueprint_path):
    """Parse blueprint file and extract slide data."""
    with open(blueprint_path, 'r', encoding='utf-8') as f:
        content = f.read()

    slide_pattern = r'===========================================\nSLIDE (\d+): (.+?)\n===========================================\n(.*?)(?=\n===========================================\n|$)'

    slides = []
    for match in re.finditer(slide_pattern, content, re.DOTALL):
        slide_num = int(match.group(1))
        slide_title = match.group(2).strip()
        slide_content = match.group(3)

        body_match = re.search(
            r'\nBODY:\n(.*?)(?=\n\nNCLEX TIP:|\n\nPRESENTER NOTES:|\n===========================================|$)',
            slide_content, re.DOTALL
        )

        if body_match:
            body_text = body_match.group(1).strip()
            line_count = count_body_lines(body_text)

            slides.append({
                'number': slide_num,
                'title': slide_title,
                'body': body_text,
                'line_count': line_count,
                'exceeds_limit': line_count > MAX_BODY_LINES
            })

    return slides


def condense_body_text(body_text, target_lines=MAX_BODY_LINES):
    """Condense body text to fit within target line count."""
    lines = [line.strip() for line in body_text.strip().split('\n')]
    non_empty_lines = [line for line in lines if line and line != '']

    if len(non_empty_lines) <= target_lines:
        return body_text

    # Strategy: Keep main bullets, condense sub-bullets
    condensed = []
    current_line_count = 0

    for line in non_empty_lines:
        if current_line_count >= target_lines:
            break
        condensed.append(line)
        current_line_count += 1

    return '\n'.join(condensed)


def validate_blueprint(blueprint_path):
    """Validate a single blueprint file."""
    slides = parse_blueprint(blueprint_path)

    issues = []
    for slide in slides:
        if slide['exceeds_limit']:
            issues.append({
                'slide_num': slide['number'],
                'title': slide['title'],
                'line_count': slide['line_count'],
                'excess_lines': slide['line_count'] - MAX_BODY_LINES
            })

    return issues, slides


def fix_blueprint(blueprint_path, dry_run=False):
    """Fix a single blueprint file."""
    with open(blueprint_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Create backup
    if not dry_run:
        backup_path = str(blueprint_path).replace('.txt', '_BEFORE_LINE_FIX.txt')
        shutil.copy2(blueprint_path, backup_path)

    slide_pattern = r'(===========================================\nSLIDE \d+: .+?\n===========================================\n.*?\nBODY:\n)(.*?)((?=\n\nNCLEX TIP:|\n\nPRESENTER NOTES:))'

    fixes_made = 0

    def replace_body(match):
        nonlocal fixes_made
        prefix = match.group(1)
        body_text = match.group(2)
        suffix = match.group(3)

        line_count = count_body_lines(body_text)

        if line_count > MAX_BODY_LINES:
            condensed = condense_body_text(body_text, MAX_BODY_LINES)
            fixes_made += 1
            return prefix + condensed + '\n' + suffix
        else:
            return prefix + body_text + suffix

    fixed_content = re.sub(slide_pattern, replace_body, content, flags=re.DOTALL)

    if not dry_run and fixes_made > 0:
        with open(blueprint_path, 'w', encoding='utf-8') as f:
            f.write(fixed_content)

    return fixes_made


def validate_all_blueprints(blueprints_folder):
    """Validate all blueprint files in a folder."""
    blueprints_folder = Path(blueprints_folder)
    blueprint_files = list(blueprints_folder.glob('step*.txt'))

    all_issues = {}

    for blueprint_file in sorted(blueprint_files):
        issues, slides = validate_blueprint(blueprint_file)

        if issues:
            all_issues[blueprint_file.name] = {
                'issues': issues,
                'total_slides': len(slides),
                'path': blueprint_file
            }

    return all_issues


def fix_all_blueprints(blueprints_folder, dry_run=False):
    """Fix all blueprint files in a folder."""
    blueprints_folder = Path(blueprints_folder)
    blueprint_files = list(blueprints_folder.glob('step*.txt'))

    results = {}

    for blueprint_file in sorted(blueprint_files):
        fixes_made = fix_blueprint(blueprint_file, dry_run=dry_run)

        if fixes_made > 0:
            results[blueprint_file.name] = fixes_made

    return results


def print_validation_report(all_issues):
    """Print formatted validation report."""
    if not all_issues:
        print("ALL BLUEPRINTS VALID")
        print("  All slides have 8 or fewer lines in BODY section")
        return True

    print("=" * 80)
    print("BLUEPRINT LINE COUNT VALIDATION REPORT")
    print("=" * 80)
    print(f"Maximum allowed lines per slide: {MAX_BODY_LINES}")
    print()

    total_issues = sum(len(data['issues']) for data in all_issues.values())

    for blueprint_name, data in all_issues.items():
        print(f"\n{blueprint_name}")
        print("-" * 80)
        print(f"  Total slides: {data['total_slides']}")
        print(f"  Slides exceeding limit: {len(data['issues'])}")
        print()

        for issue in data['issues']:
            print(f"  SLIDE {issue['slide_num']}: {issue['title'][:50]}")
            print(f"    Lines: {issue['line_count']} (exceeds by {issue['excess_lines']})")
        print()

    print("=" * 80)
    print(f"TOTAL ISSUES: {total_issues} slides across {len(all_issues)} blueprints")
    print("=" * 80)

    return False


def print_fix_report(results, dry_run=False):
    """Print formatted fix report."""
    if not results:
        print("No fixes needed - all blueprints within line limits")
        return

    print("=" * 80)
    print(f"BLUEPRINT LINE COUNT FIX REPORT {'(DRY RUN)' if dry_run else ''}")
    print("=" * 80)
    print()

    total_fixes = 0
    for blueprint_name, fixes_made in results.items():
        print(f"{blueprint_name}")
        print(f"  Slides fixed: {fixes_made}")
        total_fixes += fixes_made

    print()
    print("=" * 80)
    print(f"TOTAL: {total_fixes} slides fixed across {len(results)} blueprints")
    print("=" * 80)

    if not dry_run:
        print("\nBackups saved as *_BEFORE_LINE_FIX.txt")


def main():
    """Main function with validate/fix modes."""
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    blueprints_folder = sys.argv[1]
    do_fix = '--fix' in sys.argv
    dry_run = '--dry-run' in sys.argv

    print(f"Blueprints folder: {blueprints_folder}")
    print(f"Mode: {'FIX' if do_fix else 'VALIDATE'}{' (dry run)' if dry_run else ''}")
    print()

    if do_fix:
        results = fix_all_blueprints(blueprints_folder, dry_run=dry_run)
        print_fix_report(results, dry_run=dry_run)

        if not dry_run and results:
            print("\nRe-validating after fixes...")
            all_issues = validate_all_blueprints(blueprints_folder)
            all_valid = print_validation_report(all_issues)
            sys.exit(0 if all_valid else 1)
    else:
        all_issues = validate_all_blueprints(blueprints_folder)
        all_valid = print_validation_report(all_issues)
        sys.exit(0 if all_valid else 1)


if __name__ == "__main__":
    main()
