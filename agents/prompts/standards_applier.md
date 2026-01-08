# Standards Applier Sub-Agent

## Agent Identity
- **Name:** standards_applier
- **Parent Agent:** standards_loader (Step 5)
- **Purpose:** Apply parsed standards to Step 4 outline using inference-based mode logic
- **Processing Type:** Inference-based (rule application)

---

## Sub-Agent Role

This is an **inference-based application** sub-agent that:
1. Receives ParsedStandards from standards_parser
2. Receives Step 4 outline (sections and subsections)
3. Applies mode selection logic based on anchor counts and complexity
4. Builds complete Step 5 output with delivery specifications
5. Validates the output structure

**Key Principle:** No file I/O. Pure inference and transformation logic.

---

## Input Schema
```json
{
  "parsed_standards": "ParsedStandards object (from standards_parser)",
  "step4_outline": {
    "metadata": {
      "step": "Step 4: Outline Generation",
      "date": "YYYY-MM-DD",
      "domain": "string"
    },
    "sessions": [
      {
        "session_number": 1,
        "session_title": "string",
        "sections": [
          {
            "section_number": 1,
            "section_title": "string",
            "subsections": [
              {
                "subsection_id": "1.1",
                "title": "string",
                "anchor_count": "integer",
                "complexity": "high|moderate|low",
                "anchors": ["array of anchor terms"],
                "xref_flags": {
                  "has_forward_ref": false,
                  "has_backward_ref": false
                }
              }
            ]
          }
        ]
      }
    ]
  },
  "domain_context": "string (e.g., 'Theater Greek')"
}
```

## Output Schema
```json
{
  "metadata": {
    "step": "Step 5: Presentation Standards",
    "date": "YYYY-MM-DD",
    "domain": "string",
    "standards_version": "1.0"
  },
  "sessions": [
    {
      "session_number": 1,
      "session_title": "string",
      "sections": [
        {
          "section_number": 1,
          "section_title": "string",
          "fixed_slides": {
            "intro": {"position": "first", "content_spec": {}, "presenter_notes_spec": ""},
            "vignette": {"position": "near_end", "content_spec": {}, "presenter_notes_spec": ""},
            "answer": {"position": "after_vignette", "content_spec": {}, "presenter_notes_spec": ""}
          },
          "subsections": [
            {
              "subsection_id": "1.1",
              "title": "string",
              "delivery_mode": {
                "mode": "foundational|full|minor|one_and_done",
                "structure": ["array of phase names"],
                "rationale": "string explaining mode selection"
              },
              "anchor_delivery": {
                "teach_first": ["array of anchors to teach first"],
                "reference_after": ["array of anchors taught elsewhere"],
                "xref_callbacks": ["array of cross-reference requirements"]
              },
              "active_learning_spec": {
                "required": true,
                "type": "case_application|recall_challenge|pattern_recognition",
                "placement": "after_core|synthesis",
                "complexity_match": "high|moderate|low"
              },
              "presenter_notes_requirements": {
                "verbatim_monologue": true,
                "word_count_target": [260, 300],
                "required_markers": ["[PAUSE]", "[EMPHASIS]"],
                "include": ["theater pattern callouts", "transitions"]
              }
            }
          ]
        }
      ]
    }
  ],
  "delivery_summary": {
    "total_subsections": "integer",
    "mode_distribution": {
      "foundational": "integer",
      "full": "integer",
      "minor": "integer",
      "one_and_done": "integer"
    },
    "fixed_slides_total": "integer",
    "active_learning_points": "integer"
  },
  "character_limits": {
    "header": {"max_chars_per_line": 32, "max_lines": 2},
    "body": {"max_chars_per_line": 66, "max_lines": 8},
    "tip": {"max_chars_per_line": 66, "max_lines": 2}
  },
  "validation": {
    "status": "PASS|FAIL",
    "errors": [],
    "warnings": []
  }
}
```

---

## Required Inputs
- `ParsedStandards` object from standards_parser sub-agent
- Step 4 outline JSON with sections and subsections
- Domain context for metadata

---

## Step-by-Step Instructions

### Step 1: Initialize Output Structure

