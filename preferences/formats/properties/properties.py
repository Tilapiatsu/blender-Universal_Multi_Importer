import bpy
from os import path
from ....logger import LOG
from ....umi_const import get_umi_settings, get_batcher_list_name, get_operator_items, get_operator_boolean, DATATYPE_PREFIX, DATATYPE_PROPERTIES
from .. import COMPATIBLE_FORMATS


def update_file_stats(self, context):
    umi_settings = get_umi_settings()
    if not umi_settings.umi_file_stat_update:
        return

    selected_files = [f for f in umi_settings.umi_file_selection if f.check]
    size = [f.size for f in selected_files]
    formats = []
    for f in selected_files:
        ext = path.splitext(f.name)[1].lower()
        if ext in formats:
            continue

        formats.append(ext)

    umi_settings.umi_file_stat_selected_count = len(selected_files)
    umi_settings.umi_file_stat_selected_size = sum(size)
    umi_settings.umi_file_stat_selected_formats = '( ' + ' | '.join(formats) + ' )' if len(formats) else 'no'
    file_selected_format_items = {( COMPATIBLE_FORMATS.get_format_from_extension(f).name.upper(), COMPATIBLE_FORMATS.get_format_from_extension(f).name.upper(), '') for f in formats}
    umi_settings.umi_file_selected_format_items = str(list(file_selected_format_items))
    umi_settings.umi_file_extension_selection = formats[0]

    if len(formats) and not len(umi_settings.umi_file_format_current_settings):
        f = COMPATIBLE_FORMATS.get_format_from_extension(formats[0]).name.upper()
        umi_settings.umi_file_format_current_settings = f

def update_file_format_current_settings(self, context):
    umi_settings = get_umi_settings()
    if len(umi_settings.umi_file_format_current_settings):
        if not len(umi_settings.umi_import_batch_settings):
            return
        umi_settings.umi_file_format_current_settings = set({})

def update_import_batch_settings(self, context):
    umi_settings = get_umi_settings()
    if len(umi_settings.umi_import_batch_settings):
        if not len(umi_settings.umi_file_format_current_settings):
            return
        umi_settings.umi_import_batch_settings = set({})

def get_file_selected_items(self, context):
    return eval(get_umi_settings().umi_file_selected_format_items)

def update_file_extension_selection(self, context):
    umi_settings = get_umi_settings()
    current_extensions = {e.ext.lower() for e in umi_settings.umi_file_selection if e.ext.lower() in COMPATIBLE_FORMATS.extensions}
    umi_settings.umi_file_extension_selection_items = str([(e, e, '') for e in current_extensions])

def get_file_extension_selection(self, context):
    file_extensions_selection_items = get_umi_settings().umi_file_extension_selection_items
    return eval(file_extensions_selection_items)

def update_log_drawing(self, context):
    umi_settings = get_umi_settings()
    LOG.show_log = umi_settings.umi_global_import_settings.show_log_on_3d_view

class PG_AddonDependency(bpy.types.PropertyGroup):
    name                : bpy.props.StringProperty(name='Name', default='')
    format_name         : bpy.props.StringProperty(name='Format Name', default='')
    module_name         : bpy.props.StringProperty(name='Format Name', default='')
    addon_name          : bpy.props.StringProperty(name='Addon Name', default='')
    pkg_id              : bpy.props.StringProperty(name='Package Index', default='')
    pkg_url             : bpy.props.StringProperty(name='Package URL', default='')
    local_version       : bpy.props.StringProperty(name='Local Version', default='')
    remote_version      : bpy.props.StringProperty(name='Remote Version', default='')
    supported_version   : bpy.props.StringProperty(name='Supported Version', default='')
    is_extension        : bpy.props.BoolProperty(name='Is Extension', default=False)
    is_installed        : bpy.props.BoolProperty(name='Is Installed', default=False)
    is_enabled          : bpy.props.BoolProperty(name='Is Enabled', default=False)
    is_outdated         : bpy.props.BoolProperty(name='Is Outdated', default=False)

