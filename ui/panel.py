from typing import Callable
from ..bversion import BVERSION
from ..bversion.addon_version import AddonVersion
from ..bversion.version import Version

def draw_prop(layout, operator, prop, text=None) -> None:
    if prop not in dir(operator):
        raise ValueError(f'Property "{prop}" not found in "{operator.addon_name}" addon')
    layout.prop(operator, prop, text=text)

def draw_panel(layout,
               props:list,
               idname:str,
               header_name:str,
               icon='NONE',
               default_closed=False,
               panel=None,
               header=None,
               set_header_boolean:bool=False,
               header_bool:str=None) -> tuple:

    if BVERSION >= 4.2:
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
            col = panel.column(align=True)
            for p in props:
                if len(p) == 2:
                    draw_prop(col, p[0], p[1])
                    # col.prop(p[0], p[1])
                elif len(p) == 3:
                    draw_prop(col, p[0], p[1], text=p[2])
                    # col.prop(p[0], p[1], text=p[2])
                col.separator(factor=0.5)

        return header, panel

    if header is None and panel is None:
        box = layout.box()
        header = box.row(align=True)
        if set_header_boolean:
            header.use_property_split = False
            header.prop(header_bool[0], header_bool[1], text="")
            header.label(text=header_name, icon=icon)
        else:
            header.label(text=header_name, icon=icon)

        panel = box.column(align=True)

    if panel:
        if set_header_boolean:
            panel.enabled = getattr(header_bool[0], header_bool[1])
        for p in props:
            if len(p) == 2:
                draw_prop(col, p[0], p[1])
                # panel.prop(p[0], p[1])
            elif len(p) == 3:
                draw_prop(col, p[0], p[1], text=p[2])
                # panel.prop(p[0], p[1], text=p[2])

    return header, panel

def draw_no_settings(layout) -> None:
    box = layout.box()
    col = box.column(align=True)
    row = col.row(align=True)
    row.alignment = 'CENTER'
    row.label(text='No Settings')

def draw_version_warning(f) -> Callable:
    def __wrapper(self, operator, module_name, layout):
        addon_version = AddonVersion(operator.addon_name)
        supported_version = Version(operator.supported_version)
        if addon_version.local_version != supported_version:
            box = layout.box()
            box.label(text=f'Installed {operator.addon_name} version : {addon_version.local_version}')
            box.label(text=f'supported {operator.addon_name} version : {operator.supported_version}')
            box.label(text=f'{operator.addon_name} version does NOT match the one supported by Universal Multi Importer.')
            box.label(text=f'Please check the update the {operator.name} in the preferences of the addon')

        elif not addon_version.is_enable:
            box = layout.box()
            box.label(text=f'{operator.addon_name} is disable, please enable it before moving forward', icon='WARNING_LARGE')
            box.operator('preferences.umi_draw_addon_dependency', icon='CHECKMARK', text='Check Addon Dependency')

        try:
            return f(self, operator, module_name, layout)
        except ValueError as e:
            layout.label(text=str(e), icon='WARNING_LARGE')
            box = layout.box()
            box.label(text=f'Please check the installed version of the addon "{operator.addon_name}":')
            box.operator('preferences.umi_draw_addon_dependency', icon='CHECKMARK', text='Check Addon Dependency')

            box = layout.box()
            box.label(text='Or report an issue :')
            box.operator('wm.url_open', icon='WARNING_LARGE', text='Report Issue').url='https://github.com/Tilapiatsu/blender-Universal_Multi_Importer/issues/new'

            return None
            # return f(self, operator, module_name, layout)
            # layout.operator()

    return __wrapper
