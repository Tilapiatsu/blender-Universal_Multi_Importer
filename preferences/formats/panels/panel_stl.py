from . import draw_panel

class IMPORT_SCENE_STLSettings():
    def draw(self, operator, module_name, layout):
        layout.use_property_split = True
        layout.use_property_decorate = False  # No animation.
        
        if module_name == 'default':
            op = [[operator, 'global_scale'],
                 [operator, 'use_scene_unit'],
                 [operator, 'use_facet_normal'],
                 [operator, 'forward_axis'],
                 [operator, 'up_axis'],
                 [operator, 'use_mesh_validate']]
        
            draw_panel(layout, op, 'STLSettings_Options', 'Options', icon='OPTIONS')

        
        if module_name == 'legacy':
            op = [[operator, 'global_scale'],
                 [operator, 'use_scene_unit'],
                 [operator, 'use_facet_normal'],
                 [operator, 'axis_forward'],
                 [operator, 'axis_up']]
        
            draw_panel(layout, op, 'STLSettings_Options', 'Options', icon='OPTIONS')

