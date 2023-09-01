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
from .preferences import *


bl_info = {
	"name" : "Universal Multi Importer",
	"author" : "Tilapiatsu",
	"description" : "",
	"blender" : (2, 93, 0),
	"version": (1, 0, 0),
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
	UMI_UI_MoveOperator,
	UMI_UI_ClearOperators,
	UMI_UI_RemoveOperator,
	UMI_UI_DuplicateOperator,
	UMI_UI_EditOperator,
	UMI_UI_AddOperator,
	UMI_UI_MovePreset,
	UMI_UI_ClearPresets,
	UMI_UI_RemovePreset,
	UMI_UI_DuplicatePreset,
	UMI_UI_EditPreset,
	UMI_UI_AddPreset,
	UMI_UI_SavePresetOperator,
	UMI_UI_LoadPresetList,
	UMI_UI_LoadPresetOperator,
	UMI_Preferences
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
	parser = TILA_format_class_creator()
	parser.unregister_compatible_formats()
	
	for cls in reversed(classes):
		bpy.utils.unregister_class(cls)
	del bpy.types.Scene.umi_settings
	bpy.types.TOPBAR_MT_file_import.remove(menu_func_import)
	bpy.types.VIEW3D_MT_object.remove(menu_func_object)

if __name__ == "__main__":
	register()