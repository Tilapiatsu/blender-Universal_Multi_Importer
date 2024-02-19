import bpy
import os


class IMPORT_SCENE_OT_tila_import_blend(bpy.types.Operator):
	bl_idname = "import_scene.tila_import_blend"
	bl_label = "Import Blend"
	bl_options = {'REGISTER', 'INTERNAL'}
	bl_description = 'Append or Link Blend file'

	import_mode : bpy.props.EnumProperty(name="Import Mode", default="APPEND", items=[("APPEND", "Append", ""), ("LINK", "Link", "")])
	import_action : bpy.props.BoolProperty(name="Import Actions", default=False)
	import_armature : bpy.props.BoolProperty(name="Import Armatures", default=False)
	import_brush : bpy.props.BoolProperty(name="Import Brushes", default=False)
	import_camera : bpy.props.BoolProperty(name="Import Cameras", default=False)
	import_cache_file : bpy.props.BoolProperty(name="Import Cache files",  default=False)
	import_curve : bpy.props.BoolProperty(name="Import Curves", default=False)
	import_font : bpy.props.BoolProperty(name="Import Fonts", default=False)
	import_grease_pencil : bpy.props.BoolProperty(name="Import Grease Penil", default=False)
	import_collection : bpy.props.BoolProperty(name="Import Collections", default=False)
	import_image : bpy.props.BoolProperty(name="Import Images", default=False)
	import_light : bpy.props.BoolProperty(name="Import Lights", default=False)
	import_line_style : bpy.props.BoolProperty(name="Import Line Styes", default=False)
	import_lattice : bpy.props.BoolProperty(name="Import Lattices", default=False)
	import_mask : bpy.props.BoolProperty(name="Import Masks", default=False)
	import_material : bpy.props.BoolProperty(name="Import Materials", default=False)
	import_metaball : bpy.props.BoolProperty(name="Import Metaballs", default=False)
	import_mesh : bpy.props.BoolProperty(name="Import Meshes", default=False)
	import_movie_clip : bpy.props.BoolProperty(name="Import Movie Clips", default=False)
	import_node_tree : bpy.props.BoolProperty(name="Import Node Trees", default=False)
	import_object : bpy.props.BoolProperty(name="Import Objects", default=True)
	import_paint_curve : bpy.props.BoolProperty(name="Import Paint Cures", default=False)
	import_palette : bpy.props.BoolProperty(name="Import Palettes", default=False)
	import_particle : bpy.props.BoolProperty(name="Import Particle", default=False)
	import_point_cloud : bpy.props.BoolProperty(name="Import Point Cloud", default=False)
	import_light_probe : bpy.props.BoolProperty(name="Import Light Probes", default=False)
	import_scene : bpy.props.BoolProperty(name="Import Scenes", default=False)
	import_sound : bpy.props.BoolProperty(name="Import Sounds", default=False)
	import_speaker : bpy.props.BoolProperty(name="Import Speakers", default=False)
	import_text : bpy.props.BoolProperty(name="Import Texts", default=False)
	import_texture : bpy.props.BoolProperty(name="Import Textures", default=False)
	import_volumes : bpy.props.BoolProperty(name="Import Volumes", default=False)
	import_world : bpy.props.BoolProperty(name="Import Worlds", default=False)
	import_workspace : bpy.props.BoolProperty(name="Import Workspaces", default=False)
	
	filepath : bpy.props.StringProperty(name="File Path", subtype='FILE_PATH', options={'HIDDEN'})

	import_to_collection_source = ['objects']

	def get_import_command(self):
		return bpy.ops.wm.append if self.import_mode == "APPEND" else bpy.ops.wm.link
	
	def import_command(self, source):
		imported_objects = []
		with bpy.data.libraries.load(self.filepath, link=self.import_mode == 'LINK') as (data_from, data_to):
			for name in getattr(data_from, source):
				if name not in data_to:
					# Import objects
					print(f'Importing {source} : {name}')
					getattr(data_to, source).append(name)
				else:
					# TODO : Need to deal with Name Collision
					pass

				if source in self.import_to_collection_source:
					imported_objects.append(name)
		
		for name in imported_objects:
			self.current_collection.objects.link(bpy.data.objects[name])

	def execute(self, context):
		self.current_collection = context.collection
		if self.import_action:
			self.import_command('actions')
		if self.import_armature:
			self.import_command('armatures')
		if self.import_brush:
			self.import_command('brushes')
		if self.import_camera:
			self.import_command('cameras')
		if self.import_cache_file:
			self.import_command('cache_files')
		if self.import_curve:
			self.import_command('curves')
			self.import_command('hair_curves')
		if self.import_font:
			self.import_command('fonts')
		if self.import_grease_pencil:
			self.import_command('grease_pencils')
			self.import_command('grease_pencils_v3')
		if self.import_collection:
			self.import_command('collections')
		if self.import_image:
			self.import_command('images')
		if self.import_light:
			self.import_command('lights')
		if self.import_line_style:
			self.import_command('linestyles')
		if self.import_lattice:
			self.import_command('lattices')
		if self.import_mask:
			self.import_command('masks')
		if self.import_material:
			self.import_command('materials')
		if self.import_metaball:
			self.import_command('metaballs')
		if self.import_mesh:
			self.import_command('meshes')
		if self.import_movie_clip:
			self.import_command('movieclips')
		if self.import_node_tree:
			self.import_command('node_groups')
		if self.import_object:
			self.import_command('objects')
		if self.import_paint_curve:
			self.import_command('paint_curves')
		if self.import_particle:
			self.import_command('particles')
		if self.import_palette:
			self.import_command('palettes')
		if self.import_point_cloud:
			self.import_command('pointclouds')
		if self.import_light_probe:
			self.import_command('lightprobes')
		if self.import_scene:
			self.import_command('scenes')
		if self.import_sound:
			self.import_command('sounds')
		if self.import_speaker:
			self.import_command('speakers')
		if self.import_text:
			self.import_command('texts')
		if self.import_texture:
			self.import_command('textures')
		if self.import_volumes:
			self.import_command('volumes')
		if self.import_world:
			self.import_command('worlds')
		if self.import_workspace:
			self.import_command('workspaces')

		return {'FINISHED'}

classes = (IMPORT_SCENE_OT_tila_import_blend,)

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