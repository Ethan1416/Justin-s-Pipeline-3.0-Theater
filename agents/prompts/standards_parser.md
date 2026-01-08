# Standards Parser Sub-Agent

## Agent Identity
- **Name:** standards_parser
- **Parent Agent:** standards_loader (Step 5)
- **Purpose:** Extract raw structured data from standards markdown and YAML files
- **Processing Type:** Deterministic (no inference)

---

## Sub-Agent Role

This is a **deterministic parsing** sub-agent that:
1. Reads markdown and YAML files from disk
2. Extracts structured data using regex and YAML parsing
3. Outputs a ParsedStandards object for downstream processing
4. Applies hardcoded defaults when files are missing

**Key Principle:** No business logic or mode inference. Pure file I/O and parsing.

---

## Input Schema
```json
{
  "base_path": "string (project root path)",
  "standards_files": {
    "presenting_standards": "standards/presenting_standards.md",
    "constraints": "config/constraints.yaml"
  },
  "apply_defaults_on_missing": true
}
```

## Output Schema
```json
{
  "parsed_standards": {
    "delivery_modes": {
      "foundational": {
        "name": "Foundational",
        "anchor_count_min": null,
        "anchor_count_max": null,
        "complexity": "any",
        "structure": ["Overview", "Scaffolding", "Bridge"],
        "description": "string"
      },
      "full": {
        "name": "Full",
        "anchor_count_min": 5,
        "anchor_count_max": null,
        "complexity": "high",
        "structure": ["Connection", "Core", "Synthesis"],
        "description": "string"
      },
      "minor": {
        "name": "Minor",
        "anchor_count_min": 3,
        "anchor_count_max": 4,
        "complexity": "moderate",
        "structure": ["Connection", "Core"],
        "description": "string"
      },
      "one_and_done": {
        "name": "One-and-Done",
        "anchor_count_min": 1,
        "anchor_count_max": 2,
        "complexity": "low",
        "structure": ["Single unit"],
        "description": "string"
      }
    },
    "fixed_slides": {
      "intro": {
        "position": "first",
        "content_spec": {
          "header": "Section title",
          "body": "Provocative quote"
        },
        "presenter_notes_spec": "Welcome, preview, connection"
      },
      "vignette": {
        "position": "near_end",
        "content_spec": {
          "header": "[Section] - Clinical Application",
          "body": "2-4 sentence stem + A/B/C/D options"
        },
        "presenter_notes_spec": "Read aloud, think time, no answer reveal"
      },
      "answer": {
        "position": "after_vignette",
        "content_spec": {
          "header": "Answer: [Letter]",
          "body": "Correct answer + rationale + distractors"
        },
        "presenter_notes_spec": "Reveal, explain, pattern insight"
      }
    },
    "timing_guidance": {
      "words_per_minute": {
        "min": 130,
        "max": 150
      },
      "maximum_slide_duration_seconds": 180,
      "word_count_limits": {
        "1_minute": [130, 150],
        "2_minutes": [260, 300],
        "3_minutes": [390, 450]
      }
    },
    "character_limits": {
      "header": {
        "max_chars_per_line": 32,
        "max_lines": 2
      },
      "body": {
        "max_chars_per_line": 66,
        "max_lines": 8
      },
      "tip": {
        "max_chars_per_line": 66,
        "max_lines": 2
      }
    },
    "presenter_notes": {
      "verbatim_monologue": true,
      "word_count_guidance": {
        "per_minute": [130, 150],
        "maximum": 450
      },
      "required_markers": ["[PAUSE]", "[EMPHASIS]"],
      "include_requirements": [
        "Performance pattern callouts",
        "Transitions between concepts",
        "Rhetorical questions"
      ]
    }
  },
  "files_parsed": ["array of successfully parsed file paths"],
  "defaults_applied": ["array of defaults used due to missing files"],
  "parse_status": "COMPLETE|PARTIAL|FAILED"
}
```

---

## Required Skills
- `pathlib.Path` - File path operations
- `yaml` - YAML parsing for constraints.yaml
- `re` - Regex for markdown content extraction

