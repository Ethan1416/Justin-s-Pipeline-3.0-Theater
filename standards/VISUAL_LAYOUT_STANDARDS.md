# Visual Layout Standards

This document defines mandatory standards for all slides in the PowerPoint pipeline, including both content slides and visual aids.

---

## 📄 Content Slide Requirements

### 10-Line Body Limit (MANDATORY)

**Content slides MUST have a maximum of 10 lines in the BODY section.**
(8 content lines + up to 2 paragraph spacing lines)

### Why This Limit Exists

Content slides use a **fixed template layout** with:
- Pre-defined body textbox with fixed height
- Fixed NCLEX tip area position
- Consistent spacing and alignment

The body textbox cannot be dynamically resized without breaking the template design. The 10-line limit ensures text fits properly without overflow.

### What Counts as a Line

- **Counted:** Any non-empty line with text or bullets
- **Not counted:** Blank lines for spacing
- **Example:**
  ```
  • Item 1          ← Line 1
                    ← Not counted (blank)
  • Item 2          ← Line 2
  • Item 3          ← Line 3
  ```

### Validation

The pipeline automatically validates content slides during generation:

```
⚠️  WARNING: Slide 2 exceeds 10-line limit for content slides!
   Title: Neurotransmitter Systems: Core Functions
   Lines: 17 (maximum: 10)
   This may cause text overflow on the PowerPoint slide.
   Please condense the BODY section to 10 lines or fewer.
```

### How to Condense Content

**Techniques:**
1. Combine related sub-bullets into single lines
2. Use semicolons (;) instead of line breaks
3. Use arrows (→) for cause-effect relationships
4. Remove redundant information
5. Prioritize NCLEX-testable content

**Example - BEFORE (17 lines):**
```
• GABA: Primary inhibitory neurotransmitter
  - Reduces neuronal excitability
  - Dysregulation linked to anxiety disorders

• Dopamine: Reward and movement
  - Mesolimbic pathway mediates reward
  - Substantia nigra degeneration causes Parkinson's
```

**Example - AFTER (4 lines):**
```
• GABA: Primary inhibitory neurotransmitter; reduces excitability; dysregulation → anxiety

• Dopamine: Reward/movement; mesolimbic pathway mediates reward; substantia nigra → Parkinson's
```

### Tools for Validation

**Before Integration:**
- Location: ``
- Validation/fix script: `blueprint_line_validator.py`

**During Generation:**
- Automatic validation in `step12_powerpoint_population.py`
- Warnings displayed in console output

---

## 📏 Font Size Requirements

### Minimum Font Size Rule

**ALL visual aids must use a minimum 18-point font size.**

```python
# In step12_powerpoint_population.py (Lines 94-96)
VISUAL_MIN_FONT_SIZE = Pt(18)
```

### Why 18pt Minimum?

- **Readability**: Ensures text is easily readable during presentations
- **Professional appearance**: Maintains consistency across all visuals
- **Accessibility**: Meets accessibility standards for visual presentations
- **Distance viewing**: Readable from back of classroom/conference room

### Implementation

**ALWAYS use `VISUAL_MIN_FONT_SIZE` constant instead of hardcoded values:**

```python
# ✅ CORRECT
p.font.size = VISUAL_MIN_FONT_SIZE

# ❌ WRONG
p.font.size = Pt(14)  # Too small!
p.font.size = Pt(16)  # Too small!
```

### Coverage

This applies to ALL text in visual generators:
- Decision tree nodes
- Flowchart steps
- Hierarchy boxes
- Timeline events
- Spectrum labels
- Key differentiator features
- Table cells
- Any other visual aid text

---

## 📦 Dynamic Box Sizing

### The Problem

Fixed-size boxes cause text overflow when content varies in length.

### The Solution

**Calculate box dimensions dynamically based on content.**

### Example: KEY_DIFFERENTIATORS

```python
# Calculate dynamic height based on number of features
max_features = max(len(c['features']) for c in kd_data['concepts'])

# Base height + height per feature line
# 0.7" per feature accommodates 18pt font + bullet + spacing
features_height = Inches(0.7 + max_features * 0.7)
concept_height = Inches(0.7) + features_height  # Header + features
```

### Sizing Guidelines by Font Size

| Font Size | Height per Line | Width per Character |
|-----------|----------------|---------------------|
| 18pt | 0.7" (with spacing) | ~0.15" average |
| 20pt | 0.75" (with spacing) | ~0.17" average |
| 22pt | 0.8" (with spacing) | ~0.18" average |

### Formula

```
Total Height = Base Height + (Number of Lines × Line Height)

Where:
- Base Height = 0.7" (for title/header area)
- Line Height = 0.7" (for 18pt font with bullet and spacing)
- Number of Lines = count of text lines, bullets, or features
```

### When to Use Dynamic Sizing

✅ Use dynamic sizing when:
- Number of items varies between slides
- Text length is unpredictable
- Content comes from user-generated blueprints
- Lists, features, or bullet points are involved

