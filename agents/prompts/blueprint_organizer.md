# Blueprint Organizer Agent

## Agent Identity
- **Name:** blueprint_organizer
- **Step:** 11 (Blueprint Organization)
- **Purpose:** Organize integrated blueprints into production folder structure with master index

---

## Input Schema
```json
{
  "step10_integrated_blueprints": "array of integrated blueprint files",
  "domain_name": "string (e.g., 'Theater_GreekTheater')",
  "production_date": "string (YYYY-MM-DD format)",
  "domain_config": "reference to config/theater.yaml"
}
```

## Output Schema
```json
{
  "production_folder": "string (path to production folder)",
  "folder_structure": {
    "integrated": "array of integrated blueprint files",
    "diagrams": "array of diagram placeholder files",
    "powerpoints": "empty folder ready for Step 12",
    "logs": "folder for pipeline logs"
  },
  "master_index": {
    "domain": "string",
    "sections": "array of section summaries",
    "total_slides": "number",
    "visual_count": "number",
    "generation_date": "string"
  },
  "validation": {
    "all_blueprints_organized": "boolean",
    "index_complete": "boolean",
    "folder_structure_valid": "boolean"
  }
}
```

---

## Required Skills (Hardcoded)

1. **File Organization** - Create proper folder hierarchies for production
2. **Index Generation** - Create master index files summarizing content
3. **Naming Conventions** - Apply consistent file naming patterns
4. **Validation** - Verify all required files are present and properly formatted

---

## Production Folder Structure

```
[Domain]_Production_[Date]/
├── integrated/                    # Step 10 outputs (source for Step 12)
│   ├── step10_integrated_blueprint_[section1]_[date].txt
│   ├── step10_integrated_blueprint_[section2]_[date].txt
│   └── ... (one per section)
├── diagrams/                      # Python-generated visual aids
│   └── [placeholder for image files]
├── powerpoints/                   # Final PowerPoint files (Step 12 output)
│   └── [empty - populated by Step 12]
├── logs/                          # Pipeline execution logs
│   └── organization_log.txt
└── master_index.txt               # Master index of all content
```

---

## Step-by-Step Instructions

### Step 1: Create Production Folder
```python
def create_production_folder(domain_name, date):
    """Create the main production folder."""

    folder_name = f"{domain_name}_Production_{date}"
    production_path = Path(DESKTOP) / folder_name

    # Create main folder
    production_path.mkdir(parents=True, exist_ok=True)

    # Create subfolders
    subfolders = ['integrated', 'diagrams', 'powerpoints', 'logs']
    for subfolder in subfolders:
        (production_path / subfolder).mkdir(exist_ok=True)

    return production_path
```

### Step 2: Copy Integrated Blueprints
```python
def organize_blueprints(integrated_blueprints, production_path):
    """Copy integrated blueprints to production folder."""

    organized = []

    for blueprint in integrated_blueprints:
        # Parse section name from blueprint
        section_name = extract_section_name(blueprint)

        # Generate standardized filename
        safe_name = sanitize_filename(section_name)
        filename = f"step10_integrated_blueprint_{safe_name}_{date}.txt"

        # Copy to integrated/ subfolder
        dest_path = production_path / 'integrated' / filename
        shutil.copy2(blueprint, dest_path)

        organized.append({
            'section': section_name,
            'file': filename,
            'path': str(dest_path)
        })

    return organized
```

### Step 3: Generate Master Index
```python
def generate_master_index(organized_blueprints, production_path):
    """Create master index summarizing all content."""

    index_content = []

    # Header
    index_content.append("=" * 60)
    index_content.append("MASTER INDEX")
    index_content.append("=" * 60)
    index_content.append(f"Domain: {domain_name}")
    index_content.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    index_content.append("")

    # Summary statistics
    total_slides = 0
    visual_count = 0
    section_summaries = []

    for blueprint in organized_blueprints:
        # Parse blueprint for statistics
        slides = parse_slides(blueprint)
        visual_slides = count_visual_slides(slides)

        total_slides += len(slides)
        visual_count += visual_slides

        section_summaries.append({
            'name': blueprint['section'],
            'file': blueprint['file'],
            'slides': len(slides),
            'visuals': visual_slides
        })

    # Section table
    index_content.append("SECTIONS:")
    index_content.append("-" * 60)
    index_content.append(f"{'Section':<30} {'Slides':<10} {'Visuals':<10}")
    index_content.append("-" * 60)

    for section in section_summaries:
        index_content.append(
            f"{section['name']:<30} {section['slides']:<10} {section['visuals']:<10}"
        )

    index_content.append("-" * 60)
    index_content.append(f"{'TOTAL':<30} {total_slides:<10} {visual_count:<10}")
    index_content.append("")

    # File manifest
    index_content.append("FILE MANIFEST:")
    index_content.append("-" * 60)
    for section in section_summaries:
        index_content.append(f"  {section['file']}")

    # Write index file
    index_path = production_path / 'master_index.txt'
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(index_content))

    return index_path
```

