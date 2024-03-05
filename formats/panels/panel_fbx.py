
class IMPORT_SCENE_FBXSettings():
    def draw(operator, module_name,  layout):
        layout.use_property_split = True
        layout.use_property_decorate = False  # No animation.

        include = layout.box()
        include.label(text='Include', icon='IMPORT')
        include.prop(operator, "use_custom_normals")
        include.prop(operator, "use_subsurf")
        include.prop(operator, "use_custom_props")
        sub = include.row()
        sub.enabled = operator.use_custom_props
        sub.prop(operator, "use_custom_props_enum_as_string")
        include.prop(operator, "use_image_search")
        include.prop(operator, "colors_type")

        transform = layout.box()
        transform.label(text='Transform', icon='OBJECT_DATA')
        transform.prop(operator, "global_scale")
        transform.prop(operator, "decal_offset")
        row = transform.row()
        row.prop(operator, "bake_space_transform")
        row.label(text="", icon='ERROR')
        transform.prop(operator, "use_prepost_rot")

        transform.prop(operator, "use_manual_orientation")

        manual_transform = transform.box()
        manual_transform.enabled = operator.use_manual_orientation
        manual_transform.prop(operator, "axis_forward")
        manual_transform.prop(operator, "axis_up")

        animation = layout.box()
        animation.prop(operator, "use_anim")
        col = animation.column()
        col.enabled = operator.use_anim
        col.prop(operator, "anim_offset")

        armature = layout.box()
        armature.label(text='Armature', icon='ARMATURE_DATA')
        armature.prop(operator, "ignore_leaf_bones")
        armature.prop(operator, "force_connect_children"),
        armature.prop(operator, "automatic_bone_orientation")

        sub = armature.column()
        sub.enabled = not operator.automatic_bone_orientation
        sub.prop(operator, "primary_bone_axis")
        sub.prop(operator, "secondary_bone_axis")
