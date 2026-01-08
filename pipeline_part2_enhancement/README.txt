================================================================================
PIPELINE PART 2: LECTURE ENHANCEMENT - PYTHON VERSION
Automated Graphic Organizer Generation and Enhancement System
================================================================================

OVERVIEW
--------
This pipeline enhances PowerPoint lectures by:
1. Automatically identifying slides suitable for visual representation
2. Converting text-heavy slides into professional graphic organizers
3. Applying specifications from "repairing the pipeline" folder
4. Using Python only (NO VBA required)

GRAPHIC ORGANIZER TYPES
------------------------
1. TABLE - Comparisons, organized data, mechanism summaries (HIGHEST PRIORITY)
2. KEY_DIFFERENTIATORS - Discrimination between similar concepts
3. FLOWCHART - Sequential processes, mechanisms, protocols
4. DECISION_TREE - Diagnostic decisions, classification systems
5. HIERARCHY - Classifications, taxonomies, structures (3+ levels)
6. TIMELINE - Chronological events, developmental stages
7. SPECTRUM - Continuums, severity scales, gradients

REQUIREMENTS
------------
- Python 3.7+ with python-pptx library
  Install: pip install python-pptx
- Template file: template master.pptx (in this directory)
- Input files: PowerPoint presentations to enhance

================================================================================
INSTALLATION
================================================================================

STEP 1: Install Python Dependencies
------------------------------------
Open Command Prompt or PowerShell and run:

    pip install python-pptx

STEP 2: Verify Template Path
-----------------------------
Ensure template master.pptx is in:
   C:\Users\mcdan\OneDrive\Desktop\pipeline_part2_enhancement\

================================================================================
USAGE - THREE STEP PROCESS
================================================================================

STEP 1: View Example Graphic Organizers (OPTIONAL)
---------------------------------------------------
To see examples of all 7 graphic organizer types:

1. Open:
   C:\Users\mcdan\OneDrive\Desktop\pipeline_part2_enhancement\GRAPHIC_ORGANIZER_EXAMPLES.pptx

2. Review each slide to understand what each organizer looks like

3. To regenerate examples:
   python generate_graphic_organizer_examples.py


STEP 2: Analyze PowerPoint to Identify Candidates
--------------------------------------------------
Run the analysis script to identify which slides should get graphic organizers:

    python analyze_and_identify_slides.py

What this does:
- Analyzes slide content and presenter notes
- Scores each slide for all 7 graphic organizer types
- Applies variety algorithm to prevent repetition
- Enforces 20-40% quota per section
- Generates JSON recommendations file

Output:
- [filename]_graphic_organizer_recommendations.json
  Contains list of slides with recommended visual types

You can edit the JSON file to:
- Change the recommended visual type for a slide
- Remove slides you don't want to enhance
- Adjust the final_type field for any recommendation


STEP 3: Apply Graphic Organizers to Slides
-------------------------------------------
Run the application script to apply graphic organizers:

    python apply_graphic_organizers.py

What this does:
- Reads the recommendations JSON file
- Opens the PowerPoint presentation
- Clears the content area of identified slides
- Applies the appropriate graphic organizer
- Saves enhanced version as [filename]_ENHANCED.pptx

Output:
- [filename]_ENHANCED.pptx
  Enhanced PowerPoint with graphic organizers applied

================================================================================
CUSTOMIZATION
================================================================================

To analyze different PowerPoint files:
1. Edit analyze_and_identify_slides.py
2. Update the 'files' list at the bottom (lines 442-447)
3. Add your PowerPoint paths:
   files = [
       r"C:\path\to\your\presentation.pptx",
   ]
4. Run: python analyze_and_identify_slides.py

To apply to different files:
1. Edit apply_graphic_organizers.py
2. Update the 'files' list at the bottom (lines 815-826)
3. Add tuples of (pptx_path, json_path):
   files = [
       (
           r"C:\path\to\presentation.pptx",
           r"C:\path\to\presentation_graphic_organizer_recommendations.json"
       ),
   ]
4. Run: python apply_graphic_organizers.py

================================================================================
SPECIFICATIONS
================================================================================

All graphic organizers follow specifications from:
  C:\Users\mcdan\OneDrive\Desktop\repairing the pipeline\