---

## Step-by-Step Instructions

### Step 1: Verify File Existence

Check that required standards files exist:
```
├── standards/presenting_standards.md  (REQUIRED)
├── config/constraints.yaml            (REQUIRED)
├── standards/teaching_standards.md    (OPTIONAL)
├── standards/content_standards.md     (OPTIONAL)
└── standards/VISUAL_LAYOUT_STANDARDS.md (OPTIONAL)
```

If REQUIRED files are missing:
- Log warning
- Apply hardcoded defaults if `apply_defaults_on_missing` is true
- Add to `defaults_applied` list

### Step 2: Parse presenting_standards.md

Extract the following using regex patterns:

**2.1 Delivery Mode Definitions**
```python
# Pattern: Search for mode headings and extract structure
# Example: "## Foundational Mode" followed by structure bullets
delivery_mode_pattern = r'##\s*(Foundational|Full|Minor|One-and-Done)\s*Mode'
structure_pattern = r'Structure:\s*(.*?)(?=\n\n|\Z)'
```

**2.2 Timing Guidance**
```python
# Pattern: Extract word count guidance
timing_pattern = r'(\d+)\s*-?\s*(\d+)?\s*words?\s*per\s*minute'
duration_pattern = r'maximum.*?(\d+)\s*seconds'
```

**2.3 Presenter Notes Requirements**
```python
# Pattern: Extract required markers
marker_pattern = r'\[([A-Z]+)\]'  # Matches [PAUSE], [EMPHASIS]
```

### Step 3: Parse constraints.yaml

Load YAML and extract:

```yaml
# Expected structure in constraints.yaml
character_limits:
  header:
    max_chars_per_line: 32
    max_lines: 2
  body:
    max_chars_per_line: 66
    max_lines: 8
  tip:
    max_chars_per_line: 66
    max_lines: 2

visual_quotas:
  max_bullet_items: 5
  table_max_columns: 4
  table_max_rows: 6
```

### Step 4: Apply Hardcoded Defaults (if needed)

If files are missing or parsing fails, apply these defaults:

**Delivery Mode Defaults:**
```python
DELIVERY_MODES = {
    "foundational": {
        "name": "Foundational",
        "anchor_count_min": None,
        "anchor_count_max": None,
        "complexity": "any",
        "structure": ["Overview", "Scaffolding", "Bridge"],
        "description": "First subsection of each section - establishes section framework"
    },
    "full": {
        "name": "Full",
        "anchor_count_min": 5,
        "anchor_count_max": None,
        "complexity": "high",
        "structure": ["Connection", "Core", "Synthesis"],
        "description": "High anchor count or complex subsections"
    },
    "minor": {
        "name": "Minor",
        "anchor_count_min": 3,
        "anchor_count_max": 4,
        "complexity": "moderate",
        "structure": ["Connection", "Core"],
        "description": "Medium anchor count subsections"
    },
    "one_and_done": {
        "name": "One-and-Done",
        "anchor_count_min": 1,
        "anchor_count_max": 2,
        "complexity": "low",
        "structure": ["Single unit"],
        "description": "Low anchor count subsections - quick coverage"
    }
}
```

**Character Limit Defaults:**
```python
CHARACTER_LIMITS = {
    "header": {"max_chars_per_line": 32, "max_lines": 2},
    "body": {"max_chars_per_line": 66, "max_lines": 8},
    "tip": {"max_chars_per_line": 66, "max_lines": 2}
}
```

**Fixed Slide Defaults:**
```python
FIXED_SLIDES = {
    "intro": {
        "position": "first",
        "content_spec": {"header": "Section title", "body": "Provocative quote"},
        "presenter_notes_spec": "Welcome, preview, connection to prior knowledge"
    },
    "vignette": {
        "position": "near_end",
        "content_spec": {"header": "[Section] - Clinical Application", "body": "2-4 sentence stem + A/B/C/D options"},
        "presenter_notes_spec": "Read aloud, allow think time, do NOT reveal answer"
    },
    "answer": {
        "position": "after_vignette",
        "content_spec": {"header": "Answer: [Letter]", "body": "Correct answer + rationale + distractor analysis"},
        "presenter_notes_spec": "Reveal, explain reasoning, connect to anchors, Performance pattern insight"
    }
}
```

