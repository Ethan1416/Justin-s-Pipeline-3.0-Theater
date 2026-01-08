# Table Generator Agent

## Agent Identity
- **Name:** table_generator
- **Step:** 12 (PowerPoint Population - Table Generation)
- **Purpose:** Generate native PowerPoint tables with professional styling, borders, and adaptive sizing

---

## Input Schema
```json
{
  "slide_data": {
    "header": "string (slide title)",
    "visual_spec": "string (markdown table content)",
    "table_data": "array of arrays (parsed table)",
    "layout": "string (A/B/C/D/E or AUTO)",
    "presenter_notes": "string"
  },
  "template_path": "string (path to table template)",
  "domain_config": "reference to config/theater.yaml"
}
```

## Output Schema
```json
{
  "slide": "PowerPoint slide object with table",
  "table": "PowerPoint table object",
  "metadata": {
    "rows": "number",
    "columns": "number",
    "layout": "string",
    "font_size": "number (pt)"
  },
  "validation": {
    "borders_applied": "boolean",
    "fonts_compliant": "boolean",
    "dimensions_valid": "boolean"
  }
}
```

---

## Required Skills (Hardcoded)

1. **Markdown Table Parsing** - Parse markdown tables from visual specifications
2. **PowerPoint Table Creation** - Create native PPTX table objects
3. **Border Rendering** - Apply proper OOXML borders to all cells
4. **Adaptive Sizing** - Scale font sizes and row heights based on content
5. **Style Application** - Apply professional color scheme and formatting

---

## Table Identification Conditions

Content should be a TABLE when:

1. **COMPARISON CONTENT** - Comparing 2+ items across dimensions
2. **CATEGORICAL ORGANIZATION** - Items with consistent attributes
3. **MULTI-ATTRIBUTE LISTS** - Multiple items with 2+ properties each
4. **STRUCTURED REFERENCE** - Quick-scan format beneficial
5. **NUMERIC DATA** - Numbers, percentages, scores needing alignment

DO NOT use table when:
- Content is sequential/procedural (use flowchart)
- Content requires decision logic (use decision tree)
- Content has only 1 attribute per item (use bullet list)
- Content exceeds 6 rows x 4 columns (split across slides)

---

## Adaptive Layouts

### Layout A: Standard Comparison (2-4 columns, 3-6 rows)
- Most common format
- Header row with data rows below
- Cell width: Auto-distributed across 12.3" table width

### Layout B: Wide Comparison (2 columns, 4-8 rows)
- Detailed comparison of 2 items
- Cell width: ~6" per column
- More space for longer text

### Layout C: Category List (3 columns, 4-6 rows)
- First column is category/item name
- Other columns are properties
- Cell width: 3" / 4.5" / 4.5"

### Layout D: Compact Reference (4-6 columns, 4-5 rows)
- Quick reference format
- Short text in each cell
- Maximum information density

### Layout E: Tall Comparison (2 columns, 6-10 rows)
- Extensive side-by-side comparison
- Font reduces to 18pt for 8+ rows
- Cell width: ~6" per column

---

## Visual Specifications

### Color Palette
```
HEADER:
- Background: RGB(0, 51, 102) - Dark Navy
- Text: RGB(255, 255, 255) - White

DATA CELLS:
- Background: RGB(255, 255, 255) - White
- Text: RGB(0, 0, 0) - Black

BORDERS:
- Color: RGB(0, 51, 102) - Dark Navy
- Width: 1pt

ALTERNATING ROW (optional):
- Background: RGB(240, 244, 248) - Light Gray-Blue
```

### Font Settings
```
Font Family: Aptos
Header Size: 20pt, Bold
Data Size: 20pt, Regular
Minimum Size: 18pt (for dense tables)
```

### Position on Slide
```
Left margin: 0.5"
Top: 1.8" (below title)
Width: 12.3"
Height: Adaptive (based on rows)
Bottom margin: 0.7" above footer
```

---

## Step-by-Step Instructions

