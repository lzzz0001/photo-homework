"""
Core image processing module for watermark operations.
Handles text and image watermarking with various positioning and styling options.
"""

from PIL import Image, ImageDraw, ImageFont, ImageEnhance
import os
import math
from typing import Tuple, Optional, List, Union
from enum import Enum

class WatermarkPosition(Enum):
    """Predefined watermark positions"""
    TOP_LEFT = "top_left"
    TOP_CENTER = "top_center"
    TOP_RIGHT = "top_right"
    CENTER_LEFT = "center_left"
    CENTER = "center"
    CENTER_RIGHT = "center_right"
    BOTTOM_LEFT = "bottom_left"
    BOTTOM_CENTER = "bottom_center"
    BOTTOM_RIGHT = "bottom_right"
    CUSTOM = "custom"

class WatermarkType(Enum):
    """Types of watermarks"""
    TEXT = "text"
    IMAGE = "image"

class WatermarkConfig:
    """Configuration class for watermark settings"""
    
    def __init__(self):
        # Common settings
        self.watermark_type = WatermarkType.TEXT
        self.position = WatermarkPosition.BOTTOM_RIGHT
        self.opacity = 50  # 0-100
        self.rotation = 0  # degrees
        self.custom_x = 0  # for custom positioning
        self.custom_y = 0  # for custom positioning
        
        # Text watermark settings
        self.text = "Watermark"
        self.font_family = "Arial"
        self.font_size = 36
        self.font_bold = False
        self.font_italic = False
        self.text_color: Tuple[int, int, int] = (255, 255, 255)  # RGB
        self.stroke_width = 2
        self.stroke_color: Tuple[int, int, int] = (0, 0, 0)  # RGB
        self.shadow_offset: Tuple[int, int] = (2, 2)
        self.shadow_color: Tuple[int, int, int] = (0, 0, 0)
        
        # Image watermark settings
        self.watermark_image_path = ""
        self.scale_factor = 1.0  # scaling for image watermark
        
        # Margin settings
        self.margin_x = 20
        self.margin_y = 20

