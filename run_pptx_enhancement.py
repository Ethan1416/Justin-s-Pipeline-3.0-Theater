"""
PowerPoint Enhancement Script
=============================

Updates PowerPoint slides with fun facts or performance tips
using the SlideContentEnhancerAgent.
"""

import sys
from pathlib import Path

# Add project to path
sys.path.insert(0, str(Path(__file__).parent))

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from agents import SlideContentEnhancerAgent, FunFactGeneratorAgent

def get_slide_text(slide):
    """Extract all text from a slide."""
    text_parts = []
    for shape in slide.shapes:
        if hasattr(shape, "text"):
            text_parts.append(shape.text)
    return " ".join(text_parts)

def get_slide_title(slide):
    """Get the title of a slide."""
    if slide.shapes.title:
        return slide.shapes.title.text
    return ""

def add_fun_fact_box(slide, fact_text, label="Did You Know?"):
    """Add a trivia banner to the bottom of a slide."""
    # Position: bottom of slide
    left = Inches(0.5)
    top = Inches(6.5)
    width = Inches(9)
    height = Inches(0.8)

    # Add shape
    shape = slide.shapes.add_shape(
        1,  # Rectangle
        left, top, width, height
    )

    # Style the shape - theater-themed purple/gold
    shape.fill.solid()
    shape.fill.fore_color.rgb = RGBColor(245, 240, 255)  # Light purple
    shape.line.color.rgb = RGBColor(128, 0, 128)  # Purple
    shape.line.width = Pt(2)

    # Add text
    text_frame = shape.text_frame
    text_frame.word_wrap = True

    # Label paragraph
    p = text_frame.paragraphs[0]
    p.alignment = PP_ALIGN.LEFT
    run = p.add_run()
    run.text = f"🎭 {label}: "
    run.font.bold = True
    run.font.size = Pt(10)
    run.font.color.rgb = RGBColor(75, 0, 130)  # Indigo

    # Fact text
    run2 = p.add_run()
    run2.text = fact_text
    run2.font.size = Pt(10)
    run2.font.color.rgb = RGBColor(51, 51, 51)

    return shape

def add_performance_tip_box(slide, tip_text):
    """Add a performance tip box to the bottom of a slide."""
    left = Inches(0.5)
    top = Inches(6.5)
    width = Inches(9)
    height = Inches(0.8)

    shape = slide.shapes.add_shape(
        1,  # Rectangle
        left, top, width, height
    )

    # Style - light blue for performance tips
    shape.fill.solid()
    shape.fill.fore_color.rgb = RGBColor(230, 243, 255)  # Light blue
    shape.line.color.rgb = RGBColor(0, 102, 204)  # Blue
    shape.line.width = Pt(2)

    text_frame = shape.text_frame
    text_frame.word_wrap = True

    p = text_frame.paragraphs[0]
    p.alignment = PP_ALIGN.LEFT
    run = p.add_run()
    run.text = "🎭 Performance Tip: "
    run.font.bold = True
    run.font.size = Pt(10)
    run.font.color.rgb = RGBColor(0, 51, 102)

    run2 = p.add_run()
    run2.text = tip_text
    run2.font.size = Pt(10)
    run2.font.color.rgb = RGBColor(51, 51, 51)

    return shape

def enhance_presentation(pptx_path, output_path=None):
    """Enhance a PowerPoint presentation with fun facts and tips."""
    print(f"Loading presentation: {pptx_path}")
    prs = Presentation(pptx_path)

    enhancer = SlideContentEnhancerAgent()
    enhancer.reset()

    slides_enhanced = 0
    facts_added = 0
    tips_added = 0

    print(f"Processing {len(prs.slides)} slides...")
    print()

    for i, slide in enumerate(prs.slides, 1):
        title = get_slide_title(slide)
        content = get_slide_text(slide)

        # Skip title slides or very short content
        if len(content) < 20:
            print(f"  Slide {i}: [SKIP] '{title[:30]}...' (too short)")
            continue

        # Get enhancement
        result = enhancer.execute({
            "slide_content": content,
            "slide_title": title,
        })

        if result.output.get("success"):
            enhancement_type = result.output["enhancement_type"]
            enhancement_content = result.output["content"]
            label = result.output["label"]

            if enhancement_type == "fun_fact":
                add_fun_fact_box(slide, enhancement_content, label)
                facts_added += 1
                print(f"  Slide {i}: [{label}] '{title[:30]}...'")
            else:
                # Use the dynamic label for performance trivia
                add_fun_fact_box(slide, enhancement_content, label)
                tips_added += 1
                print(f"  Slide {i}: [{label}] '{title[:30]}...'")

            slides_enhanced += 1
        else:
            print(f"  Slide {i}: [NONE] '{title[:30]}...'")

    # Save
    if output_path is None:
        output_path = pptx_path

    prs.save(output_path)

    print()
    print("=" * 60)
    print("ENHANCEMENT COMPLETE")
    print("=" * 60)
    print(f"Total slides:      {len(prs.slides)}")
    print(f"Slides enhanced:   {slides_enhanced}")
    print(f"Fun facts added:   {facts_added}")
    print(f"Tips added:        {tips_added}")
    print(f"Saved to:          {output_path}")

    return output_path

def main():
    # Default to Romeo and Juliet presentation
    pptx_path = Path(__file__).parent / "production" / "Unit_3_Romeo_and_Juliet" / "Day_01" / "Unit3_Day01_Shakespeare.pptx"

    if not pptx_path.exists():
        print(f"ERROR: PowerPoint not found: {pptx_path}")
        return 1

    print("=" * 60)
    print("POWERPOINT ENHANCEMENT: Adding Fun Facts & Performance Tips")
    print("=" * 60)
    print()

    output_path = enhance_presentation(str(pptx_path))

    return 0

if __name__ == "__main__":
    sys.exit(main())
