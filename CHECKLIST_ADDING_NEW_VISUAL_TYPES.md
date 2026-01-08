# Checklist: Adding New Visual Types

Use this checklist when implementing a new visual type for the PowerPoint pipeline.

---

## 📋 Pre-Implementation

### Step 1: Read Documentation
- [ ] Read `SHAPE_ROTATION_GUIDELINES.md` (MANDATORY)
- [ ] Read `VISUAL_LAYOUT_STANDARDS.md` (MANDATORY)
- [ ] Read `QUICK_REFERENCE_SHAPE_ROTATION.txt`
- [ ] Review existing visual generators in `step12_powerpoint_population.py`
- [ ] Understand the blueprint format for your visual type

### Step 2: Plan Visual Layout
- [ ] Sketch the visual on paper or in PowerPoint manually
- [ ] Identify all shapes needed (boxes, lines, text, etc.)
- [ ] Calculate approximate positions and sizes
- [ ] Plan for minimum 0.5" spacing between nodes
- [ ] Determine which shapes need to connect (lines/arrows)
- [ ] Choose appropriate colors (consistent with existing visuals)
- [ ] Plan dynamic sizing if content varies (see VISUAL_LAYOUT_STANDARDS.md)

---

## 🔧 Implementation

### Step 3: Create Parser Function

Location: `step12_powerpoint_population.py` (Lines 322-612 region)

```python
def parse_YOURTYPE_spec(spec_text):
    """
    Parse VISUAL SPECIFICATION section for YOURTYPE.

    Args:
        spec_text: The VISUAL SPECIFICATION text from blueprint

    Returns:
        Dictionary with parsed data, or None if parsing fails
    """
    if not spec_text:
        return None

    # TODO: Extract your visual's data structure
    # Example patterns:
    # - Use regex to find sections
    # - Split by newlines
    # - Parse structured data

    return {
        'field1': value1,
        'field2': value2,
        # etc.
    }
```

**Checklist:**
- [ ] Function handles empty/None input
- [ ] Returns None on parse failure
- [ ] Returns dictionary with all needed data on success
- [ ] Handles edge cases (missing fields, malformed input)
- [ ] Added docstring explaining format

### Step 4: Create Generator Function

Location: `step12_powerpoint_population.py` (Lines 625-1513 region)

```python
def add_YOURTYPE_content(slide, data):
    """
    Add YOURTYPE visual to an existing slide.

    Args:
        slide: PowerPoint slide object
        data: Parsed data from parse_YOURTYPE_spec()
    """
    # 1. Clear body textbox placeholder
    body_shape = find_shape_by_name(slide, 'TextBox 3') or find_shape_by_name(slide, 'TextBox 19')
    if body_shape:
        clear_shape_text(body_shape)

    # 2. Define colors
    color1 = RGBColor(r, g, b)
    # etc.

    # 3. Define dimensions and positions
    box_width = Inches(2.5)
    box_height = Inches(1.0)
    x_pos = Inches(2.0)
    y_pos = Inches(1.5)
    # etc.

    # 4. Create shapes
    box = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE,
        x_pos, y_pos, box_width, box_height
    )
    box.fill.solid()
    box.fill.fore_color.rgb = color1
    # etc.

    # 5. Add text to shapes (ALWAYS use VISUAL_MIN_FONT_SIZE constant)
    tf = box.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "Your text here"
    p.font.size = VISUAL_MIN_FONT_SIZE  # MANDATORY: 18pt minimum
    p.font.name = "Aptos"
    p.font.color.rgb = RGBColor(255, 255, 255)
    p.alignment = PP_ALIGN.CENTER

    # 6. Add connector lines using helpers (CRITICAL)
    # ⚠️ NEVER create lines directly - always use draw_line() or draw_arrow()
    draw_line(slide,
             start_x, start_y,
             end_x, end_y,
             RGBColor(100, 100, 100),
             Pt(2))
```

**Checklist:**
- [ ] Clear body textbox at start
- [ ] Use `draw_line()` for all lines (NOT `add_connector()`)
- [ ] Use `draw_arrow()` for all arrows
- [ ] Use consistent color scheme
- [ ] Use Aptos font (or configured font)
- [ ] Use `VISUAL_MIN_FONT_SIZE` for ALL text (18pt minimum - MANDATORY)
- [ ] Calculate dynamic box sizes if content varies (see VISUAL_LAYOUT_STANDARDS.md)
- [ ] Ensure minimum 0.5" spacing between nodes
- [ ] Add text alignment (usually CENTER)
- [ ] Handle edge cases (empty data, missing fields)
- [ ] Test with different data sizes

### Step 5: Integrate Parser

Location: `step12_powerpoint_population.py` in `parse_slide_content()` function

Find the section around Lines 205-289 and add:

```python
# Initialize data field in slide dictionary (around line 210)
slide = {
    'yourtype_data': None,  # Add this line
    # ... other fields
}

# Add parser call (around line 280)
if slide['visual_type'] == 'yourtype' and slide['visual_spec']:
    slide['yourtype_data'] = parse_YOURTYPE_spec(slide['visual_spec'])
```