❌ Don't use dynamic sizing when:
- Fixed layout is required (like timeline with specific dates)
- All boxes must be identical size for visual consistency
- Content length is always the same

---

## 📐 Node Spacing Requirements

### The Problem

Nodes (boxes) positioned too close together cause horizontal overlaps, especially with varying text lengths.

### Minimum Spacing Rules

**Between sibling nodes (same level):**
- Minimum gap: 0.5 inches
- Recommended gap: 0.75 inches

**Between parent and child nodes (different levels):**
- Vertical spacing: 1.0 inch minimum
- Allows room for connector lines

### Implementation: HIERARCHY with 2 Siblings

**Problem:** Two children under one parent overlap if positioned at parent edges.

**Solution:** Extend children beyond parent width significantly.

```python
elif num_siblings == 2:
    # Two children: spread them out significantly to prevent overlap
    # L3 child width is 2.5", need at least 0.5" gap between them
    # Parent is 3.0" wide, so extend 1.25" on each side
    if sibling_idx == 0:
        l3_x = parent_x - Inches(1.25)  # Left child: extends left significantly
    else:
        l3_x = parent_x + l2_width - l3_width + Inches(1.25)  # Right child: extends right
```

**Result:**
- Left child extends 1.25" to the left of parent
- Right child extends 1.25" to the right of parent
- Total span = parent width (3.0") + extensions (2.5") = 5.5"
- With 2.5" child width each: 5.5" - 2.5" - 2.5" = 0.5" gap ✅

### Calculating Required Spacing

```
Required Span = (Number of Siblings × Box Width) + ((Number of Siblings - 1) × Min Gap)

Example with 2 siblings:
- Box Width = 2.5"
- Min Gap = 0.5"
- Required Span = (2 × 2.5") + (1 × 0.5") = 5.5"

If Parent Width = 3.0":
Extension Needed = (5.5" - 3.0") / 2 = 1.25" on each side
```

### Testing for Overlaps

After implementing spacing, verify with the analysis tool:

```bash
python "C:\Users\mcdan\Desktop\TEST_analyze_pptx_visually.py"
```

Look for:
- `[OK] No overlaps detected` (content-to-content)
- Positive horizontal gaps between boxes
- Boxes shown separately in ASCII layout map

---

## 🔍 Visual Analysis Tool

### Purpose

Programmatically detect layout issues without opening PowerPoint:
- Node overlaps
- Text overflow
- Positioning errors
- Spacing violations

### Location

```
C:\Users\mcdan\Desktop\TEST_analyze_pptx_visually.py
```

### Usage

```bash
python "C:\Users\mcdan\Desktop\TEST_analyze_pptx_visually.py"
```

### What It Reports

1. **Box Inventory**
   - All shapes on each slide
   - Position, size, and bounds
   - Text content (first 3 lines)

2. **Overlap Detection**
   - Content-to-content overlaps (CRITICAL)
   - Overlap dimensions
   - Horizontal gaps (negative = overlap)

3. **ASCII Layout Map**
   - Visual representation of slide
   - 'X' marks indicate overlaps
   - Numbers show box positions

4. **Text Overflow Analysis**
   - Estimated height needed vs actual
   - Warnings for potential overflows

### Interpreting Results

**CRITICAL Overlaps (must fix):**
```
*** OVERLAP DETECTED:
  Box #15 (Episodic Memory...)
  Box #17 (Semantic Memory...)
  Overlap size: 1.20" x 0.70"
  Horizontal gap: -1.20" (negative = overlap)
```

**Template Overlaps (ignore):**
```
*** OVERLAP DETECTED:
  Box #4 (background rectangle)
  Box #10 (content box)
```
These are normal - background boxes are meant to be behind content.

**How to Use:**
1. Run after any visual generator changes
2. Check specific slides with issues
3. Verify fixes eliminated overlaps
4. Confirm text fits in boxes

---

## ✅ Pre-Implementation Checklist

Before implementing a new visual type, ensure:

- [ ] Read SHAPE_ROTATION_GUIDELINES.md
- [ ] Read this document (VISUAL_LAYOUT_STANDARDS.md)
- [ ] Planned to use `VISUAL_MIN_FONT_SIZE` for all text
- [ ] Calculated dynamic box sizes if content varies
- [ ] Planned node spacing with 0.5" minimum gaps
- [ ] Prepared to test with analysis tool

---

## 📋 Post-Implementation Verification

After implementing a visual generator:

1. **Run integration test:**
   ```bash
   python "C:\Users\mcdan\Desktop\TEST_template_master_integration.py"
   ```

2. **Run visual analysis:**
   ```bash
   python "C:\Users\mcdan\Desktop\TEST_analyze_pptx_visually.py"
   ```

3. **Check analysis results:**
   - [ ] No content-to-content overlaps
   - [ ] All text "Likely fits" (no overflow warnings)
   - [ ] Positive horizontal gaps between nodes
   - [ ] ASCII map shows clean separation

