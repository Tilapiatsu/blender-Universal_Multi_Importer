from . import BVERSION

def axis():
    return [
        ("X", "X", "X"),
        ("Y", "Y", "Y"),
        ("Z", "Z", "Z"),
        ("-X", "-X", "-X"),
        ("-Y", "-Y", "-Y"),
        ("-Z", "-Z", "-Z")
    ]


class FormatDefinition():
    '''
    Stores all information to support import formats
    '''

    fbx = {'name' : 'fbx',
            'ext' : ['.fbx'],
            'operator' : {'default':{'command': 'bpy.ops.import_scene.fbx', 'module' : None, 'addon_name' : 'io_scene_fbx', 'pkg_id' : None, 'pkg_url':None, 'import_settings':None, 'supported_version':'5.12.5'}},
            'ignore': ['files', 'directory'],
            'generate_filter_glob':False}

    gltf = {'name' : 'gltf',
            'ext' : ['.glb', '.gltf'],
            'operator' : {'default':{'command':'bpy.ops.import_scene.gltf','module' : None, 'addon_name' : 'io_scene_gltf2', 'pkg_id' : None, 'pkg_url':None, 'import_settings':None, 'supported_version':'4.3.47'}},
            'ignore': ['files', 'directory'],
            'generate_filter_glob':False}

    abc = {'name' : 'abc',
            'ext' : ['.abc'],
            'operator' : {'default':{'command':'bpy.ops.wm.alembic_import', 'module':None, 'addon_name' : None, 'pkg_id' : None, 'import_settings':None, 'pkg_url':None, 'supported_version':'0.0.0'}},
            'ignore': ['files', 'directory'],
            'generate_filter_glob':False
            }

    dae = {'name' : 'dae',
            'ext' : ['.dae'],
            'operator' : {'default':{'command':'bpy.ops.wm.collada_import', 'module':None, 'addon_name' : None, 'pkg_id' : None, 'import_settings':None, 'pkg_url':None, 'supported_version':'0.0.0'}},
            'ignore': ['files', 'name', 'directory'],
            'generate_filter_glob':False
            }

    blend = {'name' : 'blend',
            'ext' : ['.blend'],
            'operator' : {'default':{'command':'bpy.ops.import_scene.tila_import_blend', 'module':None, 'addon_name' : None, 'pkg_id' : None, 'pkg_url':None, 'import_settings':None, 'supported_version':'0.0.0'}},
            'ignore': ['files', 'directory'],
            'generate_filter_glob':False
            }

    bvh = {'name' : 'bvh',
            'ext' : ['.bvh'],
            'operator' : {'default':{'command':'bpy.ops.import_anim.bvh', 'module':None, 'addon_name' : 'io_anim_bvh', 'pkg_id' : None, 'pkg_url':None, 'import_settings':None, 'supported_version':'1.0.1'}},
            'ignore': ['files', 'directory'],
            'generate_filter_glob':True
            }

    obj = {'name' : 'obj',
            'ext' : ['.obj'],
            'operator' : {'default':{'command':'bpy.ops.wm.obj_import', 'module':None, 'addon_name' : None, 'pkg_id' : None, 'import_settings':None, 'pkg_url':None, 'supported_version':'0.0.0'}},
            'ignore': ['files', 'directory'],
            'generate_filter_glob':False
            }

    ply = {'name' : 'ply',
            'ext' : ['.ply'],
            'operator' : {'default':{'command':'bpy.ops.wm.ply_import', 'module':None, 'addon_name' : None, 'pkg_id' : None, 'import_settings':None, 'pkg_url':None, 'supported_version':'0.0.0'}},
            'ignore': ['files', 'directory'],
            'generate_filter_glob':False}

    svg = {'name' : 'svg',
        'ext' : ['.svg'],
        'operator' : {  'default':{'command':'bpy.ops.import_curve.svg', 'module':None, 'addon_name' : None, 'pkg_id' : None, 'import_settings':None, 'pkg_url':None, 'supported_version':'0.0.0'}},
        'ignore': ['files', 'directory'],
        'generate_filter_glob':False}

    usd = {'name' : 'usd',
        'ext' : ['.usd', '.usda', '.usdc', '.usdz'],
        'operator' : {'default':{'command':'bpy.ops.wm.usd_import', 'module':None, 'addon_name' : None, 'pkg_id' : None, 'import_settings':None, 'pkg_url':None, 'supported_version':'0.0.0'}},
        'ignore': ['files', 'directory'],
        'generate_filter_glob':False}

    max = {'name' : 'max',
        'ext' : ['.max'],
        'operator' : {'default':{'command':'bpy.ops.import_scene.max', 'module':None, 'addon_name' : 'bl_ext.blender_org.io_scene_max', 'pkg_id' : 'io_scene_max', 'pkg_url': 'https://extensions.blender.org/add-ons/io-scene-max/', 'supported_version':'1.5.5', 'import_settings':
                                            [['Include',
                                            {"use_image_search": {'type':'bpy.props.BoolProperty', 'name':'"Image Search"', 'default':True},
                                            "object_filter": {'type':'bpy.props.EnumProperty', 'name':'"Object Filter"', 'default':{'MATERIAL', 'UV', 'EMPTY', 'ARMATURE'},
                                                               'enum_items':(('MATERIAL', "Material".rjust(12), "", 'MATERIAL_DATA', 0x1),
                                                                        ('UV', "UV Maps".rjust(11), "", 'UV_DATA', 0x2),
                                                                        ('EMPTY', "Empty".rjust(11), "", 'EMPTY_AXIS', 0x4),
                                                                        ('ARMATURE', "Armature".rjust(11), "", 'ARMATURE_DATA', 0x8),),
                                                                        'options':{'ENUM_FLAG'},},
                                            "use_collection": {'type':'bpy.props.BoolProperty', 'name':'"Collection"', 'default':False}}],
                                            ['Transform',
                                            {"scale_objects" : {'type':'bpy.props.FloatProperty', 'name':'"Scale"', 'default':1.0},
                                            "use_apply_matrix" : {'type':'bpy.props.BoolProperty', 'name':'"Apply Matrix"', 'default':True},
                                            "axis_forward": {'type':'bpy.props.EnumProperty', 'name':'"Forward"', 'default':'"Y"', 'enum_items':axis()},
                                            "axis_up": {'type':'bpy.props.EnumProperty', 'name':'"Up"', 'default':'"Z"', 'enum_items':axis()}}]]}},
        'ignore': ['files', 'directory'],
        'generate_filter_glob':True}

    pes = {'name' : 'pes',
        'ext' : ['.pes', '.dst', '.exp', '.jef', '.pec', '.jpx', '.phc', '.vp3', '.10o', '.bro', '.dat', '.dsb', '.dsz', '.emd', '.exy', '.fxy', '.hus', '.inb', '.new', '.pcd', '.pcm', '.pcq', '.pcs', '.phb', '.sew', '.shv', '.stc', '.stx', '.tap', '.tbf', '.xxx', '.zhs', '.zxy', '.gcode'], # '.100', '.mit', '.ksm', '.u01', '.gt',
        'operator' : {'default':{'command':'bpy.ops.import_scene.embroidery', 'module':None, 'addon_name' : 'bl_ext.blender_org.embroidery_importer', 'pkg_id' : 'embroidery_importer', 'pkg_url': 'https://extensions.blender.org/add-ons/embroidery-importer/', 'supported_version':'0.9.4', 'import_settings':
                                            [['Import',
                                            {"show_jump_wires": {'type':'bpy.props.BoolProperty', 'name':'"Import Jump Wires"', 'default':True},
                                            "do_create_material": {'type':'bpy.props.BoolProperty', 'name':'"Create Matertial"', 'default':True},
                                            "create_collection": {'type':'bpy.props.BoolProperty', 'name':'"Create a Collection"', 'default':False}}],
                                            ['Thickness',
                                            {"line_depth" : {'type':'bpy.props.EnumProperty', 'name':'"Thickness Type"', 'default':'"GEOMETRY_NODES"', 'enum_items':
                                                             [
                                                            ("NO_THICKNESS", "No thickness (curve only)", "Only curves, no thickness"),
                                                            (
                                                                "GEOMETRY_NODES",
                                                                "Using geometry nodes",
                                                                "Create a geometry node setup to add thickness. Most versatile.",
                                                            ),
                                                            ("BEVEL", "Using bevel", "Adds thickness through the bevel property")]
                                                            },
                                            "thread_thickness" : {'type':'bpy.props.FloatProperty', 'name':'"Thread Thickness"', 'default':0.2}}]]}},
        'ignore': ['files', 'directory'],
        'generate_filter_glob':True}

    x3d = {'name' : 'x3d',
        'ext' : ['.x3d', '.wrl'],
        'operator' : {'default':{'command':'bpy.ops.import_scene.x3d','module' : None, 'addon_name' : 'bl_ext.blender_org.web3d_x3d_vrml2_format', 'pkg_id' : 'web3d_x3d_vrml2_format', 'pkg_url':'https://extensions.blender.org/add-ons/web3d-x3d-vrml2-format/', 'import_settings':None, 'supported_version':'2.4.3'}},
        'ignore': ['files', 'directory'],
        'generate_filter_glob':True}

    dxf = {'name' : 'dxf',
        'ext' : ['.dxf'],
        'operator' : {'default':{'command':'bpy.ops.import_scene.dxf','module' : None, 'addon_name' : 'bl_ext.blender_org.import_autocad_dxf_format_dxf', 'pkg_id' : 'import_autocad_dxf_format_dxf', 'pkg_url':'https://extensions.blender.org/add-ons/import-autocad-dxf-format-dxf/', 'import_settings':None, 'supported_version':'0.9.10'}},
        'ignore': ['files', 'directory'],
        'generate_filter_glob':True}

    pdb = {'name' : 'pdb',
    'ext' : ['.pdb'],
    'operator' : {'default':{'command':'bpy.ops.import_mesh.pdb','module' : None, 'addon_name' : 'bl_ext.blender_org.atomic_blender_pdb_xyz', 'pkg_id' : 'atomic_blender_pdb_xyz', 'pkg_url':'https://extensions.blender.org/add-ons/atomic-blender-pdb-xyz/', 'import_settings':None, 'supported_version':'1.9.1'}},
    'ignore': ['files', 'directory'],
    'generate_filter_glob':True}

    xyz = {'name' : 'xyz',
        'ext' : ['.xyz'],
        'operator' : {'default':{'command':'bpy.ops.import_mesh.xyz','module' : None, 'addon_name' : 'bl_ext.blender_org.atomic_blender_pdb_xyz', 'pkg_id' : 'atomic_blender_pdb_xyz', 'pkg_url':'https://extensions.blender.org/add-ons/atomic-blender-pdb-xyz/', 'import_settings': None, 'supported_version':'1.9.1'}},
        'ignore': ['files', 'directory'],
        'generate_filter_glob':True}

    max3ds = {'name' : 'max3ds',
        'ext' : ['.3ds'],
        'operator' : {'default':{'command':'bpy.ops.import_scene.max3ds','module' : None, 'addon_name' : 'bl_ext.blender_org.autodesk_3ds_format', 'pkg_id' : 'autodesk_3ds_format', 'pkg_url':'https://extensions.blender.org/add-ons/autodesk-3ds-format/', 'supported_version':'2.7.5', 'import_settings':
                                 [['Include',
                                            {"use_image_search": {'type':'bpy.props.BoolProperty', 'name':'"Image Search"', 'default':True},
                                            "object_filter": {'type':'bpy.props.EnumProperty', 'name':'"Object Filter"', 'default':{'WORLD', 'MESH', 'LIGHT', 'CAMERA', 'EMPTY'},
                                                               'enum_items':(('WORLD', "World".rjust(11), "", 'WORLD_DATA', 0x1),
                                                                            ('MESH', "Mesh".rjust(11), "", 'MESH_DATA', 0x2),
                                                                            ('LIGHT', "Light".rjust(12), "", 'LIGHT_DATA', 0x4),
                                                                            ('CAMERA', "Camera".rjust(11), "", 'CAMERA_DATA', 0x8),
                                                                            ('EMPTY', "Empty".rjust(11), "", 'EMPTY_AXIS', 0x10),),
                                                                        'options':{'ENUM_FLAG'},},
                                            "use_keyframes":{'type':'bpy.props.BoolProperty', 'name':'"Collection"', 'default':True},
                                            "use_collection": {'type':'bpy.props.BoolProperty', 'name':'"Collection"', 'default':False},
                                            "use_cursor":{'type':'bpy.props.BoolProperty', 'name':'"Collection"', 'default':False}}],
                                            ['Transform',
                                            {"constrain_size" : {'type':'bpy.props.FloatProperty', 'name':'"Constrain Size"', 'default':1.0},
                                            "use_scene_unit" : {'type':'bpy.props.BoolProperty', 'name':'"Scene Unit"', 'default':False},
                                            "use_apply_transform" : {'type':'bpy.props.BoolProperty', 'name':'"Apply Transform"', 'default':True},
                                            "axis_forward": {'type':'bpy.props.EnumProperty', 'name':'"Forward"', 'default':'"Y"', 'enum_items':axis()},
                                            "axis_up": {'type':'bpy.props.EnumProperty', 'name':'"Up"', 'default':'"Z"', 'enum_items':axis()}}]]}},
        'ignore': ['files', 'directory'],
        'generate_filter_glob':True}

    if BVERSION >= 4.3:
        image = {'name' : 'image',
            'ext' : [	'.jpg', '.jpeg', '.gif', '.png', '.tif', '.tiff', '.bmp', '.cin', '.dpx', '.jp2', '.j2c', '.sig', '.rgb', '.bw',
                        '.hdr', '.exr',
                        '.mov', '.mp4', '.mkv', '.mpg', '.mpeg', '.dvd', '.vob', '.avi', '.dv', '.flv', '.webm'],
            'operator' : {  'plane':{'command':'bpy.ops.image.import_as_mesh_planes', 'module':None, 'addon_name' : None, 'pkg_id' : None, 'pkg_url':None, 'import_settings':None, 'supported_version':'0.0.0'},
                            'data':{'command':'bpy.ops.image.open', 'module':None, 'addon_name' : None, 'pkg_id' : None, 'import_settings':None, 'pkg_url':None, 'supported_version':'0.0.0'},
                            'empty':{'command':'bpy.ops.object.empty_image_add', 'module':None, 'addon_name' : None, 'pkg_id' : None , 'import_settings':None, 'pkg_url':None, 'supported_version':'0.0.0'}
                        },
            'ignore': ['files', 'directory', 'filepath'],
            'generate_filter_glob':False
            }

        stl = {'name' : 'stl',
                'ext' : ['.stl'],
                'operator' : {  'default':{'command':'bpy.ops.wm.stl_import', 'module':None, 'addon_name' : None, 'pkg_id' : None, 'import_settings':None, 'pkg_url':None, 'supported_version':'0.0.0'}},
                'ignore': ['files', 'directory'],
                'generate_filter_glob':False}

    elif BVERSION >= 4.2:
        image = {'name' : 'image',
            'ext' : [	'.jpg', '.jpeg', '.gif', '.png', '.tif', '.tiff', '.bmp', '.cin', '.dpx', '.jp2', '.j2c', '.sig', '.rgb', '.bw',
                        '.hdr', '.exr',
                         '.mov', '.mp4', '.mkv', '.mpg', '.mpeg', '.dvd', '.vob', '.avi', '.dv', '.flv', '.webm'],
            'operator' : {  'plane':{'command':'bpy.ops.image.import_as_mesh_planes', 'module':None, 'addon_name' : None, 'pkg_id' : None, 'pkg_url':None, 'import_settings':None, 'supported_version':'0.0.0'},
                            'data':{'command':'bpy.ops.image.open', 'module':None, 'addon_name' : None, 'pkg_id' : None, 'import_settings':None, 'pkg_url':None, 'supported_version':'0.0.0'},
                            'empty':{'command':'bpy.ops.object.empty_image_add', 'module':None, 'addon_name' : None, 'pkg_id' : None, 'import_settings':None, 'pkg_url':None, 'supported_version':'0.0.0'}
                        },
            'ignore': ['files', 'directory', 'filepath'],
            'generate_filter_glob':False
            }

        stl = {'name' : 'stl',
                'ext' : ['.stl'],
                'operator' : {  'default':{'command':'bpy.ops.wm.stl_import', 'module':None, 'addon_name' : None, 'pkg_id' : None, 'import_settings':None, 'pkg_url':None, 'supported_version':'0.0.0'}},
                'ignore': ['files', 'directory'],
                'generate_filter_glob':False}

        svg = {'name' : 'svg',
            'ext' : ['.svg'],
            'operator' : {  'default':{'command':'bpy.ops.import_curve.svg', 'module':None, 'addon_name' : 'io_curve_svg', 'pkg_id' : None, 'import_settings':None, 'pkg_url':None, 'supported_version':'0.0.0'}},
            'ignore': ['files', 'directory'],
            'generate_filter_glob':False}

    # 4.1 and below
    else:
        image = {'name' : 'image',
        'ext' : [	'.jpg', '.jpeg', '.gif', '.png', '.tif', '.tiff', '.bmp', '.cin', '.dpx', '.jp2', '.j2c', '.sig', '.rgb', '.bw',
                    '.hdr', '.exr',
                    '.mov', '.mp4', '.mkv', '.mpg', '.mpeg', '.dvd', '.vob', '.avi', '.dv', '.flv', '.webm'],
        'operator' : {  'plane':{'command':'bpy.ops.import_image.to_plane', 'module':None, 'addon_name' : 'io_import_images_as_planes', 'pkg_id' : None, 'pkg_url':None, 'import_settings':None, 'supported_version':'0.0.0'},
                        'data':{'command':'bpy.ops.image.open', 'module':None, 'addon_name' : None, 'pkg_id' : None , 'import_settings':None, 'pkg_url':None, 'supported_version':'0.0.0'},
                        'ref':{'command':'bpy.ops.object.load_reference_image', 'module':None, 'addon_name' : None, 'pkg_id' : None, 'pkg_url':None, 'import_settings':None, 'supported_version':'0.0.0'},
                        'background':{'command':'bpy.ops.object.load_background_image', 'module':None, 'addon_name' : None, 'pkg_id' : None, 'pkg_url':None, 'import_settings':None, 'supported_version':'0.0.0'}},
        'ignore': ['files', 'directory', 'filepath'],
        'generate_filter_glob':False
        }

        stl = {'name' : 'stl',
                'ext' : ['.stl'],
                'operator' : {  'default':{'command':'bpy.ops.wm.stl_import', 'module':None, 'addon_name' : 'io_mesh_stl', 'pkg_id' : None, 'import_settings':None, 'pkg_url':None, 'supported_version':'0.0.0'},
                                'legacy':{'command':'bpy.ops.import_mesh.stl', 'module' : None, 'addon_name' : None, 'pkg_id' : None, 'import_settings':None, 'pkg_url':None, 'supported_version':'0.0.0'}},
                'ignore': ['files', 'directory'],
                'generate_filter_glob':False}

        x3d = {'name' : 'x3d',
            'ext' : ['.x3d', '.wrl'],
            'operator' : {'default':{'command':'bpy.ops.import_scene.x3d','module' : None, 'addon_name' : None, 'pkg_id' : None, 'pkg_url':None, 'import_settings':None, 'supported_version':'2.4.3'}},
            'ignore': ['files', 'directory'],
            'generate_filter_glob':True}

        dxf = {'name' : 'dxf',
        'ext' : ['.dxf'],
        'operator' : {'default':{'command':'bpy.ops.import_scene.dxf','module' : None, 'addon_name' : 'io_import_dxf', 'pkg_id' : None, 'pkg_url':None, 'import_settings':None, 'supported_version':'0.9.10'}},
        'ignore': ['files', 'directory'],
        'generate_filter_glob':True}

        pdb = {'name' : 'pdb',
        'ext' : ['.pdb'],
        'operator' : {'default':{'command':'bpy.ops.import_mesh.pdb','module' : None, 'addon_name' : 'io_mesh_atomic', 'pkg_id' : None, 'pkg_url':None, 'import_settings':None, 'supported_version':'1.9.1'}},
        'ignore': ['files', 'directory'],
        'generate_filter_glob':True}

        xyz = {'name' : 'xyz',
            'ext' : ['.xyz'],
            'operator' : {'default':{'command':'bpy.ops.import_mesh.xyz','module' : None, 'addon_name' : 'io_mesh_atomic', 'pkg_id' : None, 'pkg_url':None, 'import_settings': None, 'supported_version':'1.9.1'}},
            'ignore': ['files', 'directory'],
            'generate_filter_glob':True}

        max3ds = {'name' : 'max3ds',
                'ext' : ['.3ds'],
                'operator' : {'default':{'command':'bpy.ops.import_scene.max3ds','module' : None, 'addon_name' : 'io_scene_3ds', 'pkg_id' : None, 'pkg_url':None, 'supported_version':'2.7.5', 'import_settings':
                                        [['Include',
                                                    {"use_image_search": {'type':'bpy.props.BoolProperty', 'name':'"Image Search"', 'default':True},
                                                    "object_filter": {'type':'bpy.props.EnumProperty', 'name':'"Object Filter"', 'default':{'WORLD', 'MESH', 'LIGHT', 'CAMERA', 'EMPTY'},
                                                                    'enum_items':(('WORLD', "World".rjust(11), "", 'WORLD_DATA', 0x1),
                                                                                    ('MESH', "Mesh".rjust(11), "", 'MESH_DATA', 0x2),
                                                                                    ('LIGHT', "Light".rjust(12), "", 'LIGHT_DATA', 0x4),
                                                                                    ('CAMERA', "Camera".rjust(11), "", 'CAMERA_DATA', 0x8),
                                                                                    ('EMPTY', "Empty".rjust(11), "", 'EMPTY_AXIS', 0x10),),
                                                                                'options':{'ENUM_FLAG'},},
                                                    "use_keyframes":{'type':'bpy.props.BoolProperty', 'name':'"Collection"', 'default':True},
                                                    "use_cursor":{'type':'bpy.props.BoolProperty', 'name':'"Cursor Origin"', 'default':False}}],
                                                    ['Transform',
                                                    {"constrain_size" : {'type':'bpy.props.FloatProperty', 'name':'"Constrain Size"', 'default':1.0},
                                                    "use_scene_unit" : {'type':'bpy.props.BoolProperty', 'name':'"Scene Unit"', 'default':False},
                                                    "use_center_pivot" : {'type':'bpy.props.BoolProperty', 'name':'"Pivot Origin"', 'default':False},
                                                    "use_apply_transform" : {'type':'bpy.props.BoolProperty', 'name':'"Apply Transform"', 'default':True},
                                                    "use_world_matrix" : {'type':'bpy.props.BoolProperty', 'name':'"World Space"', 'default':False},
                                                    "axis_forward": {'type':'bpy.props.EnumProperty', 'name':'"Forward"', 'default':'"Y"', 'enum_items':axis()},
                                                    "axis_up": {'type':'bpy.props.EnumProperty', 'name':'"Up"', 'default':'"Z"', 'enum_items':axis()}}]]}},
                'ignore': ['files', 'directory'],
                'generate_filter_glob':False}

        svg = {'name' : 'svg',
            'ext' : ['.svg'],
            'operator' : {  'default':{'command':'bpy.ops.import_curve.svg', 'module':None, 'addon_name' : 'io_curve_svg', 'pkg_id' : None, 'import_settings':None, 'pkg_url':None, 'supported_version':'0.0.0'}},
            'ignore': ['files', 'directory'],
            'generate_filter_glob':False}