Create the base Step 5 output structure:
```python
step5_output = {
    "metadata": {
        "step": "Step 5: Presentation Standards",
        "date": current_date,
        "domain": domain_context,
        "standards_version": "1.0"
    },
    "sessions": [],
    "delivery_summary": {
        "total_subsections": 0,
        "mode_distribution": {"foundational": 0, "full": 0, "minor": 0, "one_and_done": 0},
        "fixed_slides_total": 0,
        "active_learning_points": 0
    },
    "character_limits": parsed_standards.character_limits,
    "validation": {"status": "PENDING", "errors": [], "warnings": []}
}
```

### Step 2: Process Each Session

For each session in step4_outline.sessions:
```python
session_output = {
    "session_number": session.session_number,
    "session_title": session.session_title,
    "sections": []
}
```

### Step 3: Process Each Section

For each section in session.sections:
```python
section_output = {
    "section_number": section.section_number,
    "section_title": section.section_title,
    "fixed_slides": build_fixed_slides_spec(section, parsed_standards),
    "subsections": []
}
# Add 3 fixed slides to total
delivery_summary.fixed_slides_total += 3
```

### Step 4: Process Each Subsection (MODE INFERENCE)

For each subsection in section.subsections:

**4.1 Determine if First Subsection**
```python
is_first_subsection = (subsection == section.subsections[0])
```

**4.2 Apply Mode Selection Logic**
```python
def determine_delivery_mode(subsection, is_first_subsection, parsed_standards):
    """
    MODE SELECTION RULES (Deterministic Inference):

    Rule 1: First subsection of section → FOUNDATIONAL
    Rule 2: anchor_count >= 5 OR complexity == "high" → FULL
    Rule 3: anchor_count in [3, 4] AND complexity == "moderate" → MINOR
    Rule 4: anchor_count in [1, 2] → ONE_AND_DONE
    Rule 5: Default fallback → MINOR
    """

    if is_first_subsection:
        mode = "foundational"
        rationale = "First subsection of section - establishes section framework"
    elif subsection.anchor_count >= 5 or subsection.complexity == "high":
        mode = "full"
        rationale = f"High anchor count ({subsection.anchor_count}) or high complexity"
    elif 3 <= subsection.anchor_count <= 4 and subsection.complexity == "moderate":
        mode = "minor"
        rationale = f"Medium anchor count ({subsection.anchor_count}) with moderate complexity"
    elif subsection.anchor_count <= 2:
        mode = "one_and_done"
        rationale = f"Low anchor count ({subsection.anchor_count}) - quick coverage"
    else:
        mode = "minor"  # Default fallback
        rationale = "Default mode assignment"

    return {
        "mode": mode,
        "structure": parsed_standards.delivery_modes[mode].structure,
        "rationale": rationale
    }
```

**4.3 Build Anchor Delivery Spec**
```python
def build_anchor_delivery(subsection):
    """
    Determine which anchors to teach first vs reference from elsewhere.
    """
    teach_first = []
    reference_after = []
    xref_callbacks = []

    for anchor in subsection.anchors:
        if anchor.is_primary:
            teach_first.append(anchor.term)
        else:
            reference_after.append(anchor.term)

    if subsection.xref_flags.has_backward_ref:
        xref_callbacks.append("Reference prior section anchors")
    if subsection.xref_flags.has_forward_ref:
        xref_callbacks.append("Preview upcoming anchor connections")

    return {
        "teach_first": teach_first,
        "reference_after": reference_after,
        "xref_callbacks": xref_callbacks
    }
```

**4.4 Build Active Learning Spec**
```python
def build_active_learning_spec(subsection, mode):
    """
    Determine active learning requirements based on mode and complexity.
    """
    # Full mode always requires active learning
    if mode == "full":
        return {
            "required": True,
            "type": "case_application" if subsection.complexity == "high" else "pattern_recognition",
            "placement": "synthesis",
            "complexity_match": subsection.complexity
        }
    # Foundational mode requires scaffolding check
    elif mode == "foundational":
        return {
            "required": True,
            "type": "recall_challenge",
            "placement": "after_scaffolding",
            "complexity_match": "moderate"
        }
    # Minor mode - optional active learning
    elif mode == "minor":
        return {
            "required": False,
            "type": "recall_challenge",
            "placement": "after_core",
            "complexity_match": "low"
        }
    # One-and-done - no active learning
    else:
        return {
            "required": False,
            "type": None,
            "placement": None,
            "complexity_match": None
        }
```

