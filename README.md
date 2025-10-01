# Photo Watermark Application v1.1.0

A desktop application for adding watermarks to images with advanced features like batch processing, real-time preview, and template management.

## Features

### File Processing
- **Import Images**: Support for drag-drop and file selector import
- **Batch Import**: Select multiple images or entire folders
- **Format Support**: JPEG, PNG, BMP, TIFF with transparency support for PNG
- **Export Options**: Choose output format (JPEG/PNG) with quality control

### Watermark Types
- **Text Watermarks**: Customizable text with font, color, transparency, and style options
- **Image Watermarks**: Use PNG images with transparency as watermarks
- **Multilingual Support**: Full support for Chinese characters and Western text
- **Font Styling**: Bold, italic, and combined styling for all supported fonts

### Layout & Positioning
- **Real-time Preview**: See watermark effects instantly
- **Positioning**: Nine preset positions or manual drag-and-drop
- **Rotation**: Rotate watermarks at any angle
- **Transparency Control**: Adjust watermark opacity
- **Advanced Effects**: Stroke, shadow, and margin controls

### Configuration Management
- **Templates**: Save and load watermark configurations
- **Batch Processing**: Apply watermarks to multiple images at once
- **Auto-save**: Application remembers your last settings

### Enhanced Features (v1.1.0)
- **Chinese Font Support**: Full rendering of Chinese characters in watermarks
- **Simulated Italic for Chinese**: Visual italic effect using font skewing
- **Windows Native Drag-Drop**: Robust file import using windnd library
- **EXIF Orientation Support**: Automatic correction for camera-rotated images
- **Improved Filename Display**: Better handling of long filenames with tooltips
- **Enhanced Error Handling**: Better feedback and recovery from errors

## Requirements

- Windows 10/11
- Python 3.8+ (for development)

## Installation

### For Users
Download the latest release from the [Releases](../../releases) page and run the executable.

### For Developers
1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Run the application: `python main.py`

## Building

To create a Windows executable:
```
pyinstaller --onefile --windowed --add-data "assets;assets" main.py
```

## Changelog

### v1.1.0 (Latest)
- Added Chinese font support with proper rendering
- Implemented Windows native drag-drop using windnd
- Added simulated italic effect for Chinese text
- Fixed EXIF orientation issues for camera photos
- Improved large font watermark handling
- Enhanced filename display with tooltips
- Fixed font styling (bold/italic) for all font types

### v1.0.0
- Initial release with core watermarking functionality

## License

MIT License