import bpy
import os
import math
from ...umi_const import get_umi_settings, get_batcher_list_name, get_batcher_index_name, OPERTAOR_LIST, get_operator_boolean, DATATYPE_PREFIX, DATATYPE_PROPERTIES, DATATYPE_LIST
from .operators_const import COMMAND_BATCHER_PRESET_FOLDER
from ..command_batcher_const import COMMAND_BATCHER_INPUT_ITEMS, COMMAND_BATCHER_ITEM_COUNT, COMMAND_BATCHER_VARIABLE
from ...ui.panel import draw_panel
from ...bversion import BVERSION


datatype_col_count = math.ceil(len(DATATYPE_LIST)/4)
batcher_item_col_count = math.ceil(COMMAND_BATCHER_ITEM_COUNT/7)

def operators(self, context, edit_text):
    return OPERTAOR_LIST

def draw_applies_to(self, layout):
    layout.use_property_split = True
    layout.use_property_decorate = False

    if BVERSION >= 4.2:
        header, panel = layout.panel(idname='COMAND_AppliesTo')
        header.label(text='Applies to :', icon='OPTIONS')
    else:
        panel = layout.box()
        header = panel.row(align=True)
        header.label(text='Applies to :', icon='OPTIONS')

    if panel:
        row = panel.row()
        row.alignment = 'EXPAND'
        for i, d in enumerate(DATATYPE_PROPERTIES):
            if i % datatype_col_count == 0:
                col = row.column(align=True)
                col.alignment = 'RIGHT'
            row1 = col.row(align=True)
            row1.alignment = 'RIGHT'
            row1.label(text=d['name'])
            row1.label(text='', icon=d['icon'])
            row1.prop(self, f'{d["property"]}', text='')

        col3 = row.column(align=True)
        col3.alignment = 'RIGHT'
        col3.label(text='')

def read_applies_to(self, current_operator):
    for d in DATATYPE_PROPERTIES:
        exec(f'self.{d["property"]} = current_operator.{d["property"]}', {'self': self, 'current_operator': current_operator})

def set_applies_to(self, current_operator):
    for d in DATATYPE_PROPERTIES:
        exec(f'current_operator.{d["property"]} = self.{d["property"]}', {'self': self, 'current_operator': current_operator})

def draw_add_edit_operator(self, layout):
    col = layout.column()
    col.label(text='Command:')
    col.prop(self, 'operator', text='')
    col.separator()

    col.use_property_split = True
    col.use_property_decorate = False

    if BVERSION >= 4.2:
        header, panel = col.panel(idname='COMMAND_InjectVariable')
        header.label(text='Inject Variable :', icon='SORTALPHA')
    else:
        panel = col.box()
        header = panel.row(align=True)
        header.label(text='Inject Variable :', icon='SORTALPHA')

    if panel:
        row = panel.row()
        row.alignment = 'EXPAND'
        for i, c in enumerate(COMMAND_BATCHER_VARIABLE):
            if i % batcher_item_col_count == 0:
                sub_col = row.column(align=True)

            sub_col.prop(self, f'{c["property"]}', text='')

    draw_applies_to(self, col)

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

        idx, operator, _ = get_operator(get_batcher_list_name(), get_batcher_index_name())

        nextidx = 0

        if self.direction == "UP":
            nextidx = max(idx - 1, 0)
        elif self.direction == "DOWN":
            nextidx = min(idx + 1, len(operator) - 1)

        operator.move(idx, nextidx)
        exec(f"umi_settings.{get_batcher_index_name()} = nextidx")

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
        draw_add_edit_operator(self, self.layout)

    def invoke(self, context, event):
        self.umi_settings = get_umi_settings()

        target = eval(f'self.umi_settings.{get_batcher_list_name()}')

        current_operator = target[self.id]

        self.operator = current_operator.operator

        read_applies_to(self, current_operator)

        wm = context.window_manager
        return wm.invoke_props_dialog(self, width=int(self.umi_settings.umi_window_width * 0.8))

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

    operator : bpy.props.StringProperty(name="Operator Command", default="", search=operators )

    def draw(self, context):
        draw_add_edit_operator(self, self.layout)

    def invoke(self, context, event):
        self.umi_settings = get_umi_settings()
        wm = context.window_manager
        return wm.invoke_props_dialog(self, width=int(self.umi_settings.umi_window_width*0.8))

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

datatype_classes = (UI_UMIEditOperator,
                    UI_UMIAddOperator)

def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)

    from ... import class_property_injection
    class_property_injection.register(datatype_classes, DATATYPE_PROPERTIES + COMMAND_BATCHER_VARIABLE)


def unregister():
    from ... import class_property_injection
    class_property_injection.unregister(datatype_classes, DATATYPE_PROPERTIES + COMMAND_BATCHER_VARIABLE)

    from bpy.utils import unregister_class

    for cls in reversed(classes):
        unregister_class(cls)

if __name__ == "__main__":
    register()