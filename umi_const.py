import os, pathlib
import bpy
from .bversion import BVERSION

ADDON_FOLDER_PATH = os.path.dirname(__file__)
ADDON_PACKAGE = __package__
AUTOSAVE_PATH = os.path.join(pathlib.Path(bpy.utils.script_path_user()).parent.absolute(), 'autosave')
WARNING_ICON = 'ERROR' if BVERSION < 4.3 else 'WARNING_LARGE'
DATATYPE_PREFIX = 'applies_to'

def get_datalist():
    datatype_list = [
                        'actions',
                        'armatures',
                        'brushes',
                        'cache_files',
                        'cameras',
                        'collections',
                        'curves',
                        'fonts',
                        'grease_pencils',
                        'images',
                        'lattices',
                        'libraries',
                        'lightprobes',
                        'lights',
                        'linestyles',
                        'masks',
                        'materials',
                        'meshes',
                        'metaballs',
                        'movieclips',
                        'node_groups',
                        'objects',
                        'paint_curves',
                        'palettes',
                        'particles',
                        'scenes',
                        'screens',
                        'shape_keys',
                        'sounds',
                        'speakers',
                        'texts',
                        'textures',
                        'volumes',
                        'window_managers',
                        'workspaces',
                        'worlds'
                    ]

    if BVERSION >= 3.1:
        datatype_list.append('pointclouds')

    if BVERSION >= 3.3:
        datatype_list.append('hair_curves')

    if BVERSION >= 4.3:
        datatype_list.append('grease_pencils_v3')

    datatype_list.sort()

    return datatype_list


DATATYPE_LIST = get_datalist()

def get_datatype_properties():
    datatype_result = ()
    for d in DATATYPE_LIST:
        default = False
        if d == 'objects':
            default = True

        datatype_result += ({'property': f'{DATATYPE_PREFIX}_{d}', 'type':'BOOLEAN', "default":default, 'name': d.replace("_", " ").title(), 'description':'', 'set':None},)

    return datatype_result


DATATYPE_PROPERTIES = get_datatype_properties()


def get_operator_items(self, context):
    return [(f'{d}', f'{d}', '') for d in dir(bpy.data) if not d.startswith('_') and isinstance(getattr(bpy.data, d), bpy.types.bpy_prop_collection)]

def get_operator_boolean():
    return [(f'{d}', f'{d.title()}') for d in dir(bpy.data) if not d.startswith('_') and isinstance(getattr(bpy.data, d), bpy.types.bpy_prop_collection)]

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

def get_operators_list():
    i = 0
    operators = []
    for op in dir(bpy.ops):
        for o in dir(getattr(bpy.ops, op)):
            operators.append((f'bpy.ops.{op}.{o}("INVOKE_DEFAULT")', str(i)))
            i += 1
    return operators

OPERTAOR_LIST = get_operators_list()

def init_current_item_index(umi_settings):
    umi_settings.umi_current_item_index.clear()
    for d in DATATYPE_LIST:
        index = umi_settings.umi_current_item_index.add()
        index.name = d