#!/usr/bin/env python3
"""
Presenter Notes Extraction Script
==================================

Extracts verbatim presenter notes/monologues from every slide in PowerPoint
files and generates Word documents containing the full monologue text.

Uses hardcoded agents for all extraction, formatting, and validation tasks.

Usage:
    python run_notes_extraction.py                           # Process all PPTX in production/
    python run_notes_extraction.py --path /path/to/file.pptx # Process single file
    python run_notes_extraction.py --dir /path/to/folder     # Process directory
    python run_notes_extraction.py --unit 3                  # Process Unit 3 only
"""

import sys
import argparse
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any

# Add project to path
sys.path.insert(0, str(Path(__file__).parent))

from agents import (
    PresenterNotesExtractorAgent,
    MonologueFormatterAgent,
    NotesToWordGeneratorAgent,
    NotesExtractionValidatorAgent,
    PresentationNotesOrchestratorAgent,
)

# Pipeline root
PIPELINE_ROOT = Path(__file__).parent
PRODUCTION_DIR = PIPELINE_ROOT / "production"


class PresenterNotesProcessor:
    """
    Processor for extracting presenter notes from PowerPoint files.

    Uses hardcoded agents for all tasks:
    - PresenterNotesExtractorAgent: Extracts notes from PPTX
    - MonologueFormatterAgent: Formats notes for Word output
    - NotesToWordGeneratorAgent: Generates Word documents
    - NotesExtractionValidatorAgent: Validates extraction quality
    - PresentationNotesOrchestratorAgent: Orchestrates full pipeline
    """

    def __init__(self, verbose: bool = False):
        self.verbose = verbose

        # Initialize hardcoded agents
        self.extractor = PresenterNotesExtractorAgent()
        self.formatter = MonologueFormatterAgent()
        self.generator = NotesToWordGeneratorAgent()
        self.validator = NotesExtractionValidatorAgent()
        self.orchestrator = PresentationNotesOrchestratorAgent()

        # Statistics
        self.stats = {
            "files_processed": 0,
            "files_success": 0,
            "files_failed": 0,
            "total_slides": 0,
            "slides_with_notes": 0,
            "total_word_count": 0,
            "word_docs_generated": 0,
            "validation_warnings": 0,
        }

    def process_single_file(self, pptx_path: Path, output_path: Path = None) -> Dict[str, Any]:
        """Process a single PowerPoint file."""
        if output_path is None:
            output_path = pptx_path.parent / f"{pptx_path.stem}_PresenterNotes.docx"

        print(f"Processing: {pptx_path.name}")

        # Use orchestrator for full pipeline
        result = self.orchestrator.execute({
            "pptx_path": str(pptx_path),
            "output_path": str(output_path),
            "presentation_title": pptx_path.stem.replace("_", " ")
        })

        if result.output.get("success"):
            stats = result.output.get("extraction_stats", {})
            self.stats["files_success"] += 1
            self.stats["total_slides"] += stats.get("total_slides", 0)
            self.stats["slides_with_notes"] += stats.get("slides_with_notes", 0)
            self.stats["total_word_count"] += stats.get("total_word_count", 0)
            self.stats["word_docs_generated"] += 1

            validation = result.output.get("validation", {})
            self.stats["validation_warnings"] += len(validation.get("warnings", []))

            print(f"  [OK] Generated: {output_path.name}")
            print(f"       Slides: {stats.get('total_slides', 0)}, "
                  f"With Notes: {stats.get('slides_with_notes', 0)}, "
                  f"Words: {stats.get('total_word_count', 0)}")

            if validation.get("warnings"):
                for warning in validation["warnings"]:
                    print(f"       WARNING: {warning}")
        else:
            self.stats["files_failed"] += 1
            print(f"  [FAIL] {result.output.get('error', 'Unknown error')}")

        self.stats["files_processed"] += 1
        return result.output

    def process_directory(self, directory: Path, output_dir: Path = None) -> List[Dict[str, Any]]:
        """Process all PowerPoint files in a directory."""
        if output_dir is None:
            output_dir = directory

        pptx_files = sorted(directory.glob("**/*.pptx"))

        if not pptx_files:
            print(f"No PowerPoint files found in: {directory}")
            return []

        print(f"Found {len(pptx_files)} PowerPoint files")
        print()

        results = []
        for pptx_file in pptx_files:
            # Calculate relative output path
            try:
                relative_path = pptx_file.relative_to(directory)
                output_path = output_dir / relative_path.parent / f"{pptx_file.stem}_PresenterNotes.docx"
            except ValueError:
                output_path = output_dir / f"{pptx_file.stem}_PresenterNotes.docx"

            result = self.process_single_file(pptx_file, output_path)
            results.append(result)
            print()

        return results

    def process_unit(self, unit_number: int) -> List[Dict[str, Any]]:
        """Process all PowerPoint files for a specific unit."""
        # Find unit folder
        unit_folders = list(PRODUCTION_DIR.glob(f"Unit_{unit_number}_*"))

        if not unit_folders:
            print(f"Unit {unit_number} folder not found in production/")
            return []

        unit_folder = unit_folders[0]
        print(f"Processing Unit {unit_number}: {unit_folder.name}")
        print()

        return self.process_directory(unit_folder)

    def print_summary(self):
        """Print processing summary."""
        print()
        print("=" * 70)
        print("PRESENTER NOTES EXTRACTION COMPLETE")
        print("=" * 70)
        print(f"Files processed:      {self.stats['files_processed']}")
        print(f"Files successful:     {self.stats['files_success']}")
        print(f"Files failed:         {self.stats['files_failed']}")
        print(f"Word docs generated:  {self.stats['word_docs_generated']}")
        print()
        print(f"Total slides:         {self.stats['total_slides']}")
        print(f"Slides with notes:    {self.stats['slides_with_notes']}")
        print(f"Total word count:     {self.stats['total_word_count']}")
        print(f"Validation warnings:  {self.stats['validation_warnings']}")
        print()

        if self.stats['total_word_count'] > 0:
            speaking_time = round(self.stats['total_word_count'] / 150, 1)
            print(f"Est. speaking time:   {speaking_time} minutes (~150 WPM)")


