import bpy
from .constant import COMPATIBLE_FORMATS


class TILA_umi_format_handler(object):
	import_format : bpy.props.StringProperty(name='Import Format', default="", options={'HIDDEN'},)

	def __init__(self, import_format, context):
		self._format = None
		self._format_name = None
		self._format_settings = None
		self._format_class = None
		self._format_annotations = None
		self._format_settings_dict = None
		self.import_format = import_format
		self.context = context

	@property
	def format(self):
		if self._format is None:
			self._format = getattr(COMPATIBLE_FORMATS, self.import_format)

		return self._format

	@property
	def format_name(self):
		if self._format_name is None:
			self._format_name = self.format['name']

		return self._format_name

	@property
	def format_class(self):
		if self._format_class is None:
			self._format_class = eval('TILA_umi_{}_settings'.format(self.format_name))
		
		return self._format_class

	@property
	def format_annotations(self):
		if self._format_annotations is None:
			self._format_annotations = getattr(self.format_settings, "__annotations__", None)
		
		return self._format_annotations

	@property
	def format_is_imported(self):
		return self.format_settings.settings_imported

	@property
	def format_settings(self):
		if self._format_settings is None:
			self._format_settings = eval("context.scene.umi_settings.umi_import_settings.{}_import_settings".format(self.format_name), {'context':self.context})
		
		return self._format_settings

	@property
	def format_settings_dict(self):
		if self._format_settings_dict is None:
			d = {}
			for k,v in self.format_settings.items():
				d[k] = getattr(self.format_settings, k)
				if isinstance(d[k], str):
					d[k] = '"{}"'.format(d[k])

			self._format_settings_dict = d


		return self._format_settings_dict