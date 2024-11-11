from . import draw_panel

class IMPORT_SCENE_MAXSettings():
    def draw(self, operator, module_name, layout):
        layout.use_property_split = True
        layout.use_property_decorate = False  # No animation.

        op = [[operator, 'use_image_search'], 
              [operator, 'object_filter'], 
              [operator, 'use_collection']]
        
        draw_panel(layout, op, 'MAXSettings_Include', 'Include', icon='IMPORT')

        op = [[operator, 'scale_objects'],
              [operator, 'use_apply_matrix'],
              [operator, 'axis_forward'],
              [operator, 'axis_up']]
        
        draw_panel(layout, op, 'MAXSettings_Transform', 'Transform', icon='OBJECT_DATA')
