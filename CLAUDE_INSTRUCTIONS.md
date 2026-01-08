# CLAUDE_INSTRUCTIONS.md
## NCLEX Lecture Generation Pipeline - Instructions for Claude

This file contains persistent instructions for Claude when working with this pipeline.
**Read this file FIRST before making any changes to the pipeline.**

---

## Repository Structure

```
JustinPipeline/
├── templates/                    # MASTER TEMPLATES (DO NOT MODIFY)
│   ├── content_master.pptx      # For general content slides
│   └── visual_organizer.pptx    # For Q&A and graphic organizer slides
├── docs/                         # Step documentation files
├── pipeline_config.json          # Central configuration (v3.0+)
├── step12_powerpoint_population.py  # Main PowerPoint generation script
└── CLAUDE_INSTRUCTIONS.md        # THIS FILE
```

---

## Critical Rules

### 1. Template Files
- **NEVER modify** files in `templates/` folder directly
- **ALWAYS use** relative paths from repo root
- Templates:
  - `templates/content_master.pptx` - General content slides
  - `templates/visual_organizer.pptx` - Q&A and graphic organizer slides

### 2. Path Management
- **ALL paths in config must be relative** to repository root
- Exception: `paths.production_folder` is set at runtime (absolute path)
- **NEVER use hardcoded absolute paths** like `C:\Users\...\OneDrive\...`
- When code needs templates, use:
  ```python
  REPO_ROOT = Path(__file__).parent
  TEMPLATE_PATH = REPO_ROOT / CONFIG['templates']['content_master']
  ```

### 3. Config Structure (v3.0+)
```json
{
  "templates": {
    "content_master": "templates/content_master.pptx",
    "visual_organizer": "templates/visual_organizer.pptx"
  },
  "paths": {
    "production_folder": null  // SET AT RUNTIME
  }
}
```

### 4. Starting a New Production Run
Before generating PowerPoints:
1. Update `pipeline_config.json`:
   - Set `domain.name` and `domain.display_name`
   - Set `domain.date` to current date (YYYY-MM-DD)
   - Set `paths.production_folder` to the output folder

### 5. Visual Types
The pipeline supports 7 graphic organizer types:
1. **TABLE** - Comparison tables, feature lists
2. **FLOWCHART** - Process flows, sequences
3. **DECISION_TREE** - Diagnostic criteria, branching logic
4. **TIMELINE** - Historical events, developmental stages
5. **HIERARCHY** - Classification systems, organizational structures
6. **SPECTRUM** - Severity scales, continua
7. **KEY_DIFFERENTIATORS** - Similar concept discrimination

Each type has settings in `pipeline_config.json` under `template_requirements.*_settings`.

---

## Slide Content Constraints

### Character Limits (from config)
- **Title**: 32 chars/line, max 2 lines
- **Body**: 66 chars/line, max 8 lines
- **Tip**: 66 chars/line, max 2 lines

### Presenter Notes
- Max duration: 180 seconds
- Speaking rate: 150 words/minute
- Max words: 450

### Visual Quotas (MANDATORY)
Every section must have minimum graphic organizers:
- 12-15 slides: minimum 2 visuals
- 16-20 slides: minimum 3 visuals
- 21-25 slides: minimum 3 visuals
- 26-35 slides: minimum 4 visuals

---

## Common Tasks

### Generating PowerPoints
```python
# Production folder must be set in config first
python step12_powerpoint_population.py
```

### Validating Blueprints
```python
python validate_blueprint_line_count.py "path/to/blueprints"
```

---

## Troubleshooting

### "Config file not found"
- Ensure `pipeline_config.json` is in repository root
- Check you're running from the JustinPipeline directory

### "Missing production_folder"
- Set `paths.production_folder` in `pipeline_config.json` before running

### Template not found
- Verify templates exist in `templates/` folder
- Check template paths in config use forward slashes

---

## Git Workflow

1. Always pull latest before making changes
2. Test changes locally before committing
3. Commit with descriptive messages
4. Push to main branch

```bash
cd C:\Users\mcdan\JustinPipeline
git pull origin main
# make changes
git add .
git commit -m "Description of changes"
git push origin main
```

---

## Version History

- **v3.0** (2026-01-01): GitHub-based with centralized templates, relative paths
- **v2.0** (2025-12-23): Extended with 7 graphic organizer types
- **v1.0**: Original pipeline

---

**Last Updated**: 2026-01-01
**Maintainer**: ethangrucza@gmail.com
