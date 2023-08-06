import bpy
from bpy_extras.io_utils import ImportHelper, ExportHelper

def get_operator(context):
	idx = context.scene.umi_settings.umi_operator_idx
	operators = context.scene.umi_settings.umi_operators

	active = operators[idx] if operators else None

	return idx, operators, active


class LM_UI_MoveOperator(bpy.types.Operator):
	bl_idname = "scene.umi_move_operator"
	bl_label = "Move Operator"
	bl_options = {'REGISTER', 'UNDO'}
	bl_description = "Move Camera keyword Name up or down.\nThis controls the position in the Menu."

	direction: bpy.props.EnumProperty(items=[("UP", "Up", ""), ("DOWN", "Down", "")])

	def execute(self, context):
		idx, camera, _ = get_operator(context)

		if self.direction == "UP":
			nextidx = max(idx - 1, 0)
		elif self.direction == "DOWN":
			nextidx = min(idx + 1, len(camera) - 1)

		camera.move(idx, nextidx)
		context.scene.umi_settings.umi_operator_idx = nextidx

		return {'FINISHED'}


class LM_UI_ClearOperators(bpy.types.Operator):
	bl_idname = "scene.umi_clear_operators"
	bl_label = "Clear All Operators"
	bl_options = {'REGISTER', 'UNDO'}
	bl_description = "Clear All Operators."

	@classmethod
	def poll(cls, context):
		return context.scene.umi_settings.umi_operators

	def execute(self, context):
		context.scene.umi_settings.umi_operators.clear()

		return {'FINISHED'}


class LM_UI_RemoveOperator(bpy.types.Operator):
	bl_idname = "scene.umi_remove_operator"
	bl_label = "Remove Selected Operator"
	bl_options = {'REGISTER', 'UNDO'}
	bl_description = "Remove selected Operator."
	
	id : bpy.props.IntProperty(name="Operator ID", default=0)

	@classmethod
	def poll(cls, context):
		return context.scene.umi_settings.umi_operators

	def execute(self, context):
		_, operators, _ = get_operator(context)

		operators.remove(self.id)

		context.scene.umi_settings.umi_operator_idx = min(self.id, len(context.scene.umi_settings.umi_operators) - 1)

		return {'FINISHED'}

class LM_UI_DuplicateOperator(bpy.types.Operator):
	bl_idname = "scene.umi_duplicate_operator"
	bl_label = "Duplicate Selected Operator"
	bl_options = {'REGISTER', 'UNDO'}
	bl_description = "Duplicate selected Operator."
	
	id : bpy.props.IntProperty(name="Operator ID", default=0)

	@classmethod
	def poll(cls, context):
		return context.scene.umi_settings.umi_operators

	def execute(self, context):
		_, operators, _ = get_operator(context)

		o = operators.add()
		o.operator = operators[self.id].operator
		operators.move(len(operators) - 1, self.id + 1)

		return {'FINISHED'}

class LM_UI_EditOperator(bpy.types.Operator):
	bl_idname = "scene.umi_edit_operator"
	bl_label = "Edit Operator"
	bl_options = {'REGISTER', 'UNDO'}
	bl_description = "Edit current operator"

	id : bpy.props.IntProperty(name="Operator ID", default=0)
	operator : bpy.props.StringProperty(name="Operator Command", default="")

	def draw(self, context):
		layout = self.layout
		col = layout.column()
		col.prop(self, 'operator', text='Command')
	
	def invoke(self, context, event):
		current_operator = context.scene.umi_settings.umi_operators[self.id]
		self.operator = current_operator.operator
		wm = context.window_manager
		return wm.invoke_props_dialog(self, width=900)
	
	def execute(self, context):
		o = context.scene.umi_settings.umi_operators[self.id]
		o.operator = self.operator
		return {'FINISHED'}

class LM_UI_AddOperator(bpy.types.Operator):
	bl_idname = "scene.umi_add_operator"
	bl_label = "Add Operator"
	bl_options = {'REGISTER', 'UNDO'}
	bl_description = "Add a new operator"

	operator : bpy.props.StringProperty(name="Operator Command", default="")

	def draw(self, context):
		layout = self.layout
		col = layout.column()
		col.prop(self, 'operator', text='Command')

	def invoke(self, context, event):
		wm = context.window_manager
		return wm.invoke_props_dialog(self, width=900)

	def execute(self, context):
		o = context.scene.umi_settings.umi_operators.add()
		o.operator = self.operator
		return {'FINISHED'}
	

class LM_UI_SavePresetOperator(bpy.types.Operator, ExportHelper):
	bl_idname = "scene.umi_save_preset_operator"
	bl_label = "Save Preset"
	bl_options = {'REGISTER', 'UNDO'}
	bl_description = "Save a preset of the current operator list to a preset file on your disk"
	
	filepath: bpy.props.StringProperty(
		name="File Path",
		description="Filepath used for exporting the file",
		maxlen=1024,
		subtype='FILE_PATH',
	)
	check_existing: bpy.props.BoolProperty(
		name="Check Existing",
		description="Check and warn on overwriting existing files",
		default=True,
		options={'HIDDEN'},
	)

	check_extension = True
	filename_ext = '.umipreset'
	
	def invoke(self, context, event):
		# return wm.invoke_props_dialog(self, width=900)
		import os
		if not self.filepath:
			blend_filepath = context.blend_data.filepath
			if not blend_filepath:
				blend_filepath = "untitled"
			else:
				blend_filepath = os.path.splitext(blend_filepath)[0]

			self.filepath = blend_filepath + self.filename_ext

		context.window_manager.fileselect_add(self)
		return {'RUNNING_MODAL'}


	# def draw(self, context):
	# 	layout = self.layout
	# 	col = layout.column()
	# 	col.prop(self, 'operator', text='Command')

	def execute(self, context):
		print('Saving preset')
		return {'FINISHED'}
	

class LM_UI_LoadPresetOperator(bpy.types.Operator, ImportHelper):
	bl_idname = "scene.umi_load_preset_operator"
	bl_label = "Load Preset"
	bl_options = {'REGISTER', 'UNDO'}
	bl_description = "Load a preset and add the commands at the end of the current list"

	operator : bpy.props.StringProperty(name="Operator Command", default="")

	filename_ext = '.umipreset'

	def draw(self, context):
		layout = self.layout
		col = layout.column()
		col.prop(self, 'operator', text='Command')

	def invoke(self, context, event):
		wm = context.window_manager
		return wm.invoke_props_dialog(self, width=900)

	def execute(self, context):
		o = context.scene.umi_settings.umi_operators.add()
		o.operator = self.operator
		return {'FINISHED'}