Key specifications:
- Minimum font size: 18pt (enforced)
- Content area boundaries: 0.54", 0.72", 12.26" x 6.52"
- Professional color gradients and 3D effects
- Border styling per organizer type
- Dynamic sizing based on content

Refer to visual_specs.txt for detailed specifications.

================================================================================
ANALYSIS ALGORITHM
================================================================================

Condition Testing:
- Each slide is scored against 7 conditions (one per organizer type)
- Scores range from 0-15 based on keyword matches and structure
- Threshold: Minimum score of 6 required to be considered

Variety Algorithm:
- Prevents more than 2 of same type in a row
- Limits each type to max 3 uses per section
- Enforces 20-40% quota per section

Section Detection:
- Automatically detects section boundaries
- Applies quotas per section independently
- Excludes section intro slides from count

================================================================================
OUTPUT STRUCTURE
================================================================================

pipeline_part2_enhancement/
├── template master.pptx                      [Template file]
├── generate_graphic_organizer_examples.py    [Example generator]
├── analyze_and_identify_slides.py            [Slide analyzer]
├── apply_graphic_organizers.py               [Graphic organizer applicator]
├── visual_specs.txt                          [Specifications]
├── presenter_notes_tone_guidelines.txt       [Tone guidelines]
├── README.txt                                [This file]
├── GRAPHIC_ORGANIZER_EXAMPLES.pptx           [Example slides]
│
├── logs/                                     [Future: execution logs]
└── qa_reports/                               [Future: quality reports]

================================================================================
EXAMPLE WORKFLOW
================================================================================

Complete workflow for enhancing a PowerPoint:

1. Place your PowerPoint in a known location

2. Run analysis:
   python analyze_and_identify_slides.py

   Review output to see which slides were identified

3. (Optional) Edit the JSON file to adjust recommendations

4. Apply graphic organizers:
   python apply_graphic_organizers.py

   Open the _ENHANCED.pptx file to review results

5. Make manual adjustments in PowerPoint as needed

================================================================================
QUALITY SPECIFICATIONS
================================================================================

All graphic organizers must meet:
  ✓ Title preserved and visible
  ✓ Font size ≥18pt (minimum)
  ✓ Content within area: 12.26" × 6.52"
  ✓ Professional styling applied
  ✓ No text overflow
  ✓ Black text (except white text on dark backgrounds)

Section Requirements:
  ✓ 20-40% of slides should have graphic organizers
  ✓ Variety enforced (max 2 of same type before switching)
  ✓ Section intro slides excluded from count

================================================================================
TROUBLESHOOTING
================================================================================

ERROR: "No module named 'pptx'"
--------------------------------
Solution: Install python-pptx
    pip install python-pptx

ERROR: "File not found" - Template
-----------------------------------
Solution:
- Check that template master.pptx exists in pipeline_part2_enhancement folder
- Verify path in scripts matches your directory structure

ERROR: "No recommendations to apply"
------------------------------------
Solution:
- Check that analysis script ran successfully
- Verify JSON file was generated
- Lower threshold in analyze_and_identify_slides.py (line 332, change threshold=6 to threshold=4)
- Review slide content - may not match any conditions strongly

ERROR: Graphic organizers look incorrect
-----------------------------------------
Solution:
- Check visual_specs.txt for correct specifications
- Verify template master.pptx hasn't been modified
- Review GRAPHIC_ORGANIZER_EXAMPLES.pptx to see expected output

ERROR: "Index out of range" when applying
------------------------------------------
Solution:
- JSON file may reference slides that don't exist
- Verify PowerPoint file hasn't changed since analysis
- Regenerate JSON by running analysis again

================================================================================
ADVANCED CUSTOMIZATION
================================================================================

Adjust Analysis Threshold:
- Edit analyze_and_identify_slides.py, line 332
- Change threshold=6 to lower (more recommendations) or higher (fewer)

Adjust Quota Requirements:
- Edit analyze_and_identify_slides.py, lines 263-264
- Change min_quota=0.2 (20%) and max_quota=0.4 (40%)

Modify Condition Testing:
- Edit test_*_condition functions in analyze_and_identify_slides.py
- Add/remove keywords, adjust scoring weights

