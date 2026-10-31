"""Module for renaming chromatogram files in bulk.

This module provides flexible functions to rename multiple files in a folder
by removing or replacing patterns in filenames. Useful when exporting data
from ChromNAV or other chromatography software with long, unwieldy filenames.

Example usage:
    from chroma_tool_py.io.rename import remove_pattern_from_filenames

    folder = "path/to/your/files"
    pattern = "TV_analysis_1226 "
    remove_pattern_from_filenames(folder, pattern)
"""

import os
import re


def remove_pattern_from_filenames(folder_path, pattern, dry_run=True):
    """
    Remove a specific pattern from all filenames in a folder.

    Args:
        folder_path (str): Path to the folder containing files to rename
        pattern (str): Pattern to remove from filenames (can be string or regex)
        dry_run (bool): If True, only preview changes without renaming. Default: True

    Returns:
        list: List of tuples (old_name, new_name) showing the changes

    Example:
        # Preview changes
        changes = remove_pattern_from_filenames(
            "C:/data/FL",
            "TV_analysis_1226 ",
            dry_run=True
        )

        # Apply changes
        remove_pattern_from_filenames(
            "C:/data/FL",
            "TV_analysis_1226 ",
            dry_run=False
        )
    """
    changes = []

    if not os.path.exists(folder_path):
        raise FileNotFoundError(f"Folder not found: {folder_path}")

    print(f"Processing files in: {folder_path}")
    print(f"Pattern to remove: '{pattern}'")
    print(f"Mode: {'DRY RUN (preview only)' if dry_run else 'APPLYING CHANGES'}")
    print("-" * 60)

    for filename in os.listdir(folder_path):
        old_path = os.path.join(folder_path, filename)

        # Skip directories
        if os.path.isdir(old_path):
            continue

        # Remove pattern from filename
        new_filename = filename.replace(pattern, "")

        # Only process if name actually changed
        if new_filename != filename:
            new_path = os.path.join(folder_path, new_filename)
            changes.append((filename, new_filename))

            print(f"  {filename}")
            print(f"  -> {new_filename}")
            print()

            if not dry_run:
                # Check if target filename already exists
                if os.path.exists(new_path):
                    print(f"  WARNING: Skipping - target file already exists!")
                    print()
                else:
                    os.rename(old_path, new_path)

    print("-" * 60)
    print(f"Total files to rename: {len(changes)}")

    if dry_run and changes:
        print("\nTo apply these changes, run with dry_run=False")

    return changes


def remove_pattern_regex(folder_path, regex_pattern, dry_run=True):
    """
    Remove a regex pattern from all filenames in a folder.

    Args:
        folder_path (str): Path to the folder containing files to rename
        regex_pattern (str): Regex pattern to remove from filenames
        dry_run (bool): If True, only preview changes without renaming. Default: True

    Returns:
        list: List of tuples (old_name, new_name) showing the changes

    Example:
        # Remove "TV_analysis_" followed by any digits and a space
        changes = remove_pattern_regex(
            "C:/data/FL",
            r"TV_analysis_\d+ ",
            dry_run=True
        )
    """
    changes = []

    if not os.path.exists(folder_path):
        raise FileNotFoundError(f"Folder not found: {folder_path}")

    print(f"Processing files in: {folder_path}")
    print(f"Regex pattern to remove: '{regex_pattern}'")
    print(f"Mode: {'DRY RUN (preview only)' if dry_run else 'APPLYING CHANGES'}")
    print("-" * 60)

    pattern = re.compile(regex_pattern)

    for filename in os.listdir(folder_path):
        old_path = os.path.join(folder_path, filename)

        # Skip directories
        if os.path.isdir(old_path):
            continue

        # Remove pattern from filename using regex
        new_filename = pattern.sub("", filename)

        # Only process if name actually changed
        if new_filename != filename:
            new_path = os.path.join(folder_path, new_filename)
            changes.append((filename, new_filename))

            print(f"  {filename}")
            print(f"  -> {new_filename}")
            print()

            if not dry_run:
                # Check if target filename already exists
                if os.path.exists(new_path):
                    print(f"  WARNING: Skipping - target file already exists!")
                    print()
                else:
                    os.rename(old_path, new_path)

    print("-" * 60)
    print(f"Total files to rename: {len(changes)}")

    if dry_run and changes:
        print("\nTo apply these changes, run with dry_run=False")

    return changes


def replace_pattern_in_filenames(folder_path, old_pattern, new_pattern, dry_run=True):
    """
    Replace a pattern with another string in all filenames in a folder.

    Args:
        folder_path (str): Path to the folder containing files to rename
        old_pattern (str): Pattern to find in filenames
        new_pattern (str): Pattern to replace it with
        dry_run (bool): If True, only preview changes without renaming. Default: True

    Returns:
        list: List of tuples (old_name, new_name) showing the changes

    Example:
        # Replace underscores with hyphens
        changes = replace_pattern_in_filenames(
            "C:/data/FL",
            "_",
            "-",
            dry_run=True
        )
    """
    changes = []

    if not os.path.exists(folder_path):
        raise FileNotFoundError(f"Folder not found: {folder_path}")

    print(f"Processing files in: {folder_path}")
    print(f"Replace: '{old_pattern}' -> '{new_pattern}'")
    print(f"Mode: {'DRY RUN (preview only)' if dry_run else 'APPLYING CHANGES'}")
    print("-" * 60)

    for filename in os.listdir(folder_path):
        old_path = os.path.join(folder_path, filename)

        # Skip directories
        if os.path.isdir(old_path):
            continue

        # Replace pattern in filename
        new_filename = filename.replace(old_pattern, new_pattern)

        # Only process if name actually changed
        if new_filename != filename:
            new_path = os.path.join(folder_path, new_filename)
            changes.append((filename, new_filename))

            print(f"  {filename}")
            print(f"  -> {new_filename}")
            print()

            if not dry_run:
                # Check if target filename already exists
                if os.path.exists(new_path):
                    print(f"  WARNING: Skipping - target file already exists!")
                    print()
                else:
                    os.rename(old_path, new_path)

    print("-" * 60)
    print(f"Total files to rename: {len(changes)}")

    if dry_run and changes:
        print("\nTo apply these changes, run with dry_run=False")

    return changes
