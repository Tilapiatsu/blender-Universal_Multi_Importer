
class IMPORT_SCENE_SVGSettings():
    def draw(self, context, operator, module_name,  layout):
        layout.use_property_split = True
        layout.use_property_decorate = False  # No animation.

        transorm = layout.box()
        transorm.label(text='TODO', icon='OBJECT_DATA')
        # transorm.prop(operator, 'global_scale')
        # transorm.prop(operator, 'clamp_size')
        # transorm.prop(operator, 'forward_axis')
        # transorm.prop(operator, 'up_axis')

        # options = layout.box()
        # options.label(text='Options', icon='EXPORT')
        # options.prop(operator, 'use_split_objects')
        # options.prop(operator, 'use_split_groups')
        # options.prop(operator, 'import_vertex_groups')
        # options.prop(operator, 'validate_meshes')
        # options.prop(operator, 'collection_separator')