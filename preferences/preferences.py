import bpy
from ..logger import LOG
from .formats.properties import PG_UMISettings
from .properties.colors import PG_UMIColors
from .. import ADDON_PACKAGE

def update_log_drawing(self, context):
	LOG.show_log = self.umi_settings.umi_global_import_settings.show_log_on_3d_view


class Preferences(bpy.types.AddonPreferences):
	bl_idname = ADDON_PACKAGE

	umi_settings : bpy.props.PointerProperty(type = PG_UMISettings)

	umi_colors 	 : bpy.props.PointerProperty(type= PG_UMIColors)
	
	
	def draw(self, context):
		layout = self.layout
		layout.use_property_split = True
		layout.use_property_decorate = False

		column = layout.column(align=True)
		box = column.box()
		box.label(text='Theme', icon='IMAGE_BACKGROUND')
		box.prop(self.umi_colors, 'umi_info_color')
		box.prop(self.umi_colors, 'umi_success_color')
		box.prop(self.umi_colors, 'umi_cancelled_color')
		box.prop(self.umi_colors, 'umi_warning_color')
		box.prop(self.umi_colors, 'umi_error_color')
		box.prop(self.umi_colors, 'umi_command_color')
		box.prop(self.umi_colors, 'umi_import_color')


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
