import bpy
from mathutils import Vector, Euler, Color
from bpy_extras.io_utils import ImportHelper
import os, time
from os import path
from pathlib import Path
import math
from string import punctuation
from ..preferences.formats import FormatHandler, COMPATIBLE_FORMATS
from ..preferences.formats.properties.properties import update_file_stats, get_file_selected_items, update_file_extension_selection
from .OP_command_batcher import draw_command_batcher
from ..umi_const import get_umi_settings, AUTOSAVE_PATH, init_current_item_index
from ..preferences.formats.panels.presets import import_preset
from ..logger import LOG, LoggerColors, MessageType
from ..ui.panel import draw_panel
from ..bversion import BVERSION
from ..unique_name import UniqueName

# From https://gist.github.com/laundmo/b224b1f4c8ef6ca5fe47e132c8deab56
def lerp(a: float, b: float, t: float) -> float:
    """Linear interpolate on the scale given by a to b, using t as the point on that scale.
    Examples
    --------
        50 == lerp(0, 100, 0.5)
        4.2 == lerp(1, 5, 0.8)
    """
    return (1 - t) * a + t * b

if BVERSION >= 4.1:
    class IMPORT_SCENE_FH_UMI_3DVIEW(bpy.types.FileHandler):
        bl_idname = "IMPORT_SCENE_FH_UMI_3DVIEW"
        bl_label = "File handler for UMI on 3DView"
        bl_import_operator = "import_scene.tila_universal_multi_importer"
        bl_file_extensions = COMPATIBLE_FORMATS.extensions_string

        @classmethod
        def poll_drop(cls, context):
            return (context.area and context.area.type == 'VIEW_3D')

    class IMPORT_SCENE_FH_UMI_OUTLINER(bpy.types.FileHandler):
        bl_idname = "IMPORT_SCENE_FH_UMI_OUTLINER"
        bl_label = "File handler for UMI on Outliner"
        bl_import_operator = "import_scene.tila_drop_in_collection"
        bl_file_extensions = COMPATIBLE_FORMATS.extensions_string

        @classmethod
        def poll_drop(cls, context):
            return (context.area and context.area.type == 'OUTLINER' and context.area.spaces.active.display_mode in ['VIEW_LAYER'])

    class UMI_OT_Drop_In_Outliner(bpy.types.Operator):
        bl_idname = "import_scene.tila_drop_in_collection"
        bl_label = "Import ALL"
        bl_options = {'REGISTER', 'INTERNAL'}

        files : bpy.props.CollectionProperty(type=bpy.types.OperatorFileListElement, options={'SKIP_SAVE'})
        directory: bpy.props.StringProperty(name="Outdir Path", subtype='FILE_PATH')

        def execute(self, context):
            current_collection = context.collection
            current_object = context.object
            bpy.ops.outliner.item_activate('INVOKE_DEFAULT', extend=False, extend_range=False, deselect_all=True)

            if context.collection is None :
                self.report({'ERROR'}, 'UMI : Please Drop files on a Collection')
                return {'FINISHED'}

            if context.collection == current_collection and context.object != current_object:
                context.view_layer.active_layer_collection  = self.recur_layer_collection(context.view_layer.layer_collection, context.object.users_collection[0].name)

            files = []
            for f in self.files.values():
                files.append({'name':f.name})

            bpy.ops.import_scene.tila_universal_multi_importer("INVOKE_DEFAULT", import_folders=False, files=files, directory=self.directory)
            return {'FINISHED'}

        def recur_layer_collection(self, layer_coll, coll_name):
            found = None
            if (layer_coll.name == coll_name):
                return layer_coll
            for layer in layer_coll.children:
                found = self.recur_layer_collection(layer, coll_name)
                if found:
                    return found


# Legacy Settings Drawing
class UMI_OT_Settings(bpy.types.Operator):
    bl_idname = "import_scene.tila_universal_multi_importer_settings"
    bl_label = "Import Settings"
    bl_options = {'REGISTER', 'INTERNAL', 'PRESET'}
    bl_region_type = "UI"

    import_format : bpy.props.StringProperty(name='Import Format', default="", options={'HIDDEN'},)


    def unregister_annotations(self):
        for a in self.registered_annotations:
            del self.__class__.__annotations__[a]
        UMI_OT_Settings.bl_idname = f'import_scene.tila_universal_multi_importer_settings'
        bpy.utils.unregister_class(UMI_OT_Settings)
        bpy.utils.register_class(UMI_OT_Settings)

    def init_annotations(self):
        to_delete = []
        for a in self.__class__.__annotations__:
            if a in ['import_format']:
                continue
            to_delete.append(a)

        for a in to_delete:
            del self.__class__.__annotations__[a]

    def populate_property(self, property_name, property_value):
        self.__class__.__annotations__[property_name] = property_value

    def execute(self, context):
        self.umi_settings = get_umi_settings()
        # set the scene setting equal to the setting set by the user
        for k,v in self.__class__.__annotations__.items():
            if getattr(v, 'is_hidden', False) or getattr(v, 'is_readonly', False):
                continue
            if k in dir(self.format_handler.format_settings):
                try:
                    setattr(self.format_handler.format_settings, k, getattr(self, k))
                except AttributeError as e:
                    LOG.error("{}".format(e))

        if self.umi_settings.umi_last_setting_to_get:
            self.umi_settings.umi_ready_to_import = True

        self.umi_settings.umi_current_format_setting_imported = True
        self.unregister_annotations()

        return {'FINISHED'}

    def invoke(self, context, event):
        self.umi_settings = get_umi_settings()
        self.init_annotations()

        key_to_delete = []
        self.registered_annotations = []
        self.format_handler = eval(f'FormatHandler(import_format="{self.import_format}", module_name="default" context=cont)', {'self':self, 'FormatHandler':FormatHandler, 'cont':context})

        for k,v in self.format_handler.format_annotations.items():
            if getattr(v, 'is_hidden', False) or getattr(v, 'is_readonly', False):
                key_to_delete.append(k)

            if k in self.format_handler.format['ignore']:
                continue

            if self.format_handler.format_is_imported:
                if k in dir(self.format_handler.import_setting):
                    value = getattr(self.format_handler.import_setting, k)
                    self.populate_property(k, value)
                self.format_handler.format_settings.__annotations__[k] = value
                self.registered_annotations.append(k)
            else:
                self.populate_property(k, v)
                self.format_handler.format_settings.__annotations__[k] = v
                self.registered_annotations.append(k)

        for k in key_to_delete:
            del self.format_handler.format_annotations[k]

        UMI_OT_Settings.bl_label = f'{self.format_handler.format_name.upper()} Import Settings'
        UMI_OT_Settings.bl_idname = f'import_scene.tila_umi_{self.format_handler.format_name}_settings'

        bpy.utils.unregister_class(UMI_OT_Settings)
        bpy.utils.register_class(UMI_OT_Settings)

        wm = context.window_manager
        if len(self.format_handler.format_annotations)-2 > 0 :
            return wm.invoke_props_dialog(self)
        else:
            return self.execute(context)

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False
        col = layout.column()
        if len(self.format_handler.format_annotations):
            col.separator()
            for k in self.__class__.__annotations__.keys():
                if not k in ['name', 'settings_imported', 'import_format', 'ui_tab', 'addon_name', 'supported_version']:
                    col.prop(self, k)

    def cancel(self, context):
        UMI_OT_Settings.bl_idname = f'import_scene.tila_universal_multi_importer_settings'
        bpy.utils.unregister_class(UMI_OT_Settings)
        bpy.utils.register_class(UMI_OT_Settings)
        self.umi_settings.umi_current_format_setting_cancelled = True
        return {'CANCELLED'}


