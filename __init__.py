import bpy
from bpy_extras.io_utils import ImportHelper
from bpy_extras.wm_utils.progress_report import ProgressReport
import os
from os import path

bl_info = {
	"name" : "Universal Multi Importer",
	"author" : "Tilapiatsu",
	"description" : "",
	"blender" : (2, 93, 0),
	"location": "File > Import-Export",
	"warning" : "",
	"category": "Import-Export"
}

class TILA_universal_multi_importer(bpy.types.Operator, ImportHelper):
	bl_idname = "import_scene.tila_universal_multi_importer"
	bl_label = "TILA : Universal Multi Importer"
	bl_options = {'REGISTER', 'UNDO'}

	# Selected files
	files : bpy.props.CollectionProperty(type=bpy.types.PropertyGroup)
	create_collection_per_file : bpy.props.BoolProperty(name='Create collection per file', default=True)
	backup_file_after_import : bpy.props.BoolProperty(name='Backup file after each import', default=True)
	skip_already_imported_files : bpy.props.BoolProperty(name='Skip already imported files', default=True)
	save_file_after_import : bpy.props.BoolProperty(name='Save file after import', default=True)
	

	_timer = None
	thread = None
	progress = 0
	stop_early = False
	current_file_to_process = None
	processing = False
	compatible_formats = ['.obj']

	def recurLayerCollection(self, layerColl, collName):
		found = None
		if (layerColl.name == collName):
			return layerColl
		for layer in layerColl.children:
			found = self.recurLayerCollection(layer, collName)
			if found:
				return found


	def postImportCommand(self):
		bpy.ops.sculpt.tila_multires_rebuild_subdiv('INVOKE_DEFAULT')

	def modal(self, context, event):
		if event.type in {'RIGHTMOUSE', 'ESC'}:
			self.cancel(context)

			self.stop_early = True
			print('TILA : Import Canceled')

			return {'CANCELLED'}

		if event.type == 'TIMER':
			# if not self.thread.is_alive():
			if not self.processing and self.current_file_to_process is None and len(self.filepaths): # Import can start
				self.next_file()
				self.import_file(self.current_file_to_process)
			elif self.current_file_to_process is None and len(self.filepaths):
				self.processing = False
			elif self.current_file_number == self.number_of_file:
				if self.save_file_after_import:
					bpy.ops.wm.save_as_mainfile(filepath=self.current_blend_file, check_existing=False)

				print('TILA : Import Completed')
				return {'FINISHED'}

		return {'PASS_THROUGH'}

	def import_file(self, file):
		import time

		if self.stop_early:
			return

		self.processing = True

		filename = path.basename(path.splitext(file)[0])

		if self.skip_already_imported_files:
			if filename in bpy.data.collections:
				return
		
		print('TILA : Importing File {}/{} : {}'.format(self.current_file_number, self.number_of_file, filename))

		if self.create_collection_per_file:
			collection = bpy.data.collections.new(name=filename)
			self.root_collection.children.link(collection)
			
			root_layer_col = self.view_layer.layer_collection    
			layer_col = self.recurLayerCollection(root_layer_col, collection.name)
			self.view_layer.active_layer_collection = layer_col
		
		bpy.ops.import_scene.obj(filepath=file)
		
		self.postImportCommand()

		if self.backup_file_after_import:
			bpy.ops.wm.save_as_mainfile(filepath=self.blend_backup_file, check_existing=False, copy=True)

		time.sleep(.5)
		self.progress += self.number_of_file/100
		self.current_file_number += 1
		self.current_file_to_process = None

	def execute(self,context):
		self.current_blend_file = bpy.data.filepath

		if not path.exists(self.current_blend_file):
			print('Blender file not saved')
			self.save_file_after_import = False
			self.backup_file_after_import = False
		else:
			self.blend_backup_file = path.splitext(self.current_blend_file)[0] + "_bak" + path.splitext(self.current_blend_file)[1]
		
		self.folder = (os.path.dirname(self.filepath))
		self.filepaths = [path.join(self.folder, f.name) for f in self.files]
		self.filepaths.reverse()
		self.number_of_file = len(self.filepaths)

		print("{} compatible file(s) found".format(len(self.filepaths)))

		self.view_layer = bpy.context.view_layer
		self.root_collection = bpy.context.collection
		self.current_file_number = 1

		wm = context.window_manager
		self._timer = wm.event_timer_add(0.1, window=context.window)
		wm.modal_handler_add(self)
		return {'RUNNING_MODAL'}
	
	def next_file(self):
		self.current_file_to_process = self.filepaths.pop()

	def cancel(self, context):
		wm = context.window_manager
		wm.event_timer_remove(self._timer)

def menu_func_import(self, context):
	self.layout.operator(TILA_universal_multi_importer.bl_idname, text="Universal Multi Importer")

classes = (
	TILA_universal_multi_importer,
)

def register():
	for cls in classes:
		bpy.utils.register_class(cls)

	bpy.types.TOPBAR_MT_file_import.append(menu_func_import)

def unregister():
	bpy.types.TOPBAR_MT_file_import.remove(menu_func_import)

if __name__ == "__main__":
	register()