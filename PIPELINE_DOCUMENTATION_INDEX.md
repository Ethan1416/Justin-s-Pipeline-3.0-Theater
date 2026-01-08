# Pipeline Documentation Index

This document provides an index of all pipeline documentation and guidelines.

---

## 📋 Core Documentation

### Pipeline Configuration
- **File**: `pipeline_config.json`
- **Purpose**: Central configuration for all pipeline paths, settings, and requirements
- **Key Settings**: Template paths, production folder, font settings, table settings

### Main Pipeline Script
- **File**: `step12_powerpoint_population.py`
- **Purpose**: PowerPoint generation from integrated blueprints
- **Key Functions**: Blueprint parsing, slide creation, visual generation

---

## 📐 Visual Generation Guidelines

### Shape Rotation Guidelines (CRITICAL)
- **File**: `SHAPE_ROTATION_GUIDELINES.md`
- **Purpose**: Prevent line positioning/rotation issues
- **Read Before**: Implementing any rotated shapes or connector lines
- **Key Concept**: PowerPoint rotates shapes around their CENTER, not their corner

### Quick Reference
- **File**: `QUICK_REFERENCE_SHAPE_ROTATION.txt`
- **Purpose**: Quick lookup for rotation positioning rules
- **Use When**: You need a fast reminder about draw_line() vs manual shape creation

### Visual Layout Standards (CRITICAL)
- **File**: `VISUAL_LAYOUT_STANDARDS.md`
- **Purpose**: Font size, box sizing, and spacing requirements for all visuals
- **Read Before**: Implementing any visual type
- **Key Standards**:
  - Minimum 18pt font (VISUAL_MIN_FONT_SIZE constant)
  - Dynamic box sizing based on content
  - Minimum 0.5" spacing between nodes
  - Visual analysis tool usage

### Layout Quick Reference
- **File**: `QUICK_REFERENCE_LAYOUT_STANDARDS.txt`
- **Purpose**: Quick lookup for layout requirements
- **Use When**: You need a fast reminder about font sizes, spacing, or dynamic sizing

---

## 📊 Visual Type Instructions

Each visual type has specific generation instructions:

1. **step12_table_generation.txt** - Table layout and styling
2. **step12_decision_tree_generation.txt** - Decision tree diagrams
3. **step12_flowchart_generation.txt** - Flowchart diagrams
4. **step12_hierarchy_diagram_generation.txt** - Hierarchical tree structures
5. **step12_timeline_generation.txt** - Timeline diagrams
6. **step12_spectrum_generation.txt** - Spectrum/gradient diagrams
7. **step12_key_differentiators_generation.txt** - Comparison tables

**Note**: All visual generators MUST use `draw_line()` and `draw_arrow()` helper functions.

---

## 🔧 Implementation Status

### Current Status (2025-12-25)
- ✅ Template master integration working (no corruption)
- ✅ All 6 visual types implemented
- ✅ Rectangle-based connector lines (avoiding python-pptx bug)
- ✅ Rotation positioning correctly implemented
- ✅ Production-ready pipeline

### Completed Fixes
1. **Template Corruption** - Fixed by using single template master with slide duplication
2. **Connector Corruption** - Fixed by using rotated rectangles instead of add_connector()
3. **Line Positioning** - Fixed by implementing center-based rotation positioning

---

## ⚠️ Common Pitfalls

### DO NOT Do These Things:

1. ❌ **Use python-pptx connectors**
   ```python
   # WRONG - causes file corruption
   slide.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, x1, y1, x2, y2)
   ```

2. ❌ **Position shapes before rotating without accounting for center**
   ```python
   # WRONG - line will not connect points after rotation
   shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, x1, y1, length, width)
   shape.rotation = angle
   ```

3. ❌ **Create multiple template files**
   - Use single `templates/content_master.pptx` with slide duplication

4. ❌ **Modify templates directly in code**
   - Always duplicate template slides, never modify originals

---

## ✅ Best Practices

### When Adding New Visual Types:

1. **Read Shape Rotation Guidelines** first
2. **Use helper functions**:
   - `draw_line(slide, x1, y1, x2, y2, color, width)`
   - `draw_arrow(slide, x1, y1, x2, y2, color, line_width, arrow_size)`
3. **Test thoroughly**:
   - Horizontal lines
   - Vertical lines
   - Diagonal lines (45°, -45°)
   - Multiple angles
4. **Clear body textbox** before adding visual content:
   ```python
   body_shape = find_shape_by_name(slide, 'TextBox 3') or find_shape_by_name(slide, 'TextBox 19')
   if body_shape:
       clear_shape_text(body_shape)
   ```
5. **Add parser function** to extract data from blueprint
6. **Add generator function** to create visual content
7. **Update populate_section()** to call your generator

### Code Organization:

```python
# 1. Parser (Lines 322-612)
def parse_YOURTYPE_spec(spec_text):
    # Extract structured data from VISUAL SPECIFICATION section
    return data_dict

# 2. Generator (Lines 625-1513)
def add_YOURTYPE_content(slide, data):
    # Clear body textbox
    # Use draw_line() and draw_arrow() helpers
    # Create visual content

# 3. Handler in populate_section() (Lines 1957-1975)
elif visual_type == 'yourtype' and slide_data.get('yourtype_data'):
    add_YOURTYPE_content(slide, slide_data['yourtype_data'])
```

---

## 🧪 Testing

### Test Scripts

**Integration Test:**
- **File**: `C:\Users\mcdan\Desktop\TEST_template_master_integration.py`
- **Purpose**: Run full pipeline, generate PowerPoint from blueprint
- **Usage**: `python "C:\Users\mcdan\Desktop\TEST_template_master_integration.py"`

