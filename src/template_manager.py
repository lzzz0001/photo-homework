"""
Template management module for saving and loading watermark configurations.
Handles watermark template persistence and management operations.
"""

import os
import json
from typing import Dict, List, Optional, Any
from src.image_processor import WatermarkConfig, WatermarkPosition, WatermarkType

class TemplateManager:
    """Manages watermark template saving, loading, and organization"""
    
    def __init__(self, templates_dir: str = "templates"):
        self.templates_dir = templates_dir
        self.templates_file = os.path.join(templates_dir, "templates.json")
        self.last_template_file = os.path.join(templates_dir, "last_config.json")
        
        # Ensure templates directory exists
        os.makedirs(templates_dir, exist_ok=True)
        
        # Load existing templates
        self.templates = self.load_templates_from_file()
    
    def config_to_dict(self, config: WatermarkConfig) -> Dict[str, Any]:
        """Convert WatermarkConfig to dictionary for JSON serialization"""
        return {
            'watermark_type': config.watermark_type.value,
            'position': config.position.value,
            'opacity': config.opacity,
            'rotation': config.rotation,
            'custom_x': config.custom_x,
            'custom_y': config.custom_y,
            
            # Text watermark settings
            'text': config.text,
            'font_family': config.font_family,
            'font_size': config.font_size,
            'font_bold': config.font_bold,
            'font_italic': config.font_italic,
            'text_color': config.text_color,
            'stroke_width': config.stroke_width,
            'stroke_color': config.stroke_color,
            'shadow_offset': config.shadow_offset,
            'shadow_color': config.shadow_color,
            
            # Image watermark settings
            'watermark_image_path': config.watermark_image_path,
            'scale_factor': config.scale_factor,
            
            # Margin settings
            'margin_x': config.margin_x,
            'margin_y': config.margin_y
        }
    
    def dict_to_config(self, data: Dict[str, Any]) -> WatermarkConfig:
        """Convert dictionary to WatermarkConfig object"""
        config = WatermarkConfig()
        
        # Safely set attributes with defaults
        config.watermark_type = WatermarkType(data.get('watermark_type', 'text'))
        config.position = WatermarkPosition(data.get('position', 'bottom_right'))
        config.opacity = data.get('opacity', 50)
        config.rotation = data.get('rotation', 0)
        config.custom_x = data.get('custom_x', 0)
        config.custom_y = data.get('custom_y', 0)
        
        # Text watermark settings
        config.text = data.get('text', 'Watermark')
        config.font_family = data.get('font_family', 'Arial')
        config.font_size = data.get('font_size', 36)
        config.font_bold = data.get('font_bold', False)
        config.font_italic = data.get('font_italic', False)
        config.text_color = tuple(data.get('text_color', [255, 255, 255]))
        config.stroke_width = data.get('stroke_width', 2)
        config.stroke_color = tuple(data.get('stroke_color', [0, 0, 0]))
        config.shadow_offset = tuple(data.get('shadow_offset', [2, 2]))
        config.shadow_color = tuple(data.get('shadow_color', [0, 0, 0]))
        
        # Image watermark settings
        config.watermark_image_path = data.get('watermark_image_path', '')
        config.scale_factor = data.get('scale_factor', 1.0)
        
        # Margin settings
        config.margin_x = data.get('margin_x', 20)
        config.margin_y = data.get('margin_y', 20)
        
        return config
    
    def save_template(self, name: str, config: WatermarkConfig, description: str = "") -> bool:
        """Save a watermark configuration as a template"""
        try:
            template_data = {
                'name': name,
                'description': description,
                'config': self.config_to_dict(config),
                'created_at': self.get_current_timestamp()
            }
            
            # Add or update template
            self.templates[name] = template_data
            
            # Save to file
            return self.save_templates_to_file()
            
        except Exception as e:
            print(f"Error saving template {name}: {e}")
            return False
    
    def load_template(self, name: str) -> Optional[WatermarkConfig]:
        """Load a watermark configuration from template"""
        try:
            if name not in self.templates:
                return None
            
            template_data = self.templates[name]
            return self.dict_to_config(template_data['config'])
            
        except Exception as e:
            print(f"Error loading template {name}: {e}")
            return None
    
    def delete_template(self, name: str) -> bool:
        """Delete a template"""
        try:
            if name in self.templates:
                del self.templates[name]
                return self.save_templates_to_file()
            return False
        except Exception as e:
            print(f"Error deleting template {name}: {e}")
            return False
    
    def get_template_list(self) -> List[str]:
        """Get list of available template names"""
        return list(self.templates.keys())
    
    def get_template_info(self, name: str) -> Optional[Dict[str, Any]]:
        """Get template information including description and creation date"""
        if name in self.templates:
            return {
                'name': self.templates[name]['name'],
                'description': self.templates[name].get('description', ''),
                'created_at': self.templates[name].get('created_at', '')
            }
        return None
    
    def save_last_config(self, config: WatermarkConfig) -> bool:
        """Save the last used configuration for auto-loading"""
        try:
            config_data = self.config_to_dict(config)
            with open(self.last_template_file, 'w', encoding='utf-8') as f:
                json.dump(config_data, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error saving last config: {e}")
            return False
    
    def load_last_config(self) -> Optional[WatermarkConfig]:
        """Load the last used configuration"""
        try:
            if not os.path.exists(self.last_template_file):
                return None
            
            with open(self.last_template_file, 'r', encoding='utf-8') as f:
                config_data = json.load(f)
            
            return self.dict_to_config(config_data)
            
        except Exception as e:
            print(f"Error loading last config: {e}")
            return None
    
    def load_templates_from_file(self) -> Dict[str, Any]:
        """Load templates from JSON file"""
        try:
            if not os.path.exists(self.templates_file):
                return {}
            
            with open(self.templates_file, 'r', encoding='utf-8') as f:
                return json.load(f)
                
        except Exception as e:
            print(f"Error loading templates from file: {e}")
            return {}
    
    def save_templates_to_file(self) -> bool:
        """Save templates to JSON file"""
        try:
            with open(self.templates_file, 'w', encoding='utf-8') as f:
                json.dump(self.templates, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error saving templates to file: {e}")
            return False
    
    def export_template(self, name: str, export_path: str) -> bool:
        """Export a single template to a file"""
        try:
            if name not in self.templates:
                return False
            
            template_data = self.templates[name]
            with open(export_path, 'w', encoding='utf-8') as f:
                json.dump(template_data, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error exporting template {name}: {e}")
            return False
    
    def import_template(self, import_path: str) -> Optional[str]:
        """Import a template from a file"""
        try:
            with open(import_path, 'r', encoding='utf-8') as f:
                template_data = json.load(f)
            
            # Validate template data structure
            required_fields = ['name', 'config']
            if not all(field in template_data for field in required_fields):
                return None
            
            name = template_data['name']
            
            # Handle name conflicts
            original_name = name
            counter = 1
            while name in self.templates:
                name = f"{original_name}_{counter}"
                counter += 1
            
            template_data['name'] = name
            self.templates[name] = template_data
            
            if self.save_templates_to_file():
                return name
            return None
            
        except Exception as e:
            print(f"Error importing template from {import_path}: {e}")
            return None
    
    def create_default_templates(self):
        """Create some default templates for users"""
        default_templates = [
            {
                'name': 'Simple Copyright',
                'description': 'Simple white copyright text in bottom right',
                'config': {
                    'watermark_type': 'text',
                    'text': '© Your Name',
                    'position': 'bottom_right',
                    'font_family': 'Arial',
                    'font_size': 24,
                    'text_color': [255, 255, 255],
                    'opacity': 70,
                    'stroke_width': 1,
                    'stroke_color': [0, 0, 0]
                }
            },
            {
                'name': 'Large Diagonal',
                'description': 'Large diagonal watermark across center',
                'config': {
                    'watermark_type': 'text',
                    'text': 'WATERMARK',
                    'position': 'center',
                    'font_family': 'Arial',
                    'font_size': 72,
                    'text_color': [255, 255, 255],
                    'opacity': 30,
                    'rotation': -45,
                    'stroke_width': 2,
                    'stroke_color': [0, 0, 0]
                }
            },
            {
                'name': 'Subtle Corner',
                'description': 'Small, subtle watermark in corner',
                'config': {
                    'watermark_type': 'text',
                    'text': 'Photo by You',
                    'position': 'bottom_right',
                    'font_family': 'Arial',
                    'font_size': 16,
                    'text_color': [200, 200, 200],
                    'opacity': 50,
                    'margin_x': 10,
                    'margin_y': 10
                }
            }
        ]
        
        # Only create if no templates exist
        if not self.templates:
            for template_info in default_templates:
                config = self.dict_to_config(template_info['config'])
                self.save_template(
                    template_info['name'], 
                    config, 
                    template_info['description']
                )
    
    def get_current_timestamp(self) -> str:
        """Get current timestamp as formatted string"""
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def cleanup_invalid_templates(self):
        """Remove templates that have invalid configurations"""
        invalid_templates = []
        
        for name, template_data in self.templates.items():
            try:
                # Try to convert to config to validate
                self.dict_to_config(template_data.get('config', {}))
            except Exception as e:
                print(f"Invalid template found: {name} - {e}")
                invalid_templates.append(name)
        
        # Remove invalid templates
        for name in invalid_templates:
            del self.templates[name]
        
        if invalid_templates:
            self.save_templates_to_file()
            print(f"Removed {len(invalid_templates)} invalid templates")
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get template usage statistics"""
        return {
            'total_templates': len(self.templates),
            'template_names': list(self.templates.keys()),
            'has_last_config': os.path.exists(self.last_template_file)
        }