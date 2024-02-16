import bpy
import time, math
from ..formats.properties import PG_Operator
from ..logger import LOG, LoggerColors
from ..preferences import get_prefs

def draw_command_batcher(self, context):
	layout = self.layout
	col = layout.column()
	
	box = col.box()
	row = box.row()
	row.label(text='Command Batcher Operators')

	rows = len(context.scene.umi_settings.umi_operators) if len(context.scene.umi_settings.umi_operators) > 2 else 2
	row = box.row()
	row.template_list('UMI_UL_operator_list', '', context.scene.umi_settings, 'umi_operators', context.scene.umi_settings, 'umi_operator_idx', rows=rows)
	col2 = row.column()
	
	col2.separator()
	
	col2.operator('scene.umi_add_operator', text='', icon='ADD')
	col2.separator()
	col2.operator('scene.umi_move_operator', text='', icon='TRIA_UP').direction = 'UP'
	col2.operator('scene.umi_move_operator', text='', icon='TRIA_DOWN').direction = 'DOWN'
	col2.separator()
	col2.operator('scene.umi_clear_operators', text='', icon='TRASH')


	box = col.box()
	row = box.row()
	row.label(text='Command Batcher Presets')

	rows = len(context.scene.umi_settings.umi_presets) if len(context.scene.umi_settings.umi_presets) > 2 else 2
	row = box.row()
	row.template_list('UMI_UL_preset_list', '', context.scene.umi_settings, 'umi_presets', context.scene.umi_settings, 'umi_preset_idx', rows=rows)
	col2 = row.column()
	col2.separator()
	col2.operator('scene.umi_add_preset', text='', icon='ADD')
	col2.separator()
	col2.operator('scene.umi_move_preset', text='', icon='TRIA_UP').direction = 'UP'
	col2.operator('scene.umi_move_preset', text='', icon='TRIA_DOWN').direction = 'DOWN'
	col2.separator()
	col2.operator('scene.umi_clear_presets', text='', icon='TRASH')
	

