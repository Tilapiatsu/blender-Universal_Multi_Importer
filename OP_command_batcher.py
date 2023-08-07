import bpy
from .constant import LOG
from .property_group import TILA_umi_operator


class TILA_umi_command_batcher(bpy.types.Operator):
	bl_idname = "object.tila_umi_command_batcher"
	bl_label = "Command Batcher"
	bl_options = {'REGISTER'}
	operator_list : bpy.props.CollectionProperty(type=TILA_umi_operator)
	
	finished = False
	current_command = None
	
	def invoke(self, context, event):

		self.operator_to_process = [o.operator for o in self.operator_list]

		wm = context.window_manager
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
