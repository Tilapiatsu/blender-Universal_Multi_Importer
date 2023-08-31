import bpy
from .constant import COMPATIBLE_FORMATS

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

class TILA_format_class_creator(object):
	def __init__(self):
		self._classes = None

	@property
	def compatible_formats_class(self):
		if self._classes is None:
			self._classes = []
			for f in COMPATIBLE_FORMATS.formats:
				if 'module' in f[1].keys():
					format_class = self.create_format_class_from_module(f[1])
				else:
					format_class = self.create_format_class_from_operator(f[1])

				self._classes.append(format_class)

		return self._classes

	def create_format_class_from_module(self, f):
		print(f'create class from module {f["module"]}')
		format_module = getattr(bpy.types, f['module'], None)
		if format_module is None:
			print(f"Invalid module name passed : {f['module']}\nOr importer addon is disable")
			return None
		format_annotations = getattr(format_module, "__annotations__", None)
		
		exec('from .constant import TILA_umi_{}_settings'.format(f['name']))
		format_class = eval('TILA_umi_{}_settings'.format(f['name']))
		key_to_delete = []
		for k,v in format_annotations.items():
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
		
		format_class.__annotations__['settings_imported'] = bpy.props.BoolProperty(name='Settings imported', default=False, options={'HIDDEN'})
		return format_class
	
	def create_format_class_from_operator(self, f):
		print(f'create class from operator {f["operator"]["default"]}')
		exec('from .constant import TILA_umi_{}_settings'.format(f['name']))
		format_class = eval('TILA_umi_{}_settings'.format(f['name']))

		if 'import_settings' in f.keys() :
			for g in f['import_settings']:
				for k,v in g[1].items():
					if 'enum_items' in v.keys():
						command = f'{v["type"]}(name={v["name"]}, default={v["default"]}, items={v["enum_items"]})'
					else:
						command = f'{v["type"]}(name={v["name"]}, default={v["default"]})'
					format_class.__annotations__[k] = eval(command)
		
		format_class.__annotations__['settings_imported'] = bpy.props.BoolProperty(name='Settings imported', default=False, options={'HIDDEN'})
		return format_class

	def register_compatible_formats(self):
		for c in self.compatible_formats_class:
			if c is None:
				continue
			bpy.utils.register_class(c)
	
	def unregister_compatible_formats(self):
		for c in reversed(self.compatible_formats_class):
			if c is None:
				continue
			bpy.utils.unregister_class(c)
