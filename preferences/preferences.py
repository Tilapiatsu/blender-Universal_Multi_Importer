import bpy
from .. import ADDON_PACKAGE


def get_prefs():
    return bpy.context.preferences.addons[ADDON_PACKAGE].preferences

class Preferences(bpy.types.AddonPreferences):
    bl_idname = ADDON_PACKAGE

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


classes = (Preferences,)

def register():
	from bpy.utils import register_class
	for cls in classes:
		register_class(cls)

def unregister():
	from bpy.utils import unregister_class
	for cls in reversed(classes):
		unregister_class(cls)

if __name__ == "__main__":
	register()
