# Position Calculator Agent

## Agent Identity
- **Name:** position_calculator
- **Step:** 12 (PowerPoint Population - Position Calculation)
- **Purpose:** Calculate element positions with coordinate calculation, centering, and alignment for PowerPoint shapes

---

## Input Schema
```json
{
  "slide_dimensions": {
    "width": "number (inches, default 13.333)",
    "height": "number (inches, default 7.5)"
  },
  "element": {
    "width": "number (inches)",
    "height": "number (inches)",
    "content_type": "string (shape/textbox/table/image)"
  },
  "positioning": {
    "type": "string (absolute/relative/grid/center/align)",
    "reference": "string (slide/shape/region)",
    "offset": {"x": "number", "y": "number"},
    "anchor": "string (top-left/top-center/top-right/center-left/center/center-right/bottom-left/bottom-center/bottom-right)"
  },
  "constraints": {
    "margin": "number (inches from slide edge)",
    "safe_zone": {"left": "number", "top": "number", "right": "number", "bottom": "number"},
    "snap_to_grid": "boolean",
    "grid_size": "number (inches)"
  }
}
```

## Output Schema
```json
{
  "position": {
    "left": "number (inches)",
    "top": "number (inches)",
    "right": "number (inches, calculated)",
    "bottom": "number (inches, calculated)"
  },
  "position_emu": {
    "left": "number (EMUs)",
    "top": "number (EMUs)",
    "width": "number (EMUs)",
    "height": "number (EMUs)"
  },
  "validation": {
    "within_bounds": "boolean",
    "within_safe_zone": "boolean",
    "grid_aligned": "boolean"
  }
}
```

---

## Required Skills (Hardcoded)

1. **coordinate_calculation** - Calculate x,y positions in inches and EMUs
2. **centering** - Center elements horizontally or vertically
3. **alignment** - Align elements relative to other elements or regions
4. **grid_snapping** - Snap positions to grid increments
5. **bounds_checking** - Ensure positions are within slide boundaries

---

## Step-by-Step Instructions

### Step 1: Coordinate Calculation
```python
from pptx.util import Inches, Emu

# PowerPoint uses EMUs (English Metric Units)
# 914400 EMUs = 1 inch
EMU_PER_INCH = 914400

# Standard slide dimensions (widescreen 16:9)
SLIDE_WIDTH = 13.333  # inches
SLIDE_HEIGHT = 7.5    # inches

def inches_to_emu(inches):
    """Convert inches to EMUs."""
    return int(inches * EMU_PER_INCH)

def emu_to_inches(emu):
    """Convert EMUs to inches."""
    return emu / EMU_PER_INCH

def calculate_absolute_position(left, top, width, height):
    """Calculate position with absolute coordinates."""

    return {
        'left': left,
        'top': top,
        'right': left + width,
        'bottom': top + height,
        'width': width,
        'height': height
    }

def calculate_position_emu(position):
    """Convert position to EMUs for python-pptx."""

    return {
        'left': inches_to_emu(position['left']),
        'top': inches_to_emu(position['top']),
        'width': inches_to_emu(position.get('width', 0)),
        'height': inches_to_emu(position.get('height', 0))
    }

def get_shape_bounds(shape):
    """Get bounds of an existing shape in inches."""

    return {
        'left': emu_to_inches(shape.left),
        'top': emu_to_inches(shape.top),
        'right': emu_to_inches(shape.left + shape.width),
        'bottom': emu_to_inches(shape.top + shape.height),
        'width': emu_to_inches(shape.width),
        'height': emu_to_inches(shape.height)
    }
```

### Step 2: Centering
```python
def center_horizontally(element_width, container_width=SLIDE_WIDTH):
    """Calculate left position to center element horizontally."""

    left = (container_width - element_width) / 2
    return max(0, left)

def center_vertically(element_height, container_height=SLIDE_HEIGHT):
    """Calculate top position to center element vertically."""

    top = (container_height - element_height) / 2
    return max(0, top)

def center_in_container(element_width, element_height,
                        container_left=0, container_top=0,
                        container_width=SLIDE_WIDTH, container_height=SLIDE_HEIGHT):
    """Center element within a container/region."""

    left = container_left + (container_width - element_width) / 2
    top = container_top + (container_height - element_height) / 2

    return {
        'left': max(container_left, left),
        'top': max(container_top, top)
    }

def center_on_slide(element_width, element_height):
    """Center element on entire slide."""

    return {
        'left': center_horizontally(element_width),
        'top': center_vertically(element_height)
    }

def center_in_region(element_width, element_height, region):
    """Center element within a defined region."""

    region_width = region['right'] - region['left']
    region_height = region['bottom'] - region['top']

    return center_in_container(
        element_width, element_height,
        region['left'], region['top'],
        region_width, region_height
    )
```

