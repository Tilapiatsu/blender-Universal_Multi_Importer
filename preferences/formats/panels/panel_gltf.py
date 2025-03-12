from . import BVERSION
from . import draw_panel, draw_version_warning

class IMPORT_SCENE_GLTFSettings():
    @draw_version_warning
    def draw(self, operator, module_name, layout):
        layout.use_property_split = True
        layout.use_property_decorate = False  # No animation.

        if BVERSION >= 4.4:
            op =    [
                    [operator, 'merge_vertices'],
                    [operator, 'import_shading'],
                    [operator, 'export_import_convert_lighting_mode']
                    ]

            draw_panel(layout, op, 'GLTFSettings_Options', 'Options', icon='OPTIONS')

            op =    [
                    [operator, 'import_pack_images'],
                    [operator, 'import_webp_texture']
                    ]

            draw_panel(layout, op, 'GLTFSettings_Texture', 'Texture', icon='TEXTURE')

            op =    [
                    [operator, 'bone_heuristic'],
                    [operator, 'guess_original_bind_pose'],
                    [operator, 'disable_bone_shape'],
                    [operator, 'bone_shape_scale_factor']
                    ]

            draw_panel(layout, op, 'GLTFSettings_BonesNSkin', 'Bone & Skin', icon='BONE_DATA')

            op =    [
                    [operator, 'import_select_created_objects'],
                    [operator, 'import_scene_extras'],
                    ]

            draw_panel(layout, op, 'GLTFSettings_Pipeline', 'Pipeline', icon='SYSTEM')

        elif BVERSION >= 4.2:
            op =    [[operator, 'import_pack_images'],
                    [operator, 'merge_vertices'],
                    [operator, 'import_shading'],
                    [operator, 'guess_original_bind_pose'],
                    [operator, 'export_import_convert_lighting_mode'],
                    [operator, 'import_webp_texture']]

            draw_panel(layout, op, 'GLTFSettings_Options', 'Options', icon='OPTIONS')

            op =    [[operator, 'bone_heuristic'],
                    [operator, 'disable_bone_shape'],
                    [operator, 'bone_shape_scale_factor']]

            draw_panel(layout, op, 'GLTFSettings_Bones', 'Bones', icon='BONE_DATA')

        elif BVERSION >= 4.0:
            op =    [[operator, 'import_pack_images'],
                    [operator, 'merge_vertices'],
                    [operator, 'import_shading'],
                    [operator, 'guess_original_bind_pose'],
                    [operator, 'bone_heuristic'],
                    [operator, 'export_import_convert_lighting_mode'],
                    [operator, 'import_webp_texture']]

            draw_panel(layout, op, 'GLTFSettings_Options', 'Options', icon='OPTIONS')

        elif BVERSION >= 3.6:
            op =    [[operator, 'import_pack_images'],
                    [operator, 'merge_vertices'],
                    [operator, 'import_shading'],
                    [operator, 'guess_original_bind_pose'],
                    [operator, 'bone_heuristic'],
                    [operator, 'export_import_convert_lighting_mode']]

            draw_panel(layout, op, 'GLTFSettings_Options', 'Options', icon='OPTIONS')

        elif BVERSION >= 3.4:
            op =    [[operator, 'import_pack_images'],
                    [operator, 'merge_vertices'],
                    [operator, 'import_shading'],
                    [operator, 'guess_original_bind_pose'],
                    [operator, 'bone_heuristic'],
                    [operator, 'convert_lighting_mode']]

            draw_panel(layout, op, 'GLTFSettings_Options', 'Options', icon='OPTIONS')

        # elif BVERSION >= 3.1:
        else:
            op =    [[operator, 'import_pack_images'],
                    [operator, 'merge_vertices'],
                    [operator, 'import_shading'],
                    [operator, 'guess_original_bind_pose'],
                    [operator, 'bone_heuristic']]

            draw_panel(layout, op, 'GLTFSettings_Options', 'Options', icon='OPTIONS')

