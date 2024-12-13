from . import BVERSION
from . import draw_panel, draw_version_warning

class IMPORT_SCENE_GLTFSettings():
    @draw_version_warning
    def draw(self, operator, module_name, layout):
        layout.use_property_split = True
        layout.use_property_decorate = False  # No animation.

        if BVERSION >= 4.2:
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

        elif BVERSION >= 3.4:
            op =    [[operator, 'import_pack_images'],
                    [operator, 'merge_vertices'],
                    [operator, 'import_shading'],
                    [operator, 'guess_original_bind_pose'],
                    [operator, 'bone_heuristic'],
                    [operator, 'convert_lighting_mode']]

            draw_panel(layout, op, 'GLTFSettings_Options', 'Options', icon='OPTIONS')

