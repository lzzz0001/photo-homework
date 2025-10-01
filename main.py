"""
Photo Watermark Application - Main Entry Point
A comprehensive tool for adding text and image watermarks to photos.

Features:
- Text and image watermarking
- Batch processing
- Real-time preview
- Template management
- Multiple export formats

Author: Photo Watermark Team
Version: 1.1.0
"""

import sys
import os
import tkinter as tk
from tkinter import messagebox

# Add the src directory to the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(current_dir, 'src')
sys.path.insert(0, src_dir)

def check_dependencies():
    """Check if all required dependencies are available"""
    missing_deps = []
    
    try:
        from PIL import Image
    except ImportError:
        missing_deps.append("Pillow")
    
    try:
        import tkinter
    except ImportError:
        missing_deps.append("tkinter")
    
    if missing_deps:
        error_msg = f"Missing required dependencies: {', '.join(missing_deps)}\n\n"
        error_msg += "Please install them using:\n"
        error_msg += "pip install -r requirements.txt"
        
        # Try to show error in GUI if tkinter is available
        try:
            root = tk.Tk()
            root.withdraw()  # Hide the main window
            messagebox.showerror("Missing Dependencies", error_msg)
            root.destroy()
        except:
            print(f"ERROR: {error_msg}")
        
        return False
    
    return True

def setup_application_environment():
    """Setup the application environment and directories"""
    try:
        # Ensure required directories exist
        directories = ['templates', 'assets']
        for directory in directories:
            dir_path = os.path.join(current_dir, directory)
            os.makedirs(dir_path, exist_ok=True)
        
        return True
    except Exception as e:
        error_msg = f"Failed to setup application environment: {e}"
        try:
            root = tk.Tk()
            root.withdraw()
            messagebox.showerror("Setup Error", error_msg)
            root.destroy()
        except:
            print(f"ERROR: {error_msg}")
        return False

def main():
    """Main application entry point"""
    print("Starting Photo Watermark Application...")
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Setup environment
    if not setup_application_environment():
        sys.exit(1)
    
    try:
        # Import the main application class
        print("Importing GUI modules...")
        from gui_main import WatermarkApp
        print("GUI modules imported successfully!")
        
        # Create and run the application
        print("Initializing GUI...")
        app = WatermarkApp()
        print("GUI initialized successfully!")
        
        print("Application ready! Starting main loop...")
        app.run()
        print("Application closed.")
        
    except ImportError as e:
        error_msg = f"Failed to import application modules: {e}\n\n"
        error_msg += "Please ensure all source files are present in the 'src' directory."
        
        try:
            root = tk.Tk()
            root.withdraw()
            messagebox.showerror("Import Error", error_msg)
            root.destroy()
        except:
            print(f"ERROR: {error_msg}")
        
        sys.exit(1)
        
    except Exception as e:
        error_msg = f"Unexpected error occurred: {e}"
        
        try:
            root = tk.Tk()
            root.withdraw()
            messagebox.showerror("Application Error", error_msg)
            root.destroy()
        except:
            print(f"ERROR: {error_msg}")
        
        sys.exit(1)

if __name__ == "__main__":
    main()