Customize Visual Appearance:
- Edit COLORS dictionary in apply_graphic_organizers.py
- Modify individual applier functions (apply_table_to_slide, etc.)
- Adjust sizing constants in CONTENT_AREA

================================================================================
COMPARISON TO VBA VERSION
================================================================================

PYTHON VERSION ADVANTAGES:
✓ No macro security warnings
✓ Can run on any OS (Windows, Mac, Linux)
✓ Easier to customize and extend
✓ Better error handling and debugging
✓ Generates detailed analysis reports
✓ Can process multiple files in batch

VBA VERSION (DEPRECATED):
✗ Requires macro-enabled PowerPoint
✗ Windows only
✗ Security warnings every time
✗ Harder to debug and maintain
✗ No detailed analysis reports

================================================================================
SCRIPT DESCRIPTIONS
================================================================================

generate_graphic_organizer_examples.py
--------------------------------------
Purpose: Creates example PowerPoint showing all 7 graphic organizer types
Input: template master.pptx
Output: GRAPHIC_ORGANIZER_EXAMPLES.pptx
Runtime: ~10 seconds

analyze_and_identify_slides.py
-------------------------------
Purpose: Analyzes PowerPoint slides to identify graphic organizer candidates
Input: PowerPoint file(s)
Output: [filename]_graphic_organizer_recommendations.json
Runtime: ~5-10 seconds per presentation
Scoring: 7 condition tests per slide, threshold of 6 points minimum

apply_graphic_organizers.py
----------------------------
Purpose: Applies graphic organizers to identified slides
Input: PowerPoint file + recommendations JSON
Output: [filename]_ENHANCED.pptx
Runtime: ~2-5 seconds per slide being enhanced
Processing: Clears content area, generates visual, preserves notes

================================================================================
PERFORMANCE NOTES
================================================================================

Processing Time:
- Example generation: ~10 seconds
- Analysis: ~1 second per slide
- Application: ~2 seconds per enhanced slide
- Complete workflow for 20-slide deck: ~60 seconds

Expected Conversion Rates:
- Typical content: 20-30% of slides converted
- Comparison-heavy content: 30-40%
- Narrative content: 10-20%

Optimization Tips:
- Close PowerPoint before running scripts
- Process files one at a time for best results
- Run on presentations with <100 total slides
- Use SSD for faster file I/O

================================================================================
FILES CREATED BY SCRIPTS
================================================================================

After running the complete workflow, you'll have:

1. GRAPHIC_ORGANIZER_EXAMPLES.pptx
   - Example slides showing all 7 organizer types
   - Use as visual reference

2. [original_name]_analysis.json
   - Full slide-by-slide content extraction
   - Used internally, can be deleted

3. [original_name]_graphic_organizer_recommendations.json
   - List of slides recommended for graphic organizers
   - Editable before applying

4. [original_name]_ENHANCED.pptx
   - Final enhanced PowerPoint
   - Original slides preserved, identified slides enhanced

================================================================================
SUPPORT AND CONTACT
================================================================================

For issues, questions, or feedback:
- Review this README thoroughly
- Check GRAPHIC_ORGANIZER_EXAMPLES.pptx for expected output
- Verify python-pptx is installed correctly
- Ensure template file is accessible

Pipeline Version: 3.0 (Python)
Last Updated: 2026-01-01

================================================================================
CHANGELOG
================================================================================

Version 3.0 (2026-01-01):
- Removed 15 bloat files (historical fix notes, duplicate scripts)
- Tightened content extraction zone (7.3" -> 6.5")
- Increased feature limit (4 -> 10 per concept)
- Increased character limit (40 -> 100 chars)
- Consolidated to 3 core scripts
- Aligned with Part 1 pipeline standards

Version 2.0 (2025-12-27):
- Complete rewrite in Python (removed VBA dependency)
- Added example graphic organizer generator
- Improved analysis algorithm with scoring system
- Added variety algorithm to prevent repetition
- Generates editable JSON recommendations
- Better error handling and reporting
- Cross-platform compatibility

Version 1.0 (Previous):
- VBA-based implementation
- Deprecated due to security and maintenance issues

================================================================================
END OF README
================================================================================
