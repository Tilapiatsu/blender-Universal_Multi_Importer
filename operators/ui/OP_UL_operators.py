import bpy
import os
import math
from ...umi_const import get_umi_settings, get_batcher_list_name, get_batcher_index_name, OPERTAOR_LIST, get_operator_boolean, DATATYPE_PREFIX
from .operators_const import COMMAND_BATCHER_PRESET_FOLDER
from ...datatype import DATATYPE_LIST

# TODO : Copy Paste Attribute Injection to clipboard

col_count = math.ceil(len(DATATYPE_LIST)/3)

def operators(self, context, edit_text):
    return OPERTAOR_LIST

def draw_applies_to(self, layout):
    layout.label(text='Applies to :')
    row = layout.row(align=True)
    # col = row.column(align=True)
    for i, d in enumerate(DATATYPE_LIST):
        if i%col_count == 0:
            col = row.column(align=True)

        col.prop(self, f'{DATATYPE_PREFIX}_{d}')

def read_applies_to(self, current_operator):
    for d in DATATYPE_LIST:
        exec(f'self.{DATATYPE_PREFIX}_{d} = current_operator.{DATATYPE_PREFIX}_{d}', {'self': self, 'current_operator': current_operator})


def set_applies_to(self, current_operator):
    for d in DATATYPE_LIST:
        exec(f'current_operator.{DATATYPE_PREFIX}_{d} = self.{DATATYPE_PREFIX}_{d}', {'self': self, 'current_operator': current_operator})


if not os.path.exists(COMMAND_BATCHER_PRESET_FOLDER):
    print(f'UMI : Creating Preset Folder : {COMMAND_BATCHER_PRESET_FOLDER}')
    os.makedirs(COMMAND_BATCHER_PRESET_FOLDER, exist_ok=True)

def get_operator(target_name, target_id_name):
    umi_settings = get_umi_settings()
    target = eval(f'umi_settings.{target_name}')
    idx = eval(f'umi_settings.{target_id_name}')
    operators = target

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
        return eval(f'umi_settings.{get_batcher_list_name()}')

    def execute(self, context):
        umi_settings = get_umi_settings()

        idx, operator, _ = get_operator(eval(f'umi_settings.{get_batcher_list_name()}'), eval(f'umi_settings.{get_batcher_index_name()}'))

        nextidx = 0

        if self.direction == "UP":
            nextidx = max(idx - 1, 0)
        elif self.direction == "DOWN":
            nextidx = min(idx + 1, len(operator) - 1)

        operator.move(idx, nextidx)
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
        return eval(f'umi_settings.{get_batcher_list_name()}')

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_confirm(self, event)

    def execute(self, context):
        self.umi_settings = get_umi_settings()
        target = eval(f'self.umi_settings.{get_batcher_list_name()}')
        target.clear()

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
        return eval(f'umi_settings.{get_batcher_list_name()}')

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_confirm(self, event)

    def execute(self, context):
        umi_settings = get_umi_settings()

        self.umi_settings = get_umi_settings()
        target = eval(f'self.umi_settings.{get_batcher_list_name()}')

        target.remove(self.id)

        umi_settings.umi_operator_idx = min(self.id, len(target) - 1)

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
        return eval(f'umi_settings.{get_batcher_list_name()}')

    def execute(self, context):
        self.umi_settings = get_umi_settings()
        target = eval(f'self.umi_settings.{get_batcher_list_name()}')
        o = target.add()
        o.enabled = target[self.id].enabled
        o.operator = target[self.id].operator
        target.move(len(target) - 1, self.id + 1)

        return {'FINISHED'}


class UI_UMIEditOperator(bpy.types.Operator):
    bl_idname = "scene.umi_edit_operator"
    bl_label = "Edit Operator"
    bl_options = {'REGISTER', 'UNDO'}
    bl_description = "Edit current operator"

    id :                            bpy.props.IntProperty(name="Operator ID", default=0)
    operator :                      bpy.props.StringProperty(name="Operator Command", default="", search=operators )

    def draw(self, context):
        layout = self.layout
        col = layout.column()
        col.prop(self, 'operator', text='Command')
        draw_applies_to(self, col)

    def invoke(self, context, event):
        self.umi_settings = get_umi_settings()

        target = eval(f'self.umi_settings.{get_batcher_list_name()}')

        current_operator = target[self.id]

        self.operator = current_operator.operator

        read_applies_to(self, current_operator)

        wm = context.window_manager
        return wm.invoke_props_dialog(self, width=self.umi_settings.umi_window_width)

    def execute(self, context):
        self.umi_settings = get_umi_settings()
        target = eval(f'self.umi_settings.{get_batcher_list_name()}')
        o = target[self.id]
        o.operator = self.operator
        set_applies_to(self, o)
        return {'FINISHED'}


class UI_UMIAddOperator(bpy.types.Operator):
    bl_idname = "scene.umi_add_operator"
    bl_label = "Add Operator"
    bl_options = {'REGISTER', 'UNDO'}
    bl_description = "Add a new operator"

    operator :                      bpy.props.StringProperty(name="Operator Command", default="", search=operators )

    def draw(self, context):
        layout = self.layout
        col = layout.column()
        col.prop(self, 'operator', text='Command')
        draw_applies_to(self, col)

    def invoke(self, context, event):
        self.umi_settings = get_umi_settings()
        wm = context.window_manager
        return wm.invoke_props_dialog(self, width=self.umi_settings.umi_window_width)

    def execute(self, context):
        self.umi_settings = get_umi_settings()
        target = eval(f'self.umi_settings.{get_batcher_list_name()}')
        o = target.add()
        o.operator = self.operator
        set_applies_to(self, o)
        return {'FINISHED'}


classes = ( UI_UMIMoveOperator,
            UI_UMIClearOperators,
            UI_UMIRemoveOperator,
            UI_UMIDuplicateOperator)

datatype_classes = ({'class':UI_UMIEditOperator, 'prefix': DATATYPE_PREFIX},
                    {'class':UI_UMIAddOperator, 'prefix': DATATYPE_PREFIX})

def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)

    from ... import datatype
    datatype.register(datatype_classes)


def unregister():
    from ... import datatype
    datatype.unregister(datatype_classes)

    from bpy.utils import unregister_class

    for cls in reversed(classes):
        unregister_class(cls)

if __name__ == "__main__":
    register()