import bpy

class FormatDefinition(object):
	obj = {'name' : 'obj',
			'ext' : '.obj',
			'operator' : 'bpy.ops.import_scene.obj',
			'module' : 'IMPORT_SCENE_OT_obj',
			'ignore': ['files', 'directory']}
	fbx = {'name' : 'fbx',
			'ext' : '.fbx',
			'operator' : 'bpy.ops.import_scene.fbx',
			'module' : 'IMPORT_SCENE_OT_fbx',
			'ignore': ['files', 'directory']}
	gltf = {'name' : 'gltf',
			'ext' : '.gltf',
			'operator' : 'bpy.ops.import_scene.gltf',
			'module' : 'IMPORT_SCENE_OT_gltf',
			'ignore': ['files', 'directory']}
	x3d = {'name' : 'x3d',
			'ext' : '.x3d',
			'operator' : 'bpy.ops.import_scene.x3d',
			'module' : 'IMPORT_SCENE_OT_x3d',
			'ignore': ['files', 'directory']}
	stl = {'name' : 'stl',
			'ext' : '.stl',
			'operator' : 'bpy.ops.import_mesh.stl',
			'module' : 'IMPORT_MESH_OT_stl',
			'ignore': ['files', 'directory']}
	ply = {'name' : 'ply',
			'ext' : '.ply',
			'operator' : 'bpy.ops.import_mesh.ply',
			'module' : 'IMPORT_MESH_OT_ply',
			'ignore': ['files', 'directory']}
	abc = {'name' : 'abc',
			'ext' : '.abc',
			'operator' : 'bpy.ops.wm.alembic_import',
			'ignore': ['files', 'directory'],
			'import_settings': {"relative_path": {'type':'bpy.props.BoolProperty', 'name':'"Relative Path"', 'default':True},
								"scale": {'type':'bpy.props.FloatProperty', 'name':'"Scale"', 'default':1.0},
								"set_frame_range": {'type':'bpy.props.BoolProperty', 'name':'"Set Frame Range"', 'default':True},
								"validate_meshes": {'type':'bpy.props.BoolProperty', 'name':'"Validate Meshes"', 'default':False},
								"always_add_cache_reader": {'type':'bpy.props.BoolProperty', 'name':'"Always add Cache Reader"', 'default':False},
								"is_sequence": {'type':'bpy.props.BoolProperty', 'name':'"Is Sequence"', 'default':False},
								"as_background_job": {'type':'bpy.props.BoolProperty', 'name':'"As Background Job"', 'default':False}
								}
			}
	dae = {'name' : 'dae',
			'ext' : '.dae',
			'operator' : 'bpy.ops.wm.collada_import',
			'ignore': ['files', 'name', 'directory'],
			'import_settings': {"import_units": {'type':'bpy.props.BoolProperty', 'name':'"Relative Path"', 'default':False},
								"custom_normals": {'type':'bpy.props.BoolProperty', 'name':'"Custom Normals"', 'default':True},
								"fix_orientation": {'type':'bpy.props.BoolProperty', 'name':'"Fix Leaf Bones"', 'default':False},
								"find_chains": {'type':'bpy.props.BoolProperty', 'name':'"Find Bone Chains"', 'default':False},
								"auto_connect": {'type':'bpy.props.BoolProperty', 'name':'"Auto Connect"', 'default':False},
								"min_chain_length": {'type':'bpy.props.IntProperty', 'name':'"Minimum Chain Length"', 'default':0},
								"keep_bind_info": {'type':'bpy.props.BoolProperty', 'name':'"Keep Bind Info"', 'default':False}}}
	
	
	svg = {'name' : 'svg',
			'ext' : '.svg',
			'operator' : 'bpy.ops.import_curve.svg',
			'ignore': ['files', 'directory'],
			'import_settings': {}}