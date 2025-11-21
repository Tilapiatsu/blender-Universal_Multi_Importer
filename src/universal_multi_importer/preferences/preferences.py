import bpy
from universal_multi_importer.bversion import BVERSION
from universal_multi_importer.bversion.version.version import Version
from universal_multi_importer.logger import LOG
from universal_multi_importer.preferences.formats.properties.properties import PG_UMISettings
from universal_multi_importer.preferences.colors.presets import color_preset
from universal_multi_importer.preferences.colors.colors import PG_UMIColors
from universal_multi_importer.umi_const import ADDON_PACKAGE

PREFERENCE_TABS = [ ("FORMATS", "Formats", ""),
                    ("COLORS", "Colors", ""),
                    ("GENERAL", "General", "")]

def update_log_drawing(self, context):
    LOG.show_log = self.umi_settings.umi_global_import_settings.show_log_on_3d_view

def update_addon_dependency(self, context):
    if self.tabs == 'FORMATS':
        bpy.ops.preferences.umi_check_addon_dependency()

def grid_layout(layout, alignment, size):
    row = layout.row()
    row.alignment = alignment
    row.ui_units_x = size
    return row

def draw_addon_formats(context, layout, addon_dependencies, umi_settings):
    col = layout.row(align=True)
    col.label(text='Installed Formats', icon='DOCUMENTS')
    col.ui_units_x = 4

    bbox = layout.box()
    bbox.operator('preferences.umi_check_addon_dependency', icon='FILE_REFRESH')
    if not len(addon_dependencies):
        bbox.alert = True
        bbox.label(text=f'Addon dependency status have to be refreshed', icon='FILE_REFRESH')
    elif umi_settings.umi_all_addon_dependencies_installed and umi_settings.umi_all_addon_dependencies_enabled and not umi_settings.umi_addon_dependency_need_reboot:
        bbox.label(text=f'All formats are installed/enabled/updated properly', icon='CHECKMARK')
    elif umi_settings.umi_all_addon_dependencies_installed and umi_settings.umi_all_addon_dependencies_enabled and umi_settings.umi_addon_dependency_need_reboot:
        bbox.label(text=f'All formats are installed/enabled/updated properly, but before it fully works, you will have to :', icon='ERROR')
        col = bbox.column(align=True)
        col.alert = True
        col.label(text=f'Disable Universal Multi Importer Addon', icon='RADIOBUT_ON')
        col.label(text=f'Restart Blender', icon='RADIOBUT_ON')
        col.label(text=f'Enable Universal Multi Importer Addon again', icon='RADIOBUT_ON')
    else:
        bbox.label(text=f'Some formats are currently not installed/enabled/updated. If you want to use them with this addon, you will have to :', icon='ERROR')
        col = bbox.column(align=True)
        col.alert = True
        col.label(text=f'Install/Enable/Update the formats by clicking on the install/enable/update button below', icon='RADIOBUT_ON')
        col.label(text=f'Disable Universal Multi Importer Addon', icon='RADIOBUT_ON')
        col.label(text=f'Restart Blender', icon='RADIOBUT_ON')
        col.label(text=f'Enable Universal Multi Importer Addon again', icon='RADIOBUT_ON')

    main_box = layout.box()

    col1 = main_box.column(align=True)
    col2 = main_box.column(align=True)
    col3 = main_box.column(align=True)
    col4 = main_box.column(align=True)

    row1 = col1.row()
    row2 = col2.row()

    grid_layout(row1, alignment='CENTER', size=4).label(text='File Format')
    grid_layout(row1, alignment='CENTER', size=6).label(text='Addon')
    grid_layout(row1, alignment='CENTER', size=6).label(text='Version')
    grid_layout(row1, alignment='CENTER', size=4).label(text='Installed')
    grid_layout(row1, alignment='CENTER', size=4).label(text='Enable')

    grid_layout(row2, alignment='CENTER', size=4).label(text='_____')
    grid_layout(row2, alignment='CENTER', size=6).label(text='_____')
    grid_layout(row2, alignment='CENTER', size=6).label(text='_____')
    grid_layout(row2, alignment='CENTER', size=4).label(text='_____')
    grid_layout(row2, alignment='CENTER', size=4).label(text='_____')

    for ad in addon_dependencies.values():
        name = ad.format_name
        addon_name = ad.addon_name if len(ad.addon_name) else f'Built-in {ad.module_name}'
        supported_version = Version(ad.supported_version)
        local_version = Version(ad.local_version)

        need_update = ad.is_outdated and local_version < supported_version

        if not ad.is_installed and len(ad.addon_name) > 0:
            version = f'{ad.remote_version} available'
        elif need_update:
            version = f'{ad.local_version} (outdated {ad.remote_version})'
        else:
            version = f'{ad.local_version}' if ad.local_version != '0.0.0' else '-----'

        addon_diplay_name = addon_name.split('.')[2] if ad.is_extension else addon_name
        row = col3.row()

        grid_layout(row, alignment='CENTER', size=4).label(text=name)
        grid_layout(row, alignment='CENTER', size=6).label(text=addon_diplay_name)

        if not ad.is_installed and len(ad.addon_name) > 0:
            grid_layout(row, alignment='CENTER', size=6).label(text=version)
        elif need_update:
            if not context.preferences.system.use_online_access:
                grid_layout(row, alignment='CENTER', size=6).operator('extensions.userpref_allow_online', text=version, icon='INTERNET_OFFLINE')
            else:
                op = grid_layout(row, alignment='CENTER', size=6).operator('extensions.umi_install_extension', text=version, icon='FILE_REFRESH')
                op.pkg_id = ad.pkg_id
                op.repo_index = 0

        else:
            grid_layout(row, alignment='CENTER', size=6).label(text=version)

        if len(ad.addon_name) == 0:
            grid_layout(row, alignment='CENTER', size=4).label(text='', icon='CHECKMARK')

        # installed
        elif ad.is_installed:
            grid_layout(row, alignment='CENTER', size=4).label(text='', icon='CHECKMARK')
        else:
            if BVERSION < 4.2:
                op = grid_layout(row, alignment='CENTER', size=4).operator('wm.url_open', text=f'Open {name} url')
                op.url = ad.pkg_url
                grid_layout(row, alignment='CENTER', size=4).label(text='', icon='X')
                continue

            if not context.preferences.system.use_online_access:
                grid_layout(row, alignment='CENTER', size=4).operator('extensions.userpref_allow_online', text='Allow Online Access')

            elif ad.is_extension:
                op = grid_layout(row, alignment='CENTER', size=4).operator('extensions.umi_install_extension', text=f'Install {name}')
                op.pkg_id = ad.pkg_id
                op.repo_index = 0

            grid_layout(row, alignment='CENTER', size=4).label(text='', icon='X')

        # Enabled
        if ad.is_installed and ad.is_enabled or len(ad.addon_name) == 0:
            grid_layout(row, alignment='CENTER', size=4).label(text='', icon='CHECKMARK')

        elif ad.is_installed and not ad.is_enabled:
            op = grid_layout(row, alignment='CENTER', size=4).operator('preferences.umi_addon_enable', text=f'Enable {addon_name}')
            op.module = addon_name


