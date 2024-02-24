import bpy
from os import path
from .unique_name import UniqueName
from ...logger import LOG


class IMPORT_SCENE_OT_tila_import_blend(bpy.types.Operator):
	bl_idname = "import_scene.tila_import_blend"
	bl_label = "Import Blend"
	bl_options = {'REGISTER', 'INTERNAL'}
	bl_description = 'Append or Link Blend file'

	import_mode : bpy.props.EnumProperty(name="Import Mode", default="APPEND", items=[("APPEND", "Append", ""), ("LINK", "Link", "")])

	import_actions : bpy.props.BoolProperty(name="Import Actions", default=False)
	import_armatures : bpy.props.BoolProperty(name="Import Armatures", default=False)
	import_brushes : bpy.props.BoolProperty(name="Import Brushes", default=False)
	import_cameras : bpy.props.BoolProperty(name="Import Cameras", default=False)
	import_cache_files : bpy.props.BoolProperty(name="Import Cache files",  default=False)
	import_curves : bpy.props.BoolProperty(name="Import Curves", default=False)
	import_hair_curves : bpy.props.BoolProperty(name="Import Curves", default=False)
	import_fonts : bpy.props.BoolProperty(name="Import Fonts", default=False)
	import_grease_pencils : bpy.props.BoolProperty(name="Import Grease Penil", default=False)
	import_collections : bpy.props.BoolProperty(name="Import Collections", default=False)
	import_images : bpy.props.BoolProperty(name="Import Images", default=False)
	import_lights : bpy.props.BoolProperty(name="Import Lights", default=False)
	import_linestyles : bpy.props.BoolProperty(name="Import Line Styes", default=False)
	import_lattices : bpy.props.BoolProperty(name="Import Lattices", default=False)
	import_masks : bpy.props.BoolProperty(name="Import Masks", default=False)
	import_materials : bpy.props.BoolProperty(name="Import Materials", default=False)
	import_metaballs : bpy.props.BoolProperty(name="Import Metaballs", default=False)
	import_meshes : bpy.props.BoolProperty(name="Import Meshes", default=False)
	import_movieclips : bpy.props.BoolProperty(name="Import Movie Clips", default=False)
	import_node_groups : bpy.props.BoolProperty(name="Import Node Groups", default=False)
	import_objects : bpy.props.BoolProperty(name="Import Objects", default=True)
	import_paint_curves : bpy.props.BoolProperty(name="Import Paint Cures", default=False)
	import_palettes : bpy.props.BoolProperty(name="Import Palettes", default=False)
	import_particles : bpy.props.BoolProperty(name="Import Particle", default=False)
	import_pointclouds : bpy.props.BoolProperty(name="Import Point Cloud", default=False)
	import_lightprobes : bpy.props.BoolProperty(name="Import Light Probes", default=False)
	import_scenes : bpy.props.BoolProperty(name="Import Scenes", default=False)
	import_sounds : bpy.props.BoolProperty(name="Import Sounds", default=False)
	import_speakers : bpy.props.BoolProperty(name="Import Speakers", default=False)
	import_texts : bpy.props.BoolProperty(name="Import Texts", default=False)
	import_textures : bpy.props.BoolProperty(name="Import Textures", default=False)
	import_volumes : bpy.props.BoolProperty(name="Import Volumes", default=False)
	import_worlds : bpy.props.BoolProperty(name="Import Worlds", default=False)
	import_workspaces : bpy.props.BoolProperty(name="Import Workspaces", default=False)
	
	filepath : bpy.props.StringProperty(name="File Path", subtype='FILE_PATH', options={'HIDDEN'})

	import_to_collection_source = ['objects']
	excluded_datatypes = ['batch_remove', 'bl_rna', 'filepath', 'is_dirty', 'is_saved', 'libraries', 'orphans_purge', 'rna_type', 'screens', 'temp_data', 'use_autopack', 'user_map', 'version', 'window_managers']
	dependency_datatype = [	'ACTION',
							'ARMATURE',
							'BRUSH',
							'CACHEFILE',
							'CAMERA',
							'COLLECTION',
							'CURVE',
							'CURVES',
							'FONT',
							'GEOMETRY',
							'GREASEPENCIL',
							'GREASEPENCIL_V3',
							'IMAGE',
							'KEY',
							'LATTICE',
							'LIBRARY',
							'LIGHT',
							'LIGHT_PROBE',
							'LINESTYLE',
							'MASK',
							'MATERIAL',
							'MESH',
							'META',
							'MOVIECLIP',
							'NODETREE',
							'NODE'
							'OBJECT',
							'PAINTCURVE',
							'PALETTE',
							'PARTICLE',
							'POINTCLOUD',
							'SCENE',
							'SCREEN',
							'SOUND',
							'SPEAKER',
							'TEXT',
							'TEXTURE',
							'VOLUME',
							'WINDOWMANAGER',
							'WORKSPACE',
							'WORLD']
	
	@property
	def import_datas(self):
		if self._import_datas is None:
			self._import_datas = [m.replace('import_', '') for m in self.__annotations__.keys() if m.startswith('import_') and m != 'import_mode' and getattr(self, m)]
		
		return self._import_datas

	@property
	def local_names(self):
		if self._local_names is None:
			local_names = {}

			for datatype in dir(bpy.data):
				if (datatype in self.excluded_datatypes or datatype.startswith('__')) or datatype not in self.import_datas :
					continue
				
				data = getattr(bpy.data, datatype)
				
				local_names[datatype] = [d.name for d in data]
			
			self._local_names = local_names
			
		return self._local_names
	
	@property
	def operation(self):
		return 'Appending' if self.import_mode == "APPEND" else 'Linking'
	
	@property
	def library(self):
		if self._library is None:
			lib_name = path.basename(self.filepath)
			if lib_name in bpy.data.libraries:
				self._library = bpy.data.libraries[lib_name]

		return self._library

	def register_local_unique_names(self):
		for source in self.import_datas:
			local_datas = getattr(bpy.data, source)

			for e in local_datas:
				self.unique_name.register_element_correspondance(e)


	def get_import_command(self):
		return bpy.ops.wm.append if self.import_mode == "APPEND" else bpy.ops.wm.link
	
	def get_modifier_dependencies(self, obj, dependencies):
		# Capture Dependencies
		for m in obj.modifiers:
			for p in dir(m):
				if p.startswith('__'):
					continue
				
				attr = getattr(m, p, None)
				
				if attr is None:
					continue
				
				try:
					attr.rna_type
					attr_type = attr.type
				except AttributeError:
					continue

				if attr.rna_type.name != 'Object':
					continue

				if attr_type in self.dependency_datatype:
					if attr in dependencies:
						continue
					dependencies.append(attr)

	def make_local(self, objects):
		override = bpy.context.copy()
		override["selected_objects"] = objects
		with bpy.context.temp_override(**override):
			bpy.ops.object.make_local(type='SELECT_OBDATA_MATERIAL')

	def import_command(self, source):
		imported_objects = []
		source_string = source.replace('_', ' ')
		with bpy.data.libraries.load(self.filepath, link=True) as (data_from, data_to):
			data_source = getattr(data_from, source)
			for name in data_source:
				target = getattr(data_to, source)
				LOG.info(f'				Blend format : {self.operation} {source_string} : {name}')
				target.append(name)

				if source in self.import_to_collection_source:
					imported_objects.append(name)

		object_to_append = []

		for o in self.library.users_id:
			if o.rna_type.name != 'Object':
				continue
			if o.name in imported_objects:

				if o.name in self.current_collection.objects :
					library_duplicate = False

					for ob in self.current_collection.objects:
						if ob.name == o.name and ob.library is not None and ob.library.name == self.library.name:
							library_duplicate = True
							break

					if library_duplicate:
						LOG.warning(f'				Blend format : {o.name} {source_string} already in {self.current_collection.name} collection. Skipping ...')
						continue

				LOG.info(f'				Blend format : Link {o.name} {source_string} to {self.current_collection.name} collection')
				self.current_collection.objects.link(o)

				if self.import_mode == 'APPEND':
					self.get_modifier_dependencies(o, object_to_append)

					if o not in object_to_append:
						object_to_append.append(o)
		
		object_to_append.reverse()
		self.make_local(object_to_append)
			
	def execute(self, context):
		self.current_collection = context.collection
		self.unique_name = UniqueName()
		self._import_datas = None
		self._local_names = None
		self._library = None
		self.register_local_unique_names()

		if self.import_actions:
			self.import_command('actions')
		if self.import_armatures:
			self.import_command('armatures')
		if self.import_brushes:
			self.import_command('brushes')
		if self.import_cameras:
			self.import_command('cameras')
		if self.import_cache_files:
			self.import_command('cache_files')
		if self.import_curves:
			self.import_command('curves')
		if self.import_hair_curves:
			self.import_command('hair_curves')
		if self.import_fonts:
			self.import_command('fonts')
		if self.import_grease_pencils:
			self.import_command('grease_pencils')
			self.import_command('grease_pencils_v3')
		if self.import_collections:
			self.import_command('collections')
		if self.import_images:
			self.import_command('images')
		if self.import_lights:
			self.import_command('lights')
		if self.import_linestyles:
			self.import_command('linestyles')
		if self.import_lattices:
			self.import_command('lattices')
		if self.import_masks:
			self.import_command('masks')
		if self.import_materials:
			self.import_command('materials')
		if self.import_metaballs:
			self.import_command('metaballs')
		if self.import_meshes:
			self.import_command('meshes')
		if self.import_movieclips:
			self.import_command('movieclips')
		if self.import_node_groups:
			self.import_command('node_groups')
		if self.import_objects:
			self.import_command('objects')
		if self.import_paint_curves:
			self.import_command('paint_curves')
		if self.import_particles:
			self.import_command('particles')
		if self.import_palettes:
			self.import_command('palettes')
		if self.import_pointclouds:
			self.import_command('pointclouds')
		if self.import_lightprobes:
			self.import_command('lightprobes')
		if self.import_scenes:
			self.import_command('scenes')
		if self.import_sounds:
			self.import_command('sounds')
		if self.import_speakers:
			self.import_command('speakers')
		if self.import_texts:
			self.import_command('texts')
		if self.import_textures:
			self.import_command('textures')
		if self.import_volumes:
			self.import_command('volumes')
		if self.import_worlds:
			self.import_command('worlds')
		if self.import_workspaces:
			self.import_command('workspaces')

		if self.import_mode == 'APPEND':
			# TODO : Need to check if the library is use elsewhere than in the currently imported objects
			bpy.ops.data.tila_remove_library(library_name = self.library.name)
			
		return {'FINISHED'}

class IMPORT_SCENE_OT_tila_remove_library(bpy.types.Operator):
	bl_idname = "data.tila_remove_library"
	bl_label = "Remove Library"
	bl_options = {'REGISTER', 'INTERNAL'}
	bl_description = 'Remove a library by name'

	library_name : bpy.props.StringProperty(name="Library Name", default='')

	def execute(self, context):
		bpy.data.libraries.remove(bpy.data.libraries[self.library_name])
		return {'FINISHED'}

classes = (IMPORT_SCENE_OT_tila_import_blend, IMPORT_SCENE_OT_tila_remove_library)

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