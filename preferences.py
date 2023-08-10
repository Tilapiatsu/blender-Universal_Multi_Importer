import bpy
import os


def get_prefs():
    return bpy.context.preferences.addons['universal_multi_importer'].preferences

class UMI_Preferences(bpy.types.AddonPreferences):
    bl_idname = __package__

    auto_hide_text_when_finished : bpy.props.BoolProperty(name="Auto Hide Text When Finished", default=False)
    wait_before_hiding : bpy.props.FloatProperty(name="Wait Before Hiding (s)", default=5.0)

    def draw(self, context):
        layout=self.layout

        column = layout.column(align=True)
        box = column.box()

        box.prop(self, 'auto_hide_text_when_finished')
        if self.auto_hide_text_when_finished:
            box.prop(self, 'wait_before_hiding')