def main():
    parser = argparse.ArgumentParser(
        description="Extract presenter notes from PowerPoint files to Word documents",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                           Process all PPTX in production/
  %(prog)s --unit 3                  Process Unit 3 (Romeo and Juliet)
  %(prog)s --path file.pptx          Process single file
  %(prog)s --dir /path/to/folder     Process all PPTX in directory
  %(prog)s --output /path/to/output  Specify output directory
        """
    )

    parser.add_argument('--path', type=str, help='Path to single PowerPoint file')
    parser.add_argument('--dir', type=str, help='Directory containing PowerPoint files')
    parser.add_argument('--unit', type=int, choices=[1, 2, 3, 4],
                       help='Process specific unit (1-4)')
    parser.add_argument('--output', type=str, help='Output directory for Word files')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')

    args = parser.parse_args()

    # Initialize processor
    processor = PresenterNotesProcessor(verbose=args.verbose)

    print("=" * 70)
    print("PRESENTER NOTES EXTRACTION")
    print("=" * 70)
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()

    # Determine output directory
    output_dir = Path(args.output) if args.output else None

    # Process based on arguments
    if args.path:
        # Single file
        pptx_path = Path(args.path)
        if not pptx_path.exists():
            print(f"ERROR: File not found: {pptx_path}")
            return 1
        processor.process_single_file(pptx_path, output_dir)

    elif args.dir:
        # Directory
        directory = Path(args.dir)
        if not directory.exists():
            print(f"ERROR: Directory not found: {directory}")
            return 1
        processor.process_directory(directory, output_dir)

    elif args.unit:
        # Specific unit
        processor.process_unit(args.unit)

    else:
        # Default: process all production folders
        print("Processing all PowerPoint files in production/")
        print()
        processor.process_directory(PRODUCTION_DIR, output_dir)

    # Print summary
    processor.print_summary()

    return 0 if processor.stats["files_failed"] == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
