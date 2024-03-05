
class IMPORT_SCENE_PLYSettings():
    def draw(operator, module_name,  layout):
        layout.use_property_split = True
        layout.use_property_decorate = False  # No animation.

        options = layout.box()
        options.label(text='Options', icon='OPTIONS')

        options.prop(operator, 'global_scale')
        options.prop(operator, 'use_scene_unit')
        options.prop(operator, 'forward_axis')
        options.prop(operator, 'up_axis')
        options.prop(operator, 'merge_verts')
        options.prop(operator, 'import_colors')