class PG_ImportSettings(bpy.types.PropertyGroup):
    umi_import_settings_registered : bpy.props.BoolProperty(name='Import settings registered', default=False)
    umi_import_cancelled : bpy.props.BoolProperty(name='Import settings registered', default=False)

class PG_ImportSettingsCreator(bpy.types.PropertyGroup):
    name: bpy.props.StringProperty(name="Import Setting Name", default="")

class PG_Operator(bpy.types.PropertyGroup):
    enabled : bpy.props.BoolProperty(name='Enabled', default=True)
    operator : bpy.props.StringProperty(name='Operator', default='')

class PG_ItemIndex(bpy.types.PropertyGroup):
    name : bpy.props.StringProperty(name='Datatype Name', default='object')
    index : bpy.props.IntProperty(name='Index', default=0)

class PG_Preset(bpy.types.PropertyGroup):
    name : bpy.props.StringProperty(name='Name')
    path : bpy.props.StringProperty(name='File Path', default='', subtype='FILE_PATH')

class PG_ImportedData(bpy.types.PropertyGroup):
    name : bpy.props.StringProperty(name='Name')
    data : bpy.props.StringProperty(name='Data')
    data_type: bpy.props.StringProperty(name='Data Type')

class PG_FilePathSelection(bpy.types.PropertyGroup):
    name : bpy.props.StringProperty(name='Name')
    ext : bpy.props.StringProperty(name='Extension')
    path : bpy.props.StringProperty(name='File Path', default='', subtype='FILE_PATH')
    check : bpy.props.BoolProperty(name='Check', default=True, update=update_file_stats)
    size : bpy.props.FloatProperty(name='FileSize', default=0.0)
    md5 : bpy.props.StringProperty(name='MD5')

class PG_GlobalSettings(bpy.types.PropertyGroup):
    import_simultaneously_count : bpy.props.IntProperty(name="Max Simultaneously Files", default=200, min=1, description='Maximum number of file to import simultaneously')
    max_batch_size : bpy.props.FloatProperty(name="Max batch size (MB)", description="Max size per import batch. An import batch represents the number of files imported simultaneously", default=20, min=0)
    minimize_batch_number : bpy.props.BoolProperty(name="Minimize batch number", description="Try to pack files per batch in a way to be as close as possible to the Max batch size, and then minimize the number of import batches", default=True)
    create_collection_per_file : bpy.props.BoolProperty(name='Create collection per file', description='Each imported file will be placed in a collection', default=False)
    recreate_folder_structure_as_collections : bpy.props.BoolProperty(name='Recreate folder structure as collections', description='Recreate the folder structure from the hard drive into blender collections', default=False)
    backup_file_after_import : bpy.props.BoolProperty(name='Backup file during import', description='Backup file after importing file. The frequency will be made based on "Bakup Step Parameter"',  default=False)
    backup_step : bpy.props.FloatProperty(name='Backup Step (MB)', description='Backup file after X file(s) imported', default=100, min=1)
    skip_already_imported_files : bpy.props.BoolProperty(name='Skip already imported files', description='Import will be skipped if a Collection with the same name is found in the Blend file. "Create collection per file" need to be enabled', default=False)
    save_file_after_import : bpy.props.BoolProperty(name='Save file after import completed', description='Save the original file when the entire import process is complete', default=False)
    ignore_command_batcher_errors : bpy.props.BoolProperty(name='Ignore Command Batcher Errors', default=True, description='Disable it if you want to stop the process if an error occurs in the Command Batcher')
    show_log_on_3d_view : bpy.props.BoolProperty(name="Show Log on 3D View", default=True, update=update_log_drawing)
    auto_hide_text_when_finished : bpy.props.BoolProperty(name="Auto Hide Log When Finished", default=False)
    wait_before_hiding : bpy.props.FloatProperty(name="Wait Before Hiding (s)", default=5.0)
    force_refresh_viewport_after_each_import : bpy.props.BoolProperty(name="Refresh Viewport After Each Imported Files", default=False)
    force_refresh_viewport_after_each_command : bpy.props.BoolProperty(name="Refresh Viewport After Each Processed Command", default=True)
    force_refresh_viewport_after_time : bpy.props.FloatProperty(name="Refresh Viewport After time (s)", default=1.0, min=0, description='The viewport will refresh after the X seconds. It help to control viewport interactivity. A value of 0 will disable it, and the viewport will refresh after each batch')

