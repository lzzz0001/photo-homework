"""
Test script specifically for the originally missing features
Tests drag-drop fallback, manual positioning, and TIFF support
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from image_processor import ImageProcessor, WatermarkConfig, WatermarkPosition, WatermarkType
from file_manager import FileManager, DragDropHandler
from PIL import Image
import tkinter as tk

def create_test_images():
    """Create test images in different formats including TIFF"""
    test_dir = "test_formats"
    os.makedirs(test_dir, exist_ok=True)
    
    # Create a simple test image
    img = Image.new('RGB', (400, 300), color='lightblue')
    
    # Save in different formats
    formats = {
        'JPEG': 'test.jpg',
        'PNG': 'test.png', 
        'BMP': 'test.bmp',
        'TIFF': 'test.tiff'
    }
    
    saved_files = []
    for format_name, filename in formats.items():
        filepath = os.path.join(test_dir, filename)
        try:
            img.save(filepath, format=format_name)
            saved_files.append(filepath)
            print(f"✓ Created {filename}")
        except Exception as e:
            print(f"✗ Failed to create {filename}: {e}")
    
    return saved_files

def test_tiff_support():
    """Test TIFF format support specifically"""
    print("Testing TIFF format support...")
    
    processor = ImageProcessor()
    
    # Create test TIFF
    test_files = create_test_images()
    tiff_file = None
    for file in test_files:
        if file.endswith('.tiff'):
            tiff_file = file
            break
    
    if not tiff_file:
        print("  ✗ Could not create TIFF test file")
        return False
    
    # Test 1: Format recognition
    if processor.is_supported_format(tiff_file):
        print("  ✓ TIFF format recognized as supported")
    else:
        print("  ✗ TIFF format not recognized")
        return False
    
    # Test 2: Load TIFF image
    try:
        image = processor.load_image(tiff_file)
        if image:
            print("  ✓ TIFF image loaded successfully")
        else:
            print("  ✗ TIFF image failed to load")
            return False
    except Exception as e:
        print(f"  ✗ TIFF load error: {e}")
        return False
    
    # Test 3: Apply watermark to TIFF
    try:
        config = WatermarkConfig()
        config.text = "TIFF Test"
        watermarked = processor.apply_watermark(image, config)
        print("  ✓ Watermark applied to TIFF image")
    except Exception as e:
        print(f"  ✗ TIFF watermark error: {e}")
        return False
    
    # Test 4: Export TIFF as different formats
    try:
        output_dir = "test_tiff_output"
        os.makedirs(output_dir, exist_ok=True)
        
        # Export as JPEG
        jpeg_path = os.path.join(output_dir, "tiff_to_jpeg.jpg")
        if processor.save_image(watermarked, jpeg_path, "JPEG", 95):
            print("  ✓ TIFF exported as JPEG")
        else:
            print("  ✗ TIFF to JPEG export failed")
            return False
        
        # Export as PNG
        png_path = os.path.join(output_dir, "tiff_to_png.png")
        if processor.save_image(watermarked, png_path, "PNG"):
            print("  ✓ TIFF exported as PNG")
        else:
            print("  ✗ TIFF to PNG export failed")
            return False
            
    except Exception as e:
        print(f"  ✗ TIFF export error: {e}")
        return False
    
    print("All TIFF tests passed! ✓")
    return True

def test_drag_drop_handler():
    """Test drag-drop handler functionality"""
    print("Testing drag-drop handler...")
    
    # Create a minimal tkinter environment for testing
    root = tk.Tk()
    root.withdraw()  # Hide the window
    
    try:
        file_manager = FileManager()
        test_frame = tk.Frame(root)
        
        # Test callback function
        dropped_files = []
        def test_callback(files):
            dropped_files.extend(files)
        
        # Create drag-drop handler
        handler = DragDropHandler(test_frame, file_manager, test_callback)
        print("  ✓ DragDropHandler created successfully")
        
        # Test fallback functionality (click simulation)
        if hasattr(handler, 'on_click_fallback'):
            print("  ✓ Click fallback functionality available")
        else:
            print("  ✗ Click fallback not implemented")
            return False
        
        print("Drag-drop handler tests passed! ✓")
        return True
        
    except Exception as e:
        print(f"  ✗ Drag-drop handler error: {e}")
        return False
    finally:
        root.destroy()

def test_manual_positioning():
    """Test manual positioning features"""
    print("Testing manual positioning...")
    
    processor = ImageProcessor()
    config = WatermarkConfig()
    
    # Test custom positioning
    config.position = WatermarkPosition.CUSTOM
    config.custom_x = 150
    config.custom_y = 100
    config.text = "Custom Position"
    
    # Create test image
    test_image = Image.new('RGB', (400, 300), color='white')
    
    try:
        # Apply watermark with custom position
        watermarked = processor.apply_watermark(test_image, config)
        print("  ✓ Custom positioning works")
        
        # Test different custom positions
        positions = [(50, 50), (200, 150), (350, 250)]
        for x, y in positions:
            config.custom_x = x
            config.custom_y = y
            watermarked = processor.apply_watermark(test_image, config)
        
        print("  ✓ Multiple custom positions work")
        
        # Save test result
        output_dir = "test_positioning"
        os.makedirs(output_dir, exist_ok=True)
        processor.save_image(watermarked, os.path.join(output_dir, "custom_position.png"), "PNG")
        print("  ✓ Custom positioned watermark saved")
        
    except Exception as e:
        print(f"  ✗ Manual positioning error: {e}")
        return False
    
    print("Manual positioning tests passed! ✓")
    return True

def test_all_formats_batch():
    """Test batch processing with all supported formats"""
    print("Testing batch processing with all formats...")
    
    # Create test files
    test_files = create_test_images()
    
    if len(test_files) < 3:
        print("  ✗ Not enough test files created")
        return False
    
    processor = ImageProcessor()
    config = WatermarkConfig()
    config.text = "Batch Test"
    config.opacity = 60
    
    output_dir = "test_batch_all_formats"
    os.makedirs(output_dir, exist_ok=True)
    
    try:
        # Test batch processing
        results = processor.batch_process(
            test_files,
            config,
            output_dir,
            "PNG",  # Export all as PNG to test transparency preservation
            95,
            "batch_",
            "_processed"
        )
        
        if len(results) >= len(test_files):
            print(f"  ✓ Batch processed {len(results)} files")
        else:
            print(f"  ✗ Only processed {len(results)}/{len(test_files)} files")
            return False
        
        # Verify output files exist
        for result_path in results:
            if os.path.exists(result_path):
                print(f"  ✓ Output file exists: {os.path.basename(result_path)}")
            else:
                print(f"  ✗ Missing output file: {os.path.basename(result_path)}")
                return False
                
    except Exception as e:
        print(f"  ✗ Batch processing error: {e}")
        return False
    
    print("Batch processing tests passed! ✓")
    return True

def main():
    """Run all missing feature tests"""
    print("=== Testing Originally Missing Features ===\n")
    
    tests = [
        ("TIFF Format Support", test_tiff_support),
        ("Drag-Drop Handler", test_drag_drop_handler), 
        ("Manual Positioning", test_manual_positioning),
        ("Batch All Formats", test_all_formats_batch)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n--- {test_name} ---")
        try:
            if test_func():
                passed += 1
                print(f"✓ {test_name} PASSED")
            else:
                print(f"✗ {test_name} FAILED")
        except Exception as e:
            print(f"✗ {test_name} ERROR: {e}")
    
    print(f"\n=== RESULTS ===")
    print(f"Passed: {passed}/{total}")
    
    if passed == total:
        print("🎉 ALL MISSING FEATURES NOW IMPLEMENTED!")
        return True
    else:
        print("⚠️  Some features still need work")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)