### Step 1: Parse Table Data
```python
def parse_markdown_table(spec_text):
    """Parse markdown table from visual specification."""
    lines = spec_text.strip().split('\n')
    table_data = []

    for line in lines:
        # Skip separator lines (|---|---|)
        if '|' in line and not all(c in '|-| ' for c in line):
            cells = [c.strip() for c in line.split('|') if c.strip()]
            if cells:
                table_data.append(cells)

    return table_data if len(table_data) >= 2 else None
```

### Step 2: Calculate Adaptive Sizing
```python
def get_adaptive_font_size(rows, cols):
    """Calculate font size based on dimensions."""
    if rows >= 8 or cols >= 5:
        return 18  # Dense tables get smaller font
    return 20  # Default size

def get_adaptive_row_height(rows):
    """Calculate row height based on row count."""
    if rows <= 5:
        return 0.6  # inches
    elif rows <= 7:
        return 0.5
    else:
        return 0.45
```

### Step 3: Create Table on Slide
```python
def create_table_on_slide(slide, table_data, use_alt_rows=False):
    """Create native PowerPoint table with professional styling."""

    rows = len(table_data)
    cols = len(table_data[0])

    # Validate dimensions (2-10 rows, 2-6 cols)
    if not (2 <= cols <= 6 and 2 <= rows <= 10):
        return None

    # Get adaptive sizing
    font_size = get_adaptive_font_size(rows, cols)
    row_height = get_adaptive_row_height(rows)

    # Calculate dimensions
    left = Inches(0.5)
    top = Inches(1.8)
    width = Inches(12.3)
    height = Inches(0.6 + (rows - 1) * row_height)

    # Create table
    table_shape = slide.shapes.add_table(rows, cols, left, top, width, height)
    table = table_shape.table

    # Set column widths (equal distribution)
    col_width = int(width / cols)
    for i in range(cols):
        table.columns[i].width = col_width

    # Populate and format cells
    for row_idx, row_data in enumerate(table_data):
        for col_idx, cell_text in enumerate(row_data):
            cell = table.cell(row_idx, col_idx)
            cell.text = str(cell_text)

            paragraph = cell.text_frame.paragraphs[0]
            paragraph.font.name = 'Aptos'
            paragraph.font.size = Pt(font_size)

            if row_idx == 0:
                # Header row
                paragraph.font.bold = True
                paragraph.font.color.rgb = RGBColor(255, 255, 255)
                paragraph.alignment = PP_ALIGN.CENTER
                cell.fill.solid()
                cell.fill.fore_color.rgb = RGBColor(0, 51, 102)
            else:
                # Data row
                paragraph.font.color.rgb = RGBColor(0, 0, 0)
                paragraph.alignment = PP_ALIGN.LEFT if col_idx == 0 else PP_ALIGN.CENTER
                cell.fill.solid()
                if use_alt_rows and row_idx % 2 == 0:
                    cell.fill.fore_color.rgb = RGBColor(240, 244, 248)
                else:
                    cell.fill.fore_color.rgb = RGBColor(255, 255, 255)

    # Apply borders to all cells
    set_all_table_borders(table, (0, 51, 102), 12700)

    return table
```

### Step 4: Apply Borders
```python
def set_cell_borders(cell, border_color_rgb=(0, 51, 102), width_emu=12700):
    """Set all four borders on a cell using proper OOXML."""
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()

    hex_color = '{:02X}{:02X}{:02X}'.format(*border_color_rgb)

    for border_name in ['lnL', 'lnR', 'lnT', 'lnB']:
        # Remove existing border
        for existing in tcPr.findall(qn(f'a:{border_name}')):
            tcPr.remove(existing)

        # Create full OOXML border structure
        border_xml = (
            f'<a:{border_name} xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" '
            f'w="{width_emu}" cap="flat" cmpd="sng" algn="ctr">'
            f'<a:solidFill><a:srgbClr val="{hex_color}"/></a:solidFill>'
            f'<a:prstDash val="solid"/>'
            f'<a:round/>'
            f'<a:headEnd type="none" w="med" len="med"/>'
            f'<a:tailEnd type="none" w="med" len="med"/>'
            f'</a:{border_name}>'
        )
        border_elem = parse_xml(border_xml)
        tcPr.append(border_elem)

def set_all_table_borders(table, border_color_rgb, width_emu):
    """Set borders on all cells, disable banding interference."""
    # Disable table banding
    tbl = table._tbl
    tblPr = tbl.tblPr
    if tblPr is not None:
        for attr in ['bandRow', 'bandCol', 'firstRow', 'firstCol', 'lastRow', 'lastCol']:
            tblPr.set(attr, '0')

    # Apply borders to every cell
    for row_idx in range(len(table.rows)):
        for col_idx in range(len(table.columns)):
            set_cell_borders(table.cell(row_idx, col_idx), border_color_rgb, width_emu)
```