def register_import_format(self, context):
    for f in COMPATIBLE_FORMATS.formats:
        exec('self.{}_format = {{ }}'.format(f.name), {'self':self})
        current_format = eval(f'self.{f.name}_format')
        for _,name in enumerate(f.operators.operators.keys()):
            current_format[name] = FormatHandler(import_format=f"{f.name}", module_name=name, context=context)


class UMI_MD5Check(bpy.types.Operator):
    bl_idname = "import_scene.tila_universal_multi_importer_md5_check"
    bl_label = "Check MD5"
    bl_options = {'REGISTER', 'INTERNAL'}

    force : bpy.props.BoolProperty(name='Force Recompute MD5', default=False)

    file_to_process = []
    current_file = None

    # from https://stackoverflow.com/questions/3431825/how-to-generate-an-md5-checksum-of-a-file
    def md5(self, filepath):
        import hashlib
        hash_md5 = hashlib.md5()
        with open(filepath, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()

    def generate_md5(self):
        if not self.force and len(self.current_file.md5):
            self.current_file_processed = True
            return

        self.current_file.md5 = self.md5(self.current_file.path)
        LOG.info(f'MD5 for {self.current_file.path} = {self.current_file.md5}')
        bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)

        self.current_file_processed = True

    def init(self):
        self.umi_settings.umi_md5_generation_status = 'IN_PROGRESS'
        self.generating = False
        self.done = False
        self.canceled = False
        self.file_to_process = [f for f in self.umi_settings.umi_file_selection]
        self.current_file = self.file_to_process.pop()
        self.current_file_processed = False

    def finish(self, context, canceled=False):
        self.done = False
        self.generating = False
        context.window_manager.event_timer_remove(self._timer)
        bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)
        self.umi_settings.umi_md5_generation_status = 'DONE'
        if canceled:
            return {'CANCELLED'}
        else:
            return {'FINISHED'}

    def execute(self, context):
        self.umi_settings = get_umi_settings()
        self.init()
        wm = context.window_manager
        self._timer = wm.event_timer_add(0.01, window=context.window)
        wm.modal_handler_add(self)
        return {'RUNNING_MODAL'}

    def modal(self, context, event):
        if event.type in {'ESC'} and event.value == 'PRESS':
            return self.finish(context, canceled=True)
        elif event.type in {'TIMER'}:
            if not len(self.file_to_process) and self.current_file_processed:
                self.done = True

            if self.done:
                return self.finish(context)

            if not self.generating:
                self.generating = True
                self.generate_md5()

            else:
                if self.current_file_processed:
                    self.current_file = self.file_to_process.pop()
                    self.current_file_processed = False
                    self.generate_md5()

            return {'RUNNING_MODAL'}

        return {'PASS_THROUGH'}


