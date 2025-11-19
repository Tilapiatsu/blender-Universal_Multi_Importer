import bpy
from ....umi_const import get_umi_colors, ADDON_PACKAGE
from bl_ui.utils import PresetPanel
from bpy.types import Menu, Operator, Panel

from bl_operators.presets import AddPresetBase

class UMI_PT_color_presets(PresetPanel, Panel):
    bl_label = 'UMI Presets'
    preset_subdir = 'UMI/presets'
    preset_operator = 'script.execute_preset'
    preset_add_operator = 'umi.add_import_preset'


#  From https://sinestesia.co/blog/tutorials/using-blenders-presets-in-python/
class WM_MT_UMIColorPresets(Menu):
    bl_label = 'Color Presets'
    preset_subdir = 'UMI/presets'
    preset_operator = 'script.execute_preset'
    draw = Menu.draw_preset

    @property
    def preset_subdir(self):
        return AddUMIColorPreset.operator_path()

class AddUMIColorPreset(AddPresetBase, Operator):
    bl_idname = 'umi.add_color_preset'
    bl_label = 'Add UMI preset'
    preset_menu = 'WM_MT_UMIColorPresets'

    preset_defines = [
        f"umi_colors = bpy.context.preferences.addons['{ADDON_PACKAGE}'].preferences.umi_colors"
    ]

    skip_prop = ['name', 'settings_imported', 'bl_rna', 'addon_name', 'supported_version']

    @property
    def preset_subdir(self):
        return AddUMIColorPreset.operator_path()

    @property
    def preset_values(self):
        properties_blacklist = Operator.bl_rna.properties.keys()
        umi_settings = get_umi_colors()

        ret = []
        for s in dir(umi_settings):
            if s.startswith('__'):
                continue
            if s in self.skip_prop:
                continue
            if s not in properties_blacklist:
                ret.append(f"umi_colors.{s}")

        return ret

    @staticmethod
    def operator_path():
        import os
        folder = f'umi_color_presets'
        return os.path.join("umi", folder)

def panel_func(layout):
    row = layout.row(align=True)
    row.menu(WM_MT_UMIColorPresets.__name__, text=WM_MT_UMIColorPresets.bl_label)
    row.operator(AddUMIColorPreset.bl_idname, text="", icon='ADD')
    row.operator(AddUMIColorPreset.bl_idname, text="", icon='REMOVE').remove_active = True


classes = (WM_MT_UMIColorPresets, AddUMIColorPreset, UMI_PT_color_presets)

def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)

def unregister():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)