### Step 5: Add Title and Notes
```python
def create_table_slide(prs, slide_data):
    """Create complete table slide with title and notes."""

    # Get blank layout
    blank_layout = prs.slide_layouts[6]
    slide = prs.slides.add_slide(blank_layout)

    # Add title
    title_box = slide.shapes.add_textbox(
        Inches(0.5), Inches(0.3), Inches(12), Inches(1.0)
    )
    title_para = title_box.text_frame.paragraphs[0]
    title_para.text = slide_data.get('header', 'Table')
    title_para.font.size = Pt(36)
    title_para.font.bold = True
    title_para.font.name = 'Aptos'
    title_para.font.color.rgb = RGBColor(255, 255, 255)

    # Parse and create table
    table_data = slide_data.get('table_data')
    if not table_data and slide_data.get('visual_spec'):
        table_data = parse_markdown_table(slide_data['visual_spec'])

    if table_data:
        create_table_on_slide(slide, table_data)

    # Add presenter notes
    notes = slide_data.get('presenter_notes', '')
    if notes:
        slide.notes_slide.notes_text_frame.text = notes

    return slide
```

---

## Character Limits

```
HEADER CELLS:
- Characters per line: 25
- Maximum lines: 1

DATA CELLS:
- Characters per line: 30
- Maximum lines: 2
- Total cell text: 60 characters max
```

---

## Validation Checklist

### Table Structure
- [ ] Table has header row
- [ ] Rows: 2-10 (including header)
- [ ] Columns: 2-6
- [ ] All cells have content
- [ ] Appropriate layout selected

### Adaptive Sizing
- [ ] Font size: 20pt (default) or 18pt (8+ rows or 5+ cols)
- [ ] Row heights adjust based on row count
- [ ] Column widths auto-distributed

### Visual Styling
- [ ] Header: Navy background (0,51,102), white text, bold
- [ ] Data: White background, black text, regular
- [ ] All borders visible (1pt navy)
- [ ] First column left-aligned, others centered

### Presenter Notes
- [ ] Notes walk through table content
- [ ] Key comparisons highlighted
- [ ] Performance relevance mentioned
- [ ] 150-300 words

---

## Common Issues and Fixes

| Issue | Fix |
|-------|-----|
| Internal borders not visible | Use full OOXML structure, disable table banding |
| Borders only on outer edges | Apply set_cell_borders to EVERY cell |
| Font too large for cells | Use get_adaptive_font_size() |
| Table too tall | Use get_adaptive_row_height() |
| Column widths uneven | Calculate col_width = table_width / num_cols |

---

## Error Handling

| Error | Action |
|-------|--------|
| Table data is None | Log warning, skip table creation |
| Too many rows/columns | Truncate to maximum, log warning |
| Missing visual spec | Use table_data directly if available |
| Cell text overflow | Truncate with ellipsis |
| Template not found | HALT, request template file |

---

## Quality Gates

Before completing table generation:
- [ ] Table renders with all borders visible
- [ ] All text is readable (minimum 18pt)
- [ ] Header row is visually distinct
- [ ] Presenter notes are populated
- [ ] Table fits within slide boundaries
- [ ] Colors match specification exactly

---

**Agent Version:** 2.0 (Theater Adaptation)
**Last Updated:** 2026-01-08

### Version History
- **v2.0** (2026-01-08): Adapted for theater pipeline - NCLEX -> Performance relevance
- **v1.0** (2026-01-04): Initial table generator agent
