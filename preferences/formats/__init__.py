import bpy
from . import panels


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
		cl_name = f'UMI_{f[0]}_module'
		cl = eval(cl_name)
		properties.PG_ImportSettings.__annotations__[f'{f[0]}_import_module'] = bpy.props.PointerProperty(type=cl)
		for name in f[1]['operator'].keys():
			cl_name = f'UMI_{f[0]}_{name}_settings'
			cl = eval(cl_name)
			properties.PG_ImportSettings.__annotations__[f'{f[0]}_{name}_import_settings'] = bpy.props.PointerProperty(type=cl)
			
	properties.PG_ImportSettings.umi_import_settings_registered = True
	
def register():
	class_parser = FormatClassCreator()
	class_parser.register_compatible_formats()
	register_import_setting_class()
	panels.register()
	properties.register()

def unregister():
	properties.unregister()
	panels.unregister()
	class_parser = FormatClassCreator()
	class_parser.unregister_compatible_formats()
	
for f in COMPATIBLE_FORMATS.formats:
	module_items = [(m.upper(), m.title().replace('_', ' '), '') for m in f[1]['operator'].keys()]
	exec(f'class UMI_{f[0]}_module(bpy.types.PropertyGroup):name: bpy.props.EnumProperty(items={module_items}, name="Import Module")')
	for name in f[1]['operator'].keys():
		exec(f'class UMI_{f[0]}_{name}_settings(bpy.types.PropertyGroup):name: bpy.props.StringProperty(name="Import Setting Name", default="{f[0]}_{name}")')