import bpy
from .OP_ui_list_operators import *
from .constant import register_import_setting_class
from.property_group import *
from .OP_import import *
from .OP_class_creator import TILA_format_class_creator
from .UI_list import *
from .OP_command_batcher import *
from .OP_ui_list_operators import *
from .OP_ui_list_preset import *


bl_info = {
	"name" : "Universal Multi Importer",
	"author" : "Tilapiatsu",
	"description" : "",
	"blender" : (2, 93, 0),
	"location": "File > Import-Export",
	"warning" : "",
	"category": "Import-Export"
}
	

# function to append the operator in the File>Import menu
def menu_func_import(self, context):
	self.layout.operator(TILA_umi.bl_idname, text="Universal Multi Importer", icon='LONGDISPLAY')

# function to append the operator in the File>Import menu
def menu_func_object(self, context):
	self.layout.separator()
	op = self.layout.operator(TILA_umi_command_batcher.bl_idname, text="Command Batcher", icon='SHORTDISPLAY')
	op.importer_mode = False

classes = (
	TILA_UL_umi_operator_list,
	TILA_UL_umi_preset_list,
	TILA_umi_operator,
	TILA_umi_preset,
	TILA_umi_import_settings,
	TILA_umi_scene_settings,
	TILA_umi_settings,
	TILA_umi_command_batcher,
	TILA_umi,
	LM_UI_MoveOperator,
	LM_UI_ClearOperators,
	LM_UI_RemoveOperator,
	LM_UI_DuplicateOperator,
	LM_UI_EditOperator,
	LM_UI_AddOperator,
	LM_UI_MovePreset,
	LM_UI_ClearPresets,
	LM_UI_RemovePreset,
	LM_UI_DuplicatePreset,
	LM_UI_EditPreset,
	LM_UI_AddPreset,
	LM_UI_SavePresetOperator,
	LM_UI_LoadPresetList,
	LM_UI_LoadPresetOperator
)


def register():
	parser = TILA_format_class_creator()
	parser.register_compatible_formats()
	register_import_setting_class()
	
	for cls in classes:
		bpy.utils.register_class(cls)
	
	bpy.types.Scene.umi_settings = bpy.props.PointerProperty(type=TILA_umi_scene_settings)
	bpy.types.TOPBAR_MT_file_import.append(menu_func_import)
	bpy.types.VIEW3D_MT_object.append(menu_func_object)

def unregister():
	for cls in reversed(classes):
		bpy.utils.unregister_class(cls)
	parser = TILA_format_class_creator()
	parser.unregister_compatible_formats()
	del bpy.types.Scene.umi_settings
	bpy.types.TOPBAR_MT_file_import.remove(menu_func_import)
	bpy.types.VIEW3D_MT_object.remove(menu_func_object)

if __name__ == "__main__":
	register()