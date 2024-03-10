
def draw_no_settings(layout):
    box = layout.box()
    col = box.column(align=True)
    row = col.row(align=True)
    row.alignment = 'CENTER'
    row.label(text='No Settings')

from . import presets
from ....blender_version import BVERSION
from . import panel_abc, panel_blend, panel_dae, panel_fbx, panel_gltf, panel_obj, panel_ply, panel_stl, panel_svg, panel_usd, panel_x3d

def register():
    presets.register()

def unregister():
    presets.unregister()