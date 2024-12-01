from . import draw_panel, draw_version_warning

class IMPORT_SCENE_OBJSettings():
    @draw_version_warning
    def draw(self, operator, module_name, layout):
        layout.use_property_split = True
        layout.use_property_decorate = False  # No animation.

        op =    [[operator, 'global_scale'],
                 [operator, 'clamp_size'],
                 [operator, 'forward_axis'],
                 [operator, 'up_axis']]

        draw_panel(layout, op, 'OBJSettings_Transform', 'Transform', icon='OBJECT_DATA')


        op =    [[operator, 'use_split_objects'],
                [operator, 'use_split_groups'],
                [operator, 'import_vertex_groups'],
                [operator, 'validate_meshes'],
                [operator, 'collection_separator']]

        draw_panel(layout, op, 'OBJSettings_Options', 'Options', icon='OPTIONS')