
import sys
import traceback

def verify_imports():
    """Verify all critical imports work within the executable"""
    print("Verifying imports within executable...")
    
    critical_imports = [
        ("tkinter", "GUI framework"),
        ("PIL", "Python Imaging Library"),
        ("PIL.Image", "Image processing"),
        ("PIL.ImageDraw", "Image drawing"),
        ("PIL.ImageFont", "Font handling"),
        ("PIL.ImageTk", "Tkinter-PIL integration"),
        ("windnd", "Drag and drop functionality"),
        ("src.gui_main", "Main application module"),
        ("src.image_processor", "Image processing module"),
        ("src.file_manager", "File management module"),
        ("src.template_manager", "Template management module")
    ]
    
    failed_imports = []
    
    for module_name, description in critical_imports:
        try:
            __import__(module_name)
            print(f"✓ {module_name} - {description}")
        except ImportError as e:
            print(f"✗ {module_name} - {description} - FAILED: {e}")
            failed_imports.append((module_name, str(e)))
        except Exception as e:
            print(f"✗ {module_name} - {description} - ERROR: {e}")
            failed_imports.append((module_name, str(e)))
    
    if failed_imports:
        print(f"\nFailed imports ({len(failed_imports)}):")
        for module, error in failed_imports:
            print(f"  {module}: {error}")
        return False
    else:
        print("\nAll imports successful!")
        return True

if __name__ == "__main__":
    try:
        success = verify_imports()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"Unexpected error during import verification: {e}")
        traceback.print_exc()
        sys.exit(1)
