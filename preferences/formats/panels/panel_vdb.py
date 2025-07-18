from . import draw_panel, draw_version_warning

class IMPORT_SCENE_VDBSettings():
    @draw_version_warning
    def draw(self, operator, module_name, layout):
        layout.use_property_split = True
        layout.use_property_decorate = False  # No animation.

        op = [[operator, 'relative_path'],
              [operator, 'use_sequence_detection'],
              [operator, 'align'],
              [operator, 'location'],
              [operator, 'rotation']]

        draw_panel(layout, op, 'VDBSettings_transform', 'Options', icon='OPTIONS')

