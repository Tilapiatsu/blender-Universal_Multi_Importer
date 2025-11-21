from universal_multi_importer.bversion import BVERSION
from universal_multi_importer.preferences.formats.panels import draw_panel, draw_version_warning, draw_no_settings, draw_import_as_geometry_node_settings

class IMPORT_SCENE_PLYSettings():
    @draw_version_warning
    def draw(self, operator, module_name, layout):
        layout.use_property_split = True
        layout.use_property_decorate = False  # No animation.

        if module_name == 'geometry_node':
            draw_import_as_geometry_node_settings(layout, operator, 'PLYGNSettings')

        if module_name == 'default':
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
