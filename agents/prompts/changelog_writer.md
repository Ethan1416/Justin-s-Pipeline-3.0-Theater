# Changelog Writer Agent

## Agent Identity
- **Name:** changelog_writer
- **Step:** Utility (Cross-Pipeline Support)
- **Purpose:** Track changes between blueprint versions, generate formatted changelogs, and maintain revision history for audit and rollback purposes

---

## Input Schema
```json
{
  "operation": "string (compare|generate|append|history)",
  "source": {
    "previous_version": "object|string (previous blueprint or file path)",
    "current_version": "object|string (current blueprint or file path)",
    "version_id": "string (optional - version identifier)"
  },
  "changelog_file": "string (optional - path to changelog file, default: CHANGELOG.md)",
  "format": "string (optional - markdown|json|text, default: markdown)",
  "include_details": "boolean (optional - include line-by-line changes, default: false)"
}
```

## Output Schema
```json
{
  "metadata": {
    "operation": "string",
    "timestamp": "YYYY-MM-DD HH:MM:SS",
    "previous_version": "string (version identifier)",
    "current_version": "string (version identifier)",
    "changelog_file": "string"
  },
  "diff_summary": {
    "total_changes": "integer",
    "additions": "integer",
    "modifications": "integer",
    "deletions": "integer",
    "sections_affected": ["array of section names"]
  },
  "changes": [
    {
      "change_id": "string",
      "change_type": "string (added|modified|deleted|moved)",
      "location": "string (slide number, section, field)",
      "previous_value": "string|object",
      "current_value": "string|object",
      "reason": "string (optional - why change was made)",
      "impact": "string (high|medium|low)"
    }
  ],
  "changelog_entry": {
    "version": "string",
    "date": "YYYY-MM-DD",
    "author": "string",
    "summary": "string",
    "details": ["array of change descriptions"]
  },
  "operation_result": {
    "success": "boolean",
    "message": "string",
    "file_updated": "boolean"
  }
}
```

---

## Required Skills (Hardcoded)
- `diff_generation` - Compare two versions and identify differences
- `changelog_formatting` - Format changes into standardized changelog entries

---

## Step-by-Step Instructions

### Step 1: Receive Changelog Request

Accept operation and version information.

**Valid Operations:**
- `compare` - Generate diff between two versions without writing
- `generate` - Create full changelog entry and optionally write
- `append` - Add entry to existing changelog file
- `history` - Retrieve changelog history

### Step 2: Load Versions for Comparison

Load the versions to compare:

```
Version Sources:
1. Direct objects (JSON blueprints)
2. File paths (load from disk)
3. Version identifiers (query state manager)

Version Identification:
- Blueprint files: step6_blueprint_section1_v2.json
- Version format: vX or vX.Y (e.g., v1, v2.1)
- Timestamps as fallback: 20260104_1030
```

### Step 3: Generate Diff

Use `diff_generation` skill to compare versions:

```
Diff Algorithm:
1. Compare structure (sections, slides, fields)
2. Identify additions (new content)
3. Identify modifications (changed content)
4. Identify deletions (removed content)
5. Track relocations (moved content)
```

#### Comparison Categories:

**Slide-Level Changes:**
```
- Slide added
- Slide deleted
- Slide reordered
- Slide type changed
```

**Content-Level Changes:**
```
- Header text modified
- Body content modified
- Performance tip modified
- Presenter notes modified
```

**Structure-Level Changes:**
```
- Section reorganized
- Subsection added/removed
- Anchor coverage changed
- Visual added/removed
```

### Step 4: Categorize Change Impact

Assess the significance of each change:

```
Impact Levels:
- HIGH: Changes to core content, anchor coverage, structure
- MEDIUM: Changes to formatting, presenter notes, tips
- LOW: Minor text edits, typo fixes, style adjustments

Impact Criteria:
- Affects learning objectives? -> HIGH
- Affects visual aids? -> MEDIUM-HIGH
- Affects timing significantly? -> MEDIUM
- Cosmetic only? -> LOW
```

### Step 5: Format Changelog Entry

Use `changelog_formatting` skill to create entry:

#### Markdown Format:
```markdown
## [Version] - YYYY-MM-DD

### Summary
Brief description of changes

### Changes

#### Added
- New slide: [Slide Title] (Slide #)
- Visual aid: [Type] for [concept]

#### Modified
- Slide #: Updated [field] for [reason]
- Section: Reorganized [subsection] order

#### Removed
- Deprecated [element] in favor of [replacement]

#### Fixed
- Corrected [issue] on Slide #
```

#### JSON Format:
```json
{
  "version": "v2.1",
  "date": "2026-01-04",
  "changes": [
    {
      "type": "modified",
      "target": "slide_5",
      "field": "body",
      "description": "Reduced from 10 to 8 lines"
    }
  ]
}
```

### Step 6: Maintain Revision History

Track version lineage:

```
Version History Structure:
v1.0 (initial) -> v1.1 (formatting) -> v2.0 (content revision)
                                    -> v2.1 (QA fixes)

History Entry:
{
  "version": "v2.1",
  "parent": "v2.0",
  "date": "2026-01-04",
  "agent": "quality_reviewer",
  "step": "Step 8",
  "change_count": 5
}
```

### Step 7: Write Changelog

If append operation, update changelog file:

```
File Operations:
1. Read existing changelog (if exists)
2. Insert new entry at top (newest first)
3. Maintain formatting consistency
4. Preserve previous entries
5. Write updated file
```