**Checklist:**
- [ ] Added data field to slide dictionary
- [ ] Added parser call with correct visual_type string
- [ ] Parser called only when visual_spec exists
- [ ] Tested with sample blueprint

### Step 6: Integrate Generator

Location: `step12_powerpoint_population.py` in `populate_section()` function

Find the section around Lines 1957-1975 and add:

```python
# For yourtype slides - add yourtype visual
elif visual_type == 'yourtype' and slide_data.get('yourtype_data'):
    add_YOURTYPE_content(slide, slide_data['yourtype_data'])
```

**Checklist:**
- [ ] Added handler in correct location (with other visual handlers)
- [ ] Checks both visual_type and data existence
- [ ] Uses correct function name
- [ ] Passes slide and data correctly

---

## 🧪 Testing

### Step 7: Unit Testing

Create a test script:

```python
"""Test YOURTYPE visual generation"""
import sys
sys.path.insert(0, r'repository root')

from pptx import Presentation
from step12_powerpoint_population import parse_YOURTYPE_spec, add_YOURTYPE_content

# Test parser
test_spec = """
YOUR TEST VISUAL SPECIFICATION HERE
"""
parsed = parse_YOURTYPE_spec(test_spec)
print("Parsed data:", parsed)

# Test generator
template_path = r'templates/content_master.pptx'
prs = Presentation(template_path)
test_slide = prs.slides[1]  # Visual template

add_YOURTYPE_content(test_slide, parsed)

# Save test output
prs.save(r'C:\Users\mcdan\Desktop\TEST_yourtype.pptx')
print("Test file saved. Open it to verify visual appearance.")
```

**Checklist:**
- [ ] Parser returns expected data structure
- [ ] Generator creates shapes without errors
- [ ] Test file opens without corruption
- [ ] Visual appears on slide correctly
- [ ] Body textbox is cleared
- [ ] All text is readable
- [ ] Lines connect properly (if applicable)

### Step 8: Integration Testing

Use the full pipeline test:

```bash
python "C:\Users\mcdan\Desktop\TEST_template_master_integration.py"
```

**Checklist:**
- [ ] Pipeline runs without errors
- [ ] Your visual type appears in output
- [ ] No corruption prompt when opening file
- [ ] Visual matches design intent
- [ ] All other visual types still work

### Step 9: Automated Layout Analysis

Run the visual analysis tool to detect overlaps and sizing issues:

```bash
python "C:\Users\mcdan\Desktop\TEST_analyze_pptx_visually.py"
```

The tool will analyze your visual and report:
- Box positions and dimensions
- Overlap detection (content-to-content overlaps are CRITICAL)
- Text overflow warnings
- ASCII layout map showing spacing

