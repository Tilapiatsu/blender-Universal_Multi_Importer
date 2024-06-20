from . import draw_no_settings
from ....blender_version import BVERSION

class IMPORT_SCENE_IMAGESettings():
    def draw(self, operator, module_name, layout):
        layout.use_property_split = True
        layout.use_property_decorate = False  # No animation.

        if module_name == 'plane':
            import_options = layout.box()
            import_options.label(text='Import Options', icon='IMPORT')
            import_options.prop(operator, 'relative')
            import_options.prop(operator, 'force_reload')
            import_options.prop(operator, 'image_sequence')

            if BVERSION >= 4.2:
                pass
            else:
                compositing = layout.box()
                compositing.label(text='Compositing Nodes', icon='NODE_COMPOSITING')
                compositing.prop(operator, 'compositing_nodes')

            material = layout.box()
            material.label(text='Material Settings', icon='MATERIAL')
            row = material.row(align=True)
            row.prop(operator, 'shader', expand=True)
            row = material.row(align=True)
            row.prop(operator, 'blend_method', expand=True)
            material.prop(operator, 'show_transparent_back')
            row = material.row(align=True)
            row.prop(operator, 'shadow_method', expand=True)
            material.prop(operator, 'use_backface_culling')
            material.prop(operator, 'overwrite_material')

            texture = layout.box()
            texture.label(text='Texture Settings', icon='TEXTURE')
            row = material.row(align=True)
            row.prop(operator, 'interpolation', expand=True)
            row = material.row(align=True)
            row.prop(operator, 'extension', expand=True)
            row = texture.row(align=True)
            row.prop(operator, 'use_transparency')
            if operator.use_transparency:
                row.prop(operator, 'alpha_mode', text='')
            texture.prop(operator, 'use_auto_refresh')


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
        
        elif module_name in ['ref', 'background']:
            options = layout.box()
            options.label(text='Options', icon='OPTIONS')

            if BVERSION >= 4.2:
                options.prop(operator, 'align')
            else:
                options.prop(operator, 'view_align')
            