import bpy
from bl_ui.utils import PresetPanel
from bpy.types import Menu, Operator, Panel
from bpy.props import StringProperty

from bl_operators.presets import AddPresetBase

class UMI_PT_presets(PresetPanel, Panel):
	bl_label = 'UMI Presets' 
	preset_subdir = 'UMI/presets' 
	preset_operator = 'script.execute_preset' 
	preset_add_operator = 'umi.add_preset'
	

#  From https://sinestesia.co/blog/tutorials/using-blenders-presets-in-python/
class WM_MT_UMIPresets(Menu):
	bl_label = 'Import Presets'
	preset_subdir = 'UMI/presets'
	preset_operator = 'script.execute_preset' 
	draw = Menu.draw_preset

	@property
	def preset_subdir(self):
		current_format = bpy.context.scene.umi_settings.umi_file_format_current_settings.copy().pop().lower()
		current_module = eval(f'bpy.context.scene.umi_settings.umi_import_settings.{current_format}_import_module', {'bpy':bpy}).name.lower()
		return AddUMIPreset.operator_path(current_format, current_module)

class AddUMIPreset(AddPresetBase, Operator): 
	bl_idname = 'umi.add_preset' 
	bl_label = 'Add UMI preset' 
	preset_menu = 'WM_MT_UMIPresets' 
	
	operator: StringProperty(
		name="Operator",
		maxlen=64,
		options={'HIDDEN', 'SKIP_SAVE'},
	)

	preset_defines = [
		"umi_settings = bpy.context.scene.umi_settings.umi_import_settings"
	]

	skip_prop = ['name', 'settings_imported', 'bl_rna']

	@property
	def preset_subdir(self):
		current_format = bpy.context.scene.umi_settings.umi_file_format_current_settings.copy().pop().lower()
		current_module = eval(f'bpy.context.scene.umi_settings.umi_import_settings.{current_format}_import_module', {'bpy':bpy}).name.lower()
		return AddUMIPreset.operator_path(current_format, current_module)

	@property
	def preset_values(self):
		properties_blacklist = Operator.bl_rna.properties.keys()

		current_format = bpy.context.scene.umi_settings.umi_file_format_current_settings.copy().pop().lower()
		current_module = eval(f'bpy.context.scene.umi_settings.umi_import_settings.{current_format}_import_module', {'bpy':bpy}).name.lower()
		from ...format_handler import FormatHandler
		settings = FormatHandler(import_format=f"{current_format}", module_name=current_module, context=bpy.context).format_settings
		
		ret = []
		for s in dir(settings):
			if s.startswith('__'):
				continue
			if s in self.skip_prop:
				continue
			if s not in properties_blacklist:
				ret.append(f"umi_settings.{current_format}_{current_module}_import_settings.{s}")

		return ret

	@staticmethod
	def operator_path(current_format, current_module):
		import os
		folder = f'{current_format}_{current_module}_presets'
		return os.path.join("operator", folder)

def panel_func(self, context): 
	row = self.layout.row(align=True)
	row.menu(WM_MT_UMIPresets.__name__, text=WM_MT_UMIPresets.bl_label)
	row.operator(AddUMIPreset.bl_idname, text="", icon='ADD')
	row.operator(AddUMIPreset.bl_idname, text="", icon='REMOVE').remove_active = True


classes = (WM_MT_UMIPresets, AddUMIPreset, UMI_PT_presets)

def register():
	from bpy.utils import register_class
	for cls in classes:
		register_class(cls)

def unregister():
	from bpy.utils import unregister_class
	for cls in reversed(classes):
		unregister_class(cls)