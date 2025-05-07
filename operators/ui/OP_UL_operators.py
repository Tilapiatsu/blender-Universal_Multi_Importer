import bpy
import os
from ...umi_const import get_umi_settings, get_batcher_list_name, get_batcher_index_name, OPERTAOR_LIST, get_operator_boolean
from .operators_const import COMMAND_BATCHER_PRESET_FOLDER

def operators(self, context, edit_text):
    return OPERTAOR_LIST

def draw_applies_to(self, layout):
    layout.label(text='Applies to :')
    row = layout.row(align=True)
    col = row.column(align=True)
    col.prop(self, 'applies_to_actions')
    col.prop(self, 'applies_to_armatures')
    col.prop(self, 'applies_to_brushes')
    col.prop(self, 'applies_to_cache_files')
    col.prop(self, 'applies_to_cameras')
    col.prop(self, 'applies_to_collections')
    col.prop(self, 'applies_to_curves')
    col.prop(self, 'applies_to_fonts')
    col.prop(self, 'applies_to_grease_pencils')
    col.prop(self, 'applies_to_grease_pencils_v3')

    col = row.column(align=True)
    col.prop(self, 'applies_to_hair_curves')
    col.prop(self, 'applies_to_images')
    col.prop(self, 'applies_to_lattices')
    col.prop(self, 'applies_to_libraries')
    col.prop(self, 'applies_to_lightprobes')
    col.prop(self, 'applies_to_lights')
    col.prop(self, 'applies_to_linestyles')
    col.prop(self, 'applies_to_masks')
    col.prop(self, 'applies_to_materials')
    col.prop(self, 'applies_to_meshes')

    col = row.column(align=True)
    col.prop(self, 'applies_to_metaballs')
    col.prop(self, 'applies_to_movieclips')
    col.prop(self, 'applies_to_node_groups')
    col.prop(self, 'applies_to_objects')
    col.prop(self, 'applies_to_paint_curves')
    col.prop(self, 'applies_to_palettes')
    col.prop(self, 'applies_to_particles')
    col.prop(self, 'applies_to_pointclouds')
    col.prop(self, 'applies_to_scenes')
    col.prop(self, 'applies_to_screens')

    col = row.column(align=True)
    col.prop(self, 'applies_to_shape_keys')
    col.prop(self, 'applies_to_sounds')
    col.prop(self, 'applies_to_speakers')
    col.prop(self, 'applies_to_texts')
    col.prop(self, 'applies_to_textures')
    col.prop(self, 'applies_to_volumes')
    col.prop(self, 'applies_to_window_managers')
    col.prop(self, 'applies_to_workspaces')
    col.prop(self, 'applies_to_worlds')


def read_applies_to(self, current_operator):
    self.applies_to_actions             = current_operator.applies_to_actions
    self.applies_to_armatures           = current_operator.applies_to_armatures
    self.applies_to_brushes             = current_operator.applies_to_brushes
    self.applies_to_cache_files         = current_operator.applies_to_cache_files
    self.applies_to_cameras             = current_operator.applies_to_cameras
    self.applies_to_collections         = current_operator.applies_to_collections
    self.applies_to_curves              = current_operator.applies_to_curves
    self.applies_to_fonts               = current_operator.applies_to_fonts
    self.applies_to_grease_pencils      = current_operator.applies_to_grease_pencils
    self.applies_to_grease_pencils_v3   = current_operator.applies_to_grease_pencils_v3
    self.applies_to_hair_curves         = current_operator.applies_to_hair_curves
    self.applies_to_images              = current_operator.applies_to_images
    self.applies_to_lattices            = current_operator.applies_to_lattices
    self.applies_to_libraries           = current_operator.applies_to_libraries
    self.applies_to_lightprobes         = current_operator.applies_to_lightprobes
    self.applies_to_lights              = current_operator.applies_to_lights
    self.applies_to_linestyles          = current_operator.applies_to_linestyles
    self.applies_to_masks               = current_operator.applies_to_masks
    self.applies_to_materials           = current_operator.applies_to_materials
    self.applies_to_meshes              = current_operator.applies_to_meshes
    self.applies_to_metaballs           = current_operator.applies_to_metaballs
    self.applies_to_movieclips          = current_operator.applies_to_movieclips
    self.applies_to_node_groups         = current_operator.applies_to_node_groups
    self.applies_to_objects             = current_operator.applies_to_objects
    self.applies_to_paint_curves        = current_operator.applies_to_paint_curves
    self.applies_to_palettes            = current_operator.applies_to_palettes
    self.applies_to_particles           = current_operator.applies_to_particles
    self.applies_to_pointclouds         = current_operator.applies_to_pointclouds
    self.applies_to_scenes              = current_operator.applies_to_scenes
    self.applies_to_screens             = current_operator.applies_to_screens
    self.applies_to_shape_keys          = current_operator.applies_to_shape_keys
    self.applies_to_sounds              = current_operator.applies_to_sounds
    self.applies_to_speakers            = current_operator.applies_to_speakers
    self.applies_to_texts               = current_operator.applies_to_texts
    self.applies_to_textures            = current_operator.applies_to_textures
    self.applies_to_volumes             = current_operator.applies_to_volumes
    self.applies_to_window_managers     = current_operator.applies_to_window_managers
    self.applies_to_workspaces          = current_operator.applies_to_workspaces
    self.applies_to_worlds              = current_operator.applies_to_worlds


