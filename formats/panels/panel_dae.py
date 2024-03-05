
class IMPORT_SCENE_DAESettings():
    def draw(operator,  layout):
        layout.use_property_split = True
        layout.use_property_decorate = False  # No animation.

        data = layout.box()
        data.label(text='Import Data Options', icon='MESH_DATA')
        data.prop(operator, 'import_units')
        data.prop(operator, 'custom_normals')

        armature = layout.box()
        armature.label(text='Armature', icon='ARMATURE_DATA')
        armature.prop(operator, 'fix_orientation')
        armature.prop(operator, 'find_chains')
        armature.prop(operator, 'auto_connect')
        armature.prop(operator, 'min_chain_length')

        misc = layout.box()
        misc.prop(operator, 'keep_bind_info')
