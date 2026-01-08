# PowerPoint Shape Rotation Guidelines

## ⚠️ CRITICAL: Understanding PowerPoint Rotation Behavior

When working with python-pptx and rotating shapes, **rotation happens around the shape's CENTER, not its top-left corner**.

This is the #1 cause of positioning issues when drawing lines, arrows, and rotated shapes.

---

## The Problem

### ❌ INCORRECT Approach (will cause misaligned lines):

```python
# BAD: Positioning at start point, then rotating
line = slide.shapes.add_shape(
    MSO_SHAPE.RECTANGLE,
    x1, y1,  # Top-left corner at start point
    length, thickness
)
line.rotation = angle  # Rotates around CENTER, not (x1, y1)!
# Result: Line does NOT connect start to end points
```

**What happens:**
1. Rectangle created with top-left at (x1, y1)
2. Rectangle's center is at (x1 + length/2, y1 + thickness/2)
3. Rotation happens around that center
4. After rotation, the line no longer starts at (x1, y1)
5. Lines appear misaligned and intersecting

---

## The Solution

### ✅ CORRECT Approach:

```python
# GOOD: Calculate where center should be, position accordingly
# 1. Calculate midpoint between start and end
mid_x = (x1 + x2) / 2
mid_y = (y1 + y2) / 2

# 2. Calculate top-left position so CENTER is at midpoint
left = mid_x - length / 2
top = mid_y - thickness / 2

# 3. Create shape with calculated position
line = slide.shapes.add_shape(
    MSO_SHAPE.RECTANGLE,
    left, top,  # Positioned so center is at midpoint
    length, thickness
)

# 4. Rotate around center (which is now at the midpoint)
line.rotation = angle
# Result: Line correctly connects start to end points
```

---

## Step-by-Step Positioning Math

### For a Line from (x1, y1) to (x2, y2):

1. **Calculate line properties:**
   ```python
   dx = x2 - x1
   dy = y2 - y1
   length = math.sqrt(dx**2 + dy**2)
   angle = math.atan2(dy, dx)  # in radians
   ```

2. **Calculate desired center position:**
   ```python
   center_x = (x1 + x2) / 2
   center_y = (y1 + y2) / 2
   ```

3. **Calculate top-left position:**
   ```python
   # For a horizontal rectangle (before rotation):
   # center_x = left + width/2  →  left = center_x - width/2
   # center_y = top + height/2  →  top = center_y - height/2

   left = center_x - length / 2
   top = center_y - thickness / 2
   ```

4. **Create and rotate:**
   ```python
   shape = slide.shapes.add_shape(
       MSO_SHAPE.RECTANGLE,
       Emu(int(left)), Emu(int(top)),
       Emu(int(length)), Emu(thickness)
   )
   shape.rotation = math.degrees(angle)  # Convert to degrees
   ```

---

## Code Examples

### Example 1: Drawing a Line

```python
def draw_line(slide, x1, y1, x2, y2, color, width=Pt(2)):
    """Draw a line from (x1,y1) to (x2,y2) using a rotated rectangle."""
    import math

    # Convert to EMU
    x1_emu = x1.emu if hasattr(x1, 'emu') else Emu(x1)
    y1_emu = y1.emu if hasattr(y1, 'emu') else Emu(y1)
    x2_emu = x2.emu if hasattr(x2, 'emu') else Emu(x2)
    y2_emu = y2.emu if hasattr(y2, 'emu') else Emu(y2)
    width_emu = width.emu if hasattr(width, 'emu') else Emu(width)

    # Calculate line properties
    dx = x2_emu - x1_emu
    dy = y2_emu - y1_emu
    length = math.sqrt(dx**2 + dy**2)
    angle = math.atan2(dy, dx)

    # Calculate midpoint (desired center)
    mid_x = (x1_emu + x2_emu) / 2
    mid_y = (y1_emu + y2_emu) / 2

    # Calculate top-left so center is at midpoint
    left = mid_x - length / 2
    top = mid_y - width_emu / 2

    # Create rectangle
    line = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE,
        Emu(int(left)), Emu(int(top)),
        Emu(int(length)), Emu(width_emu)
    )

    # Style
    line.fill.solid()
    line.fill.fore_color.rgb = color
    line.line.fill.background()

    # Rotate around center
    line.rotation = math.degrees(angle)

    return line
```

### Example 2: Drawing an Arrow

```python
def draw_arrow(slide, x1, y1, x2, y2, color, line_width=Pt(2), arrow_size=Inches(0.15)):
    """Draw an arrow with a triangular arrowhead."""
    import math

    # Convert to EMU
    x1_emu = x1.emu if hasattr(x1, 'emu') else Emu(x1)
    y1_emu = y1.emu if hasattr(y1, 'emu') else Emu(y1)
    x2_emu = x2.emu if hasattr(x2, 'emu') else Emu(x2)
    y2_emu = y2.emu if hasattr(y2, 'emu') else Emu(y2)
    arrow_size_emu = arrow_size.emu if hasattr(arrow_size, 'emu') else Emu(arrow_size)

    # Calculate angle
    dx = x2_emu - x1_emu
    dy = y2_emu - y1_emu
    total_length = math.sqrt(dx**2 + dy**2)
    angle = math.atan2(dy, dx)

    # Shorten line for arrowhead
    line_length = total_length - (arrow_size_emu * 0.6)
    line_end_x = x1_emu + line_length * math.cos(angle)
    line_end_y = y1_emu + line_length * math.sin(angle)

    # Draw line using corrected positioning
    line = draw_line(slide,
                    Emu(x1_emu), Emu(y1_emu),
                    Emu(int(line_end_x)), Emu(int(line_end_y)),
                    color, line_width)

    # Position arrowhead
    # Calculate where center should be so tip lands at (x2, y2) after rotation
    arrow_center_offset = arrow_size_emu / 3
    arrow_center_x = x2_emu - arrow_center_offset * math.cos(angle)
    arrow_center_y = y2_emu - arrow_center_offset * math.sin(angle)

    # Calculate top-left so center is at calculated position
    arrow_left = arrow_center_x - arrow_size_emu / 2
    arrow_top = arrow_center_y - arrow_size_emu / 2

    # Create arrowhead
    arrowhead = slide.shapes.add_shape(
        MSO_SHAPE.ISOSCELES_TRIANGLE,
        Emu(int(arrow_left)), Emu(int(arrow_top)),
        Emu(arrow_size_emu), Emu(arrow_size_emu)
    )

    # Style
    arrowhead.fill.solid()
    arrowhead.fill.fore_color.rgb = color
    arrowhead.line.fill.background()

    # Rotate (triangle points up by default, add 90° for direction)
    arrowhead.rotation = math.degrees(angle) + 90

    return line, arrowhead
```

