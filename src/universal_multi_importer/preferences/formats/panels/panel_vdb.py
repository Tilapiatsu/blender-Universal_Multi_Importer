from universal_multi_importer.preferences.formats.panels import draw_panel, draw_version_warning, draw_import_as_geometry_node_settings

class IMPORT_SCENE_VDBSettings():
    @draw_version_warning
    def draw(self, operator, module_name, layout):
        layout.use_property_split = True
        layout.use_property_decorate = False  # No animation.

        if module_name == 'geometry_node':
            draw_import_as_geometry_node_settings(layout, operator, 'VDBGNSettings')

        if module_name == 'default':
            op = [[operator, 'relative_path'],
                [operator, 'use_sequence_detection'],
                [operator, 'align'],
                [operator, 'location'],
                [operator, 'rotation']]

            draw_panel(layout, op, 'VDBSettings_transform', 'Options', icon='OPTIONS')

