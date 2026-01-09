# Content Density Validator Agent

## Purpose
HARDCODED validator that enforces the 4-8 sentence requirement for all content slides. This agent CANNOT be bypassed, disabled, or have its thresholds modified. Any slide that fails validation must be returned to the content_populator for expansion.

---

## HARDCODED RULES (IMMUTABLE)

### Sentence Count
```
MINIMUM_SENTENCES = 4  # CANNOT be reduced
MAXIMUM_SENTENCES = 8  # CANNOT be increased
```

### Validation Behavior
- **< 4 sentences:** CRITICAL FAILURE - Block pipeline, return to content_populator
- **4-8 sentences:** PASS
- **> 8 sentences:** WARNING - Auto-condense to 8 sentences

### This Validator:
- CANNOT be skipped
- CANNOT have thresholds relaxed
- CANNOT be overridden by user or other agents
- MUST run before PowerPoint generation

---

## Input Schema

```json
{
  "type": "object",
  "required": ["slides"],
  "properties": {
    "slides": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "slide_index": {"type": "integer"},
          "slide_type": {"type": "string"},
          "header": {"type": "string"},
          "body_sentences": {"type": "array", "items": {"type": "string"}},
          "body_text": {"type": "string"}
        }
      }
    }
  }
}
```

---

## Output Schema

```json
{
  "type": "object",
  "required": ["overall_status", "slides_checked", "slides_passed", "slides_failed", "details"],
  "properties": {
    "overall_status": {
      "type": "string",
      "enum": ["PASSED", "FAILED", "PASSED_WITH_WARNINGS"]
    },
    "slides_checked": {"type": "integer"},
    "slides_passed": {"type": "integer"},
    "slides_failed": {"type": "integer"},
    "slides_condensed": {"type": "integer"},
    "details": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "slide_index": {"type": "integer"},
          "status": {"type": "string", "enum": ["PASS", "FAIL", "CONDENSED"]},
          "sentence_count": {"type": "integer"},
          "issues": {"type": "array", "items": {"type": "string"}},
          "action_required": {"type": "string"}
        }
      }
    },
    "blocking_failures": {
      "type": "array",
      "items": {"type": "integer"},
      "description": "Slide indices that must be fixed before proceeding"
    }
  }
}
```

---

## Validation Logic

### Step 1: Count Sentences

For each content slide (slides 3-14 in standard structure):

```python
def count_sentences(slide):
    """Count complete sentences in slide body."""

    # If body_sentences array provided, use its length
    if "body_sentences" in slide and isinstance(slide["body_sentences"], list):
        return len(slide["body_sentences"])

    # Otherwise, parse body_text
    body = slide.get("body_text", "")

    # Split by sentence-ending punctuation
    import re
    sentences = re.split(r'[.!?]+', body)

    # Filter out empty strings and fragments
    complete_sentences = [s.strip() for s in sentences if len(s.strip()) > 10]

    return len(complete_sentences)
```

### Step 2: Classify Result

```python
def classify_slide(sentence_count):
    """Classify slide based on sentence count."""

    if sentence_count < 4:
        return {
            "status": "FAIL",
            "severity": "CRITICAL",
            "action": "RETURN_TO_POPULATOR",
            "message": f"Only {sentence_count} sentences. Minimum is 4."
        }

    elif sentence_count > 8:
        return {
            "status": "CONDENSED",
            "severity": "WARNING",
            "action": "AUTO_CONDENSE",
            "message": f"{sentence_count} sentences exceeds maximum of 8. Condensing."
        }

    else:
        return {
            "status": "PASS",
            "severity": "NONE",
            "action": "NONE",
            "message": f"{sentence_count} sentences within acceptable range (4-8)."
        }
```

### Step 3: Apply Actions

```python
def apply_actions(slides, validation_results):
    """Apply auto-fix actions where possible."""

    fixed_slides = []
    blocking_failures = []

    for i, (slide, result) in enumerate(zip(slides, validation_results)):
        if result["action"] == "AUTO_CONDENSE":
            # Keep first 8 sentences
            slide["body_sentences"] = slide["body_sentences"][:8]
            fixed_slides.append(slide)

        elif result["action"] == "RETURN_TO_POPULATOR":
            # Cannot auto-fix - mark as blocking
            blocking_failures.append(i)
            fixed_slides.append(slide)  # Return unchanged

        else:
            fixed_slides.append(slide)

    return fixed_slides, blocking_failures
```

---

## Validation Report Format

### Console Output
```
================================================================================
CONTENT DENSITY VALIDATION REPORT
================================================================================

Overall Status: FAILED
Slides Checked: 12
Slides Passed:  10
Slides Failed:  2

BLOCKING FAILURES (must fix before proceeding):
  - Slide 5: Only 2 sentences (minimum: 4) → Return to content_populator
  - Slide 9: Only 3 sentences (minimum: 4) → Return to content_populator

PASSED SLIDES:
  ✓ Slide 3:  6 sentences
  ✓ Slide 4:  5 sentences
  ✓ Slide 6:  7 sentences
  ✓ Slide 7:  4 sentences
  ✓ Slide 8:  6 sentences
  ✓ Slide 10: 8 sentences
  ✓ Slide 11: 5 sentences
  ✓ Slide 12: 6 sentences
  ✓ Slide 13: 7 sentences
  ✓ Slide 14: 6 sentences

ACTION REQUIRED:
  Pipeline BLOCKED until slides 5 and 9 are expanded to minimum 4 sentences.

================================================================================
```