class Preferences(bpy.types.AddonPreferences):
    bl_idname = ADDON_PACKAGE

    umi_settings : bpy.props.PointerProperty(type = PG_UMISettings)

    umi_colors 	 : bpy.props.PointerProperty(type= PG_UMIColors)

    tabs: bpy.props.EnumProperty(name="Tabs", items=PREFERENCE_TABS, default="FORMATS", update=update_addon_dependency)

    def grid_layout(self, layout, alignment, size):
        row = layout.row()
        row.alignment = alignment
        row.ui_units_x = size
        return row

    def draw(self, context):
        layout = self.layout
        column = layout.column(align=True)
        row = column.row()
        row.prop(self, "tabs", expand=True)

        addon_dependencies = self.umi_settings.umi_addon_dependencies

        box = column.box()
        box.use_property_split = True
        box.use_property_decorate = False
        if self.tabs == 'FORMATS':
            draw_addon_formats(context, box, addon_dependencies, self.umi_settings)

        elif self.tabs == "COLORS":
            col = box.row(align=True)
            col.label(text='Theme', icon='IMAGE_BACKGROUND')
            color_preset.panel_func(col)
            box.prop(self.umi_colors, 'umi_info_color')
            box.prop(self.umi_colors, 'umi_success_color')
            box.prop(self.umi_colors, 'umi_cancelled_color')
            box.prop(self.umi_colors, 'umi_warning_color')
            box.prop(self.umi_colors, 'umi_error_color')
            box.prop(self.umi_colors, 'umi_command_color')
            box.prop(self.umi_colors, 'umi_command_warning_color')
            box.prop(self.umi_colors, 'umi_import_color')

        elif self.tabs == 'GENERAL':
            box.prop(self.umi_settings, 'umi_window_width')


classes = (Preferences,)

def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)

def unregister():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)

if __name__ == "__main__":
    register()