**Visual Analysis Tool:**
- **File**: `C:\Users\mcdan\Desktop\TEST_analyze_pptx_visually.py`
- **Purpose**: Detect overlaps, text overflow, and layout issues programmatically
- **Usage**: `python "C:\Users\mcdan\Desktop\TEST_analyze_pptx_visually.py"`
- **Reports**:
  - Box positions and dimensions
  - Content-to-content overlaps (CRITICAL to fix)
  - Text overflow warnings
  - ASCII layout map showing spacing
- **See**: VISUAL_LAYOUT_STANDARDS.md for usage details

### Test File Locations:
- Test blueprint: `TEST_Pipeline_Integration_2025-12-25\integrated\`
- Test output: `TEST_Pipeline_Integration_2025-12-25\powerpoints\`

### Verification Checklist:
- ☐ File opens without corruption (no "needs repair" prompt)
- ☐ All slides present with correct templates
- ☐ Content slides have NCLEX tip area
- ☐ Visual slides do NOT have NCLEX tip area
- ☐ Visual content generated correctly (not placeholder "text")
- ☐ No content-to-content overlaps (verified by analysis tool)
- ☐ No text overflow warnings (verified by analysis tool)
- ☐ All fonts 18pt or larger (VISUAL_MIN_FONT_SIZE)
- ☐ Minimum 0.5" spacing between nodes
- ☐ Lines connect node centers properly
- ☐ No intersecting or misaligned lines
- ☐ Presenter notes preserved
- ☐ All text readable and properly positioned

---

## 🚀 Production Deployment

### Before Running on Production Data:

1. Verify `pipeline_config.json` paths are correct
2. Ensure template master file exists and is uncorrupted
3. Test with sample blueprint first
4. Verify output in test folder before overwriting production files
5. Back up existing production files

### Production Folder Structure:
```
Production_Folder/
├── integrated/          # Step 10 integrated blueprints
├── powerpoints/         # Generated PowerPoint files
│   └── [section_name]/  # One folder per section
├── blueprints/          # Step 8 blueprints
├── visual_specs/        # Visual specifications
└── qa_reports/          # Quality assurance reports
```

---

## 📝 Maintenance

### When Issues Arise:

1. **Check status files** in Desktop folder:
   - `ALL_VISUAL_TYPES_COMPLETE.txt`
   - `TEMPLATE_MASTER_STATUS_UPDATE.txt`
   - `CONNECTOR_CORRUPTION_FIX_COMPLETE.txt`
   - `RECTANGLE_LINES_IMPLEMENTATION_COMPLETE.txt`

2. **Review guidelines**:
   - `SHAPE_ROTATION_GUIDELINES.md`
   - `QUICK_REFERENCE_SHAPE_ROTATION.txt`

3. **Test in isolation**:
   - Use test scripts to isolate issues
   - Test visual types individually
   - Check template duplication separately

4. **Add debug markers**:
   ```python
   # Temporary debug: Add red circle at line endpoint
   marker = slide.shapes.add_shape(MSO_SHAPE.OVAL, x, y, Inches(0.1), Inches(0.1))
   marker.fill.solid()
   marker.fill.fore_color.rgb = RGBColor(255, 0, 0)
   ```

---

## 🔗 Related Files

### Helper Functions (step12_powerpoint_population.py):
- **Lines 104-118**: Shape finding and text clearing
- **Lines 157-293**: Shape drawing helpers (draw_line, draw_arrow)
- **Lines 322-612**: Visual specification parsers
- **Lines 625-1513**: Visual content generators
- **Lines 1957-1975**: populate_section() with visual handlers

### Configuration:
- **pipeline_config.json**: All paths and settings
- **templates/content_master.pptx**: Single template file with 2 slide layouts

---

## 📚 Additional Resources

### Python-pptx Documentation:
- Main docs: https://python-pptx.readthedocs.io/
- Shape rotation: https://python-pptx.readthedocs.io/en/latest/api/shapes.html
- Positioning: https://python-pptx.readthedocs.io/en/latest/user/understanding-shapes.html

### PowerPoint Coordinate System:
- Origin (0,0) at top-left
- X increases rightward
- Y increases downward
- Standard slide: 13.33" × 7.5"
- Units: Inches(), Pt(), Emu()

---

## 📞 Support

If you encounter issues not covered in this documentation:

1. Check existing status files in Desktop folder
2. Review SHAPE_ROTATION_GUIDELINES.md
3. Test with TEST_template_master_integration.py
4. Add debug output/markers to isolate issue
5. Document new issues and solutions

---

## Version History

- **2025-12-25 (v2.1)**: Added layout standards and visual analysis tool
  - Created VISUAL_LAYOUT_STANDARDS.md (font sizes, spacing, dynamic sizing)
  - Implemented VISUAL_MIN_FONT_SIZE constant (18pt minimum)
  - Created TEST_analyze_pptx_visually.py for automated layout verification
  - Fixed KEY_DIFFERENTIATORS dynamic height calculation (0.7" per feature)
  - Fixed HIERARCHY node spacing for 2-sibling layouts (1.25" extension)
  - Updated CHECKLIST_ADDING_NEW_VISUAL_TYPES.md with new requirements

- **2025-12-25 (v2.0)**: Initial documentation index created
  - All visual types working with rectangle-based lines
  - Shape rotation positioning corrected
  - Production-ready pipeline

---

**Last Updated**: 2025-12-25
**Pipeline Version**: v2.1 (Layout Standards Integrated)
