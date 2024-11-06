from . import draw_panel

class IMPORT_SCENE_X3DSettings():
    def draw(self, operator, module_name,  layout):
        layout.use_property_split = True
        layout.use_property_decorate = False  # No animation.

        transform = layout.box()
        transform.label(text='Transform', icon='OBJECT_DATA')
        transform.prop(operator, 'axis_forward')
        transform.prop(operator, 'axis_up')