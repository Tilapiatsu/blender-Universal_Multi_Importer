import os
import importlib
from universal_multi_importer.umi_const import EXTENSION_MODULE_NAME
from pathlib import Path
from universal_multi_importer.preferences.formats.panels import presets

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