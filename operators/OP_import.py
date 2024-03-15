import bpy
from bpy_extras.io_utils import ImportHelper
import os, time
from os import path
import math
from string import punctuation
from ..preferences.formats import FormatHandler, COMPATIBLE_FORMATS
from ..preferences.formats.properties.properties import update_file_stats, get_file_selected_items, update_file_extension_selection
from .OP_command_batcher import draw_command_batcher
from ..umi_const import get_umi_settings
from ..preferences.formats.panels.presets import import_preset
from ..logger import LOG, LoggerColors, MessageType
from ..blender_version import BVERSION

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
			bpy.ops.outliner.item_activate('INVOKE_DEFAULT', extend=False, extend_range=False, deselect_all=True)
			if context.collection is None :
				self.report({'ERROR'}, 'UMI : Please Drop files on a Collection')
				return {'FINISHED'}
			files = []
			for f in self.files.values():
				files.append({'name':f.name})

			bpy.ops.import_scene.tila_universal_multi_importer("INVOKE_DEFAULT", import_folders=False, files=files, directory=self.directory)
			return {'FINISHED'}

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
				if not k in ['name', 'settings_imported', 'import_format', 'ui_tab']:
					col.prop(self, k)
	
	def cancel(self, context):
		UMI_OT_Settings.bl_idname = f'import_scene.tila_universal_multi_importer_settings'
		bpy.utils.unregister_class(UMI_OT_Settings)
		bpy.utils.register_class(UMI_OT_Settings)
		self.umi_settings.umi_current_format_setting_cancelled = True
		return {'CANCELLED'}


def register_import_format(self, context):
	for f in COMPATIBLE_FORMATS.formats:
		exec('self.{}_format = {{ }}'.format(f[0]), {'self':self})
		current_format = eval(f'self.{f[0]}_format')
		for i,name in enumerate(f[1]['operator'].keys()):
			current_format[name] = FormatHandler(import_format=f"{f[0]}", module_name=name, context=context)

