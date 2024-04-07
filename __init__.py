import bpy
from .umi_const import ADDON_FOLDER_PATH, ADDON_PACKAGE
from . import import_module


bl_info = {
	"name" : "Universal Multi Importer",
	"author" : "Tilapiatsu",
	"description" : "",
	"blender" : (2, 93, 0),
	"version": (2, 0, 1),
	"location": "File > Import-Export",
	"warning" : "",
	"category": "Import-Export"
}

def register():
	import_module.register()
	from . import preferences
	from . import operators
	preferences.register()
	operators.register()

def unregister():
	from . import preferences
	from . import operators
	operators.unregister()
	preferences.unregister()
	import_module.unregister()
	

if __name__ == "__main__":
	register()