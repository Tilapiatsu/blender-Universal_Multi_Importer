import bpy
from ..logger import LOG
from .formats.properties import PG_UMISettings
from .. import ADDON_PACKAGE

def update_log_drawing(self, context):
	LOG.show_log = self.umi_settings.umi_global_import_settings.show_log_on_3d_view


class Preferences(bpy.types.AddonPreferences):
	bl_idname = ADDON_PACKAGE

	umi_settings : bpy.props.PointerProperty(type=PG_UMISettings)

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
