#!/usr/bin/env python3
"""
Test script to verify Chinese watermark functionality
"""

import sys
import os
from PIL import Image

# Add src directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from image_processor import ImageProcessor, WatermarkConfig, WatermarkType

def test_chinese_watermark():
    """Test Chinese watermark functionality"""
    print("Testing Chinese watermark functionality...")
    
    # Create image processor
    processor = ImageProcessor()
    
    # Create a simple test image
    test_image = Image.new('RGBA', (800, 600), (255, 255, 255, 255))
    
    # Test 1: Chinese watermark
    config = WatermarkConfig()
    config.text = "中文水印测试"
    config.font_family = "微软雅黑"
    config.font_size = 36
    config.text_color = (255, 0, 0)  # Red color
    
    print(f"Testing Chinese text: {config.text}")
    
    # Check if Chinese characters are detected
    has_chinese = processor.has_chinese_characters(config.text)
    print(f"Chinese characters detected: {has_chinese}")
    
    # Create watermark
    watermark = processor.create_text_watermark(config.text, config)
    print(f"Watermark created: {watermark is not None}")
    
    if watermark:
        print(f"Watermark size: {watermark.size}")
        
        # Apply watermark to image
        result = processor.apply_watermark(test_image, config)
        print(f"Watermark applied: {result is not None}")
        
        # Save test result
        result.save("test_chinese_watermark.png")
        print("Test image saved as test_chinese_watermark.png")
    
    # Test 2: Mixed text
    config2 = WatermarkConfig()
    config2.text = "Test测试"
    config2.font_family = "Arial"
    config2.font_size = 36
    config2.text_color = (0, 0, 255)  # Blue color
    
    print(f"\nTesting mixed text: {config2.text}")
    
    # Check if Chinese characters are detected
    has_chinese2 = processor.has_chinese_characters(config2.text)
    print(f"Chinese characters detected: {has_chinese2}")
    
    # Create watermark
    watermark2 = processor.create_text_watermark(config2.text, config2)
    print(f"Watermark created: {watermark2 is not None}")
    
    if watermark2:
        print(f"Watermark size: {watermark2.size}")
        
        # Apply watermark to image
        result2 = processor.apply_watermark(test_image, config2)
        print(f"Watermark applied: {result2 is not None}")
        
        # Save test result
        result2.save("test_mixed_watermark.png")
        print("Test image saved as test_mixed_watermark.png")
    
    print("\nTest completed!")

if __name__ == "__main__":
    test_chinese_watermark()