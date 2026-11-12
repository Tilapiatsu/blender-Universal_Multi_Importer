import bpy
from ...preferences.formats import panels


from ...preferences.formats.format_definition import FormatDefinition

FORMATS = [f for f in dir(FormatDefinition) if not f.startswith("_")]

from ...preferences.formats.format_compatible import CompatibleFormats

COMPATIBLE_FORMATS = CompatibleFormats(auto_discover=False)

from ...preferences.formats.properties import properties
from ...preferences.formats.format_class_creator import FormatClassCreator, ClassFactory
from .format_discovery import FormatDiscovery

_operator_metadata = {}
_class_parser = None
_initialized = False


def finalize_discovery(discovery):

    global _operator_metadata
    global _initialized

    COMPATIBLE_FORMATS.refresh(available_operators=discovery.available)

    _operator_metadata = discovery.properties

    # Generate classes only after operator discovery.
    modules.clear()
    modules.update(get_import_modules())

    _initialized = True


# function to register dynamically generated classes for each compatible formats
def register_import_setting_class():
    for f in COMPATIBLE_FORMATS.formats:
        if f"{f.name}_module" not in modules:
            continue

        cl = modules[f"{f.name}_module"]
        properties.PG_ImportSettings.__annotations__[f"{f.name}_import_module"] = bpy.props.PointerProperty(type=cl)
        for name in f.operators.operators.keys():
            if f"{f.name}_{name}_settings" not in modules:
                continue

            cl = modules[f"{f.name}_{name}_settings"]
            properties.PG_ImportSettings.__annotations__[f"{f.name}_{name}_import_settings"] = (
                bpy.props.PointerProperty(type=cl)
            )

    properties.PG_ImportSettings.umi_import_settings_registered = True


def register():

    global _class_parser

    if not _initialized:
        raise RuntimeError("UMI formats have not completed initialization")

    _class_parser = FormatClassCreator(operator_metadata=_operator_metadata)

    _class_parser.register_compatible_formats()

    register_import_setting_class()

    panels.register()
    properties.register()


def unregister():

    global _class_parser
    global _initialized

    properties.unregister()
    panels.unregister()

    if _class_parser is not None:
        _class_parser.unregister_compatible_formats()
        _class_parser = None

    _initialized = False


def get_import_modules():
    modules = {}
    for f in COMPATIBLE_FORMATS.formats:
        module_items = [
            (m.upper(), m.title().replace("_", " "), f.operators.operators[m].description)
            for m in f.operators.operators.keys()
        ]
        c = ClassFactory(f"UMI_{f.name}_module", None, bpy.types.PropertyGroup)
        c.__annotations__["name"] = bpy.props.EnumProperty(items=module_items, name="Import Module")
        modules[f"{f.name}_module"] = c

        for name in f.operators.operators.keys():
            c = ClassFactory(f"UMI_{f.name}_{name}_settings", None, bpy.types.PropertyGroup)
            c.__annotations__["name"] = bpy.props.StringProperty(name="Import Setting Name", default=f"{f.name}_{name}")
            modules[f"{f.name}_{name}_settings"] = c

    return modules


modules = {}