### Step 3: Alignment
```python
def align_left(element_width, target_left):
    """Align element's left edge with target."""
    return target_left

def align_right(element_width, target_right):
    """Align element's right edge with target."""
    return target_right - element_width

def align_center_horizontal(element_width, target_center_x):
    """Align element's center with target x position."""
    return target_center_x - (element_width / 2)

def align_top(element_height, target_top):
    """Align element's top edge with target."""
    return target_top

def align_bottom(element_height, target_bottom):
    """Align element's bottom edge with target."""
    return target_bottom - element_height

def align_center_vertical(element_height, target_center_y):
    """Align element's center with target y position."""
    return target_center_y - (element_height / 2)

def align_to_shape(element_width, element_height, reference_shape, alignment='center'):
    """Align element to another shape."""

    ref_bounds = get_shape_bounds(reference_shape)
    ref_center_x = ref_bounds['left'] + ref_bounds['width'] / 2
    ref_center_y = ref_bounds['top'] + ref_bounds['height'] / 2

    ALIGNMENTS = {
        'top-left': {
            'left': ref_bounds['left'],
            'top': ref_bounds['top']
        },
        'top-center': {
            'left': align_center_horizontal(element_width, ref_center_x),
            'top': ref_bounds['top']
        },
        'top-right': {
            'left': align_right(element_width, ref_bounds['right']),
            'top': ref_bounds['top']
        },
        'center-left': {
            'left': ref_bounds['left'],
            'top': align_center_vertical(element_height, ref_center_y)
        },
        'center': {
            'left': align_center_horizontal(element_width, ref_center_x),
            'top': align_center_vertical(element_height, ref_center_y)
        },
        'center-right': {
            'left': align_right(element_width, ref_bounds['right']),
            'top': align_center_vertical(element_height, ref_center_y)
        },
        'bottom-left': {
            'left': ref_bounds['left'],
            'top': align_bottom(element_height, ref_bounds['bottom'])
        },
        'bottom-center': {
            'left': align_center_horizontal(element_width, ref_center_x),
            'top': align_bottom(element_height, ref_bounds['bottom'])
        },
        'bottom-right': {
            'left': align_right(element_width, ref_bounds['right']),
            'top': align_bottom(element_height, ref_bounds['bottom'])
        }
    }

    return ALIGNMENTS.get(alignment, ALIGNMENTS['center'])

def distribute_horizontally(elements_info, start_x, end_x):
    """Distribute elements evenly across horizontal space."""

    # elements_info: list of {'width': w, 'height': h}
    total_width = sum(e['width'] for e in elements_info)
    available_space = end_x - start_x - total_width

    if len(elements_info) <= 1:
        gap = 0
    else:
        gap = available_space / (len(elements_info) - 1)

    positions = []
    current_x = start_x

    for element in elements_info:
        positions.append({
            'left': current_x,
            'top': None  # Must be set separately
        })
        current_x += element['width'] + gap

    return positions

def distribute_vertically(elements_info, start_y, end_y):
    """Distribute elements evenly across vertical space."""

    total_height = sum(e['height'] for e in elements_info)
    available_space = end_y - start_y - total_height

    if len(elements_info) <= 1:
        gap = 0
    else:
        gap = available_space / (len(elements_info) - 1)

    positions = []
    current_y = start_y

    for element in elements_info:
        positions.append({
            'left': None,  # Must be set separately
            'top': current_y
        })
        current_y += element['height'] + gap

    return positions
```

### Step 4: Grid Snapping
```python
def snap_to_grid(value, grid_size=0.1):
    """Snap a value to the nearest grid point."""

    return round(value / grid_size) * grid_size

def snap_position_to_grid(position, grid_size=0.1):
    """Snap position to grid."""

    return {
        'left': snap_to_grid(position['left'], grid_size),
        'top': snap_to_grid(position['top'], grid_size)
    }

def calculate_grid_position(row, col, grid_config):
    """Calculate position from grid row/column."""

    cell_width = grid_config.get('cell_width', 2.0)
    cell_height = grid_config.get('cell_height', 1.5)
    start_x = grid_config.get('start_x', 0.5)
    start_y = grid_config.get('start_y', 1.0)
    h_gap = grid_config.get('h_gap', 0.2)
    v_gap = grid_config.get('v_gap', 0.2)

    left = start_x + col * (cell_width + h_gap)
    top = start_y + row * (cell_height + v_gap)

    return {
        'left': left,
        'top': top,
        'width': cell_width,
        'height': cell_height
    }

def create_grid_layout(rows, cols, area, h_gap=0.2, v_gap=0.2):
    """Create a grid layout within an area."""

    area_width = area['right'] - area['left']
    area_height = area['bottom'] - area['top']

    cell_width = (area_width - (cols - 1) * h_gap) / cols
    cell_height = (area_height - (rows - 1) * v_gap) / rows

    grid = []
    for row in range(rows):
        grid_row = []
        for col in range(cols):
            grid_row.append({
                'left': area['left'] + col * (cell_width + h_gap),
                'top': area['top'] + row * (cell_height + v_gap),
                'width': cell_width,
                'height': cell_height
            })
        grid.append(grid_row)

    return grid
```

