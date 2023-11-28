import bpy

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

class PG_SceneSettings(bpy.types.PropertyGroup):
	umi_ready_to_import : bpy.props.BoolProperty(name='Ready to Import', default=False)
	umi_last_setting_to_get : bpy.props.BoolProperty(name='Ready to Import', default=False)
	umi_batcher_is_processing : bpy.props.BoolProperty(name="Is Batcher Processing", default=False)
	umi_current_format_setting_imported : bpy.props.BoolProperty(name='Current Format Settings Imported', default=False)
	umi_operators : bpy.props.CollectionProperty(type = PG_Operator)
	umi_operator_idx : bpy.props.IntProperty()
	umi_presets : bpy.props.CollectionProperty(type = PG_Preset)
	umi_preset_idx : bpy.props.IntProperty()
	umi_import_settings : bpy.props.PointerProperty(type=PG_ImportSettings)

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

classes = (PG_ImportSettings, 
		   PG_ImportSettingsCreator, 
		   PG_Operator, 
		   PG_Preset, 
		   PG_SceneSettings, 
		   UMI_UL_OperatorList, 
		   UMI_UL_PresetList)

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