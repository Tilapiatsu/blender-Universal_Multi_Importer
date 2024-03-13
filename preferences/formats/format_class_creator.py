import bpy
from . import COMPATIBLE_FORMATS

### from https://stackoverflow.com/questions/15247075/how-can-i-dynamically-create-derived-classes-from-a-base-class
# class BaseClass(object):
#     def __init__(self, classtype):
#         self._type = classtype

# def ClassFactory(name, argnames, BaseClass=BaseClass):
#     def __init__(self, **kwargs):
#         for key, value in kwargs.items():
#             # here, the argnames variable is the one passed to the
#             # ClassFactory call
#             if key not in argnames:
#                 raise TypeError("Argument %s not valid for %s" 
#                     % (key, self.__class__.__name__))
#             setattr(self, key, value)
#         BaseClass.__init__(self, name[:-len("Class")])
#     newclass = type(name, (BaseClass,),{"__init__": __init__})
#     return newclass

class FormatClassCreator():
	def __init__(self):
		self._classes = None

	incompatible_subclass = ['Operator', 'bpy_struct', 'object']
	
	@property
	def compatible_formats_class(self):
		if self._classes is None:
			self._classes = []
			for f in COMPATIBLE_FORMATS.formats:
				exec(f'from . import UMI_{f[0]}_module')
				import_module = eval(f'UMI_{f[0]}_module')
				for name, operator in f[1]['operator'].items():
					exec(f'from . import UMI_{f[0]}_{name}_settings')
					format_class = eval(f'UMI_{f[0]}_{name}_settings')

					if operator['module'] is not None:
						format_class = self.create_format_class_from_module(operator, format_class)
					else:
						format_class = self.create_format_class_from_operator(operator, format_class)

					self._classes.append(format_class)
					self._classes.append(import_module)

		return self._classes

	def create_format_class_from_module(self, f, format_class):
		print(f'create class from module {f["module"]}')
		format_module = getattr(bpy.types, f['module'], None)

		if format_module is None:
			print(f"Invalid module name passed : {f['module']}\nOr importer addon is disable")
			return None
		
		for sub_module in self.get_valid_submodule(format_module):
			self.create_format_class_hierarchy_from_module(f, format_class, sub_module)

		format_class.__annotations__['settings_imported'] = bpy.props.BoolProperty(name='Settings imported', default=False, options={'HIDDEN'})
		return format_class
	
	def create_format_class_hierarchy_from_module(self, f, format_class, format_module):

		if format_module is None:
			print(f"Invalid module name passed : {f['module']}\nOr importer addon is disable")
			return None
		
		format_annotations = getattr(format_module, "__annotations__", None)

		key_to_delete = []
		for k,v in format_annotations.items():
			try:
				v.keywords
			except AttributeError:
				continue
			
			if 'options' in v.keywords.keys():
				options = v.keywords['options']
			else:
				options = None

			if options == {'HIDDEN'}:
				key_to_delete.append(k)
				continue

			format_class.__annotations__[k] = v

		for k in key_to_delete:
			del format_annotations[k]

		return format_class

	def create_format_class_from_operator(self, f, format_class):
		print(f'create class from operator {f["command"]}')
		if 'import_settings' in f.keys() :
			# TODO : create a pointer to a settings for each g[0]
			for g in f['import_settings']:
				if not len(g):
					continue
				if not len(g[1].keys()):
					continue
				for k,v in g[1].items():
					command = f'{v["type"]}(name={v["name"]}, default={v["default"]}'
					
					if 'enum_items' in v.keys():
						command += f', items={v["enum_items"]}'
					if 'min' in v.keys():
						command += f', min={v["min"]}'
					if 'max' in v.keys():
						command += f', max={v["max"]}'
						
					command += f')'
					
					format_class.__annotations__[k] = eval(command)
		
		format_class.__annotations__['settings_imported'] = bpy.props.BoolProperty(name='Settings imported', default=False, options={'HIDDEN'})
		return format_class
	
	def get_valid_submodule(self, format_module):
		return [c for c in format_module.__mro__ if c.__name__ not in self.incompatible_subclass]

	def register_compatible_formats(self):
		for c in self.compatible_formats_class:
			if c is None:
				continue
			try:
				bpy.utils.register_class(c)
			except ValueError:
				pass
	
	def unregister_compatible_formats(self):
		for c in reversed(self.compatible_formats_class):
			if c is None:
				continue
			try:
				bpy.utils.unregister_class(c)
			except ValueError:
				pass
