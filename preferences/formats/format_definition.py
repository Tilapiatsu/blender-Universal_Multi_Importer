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
    
    fbx = {'name' : 'fbx',
            'ext' : ['.fbx'],
            'operator' : {'default':{'command': 'bpy.ops.import_scene.fbx', 'module' : 'IMPORT_SCENE_OT_fbx', 'addon_name' : 'io_scene_fbx', 'pkg_id' : None}},
            'ignore': ['files', 'directory'],
            'generate_filter_glob':False}
    
    gltf = {'name' : 'gltf',
            'ext' : ['.glb', '.gltf'],
            'operator' : {'default':{'command':'bpy.ops.import_scene.gltf','module' : 'IMPORT_SCENE_OT_gltf', 'addon_name' : 'io_scene_gltf2', 'pkg_id' : None}},
            'ignore': ['files', 'directory'],
            'generate_filter_glob':False}
    
    abc = {'name' : 'abc',
            'ext' : ['.abc'],
            'operator' : {'default':{'command':'bpy.ops.wm.alembic_import', 'module':None, 'addon_name' : None, 'pkg_id' : None, 'import_settings':None}},
            'ignore': ['files', 'directory'],
            'generate_filter_glob':False
            }
    
    dae = {'name' : 'dae',
            'ext' : ['.dae'],
            'operator' : {'default':{'command':'bpy.ops.wm.collada_import', 'module':None, 'addon_name' : None, 'pkg_id' : None, 'import_settings':None}},
            'ignore': ['files', 'name', 'directory'],
            'generate_filter_glob':False
            }

    blend = {'name' : 'blend',
            'ext' : ['.blend'],
            'operator' : {'default':{'command':'bpy.ops.import_scene.tila_import_blend', 'module':'IMPORT_SCENE_OT_tila_import_blend', 'addon_name' : None, 'pkg_id' : None}},
            'ignore': ['files', 'directory'],
            'generate_filter_glob':False		
            }
    
    bvh = {'name' : 'bvh',
            'ext' : ['.bvh'],
            'operator' : {'default':{'command':'bpy.ops.import_anim.bvh', 'module':'IMPORT_ANIM_OT_bvh', 'addon_name' : 'io_anim_bvh', 'pkg_id' : None}},
            'ignore': ['files', 'directory'],
            'generate_filter_glob':True		
            }
    
    obj = {'name' : 'obj',
            'ext' : ['.obj'],
            'operator' : {'default':{'command':'bpy.ops.wm.obj_import', 'module':None, 'addon_name' : None, 'pkg_id' : None, 'import_settings':None}},
            'ignore': ['files', 'directory'],
            'generate_filter_glob':False
            }
    
    ply = {'name' : 'ply',
            'ext' : ['.ply'],
            'operator' : {'default':{'command':'bpy.ops.wm.ply_import', 'module':None, 'addon_name' : None, 'pkg_id' : None, 'import_settings':None}},
            'ignore': ['files', 'directory'],
            'generate_filter_glob':False}


        
    svg = {'name' : 'svg',
        'ext' : ['.svg'],
        'operator' : {  'default':{'command':'bpy.ops.import_curve.svg', 'module':None, 'addon_name' : 'io_curve_svg', 'pkg_id' : None, 'import_settings':None}},
        'ignore': ['files', 'directory'],
        'generate_filter_glob':False}
    
    x3d = {'name' : 'x3d',
        'ext' : ['.x3d', '.wrl'],
        'operator' : {'default':{'command':'bpy.ops.import_scene.x3d','module' : 'IMPORT_SCENE_OT_x3d', 'addon_name' : 'bl_ext.blender_org.web3d_x3d_vrml2_format', 'pkg_id' : 'web3d_x3d_vrml2_format'}},
        'ignore': ['files', 'directory'],
        'generate_filter_glob':True}
                

    usd = {'name' : 'usd',
        'ext' : ['.usd', '.usda', '.usdc', '.usdz'],
        'operator' : {'default':{'command':'bpy.ops.wm.usd_import', 'module':None, 'addon_name' : None, 'pkg_id' : None, 'import_settings':None}},
        'ignore': ['files', 'directory'],
        'generate_filter_glob':False}
    
    max = {'name' : 'max',
        'ext' : ['.max'],
        'operator' : {'default':{'command':'bpy.ops.import_scene.max', 'module':None, 'addon_name' : 'bl_ext.blender_org.io_scene_max', 'pkg_id' : 'io_scene_max', 'import_settings':
                                            [['Include', 
                                            {"use_image_search": {'type':'bpy.props.BoolProperty', 'name':'"Image Searcg"', 'default':True},
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
    
    if BVERSION >=4.3:
        image = {'name' : 'image',
            'ext' : [	'.jpg', '.jpeg', '.gif', '.png', '.tif', '.tiff', '.bmp', '.cin', '.dpx', '.jp2', '.j2c', '.sig', '.rgb', '.bw',
                        '.hdr', '.exr',
                        '.mov', '.mp4', '.mkv', '.mpg', '.mpeg', '.dvd', '.vob', '.avi', '.dv', '.flv', '.webm'],
            'operator' : {  'plane':{'command':'bpy.ops.image.import_as_mesh_planes', 'module':'IMAGE_OT_import_as_mesh_planes', 'addon_name' : None, 'pkg_id' : None},

                            'data':{'command':'bpy.ops.image.open', 'module':None, 'addon_name' : None, 'pkg_id' : None, 'import_settings':None},
                            'empty':{'command':'bpy.ops.object.empty_image_add', 'module':None, 'addon_name' : None, 'pkg_id' : None , 'import_settings':None}
                        },
            'ignore': ['files', 'directory', 'filepath'],
            'generate_filter_glob':False
            }
        
        stl = {'name' : 'stl',
                'ext' : ['.stl'],
                'operator' : {  'default':{'command':'bpy.ops.wm.stl_import', 'module':None, 'addon_name' : None, 'pkg_id' : None, 'import_settings':None}},
                'ignore': ['files', 'directory'],
                'generate_filter_glob':False}
        
    elif BVERSION >=4.2:
        image = {'name' : 'image',
            'ext' : [	'.jpg', '.jpeg', '.gif', '.png', '.tif', '.tiff', '.bmp', '.cin', '.dpx', '.jp2', '.j2c', '.sig', '.rgb', '.bw',
                        '.hdr', '.exr',
                         '.mov', '.mp4', '.mkv', '.mpg', '.mpeg', '.dvd', '.vob', '.avi', '.dv', '.flv', '.webm'],
            'operator' : {  'plane':{'command':'bpy.ops.image.import_as_mesh_planes', 'module':'IMAGE_OT_import_as_mesh_planes', 'addon_name' : None, 'pkg_id' : None},

                            'data':{'command':'bpy.ops.image.open', 'module':None, 'addon_name' : None, 'pkg_id' : None, 'import_settings':None},
                            'empty':{'command':'bpy.ops.object.empty_image_add', 'module':None, 'addon_name' : None, 'pkg_id' : None, 'import_settings':None}
                        },
            'ignore': ['files', 'directory', 'filepath'],
            'generate_filter_glob':False
            }
        
        stl = {'name' : 'stl',
                'ext' : ['.stl'],
                'operator' : {  'default':{'command':'bpy.ops.wm.stl_import', 'module':None, 'addon_name' : None, 'pkg_id' : None, 'import_settings':None}},
                'ignore': ['files', 'directory'],
                'generate_filter_glob':False}
        
    else:
        image = {'name' : 'image',
        'ext' : [	'.jpg', '.jpeg', '.gif', '.png', '.tif', '.tiff', '.bmp', '.cin', '.dpx', '.jp2', '.j2c', '.sig', '.rgb', '.bw',
                    '.hdr', '.exr',
                    '.mov', '.mp4', '.mkv', '.mpg', '.mpeg', '.dvd', '.vob', '.avi', '.dv', '.flv', '.webm'],
        'operator' : {  'plane':{'command':'bpy.ops.import_image.to_plane', 'module':'IMPORT_IMAGE_OT_to_plane', 'addon_name' : 'io_import_images_as_planes', 'pkg_id' : None},
                        'data':{'command':'bpy.ops.image.open', 'module':None, 'addon_name' : None, 'pkg_id' : None , 'import_settings':None},
                        'ref':{'command':'bpy.ops.object.load_reference_image', 'module':'OBJECT_OT_load_reference_image', 'addon_name' : None, 'pkg_id' : None },
                        'background':{'command':'bpy.ops.object.load_background_image', 'module':'OBJECT_OT_load_background_image', 'addon_name' : None, 'pkg_id' : None }},
        'ignore': ['files', 'directory', 'filepath'],
        'generate_filter_glob':False
        }

        stl = {'name' : 'stl',
                'ext' : ['.stl'],
                'operator' : {  'default':{'command':'bpy.ops.wm.stl_import', 'module':None, 'addon_name' : 'io_mesh_stl', 'pkg_id' : None, 'import_settings':None},
                                'legacy':{'command':'bpy.ops.import_mesh.stl', 'module' : 'IMPORT_MESH_OT_stl', 'addon_name' : None, 'pkg_id' : None, 'import_settings':None}},
                'ignore': ['files', 'directory'],
                'generate_filter_glob':False}