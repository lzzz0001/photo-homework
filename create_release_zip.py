import zipfile
import os
from datetime import datetime

def create_release_zip():
    """Create a zip file of the release directory"""
    # Get current timestamp
    timestamp = datetime.now().strftime("%Y%m%d")
    zip_filename = f"PhotoWatermark_v1.1.0_GitHub_Release_{timestamp}.zip"
    
    # Get all files in the release directory
    release_dir = "github_release_v1.1.0"
    release_files = os.listdir(release_dir)
    
    # Create zip file
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zf:
        for filename in release_files:
            file_path = os.path.join(release_dir, filename)
            zf.write(file_path, filename)
    
    print(f"Created release package: {zip_filename}")
    file_size = os.path.getsize(zip_filename) / (1024 * 1024)  # MB
    print(f"Package size: {file_size:.1f} MB")

if __name__ == "__main__":
    create_release_zip()