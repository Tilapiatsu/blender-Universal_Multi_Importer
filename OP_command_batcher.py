import bpy
from .constant import LOG
from .property_group import TILA_umi_operator
from .OP_ui_list_operators import *
from .OP_ui_list_preset import *

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
	show_dialog : bpy.props.CollectionProperty(name='show_dialog', default=False) 
	
	finished = False
	current_command = None
	
	def invoke(self, context, event):
		
		self.operator_to_process = [o.operator for o in self.operator_list]

		wm = context.window_manager
		if self.show_dialog:
			return wm.invoke_props_dialog(self, width=900)
	
		self._timer = wm.event_timer_add(0.1, window=context.window)
		wm.modal_handler_add(self)
		return {'RUNNING_MODAL'}
	
	def revert_parameters(self, context):
		self.finished = False
		context.window_manager.event_timer_remove(self._timer)

	def finish(self, context):
		self.revert_parameters(context)
		bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)
		return {'FINISHED'}
		
	def modal(self, context, event):
		if self.finished:
			return self.finish(context)

		if self.current_command is None and len(self.operator_to_process):
			self.current_command = self.operator_to_process.pop()

		if self.current_command is None and not len(self.operator_to_process):
			self.finished = True

		else:
			try:
				LOG.info(f'Executing command : "{self.current_command}"')
				exec(self.current_command, {'bpy':bpy})
			except Exception as e:
				LOG.error('Post Import Command "{}" is not valid - {}'.format(self.current_command, e)) 
				
			self.current_command = None
		
		return {'PASS_THROUGH'}
	
	def draw(self, context):
		draw_command_batcher(self, context)
