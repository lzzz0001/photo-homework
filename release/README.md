# Photo Watermark Application

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

### Layout & Positioning
- **Real-time Preview**: See watermark effects instantly
- **Positioning**: Nine preset positions or manual drag-and-drop
- **Rotation**: Rotate watermarks at any angle
- **Transparency Control**: Adjust watermark opacity

### Configuration Management
- **Templates**: Save and load watermark configurations
- **Batch Processing**: Apply watermarks to multiple images at once

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

## License

MIT License