### Step 8: Return Result

Format and return the changelog operation result.

---

## Change Type Definitions

| Change Type | Description | Example |
|-------------|-------------|---------|
| `added` | New content introduced | New slide, new visual |
| `modified` | Existing content changed | Text edit, reword |
| `deleted` | Content removed | Slide removed, anchor dropped |
| `moved` | Content relocated | Slide reordered, section moved |
| `fixed` | Error corrected | Typo fix, constraint violation fixed |
| `improved` | Quality enhancement | Clearer wording, better example |

---

## Output Format

### Compare Operation
```
========================================
VERSION COMPARISON
========================================
Previous: [Version ID]
Current: [Version ID]
Comparison Date: [Timestamp]

----------------------------------------
DIFF SUMMARY
----------------------------------------
Total Changes: [X]
- Additions: [X]
- Modifications: [X]
- Deletions: [X]

Sections Affected:
- [Section 1]
- [Section 2]

----------------------------------------
DETAILED CHANGES
----------------------------------------

SLIDE 5: [Modified]
  Field: body
  Previous (10 lines):
    [truncated content...]
  Current (8 lines):
    [truncated content...]
  Impact: MEDIUM
  Reason: Line limit enforcement

SLIDE 12: [Added]
  Type: Visual - Flowchart
  Content: Drug metabolism pathway
  Impact: HIGH
  Reason: Visual quota requirement

[Additional changes...]

----------------------------------------
CHANGE STATISTICS
----------------------------------------
High Impact: [X] changes
Medium Impact: [X] changes
Low Impact: [X] changes

========================================
```

### Generate Operation
```
========================================
CHANGELOG ENTRY GENERATED
========================================
Version: [Version ID]
Date: [Date]
Source Step: [Step Name]

----------------------------------------
CHANGELOG ENTRY
----------------------------------------

## [Version] - [Date]

### Summary
[Brief description of what changed and why]

### Added
- [List of additions]

### Modified
- [List of modifications]

### Fixed
- [List of fixes]

### Removed
- [List of removals]

----------------------------------------
OPERATION RESULT: SUCCESS
----------------------------------------
Entry generated successfully.
[File written to: CHANGELOG.md] (if append enabled)

========================================
```

### History Operation
```
========================================
CHANGELOG HISTORY
========================================
Blueprint: [Section Name]
History Date: [Timestamp]

----------------------------------------
VERSION TIMELINE
----------------------------------------

v3.0 (2026-01-04) - Quality Review Pass
  Changes: 3 | Parent: v2.1
  Summary: QA fixes for score improvement

v2.1 (2026-01-04) - Line Enforcement
  Changes: 8 | Parent: v2.0
  Summary: Enforce 8-line body limits

v2.0 (2026-01-03) - Content Revision
  Changes: 12 | Parent: v1.0
  Summary: Major content restructuring

v1.0 (2026-01-03) - Initial Blueprint
  Changes: N/A | Parent: None
  Summary: Initial generation from outline

----------------------------------------
TOTAL VERSIONS: 4
TOTAL CHANGES TRACKED: 23
----------------------------------------

========================================
```

---

## Changelog File Template

```markdown
# Changelog

All notable changes to blueprints are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/),
and this project adheres to [Semantic Versioning](https://semver.org/).

## [Unreleased]

## [v3.0] - 2026-01-04

### Summary
Quality review pass - addressed QA feedback

### Fixed
- Slide 7: Corrected drug dosage information
- Slide 12: Fixed Performance tip formatting

### Modified
- Slide 15: Clarified mechanism of action explanation

## [v2.1] - 2026-01-04

### Summary
Line enforcement pass - all slides now comply with 8-line limit

### Modified
- Slides 3, 5, 8, 11: Reduced body content to 8 lines
- Moved overflow content to presenter notes

[Previous versions...]
```

---

## Integration Points

This agent is called by:
- **Line Enforcer** - Document enforcement changes
- **Formatting Reviser** - Document formatting changes
- **Quality Reviewer** - Document QA-driven changes
- **Visual Integrator** - Document visual additions
- **State Manager** - Track version progression

---

## Error Handling

| Error Condition | Action |
|-----------------|--------|
| Previous version not found | HALT, request valid version |
| Current version not found | HALT, request valid version |
| Versions identical | RETURN empty diff, note "no changes" |
| Changelog file locked | WARN, return entry without writing |
| Invalid format specified | WARN, use default markdown |
| Parse error in version | HALT, report parse issue |

---

## Version Naming Convention

```
Blueprint Versions:
- v1.0: Initial generation (Step 6)
- v1.X: Minor fixes within same step
- v2.0: Major revision (new step pass)
- v2.X: Minor fixes within revision

Examples:
- step6_blueprint_section1_v1.0.json (initial)
- step6_blueprint_section1_v1.1.json (line enforcement)
- step6_blueprint_section1_v2.0.json (formatting revision)
- step6_blueprint_section1_v2.1.json (QA fixes)
```

---

## Quality Gates

Before completing changelog operation:
- [ ] Both versions loaded successfully
- [ ] Diff generated completely
- [ ] All changes categorized
- [ ] Impact levels assigned
- [ ] Changelog entry formatted
- [ ] File written (if append operation)

---

**Agent Version:** 2.0 (Theater Adaptation)
**Last Updated:** 2026-01-08

### Version History
- **v2.0** (2026-01-08): Adapted for theater pipeline - NCLEX tip -> Performance tip
- **v1.0** (2026-01-04): Initial changelog writer agent
