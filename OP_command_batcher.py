import bpy
import time, math
from .constant import LOG
from .property_group import TILA_umi_operator

def draw_command_batcher(self, context):
	layout = self.layout
	col = layout.column()
	
	box = col.box()
	row = box.row()
	row.label(text='Batch process imported files')

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
	row.label(text='Batch Process Presets')

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
	

class TILA_umi_command_batcher(bpy.types.Operator):
	bl_idname = "object.tila_umi_command_batcher"
	bl_label = "Command Batcher"
	bl_options = {'REGISTER'}

	operator_list : bpy.props.CollectionProperty(type=TILA_umi_operator)
	importer_mode : bpy.props.BoolProperty(name='Importer_mode', default=False) 
	
	finished = False
	current_command = None
	progress = 0
	processing = False
	process_complete = False
	canceled = False
	end = False
	counter = 0
	wait_before_hiding = 5
	counter_start_time = 0.0
	counter_end_time = 0.0
	delta = 0.0
	previous_counter = 0
	objects_to_process = []
	current_object_to_process = None

	def fill_operator_to_process(self):
		operator_list = [{'name':'operator', 'operator': o.operator} for o in bpy.context.scene.umi_settings.umi_operators]
		self.operators_to_process = [o['operator'] for o in operator_list]
		self.operators_to_process.reverse()

	def decrement_counter(self):
		self.counter = self.counter + (self.counter_start_time - self.counter_end_time)*1000
	
	def store_delta_start(self):
		self.counter_start_time = time.perf_counter()

	def store_delta_end(self):
		self.counter_end_time = time.perf_counter()

	def log_enter_text(self):
		LOG.info('-----------------------------------')
		LOG.info('Click "ENTER" to hide this text ...')
		LOG.info('-----------------------------------')
	
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
		bpy.context.scene.umi_settings.umi_batcher_is_processing = False
		if canceled:
			return {'CANCELLED'}
		else:
			return {'FINISHED'}
		
	def modal(self, context, event):
		if not self.end and event.type in {'RIGHTMOUSE', 'ESC'}:
			LOG.error('Cancelling...')
			self.cancel(context)

			self.log_enter_text()
			self.counter = self.wait_before_hiding
			self.end = True


		if self.end and event.type in {'RET'}:
			return self.finish(context, self.canceled)
		
		if not self.importer_mode and self.end:
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
			
			if event.type in {'RET'}:
				return self.finish(context, self.canceled)
			
			self.previous_counter = remaining_seconds
			self.store_delta_end()
			self.decrement_counter()
			bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)
			return {'PASS_THROUGH'}
		
		if event.type == 'TIMER':
			if not self.processing and self.current_object_to_process is None and len(self.objects_to_process): # Process can start
				self.next_object()
			elif self.current_object_to_process is None and len(self.objects_to_process):
				self.processing = False
			elif len(self.objects_to_process) == 0:
				if not self.importer_mode:
					LOG.complete_progress_importer()
					self.end = True
					self.counter = self.wait_before_hiding

			if self.finished:
				return self.finish(context)

			if self.current_command is None and len(self.operators_to_process):
				self.current_command = self.operators_to_process.pop()

			if self.current_command is None and not len(self.operators_to_process):
				self.current_object_to_process = None
				if self.importer_mode:
					self.finished = True

			else:
				try: # Executing command
					self.progress += 100 / self.number_of_operations_to_perform
					self.current_operation_number += 1
					
					LOG.info(f'Executing command {self.current_operation_number}/{self.number_of_operations_to_perform} - {round(self.progress,2)}% : "{self.current_command}"', color=(0.95, 0.71, 0.10))
					bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)
					exec(self.current_command, {'bpy':bpy})
				except Exception as e:
					LOG.error('Post Import Command "{}" is not valid - {}'.format(self.current_command, e))
				
				self.current_command = None

		return {'PASS_THROUGH'}
	
	def execute(self, context):
		self.objects_to_process = [o for o in bpy.context.selected_objects]
		if not len(self.objects_to_process):
			self.report({'ERROR_INVALID_INPUT'}, 'UMI : You have to select at least one object.')
			return {'CANCELLED'}
		
		if not self.importer_mode and not len(bpy.context.scene.umi_settings.umi_operators):
			self.report({'ERROR_INVALID_INPUT'}, 'UMI : You need to add at least one command.')
			return {'CANCELLED'}
		
		self.progress = 0
		self.number_of_operations_to_perform = 0
		self.current_operation_number = 0

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

		wm = context.window_manager
		self._timer = wm.event_timer_add(0.1, window=context.window)
		wm.modal_handler_add(self)
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
		context.window_manager.event_timer_remove(self._timer)
		if not self.importer_mode:
			LOG.clear_all()

	def cancel(self, context):
		if self._timer is not None:
			wm = context.window_manager
			wm.event_timer_remove(self._timer)

	def next_object(self):
		self.current_object_to_process = self.objects_to_process.pop()
		if not self.importer_mode:
			LOG.separator()
			LOG.info(f'Processing {self.current_object_to_process.name}')
		bpy.ops.object.select_all(action='DESELECT')
		bpy.data.objects[self.current_object_to_process.name].select_set(True)
		self.fill_operator_to_process()
