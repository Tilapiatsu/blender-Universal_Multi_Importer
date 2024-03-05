from .format_definition import FormatDefinition
from . import FORMATS
from ..logger import LOG
import inspect

class CompatibleFormats():
	for format in FORMATS:
		exec('{} = {}'.format(format, getattr(FormatDefinition, format)))
	
	def __init__(self):
		self._extensions = None
		self._extensions_string = None
		self._operators = None
		self._module = None		
		# automatically gather format
		attributes = inspect.getmembers(CompatibleFormats, lambda a:not(inspect.isroutine(a)))
		self.formats = [a for a in attributes if (not(a[0].startswith('__') and a[0].endswith('__')) and isinstance(a[1], dict))]
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
	
	def draw_format_settings(self, format_name, operator, module_name, layout):
		exec(f'from .panels import panel_{format_name}')
		module = eval(f'panel_{format_name}.IMPORT_SCENE_{format_name.upper()}Settings')
		module.draw(operator, module_name, layout)