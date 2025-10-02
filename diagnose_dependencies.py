#!/usr/bin/env python3
"""
Diagnostic script to verify PIL/Pillow installation and import capabilities.
This helps diagnose import issues that might appear in IDEs but not in runtime.
"""

import sys
import os

def check_python_environment():
    """Check current Python environment"""
    print("=" * 60)
    print("PYTHON ENVIRONMENT DIAGNOSTICS")
    print("=" * 60)
    print(f"Python executable: {sys.executable}")
    print(f"Python version: {sys.version}")
    print(f"Python path: {sys.path}")
    print()

def check_pil_installation():
    """Check PIL/Pillow installation and functionality"""
    print("=" * 60)
    print("PIL/PILLOW DIAGNOSTICS")
    print("=" * 60)
    
    try:
        import PIL
        print(f"✓ PIL package found at: {PIL.__file__}")
        print(f"✓ PIL version: {PIL.__version__}")
    except ImportError as e:
        print(f"✗ PIL package not found: {e}")
        return False
    
    # Test specific PIL modules
    modules_to_test = [
        'PIL.Image',
        'PIL.ImageDraw', 
        'PIL.ImageFont',
        'PIL.ImageTk',
        'PIL.ImageOps',
        'PIL.ImageEnhance'
    ]
    
    for module_name in modules_to_test:
        try:
            __import__(module_name)
            print(f"✓ {module_name} import successful")
        except ImportError as e:
            print(f"✗ {module_name} import failed: {e}")
    
    # Test basic PIL functionality
    try:
        from PIL import Image
        # Create a test image
        test_image = Image.new('RGB', (100, 100), color='red')
        print("✓ PIL basic functionality test passed")
        return True
    except Exception as e:
        print(f"✗ PIL functionality test failed: {e}")
        return False

def check_tkinter_installation():
    """Check tkinter installation"""
    print("=" * 60)
    print("TKINTER DIAGNOSTICS")
    print("=" * 60)
    
    try:
        import tkinter as tk
        print(f"✓ tkinter found at: {tk.__file__}")
        
        # Test tkinter submodules
        submodules = ['tkinter.ttk', 'tkinter.messagebox', 'tkinter.filedialog']
        for submodule in submodules:
            try:
                __import__(submodule)
                print(f"✓ {submodule} import successful")
            except ImportError as e:
                print(f"✗ {submodule} import failed: {e}")
        
        return True
    except ImportError as e:
        print(f"✗ tkinter not found: {e}")
        return False

def check_project_structure():
    """Check project structure"""
    print("=" * 60)
    print("PROJECT STRUCTURE DIAGNOSTICS")
    print("=" * 60)
    
    current_dir = os.path.dirname(os.path.abspath(__file__))
    print(f"Current directory: {current_dir}")
    
    required_files = ['main.py', 'requirements.txt', 'src/gui_main.py']
    for file_path in required_files:
        full_path = os.path.join(current_dir, file_path)
        if os.path.exists(full_path):
            print(f"✓ {file_path} exists")
        else:
            print(f"✗ {file_path} missing")

def main():
    """Run all diagnostic checks"""
    print("Photo Watermark Application - Dependency Diagnostics")
    print("This script checks if all required dependencies are properly installed.")
    print()
    
    check_python_environment()
    pil_ok = check_pil_installation()
    tkinter_ok = check_tkinter_installation()
    check_project_structure()
    
    print("=" * 60)
    print("SUMMARY")
    print("=" * 60)
    
    if pil_ok and tkinter_ok:
        print("✓ All core dependencies are working correctly!")
        print("✓ The application should run without import issues.")
        print()
        print("If you're still seeing PIL import errors in your IDE:")
        print("1. Make sure your IDE is using the correct Python interpreter")
        print("2. Try reloading/restarting your IDE")
        print("3. Check if your IDE has a virtual environment activated")
    else:
        print("✗ Some dependencies are missing or not working correctly.")
        print("Please install missing dependencies using:")
        print("pip install -r requirements.txt")
    
    return 0 if (pil_ok and tkinter_ok) else 1

if __name__ == "__main__":
    sys.exit(main())