class PG_UMISettings(bpy.types.PropertyGroup):
    umi_file_selected_format_items : bpy.props.StringProperty(name='Selected format items')
    umi_file_extension_selection_items : bpy.props.StringProperty(name='Selected extension items')
    umi_ready_to_import : bpy.props.BoolProperty(name='Ready to Import', default=False)
    umi_last_setting_to_get : bpy.props.BoolProperty(name='Last Setting to get', default=False)
    umi_batcher_is_processing : bpy.props.BoolProperty(name="Is Batcher Processing", default=False)
    umi_current_format_setting_imported : bpy.props.BoolProperty(name='Current Format Settings Imported', default=False)
    umi_current_format_setting_cancelled : bpy.props.BoolProperty(name='Current Format Settings cancelled', default=False)
    umi_file_selection_started : bpy.props.BoolProperty(name='File selection_started', default=False)
    umi_file_selection_done : bpy.props.BoolProperty(name='File Selected', default=False)
    umi_pre_operators : bpy.props.CollectionProperty(type = PG_Operator)
    umi_pre_operator_idx : bpy.props.IntProperty()
    umi_each_operators : bpy.props.CollectionProperty(type = PG_Operator)
    umi_each_operator_idx : bpy.props.IntProperty()
    umi_post_operators : bpy.props.CollectionProperty(type = PG_Operator)
    umi_post_operator_idx : bpy.props.IntProperty()
    umi_presets : bpy.props.CollectionProperty(type = PG_Preset)
    umi_preset_idx : bpy.props.IntProperty()
    umi_file_selection : bpy.props.CollectionProperty(type = PG_FilePathSelection)
    umi_file_selection_idx : bpy.props.IntProperty()
    umi_format_import_settings : bpy.props.PointerProperty(type=PG_ImportSettings)
    umi_global_import_settings : bpy.props.PointerProperty(type=PG_GlobalSettings)
    umi_skip_settings : bpy.props.BoolProperty(name='Skip Setting Windows', default=False)
    umi_file_extension_selection : bpy.props.EnumProperty(name='ext', items=get_file_extension_selection)
    umi_import_batch_settings : bpy.props.EnumProperty(items=[('IMPORT', 'Format Settings', ''), ('GLOBAL', 'Global Settings', ''), ('BATCHER', 'Command Batcher', '')])
    umi_command_batcher_settings : bpy.props.EnumProperty(items=[('PRE_PROCESS', 'Pre-Process', ''), ('EACH_ELEMENTS', 'Each Elements', ''), ('POST_PROCESS', 'Post-Process', '')], default='EACH_ELEMENTS')
    umi_file_format_current_settings : bpy.props.EnumProperty(items=get_file_selected_items)
    umi_file_size_min_selection : bpy.props.FloatProperty( min=0, name='min (Mb)', default=0.0)
    umi_file_size_max_selection : bpy.props.FloatProperty( min=0, name='max (Mb)', default=1.0)
    umi_file_name_selection : bpy.props.StringProperty(name='name', default='')
    umi_file_name_case_sensitive_selection : bpy.props.BoolProperty(name='Case Sensitive', default=True)
    umi_file_name_include_folder_selection : bpy.props.BoolProperty(name='Include Folder', default=False)
    umi_file_stat_update : bpy.props.BoolProperty(name='update file stats', default=True)
    umi_file_stat_selected_count : bpy.props.IntProperty(name='file(s)', default=0)
    umi_file_stat_selected_size : bpy.props.FloatProperty(name='Mb', default=0)
    umi_file_stat_selected_formats : bpy.props.StringProperty(name='format(s)', default='')
    umi_addon_dependencies : bpy.props.CollectionProperty(type = PG_AddonDependency)
    umi_all_addon_dependencies_installed : bpy.props.BoolProperty(name='All Addon Dependencies Installed', default=False)
    umi_all_addon_dependencies_enabled : bpy.props.BoolProperty(name='All Addon Dependencies Enabled', default=False)
    umi_addon_dependency_need_reboot : bpy.props.BoolProperty(name='Need Reboot', default=False)
    umi_md5_generation_status : bpy.props.EnumProperty(name='MD5 Generation Status', default='NOT_STARTED', items=[('NOT_STARTED', 'Not Started', ''), ('IN_PROGRESS', 'In Progress', ''), ('DONE', 'Done', '')])
    umi_show_import_settings : bpy.props.BoolProperty(name='Show Import Settings', default=True)
    umi_settings_dialog_width : bpy.props.FloatProperty(name='Dialog Width', min=0.0, max=1.0, default=0.65)
    umi_import_directory : bpy.props.BoolProperty(name='Import Directory', default=False)
    umi_window_width : bpy.props.IntProperty(name='Window Width (px)', min=500, default=1300)
    umi_current_item_index: bpy.props.CollectionProperty(type = PG_ItemIndex)
    umi_imported_data: bpy.props.CollectionProperty(type = PG_ImportedData)
    umi_valid_datatypes: bpy.props.BoolProperty(name='Valid Datatypes', default=False)
    umi_updating_batcher_variable: bpy.props.BoolProperty(name='Updating Batcher Variable', default=False)

