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
        
        # Chinese font support
        self.chinese_font_paths = [
            "C:/Windows/Fonts/simsun.ttc",  # 宋体
            "C:/Windows/Fonts/simhei.ttf",  # 黑体
            "C:/Windows/Fonts/msyh.ttc",    # 微软雅黑
            "C:/Windows/Fonts/simkai.ttf",  # 楷体
            "C:/Windows/Fonts/simfang.ttf", # 仿宋
            "C:/Windows/Fonts/STXIHEI.TTF", # 华文细黑
            "C:/Windows/Fonts/STZHONGS.TTF", # 华文中宋
        ]
    
    def is_supported_format(self, file_path: str) -> bool:
        """Check if the file format is supported"""
        _, ext = os.path.splitext(file_path.lower())
        return ext in self.SUPPORTED_INPUT_FORMATS
    
    def load_image(self, file_path: str) -> Optional[Image.Image]:
        """Load an image from file path with EXIF orientation handling"""
        try:
            if not self.is_supported_format(file_path):
                return None
            
            image = Image.open(file_path)
            
            # Handle EXIF orientation using ImageOps
            try:
                from PIL import ImageOps
                image = ImageOps.exif_transpose(image)
            except Exception:
                # If EXIF handling fails, continue with original image
                pass
            
            # Convert to RGBA to handle transparency consistently
            if image.mode != 'RGBA':
                image = image.convert('RGBA')
            return image
        except Exception as e:
            print(f"Error loading image {file_path}: {e}")
            return None
    
    def get_font(self, font_family: str, font_size: int, bold: bool = False, italic: bool = False):
        """Get font object with fallback handling and Chinese character support"""
        # Try to find the font with specific styling first
        font_paths_to_try = []
        
        # Add specific font family paths with styling
        if font_family.lower() == "arial":
            # Try styled versions first
            if bold and italic:
                font_paths_to_try.extend([
                    "C:/Windows/Fonts/arialbi.ttf",
                    "C:/Windows/Fonts/Arial Bold Italic.ttf"
                ])
            elif bold:
                font_paths_to_try.extend([
                    "C:/Windows/Fonts/arialbd.ttf",
                    "C:/Windows/Fonts/Arial Bold.ttf"
                ])
            elif italic:
                font_paths_to_try.extend([
                    "C:/Windows/Fonts/ariali.ttf",
                    "C:/Windows/Fonts/Arial Italic.ttf"
                ])
            # Fallback to regular
            font_paths_to_try.extend([
                "C:/Windows/Fonts/arial.ttf",
                "C:/Windows/Fonts/Arial.ttf"
            ])
        elif font_family.lower() == "times new roman":
            # Try styled versions first
            if bold and italic:
                font_paths_to_try.extend([
                    "C:/Windows/Fonts/timesbi.ttf",
                    "C:/Windows/Fonts/timesbi.ttc",
                    "C:/Windows/Fonts/Times New Roman Bold Italic.ttf"
                ])
            elif bold:
                font_paths_to_try.extend([
                    "C:/Windows/Fonts/timesbd.ttf",
                    "C:/Windows/Fonts/timesb.ttc",
                    "C:/Windows/Fonts/Times New Roman Bold.ttf"
                ])
            elif italic:
                font_paths_to_try.extend([
                    "C:/Windows/Fonts/timesi.ttf",
                    "C:/Windows/Fonts/timesi.ttc",
                    "C:/Windows/Fonts/Times New Roman Italic.ttf"
                ])
            # Fallback to regular
            font_paths_to_try.extend([
                "C:/Windows/Fonts/times.ttf",
                "C:/Windows/Fonts/times.ttc",
                "C:/Windows/Fonts/Times New Roman.ttf"
            ])
        elif font_family.lower() == "calibri":
            # Try styled versions first
            if bold and italic:
                font_paths_to_try.extend([
                    "C:/Windows/Fonts/calibribi.ttf",
                    "C:/Windows/Fonts/calibribi.ttf",
                    "C:/Windows/Fonts/Calibri Bold Italic.ttf"
                ])
            elif bold:
                font_paths_to_try.extend([
                    "C:/Windows/Fonts/calibrib.ttf",
                    "C:/Windows/Fonts/calibri-bold.ttf",
                    "C:/Windows/Fonts/Calibri Bold.ttf"
                ])
            elif italic:
                font_paths_to_try.extend([
                    "C:/Windows/Fonts/calibrii.ttf",
                    "C:/Windows/Fonts/calibri-italic.ttf",
                    "C:/Windows/Fonts/Calibri Italic.ttf"
                ])
            # Fallback to regular
            font_paths_to_try.extend([
                "C:/Windows/Fonts/calibri.ttf",
                "C:/Windows/Fonts/Calibri.ttf"
            ])
        elif font_family.lower() in ["simsun", "宋体"]:
            font_paths_to_try.extend([
                "C:/Windows/Fonts/simsun.ttc",
                "C:/Windows/Fonts/simsunb.ttf" if bold else "C:/Windows/Fonts/simsun.ttc"
            ])
        elif font_family.lower() in ["simhei", "黑体"]:
            font_paths_to_try.extend([
                "C:/Windows/Fonts/simhei.ttf"
            ])
        elif font_family.lower() in ["microsoftyahei", "微软雅黑", "yahei"]:
            # Try styled versions first
            if bold:
                font_paths_to_try.extend([
                    "C:/Windows/Fonts/msyhbd.ttc",
                    "C:/Windows/Fonts/msyhbd.ttf",
                    "C:/Windows/Fonts/MSYHBD.TTC"
                ])
            # Fallback to regular
            font_paths_to_try.extend([
                "C:/Windows/Fonts/msyh.ttc",
                "C:/Windows/Fonts/msyh.ttf",
                "C:/Windows/Fonts/MSYH.TTC"
            ])
        
        # Add default Western font paths
        font_paths_to_try.extend(self.default_font_paths)
        
        # Add Chinese font paths as fallback
        font_paths_to_try.extend(self.chinese_font_paths)
        
        for font_path in font_paths_to_try:
            try:
                if os.path.exists(font_path):
                    return ImageFont.truetype(font_path, font_size)
            except Exception as e:
                continue
        
        # Ultimate fallback to default font
        try:
            return ImageFont.load_default()
        except:
            return ImageFont.load_default()
    
    def has_chinese_characters(self, text: str) -> bool:
        """Check if text contains Chinese characters"""
        for char in text:
            if '\u4e00' <= char <= '\u9fff':
                return True
        return False
    
    def get_chinese_font(self, font_family: str, font_size: int, bold: bool = False, italic: bool = False):
        """Get a Chinese-compatible font with styling support"""
        chinese_fonts = []
        
        # Try to find the best Chinese font based on selected family
        if font_family.lower() in ["microsoftyahei", "微软雅黑", "yahei"]:
            # 微软雅黑 (Microsoft YaHei) - best for Chinese text
            if bold and italic:
                chinese_fonts.extend([
                    "C:/Windows/Fonts/msyhbd.ttc",
                    "C:/Windows/Fonts/msyhbd.ttf",
                    "C:/Windows/Fonts/MSYHBD.TTC"
                ])
            elif bold:
                chinese_fonts.extend([
                    "C:/Windows/Fonts/msyhbd.ttc",
                    "C:/Windows/Fonts/msyhbd.ttf",
                    "C:/Windows/Fonts/MSYHBD.TTC"
                ])
            elif italic:
                # YaHei doesn't have a true italic, but we can try
                chinese_fonts.extend([
                    "C:/Windows/Fonts/msyh.ttc",
                    "C:/Windows/Fonts/msyh.ttf",
                    "C:/Windows/Fonts/MSYH.TTC"
                ])
            else:
                chinese_fonts.extend([
                    "C:/Windows/Fonts/msyh.ttc",
                    "C:/Windows/Fonts/msyh.ttf",
                    "C:/Windows/Fonts/MSYH.TTC"
                ])
        elif font_family.lower() in ["simsun", "宋体"]:
            # 宋体 (SimSun)
            if bold:
                chinese_fonts.extend([
                    "C:/Windows/Fonts/simsunb.ttf"
                ])
            chinese_fonts.extend([
                "C:/Windows/Fonts/simsun.ttc"
            ])
        elif font_family.lower() in ["simhei", "黑体"]:
            # 黑体 (SimHei) - usually doesn't have bold/italic variants
            chinese_fonts.extend([
                "C:/Windows/Fonts/simhei.ttf"
            ])
        else:
            # Default to YaHei if unknown font family
            if bold:
                chinese_fonts.extend([
                    "C:/Windows/Fonts/msyhbd.ttc",
                    "C:/Windows/Fonts/msyhbd.ttf"
                ])
            chinese_fonts.extend([
                "C:/Windows/Fonts/msyh.ttc",
                "C:/Windows/Fonts/msyh.ttf"
            ])
        
        # Add fallback Chinese fonts
        chinese_fonts.extend([
            "C:/Windows/Fonts/simkai.ttf",
            "C:/Windows/Fonts/simfang.ttf",
            "C:/Windows/Fonts/STXIHEI.TTF",
            "C:/Windows/Fonts/STZHONGS.TTF"
        ])
        
        for font_path in chinese_fonts:
            try:
                if os.path.exists(font_path):
                    return ImageFont.truetype(font_path, font_size)
            except Exception:
                continue
        
        # Fallback to default font
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
        """Create a text watermark image with Chinese character support and proper sizing"""
        # Check if text contains Chinese characters and get appropriate font
        has_chinese = self.has_chinese_characters(text)
        
        if has_chinese:
            # Use Chinese font for Chinese text
            font = self.get_chinese_font(config.font_family, config.font_size, 
                                       config.font_bold, config.font_italic)
        else:
            # Use regular font for Western text
            font = self.get_font(config.font_family, config.font_size, 
                               config.font_bold, config.font_italic)
        
        # Calculate text size using proper font metrics
        # Create a temporary image to measure text
        temp_img = Image.new('RGBA', (1, 1), (0, 0, 0, 0))
        temp_draw = ImageDraw.Draw(temp_img)
        
        # Get text bounding box
        bbox = temp_draw.textbbox((0, 0), text, font=font, stroke_width=config.stroke_width)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        # Add generous padding for shadow, stroke, and font rendering
        # This is especially important for large fonts to prevent clipping
        base_padding = max(config.stroke_width, max(abs(config.shadow_offset[0]), 
                                               abs(config.shadow_offset[1]))) + 10
        
        # Add extra padding for large fonts to prevent clipping
        extra_padding = 0
        if config.font_size > 50:
            extra_padding = min(config.font_size // 5, 20)  # Add extra padding for large fonts
        
        padding = base_padding + extra_padding
        
        # Create watermark image with adequate padding
        wm_width = int(text_width + padding * 2)
        wm_height = int(text_height + padding * 2)
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
        
        # For Chinese text with italic requested, apply skew transformation
        if has_chinese and config.font_italic:
            # Apply skew transformation to simulate italic effect
            width, height = watermark.size
            skew_factor = 0.2  # Adjust this to control the italic effect
            
            # Create transformation matrix for skew
            from PIL import ImageTransform
            matrix = (1, skew_factor, -skew_factor * height, 0, 1, 0)
            skewed_watermark = watermark.transform(
                (int(width + skew_factor * height), height),
                ImageTransform.AffineTransform(matrix)
            )
            watermark = skewed_watermark
        
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
                     filename_suffix: str = "", resize_options: Optional[dict] = None) -> List[str]:
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