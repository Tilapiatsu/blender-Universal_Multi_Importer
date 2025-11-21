import bpy
import os, shutil
from universal_multi_importer.umi_const import get_umi_settings, get_batcher_list_name, DATATYPE_PREFIX, DATATYPE_LIST
from universal_multi_importer.operators.ui.operators_const import COMMAND_BATCHER_PRESET_FOLDER, UMIPRESET_EXTENSION, UMIPRESET_SPLITTER


def get_presets(context):
    umi_settings = get_umi_settings()
    idx = umi_settings.umi_preset_idx
    presets = umi_settings.umi_presets

    active = presets[idx] if presets else None

    return idx, presets, active


class UI_MovePreset(bpy.types.Operator):
    bl_idname = "scene.umi_move_preset"
    bl_label = "Move Preset"
    bl_options = {'REGISTER', 'UNDO'}
    bl_description = "Move Preset up or down.\nThis controls the position in the Menu."

    direction: bpy.props.EnumProperty(items=[("UP", "Up", ""), ("DOWN", "Down", "")])

    @classmethod
    def poll(cls, context):
        umi_settings = get_umi_settings()
        return len(umi_settings.umi_presets)

    def execute(self, context):
        umi_settings = get_umi_settings()
        idx, preset, _ = get_presets(context)

        if self.direction == "UP":
            nextidx = max(idx - 1, 0)
        elif self.direction == "DOWN":
            nextidx = min(idx + 1, len(preset) - 1)

        preset.move(idx, nextidx)
        umi_settings.umi_preset_idx = nextidx

        return {'FINISHED'}


class UI_ClearPresets(bpy.types.Operator):
    bl_idname = "scene.umi_clear_presets"
    bl_label = "Clear All Presets"
    bl_options = {'REGISTER', 'UNDO'}
    bl_description = "Clear All Presets."

    @classmethod
    def poll(cls, context):
        umi_settings = get_umi_settings()
        return len(umi_settings.umi_presets)

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_confirm(self, event)

    def execute(self, context):
        umi_settings = get_umi_settings()
        umi_settings.umi_presets.clear()

        return {'FINISHED'}


class UI_RemovePreset(bpy.types.Operator):
    bl_idname = "scene.umi_remove_preset"
    bl_label = "Remove Selected Preset"
    bl_options = {'REGISTER', 'UNDO'}
    bl_description = "Remove Selected Preset PERMANENTLY ?"

    id : bpy.props.IntProperty(name="Preset ID", default=0)

    @classmethod
    def poll(cls, context):
        umi_settings = get_umi_settings()
        return len(umi_settings.umi_presets)

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_confirm(self, event)


    def execute(self, context):
        umi_settings = get_umi_settings()
        _, self.presets, self.item = get_presets(context)
        if os.path.isfile(self.presets[self.id].path):
            os.remove(self.presets[self.id].path)

        self.presets.remove(self.id)

        umi_settings.umi_preset_idx = min(self.id, len(umi_settings.umi_presets) - 1)

        return {'FINISHED'}


