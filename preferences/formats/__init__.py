import bpy
from ...bversion import BVERSION
from . import panels


from .format_definition import FormatDefinition
FORMATS = [f for f in dir(FormatDefinition) if not f.startswith('_')]

from .format_compatible import CompatibleFormats
COMPATIBLE_FORMATS = CompatibleFormats()

from .format_handler import FormatHandler

from . import properties

from .format_class_creator import FormatClassCreator, ClassFactory

# function to register dynamically generated classes for each compatible formats
def register_import_setting_class():
    for f in COMPATIBLE_FORMATS.formats:
        if f'{f[0]}_module' not in modules:
            continue

        cl = modules[f'{f[0]}_module']
        properties.PG_ImportSettings.__annotations__[f'{f[0]}_import_module'] = bpy.props.PointerProperty(type=cl)
        for name in f[1]['operator'].keys():
            if f'{f[0]}_{name}_settings' not in modules:
                continue

            cl = modules[f'{f[0]}_{name}_settings']
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

def get_import_modules():
    modules = {}
    for f in COMPATIBLE_FORMATS.formats:
        module_items = [(m.upper(), m.title().replace('_', ' '), '') for m in f[1]['operator'].keys()]
        c = ClassFactory(f'UMI_{f[0]}_module', None, bpy.types.PropertyGroup)
        c.__annotations__['name'] = bpy.props.EnumProperty(items=module_items, name="Import Module")
        modules[f'{f[0]}_module'] = c

        for name in f[1]['operator'].keys():
            c = ClassFactory(f'UMI_{f[0]}_{name}_settings', None, bpy.types.PropertyGroup)
            c.__annotations__['name'] = bpy.props.StringProperty(name="Import Setting Name", default=f"{f[0]}_{name}")
            modules[f'{f[0]}_{name}_settings'] = c

    return modules

modules = get_import_modules()