class ImageProcessor:
    """Main class for image processing and watermarking operations"""
    
    SUPPORTED_INPUT_FORMATS = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.tif'}
    SUPPORTED_OUTPUT_FORMATS = {'JPEG', 'PNG'}
    
    def __init__(self):
        self.default_font_paths = [
            "C:/Windows/Fonts/arial.ttf",
            "C:/Windows/Fonts/calibri.ttf",
            "C:/Windows/Fonts/times.ttf",
            "arial.ttf",  # fallback
        ]
    
    def is_supported_format(self, file_path: str) -> bool:
        """Check if the file format is supported"""
        _, ext = os.path.splitext(file_path.lower())
        return ext in self.SUPPORTED_INPUT_FORMATS
    
    def load_image(self, file_path: str) -> Optional[Image.Image]:
        """Load an image from file path"""
        try:
            if not self.is_supported_format(file_path):
                return None
            
            image = Image.open(file_path)
            # Convert to RGBA to handle transparency consistently
            if image.mode != 'RGBA':
                image = image.convert('RGBA')
            return image
        except Exception as e:
            print(f"Error loading image {file_path}: {e}")
            return None
    
    def get_font(self, font_family: str, font_size: int, bold: bool = False, italic: bool = False) -> ImageFont.ImageFont:
        """Get font object with fallback handling"""
        font_style = ""
        if bold and italic:
            font_style = "bi"
        elif bold:
            font_style = "b"
        elif italic:
            font_style = "i"
        
        # Try to find the font in system fonts
        font_paths_to_try = []
        
        # Add specific font family paths
        if font_family.lower() == "arial":
            font_paths_to_try.extend([
                f"C:/Windows/Fonts/arial{font_style}.ttf",
                "C:/Windows/Fonts/arial.ttf"
            ])
        elif font_family.lower() == "times new roman":
            font_paths_to_try.extend([
                f"C:/Windows/Fonts/times{font_style}.ttf",
                "C:/Windows/Fonts/times.ttf"
            ])
        elif font_family.lower() == "calibri":
            font_paths_to_try.extend([
                f"C:/Windows/Fonts/calibri{font_style}.ttf",
                "C:/Windows/Fonts/calibri.ttf"
            ])
        
        # Add default font paths
        font_paths_to_try.extend(self.default_font_paths)
        
        for font_path in font_paths_to_try:
            try:
                if os.path.exists(font_path):
                    return ImageFont.truetype(font_path, font_size)
            except:
                continue
        
        # Ultimate fallback to default font
        try:
            return ImageFont.load_default()
        except:
            return ImageFont.load_default()
    
    def calculate_position(self, image_size: Tuple[int, int], watermark_size: Tuple[int, int], 
                          config: WatermarkConfig) -> Tuple[int, int]:
        """Calculate watermark position based on configuration"""
        img_width, img_height = image_size
        wm_width, wm_height = watermark_size
        
        if config.position == WatermarkPosition.CUSTOM:
            return (config.custom_x, config.custom_y)
        
        # Calculate positions with margins
        positions = {
            WatermarkPosition.TOP_LEFT: (config.margin_x, config.margin_y),
            WatermarkPosition.TOP_CENTER: (
                (img_width - wm_width) // 2, 
                config.margin_y
            ),
            WatermarkPosition.TOP_RIGHT: (
                img_width - wm_width - config.margin_x, 
                config.margin_y
            ),
            WatermarkPosition.CENTER_LEFT: (
                config.margin_x, 
                (img_height - wm_height) // 2
            ),
            WatermarkPosition.CENTER: (
                (img_width - wm_width) // 2, 
                (img_height - wm_height) // 2
            ),
            WatermarkPosition.CENTER_RIGHT: (
                img_width - wm_width - config.margin_x, 
                (img_height - wm_height) // 2
            ),
            WatermarkPosition.BOTTOM_LEFT: (
                config.margin_x, 
                img_height - wm_height - config.margin_y
            ),
            WatermarkPosition.BOTTOM_CENTER: (
                (img_width - wm_width) // 2, 
                img_height - wm_height - config.margin_y
            ),
            WatermarkPosition.BOTTOM_RIGHT: (
                img_width - wm_width - config.margin_x, 
                img_height - wm_height - config.margin_y
            )
        }
        
        return positions.get(config.position, (config.margin_x, config.margin_y))
    
    def create_text_watermark(self, text: str, config: WatermarkConfig) -> Image.Image:
        """Create a text watermark image"""
        # Get font
        font = self.get_font(config.font_family, config.font_size, 
                           config.font_bold, config.font_italic)
        
        # Calculate text size
        # Create a temporary image to measure text
        temp_img = Image.new('RGBA', (1, 1), (0, 0, 0, 0))
        temp_draw = ImageDraw.Draw(temp_img)
        
        # Get text bounding box
        bbox = temp_draw.textbbox((0, 0), text, font=font, stroke_width=config.stroke_width)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        # Add padding for shadow and stroke
        padding = max(config.stroke_width, max(abs(config.shadow_offset[0]), 
                                               abs(config.shadow_offset[1]))) + 5
        
        # Create watermark image with padding
        wm_width = text_width + padding * 2
        wm_height = text_height + padding * 2
        watermark = Image.new('RGBA', (wm_width, wm_height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(watermark)
        
        # Text position with padding
        text_x = padding
        text_y = padding
        
        # Draw shadow if offset is specified
        if config.shadow_offset != (0, 0):
            shadow_x = text_x + config.shadow_offset[0]
            shadow_y = text_y + config.shadow_offset[1]
            shadow_color_with_alpha = config.shadow_color + (int(255 * config.opacity / 100),)
            draw.text((shadow_x, shadow_y), text, font=font, fill=shadow_color_with_alpha)
        
        # Draw main text with stroke
        text_color_with_alpha = config.text_color + (int(255 * config.opacity / 100),)
        stroke_color_with_alpha = config.stroke_color + (int(255 * config.opacity / 100),)
        
        draw.text((text_x, text_y), text, font=font, fill=text_color_with_alpha,
                 stroke_width=config.stroke_width, stroke_fill=stroke_color_with_alpha)
        
        # Apply rotation if specified
        if config.rotation != 0:
            watermark = watermark.rotate(config.rotation, expand=True)
        
        return watermark
    
    def create_image_watermark(self, config: WatermarkConfig) -> Optional[Image.Image]:
        """Create an image watermark from file"""
        try:
            if not config.watermark_image_path or not os.path.exists(config.watermark_image_path):
                return None
            
            watermark = Image.open(config.watermark_image_path)
            
            # Ensure RGBA mode for transparency
            if watermark.mode != 'RGBA':
                watermark = watermark.convert('RGBA')
            
            # Apply scaling
            if config.scale_factor != 1.0:
                new_width = int(watermark.width * config.scale_factor)
                new_height = int(watermark.height * config.scale_factor)
                watermark = watermark.resize((new_width, new_height), Image.Resampling.LANCZOS)
            
            # Apply opacity
            if config.opacity < 100:
                alpha = watermark.split()[3]  # Get alpha channel
                alpha = ImageEnhance.Brightness(alpha).enhance(config.opacity / 100.0)
                watermark.putalpha(alpha)
            
            # Apply rotation if specified
            if config.rotation != 0:
                watermark = watermark.rotate(config.rotation, expand=True)
            
            return watermark
            
        except Exception as e:
            print(f"Error creating image watermark: {e}")
            return None
    
    def apply_watermark(self, image: Image.Image, config: WatermarkConfig) -> Image.Image:
        """Apply watermark to an image based on configuration"""
        # Create watermark based on type
        if config.watermark_type == WatermarkType.TEXT:
            watermark = self.create_text_watermark(config.text, config)
        else:
            watermark = self.create_image_watermark(config)
            
        if watermark is None:
            return image
        
        # Calculate position
        position = self.calculate_position(image.size, watermark.size, config)
        
        # Create a copy of the original image
        result = image.copy()
        
        # Paste watermark onto the image
        result.paste(watermark, position, watermark)
        
        return result
    
    def save_image(self, image: Image.Image, output_path: str, 
                   output_format: str = 'JPEG', quality: int = 95) -> bool:
        """Save image to file with specified format and quality"""
        try:
            # Ensure output directory exists
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            if output_format.upper() == 'JPEG':
                # Convert to RGB for JPEG (remove alpha channel)
                if image.mode == 'RGBA':
                    # Create white background
                    background = Image.new('RGB', image.size, (255, 255, 255))
                    background.paste(image, mask=image.split()[3])  # Use alpha as mask
                    image = background
                image.save(output_path, format='JPEG', quality=quality, optimize=True)
            else:  # PNG
                image.save(output_path, format='PNG', optimize=True)
            
            return True
        except Exception as e:
            print(f"Error saving image to {output_path}: {e}")
            return False
    
    def resize_image(self, image: Image.Image, width: Optional[int] = None, 
                    height: Optional[int] = None, scale_percent: Optional[float] = None) -> Image.Image:
        """Resize image with different options"""
        if scale_percent:
            new_width = int(image.width * scale_percent / 100)
            new_height = int(image.height * scale_percent / 100)
        elif width and height:
            new_width, new_height = width, height
        elif width:
            aspect_ratio = image.height / image.width
            new_width = width
            new_height = int(width * aspect_ratio)
        elif height:
            aspect_ratio = image.width / image.height
            new_height = height
            new_width = int(height * aspect_ratio)
        else:
            return image
        
        return image.resize((new_width, new_height), Image.Resampling.LANCZOS)
    
    def batch_process(self, image_paths: List[str], config: WatermarkConfig, 
                     output_dir: str, output_format: str = 'JPEG', 
                     quality: int = 95, filename_prefix: str = "", 
                     filename_suffix: str = "", resize_options: dict = None) -> List[str]:
        """Process multiple images with watermarks"""
        results = []
        
        for image_path in image_paths:
            try:
                # Load image
                image = self.load_image(image_path)
                if image is None:
                    continue
                
                # Apply resize if specified
                if resize_options:
                    image = self.resize_image(image, **resize_options)
                
                # Apply watermark
                watermarked_image = self.apply_watermark(image, config)
                
                # Generate output filename
                base_name = os.path.splitext(os.path.basename(image_path))[0]
                new_filename = f"{filename_prefix}{base_name}{filename_suffix}"
                
                # Add appropriate extension
                if output_format.upper() == 'JPEG':
                    new_filename += '.jpg'
                else:
                    new_filename += '.png'
                
                output_path = os.path.join(output_dir, new_filename)
                
                # Save image
                if self.save_image(watermarked_image, output_path, output_format, quality):
                    results.append(output_path)
                
            except Exception as e:
                print(f"Error processing {image_path}: {e}")
                continue
        
        return results