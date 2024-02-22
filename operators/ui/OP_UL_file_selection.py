import bpy
import os
from ...formats.properties.properties import update_file_stats


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

	action: bpy.props.EnumProperty(items=[("SELECT", "Select", ""), ("DESELECT", "Deselect", "")])
	mode: bpy.props.EnumProperty(items=[('ALL', 'All', ''), ('EXTENSION', 'Extension', ''), ('SIZE', 'Size', ''), ('NAME', 'name', '')])

	@classmethod
	def poll(cls, context):
		return len(context.scene.umi_settings.umi_file_selection)
	
	@property
	def bool_action(self):
		return True if self.action == "SELECT" else False
	
	def invoke(self, context, event):
		self.umi_settings = context.scene.umi_settings
		return self.execute(context)

	def execute(self, context):
		_, file_selection, _ = get_file_selection(context)
		
		self.umi_settings.umi_file_stat_update = False

		if self.mode == "ALL":
			for f in file_selection:
				f.check = self.bool_action
		elif self.mode == "EXTENSION":
			for f in file_selection:
				if os.path.splitext(f.name)[1].lower() == self.umi_settings.umi_file_extension_selection:
					f.check = self.bool_action
		elif self.mode == "SIZE":
			for f in file_selection:
				if f.size > self.umi_settings.umi_file_size_min_selection and f.size < self.umi_settings.umi_file_size_max_selection:
					f.check = self.bool_action
		elif self.mode == "NAME":
			for f in file_selection:
				name = os.path.splitext(f.name)[0]
				ref = self.umi_settings.umi_file_name_selection

				if not self.umi_settings.umi_file_name_include_folder_selection:
					name = os.path.basename(name)

				if not self.umi_settings.umi_file_name_case_sensitive_selection:
					name = name.lower()
					ref = ref.lower()
					
				if ref in name:
					f.check = self.bool_action

		self.umi_settings.umi_file_stat_update = True
		update_file_stats(self, context)
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