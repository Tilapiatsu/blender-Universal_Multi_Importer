import bpy


class PG_UMIColors(bpy.types.PropertyGroup):
    info_color: bpy.props.FloatVectorProperty(name="Info Color", subtype="COLOR_GAMMA", default=[0.62, 0.86, 0.92])
    success_color: bpy.props.FloatVectorProperty(name="Success Color", subtype="COLOR_GAMMA", default=[0.1, 1.0, 0.1])
    cancelled_color: bpy.props.FloatVectorProperty(
        name="Cancelled Color", subtype="COLOR_GAMMA", default=[1.0, 0.4, 0.1]
    )
    warning_color: bpy.props.FloatVectorProperty(name="Warning Color", subtype="COLOR_GAMMA", default=[1.0, 0.4, 0.1])
    error_color: bpy.props.FloatVectorProperty(name="Error Color", subtype="COLOR_GAMMA", default=[1.0, 0.1, 0.1])
    command_color: bpy.props.FloatVectorProperty(
        name="Command Color", subtype="COLOR_GAMMA", default=[0.95, 0.91, 0.10]
    )
    command_warning_color: bpy.props.FloatVectorProperty(
        name="Command Warning Color", subtype="COLOR_GAMMA", default=[0.95, 0.61, 0.10]
    )
    import_color: bpy.props.FloatVectorProperty(name="Import Color", subtype="COLOR_GAMMA", default=[0.13, 0.69, 0.72])


classes = (PG_UMIColors,)


def register():
    from bpy.utils import register_class

    for cls in classes:
        register_class(cls)


def unregister():
    from bpy.utils import unregister_class

    for cls in reversed(classes):
        unregister_class(cls)