class UMI_FileSelection(bpy.types.Operator):
    bl_idname = "import_scene.tila_universal_multi_importer_file_selection"
    bl_label = "Universal Multi Importer"
    bl_options = {'REGISTER', 'INTERNAL'}
    bl_region_type = "UI"
    bl_space_type = "TILA_SETTINGS"

    def invoke(self, context, event):
        self.umi_settings = get_umi_settings()
        self.umi_settings.umi_file_selection_started = True

        register_import_format(self, context)

        update_file_stats(self, context)
        wm = context.window_manager
        return wm.invoke_props_dialog(self, width=self.umi_settings.umi_window_width)

    def execute(self, context):
        self.umi_settings.umi_file_selection_done = True
        self.umi_settings.umi_ready_to_import = True

        self.umi_settings.umi_current_format_setting_imported = True
        return {'FINISHED'}

    def draw(self, context):
        layout = self.layout
        main_col = layout.column()
        row = main_col.row(align = True)
        row.alignment = 'RIGHT'
        row.prop(self.umi_settings, 'umi_show_import_settings', toggle=1, icon='OPTIONS')
        row.prop(self.umi_settings, 'umi_settings_dialog_width', slider=True)


        main_row = main_col.split(factor = lerp(0.1, 0.9, self.umi_settings.umi_settings_dialog_width) if self.umi_settings.umi_show_import_settings else 1.0)
        file_selection_col = main_row.column(align=True)
        file_selection_col.label(text='File Selection')
        file_selection_box = file_selection_col.box()

        row1 = file_selection_box.row(align=True)

        row1.separator()

        box = row1.box()
        box.ui_units_x = 3
        box.label(text='All')
        row2 = box.row(align=True)
        op = row2.operator('scene.umi_select_file', text='', icon='CHECKBOX_HLT')
        op.action = 'SELECT'
        op.mode = "ALL"
        op = row2.operator('scene.umi_select_file', text='', icon='CHECKBOX_DEHLT')
        op.action = 'DESELECT'
        op.mode = "ALL"

        row1.separator()

        box = row1.box()
        box.ui_units_x = 8
        box.label(text='Ext')
        row2 = box.row(align=True)
        op = row2.operator('scene.umi_select_file', text='', icon='CHECKBOX_HLT')
        op.action = 'SELECT'
        op.mode = "EXTENSION"
        op = row2.operator('scene.umi_select_file', text='', icon='CHECKBOX_DEHLT')
        op.action = 'DESELECT'
        op.mode = "EXTENSION"
        row2.separator()
        row2.prop(self.umi_settings, 'umi_file_extension_selection', text='')

        row1.separator()

        box = row1.box()
        box.label(text='Size')
        row2 = box.row(align=True)

        op = row2.operator('scene.umi_select_file', text='', icon='CHECKBOX_HLT', )
        op.action = 'SELECT'
        op.mode = "SIZE"
        op = row2.operator('scene.umi_select_file', text='', icon='CHECKBOX_DEHLT')
        op.action = 'DESELECT'
        op.mode = "SIZE"
        row2.separator()
        row2.prop(self.umi_settings, 'umi_file_size_min_selection')
        row2.prop(self.umi_settings, 'umi_file_size_max_selection')

        row1.separator()

        row1 = file_selection_box.row(align=True)
        box = row1.box()
        box.label(text='Name')
        row2 = box.row(align=True)
        op = row2.operator('scene.umi_select_file', text='', icon='CHECKBOX_HLT', )
        op.action = 'SELECT'
        op.mode = "NAME"
        op = row2.operator('scene.umi_select_file', text='', icon='CHECKBOX_DEHLT')
        op.action = 'DESELECT'
        op.mode = "NAME"
        row2.separator()
        row2.prop(self.umi_settings, 'umi_file_name_selection', text='')
        row2.prop(self.umi_settings, 'umi_file_name_case_sensitive_selection', text='', icon='SYNTAX_OFF')
        row2.prop(self.umi_settings, 'umi_file_name_include_folder_selection', text='', icon='FILEBROWSER')

        box = row1.box()
        box.ui_units_x = 2
        box.label(text='Duplicates')
        row2 = box.row(align=True)
        op = row2.operator('scene.umi_select_file', text='', icon='CHECKBOX_HLT', )
        op.action = 'SELECT'
        op.mode = "MD5"
        op = row2.operator('scene.umi_select_file', text='', icon='CHECKBOX_DEHLT')
        op.action = 'DESELECT'
        op.mode = "MD5"

        row2 = file_selection_box.row(align=True)
        row2.alignment = 'LEFT'
        row2.label(text=str(self.umi_settings.umi_file_stat_selected_count) + ' file(s)  |  ')
        row2.label(text=str(round(self.umi_settings.umi_file_stat_selected_size, 4)) + ' Mb')
        file_selection_box.label(text=self.umi_settings.umi_file_stat_selected_formats + ' format(s) selected')

        main_col.separator()

        rows = min(len(self.umi_settings.umi_file_selection) if len(self.umi_settings.umi_file_selection) > 2 else 2, 20)
        col1 = file_selection_box.column()
        col1.template_list('UMI_UL_file_selection_list', '', self.umi_settings, 'umi_file_selection', self.umi_settings, 'umi_file_selection_idx', rows=rows)

        if self.umi_settings.umi_show_import_settings:
            col1 = main_row.column()
            col1.label(text='Import Settings')

            box = col1.box()
            col2 = box.column(align=True)
            row1 = col2.row(align=True)
            row1.prop_tabs_enum(self.umi_settings, 'umi_import_batch_settings')
            row1 = col2.row(align=True)

            if self.umi_settings.umi_import_batch_settings == 'IMPORT':
                if len(self.umi_settings.umi_file_extension_selection) and len(get_file_selected_items(self, context)):
                    row1.prop_tabs_enum(self.umi_settings, 'umi_file_format_current_settings')
                    col1.separator()

                    if len(self.umi_settings.umi_file_format_current_settings):
                        current_setting_name = self.umi_settings.umi_file_format_current_settings.lower()
                        self.draw_current_settings(context, box, current_setting_name)
                else:
                    row1.alignment = 'CENTER'
                    row1.label(text='Select at least one file')

            elif self.umi_settings.umi_import_batch_settings == 'GLOBAL':
                col1.separator()
                import_preset.panel_func(box)
                self.draw_global_settings(context, box)
            elif self.umi_settings.umi_import_batch_settings == 'BATCHER':
                col1.separator()
                draw_command_batcher(self, context, box)

    def draw_current_settings(self, context, layout, format_name):
        layout.use_property_split = True
        layout.use_property_decorate = False
        col = layout.column()
        current_format = eval(f'self.{format_name}_format')
        if len(current_format.keys()) > 1:
            row = col.row()
            row.prop(eval(f"self.umi_settings.umi_format_import_settings.{format_name}_import_module", {'self':self}), 'name' , expand=True)
            col.separator()

        current_module = eval(f'self.umi_settings.umi_format_import_settings.{format_name}_import_module', {'self':self}).name.lower()
        current_settings = current_format[current_module]
        COMPATIBLE_FORMATS.draw_format_settings(context, format_name, current_settings.format_settings, current_module, col)

    def draw_global_settings(self, context, layout):
        layout.use_property_split = True
        layout.use_property_decorate = False
        col = layout.column()
        if BVERSION >= 4.2:
            header, import_count = col.panel(idname='UMI_Filecount')
            header.label(text='File Count', icon='LONGDISPLAY')
            if import_count:
                import_count.prop(self.umi_settings.umi_global_import_settings, 'import_simultaneously_count')
                import_count.prop(self.umi_settings.umi_global_import_settings, 'max_batch_size')
                if self.umi_settings.umi_global_import_settings.max_batch_size:
                    import_count.prop(self.umi_settings.umi_global_import_settings, 'minimize_batch_number')
                import_count.prop(self.umi_settings.umi_global_import_settings, 'force_refresh_viewport_after_time')

            header, settings = col.panel(idname='UMI_Options')
            header.label(text='Options', icon='OPTIONS')
            if settings:
                if self.umi_settings.umi_import_directory:
                    settings.prop(self.umi_settings.umi_global_import_settings, 'recreate_folder_structure_as_collections')

                settings.prop(self.umi_settings.umi_global_import_settings, 'create_collection_per_file')

                if self.umi_settings.umi_global_import_settings.create_collection_per_file:
                    row = settings.row()
                    split = row.split(factor=0.1, align=True)
                    split.label(text='')
                    split = split.split()
                    split.prop(self.umi_settings.umi_global_import_settings, 'skip_already_imported_files')

            header, log = col.panel(idname='UMI_LogDisplay')
            header.label(text='Log Display', icon='WORDWRAP_ON')
            if log:

                column = log.column(align=True)

                column.prop(self.umi_settings.umi_global_import_settings, 'show_log_on_3d_view')
                if self.umi_settings.umi_global_import_settings.show_log_on_3d_view:
                    column.prop(self.umi_settings.umi_global_import_settings, 'auto_hide_text_when_finished')
                    if self.umi_settings.umi_global_import_settings.auto_hide_text_when_finished:
                        column.prop(self.umi_settings.umi_global_import_settings, 'wait_before_hiding')
                column.prop(self.umi_settings.umi_global_import_settings, 'force_refresh_viewport_after_each_import')
                column.prop(self.umi_settings.umi_global_import_settings, 'force_refresh_viewport_after_each_command')


            header, backup = col.panel(idname='UMI_backup')
            header.label(text='backup', icon='FILE_TICK')
            if backup:
                col1 = backup.column()
                col1.prop(self.umi_settings.umi_global_import_settings, 'save_file_after_import')
                col1.prop(self.umi_settings.umi_global_import_settings, 'backup_file_after_import')

                if self.umi_settings.umi_global_import_settings.backup_file_after_import:
                    backup.prop(self.umi_settings.umi_global_import_settings, 'backup_step')
        else:
            import_count = layout.box()
            header = import_count.row(align=True)
            header.label(text='File Count', icon='LONGDISPLAY')
            import_count.prop(self.umi_settings.umi_global_import_settings, 'import_simultaneously_count')
            import_count.prop(self.umi_settings.umi_global_import_settings, 'max_batch_size')
            if self.umi_settings.umi_global_import_settings.max_batch_size:
                import_count.prop(self.umi_settings.umi_global_import_settings, 'minimize_batch_number')


            settings = layout.box()
            header = settings.row(align=True)
            header.label(text='Options', icon='OPTIONS')
            if self.umi_settings.umi_import_directory:
                settings.prop(self.umi_settings.umi_global_import_settings, 'recreate_folder_structure_as_collections')
            settings.prop(self.umi_settings.umi_global_import_settings, 'create_collection_per_file')

            if self.umi_settings.umi_global_import_settings.create_collection_per_file:
                row = settings.row()
                split = row.split(factor=0.1, align=True)
                split.label(text='')
                split = split.split()
                split.prop(self.umi_settings.umi_global_import_settings, 'skip_already_imported_files')

            log = layout.box()
            header = log.row(align=True)
            header.label(text='Log Display', icon='WORDWRAP_ON')
            column = log.column(align=True)

            column.prop(self.umi_settings.umi_global_import_settings, 'show_log_on_3d_view')
            if self.umi_settings.umi_global_import_settings.show_log_on_3d_view:
                column.prop(self.umi_settings.umi_global_import_settings, 'auto_hide_text_when_finished')
                if self.umi_settings.umi_global_import_settings.auto_hide_text_when_finished:
                    column.prop(self.umi_settings.umi_global_import_settings, 'wait_before_hiding')
            column.prop(self.umi_settings.umi_global_import_settings, 'force_refresh_viewport_after_each_import')
            column.prop(self.umi_settings.umi_global_import_settings, 'force_refresh_viewport_after_each_command')


            backup = layout.box()
            header = backup.row(align=True)
            header.label(text='Backup', icon='FILE_TICK')
            col1 = backup.column()
            col1.prop(self.umi_settings.umi_global_import_settings, 'save_file_after_import')
            col1.prop(self.umi_settings.umi_global_import_settings, 'backup_file_after_import')

            if self.umi_settings.umi_global_import_settings.backup_file_after_import:
                backup.prop(self.umi_settings.umi_global_import_settings, 'backup_step')

    def cancel(self, context):
        self.umi_settings.umi_current_format_setting_cancelled = True
        return {'CANCELLED'}


