from . import draw_panel, draw_version_warning

class IMPORT_SCENE_XYZSettings():
    @draw_version_warning
    def draw(self, operator, module_name, layout):
        layout.use_property_split = True
        layout.use_property_decorate = False  # No animation.

        op = [[operator, 'use_camera'],
              [operator, 'use_lamp'],
              [operator, 'use_center'],
              [operator, 'use_center_all']]

        draw_panel(layout, op, 'XYZSettings_General', 'General', icon='OPTIONS')

        op = [[operator, 'ball']]

        header, panel = draw_panel(layout, op, 'XYZSettings_BallsAtoms', 'Balls / Atoms', icon='NODE_MATERIAL')

        if panel:
            sub = panel.column()
            sub.enabled = operator.ball == '1'

            sub.prop(operator, 'mesh_azimuth')
            sub.prop(operator, 'mesh_zenith')

        op = [[operator, 'scale_ballradius'],
              [operator, 'scale_distances'],
              [operator, 'atomradius']]

        draw_panel(layout, op, 'XYZSettings_BallsAtoms', 'Balls / Atoms', icon='NODE_MATERIAL', panel=panel, header=header)

        op = [[operator, 'skip_frames', 'Skip Frames'],
              [operator, 'images_per_key', 'Frames/key']]

        draw_panel(layout, op, 'XYZSettings_Frames', 'Frames', icon='SHADING_BBOX', set_header_boolean=True, header_bool=[operator, 'use_frames'])