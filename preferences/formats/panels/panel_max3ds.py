from . import draw_panel, BVERSION, draw_version_warning

class IMPORT_SCENE_MAX3DSSettings():
    @draw_version_warning
    def draw(self, operator, module_name, layout):
        layout.use_property_split = True
        layout.use_property_decorate = False  # No animation.

        if BVERSION >= 4.2:
            op = [[operator, 'use_image_search'],
                [operator, 'object_filter'],
                [operator, 'use_keyframes'],
                [operator, 'use_collection'],
                [operator, 'use_cursor']]

            draw_panel(layout, op, 'MAX3DSSettings_Include', 'Include', icon='IMPORT')

            op = [[operator, 'constrain_size'],
                [operator, 'use_scene_unit'],
                [operator, 'use_apply_transform'],
                [operator, 'axis_forward'],
                [operator, 'axis_up']]

            draw_panel(layout, op, 'MAX3DSSettings_Transform', 'Transform', icon='OBJECT_DATA')

        elif BVERSION >= 4.0:
            op = [[operator, 'use_image_search'],
                [operator, 'object_filter'],
                [operator, 'use_keyframes'],
                [operator, 'use_cursor']]

            draw_panel(layout, op, 'MAX3DSSettings_Include', 'Include', icon='IMPORT')

            op = [[operator, 'constrain_size'],
                [operator, 'use_scene_unit'],
                [operator, 'use_apply_transform'],
                [operator, 'axis_forward'],
                [operator, 'axis_up']]

            draw_panel(layout, op, 'MAX3DSSettings_Transform', 'Transform', icon='OBJECT_DATA')

        elif BVERSION >= 3.6:

            op = [[operator, 'constrain_size'],
                [operator, 'use_image_search'],
                [operator, 'use_apply_transform'],
                [operator, 'read_keyframe'],
                [operator, 'axis_forward'],
                [operator, 'axis_up']]

            draw_panel(layout, op, 'MAX3DSSettings_Transform', 'Transform', icon='OBJECT_DATA')

        else:
            op = [[operator, 'use_image_search'],
                [operator, 'object_filter'],
                [operator, 'use_keyframes'],
                [operator, 'use_cursor']]

            draw_panel(layout, op, 'MAX3DSSettings_Include', 'Include', icon='IMPORT')

            op = [[operator, 'constrain_size'],
                [operator, 'use_scene_unit'],
                [operator, 'use_center_pivot'],
                [operator, 'use_apply_transform'],
                [operator, 'use_world_matrix'],
                [operator, 'axis_forward'],
                [operator, 'axis_up']]

            draw_panel(layout, op, 'MAX3DSSettings_Transform', 'Transform', icon='OBJECT_DATA')
