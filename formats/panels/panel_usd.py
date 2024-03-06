
class IMPORT_SCENE_USDSettings():
    def draw(self, operator, module_name,  layout):
        layout.use_property_split = True
        layout.use_property_decorate = False  # No animation.

        include = layout.box()
        include.label(text='Data Types', icon='IMPORT')
        row = include.row(align=True)
        col = row.column(align=True)
        col.prop(operator, 'import_cameras')
        col.prop(operator, 'import_curves')
        col.prop(operator, 'import_lights')
        col.prop(operator, 'import_materials')
        col.prop(operator, 'import_meshes')
        col = row.column(align=True)
        col.prop(operator, 'import_volumes')
        col.prop(operator, 'import_shapes')
        col.prop(operator, 'import_skeletons')
        col.prop(operator, 'import_blendshapes')
        col = include.column(align=True)
        col.prop(operator, 'prim_path_mask')
        col.prop(operator, 'scale')

        misc = layout.box()
        base_col = misc.column(align=True)
        base_col.label(text='Mesh Data', icon='MESH_DATA')
        col = base_col.column(align=True)
        col.prop(operator, 'read_mesh_uvs')
        col.prop(operator, 'read_mesh_colors')
        col.prop(operator, 'read_mesh_attributes')

        base_col.separator()

        base_col = misc.column(align=True)
        base_col.label(text='Include', icon='IMPORT')
        col = base_col.column(align=True)
        col.prop(operator, 'import_subdiv')
        col.prop(operator, 'support_scene_instancing')
        col.prop(operator, 'import_visible_only')
        col.prop(operator, 'import_guide')
        col.prop(operator, 'import_proxy')
        col.prop(operator, 'import_render')

        base_col.separator()

        base_col = misc.column(align=True)
        base_col.label(text='Options', icon='OPTIONS')
        col = base_col.column(align=True)
        col.prop(operator, 'set_frame_range')
        col.prop(operator, 'relative_path')
        col.prop(operator, 'create_collection')
        col.prop(operator, 'light_intensity_scale')

        materials = layout.box()
        materials.label(text='Materials', icon='MATERIAL')
        col = materials.column(align=True)
        col.prop(operator, 'import_all_materials')
        col.prop(operator, 'import_usd_preview')
        col.prop(operator, 'set_material_blend')
        col.prop(operator, 'mtl_name_collision_mode')

        textures = layout.box()
        textures.label(text='Textures', icon='TEXTURE')
        col = textures.column(align=True)
        col.prop(operator, 'import_textures_mode')
        col.prop(operator, 'import_textures_dir')
        col.prop(operator, 'tex_name_collision_mode')