import os
import bpy
import importlib
from ....umi_const import EXTENSION_MODULE_NAME
from pathlib import Path
from . import presets
from ....bversion import BVERSION, AddonVersion
from ....ui.panel import draw_panel, draw_no_settings, draw_version_warning, draw_prop, draw_import_as_geometry_node_settings

panel_path = [p.name.replace('panel_', '').replace('.py', '') for p in Path(os.path.dirname(__file__)).iterdir() if p.name.startswith('panel_') ]

def get_panels(name: str):
    if name not in panel_path:
        return None

    m = importlib.import_module('.preferences.formats.panels.panel_' + name, EXTENSION_MODULE_NAME.module_name)

    panel = getattr(m, f'IMPORT_SCENE_{name.upper()}Settings')
    return panel


modules = (presets,)

def register():
    for m in modules:
        m.register()

def unregister():
    for m in reversed(modules):
        m.unregister()