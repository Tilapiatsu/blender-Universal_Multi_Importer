import os
import bpy
from .logger import LoggerProgress
from .format_definition import FormatDefinition
import inspect
from .property_group import TILA_umi_import_settings


PRESET_FOLDER = os.path.join(os.path.dirname(__file__), 'Preset')
LOG = LoggerProgress('UMI')
FORMATS = [f for f in dir(FormatDefinition) if not f.startswith('__')]
SUCCESS_COLOR = (0.1, 1.0, 0.1)
CANCELLED_COLOR = (1.0, 0.4, 0.1)
SCROLL_OFFSET_INCREMENT = 50


class TILA_compatible_formats(object):
	for format in FORMATS:
		exec('{} = {}'.format(format, getattr(FormatDefinition, format)))
	
	def __init__(self):
		self._extensions = None
		self._operators = None
		self._module = None		
		# automatically gather format
		attributes = inspect.getmembers(TILA_compatible_formats, lambda a:not(inspect.isroutine(a)))
		self.formats = [a for a in attributes if (not(a[0].startswith('__') and a[0].endswith('__')) and isinstance(a[1], dict))]


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


COMPATIBLE_FORMATS = TILA_compatible_formats()

# function to register dynamically generated classes for each compatible formats
def register_import_setting_class():
	for f in COMPATIBLE_FORMATS.formats:
		cl_name = 'TILA_umi_{}_settings'.format(f[1]['name'])
		cl = eval(cl_name)
		exec('TILA_umi_import_settings.__annotations__["{}_import_settings"] = bpy.props.PointerProperty(type={})'.format(f[1]['name'], cl_name), {'bpy': bpy, 'TILA_umi_import_settings':TILA_umi_import_settings, cl_name:cl})
		
	TILA_umi_import_settings.umi_import_settings_registered = True
	

for f in COMPATIBLE_FORMATS.formats:
	exec(f'class TILA_umi_{f[1]["name"]}_settings(bpy.types.PropertyGroup):name: bpy.props.StringProperty(name="Import Setting Name", default="{f[1]["name"]}")')