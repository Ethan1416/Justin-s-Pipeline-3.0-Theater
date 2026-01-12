"""
Run Document Conversion
=======================

Script to convert all markdown files in production folder to Word documents.
"""

import sys
from pathlib import Path

# Add project to path
sys.path.insert(0, str(Path(__file__).parent))

from agents import ProductionDocGeneratorAgent, FileScannerAgent

def main():
    production_path = Path(__file__).parent / "production"

    print("=" * 60)
    print("DOCUMENT CONVERSION: Markdown to Word")
    print("=" * 60)
    print()

    # First, scan for files
    print("Step 1: Scanning for markdown files...")
    scanner = FileScannerAgent()
    scan_result = scanner.execute({"production_path": str(production_path)})

    if scan_result.output.get("success"):
        print(f"  Found {scan_result.output['total_markdown_files']} markdown files")
        print(f"  Already converted: {scan_result.output['already_converted']}")
        print(f"  Need conversion: {scan_result.output['needs_conversion']}")
        print()

        # List files
        print("Files found:")
        for f in scan_result.output.get("files", []):
            status = "[EXISTS]" if f["word_exists"] else "[PENDING]"
            print(f"  {status} {f['relative_path']}")
        print()
    else:
        print(f"  Error: {scan_result.output.get('error')}")
        return 1

    # Run conversion
    print("Step 2: Converting files...")
    converter = ProductionDocGeneratorAgent()
    convert_result = converter.execute({"production_path": str(production_path)})

    if convert_result.output.get("success"):
        print(f"  Successfully converted {convert_result.output['successful']} files")
    else:
        print(f"  Converted {convert_result.output.get('successful', 0)} files")
        print(f"  Failed: {convert_result.output.get('failed', 0)} files")

    print()
    print("Conversion details:")
    for conv in convert_result.output.get("conversions", []):
        if conv.get("success"):
            print(f"  [OK] {Path(conv['source']).name} -> {Path(conv['output']).name}")
        else:
            print(f"  [XX] {Path(conv['source']).name}: {conv.get('error', 'Unknown error')}")

    print()
    print("=" * 60)
    print("CONVERSION COMPLETE")
    print("=" * 60)

    return 0 if convert_result.output.get("success") else 1

if __name__ == "__main__":
    sys.exit(main())
