from . import draw_panel

class IMPORT_SCENE_STLSettings():
    def draw(self, operator, module_name, layout):
        layout.use_property_split = True
        layout.use_property_decorate = False  # No animation.
        

        options = layout.box()
        options.label(text='Options', icon='OPTIONS')

        options.prop(operator, 'global_scale')
        options.prop(operator, 'use_scene_unit')
        options.prop(operator, 'use_facet_normal')
        
        if module_name == 'default':
            options.prop(operator, 'forward_axis')
            options.prop(operator, 'up_axis')
            options.prop(operator, 'use_mesh_validate')
        
        if module_name == 'legacy':
            options.prop(operator, 'axis_forward')
            options.prop(operator, 'axis_up')