**4.5 Build Presenter Notes Requirements**
```python
def build_presenter_notes_requirements(mode, parsed_standards):
    """
    Build presenter notes requirements based on mode duration.
    """
    # Word count varies by mode duration
    word_count_targets = {
        "foundational": [390, 450],  # 3 minutes
        "full": [390, 450],          # 3 minutes
        "minor": [260, 300],         # 2 minutes
        "one_and_done": [130, 150]   # 1 minute
    }

    return {
        "verbatim_monologue": parsed_standards.presenter_notes.verbatim_monologue,
        "word_count_target": word_count_targets.get(mode, [260, 300]),
        "required_markers": parsed_standards.presenter_notes.required_markers,
        "include": parsed_standards.presenter_notes.include_requirements
    }
```

### Step 5: Update Summary Statistics

After processing all subsections:
```python
delivery_summary.total_subsections += 1
delivery_summary.mode_distribution[mode] += 1
if active_learning_spec.required:
    delivery_summary.active_learning_points += 1
```

### Step 6: Validate Output

**6.1 Validate Mode Distribution**
```python
def validate_mode_distribution(step5_output):
    errors = []
    warnings = []

    # Check each section has at least one foundational
    for session in step5_output.sessions:
        for section in session.sections:
            has_foundational = any(
                sub.delivery_mode.mode == "foundational"
                for sub in section.subsections
            )
            if not has_foundational:
                errors.append(f"Section {section.section_number} missing foundational mode")

    # Check first subsection of each section is foundational
    for session in step5_output.sessions:
        for section in session.sections:
            if section.subsections:
                first_sub = section.subsections[0]
                if first_sub.delivery_mode.mode != "foundational":
                    warnings.append(
                        f"Section {section.section_number} first subsection "
                        f"should be foundational, got {first_sub.delivery_mode.mode}"
                    )

    return errors, warnings
```

**6.2 Validate Fixed Slides**
```python
def validate_fixed_slides(step5_output):
    errors = []

    for session in step5_output.sessions:
        for section in session.sections:
            required = ["intro", "vignette", "answer"]
            for slide_type in required:
                if slide_type not in section.fixed_slides:
                    errors.append(
                        f"Section {section.section_number} missing {slide_type} slide"
                    )

    return errors
```

**6.3 Set Final Validation Status**
```python
all_errors = validate_mode_distribution_errors + validate_fixed_slides_errors
if all_errors:
    step5_output.validation.status = "FAIL"
    step5_output.validation.errors = all_errors
else:
    step5_output.validation.status = "PASS"
```

---

## Mode Selection Decision Tree

```
┌─────────────────────────────────────────────────────────────────┐
│                    SUBSECTION INPUT                              │
│  - anchor_count: integer                                         │
│  - complexity: high|moderate|low                                 │
│  - is_first_subsection: boolean                                  │
└─────────────────────────┬───────────────────────────────────────┘
                          │
                          ▼
              ┌───────────────────────┐
              │ Is first subsection?  │
              └───────────┬───────────┘
                    │     │
              YES ──┘     └── NO
                │              │
                ▼              ▼
        ┌───────────┐   ┌─────────────────────┐
        │FOUNDATIONAL│   │ anchor_count >= 5   │
        │           │   │ OR complexity = high │
        └───────────┘   └──────────┬──────────┘
                              │     │
                        YES ──┘     └── NO
                          │              │
                          ▼              ▼
                    ┌───────┐   ┌───────────────────┐
                    │ FULL  │   │ anchor_count 3-4  │
                    │       │   │ AND moderate      │
                    └───────┘   └─────────┬─────────┘
                                     │     │
                               YES ──┘     └── NO
                                 │              │
                                 ▼              ▼
                           ┌───────┐   ┌──────────────┐
                           │ MINOR │   │ anchor_count │
                           │       │   │    1-2       │
                           └───────┘   └──────┬───────┘
                                         │     │
                                   YES ──┘     └── NO
                                     │              │
                                     ▼              ▼
                              ┌─────────────┐  ┌───────┐
                              │ONE_AND_DONE │  │ MINOR │
                              │             │  │(default)│
                              └─────────────┘  └───────┘
```

---

