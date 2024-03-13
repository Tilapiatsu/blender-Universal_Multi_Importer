import bpy
from .format_definition import FormatDefinition
from . import FORMATS
from ...logger import LOG
from .panels.presets import format_preset
import inspect

class CompatibleFormats():
	for format in FORMATS:
		exec('{} = {}'.format(format, getattr(FormatDefinition, format)))
	
	def __init__(self):
		self._extensions = None
		self._extensions_string = None
		self._operators = None
		self._module = None		
		self._filename_ext = None
		self._filter_glob = None
		# automatically gather format
		self.formats = CompatibleFormats.get_formats()
		self.formats_dict = {a[0]:a[1] for a in self.formats}


	@property
	def extensions(self):
		if self._extensions is None:
			extensions = []
			for f in self.formats:
				if isinstance(f[1], dict):
					extensions = extensions + f[1]['ext']
			self._extensions = extensions
		return self._extensions
	
	@property
	def extensions_string(self):
		if self._extensions_string is None:
			self._extensions_string = ';'.join(self.extensions)
		return self._extensions_string

	@property
	def operators(self):
		if self._operators is None:
			operators = []
			for f in self.formats:
				if isinstance(f[1], dict):
					operators.append(f[1]['operator'])
			self._operators = operators
		return self._operators
	
	@property
	def module(self):
		if self._module is None:
			module = []
			for f in self.formats:
				if isinstance(f[1], dict):
					module.append(f[1]['module'])
			self._module = module
		return self._module
	
	@property
	def filename_ext(self):
		if self._filename_ext is None:
			self._filename_ext = {e for e in self.extensions}

		return self._filename_ext
	
	@property
	def filter_glob(self):
		if self._filter_glob is None:
			extensions = ['*' + e for e in self.extensions]
			self._filter_glob = ';'.join(extensions)

		return self._filter_glob

	@classmethod
	def get_formats(cls):
		attributes = inspect.getmembers(CompatibleFormats, lambda a:not(inspect.isroutine(a)))
		formats = [a for a in attributes if (not(a[0].startswith('__') and a[0].endswith('__')) and isinstance(a[1], dict))]

		valid_formats = []
		for f in formats:
			for o in f[1]['operator'].values():
				if o['module'] is None:
					# Check Command
					try:
						eval(o['command'])
					except:
						continue
					valid_formats.append(f)
				else:
					# Check Module
					if o['module'] not in dir(bpy.types):
						continue
					valid_formats.append(f)

		return valid_formats
	
	def get_format_from_extension(self, ext):
		if ext.lower() not in self.extensions:
			# raise Exception("extension '{}' is not supported".format(ext))
			message = f"extension '{ext}' is not supported"
			LOG.error(message)
			return None
		else:
			for f in self.formats:
				if  ext.lower() in f[1]['ext']:
					return f[1]
	
	def get_operator_name_from_extension(self, ext):
		format = self.get_format_from_extension(ext)
		if format is None:
			return None
		formats = {}
		for k,v in format['operator'].items():
			formats[k] = v
		
		return formats
	
	def draw_format_settings(self, context, format_name, operator, module_name, layout):
		exec(f'from .panels import panel_{format_name}')
		module = eval(f'panel_{format_name}.IMPORT_SCENE_{format_name.upper()}Settings')
		self.layout = layout
		
		format_preset.panel_func(self, context)

		layout.separator()
		layout.separator()
	
		module.draw(self, operator, module_name, layout)