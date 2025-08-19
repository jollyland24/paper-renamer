#!/usr/bin/env python3
"""
Academic PDF Renamer
Automatically renames academic papers based on their title content.

Usage:
1. Install PyPDF2: pip install PyPDF2
2. Update the FOLDER_PATH variable below to point to your PDF folder
3. Run: python rename_papers.py

License: MIT
"""

import PyPDF2
import re
import os
from pathlib import Path

# CONFIGURATION
FOLDER_PATH = "path/to/your/pdf/folder"  # UPDATE THIS PATH
MAX_FILENAME_LENGTH = 120
MIN_TITLE_LENGTH = 15

def clean_filename(text):
    """Clean text to be safe for use as filename."""
    # Remove invalid filename characters
    text = re.sub(r'[<>:"/\\|?*]', '', text)
    # Replace multiple spaces with single space
    text = re.sub(r'\s+', ' ', text).strip()
    # Limit length
    return text[:MAX_FILENAME_LENGTH]

def extract_paper_title(pdf_path):
    """Extract title from PDF using multiple strategies."""
    try:
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            
            # Strategy 1: Try PDF metadata first
            if reader.metadata and reader.metadata.title:
                title = reader.metadata.title.strip()
                if len(title) > MIN_TITLE_LENGTH:
                    return clean_filename(title)
            
            # Strategy 2: Extract from first page content
            first_page = reader.pages[0].extract_text()
            lines = [line.strip() for line in first_page.split('\n') if line.strip()]
            
            # Look for title patterns in first 15 lines
            potential_titles = []
            
            for i, line in enumerate(lines[:15]):
                # Filter out short lines, page numbers, and headers
                if (len(line) > MIN_TITLE_LENGTH and 
                    not re.match(r'^\d+$', line) and  # Skip page numbers
                    not re.match(r'^[A-Z\s]{3,}$', line) and  # Skip ALL CAPS headers
                    (':' in line or len(line) > 30)):  # Prefer lines with colons or longer lines
                    
                    potential_titles.append((len(line), line, i))
            
            # Sort by length (longer first) then by position (earlier first)
            potential_titles.sort(key=lambda x: (-x[0], x[2]))
            
            if potential_titles:
                return clean_filename(potential_titles[0][1])
            
            # Strategy 3: Fallback to first substantial line
            for line in lines[:10]:
                if MIN_TITLE_LENGTH <= len(line) <= 200:
                    return clean_filename(line)
                    
    except Exception as e:
        print(f"Error reading {pdf_path}: {e}")
    
    return None

def is_already_renamed(filename):
    """Check if file already has a descriptive name."""
    stem = Path(filename).stem
    # Skip if filename is long and doesn't look like random characters
    return (len(stem) > 50 and 
            not re.match(r'^[a-f0-9\-_]+$', stem.lower()) and
            not re.match(r'^(document|paper|file)\d*$', stem.lower()))

def rename_academic_pdfs(folder_path):
    """Main function to rename PDFs in specified folder."""
    folder = Path(folder_path)
    
    if not folder.exists():
        print(f"Error: Folder '{folder_path}' doesn't exist!")
        print("Please update the FOLDER_PATH variable in the script.")
        return
    
    pdf_files = list(folder.glob("*.pdf"))
    
    if not pdf_files:
        print(f"No PDF files found in '{folder_path}'")
        return
    
    print(f"Found {len(pdf_files)} PDF files")
    print("-" * 50)
    
    renamed_count = 0
    skipped_count = 0
    
    for pdf_file in pdf_files:
        print(f"\nProcessing: {pdf_file.name}")
        
        # Skip if already has descriptive name
        if is_already_renamed(pdf_file.name):
            print("  → Skipping (already has descriptive name)")
            skipped_count += 1
            continue
        
        # Extract title
        title = extract_paper_title(pdf_file)
        
        if not title:
            print("  ✗ Could not extract title")
            continue
        
        # Check if new title is meaningfully different
        if title.lower() == pdf_file.stem.lower():
            print("  → Title same as current filename, skipping")
            skipped_count += 1
            continue
        
        # Handle potential filename conflicts
        new_name = f"{title}.pdf"
        new_path = pdf_file.parent / new_name
        
        counter = 1
        base_title = title
        while new_path.exists() and new_path != pdf_file:
            title = f"{base_title}_{counter}"
            new_name = f"{title}.pdf"
            new_path = pdf_file.parent / new_name
            counter += 1
        
        # Rename the file
        try:
            pdf_file.rename(new_path)
            print(f"  ✓ Renamed to: {new_name}")
            renamed_count += 1
        except Exception as e:
            print(f"  ✗ Error renaming: {e}")
    
    print("\n" + "=" * 50)
    print(f"SUMMARY:")
    print(f"  Renamed: {renamed_count} files")
    print(f"  Skipped: {skipped_count} files")
    print(f"  Total processed: {len(pdf_files)} files")

def main():
    """Entry point of the script."""
    print("Academic PDF Renamer")
    print("=" * 50)
    
    # Check if user updated the folder path
    if FOLDER_PATH == "path/to/your/pdf/folder":
        print("ERROR: Please update the FOLDER_PATH variable in the script!")
        print("Current path:", FOLDER_PATH)
        return
    
    rename_academic_pdfs(FOLDER_PATH)

if __name__ == "__main__":
    main()