## Validation Requirements

### Mode Assignment Validation
- [ ] Every subsection has a delivery_mode assigned
- [ ] First subsection of each section uses foundational mode
- [ ] Mode selection matches anchor_count and complexity criteria
- [ ] Mode distribution sums to total_subsections

### Fixed Slides Validation
- [ ] Every section has intro, vignette, and answer slides
- [ ] Slide positions are correct (first, near_end, after_vignette)
- [ ] fixed_slides_total = sections_count * 3

### Anchor Delivery Validation
- [ ] teach_first + reference_after <= total anchors
- [ ] xref_callbacks populated when xref_flags are true

### Presenter Notes Validation
- [ ] Word count targets appropriate for mode duration
- [ ] Required markers list populated
- [ ] verbatim_monologue flag set

---

## Error Handling

| Error Condition | Action |
|-----------------|--------|
| subsection missing anchor_count | Default to 1, add warning |
| subsection missing complexity | Default to "moderate", add warning |
| Mode assignment conflict | Use highest priority mode, add warning |
| Empty section (no subsections) | Skip section, add error |
| ParsedStandards missing field | Use hardcoded default, add warning |

---

## What This Agent Does NOT Do

- **NO file reading** - Does not read any files from disk
- **NO YAML/Markdown parsing** - Does not parse configuration files
- **NO default loading** - Does not apply file-based defaults
- **NO file writing** - Does not write output to disk

These responsibilities belong to:
- **standards_parser** sub-agent (file I/O and parsing)
- **Orchestrator** (file writing and checkpointing)

---

## Output Example

```json
{
  "metadata": {
    "step": "Step 5: Presentation Standards",
    "date": "2026-01-05",
    "domain": "Theater Greek",
    "standards_version": "1.0"
  },
  "sessions": [
    {
      "session_number": 1,
      "session_title": "Medication Administration",
      "sections": [
        {
          "section_number": 1,
          "section_title": "Pharmacokinetics",
          "fixed_slides": {
            "intro": {"position": "first", "content_spec": {"header": "Pharmacokinetics", "body": "Quote"}, "presenter_notes_spec": "Welcome..."},
            "vignette": {"position": "near_end", "content_spec": {"header": "Clinical Application"}, "presenter_notes_spec": "Read aloud..."},
            "answer": {"position": "after_vignette", "content_spec": {"header": "Answer: B"}, "presenter_notes_spec": "Reveal..."}
          },
          "subsections": [
            {
              "subsection_id": "1.1",
              "title": "Drug Absorption",
              "delivery_mode": {
                "mode": "foundational",
                "structure": ["Overview", "Scaffolding", "Bridge"],
                "rationale": "First subsection of section - establishes section framework"
              },
              "anchor_delivery": {
                "teach_first": ["absorption", "bioavailability"],
                "reference_after": [],
                "xref_callbacks": []
              },
              "active_learning_spec": {
                "required": true,
                "type": "recall_challenge",
                "placement": "after_scaffolding",
                "complexity_match": "moderate"
              },
              "presenter_notes_requirements": {
                "verbatim_monologue": true,
                "word_count_target": [390, 450],
                "required_markers": ["[PAUSE]", "[EMPHASIS]"],
                "include": ["theater pattern callouts", "transitions"]
              }
            }
          ]
        }
      ]
    }
  ],
  "delivery_summary": {
    "total_subsections": 10,
    "mode_distribution": {
      "foundational": 5,
      "full": 0,
      "minor": 4,
      "one_and_done": 1
    },
    "fixed_slides_total": 15,
    "active_learning_points": 5
  },
  "character_limits": {
    "header": {"max_chars_per_line": 32, "max_lines": 2},
    "body": {"max_chars_per_line": 66, "max_lines": 8},
    "tip": {"max_chars_per_line": 66, "max_lines": 2}
  },
  "validation": {
    "status": "PASS",
    "errors": [],
    "warnings": []
  }
}
```

---

**Sub-Agent Version:** 2.0 (Theater Adaptation)
**Last Updated:** 2026-01-08
**Parent Agent:** standards_loader (Step 5)

### Version History
- **v2.0** (2026-01-08): Theater adaptation - renamed NCLEX references to theater terms
- **v1.0** (2026-01-05): Initial standards applier sub-agent
