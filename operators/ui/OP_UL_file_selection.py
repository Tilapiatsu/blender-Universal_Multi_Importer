import bpy
import os


def get_file_selection(context):
	idx = context.scene.umi_settings.umi_file_selection_idx
	file_selection = context.scene.umi_settings.umi_file_selection

	active = file_selection[idx] if len(file_selection) else None

	return idx, file_selection, active


class UI_Select(bpy.types.Operator):
	bl_idname = "scene.umi_select_file"
	bl_label = "Select File"
	bl_options = {'REGISTER', 'UNDO'}
	bl_description = "Select Files"

	mode: bpy.props.EnumProperty(items=[("SELECT_ALL", "Select All", ""), ("DESELECT_ALL", "Deselect All", "")])

	@classmethod
	def poll(cls, context):
		return len(context.scene.umi_settings.umi_file_selection)

	def execute(self, context):
		_, file_selection, _ = get_file_selection(context)

		if self.mode == "SELECT_ALL":
			for f in file_selection:
				f.check = True
		elif self.mode == "DESELECT_ALL":
			for f in file_selection:
				f.check = False

		return {'FINISHED'}

classes = ( UI_Select, 
			)

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