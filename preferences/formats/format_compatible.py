import bpy, addon_utils
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
        self._filter_glob_extensions = None
        self._filter_glob = None
        # automatically gather format
        self.formats = CompatibleFormats.get_formats()
        self.formats_dict = {a[0]:a[1] for a in self.formats}

    def is_format_installed(self, addon_name):
        return addon_name in self.installed_addons
    
    def is_format_enabled(self, addon_name):
        return addon_name in self.enabled_addons

    def is_format_extension(self, format_name, module):
        return self.all_formats[format_name]['operator'][module]['pkg_id'] != None

    @property
    def all_valid_addons(self):
        all_valid_addons = []
        for f in self.all_formats.values():
            for module in f['operator'].values():
                # if module['addon_name'] is None:
                #     continue
                all_valid_addons.append(module['addon_name'])

        return all_valid_addons

    @property
    def valid_installed_addons(self):
        return [a for a in self.installed_addons if a in self.all_valid_addons]

    @property
    def installed_addons(self):
        return [a.__name__ for a in addon_utils.modules()]
    
    @property
    def enabled_addons(self):
        return list(bpy.context.preferences.addons.keys())

    @property
    def is_all_formats_installed(self):
        valid = True
        valid_installed_addons = self.valid_installed_addons
        for a in self.all_valid_addons:
            if a is None:
                continue

            if a not in valid_installed_addons:
                valid = False
                break

        return valid

    @property
    def is_all_formats_enabled(self):
        valid = True
        enabled_addons = self.enabled_addons
        for a in self.all_valid_addons:
            if a is None:
                continue

            if a not in enabled_addons:
                valid = False
                break

        return valid

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
    def filter_glob_extensions(self):
        if self._filter_glob_extensions is None:
            filter_glob_extensions = []
            for f in self.formats:
                if isinstance(f[1], dict):
                    if not f[1]['generate_filter_glob']:
                        continue
                    filter_glob_extensions = filter_glob_extensions + f[1]['ext']
            self._filter_glob_extensions = filter_glob_extensions
        return self._filter_glob_extensions
    
    @property
    def filter_glob(self):
        if self._filter_glob is None:
            extensions = ['*' + e for e in self.filter_glob_extensions]
            self._filter_glob = ';'.join(extensions)

        return self._filter_glob

    @property
    def all_formats(self):
        attributes = inspect.getmembers(CompatibleFormats, lambda a:not(inspect.isroutine(a)))
        formats = [a for a in attributes if (not(a[0].startswith('__') and a[0].endswith('__')) and isinstance(a[1], dict))]

        all_formats = {a[0]:a[1] for a in formats}
        return all_formats

    @classmethod
    def get_formats(cls):
        attributes = inspect.getmembers(CompatibleFormats, lambda a:not(inspect.isroutine(a)))
        formats = [a for a in attributes if (not(a[0].startswith('__') and a[0].endswith('__')) and isinstance(a[1], dict))]

        valid_formats = []
        for f in formats:
            op = {}
            new_f = f
            assigned = []
            for n,o in f[1]['operator'].items():
                if o['module'] is None:
                    # Check Command
                    try:
                        eval(o['command'])
                    except:
                        assigned.append(False)
                        print(o['command'], 'not found')
                        continue

                    op[n] = f[1]['operator'][n]
                else:
                    # Check Module
                    if o['module'] not in dir(bpy.types):
                        assigned.append(False)
                        print(o['module'], 'not in bpy.types')
                        continue

                    op[n] = f[1]['operator'][n]
            
            # check if at leas one modyle succeeded
            if len(assigned) < len(f[1]['operator'].keys()):
                new_f[1]['operator'] = op
                valid_formats.append(new_f)

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