class UMI_FileSelection(bpy.types.Operator):
	bl_idname = "import_scene.tila_universal_multi_importer_file_selection"
	bl_label = "Universal Multi Importer"
	bl_options = {'REGISTER', 'INTERNAL'}
	bl_region_type = "UI"

	def invoke(self, context, event):
		self.umi_settings = get_umi_settings()
		self.umi_settings.umi_file_selection_started = True
		
		register_import_format(self, context)
		
		update_file_stats(self, context)
		wm = context.window_manager
		return wm.invoke_props_dialog(self, width=1100)

	def execute(self, context):
		self.umi_settings.umi_file_selection_done = True
		self.umi_settings.umi_ready_to_import = True

		self.umi_settings.umi_current_format_setting_imported = True
		return {'FINISHED'}

	def draw(self, context):
		layout = self.layout
		main_col = layout.column()

		main_row = main_col.split(factor = 0.55)
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
		
		box = file_selection_box.box()
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
		
		row2 = file_selection_box.row(align=True)
		row2.alignment = 'LEFT'
		row2.label(text=str(self.umi_settings.umi_file_stat_selected_count) + ' file(s)  |  ')
		row2.label(text=str(round(self.umi_settings.umi_file_stat_selected_size, 4)) + ' Mb')
		file_selection_box.label(text=self.umi_settings.umi_file_stat_selected_formats + ' format(s) selected')

		main_col.separator()
		
		rows = min(len(self.umi_settings.umi_file_selection) if len(self.umi_settings.umi_file_selection) > 2 else 2, 20)
		col1 = file_selection_box.column()
		col1.template_list('UMI_UL_file_selection_list', '', self.umi_settings, 'umi_file_selection', self.umi_settings, 'umi_file_selection_idx', rows=rows)
		
		col1 = main_row.column()
		col1.label(text='Import Settings')

		box = col1.box()
		col2 = box.column(align=True)
		row1 = col2.row(align=True)
		row1.prop(self.umi_settings, 'umi_import_batch_settings', expand=True)
		row1 = col2.row(align=True)

		if len(self.umi_settings.umi_file_extension_selection) and len(get_file_selected_items(self, context)):
			row1.prop(self.umi_settings, 'umi_file_format_current_settings', expand=True)
		else:
			row1.alignment = 'CENTER'
			row1.label(text='Select at least one file')
		col1.separator()
		if len(self.umi_settings.umi_file_format_current_settings):
			current_setting_name = self.umi_settings.umi_file_format_current_settings.copy().pop().lower()
			self.draw_current_settings(context, box, current_setting_name)
		elif len(self.umi_settings.umi_import_batch_settings):
			if self.umi_settings.umi_import_batch_settings == {'GLOBAL'}:
				import_preset.panel_func(box)
				self.draw_global_settings(context, box)
			elif self.umi_settings.umi_import_batch_settings == {'BATCHER'}:
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
		import_count = col.box()
		import_count.label(text='File Count', icon='LONGDISPLAY')
		import_count.prop(self.umi_settings.umi_global_import_settings, 'import_simultaneously_count')
		import_count.prop(self.umi_settings.umi_global_import_settings, 'max_batch_size')
		if self.umi_settings.umi_global_import_settings.max_batch_size:
			import_count.prop(self.umi_settings.umi_global_import_settings, 'minimize_batch_number')

		settings = col.box()
		settings.label(text='Options', icon='OPTIONS')
		settings.prop(self.umi_settings.umi_global_import_settings, 'create_collection_per_file')
		
		if self.umi_settings.umi_global_import_settings.create_collection_per_file:
			row = settings.row()
			split = row.split(factor=0.1, align=True)
			split.label(text='')
			split = split.split()
			split.prop(self.umi_settings.umi_global_import_settings, 'skip_already_imported_files')

		log = col.box()
		log.label(text='Log Display', icon='WORDWRAP_ON')

		column = log.column(align=True)

		column.prop(self.umi_settings.umi_global_import_settings, 'show_log_on_3d_view')
		if self.umi_settings.umi_global_import_settings.show_log_on_3d_view:
			column.prop(self.umi_settings.umi_global_import_settings, 'auto_hide_text_when_finished')
			if self.umi_settings.umi_global_import_settings.auto_hide_text_when_finished:
				column.prop(self.umi_settings.umi_global_import_settings, 'wait_before_hiding')
		column.prop(self.umi_settings.umi_global_import_settings, 'force_refresh_viewport_after_each_import')

		backup = col.box()
		col1 = backup.column()
		col1.label(text='backup', icon='FILE_TICK')
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
	filter_glob: bpy.props.StringProperty(default=COMPATIBLE_FORMATS.filter_glob, options={"HIDDEN"})
	filter_folder: bpy.props.BoolProperty(default=True, options = {"HIDDEN"})
	filter_blender : bpy.props.BoolProperty(default=True, options={"HIDDEN"})
	filter_usd : bpy.props.BoolProperty(default=True, options={"HIDDEN"})
	filter_obj : bpy.props.BoolProperty(default=True, options={"HIDDEN"})
	filter_fbx : bpy.props.BoolProperty(default=True, options={"HIDDEN"})
	filter_image : bpy.props.BoolProperty(default=True, options={"HIDDEN"})
	filter_movie : bpy.props.BoolProperty(default=True, options={"HIDDEN"})
	filter_collada : bpy.props.BoolProperty(default=True, options={"HIDDEN"})
	filter_alembic : bpy.props.BoolProperty(default=True, options={"HIDDEN"})
	filter_volume : bpy.props.BoolProperty(default=True, options={"HIDDEN"})
	filter_ply : bpy.props.BoolProperty(default=True, options={"HIDDEN"})
	filter_gltf : bpy.props.BoolProperty(default=True, options={"HIDDEN"})
	filter_x3d : bpy.props.BoolProperty(default=True, options={"HIDDEN"})
	filter_stl : bpy.props.BoolProperty(default=True, options={"HIDDEN"})
	filter_svg : bpy.props.BoolProperty(default=True, options={"HIDDEN"})
	

	# Selected files
	files : bpy.props.CollectionProperty(type=bpy.types.OperatorFileListElement, options={'SKIP_SAVE'})
	# Support Folder selection
	import_folders : bpy.props.BoolProperty(name="Import Folder",default=False)
	directory: bpy.props.StringProperty(name="Outdir Path", subtype='FILE_PATH')
	# Support for Image and movie file
	# filter_image: bpy.props.BoolProperty(default=True, options={'HIDDEN', 'SKIP_SAVE'})
	# filter_movie: bpy.props.BoolProperty(default=True, options={'HIDDEN', 'SKIP_SAVE'})
	# Import Settings
	recursion_depth : bpy.props.IntProperty(name='Recursion Depth', default=0, min=0, description='How many Subfolders will be used to search for compatible files to import.\n/!\ WARNING : A too big number may result of a huge number of files to import and may cause instability')

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
		self.umi_settings.umi_skip_settings = False
		bpy.ops.scene.umi_load_preset_list()

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
	
	def log_end_text(self):
		LOG.info('-----------------------------------')
		if self.import_complete:
			if False in self.files_succeeded:
				LOG.info('Batch Import completed with errors !', color=LoggerColors.ERROR_COLOR)
				LOG.esc_message = '[Esc] to Hide'
				LOG.message_offset = 4
			else:
				LOG.info('Batch Import completed successfully !', color=LoggerColors.SUCCESS_COLOR)
				LOG.esc_message = '[Esc] to Hide'
				LOG.message_offset = 4
		else:
			LOG.info('Batch Import cancelled !', color=LoggerColors.CANCELLED_COLOR)
			
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

	def post_import_command(self, objects, operator_list):
		bpy.ops.object.select_all(action='DESELECT')
		for o in objects:
			bpy.data.objects[o.name].select_set(True)
		bpy.ops.object.tila_umi_command_batcher('INVOKE_DEFAULT', operator_list=operator_list, importer_mode=True)

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
				
				self.operator_list = [{'name':'operator', 'operator': o.operator} for o in self.umi_settings.umi_operators]

				self.umi_settings.umi_file_selection.clear()
				self.umi_settings.umi_file_selection_started = False

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
						LOG.separator()
						self.next_batch()
						self.log_next_batch()

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
				elif len(self.objects_to_process): 
					self.post_import_command(self.objects_to_process, self.operator_list)
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

	def import_command(self, context, filepath):
		success = True
		ext = os.path.splitext(filepath)[1]
		format_name = COMPATIBLE_FORMATS.get_format_from_extension(ext)['name']
		current_format = eval(f'self.{format_name}_format')
		current_module = eval(f'self.umi_settings.umi_format_import_settings.{format_name}_import_module', {'self':self}).name.lower()
		# format_settings = current_format[current_module].format_settings
		
		operators = COMPATIBLE_FORMATS.get_operator_name_from_extension(ext)[current_module]['command']

		# Double \\ in the path causing error in the string
		args = current_format[current_module].format_settings_dict
		raw_path = filepath.replace('\\\\', punctuation[23])
		
		if format_name == 'image' and current_module in ['plane']:
			args['files'] = '[{"name":' + f'r"{raw_path}"' + '}]'
		else:
			args['filepath'] = f'r"{raw_path}"'

		args_as_string = ''
		arg_number = len(args.keys())
		for k,v in args.items():
			if k in ['settings_imported', 'name']:
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
				self.objects_to_process = self.objects_to_process + [o for o in context.selected_objects]

		return success

	def update_progress(self):
			self.progress = (self.total_imported_size * 100) / self.total_import_size
	
	def import_file(self, context, current_file):
		self.importing = True
		filename = path.basename(current_file)
		name = (path.splitext(current_file)[0])
		name = path.basename(name)
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

		LOG.info(f'Importing file {len(self.imported_files) + 1}/{self.number_of_files} - {round(self.progress,2)}% - {round(current_file_size, 2)}MB : {filename}', color=LoggerColors.IMPORT_COLOR)
		self.current_backup_step += current_file_size
		
		if self.umi_settings.umi_global_import_settings.force_refresh_viewport_after_each_import:
			bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)

		if self.umi_settings.umi_global_import_settings.create_collection_per_file:
			collection = bpy.data.collections.new(name=filename)
			self.root_collection.children.link(collection)
			
			root_layer_col = self.view_layer.layer_collection    
			layer_col = self.recur_layer_collection(root_layer_col, collection.name)
			self.view_layer.active_layer_collection = layer_col

		succeeded = self.import_command(context, filepath=current_file)
		self.imported_files.append(current_file)
		return succeeded

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
				if path.splitext(f)[1] in self.compatible_extensions:
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
		self.umi_settings.umi_format_import_settings.umi_import_cancelled = False
		self.umi_settings.umi_file_selection.clear()
		self.umi_settings.umi_file_selection_started = False
		self.umi_settings.umi_file_selection_done = False
		LOG.revert_parameters()
		LOG.esc_message = '[Esc] to Cancel'
		LOG.message_offset = 15

	def execute(self,context):
		self.init_importer(context)

		register_import_format(self, context)

		if not path.exists(self.current_blend_file):
			LOG.warning('Blender file not saved')
			self.umi_settings.umi_global_import_settings.save_file_after_import = False
			autosave = path.join(bpy.utils.user_resource(resource_type='AUTOSAVE', create=True), 'umi_autosave_' + time.strftime('%Y-%m-%d-%H-%M-%S') + '.blend')
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
	op.filter_glob = COMPATIBLE_FORMATS.filter_glob
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

classes = (UMI_OT_Settings, UMI_FileSelection, UMI)

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