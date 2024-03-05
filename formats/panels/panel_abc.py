
class IMPORT_SCENE_ABCSettings():
    def draw(operator,  layout):
        layout.use_property_split = True
        layout.use_property_decorate = False  # No animation.

        transorm = layout.box()
        transorm.label(text='Manual Transform', icon='OBJECT_DATA')
        transorm.prop(operator, 'scale')

        option = layout.box()
        option.label(text='Options', icon='OPTIONS')
        option.prop(operator, 'relative_path')
        option.prop(operator, 'set_frame_range')
        option.prop(operator, 'is_sequence')
        option.prop(operator, 'validate_meshes')
        option.prop(operator, 'always_add_cache_reader')
        

