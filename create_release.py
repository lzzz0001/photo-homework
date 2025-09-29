"""
Script to help create a GitHub release with the built executable
"""

import os
import shutil
import zipfile
from datetime import datetime

def create_release_package():
    """Create a release package with the executable and documentation"""
    
    print("Creating release package...")
    
    # Create release directory
    release_dir = "release"
    if os.path.exists(release_dir):
        shutil.rmtree(release_dir)
    os.makedirs(release_dir)
    
    # Copy executable
    if os.path.exists("dist/PhotoWatermark.exe"):
        shutil.copy2("dist/PhotoWatermark.exe", os.path.join(release_dir, "PhotoWatermark.exe"))
        print("✓ Copied executable")
    else:
        print("✗ Executable not found! Run 'pyinstaller PhotoWatermark.spec' first")
        return False
    
    # Copy documentation
    docs_to_copy = [
        "README.md",
        "RELEASE_NOTES.md", 
        "LICENSE",
        "CHANGELOG.md"
    ]
    
    for doc in docs_to_copy:
        if os.path.exists(doc):
            shutil.copy2(doc, os.path.join(release_dir, doc))
            print(f"✓ Copied {doc}")
    
    # Create source code zip
    print("Creating source code archive...")
    source_files = [
        "main.py",
        "requirements.txt",
        "PhotoWatermark.spec",
        "test_app.py",
        "src/"
    ]
    
    with zipfile.ZipFile(os.path.join(release_dir, "source_code.zip"), 'w', zipfile.ZIP_DEFLATED) as zf:
        for item in source_files:
            if os.path.isfile(item):
                zf.write(item)
            elif os.path.isdir(item):
                for root, dirs, files in os.walk(item):
                    for file in files:
                        file_path = os.path.join(root, file)
                        zf.write(file_path)
    
    print("✓ Created source code archive")
    
    # Create final release zip
    timestamp = datetime.now().strftime("%Y%m%d")
    release_zip = f"PhotoWatermark_v1.0.0_{timestamp}.zip"
    
    with zipfile.ZipFile(release_zip, 'w', zipfile.ZIP_DEFLATED) as zf:
        for root, dirs, files in os.walk(release_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, release_dir)
                zf.write(file_path, arcname)
    
    print(f"✓ Created release package: {release_zip}")
    
    # Calculate file sizes
    exe_size = os.path.getsize("dist/PhotoWatermark.exe") / (1024 * 1024)  # MB
    zip_size = os.path.getsize(release_zip) / (1024 * 1024)  # MB
    
    print(f"\n📦 Release Summary:")
    print(f"   Executable size: {exe_size:.1f} MB")
    print(f"   Release package: {zip_size:.1f} MB")
    print(f"   Files included: {len(os.listdir(release_dir))} items")
    
    print(f"\n🚀 Ready for GitHub release!")
    print(f"   Upload: {release_zip}")
    print(f"   Tag: v1.0.0")
    print(f"   Title: Photo Watermark Application v1.0.0")
    
    return True

if __name__ == "__main__":
    success = create_release_package()
    if not success:
        exit(1)