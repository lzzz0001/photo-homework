#!/usr/bin/env python3
"""
Test script to verify font styling functionality (bold, italic) for both English and Chinese text
"""

import sys
import os
from PIL import Image

# Add src directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from image_processor import ImageProcessor, WatermarkConfig, WatermarkType

def test_font_styling():
    """Test font styling functionality"""
    print("Testing font styling functionality...")
    
    # Create image processor
    processor = ImageProcessor()
    
    # Create a simple test image
    test_image = Image.new('RGBA', (800, 600), (255, 255, 255, 255))
    
    # Test 1: English text with different styling
    print("\n=== Testing English Font Styling ===")
    
    # Regular Arial
    config1 = WatermarkConfig()
    config1.text = "Regular Arial"
    config1.font_family = "Arial"
    config1.font_size = 36
    config1.text_color = (255, 0, 0)  # Red
    
    watermark1 = processor.create_text_watermark(config1.text, config1)
    print(f"Regular Arial - Created: {watermark1 is not None}")
    if watermark1:
        result1 = processor.apply_watermark(test_image, config1)
        result1.save("test_regular_arial.png")
        print("Saved as test_regular_arial.png")
    
    # Bold Arial
    config2 = WatermarkConfig()
    config2.text = "Bold Arial"
    config2.font_family = "Arial"
    config2.font_size = 36
    config2.font_bold = True
    config2.text_color = (0, 255, 0)  # Green
    
    watermark2 = processor.create_text_watermark(config2.text, config2)
    print(f"Bold Arial - Created: {watermark2 is not None}")
    if watermark2:
        result2 = processor.apply_watermark(test_image, config2)
        result2.save("test_bold_arial.png")
        print("Saved as test_bold_arial.png")
    
    # Italic Arial
    config3 = WatermarkConfig()
    config3.text = "Italic Arial"
    config3.font_family = "Arial"
    config3.font_size = 36
    config3.font_italic = True
    config3.text_color = (0, 0, 255)  # Blue
    
    watermark3 = processor.create_text_watermark(config3.text, config3)
    print(f"Italic Arial - Created: {watermark3 is not None}")
    if watermark3:
        result3 = processor.apply_watermark(test_image, config3)
        result3.save("test_italic_arial.png")
        print("Saved as test_italic_arial.png")
    
    # Bold Italic Arial
    config4 = WatermarkConfig()
    config4.text = "Bold Italic Arial"
    config4.font_family = "Arial"
    config4.font_size = 36
    config4.font_bold = True
    config4.font_italic = True
    config4.text_color = (255, 0, 255)  # Magenta
    
    watermark4 = processor.create_text_watermark(config4.text, config4)
    print(f"Bold Italic Arial - Created: {watermark4 is not None}")
    if watermark4:
        result4 = processor.apply_watermark(test_image, config4)
        result4.save("test_bold_italic_arial.png")
        print("Saved as test_bold_italic_arial.png")
    
    # Test 2: Chinese text with different styling
    print("\n=== Testing Chinese Font Styling ===")
    
    # Regular Chinese
    config5 = WatermarkConfig()
    config5.text = "普通中文字体"
    config5.font_family = "微软雅黑"
    config5.font_size = 36
    config5.text_color = (255, 165, 0)  # Orange
    
    watermark5 = processor.create_text_watermark(config5.text, config5)
    print(f"Regular Chinese - Created: {watermark5 is not None}")
    if watermark5:
        result5 = processor.apply_watermark(test_image, config5)
        result5.save("test_regular_chinese.png")
        print("Saved as test_regular_chinese.png")
    
    # Bold Chinese
    config6 = WatermarkConfig()
    config6.text = "粗体中文字体"
    config6.font_family = "微软雅黑"
    config6.font_size = 36
    config6.font_bold = True
    config6.text_color = (128, 0, 128)  # Purple
    
    watermark6 = processor.create_text_watermark(config6.text, config6)
    print(f"Bold Chinese - Created: {watermark6 is not None}")
    if watermark6:
        result6 = processor.apply_watermark(test_image, config6)
        result6.save("test_bold_chinese.png")
        print("Saved as test_bold_chinese.png")
    
    # Test with different Chinese fonts
    print("\n=== Testing Different Chinese Fonts ===")
    
    # SimSun (宋体)
    config7 = WatermarkConfig()
    config7.text = "宋体测试"
    config7.font_family = "宋体"
    config7.font_size = 36
    config7.font_bold = True
    config7.text_color = (0, 128, 128)  # Teal
    
    watermark7 = processor.create_text_watermark(config7.text, config7)
    print(f"SimSun Bold - Created: {watermark7 is not None}")
    if watermark7:
        result7 = processor.apply_watermark(test_image, config7)
        result7.save("test_simsun_bold.png")
        print("Saved as test_simsun_bold.png")
    
    # SimHei (黑体)
    config8 = WatermarkConfig()
    config8.text = "黑体测试"
    config8.font_family = "黑体"
    config8.font_size = 36
    config8.text_color = (128, 128, 0)  # Olive
    
    watermark8 = processor.create_text_watermark(config8.text, config8)
    print(f"SimHei - Created: {watermark8 is not None}")
    if watermark8:
        result8 = processor.apply_watermark(test_image, config8)
        result8.save("test_simhei.png")
        print("Saved as test_simhei.png")
    
    print("\nTest completed! Check the generated PNG files to verify font styling.")

if __name__ == "__main__":
    test_font_styling()