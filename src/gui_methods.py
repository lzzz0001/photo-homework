"""
GUI Event Handlers and Methods for the Photo Watermark Application.
This module contains all the event handling and interaction methods.
"""

import tkinter as tk
from tkinter import messagebox, filedialog, colorchooser
import os
from PIL import Image, ImageTk
from typing import Optional, List

class WatermarkAppMethods:
    """Event handlers and methods for the main WatermarkApp class"""
    
    def load_last_template(self):
        """Load the last used template on startup"""
        try:
            last_config = self.template_manager.load_last_config()
            if last_config:
                self.apply_config_to_gui(last_config)
                self.update_config_from_gui()
        except Exception as e:
            print(f"Error loading last template: {e}")
    
    def apply_config_to_gui(self, config):
        """Apply a configuration to all GUI controls"""
        # Text watermark settings
        self.var_watermark_text.set(config.text)
        self.var_font_family.set(config.font_family)
        self.var_font_size.set(config.font_size)
        self.var_font_bold.set(config.font_bold)
        self.var_font_italic.set(config.font_italic)
        self.var_text_color.set(self.rgb_to_hex(config.text_color))
        self.var_opacity.set(config.opacity)
        self.var_rotation.set(config.rotation)
        
        # Position settings
        self.var_position.set(config.position.value)
        self.var_margin_x.set(config.margin_x)
        self.var_margin_y.set(config.margin_y)
        
        # Watermark type
        self.var_watermark_type.set(config.watermark_type.value)
        
        # Image watermark
        self.var_watermark_image_path.set(config.watermark_image_path)
        self.var_scale_factor.set(config.scale_factor)
        
        # Advanced settings
        self.var_stroke_width.set(config.stroke_width)
        self.var_stroke_color.set(self.rgb_to_hex(config.stroke_color))
        self.var_shadow_offset_x.set(config.shadow_offset[0])
        self.var_shadow_offset_y.set(config.shadow_offset[1])
        self.var_shadow_color.set(self.rgb_to_hex(config.shadow_color))
        
        # Update UI elements
        self.update_color_buttons()
        self.on_watermark_type_change()
    
    def update_config_from_gui(self):
        """Update the current configuration from GUI values"""
        from src.image_processor import WatermarkPosition, WatermarkType
        
        # Update configuration object
        self.current_config.watermark_type = WatermarkType(self.var_watermark_type.get())
        self.current_config.position = WatermarkPosition(self.var_position.get())
        self.current_config.opacity = self.var_opacity.get()
        self.current_config.rotation = self.var_rotation.get()
        
        # Text settings
        self.current_config.text = self.var_watermark_text.get()
        self.current_config.font_family = self.var_font_family.get()
        self.current_config.font_size = self.var_font_size.get()
        self.current_config.font_bold = self.var_font_bold.get()
        self.current_config.font_italic = self.var_font_italic.get()
        self.current_config.text_color = self.hex_to_rgb(self.var_text_color.get())
        
        # Position and margins
        self.current_config.margin_x = self.var_margin_x.get()
        self.current_config.margin_y = self.var_margin_y.get()
        
        # Image watermark
        self.current_config.watermark_image_path = self.var_watermark_image_path.get()
        self.current_config.scale_factor = self.var_scale_factor.get()
        
        # Advanced settings
        self.current_config.stroke_width = self.var_stroke_width.get()
        self.current_config.stroke_color = self.hex_to_rgb(self.var_stroke_color.get())
        self.current_config.shadow_offset = (self.var_shadow_offset_x.get(), self.var_shadow_offset_y.get())
        self.current_config.shadow_color = self.hex_to_rgb(self.var_shadow_color.get())
    
    # File operations
    def import_files(self):
        """Import image files using file dialog"""
        file_paths = self.file_manager.select_files_dialog(self.root)
        if file_paths:
            imported = self.file_manager.import_multiple_files(file_paths)
            self.update_file_list()
            self.update_file_count()
            if imported:
                self.current_image_index = len(self.file_manager.imported_files) - len(imported)
                self.load_current_image()
    
    def import_folder(self):
        """Import all images from a folder"""
        folder_path = self.file_manager.select_folder_dialog(self.root)
        if folder_path:
            imported = self.file_manager.import_folder(folder_path)
            self.update_file_list()
            self.update_file_count()
            if imported:
                self.current_image_index = 0
                self.load_current_image()
    
    def clear_files(self):
        """Clear all imported files"""
        if self.file_manager.imported_files:
            result = messagebox.askyesno("Clear Files", 
                                       "Are you sure you want to clear all imported files?")
            if result:
                self.file_manager.clear_all_files()
                self.update_file_list()
                self.update_file_count()
                self.clear_preview()
    
    def update_file_count(self):
        """Update the file count label"""
        count = len(self.file_manager.imported_files)
        self.file_count_label.config(text=f"Files imported: {count}")
    
    def update_file_list(self):
        """Update the thumbnail list of images"""
        # Clear existing thumbnails
        for widget in self.thumbnail_frame.winfo_children():
            widget.destroy()
        
        # Create thumbnails for each image
        for i, file_path in enumerate(self.file_manager.imported_files):
            self.create_thumbnail_widget(file_path, i)
        
        # Update canvas scroll region
        self.thumbnail_frame.update_idletasks()
        self.image_list_canvas.configure(scrollregion=self.image_list_canvas.bbox("all"))
    
    def create_thumbnail_widget(self, file_path: str, index: int):
        """Create a thumbnail widget for an image"""
        try:
            # Create thumbnail
            thumbnail = self.file_manager.create_thumbnail(file_path, (100, 100))
            if thumbnail:
                # Convert to PhotoImage
                photo = ImageTk.PhotoImage(thumbnail)
                
                # Create frame for thumbnail
                thumb_frame = ttk.Frame(self.thumbnail_frame, relief=tk.RAISED, borderwidth=1)
                thumb_frame.pack(side=tk.LEFT, padx=2, pady=2)
                
                # Create label with image
                thumb_label = tk.Label(thumb_frame, image=photo, cursor="hand2")
                thumb_label.pack()
                thumb_label.image = photo  # Keep reference
                
                # Create filename label
                filename = os.path.basename(file_path)
                if len(filename) > 15:
                    filename = filename[:12] + "..."
                name_label = tk.Label(thumb_frame, text=filename, font=("Arial", 8))
                name_label.pack()
                
                # Bind click event
                thumb_label.bind("<Button-1>", lambda e, idx=index: self.select_image(idx))
                name_label.bind("<Button-1>", lambda e, idx=index: self.select_image(idx))
                
                # Highlight current image
                if index == self.current_image_index:
                    thumb_frame.configure(relief=tk.SOLID, borderwidth=2)
        except Exception as e:
            print(f"Error creating thumbnail for {file_path}: {e}")
    
    def select_image(self, index: int):
        """Select an image by index"""
        if 0 <= index < len(self.file_manager.imported_files):
            self.current_image_index = index
            self.load_current_image()
            self.update_file_list()  # Refresh to update highlighting
    
    def load_current_image(self):
        """Load and display the current image with watermark"""
        if not self.file_manager.imported_files:
            self.clear_preview()
            return
        
        if self.current_image_index >= len(self.file_manager.imported_files):
            self.current_image_index = 0
        
        try:
            file_path = self.file_manager.imported_files[self.current_image_index]
            self.original_image = self.image_processor.load_image(file_path)
            
            if self.original_image:
                self.update_preview()
                self.no_image_label.place_forget()
            else:
                self.clear_preview()
        except Exception as e:
            print(f"Error loading image: {e}")
            self.clear_preview()
    
    def update_preview(self):
        """Update the preview with current watermark"""
        if not self.original_image:
            return
        
        try:
            # Update configuration from GUI
            self.update_config_from_gui()
            
            # Apply watermark
            watermarked_image = self.image_processor.apply_watermark(
                self.original_image, self.current_config
            )
            
            # Scale image for preview if too large
            display_image = self.scale_for_preview(watermarked_image)
            
            # Convert to PhotoImage
            self.preview_photo = ImageTk.PhotoImage(display_image)
            
            # Update canvas
            self.preview_canvas.delete("all")
            self.preview_canvas.create_image(0, 0, anchor=tk.NW, image=self.preview_photo)
            
            # Update scroll region
            self.preview_canvas.configure(scrollregion=self.preview_canvas.bbox("all"))
            
        except Exception as e:
            print(f"Error updating preview: {e}")
    
    def scale_for_preview(self, image: Image.Image, max_size: int = 800) -> Image.Image:
        """Scale image for preview display"""
        width, height = image.size
        
        if width <= max_size and height <= max_size:
            return image
        
        # Calculate scaling factor
        scale_factor = min(max_size / width, max_size / height)
        new_width = int(width * scale_factor)
        new_height = int(height * scale_factor)
        
        return image.resize((new_width, new_height), Image.Resampling.LANCZOS)
    
    def clear_preview(self):
        """Clear the preview area"""
        self.preview_canvas.delete("all")
        self.preview_photo = None
        self.original_image = None
        self.no_image_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
    
    # Watermark event handlers
    def on_watermark_type_change(self):
        """Handle watermark type change"""
        watermark_type = self.var_watermark_type.get()
        
        if watermark_type == "text":
            self.text_frame.pack(fill=tk.X, padx=5, pady=5)
            self.image_frame.pack_forget()
            self.advanced_frame.pack(fill=tk.X, padx=5, pady=5)
        else:
            self.text_frame.pack_forget()
            self.image_frame.pack(fill=tk.X, padx=5, pady=5)
            self.advanced_frame.pack_forget()
        
        self.update_preview()
    
    def on_text_change(self, event=None):
        """Handle text content change"""
        self.update_preview()
    
    def on_font_change(self, event=None):
        """Handle font family change"""
        self.update_preview()
    
    def on_font_size_change(self, event=None):
        """Handle font size change"""
        self.update_preview()
    
    def on_font_style_change(self):
        """Handle font style change"""
        self.update_preview()
    
    def on_scale_change(self, event=None):
        """Handle image watermark scale change"""
        self.update_preview()
    
    def on_opacity_change(self, value=None):
        """Handle opacity change"""
        self.update_preview()
    
    def on_rotation_change(self, value=None):
        """Handle rotation change"""
        self.update_preview()
    
    def on_margin_change(self, event=None):
        """Handle margin change"""
        self.update_preview()
    
    def on_stroke_change(self, event=None):
        """Handle stroke width change"""
        self.update_preview()
    
    def on_format_change(self, event=None):
        """Handle output format change"""
        format_type = self.var_output_format.get()
        if format_type == "JPEG":
            self.quality_frame.pack(fill=tk.X, pady=5)
        else:
            self.quality_frame.pack_forget()
    
    def on_config_change(self, *args):
        """Handle any configuration change"""
        self.update_preview()
    
    # Color choosers
    def choose_text_color(self):
        """Open color chooser for text color"""
        current_color = self.var_text_color.get()
        color = colorchooser.askcolor(color=current_color, title="Choose Text Color")
        if color[1]:  # color[1] is the hex value
            self.var_text_color.set(color[1])
            self.color_button.configure(bg=color[1])
            self.update_preview()
    
    def choose_stroke_color(self):
        """Open color chooser for stroke color"""
        current_color = self.var_stroke_color.get()
        color = colorchooser.askcolor(color=current_color, title="Choose Stroke Color")
        if color[1]:
            self.var_stroke_color.set(color[1])
            self.stroke_color_button.configure(bg=color[1])
            self.update_preview()
    
    def update_color_buttons(self):
        """Update color button appearances"""
        self.color_button.configure(bg=self.var_text_color.get())
        self.stroke_color_button.configure(bg=self.var_stroke_color.get())
    
    # Position methods
    def set_position(self, position):
        """Set watermark position"""
        self.var_position.set(position.value)
        self.current_config.position = position
        self.update_preview()
    
    # Watermark image selection
    def select_watermark_image(self):
        """Select watermark image file"""
        file_types = [
            ("PNG files", "*.png"),
            ("All Supported Images", "*.jpg;*.jpeg;*.png;*.bmp"),
            ("All files", "*.*")
        ]
        
        file_path = filedialog.askopenfilename(
            parent=self.root,
            title="Select Watermark Image",
            filetypes=file_types
        )
        
        if file_path:
            self.var_watermark_image_path.set(file_path)
            filename = os.path.basename(file_path)
            if len(filename) > 30:
                filename = filename[:27] + "..."
            self.watermark_image_label.config(text=filename, foreground='black')
            self.update_preview()
    
    # Export methods
    def select_output_directory(self):
        """Select output directory for exports"""
        folder_path = self.file_manager.select_output_directory(self.root)
        if folder_path:
            # Truncate long paths for display
            display_path = folder_path
            if len(display_path) > 40:
                display_path = "..." + display_path[-37:]
            self.output_dir_label.config(text=display_path, foreground='black')
    
    def export_current_image(self):
        """Export the currently selected image with watermark"""
        if not self.original_image:
            messagebox.showwarning("No Image", "Please select an image to export.")
            return
        
        if not self.var_output_directory.get():
            self.select_output_directory()
            if not self.var_output_directory.get():
                return
        
        try:
            # Get current image path
            current_file = self.file_manager.imported_files[self.current_image_index]
            
            # Validate output directory
            valid, message = self.file_manager.validate_output_directory(
                self.file_manager.output_directory
            )
            if not valid:
                messagebox.showerror("Invalid Output Directory", message)
                return
            
            # Update configuration
            self.update_config_from_gui()
            
            # Apply watermark
            watermarked_image = self.image_processor.apply_watermark(
                self.original_image, self.current_config
            )
            
            # Generate output filename
            output_filename = self.file_manager.generate_output_filename(
                current_file,
                self.var_filename_prefix.get(),
                self.var_filename_suffix.get(),
                self.var_output_format.get()
            )
            
            output_path = os.path.join(self.file_manager.output_directory, output_filename)
            
            # Save image
            success = self.image_processor.save_image(
                watermarked_image,
                output_path,
                self.var_output_format.get(),
                self.var_jpeg_quality.get()
            )
            
            if success:
                messagebox.showinfo("Export Successful", 
                                  f"Image exported successfully to:\n{output_path}")
            else:
                messagebox.showerror("Export Failed", "Failed to export image.")
                
        except Exception as e:
            messagebox.showerror("Export Error", f"Error exporting image:\n{e}")
    
    def export_all_images(self):
        """Export all imported images with watermarks"""
        if not self.file_manager.imported_files:
            messagebox.showwarning("No Images", "Please import images to export.")
            return
        
        if not self.var_output_directory.get():
            self.select_output_directory()
            if not self.var_output_directory.get():
                return
        
        # Validate output directory
        valid, message = self.file_manager.validate_output_directory(
            self.file_manager.output_directory
        )
        if not valid:
            messagebox.showerror("Invalid Output Directory", message)
            return
        
        # Check for file conflicts
        conflicts = self.file_manager.check_file_conflicts(
            self.file_manager.output_directory,
            self.file_manager.imported_files,
            self.var_filename_prefix.get(),
            self.var_filename_suffix.get(),
            self.var_output_format.get()
        )
        
        if conflicts:
            result = messagebox.askyesno(
                "File Conflicts",
                f"The following files will be overwritten:\n" +
                "\n".join(conflicts[:5]) +
                (f"\n... and {len(conflicts)-5} more" if len(conflicts) > 5 else "") +
                "\n\nContinue with export?"
            )
            if not result:
                return
        
        try:
            # Update configuration
            self.update_config_from_gui()
            
            # Process all images
            results = self.image_processor.batch_process(
                self.file_manager.imported_files,
                self.current_config,
                self.file_manager.output_directory,
                self.var_output_format.get(),
                self.var_jpeg_quality.get(),
                self.var_filename_prefix.get(),
                self.var_filename_suffix.get()
            )
            
            if results:
                messagebox.showinfo("Export Successful", 
                                  f"Successfully exported {len(results)} images to:\n"
                                  f"{self.file_manager.output_directory}")
            else:
                messagebox.showerror("Export Failed", "Failed to export images.")
                
        except Exception as e:
            messagebox.showerror("Export Error", f"Error exporting images:\n{e}")
    
    # Template methods
    def save_template(self):
        """Save current configuration as template"""
        name = tk.simpledialog.askstring("Save Template", "Enter template name:")
        if name:
            name = name.strip()
            if name:
                self.update_config_from_gui()
                
                description = tk.simpledialog.askstring(
                    "Template Description", 
                    "Enter template description (optional):"
                ) or ""
                
                success = self.template_manager.save_template(name, self.current_config, description)
                if success:
                    self.refresh_template_list()
                    messagebox.showinfo("Template Saved", f"Template '{name}' saved successfully.")
                else:
                    messagebox.showerror("Save Failed", "Failed to save template.")
    
    def load_template(self):
        """Load selected template"""
        selection = self.template_listbox.curselection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a template to load.")
            return
        
        template_name = self.template_listbox.get(selection[0])
        config = self.template_manager.load_template(template_name)
        
        if config:
            self.apply_config_to_gui(config)
            self.current_config = config
            self.update_preview()
            messagebox.showinfo("Template Loaded", f"Template '{template_name}' loaded successfully.")
        else:
            messagebox.showerror("Load Failed", "Failed to load template.")
    
    def delete_template(self):
        """Delete selected template"""
        selection = self.template_listbox.curselection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a template to delete.")
            return
        
        template_name = self.template_listbox.get(selection[0])
        result = messagebox.askyesno("Delete Template", 
                                   f"Are you sure you want to delete template '{template_name}'?")
        
        if result:
            success = self.template_manager.delete_template(template_name)
            if success:
                self.refresh_template_list()
                messagebox.showinfo("Template Deleted", f"Template '{template_name}' deleted successfully.")
            else:
                messagebox.showerror("Delete Failed", "Failed to delete template.")
    
    def refresh_template_list(self):
        """Refresh the template list"""
        self.template_listbox.delete(0, tk.END)
        templates = self.template_manager.get_template_list()
        for template in templates:
            self.template_listbox.insert(tk.END, template)
    
    # Canvas event handlers
    def on_thumbnail_frame_configure(self, event):
        """Handle thumbnail frame configuration changes"""
        self.image_list_canvas.configure(scrollregion=self.image_list_canvas.bbox("all"))
    
    # Application lifecycle
    def on_closing(self):
        """Handle application closing"""
        try:
            # Save last configuration
            self.update_config_from_gui()
            self.template_manager.save_last_config(self.current_config)
        except:
            pass  # Don't prevent closing if save fails
        
        self.root.destroy()