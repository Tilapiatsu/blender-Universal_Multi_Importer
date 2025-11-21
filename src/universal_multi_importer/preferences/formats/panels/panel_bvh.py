from universal_multi_importer.ui.panel import draw_panel, draw_version_warning

class IMPORT_SCENE_BVHSettings():
    @draw_version_warning
    def draw(self, operator, module_name, layout):
        layout.use_property_split = True
        layout.use_property_decorate = False

        layout.prop(operator, 'target')

        op = [[operator, 'global_scale'],
              [operator, 'rotate_mode'],
              [operator, 'axis_forward'],
              [operator, 'axis_up']]

        draw_panel(layout, op, 'BVHSettings_Transform', 'Transform', icon='OBJECT_DATA')

        op = [[operator, 'frame_start'],
              [operator, 'use_fps_scale'],
              [operator, 'use_cyclic'],
              [operator, 'update_scene_fps'],
              [operator, 'update_scene_duration']]

        draw_panel(layout, op, 'BVHSettings_Animation', 'Animation', icon='ARMATURE_DATA')