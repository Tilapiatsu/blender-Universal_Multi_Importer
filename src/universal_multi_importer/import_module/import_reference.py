import bpy


class IMPORT_SCENE_OT_tila_import_reference(bpy.types.Operator):
    bl_idname = "import_scene.tila_import_reference"
    bl_label = "Import as reference"
    bl_options = {"REGISTER", "INTERNAL"}
    bl_description = "Import file as geometry node"

    filepath: bpy.props.StringProperty(name="File Path", subtype="FILE_PATH", options={"HIDDEN"})
    location: bpy.props.FloatVectorProperty(name="Location", subtype="XYZ", unit="LENGTH")
    rotation: bpy.props.FloatVectorProperty(name="Rotation", subtype="EULER")
    align: bpy.props.EnumProperty(name="Align", items=(("WORLD", "World", ""), ("CURSOR", "3D Cursor", "")))
    background: bpy.props.BoolProperty(name="Put in Background", default=False)

    def execute(self, context):
        empty = bpy.data.objects.new(name="ImageEmpty", object_data=None)
        bpy.context.collection.objects.link(empty)

        # Set empty properties
        empty.empty_display_type = "IMAGE"
        empty.data = bpy.data.images.load(self.filepath)
        match self.align:
            case "CURSOR":
                empty.location = context.scene.cursor.location + self.location
                empty.rotation_euler = context.scene.cursor.rotation_euler
                empty.rotation_euler[0] += self.rotation[0]
                empty.rotation_euler[1] += self.rotation[1]
                empty.rotation_euler[2] += self.rotation[2]
            case "WORLD":
                empty.rotation_euler = self.rotation
                empty.location = self.location
        empty.empty_display_size = 5  # data api default is 1 whereas operator is 5
        if self.background:
            empty.empty_image_depth = "BACK"  # data api equivalent of 'background=True'

        # Update the UI!!!!
        bpy.context.view_layer.update()
        return {"FINISHED"}


classes = (IMPORT_SCENE_OT_tila_import_reference,)


def register():

    from bpy.utils import register_class

    for cls in classes:
        register_class(cls)


def unregister():
    from bpy.utils import unregister_class

    for cls in reversed(classes):
        unregister_class(cls)
