import bpy

class PG_UMIColors(bpy.types.PropertyGroup):
	umi_info_color      : bpy.props.FloatVectorProperty(name="Info Color",      subtype='COLOR_GAMMA', default=[0.1,  0.5,  0.6])
	umi_success_color   : bpy.props.FloatVectorProperty(name="Success Color",   subtype='COLOR_GAMMA', default=[0.1,  1.0,  0.1])
	umi_cancelled_color : bpy.props.FloatVectorProperty(name="Cancelled Color", subtype='COLOR_GAMMA', default=[1.0,  0.4,  0.1])
	umi_warning_color   : bpy.props.FloatVectorProperty(name="Warning Color",   subtype='COLOR_GAMMA', default=[1.0,  0.4,  0.1])
	umi_error_color     : bpy.props.FloatVectorProperty(name="Error Color",     subtype='COLOR_GAMMA', default=[1.0,  0.1,  0.1])
	umi_command_color   : bpy.props.FloatVectorProperty(name="Command Color",   subtype='COLOR_GAMMA', default=[0.95, 0.91, 0.10])
	umi_import_color    : bpy.props.FloatVectorProperty(name="Import Color",    subtype='COLOR_GAMMA', default=[0.13, 0.69, 0.72])

classes = (PG_UMIColors, )

def register():
	from bpy.utils import register_class
	for cls in classes:
		register_class(cls)

def unregister():
	from bpy.utils import unregister_class
	for cls in reversed(classes):
		unregister_class(cls)