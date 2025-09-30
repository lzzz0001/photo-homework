"""
File management module for handling image import, export, and file operations.
Supports drag-drop, batch import, and various file format operations.
"""

import os
import shutil
from typing import List, Optional, Tuple, Dict
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image
import sys
import platform

# Import Windows-specific modules for drag-drop if available
if platform.system() == "Windows":
    try:
        import ctypes
        from ctypes import wintypes
        WINDOWS_DND_AVAILABLE = True
    except ImportError:
        WINDOWS_DND_AVAILABLE = False
else:
    WINDOWS_DND_AVAILABLE = False

class FileManager:
    """Handles all file operations for the watermark application"""
    
    # Supported file extensions
    SUPPORTED_EXTENSIONS = {
        '.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.tif'
    }
    
    OUTPUT_FORMATS = {
        'JPEG': ['.jpg', '.jpeg'],
        'PNG': ['.png']
    }
    
    def __init__(self):
        self.imported_files = []  # List of imported file paths
        self.output_directory = ""
        self.prevent_overwrite = True
    
    def is_image_file(self, file_path: str) -> bool:
        """Check if file is a supported image format"""
        _, ext = os.path.splitext(file_path.lower())
        return ext in self.SUPPORTED_EXTENSIONS
    
    def get_image_info(self, file_path: str) -> Optional[Dict]:
        """Get basic information about an image file"""
        try:
            if not self.is_image_file(file_path):
                return None
            
            with Image.open(file_path) as img:
                info = {
                    'path': file_path,
                    'filename': os.path.basename(file_path),
                    'size': img.size,
                    'mode': img.mode,
                    'format': img.format,
                    'file_size': os.path.getsize(file_path)
                }
                return info
        except Exception as e:
            print(f"Error getting image info for {file_path}: {e}")
            return None
    
    def import_single_file(self, file_path: str) -> bool:
        """Import a single image file"""
        if not os.path.exists(file_path):
            return False
        
        if not self.is_image_file(file_path):
            return False
        
        if file_path not in self.imported_files:
            self.imported_files.append(file_path)
            return True
        return False
    
    def import_multiple_files(self, file_paths: List[str]) -> List[str]:
        """Import multiple image files, returns list of successfully imported files"""
        imported = []
        for file_path in file_paths:
            if self.import_single_file(file_path):
                imported.append(file_path)
        return imported
    
    def import_folder(self, folder_path: str, recursive: bool = False) -> List[str]:
        """Import all image files from a folder"""
        imported = []
        
        if not os.path.exists(folder_path) or not os.path.isdir(folder_path):
            return imported
        
        try:
            if recursive:
                # Recursively find all image files
                for root, dirs, files in os.walk(folder_path):
                    for file in files:
                        file_path = os.path.join(root, file)
                        if self.import_single_file(file_path):
                            imported.append(file_path)
            else:
                # Only scan the immediate directory
                for file in os.listdir(folder_path):
                    file_path = os.path.join(folder_path, file)
                    if os.path.isfile(file_path) and self.import_single_file(file_path):
                        imported.append(file_path)
        except Exception as e:
            print(f"Error importing folder {folder_path}: {e}")
        
        return imported
    
    def remove_file(self, file_path: str) -> bool:
        """Remove a file from the imported list"""
        if file_path in self.imported_files:
            self.imported_files.remove(file_path)
            return True
        return False
    
    def clear_all_files(self):
        """Clear all imported files"""
        self.imported_files.clear()
    
    def get_imported_files(self) -> List[str]:
        """Get list of imported file paths"""
        return self.imported_files.copy()
    
    def get_imported_files_info(self) -> List[Dict]:
        """Get detailed information about all imported files"""
        info_list = []
        for file_path in self.imported_files:
            info = self.get_image_info(file_path)
            if info:
                info_list.append(info)
        return info_list
    
    def select_files_dialog(self, parent=None) -> List[str]:
        """Open file dialog to select multiple image files"""
        file_types = [
            ("All Supported Images", "*.jpg;*.jpeg;*.png;*.bmp;*.tiff;*.tif"),
            ("JPEG files", "*.jpg;*.jpeg"),
            ("PNG files", "*.png"),
            ("BMP files", "*.bmp"),
            ("TIFF files", "*.tiff;*.tif"),
            ("All files", "*.*")
        ]
        
        try:
            file_paths = filedialog.askopenfilenames(
                parent=parent,
                title="Select Image Files",
                filetypes=file_types
            )
            return list(file_paths) if file_paths else []
        except Exception as e:
            print(f"Error in file dialog: {e}")
            return []
    
    def select_folder_dialog(self, parent=None) -> str:
        """Open folder dialog to select a directory"""
        try:
            folder_path = filedialog.askdirectory(
                parent=parent,
                title="Select Folder"
            )
            return folder_path if folder_path else ""
        except Exception as e:
            print(f"Error in folder dialog: {e}")
            return ""
    
    def select_output_directory(self, parent=None) -> str:
        """Select output directory for processed images"""
        try:
            folder_path = filedialog.askdirectory(
                parent=parent,
                title="Select Output Directory"
            )
            if folder_path:
                self.output_directory = folder_path
                return folder_path
            return ""
        except Exception as e:
            print(f"Error selecting output directory: {e}")
            return ""
    
    def validate_output_directory(self, output_dir: str) -> Tuple[bool, str]:
        """Validate if output directory is suitable for export"""
        if not output_dir:
            return False, "Output directory not specified"
        
        if not os.path.exists(output_dir):
            try:
                os.makedirs(output_dir, exist_ok=True)
            except Exception as e:
                return False, f"Cannot create output directory: {e}"
        
        if not os.path.isdir(output_dir):
            return False, "Output path is not a directory"
        
        if not os.access(output_dir, os.W_OK):
            return False, "No write permission for output directory"
        
        # Check if output directory is same as any input directory (prevent overwrite)
        if self.prevent_overwrite:
            for file_path in self.imported_files:
                file_dir = os.path.dirname(os.path.abspath(file_path))
                if os.path.abspath(output_dir) == file_dir:
                    return False, "Output directory cannot be the same as input directory to prevent overwriting"
        
        return True, "Output directory is valid"
    
    def generate_output_filename(self, input_path: str, prefix: str = "", 
                                suffix: str = "", output_format: str = "JPEG") -> str:
        """Generate output filename based on naming rules"""
        base_name = os.path.splitext(os.path.basename(input_path))[0]
        new_name = f"{prefix}{base_name}{suffix}"
        
        # Add appropriate extension
        if output_format.upper() == "JPEG":
            new_name += ".jpg"
        else:  # PNG
            new_name += ".png"
        
        return new_name
    
    def check_file_conflicts(self, output_dir: str, input_files: List[str], 
                           prefix: str = "", suffix: str = "", 
                           output_format: str = "JPEG") -> List[str]:
        """Check for potential file conflicts in output directory"""
        conflicts = []
        
        for input_file in input_files:
            output_filename = self.generate_output_filename(
                input_file, prefix, suffix, output_format
            )
            output_path = os.path.join(output_dir, output_filename)
            
            if os.path.exists(output_path):
                conflicts.append(output_path)
        
        return conflicts
    
    def get_file_size_formatted(self, file_path: str) -> str:
        """Get formatted file size string"""
        try:
            size = os.path.getsize(file_path)
            for unit in ['B', 'KB', 'MB', 'GB']:
                if size < 1024.0:
                    return f"{size:.1f} {unit}"
                size /= 1024.0
            return f"{size:.1f} TB"
        except:
            return "Unknown"
    
    def create_thumbnail(self, image_path: str, thumbnail_size: Tuple[int, int] = (150, 150)) -> Optional[Image.Image]:
        """Create a thumbnail image for preview"""
        try:
            with Image.open(image_path) as img:
                # Convert to RGB if necessary for thumbnail
                if img.mode == 'RGBA':
                    # Create white background for RGBA images
                    background = Image.new('RGB', img.size, (255, 255, 255))
                    background.paste(img, mask=img.split()[3])
                    img = background
                elif img.mode != 'RGB':
                    img = img.convert('RGB')
                
                # Create thumbnail maintaining aspect ratio
                img.thumbnail(thumbnail_size, Image.Resampling.LANCZOS)
                return img.copy()
        except Exception as e:
            print(f"Error creating thumbnail for {image_path}: {e}")
            return None
    
    def backup_file(self, file_path: str, backup_dir: Optional[str] = None) -> Optional[str]:
        """Create a backup of a file before processing"""
        try:
            if backup_dir is None:
                backup_dir = os.path.join(os.path.dirname(file_path), "backup")
            
            os.makedirs(backup_dir, exist_ok=True)
            
            filename = os.path.basename(file_path)
            backup_path = os.path.join(backup_dir, filename)
            
            # Add timestamp if file exists
            counter = 1
            base_backup_path = backup_path
            while os.path.exists(backup_path):
                name, ext = os.path.splitext(base_backup_path)
                backup_path = f"{name}_{counter}{ext}"
                counter += 1
            
            shutil.copy2(file_path, backup_path)
            return backup_path
        except Exception as e:
            print(f"Error creating backup for {file_path}: {e}")
            return None

