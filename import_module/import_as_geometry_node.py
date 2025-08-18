import bpy
from os import path
from ..logger import LOG
from ..bversion import BVERSION
from mathutils import Vector


NODE_IMPORT_MODULES = [     ("OBJ", "GeometryNodeImportOBJ"),
                            ("CSV", "GeometryNodeImportCSV"),
                            ("STL", "GeometryNodeImportSTL"),
                            ("TXT", "GeometryNodeImportText"),
                            ("VDB", "GeometryNodeImportVDB"),
                            ("PLY", "GeometryNodeImportPLY"),]

NODE_IMPORT_MODULES_ITEMS = [(m[0], m[0].lower(), "") for m in NODE_IMPORT_MODULES]

NODE_GROUP_GROUP_NAMES = {m[0]:m[1] for m in NODE_IMPORT_MODULES}

GAP = Vector((200, 0))


class IMPORT_SCENE_OT_tila_import_as_geometry_node(bpy.types.Operator):
    bl_idname = "import_scene.tila_import_as_geometry_node"
    bl_label = "Import as geometry_node"
    bl_options = {'REGISTER', 'INTERNAL'}
    bl_description = 'Import file as geometry node'

    import_module : bpy.props.EnumProperty(name="Import Module", default="OBJ", items=NODE_IMPORT_MODULES_ITEMS)
    filepath : bpy.props.StringProperty(name="File Path", subtype='FILE_PATH', options={'HIDDEN'})

    @property
    def node_tree_name(self) -> str:
        return f'Import {self.import_module}'

    def execute(self, context):
        self.current_collection = context.collection
        self.import_started = False
        self.importing = False
        self.import_finished = False

        self.import_data()

        return {'FINISHED'}

    def import_data(self) -> None :
        file_name = path.basename(self.filepath)
        obj = self.create_object(file_name)

        node_tree = None
        if self.node_tree_name in bpy.data.node_groups:
            node_tree = bpy.data.node_groups[self.node_tree_name]
        else:
            node_tree = self.create_geometry_node_tree()

        if node_tree is None:
            LOG.error(f'Geometry Node Import format : Node Tree Creation Failed')
            return {'ERROR'}

        self.create_geometry_node_modifier(obj, node_tree, self.filepath)

    def create_object(self, name:str) -> bpy.types.Object:
        mesh = bpy.data.meshes.new(name=name)
        obj = bpy.data.objects.new(name=name, object_data=mesh)
        bpy.context.collection.objects.link(obj)
        bpy.data.objects[obj.name].select_set(True)
        return obj

    def create_geometry_node_tree(self) -> bpy.types.NodeTree:
        node_tree = bpy.data.node_groups.new(name=self.node_tree_name, type='GeometryNodeTree')

        input_node = node_tree.nodes.new(type='NodeGroupInput')
        import_node = node_tree.nodes.new(type=NODE_GROUP_GROUP_NAMES[self.import_module])
        output_node = node_tree.nodes.new(type='NodeGroupOutput')

        position = Vector((0, 0))

        input_node.location = position
        import_node.location = input_node.location + GAP
        output_node.location = import_node.location + GAP

        node_tree.interface.new_socket(name='File Path', in_out='INPUT', socket_type='NodeSocketString')
        node_tree.interface.new_socket(name='Geometry', in_out='OUTPUT', socket_type='NodeSocketGeometry')

        node_tree.links.new(input_node.outputs[0], import_node.inputs[0])
        node_tree.links.new(import_node.outputs[0], output_node.inputs[0])

        return node_tree

    def create_geometry_node_modifier(self, obj: bpy.types.Object, node_tree: bpy.types.NodeGroup, filepath: str) -> bpy.types.Modifier:
        modifier = obj.modifiers.new(name='Import', type='NODES')

        modifier.node_group = node_tree

        modifier['Socket_0'] = filepath

        return modifier

classes = (IMPORT_SCENE_OT_tila_import_as_geometry_node, )

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