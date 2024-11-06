from . import draw_panel

class IMPORT_SCENE_X3DSettings():
    def draw(self, operator, module_name,  layout):
        layout.use_property_split = True
        layout.use_property_decorate = False  # No animation.

        op = [  [operator, 'axis_forward'],
                [operator, 'axis_up']]
        
        draw_panel(layout, op, 'X3DSettings_Transform', 'Transform', icon='OBJECT_DATA')
