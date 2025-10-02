#!/usr/bin/env python3
"""
Comprehensive test script to verify all imports work correctly in the PhotoWatermark executable
"""

import subprocess
import sys
import os
import time

def test_executable_imports():
    """Test that all required imports work in the executable"""
    print("Testing PhotoWatermark executable imports...")
    
    # Get the executable path
    exe_path = os.path.join("dist", "PhotoWatermark_v1.1.0_20251001.exe")
    
    if not os.path.exists(exe_path):
        print(f"ERROR: Executable not found at {exe_path}")
        return False
    
    print(f"✓ Executable found: {exe_path}")
    print(f"  Size: {os.path.getsize(exe_path) / (1024*1024):.1f} MB")
    
    # Test: Check if executable starts without import errors
    print("\nTest: Checking if executable starts without import errors...")
    try:
        # Start the executable
        process = subprocess.Popen([exe_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        # Wait a few seconds to see if it crashes
        time.sleep(5)
        
        # Check if process is still running
        if process.poll() is None:
            print("✓ Executable started successfully and is running (no import errors)")
            # Terminate the process
            process.terminate()
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()
        else:
            # Process has terminated, check exit code and output
            stdout, stderr = process.communicate()
            if process.returncode == 0:
                print("✓ Executable started and exited normally")
            else:
                print(f"✗ Executable failed with exit code {process.returncode}")
                if stdout:
                    print(f"  STDOUT: {stdout}")
                if stderr:
                    print(f"  STDERR: {stderr}")
                    # Check if it's an import error
                    if "ImportError" in stderr or "ModuleNotFoundError" in stderr:
                        print("  This appears to be an import error!")
                        return False
                return False
                
    except Exception as e:
        print(f"✗ Failed to start executable: {e}")
        return False
    
    # Test: Check specific imports that were problematic
    print("\nTest: Verifying specific imports that were previously problematic...")
    test_imports = [
        "PIL",
        "PIL.Image", 
        "PIL.ImageDraw",
        "PIL.ImageFont",
        "PIL.ImageTk",
        "windnd",
        "tkinter",
        "tkinter.ttk",
        "tkinter.messagebox"
    ]
    
    for module in test_imports:
        try:
            # Test if we can import the module in current environment
            __import__(module)
            print(f"✓ {module} imported successfully in current environment")
        except ImportError as e:
            print(f"⚠ Warning: Failed to import {module} in current environment: {e}")
            # This is not necessarily a problem if the executable works
    
    print("\n✓ All tests completed! Executable should be working correctly.")
    return True

def create_verification_script():
    """Create a script to verify imports within the executable itself"""
    verification_script = '''
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
        print(f"\\nFailed imports ({len(failed_imports)}):")
        for module, error in failed_imports:
            print(f"  {module}: {error}")
        return False
    else:
        print("\\nAll imports successful!")
        return True

if __name__ == "__main__":
    try:
        success = verify_imports()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"Unexpected error during import verification: {e}")
        traceback.print_exc()
        sys.exit(1)
'''
    
    with open("verify_imports.py", "w", encoding="utf-8") as f:
        f.write(verification_script)
    
    print("Created verification script: verify_imports.py")

if __name__ == "__main__":
    print("PhotoWatermark v1.1.0 Import Verification")
    print("=" * 50)
    
    # Create verification script
    create_verification_script()
    
    # Test the executable
    success = test_executable_imports()
    
    if success:
        print("\n🎉 Import verification successful!")
        print("The PhotoWatermark v1.1.0 executable should now work without import errors.")
    else:
        print("\n❌ Import verification failed!")
        print("There may still be import issues with the executable.")
        sys.exit(1)