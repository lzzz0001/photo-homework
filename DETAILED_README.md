# Photo Watermark Application

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Platform](https://img.shields.io/badge/platform-Windows-lightgrey.svg)
![Python](https://img.shields.io/badge/python-3.8+-brightgreen.svg)

A comprehensive Windows desktop application for adding watermarks to images with advanced features and batch processing capabilities.

## 🌟 Features

### File Processing
- **Multiple Import Options**: Drag-drop, file selector, or entire folder import
- **Format Support**: JPEG, PNG, BMP, TIFF with full transparency support
- **Batch Processing**: Process multiple images simultaneously
- **Smart Export**: Customizable output formats, quality settings, and naming rules

### Watermark Types
- **Text Watermarks**: 
  - Customizable fonts, sizes, colors
  - Bold and italic styling
  - Stroke and shadow effects
  - Adjustable transparency (0-100%)
- **Image Watermarks**: 
  - PNG support with transparency
  - Scalable sizing
  - Rotation support

### Advanced Positioning
- **Nine Preset Positions**: Quick placement with one click
- **Manual Positioning**: Drag and drop watermarks anywhere
- **Rotation Control**: Rotate watermarks to any angle
- **Margin Settings**: Fine-tune positioning with pixel precision

### Real-time Preview
- **Live Updates**: See changes instantly as you adjust settings
- **Multiple Image Preview**: Switch between imported images
- **Zoom and Scroll**: Navigate large images easily

### Template Management
- **Save Configurations**: Store watermark settings as reusable templates
- **Quick Loading**: Apply saved templates instantly
- **Template Library**: Manage multiple watermark styles
- **Auto-save**: Remember last used settings

## 📸 Screenshots

### Main Interface
The application features a clean, intuitive interface with tabbed controls and real-time preview.

### Watermark Examples
- Simple copyright text in corner
- Large diagonal watermarks
- Custom image watermarks with transparency

## 🚀 Quick Start

### Download and Run (Recommended)
1. Download the latest `PhotoWatermark.exe` from the [Releases](../../releases) page
2. Run the executable - no installation required!
3. Import your images and start watermarking

### For Developers
```bash
# Clone the repository
git clone https://github.com/your-username/photo-watermark.git
cd photo-watermark

# Install dependencies
pip install -r requirements.txt

# Run the application
python main.py
```

## 💡 Usage Guide

### Basic Workflow
1. **Import Images**: Use the Files tab to import single images, multiple files, or entire folders
2. **Configure Watermark**: Set up your text or image watermark in the Watermark tab
3. **Position & Style**: Adjust position, opacity, rotation in the Position & Style tab
4. **Preview**: Check the result in the real-time preview
5. **Export**: Configure output settings and export your images

### Tips
- **Batch Processing**: Import multiple images and apply the same watermark to all
- **Templates**: Save frequently used watermark configurations as templates
- **Format Choice**: Use PNG for images requiring transparency, JPEG for smaller file sizes
- **Quality Control**: Adjust JPEG quality slider for optimal file size vs. quality balance

## 🔧 Technical Details

### System Requirements
- **Operating System**: Windows 10/11
- **Memory**: 512MB RAM minimum, 1GB recommended
- **Storage**: 50MB free space
- **Display**: 1024x768 minimum resolution

### Supported Formats
- **Input**: JPEG, PNG, BMP, TIFF
- **Output**: JPEG (with quality control), PNG (with transparency)

### Architecture
- **GUI Framework**: Tkinter (Python's standard GUI library)
- **Image Processing**: Pillow (PIL) for high-quality image operations
- **Packaging**: PyInstaller for standalone executable creation

## 🛠️ Building from Source

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Build Instructions
```bash
# Install development dependencies
pip install -r requirements.txt
pip install pyinstaller

# Run tests
python test_app.py

# Create executable
pyinstaller PhotoWatermark.spec --clean

# Find executable in dist/ folder
```

### Development Setup
```bash
# Install in development mode
pip install -e .

# Run tests
python test_app.py

# Run application
python main.py
```

## 📝 Changelog

### Version 1.0.0 (Initial Release)
- Complete text watermarking system
- Image watermark support
- Real-time preview functionality
- Template management system
- Batch processing capabilities
- Windows executable packaging
- Comprehensive file format support

## 🤝 Contributing

We welcome contributions! Here's how you can help:

1. **Report Bugs**: Open an issue with detailed reproduction steps
2. **Suggest Features**: Share your ideas for new functionality
3. **Submit Pull Requests**: Implement fixes or new features
4. **Improve Documentation**: Help make the docs clearer

### Development Guidelines
- Follow PEP 8 style guidelines
- Add tests for new functionality
- Update documentation for changes
- Test on multiple Windows versions

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Pillow Team**: For the excellent Python Imaging Library
- **Python Community**: For the robust tkinter GUI framework
- **PyInstaller**: For enabling easy application distribution
- **Contributors**: Thanks to everyone who helps improve this project

## 📞 Support

- **Issues**: Report bugs via [GitHub Issues](../../issues)
- **Discussions**: Join conversations in [GitHub Discussions](../../discussions)
- **Documentation**: Check the [Wiki](../../wiki) for detailed guides

## 🔗 Links

- [Download Latest Release](../../releases/latest)
- [View Source Code](../../)
- [Report Issues](../../issues)
- [Documentation Wiki](../../wiki)

---

**Made with ❤️ for photographers, designers, and content creators**