class UI_DuplicatePreset(bpy.types.Operator):
    bl_idname = "scene.umi_duplicate_preset"
    bl_label = "Duplicate Selected Preset"
    bl_options = {'REGISTER', 'UNDO'}
    bl_description = "Duplicate selected Preset."

    id : bpy.props.IntProperty(name="Preset ID", default=0)

    def get_unique_name(self, name, name_list, separator='_', is_path=False):
        def name_exists(name_list_splited, suffix):
            exists = False
            for n in name_list_splited:
                if basename == n[0] and new_suffix == n[1][1:3]:
                    suffix = separator +  new_suffix
                    exists = True
                    break
            else:
                suffix = separator +  new_suffix
            return exists, suffix

        if is_path:
            extension_size = len(UMIPRESET_EXTENSION)
        else:
            extension_size = 0

        basename = name[0:-3-extension_size]
        suffix = name[-3-extension_size:]
        name_list_basenames = [n[0:-3-extension_size] for n in name_list]
        name_list_suffixes = [n[-3-extension_size:] for n in name_list]
        name_list_splited = list(zip(name_list_basenames, name_list_suffixes))
        same_name_found = True

        while(same_name_found):
            if suffix[0] == separator and suffix[1:3].isnumeric():
                new_suffix = int(suffix[2:3]) + 1
                new_suffix = f'{new_suffix:02}'

                exist, suffix = name_exists(name_list_splited, suffix)

                if exist:
                    continue

                if is_path:
                    new_name = name[0:-3-extension_size] + separator + new_suffix + UMIPRESET_EXTENSION
                else:
                    new_name = basename + separator + new_suffix
                same_name_found = False

            elif is_path:
                basename = name
                new_suffix = '01'
                exist, _ = name_exists(name_list_splited, new_suffix)
                if exist:
                    suffix = '_02'
                    continue

                new_name = name[0:-extension_size] + separator + new_suffix + UMIPRESET_EXTENSION
            else:
                basename = name
                new_suffix = '01'
                exist, _ = name_exists(name_list_splited, new_suffix)
                if exist:
                    suffix = '_02'
                    continue

                new_name = name + separator + new_suffix
            same_name_found = False

        return new_name

    @classmethod
    def poll(cls, context):
        umi_settings = get_umi_settings()
        return len(umi_settings.umi_presets)

    def execute(self, context):
        _, presets, _ = get_presets(context)

        name_list = [p.name for p in presets]
        path_list = [p.path for p in presets]

        o = presets.add()
        o.name = self.get_unique_name(presets[self.id].name, name_list=name_list)
        o.path = self.get_unique_name(presets[self.id].path, name_list=path_list, is_path=True)

        shutil.copy(presets[self.id].path, o.path)
        presets.move(len(presets) - 1, self.id + 1)

        return {'FINISHED'}


class UI_EditPreset(bpy.types.Operator):
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
        umi_settings = get_umi_settings()
        current_preset = umi_settings.umi_presets[self.id]
        self.name = current_preset.name
        wm = context.window_manager
        return wm.invoke_props_dialog(self, width=900)

    def execute(self, context):
        umi_settings = get_umi_settings()
        o = umi_settings.umi_presets[self.id]
        o.name = self.name
        old_name = o.path
        o.path = os.path.join(COMMAND_BATCHER_PRESET_FOLDER, self.name + UMIPRESET_EXTENSION)

        os.rename(old_name, o.path)
        return {'FINISHED'}


class UI_AddPreset(bpy.types.Operator):
    bl_idname = "scene.umi_add_preset"
    bl_label = "Add Preset"
    bl_options = {'REGISTER', 'UNDO'}
    bl_description = "Add a new operator"

    name : bpy.props.StringProperty(name="Preset name", default="")
    from_list : bpy.props.BoolProperty(name="From List", default=True)
    target : bpy.props.StringProperty(name="Target List Name", default="")

    def draw(self, context):
        layout = self.layout
        col = layout.column()
        col.prop(self, 'name', text='Preset Name')

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self, width=500)

    def execute(self, context):
        umi_settings = get_umi_settings()

        if self.name not in umi_settings.umi_presets:
            o = umi_settings.umi_presets.add()
        else:
            o = umi_settings.umi_presets[self.name]

        o.name = self.name
        o.path = os.path.join(COMMAND_BATCHER_PRESET_FOLDER, self.name + UMIPRESET_EXTENSION)
        if self.from_list:
            bpy.ops.scene.umi_save_preset_operator(filepath=o.path)
        return {'FINISHED'}


