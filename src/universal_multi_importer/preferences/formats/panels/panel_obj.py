from . import draw_panel, draw_version_warning, draw_prop, BVERSION, draw_import_as_geometry_node_settings

class IMPORT_SCENE_OBJSettings():
    @draw_version_warning
    def draw(self, operator, module_name, layout):
        layout.use_property_split = True
        layout.use_property_decorate = False  # No animation.

        if module_name == 'geometry_node':
            draw_import_as_geometry_node_settings(layout, operator, 'OBJGNSettings')

        if module_name == 'default':
            if BVERSION >=4.1:
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

            elif BVERSION >= 3.5:
                op =    [[operator, 'global_scale'],
                        [operator, 'clamp_size'],
                        [operator, 'forward_axis'],
                        [operator, 'up_axis']]

                draw_panel(layout, op, 'OBJSettings_Transform', 'Transform', icon='OBJECT_DATA')


                op =    [[operator, 'use_split_objects'],
                        [operator, 'use_split_groups'],
                        [operator, 'import_vertex_groups'],
                        [operator, 'validate_meshes']]

                draw_panel(layout, op, 'OBJSettings_Options', 'Options', icon='OPTIONS')

            elif BVERSION >= 3.4:
                op =    [[operator, 'global_scale'],
                        [operator, 'clamp_size'],
                        [operator, 'forward_axis'],
                        [operator, 'up_axis']]

                draw_panel(layout, op, 'OBJSettings_Transform', 'Transform', icon='OBJECT_DATA')


                op =    [[operator, 'import_vertex_groups'],
                        [operator, 'validate_meshes']]

                draw_panel(layout, op, 'OBJSettings_Options', 'Options', icon='OPTIONS')

            elif BVERSION >= 3.3:
                op =    [[operator, 'clamp_size'],
                        [operator, 'forward_axis'],
                        [operator, 'up_axis']]

                draw_panel(layout, op, 'OBJSettings_Transform', 'Transform', icon='OBJECT_DATA')


                op =    [[operator, 'import_vertex_groups'],
                        [operator, 'validate_meshes']]

                draw_panel(layout, op, 'OBJSettings_Options', 'Options', icon='OPTIONS')

            else:
                op =    [[operator, 'use_image_search'],
                        [operator, 'use_smooth_groups'],
                        [operator, 'use_edges']]

                draw_panel(layout, op, 'OBJSettings_Include', 'Include', icon='IMPORT')

                op =    [[operator, 'global_clamp_size'],
                        [operator, 'axis_forward'],
                        [operator, 'axis_up']]

                draw_panel(layout, op, 'OBJSettings_Transform', 'Transform', icon='OBJECT_DATA')


                op =    [[operator, 'split_mode']]

                _, panel = draw_panel(layout, op, 'OBJSettings_Options', 'Options', icon='OPTIONS', default_closed=True)

                if panel:
                    if operator.split_mode == 'ON':
                        draw_prop(panel, operator, 'use_split_objects')
                        draw_prop(panel, operator, 'use_split_groups')

                    elif operator.split_mode == 'OFF':
                        draw_prop(panel, operator, 'use_groups_as_vgroups')