from typing import Callable
from ..bversion import BVERSION
from ..bversion.addon_version import AddonVersion
from ..bversion.version import Version
from ..umi_const import WARNING_ICON,  GITHUB_NEW_ISSUE_URL, EXTENSION_MODULE_NAME

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
        col = panel.column(align=True)
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

def draw_custom_panel(  layout,
                        idname,
                        header_name:str,
                        icon='NONE') -> tuple:

    if BVERSION >= 4.2:
        header, panel = layout.panel(idname=idname)
        header.label(text=header_name, icon=icon)
        return header, panel

    panel = layout.box()
    header = panel.row(align=True)
    header.label(text=header_name, icon=icon)
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

        if not addon_version.is_installed:
            header, panel = draw_custom_panel(layout, 'NotInstalled', 'Addon Not Installed', icon=WARNING_ICON)
            header.alert = True
            if panel:
                panel.alert = True
                panel.label(text=f'{operator.name} addon is not installed, you can fix dependencies with the button bellow')
                panel.operator('preferences.umi_draw_addon_dependency', icon='CHECKMARK', text='Check Addon Dependency')

        elif addon_version.local_version != supported_version:
            header, panel = draw_custom_panel(layout, 'VersionMismatch', 'Addon Version Mismatch', icon=WARNING_ICON)
            header.alert = True
            if panel:
                panel.alert = True
                panel.label(text=f'Installed {addon_version.pkg_name} version : {addon_version.local_version}')
                panel.label(text=f'supported {addon_version.pkg_name} version : {operator.supported_version}')
                panel.label(text='Installed version does NOT match the one supported by Universal Multi Importer.')
                if addon_version.local_version > supported_version:
                    panel.label(text='Please update Universal Multi Importer or report an issue :')
                    op = panel.operator('extensions.umi_install_extension', icon='FILE_REFRESH', text='Update Universal Multi Importer')
                    op.pkg_id = EXTENSION_MODULE_NAME.module_name
                    panel.operator("wm.url_open", text="Report Issue", icon='URL').url = GITHUB_NEW_ISSUE_URL
                else:
                    panel.label(text=f'Please update the {addon_version.pkg_name}')
                    op = panel.operator('extensions.umi_install_extension', icon='FILE_REFRESH', text=f'Update {addon_version.pkg_name} addon')
                    op.pkg_id = addon_version.pkg_name

        elif not addon_version.is_enable:
            header, panel = draw_custom_panel(layout, 'AddonDisabled', 'Addon Disabled', icon=WARNING_ICON)
            header.alert = True
            if panel:
                panel.alert = True
                panel.label(text=f'{addon_version.pkg_name} is disable, please enable it before moving forward', icon=WARNING_ICON)
                panel.operator('preferences.umi_addon_enable', icon='CHECKMARK', text=f'Enable {addon_version.pkg_name} addon')

        try:
            return f(self, operator, module_name, layout)
        except ValueError as e:
            header, panel = draw_custom_panel(layout, 'ImportSettingMismatch', 'Import Settings not found', icon=WARNING_ICON)
            header.alert = True
            if panel:
                panel.alert = True
                panel.label(text=str(e), icon=WARNING_ICON)
                box = panel.box()
                box.label(text=f'Please check the installed version of the addon "{addon_version.pkg_name}":')
                box.operator('preferences.umi_draw_addon_dependency', icon='CHECKMARK', text='Check Addon Dependency')

                box = panel.box()
                box.label(text='Or report an issue :')
                box.operator('wm.url_open', icon=WARNING_ICON, text='Report Issue').url='https://github.com/Tilapiatsu/blender-Universal_Multi_Importer/issues/new'

            return None
            # return f(self, operator, module_name, layout)
            # layout.operator()

    return __wrapper

def draw_import_as_geometry_node_settings(layout, operator, pannel_name:str) -> None:
    header, panel = draw_custom_panel(layout, pannel_name, 'Options', 'OPTIONS')
    row = panel.row(align=True)
    row.prop(operator, 'import_mode', expand=True)
    if operator.import_mode == "SEQUENCE":
        col = panel.column()
        col.alignment = 'RIGHT'
        col.label(text='Select only ONE file in the file selection panel,')
        col.label(text='the entire sequence will be detected automatically.')
        col.label(text='Each filename need to contain a number :')
        col.label(text='"base_file_name_0028.ext"')
        panel.prop(operator, 'loop_sequence')
