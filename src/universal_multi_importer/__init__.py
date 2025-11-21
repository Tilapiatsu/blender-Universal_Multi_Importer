
bl_info = {
    "name"          : "Universal Multi Importer",
    "author"        : "Tilapiatsu <tilapiatsu@hotmail.fr>",
    "description"   : "Batch Import many file formats at once, Batch process them",
    "blender"       : (3, 0, 0),
    "version"       : (2, 3, 4),
    "location"      : "File > Import > Universal Multi Importer (File / Folder) | Object > Command Batcher",
    "warning"       : "",
    "doc_url"       : "https://github.com/Tilapiatsu/blender-Universal_Multi_Importer",
    "tracker_url"   : ("https://github.com/Tilapiatsu/blender-Universal_Multi_Importer/issues/new"),
    "support"       : "COMMUNITY",
    "category"      : "Import-Export"
}

def register():
    from universal_multi_importer import import_module
    import_module.register()
    from universal_multi_importer import preferences
    from universal_multi_importer import operators
    preferences.register()
    operators.register()

def unregister():
    from universal_multi_importer import import_module
    from universal_multi_importer import preferences
    from universal_multi_importer import operators
    operators.unregister()
    preferences.unregister()
    import_module.unregister()


if __name__ == "__main__":
    register()