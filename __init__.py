import bpy
from .umi_const import ADDON_FOLDER_PATH, ADDON_PACKAGE


bl_info = {
    "name"          : "Universal Multi Importer",
    "author"        : "Tilapiatsu",
    "description"   : "Batch Import many file formats at once, Batch process",
    "blender"       : (2, 93, 0),
    "version"       : (2, 0, 2),
    "location"      : "File > Import > Universal Multi Importer (File / Folder) | Object > Command Batcher",
    "warning"       : "",
    "doc_url"       : "https://github.com/Tilapiatsu/blender-Universal_Multi_Importer",
    "support"       : "COMMUNITY",
    "category"      : "Import-Export"
}

def register():
    from . import import_module
    import_module.register()
    from . import preferences
    from . import operators
    preferences.register()
    operators.register()

def unregister():
    from . import import_module
    from . import preferences
    from . import operators
    operators.unregister()
    preferences.unregister()
    import_module.unregister()
    

if __name__ == "__main__":
    register()