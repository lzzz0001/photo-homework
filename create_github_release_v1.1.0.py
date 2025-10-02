#!/usr/bin/env python3
"""
Script to create a complete GitHub release package for the Photo Watermark Application v1.1.0.
This includes the fixed executable and all necessary documentation.
"""

import os
import sys
import zipfile
import shutil
import subprocess
from datetime import datetime

def create_github_release_package():
    """Create a complete GitHub release package with the fixed executable"""
    print("Creating GitHub release package for Photo Watermark Application v1.1.0...")
    print("=" * 60)
    
    # Create release directory
    release_dir = "github_release_v1.1.0"
    if os.path.exists(release_dir):
        shutil.rmtree(release_dir)
    os.makedirs(release_dir)
    
    # Check if the fixed executable exists
    exe_path = os.path.join("dist", "PhotoWatermark_v1.1.0_20251001.exe")
    if not os.path.exists(exe_path):
        print("❌ Error: Fixed executable not found!")
        print(f"   Expected path: {exe_path}")
        print("   Please run build_robust.bat first to create the executable.")
        return False
    
    print("✓ Found fixed executable")
    
    # Copy the fixed executable to release directory
    release_exe_name = "PhotoWatermark_v1.1.0_Windows_x64.exe"
    shutil.copy2(exe_path, os.path.join(release_dir, release_exe_name))
    print(f"✓ Copied executable as: {release_exe_name}")
    
    # Copy documentation files
    docs_to_copy = [
        "README.md",
        "RELEASE_NOTES.md", 
        "LICENSE",
        "CHANGELOG.md",
        "IMPORT_FIXES_SUMMARY.md",
        "GITHUB_RELEASE_INSTRUCTIONS.md"
    ]
    
    for doc in docs_to_copy:
        if os.path.exists(doc):
            shutil.copy2(doc, os.path.join(release_dir, doc))
            print(f"✓ Copied {doc}")
        else:
            print(f"⚠ Warning: {doc} not found")
    
    # Create installation instructions
    install_instructions = os.path.join(release_dir, "INSTALLATION.md")
    with open(install_instructions, 'w', encoding='utf-8') as f:
        f.write("""# Photo Watermark Application v1.1.0 - Installation Instructions

## Windows Installation

1. Download `PhotoWatermark_v1.1.0_Windows_x64.exe`
2. Right-click the executable and select "Run as administrator" (recommended)
3. If you see a Windows SmartScreen warning, click "More info" then "Run anyway"
4. The application will start immediately - no installation required

## System Requirements

- Windows 7 or later (64-bit)
- No additional software installation required

## Features

- Text and image watermarking
- Batch processing of multiple images
- Real-time preview
- Drag-and-drop file import
- Template management
- Support for Chinese and Western fonts
- Multiple export formats (JPEG, PNG)

## Usage

1. Launch the application
2. Import images using:
   - Drag-and-drop files or folders onto the application window
   - Click "Select Files" or "Select Folder" buttons
3. Configure watermark settings:
   - Text watermark: Enter text, select font, size, color
   - Image watermark: Select an image file
4. Adjust position and styling options
5. Preview the watermark effect
6. Export watermarked images

## Troubleshooting

If the application fails to start:
1. Ensure you're running the latest version
2. Check Windows Event Viewer for error details
3. Try running as administrator
4. Verify Windows Defender or antivirus is not blocking the application

For any issues, please report them at:
https://github.com/lzzz0001/photo-homework/issues
""")
    
    print("✓ Created installation instructions")
    
    # Create source code package
    source_files = [
        "main.py",
        "safe_main.py",
        "requirements.txt",
        "requirements_full.txt",
        "README.md",
        "RELEASE_NOTES.md",
        "CHANGELOG.md",
        "LICENSE",
        "build_robust.bat",
        "src/"
    ]
    
    source_zip = os.path.join(release_dir, "PhotoWatermark_v1.1.0_source.zip")
    with zipfile.ZipFile(source_zip, 'w', zipfile.ZIP_DEFLATED) as zf:
        for item in source_files:
            if os.path.exists(item):
                if os.path.isfile(item):
                    zf.write(item)
                    print(f"✓ Added to source package: {item}")
                elif os.path.isdir(item):
                    for root, dirs, files in os.walk(item):
                        # Skip __pycache__ directories
                        dirs[:] = [d for d in dirs if not d.startswith('__') and d != '.git']
                        for file in files:
                            if not file.endswith(('.pyc', '.pyo')):
                                file_path = os.path.join(root, file)
                                zf.write(file_path)
                                print(f"✓ Added to source package: {file_path}")
    
    print("✓ Created source code package")
    
    # Create release notes specific to this release
    release_notes = os.path.join(release_dir, "RELEASE_NOTES_v1.1.0.md")
    with open(release_notes, 'w', encoding='utf-8') as f:
        f.write("""# Photo Watermark Application v1.1.0 Release Notes

## Version Information
- Version: v1.1.0
- Release Date: October 1, 2025
- Platform: Windows 64-bit

## What's New

### Fixed Import Issues
- Resolved critical import errors that prevented the application from starting
- Properly bundled all tkinter and PIL dependencies
- Fixed windnd library inclusion for drag-and-drop functionality
- Enhanced executable stability and reliability

### Enhanced Features
- Improved drag-and-drop support with Windows native integration
- Better error handling and user feedback
- Optimized startup performance
- Enhanced compatibility with various Windows versions

## Files Included

1. `PhotoWatermark_v1.1.0_Windows_x64.exe` - Standalone Windows executable
2. `PhotoWatermark_v1.1.0_source.zip` - Complete source code
3. `README.md` - Main documentation
4. `RELEASE_NOTES_v1.1.0.md` - This file
5. `INSTALLATION.md` - Installation instructions
6. `LICENSE` - License information
7. `CHANGELOG.md` - Complete change history

## Installation

Simply download and run `PhotoWatermark_v1.1.0_Windows_x64.exe`. No installation is required.

## System Requirements

- Windows 7 or later (64-bit)
- No additional dependencies required

## Known Issues

None at this time. This release fixes all known import and startup issues from previous versions.

## Changelog Summary

For a complete changelog, see `CHANGELOG.md`.

## Support

For issues, questions, or feature requests, please visit:
https://github.com/lzzz0001/photo-homework/issues
""")
    
    print("✓ Created release notes")
    
    # Create a summary file
    summary_file = os.path.join(release_dir, "RELEASE_SUMMARY.txt")
    with open(summary_file, 'w', encoding='utf-8') as f:
        f.write("""Photo Watermark Application v1.1.0 - GitHub Release Package
================================================================

This package contains everything needed for the v1.1.0 release of the Photo Watermark Application.

Contents:
1. PhotoWatermark_v1.1.0_Windows_x64.exe - Fixed standalone executable
2. PhotoWatermark_v1.1.0_source.zip - Complete source code
3. Documentation files (README.md, LICENSE, etc.)
4. Installation and release notes

Important: This release fixes critical import errors that affected previous versions.
The executable now properly includes all dependencies and should start without issues.

For installation instructions, see INSTALLATION.md
For detailed release notes, see RELEASE_NOTES_v1.1.0.md
""")
    
    print("✓ Created release summary")
    
    # Calculate file sizes
    exe_size = os.path.getsize(os.path.join(release_dir, release_exe_name)) / (1024 * 1024)  # MB
    source_size = os.path.getsize(source_zip) / (1024 * 1024)  # MB
    
    print(f"\n📦 Release Package Summary:")
    print(f"   Executable: {exe_size:.1f} MB")
    print(f"   Source code: {source_size:.1f} MB")
    print(f"   Total files: {len(os.listdir(release_dir))} items")
    print(f"   Release directory: {release_dir}")
    
    print(f"\n🚀 GitHub Release Package Ready!")
    print(f"   Contents are in the '{release_dir}' directory.")
    print(f"   You can now upload these files to GitHub Releases.")
    
    print(f"\n📋 Next Steps for GitHub Release:")
    print(f"   1. Go to https://github.com/lzzz0001/photo-homework/releases")
    print(f"   2. Click 'Draft a new release'")
    print(f"   3. Create tag: v1.1.0")
    print(f"   4. Title: 'Photo Watermark Application v1.1.0'")
    print(f"   5. Upload all files from the '{release_dir}' directory")
    print(f"   6. Copy release notes from RELEASE_NOTES_v1.1.0.md")
    print(f"   7. Publish release")
    
    return True

def main():
    """Main function"""
    print("Photo Watermark Application - GitHub Release Package Creator v1.1.0")
    print("=" * 70)
    
    success = create_github_release_package()
    if not success:
        sys.exit(1)
    
    print("\n🎉 Release package creation completed successfully!")

if __name__ == "__main__":
    main()