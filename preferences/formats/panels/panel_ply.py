from . import draw_panel

class IMPORT_SCENE_PLYSettings():
    def draw(self, operator, module_name, layout):
        layout.use_property_split = True
        layout.use_property_decorate = False  # No animation.

        op =    [[operator, 'global_scale'],
                 [operator, 'use_scene_unit'],
                 [operator, 'forward_axis'],
                 [operator, 'up_axis'],
                 [operator, 'merge_verts'],
                 [operator, 'import_colors']]
        
        draw_panel(layout, op, 'PLYSettings_Options', 'Options', icon='OPTIONS')
