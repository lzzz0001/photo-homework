#!/usr/bin/env python3
"""
Comprehensive test script to verify all font styling functionality
"""

import sys
import os
from PIL import Image

# Add src directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from image_processor import ImageProcessor, WatermarkConfig, WatermarkType

def test_comprehensive_font_styling():
    """Test all font styling combinations"""
    print("Testing comprehensive font styling functionality...")
    
    # Create image processor
    processor = ImageProcessor()
    
    # Create a simple test image
    test_image = Image.new('RGBA', (800, 600), (255, 255, 255, 255))
    
    # Test English fonts with all combinations
    print("\n=== Testing English Font Styling ===")
    
    english_tests = [
        ("Arial Regular", "Arial", False, False),
        ("Arial Bold", "Arial", True, False),
        ("Arial Italic", "Arial", False, True),
        ("Arial Bold Italic", "Arial", True, True),
        ("Times New Roman Regular", "Times New Roman", False, False),
        ("Times New Roman Bold", "Times New Roman", True, False),
        ("Times New Roman Italic", "Times New Roman", False, True),
        ("Times New Roman Bold Italic", "Times New Roman", True, True),
        ("Calibri Regular", "Calibri", False, False),
        ("Calibri Bold", "Calibri", True, False),
        ("Calibri Italic", "Calibri", False, True),
        ("Calibri Bold Italic", "Calibri", True, True),
    ]
    
    for i, (description, font_family, bold, italic) in enumerate(english_tests):
        config = WatermarkConfig()
        config.text = description
        config.font_family = font_family
        config.font_size = 24
        config.font_bold = bold
        config.font_italic = italic
        config.text_color = (255, 0, 0) if not bold and not italic else \
                           (0, 255, 0) if bold and not italic else \
                           (0, 0, 255) if not bold and italic else \
                           (255, 0, 255)  # Bold italic
        
        watermark = processor.create_text_watermark(config.text, config)
        print(f"{description} - Created: {watermark is not None}")
        if watermark:
            result = processor.apply_watermark(test_image, config)
            filename = f"test_english_{i:02d}_{font_family.replace(' ', '_')}_{('bold_' if bold else '') + ('italic' if italic else 'regular')}.png".lower()
            result.save(filename)
            print(f"  Saved as {filename}")
    
    # Test Chinese fonts with all combinations
    print("\n=== Testing Chinese Font Styling ===")
    
    chinese_tests = [
        ("微软雅黑 Regular", "微软雅黑", False, False),
        ("微软雅黑 Bold", "微软雅黑", True, False),
        ("微软雅黑 Italic", "微软雅黑", False, True),
        ("微软雅黑 Bold Italic", "微软雅黑", True, True),
        ("宋体 Regular", "宋体", False, False),
        ("宋体 Bold", "宋体", True, False),
        ("黑体 Regular", "黑体", False, False),
    ]
    
    for i, (description, font_family, bold, italic) in enumerate(chinese_tests):
        config = WatermarkConfig()
        config.text = description
        config.font_family = font_family
        config.font_size = 24
        config.font_bold = bold
        config.font_italic = italic
        config.text_color = (255, 165, 0) if not bold and not italic else \
                           (128, 0, 128) if bold and not italic else \
                           (0, 128, 128) if not bold and italic else \
                           (128, 128, 0)  # Bold italic
        
        watermark = processor.create_text_watermark(config.text, config)
        print(f"{description} - Created: {watermark is not None}")
        if watermark:
            result = processor.apply_watermark(test_image, config)
            filename = f"test_chinese_{i:02d}_{font_family}_{('bold_' if bold else '') + ('italic' if italic else 'regular')}.png".lower()
            # Replace Chinese characters in filename
            filename = filename.replace('微', 'wei').replace('软', 'ruan').replace('宋', 'song').replace('黑', 'hei')
            result.save(filename)
            print(f"  Saved as {filename}")
    
    # Test font family switching
    print("\n=== Testing Font Family Switching ===")
    
    font_family_tests = [
        ("Arial Font", "Arial"),
        ("Times New Roman Font", "Times New Roman"),
        ("Calibri Font", "Calibri"),
        ("微软雅黑 Font", "微软雅黑"),
        ("宋体 Font", "宋体"),
        ("黑体 Font", "黑体"),
    ]
    
    for i, (description, font_family) in enumerate(font_family_tests):
        config = WatermarkConfig()
        config.text = description
        config.font_family = font_family
        config.font_size = 28
        config.text_color = (0, 0, 0)
        
        watermark = processor.create_text_watermark(config.text, config)
        print(f"{description} - Created: {watermark is not None}")
        if watermark:
            result = processor.apply_watermark(test_image, config)
            filename = f"test_font_family_{i:02d}_{font_family.replace(' ', '_').replace('微', 'wei').replace('软', 'ruan').replace('宋', 'song').replace('黑', 'hei')}.png".lower()
            result.save(filename)
            print(f"  Saved as {filename}")
    
    print("\nTest completed! Check the generated PNG files to verify all font styling combinations.")

if __name__ == "__main__":
    test_comprehensive_font_styling()