def set_applies_to(self, current_operator):
    current_operator.applies_to_actions             = self.applies_to_actions
    current_operator.applies_to_armatures           = self.applies_to_armatures
    current_operator.applies_to_brushes             = self.applies_to_brushes
    current_operator.applies_to_cache_files         = self.applies_to_cache_files
    current_operator.applies_to_cameras             = self.applies_to_cameras
    current_operator.applies_to_collections         = self.applies_to_collections
    current_operator.applies_to_curves              = self.applies_to_curves
    current_operator.applies_to_fonts               = self.applies_to_fonts
    current_operator.applies_to_grease_pencils      = self.applies_to_grease_pencils
    current_operator.applies_to_grease_pencils_v3   = self.applies_to_grease_pencils_v3
    current_operator.applies_to_hair_curves         = self.applies_to_hair_curves
    current_operator.applies_to_images              = self.applies_to_images
    current_operator.applies_to_lattices            = self.applies_to_lattices
    current_operator.applies_to_libraries           = self.applies_to_libraries
    current_operator.applies_to_lightprobes         = self.applies_to_lightprobes
    current_operator.applies_to_lights              = self.applies_to_lights
    current_operator.applies_to_linestyles          = self.applies_to_linestyles
    current_operator.applies_to_masks               = self.applies_to_masks
    current_operator.applies_to_materials           = self.applies_to_materials
    current_operator.applies_to_meshes              = self.applies_to_meshes
    current_operator.applies_to_metaballs           = self.applies_to_metaballs
    current_operator.applies_to_movieclips          = self.applies_to_movieclips
    current_operator.applies_to_node_groups         = self.applies_to_node_groups
    current_operator.applies_to_objects             = self.applies_to_objects
    current_operator.applies_to_paint_curves        = self.applies_to_paint_curves
    current_operator.applies_to_palettes            = self.applies_to_palettes
    current_operator.applies_to_particles           = self.applies_to_particles
    current_operator.applies_to_pointclouds         = self.applies_to_pointclouds
    current_operator.applies_to_scenes              = self.applies_to_scenes
    current_operator.applies_to_screens             = self.applies_to_screens
    current_operator.applies_to_shape_keys          = self.applies_to_shape_keys
    current_operator.applies_to_sounds              = self.applies_to_sounds
    current_operator.applies_to_speakers            = self.applies_to_speakers
    current_operator.applies_to_texts               = self.applies_to_texts
    current_operator.applies_to_textures            = self.applies_to_textures
    current_operator.applies_to_volumes             = self.applies_to_volumes
    current_operator.applies_to_window_managers     = self.applies_to_window_managers
    current_operator.applies_to_workspaces          = self.applies_to_workspaces
    current_operator.applies_to_worlds              = self.applies_to_worlds


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

    applies_to_actions:             bpy.props.BoolProperty(name='Actions')
    applies_to_armatures:           bpy.props.BoolProperty(name='Armatures')
    applies_to_brushes:             bpy.props.BoolProperty(name='Brushes')
    applies_to_cache_files:         bpy.props.BoolProperty(name='Cache Files')
    applies_to_cameras:             bpy.props.BoolProperty(name='Cameras')
    applies_to_collections:         bpy.props.BoolProperty(name='Collections')
    applies_to_curves:              bpy.props.BoolProperty(name='Curves')
    applies_to_fonts:               bpy.props.BoolProperty(name='Fonts')
    applies_to_grease_pencils:      bpy.props.BoolProperty(name='Grease Pencils')
    applies_to_grease_pencils_v3:   bpy.props.BoolProperty(name='Grease Pencils v3')
    applies_to_hair_curves:         bpy.props.BoolProperty(name='Hair Curves')
    applies_to_images:              bpy.props.BoolProperty(name='Images')
    applies_to_lattices:            bpy.props.BoolProperty(name='Lattices')
    applies_to_libraries:           bpy.props.BoolProperty(name='Libraries')
    applies_to_lightprobes:         bpy.props.BoolProperty(name='Lightprobes')
    applies_to_lights:              bpy.props.BoolProperty(name='Lights')
    applies_to_linestyles:          bpy.props.BoolProperty(name='Linestyles')
    applies_to_masks:               bpy.props.BoolProperty(name='Masks')
    applies_to_materials:           bpy.props.BoolProperty(name='Materials')
    applies_to_meshes:              bpy.props.BoolProperty(name='Meshes')
    applies_to_metaballs:           bpy.props.BoolProperty(name='Metaballs')
    applies_to_movieclips:          bpy.props.BoolProperty(name='Movieclips')
    applies_to_node_groups:         bpy.props.BoolProperty(name='Node Groups')
    applies_to_objects:             bpy.props.BoolProperty(name='Objects')
    applies_to_paint_curves:        bpy.props.BoolProperty(name='Paint Curves')
    applies_to_palettes:            bpy.props.BoolProperty(name='Palettes')
    applies_to_particles:           bpy.props.BoolProperty(name='Particles')
    applies_to_pointclouds:         bpy.props.BoolProperty(name='Pointclouds')
    applies_to_scenes:              bpy.props.BoolProperty(name='Scenes')
    applies_to_screens:             bpy.props.BoolProperty(name='Screens')
    applies_to_shape_keys:          bpy.props.BoolProperty(name='Shape keys')
    applies_to_sounds:              bpy.props.BoolProperty(name='Sounds')
    applies_to_speakers:            bpy.props.BoolProperty(name='Speakers')
    applies_to_texts:               bpy.props.BoolProperty(name='Texts')
    applies_to_textures:            bpy.props.BoolProperty(name='Textures')
    applies_to_volumes:             bpy.props.BoolProperty(name='Volumes')
    applies_to_window_managers:     bpy.props.BoolProperty(name='Window managers')
    applies_to_workspaces:          bpy.props.BoolProperty(name='Workspaces')
    applies_to_worlds:              bpy.props.BoolProperty(name='Worlds')

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

    applies_to_actions:             bpy.props.BoolProperty(name='Actions')
    applies_to_armatures:           bpy.props.BoolProperty(name='Armatures')
    applies_to_brushes:             bpy.props.BoolProperty(name='Brushes')
    applies_to_cache_files:         bpy.props.BoolProperty(name='Cache Files')
    applies_to_cameras:             bpy.props.BoolProperty(name='Cameras')
    applies_to_collections:         bpy.props.BoolProperty(name='Collections')
    applies_to_curves:              bpy.props.BoolProperty(name='Curves')
    applies_to_fonts:               bpy.props.BoolProperty(name='Fonts')
    applies_to_grease_pencils:      bpy.props.BoolProperty(name='Grease Pencils')
    applies_to_grease_pencils_v3:   bpy.props.BoolProperty(name='Grease Pencils v3')
    applies_to_hair_curves:         bpy.props.BoolProperty(name='Hair Curves')
    applies_to_images:              bpy.props.BoolProperty(name='Images')
    applies_to_lattices:            bpy.props.BoolProperty(name='Lattices')
    applies_to_libraries:           bpy.props.BoolProperty(name='Libraries')
    applies_to_lightprobes:         bpy.props.BoolProperty(name='Lightprobes')
    applies_to_lights:              bpy.props.BoolProperty(name='Lights')
    applies_to_linestyles:          bpy.props.BoolProperty(name='Linestyles')
    applies_to_masks:               bpy.props.BoolProperty(name='Masks')
    applies_to_materials:           bpy.props.BoolProperty(name='Materials')
    applies_to_meshes:              bpy.props.BoolProperty(name='Meshes')
    applies_to_metaballs:           bpy.props.BoolProperty(name='Metaballs')
    applies_to_movieclips:          bpy.props.BoolProperty(name='Movieclips')
    applies_to_node_groups:         bpy.props.BoolProperty(name='Node Groups')
    applies_to_objects:             bpy.props.BoolProperty(name='Objects', default=True)
    applies_to_paint_curves:        bpy.props.BoolProperty(name='Paint Curves')
    applies_to_palettes:            bpy.props.BoolProperty(name='Palettes')
    applies_to_particles:           bpy.props.BoolProperty(name='Particles')
    applies_to_pointclouds:         bpy.props.BoolProperty(name='Pointclouds')
    applies_to_scenes:              bpy.props.BoolProperty(name='Scenes')
    applies_to_screens:             bpy.props.BoolProperty(name='Screens')
    applies_to_shape_keys:          bpy.props.BoolProperty(name='Shape keys')
    applies_to_sounds:              bpy.props.BoolProperty(name='Sounds')
    applies_to_speakers:            bpy.props.BoolProperty(name='Speakers')
    applies_to_texts:               bpy.props.BoolProperty(name='Texts')
    applies_to_textures:            bpy.props.BoolProperty(name='Textures')
    applies_to_volumes:             bpy.props.BoolProperty(name='Volumes')
    applies_to_window_managers:     bpy.props.BoolProperty(name='Window managers')
    applies_to_workspaces:          bpy.props.BoolProperty(name='Workspaces')
    applies_to_worlds:              bpy.props.BoolProperty(name='Worlds')

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