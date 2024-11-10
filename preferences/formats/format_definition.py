from . import BVERSION
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
        'operator' : {  'default':{'command':'bpy.ops.import_curve.svg', 'module':None, 'addon_name' : 'io_curve_svg', 'pkg_id' : None, 'import_settings':None}
                        },
        'ignore': ['files', 'directory'],
        'generate_filter_glob':False}
    
    x3d = {'name' : 'x3d',
        'ext' : ['.x3d', '.wrl'],
        'operator' : {'default':{'command':'bpy.ops.import_scene.x3d','module' : 'IMPORT_SCENE_OT_x3d', 'addon_name' : 'io_scene_x3d', 'pkg_id' : None}},
        'ignore': ['files', 'directory'],
        'generate_filter_glob':True}
                
    stl = {'name' : 'stl',
            'ext' : ['.stl'],
            'operator' : {  'default':{'command':'bpy.ops.wm.stl_import', 'module':None, 'addon_name' : 'io_mesh_stl', 'pkg_id' : None, 'import_settings':None},
                            'legacy':{'command':'bpy.ops.import_mesh.stl', 'module' : 'IMPORT_MESH_OT_stl', 'addon_name' : None, 'pkg_id' : None}},
            'ignore': ['files', 'directory'],
            'generate_filter_glob':False}

    usd = {'name' : 'usd',
        'ext' : ['.usd', '.usda', '.usdc', '.usdz'],
        'operator' : {'default':{'command':'bpy.ops.wm.usd_import', 'module':None, 'addon_name' : None, 'pkg_id' : None, 'import_settings':None}},
        'ignore': ['files', 'directory'],
        'generate_filter_glob':False}

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