class UMI(bpy.types.Operator, ImportHelper):
    bl_idname = "import_scene.tila_universal_multi_importer"
    bl_label = "Import ALL"
    bl_options = {'REGISTER', 'INTERNAL'}
    bl_region_type = "UI"
    bl_description = 'Import multiple files of different formats from the same import dialog. You can also scan folders and subfolders to import everything inside.'

    # Supported File Extensions
    filename_ext = COMPATIBLE_FORMATS.filename_ext
    filter_glob: bpy.props.StringProperty(default=COMPATIBLE_FORMATS.filter_glob, options={"HIDDEN", "SKIP_SAVE"})
    filter_folder: bpy.props.BoolProperty(default=True, options = {"HIDDEN", "SKIP_SAVE"})
    filter_blender : bpy.props.BoolProperty(default=True, options={"HIDDEN", "SKIP_SAVE"})
    filter_usd : bpy.props.BoolProperty(default=True, options={"HIDDEN", "SKIP_SAVE"})
    filter_obj : bpy.props.BoolProperty(default=True, options={"HIDDEN", "SKIP_SAVE"})
    filter_fbx : bpy.props.BoolProperty(default=True, options={"HIDDEN", "SKIP_SAVE"})
    filter_image : bpy.props.BoolProperty(default=True, options={"HIDDEN", "SKIP_SAVE"})
    filter_movie : bpy.props.BoolProperty(default=True, options={"HIDDEN", "SKIP_SAVE"})
    filter_sound : bpy.props.BoolProperty(default=True, options={"HIDDEN", "SKIP_SAVE"})
    filter_collada : bpy.props.BoolProperty(default=True, options={"HIDDEN", "SKIP_SAVE"})
    filter_alembic : bpy.props.BoolProperty(default=True, options={"HIDDEN", "SKIP_SAVE"})
    filter_volume : bpy.props.BoolProperty(default=True, options={"HIDDEN", "SKIP_SAVE"})
    filter_ply : bpy.props.BoolProperty(default=True, options={"HIDDEN", "SKIP_SAVE"})
    filter_gltf : bpy.props.BoolProperty(default=True, options={"HIDDEN", "SKIP_SAVE"})
    filter_x3d : bpy.props.BoolProperty(default=True, options={"HIDDEN", "SKIP_SAVE"})
    filter_stl : bpy.props.BoolProperty(default=True, options={"HIDDEN", "SKIP_SAVE"})
    filter_svg : bpy.props.BoolProperty(default=True, options={"HIDDEN", "SKIP_SAVE"})


    # Selected files
    files : bpy.props.CollectionProperty(type=bpy.types.OperatorFileListElement, options={'SKIP_SAVE'})
    # Support Folder selection
    import_folders : bpy.props.BoolProperty(name="Import Folder",default=False, options={'SKIP_SAVE'})
    directory: bpy.props.StringProperty(name="Outdir Path", subtype='FILE_PATH')
    # Import Settings
    recursion_depth : bpy.props.IntProperty(name='Recursion Depth', default=0, min=0, description='How many Subfolders will be used to search for compatible files to import.\n' + r'/!\ WARNING : A too high number may result of a huge number of files to import and may cause instability')

    _timer = None
    thread = None
    progress = 0
    current_files_to_import = None
    importing = False
    processing = False
    all_parameters_imported = False
    first_setting_to_import = True
    formats_to_import = []
    import_complete = False
    canceled = False
    import_complete = False
    current_backup_step = 0
    counter = 0
    counter_start_time = 0.0
    counter_end_time = 0.0
    _timer_start_time = 0.0
    delta = 0.0
    previous_counter = 0

    @property
    def filepaths(self):
        if self._filepaths is None:
            compatible_extensions = self.compatible_extensions

            if self.import_folders:
                self._filepaths = self.get_compatible_files_in_folder(self.directory, recursion_depth=self.recursion_depth)
            else:
                self._filepaths = [path.join(self.directory, f.name) for f in self.files if path.splitext(f.name)[1].lower() in compatible_extensions]

        return self._filepaths

    @filepaths.setter
    def filepaths(self, value):
        self._filepaths = value

    @property
    def compatible_extensions(self):
        return COMPATIBLE_FORMATS.extensions

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False

        if self.import_folders:
            options = layout.box()
            options.label(text='Options', icon='OPTIONS')
            options.prop(self, 'recursion_depth')

    def invoke(self, context, event):
        self.umi_settings = get_umi_settings()
        self.umi_settings.umi_batcher_is_processing = False
        bpy.ops.scene.umi_load_preset_list()

        # If one blend file is dropped, skip UMI to let blender handle it
        if len(self.files) == 1 and path.splitext(self.files[0].name)[1].lower() == '.blend':
            bpy.ops.wm.drop_blend_file('INVOKE_DEFAULT', filepath=self.filepath)
            return {'FINISHED'}

        if self.directory and not self.import_folders and len(self.files):
            if event.shift:
                self.umi_settings.umi_skip_settings = True
            return self.execute(context)

        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

    def init_progress(self):
        self.number_of_files = len(self.filepaths)
        self.number_of_operations = self.number_of_files
        self.total_import_size = self.get_total_size(self.filepaths)

    def decrement_counter(self):
        self.counter = self.counter + (self.counter_start_time - self.counter_end_time)*1000

    def store_delta_start(self):
        self.counter_start_time = time.perf_counter()

    def store_delta_end(self):
        self.counter_end_time = time.perf_counter()

    @property
    def refresh_timer(self):
        if self.umi_settings.umi_global_import_settings.force_refresh_viewport_after_time:
            return self.timer_start_time + self.umi_settings.umi_global_import_settings.force_refresh_viewport_after_time - time.perf_counter()
        return 1

    @property
    def timer_start_time(self):
        if self._timer_start_time == 0:
            self._timer_start_time = time.perf_counter()
        return self._timer_start_time

    def store_timer_start(self):
        self._timer_start_time = time.perf_counter()

    def log_end_text(self):
        LOG.info('-----------------------------------')
        if self.import_complete:
            if False in self.files_succeeded:
                LOG.info('Batch Import completed with errors !', color=LoggerColors.ERROR_COLOR())
                LOG.esc_message = '[Esc] to Hide'
                LOG.message_offset = 4
            else:
                LOG.info('Batch Import completed successfully !', color=LoggerColors.SUCCESS_COLOR())
                LOG.esc_message = '[Esc] to Hide'
                LOG.message_offset = 4
        else:
            LOG.info('Batch Import cancelled !', color=LoggerColors.CANCELLED_COLOR())

        LOG.info('Click [ESC] to hide this text ...')
        LOG.info('-----------------------------------')
        self.end_text_written = True
        bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)

    def recur_layer_collection(self, layer_coll, coll_name):
        found = None
        if (layer_coll.name == coll_name):
            return layer_coll
        for layer in layer_coll.children:
            found = self.recur_layer_collection(layer, coll_name)
            if found:
                return found

    def pre_process(self):
        bpy.ops.object.tila_umi_command_batcher('INVOKE_DEFAULT', importer_mode=True, execute_each_process=False, execute_pre_process=True, execute_post_process=False)

    def post_process(self):
        self.post_processing = True
        bpy.ops.object.tila_umi_command_batcher('INVOKE_DEFAULT', importer_mode=True, execute_each_process=False, execute_pre_process=False, execute_post_process=True)

    def post_import_command(self, objects):
        bpy.ops.object.select_all(action='DESELECT')
        for o in objects:
            bpy.data.objects[o.name].select_set(True)
        bpy.ops.object.tila_umi_command_batcher('INVOKE_DEFAULT', importer_mode=True, execute_each_process=True, execute_pre_process=False, execute_post_process=False)

    def import_settings(self):
        self.current_format = self.formats_to_import.pop()

        if len(self.formats_to_import) == 0:
            self.umi_settings.umi_last_setting_to_get = True

        self.umi_settings.umi_current_format_setting_imported = False

        # gather import setting from the user for each format selected
        bpy.ops.import_scene.tila_universal_multi_importer_settings('INVOKE_DEFAULT', import_format=self.current_format['name'])
        self.first_setting_to_import = False

    def select_files(self):
        for f in self.filepaths:
            filepath = self.umi_settings.umi_file_selection.add()
            filepath.name = f
            filepath.ext = path.splitext(f)[1]
            filepath.path = f
            filesize = self.get_filesize(f)
            filepath.size = filesize

        update_file_extension_selection(self, bpy.context)
        bpy.ops.import_scene.tila_universal_multi_importer_file_selection('INVOKE_DEFAULT')

    def finish(self, context, canceled=False):
        bpy.types.SpaceView3D.draw_handler_remove(self._handle, 'WINDOW')
        self.revert_parameters(context)
        bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)
        if canceled:
            return {'CANCELLED'}
        else:
            return {'FINISHED'}

    def modal(self, context, event):
        # If Escape is Pressed :Cancelling
        if not self.import_complete and event.type in {'ESC'} and event.value == 'PRESS':
            LOG.warning('Cancelling...')
            self.cancel(context)

            self.log_end_text()
            self.counter = self.umi_settings.umi_global_import_settings.wait_before_hiding
            self.import_complete = True
            LOG.completed = True
            self.umi_settings.umi_format_import_settings.umi_import_cancelled = True
            return {'RUNNING_MODAL'}

        # If Import Complete, show Import Summary
        if self.import_complete:
            if not self.show_scroll_text:
                bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)
                self.show_scroll_text = True

            if event.type in {'WHEELUPMOUSE'} and event.ctrl and event.shift:
                LOG.scroll(up=True, multiplier=9)
            elif event.type in {'WHEELDOWNMOUSE'} and event.ctrl and event.shift:
                LOG.scroll(up=False, multiplier=9)
            if event.type in {'WHEELUPMOUSE'} and event.ctrl:
                LOG.scroll(up=True)
                bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)
                return {'PASS_THROUGH'}
            elif event.type in {'WHEELDOWNMOUSE'} and event.ctrl:
                LOG.scroll(up=False)
                bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)
                return {'PASS_THROUGH'}

            if self.umi_settings.umi_global_import_settings.auto_hide_text_when_finished:
                self.store_delta_start()

                if self.counter == self.umi_settings.umi_global_import_settings.wait_before_hiding:
                    self.previous_counter = self.counter
                    self.store_delta_end()

                remaining_seconds = math.ceil(self.counter)

                if remaining_seconds < self.previous_counter:
                    LOG.info(f'Hidding in {remaining_seconds}s ...')
                    self.previous_counter = remaining_seconds

                if self.counter <= 0:
                    return self.finish(context, self.canceled)

            if event.type in {'ESC'} and event.value == 'PRESS':
                return self.finish(context, self.canceled)

            if self.umi_settings.umi_global_import_settings.auto_hide_text_when_finished:
                self.previous_counter = remaining_seconds
                self.store_delta_end()
                self.decrement_counter()
                bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)

            return {'RUNNING_MODAL'}

        if event.type == 'TIMER':
            if self.umi_settings.umi_skip_settings:
                self.umi_settings.umi_skip_settings = False
                self.umi_settings.umi_file_selection_done = True
                self.umi_settings.umi_file_selection_started = False
                self.umi_settings.umi_ready_to_import = True
                self.operator_list = [{'name':'operator', 'operator': o.operator} for o in self.umi_settings.umi_each_operators]

            # Select files if in folder mode
            if not self.umi_settings.umi_file_selection_done:
                if not self.umi_settings.umi_file_selection_started:
                    self.select_files()
                if self.umi_settings.umi_current_format_setting_cancelled:
                    return self.cancel_finish(context)
                return {'PASS_THROUGH'}

            # File Selection is approved and fed into self.filepaths
            elif self.umi_settings.umi_file_selection_done and self.umi_settings.umi_file_selection_started:
                self.filepaths = [f.path for f in self.umi_settings.umi_file_selection if f.check]
                self.store_formats_to_import()

                self.init_progress()

                if not len (self.formats_to_import):
                    return self.cancel_finish(context)

                LOG.info(f'{len(self.filepaths)}  files selected')

                self.operator_list = [{'name':'operator', 'operator': o.operator} for o in self.umi_settings.umi_each_operators]

                self.umi_settings.umi_file_selection.clear()
                self.umi_settings.umi_file_selection_started = False
                self.pre_process()

            # LEGACY : Loop through all import format settings
            if not self.umi_settings.umi_ready_to_import:
                if not self.first_setting_to_import:
                    if self.umi_settings.umi_current_format_setting_cancelled:
                        return self.cancel_finish(context)
                    if not self.umi_settings.umi_current_format_setting_imported:
                        return {'PASS_THROUGH'}
                    else:
                        self.import_settings()
                else:
                    self.import_settings()

            # Import Loop
            else:
                #INIT Counter
                if self.start_time == 0:
                    self.start_time = time.perf_counter()

                # wait if post processing in progress
                if self.umi_settings.umi_batcher_is_processing:
                    return {'PASS_THROUGH'}

                # After each Import Batch, and batch process
                elif not len(self.objects_to_process) and not self.importing and self.current_object_to_process is None and self.current_file_number and not len (self.current_files_to_import):
                    # update End LOGs
                    i=len(self.current_filenames)
                    for filename in self.current_filenames:
                        index = len(self.imported_files) - i
                        if len(self.files_succeeded) and self.files_succeeded[index]:
                            message = f'File {index + 1} imported successfully : {filename}'
                            LOG.success(message)
                            LOG.store_success(message)
                        else:
                            message = f'File {index + 1} NOT imported correctly : {filename}'
                            LOG.error(message)

                        i -= 1

                    # Backup file
                    if self.umi_settings.umi_global_import_settings.backup_file_after_import:
                        if self.umi_settings.umi_global_import_settings.backup_step <= self.current_backup_step:
                            self.current_backup_step = 0
                            LOG.info('Saving backup file : {}'.format(path.basename(self.blend_backup_file)))
                            bpy.ops.wm.save_as_mainfile(filepath=self.blend_backup_file, check_existing=False, copy=True)

                    # Register Next Batch if files are remaining in the import list
                    if len(self.filepaths):
                        self.umi_settings.umi_imported_data.clear()
                        LOG.separator()
                        self.next_batch()
                        self.log_next_batch()

                    elif not self.post_processing:
                        self.post_process()
                    # All Batches are imported and processed : init ending
                    else:
                        if self.umi_settings.umi_global_import_settings.save_file_after_import:
                            bpy.ops.wm.save_as_mainfile(filepath=self.current_blend_file, check_existing=False)

                        LOG.complete_progress_importer(show_successes=False, duration=round(time.perf_counter() - self.start_time, 2), size=self.total_imported_size, batch_count=self.batch_number)
                        self.import_complete = True
                        LOG.completed = True
                        self.log_end_text()
                        self.counter = self.umi_settings.umi_global_import_settings.wait_before_hiding
                        bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)

                # Running Current Batcher on Imported Objects
                elif len(self.objects_to_process) or len(self.umi_settings.umi_imported_data):
                    self.post_import_command(self.objects_to_process)
                    self.objects_to_process = []

                # Current Batch Imported, update parameters
                elif self.importing and self.current_batch_imported:
                    self.importing = False

                # Register Next Batch Files
                elif self.current_files_to_import == [] and len(self.filepaths):
                    LOG.separator()
                    self.next_batch()
                    self.log_next_batch()

                # Start Importing
                elif not self.importing and len(self.current_files_to_import):
                    self.files_succeeded += self.import_files(context, self.current_files_to_import)
                    self.current_files_to_import = []

                elif self.current_files_to_import == [] and len(self.filepaths):
                    self.importing = False

        return {'PASS_THROUGH'}

    # from : https://www.digitalocean.com/community/tutorials/how-to-get-file-size-in-python
    def get_filesize(self, file_path):
        file_stats = os.stat(file_path)

        # print(file_path)
        # print(f'File Size in Bytes is {file_path.st_size}')
        filesize = file_stats.st_size / (1024 * 1024)
        # print(f'File Size in MegaBytes is {filesize}')
        return filesize

    def get_total_size(self, filepaths):
        size = 0
        for f in filepaths:
            size += self.get_filesize(f)

        return size

    def get_imported_data(self, before_imported_data)->list:
        imported_data = []
        for d in dir(bpy.data):
            if d.startswith('_') or d in ['objects', 'screens']:
                continue


            data_type = getattr(bpy.data, d)

            if not isinstance(data_type, bpy.types.bpy_prop_collection):
                continue

            if d not in before_imported_data:
                continue

            for data in data_type:
                imported_data_type = before_imported_data[d]

                if data.name in imported_data_type:
                    continue

                imported_data.append({'data' : repr(data), 'data_type': d})

        return imported_data

    def capture_data_dict(self) -> dict:
        data_dict = {}
        for d in dir(bpy.data):
            if d.startswith('_'):
                continue

            data_type = getattr(bpy.data, d)

            if not isinstance(data_type, bpy.types.bpy_prop_collection):
                continue

            data_dict[d] = []

            for data in data_type:
                data_dict[d].append(data.name)

        return data_dict

    def import_command(self, context, filepath):
        success = True
        ext = os.path.splitext(filepath)[1]
        format_name = COMPATIBLE_FORMATS.get_format_from_extension(ext).name

        current_format = eval(f'self.{format_name}_format')
        current_module = eval(f'self.umi_settings.umi_format_import_settings.{format_name}_import_module', {'self':self}).name.lower()
        import_objects = COMPATIBLE_FORMATS.is_import_objects(format_name, current_module)
        import_data = COMPATIBLE_FORMATS.is_import_data(format_name, current_module)
        # format_settings = current_format[current_module].format_settings

        before_import_data = {}
        if import_data:
            before_import_data = self.capture_data_dict()

        operators = COMPATIBLE_FORMATS.get_operator_name_from_extension(ext)[current_module].command

        # Double \\ in the path causing error in the string
        args = current_format[current_module].format_settings_dict
        raw_path = filepath.replace('\\\\', punctuation[23])

        # if format_name == 'image' and current_module in ['plane']:
        if 'files' in args['forced_properties']:
            args['files'] = '[{"name":' + f'r"{raw_path}"' + '}]'

        if 'directory' in args['forced_properties']:
            args['directory'] = f'r"{str(Path(raw_path).parent)}"'

        args['filepath'] = f'r"{raw_path}"'

        args_as_string = ''
        arg_number = len(args.keys())
        for k,v in args.items():
            if k in ['settings_imported', 'name', 'addon_name', 'supported_version', 'forced_properties']:
                arg_number -= 1
                continue
            if isinstance(v, bpy.types.bpy_prop_collection):
                if not len(v):
                    continue

                col_as_string = ''
                for i,f in enumerate(v):
                    if i == 0:
                        col_as_string += '['
                    elif i < len(v) -1:
                        col_as_string += ','

                    col_as_string += f'"{f}"'
                col_as_string += ']'

                args_as_string += f' {k}={col_as_string}'
            elif isinstance(v, Vector) or isinstance(v, Euler) or isinstance(v, Color):
                val = '['
                for i in range(len(v)):
                    if i == 0:
                        val += f'{v[i]}'
                    else:
                        val += f', {v[i]}'
                val += ']'
                args_as_string += f' {k}={val}'
            else:
                args_as_string += f' {k}={v}'
            if arg_number >= 2:
                args_as_string += ','

            arg_number -= 1

        command = '{}({})'.format(operators, args_as_string)
        # Execute the import command
        try:
            exec(command, {'bpy':bpy})
        except Exception as e:
            LOG.error(e)
            LOG.store_failure(e)
            success = False
            # raise Exception(e)

        if len(self.operator_list):
            if success:
                if import_objects and len(context.selected_objects):
                    self.objects_to_process = self.objects_to_process + [o for o in context.selected_objects]

                if import_data:
                    imported_data = self.get_imported_data(before_import_data)
                    for d in imported_data:
                        data = self.umi_settings.umi_imported_data.add()
                        data.data = d['data']
                        data.data_type = d['data_type']
                        data.name = eval(d['data']).name

        del before_import_data

        return success

    def update_progress(self):
            self.progress = (self.total_imported_size * 100) / self.total_import_size

    def import_file(self, context, current_file):
        self.importing = True
        filename = path.basename(current_file)
        name = (path.splitext(current_file)[0])
        name = path.basename(name)
        ext = path.splitext(filename)[1]
        self.current_filenames.append(path.basename(filename))

        if self.umi_settings.umi_global_import_settings.skip_already_imported_files:
            if filename in bpy.data.collections:
                self.current_files_to_import = []
                self.importing = False
                LOG.warning(f'File {filename} have already been imported, skiping file...')
                return

        current_file_size = self.get_filesize(current_file)
        self.total_imported_size += current_file_size
        self.update_progress()

        LOG.info(f'Importing file {len(self.imported_files) + 1}/{self.number_of_files} - {round(self.progress,2)}% - {round(current_file_size, 2)}MB : {filename}', color=LoggerColors.IMPORT_COLOR())
        self.current_backup_step += current_file_size

        if self.umi_settings.umi_global_import_settings.force_refresh_viewport_after_each_import:
            bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)
        elif self.refresh_timer <= 0:
            self.store_timer_start()
            bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)

        import_col = self.root_collection

        if self.umi_settings.umi_global_import_settings.recreate_folder_structure_as_collections and self.import_folders:
            hierarchy_path = str(Path(path.dirname(current_file).replace(str(Path(self.directory).parent.absolute()), '')))

            herarchy_list = hierarchy_path.split("\\")[1:]

            import_col = self.create_collection_hierarchy(herarchy_list)

            root_layer_col = self.view_layer.layer_collection
            layer_col = self.recur_layer_collection(root_layer_col, import_col.name)
            self.view_layer.active_layer_collection = layer_col

        if self.umi_settings.umi_global_import_settings.create_collection_per_file:
            collection = bpy.data.collections.new(name=filename)
            import_col.children.link(collection)

            root_layer_col = self.view_layer.layer_collection
            layer_col = self.recur_layer_collection(root_layer_col, collection.name)
            self.view_layer.active_layer_collection = layer_col
            import_col = collection

        self.store_objects()

        # Running Import Command
        succeeded = self.import_command(context, filepath=current_file)

        # Prevent to link object if no object imported
        if ext.lower() == '.blend' and not self.blend_format['default'].format_settings.import_objects:
            pass
        else:
            self.link_new_object_in_collection(import_col)

        self.imported_files.append(current_file)
        return succeeded

    def store_objects(self) -> None:
        self._stored_objects = [o for o in bpy.data.objects]

    def create_collection_hierarchy(self, collection_hierarcy:list) -> bpy.types.Collection:
        collection: bpy.types.Collection
        parent_collection: bpy.types.Collection

        for i,c in enumerate(collection_hierarcy):
            if c not in bpy.data.collections:
                # print(f'create collection "{c}"')
                collection = bpy.data.collections.new(name=c)
                self.unique_name.register_element_correspondance(collection)

            else:
                if i > 0 and parent_collection.name in self.parent_names_dict.keys():
                    # print(f'using collection "{parent_collection.name}"')
                    collection = bpy.data.collections[self.parent_names_dict[parent_collection.name]]
                elif i > 0 and parent_collection not in self.get_collection_parents(bpy.data.collections[c]):
                    name = self.unique_name.get_next_valid_name(c)
                    # print(f'create collection "{name}"')
                    collection = bpy.data.collections.new(name=name)
                    self.unique_name.register_element_correspondance(collection)
                    self.parent_names_dict[parent_collection.name] = name
                else:
                    # print(f'using collection "{c}"')
                    collection = bpy.data.collections[c]

            if i == 0:
                parent_collection = collection
                if collection.name not in self.root_collection.children:
                    root_collection = self.root_collection
                    if root_collection not in collection.children_recursive:
                        # print(f'Link collection "{collection.name}" to "{root_collection.name}"')
                        root_collection.children.link(collection)
                continue

            if collection.name not in parent_collection.children:
                # print(f'Link collection "{collection.name}" to "{parent_collection.name}"')
                parent_collection.children.link(collection)

            parent_collection = collection

        return collection

    def get_collection_parents(self, collection: bpy.types.Collection) -> list[bpy.types.Collection]:
        parent_list:list[bpy.types.Collection] = []
        for c in bpy.data.collections:
            if c == collection:
                continue

            if collection.name in c.children:
                parent_list.append(c)

        return parent_list

    def get_new_objects(self):
        return [o for o in bpy.data.objects if o not in self._stored_objects]

    def link_new_object_in_collection(self, import_col):
        new_objects = self.get_new_objects()

        if len(new_objects):
            for o in new_objects:
                if not len(o.users_collection) or o.name in import_col.all_objects:
                    print(f'skip linking "{o.name}" to collection')
                    continue
                previous_col = o.users_collection[0]
                import_col.objects.link(o)
                previous_col.objects.unlink(o)

    def import_files(self, context, filepaths):
        self.importing = True
        success = []
        for f in filepaths:
            success.append(self.import_file(context, f))
        self.current_batch_imported = True
        return success

    def get_compatible_files_in_folder(self, folder_path, recursion_depth=0):
        compatible_files = []
        for f in os.listdir(folder_path):
            filepath = path.join(folder_path, f)
            if path.isfile(filepath):
                if path.splitext(f)[1].lower() in self.compatible_extensions:
                    compatible_files.append(filepath)
            elif path.isdir(filepath):
                if recursion_depth > 0:
                    compatible_files = compatible_files + self.get_compatible_files_in_folder(filepath, recursion_depth-1)

        return compatible_files

    def store_formats_to_import(self):
        for f in self.filepaths:
            format = COMPATIBLE_FORMATS.get_format_from_extension(path.splitext(f)[1])
            if format not in self.formats_to_import:
                self.formats_to_import.append(format)

    def revert_parameters(self, context):
        self.formats_to_import = []
        self.all_parameters_imported = False
        self.thread = None
        self.progress = 0
        self.current_backup_step = 0
        self.current_files_to_import = []
        self.importing = False
        self.first_setting_to_import = True
        self.canceled = False
        self.import_complete = False
        self.current_batch_imported = False
        self.files_succeeded = []
        self.umi_settings.umi_last_setting_to_get = False
        self.umi_settings.umi_ready_to_import = False
        self.umi_settings.umi_current_format_setting_imported = False
        self.umi_settings.umi_current_format_setting_cancelled = False
        self._filepaths = None
        context.window_manager.event_timer_remove(self._timer)
        LOG.revert_parameters()
        LOG.clear_all()

    def init_importer(self, context):
        bpy.utils.unregister_class(UMI_OT_Settings)
        bpy.utils.register_class(UMI_OT_Settings)
        self._filepaths = None
        self.current_blend_file = bpy.data.filepath
        self.current_files_to_import = []
        self.current_filenames = []
        self.imported_files = []
        self.operation_processed = 0
        self.show_scroll_text = False
        self.start_time = 0
        self.batch_number = 0
        self.total_imported_size = 0
        self.current_batch_imported = False
        self.files_succeeded = []
        self.umi_settings = get_umi_settings()
        self.post_processing = False
        self.umi_settings.umi_format_import_settings.umi_import_cancelled = False
        self.umi_settings.umi_file_selection.clear()
        self.umi_settings.umi_file_selection_started = False
        self.umi_settings.umi_file_selection_done = False
        self.umi_settings.umi_import_directory = self.import_folders

        init_current_item_index(self.umi_settings)

        self.umi_settings.umi_imported_data.clear()
        LOG.revert_parameters()
        LOG.esc_message = '[Esc] to Cancel'
        LOG.message_offset = 15
        if self.umi_settings.umi_import_directory:
            self.unique_name = UniqueName()
            for c in bpy.data.collections:
                self.unique_name.register_element_correspondance(c)
                self.parent_names_dict = {}

    def execute(self,context):
        self.init_importer(context)

        register_import_format(self, context)

        if not path.exists(self.current_blend_file):
            LOG.warning('Blender file not saved')
            self.umi_settings.umi_global_import_settings.save_file_after_import = False
            autosave = path.join(AUTOSAVE_PATH, 'umi_autosave_' + time.strftime('%Y-%m-%d-%H-%M-%S') + '.blend')
        else:
            autosave = path.splitext(self.current_blend_file)[0] + "_bak" + path.splitext(self.current_blend_file)[1]

        self.blend_backup_file = autosave

        if not len(self.filepaths):
            message = "No compatible file selected"
            LOG.error(message)
            self.report({'ERROR'}, message)
            return {'CANCELLED'}

        if self.umi_settings.umi_global_import_settings.max_batch_size and self.umi_settings.umi_global_import_settings.minimize_batch_number:
            # Sorting filepaths per Filesize for optimization
            self.filepaths = self.sort_per_filesize(self.filepaths)

        self.init_progress()

        LOG.info("{} compatible file(s) found".format(len(self.filepaths)))
        LOG.separator()

        self.view_layer = bpy.context.view_layer
        self.root_collection = bpy.context.collection
        self.current_file_number = 0

        self.umi_settings.umi_ready_to_import = False

        # If in File mode Store Format to import now. If in folder mode, formats will be stored after file selection
        if not self.import_folders:
            self.store_formats_to_import()

        self.objects_to_process = []
        self.current_object_to_process = None

        args = (context,)
        self._handle = bpy.types.SpaceView3D.draw_handler_add(LOG.draw_callback_px, args, 'WINDOW', 'POST_PIXEL')

        wm = context.window_manager
        self._timer = wm.event_timer_add(0.01, window=context.window)
        wm.modal_handler_add(self)
        return {'RUNNING_MODAL'}

    def sort_zipped_list(self, zipped):
        sorted_filepaths = []
        i = 0
        for z in zipped:
            if len(sorted_filepaths):
                j = 0
                for s in sorted_filepaths:
                    if s[0] > z[0]:
                        j += 1
                        # print(f'{s[0]} > {z[0]}')
                        continue
                    else:
                        # print(f'Assigning {z} to position {z}')
                        sorted_filepaths.insert(j, z)
                        break
                else:
                    sorted_filepaths.insert(j, z)
            else:
                sorted_filepaths.insert(0, z)
            i += 1

        return sorted_filepaths

    def sort_per_filesize(self, filepaths):
        size_list = [self.get_filesize(f) for f in filepaths]

        zipped = zip(size_list, filepaths)
        zipped = list(zipped)

        sorted_filepaths = self.sort_zipped_list(zipped)

        # Unzip List
        sorted_filepaths =  [[i for i, j in sorted_filepaths], [j for i, j in sorted_filepaths]]
        sorted_filepaths = sorted_filepaths[1]
        return sorted_filepaths

    def get_next_viable_file(self, filepaths, initial_size, max_size, selected_files):
        for f in filepaths:
            if self.umi_settings.umi_global_import_settings.minimize_batch_number:
                current_size = self.get_filesize(f)
                if initial_size + current_size > max_size:
                    if len(selected_files):
                        continue
                return f
            else:
                return f

        return None

    def log_next_batch(self):
        LOG.info(f'Starting Batch n°{self.batch_number} with {len(self.current_files_to_import)} files')
        LOG.info(f'Batch size : {round(self.current_batch_size, 2)}MB')

    def next_batch(self):
        self.current_files_to_import = []
        self.current_filenames = []
        self.current_batch_size = 0
        self.batch_number += 1
        self.batch_file_count = 0

        for _ in range(self.umi_settings.umi_global_import_settings.import_simultaneously_count):
            if not len(self.filepaths):
                return

            next_files = self.get_next_viable_file(self.filepaths, self.current_batch_size, self.umi_settings.umi_global_import_settings.max_batch_size, self.current_files_to_import)
            if next_files is not None:
                next_filesize = self.get_filesize(next_files)
            # Batch is Full
            if next_files is None:
                if len(self.current_files_to_import):
                    return
                next_files = self.filepaths.pop(0)

            elif self.current_batch_size + next_filesize > self.umi_settings.umi_global_import_settings.max_batch_size:
                if len(self.current_files_to_import):
                    return

            self.batch_file_count += 1

            # increment batch and import size
            self.current_batch_size += next_filesize
            self.filepaths.remove(next_files)
            self.current_files_to_import.append(next_files)
            self.current_file_number += 1
            self.current_batch_imported = False

    def cancel(self, context):
        self.canceled = True
        if self._timer is not None:
            wm = context.window_manager
            wm.event_timer_remove(self._timer)

    def cancel_finish(self, context):
        self.cancel(context)
        return self.finish(context, canceled=True)


