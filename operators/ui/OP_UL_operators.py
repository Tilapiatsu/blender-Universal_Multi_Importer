import bpy
import os
from ...umi_const import get_umi_settings
from .operators_const import PRESET_FOLDER

if not os.path.exists(PRESET_FOLDER):
		print(f'UMI : Creating Preset Folder : {PRESET_FOLDER}')
		os.mkdir(PRESET_FOLDER)

def get_operator(self):
	idx = self.umi_settings.umi_operator_idx
	operators = self.umi_settings.umi_operators

	active = operators[idx] if len(operators) else None

	return idx, operators, active


class UI_UMIMoveOperator(bpy.types.Operator):
	bl_idname = "scene.umi_move_operator"
	bl_label = "Move Operator"
	bl_options = {'REGISTER', 'UNDO'}
	bl_description = "Move Operator up or down.\nThis controls the position in the Menu."

	direction: bpy.props.EnumProperty(items=[("UP", "Up", ""), ("DOWN", "Down", "")])

	@classmethod
	def poll(cls, context):
		umi_settings = get_umi_settings()
		return len(umi_settings.umi_operators)

	def execute(self, context):
		umi_settings = get_umi_settings()
		idx, camera, _ = get_operator(context)

		if self.direction == "UP":
			nextidx = max(idx - 1, 0)
		elif self.direction == "DOWN":
			nextidx = min(idx + 1, len(camera) - 1)

		camera.move(idx, nextidx)
		umi_settings.umi_operator_idx = nextidx

		return {'FINISHED'}


class UI_UMIClearOperators(bpy.types.Operator):
	bl_idname = "scene.umi_clear_operators"
	bl_label = "Clear All Operators"
	bl_options = {'REGISTER', 'UNDO'}
	bl_description = "Clear All Operators."

	@classmethod
	def poll(cls, context):
		umi_settings = get_umi_settings()
		return len(umi_settings.umi_operators)
	
	def invoke(self, context, event):
		wm = context.window_manager
		return wm.invoke_confirm(self, event)

	def execute(self, context):
		umi_settings = get_umi_settings()
		umi_settings.umi_operators.clear()

		return {'FINISHED'}


class UI_UMIRemoveOperator(bpy.types.Operator):
	bl_idname = "scene.umi_remove_operator"
	bl_label = "Remove Selected Operator"
	bl_options = {'REGISTER', 'UNDO'}
	bl_description = "Remove selected Operator."
	
	id : bpy.props.IntProperty(name="Operator ID", default=0)

	@classmethod
	def poll(cls, context):
		umi_settings = get_umi_settings()
		return umi_settings.umi_operators
	
	def invoke(self, context, event):
		wm = context.window_manager
		return wm.invoke_confirm(self, event)

	def execute(self, context):
		umi_settings = get_umi_settings()
		_, operators, _ = get_operator(context)

		operators.remove(self.id)

		umi_settings.umi_operator_idx = min(self.id, len(umi_settings.umi_operators) - 1)

		return {'FINISHED'}


class UI_UMIDuplicateOperator(bpy.types.Operator):
	bl_idname = "scene.umi_duplicate_operator"
	bl_label = "Duplicate Selected Operator"
	bl_options = {'REGISTER', 'UNDO'}
	bl_description = "Duplicate selected Operator."
	
	id : bpy.props.IntProperty(name="Operator ID", default=0)

	@classmethod
	def poll(cls, context):
		umi_settings = get_umi_settings()
		return umi_settings.umi_operators

	def execute(self, context):
		_, operators, _ = get_operator(context)

		o = operators.add()
		o.operator = operators[self.id].operator
		operators.move(len(operators) - 1, self.id + 1)

		return {'FINISHED'}


class UI_UMIEditOperator(bpy.types.Operator):
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
		self.umi_settings = get_umi_settings()
		current_operator = self.umi_settings.umi_operators[self.id]
		self.operator = current_operator.operator
		wm = context.window_manager
		return wm.invoke_props_dialog(self, width=900)
	
	def execute(self, context):
		o = self.umi_settings.umi_operators[self.id]
		o.operator = self.operator
		return {'FINISHED'}


class UI_UMIAddOperator(bpy.types.Operator):
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
		self.umi_settings = get_umi_settings()
		o = self.umi_settings.umi_operators.add()
		o.operator = self.operator
		return {'FINISHED'}
	

classes = ( UI_UMIMoveOperator, 
			UI_UMIClearOperators, 
			UI_UMIRemoveOperator, 
			UI_UMIDuplicateOperator,
			UI_UMIEditOperator,
			UI_UMIAddOperator)

def register():
	from bpy.utils import register_class
	for cls in classes:
		register_class(cls)


def unregister():
	from bpy.utils import unregister_class
	for cls in reversed(classes):
		unregister_class(cls)

if __name__ == "__main__":
	register()