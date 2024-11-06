
def draw_no_settings(layout):
    box = layout.box()
    col = box.column(align=True)
    row = col.row(align=True)
    row.alignment = 'CENTER'
    row.label(text='No Settings')

def draw_panel(layout, props:list, idname:str, header_name:str, icon='NONE', default_closed=False, panel=None, header=None, set_header_boolean:bool=False, header_bool:str=None):
    if header is None and panel is None:
        header, panel = layout.panel(idname=idname, default_closed=default_closed)
        if set_header_boolean:
            header.use_property_split = False
            header.prop(header_bool[0], header_bool[1], text="")
            header.label(text=header_name, icon=icon)
        else:
            header.label(text=header_name, icon=icon)

    if panel:
        if set_header_boolean:
            panel.enabled = getattr(header_bool[0], header_bool[1])
        for p in props:
            panel.prop(p[0], p[1])
    
    return header, panel

from . import presets
from ....blender_version import BVERSION
from . import panel_abc, panel_blend, panel_dae, panel_fbx, panel_gltf, panel_obj, panel_ply, panel_stl, panel_svg, panel_usd, panel_x3d


modules = (presets,)

def register():
    for m in modules:
        m.register()

def unregister():
    for m in reversed(modules):
        m.unregister()