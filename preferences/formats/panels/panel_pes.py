from . import draw_panel

class IMPORT_SCENE_MAXSettings():
    def draw(self, operator, module_name, layout):
        layout.use_property_split = True
        layout.use_property_decorate = False  # No animation.

        op = [[operator, 'show_jump_wires'], 
              [operator, 'do_create_material'], 
              [operator, 'create_collection']]
        
        draw_panel(layout, op, 'PESSettings_Import', 'Import', icon='IMPORT')

        op = [[operator, 'line_depth'],
              [operator, 'thread_thickness']]
        
        draw_panel(layout, op, 'PESSettings_Thickness', 'Thickness', icon='MOD_OUTLINE')
