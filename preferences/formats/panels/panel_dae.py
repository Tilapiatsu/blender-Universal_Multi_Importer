from . import draw_panel

class IMPORT_SCENE_DAESettings():
    def draw(self, operator, module_name, layout):
        layout.use_property_split = True
        layout.use_property_decorate = False  # No animation.

        op = [[operator, 'import_units'],
              [operator, 'custom_normals']]
        
        draw_panel(layout, op, 'DAESettings_Options', 'Import Data Options', icon='MESH_DATA')

        op = [[operator, 'fix_orientation'],
              [operator, 'find_chains'],
              [operator, 'auto_connect'],
              [operator, 'min_chain_length']]
        
        draw_panel(layout, op, 'DAESettings_Armature', 'Armature', icon='ARMATURE_DATA')

        op = [[operator, 'keep_bind_info']]
        
        draw_panel(layout, op, 'DAESettings_Misc', 'Miscandelous', icon='PRESET')

