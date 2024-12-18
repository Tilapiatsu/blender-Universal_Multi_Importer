from . import draw_panel, draw_version_warning, draw_no_settings, BVERSION

class IMPORT_SCENE_PLYSettings():
    @draw_version_warning
    def draw(self, operator, module_name, layout):
        layout.use_property_split = True
        layout.use_property_decorate = False  # No animation.

        if BVERSION >= 3.4:
            op =    [[operator, 'global_scale'],
                    [operator, 'use_scene_unit'],
                    [operator, 'forward_axis'],
                    [operator, 'up_axis']]

            draw_panel(layout, op, 'PLYSettings_General', 'General', icon='OBJECT_DATA')

            op =    [[operator, 'merge_verts'],
                    [operator, 'import_colors']]

            draw_panel(layout, op, 'PLYSettings_Options', 'Options', icon='OPTIONS')
        else:
            draw_no_settings(layout)
