from . import presets
from ....bversion import BVERSION, AddonVersion
from ....ui.panel import draw_panel, draw_no_settings, draw_version_warning, draw_prop
from . import panel_abc, panel_blend, panel_dae, panel_fbx, panel_gltf, panel_obj, panel_ply, panel_stl, panel_svg, panel_usd, panel_x3d

modules = (presets,)

def register():
    for m in modules:
        m.register()

def unregister():
    for m in reversed(modules):
        m.unregister()