import bpy
from .format_definition import FormatDefinition
FORMATS = [f for f in dir(FormatDefinition) if not f.startswith('__')]

from .format_compatible import CompatibleFormats
COMPATIBLE_FORMATS = CompatibleFormats()

from .format_handler import FormatHandler

from . import properties

from .format_class_creator import FormatClassCreator

# function to register dynamically generated classes for each compatible formats
def register_import_setting_class():
	for f in COMPATIBLE_FORMATS.formats:
		cl_name = f'UMI_{f[1]["name"]}_settings'
		cl = eval(cl_name)
		exec(f'PG_ImportSettings.__annotations__["{f[1]["name"]}_import_settings"] = bpy.props.PointerProperty(type={cl_name})', {'bpy': bpy, 'PG_ImportSettings':properties.PG_ImportSettings, cl_name:cl})
		
	properties.PG_ImportSettings.umi_import_settings_registered = True
	
def register():
	class_parser = FormatClassCreator()
	class_parser.register_compatible_formats()
	register_import_setting_class()
	properties.register()

def unregister():
	properties.unregister()
	class_parser = FormatClassCreator()
	class_parser.unregister_compatible_formats()
	
for f in COMPATIBLE_FORMATS.formats:
	exec(f'class UMI_{f[1]["name"]}_settings(bpy.types.PropertyGroup):name: bpy.props.StringProperty(name="Import Setting Name", default="{f[1]["name"]}")')