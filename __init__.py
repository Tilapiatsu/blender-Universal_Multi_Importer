import bpy
from bpy.types import BoolProperty, StringProperty, IntProperty, FloatProperty
from bpy_extras.io_utils import ImportHelper
from bpy_extras.wm_utils.progress_report import ProgressReport
import os, time
from os import path
import inspect
from string import punctuation
from .logger import LoggerProgress
from .OP_ui_list_operator import *
from .format_definition import FormatDefinition
import math
from datetime import datetime
import time

bl_info = {
	"name" : "Universal Multi Importer",
	"author" : "Tilapiatsu",
	"description" : "",
	"blender" : (2, 93, 0),
	"location": "File > Import-Export",
	"warning" : "",
	"category": "Import-Export"
}

# TODO : add popup dialog box if file is not save
# TODO : Need to create a save/load preset for command list ( Macros ?)
# TODO : Need to create a autocomplete command creation
	# bpy.types.UILayout.template_search_preview ?
	# bpy.types.UILayout.template_operator_search ?

log = LoggerProgress('UMI')
formats = [f for f in dir(FormatDefinition) if not f.startswith('__')]

class TILA_compatible_formats(object):
	for format in formats:
		exec('{} = {}'.format(format, getattr(FormatDefinition, format)))
	
	def __init__(self):
		self._extensions = None
		self._operators = None
		self._module = None
		# automatically gather format
		attributes = inspect.getmembers(TILA_compatible_formats, lambda a:not(inspect.isroutine(a)))
		self.formats = [a for a in attributes if (not(a[0].startswith('__') and a[0].endswith('__')) and isinstance(a[1], dict))]


	@property
	def extensions(self):
		if self._extensions is None:
			extensions = []
			for f in self.formats:
				if isinstance(f[1], dict):
					extensions = extensions + f[1]['ext']
			self._extensions = extensions
		return self._extensions

	@property
	def operators(self):
		if self._operators is None:
			operators = []
			for f in self.formats:
				if isinstance(f[1], dict):
					operators.append(f[1]['operator'])
			self._operators = operators
		return self._operators
	
	@property
	def module(self):
		if self._module is None:
			module = []
			for f in self.formats:
				if isinstance(f[1], dict):
					module.append(f[1]['module'])
			self._module = module
		return self._module

	def get_format_from_extension(self, ext):
		if ext.lower() not in self.extensions:
			# raise Exception("extension '{}' is not supported".format(ext))
			message = f"extension '{ext}' is not supported"
			log.error(message)
			return None
		else:
			for f in self.formats:
				if  ext.lower() in f[1]['ext']:
					return f[1]
	
	def get_operator_name_from_extension(self, ext):
		format = self.get_format_from_extension(ext)
		if format is None:
			return None
		formats = {}
		for k,v in format['operator'].items():
			formats[k] = v
		
		return formats

compatible_formats = TILA_compatible_formats()


for f in compatible_formats.formats:
	exec('class TILA_umi_{}_settings(bpy.types.PropertyGroup):name: bpy.props.StringProperty(name="Import Setting Name", default="{}")'.format(f[1]['name'], f[1]['name']))

class TILA_import_settings_creator(bpy.types.PropertyGroup):
	name: bpy.props.StringProperty(name="Import Setting Name", default="")

