from . import draw_panel, draw_version_warning, BVERSION

class IMPORT_SCENE_FBXSettings():
    @draw_version_warning
    def draw(self, operator, module_name, layout):
        layout.use_property_split = True
        layout.use_property_decorate = False  # No animation.

        if BVERSION >= 5.0:
            ##### General
            op = [[operator, 'global_scale'],
                [operator, 'use_custom_props']]

            header, panel = draw_panel(layout, op, 'FBXSettings_General', 'Genreral', icon='OPTIONS')

            if panel:
                sub = panel.row()
                sub.enabled = operator.use_custom_props
                sub.prop(operator, "use_custom_props_enum_as_string")

            #### Geometry
            op = [[operator, 'use_custom_normals'],
                [operator, 'import_subdivision'],
                [operator, 'import_colors'],
                [operator, 'validate_meshes']]

            header, panel = draw_panel(layout, op, 'FBXSettings_Geometry', 'Geometry', icon='OBJECT_DATA')

            #### Materials
            op = [[operator, 'mtl_name_collision_mode']]

            header, panel = draw_panel(layout, op, 'FBXSettings_Materials', 'Materials', icon='MATERIAL')

            op = []
            #### Anim
            _, panel = draw_panel(layout, op, 'FBXSettings_Animation', 'Animation', set_header_boolean=True, header_bool=[operator, 'use_anim'])

            if panel:
                sub = panel.column()
                sub.enabled = operator.use_anim

                sub.prop(operator, 'anim_offset')

            #### Armature
            op = [[operator, 'ignore_leaf_bones']]

            header, panel = draw_panel(layout, op, 'FBXSettings_Armature', 'Armature', icon='ARMATURE_DATA')

        elif BVERSION >= 3.4:
            ##### Include
            op = [[operator, 'use_custom_normals'],
                [operator, 'use_subsurf'],
                [operator, 'use_custom_props']]

            header, panel = draw_panel(layout, op, 'FBXSettings_Include', 'Include', icon='IMPORT')

            if panel:
                sub = panel.row()
                sub.enabled = operator.use_custom_props
                sub.prop(operator, "use_custom_props_enum_as_string")

                op = [[operator, 'use_image_search'],
                    [operator, 'colors_type']]

                draw_panel(layout, op, 'FBXSettings_Include', 'Include', icon='IMPORT', panel=panel, header=header)

            #### Transform
            op = [[operator, 'global_scale'],
                [operator, 'decal_offset']]

            header, panel = draw_panel(layout, op, 'FBXSettings_Transform', 'Transform', icon='OBJECT_DATA')
            if panel:
                row = panel.row()
                row.prop(operator, "bake_space_transform")
                row.label(text="", icon='ERROR')
                panel.prop(operator, "use_prepost_rot")

            #### Manual Orientation
            op = [[operator, 'axis_forward'],
                [operator, 'axis_up']]

            draw_panel(layout, op, 'FBXSettings_Transform_Manual_Orientation', 'Manual Orientation', default_closed=True, set_header_boolean=True, header_bool=[operator, 'use_manual_orientation'])

            #### Animation
            op = [[operator, 'anim_offset']]

            header, panel = draw_panel(layout, op, 'FBXSettings_Animation', 'Animation', icon='ANIM', default_closed=True, set_header_boolean=True, header_bool=[operator, 'use_anim'])

            op = [[operator, 'ignore_leaf_bones'],
                [operator, 'force_connect_children'],
                [operator, 'automatic_bone_orientation']]

            #### Armature
            header, panel = draw_panel(layout, op, 'FBXSettings_Armature', 'Armature', icon='ARMATURE_DATA', default_closed=True)

            if panel:
                sub = panel.column()
                sub.enabled = not operator.automatic_bone_orientation
                sub.prop(operator, "primary_bone_axis")
                sub.prop(operator, "secondary_bone_axis")

        # elif BVERSION >= 3.1:
        else:
            ##### Include
            op = [[operator, 'use_custom_normals'],
                [operator, 'use_subsurf'],
                [operator, 'use_custom_props']]

            header, panel = draw_panel(layout, op, 'FBXSettings_Include', 'Include', icon='IMPORT')

            if panel:
                sub = panel.row()
                sub.enabled = operator.use_custom_props
                sub.prop(operator, "use_custom_props_enum_as_string")

                op = [[operator, 'use_image_search']]

                draw_panel(layout, op, 'FBXSettings_Include', 'Include', icon='IMPORT', panel=panel, header=header)

            #### Transform
            op = [[operator, 'global_scale'],
                [operator, 'decal_offset']]

            header, panel = draw_panel(layout, op, 'FBXSettings_Transform', 'Transform', icon='OBJECT_DATA')
            if panel:
                row = panel.row()
                row.prop(operator, "bake_space_transform")
                row.label(text="", icon='ERROR')
                panel.prop(operator, "use_prepost_rot")

            #### Manual Orientation
            op = [[operator, 'axis_forward'],
                [operator, 'axis_up']]

            draw_panel(layout, op, 'FBXSettings_Transform_Manual_Orientation', 'Manual Orientation', default_closed=True, set_header_boolean=True, header_bool=[operator, 'use_manual_orientation'])

            #### Animation
            op = [[operator, 'anim_offset']]

            header, panel = draw_panel(layout, op, 'FBXSettings_Animation', 'Animation', icon='ANIM', default_closed=True, set_header_boolean=True, header_bool=[operator, 'use_anim'])

            op = [[operator, 'ignore_leaf_bones'],
                [operator, 'force_connect_children'],
                [operator, 'automatic_bone_orientation']]

            #### Armature
            header, panel = draw_panel(layout, op, 'FBXSettings_Armature', 'Armature', icon='ARMATURE_DATA', default_closed=True)

            if panel:
                sub = panel.column()
                sub.enabled = not operator.automatic_bone_orientation
                sub.prop(operator, "primary_bone_axis")
                sub.prop(operator, "secondary_bone_axis")
