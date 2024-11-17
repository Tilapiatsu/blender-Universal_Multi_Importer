from . import draw_panel

class IMPORT_SCENE_ABCSettings():
    def draw(self, operator, module_name, layout):
        layout.use_property_split = True
        layout.use_property_decorate = False  # No animation.

        op = [[operator, 'scale']]
        
        draw_panel(layout, [[operator, 'scale']], 'ABCSettings_transform', 'Manual Transform', icon='OBJECT_DATA')

        op = [[operator, 'relative_path'],
              [operator, 'set_frame_range'],
              [operator, 'is_sequence'],
              [operator, 'validate_meshes'],
              [operator, 'always_add_cache_reader']]
        
        draw_panel(layout, op, 'ABCSettings_options', 'Options', icon='OPTIONS')
