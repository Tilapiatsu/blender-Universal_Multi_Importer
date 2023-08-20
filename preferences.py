import bpy
import os


def get_prefs():
    return bpy.context.preferences.addons['universal_multi_importer'].preferences

class UMI_Preferences(bpy.types.AddonPreferences):
    bl_idname = __package__

    show_log_on_3d_view : bpy.props.BoolProperty(name="Show Log on 3D View", default=True)
    auto_hide_text_when_finished : bpy.props.BoolProperty(name="Auto Hide Text When Finished", default=False)
    wait_before_hiding : bpy.props.FloatProperty(name="Wait Before Hiding (s)", default=5.0)
    force_refresh_viewport_after_each_import : bpy.props.BoolProperty(name="Force Refresh Viewport After Each Imported Files", default=False)

    def draw(self, context):
        layout=self.layout

        column = layout.column(align=True)
        box = column.box()
        box.prop(self, 'show_log_on_3d_view')
        if self.show_log_on_3d_view:
            box.prop(self, 'auto_hide_text_when_finished')
            if self.auto_hide_text_when_finished:
                box.prop(self, 'wait_before_hiding')
        box.prop(self, 'force_refresh_viewport_after_each_import')



