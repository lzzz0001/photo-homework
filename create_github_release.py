#!/usr/bin/env python3
"""
Script to create GitHub releases for the Photo Watermark Application.
This script helps package the application and prepare it for GitHub Releases.
"""

import os
import sys
import zipfile
import shutil
import subprocess
from datetime import datetime

def create_release_package():
    """Create a release package for GitHub Releases"""
    print("Creating release package for GitHub...")
    
    # Get version from create_release.py or use current date
    version = datetime.now().strftime("v1.0.%Y%m%d")
    
    # Create release directory
    release_dir = "temp_release"
    if os.path.exists(release_dir):
        shutil.rmtree(release_dir)
    os.makedirs(release_dir)
    
    # Copy source code
    source_code_zip = os.path.join(release_dir, f"PhotoWatermark_{version}_source.zip")
    with zipfile.ZipFile(source_code_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk('.'):
            # Skip git, temp, and release directories
            dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['temp_release', 'release', '__pycache__', 'test_output', 'test_formats']]
            
            for file in files:
                if not file.endswith(('.pyc', '.pyo', '.log')) and not file.startswith('.'):
                    file_path = os.path.join(root, file)
                    arc_path = os.path.relpath(file_path, '.')
                    zipf.write(file_path, arc_path)
    
    print(f"Created source code package: {source_code_zip}")
    
    # Create a simple README for releases
    release_readme = os.path.join(release_dir, "RELEASE_INSTRUCTIONS.md")
    with open(release_readme, 'w', encoding='utf-8') as f:
        f.write(f"""# Photo Watermark Application Release {version}

## Contents
- `PhotoWatermark_{version}_source.zip` - Complete source code package

## How to Create Executable
1. Install requirements: `pip install -r requirements.txt`
2. Install PyInstaller: `pip install pyinstaller`
3. Create executable: `pyinstaller --onefile --windowed main.py`
4. The executable will be in the `dist/` folder

## How to Upload to GitHub Releases
1. Go to https://github.com/lzzz0001/photo-homework/releases
2. Click "Draft a new release"
3. Create a new tag: {version}
4. Set release title: "Photo Watermark Application {version}"
5. Upload the source code ZIP file
6. Add release notes describing changes
7. Publish release

## Requirements
- Python 3.7 or higher
- Dependencies listed in requirements.txt
""")
    
    print(f"Created release instructions: {release_readme}")
    print("\nRelease package created successfully!")
    print(f"Files are in the '{release_dir}' directory.")
    print("You can now upload these files to GitHub Releases.")

def main():
    """Main function"""
    print("Photo Watermark Application - GitHub Release Creator")
    print("=" * 50)
    
    create_release_package()

if __name__ == "__main__":
    main()