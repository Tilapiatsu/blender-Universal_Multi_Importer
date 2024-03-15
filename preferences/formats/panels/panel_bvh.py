
class IMPORT_SCENE_BVHSettings():
    def draw(self, operator, module_name, layout):
        layout.use_property_split = True
        layout.use_property_decorate = False

        layout.prop(operator, 'target')

        transform = layout.box()
        transform.label(text='Transform', icon='OBJECT_DATA')

        transform.prop(operator, 'global_scale')
        transform.prop(operator, 'rotate_mode')
        transform.prop(operator, 'axis_forward')
        transform.prop(operator, 'axis_up')

        animation = layout.box()
        animation.label(text='Animation', icon='ARMATURE_DATA')
        animation.prop(operator, 'frame_start')
        animation.prop(operator, 'use_fps_scale')
        animation.prop(operator, 'use_cyclic')
        animation.prop(operator, 'update_scene_fps')
        animation.prop(operator, 'update_scene_duration')