### Step 5: Bounds Checking
```python
def is_within_bounds(position, width, height,
                     bounds_width=SLIDE_WIDTH, bounds_height=SLIDE_HEIGHT):
    """Check if element is within slide bounds."""

    left = position['left']
    top = position['top']
    right = left + width
    bottom = top + height

    return (
        left >= 0 and
        top >= 0 and
        right <= bounds_width and
        bottom <= bounds_height
    )

def clamp_to_bounds(position, width, height,
                    bounds_width=SLIDE_WIDTH, bounds_height=SLIDE_HEIGHT):
    """Clamp position to keep element within bounds."""

    left = position['left']
    top = position['top']

    # Clamp left
    left = max(0, left)
    left = min(bounds_width - width, left)

    # Clamp top
    top = max(0, top)
    top = min(bounds_height - height, top)

    return {
        'left': left,
        'top': top
    }

def is_within_safe_zone(position, width, height, safe_zone):
    """Check if element is within safe zone."""

    left = position['left']
    top = position['top']
    right = left + width
    bottom = top + height

    return (
        left >= safe_zone['left'] and
        top >= safe_zone['top'] and
        right <= SLIDE_WIDTH - safe_zone['right'] and
        bottom <= SLIDE_HEIGHT - safe_zone['bottom']
    )

def clamp_to_safe_zone(position, width, height, safe_zone):
    """Clamp position to keep element within safe zone."""

    max_left = SLIDE_WIDTH - safe_zone['right'] - width
    max_top = SLIDE_HEIGHT - safe_zone['bottom'] - height

    left = max(safe_zone['left'], position['left'])
    left = min(max_left, left)

    top = max(safe_zone['top'], position['top'])
    top = min(max_top, top)

    return {
        'left': left,
        'top': top
    }

# Default safe zones for NCLEX slides
SAFE_ZONES = {
    'standard': {
        'left': 0.5,
        'top': 0.8,
        'right': 0.5,
        'bottom': 0.8
    },
    'visual': {
        'left': 0.75,
        'top': 1.2,
        'right': 0.75,
        'bottom': 1.0
    },
    'content': {
        'left': 0.78,
        'top': 1.45,
        'right': 0.5,
        'bottom': 1.0
    }
}
```

