from . import draw_panel, draw_version_warning

class IMPORT_SCENE_PDBSettings():
    @draw_version_warning
    def draw(self, operator, module_name, layout):
        layout.use_property_split = True
        layout.use_property_decorate = False  # No animation.

        op = [[operator, 'use_camera'],
              [operator, 'use_light'],
              [operator, 'use_center']]

        draw_panel(layout, op, 'PDBSettings_General', 'General', icon='OPTIONS')

        op = [[operator, 'ball']]

        header, panel = draw_panel(layout, op, 'PDBSettings_BallsAtoms', 'Balls / Atoms', icon='NODE_MATERIAL')

        if panel:
            sub = panel.column()
            sub.enabled = operator.ball == '1'

            sub.prop(operator, 'mesh_azimuth')
            sub.prop(operator, 'mesh_zenith')

        op = [[operator, 'scale_ballradius'],
              [operator, 'scale_distances'],
              [operator, 'atomradius']]

        draw_panel(layout, op, 'PDBSettings_BallsAtoms', 'Balls /  Atoms', icon='NODE_MATERIAL', panel=panel, header=header)

        op = [[operator, 'use_sticks_type']]

        _, panel = draw_panel(layout, op, 'PDBSettings_Frames', 'Frames', icon='SHADING_BBOX', set_header_boolean=True, header_bool=[operator, 'use_sticks'])

        if panel:
            if operator.use_sticks_type == '0' :
                panel.prop(operator, 'sticks_sectors')
                panel.prop(operator, 'sticks_radius')
                panel.prop(operator, 'sticks_unit_length')
                panel.prop(operator, 'use_sticks_color')
                panel.prop(operator, 'use_sticks_smooth')
                panel.prop(operator, 'use_sticks_bonds')

                sub = panel.column()
                sub.enabled = operator.use_sticks_bonds

                panel.prop(operator, 'sticks_dist')
            elif operator.use_sticks_type == '1':
                panel.prop(operator, 'sticks_radius')
                panel.prop(operator, 'sticks_subdiv_view')
                panel.prop(operator, 'sticks_subdiv_render')
                panel.prop(operator, 'use_sticks_bonds')
            elif operator.use_sticks_type == '2':
                panel.prop(operator, 'sticks_sectors')
                panel.prop(operator, 'sticks_radius')
                panel.prop(operator, 'use_sticks_smooth')
                panel.prop(operator, 'use_sticks_bonds')

                sub = panel.column()
                sub.enabled = operator.use_sticks_bonds

                panel.prop(operator, 'sticks_dist')
                panel.prop(operator, 'use_sticks_one_object')