class TILA_format_class_creator(object):
	def __init__(self):
		self._classes = None

	@property
	def compatible_formats_class(self):
		if self._classes is None:
			self._classes = []
			for f in compatible_formats.formats:
				if 'module' in f[1].keys():
					format_class = self.create_format_class_from_module(f[1])
				else:
					format_class = self.create_format_class_from_operator(f[1])

				self._classes.append(format_class)

		return self._classes

	def create_format_class_from_module(self, f):
		print(f'create class from module {f["module"]}')
		format_module = getattr(bpy.types, f['module'], None)
		if format_module is None:
			raise Exception("Invalid module name passed")
		format_annotations = getattr(format_module, "__annotations__", None)

		# format_class = type('TILA_umi_' + f['name'] + '_settings', TILA_import_collection_property_creator.__bases__, dict(TILA_import_collection_property_creator.__dict__))
		format_class = eval('TILA_umi_{}_settings'.format(f['name']))
		key_to_delete = []
		for k,v in format_annotations.items():
			if 'options' in v.keywords.keys():
				options = v.keywords['options']
			else:
				options = None

			if options == {'HIDDEN'}:
				key_to_delete.append(k)
				continue

			format_class.__annotations__[k] = v

		for k in key_to_delete:
			del format_annotations[k]
		
		format_class.__annotations__['settings_imported'] = bpy.props.BoolProperty(name='Settings imported', default=False, options={'HIDDEN'})
		return format_class
	
	def create_format_class_from_operator(self, f):
		format_class = eval('TILA_umi_{}_settings'.format(f['name']))

		if 'import_settings' in f.keys() :
			for g in f['import_settings']:
				for k,v in g[1].items():
					print(k)
					if 'enum_items' in v.keys():
						command = f'{v["type"]}(name={v["name"]}, default={v["default"]}, items={v["enum_items"]})'
					else:
						command = f'{v["type"]}(name={v["name"]}, default={v["default"]})'
					print(command)
					format_class.__annotations__[k] = eval(command)
		
		format_class.__annotations__['settings_imported'] = bpy.props.BoolProperty(name='Settings imported', default=False, options={'HIDDEN'})
		return format_class

	def register_compatible_formats(self):
		for c in self.compatible_formats_class:
			bpy.utils.register_class(c)
	
	def unregister_compatible_formats(self):
		for c in reversed(self.compatible_formats_class):
			bpy.utils.unregister_class(c)

class TILA_umi_import_settings(bpy.types.PropertyGroup):
	umi_import_settings_registered : bpy.props.BoolProperty(name='Import settings registered', default=False)

class TILA_umi_operator(bpy.types.PropertyGroup):
	operator : bpy.props.StringProperty(name='Operator', default='')

class TILA_umi_scene_settings(bpy.types.PropertyGroup):
	umi_ready_to_import : bpy.props.BoolProperty(name='Ready to Import', default=False)
	umi_last_setting_to_get : bpy.props.BoolProperty(name='Ready to Import', default=False)
	umi_current_format_setting_imported : bpy.props.BoolProperty(name='Current Format Settings Imported', default=False)
	umi_operators : bpy.props.CollectionProperty(type = TILA_umi_operator)
	umi_operator_idx : bpy.props.IntProperty()
	umi_import_settings : bpy.props.PointerProperty(type=TILA_umi_import_settings)

class TILA_umi_format_handler(object):
	import_format : bpy.props.StringProperty(name='Import Format', default="", options={'HIDDEN'},)

	def __init__(self, import_format, context):
		self._format = None
		self._format_name = None
		self._format_settings = None
		self._format_class = None
		self._format_annotations = None
		self._format_settings_dict = None
		self.import_format = import_format
		self.context = context

	@property
	def format(self):
		if self._format is None:
			self._format = getattr(compatible_formats, self.import_format)

		return self._format

	@property
	def format_name(self):
		if self._format_name is None:
			self._format_name = self.format['name']

		return self._format_name

	@property
	def format_class(self):
		if self._format_class is None:
			self._format_class = eval('TILA_umi_{}_settings'.format(self.format_name))
		
		return self._format_class

	@property
	def format_annotations(self):
		if self._format_annotations is None:
			self._format_annotations = getattr(self.format_settings, "__annotations__", None)
		
		return self._format_annotations

	@property
	def format_is_imported(self):
		return self.format_settings.settings_imported

	@property
	def format_settings(self):
		if self._format_settings is None:
			self._format_settings = eval("context.scene.umi_settings.umi_import_settings.{}_import_settings".format(self.format_name), {'context':self.context})
		
		return self._format_settings

	@property
	def format_settings_dict(self):
		if self._format_settings_dict is None:
			d = {}
			for k,v in self.format_settings.items():
				d[k] = getattr(self.format_settings, k)
				if isinstance(d[k], str):
					d[k] = '"{}"'.format(d[k])

			self._format_settings_dict = d


		return self._format_settings_dict

