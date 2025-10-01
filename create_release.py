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
    
    # Note: We no longer copy the executable to the repository
    # Executables should be uploaded as GitHub Releases instead
    print("ℹ️  Executables are no longer stored in the repository.")
    print("   They should be uploaded as GitHub Releases instead.")
    
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
        "create_release.py",
        "create_github_release.py",
        "PhotoWatermark.spec",
        "test_app.py",
        "test_dragdrop.py",
        "test_missing_features.py",
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
    
    # Create a simple release package with just documentation
    timestamp = datetime.now().strftime("%Y%m%d")
    release_zip = f"PhotoWatermark_v1.1.0_{timestamp}_source_only.zip"
    
    with zipfile.ZipFile(release_zip, 'w', zipfile.ZIP_DEFLATED) as zf:
        for root, dirs, files in os.walk(release_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, release_dir)
                zf.write(file_path, arcname)
    
    print(f"✓ Created source-only release package: {release_zip}")
    
    # Calculate file sizes
    zip_size = os.path.getsize(release_zip) / (1024 * 1024)  # MB
    
    print(f"\n📦 Release Summary:")
    print(f"   Release package: {zip_size:.1f} MB")
    print(f"   Files included: {len(os.listdir(release_dir))} items")
    
    print(f"\n🚀 Ready for GitHub release!")
    print(f"   Upload: {release_zip}")
    print(f"   Tag: v1.1.0")
    print(f"   Title: Photo Watermark Application v1.1.0")
    print("\n💡 To create executables for release:")
    print("   1. Run 'pyinstaller --onefile --windowed main.py'")
    print("   2. Upload the executable as a GitHub Release asset")
    print("   3. Source code is already in this package")
    
    return True

if __name__ == "__main__":
    success = create_release_package()
    if not success:
        exit(1)