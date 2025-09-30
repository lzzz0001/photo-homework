"""
Main GUI window for the Photo Watermark Application.
Provides the primary interface with all watermarking controls and preview functionality.
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog, colorchooser, simpledialog
import os
import sys
from PIL import Image, ImageTk
from typing import Optional, List, Dict, Any

# Add src directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__)))

from image_processor import ImageProcessor, WatermarkConfig, WatermarkPosition, WatermarkType
from file_manager import FileManager, DragDropHandler
from template_manager import TemplateManager
import tkinter.simpledialog

class WatermarkApp:
    """Main application class for the Photo Watermark tool"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Photo Watermark Application")
        self.root.geometry("1200x800")
        self.root.minsize(1000, 600)
        
        # Initialize core components
        self.image_processor = ImageProcessor()
        self.file_manager = FileManager()
        self.template_manager = TemplateManager()
        
        # Current state
        self.current_config = WatermarkConfig()
        self.current_image_index = 0
        self.preview_image = None
        self.original_image = None
        
        # GUI variables
        self.setup_gui_variables()
        
        # Create GUI
        self.create_widgets()
        self.setup_layout()
        self.bind_events()
        
        # Setup drag and drop functionality
        self.setup_drag_drop()
        
        # Setup manual watermark positioning
        self.setup_manual_positioning()
        
        # Setup tooltip functionality
        self.setup_tooltips()
        
        # Load default template if available
        self.load_last_template()
    
    def setup_gui_variables(self):
        """Initialize all GUI variables"""
        # Text watermark variables
        self.var_watermark_text = tk.StringVar(value=self.current_config.text)
        self.var_font_family = tk.StringVar(value=self.current_config.font_family)
        self.var_font_size = tk.IntVar(value=self.current_config.font_size)
        self.var_font_bold = tk.BooleanVar(value=self.current_config.font_bold)
        self.var_font_italic = tk.BooleanVar(value=self.current_config.font_italic)
        self.var_text_color = tk.StringVar(value=self.rgb_to_hex(self.current_config.text_color))
        self.var_opacity = tk.IntVar(value=self.current_config.opacity)
        self.var_rotation = tk.IntVar(value=self.current_config.rotation)
        
        # Position variables
        self.var_position = tk.StringVar(value=self.current_config.position.value)
        self.var_margin_x = tk.IntVar(value=self.current_config.margin_x)
        self.var_margin_y = tk.IntVar(value=self.current_config.margin_y)
        
        # Watermark type
        self.var_watermark_type = tk.StringVar(value=self.current_config.watermark_type.value)
        
        # Image watermark variables
        self.var_watermark_image_path = tk.StringVar(value=self.current_config.watermark_image_path)
        self.var_scale_factor = tk.DoubleVar(value=self.current_config.scale_factor)
        
        # Export variables
        self.var_output_format = tk.StringVar(value="JPEG")
        self.var_jpeg_quality = tk.IntVar(value=95)
        self.var_filename_prefix = tk.StringVar(value="")
        self.var_filename_suffix = tk.StringVar(value="_watermarked")
        self.var_output_directory = tk.StringVar(value="")
        
        # Advanced features
        self.var_stroke_width = tk.IntVar(value=self.current_config.stroke_width)
        self.var_stroke_color = tk.StringVar(value=self.rgb_to_hex(self.current_config.stroke_color))
        self.var_shadow_offset_x = tk.IntVar(value=self.current_config.shadow_offset[0])
        self.var_shadow_offset_y = tk.IntVar(value=self.current_config.shadow_offset[1])
        self.var_shadow_color = tk.StringVar(value=self.rgb_to_hex(self.current_config.shadow_color))
    
    def rgb_to_hex(self, rgb_tuple):
        """Convert RGB tuple to hex string"""
        return f"#{rgb_tuple[0]:02x}{rgb_tuple[1]:02x}{rgb_tuple[2]:02x}"
    
    def hex_to_rgb(self, hex_string):
        """Convert hex string to RGB tuple"""
        hex_string = hex_string.lstrip('#')
        return tuple(int(hex_string[i:i+2], 16) for i in (0, 2, 4))
    
    def create_widgets(self):
        """Create all GUI widgets"""
        # Create main frame
        self.main_frame = ttk.Frame(self.root)
        
        # Create paned window for resizable layout
        self.paned_window = ttk.PanedWindow(self.main_frame, orient=tk.HORIZONTAL)
        
        # Left panel for controls
        self.left_panel = ttk.Frame(self.paned_window, width=350)
        self.paned_window.add(self.left_panel, weight=0)
        
        # Right panel for preview and image list
        self.right_panel = ttk.Frame(self.paned_window)
        self.paned_window.add(self.right_panel, weight=1)
        
        # Create left panel widgets
        self.create_left_panel()
        
        # Create right panel widgets
        self.create_right_panel()
    
    def create_left_panel(self):
        """Create the left control panel"""
        # Create notebook for organized tabs
        self.control_notebook = ttk.Notebook(self.left_panel)
        
        # File Operations Tab
        self.create_file_tab()
        
        # Watermark Settings Tab
        self.create_watermark_tab()
        
        # Position & Style Tab
        self.create_position_tab()
        
        # Export Settings Tab
        self.create_export_tab()
        
        # Template Management Tab
        self.create_template_tab()
    
    def create_file_tab(self):
        """Create file operations tab"""
        file_frame = ttk.Frame(self.control_notebook)
        self.control_notebook.add(file_frame, text="Files")
        
        # Import section
        import_frame = ttk.LabelFrame(file_frame, text="Import Images", padding=10)
        import_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(import_frame, text="Select Files", 
                  command=self.import_files).pack(fill=tk.X, pady=2)
        ttk.Button(import_frame, text="Select Folder", 
                  command=self.import_folder).pack(fill=tk.X, pady=2)
        ttk.Button(import_frame, text="Clear All", 
                  command=self.clear_files).pack(fill=tk.X, pady=2)
        
        # Drag and drop area
        self.drop_frame = tk.Frame(import_frame, height=80, bg='lightgray', relief='sunken', bd=2)
        self.drop_frame.pack(fill=tk.X, pady=10)
        self.drop_frame.pack_propagate(False)
        
        self.drop_label = tk.Label(self.drop_frame, text="Drag & Drop Images Here\nor Click to Browse", 
                             bg='lightgray', fg='darkblue', font=('Arial', 10))
        self.drop_label.pack(expand=True)
        
        # File count label
        self.file_count_label = ttk.Label(import_frame, text="Files imported: 0")
        self.file_count_label.pack(pady=2)
    
    def create_watermark_tab(self):
        """Create watermark settings tab"""
        watermark_frame = ttk.Frame(self.control_notebook)
        self.control_notebook.add(watermark_frame, text="Watermark")
        
        # Watermark type selection
        type_frame = ttk.LabelFrame(watermark_frame, text="Watermark Type", padding=5)
        type_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Radiobutton(type_frame, text="Text Watermark", variable=self.var_watermark_type,
                       value="text", command=self.on_watermark_type_change).pack(anchor=tk.W)
        ttk.Radiobutton(type_frame, text="Image Watermark", variable=self.var_watermark_type,
                       value="image", command=self.on_watermark_type_change).pack(anchor=tk.W)
        
        # Text watermark settings
        self.text_frame = ttk.LabelFrame(watermark_frame, text="Text Settings", padding=5)
        self.text_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Text content
        ttk.Label(self.text_frame, text="Text:").pack(anchor=tk.W)
        self.text_entry = ttk.Entry(self.text_frame, textvariable=self.var_watermark_text)
        self.text_entry.pack(fill=tk.X, pady=2)
        self.text_entry.bind('<KeyRelease>', self.on_text_change)
        
        # Font settings
        font_frame = ttk.Frame(self.text_frame)
        font_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(font_frame, text="Font:").pack(anchor=tk.W)
        self.font_combo = ttk.Combobox(font_frame, textvariable=self.var_font_family,
                                      values=["Arial", "Times New Roman", "Calibri", "Verdana"])
        self.font_combo.pack(fill=tk.X, pady=2)
        self.font_combo.bind('<<ComboboxSelected>>', self.on_font_change)
        
        size_frame = ttk.Frame(font_frame)
        size_frame.pack(fill=tk.X, pady=2)
        ttk.Label(size_frame, text="Size:").pack(side=tk.LEFT)
        size_spin = ttk.Spinbox(size_frame, from_=8, to=200, textvariable=self.var_font_size,
                               width=10, command=self.on_font_size_change)
        size_spin.pack(side=tk.RIGHT)
        size_spin.bind('<KeyRelease>', self.on_font_size_change)
        
        # Font style
        style_frame = ttk.Frame(self.text_frame)
        style_frame.pack(fill=tk.X, pady=2)
        ttk.Checkbutton(style_frame, text="Bold", variable=self.var_font_bold,
                       command=self.on_font_style_change).pack(side=tk.LEFT)
        ttk.Checkbutton(style_frame, text="Italic", variable=self.var_font_italic,
                       command=self.on_font_style_change).pack(side=tk.LEFT)
        
        # Color selection
        color_frame = ttk.Frame(self.text_frame)
        color_frame.pack(fill=tk.X, pady=5)
        ttk.Label(color_frame, text="Text Color:").pack(side=tk.LEFT)
        self.color_button = tk.Button(color_frame, width=3, height=1,
                                     bg=self.var_text_color.get(),
                                     command=self.choose_text_color)
        self.color_button.pack(side=tk.RIGHT)
        
        # Image watermark settings
        self.image_frame = ttk.LabelFrame(watermark_frame, text="Image Settings", padding=5)
        self.image_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(self.image_frame, text="Select Watermark Image",
                  command=self.select_watermark_image).pack(fill=tk.X, pady=2)
        
        self.watermark_image_label = ttk.Label(self.image_frame, text="No image selected",
                                              foreground='gray')
        self.watermark_image_label.pack(fill=tk.X, pady=2)
        
        # Scale factor
        scale_frame = ttk.Frame(self.image_frame)
        scale_frame.pack(fill=tk.X, pady=5)
        ttk.Label(scale_frame, text="Scale:").pack(side=tk.LEFT)
        scale_spin = ttk.Spinbox(scale_frame, from_=0.1, to=5.0, increment=0.1,
                                textvariable=self.var_scale_factor, width=10,
                                command=self.on_scale_change)
        scale_spin.pack(side=tk.RIGHT)
        scale_spin.bind('<KeyRelease>', self.on_scale_change)
        
        # Initially hide image frame
        self.image_frame.pack_forget()
    
    def create_position_tab(self):
        """Create position and style settings tab"""
        position_frame = ttk.Frame(self.control_notebook)
        self.control_notebook.add(position_frame, text="Position & Style")
        
        # Position settings
        pos_frame = ttk.LabelFrame(position_frame, text="Position", padding=5)
        pos_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Position grid (3x3)
        grid_frame = ttk.Frame(pos_frame)
        grid_frame.pack(pady=5)
        
        positions = [
            ("↖", WatermarkPosition.TOP_LEFT), ("↑", WatermarkPosition.TOP_CENTER), ("↗", WatermarkPosition.TOP_RIGHT),
            ("←", WatermarkPosition.CENTER_LEFT), ("●", WatermarkPosition.CENTER), ("→", WatermarkPosition.CENTER_RIGHT),
            ("↙", WatermarkPosition.BOTTOM_LEFT), ("↓", WatermarkPosition.BOTTOM_CENTER), ("↘", WatermarkPosition.BOTTOM_RIGHT)
        ]
        
        for i, (symbol, pos) in enumerate(positions):
            row, col = divmod(i, 3)
            btn = ttk.Button(grid_frame, text=symbol, width=3,
                           command=lambda p=pos: self.set_position(p))
            btn.grid(row=row, column=col, padx=1, pady=1)
        
        # Margin settings
        margin_frame = ttk.Frame(pos_frame)
        margin_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(margin_frame, text="Margins:").pack(anchor=tk.W)
        
        margin_x_frame = ttk.Frame(margin_frame)
        margin_x_frame.pack(fill=tk.X, pady=2)
        ttk.Label(margin_x_frame, text="X:").pack(side=tk.LEFT)
        margin_x_spin = ttk.Spinbox(margin_x_frame, from_=0, to=200,
                                   textvariable=self.var_margin_x, width=10,
                                   command=self.on_margin_change)
        margin_x_spin.pack(side=tk.RIGHT)
        margin_x_spin.bind('<KeyRelease>', self.on_margin_change)
        
        margin_y_frame = ttk.Frame(margin_frame)
        margin_y_frame.pack(fill=tk.X, pady=2)
        ttk.Label(margin_y_frame, text="Y:").pack(side=tk.LEFT)
        margin_y_spin = ttk.Spinbox(margin_y_frame, from_=0, to=200,
                                   textvariable=self.var_margin_y, width=10,
                                   command=self.on_margin_change)
        margin_y_spin.pack(side=tk.RIGHT)
        margin_y_spin.bind('<KeyRelease>', self.on_margin_change)
        
        # Opacity and rotation
        style_frame = ttk.LabelFrame(position_frame, text="Style", padding=5)
        style_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Opacity
        opacity_frame = ttk.Frame(style_frame)
        opacity_frame.pack(fill=tk.X, pady=2)
        ttk.Label(opacity_frame, text="Opacity:").pack(side=tk.LEFT)
        self.opacity_scale = ttk.Scale(opacity_frame, from_=0, to=100, orient=tk.HORIZONTAL,
                                      variable=self.var_opacity, command=self.on_opacity_change)
        self.opacity_scale.pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=(10, 0))
        
        # Rotation
        rotation_frame = ttk.Frame(style_frame)
        rotation_frame.pack(fill=tk.X, pady=2)
        ttk.Label(rotation_frame, text="Rotation:").pack(side=tk.LEFT)
        self.rotation_scale = ttk.Scale(rotation_frame, from_=-180, to=180, orient=tk.HORIZONTAL,
                                       variable=self.var_rotation, command=self.on_rotation_change)
        self.rotation_scale.pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=(10, 0))
        
        # Advanced text effects
        self.advanced_frame = ttk.LabelFrame(position_frame, text="Advanced Effects", padding=5)
        self.advanced_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Stroke settings
        stroke_frame = ttk.Frame(self.advanced_frame)
        stroke_frame.pack(fill=tk.X, pady=2)
        ttk.Label(stroke_frame, text="Stroke Width:").pack(side=tk.LEFT)
        stroke_spin = ttk.Spinbox(stroke_frame, from_=0, to=10,
                                 textvariable=self.var_stroke_width, width=10,
                                 command=self.on_stroke_change)
        stroke_spin.pack(side=tk.RIGHT)
        stroke_spin.bind('<KeyRelease>', self.on_stroke_change)
        
        stroke_color_frame = ttk.Frame(self.advanced_frame)
        stroke_color_frame.pack(fill=tk.X, pady=2)
        ttk.Label(stroke_color_frame, text="Stroke Color:").pack(side=tk.LEFT)
        self.stroke_color_button = tk.Button(stroke_color_frame, width=3, height=1,
                                            bg=self.var_stroke_color.get(),
                                            command=self.choose_stroke_color)
        self.stroke_color_button.pack(side=tk.RIGHT)
    
    def create_export_tab(self):
        """Create export settings tab"""
        export_frame = ttk.Frame(self.control_notebook)
        self.control_notebook.add(export_frame, text="Export")
        
        # Output directory
        dir_frame = ttk.LabelFrame(export_frame, text="Output Directory", padding=5)
        dir_frame.pack(fill=tk.X, padx=5, pady=5)
        
        dir_select_frame = ttk.Frame(dir_frame)
        dir_select_frame.pack(fill=tk.X, pady=2)
        ttk.Button(dir_select_frame, text="Select Folder",
                  command=self.select_output_directory).pack(side=tk.LEFT)
        
        self.output_dir_label = ttk.Label(dir_frame, text="No directory selected",
                                         foreground='gray')
        self.output_dir_label.pack(fill=tk.X, pady=2)
        
        # Format settings
        format_frame = ttk.LabelFrame(export_frame, text="Format Settings", padding=5)
        format_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(format_frame, text="Output Format:").pack(anchor=tk.W)
        format_combo = ttk.Combobox(format_frame, textvariable=self.var_output_format,
                                   values=["JPEG", "PNG"], state="readonly")
        format_combo.pack(fill=tk.X, pady=2)
        format_combo.bind('<<ComboboxSelected>>', self.on_format_change)
        
        # JPEG quality (only shown for JPEG)
        self.quality_frame = ttk.Frame(format_frame)
        self.quality_frame.pack(fill=tk.X, pady=5)
        ttk.Label(self.quality_frame, text="JPEG Quality:").pack(side=tk.LEFT)
        self.quality_scale = ttk.Scale(self.quality_frame, from_=1, to=100, orient=tk.HORIZONTAL,
                                      variable=self.var_jpeg_quality)
        self.quality_scale.pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=(10, 0))
        
        # Filename settings
        filename_frame = ttk.LabelFrame(export_frame, text="Filename Settings", padding=5)
        filename_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(filename_frame, text="Prefix:").pack(anchor=tk.W)
        ttk.Entry(filename_frame, textvariable=self.var_filename_prefix).pack(fill=tk.X, pady=2)
        
        ttk.Label(filename_frame, text="Suffix:").pack(anchor=tk.W)
        ttk.Entry(filename_frame, textvariable=self.var_filename_suffix).pack(fill=tk.X, pady=2)
        
        # Export buttons
        export_btn_frame = ttk.Frame(export_frame)
        export_btn_frame.pack(fill=tk.X, padx=5, pady=10)
        
        ttk.Button(export_btn_frame, text="Export Current Image",
                  command=self.export_current_image).pack(fill=tk.X, pady=2)
        ttk.Button(export_btn_frame, text="Export All Images",
                  command=self.export_all_images).pack(fill=tk.X, pady=2)
    
    def create_template_tab(self):
        """Create template management tab"""
        template_frame = ttk.Frame(self.control_notebook)
        self.control_notebook.add(template_frame, text="Templates")
        
        # Template management
        mgmt_frame = ttk.LabelFrame(template_frame, text="Template Management", padding=5)
        mgmt_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(mgmt_frame, text="Save Current as Template",
                  command=self.save_template).pack(fill=tk.X, pady=2)
        
        # Template list
        list_frame = ttk.LabelFrame(template_frame, text="Saved Templates", padding=5)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Template listbox with scrollbar
        listbox_frame = ttk.Frame(list_frame)
        listbox_frame.pack(fill=tk.BOTH, expand=True)
        
        self.template_listbox = tk.Listbox(listbox_frame)
        template_scrollbar = ttk.Scrollbar(listbox_frame, orient=tk.VERTICAL,
                                          command=self.template_listbox.yview)
        self.template_listbox.configure(yscrollcommand=template_scrollbar.set)
        
        self.template_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        template_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Template action buttons
        template_btn_frame = ttk.Frame(list_frame)
        template_btn_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(template_btn_frame, text="Load Template",
                  command=self.load_template).pack(side=tk.LEFT, padx=2)
        ttk.Button(template_btn_frame, text="Delete Template",
                  command=self.delete_template).pack(side=tk.LEFT, padx=2)
        
        # Load templates
        self.refresh_template_list()
    
    def create_right_panel(self):
        """Create the right panel with preview and image list"""
        # Create vertical paned window
        self.right_paned = ttk.PanedWindow(self.right_panel, orient=tk.VERTICAL)
        self.right_paned.pack(fill=tk.BOTH, expand=True)
        
        # Preview area
        self.preview_frame = ttk.LabelFrame(self.right_paned, text="Preview", padding=5)
        self.right_paned.add(self.preview_frame, weight=3)
        
        # Create canvas for preview with scrollbars
        self.create_preview_canvas()
        
        # Image list area
        self.image_list_frame = ttk.LabelFrame(self.right_paned, text="Image List", padding=5)
        self.right_paned.add(self.image_list_frame, weight=1)
        
        # Create image list
        self.create_image_list()
    
    def create_preview_canvas(self):
        """Create preview canvas with scrollbars"""
        canvas_frame = ttk.Frame(self.preview_frame)
        canvas_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create canvas with scrollbars
        self.preview_canvas = tk.Canvas(canvas_frame, bg='white')
        
        h_scrollbar = ttk.Scrollbar(canvas_frame, orient=tk.HORIZONTAL,
                                   command=self.preview_canvas.xview)
        v_scrollbar = ttk.Scrollbar(canvas_frame, orient=tk.VERTICAL,
                                   command=self.preview_canvas.yview)
        
        self.preview_canvas.configure(xscrollcommand=h_scrollbar.set,
                                     yscrollcommand=v_scrollbar.set)
        
        # Grid layout
        self.preview_canvas.grid(row=0, column=0, sticky="nsew")
        h_scrollbar.grid(row=1, column=0, sticky="ew")
        v_scrollbar.grid(row=0, column=1, sticky="ns")
        
        canvas_frame.grid_columnconfigure(0, weight=1)
        canvas_frame.grid_rowconfigure(0, weight=1)
        
        # No image label
        self.no_image_label = ttk.Label(self.preview_frame, text="No image selected",
                                       foreground='gray')
        self.no_image_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
    
    def create_image_list(self):
        """Create image list with thumbnails"""
        list_canvas_frame = ttk.Frame(self.image_list_frame)
        list_canvas_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create horizontal scrollable frame for thumbnails
        self.image_list_canvas = tk.Canvas(list_canvas_frame, height=120)
        list_h_scrollbar = ttk.Scrollbar(list_canvas_frame, orient=tk.HORIZONTAL,
                                        command=self.image_list_canvas.xview)
        
        self.image_list_canvas.configure(xscrollcommand=list_h_scrollbar.set)
        
        self.image_list_canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        list_h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Frame inside canvas for thumbnails
        self.thumbnail_frame = ttk.Frame(self.image_list_canvas)
        self.image_list_canvas.create_window((0, 0), window=self.thumbnail_frame, anchor=tk.NW)
        
        # Bind canvas resize
        self.thumbnail_frame.bind('<Configure>', self.on_thumbnail_frame_configure)
    
    def setup_layout(self):
        """Setup the main layout"""
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.paned_window.pack(fill=tk.BOTH, expand=True)
        self.control_notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
    
    def bind_events(self):
        """Bind events and shortcuts"""
        # Window events
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Keyboard shortcuts
        self.root.bind('<Control-o>', lambda e: self.import_files())
        self.root.bind('<Control-s>', lambda e: self.save_template())
        self.root.bind('<Control-e>', lambda e: self.export_all_images())
        
        # Variable traces for real-time updates
        self.var_watermark_text.trace('w', self.on_config_change)
        self.var_opacity.trace('w', self.on_config_change)
        self.var_rotation.trace('w', self.on_config_change)
    
    def setup_tooltips(self):
        """Setup tooltip functionality"""
        self.tooltips = {}
    
    def add_tooltip(self, widget, text):
        """Add tooltip to a widget"""
        def on_enter(event):
            self.show_tooltip(widget, text)
        
        def on_leave(event):
            self.hide_tooltip()
        
        widget.bind("<Enter>", on_enter)
        widget.bind("<Leave>", on_leave)
    
    def format_filename_for_display(self, filename, max_length=30):
        """Format filename for display, showing beginning and end for long names"""
        if len(filename) <= max_length:
            return filename
        
        # For very long filenames, show start and end with "..." in middle
        half_length = (max_length - 3) // 2
        start = filename[:half_length]
        end = filename[-half_length:] if len(filename) > half_length else filename
        return f"{start}...{end}"
    
    def show_tooltip(self, widget, text):
        """Show tooltip with full text"""
        # Get widget position
        x, y = widget.winfo_rootx(), widget.winfo_rooty()
        
        # Create tooltip window if it doesn't exist
        if not hasattr(self, '_tooltip_window') or not self._tooltip_window:
            self._tooltip_window = tk.Toplevel()
            self._tooltip_window.wm_overrideredirect(True)
            self._tooltip_window.configure(bg='yellow')
            
            self._tooltip_label = tk.Label(
                self._tooltip_window,
                text=text,
                bg='yellow',
                fg='black',
                font=('Arial', 8),
                padx=5,
                pady=2
            )
            self._tooltip_label.pack()
        else:
            self._tooltip_label.configure(text=text)
            self._tooltip_window.configure(bg='yellow')
            self._tooltip_label.configure(bg='yellow', fg='black')
        
        # Position tooltip near the widget
        self._tooltip_window.wm_geometry(f"+{x}+{y-30}")
        self._tooltip_window.deiconify()
    
    def hide_tooltip(self):
        """Hide tooltip"""
        if hasattr(self, '_tooltip_window') and self._tooltip_window:
            self._tooltip_window.withdraw()
    
    def setup_drag_drop(self):
        """Setup drag and drop functionality"""
        try:
            # Create drag drop handler for the drop frame
            self.drag_drop_handler = DragDropHandler(
                self.drop_frame, 
                self.file_manager, 
                callback=self.on_files_dropped
            )
            
            # Update label based on drag-drop capability
            if hasattr(self.drag_drop_handler, 'dnd_enabled') and self.drag_drop_handler.dnd_enabled:
                self.drop_label.config(text="✓ Drag & Drop Images Here\n(Native drag-drop enabled)", 
                                     fg='darkgreen')
            else:
                self.drop_label.config(text="Click to Import Images\n(Drag-drop fallback mode)", 
                                     fg='darkorange')
                
        except Exception as e:
            print(f"Warning: Drag-drop functionality not available: {e}")
            # Create fallback simple drag-drop for standard tkinter
            self.drop_frame.bind("<Button-1>", lambda e: self.import_files())
            self.drop_label.config(text="Click to Import Images\n(Fallback mode)", fg='darkred')
    
    def on_files_dropped(self, file_paths):
        """Handle files dropped into the application"""
        if file_paths:
            self.update_file_list()
            self.update_file_count()
            # Select the first newly imported image
            if self.file_manager.imported_files:
                self.current_image_index = max(0, len(self.file_manager.imported_files) - len(file_paths))
                self.load_current_image()
    
    def setup_manual_positioning(self):
        """Setup manual watermark positioning with mouse drag"""
        # Bind mouse events to preview canvas for watermark dragging
        self.preview_canvas.bind("<Button-1>", self.on_preview_click)
        self.preview_canvas.bind("<B1-Motion>", self.on_preview_drag)
        self.preview_canvas.bind("<ButtonRelease-1>", self.on_preview_release)
        self.dragging_watermark = False
        self.drag_start_x = 0
        self.drag_start_y = 0
    
    def on_preview_click(self, event):
        """Handle mouse click on preview canvas"""
        if self.original_image:
            self.dragging_watermark = True
            self.drag_start_x = event.x
            self.drag_start_y = event.y
            # Set position to custom and update coordinates
            self.var_position.set(WatermarkPosition.CUSTOM.value)
            self.current_config.position = WatermarkPosition.CUSTOM
    
    def on_preview_drag(self, event):
        """Handle mouse drag on preview canvas"""
        if self.dragging_watermark and self.original_image:
            # Calculate new position relative to image
            self.current_config.custom_x = event.x
            self.current_config.custom_y = event.y
            self.update_preview()
    
    def on_preview_release(self, event):
        """Handle mouse release on preview canvas"""
        self.dragging_watermark = False
    
    # File operations methods
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
        # Update configuration object
        self.current_config.watermark_type = WatermarkType(self.var_watermark_type.get())
        self.current_config.position = WatermarkPosition(self.var_position.get())
        self.current_config.opacity = self.var_opacity.get()
        self.current_config.rotation = self.var_rotation.get()
        
        # Text settings
        text_color_rgb = self.hex_to_rgb(self.var_text_color.get())
        self.current_config.text_color = (text_color_rgb[0], text_color_rgb[1], text_color_rgb[2])
        self.current_config.text = self.var_watermark_text.get()
        self.current_config.font_family = self.var_font_family.get()
        self.current_config.font_size = self.var_font_size.get()
        self.current_config.font_bold = self.var_font_bold.get()
        self.current_config.font_italic = self.var_font_italic.get()
        
        # Position and margins
        self.current_config.margin_x = self.var_margin_x.get()
        self.current_config.margin_y = self.var_margin_y.get()
        
        # Image watermark
        self.current_config.watermark_image_path = self.var_watermark_image_path.get()
        self.current_config.scale_factor = self.var_scale_factor.get()
        
        # Advanced settings
        stroke_color_rgb = self.hex_to_rgb(self.var_stroke_color.get())
        shadow_color_rgb = self.hex_to_rgb(self.var_shadow_color.get())
        self.current_config.stroke_width = self.var_stroke_width.get()
        self.current_config.stroke_color = (stroke_color_rgb[0], stroke_color_rgb[1], stroke_color_rgb[2])
        self.current_config.shadow_offset = (self.var_shadow_offset_x.get(), self.var_shadow_offset_y.get())
        self.current_config.shadow_color = (shadow_color_rgb[0], shadow_color_rgb[1], shadow_color_rgb[2])
    
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
                # Keep reference to prevent garbage collection
                setattr(thumb_label, 'image_ref', photo)
                
                # Create filename label
                filename = os.path.basename(file_path)
                display_name = self.format_filename_for_display(filename, 30)
                name_label = tk.Label(thumb_frame, text=display_name, font=("Arial", 8))
                name_label.pack()
                
                # Add tooltip for full filename on hover
                self.add_tooltip(thumb_label, filename)
                self.add_tooltip(name_label, filename)
                
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
        
        if not self.file_manager.output_directory:
            self.select_output_directory()
            if not self.file_manager.output_directory:
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
        
        if not self.file_manager.output_directory:
            self.select_output_directory()
            if not self.file_manager.output_directory:
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
        name = simpledialog.askstring("Save Template", "Enter template name:")
        if name:
            name = name.strip()
            if name:
                self.update_config_from_gui()
                
                description = simpledialog.askstring(
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
    
    def run(self):
        """Start the application"""
        self.root.mainloop()

if __name__ == "__main__":
    app = WatermarkApp()
    app.run()