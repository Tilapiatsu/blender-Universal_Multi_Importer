from ..blender_version import BVERSION

def axis():
	return [
		("X", "X", "X"),
		("Y", "Y", "Y"),
		("Z", "Z", "Z"),
		("NEGATIVE_X", "-X", "-X"),
		("NEGATIVE_Y", "-Y", "-Y"),
		("NEGATIVE_Z", "-Z", "-Z")
	]

class FormatDefinition():
	if BVERSION >= 4.0:
		obj = {'name' : 'obj',
				'ext' : ['.obj'],
				'operator' : {'default':'bpy.ops.wm.obj_import'},
				'ignore': ['files', 'directory'],
				'import_settings': [['Transform',
									{"global_scale": {'type':'bpy.props.FloatProperty', 'name':'"Scale"', 'default':1.0},
									"clamp_size" : {'type':'bpy.props.FloatProperty', 'name':'"Clamp Bounding Box"', 'default':1.0},
									"forward_axis" : {'type':'bpy.props.EnumProperty', 'name':'"Forward Axis"', 'default':'"NEGATIVE_Z"', 'enum_items':axis()},
									"up_axis" : {'type':'bpy.props.EnumProperty', 'name':'"Up Axis"', 'default':'"Y"', 'enum_items':axis()}}],

									['Options',
									{"use_split_objects": {'type':'bpy.props.BoolProperty', 'name':'"Split By Object"', 'default':True},
									"use_split_groups": {'type':'bpy.props.BoolProperty', 'name':'"Split By Group"', 'default':False},
									"import_vertex_groups": {'type':'bpy.props.BoolProperty', 'name':'"Vertex Groups"', 'default':False},
									"validate_meshes": {'type':'bpy.props.BoolProperty', 'name':'"Validate Meshes"', 'default':False}
									}]]}
		ply = {'name' : 'ply',
				'ext' : ['.ply'],
				'operator' : {'default':'bpy.ops.wm.ply_import'},
				'ignore': ['files', 'directory'],
				'import_settings': [['Transform',
									{"global_scale": {'type':'bpy.props.FloatProperty', 'name':'"Scale"', 'default':1.0},
									"use_scene_unit": {'type':'bpy.props.BoolProperty', 'name':'"Scene Unit"', 'default':False},
									"forward_axis" : {'type':'bpy.props.EnumProperty', 'name':'"Forward Axis"', 'default':'"Y"', 'enum_items':axis()},
									"up_axis" : {'type':'bpy.props.EnumProperty', 'name':'"Up Axis"', 'default':'"Z"', 'enum_items':axis()}}],

									['Options',
									{"merge_verts": {'type':'bpy.props.BoolProperty', 'name':'"Merge Verticies"', 'default':False},
									"import_colors" : {'type':'bpy.props.EnumProperty', 'name':'"Forward Axis"', 'default':'"SRGB"', 'enum_items':[("SRGB", "sRGB", ""), ("LINEAR", "Linear", ""), ("NONE", "None", "")]}
									}]]}
	else:
		obj = {	'name' : 'obj',
				'ext' : ['.obj'],
				'operator' : {'default':'bpy.ops.import_scene.obj'},
				'module' : 'IMPORT_SCENE_OT_obj',
				'ignore': ['files', 'directory']}
		ply = {	'name' : 'ply',
				'ext' : ['.ply'],
				'operator' : {'default':'bpy.ops.import_mesh.ply'},
				'module' : 'IMPORT_MESH_OT_ply',
				'ignore': ['files', 'directory']}
		
	fbx = {'name' : 'fbx',
			'ext' : ['.fbx'],
			'operator' : {'default':'bpy.ops.import_scene.fbx'},
			'module' : 'IMPORT_SCENE_OT_fbx',
			'ignore': ['files', 'directory']}
	
	gltf = {'name' : 'gltf',
			'ext' : ['.glb', '.gltf'],
			'operator' : {'default':'bpy.ops.import_scene.gltf'},
			'module' : 'IMPORT_SCENE_OT_gltf',
			'ignore': ['files', 'directory']}
	
	x3d = {'name' : 'x3d',
			'ext' : ['.x3d'],
			'operator' : {'default':'bpy.ops.import_scene.x3d'},
			'module' : 'IMPORT_SCENE_OT_x3d',
			'ignore': ['files', 'directory']}
	
	stl = {'name' : 'stl',
			'ext' : ['.stl'],
			'operator' : {'default':'bpy.ops.import_mesh.stl'},
			'module' : 'IMPORT_MESH_OT_stl',
			'ignore': ['files', 'directory']}
	
	abc = {'name' : 'abc',
			'ext' : ['.abc'],
			'operator' : {'default':'bpy.ops.wm.alembic_import'},
			'ignore': ['files', 'directory'],
			'import_settings': [['Manual Transform',
								{"scale": {'type':'bpy.props.FloatProperty', 'name':'"Scale"', 'default':1.0}}],

								['Options',
								{"relative_path": {'type':'bpy.props.BoolProperty', 'name':'"Relative Path"', 'default':True},
								"set_frame_range": {'type':'bpy.props.BoolProperty', 'name':'"Set Frame Range"', 'default':True},
								"is_sequence": {'type':'bpy.props.BoolProperty', 'name':'"Is Sequence"', 'default':False},
								"validate_meshes": {'type':'bpy.props.BoolProperty', 'name':'"Validate Meshes"', 'default':False},
								"always_add_cache_reader": {'type':'bpy.props.BoolProperty', 'name':'"Always add Cache Reader"', 'default':False}
								# "as_background_job": {'type':'bpy.props.BoolProperty', 'name':'"As Background Job"', 'default':False}
								}]]
			}
	
	dae = {'name' : 'dae',
			'ext' : ['.dae'],
			'operator' : {'default':'bpy.ops.wm.collada_import'},
			'ignore': ['files', 'name', 'directory'],
			'import_settings': [['Import Data Options',
								{"import_units": {'type':'bpy.props.BoolProperty', 'name':'"Relative Path"', 'default':False},
								"custom_normals": {'type':'bpy.props.BoolProperty', 'name':'"Custom Normals"', 'default':True}}],
								
								['Armature Options',
								{"fix_orientation": {'type':'bpy.props.BoolProperty', 'name':'"Fix Leaf Bones"', 'default':False},
								"find_chains": {'type':'bpy.props.BoolProperty', 'name':'"Find Bone Chains"', 'default':False},
								"auto_connect": {'type':'bpy.props.BoolProperty', 'name':'"Auto Connect"', 'default':False},
								"min_chain_length": {'type':'bpy.props.IntProperty', 'name':'"Minimum Chain Length"', 'default':0}}],
								
								['', 
								{"keep_bind_info": {'type':'bpy.props.BoolProperty', 'name':'"Keep Bind Info"', 'default':False}}]]}
	
	
	svg = {'name' : 'svg',
			'ext' : ['.svg'],
			'operator' : {'default':'bpy.ops.import_curve.svg', 'grease_pencil':'bpy.ops.wm.gpencil_import_svg'},
			'ignore': ['files', 'directory']}
	
	
	usd = {'name' : 'usd',
			'ext' : ['.usd', '.usda', '.usdc', '.usdz'],
			'operator' : {'default':'bpy.ops.wm.usd_import'},
			'ignore': ['files', 'directory'],
			'import_settings': [['Data Types', 
								{"import_cameras": {'type':'bpy.props.BoolProperty', 'name':'"Import Cameras"', 'default':True},
								"import_curves": {'type':'bpy.props.BoolProperty', 'name':'"Import Curves"', 'default':True},
								"import_lights": {'type':'bpy.props.BoolProperty', 'name':'"Import Lights"', 'default':True},
								"import_materials": {'type':'bpy.props.BoolProperty', 'name':'"Import Materials"', 'default':True},
								"import_meshes": {'type':'bpy.props.BoolProperty', 'name':'"Import Meshes"', 'default':True},
								"import_volumes": {'type':'bpy.props.BoolProperty', 'name':'"Import Volumes"', 'default':True},
								"import_shapes": {'type':'bpy.props.BoolProperty', 'name':'"Import Shapes"', 'default':True}}],

								['',
								{"prim_path_mask": {'type':'bpy.props.StringProperty', 'name':'"Path Mask"', 'default':'""'},
								"scale": {'type':'bpy.props.FloatProperty', 'name':'"Scale"', 'default':1.0}}],
				
								['Mesh Data', 
								{"read_mesh_uvs": {'type':'bpy.props.BoolProperty', 'name':'"UV Coordinates"', 'default':True},
								"read_mesh_colors": {'type':'bpy.props.BoolProperty', 'name':'"Collor Attributes"', 'default':True}}],
				
								['Include', 
								{"import_subdiv": {'type':'bpy.props.BoolProperty', 'name':'"Subdivision"', 'default':False},
								"import_instance_proxies": {'type':'bpy.props.BoolProperty', 'name':'"Import Instance Proxies"', 'default':True},
								"import_visible_only": {'type':'bpy.props.BoolProperty', 'name':'"Visible Primitives Only"', 'default':True},
								"import_guide": {'type':'bpy.props.BoolProperty', 'name':'"Guide"', 'default':False},
								"import_proxy": {'type':'bpy.props.BoolProperty', 'name':'"Proxy"', 'default':True},
								"import_render": {'type':'bpy.props.BoolProperty', 'name':'"Render"', 'default':True}}],
				
								['Options',
								{"set_frame_range": {'type':'bpy.props.BoolProperty', 'name':'"Set Frame Range"', 'default':True},
								"relative_path": {'type':'bpy.props.BoolProperty', 'name':'"Relative Path"', 'default':True},
								"create_collection": {'type':'bpy.props.BoolProperty', 'name':'"Create Collection"', 'default':False}}],
				
								['', 
								{"light_intensity_scale": {'type':'bpy.props.FloatProperty', 'name':'"Light Intensity Scale"', 'default':1.0}}],
								
								['Materials',
								{"import_all_materials": {'type':'bpy.props.BoolProperty', 'name':'"Import All Materials"', 'default':False},
								"import_usd_preview": {'type':'bpy.props.BoolProperty', 'name':'"Import USD Preview"', 'default':True},
								"set_material_blend": {'type':'bpy.props.BoolProperty', 'name':'"Set Material Blend"', 'default':True}}],
				
								['',
								{"mtl_name_collision_mode": {'type':'bpy.props.EnumProperty', 'name':'"Material Name Collision"', 'default':'"MAKE_UNIQUE"', 'enum_items':[("MAKE_UNIQUE", "Make Unique", ""), ("REFERENCE_EXISTING", "Reference Existing", "")]}}],

								['',
								{"import_textures_mode": {'type':'bpy.props.EnumProperty', 'name':'"Import Textures"', 'default':'"IMPORT_PACK"', 'enum_items':[("IMPORT_NONE", "None", ""), ("IMPORT_PACK", "Packed", ""), ("IMPORT_COPY", "Copy", "")]},
								"import_textures_dir": {'type':'bpy.props.StringProperty', 'name':'"Textures Directory"', 'default':'"//textures/"'},
								"tex_name_collision_mode": {'type':'bpy.props.EnumProperty', 'name':'"File Name Collision"', 'default':'"USE_EXISTING"', 'enum_items':[("USE_EXISTING", "Use Existing", ""), ("OVERWRITE", "Overwrite Existing", "")]}}]]
								}
	
	blend = {'name' : 'blend',
			'ext' : ['.blend'],
			'operator' : {'default':'bpy.ops.import_scene.tila_import_blend'},
			'module' : 'IMPORT_SCENE_OT_tila_import_blend',
			'ignore': ['files', 'directory']		
			}