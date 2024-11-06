from . import draw_no_settings
from . import BVERSION
from . import draw_panel

class IMPORT_SCENE_IMAGESettings():
    def draw(self, operator, module_name, layout):
        layout.use_property_split = True
        layout.use_property_decorate = False  # No animation.

        if module_name == 'plane':
            if BVERSION >= 4.2:
                op =    [[operator, 'relative'],
                        [operator, 'force_reload'],
                        [operator, 'image_sequence']]
        
                draw_panel(layout, op, 'IMAGESettings_Options', 'Import Options', icon='IMPORT')

                op =    [[operator, 'shader'],
                        [operator, 'show_transparent_back'],
                        [operator, 'use_backface_culling'],
                        [operator, 'overwrite_material']]
        
                draw_panel(layout, op, 'IMAGESettings_MaterialSettings', 'Material Settings', icon='MATERIAL')

                op =    [[operator, 'interpolation'],
                         [operator, 'extension'],
                        [operator, 'use_transparency'],
                        [operator, 'alpha_mode'],
                        [operator, 'use_auto_refresh']]
        
                draw_panel(layout, op, 'IMAGESettings_TextureSettings', 'Texture Settings', icon='TEXTURE')

            elif BVERSION >= 4.1:
                op =    [[operator, 'relative'],
                        [operator, 'force_reload'],
                        [operator, 'image_sequence']]
        
                draw_panel(layout, op, 'IMAGESettings_Options', 'Import Options', icon='IMPORT')

                op =    [[operator, 'compositing_nodes']]
        
                draw_panel(layout, op, 'IMAGESettings_Options', 'Compositing Nodes', icon='NODE_COMPOSITING')

                op =    [[operator, 'shader'],
                        [operator, 'show_transparent_back'],
                        [operator, 'use_backface_culling'],
                        [operator, 'overwrite_material']]
        
                draw_panel(layout, op, 'IMAGESettings_MaterialSettings', 'Material Settings', icon='MATERIAL')

            # elif BVERSION >= 4.0:
            #     op =    [[operator, 'relative'],
            #             [operator, 'force_reload'],
            #             [operator, 'image_sequence']]
        
            #     draw_panel(layout, op, 'IMAGESettings_Options', 'Import Options', icon='IMPORT')

            #     op =    [[operator, 'compositing_nodes']]
        
            #     draw_panel(layout, op, 'IMAGESettings_Options', 'Compositing Nodes', icon='NODE_COMPOSITING')

            #     op =    [[operator, 'shader'],
            #             [operator, 'show_transparent_back'],
            #             [operator, 'use_backface_culling'],
            #             [operator, 'overwrite_material']]
        
            #     draw_panel(layout, op, 'IMAGESettings_MaterialSettings', 'Material Settings', icon='MATERIAL')


            # material = layout.box()
            # material.label(text='Material Settings', icon='MATERIAL')
            # row = material.row(align=True)
            # row.prop(operator, 'shader', expand=True)
            # if BVERSION < 4.2:
            #     row = material.row(align=True)
            #     row.prop(operator, 'blend_method', expand=True)
            # material.prop(operator, 'show_transparent_back')

            # if BVERSION < 4.2:
            #     row = material.row(align=True)
            #     row.prop(operator, 'shadow_method', expand=True)
            # material.prop(operator, 'use_backface_culling')
            # material.prop(operator, 'overwrite_material')

            # texture = layout.box()
            # texture.label(text='Texture Settings', icon='TEXTURE')
            # row = material.row(align=True)
            # row.prop(operator, 'interpolation', expand=True)
            # row = material.row(align=True)
            # row.prop(operator, 'extension', expand=True)
            # row = texture.row(align=True)
            # row.prop(operator, 'use_transparency')
            # if operator.use_transparency:
            #     row.prop(operator, 'alpha_mode', text='')
            # texture.prop(operator, 'use_auto_refresh')


            # position = layout.box()
            # position.label(text='Position', icon='SNAP_GRID')
            # position.prop(operator, 'offset')
            # col = position.column(align=True)
            # col.enabled = operator.offset
            # row = col.row(align=True)
            # row.prop(operator, 'offset_axis', expand=True)
            # col.prop(operator, 'offset_amount')
            # row = material.row(align=True)
            # row.prop(operator, 'size_mode', expand=True)
            # position.prop(operator, 'height')
            # position.prop(operator, 'align_axis')
            # position.prop(operator, 'align_track')
        
        elif module_name == 'data':
            options = layout.box()
            options.label(text='Options', icon='OPTIONS')

            options.prop(operator, 'relative_path')
            options.prop(operator, 'use_sequence_detection')
            options.prop(operator, 'use_udim_detecting')
        
        elif module_name in ['ref', 'background', 'empty']:
            options = layout.box()
            options.label(text='Options', icon='OPTIONS')

            if BVERSION >= 4.2:
                options.prop(operator, 'align')
                options.prop(operator, 'background')
            else:
                options.prop(operator, 'view_align')
            