4. **Manual verification in PowerPoint:**
   - [ ] Open generated file
   - [ ] File opens without corruption
   - [ ] All text is readable (not too small)
   - [ ] No text bleeding out of boxes
   - [ ] Nodes don't overlap
   - [ ] Proper spacing between elements

---

## 🐛 Common Issues and Fixes

### Issue 1: Text Bleeding Out of Boxes

**Symptoms:**
- Text cut off at bottom of box
- Overflow warnings in analysis tool

**Cause:**
- Box height too small for content
- Font size increased without adjusting height

**Fix:**
```python
# Increase height per line from 0.5" to 0.7" for 18pt font
features_height = Inches(0.7 + max_features * 0.7)
```

### Issue 2: Nodes Overlapping Horizontally

**Symptoms:**
- Boxes intersecting each other
- Negative horizontal gap in analysis
- 'X' marks in ASCII map

**Cause:**
- Insufficient spacing between siblings
- Not accounting for box width when positioning

**Fix:**
```python
# Increase extension from 0.4" to 1.25" for 2 siblings
if sibling_idx == 0:
    l3_x = parent_x - Inches(1.25)
else:
    l3_x = parent_x + l2_width - l3_width + Inches(1.25)
```

### Issue 3: Font Too Small

**Symptoms:**
- Text hard to read
- Inconsistent with other visuals

**Cause:**
- Hardcoded font size below 18pt

**Fix:**
```python
# Replace hardcoded size with constant
p.font.size = VISUAL_MIN_FONT_SIZE  # Always use this
```

---

## 📐 Standard Dimensions Reference

### Slide Dimensions
- Width: 13.33 inches
- Height: 7.5 inches

### Typical Box Sizes

**Small node (e.g., outcome in decision tree):**
- Width: 2.0 inches
- Height: 0.6 inches

**Medium node (e.g., hierarchy L3):**
- Width: 2.5 inches
- Height: 0.7 inches

**Large node (e.g., hierarchy L2):**
- Width: 3.0 inches
- Height: 0.7 inches

**Panel (e.g., key differentiators):**
- Width: 5.5 inches
- Height: Dynamic (0.7" + features × 0.7")

### Spacing Standards

**Horizontal:**
- Minimum gap between nodes: 0.5 inches
- Typical gap: 0.75 inches
- Wide gap (for clarity): 1.0 inches

**Vertical:**
- Between hierarchy levels: 1.6 inches
- Between timeline events: 1.0 inches
- Between flowchart steps: 0.8 inches

---

## 🔧 Code Examples

### Example 1: Dynamic Height Calculation

```python
def add_my_visual_content(slide, data):
    # Count items to determine height
    num_items = len(data['items'])

    # Calculate dynamic height
    # Base (0.7") + per-item height (0.7" each for 18pt font)
    box_height = Inches(0.7 + num_items * 0.7)

    # Create box with dynamic height
    box = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE,
        Inches(2.0), Inches(1.5),
        Inches(4.0), box_height  # Dynamic height
    )
```

### Example 2: Spacing Siblings

```python
def position_siblings(parent_x, parent_width, child_width, num_siblings):
    """Calculate positions for sibling nodes to prevent overlap."""

    if num_siblings == 1:
        # Center single child under parent
        return [parent_x + (parent_width - child_width) / 2]

    # Calculate required span for all children with gaps
    min_gap = Inches(0.5)
    required_span = (num_siblings * child_width) + ((num_siblings - 1) * min_gap)

    # Calculate extension beyond parent width
    extension = max(0, (required_span - parent_width) / 2)

    # Position children evenly across span
    positions = []
    start_x = parent_x - extension
    for i in range(num_siblings):
        x = start_x + i * (child_width + min_gap)
        positions.append(x)

    return positions
```

### Example 3: Using VISUAL_MIN_FONT_SIZE

```python
def add_text_to_shape(shape, text):
    """Add text to shape with proper formatting."""
    tf = shape.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = text
    p.font.size = VISUAL_MIN_FONT_SIZE  # Always use constant
    p.font.name = "Aptos"
    p.font.bold = False
    p.alignment = PP_ALIGN.CENTER
```

---

## 📚 Related Documentation

- **SHAPE_ROTATION_GUIDELINES.md** - Rotation positioning for lines/arrows
- **CHECKLIST_ADDING_NEW_VISUAL_TYPES.md** - Step-by-step implementation guide
- **PIPELINE_DOCUMENTATION_INDEX.md** - Master documentation index

---

## 🎯 Success Criteria

Your visual implementation meets standards when:

1. ✅ All fonts are 18pt or larger (using `VISUAL_MIN_FONT_SIZE`)
2. ✅ Box heights calculated dynamically based on content
3. ✅ Nodes have minimum 0.5" gaps (no overlaps)
4. ✅ Analysis tool shows "[OK] No overlaps detected"
5. ✅ Analysis tool shows all text "Likely fits"
6. ✅ Manual verification: text fully visible, no bleeding
7. ✅ Manual verification: nodes properly spaced, no intersections

---

**Last Updated:** 2026-01-01
**Pipeline Version:** v3.0 (GitHub-based)
