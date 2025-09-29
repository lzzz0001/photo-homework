"""
Test script for the Photo Watermark Application
Tests core functionality without GUI
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from image_processor import ImageProcessor, WatermarkConfig, WatermarkPosition, WatermarkType
from file_manager import FileManager
from template_manager import TemplateManager
from PIL import Image

def create_test_image():
    """Create a simple test image"""
    # Create a 800x600 test image with gradient
    img = Image.new('RGB', (800, 600), color='lightblue')
    
    # Add some content to make it more realistic
    from PIL import ImageDraw, ImageFont
    draw = ImageDraw.Draw(img)
    
    # Draw some shapes
    draw.rectangle([100, 100, 700, 500], fill='white', outline='black', width=3)
    draw.ellipse([200, 200, 600, 400], fill='yellow', outline='red', width=2)
    
    # Add text
    try:
        font = ImageFont.load_default()
        draw.text((300, 280), "TEST IMAGE", fill='black', font=font)
    except:
        draw.text((300, 280), "TEST IMAGE", fill='black')
    
    return img

def test_basic_functionality():
    """Test basic watermarking functionality"""
    print("Testing basic functionality...")
    
    # Create test components
    processor = ImageProcessor()
    file_manager = FileManager()
    template_manager = TemplateManager()
    
    # Create test image
    test_image = create_test_image()
    
    # Test 1: Text watermark
    print("  1. Testing text watermark...")
    config = WatermarkConfig()
    config.text = "© Test Watermark"
    config.position = WatermarkPosition.BOTTOM_RIGHT
    config.opacity = 70
    
    try:
        watermarked = processor.apply_watermark(test_image, config)
        print("     ✓ Text watermark applied successfully")
    except Exception as e:
        print(f"     ✗ Text watermark failed: {e}")
        return False
    
    # Test 2: Position variations
    print("  2. Testing different positions...")
    positions = [WatermarkPosition.TOP_LEFT, WatermarkPosition.CENTER, WatermarkPosition.BOTTOM_RIGHT]
    for pos in positions:
        try:
            config.position = pos
            watermarked = processor.apply_watermark(test_image, config)
            print(f"     ✓ Position {pos.value} works")
        except Exception as e:
            print(f"     ✗ Position {pos.value} failed: {e}")
            return False
    
    # Test 3: File format support
    print("  3. Testing file format support...")
    formats = ['.jpg', '.png', '.bmp']
    for fmt in formats:
        if processor.is_supported_format(f"test{fmt}"):
            print(f"     ✓ Format {fmt} supported")
        else:
            print(f"     ✗ Format {fmt} not supported")
    
    # Test 4: Template management
    print("  4. Testing template management...")
    try:
        template_manager.save_template("Test Template", config, "Test description")
        loaded_config = template_manager.load_template("Test Template")
        if loaded_config and loaded_config.text == config.text:
            print("     ✓ Template save/load works")
        else:
            print("     ✗ Template save/load failed")
            return False
    except Exception as e:
        print(f"     ✗ Template management failed: {e}")
        return False
    
    # Test 5: Save functionality
    print("  5. Testing image save...")
    try:
        # Create output directory
        output_dir = "test_output"
        os.makedirs(output_dir, exist_ok=True)
        
        # Save as JPEG
        jpeg_path = os.path.join(output_dir, "test_watermark.jpg")
        success = processor.save_image(watermarked, jpeg_path, "JPEG", 95)
        if success and os.path.exists(jpeg_path):
            print("     ✓ JPEG save works")
        else:
            print("     ✗ JPEG save failed")
            return False
        
        # Save as PNG
        png_path = os.path.join(output_dir, "test_watermark.png")
        success = processor.save_image(watermarked, png_path, "PNG")
        if success and os.path.exists(png_path):
            print("     ✓ PNG save works")
        else:
            print("     ✗ PNG save failed")
            return False
            
    except Exception as e:
        print(f"     ✗ Image save failed: {e}")
        return False
    
    print("All basic tests passed! ✓")
    return True

def test_advanced_features():
    """Test advanced features"""
    print("\nTesting advanced features...")
    
    processor = ImageProcessor()
    test_image = create_test_image()
    
    # Test 1: Rotation
    print("  1. Testing rotation...")
    config = WatermarkConfig()
    config.text = "ROTATED"
    config.rotation = 45
    
    try:
        watermarked = processor.apply_watermark(test_image, config)
        print("     ✓ Rotation works")
    except Exception as e:
        print(f"     ✗ Rotation failed: {e}")
        return False
    
    # Test 2: Opacity variations
    print("  2. Testing opacity...")
    for opacity in [10, 50, 90]:
        try:
            config.opacity = opacity
            watermarked = processor.apply_watermark(test_image, config)
            print(f"     ✓ Opacity {opacity}% works")
        except Exception as e:
            print(f"     ✗ Opacity {opacity}% failed: {e}")
            return False
    
    # Test 3: Font styling
    print("  3. Testing font styling...")
    try:
        config.font_bold = True
        config.font_italic = True
        config.font_size = 48
        watermarked = processor.apply_watermark(test_image, config)
        print("     ✓ Font styling works")
    except Exception as e:
        print(f"     ✗ Font styling failed: {e}")
        return False
    
    print("All advanced tests passed! ✓")
    return True

def main():
    """Run all tests"""
    print("=== Photo Watermark Application Tests ===\n")
    
    try:
        basic_success = test_basic_functionality()
        advanced_success = test_advanced_features()
        
        if basic_success and advanced_success:
            print("\n=== ALL TESTS PASSED! ===")
            print("The application is ready for use.")
            return True
        else:
            print("\n=== SOME TESTS FAILED ===")
            print("Please check the error messages above.")
            return False
            
    except Exception as e:
        print(f"\nUnexpected error during testing: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)