---

## Common Mistakes and How to Avoid Them

### Mistake 1: Using Connector Objects

```python
# ❌ CAUSES FILE CORRUPTION
line = slide.shapes.add_connector(
    MSO_CONNECTOR.STRAIGHT,
    x1, y1, x2, y2
)
```

**Solution:** Use rotated rectangles instead (see examples above)

---

### Mistake 2: Forgetting Center-Based Rotation

```python
# ❌ Lines won't connect properly
line = slide.shapes.add_shape(
    MSO_SHAPE.RECTANGLE,
    x1, y1,  # Wrong: assumes rotation around top-left
    length, thickness
)
line.rotation = angle
```

**Solution:** Calculate midpoint, position so center is at midpoint

---

### Mistake 3: Wrong Arrowhead Rotation Offset

```python
# ❌ Different shapes have different default orientations
arrowhead.rotation = math.degrees(angle)  # Wrong for triangles
```

**Solution:**
- Isosceles triangle points UP by default
- Add 90° to rotation: `math.degrees(angle) + 90`
- Test with horizontal/vertical arrows first

---

## Testing Checklist

When implementing rotated shapes, always test:

1. **Horizontal line** (left to right): Should be perfectly horizontal
2. **Vertical line** (top to bottom): Should be perfectly vertical
3. **Diagonal line** (45° angle): Should connect corners exactly
4. **Multiple angles**: Test 0°, 45°, 90°, 135°, 180°, -45°
5. **Different lengths**: Short lines and long lines
6. **Arrow direction**: Arrowhead should point toward end point

---

## Visual Debugging Tips

If lines are misaligned:

1. **Add temporary markers** at start/end points:
   ```python
   # Debug: Add small circles at line endpoints
   marker = slide.shapes.add_shape(MSO_SHAPE.OVAL, x1, y1, Inches(0.1), Inches(0.1))
   marker.fill.solid()
   marker.fill.fore_color.rgb = RGBColor(255, 0, 0)  # Red
   ```

2. **Check without rotation** first:
   ```python
   # Temporarily comment out rotation
   # line.rotation = angle
   # Are endpoints correct when horizontal?
   ```

3. **Verify midpoint calculation**:
   ```python
   # Add marker at calculated midpoint
   mid_marker = slide.shapes.add_shape(MSO_SHAPE.OVAL,
                                      Emu(mid_x), Emu(mid_y),
                                      Inches(0.15), Inches(0.15))
   ```

---

## Reference: PowerPoint Coordinate System

```
(0, 0) ----------------------> X (increases right)
  |
  |    Slide Area
  |    (13.33" × 7.5")
  |
  v
  Y (increases down)
```

- Origin (0,0) is top-left corner
- Standard slide size: 13.33" × 7.5"
- Units: Can use Inches(), Pt(), or Emu()
- 1 inch = 914,400 EMU (English Metric Units)

---

## Best Practices Summary

1. ✅ **Always use rotated rectangles** for lines (never python-pptx connectors)
2. ✅ **Calculate midpoint** between start/end for rotation center
3. ✅ **Position shape** so its center is at the desired point
4. ✅ **Then rotate** - rotation happens around center
5. ✅ **Test thoroughly** with horizontal, vertical, and diagonal lines
6. ✅ **Add comments** explaining the positioning math
7. ✅ **Use helper functions** (draw_line, draw_arrow) instead of inline code

---

## Integration with Pipeline

The corrected helper functions are located in:
```
step12_powerpoint_population.py
Lines 157-293: draw_line() and draw_arrow() functions
```

**All future visual generators MUST use these helper functions.**

Never create lines/arrows directly - always use:
- `draw_line(slide, x1, y1, x2, y2, color, width)`
- `draw_arrow(slide, x1, y1, x2, y2, color, line_width, arrow_size)`

---

## Additional Resources

- **python-pptx docs**: https://python-pptx.readthedocs.io/
- **Shape rotation property**: https://python-pptx.readthedocs.io/en/latest/api/shapes.html#pptx.shapes.base.BaseShape.rotation
- **EMU conversion**: `1 inch = 914400 EMU`, `Pt(12) = 152400 EMU`

---

## Version History

- **2025-12-25**: Initial guidelines created after fixing line intersection bug
- Issue: Lines were positioned at top-left, causing misalignment after rotation
- Solution: Position rectangles so center is at midpoint, then rotate

---

## Questions?

If you encounter rotation/positioning issues:

1. Review this document
2. Check if you're using `draw_line()` or `draw_arrow()` helpers
3. Verify you're not positioning shapes at corners before rotating
4. Test with simple horizontal/vertical cases first
5. Add debug markers to visualize calculated positions

**Remember: Rotation in PowerPoint ALWAYS happens around the shape's CENTER.**
