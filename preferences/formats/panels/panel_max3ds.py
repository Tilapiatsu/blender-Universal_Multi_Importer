from . import draw_panel

class IMPORT_SCENE_MAX3DSSettings():
    def draw(self, operator, module_name, layout):
        layout.use_property_split = True
        layout.use_property_decorate = False  # No animation.

        op = [[operator, 'use_image_search'], 
              [operator, 'object_filter'],
              [operator, 'use_keyframes'], 
              [operator, 'use_collection'], 
              [operator, 'use_cursor']]
        
        draw_panel(layout, op, 'MAX3DSSettings_Include', 'Include', icon='IMPORT')

        op = [[operator, 'constrain_size'],
              [operator, 'use_scene_unit'],
              [operator, 'use_apply_transform'],
              [operator, 'axis_forward'],
              [operator, 'axis_up']]
        
        draw_panel(layout, op, 'MAX3DSSettings_Transform', 'Transform', icon='OBJECT_DATA')
