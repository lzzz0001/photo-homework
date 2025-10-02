#!/usr/bin/env python3
"""
Visual test for italic font styling to see the actual difference
"""

import sys
import os
from PIL import Image, ImageDraw, ImageFont

# Add src directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from image_processor import ImageProcessor, WatermarkConfig

def test_italic_visual():
    """Visual test for italic font styling"""
    print("Creating visual comparison of italic vs regular fonts...")
    
    # Create image processor
    processor = ImageProcessor()
    
    # Create a larger test image for better visibility
    test_image = Image.new('RGBA', (600, 200), (255, 255, 255, 255))
    
    # Test 1: Arial Regular
    config1 = WatermarkConfig()
    config1.text = "Arial Regular Text"
    config1.font_family = "Arial"
    config1.font_size = 36
    config1.font_bold = False
    config1.font_italic = False
    config1.text_color = (255, 0, 0)  # Red
    
    watermark1 = processor.create_text_watermark(config1.text, config1)
    print(f"Arial Regular - Created: {watermark1 is not None}")
    if watermark1:
        result1 = processor.apply_watermark(test_image, config1)
        result1.save("test_visual_regular.png")
        print("Saved as test_visual_regular.png")
    
    # Test 2: Arial Italic
    config2 = WatermarkConfig()
    config2.text = "Arial Italic Text"
    config2.font_family = "Arial"
    config2.font_size = 36
    config2.font_bold = False
    config2.font_italic = True
    config2.text_color = (0, 0, 255)  # Blue
    
    watermark2 = processor.create_text_watermark(config2.text, config2)
    print(f"Arial Italic - Created: {watermark2 is not None}")
    if watermark2:
        result2 = processor.apply_watermark(test_image, config2)
        result2.save("test_visual_italic.png")
        print("Saved as test_visual_italic.png")
    
    # Test 3: Side-by-side comparison
    print("\nCreating side-by-side comparison...")
    
    # Create a wide image for comparison
    comparison_image = Image.new('RGBA', (1200, 200), (255, 255, 255, 255))
    draw = ImageDraw.Draw(comparison_image)
    
    # Create regular watermark
    regular_watermark = processor.create_text_watermark("Regular ABC", config1)
    
    # Create italic watermark
    italic_watermark = processor.create_text_watermark("Italic ABC", config2)
    
    if regular_watermark and italic_watermark:
        # Paste regular on left
        comparison_image.paste(regular_watermark, (50, 50), regular_watermark)
        
        # Paste italic on right
        comparison_image.paste(italic_watermark, (650, 50), italic_watermark)
        
        # Add labels
        try:
            label_font = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 24)
        except:
            label_font = ImageFont.load_default()
        
        draw.text((100, 20), "Regular Text", font=label_font, fill=(0, 0, 0))
        draw.text((700, 20), "Italic Text", font=label_font, fill=(0, 0, 0))
        
        comparison_image.save("test_visual_comparison.png")
        print("Saved side-by-side comparison as test_visual_comparison.png")
    
    # Test 4: Chinese text comparison
    print("\nTesting Chinese text...")
    
    # Chinese Regular
    config3 = WatermarkConfig()
    config3.text = "中文常规"
    config3.font_family = "微软雅黑"
    config3.font_size = 36
    config3.font_bold = False
    config3.font_italic = False
    config3.text_color = (0, 128, 0)  # Green
    
    watermark3 = processor.create_text_watermark(config3.text, config3)
    print(f"Chinese Regular - Created: {watermark3 is not None}")
    
    # Chinese 'Italic' (will likely be the same font)
    config4 = WatermarkConfig()
    config4.text = "中文斜体"
    config4.font_family = "微软雅黑"
    config4.font_size = 36
    config4.font_bold = False
    config4.font_italic = True
    config4.text_color = (255, 165, 0)  # Orange
    
    watermark4 = processor.create_text_watermark(config4.text, config4)
    print(f"Chinese 'Italic' - Created: {watermark4 is not None}")
    
    if watermark3 and watermark4:
        chinese_image = Image.new('RGBA', (1200, 200), (255, 255, 255, 255))
        draw = ImageDraw.Draw(chinese_image)
        
        # Paste regular on left
        chinese_image.paste(watermark3, (50, 50), watermark3)
        
        # Paste 'italic' on right
        chinese_image.paste(watermark4, (650, 50), watermark4)
        
        # Add labels
        draw.text((100, 20), "Regular Chinese", font=label_font, fill=(0, 0, 0))
        draw.text((700, 20), "Italic Chinese", font=label_font, fill=(0, 0, 0))
        
        chinese_image.save("test_chinese_visual_comparison.png")
        print("Saved Chinese comparison as test_chinese_visual_comparison.png")
    
    print("\nVisual test completed! Check the generated PNG files to see the font styling differences.")

if __name__ == "__main__":
    test_italic_visual()