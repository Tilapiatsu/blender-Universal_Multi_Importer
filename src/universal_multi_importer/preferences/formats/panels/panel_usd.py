from universal_multi_importer.bversion import BVERSION
from universal_multi_importer.preferences.formats.panels import draw_panel, draw_version_warning

class IMPORT_SCENE_USDSettings():
    @draw_version_warning
    def draw(self, operator, module_name,  layout):
        layout.use_property_split = True
        layout.use_property_decorate = False  # No animation.

        if BVERSION >= 5.0:
            op = [[operator,    'prim_path_mask'],
                 [operator,     'import_visible_only'],
                 [operator,     'import_defined_only'],
                 [operator,     'set_frame_range'],
                 [operator,     'create_collection'],
                 [operator,     'relative_path'],
                 [operator,     'scale'],
                 [operator,     'light_intensity_scale'],
                 [operator,     'property_import_mode']]

            draw_panel(layout, op, 'USDSettings_General', 'General', icon='IMPORT')

            header, object_type = layout.panel(idname='USDSettings_ObjectTypes')
            header.label(text='Object Types', icon='IMPORT')

            if object_type:
                row = object_type.row(align=True)
                col = row.column(align=True)
                col.prop(operator, 'import_cameras')
                col.prop(operator, 'import_curves')
                col.prop(operator, 'import_lights')
                col.prop(operator, 'create_world_material')
                col.prop(operator, 'import_materials')
                col = row.column(align=True)
                col.prop(operator, 'import_meshes')
                col.prop(operator, 'import_volumes')
                col.prop(operator, 'import_points')
                col.prop(operator, 'import_shapes')

            op = [[operator,    'import_render'],
                [operator,     'import_proxy'],
                [operator,     'import_guide'],
                [operator,     'mtl_purpose']]

            draw_panel(layout, op, 'USDSettings_DisplayPurpose', 'Display Purpose', icon='RESTRICT_VIEW_OFF')

            op = [  [operator,    'read_mesh_uvs'],
                    [operator,    'read_mesh_colors'],
                    [operator,    'read_mesh_attributes'],
                    [operator,    'import_subdivision'],
                    [operator,    'validate_meshes'],
                    [operator,    'merge_parent_xform']]

            draw_panel(layout, op, 'USDSettings_Geometry', 'Geometry', icon='MESH_DATA', default_closed=True)

            op = [[operator,    'import_blendshapes'],
                 [operator,     'import_skeletons']]

            draw_panel(layout, op, 'USDSettings_Rigging', 'Rigging', icon='BONE_DATA', default_closed=True)

            op = [  [operator,    'import_all_materials'],
                    [operator,    'import_usd_preview'],
                    [operator,    'set_material_blend'],
                    [operator,    'mtl_name_collision_mode']]

            draw_panel(layout, op, 'USDSettings_Materials', 'Materials', icon='MATERIAL', default_closed=True)

            op = [[operator,    'import_textures_mode']]

            header, panel = draw_panel(layout, op, 'USDSettings_Textures', 'Textures', icon='TEXTURE', default_closed=True)

            if panel:
                col = panel.column()
                col.enabled = operator.import_textures_mode in ['IMPORT_COPY']

                col.prop(operator, 'import_textures_dir')
                col.prop(operator, 'tex_name_collision_mode')

            op = [[operator,    'support_scene_instancing']]

            draw_panel(layout, op, 'USDSettings_ParticlesAndInstancing', 'Particles and Instancing', icon='MOD_PARTICLE_INSTANCE', default_closed=True)

        elif BVERSION >= 4.3:
            op = [[operator,    'prim_path_mask'],
                 [operator,     'import_visible_only'],
                 [operator,     'import_defined_only'],
                 [operator,     'set_frame_range'],
                 [operator,     'create_collection'],
                 [operator,     'relative_path'],
                 [operator,     'scale'],
                 [operator,     'light_intensity_scale'],
                 [operator,     'attr_import_mode']]

            draw_panel(layout, op, 'USDSettings_General', 'General', icon='IMPORT')

            header, object_type = layout.panel(idname='USDSettings_ObjectTypes')
            header.label(text='Object Types', icon='IMPORT')

            if object_type:
                row = object_type.row(align=True)
                col = row.column(align=True)
                col.prop(operator, 'import_cameras')
                col.prop(operator, 'import_curves')
                col.prop(operator, 'import_lights')
                col.prop(operator, 'import_materials')
                col = row.column(align=True)
                col.prop(operator, 'import_meshes')
                col.prop(operator, 'import_volumes')
                col.prop(operator, 'import_points')
                col.prop(operator, 'import_shapes')

            op = [[operator,    'import_render'],
                [operator,     'import_proxy'],
                [operator,     'import_guide'],
                [operator,     'mtl_purpose']]

            draw_panel(layout, op, 'USDSettings_DisplayPurpose', 'Display Purpose', icon='RESTRICT_VIEW_OFF')

            op = [[operator,    'read_mesh_uvs'],
                 [operator,     'read_mesh_colors'],
                 [operator,     'read_mesh_attributes'],
                 [operator,     'import_subdiv'],
                 [operator,     'validate_meshes']]

            draw_panel(layout, op, 'USDSettings_Geometry', 'Geometry', icon='MESH_DATA', default_closed=True)

            op = [[operator,    'import_blendshapes'],
                 [operator,     'import_skeletons']]

            draw_panel(layout, op, 'USDSettings_Rigging', 'Rigging', icon='BONE_DATA', default_closed=True)

            op = [[operator,    'import_all_materials'],
                 [operator,     'import_usd_preview'],
                 [operator,     'create_world_material'],
                 [operator,     'set_material_blend'],
                 [operator,     'mtl_name_collision_mode']]

            draw_panel(layout, op, 'USDSettings_Materials', 'Materials', icon='MATERIAL', default_closed=True)

            op = [[operator,    'import_textures_mode']]

            header, panel = draw_panel(layout, op, 'USDSettings_Textures', 'Textures', icon='TEXTURE', default_closed=True)

            if panel:
                col = panel.column()
                col.enabled = operator.import_textures_mode in ['IMPORT_COPY']

                col.prop(operator, 'import_textures_dir')
                col.prop(operator, 'tex_name_collision_mode')

            op = [[operator,    'support_scene_instancing']]

            draw_panel(layout, op, 'USDSettings_ParticlesAndInstancing', 'Particles and Instancing', icon='MOD_PARTICLE_INSTANCE', default_closed=True)

        elif BVERSION >= 4.2:
            op = [[operator,    'prim_path_mask'],
                 [operator,     'import_visible_only'],
                 [operator,     'import_defined_only'],
                 [operator,     'set_frame_range'],
                 [operator,     'create_collection'],
                 [operator,     'relative_path'],
                 [operator,     'scale'],
                 [operator,     'light_intensity_scale'],
                 [operator,     'attr_import_mode']]

            draw_panel(layout, op, 'USDSettings_General', 'General', icon='IMPORT')

            header, object_type = layout.panel(idname='USDSettings_ObjectTypes')
            header.label(text='Object Types', icon='IMPORT')

            if object_type:
                row = object_type.row(align=True)
                col = row.column(align=True)
                col.prop(operator, 'import_cameras')
                col.prop(operator, 'import_curves')
                col.prop(operator, 'import_lights')
                col.prop(operator, 'import_materials')
                col = row.column(align=True)
                col.prop(operator, 'import_meshes')
                col.prop(operator, 'import_volumes')
                col.prop(operator, 'import_points')
                col.prop(operator, 'import_shapes')

            op = [[operator,    'import_render'],
                [operator,     'import_proxy'],
                [operator,     'import_guide']]

            draw_panel(layout, op, 'USDSettings_DisplayPurpose', 'Display Purpose', icon='RESTRICT_VIEW_OFF')

            op = [[operator,    'read_mesh_uvs'],
                 [operator,     'read_mesh_colors'],
                 [operator,     'read_mesh_attributes'],
                 [operator,     'import_subdiv'],
                 [operator,     'validate_meshes']]

            draw_panel(layout, op, 'USDSettings_Geometry', 'Geometry', icon='MESH_DATA', default_closed=True)

            op = [[operator,    'import_blendshapes'],
                 [operator,     'import_skeletons']]

            draw_panel(layout, op, 'USDSettings_Rigging', 'Rigging', icon='BONE_DATA', default_closed=True)

            op = [[operator,    'import_all_materials'],
                 [operator,     'import_usd_preview'],
                 [operator,     'create_world_material'],
                 [operator,     'set_material_blend'],
                 [operator,     'mtl_name_collision_mode']]

            draw_panel(layout, op, 'USDSettings_Materials', 'Materials', icon='MATERIAL', default_closed=True)

            op = [[operator,    'import_textures_mode']]

            header, panel = draw_panel(layout, op, 'USDSettings_Textures', 'Textures', icon='TEXTURE', default_closed=True)

            if panel:
                col = panel.column()
                col.enabled = operator.import_textures_mode in ['IMPORT_COPY']

                col.prop(operator, 'import_textures_dir')
                col.prop(operator, 'tex_name_collision_mode')

            op = [[operator,    'support_scene_instancing']]

            draw_panel(layout, op, 'USDSettings_ParticlesAndInstancing', 'Particles and Instancing', icon='MOD_PARTICLE_INSTANCE', default_closed=True)

        elif BVERSION >= 4.1:
            op = [[operator,    'prim_path_mask'],
                 [operator,     'import_visible_only'],
                 [operator,     'set_frame_range'],
                 [operator,     'create_collection'],
                 [operator,     'relative_path'],
                 [operator,     'scale'],
                 [operator,     'light_intensity_scale']]

            draw_panel(layout, op, 'USDSettings_General', 'General', icon='IMPORT')

            object_type = layout.box()
            header = object_type.row(align=True)
            header.label(text='Object Types', icon='IMPORT')

            row = object_type.row(align=True)
            col = row.column(align=True)
            col.prop(operator, 'import_cameras')
            col.prop(operator, 'import_curves')
            col.prop(operator, 'import_lights')
            col.prop(operator, 'import_materials')
            col = row.column(align=True)
            col.prop(operator, 'import_meshes')
            col.prop(operator, 'import_volumes')
            col.prop(operator, 'import_shapes')

            op = [[operator,    'import_render'],
                [operator,     'import_proxy'],
                [operator,     'import_guide']]

            draw_panel(layout, op, 'USDSettings_DisplayPurpose', 'Display Purpose', icon='RESTRICT_VIEW_OFF')

            op = [[operator,    'read_mesh_uvs'],
                 [operator,     'read_mesh_colors'],
                 [operator,     'read_mesh_attributes'],
                 [operator,     'import_subdiv']]

            draw_panel(layout, op, 'USDSettings_Geometry', 'Geometry', icon='MESH_DATA', default_closed=True)

            op = [[operator,    'import_blendshapes'],
                 [operator,     'import_skeletons']]

            draw_panel(layout, op, 'USDSettings_Rigging', 'Rigging', icon='BONE_DATA', default_closed=True)

            op = [[operator,    'import_all_materials'],
                 [operator,     'import_usd_preview'],
                 [operator,     'set_material_blend'],
                 [operator,     'mtl_name_collision_mode']]

            draw_panel(layout, op, 'USDSettings_Materials', 'Materials', icon='MATERIAL', default_closed=True)

            op = [[operator,    'import_textures_mode'],
                 [operator,     'import_textures_dir'],
                 [operator,     'tex_name_collision_mode']]

            draw_panel(layout, op, 'USDSettings_Textures', 'Textures', icon='TEXTURE', default_closed=True)

            op = [[operator,    'support_scene_instancing']]

            draw_panel(layout, op, 'USDSettings_ParticlesAndInstancing', 'Particles and Instancing', icon='MOD_PARTICLE_INSTANCE', default_closed=True)

        else:
            op = [[operator,    'import_cameras'],
                 [operator,     'import_curves'],
                 [operator,     'import_lights'],
                 [operator,     'import_materials'],
                 [operator,     'import_meshes'],
                 [operator,     'import_volumes'],
                 [operator,     'prim_path_mask'],
                 [operator,     'scale']]

            draw_panel(layout, op, 'USDSettings_General', 'Data Types', icon='IMPORT')

            op = [[operator,    'read_mesh_uvs'],
                 [operator,     'read_mesh_colors']]

            draw_panel(layout, op, 'USDSettings_MeshData', 'Mesh Data', icon='OBJECT_DATA')

            op = [[operator,    'import_subdiv'],
                 [operator,     'import_instance_proxies'],
                 [operator,     'import_visible_only'],
                 [operator,     'import_guide'],
                 [operator,     'import_proxy'],
                 [operator,     'import_render']]

            draw_panel(layout, op, 'USDSettings_MeshData', 'Include', icon='IMPORT')

            op = [[operator,    'set_frame_range'],
                 [operator,     'relative_path'],
                 [operator,     'light_intensity_scale']]

            draw_panel(layout, op, 'USDSettings_MeshData', 'Options', icon='OPTIONS')

            op = [[operator,    'import_usd_preview'],
                 [operator,     'set_material_blend']]

            draw_panel(layout, op, 'USDSettings_Experimental', 'Experimental', icon='ERROR')