**Checklist:**
- [ ] No content-to-content overlaps detected (ignore template overlaps)
- [ ] All text boxes show "[OK] Likely fits" (no overflow warnings)
- [ ] Horizontal gaps between nodes are positive (minimum 0.5")
- [ ] ASCII map shows clean separation (no excessive 'X' marks)
- [ ] Box sizes appropriate for 18pt font content

**If issues are found:**
1. Increase box height for text overflow (add 0.2" per line)
2. Increase node spacing for overlaps (extend by 0.5" increments)
3. Re-run integration test and analysis tool
4. Repeat until all checks pass

### Step 10: Visual Quality Check

Open the generated PowerPoint and verify:

**Basic Checks:**
- [ ] Slide uses correct template (visual, not content)
- [ ] Body textbox is empty/cleared
- [ ] NCLEX tip area is NOT present (visual slides don't have it)
- [ ] Presenter notes are present

**Shape Checks:**
- [ ] All shapes visible and positioned correctly
- [ ] Text is readable (not too small or cut off)
- [ ] Colors match design intent
- [ ] Shapes don't overlap unintentionally

**Line Checks (if applicable):**
- [ ] Lines connect shape centers (not corners)
- [ ] Lines don't intersect incorrectly
- [ ] Lines are the right thickness
- [ ] Arrow heads point in correct direction

**Edge Case Checks:**
- [ ] Works with minimum data (e.g., 2 items instead of 5)
- [ ] Works with maximum data (e.g., many items)
- [ ] Handles long text without overflow
- [ ] Handles special characters in text

---

## 📐 Critical Rules (NEVER VIOLATE)

### 🚫 NEVER Do These:

1. **NEVER use `add_connector()`**
   ```python
   # ❌ WRONG - causes file corruption
   slide.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, x1, y1, x2, y2)
   ```

2. **NEVER position shapes then rotate without accounting for center**
   ```python
   # ❌ WRONG - line won't connect points
   line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, x1, y1, length, width)
   line.rotation = angle
   ```

3. **NEVER forget to clear body textbox**
   ```python
   # ❌ WRONG - "text" placeholder will remain
   # (always call clear_shape_text on body at start)
   ```

### ✅ ALWAYS Do These:

1. **ALWAYS use helper functions for lines/arrows**
   ```python
   # ✅ CORRECT
   draw_line(slide, x1, y1, x2, y2, color, width)
   draw_arrow(slide, x1, y1, x2, y2, color, line_width, arrow_size)
   ```

2. **ALWAYS clear body textbox first**
   ```python
   # ✅ CORRECT
   body_shape = find_shape_by_name(slide, 'TextBox 3') or find_shape_by_name(slide, 'TextBox 19')
   if body_shape:
       clear_shape_text(body_shape)
   ```

3. **ALWAYS use VISUAL_MIN_FONT_SIZE constant**
   ```python
   # ✅ CORRECT
   p.font.size = VISUAL_MIN_FONT_SIZE  # 18pt minimum

   # ❌ WRONG
   p.font.size = Pt(14)  # Too small!
   ```

4. **ALWAYS ensure minimum 0.5" spacing between nodes**
   - Calculate positions to prevent overlaps
   - Use visual analysis tool to verify
   - See VISUAL_LAYOUT_STANDARDS.md for formulas

5. **ALWAYS test rotation with multiple angles** (if using lines)
   - Horizontal (0°)
   - Vertical (90°)
   - Diagonal (45°, -45°, 135°)

---

## 📚 Reference Examples

### Good Examples to Study:

1. **Simple boxes**: `add_key_differentiator_content()` - Side-by-side comparison
2. **Lines only**: `add_hierarchy_content()` - Tree structure with connector lines
3. **Arrows**: `add_flowchart_content()` - Vertical flow with arrows
4. **Complex layout**: `add_decision_tree_content()` - Multi-level tree with colored outcomes

---

## ✅ Final Checklist

Before committing your code:

- [ ] Read SHAPE_ROTATION_GUIDELINES.md
- [ ] Read VISUAL_LAYOUT_STANDARDS.md
- [ ] Created parser function
- [ ] Created generator function
- [ ] Integrated parser into parse_slide_content()
- [ ] Integrated generator into populate_section()
- [ ] Used draw_line() and draw_arrow() helpers (never add_connector)
- [ ] Used VISUAL_MIN_FONT_SIZE for all text (18pt minimum)
- [ ] Implemented dynamic box sizing if content varies
- [ ] Ensured minimum 0.5" spacing between nodes
- [ ] Clear body textbox at start
- [ ] Unit tested parser
- [ ] Unit tested generator
- [ ] Integration tested with full pipeline
- [ ] Ran visual analysis tool (TEST_analyze_pptx_visually.py)
- [ ] No content-to-content overlaps detected
- [ ] No text overflow warnings
- [ ] Visual quality verified in PowerPoint
- [ ] Tested edge cases (min/max data)
- [ ] No file corruption
- [ ] All existing tests still pass
- [ ] Added docstrings to functions
- [ ] Added comments explaining layout logic
- [ ] Documented blueprint format (if new)

---

## 🎯 Success Criteria

Your implementation is complete when:

1. ✅ File opens without corruption
2. ✅ Visual appears correctly on slide
3. ✅ All fonts are 18pt or larger (using VISUAL_MIN_FONT_SIZE)
4. ✅ No content-to-content overlaps (verified by analysis tool)
5. ✅ No text overflow (all text fits in boxes)
6. ✅ Minimum 0.5" spacing between nodes
7. ✅ Lines connect properly (if applicable)
8. ✅ Text is readable and properly positioned
9. ✅ Works with various data sizes (dynamic sizing)
10. ✅ Follows existing code style and patterns
11. ✅ All tests pass (unit, integration, and analysis)
12. ✅ Documentation updated

---

## 📝 Documentation Requirements

After implementation, update:

1. **This checklist**: Add your visual type to examples if it introduces new patterns
2. **PIPELINE_DOCUMENTATION_INDEX.md**: Add reference to your visual type
3. **Blueprint format docs**: Document your VISUAL SPECIFICATION format
4. **Comments in code**: Explain any complex positioning logic

---

## 🆘 Troubleshooting

### Lines don't connect properly
→ Review SHAPE_ROTATION_GUIDELINES.md
→ Verify you're using draw_line() helper
→ Add debug markers at endpoints to verify positions

### File is corrupted
→ Check if you used add_connector() anywhere (remove it)
→ Test with simpler version (fewer shapes)
→ Use TEST_simple_visual.py to isolate issue

### Shapes overlap incorrectly
→ Review your position calculations
→ Add print statements to debug coordinates
→ Test with slide grid overlay in PowerPoint

### Text is cut off
→ Increase shape size or decrease font size
→ Set word_wrap = True on text frame
→ Adjust margins if needed

---

**Remember: Read SHAPE_ROTATION_GUIDELINES.md BEFORE implementing any rotated shapes!**

---

**Last Updated**: 2025-12-25
