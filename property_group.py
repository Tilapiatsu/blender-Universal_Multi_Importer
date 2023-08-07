import bpy


class TILA_import_settings_creator(bpy.types.PropertyGroup):
	name: bpy.props.StringProperty(name="Import Setting Name", default="")

class TILA_umi_import_settings(bpy.types.PropertyGroup):
	umi_import_settings_registered : bpy.props.BoolProperty(name='Import settings registered', default=False)

class TILA_umi_operator(bpy.types.PropertyGroup):
	operator : bpy.props.StringProperty(name='Operator', default='')

class TILA_umi_preset(bpy.types.PropertyGroup):
	name : bpy.props.StringProperty(name='Name')
	path : bpy.props.StringProperty(name='File Path', default='', subtype='FILE_PATH')

class TILA_umi_scene_settings(bpy.types.PropertyGroup):
	umi_ready_to_import : bpy.props.BoolProperty(name='Ready to Import', default=False)
	umi_last_setting_to_get : bpy.props.BoolProperty(name='Ready to Import', default=False)
	umi_current_format_setting_imported : bpy.props.BoolProperty(name='Current Format Settings Imported', default=False)
	umi_operators : bpy.props.CollectionProperty(type = TILA_umi_operator)
	umi_operator_idx : bpy.props.IntProperty()
	umi_presets : bpy.props.CollectionProperty(type = TILA_umi_preset)
	umi_preset_idx : bpy.props.IntProperty()
	umi_import_settings : bpy.props.PointerProperty(type=TILA_umi_import_settings)