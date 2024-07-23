import bpy
from ..blender_version import BVERSION
from ..logger import LOG
from .formats.properties import PG_UMISettings
from .colors.presets import color_preset
from .colors.colors import PG_UMIColors
from .formats import COMPATIBLE_FORMATS
from .. import ADDON_PACKAGE


PREFERENCE_TABS = [ ("FORMATS", "Formats", ""),
                    ("COLORS", "Colors", "")]

def update_log_drawing(self, context):
    LOG.show_log = self.umi_settings.umi_global_import_settings.show_log_on_3d_view

def update_addon_dependency(self, context):
    if self.tabs == 'FORMATS':
        bpy.ops.preferences.umi_check_addon_dependency()

class Preferences(bpy.types.AddonPreferences):
    bl_idname = ADDON_PACKAGE

    umi_settings : bpy.props.PointerProperty(type = PG_UMISettings)

    umi_colors 	 : bpy.props.PointerProperty(type= PG_UMIColors)

    tabs: bpy.props.EnumProperty(name="Tabs", items=PREFERENCE_TABS, default="FORMATS", update=update_addon_dependency)
    
    
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
            col = box.row(align=True)
            col.label(text='Installed Formats', icon='DOCUMENTS')
            col.operator('preferences.umi_check_addon_dependency', icon='FILE_REFRESH')
            
            if self.umi_settings.umi_all_addon_dependencies_installed and self.umi_settings.umi_all_addon_dependencies_enabled and not self.umi_settings.umi_addon_dependency_need_reboot:
                bbox = box.box()
                bbox.label(text=f'All formats are installed/enabled properly', icon='CHECKMARK')
            elif self.umi_settings.umi_all_addon_dependencies_installed and self.umi_settings.umi_all_addon_dependencies_enabled and self.umi_settings.umi_addon_dependency_need_reboot:
                bbox = box.box()
                bbox.label(text=f'All formats are installed/enabled properly, but before it fully works, you will have to :', icon='ERROR')
                col = bbox.column(align=True)
                col.label(text=f'Disable Universal Multi Importer Addon', icon='RADIOBUT_ON')
                col.label(text=f'Restart Blender', icon='RADIOBUT_ON')
                col.label(text=f'Enable Universal Multi Importer Addon again', icon='RADIOBUT_ON')
            else:
                bbox = box.box()
                bbox.label(text=f'Some formats are currently not installed/enabled. If you want to use them with this addon, you will have to :', icon='ERROR')
                col = bbox.column(align=True)
                col.label(text=f'Install/Enable the missing formats by clicking on the install/enable button bellow', icon='RADIOBUT_ON')
                col.label(text=f'Disable Universal Multi Importer Addon', icon='RADIOBUT_ON')
                col.label(text=f'Restart Blender', icon='RADIOBUT_ON')
                col.label(text=f'Enable Universal Multi Importer Addon again', icon='RADIOBUT_ON')

            for ad in addon_dependencies.values():
                name = ad.format_name
                addon_name = ad.addon_name if len(ad.addon_name) else f'Builtin {ad.module_name}'

                if not len(ad.addon_name):
                    box.label(text=f'{name} : {addon_name} addon installed/enabled properly', icon='CHECKMARK')

                elif ad.is_enabled:
                    box.label(text=f'{name} : {addon_name} addon installed/enabled properly', icon='CHECKMARK')

                elif ad.is_installed and not ad.is_enabled:
                    bbox = box.box()
                    row = bbox.row(align=True)
                    row.label(text=f'{name} : {addon_name} addon is NOT enabled', icon='X')
                    op = row.operator('preferences.umi_addon_enable', text=f'Enable {addon_name} addon')
                    op.module = addon_name

                else:
                    bbox = box.box()
                    row = bbox.row(align=True)
                    row.label(text=f'{name} : {addon_name} addon is NOT Installed', icon='X')
                    if BVERSION < 4.2:
                        continue

                    if not context.preferences.system.use_online_access:
                        row.operator('extensions.userpref_allow_online', text='Allow Online Access')
                    
                    elif ad.is_extension:
                        op = row.operator('extensions.umi_install_extension', text=f'Install {name} Extension')
                        op.pkg_id = ad.pkg_id
                        op.repo_index = 0


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
            box.prop(self.umi_colors, 'umi_import_color')


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