# function to append the operator in the File>Import menu
def menu_func_import(self, context):
    op = self.layout.operator(UMI.bl_idname, text="Universal Multi Importer Files", icon='LONGDISPLAY')
    op.import_folders = False
    op.filter_blender = True
    op.filter_usd = True
    op.filter_obj = True
    op.filter_fbx = True
    op.filter_image = True
    op.filter_movie = True
    op.filter_collada = True
    op.filter_alembic = True
    op.filter_volume = True
    op.filter_ply = True
    op.filter_gltf = True
    op.filter_stl = True
    op.filter_svg = True

    op = self.layout.operator(UMI.bl_idname, text="Universal Multi Importer Folders", icon='FILEBROWSER')
    op.filter_glob = ''
    op.import_folders = True
    op.filter_blender = False
    op.filter_usd = False
    op.filter_obj = False
    op.filter_fbx = False
    op.filter_image = False
    op.filter_movie = False
    op.filter_collada = False
    op.filter_alembic = False
    op.filter_volume = False
    op.filter_ply = False
    op.filter_gltf = False
    op.filter_stl = False
    op.filter_svg = False

classes = (UMI_OT_Settings, UMI_FileSelection, UMI, UMI_MD5Check)

if BVERSION >= 4.1:
    classes = classes + (IMPORT_SCENE_FH_UMI_3DVIEW, IMPORT_SCENE_FH_UMI_OUTLINER, UMI_OT_Drop_In_Outliner)

def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)

    bpy.types.TOPBAR_MT_file_import.append(menu_func_import)

def unregister():
    bpy.types.TOPBAR_MT_file_import.remove(menu_func_import)

    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)

if __name__ == "__main__":
    register()