import os, pathlib
import bpy

ADDON_FOLDER_PATH = os.path.dirname(__file__)
ADDON_PACKAGE = __package__
AUTOSAVE_PATH = os.path.join(pathlib.Path(bpy.utils.script_path_user()).parent.absolute(), 'autosave')

if not os.path.exists(AUTOSAVE_PATH):
    print(f'UMI : Creating Autosave Folder : {AUTOSAVE_PATH}')
    os.makedirs(AUTOSAVE_PATH, exist_ok=True)

def get_prefs():
    return bpy.context.preferences.addons[ADDON_PACKAGE].preferences

def get_umi_settings():
    return get_prefs().umi_settings

def get_umi_colors():
    try:
        prefs = get_prefs()
        return prefs.umi_colors
    except Exception as e:
        print(e)
        return None