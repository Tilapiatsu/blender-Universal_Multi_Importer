from . import draw_no_settings
from . import BVERSION
from . import draw_panel

class IMPORT_SCENE_IMAGESettings():
    def draw(self, operator, module_name, layout):
        layout.use_property_split = True
        layout.use_property_decorate = False  # No animation.

        if module_name == 'plane':
            if BVERSION >= 4.3:
                op =    [[operator, 'relative'],
                        [operator, 'force_reload'],
                        [operator, 'image_sequence']]
        
                draw_panel(layout, op, 'IMAGESettings_Options', 'Import Options', icon='IMPORT')

                op =    [[operator, 'shader'],
                        [operator, 'render_method'],
                        [operator, 'show_transparent_back'],
                        [operator, 'use_backface_culling'],
                        [operator, 'overwrite_material']]
        
                draw_panel(layout, op, 'IMAGESettings_MaterialSettings', 'Material Settings', icon='MATERIAL')

                op =    [[operator, 'interpolation'],
                        [operator, 'extension'],
                        [operator, 'use_transparency']]
        
                header, panel = draw_panel(layout, op, 'IMAGESettings_TextureSettings', 'Texture Settings', icon='TEXTURE')

                if panel:
                    col = panel.column(align=True)
                    col.enabled = operator.use_transparency
                    col.prop(operator, 'alpha_mode')

                op =    [[operator, 'use_auto_refresh']]
        
                draw_panel(layout, op, 'IMAGESettings_TextureSettings', 'Texture Settings', icon='TEXTURE', panel=panel, header=header)

            elif BVERSION >= 4.2:
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
                        [operator, 'use_transparency']]
        
                header, panel = draw_panel(layout, op, 'IMAGESettings_TextureSettings', 'Texture Settings', icon='TEXTURE')

                if panel:
                    col = panel.column(align=True)
                    col.enabled = operator.use_transparency
                    col.prop(operator, 'alpha_mode')

                op =    [[operator, 'use_auto_refresh']]
        
                draw_panel(layout, op, 'IMAGESettings_TextureSettings', 'Texture Settings', icon='TEXTURE', panel=panel, header=header)

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

            else:
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
        
        elif module_name == 'data':
            op =    [[operator, 'relative_path'],
                    [operator, 'use_sequence_detection'],
                    [operator, 'use_udim_detecting']]
        
            draw_panel(layout, op, 'IMAGESettings_Options', 'Import Options', icon='OPTIONS')

        
        elif module_name in ['ref', 'background', 'empty']:
            if BVERSION >= 4.2:
                op =    [[operator, 'align'],
                        [operator, 'background']]
            
                draw_panel(layout, op, 'IMAGESettings_Options', 'Options', icon='OPTIONS')
            else:
                op =    [[operator, 'view_align']]
            
                draw_panel(layout, op, 'IMAGESettings_Options', 'Options', icon='OPTIONS')
            