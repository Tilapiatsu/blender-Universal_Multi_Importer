import bpy
import re
from pathlib import Path
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
    import_mode : bpy.props.EnumProperty(name="Import Mode", default="SINGLE", items=[  ('SINGLE', 'Single File', ''),
                                                                                        ('SEQUENCE', 'Detect File Sequence', ''),])
    loop_sequence : bpy.props.BoolProperty(name="Loop Sequence", default=False)
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
        path = Path(self.filepath)
        file_name = path.stem
        obj = self.create_object(file_name)

        node_tree = None
        if self.node_tree_name in bpy.data.node_groups:
            node_tree = bpy.data.node_groups[self.node_tree_name]
        else:
            node_tree = self.create_geometry_node_tree()

        if node_tree is None:
            LOG.error(f'Geometry Node Import format : Node Tree Creation Failed')
            return {'ERROR'}

        if self.import_mode == 'SEQUENCE':
            self.filepath, file_range = self.detect_sequence(Path(self.filepath))

        self.create_geometry_node_modifier(obj, node_tree, self.filepath, file_range)

    def create_object(self, name:str) -> bpy.types.Object:
        mesh = bpy.data.meshes.new(name=name)
        obj = bpy.data.objects.new(name=name, object_data=mesh)
        bpy.context.collection.objects.link(obj)
        if bpy.context.mode == 'OBJECT':
            bpy.ops.object.select_all(action='DESELECT')
            bpy.context.view_layer.objects.active = obj
            bpy.data.objects[obj.name].select_set(True)
        return obj

    def get_file_sequence_range(self, filepath:Path, basename: str, ext:str) -> Vector:
        root = filepath.parent
        files = [x for x in root.glob(f'**/*{ext}') if x.is_file() and basename in str(x)]
        ids = []
        for f in files:
            pattern = re.compile(r'(\d+)(?!.*\d)')
            for match in pattern.finditer(str(f)):
                ids.append(int(match.group(1)))

        ids.sort()

        return Vector((ids[0], ids[-1], 0))

    def detect_sequence(self, filepath: Path) -> (str, Vector):
        pattern = re.compile(r'([\D]+)|([\d]+)')
        matches = {1:[], 2:[]}


        index = 0
        for match in pattern.finditer(str(filepath)):
            matches[match.lastindex] += [[index, match.group(match.lastindex)]]
            index += 1

        last_number = matches[2][-1][1]
        hash_number = ''
        for _ in range(len(last_number)):
            hash_number += '#'

        replacement_string = r'{:' + hash_number + r'}'

        matches[2][-1][1] = replacement_string

        # Recompose String
        sequence_path = ''
        index = 0
        for a in matches[1]:
            for n in matches[2]:
                if a[0] == index:
                    sequence_path += a[1]
                    index += 1
                    continue
                elif n[0] == index:
                    sequence_path += n[1]
                    index += 1
                    continue
                else:
                    continue
            if a[0] == index:
                    sequence_path += a[1]
                    index += 1
                    continue

        return sequence_path, self.get_file_sequence_range(filepath, basename= sequence_path.split(replacement_string)[0],  ext=matches[1][-1])

    def create_geometry_node_tree(self) -> bpy.types.NodeTree:
        node_tree = bpy.data.node_groups.new(name=self.node_tree_name, type='GeometryNodeTree')

        ###    Declare Input Sockets
        node_tree.interface.new_socket(name='File Path', in_out='INPUT', socket_type='NodeSocketString')
        p = node_tree.interface.new_panel(name='Use Sequence', description='Thread File inputs as sequence, The filepath need to contains {:####} to itentify the frame number. The number of # defines the number of digits in the frame number', default_closed=True)
        b = node_tree.interface.new_socket(name='Use Sequence', in_out='INPUT', socket_type='NodeSocketBool')

        pid = 0
        node_tree.interface.move_to_parent(b, p, pid)
        b.is_panel_toggle = True

        pid += 1
        b = node_tree.interface.new_socket(name='Loop', in_out='INPUT', socket_type='NodeSocketBool')
        node_tree.interface.move_to_parent(b, p, pid)

        pid += 1
        b = node_tree.interface.new_socket(name='Range', in_out='INPUT', socket_type='NodeSocketVector')
        b.dimensions = 2
        node_tree.interface.move_to_parent(b, p, pid)

        pp = node_tree.interface.new_panel(name='Debug FilePath', description='Display Filepath of the currently loaded file', default_closed=True)
        b = node_tree.interface.new_socket(name='Debug FilePath', in_out='INPUT', socket_type='NodeSocketBool')

        pid += 1
        node_tree.interface.move_to_parent(pp, p, pid)
        node_tree.interface.move_to_parent(b, pp, pid)
        b.is_panel_toggle = True

        pid += 1
        b = node_tree.interface.new_socket(name='Debug Position', in_out='INPUT', socket_type='NodeSocketVector')
        node_tree.interface.move_to_parent(b, pp, pid)

        ###    Declare Output Socket
        node_tree.interface.new_socket(name='Geometry', in_out='OUTPUT', socket_type='NodeSocketGeometry')

        ###   Create Clamping Nodes
        #   Create Nodes
        input_node_01 = node_tree.nodes.new(type='NodeGroupInput')
        separate_node_01 = node_tree.nodes.new(type='ShaderNodeSeparateXYZ')
        time_node_01 = node_tree.nodes.new(type='GeometryNodeInputSceneTime')
        clamp_node_01 = node_tree.nodes.new(type='ShaderNodeClamp')

        #   Store Initial position of node
        position = Vector((0, 0))

        #   Set Nodes Position
        input_node_01.location = position
        separate_node_01.location = input_node_01.location + GAP
        time_node_01.location = separate_node_01.location + Vector((0, 100))
        clamp_node_01.location = separate_node_01.location + Vector((200, 50))

        #   Link Nodes Together
        #   Create Claping Link
        node_tree.links.new(input_node_01.outputs[3], separate_node_01.inputs[0])
        node_tree.links.new(time_node_01.outputs[1], clamp_node_01.inputs[0])
        node_tree.links.new(separate_node_01.outputs[0], clamp_node_01.inputs[1])
        node_tree.links.new(separate_node_01.outputs[1], clamp_node_01.inputs[2])

        ###   Create Looping Nodes
        #   Create Nodes
        input_node_01 = node_tree.nodes.new(type='NodeGroupInput')
        separate_node_01 = node_tree.nodes.new(type='ShaderNodeSeparateXYZ')
        time_node_01 = node_tree.nodes.new(type='GeometryNodeInputSceneTime')
        modulo_node_01 = node_tree.nodes.new(type='ShaderNodeMath')
        modulo_node_01.operation = 'FLOORED_MODULO'
        add_node_01 = node_tree.nodes.new(type='ShaderNodeMath')
        add_node_01.operation = 'ADD'

        #   Store Initial position of node
        position = input_node_01.location + Vector((0, -300))

        #   Set Nodes Position
        input_node_01.location = position
        separate_node_01.location = input_node_01.location + GAP
        time_node_01.location = separate_node_01.location + Vector((0, 100))
        modulo_node_01.location = separate_node_01.location + Vector((200, 50))
        add_node_01.location = modulo_node_01.location + GAP

        #   Link Nodes Together
        node_tree.links.new(input_node_01.outputs[3], separate_node_01.inputs[0])
        node_tree.links.new(time_node_01.outputs[1], modulo_node_01.inputs[0])
        node_tree.links.new(separate_node_01.outputs[1], modulo_node_01.inputs[1])
        node_tree.links.new(modulo_node_01.outputs[0], add_node_01.inputs[0])
        node_tree.links.new(separate_node_01.outputs[0], add_node_01.inputs[1])

        ###   Switch Loop And Clamp
        #   Create Nodes
        input_node_01 = node_tree.nodes.new(type='NodeGroupInput')
        switch_node_01 = node_tree.nodes.new(type='GeometryNodeSwitch')
        switch_node_01.input_type = 'FLOAT'

        #   Store Initial position of node
        position = add_node_01.location + GAP

        #   Set Nodes Position
        input_node_01.location = position
        switch_node_01.location = input_node_01.location + GAP

        #   Link Nodes Together
        node_tree.links.new(input_node_01.outputs[2], switch_node_01.inputs[0])
        node_tree.links.new(clamp_node_01.outputs[0], switch_node_01.inputs[1])
        node_tree.links.new(add_node_01.outputs[0], switch_node_01.inputs[2])

        ###   Format String
        #   Create Nodes
        input_node_01 = node_tree.nodes.new(type='NodeGroupInput')
        format_string_node_01 = node_tree.nodes.new(type='FunctionNodeFormatString')
        format_string_node_01.format_items.new(socket_type='FLOAT', name='path')

        #   Store Initial position of node
        position = switch_node_01.location + GAP

        #   Set Nodes Position
        input_node_01.location = position
        format_string_node_01.location = input_node_01.location + GAP

        #   Link Nodes Together
        node_tree.links.new(input_node_01.outputs[0], format_string_node_01.inputs[0])
        node_tree.links.new(switch_node_01.outputs[0], format_string_node_01.inputs[1])

        ###   Use Sequence
        #   Create Nodes
        input_node_01 = node_tree.nodes.new(type='NodeGroupInput')
        switch_node_01 = node_tree.nodes.new(type='GeometryNodeSwitch')
        switch_node_01.input_type = 'STRING'

        #   Store Initial position of node
        position = format_string_node_01.location + GAP

        #   Set Nodes Position
        input_node_01.location = position
        switch_node_01.location = input_node_01.location + GAP

        #   Link Nodes Together
        node_tree.links.new(input_node_01.outputs[0], switch_node_01.inputs[1])
        node_tree.links.new(input_node_01.outputs[1], switch_node_01.inputs[0])
        node_tree.links.new(format_string_node_01.outputs[0], switch_node_01.inputs[2])

        ###   Debug FilePath
        #   Create Nodes
        input_node_01 = node_tree.nodes.new(type='NodeGroupInput')
        string_curve_node_01 = node_tree.nodes.new(type='GeometryNodeStringToCurves')
        fill_curve_node_01 = node_tree.nodes.new(type='GeometryNodeFillCurve')
        set_position_node_01 = node_tree.nodes.new(type='GeometryNodeSetPosition')

        #   Store Initial position of node
        position = switch_node_01.location + Vector((200, -300))

        #   Set Nodes Position
        string_curve_node_01.location = position
        fill_curve_node_01.location = string_curve_node_01.location + GAP
        input_node_01.location = fill_curve_node_01.location + Vector((0, -200))
        set_position_node_01.location = fill_curve_node_01.location + GAP

        #   Link Nodes Together
        node_tree.links.new(switch_node_01.outputs[0], string_curve_node_01.inputs[0])
        node_tree.links.new(string_curve_node_01.outputs[0], fill_curve_node_01.inputs[0])
        node_tree.links.new(fill_curve_node_01.outputs[0], set_position_node_01.inputs[0])
        node_tree.links.new(input_node_01.outputs[5], set_position_node_01.inputs[3])

        ###   Import Node
        #   Create Nodes
        import_node = node_tree.nodes.new(type=NODE_GROUP_GROUP_NAMES[self.import_module])
        join_geometry_node = node_tree.nodes.new(type='GeometryNodeJoinGeometry')

        #   Store Initial position of node
        position = switch_node_01.location + GAP

        #   Set Nodes Position
        import_node.location = position
        join_geometry_node.location = import_node.location + GAP * 3

        #   Link Nodes Together
        node_tree.links.new(switch_node_01.outputs[0], import_node.inputs[0])
        node_tree.links.new(import_node.outputs[0], join_geometry_node.inputs[0])
        node_tree.links.new(set_position_node_01.outputs[0], join_geometry_node.inputs[0])

        ###   Switch
        #   Create Nodes
        input_node_01 = node_tree.nodes.new(type='NodeGroupInput')
        boolean_math_node = node_tree.nodes.new(type='FunctionNodeBooleanMath')
        boolean_math_node.operation = 'AND'
        switch_node_01 = node_tree.nodes.new(type='GeometryNodeSwitch')
        switch_node_01.input_type = 'GEOMETRY'
        output_node = node_tree.nodes.new(type='NodeGroupOutput')

        #   Store Initial position of node
        position = join_geometry_node.location + Vector((200, 100))

        #   Set Nodes Position
        input_node_01.location = position
        boolean_math_node.location = input_node_01.location + GAP
        switch_node_01.location = boolean_math_node.location + GAP
        output_node.location = switch_node_01.location + GAP

        #   Link Nodes Together
        node_tree.links.new(import_node.outputs[0], switch_node_01.inputs[1])
        node_tree.links.new(join_geometry_node.outputs[0], switch_node_01.inputs[2])
        node_tree.links.new(input_node_01.outputs[1], boolean_math_node.inputs[1])
        node_tree.links.new(input_node_01.outputs[4], boolean_math_node.inputs[0])
        node_tree.links.new(boolean_math_node.outputs[0], switch_node_01.inputs[0])
        node_tree.links.new(switch_node_01.outputs[0], output_node.inputs[0])

        for n in node_tree.nodes:
            if n.type in ['GROUP_INPUT', 'GROUP_OUTPUT']:
                n.hide = True

        return node_tree

    def create_geometry_node_modifier(self, obj: bpy.types.Object, node_tree: bpy.types.NodeGroup, filepath: str, frame_range: Vector) -> bpy.types.Modifier:
        modifier = obj.modifiers.new(name='Import', type='NODES')

        modifier.node_group = node_tree

        modifier['Socket_0'] = filepath
        modifier['Socket_2'] = self.import_mode == "SEQUENCE"
        modifier['Socket_3'] = self.loop_sequence
        modifier['Socket_4'][0] = frame_range[0]
        modifier['Socket_4'][1] = frame_range[1]

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