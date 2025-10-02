#!/usr/bin/env python3
"""
Test to simulate italic effect for Chinese text using PIL transformations
"""

import sys
import os
from PIL import Image, ImageDraw, ImageFont, ImageOps

# Add src directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from image_processor import ImageProcessor, WatermarkConfig

def simulate_chinese_italic():
    """Test simulating italic effect for Chinese text"""
    print("Testing Chinese italic simulation...")
    
    # Create image processor
    processor = ImageProcessor()
    
    # Create test image
    test_image = Image.new('RGBA', (500, 300), (255, 255, 255, 255))
    
    # Test 1: Regular Chinese text
    config1 = WatermarkConfig()
    config1.text = "中文水印"
    config1.font_family = "微软雅黑"
    config1.font_size = 48
    config1.font_italic = False
    config1.text_color = (255, 0, 0)  # Red
    
    watermark1 = processor.create_text_watermark(config1.text, config1)
    print(f"Regular Chinese watermark created: {watermark1 is not None}")
    
    # Test 2: Try to create italic effect manually using skew transformation
    print("\nCreating simulated italic effect...")
    
    try:
        # Get the Chinese font
        font = processor.get_chinese_font("微软雅黑", 48, False)
        
        # Create text image
        # First, measure text size
        temp_img = Image.new('RGBA', (1, 1), (0, 0, 0, 0))
        temp_draw = ImageDraw.Draw(temp_img)
        bbox = temp_draw.textbbox((0, 0), "中文水印", font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        # Add padding
        padding = 20
        img_width = int(text_width + padding * 2)
        img_height = int(text_height + padding * 2)
        
        # Create text image
        text_img = Image.new('RGBA', (img_width, img_height), (0, 0, 0, 0))
        text_draw = ImageDraw.Draw(text_img)
        text_draw.text((padding, padding), "中文水印", font=font, fill=(0, 0, 255, 255))  # Blue
        
        # Apply skew transformation to simulate italic
        # Skew the image to create italic effect
        width, height = text_img.size
        skew_factor = 0.3  # Adjust this to control the italic effect
        
        # Create transformation matrix for skew
        from PIL import ImageTransform
        matrix = (1, skew_factor, -skew_factor * height, 0, 1, 0)
        skewed_img = text_img.transform(
            (int(width + skew_factor * height), height),
            ImageTransform.AffineTransform(matrix)
        )
        
        # Save for comparison
        text_img.save("chinese_regular.png")
        skewed_img.save("chinese_simulated_italic.png")
        print("✓ Created simulated italic effect for Chinese text")
        print("  - Regular saved as chinese_regular.png")
        print("  - Simulated italic saved as chinese_simulated_italic.png")
        
    except Exception as e:
        print(f"Error creating simulated italic: {e}")
    
    # Test 3: Compare with actual italic (should be same as regular for Chinese)
    config2 = WatermarkConfig()
    config2.text = "中文水印"
    config2.font_family = "微软雅黑"
    config2.font_size = 48
    config2.font_italic = True  # This should have no effect
    config2.text_color = (0, 128, 0)  # Green
    
    watermark2 = processor.create_text_watermark(config2.text, config2)
    print(f"\nItalic Chinese watermark created: {watermark2 is not None}")
    
    if watermark1 and watermark2:
        # Save both for visual comparison
        result1 = processor.apply_watermark(test_image, config1)
        result2 = processor.apply_watermark(test_image, config2)
        
        result1.save("chinese_actual_regular.png")
        result2.save("chinese_actual_italic.png")
        
        print("✓ Saved actual regular and 'italic' versions for comparison")
        print("  Note: These should look identical since Chinese fonts")
        print("  typically don't have italic variants.")

def explain_chinese_typography():
    """Explain why Chinese italic is different"""
    print("\n" + "="*50)
    print("CHINESE TYPOGRAPHY EXPLANATION")
    print("="*50)
    print("1. Chinese characters are complex ideographs, not alphabetic")
    print("2. Traditional Chinese typography doesn't use italicization")
    print("3. Most Chinese fonts don't include italic variants")
    print("4. When 'italic' is requested, system falls back to regular")
    print()
    print("SOLUTIONS:")
    print("- Use font skewing/transformation to simulate italic")
    print("- Consider using different font weights instead")
    print("- Use color or stroke effects for emphasis")
    print("- Combine with rotation for stylistic effect")

if __name__ == "__main__":
    simulate_chinese_italic()
    explain_chinese_typography()