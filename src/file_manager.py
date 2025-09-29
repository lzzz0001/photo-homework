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
    """Handles drag and drop functionality for file import with fallback support"""
    
    def __init__(self, widget, file_manager: FileManager, callback=None):
        self.widget = widget
        self.file_manager = file_manager
        self.callback = callback
        
        # Try to enable enhanced drag and drop, fall back to basic functionality
        try:
            # Try to use tkinter DND if available
            self.widget.drop_target_register('DND_FILES')
            self.widget.dnd_bind('<<Drop>>', self.on_drop)
            self.widget.dnd_bind('<<DragEnter>>', self.on_drag_enter)
            self.widget.dnd_bind('<<DragLeave>>', self.on_drag_leave)
            self.dnd_enabled = True
        except (AttributeError, Exception):
            # Fallback: Use basic tkinter events
            self.widget.bind('<Button-1>', self.on_click_fallback)
            self.dnd_enabled = False
            print("Enhanced drag-drop not available, using click fallback")
    
    def on_click_fallback(self, event):
        """Fallback: Open file dialog when drag area is clicked"""
        if self.callback:
            # Simulate file selection
            file_paths = self.file_manager.select_files_dialog()
            if file_paths:
                imported = self.file_manager.import_multiple_files(file_paths)
                self.callback(imported)
    
    def on_drag_enter(self, event):
        """Handle drag enter event"""
        if hasattr(self.widget, 'configure'):
            self.widget.configure(relief='sunken')
    
    def on_drag_leave(self, event):
        """Handle drag leave event"""
        if hasattr(self.widget, 'configure'):
            self.widget.configure(relief='raised')
    
    def on_drop(self, event):
        """Handle file drop event"""
        self.widget.configure(relief='raised')
        
        files = []
        # Parse dropped data
        if hasattr(event, 'data'):
            # Handle different data formats
            data = event.data
            if isinstance(data, str):
                # Split by spaces or newlines and clean up
                files = [f.strip('{}').strip('"').strip("'") for f in data.split()]
            elif isinstance(data, (list, tuple)):
                files = [str(f) for f in data]
        
        imported_files = []
        imported_folders = []
        
        for file_path in files:
            if os.path.isfile(file_path):
                if self.file_manager.import_single_file(file_path):
                    imported_files.append(file_path)
            elif os.path.isdir(file_path):
                folder_files = self.file_manager.import_folder(file_path, recursive=False)
                imported_folders.extend(folder_files)
        
        # Call callback if provided
        if self.callback:
            self.callback(imported_files + imported_folders)
        
        return 'copy'