
class IMPORT_SCENE_SVGSettings():
    def draw(self, operator, module_name,  layout):
        layout.use_property_split = True
        layout.use_property_decorate = False  # No animation.

        if module_name == 'default':
            options = layout.box()
            options.label(text='No Settings')

        if module_name == 'grease_pencil':
            options = layout.box()
            options.label(text='Options', icon='OPTIONS')
            options.prop(operator, 'resolution')
            options.prop(operator, 'scale')