class UMI_UL_OperatorList(bpy.types.UIList):
    bl_idname = "UMI_UL_operator_list"

    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        row = layout.row(align=True)

        row.prop(item, 'enabled', text='')
        row.label(text=f'{index + 1} : {item.operator}')

        row = row.row(align=True)
        row.alignment = 'RIGHT'

        row.operator('scene.umi_edit_operator', text='', icon='GREASEPENCIL').id = index
        row.operator('scene.umi_duplicate_operator', text='', icon='PASTEDOWN').id = index
        row.separator()
        row.operator('scene.umi_remove_operator', text='', icon='PANEL_CLOSE').id = index

class UMI_UL_PresetList(bpy.types.UIList):
    bl_idname = "UMI_UL_preset_list"

    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        row = layout.row(align=True)

        row.label(text=f'{item.name}')

        row = row.row(align=True)
        row.alignment = 'RIGHT'

        row.operator('scene.umi_edit_preset', text='', icon='GREASEPENCIL').id = index
        row.operator('scene.umi_duplicate_preset', text='', icon='PASTEDOWN').id = index
        row.separator()
        row.operator('scene.umi_load_preset_operator', text='', icon='TRIA_UP').filepath = item.path
        row.operator('scene.umi_save_preset_operator', text='', icon='PRESET_NEW').filepath = item.path
        row.separator()
        row.operator('scene.umi_remove_preset', text='', icon='PANEL_CLOSE').id = index

class UMI_UL_FileSelectionList(bpy.types.UIList):
    bl_idname = "UMI_UL_file_selection_list"

    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        scn = context.scene
        row = layout.row(align=True)
        row.prop(item, 'check', text='')
        row.separator()
        row.label(text=f'{item.path}')
        row = layout.row(align=True)
        row.alignment = 'RIGHT'
        row.label(text=f'{round(item.size, 4)} MB')

classes = ( PG_ImportSettings,
            PG_ImportSettingsCreator,
            PG_Preset,
            PG_FilePathSelection,
            PG_GlobalSettings,
            PG_AddonDependency,
            PG_ImportedData,
            PG_ItemIndex,
            PG_UMISettings,
            UMI_UL_OperatorList,
            UMI_UL_PresetList,
            UMI_UL_FileSelectionList)

datatype_classes = (PG_Operator,)

def register():
    from .... import class_property_injection
    class_property_injection.register(datatype_classes, DATATYPE_PROPERTIES)

    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)


def unregister():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)

    from .... import class_property_injection
    class_property_injection.unregister(datatype_classes, DATATYPE_PROPERTIES)