import os
from pathlib import Path
import bpy
from .bversion import BVERSION
from .module_name import ModuleName
ADDON_FOLDER_PATH = os.path.dirname(__file__)
ADDON_PACKAGE = __package__
AUTOSAVE_PATH = os.path.join(Path(bpy.utils.script_path_user()).parent.absolute(), 'autosave')
WARNING_ICON = 'ERROR' if BVERSION < 4.3 else 'WARNING_LARGE'
DATATYPE_PREFIX = 'applies_to'
MODIFIER_TYPES = [modifier.identifier for modifier in bpy.types.Modifier.bl_rna.properties['type'].enum_items]

def get_datalist():
    datatype_list = [
                        {'name':'actions',          'icon':'ACTION'},
                        {'name':'armatures',        'icon':'OUTLINER_OB_ARMATURE'},
                        {'name':'brushes',          'icon':'BRUSH_DATA'},
                        {'name':'cache_files',      'icon':'CAMERA_DATA'},
                        {'name':'cameras',          'icon':'FILE_CACHE'},
                        {'name':'collections',      'icon':'OUTLINER_COLLECTION'},
                        {'name':'curves',           'icon':'OUTLINER_OB_CURVE'},
                        {'name':'fonts',            'icon':'OUTLINER_OB_FONT'},
                        {'name':'grease_pencils',   'icon':'OUTLINER_OB_GREASEPENCIL'},
                        {'name':'images',           'icon':'IMAGE_DATA'},
                        {'name':'lattices',         'icon':'LATTICE_DATA'},
                        {'name':'libraries',        'icon':'LIBRARY_DATA_DIRECT'},
                        {'name':'lights',           'icon':'LIGHT'},
                        {'name':'linestyles',       'icon':'LINE_DATA'},
                        {'name':'masks',            'icon':'MOD_MASK'},
                        {'name':'materials',        'icon':'MATERIAL'},
                        {'name':'meshes',           'icon':'MESH_DATA'},
                        {'name':'metaballs',        'icon':'OUTLINER_OB_META'},
                        {'name':'modifiers',        'icon':'MODIFIER'},
                        {'name':'movieclips',       'icon':'FILE_MOVIE'},
                        {'name':'node_groups',      'icon':'NODETREE'},
                        {'name':'objects',          'icon':'OBJECT_DATA'},
                        {'name':'paint_curves',     'icon':'CURVE_BEZCURVE'},
                        {'name':'palettes',         'icon':'RESTRICT_COLOR_ON'},
                        {'name':'particles',        'icon':'PARTICLE_DATA'},
                        {'name':'scenes',           'icon':'SCENE_DATA'},
                        {'name':'shape_keys',       'icon':'SHAPEKEY_DATA'},
                        {'name':'sounds',           'icon':'PLAY_SOUND'},
                        {'name':'speakers',         'icon':'PLAY_SOUND'},
                        {'name':'texts',            'icon':'FILE_TEXT'},
                        {'name':'textures',         'icon':'TEXTURE'},
                        {'name':'volumes',          'icon':'VOLUME_DATA'},
                        {'name':'workspaces',       'icon':'WORKSPACE'},
                        {'name':'worlds',           'icon':'WORLD'}
                    ]


    if BVERSION >= 4.1:
        datatype_list.append({'name':'lightprobes', 'icon':'LIGHTPROBE_SPHERE'},)
    else:
        datatype_list.append({'name':'lightprobes', 'icon':'LIGHTPROBE_CUBEMAP'},)

    if BVERSION >= 3.1:
        datatype_list.append({'name':'pointclouds', 'icon':'OUTLINER_OB_FONT'})

    if BVERSION >= 3.3:
        datatype_list.append({'name':'hair_curves', 'icon':'OUTLINER_OB_CURVES'})

    if BVERSION >= 4.3:
        datatype_list.append({'name':'grease_pencils_v3', 'icon':'OUTLINER_OB_GREASEPENCIL'})

    datatype_list.sort(key=lambda name: name['name'])
    return datatype_list


DATATYPE_LIST = get_datalist()

def get_datatype_properties():
    datatype_result = ()
    for d in DATATYPE_LIST:
        default = False
        if d['name'] == 'objects':
            default = True

        datatype_result += ({'property': f'{DATATYPE_PREFIX}_{d["name"]}', 'type':'BOOLEAN', "default":default, 'name': d["name"].replace("_", " ").title(), 'description':'', 'set':None, 'icon':d['icon']},)
        if d["name"] == 'modifiers':
            items = [(i, i.replace('_', ' ').title(), '') for i in MODIFIER_TYPES]
            datatype_result += ({'property': 'modifier_type', 'type':'ENUM', "items":items, "default":MODIFIER_TYPES[0], 'name': d["name"].replace("_", " ").title() + ' Type', 'description':'Restrict the execution of the command to a specific modifier type', 'set':None, 'icon':d['icon']},)

    return datatype_result


DATATYPE_PROPERTIES = get_datatype_properties()
DATATYPE_PROPERTIES_DICT = {d['name']: d['property'] for d in DATATYPE_PROPERTIES}

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
    return get_batcher_list_name()[:-1]+'_idx'

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
        index.name = d['name']

EXTENSION_MODULE_NAME = ModuleName()