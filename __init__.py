import bpy
from .umi_const import ADDON_FOLDER_PATH, ADDON_PACKAGE
from . import formats
from . import preferences
from . import operators

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

# TODO: check https://github.com/mika-f/blender-drag-and-drop for Drag and drop support

# function to append the operator in the File>Import menu
def menu_func_import(self, context):
	self.layout.operator(operators.OP_import.UMI.bl_idname, text="Universal Multi Importer", icon='LONGDISPLAY')

# function to append the operator in the File>Import menu
def menu_func_object(self, context):
	self.layout.separator()
	op = self.layout.operator(operators.OP_command_batcher.CommandBatcher.bl_idname, text="Command Batcher", icon='SHORTDISPLAY')
	op.importer_mode = False


def register():
	formats.register()
	preferences.register()
	operators.register()
	
	bpy.types.TOPBAR_MT_file_import.append(menu_func_import)
	bpy.types.VIEW3D_MT_object.append(menu_func_object)

def unregister():
	bpy.types.TOPBAR_MT_file_import.remove(menu_func_import)
	bpy.types.VIEW3D_MT_object.remove(menu_func_object)
	
	operators.unregister()
	preferences.unregister()
	formats.unregister()
	

if __name__ == "__main__":
	register()