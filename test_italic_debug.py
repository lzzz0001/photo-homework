#!/usr/bin/env python3
"""
Debug test for italic font styling functionality
"""

import sys
import os
from PIL import Image, ImageFont

# Add src directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from image_processor import ImageProcessor, WatermarkConfig

def test_italic_debug():
    """Debug italic font functionality"""
    print("Debugging italic font functionality...")
    
    # Create image processor
    processor = ImageProcessor()
    
    # Test if italic font files exist
    print("\n=== Checking Italic Font Files ===")
    
    italic_font_paths = [
        "C:/Windows/Fonts/ariali.ttf",
        "C:/Windows/Fonts/Arial Italic.ttf",
        "C:/Windows/Fonts/timesi.ttf",
        "C:/Windows/Fonts/timesi.ttc",
        "C:/Windows/Fonts/Times New Roman Italic.ttf",
        "C:/Windows/Fonts/calibrii.ttf",
        "C:/Windows/Fonts/calibri-italic.ttf",
        "C:/Windows/Fonts/Calibri Italic.ttf"
    ]
    
    available_fonts = []
    for font_path in italic_font_paths:
        exists = os.path.exists(font_path)
        status = 'FOUND' if exists else 'NOT FOUND'
        print(f"{font_path}: {status}")
        if exists:
            available_fonts.append(font_path)
    
    # Test direct font creation
    print("\n=== Testing Direct Font Creation ===")
    
    for font_path in available_fonts[:3]:  # Test first 3 available fonts
        try:
            font = ImageFont.truetype(font_path, 24)
            print(f"✓ Successfully created font from {font_path}")
        except Exception as e:
            print(f"✗ Failed to create font from {font_path}: {e}")
    
    # Test the get_font method directly
    print("\n=== Testing get_font Method ===")
    
    # Test Arial Italic
    try:
        font = processor.get_font("Arial", 24, False, True)  # italic only
        print(f"✓ Arial Italic font created: {font}")
    except Exception as e:
        print(f"✗ Failed to create Arial Italic: {e}")
    
    # Test Times New Roman Italic
    try:
        font = processor.get_font("Times New Roman", 24, False, True)  # italic only
        print(f"✓ Times New Roman Italic font created: {font}")
    except Exception as e:
        print(f"✗ Failed to create Times New Roman Italic: {e}")
    
    # Test Calibri Italic
    try:
        font = processor.get_font("Calibri", 24, False, True)  # italic only
        print(f"✓ Calibri Italic font created: {font}")
    except Exception as e:
        print(f"✗ Failed to create Calibri Italic: {e}")

if __name__ == "__main__":
    test_italic_debug()