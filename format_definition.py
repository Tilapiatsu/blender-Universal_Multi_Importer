import bpy

class FormatDefinition(object):
	obj = {'name' : 'obj',
			'ext' : '.obj',
			'operator' : 'bpy.ops.import_scene.obj'}
	fbx = {'name' : 'fbx',
			'ext' : '.fbx',
			'operator' : 'bpy.ops.import_scene.fbx'}
	gltf = {'name' : 'gltf',
			'ext' : '.gltf',
			'operator' : 'bpy.ops.import_scene.gltf'}
	x3d = {'name' : 'x3d',
			'ext' : '.x3d',
			'operator' : 'bpy.ops.import_scene.x3d'}
	stl = {'name' : 'stl',
			'ext' : '.stl',
			'operator' : 'bpy.ops.import_mesh.stl'}
	ply = {'name' : 'ply',
			'ext' : '.ply',
			'operator' : 'bpy.ops.import_mesh.ply'}
	abc = {'name' : 'abc',
			'ext' : '.abc',
			'operator' : 'bpy.ops.wm.alembic_import'}
	dae = {'name' : 'dae',
			'ext' : '.dae',
			'operator' : 'bpy.ops.wm.collada_import'}
	svg = {'name' : 'svg',
			'ext' : '.svg',
			'operator' : 'bpy.ops.import_curve.svg'}

