"""
Simple test for drag-drop functionality
"""

import tkinter as tk
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_windnd():
    """Test windnd functionality directly"""
    try:
        import windnd
        
        root = tk.Tk()
        root.title("Drag-Drop Test")
        root.geometry("400x300")
        
        # Create a simple frame
        frame = tk.Frame(root, bg='lightgray', relief='sunken', bd=2)
        frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        label = tk.Label(frame, text="Drag files here to test", bg='lightgray', font=('Arial', 14))
        label.pack(expand=True)
        
        def on_drop(files):
            print(f"Files dropped: {files}")
            print(f"Type: {type(files)}")
            for i, file in enumerate(files):
                print(f"  {i}: {file} (exists: {os.path.exists(file)})")
            
            # Update label
            label.config(text=f"Dropped {len(files)} files\nCheck console for details")
        
        # Hook drag-drop
        windnd.hook_dropfiles(frame, func=on_drop)
        
        print("Windnd test ready - drag files to the window")
        root.mainloop()
        
    except ImportError:
        print("windnd not available")
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_windnd()