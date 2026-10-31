"""Example script for renaming files using the chroma_tool_py.io.rename module.

This script demonstrates how to remove patterns from filenames in a folder.
Modify the folder_path and pattern variables according to your needs.
"""

from chroma_tool_py.io.rename import remove_pattern_from_filenames, remove_pattern_regex

# === CONFIGURATION ===
# Folder containing the files to rename
import sys
from pathlib import Path

# Usage: python rename_files.py path/to/folder
folder_path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("path/to/folder")

""" # Pattern to remove from filenames
# Example: "TV_analysis_1226 " will be removed from "TV_analysis_1226 MPC_A2.1_001 (01)_FL"
# Result: "MPC_A2.1_001 (01)_FL"
pattern_to_remove = "TV_analysis_1226 "

# === STEP 1: Preview changes (dry run) ===
print("=== PREVIEW: What will be changed ===\n")
changes = remove_pattern_from_filenames(folder_path, pattern_to_remove, dry_run=True)

if changes:
    # === STEP 2: Confirm and apply changes ===
    print("\n" + "=" * 60)
    response = input("Do you want to apply these changes? (yes/no): ").strip().lower()

    if response in ["yes", "y"]:
        print("\n=== APPLYING CHANGES ===\n")
        remove_pattern_from_filenames(folder_path, pattern_to_remove, dry_run=False)
        print("\n✓ Files renamed successfully!")
    else:
        print("\n✗ Renaming cancelled.")
else:
    print("\nNo files matched the pattern.") """


# === ALTERNATIVE: Using regex pattern ===
# Uncomment the lines below to use regex instead of exact string matching
# This is useful when you want to remove patterns with variable parts


# Example: Remove "TV_analysis_" followed by any number and a space
# This will match "TV_analysis_1226 ", "TV_analysis_0001 ", etc.
import re

regex_pattern = r"TV_analysis_\d+ "

print("\n\n=== USING REGEX PATTERN ===\n")
changes = remove_pattern_regex(folder_path, regex_pattern, dry_run=True)

if changes:
    response = input("\nApply regex-based changes? (yes/no): ").strip().lower()
    if response in ["yes", "y"]:
        remove_pattern_regex(folder_path, regex_pattern, dry_run=False)
        print("\n✓ Files renamed successfully!")
