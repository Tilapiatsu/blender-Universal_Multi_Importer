import bpy
import os
from .constant import PRESET_FOLDER

def get_presets(context):
	idx = context.scene.umi_settings.umi_preset_idx
	presets = context.scene.umi_settings.umi_presets

	active = presets[idx] if presets else None

	return idx, presets, active


class LM_UI_MovePreset(bpy.types.Operator):
	bl_idname = "scene.umi_move_preset"
	bl_label = "Move Preset"
	bl_options = {'REGISTER', 'UNDO'}
	bl_description = "Move Preset up or down.\nThis controls the position in the Menu."

	direction: bpy.props.EnumProperty(items=[("UP", "Up", ""), ("DOWN", "Down", "")])

	@classmethod
	def poll(cls, context):
		return len(context.scene.umi_settings.umi_presets)

	def execute(self, context):
		idx, preset, _ = get_presets(context)

		if self.direction == "UP":
			nextidx = max(idx - 1, 0)
		elif self.direction == "DOWN":
			nextidx = min(idx + 1, len(preset) - 1)

		preset.move(idx, nextidx)
		context.scene.umi_settings.umi_preset_idx = nextidx

		return {'FINISHED'}


class LM_UI_ClearPresets(bpy.types.Operator):
	bl_idname = "scene.umi_clear_presets"
	bl_label = "Clear All Presets"
	bl_options = {'REGISTER', 'UNDO'}
	bl_description = "Clear All Presets."

	@classmethod
	def poll(cls, context):
		return len(context.scene.umi_settings.umi_presets)

	def execute(self, context):
		context.scene.umi_settings.umi_presets.clear()

		return {'FINISHED'}


class LM_UI_RemovePreset(bpy.types.Operator):
	bl_idname = "scene.umi_remove_preset"
	bl_label = "Remove Selected Preset"
	bl_options = {'REGISTER', 'UNDO'}
	bl_description = "Remove Selected Preset PERMANENTLY ?"
	
	id : bpy.props.IntProperty(name="Preset ID", default=0)

	@classmethod
	def poll(cls, context):
		return len(context.scene.umi_settings.umi_presets)
	
	def invoke(self, context, event):
		wm = context.window_manager
		return wm.invoke_confirm(self, event)
		

	def execute(self, context):
		_, self.presets, self.item = get_presets(context)
		if os.path.isfile(self.item.path):
			os.remove(self.item.path)

		self.presets.remove(self.id)

		context.scene.umi_settings.umi_preset_idx = min(self.id, len(context.scene.umi_settings.umi_presets) - 1)

		return {'FINISHED'}


class LM_UI_DuplicatePreset(bpy.types.Operator):
	bl_idname = "scene.umi_duplicate_preset"
	bl_label = "Duplicate Selected Preset"
	bl_options = {'REGISTER', 'UNDO'}
	bl_description = "Duplicate selected Preset."
	
	id : bpy.props.IntProperty(name="Preset ID", default=0)

	@classmethod
	def poll(cls, context):
		return len(context.scene.umi_settings.umi_presets)

	def execute(self, context):
		_, presets, _ = get_presets(context)

		o = presets.add()
		o.name = presets[self.id].name
		o.path = presets[self.id].path
		presets.move(len(presets) - 1, self.id + 1)

		return {'FINISHED'}


class LM_UI_EditPreset(bpy.types.Operator):
	bl_idname = "scene.umi_edit_preset"
	bl_label = "Edit Operator"
	bl_options = {'REGISTER', 'UNDO'}
	bl_description = "Edit current preset"

	id : bpy.props.IntProperty(name="Operator ID", default=0)
	name : bpy.props.StringProperty(name="Preset Name", default="")

	def draw(self, context):
		layout = self.layout
		col = layout.column()
		col.prop(self, 'name', text='Preset Name')
	
	def invoke(self, context, event):
		current_preset = context.scene.umi_settings.umi_presets[self.id]
		self.name = current_preset.name
		wm = context.window_manager
		return wm.invoke_props_dialog(self, width=900)
	
	def execute(self, context):
		o = context.scene.umi_settings.umi_presets[self.id]
		o.name = self.name
		old_name = o.path
		o.path = os.path.join(PRESET_FOLDER, self.name + '.umipreset')

		os.rename(old_name, o.path)
		return {'FINISHED'}	


class LM_UI_AddPreset(bpy.types.Operator):
	bl_idname = "scene.umi_add_preset"
	bl_label = "Add Operator"
	bl_options = {'REGISTER', 'UNDO'}
	bl_description = "Add a new operator"

	name : bpy.props.StringProperty(name="Preset name", default="")
	from_list : bpy.props.BoolProperty(name="From List", default=True)

	def draw(self, context):
		layout = self.layout
		col = layout.column()
		col.prop(self, 'name', text='Preset Name')

	def invoke(self, context, event):
		wm = context.window_manager
		return wm.invoke_props_dialog(self, width=500)

	def execute(self, context):
		o = context.scene.umi_settings.umi_presets.add()
		o.name = self.name
		o.path = os.path.join(PRESET_FOLDER, self.name + '.umipreset')
		if self.from_list:
			bpy.ops.scene.umi_save_preset_operator(filepath=o.path)
		return {'FINISHED'}


class LM_UI_SavePresetOperator(bpy.types.Operator):
	bl_idname = "scene.umi_save_preset_operator"
	bl_label = "Save Preset"
	bl_options = {'REGISTER', 'UNDO'}
	bl_description = "Save a preset of the current operator list to a preset file on your disk"

	filepath: bpy.props.StringProperty(name='Filepath', default='', subtype="FILE_PATH") 


	def execute(self, context):
		print(f'Saving preset : {os.path.basename(self.filepath)}')
		self.umi_settings = context.scene.umi_settings
		with open(self.filepath, 'w') as f:
			lines = [l.operator.replace('\n', '') for l in self.umi_settings.umi_operators]

			f.writelines('%s\n' % l for l in lines)

		return {'FINISHED'}
	

class LM_UI_LoadPresetOperator(bpy.types.Operator):
	bl_idname = "scene.umi_load_preset_operator"
	bl_label = "Load Preset"
	bl_options = {'REGISTER', 'UNDO'}
	bl_description = "Load a preset and add the commands at the end of the current list"

	filepath: bpy.props.StringProperty(name='Filepath', default='', subtype="FILE_PATH") 

	def execute(self, context):
		print(f'Loading preset : {os.path.basename(self.filepath)}')
		with open(self.filepath) as f:
			lines = [line for line in f]
			for l in lines:
				bpy.ops.scene.umi_add_operator(operator=l)

		return {'FINISHED'}
	

class LM_UI_LoadPresetList(bpy.types.Operator):
	bl_idname = "scene.umi_load_preset_list"
	bl_label = "Load Preset"
	bl_options = {'REGISTER', 'UNDO'}
	bl_description = "Load the list of all presets saved on disks"

	def execute(self, context):
		presets = [f for f in os.listdir(PRESET_FOLDER) if os.path.splitext(f)[1].lower() == '.umipreset']
		if len(bpy.context.scene.umi_settings.umi_presets):
			bpy.ops.scene.umi_clear_presets('INVOKE_DEFAULT')

		for p in presets:
			bpy.ops.scene.umi_add_preset('EXEC_DEFAULT', name=os.path.splitext(p)[0], from_list=False)

		return {'FINISHED'}