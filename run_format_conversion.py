"""
Run Format Conversion
=====================

Script to convert all markdown files in production folder to HTML and PDF,
with answer keys extracted to separate folder.
"""

import sys
from pathlib import Path

# Add project to path
sys.path.insert(0, str(Path(__file__).parent))

from agents import ProductionFormatterAgent

def main():
    production_path = Path(__file__).parent / "production"

    print("=" * 70)
    print("FORMAT CONVERSION: Markdown to HTML/PDF with Answer Keys")
    print("=" * 70)
    print()

    # Run formatter
    formatter = ProductionFormatterAgent()

    print("Processing files...")
    print()

    result = formatter.execute({"production_path": str(production_path)})

    # Print results
    print(f"Total files processed: {result.output.get('total_files', 0)}")
    print(f"HTML files generated:  {result.output.get('html_generated', 0)}")
    print(f"PDF files generated:   {result.output.get('pdf_generated', 0)}")
    print(f"Answer keys generated: {result.output.get('answer_keys_generated', 0)}")
    print()

    # Print details
    print("File Details:")
    print("-" * 70)
    for file_result in result.output.get("files_processed", []):
        status_icons = []
        if file_result.get("html_created"):
            status_icons.append("HTML")
        if file_result.get("pdf_created"):
            status_icons.append("PDF")
        if file_result.get("answer_key_created"):
            status_icons.append("AK")

        status = " + ".join(status_icons) if status_icons else "SKIP"
        print(f"  [{status:15}] {file_result.get('file', 'unknown')}")

        if file_result.get("error"):
            print(f"                    ERROR: {file_result['error']}")

    # Print errors if any
    errors = result.output.get("errors", [])
    if errors:
        print()
        print("ERRORS:")
        print("-" * 70)
        for error in errors:
            print(f"  - {error}")

    print()
    print("=" * 70)
    print("CONVERSION COMPLETE")
    print("=" * 70)

    # List generated files
    print()
    print("Generated Files:")
    print("-" * 70)

    for ext in [".html", ".pdf"]:
        files = list(production_path.rglob(f"*{ext}"))
        if files:
            print(f"\n{ext.upper()} files ({len(files)}):")
            for f in sorted(files):
                print(f"  {f.relative_to(production_path)}")

    # List answer keys
    ak_folders = list(production_path.rglob("answer_keys"))
    if ak_folders:
        print("\nAnswer Keys:")
        for ak_folder in ak_folders:
            for ak_file in ak_folder.glob("*.pdf"):
                print(f"  {ak_file.relative_to(production_path)}")

    return 0 if result.output.get("success") else 1

if __name__ == "__main__":
    sys.exit(main())