class DragDropHandler:
    """Handles drag and drop functionality for file import with robust Windows support"""
    
    def __init__(self, widget, file_manager: FileManager, callback=None):
        self.widget = widget
        self.file_manager = file_manager
        self.callback = callback
        self.dnd_enabled = False
        
        # Setup drag-drop functionality
        self.setup_dragdrop()
    
    def setup_dragdrop(self):
        """Setup the most compatible drag-drop solution"""
        # Method 1: Try tkdnd if available (most reliable)
        if self.try_tkdnd():
            return
        
        # Method 2: Try Windows native if on Windows
        if platform.system() == "Windows" and self.try_windows_native():
            return
        
        # Method 3: Enhanced fallback with visual feedback
        self.setup_enhanced_fallback()
    
    def try_tkdnd(self):
        """Try to use tkdnd library if available"""
        try:
            # Check if tkdnd is available
            self.widget.tk.call('package', 'require', 'tkdnd')
            
            # Register as drop target
            self.widget.tk.call('tkdnd::drop_target', 'register', self.widget, 'DND_Files')
            
            # Bind events
            self.widget.bind('<<Drop:DND_Files>>', self.on_tkdnd_drop)
            self.widget.bind('<<DragEnter>>', self.on_drag_enter)
            self.widget.bind('<<DragLeave>>', self.on_drag_leave)
            
            self.dnd_enabled = True
            print("✓ tkdnd drag-drop enabled")
            return True
            
        except (tk.TclError, Exception) as e:
            print(f"tkdnd not available: {e}")
            return False
    
    def try_windows_native(self):
        """Try Windows-specific drag-drop using windnd"""
        try:
            # Try importing windnd (Windows-specific drag-drop)
            import windnd
            
            # Hook the widget for file drops
            windnd.hook_dropfiles(self.widget, func=self.on_windows_drop)
            
            self.dnd_enabled = True
            print("✓ Windows native drag-drop enabled")
            return True
            
        except ImportError:
            try:
                # Fallback: Try installing windnd dynamically
                import subprocess
                import sys
                subprocess.check_call([sys.executable, "-m", "pip", "install", "windnd"])
                
                # Try importing again
                import windnd
                windnd.hook_dropfiles(self.widget, func=self.on_windows_drop)
                
                self.dnd_enabled = True
                print("✓ Windows native drag-drop enabled (windnd installed)")
                return True
                
            except Exception as e:
                print(f"Windows native drag-drop failed: {e}")
                return False
        except Exception as e:
            print(f"Windows native drag-drop setup failed: {e}")
            return False
    
    def setup_enhanced_fallback(self):
        """Setup enhanced fallback with better visual feedback"""
        print("Setting up enhanced click-to-import fallback")
        
        # Configure the widget as a drop zone
        self.widget.configure(
            relief='ridge',
            bd=2,
            bg='#f0f0f0',
            cursor='hand2'
        )
        
        # Bind events
        self.widget.bind('<Button-1>', self.on_click_import)
        self.widget.bind('<Enter>', self.on_hover_enter)
        self.widget.bind('<Leave>', self.on_hover_leave)
        
        # Add instruction text if widget is a frame
        try:
            for child in self.widget.winfo_children():
                if isinstance(child, tk.Label):
                    child.configure(text="Click to Import Images\n(Drag-drop not available)")
                    break
        except:
            pass
    
    def on_tkdnd_drop(self, event):
        """Handle drop event from tkdnd"""
        try:
            # Get dropped files
            files = self.widget.tk.splitlist(event.data)
            self._process_dropped_files(files)
        except Exception as e:
            print(f"Error processing tkdnd drop: {e}")
    
    def on_windows_drop(self, files):
        """Handle drop event from Windows native"""
        try:
            print(f"Windows drop received: {files} (type: {type(files)})")
            if isinstance(files, (list, tuple)):
                self._process_dropped_files(files)
            elif isinstance(files, str):
                # Single file as string
                self._process_dropped_files([files])
            else:
                print(f"Unexpected drop data type: {type(files)}")
        except Exception as e:
            print(f"Error processing Windows drop: {e}")
            import traceback
            traceback.print_exc()
    
    def on_click_import(self, event):
        """Handle click to import files"""
        if self.callback:
            # Open file selection dialog
            file_paths = self.file_manager.select_files_dialog()
            if file_paths:
                imported = self.file_manager.import_multiple_files(file_paths)
                if imported:
                    self.callback(imported)
                    print(f"Imported {len(imported)} files via click")
    
    def on_hover_enter(self, event):
        """Handle mouse hover enter"""
        self.widget.configure(bg='#e6f3ff', relief='solid')
    
    def on_hover_leave(self, event):
        """Handle mouse hover leave"""
        self.widget.configure(bg='#f0f0f0', relief='ridge')
    
    def on_drag_enter(self, event):
        """Handle drag enter event"""
        self.widget.configure(bg='#d4edda', relief='solid')
    
    def on_drag_leave(self, event):
        """Handle drag leave event"""
        self.widget.configure(bg='#f0f0f0', relief='ridge')
    
    def _process_dropped_files(self, files):
        """Process the list of dropped files"""
        try:
            print(f"Processing {len(files)} dropped files: {files}")
            imported_files = []
            imported_folders = []
            
            for file_path in files:
                # Clean the file path - handle bytes from windnd
                if isinstance(file_path, bytes):
                    file_path = file_path.decode('utf-8')
                file_path = str(file_path).strip('"\'{}')
                print(f"Processing file: {file_path}")
                
                if os.path.isfile(file_path):
                    print(f"File exists: {file_path}")
                    if self.file_manager.is_image_file(file_path):
                        print(f"Valid image file: {file_path}")
                        if self.file_manager.import_single_file(file_path):
                            imported_files.append(file_path)
                            print(f"Successfully imported: {file_path}")
                    else:
                        print(f"Not an image file: {file_path}")
                elif os.path.isdir(file_path):
                    print(f"Processing directory: {file_path}")
                    folder_files = self.file_manager.import_folder(file_path, recursive=False)
                    imported_folders.extend(folder_files)
                    print(f"Imported {len(folder_files)} files from folder")
                else:
                    print(f"Path does not exist: {file_path}")
            
            # Call callback if provided
            all_imported = imported_files + imported_folders
            if self.callback and all_imported:
                self.callback(all_imported)
                print(f"✓ Successfully imported {len(all_imported)} files via drag-drop")
            elif not all_imported:
                print("No valid image files found in dropped items")
            else:
                print("No callback provided")
                
        except Exception as e:
            print(f"Error processing dropped files: {e}")
            import traceback
            traceback.print_exc()