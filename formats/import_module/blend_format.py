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
	import_hair_curves : bpy.props.BoolProperty(name="Import Hair Curves", default=False)
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
	import_particles : bpy.props.BoolProperty(name="Import Particles", default=False)
	import_pointclouds : bpy.props.BoolProperty(name="Import Point Clouds", default=False)
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

	import_to_collection_source = ['objects', 'collections']
	import_to_collection_rnatype_name = ['Object', 'Collection']
	force_append_mode = ['collections', 'workspaces', 'volumes', 'scenes', 'lightprobes', 'particles', 'pointclouds']
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
	def is_append(self):
		return self.import_mode == 'APPEND'

	@property
	def is_link(self):
		return self.import_mode == 'LINK'
	
	@property
	def filename(self):
		return path.basename(self.filepath)

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
		return 'Appending' if self.is_append else 'Linking'
	
	@property
	def library(self):
		if self._library is None:
			lib_name = self.filename
			if lib_name in bpy.data.libraries:
				self._library = bpy.data.libraries[lib_name]

		return self._library

	def register_local_unique_names(self):
		for source in self.import_datas:
			local_datas = getattr(bpy.data, source)

			for e in local_datas:
				self.unique_name.register_element_correspondance(e)


	def get_import_command(self):
		return bpy.ops.wm.append if self.is_append else bpy.ops.wm.link
	
	def get_data_dependencies(self, src, object_to_import, dependencies, data):
		# Capture Dependencies
		for p in dir(src):
			if p.startswith('__'):
				continue
			
			attr = getattr(src, p, None)
			
			if attr is None:
				continue
			
			try:
				attr.rna_type
				attr_type = attr.id_type
			except AttributeError:
				continue

			if attr_type in self.dependency_datatype:
				if attr in object_to_import:
					continue

				if attr_type == 'OBJECT':
					if attr in object_to_import:
						continue
					LOG.info(f'Blend format : Link Object Depencency "{attr.name}"')
					object_to_import.append(attr)
				elif attr_type in ['NODETREE', 'GEOMETRY']:
					if attr in data:
						continue
					LOG.info(f'Blend format : Link Node Depencency "{attr.name}"')
					data.append(attr.name)
				else:
					if attr in dependencies:
						continue
					LOG.info(f'Blend format : Link Depencency "{attr.name}"')
					dependencies.append(attr)

	def append_data(self, source, data_list):
		source_string = source.replace('_', ' ')
		# Import Loop
		with bpy.data.libraries.load(self.filepath, link=False) as (data_from, data_to):
			data_source = getattr(data_from, source)
			for name in data_source:
				if name not in data_list:
					continue

				target = getattr(data_to, source)
				LOG.info(f'Blend format : Appending {source_string} : {name}')
				target.append(name)

	def get_node_dependencies(self, data, dep=[], local_data=[]):
		for n in data.nodes:
			node_tree = getattr(n, 'node_tree', None)
			if node_tree is None:
				continue

			if node_tree in local_data:
				# n.node_tree = bpy.data.node_groups[node_tree.name]
				continue

			if node_tree.library is None:
				continue
			
			if node_tree in dep:
				continue
			
			dep.append(node_tree)

			new_dep = self.get_node_dependencies(node_tree, dep=[], local_data = local_data)

			for nd in new_dep:
				if nd in dep:
					continue

				dep.append(nd)

		return dep
	
	def get_font_dependencies(self, data):
		if data.font.library is None:
			return False
		LOG.info(f'Blend format : Appending "{data.font.name}"')
		data.font.make_local()
		return True

	def make_local(self, to_append, dependencies, data):
		local_data = []
		if len(to_append['Object']):
			override = {}
			override["selected_objects"] = to_append['Object']
			with bpy.context.temp_override(**override):
				bpy.ops.object.make_local(type='SELECT_OBDATA_MATERIAL') 

				for o in bpy.context.selected_objects:
					if o.data is None:
						continue
					
					# Make Fonts Local
					if o.data.rna_type.name == 'Text Curve':
						if not self.get_font_dependencies(o.data):
							continue

			with bpy.context.temp_override(**override):
				bpy.ops.object.make_local(type='SELECT_OBDATA_MATERIAL')
	
		for d in dependencies:
			if d in local_data:
				continue
			d.make_local()
			local_data.append(d)
			
		for d in data:
			if d in local_data:
				continue
			d.make_local()

			local_data.append(d)
			LOG.info(f'Blend format : Appending "{d.name}"')

			# Make Fonts Local
			if d.rna_type.name == 'Text Curve':
				if not self.get_font_dependencies(d):
					continue

			if d.id_type in ['NODETREE']:
				dep = self.get_node_dependencies(d, dep=[], local_data=local_data)
				while len(dep):
					for dd in dep:
						if dd in local_data:
							continue
						
						if dd.library is None:
							continue

						local_dd = dd.make_local()
						local_data.append(dd)

					dep = self.get_node_dependencies(d, dep=[], local_data=local_data)

	def prevent_name_collision(self, source):
		need_rename = {}
		with bpy.data.libraries.load(self.filepath, link=self.is_link) as (data_from, data_to):
			data_source = getattr(data_from, source)
			data_target = getattr(bpy.data, source)
			data_target = [d.name for d in data_target]
			for name in data_source:
				if name in data_target:
					need_rename[name] = None

		for name in need_rename.keys():
			new_name = self.unique_name.get_unique_name(name)
			element = getattr(bpy.data, source)[name]
			need_rename[name] = element
			element.name = new_name
			# self.unique_name.element_correspondance[element] = new_name
		
		return need_rename

	def revert_name_collision(self, source:str, duplicate_data_names:dict):
		data = getattr(bpy.data, source)

		for name in duplicate_data_names.keys():
			data[name].name = self.unique_name.get_next_valid_name(name)
			duplicate_data_names[name].name = name


	def import_command(self, source):
		imported_object_names = []
		data = []
		data_names = []
		name_collison_data = {}
		source_string = source.replace('_', ' ')

		before_import_data = {d.name:None for d in getattr(bpy.data, source)}
		self.register_local_unique_names()

		name_collison_data = self.prevent_name_collision(source)

		# Import Loop
		with bpy.data.libraries.load(self.filepath, link=self.is_link) as (data_from, data_to):
			data_source = getattr(data_from, source)
			for name in data_source:
				target = getattr(data_to, source)
				LOG.info(f'Blend format : {self.operation} {source_string} : {name}')
				target.append(name)

				if source in self.import_to_collection_source:
					# Element Already in local file
					if name in before_import_data.keys():
						new_name = self.unique_name.get_next_valid_name(name)
						before_import_data[name] = new_name
						
					imported_object_names.append(name)
				else:
					data_names.append(name)

		self.revert_name_collision(source, name_collison_data)

		self.register_local_unique_names()

		if self.import_mode == 'APPEND':
			for name, new_name in before_import_data.items():
				if new_name is None:
					continue
				self.unique_name.register_element_correspondance(getattr(bpy.data, source)[new_name])
				i = imported_object_names.index(name)
				imported_object_names[i] = new_name
				before_import_data[name] = getattr(bpy.data, source)[new_name]

		to_append = {'Object':[], 'Collection':[]}
		dependencies = []

		# Stop Import if no data found in Blend file
		if self.library is None:
			message = f'No {source_string} found in {self.filename}. Skipping ...'
			LOG.warning(f'Blend format : ' + message)
			LOG.store_failure(message)
			self.errors.append(message)
			return
		
		if source == 'objects':
			source_data = self.library.users_id if self.is_link else getattr(bpy.data, source)
			library_objects = [o for o in source_data if o.rna_type.name in self.import_to_collection_rnatype_name]
			# Link to Collection
			for o in library_objects:
				if o.name not in imported_object_names:
					continue

				if o.name in self.current_collection.objects :
					library_duplicate = False

					for ob in self.current_collection.objects:
						if ob.name == o.name and ob.library is not None and ob.library.name == self.library.name:
							library_duplicate = True
							break

					if library_duplicate:
						LOG.warning(f'Blend format : "{o.name}" {source_string} already in "{self.current_collection.name}" collection. Skipping ...')
						continue

				LOG.info(f'Blend format : Link "{o.name}" {source_string} to "{self.current_collection.name}" collection')

				if o.rna_type.name == "Object":
					if o.name in self.current_collection.objects:
						o = before_import_data[o.name]
					self.current_collection.objects.link(o)

					if self.is_append:
						for m in o.modifiers:
							self.get_data_dependencies(m, to_append, dependencies, data_names)

						if o not in to_append['Object']:
							to_append['Object'].append(o)

				elif o.rna_type.name == 'Collection':
					self.current_collection.children.link(o)

					if self.is_append:
						if o not in to_append['Collection']:
							to_append['Collection'].append(o)

				# append Data:
				if 'data' in dir(o):
					if o.data is not None:
						if o.data.name not in data_names:
							data_names.append(o.data.name)
						self.get_data_dependencies(o.data, to_append, dependencies, data_names)

		elif source == 'collections':
			for c in getattr(bpy.data, source):
				if c.name not in imported_object_names and self.is_append:
					continue

				self.current_collection.children.link(c)

				if self.is_append:
					if c not in to_append['Collection']:
						to_append['Collection'].append(c)
			
		# reorder data to ensure make local will work as expected
		lib = [d for d in self.library.users_id if d.name in data_names]
		for d in data_names:
			for l in lib:
				if l.name !=d:
					continue
				
				data.append(l)

		if self.is_append:
			self.make_local(to_append, dependencies, data)

		self._library = None
	
	def import_data(self):
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
			# self.import_command('grease_pencils_v3')
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
		
		self.importing = False

	def modal(self, context, event):
		bpy.ops.wm.redraw_timer(type='DRAW', iterations=1)
		if not self.import_started:
			self.import_started = True
			self.importing = True
			self.import_data()
		
		if not self.import_finished and not self.importing:
			if self.import_mode == 'APPEND' and self.library is not None:
				bpy.ops.data.tila_remove_library(library_name=self.library.name)

			self.import_finished = True
			
			context.window_manager.event_timer_remove(self._timer)
			
			return {'FINISHED'}

		return {'RUNNING_MODAL'}


	def execute(self, context):
		self.current_collection = context.collection
		self.unique_name = UniqueName()
		self._import_datas = None
		self._local_names = None
		self._library = None
		self.import_started = False
		self.importing = False
		self.import_finished = False
		self.errors = []
		self.register_local_unique_names()

		wm = context.window_manager
		self._timer = wm.event_timer_add(0.01, window=context.window)
		wm.modal_handler_add(self)
		return {'RUNNING_MODAL'}

class RemoveLibrary(bpy.types.Operator):
	bl_idname = "data.tila_remove_library"
	bl_label = "Remove Library"
	bl_options = {'REGISTER', 'INTERNAL'}
	bl_description = 'Remove a library by name'

	library_name : bpy.props.StringProperty(name="Library Name", default='')

	def execute(self, context):
		bpy.data.libraries.remove(bpy.data.libraries[self.library_name])
		return {'FINISHED'}

classes = (IMPORT_SCENE_OT_tila_import_blend, RemoveLibrary)

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