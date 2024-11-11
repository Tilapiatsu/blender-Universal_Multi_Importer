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

    _incompatible_subclass = ['Operator', 'bpy_struct', 'object']

    _property_type = {  'STRING': 'bpy.props.StringProperty',
                        'ENUM': 'bpy.props.EnumProperty',
                        'BOOLEAN': 'bpy.props.BoolProperty',
                        'FLOAT': 'bpy.props.FloatProperty',
                        'INT': 'bpy.props.IntProperty'}
    
    @property
    def compatible_formats_class(self):
        if self._classes is None:
            self._classes = {'classes':[], 'modules':[]}
            for f in COMPATIBLE_FORMATS.formats:
                try:
                    exec(f'from . import UMI_{f[0]}_module')
                except ImportError as e:
                    continue
                import_module = eval(f'UMI_{f[0]}_module')
                self._classes['modules'].append(import_module)
                for name, operator in f[1]['operator'].items():
                    exec(f'from . import UMI_{f[0]}_{name}_settings')
                    format_class = eval(f'UMI_{f[0]}_{name}_settings')

                    if operator['module'] is not None:
                        format_class = self.create_format_class_from_module(operator, format_class)
                    else:
                        format_class = self.create_format_class_from_operator(operator, format_class)
                    
                    self._classes['classes'].append(format_class)

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
            if f['import_settings'] is None:
                try:
                    properties = eval(f['command']).get_rna_type().properties
                except KeyError:
                    format_class.__annotations__['settings_imported'] = bpy.props.BoolProperty(name='Settings imported', default=False, options={'HIDDEN'})
                    return format_class
                # print(f['command'])
                for p in properties:
                    if p.is_hidden or p.is_readonly:
                        continue

                    if p.type == 'STRING':
                        command = self._property_type[p.type]
                        command += self.get_property_command_string(p)
                    elif p.type == 'ENUM':
                        command = self._property_type[p.type]
                        command += self.get_property_command_string(p, additionnal_props={'items': self.get_enum_items(p.enum_items)})
                    elif p.type == 'BOOLEAN':
                        command = self._property_type[p.type]
                        command += self.get_property_command_string(p)
                    elif p.type == 'FLOAT':
                        is_array = getattr(p, 'is_array', None)
                        if is_array: # Vector field
                            command = 'bpy.props.FloatVectorProperty'
                            command += self.get_property_command_string(p,  additionnal_props={ 'subtype': f'"{p.subtype}"',
                                                                                                'size':len(p.default_array),
                                                                                                'min': p.soft_min,
                                                                                                'max':p.soft_max,
                                                                                                'unit':f'"{p.unit}"'})
                        else:
                            command = self._property_type[p.type]
                            command += self.get_property_command_string(p,  additionnal_props={ 'subtype': f'"{p.subtype}"', 
                                                                                                'min': p.soft_min,
                                                                                                'max':p.soft_max,
                                                                                                'unit':f'"{p.unit}"'})
                    elif p.type == 'INT':
                        is_array = getattr(p, 'is_array', None)
                        if is_array: # Vector field
                            command = 'bpy.props.IntVectorProperty'
                            command += self.get_property_command_string(p,  additionnal_props={ 'subtype': f'"{p.subtype}"',
                                                                                                'size':len(p.default_array),
                                                                                                'min': p.soft_min,
                                                                                                'max':p.soft_max,
                                                                                                'unit':f'"{p.unit}"'})
                        else:
                            command = self._property_type[p.type]
                            command += self.get_property_command_string(p,  additionnal_props={'subtype': f'"{p.subtype}"', 
                                                                                                'min': p.soft_min,
                                                                                                'max':p.soft_max})
                    # print(p.identifier, " = ", command)
                    format_class.__annotations__[p.identifier] = eval(command)
            else:
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
                        if 'options' in v.keys():
                            command += f', options={v["options"]}'
                            
                        command += f')'
                        
                        format_class.__annotations__[k] = eval(command)
        
        format_class.__annotations__['settings_imported'] = bpy.props.BoolProperty(name='Settings imported', default=False, options={'HIDDEN'})
        return format_class
    
    def get_property_command_string(self, prop, additionnal_props:dict={}):
        command = f'(name="{prop.name}", description="{prop.description}"'
        if prop.type in ['ENUM', 'STRING']:
            command += f', default="{prop.default}"'
        elif prop.type in ['FLOAT', 'INT']:
            is_array = getattr(prop, 'is_array', None)
            if is_array:
                val = '['
                for i in range(len(prop.default_array)):
                    if i == 0:
                        val += f'{prop.default_array[i]}'
                    else:
                        val += f', {prop.default_array[i]}'
                val += ']'
                command += f', default={val}'
            else:
                command += f', default={prop.default}'
        else:
            command += f', default={prop.default}'
        if len(additionnal_props.keys()):
            for k,v in additionnal_props.items():
                command += f', {k}={v}'
        
        command += f')'
        return command
    
    def get_enum_items(self, enum):
        command = []
        for e in enum:
            command.append((e.identifier, e.name, f'{e.icon}'))
        return command

    def get_valid_submodule(self, format_module):
        return [c for c in format_module.__mro__ if c.__name__ not in self._incompatible_subclass]

    def register_compatible_formats(self):
        for c in self.compatible_formats_class['classes']:
            if c is None:
                continue
            try:
                bpy.utils.register_class(c)
            except ValueError:
                continue

        for c in self.compatible_formats_class['modules']:
            if c is None:
                continue
            try:
                bpy.utils.register_class(c)
            except ValueError:
                continue
    
    def unregister_compatible_formats(self):
        for c in reversed(self.compatible_formats_class['classes']):
            if c is None:
                continue
            try:
                bpy.utils.unregister_class(c)
            except ValueError:
                continue

        for c in reversed(self.compatible_formats_class['modules']):
            if c is None:
                continue
            try:
                bpy.utils.unregister_class(c)
            except ValueError:
                continue
        
