from . import draw_panel

class IMPORT_SCENE_DXFSettings():
    def draw(self, operator, module_name, layout):
        layout.use_property_split = True
        layout.use_property_decorate = False  # No animation.

        op = [[operator, 'scene_options'], 
              [operator, 'collection_options']]
        
        draw_panel(layout, op, 'DXFSettings_Import', 'Import Options', icon='IMPORT')

        op = [[operator, 'block_options'], 
              [operator, 'do_bbox'], 
              [operator, 'merge']]
        
        _, panel = draw_panel(layout, op, 'DXFSettings_MergeOptions', 'Merge Options', icon='AUTOMERGE_ON')

        if panel:
            sub = panel.column()
            sub.enabled = operator.merge

            sub.prop(operator, 'merge_options')
            panel.prop(operator, 'merge_lines')

        op = [[operator, 'represent_thickness_and_width']]
        
        _, panel = draw_panel(layout, op, 'DXFSettings_Thickness', 'Line Thickness and Width', icon='MOD_OUTLINE')

        if panel:
            sub = panel.column()
            sub.enabled = not operator.represent_thickness_and_width

            sub.prop(operator, 'import_atts')

            if operator.represent_thickness_and_width:
                operator.import_atts = operator.merge
            else:
                if not operator.merge:
                    operator.import_atts = False

        op = [[operator, 'import_text'], 
              [operator, 'import_light'], 
              [operator, 'export_acis']]
        
        draw_panel(layout, op, 'DXFSettings_OptionalObjects', 'Optional Objects', icon='IMPORT')

        op = [[operator, 'outliner_groups'], 
              [operator, 'recenter']]
        
        draw_panel(layout, op, 'DXFSettings_ViewOptions', 'View Options', icon='RESTRICT_VIEW_OFF')

        op = [[operator, 'dxf_indi'], 
              [operator, 'dxf_scale']]
        
        _, panel = draw_panel(layout, op, 'DXFSettings_GeoReferencing', 'Geo Referencing', set_header_boolean=True, header_bool=[operator, 'use_georeferencing'])

        if panel:
            sub = panel.column()
            sub.enabled = operator.dxf_indi == 'SPHERICAL'
            
            sub.prop(operator, 'merc_scene_lat')
            sub.prop(operator, 'merc_scene_lon')

