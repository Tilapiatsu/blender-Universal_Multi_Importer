from . import draw_no_settings
class IMPORT_SCENE_SVGSettings():
    def draw(self, operator, module_name,  layout):
        if module_name == 'default':
            draw_no_settings(layout)

        if module_name == 'grease_pencil':
            layout.use_property_split = True
            layout.use_property_decorate = False
            options = layout.box()
            options.label(text='Options', icon='OPTIONS')
            options.prop(operator, 'resolution')
            options.prop(operator, 'scale')