from . import draw_panel, BVERSION, draw_version_warning

class IMPORT_SCENE_X3DSettings():
    @draw_version_warning
    def draw(self, operator, module_name,  layout):
        layout.use_property_split = True
        layout.use_property_decorate = False  # No animation.

        if BVERSION >= 4.2:

            header, panel = layout.panel(idname='X3DSettings_Transform')
            header.label(text='Transform', icon='OBJECT_DATA')

            if panel:
                panel.prop(operator, 'file_unit')
                sub = panel.column()
                sub.enabled = operator.file_unit == 'CUSTOM'
                sub.prop(operator, 'global_scale')
                if operator.file_unit == 'M':
                    operator.global_scale = 1.0
                elif operator.file_unit == 'DM':
                    operator.global_scale = 0.1
                elif operator.file_unit == 'CM':
                    operator.global_scale = 0.01
                elif operator.file_unit == 'MM':
                    operator.global_scale = 0.001
                elif operator.file_unit == 'IN':
                    operator.global_scale = 0.0254

                op = [  [operator, 'axis_forward'],
                        [operator, 'axis_up']]

                draw_panel(layout, op, 'X3DSettings_Transform', 'Transform', icon='OBJECT_DATA', panel=panel, header=header)

            op = [ [operator, 'solidify_value']]

            draw_panel(layout, op, 'X3DSettings_Mesh', 'Solidify', icon='MOD_SOLIDIFY', set_header_boolean=True, header_bool=[operator, 'solidify'])

        elif BVERSION >= 3.3:
            op = [  [operator, 'axis_forward'],
                [operator, 'axis_up']]

            draw_panel(layout, op, 'X3DSettings_Transform', 'Transform', icon='OBJECT_DATA')

