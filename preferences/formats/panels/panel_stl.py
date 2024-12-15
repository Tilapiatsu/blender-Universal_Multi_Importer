from . import draw_panel, draw_version_warning, BVERSION

class IMPORT_SCENE_STLSettings():
    @draw_version_warning
    def draw(self, operator, module_name, layout):
        layout.use_property_split = True
        layout.use_property_decorate = False  # No animation.

        if BVERSION >= 3.1:
            if module_name == 'default':
                op = [[operator, 'global_scale'],
                    [operator, 'use_scene_unit'],
                    [operator, 'forward_axis'],
                    [operator, 'up_axis']]

                draw_panel(layout, op, 'STLSettings_General', 'General', icon='OBJECT_DATA')

                op = [[operator, 'use_facet_normal'],
                    [operator, 'use_mesh_validate']]

                draw_panel(layout, op, 'STLSettings_Options', 'Options', icon='OPTIONS')


            if module_name == 'legacy':
                op = [[operator, 'global_scale'],
                    [operator, 'use_scene_unit'],
                    [operator, 'use_facet_normal'],
                    [operator, 'axis_forward'],
                    [operator, 'axis_up']]

                draw_panel(layout, op, 'STLSettings_Options', 'Options', icon='OPTIONS')
        else:
            op = [[operator, 'global_scale'],
                    [operator, 'use_scene_unit'],
                    [operator, 'use_facet_normal'],
                    [operator, 'axis_forward'],
                    [operator, 'axis_up']]

            draw_panel(layout, op, 'STLSettings_Options', 'Options', icon='OPTIONS')