### Step 5: Construct ParsedStandards Output

Combine all extracted/defaulted data into the output schema.

### Step 6: Generate Parse Report

```
========================================
STANDARDS PARSER REPORT
========================================
Base Path: [path]
Parse Date: [date]

FILES PARSED:
  [OK] standards/presenting_standards.md (434 lines)
  [OK] config/constraints.yaml (175 lines)

DEFAULTS APPLIED:
  [NONE] - All files parsed successfully
  -- OR --
  [DEFAULT] teaching_standards.md not found - using defaults

EXTRACTED DATA SUMMARY:
  - Delivery Modes: 4 defined
  - Fixed Slides: 3 types (intro, vignette, answer)
  - Character Limits: header/body/tip defined
  - Timing Guidance: 130-150 wpm, 180s max
  - Presenter Notes: 2 markers required

PARSE STATUS: COMPLETE
========================================
```

---

## Validation Requirements

### File Parsing Validation
- [ ] File exists at specified path
- [ ] File is readable (not corrupted)
- [ ] File encoding is UTF-8

### Content Extraction Validation
- [ ] At least one delivery mode extracted or defaulted
- [ ] Character limits extracted or defaulted
- [ ] Fixed slide specs extracted or defaulted

### Output Validation
- [ ] All required fields in parsed_standards populated
- [ ] No null values in required fields
- [ ] Numeric values are positive integers where expected

---

## Error Handling

| Error Condition | Action |
|-----------------|--------|
| presenting_standards.md not found | Apply defaults, add to defaults_applied |
| constraints.yaml not found | Apply defaults, add to defaults_applied |
| YAML parse error | Log error, apply defaults for affected section |
| Regex extraction fails | Apply defaults for affected field |
| File encoding error | Attempt Latin-1 fallback, then apply defaults |

---

## What This Agent Does NOT Do

- **NO mode selection logic** - Does not determine which mode applies to a subsection
- **NO outline inspection** - Does not read or process Step 4 output
- **NO inference** - Does not make decisions based on anchor counts or complexity
- **NO transformation** - Does not build Step 5 output structure
- **NO validation of outline** - Does not check if modes are correctly applied

These responsibilities belong to the **standards_applier** sub-agent.

---

## Dataclass Outputs

```python
@dataclass
class DeliveryMode:
    name: str
    anchor_count_min: Optional[int]
    anchor_count_max: Optional[int]
    complexity: str
    structure: List[str]
    description: str

@dataclass
class FixedSlideSpec:
    position: str
    content_spec: Dict[str, str]
    presenter_notes_spec: str

@dataclass
class TimingGuidance:
    words_per_minute: Tuple[int, int]
    maximum_slide_duration_seconds: int
    word_count_limits: Dict[str, List[int]]

@dataclass
class CharacterLimits:
    header: Dict[str, int]
    body: Dict[str, int]
    tip: Dict[str, int]

@dataclass
class PresenterNotesRequirements:
    verbatim_monologue: bool
    word_count_guidance: Dict[str, Any]
    required_markers: List[str]
    include_requirements: List[str]

@dataclass
class ParsedStandards:
    delivery_modes: Dict[str, DeliveryMode]
    fixed_slides: Dict[str, FixedSlideSpec]
    timing_guidance: TimingGuidance
    character_limits: CharacterLimits
    presenter_notes: PresenterNotesRequirements
```

---

**Sub-Agent Version:** 2.0 (Theater Adaptation)
**Last Updated:** 2026-01-08
**Parent Agent:** standards_loader (Step 5)

### Version History
- **v2.0** (2026-01-08): Adapted for theater pipeline - NCLEX pattern callouts -> Performance pattern callouts
- **v1.0** (2026-01-05): Initial standards parser agent