class CommandBatcher(bpy.types.Operator):
	bl_idname = "object.tila_umi_command_batcher"
	bl_label = "Command Batcher"
	bl_options = {'REGISTER'}

	operator_list : bpy.props.CollectionProperty(type=PG_Operator)
	importer_mode : bpy.props.BoolProperty(name='Importer_mode', default=False) 
	
	finished = False
	current_command = None
	progress = 0
	processing = False
	process_complete = False
	canceled = False
	end = False
	counter = 0
	counter_start_time = 0.0
	counter_end_time = 0.0
	delta = 0.0
	previous_counter = 0
	objects_to_process = []
	current_object_to_process = None
	_timer = None

	def fill_operator_to_process(self):
		operator_list = [{'name':'operator', 'operator': o.operator} for o in self.umi_settings.umi_operators]
		self.operators_to_process = [o['operator'] for o in operator_list]
		self.operators_to_process.reverse()

	def decrement_counter(self):
		self.counter = self.counter + (self.counter_start_time - self.counter_end_time)*1000
	
	def store_delta_start(self):
		self.counter_start_time = time.perf_counter()

	def store_delta_end(self):
		self.counter_end_time = time.perf_counter()
		
	def log_end_text(self):
		LOG.info('-----------------------------------')
		if self.canceled:
			LOG.info('Batch Process cancelled !', color=LoggerColors.CANCELLED_COLOR)
		else:
			if False in self.process_succeeded:
				LOG.info('Batch Process completed with errors !', color=LoggerColors.ERROR_COLOR)
				LOG.esc_message = '[Esc] to Hide'
				LOG.message_offset = 4
			else:
				LOG.info('Batch Process completed successfully !', color=LoggerColors.SUCCESS_COLOR)
				LOG.esc_message = '[Esc] to Hide'
				LOG.message_offset = 4
		LOG.info('Click [ESC] to hide this text ...')
		LOG.info('-----------------------------------')
		self.end_text_written = True
		bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)
	
	def invoke(self, context, event):
		if not self.importer_mode:
			bpy.ops.scene.umi_load_preset_list()
			
			wm = context.window_manager
			return wm.invoke_props_dialog(self, width=900)
		
		return self.execute(context)

	def finish(self, context, canceled=False):
		if not self.importer_mode:
			bpy.types.SpaceView3D.draw_handler_remove(self._handle, 'WINDOW')
		self.revert_parameters(context)
		bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)
		self.umi_settings.umi_batcher_is_processing = False
		if canceled:
			return {'CANCELLED'}
		else:
			return {'FINISHED'}
		
	def modal(self, context, event):
		if self.start_time == 0 :
			self.start_time = time.perf_counter()
		if not self.importer_mode and not self.end and event.type in {'ESC'} and event.value == 'PRESS':
			if not self.importer_mode:
				LOG.warning('Cancelling...')
			self.cancel(context)

			self.counter = self.wait_before_hiding
			self.end = True
			LOG.completed = True
			return {'RUNNING_MODAL'}
		
		if not self.importer_mode and self.end:

			if not self.end_text_written:
				self.log_end_text()
				LOG.completed = True
				bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)
			
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
			
			if self.auto_hide_text_when_finished:
				self.store_delta_start()

				if self.counter == self.wait_before_hiding:
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
			
			if self.auto_hide_text_when_finished:
				self.previous_counter = remaining_seconds
				self.store_delta_end()
				self.decrement_counter()
				bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)

			return {'RUNNING_MODAL'}

		if event.type == 'TIMER':
			if self.start_time == 0:
				self.start_time = time.perf_counter()
			if not self.processing and self.current_object_to_process is None and len(self.objects_to_process): # Process can start
				self.next_object()

			elif self.current_object_to_process is None and len(self.objects_to_process):
				self.processing = False

			elif self.current_object_to_process is None and len(self.objects_to_process) == 0:
				if not self.importer_mode:
					LOG.complete_progress_importer(show_successes=False, duration=round(time.perf_counter() - self.start_time, 2))
					self.counter = self.wait_before_hiding
				else:
					self.finished = True
				self.end = True

			if self.finished:
				return self.finish(context)

			if self.current_command is None and len(self.operators_to_process):
				self.current_command = self.operators_to_process.pop()

			if self.current_command is None and not len(self.operators_to_process):
				self.current_object_to_process = None

			else:
				try: # Executing command
					self.progress += 100 / self.number_of_operations_to_perform
					self.current_operation_number += 1
					
					LOG.info(f'Executing command {self.current_operation_number}/{self.number_of_operations_to_perform} - {round(self.progress,2)}% : "{self.current_command}"', color=LoggerColors.COMMAND_COLOR)
					bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)
					exec(self.current_command, {'bpy':bpy})
					LOG.store_success('Command executed successfully')
					self.process_succeeded.append(True)
				except Exception as e:
					message = f'{context.selected_objects[0].name} : Command "{self.current_command}" is not valid - {e}'
					LOG.error(message)
					LOG.store_failure(message)
					self.process_succeeded.append(False)
				
				self.current_command = None

		return {'PASS_THROUGH'}
	
	def execute(self, context):
		self.preferences = get_prefs()
		self.auto_hide_text_when_finished = self.preferences.auto_hide_text_when_finished
		self.wait_before_hiding = self.preferences.wait_before_hiding
		self.completed = False
		self.succeedeed = False
		self.end_text_written = False
		self.start_time = 0
		self.process_succeeded = []
		LOG.esc_message = '[Esc] to Cancel'
		LOG.message_offset = 15
		LOG.show_log = self.preferences.show_log_on_3d_view
		self.umi_settings = context.scene.umi_settings

		if not self.importer_mode:
			LOG.revert_parameters()

		self.objects_to_process = [o for o in bpy.context.selected_objects]
		if not len(self.objects_to_process):
			self.report({'ERROR_INVALID_INPUT'}, 'UMI : You need to select at least one object.')
			return {'CANCELLED'}
		
		if not self.importer_mode and not len(self.umi_settings.umi_operators):
			self.report({'ERROR_INVALID_INPUT'}, 'UMI : You need to add at least one command.')
			return {'CANCELLED'}
		
		self.progress = 0
		self.number_of_operations_to_perform = 0
		self.number_of_object_to_process = len(self.objects_to_process)
		self.current_operation_number = 0
		self.current_object_number = 0

		if not self.importer_mode:
			self.next_object()

			args = (context,)
			self._handle = bpy.types.SpaceView3D.draw_handler_add(LOG.draw_callback_px, args, 'WINDOW', 'POST_PIXEL')
		else:
			operator_list = self.operator_list
			self.operators_to_process = [o.operator for o in operator_list]
			self.operators_to_process.reverse()

		number_of_operations = len(self.operators_to_process)
		number_of_objects = len(self.objects_to_process)

		self.number_of_operations_to_perform = number_of_operations * number_of_objects

		self.register_timer(context)
		self.umi_settings.umi_batcher_is_processing = True
		return {'RUNNING_MODAL'}
	
	def draw(self, context):
		draw_command_batcher(self, context)

	def revert_parameters(self, context):
		self.finished = False
		self.progress = 0
		self.processing = False
		self.process_complete = False
		self.canceled = False
		self.end = False
		self.completed = False
		self.end_text_written = False
		self.process_succeeded = []
		context.window_manager.event_timer_remove(self._timer)
		if not self.importer_mode:
			LOG.clear_all()
			LOG.revert_parameters()

	def cancel(self, context):
		self.canceled = True
		if self._timer is not None:
			wm = context.window_manager
			wm.event_timer_remove(self._timer)
	
	def register_timer(self, context):
		wm = context.window_manager
		self._timer = wm.event_timer_add(0.01, window=context.window)
		wm.modal_handler_add(self)
		
	def next_object(self):
		if self.importer_mode:
			if self.umi_settings.umi_import_settings.umi_import_cancelled:
				self.canceled = True
				return
		else:
			LOG.separator()
			
		self.current_object_to_process = self.objects_to_process.pop()
		self.current_object_number += 1
		self.object_progress = round(self.current_object_number * 100 / self.number_of_object_to_process, 2)
		
		LOG.info(f'Processing object {self.current_object_number}/{self.number_of_object_to_process} - {self.object_progress}% : {self.current_object_to_process.name}')
		bpy.ops.object.select_all(action='DESELECT')
		bpy.data.objects[self.current_object_to_process.name].select_set(True)
		self.fill_operator_to_process()

# function to append the operator in the File>Import menu
def menu_func_object(self, context):
	self.layout.separator()
	op = self.layout.operator(CommandBatcher.bl_idname, text="Command Batcher", icon='SHORTDISPLAY')
	op.importer_mode = False

classes = (CommandBatcher,)

def register():
	from bpy.utils import register_class
	for cls in classes:
		register_class(cls)
	
	bpy.types.VIEW3D_MT_object.append(menu_func_object)


def unregister():
	bpy.types.VIEW3D_MT_object.remove(menu_func_object)
	
	from bpy.utils import unregister_class
	for cls in reversed(classes):
		unregister_class(cls)

if __name__ == "__main__":
	register()