class UI_SavePresetOperator(bpy.types.Operator):
    bl_idname = "scene.umi_save_preset_operator"
    bl_label = "Save Preset"
    bl_options = {'REGISTER', 'UNDO'}
    bl_description = "Save a preset of the current operator list to a preset file on your disk"

    filepath: bpy.props.StringProperty(name='Filepath', default='', subtype="FILE_PATH")

    def invoke(self, context, event):
        if os.path.exists(self.filepath):
            wm = context.window_manager
            return wm.invoke_confirm(self, event)

        self.execute(context)

    def execute(self, context):
        print(f'Saving preset : {os.path.basename(self.filepath)}')
        self.umi_settings = get_umi_settings()
        with open(self.filepath, 'w') as f:
            lines = []
            operators = eval(f'self.umi_settings.{get_batcher_list_name()}')
            for i,o in enumerate(operators):
                lines.append(o.operator.replace('\n', '') + f' {UMIPRESET_SPLITTER}')
                for d in DATATYPE_LIST:
                    lines[i] += f' --{DATATYPE_PREFIX}_{d["name"]}' if getattr(o, f'{DATATYPE_PREFIX}_{d["name"]}') else ''

                if getattr(o, f'{DATATYPE_PREFIX}_modifiers'):
                    lines[i] += f' --modifier_type={o.modifier_type}'

            f.writelines('%s\n' % l for l in lines)

        return {'FINISHED'}


class UI_LoadPresetOperator(bpy.types.Operator):
    bl_idname = "scene.umi_load_preset_operator"
    bl_label = "Load Preset"
    bl_options = {'REGISTER', 'UNDO'}
    bl_description = "Load a preset and add the commands at the end of the current list"

    filepath: bpy.props.StringProperty(name='Filepath', default='', subtype="FILE_PATH")
    target : bpy.props.StringProperty(name="Target List Name", default="")

    def execute(self, context):
        print(f'Loading preset : {os.path.basename(self.filepath)}')
        with open(self.filepath) as f:
            lines = [line for line in f]
            for l in lines:
                l = l.replace('\n', '')
                applies_to_dict = {f'{DATATYPE_PREFIX}_{a["name"]}':False for a in DATATYPE_LIST}
                applies_to_dict['modifier_type'] = 'ARRAY'

                if f' {UMIPRESET_SPLITTER}' in l:
                    op, applies_to = l.split(f' {UMIPRESET_SPLITTER}')
                else:
                    op = l
                    applies_to = ''

                if len(applies_to):
                    applies_to = applies_to.split(' --')[1:]

                    for a in applies_to:
                        if '=' in a:
                            key, value = a.split('=')
                            applies_to_dict[key] = value
                        else:
                            applies_to_dict[a] = True
                else:
                    applies_to_dict[f'{DATATYPE_PREFIX}_objects'] = True

                bpy.ops.scene.umi_add_operator(operator=op, **applies_to_dict)

        return {'FINISHED'}


class UI_LoadPresetList(bpy.types.Operator):
    bl_idname = "scene.umi_load_preset_list"
    bl_label = "Load Preset"
    bl_options = {'REGISTER', 'UNDO'}
    bl_description = "Load the list of all presets saved on disks"

    def execute(self, context):
        umi_settings = get_umi_settings()
        presets = [f for f in os.listdir(COMMAND_BATCHER_PRESET_FOLDER) if os.path.splitext(f)[1].lower() == UMIPRESET_EXTENSION]
        if len(umi_settings.umi_presets):
            bpy.ops.scene.umi_clear_presets('EXEC_DEFAULT')

        for p in presets:
            bpy.ops.scene.umi_add_preset('EXEC_DEFAULT', name=os.path.splitext(p)[0], from_list=False)

        return {'FINISHED'}

classes = ( UI_MovePreset,
            UI_ClearPresets,
            UI_RemovePreset,
            UI_DuplicatePreset,
            UI_EditPreset,
            UI_AddPreset,
            UI_SavePresetOperator,
            UI_LoadPresetOperator,
            UI_LoadPresetList)

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