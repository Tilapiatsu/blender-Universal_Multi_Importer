import bpy
from universal_multi_importer.preferences.formats import COMPATIBLE_FORMATS
from universal_multi_importer.preferences.formats.format import FormatOperator

### from https://stackoverflow.com/questions/15247075/how-can-i-dynamically-create-derived-classes-from-a-base-class
class BaseClass(object):
    def __init__(self, classtype):
        self._type = classtype

def ClassFactory(name, argnames, BaseClass=BaseClass):
    def __init__(self, *args, **kwargs):
        BaseClass.__init__(self, *args, **kwargs)

    newclass = type(name, (BaseClass,), {"__init__": __init__})
    return newclass

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
            from . import modules
            for f in COMPATIBLE_FORMATS.formats:
                if f'{f.name}_module' not in modules:
                    continue

                import_module = modules[f'{f.name}_module']
                self._classes['modules'].append(import_module)

                for name, operator in f.operators.operators.items():
                    if f'{f.name}_{name}_settings' not in modules:
                        continue

                    format_class = modules[f'{f.name}_{name}_settings']

                    if operator.module is not None:
                        format_class = self.create_format_class_from_module(operator, format_class)
                    else:
                        format_class = self.create_format_class_from_operator(operator, format_class)

                    self._classes['classes'].append(format_class)

        return self._classes

    def create_format_class_from_module(self, f: FormatOperator, format_class):
        print(f'UMI : create class from module {f.module}')
        format_module = getattr(bpy.types, f.module, None)

        if format_module is None:
            print(f"UMI : Invalid module name passed : {f.module}\nOr importer addon is disable")
            return None

        for sub_module in self.get_valid_submodule(format_module):
            self.create_format_class_hierarchy_from_module(f, format_class, sub_module)

        format_class.__annotations__['settings_imported'] = bpy.props.BoolProperty(name='Settings imported', default=False, options={'HIDDEN'})
        format_class.__annotations__['addon_name'] = bpy.props.StringProperty(name='Addon Name', default=f.addon_name if f.addon_name else '')
        format_class.__annotations__['supported_version'] = bpy.props.StringProperty(name='Addon Name', default=f.supported_version)
        return format_class

    def create_format_class_hierarchy_from_module(self, f, format_class, format_module):
        if format_module is None:
            print(f"UMI : Invalid module name passed : {f.module}\nOr importer addon is disable")
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

    def create_format_class_from_operator(self, f: FormatOperator, format_class):
        print(f'UMI : create class from operator {f.command}')

        if f.import_settings is None:
            try:
                properties = eval(f.command).get_rna_type().properties
            except KeyError:
                format_class.__annotations__['settings_imported'] = bpy.props.BoolProperty(name='Settings imported', default=False, options={'HIDDEN'})
                format_class.__annotations__['addon_name'] = bpy.props.StringProperty(name='Addon Name', default=f.addon_name if f.addon_name else '')
                format_class.__annotations__['supported_version'] = bpy.props.StringProperty(name='Addon Name', default=f.supported_version)
                return format_class

            for p in properties:
                if p.is_hidden or p.is_readonly:
                    continue

                if p.type == 'STRING':
                    command = self._property_type[p.type]
                    command += self.get_property_command_string(p, default_values=f.default_values)
                elif p.type == 'ENUM':
                    command = self._property_type[p.type]
                    command += self.get_property_command_string(p, additionnal_props={'items': self.get_enum_items(p.enum_items)}, default_values=f.default_values)
                elif p.type == 'BOOLEAN':
                    command = self._property_type[p.type]
                    command += self.get_property_command_string(p, default_values=f.default_values)
                elif p.type == 'FLOAT':
                    is_array = getattr(p, 'is_array', None)
                    if is_array: # Vector field
                        command = 'bpy.props.FloatVectorProperty'
                        command += self.get_property_command_string(p,  additionnal_props={ 'subtype': f'"{p.subtype}"',
                                                                                            'size':len(p.default_array),
                                                                                            'min': p.soft_min,
                                                                                            'max':p.soft_max,
                                                                                            'unit':f'"{p.unit}"',
                                                                                            'precision':p.precision},
                                                                        default_values=f.default_values)
                    else:
                        command = self._property_type[p.type]
                        command += self.get_property_command_string(p,  additionnal_props={ 'subtype': f'"{p.subtype}"',
                                                                                            'min': p.soft_min,
                                                                                            'max':p.soft_max,
                                                                                            'unit':f'"{p.unit}"',
                                                                                            'precision':p.precision},
                                                                        default_values=f.default_values)
                elif p.type == 'INT':
                    is_array = getattr(p, 'is_array', None)
                    if is_array: # Vector field
                        command = 'bpy.props.IntVectorProperty'
                        command += self.get_property_command_string(p,  additionnal_props={ 'subtype': f'"{p.subtype}"',
                                                                                            'size':len(p.default_array),
                                                                                            'min': p.soft_min,
                                                                                            'max':p.soft_max,
                                                                                            'unit':f'"{p.unit}"'},
                                                                        default_values=f.default_values)
                    else:
                        command = self._property_type[p.type]
                        command += self.get_property_command_string(p,  additionnal_props={'subtype': f'"{p.subtype}"',
                                                                                            'min': p.soft_min,
                                                                                            'max':p.soft_max},
                                                                        default_values=f.default_values)
                format_class.__annotations__[p.identifier] = eval(command)
        else:
            # TODO : create a pointer to a settings for each g[0]
            for s in f.import_settings.settings.values():
                if len(s.keys()) == 0:
                    continue
                for k,v in s.items():
                    command = f'{v["type"]}(name={v["name"]}, default={v["default"]}'

                    if 'enum_items' in v.keys():
                        command += f', items={v["enum_items"]}'
                    if 'min' in v.keys():
                        command += f', min={v["min"]}'
                    if 'max' in v.keys():
                        command += f', max={v["max"]}'
                    if 'options' in v.keys():
                        command += f', options={v["options"]}'

                    command += ')'

                    format_class.__annotations__[k] = eval(command)

        format_class.__annotations__['settings_imported'] = bpy.props.BoolProperty(name='Settings imported', default=False, options={'HIDDEN'})
        format_class.__annotations__['addon_name'] = bpy.props.StringProperty(name='Addon Name', default=f.addon_name if f.addon_name else '')
        format_class.__annotations__['supported_version'] = bpy.props.StringProperty(name='Addon Name', default=f.supported_version)
        format_class.__annotations__['forced_properties'] = bpy.props.StringProperty(name='Forced Properties', default=f"{f.forced_properties}")
        return format_class

    def get_property_command_string(self, prop, additionnal_props:dict={}, default_values:dict={}):
        command = f'(name="{prop.name}", description="{prop.description}"'
        default_value = prop.default if prop.identifier not in default_values.keys() else default_values[prop.identifier]
        if prop.type in ['ENUM', 'STRING']:
            command += f', default="{default_value}"'
        elif prop.type in ['FLOAT', 'INT']:
            is_array = getattr(prop, 'is_array', None)
            if is_array:
                if prop.name not in default_values.keys():
                    default_value = '['
                    for i in range(len(prop.default_array)):
                        if i == 0:
                            default_value += f'{prop.default_array[i]}'
                        else:
                            default_value += f', {prop.default_array[i]}'
                    default_value += ']'
                command += f', default={default_value}'
            else:
                command += f', default={default_value}'
        else:
            command += f', default={default_value}'
        if len(additionnal_props.keys()):
            for k,v in additionnal_props.items():
                command += f', {k}={v}'

        command += ')'
        return command

    def get_enum_items(self, enum):
        command = []
        for e in enum:
            command.append((e.identifier, e.name, e.description))
        return command

    def get_valid_submodule(self, format_module):
        return [c for c in format_module.__mro__ if c.__name__ not in self._incompatible_subclass]

    def register_compatible_formats(self):
        for c in self.compatible_formats_class['classes']:
            if c is None:
                continue
            try:
                bpy.utils.register_class(c)
            except [ValueError, TypeError] as e:
                print(e, c)
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
