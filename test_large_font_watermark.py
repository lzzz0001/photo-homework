#!/usr/bin/env python3
"""
Test script to verify large font watermark functionality
"""

import sys
import os
from PIL import Image

# Add src directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from image_processor import ImageProcessor, WatermarkConfig, WatermarkType

def test_large_font_watermark():
    """Test large font watermark functionality"""
    print("Testing large font watermark functionality...")
    
    # Create image processor
    processor = ImageProcessor()
    
    # Create a simple test image
    test_image = Image.new('RGBA', (800, 600), (255, 255, 255, 255))
    
    # Test different font sizes
    font_sizes = [24, 36, 48, 72, 96, 120]
    
    for font_size in font_sizes:
        print(f"\nTesting font size: {font_size}")
        
        config = WatermarkConfig()
        config.text = "Large Text"
        config.font_family = "Arial"
        config.font_size = font_size
        config.text_color = (255, 0, 0)  # Red color
        config.stroke_width = 2
        config.shadow_offset = (3, 3)
        
        # Create watermark
        watermark = processor.create_text_watermark(config.text, config)
        print(f"Watermark created: {watermark is not None}")
        
        if watermark:
            print(f"Watermark size: {watermark.size}")
            
            # Apply watermark to image
            result = processor.apply_watermark(test_image, config)
            print(f"Watermark applied: {result is not None}")
            
            # Save test result
            result.save(f"test_large_font_{font_size}.png")
            print(f"Test image saved as test_large_font_{font_size}.png")
    
    # Test with Chinese text and large font
    print(f"\nTesting large Chinese font")
    config_chinese = WatermarkConfig()
    config_chinese.text = "大字体测试"
    config_chinese.font_family = "微软雅黑"
    config_chinese.font_size = 96
    config_chinese.text_color = (0, 0, 255)  # Blue color
    
    watermark_chinese = processor.create_text_watermark(config_chinese.text, config_chinese)
    print(f"Chinese watermark created: {watermark_chinese is not None}")
    
    if watermark_chinese:
        print(f"Chinese watermark size: {watermark_chinese.size}")
        
        # Apply watermark to image
        result_chinese = processor.apply_watermark(test_image, config_chinese)
        print(f"Chinese watermark applied: {result_chinese is not None}")
        
        # Save test result
        result_chinese.save("test_large_chinese_font.png")
        print("Chinese test image saved as test_large_chinese_font.png")
    
    print("\nTest completed!")

if __name__ == "__main__":
    test_large_font_watermark()