class TILA_umi_settings(bpy.types.Operator, ImportHelper):
	bl_idname = "import_scene.tila_universal_multi_importer_settings"
	bl_label = "Import ALL"
	bl_options = {'REGISTER', 'INTERNAL'}
	bl_region_type = "UI"

	import_format : bpy.props.StringProperty(name='Import Format', default="", options={'HIDDEN'},)
	
	def unregister_annotations(self):
		for a in self.registered_annotations:
			del self.__class__.__annotations__[a]

	def populate_property(self, property_name, property_value):
		self.__class__.__annotations__[property_name] = property_value

	def execute(self, context):
		# set the scene setting equal to the setting set by the user
		for k,v in self.__class__.__annotations__.items():
			if getattr(v, 'is_hidden', False) or getattr(v, 'is_readonly', False):
				continue
			print(k)
			if k in dir(self.format_handler.format_settings):
				try:
					setattr(self.format_handler.format_settings, k, getattr(self, k))
				except AttributeError as e:
					log.error("{}".format(e))

		if context.scene.umi_settings.umi_last_setting_to_get:
			context.scene.umi_settings.umi_ready_to_import = True

		context.scene.umi_settings.umi_current_format_setting_imported = True
		self.unregister_annotations()

		return {'FINISHED'}

	def invoke(self, context, event):
		key_to_delete = []
		self.registered_annotations = []
		self.format_handler = eval('TILA_umi_format_handler(import_format="{}", context=cont)'.format(self.import_format), {'self':self, 'TILA_umi_format_handler':TILA_umi_format_handler, 'cont':context})

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

		bpy.utils.unregister_class(TILA_umi_settings)
		bpy.utils.register_class(TILA_umi_settings)

		wm = context.window_manager
		if len(self.format_handler.format_annotations)-2 > 0 :
			return wm.invoke_props_dialog(self)
		else:
			return self.execute(context)

	def draw(self, context):
		layout = self.layout
		col = layout.column()
		if len(self.format_handler.format_annotations):
			col.label(text='{} Import Settings'.format(self.format_handler.format_name))
			col.separator()
			for k in self.__class__.__annotations__.keys():
				if not k in ['name', 'settings_imported', 'import_format']:
					col.prop(self, k)