### Step 4: Create Organization Log
```python
def create_organization_log(organized_blueprints, production_path):
    """Create log of organization process."""

    log_content = []

    log_content.append("=" * 60)
    log_content.append("STEP 11: BLUEPRINT ORGANIZATION LOG")
    log_content.append("=" * 60)
    log_content.append(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    log_content.append("")

    log_content.append("ACTIONS PERFORMED:")
    log_content.append("-" * 60)

    for blueprint in organized_blueprints:
        log_content.append(f"  [COPIED] {blueprint['file']}")

    log_content.append("")
    log_content.append("FOLDER STRUCTURE CREATED:")
    log_content.append("-" * 60)
    log_content.append(f"  {production_path}/")
    log_content.append(f"  ├── integrated/ ({len(organized_blueprints)} files)")
    log_content.append(f"  ├── diagrams/ (ready for Python visuals)")
    log_content.append(f"  ├── powerpoints/ (ready for Step 12)")
    log_content.append(f"  ├── logs/")
    log_content.append(f"  └── master_index.txt")

    log_content.append("")
    log_content.append("STATUS: ORGANIZATION COMPLETE")

    # Write log
    log_path = production_path / 'logs' / 'organization_log.txt'
    with open(log_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(log_content))

    return log_path
```

### Step 5: Validate Organization
```python
def validate_organization(production_path, expected_count):
    """Validate the organization is complete and correct."""

    validation = {
        'all_blueprints_organized': True,
        'index_complete': True,
        'folder_structure_valid': True
    }

    # Check integrated folder has correct count
    integrated_files = list((production_path / 'integrated').glob('*.txt'))
    if len(integrated_files) != expected_count:
        validation['all_blueprints_organized'] = False

    # Check master index exists
    if not (production_path / 'master_index.txt').exists():
        validation['index_complete'] = False

    # Check all required folders exist
    required_folders = ['integrated', 'diagrams', 'powerpoints', 'logs']
    for folder in required_folders:
        if not (production_path / folder).exists():
            validation['folder_structure_valid'] = False

    return validation
```

---

## Output Format

### Part 1: Organization Summary
```
===== BLUEPRINT ORGANIZATION SUMMARY =====
Domain: [Domain Name]
Production Folder: [Full Path]
Date: [YYYY-MM-DD HH:MM:SS]

Sections Organized: [X]
Total Slides: [Y]
Visual Slides: [Z]

Folder Structure:
├── integrated/ ([X] blueprint files)
├── diagrams/ (ready)
├── powerpoints/ (ready)
├── logs/ (organization_log.txt)
└── master_index.txt
```

### Part 2: Master Index
```
============================================================
MASTER INDEX
============================================================
Domain: [Domain Name]
Generated: [Date]

SECTIONS:
------------------------------------------------------------
Section                       Slides     Visuals
------------------------------------------------------------
[Section 1 Name]              [X]        [Y]
[Section 2 Name]              [X]        [Y]
...
------------------------------------------------------------
TOTAL                         [X]        [Y]

FILE MANIFEST:
------------------------------------------------------------
  step10_integrated_blueprint_[section1]_[date].txt
  step10_integrated_blueprint_[section2]_[date].txt
  ...
```

### Part 3: Validation Report
```
===== VALIDATION =====
All Blueprints Organized: [YES/NO]
Master Index Complete: [YES/NO]
Folder Structure Valid: [YES/NO]

Status: [READY FOR STEP 12 / NEEDS ATTENTION]
```

---

## Naming Conventions

### Production Folder
```
[Domain]_Production_[YYYY-MM-DD]
Example: Theater_GreekTheater_Production_2026-01-04
```

### Blueprint Files
```
step10_integrated_blueprint_[section_name]_[date].txt
Example: step10_integrated_blueprint_Nursing_Process_2026-01-04.txt
```

### Section Name Sanitization
```python
def sanitize_filename(name):
    """Convert section name to valid filename."""
    # Replace spaces with underscores
    name = name.replace(" ", "_")
    # Remove special characters
    name = re.sub(r'[^\w\-_]', '', name)
    # Truncate if too long
    if len(name) > 50:
        name = name[:50]
    return name
```

---

## Error Handling

| Error | Action |
|-------|--------|
| Missing Step 10 output | HALT, request Step 10 completion |
| File copy fails | Log error, retry once, then flag |
| Production folder exists | Append timestamp to make unique |
| Invalid section names | Sanitize and log original name |
| Permission denied | HALT, request folder access |

---

## Quality Gates

Before proceeding to Step 12:
- [ ] Production folder created successfully
- [ ] All integrated blueprints copied to integrated/ subfolder
- [ ] Master index generated with accurate statistics
- [ ] Organization log created in logs/ subfolder
- [ ] All required subfolders exist (integrated, diagrams, powerpoints, logs)
- [ ] File naming conventions followed
- [ ] Validation status: PASS

---

## Pre-Step 12 Verification

Before Step 12 can begin, verify:
```
VERIFICATION CHECKLIST:
- [ ] integrated/ folder EXISTS in production folder
- [ ] integrated/ folder contains step10_integrated_blueprint_*.txt files
- [ ] Each blueprint has Visual: Yes or Visual: No on EVERY slide
- [ ] master_index.txt exists and is readable
- [ ] powerpoints/ folder exists and is empty (ready for output)
- [ ] diagrams/ folder exists (for Python-generated visuals)
```

---

**Agent Version:** 2.0 (Theater Adaptation)
**Last Updated:** 2026-01-08

### Version History
- **v2.0** (2026-01-08): Adapted for theater pipeline - NCLEX → Theater naming conventions
- **v1.0** (2026-01-04): Initial blueprint organizer agent
