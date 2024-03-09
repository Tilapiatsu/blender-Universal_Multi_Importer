
class IMPORT_SCENE_GLTFSettings():
    def draw(self, operator, module_name, layout):
        layout.use_property_split = True
        layout.use_property_decorate = False  # No animation.

        options = layout.box()
        options.label(text='Options', icon='OPTIONS')

        options.prop(operator, 'import_pack_images')
        options.prop(operator, 'merge_vertices')
        options.prop(operator, 'import_shading')
        options.prop(operator, 'guess_original_bind_pose')
        options.prop(operator, 'bone_heuristic')
        options.prop(operator, 'export_import_convert_lighting_mode')
        options.prop(operator, 'import_webp_texture')