class TILA_umi(bpy.types.Operator, ImportHelper):
	bl_idname = "import_scene.tila_universal_multi_importer"
	bl_label = "Import ALL"
	bl_options = {'REGISTER', 'INTERNAL'}
	bl_region_type = "UI"

	# Selected files
	files : bpy.props.CollectionProperty(type=bpy.types.PropertyGroup)
	create_collection_per_file : bpy.props.BoolProperty(name='Create collection per file', description='Each imported file will be placed in a collection', default=True)
	backup_file_after_import : bpy.props.BoolProperty(name='Backup file after each import', description='Backup file after importing file. The frequency will be made based on "Bakup Step Parameter"',  default=False)
	backup_step : bpy.props.IntProperty(name='Backup Step', description='Save file after X file imported', default=1, min=1, soft_max=50)
	skip_already_imported_files : bpy.props.BoolProperty(name='Skip already imported files', description='Import will be skipped if a Collection with the same name is found in the Blend file. "Create collection per file" need to be enabled', default=False)
	save_file_after_import : bpy.props.BoolProperty(name='Save file after import', description='Save the original file when the entire import process is compete', default=False)
	ignore_post_process_errors : bpy.props.BoolProperty(name='Ignore Post Process Errors', description='If any error occurs during prost processing of imported file, error will be ignore and the import process will continue', default=True)
	import_svg_as_grease_pencil : bpy.props.BoolProperty(name='Import SVG as Grease Pencil', description='SVG file will be imported as grease Pencil instead of curve objects', default=False)

	_timer = None
	thread = None
	progress = 0
	current_file_to_process = None
	processing = False
	all_parameters_imported = False
	first_setting_to_import = True
	format_to_import = []
	import_complete = False
	canceled = False
	end = False
	current_backup_step = 0
	counter = 0
	wait_before_hiding = 5
	counter_start_time = 0.0
	counter_end_time = 0.0
	delta = 0.0
	previous_counter = 0
	
	def decrement_counter(self):
		self.counter = self.counter + (self.counter_start_time - self.counter_end_time)*3000
	
	def store_delta_start(self):
		self.counter_start_time = time.perf_counter()

	def store_delta_end(self):
		self.counter_end_time = time.perf_counter()

	def log_enter_text(self):
		log.info('-----------------------------------')
		log.info('Click "ENTER" to hide this text ...')
		log.info('-----------------------------------')

	def draw(self, context):
		layout = self.layout
		col = layout.column()
		col.label(text='Import Settings')
		
		col.prop(self, 'create_collection_per_file')
		
		if self.create_collection_per_file:
			row = col.row()
			split = row.split(factor=0.1, align=True)
			split.label(text='')
			split = split.split()
			split.prop(self, 'skip_already_imported_files')

		col.prop(self, 'backup_file_after_import')


		if self.backup_file_after_import:
			row = col.row()
			split = row.split(factor=0.1, align=True)
			split.label(text='')
			split = split.split()
			split.prop(self, 'backup_step')

		
		col = layout.column()
		col.prop(self, 'save_file_after_import')
		col.prop(self, 'ignore_post_process_errors')
		# col.prop(self, 'import_svg_as_grease_pencil')
		

		col.separator()

		col.label(text='Batch process imported files')

		rows = len(context.scene.umi_settings.umi_operators) if len(context.scene.umi_settings.umi_operators) > 2 else 2
		row = col.row()
		row.template_list('UMI_UL_operator_list', '', context.scene.umi_settings, 'umi_operators', context.scene.umi_settings, 'umi_operator_idx', rows=rows)
		col2 = row.column()
		col2.operator('scene.umi_add_operator', text='', icon='ADD')
		col2.separator()
		col2.operator('scene.umi_move_operator', text='', icon='TRIA_UP').direction = 'UP'
		col2.operator('scene.umi_move_operator', text='', icon='TRIA_DOWN').direction = 'DOWN'
		col2.separator()
		col2.operator('scene.umi_clear_operators', text='', icon='TRASH')

	def recurLayerCollection(self, layerColl, collName):
		found = None
		if (layerColl.name == collName):
			return layerColl
		for layer in layerColl.children:
			found = self.recurLayerCollection(layer, collName)
			if found:
				return found

	def postImportCommand(self):
		# TODO : need to create a save/load preset for command list ( Macros ?)
		log.info('Post process file : {}'.format(path.basename(self.current_file_to_process)))
		for c in self.umi_settings.umi_operators:
			c = c.operator
			try:
				log.info('Executing command : "{}"'.format(c))
				exec(c, {'bpy':bpy})	
			except Exception as e:
				log.error('Post Import Command "{}" is not valid - {}'.format(c, e))
				if not self.ignore_post_process_errors:
					self.canceled = True

	def import_settings(self):
		self.current_format = self.format_to_import.pop()

		if len(self.format_to_import) == 0:
			self.umi_settings.umi_last_setting_to_get = True
		
		self.umi_settings.umi_current_format_setting_imported = False

		# gather import setting from the user for each format selected
		bpy.ops.import_scene.tila_universal_multi_importer_settings('INVOKE_DEFAULT', import_format=self.current_format['name'])
		self.first_setting_to_import = False

	def finish(self, context, canceled=False):
		bpy.types.SpaceView3D.draw_handler_remove(self._handle, 'WINDOW')
		self.revert_parameters(context)
		bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)
		if canceled:
			return {'CANCELLED'}
		else:
			return {'FINISHED'}

	def modal(self, context, event):
		if event.type in {'RIGHTMOUSE', 'ESC'} or self.canceled:
			log.error('Cancelling...')
			self.cancel(context)

			log.warning('Import Canceled')
			self.log_enter_text()
			self.counter = self.wait_before_hiding
			self.end = True

		if event.type == 'TIMER':
			if self.end:
				self.store_delta_start()

				if self.counter == self.wait_before_hiding:
					self.previous_counter = self.counter
					self.store_delta_end()
					
				remaining_seconds = math.ceil(self.counter)

				if remaining_seconds < self.previous_counter:
					log.info(f'Hidding in {remaining_seconds}s ...')
					self.previous_counter = remaining_seconds

				if self.counter <= 0:
					return self.finish(context, self.canceled)
				
				if event.type in {'RET'}:
					return self.finish(context, self.canceled)
				
				self.previous_counter = remaining_seconds
				self.store_delta_end()
				self.decrement_counter()
				bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)
				return {'PASS_THROUGH'}
		
			# Loop through all import format settings
			if not self.umi_settings.umi_ready_to_import:
				if not self.first_setting_to_import:
					if not self.umi_settings.umi_current_format_setting_imported:
						return {'PASS_THROUGH'}
					else:
						self.import_settings()
				else:
					self.import_settings()
			
			elif self.import_complete:
				self.log_enter_text()
				self.counter = self.wait_before_hiding
				self.end = True

			# Import Loop
			else:
				if not self.processing and self.current_file_to_process is None and len(self.filepaths): # Import can start
					self.next_file()
					self.import_file(self.current_file_to_process)
				elif self.current_file_to_process is None and len(self.filepaths):
					self.processing = False
				elif len(self.filepaths) == 0:
					if self.save_file_after_import:
						bpy.ops.wm.save_as_mainfile(filepath=self.current_blend_file, check_existing=False)

					log.complete_progress_importer()
					self.import_complete = True

		return {'PASS_THROUGH'}

	def import_command(self, filepath):
		ext = os.path.splitext(filepath)[1]
		operators = compatible_formats.get_operator_name_from_extension(ext)
		format_names = compatible_formats.get_format_from_extension(ext)['name']
		if operators is None:
			message = f"'{ext}' format is not supported"
			log.error(message)
			log.store_failure(message)
			return
			# raise Exception(message)

		if len(operators) == 1:
			operators = operators['default']
		else:
			if ext == '.svg':
				if self.import_svg_as_grease_pencil:
					operators = operators['grease_pencil']
				else:
					operators = operators['default']

		# Double \\ in the path causing error in the string
		args = eval(f'self.{format_names}_format.format_settings_dict', {'self':self})
		raw_path = filepath.replace('\\\\', punctuation[23])
		args['filepath'] = 'r"{}"'.format(raw_path)

		args_as_string = ''
		arg_number = len(args.keys())
		for k,v in args.items():
			if k in ['settings_imported', 'name']:
				arg_number -= 1
				continue
			args_as_string += ' {}={}'.format(k, v)
			if arg_number >= 2:
				args_as_string += ','

			arg_number -= 1
			
		command = '{}({})'.format(operators, args_as_string)
		print(command)
		# Execute the import command
		try:
			exec(command, {'bpy':bpy})
		except Exception as e:
			log.error(str(e))
			log.store_failure(str(e))
			return False
			# raise Exception(e)
		
		return True

	def import_file(self, filepath):

		self.processing = True

		filename = path.basename(path.splitext(filepath)[0])

		if self.skip_already_imported_files:
			if filename in bpy.data.collections:
				self.current_file_to_process = None
				self.processing = False
				log.warning('File {} have already been imported, skiping file...'.format(filename))
				return
		
		log.info('Importing file {}/{} - {}% : {}'.format(self.current_file_number, self.number_of_file, self.progress, filename))
		self.current_backup_step += 1

		if self.create_collection_per_file:
			collection = bpy.data.collections.new(name=filename)
			self.root_collection.children.link(collection)
			
			root_layer_col = self.view_layer.layer_collection    
			layer_col = self.recurLayerCollection(root_layer_col, collection.name)
			self.view_layer.active_layer_collection = layer_col
		
		succeeded = self.import_command(filepath=filepath)
		
		if succeeded:

			self.postImportCommand()

			if self.backup_file_after_import:
				if self.backup_step <= self.current_backup_step:
					self.current_backup_step = 0
					log.info('Saving backup file : {}'.format(path.basename(self.blend_backup_file)))
					bpy.ops.wm.save_as_mainfile(filepath=self.blend_backup_file, check_existing=False, copy=True)

			message = 'File {} is imported successfully : {}'.format(self.current_file_number, filename)
			self.current_file_number += 1
			log.success(message)
			log.store_success(message)
		
		# time.sleep(.5)
		self.progress += 100/self.number_of_file

		self.current_file_to_process = None

	def get_compatible_extensions(self):
		return compatible_formats.extensions

	def store_format_to_import(self):
		for f in self.filepaths:
			format = compatible_formats.get_format_from_extension(path.splitext(f)[1])
			if format not in self.format_to_import:
				self.format_to_import.append(format)

	def revert_parameters(self, context):
		self.format_to_import = []
		self.all_parameters_imported = False
		self.thread = None
		self.progress = 0
		self.current_backup_step = 0
		self.current_file_to_process = None
		self.processing = False
		self.first_setting_to_import = True
		self.import_complete = False
		self.canceled = False
		self.end = False
		self.umi_settings.umi_last_setting_to_get = False
		self.umi_settings.umi_ready_to_import = False
		self.umi_settings.umi_current_format_setting_imported = False
		context.window_manager.event_timer_remove(self._timer)
		log.clear_all()
	
	def execute(self,context):
		bpy.utils.unregister_class(TILA_umi_settings)
		bpy.utils.register_class(TILA_umi_settings)
		self.current_blend_file = bpy.data.filepath

		for f in compatible_formats.formats:
			exec('self.{}_format = TILA_umi_format_handler(import_format="{}", context=cont)'.format(f[0], f[0]), {'self':self, 'TILA_umi_format_handler':TILA_umi_format_handler, 'cont':context})

		if not path.exists(self.current_blend_file):
			log.warning('Blender file not saved')
			self.save_file_after_import = False
			autosave = path.join(bpy.utils.user_resource(resource_type='AUTOSAVE', create=True), 'umi_autosave_' + time.strftime('%Y-%m-%d-%H-%M-%S') + '.blend')
		else:
			autosave = path.splitext(self.current_blend_file)[0] + "_bak" + path.splitext(self.current_blend_file)[1]

		self.blend_backup_file = autosave
		
		compatible_extensions = self.get_compatible_extensions()
		self.folder = (os.path.dirname(self.filepath))
		self.filepaths = [path.join(self.folder, f.name) for f in self.files if path.splitext(f.name)[1].lower() in compatible_extensions]

		if not len(self.filepaths):
			message = "No compatible file selected"
			log.error(message)
			self.report({'ERROR'}, message)
			return {'CANCELLED'}

		self.filepaths.reverse()
		self.number_of_file = len(self.filepaths)

		log.info("{} compatible file(s) found".format(len(self.filepaths)))
		log.separator()

		self.view_layer = bpy.context.view_layer
		self.root_collection = bpy.context.collection
		self.current_file_number = 1

		self.umi_settings = context.scene.umi_settings

		context.scene.umi_settings.umi_ready_to_import = False

		self.store_format_to_import()

		args = (context,)
		self._handle = bpy.types.SpaceView3D.draw_handler_add(log.draw_callback_px, args, 'WINDOW', 'POST_PIXEL')

		self.progress += 100/self.number_of_file
		wm = context.window_manager
		self._timer = wm.event_timer_add(0.1, window=context.window)
		wm.modal_handler_add(self)
		return {'RUNNING_MODAL'}
	
	def next_file(self):
		self.current_file_to_process = self.filepaths.pop()

	def cancel(self, context):
		if self._timer is not None:
			wm = context.window_manager
			wm.event_timer_remove(self._timer)

