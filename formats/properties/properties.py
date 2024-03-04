import bpy
from os import path
from .. import COMPATIBLE_FORMATS


def update_file_stats(self, context):

	if not context.scene.umi_settings.umi_file_stat_update:
		return
	
	selected_files = [f for f in context.scene.umi_settings.umi_file_selection if f.check]
	size = [f.size for f in selected_files]
	formats = []
	for f in selected_files:
		ext = path.splitext(f.name)[1].lower()
		if ext in formats:
			continue

		formats.append(ext)
	
	context.scene.umi_settings.umi_file_stat_selected_count = len(selected_files)
	context.scene.umi_settings.umi_file_stat_selected_size = sum(size)
	context.scene.umi_settings.umi_file_stat_selected_formats = '( ' + ' | '.join(formats) + ' )' if len(formats) else 'no'
	context.scene.umi_settings.umi_file_selected_format_items = str([(COMPATIBLE_FORMATS.get_format_from_extension(f)['name'].upper(), COMPATIBLE_FORMATS.get_format_from_extension(f)['name'].upper(), '') for f in formats])
	
class PG_ImportSettings(bpy.types.PropertyGroup):
	umi_import_settings_registered : bpy.props.BoolProperty(name='Import settings registered', default=False)
	umi_import_cancelled : bpy.props.BoolProperty(name='Import settings registered', default=False)

class PG_ImportSettingsCreator(bpy.types.PropertyGroup):
	name: bpy.props.StringProperty(name="Import Setting Name", default="")

class PG_Operator(bpy.types.PropertyGroup):
	operator : bpy.props.StringProperty(name='Operator', default='')

class PG_Preset(bpy.types.PropertyGroup):
	name : bpy.props.StringProperty(name='Name')
	path : bpy.props.StringProperty(name='File Path', default='', subtype='FILE_PATH')
	
class PG_FilePathSelection(bpy.types.PropertyGroup):
	name : bpy.props.StringProperty(name='Name')
	path : bpy.props.StringProperty(name='File Path', default='', subtype='FILE_PATH')
	check : bpy.props.BoolProperty(name='Check', default=True, update=update_file_stats)
	size : bpy.props.FloatProperty(name='FileSize', default=0.0)

class PG_SceneSettings(bpy.types.PropertyGroup):
	umi_file_selected_format_items : bpy.props.StringProperty(name='Selected format items')
	umi_ready_to_import : bpy.props.BoolProperty(name='Ready to Import', default=False)
	umi_last_setting_to_get : bpy.props.BoolProperty(name='Ready to Import', default=False)
	umi_batcher_is_processing : bpy.props.BoolProperty(name="Is Batcher Processing", default=False)
	umi_current_format_setting_imported : bpy.props.BoolProperty(name='Current Format Settings Imported', default=False)
	umi_current_format_setting_cancelled : bpy.props.BoolProperty(name='Current Format Settings cancelled', default=False)
	umi_file_selection_started : bpy.props.BoolProperty(name='File selection_started', default=False)
	umi_file_selection_done : bpy.props.BoolProperty(name='File Selected', default=False)
	umi_operators : bpy.props.CollectionProperty(type = PG_Operator)
	umi_operator_idx : bpy.props.IntProperty()
	umi_presets : bpy.props.CollectionProperty(type = PG_Preset)
	umi_preset_idx : bpy.props.IntProperty()
	umi_file_selection : bpy.props.CollectionProperty(type = PG_FilePathSelection)
	umi_file_selection_idx : bpy.props.IntProperty()
	umi_import_settings : bpy.props.PointerProperty(type=PG_ImportSettings)
	umi_file_extension_selection : bpy.props.EnumProperty(name='ext', items=[(e, e, '') for e in COMPATIBLE_FORMATS.extensions])
	umi_file_size_min_selection : bpy.props.FloatProperty( min=0, name='min (Mb)', default=0.0)
	umi_file_size_max_selection : bpy.props.FloatProperty( min=0, name='max (Mb)', default=1.0)
	umi_file_name_selection : bpy.props.StringProperty(name='name', default='')
	umi_file_name_case_sensitive_selection : bpy.props.BoolProperty(name='Case Sensitive', default=True)
	umi_file_name_include_folder_selection : bpy.props.BoolProperty(name='Include Folder', default=False)
	umi_file_stat_update : bpy.props.BoolProperty(name='update file stats', default=True)
	umi_file_stat_selected_count : bpy.props.IntProperty(name='file(s)', default=0)
	umi_file_stat_selected_size : bpy.props.FloatProperty(name='Mb', default=0)
	umi_file_stat_selected_formats : bpy.props.StringProperty(name='format(s)', default='')

class UMI_UL_OperatorList(bpy.types.UIList):
	bl_idname = "UMI_UL_operator_list"

	def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
		scn = context.scene

		grid = layout.grid_flow(columns=2, align=True, even_columns=True)
		row = grid.row()
		row.alignment = 'LEFT'
		row.label(text=f'{index + 1} : {item.operator}')

		row = grid.row(align=True)
		row.alignment = 'RIGHT'

		row.operator('scene.umi_edit_operator', text='', icon='GREASEPENCIL').id = index
		row.operator('scene.umi_duplicate_operator', text='', icon='PASTEDOWN').id = index
		row.separator()
		row.operator('scene.umi_remove_operator', text='', icon='PANEL_CLOSE').id = index

class UMI_UL_PresetList(bpy.types.UIList):
	bl_idname = "UMI_UL_preset_list"

	def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
		scn = context.scene

		grid = layout.grid_flow(columns=2, align=True, even_columns=True)
		row = grid.row()
		row.alignment = 'LEFT'
		row.label(text=f'{item.name}')

		row = grid.row(align=True)
		row.alignment = 'RIGHT'

		row.operator('scene.umi_edit_preset', text='', icon='GREASEPENCIL').id = index
		row.operator('scene.umi_duplicate_preset', text='', icon='PASTEDOWN').id = index
		row.separator()
		row.operator('scene.umi_load_preset_operator', text='', icon='TRIA_UP').filepath = item.path
		row.operator('scene.umi_save_preset_operator', text='', icon='PRESET_NEW').filepath = item.path
		row.separator()
		row.operator('scene.umi_remove_preset', text='', icon='PANEL_CLOSE').id = index
		
class UMI_UL_FileSelectionList(bpy.types.UIList):
	bl_idname = "UMI_UL_file_selection_list"

	def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
		scn = context.scene

		# grid = layout.grid_flow(columns=3, align=True, even_columns=True)
		row = layout.row(align=True)
		row.alignment = 'LEFT'
		row.prop(item, 'check', text='')
		row.label(text=f'{item.path}')
		row = layout.row(align=True)
		row.alignment = 'RIGHT'
		row.label(text=f'{round(item.size, 4)} MB')

classes = (PG_ImportSettings, 
		   PG_ImportSettingsCreator, 
		   PG_Operator, 
		   PG_Preset,
		   PG_FilePathSelection,
		   PG_SceneSettings, 
		   UMI_UL_OperatorList, 
		   UMI_UL_PresetList,
		   UMI_UL_FileSelectionList)

def register():
	from bpy.utils import register_class
	for cls in classes:
		register_class(cls)
	
	bpy.types.Scene.umi_settings = bpy.props.PointerProperty(type=PG_SceneSettings)

def unregister():
	del bpy.types.Scene.umi_settings

	from bpy.utils import unregister_class
	for cls in reversed(classes):
		unregister_class(cls)