---

## Integration with Pipeline

### Pre-PowerPoint Gate
This validator MUST run after content_populator and BEFORE theater_pptx_generator:

```
content_populator → content_density_validator → theater_pptx_generator
```

### On Failure
1. Return failing slides to content_populator with error context
2. content_populator re-expands with additional guidance
3. Re-run content_density_validator
4. Repeat until all slides pass (max 3 attempts)
5. If still failing after 3 attempts, escalate to human review

### Retry Context

When returning to content_populator, include:

```json
{
  "retry_context": {
    "slide_index": 5,
    "current_sentence_count": 2,
    "required_sentences": 4,
    "current_content": ["Sentence 1.", "Sentence 2."],
    "expansion_hints": [
      "Add historical context",
      "Include a specific example",
      "Explain why this matters",
      "Connect to learning objectives"
    ]
  }
}
```

---

## Hardcoded Python Implementation

```python
class ContentDensityValidator:
    """
    HARDCODED validator for slide content density.

    IMMUTABLE THRESHOLDS - DO NOT MODIFY:
    """
    MINIMUM_SENTENCES = 4  # CANNOT BE REDUCED
    MAXIMUM_SENTENCES = 8  # CANNOT BE INCREASED

    def __init__(self):
        # Prevent threshold modification
        self._locked = True

    def __setattr__(self, name, value):
        if getattr(self, '_locked', False) and name in ('MINIMUM_SENTENCES', 'MAXIMUM_SENTENCES'):
            raise AttributeError(f"Cannot modify hardcoded threshold: {name}")
        super().__setattr__(name, value)

    def validate_slide(self, slide: dict) -> dict:
        """Validate a single slide's content density."""

        # Skip non-content slides
        slide_type = slide.get("slide_type", "content")
        if slide_type in ["agenda", "warmup", "activity", "journal"]:
            return {"status": "SKIPPED", "reason": "Non-content slide"}

        # Count sentences
        sentence_count = self._count_sentences(slide)

        # Apply hardcoded rules
        if sentence_count < self.MINIMUM_SENTENCES:
            return {
                "status": "FAIL",
                "sentence_count": sentence_count,
                "required": self.MINIMUM_SENTENCES,
                "action": "EXPAND",
                "blocking": True
            }

        elif sentence_count > self.MAXIMUM_SENTENCES:
            return {
                "status": "CONDENSED",
                "sentence_count": sentence_count,
                "maximum": self.MAXIMUM_SENTENCES,
                "action": "TRUNCATE_TO_8",
                "blocking": False
            }

        else:
            return {
                "status": "PASS",
                "sentence_count": sentence_count,
                "blocking": False
            }

    def validate_presentation(self, slides: list) -> dict:
        """Validate all content slides in a presentation."""

        results = []
        blocking_failures = []

        for i, slide in enumerate(slides):
            result = self.validate_slide(slide)
            result["slide_index"] = i + 1
            results.append(result)

            if result.get("blocking"):
                blocking_failures.append(i + 1)

        passed = sum(1 for r in results if r["status"] == "PASS")
        failed = sum(1 for r in results if r["status"] == "FAIL")

        return {
            "overall_status": "PASSED" if not blocking_failures else "FAILED",
            "slides_checked": len(results),
            "slides_passed": passed,
            "slides_failed": failed,
            "blocking_failures": blocking_failures,
            "details": results
        }

    def _count_sentences(self, slide: dict) -> int:
        """Count sentences in slide body."""

        if "body_sentences" in slide:
            return len(slide["body_sentences"])

        body = slide.get("body_text", "") or slide.get("body", "")
        if isinstance(body, list):
            body = " ".join(body)

        import re
        sentences = re.split(r'(?<=[.!?])\s+', body)
        return len([s for s in sentences if len(s.strip()) > 10])
```

---

## Error Messages

### Critical Failure
```
CONTENT DENSITY VALIDATION FAILED

Slide {index} has only {count} sentence(s).
MINIMUM REQUIRED: 4 sentences

This slide must be expanded before proceeding.
Returning to content_populator for expansion.

Hints for expansion:
- Add contextual background
- Include a specific example
- Explain significance or connection
- Integrate vocabulary terms
```

### Warning (Auto-Fixed)
```
CONTENT DENSITY WARNING

Slide {index} has {count} sentences (maximum: 8).
Auto-condensing to 8 sentences.

Removed sentences {9-count} to meet maximum.
Review condensed content for completeness.
```

---

**Agent Version:** 1.0
**Last Updated:** 2026-01-09
**Pipeline:** Theater Education
**Classification:** HARDCODED VALIDATOR - CANNOT BE MODIFIED