class TILA_UL_umi_operator_list(bpy.types.UIList):
	bl_idname = "UMI_UL_operator_list"

	def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
		scn = context.scene

		col = layout.column_flow(columns=2, align=True)

		row = col.row(align=True)
		row.alignment = 'LEFT'
		row.label(text='{}'.format(item.operator))

		row = col.row(align=True)
		row.alignment = 'RIGHT'

		row.operator('scene.umi_edit_operator', text='', icon='GREASEPENCIL').id = index
		row.operator('scene.umi_duplicate_operator', text='', icon='PASTEDOWN').id = index
		row.separator()
		row.operator('scene.umi_remove_operator', text='', icon='PANEL_CLOSE').id = index


# function to append the operator in the File>Import menu
def menu_func_import(self, context):
	self.layout.operator(TILA_umi.bl_idname, text="Universal Multi Importer")

# function to register dynamically generated classes for each compatible formats
def register_import_setting_class():
	for f in compatible_formats.formats:
		cl_name = 'TILA_umi_{}_settings'.format(f[1]['name'])
		cl = eval(cl_name)
		exec('TILA_umi_import_settings.__annotations__["{}_import_settings"] = bpy.props.PointerProperty(type={})'.format(f[1]['name'], cl_name), {'bpy': bpy, 'TILA_umi_import_settings':TILA_umi_import_settings, cl_name:cl})
	TILA_umi_import_settings.umi_import_settings_registered = True


classes = (
	TILA_UL_umi_operator_list,
	TILA_umi_operator,
	TILA_umi_import_settings,
	TILA_umi_scene_settings,
	TILA_umi_settings,
	TILA_umi,
	LM_UI_MoveOperator,
	LM_UI_ClearOperators,
	LM_UI_RemoveOperator,
	LM_UI_DuplicateOperator,
	LM_UI_EditOperator,
	LM_UI_AddOperator
)


def register():
	parser = TILA_format_class_creator()
	parser.register_compatible_formats()
	register_import_setting_class()
	
	for cls in classes:
		bpy.utils.register_class(cls)
	
	bpy.types.Scene.umi_settings = bpy.props.PointerProperty(type=TILA_umi_scene_settings)
	bpy.types.TOPBAR_MT_file_import.append(menu_func_import)

def unregister():
	for cls in reversed(classes):
		bpy.utils.unregister_class(cls)
	parser = TILA_format_class_creator()
	parser.unregister_compatible_formats()
	del bpy.types.Scene.umi_settings
	bpy.types.TOPBAR_MT_file_import.remove(menu_func_import)

if __name__ == "__main__":
	register()