import os, pathlib
import bpy
from .bversion import BVERSION

ADDON_FOLDER_PATH = os.path.dirname(__file__)
ADDON_PACKAGE = __package__
AUTOSAVE_PATH = os.path.join(pathlib.Path(bpy.utils.script_path_user()).parent.absolute(), 'autosave')
WARNING_ICON = 'ERROR' if BVERSION < 4.3 else 'WARNING_LARGE'

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
        return None

def get_batcher_list_name() -> str:
    umi_settings = get_umi_settings()
    match umi_settings.umi_command_batcher_settings:
        case "PRE_PROCESS":
            target = 'umi_pre_operators'
        case "EACH_ELEMENTS":
            target = 'umi_each_operators'
        case "POST_PROCESS":
            target = 'umi_post_operators'

    return target

def get_batcher_index_name() -> str:
    return get_batcher_list_name()+'_idx'
