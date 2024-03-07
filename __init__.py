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

def register():
	formats.register()
	preferences.register()
	operators.register()

def unregister():
	operators.unregister()
	preferences.unregister()
	formats.unregister()
	

if __name__ == "__main__":
	register()