### Step 6: Complete Position Calculator
```python
def calculate_position(element, positioning, constraints=None,
                       slide_width=SLIDE_WIDTH, slide_height=SLIDE_HEIGHT):
    """Complete position calculation function."""

    element_width = element.get('width', 1)
    element_height = element.get('height', 1)

    position_type = positioning.get('type', 'absolute')

    # Calculate initial position based on type
    if position_type == 'absolute':
        # Direct coordinates
        position = {
            'left': positioning.get('left', 0),
            'top': positioning.get('top', 0)
        }

    elif position_type == 'center':
        # Center on slide or in container
        reference = positioning.get('reference', 'slide')

        if reference == 'slide':
            position = center_on_slide(element_width, element_height)
        elif isinstance(reference, dict):
            # Reference is a region
            position = center_in_region(element_width, element_height, reference)

    elif position_type == 'align':
        # Align to anchor point
        anchor = positioning.get('anchor', 'center')
        reference = positioning.get('reference_shape')

        if reference:
            position = align_to_shape(element_width, element_height, reference, anchor)
        else:
            # Align to slide
            position = calculate_anchor_position(
                element_width, element_height, anchor,
                slide_width, slide_height
            )

    elif position_type == 'grid':
        # Grid-based position
        row = positioning.get('row', 0)
        col = positioning.get('col', 0)
        grid_config = positioning.get('grid_config', {})

        grid_pos = calculate_grid_position(row, col, grid_config)
        position = {
            'left': grid_pos['left'],
            'top': grid_pos['top']
        }

    elif position_type == 'relative':
        # Relative to another shape
        reference_shape = positioning.get('reference_shape')
        offset = positioning.get('offset', {'x': 0, 'y': 0})

        if reference_shape:
            ref_bounds = get_shape_bounds(reference_shape)
            position = {
                'left': ref_bounds['left'] + offset.get('x', 0),
                'top': ref_bounds['top'] + offset.get('y', 0)
            }
        else:
            position = {
                'left': offset.get('x', 0),
                'top': offset.get('y', 0)
            }

    else:
        position = {'left': 0, 'top': 0}

    # Apply offset if specified
    offset = positioning.get('offset', {})
    position['left'] += offset.get('x', 0)
    position['top'] += offset.get('y', 0)

    # Apply constraints
    validation = {
        'within_bounds': True,
        'within_safe_zone': True,
        'grid_aligned': True
    }

    if constraints:
        # Grid snapping
        if constraints.get('snap_to_grid'):
            grid_size = constraints.get('grid_size', 0.1)
            position = snap_position_to_grid(position, grid_size)
        else:
            validation['grid_aligned'] = False

        # Safe zone
        safe_zone = constraints.get('safe_zone')
        if safe_zone:
            if not is_within_safe_zone(position, element_width, element_height, safe_zone):
                position = clamp_to_safe_zone(position, element_width, element_height, safe_zone)
                validation['within_safe_zone'] = False

    # Check bounds
    if not is_within_bounds(position, element_width, element_height, slide_width, slide_height):
        position = clamp_to_bounds(position, element_width, element_height, slide_width, slide_height)
        validation['within_bounds'] = False

    # Calculate full position info
    full_position = calculate_absolute_position(
        position['left'], position['top'],
        element_width, element_height
    )

    return {
        'position': full_position,
        'position_emu': calculate_position_emu(full_position),
        'validation': validation
    }

def calculate_anchor_position(width, height, anchor, slide_width=SLIDE_WIDTH, slide_height=SLIDE_HEIGHT):
    """Calculate position based on anchor point."""

    ANCHORS = {
        'top-left': {'left': 0, 'top': 0},
        'top-center': {'left': center_horizontally(width, slide_width), 'top': 0},
        'top-right': {'left': slide_width - width, 'top': 0},
        'center-left': {'left': 0, 'top': center_vertically(height, slide_height)},
        'center': {'left': center_horizontally(width, slide_width), 'top': center_vertically(height, slide_height)},
        'center-right': {'left': slide_width - width, 'top': center_vertically(height, slide_height)},
        'bottom-left': {'left': 0, 'top': slide_height - height},
        'bottom-center': {'left': center_horizontally(width, slide_width), 'top': slide_height - height},
        'bottom-right': {'left': slide_width - width, 'top': slide_height - height}
    }

    return ANCHORS.get(anchor, ANCHORS['top-left'])
```

---

## Common Position Configurations

### Title Position
```python
TITLE_POSITION = {
    'left': 0.07,
    'top': -0.06,
    'width': 11.42,
    'height': 0.71
}
```

### Body Content Area
```python
BODY_POSITION = {
    'left': 0.78,
    'top': 1.45,
    'width': 11.0,
    'height': 4.5
}
```

### Visual Area (for diagrams)
```python
VISUAL_AREA = {
    'left': 0.75,
    'top': 1.2,
    'right': 12.58,
    'bottom': 6.5,
    'width': 11.83,
    'height': 5.3
}
```

### NCLEX Tip Position
```python
TIP_POSITION = {
    'left': 0.07,
    'top': 6.63,
    'width': 12.0,
    'height': 0.5
}
```

---

## Validation Checklist

### Pre-Calculation
- [ ] Element dimensions are valid (positive numbers)
- [ ] Positioning type is recognized
- [ ] Reference shape exists (if required)
- [ ] Grid config is complete (if grid type)

### Post-Calculation
- [ ] Position is within slide bounds
- [ ] Position is within safe zone (if specified)
- [ ] Position is grid-aligned (if snapping enabled)
- [ ] Element does not overflow slide

---

## Error Handling

| Error | Action |
|-------|--------|
| Negative dimensions | Use absolute value |
| Position out of bounds | Clamp to slide bounds |
| Invalid anchor name | Default to top-left |
| Missing reference shape | Use absolute positioning |
| Invalid grid config | Use default grid settings |
| Overlap with safe zone | Shift to nearest valid position |

---

**Agent Version:** 1.0
**Last Updated:** 2026-01-04
