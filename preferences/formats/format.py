from typing import Union, Optional, Dict


def axis():
    return [
            ("X", "X", "X"),
            ("Y", "Y", "Y"),
            ("Z", "Z", "Z"),
            ("-X", "-X", "-X"),
            ("-Y", "-Y", "-Y"),
            ("-Z", "-Z", "-Z")
            ]


class FormatImportSetting:
    def __init__(self, settings:Optional[Dict[str, Dict[str, Dict]]]=None) -> None:
        if settings is None:
            self.settings = {}
            return

        self.settings = settings


    def add_section(self, name:str) -> dict:
        '''
        Add a new section in the settings
        '''
        if name in self.settings.keys():
            return self.settings[name]

        self.settings[name] = {}

        return self.settings[name]


    def add_set_settings(self, section_name:str, settings:Union[Dict[str, Dict]]):
        '''
        Add or replace a dict of setting in the given section
        '''
        section = self.add_section(section_name)

        for k,v in settings.items():
            section[k] = v


    def add_set_boolean_setting(self,
                                section_name:str,
                                name:str,
                                display_name:str,
                                default:bool,
                                options:Optional[set]=None) -> None:

        if options is None:
            options = set()

        self.add_set_settings(section_name,
                              {name:{'type':'bpy.props.BoolProperty',
                                     'name':f'"{display_name}"',
                                     'default':default,
                                     'options':options}})


    def add_set_float_setting(self,
                              section_name:str,
                              name:str,
                              display_name:str,
                              default:float,
                              options:Optional[set]=None) -> None:

        if options is None:
            options = set()

        self.add_set_settings(section_name,
                              {name:{'type':'bpy.props.FloatProperty',
                                     'name':f'"{display_name}"',
                                     'default':default,
                                     'options':options}})


    def add_set_int_setting(self,
                            section_name:str,
                            name:str,
                            display_name:str,
                            default:int,
                            options:Optional[set]=None) -> None:

        if options is None:
            options = set()

        self.add_set_settings(section_name,
                              {name:{'type':'bpy.props.IntProperty',
                                     'name':f'"{display_name}"',
                                     'default':default,
                                     'options':options}})


    def add_set_string_setting(self,
                            section_name:str,
                            name:str,
                            display_name:str,
                            default:str,
                            options:Optional[set]=None) -> None:

        if options is None:
            options = set()

        self.add_set_settings(section_name,
                              {name:{'type':'bpy.props.StringProperty',
                                     'name':f'"{display_name}"',
                                     'default':f'"{default}"',
                                     'options':options}})


    def add_set_enum_setting(self,
                             section_name:str,
                             name:str,
                             display_name:str,
                             default:Union[str,set],
                             enum_items:tuple,
                             options:Optional[set]=None) -> None:

        if options is None:
            options = set()

        self.add_set_settings(section_name,
                              {name:{'type':'bpy.props.EnumProperty',
                                     'name':f'"{display_name}"',
                                     'default':default if isinstance(default, set) else f'"{default}"',
                                     'enum_items':enum_items,
                                     'options':options}})


    def as_dict(self):
        return self.settings


class FormatOperator:
    def __init__(self,
                 name:str,
                 command:str,
                 supported_version:str,
                 module:Optional[str]=None,
                 addon_name:Optional[str]=None,
                 pkg_id:Optional[str]=None,
                 pkg_url:Optional[str]=None,
                 import_settings:Optional[FormatImportSetting]=None):

        self.name = name
        self.command = command
        self.supported_version = supported_version
        self.module = module
        self.addon_name = addon_name
        self.pkg_id = pkg_id
        self.pkg_url = pkg_url
        self.import_settings = import_settings


    def as_dict(self):
        '''
        returns the representation of the Format Operator as a dict
        '''
        return {self.name:{ 'command':self.command,
                            'supported_version':self.supported_version,
                            'addon_name':self.addon_name,
                            'module':self.module,
                            'pkg_id':self.pkg_id,
                            'pkg_url':self.pkg_url,
                            'import_settings':self.import_settings.as_dict() if isinstance(self.import_settings, FormatImportSetting) else None}}


class FormatOperators:
    def __init__(self, operator:Union[FormatOperator, tuple[str, dict]]):
        if isinstance(operator, FormatOperator):
            self.operators = {operator.name: operator}

        elif isinstance(operator, dict[str:dict]):
            self.operators = {operator[0]:FormatOperator(   operator[0],
                                                            operator[1]['command'],
                                                            operator[1]['supported_version'],
                                                            module=operator[1]['module'],
                                                            addon_name=operator[1]['addon_name'],
                                                            pkg_id=operator[1]['pkg_id'],
                                                            pkg_url=operator[1]['url'],
                                                            import_settings=operator[1]['import_settings'])}

        else:
            raise ValueError(f'operator parameters should NOT be of type "{type(operator)}" \n It should be either tuple[str, dict] or FormatOperator type')


    def add_operator(self, operator:Union[FormatOperator,tuple[str, dict]]):
        if isinstance(operator, FormatOperator):
            self.operators[operator.name] = operator

        elif isinstance(operator, dict[str:dict]):
            self.operators[operator[0]] = FormatOperator(   operator[0],
                                                            operator[1]['command'],
                                                            operator[1]['supported_version'],
                                                            module=operator[1]['module'],
                                                            addon_name=operator[1]['addon_name'],
                                                            pkg_id=operator[1]['pkg_id'],
                                                            pkg_url=operator[1]['url'],
                                                            import_settings=operator[1]['import_settings'])

        else:
            raise ValueError(f'operator parameters should NOT be of type "{type(operator)}" \n It should be either tuple[str, dict] or FormatOperator type')


    def as_dict(self):
        '''
        returns the representation of Format Operators as a dict
        '''

        d = {}

        for v in self.operators.values():
            d.update(v.as_dict())

        return d


class Format:
    '''
    Defines the data structure of a format
    '''

    def __init__(self,
                 name:str,
                 ext:list[str],
                 operators:FormatOperators,
                 ignore:Optional[list[str]]=None,
                 generate_filter_glob:bool=False) -> None:

        self.name = name
        self.ext = ext
        self.operators = operators

        if ignore is None:
            ignore = ['files', 'directory']

        self.ignore = ignore
        self.generate_filter_glob = generate_filter_glob


    def as_dict(self):
        '''
        returns the representation of the format as a dict
        '''

        return {'name':self.name,
                'ext':self.ext,
                'operator':self.operators.as_dict(),
                'ignore':self.ignore,
                'generate_filter_glob':self.generate_filter_glob}

