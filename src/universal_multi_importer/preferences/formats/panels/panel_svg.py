from . import draw_no_settings, draw_panel, draw_version_warning

class IMPORT_SCENE_SVGSettings():
    @draw_version_warning
    def draw(self, operator, module_name,  layout):
        if module_name == 'default':
            draw_no_settings(layout)

        if module_name == 'grease_pencil':
            layout.use_property_split = True
            layout.use_property_decorate = False

            op=[[operator, 'resolution'],
                [operator, 'scale']]

            draw_panel(layout, op, 'SVGSettings_options', 'Options', 'OPTIONS')
