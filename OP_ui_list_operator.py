import bpy

def get_operator(context):
    idx = context.scene.umi_settings.umi_operator_idx
    operators = context.scene.umi_settings.umi_operators

    active = operators[idx] if operators else None

    return idx, operators, active


class LM_UI_MoveOperator(bpy.types.Operator):
    bl_idname = "scene.lm_move_operator"
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
    bl_idname = "scene.lm_clear_operators"
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
    bl_idname = "scene.lm_remove_operator"
    bl_label = "Remove Selected Operator"
    bl_options = {'REGISTER', 'UNDO'}
    bl_description = "Remove selected Operator."

    @classmethod
    def poll(cls, context):
        return context.scene.umi_settings.umi_operators

    def execute(self, context):
        idx, operator, _ = get_operator(context)

        operator.remove(idx)

        context.scene.umi_settings.umi_operator_idx = min(idx, len(context.scene.umi_settings.umi_operators) - 1)

        return {'FINISHED'}

class LM_UI_EditOperator(bpy.types.Operator):
    bl_idname = "scene.lm_edit_operator"
    bl_label = "Edit Operator"
    bl_options = {'REGISTER', 'UNDO'}
    bl_description = "Edit current operator"

    @classmethod
    def poll(cls, context):
        return context.scene.umi_settings.umi_operators

    def execute(self, context):
        context.scene.umi_umi_settings.umi_operators.clear()

        return {'FINISHED'}