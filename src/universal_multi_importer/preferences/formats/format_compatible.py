import inspect
from typing import Union, Optional, Dict
import bpy
import addon_utils
from universal_multi_importer.preferences.formats.format_definition import FormatDefinition
from universal_multi_importer.preferences.formats import FORMATS
from universal_multi_importer.preferences.formats.format import Format
from universal_multi_importer.logger import LOG
from universal_multi_importer.preferences.formats.panels import get_panels
from universal_multi_importer.preferences.formats.panels.presets import format_preset
from universal_multi_importer.bversion import AddonVersion
from universal_multi_importer.bversion.version.version import Version

class CompatibleFormats(object):

    def __init__(self):
        self._all_formats = {}
        for f in FORMATS:
            exec(f'self._all_formats["{f}"] = Format', {'self': self, 'Format': getattr(FormatDefinition, f)})
        self._extensions = None
        self._extensions_string = None
        self._operators = None
        self._module = None
        self._filename_ext = None
        self._filter_glob_extensions = None
        self._filter_glob = None
        # automatically gather format
        self.formats = self.get_formats()
        self.formats_dict: dict[str: Format]= {f.name:f for f in self.formats}


    def is_format_installed(self, addon_name):
        return addon_name in self.installed_addons


    def is_format_enabled(self, addon_name):
        return addon_name in self.enabled_addons


    def is_format_extension(self, format_name, module):
        if format_name not in self.all_formats:
            return False
        return self.all_formats[format_name].operators.operators[module].pkg_id is not None


    def get_format_extension_url(self, format_name, module):
        if self.is_format_extension(format_name, module):
            return self.all_formats[format_name].operators.operators[module].pkg_url
        else:
            return None


    def get_format_supported_version(self, format_name, module) -> Version:
        if self.is_format_extension(format_name, module):
            return Version(self.all_formats[format_name].operators.operators[module].supported_version)
        else:
            return Version((0, 0, 0))


    def get_format_from_addon_name(self, addon_name):
        result_format = None
        for f in self.all_formats.values():
            for m in f.operators.operators.values():
                if m.addon_name == addon_name:
                    return m
        return result_format


    @property
    def all_valid_addons(self):
        all_valid_addons = []
        for f in self.all_formats.values():
            for module in f.operators.operators.values():
                all_valid_addons.append(module.addon_name)

        return all_valid_addons


    @property
    def valid_installed_addons(self):
        return [a for a in self.installed_addons if a in self.all_valid_addons]


    @property
    def installed_addons(self):
        # return [addon.module for addon in bpy.context.preferences.addons]
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

            supported_version = Version(self.get_format_from_addon_name(a).supported_version)

            av = AddonVersion(a)

            if av.local_version < supported_version:
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
                LOG.debug(f'{a} is not enabled')
                break

        return valid


    @property
    def need_reboot(self):
        from . import modules
        for f in self.all_formats.values():
            for name in f.operators.operators.keys():
                if f'{f.name}_{name}_settings' not in modules.keys():
                    return True
        return False


    @property
    def extensions(self):
        if self._extensions is None:
            extensions = []
            for f in self.formats:
                extensions = extensions + f.ext
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
                operators.append(f.operators.operators)
            self._operators = operators
        return self._operators


    @property
    def module(self):
        if self._module is None:
            module = []
            for f in self.formats:
                for m in f.operators.operators.values():
                    if m.module is None:
                        continue
                    module.append(m.module)
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
                if not self.is_format_valid(f.name):
                    continue
                if isinstance(f.operators.operators, dict):
                    if not f.generate_filter_glob:
                        continue
                    filter_glob_extensions = filter_glob_extensions + f.ext
            self._filter_glob_extensions = filter_glob_extensions
        return self._filter_glob_extensions


    @property
    def filter_glob(self):
        if self._filter_glob is None:
            extensions = ['*' + e for e in self.filter_glob_extensions]
            self._filter_glob = ';'.join(extensions)

        return self._filter_glob


    @property
    def all_formats(self) -> dict[str: Format]:
        return self._all_formats


    @property
    def all_registered_formats(self) -> dict[str: Format]:
        attributes = inspect.getmembers(CompatibleFormats, lambda a:not(inspect.isroutine(a)))
        formats = [a for a in attributes if (not(a[0].startswith('__') and a[0].endswith('__')) and isinstance(a[1], Format))]

        all_formats = {a[0]:a[1] for a in formats}
        return all_formats


    def get_formats(self) -> list[Format]:
        valid_formats = []
        for f in self.all_formats.values():
            op = {}
            new_f = f
            assigned = []
            for n,o in f.operators.operators.items():
                if o.module is None:
                    # Check Command
                    try:
                        eval(o.command).__repr__()
                    except:
                        assigned.append(False)
                        print(o.command, 'not found')
                        continue

                    op[n] = f.operators.operators[n]
                else:
                    # Check Module
                    if o.module not in dir(bpy.types):
                        assigned.append(False)
                        print(o.module, 'not in bpy.types')
                        continue

                    op[n] = f.operators.operators[n]

            # check if at least one module succeeded
            if len(assigned) < len(f.operators.operators.keys()):
                new_f.operators.operators = op
                valid_formats.append(new_f)

        return valid_formats


    def is_import_objects(self, format_name: str, module_name: str ) -> bool:
        if format_name not in self.all_formats:
            return False
        else:
            if module_name not in self.all_formats[format_name].operators.operators:
                return False
        return self.all_formats[format_name].operators.operators[module_name].import_objects


    def is_import_data(self, format_name: str, module_name: str ) -> bool:
        if format_name not in self.all_formats:
            return False
        else:
            if module_name not in self.all_formats[format_name].operators.operators:
                return False
        return self.all_formats[format_name].operators.operators[module_name].import_data


    def get_format_from_name(self, name: str) -> Format:
        if name not in self.all_formats.keys():
            return None
        else:
            return self.all_formats[name]


    def get_format_from_extension(self, ext):
        if ext.lower() not in self.extensions:
            # raise Exception("extension '{}' is not supported".format(ext))
            message = f"extension '{ext}' is not supported"
            LOG.error(message)
            return None
        else:
            for f in self.formats:
                if  ext.lower() in f.ext:
                    return f


    def get_operator_name_from_extension(self, ext):
        format = self.get_format_from_extension(ext)
        if format is None:
            return None
        formats = {}
        for k,v in format.operators.operators.items():
            formats[k] = v

        return formats


    def get_default_values(self, format_name: str, module_name: str) -> dict:
        if format_name not in self.all_formats:
            return {}
        else:
            if module_name not in self.all_formats[format_name].operators.operators:
                return {}
        return self.all_formats[format_name].operators.operators[module_name].default_values


    def is_format_valid(self, format):
        if format not in self.formats_dict.keys():
            return False

        operators = self.formats_dict[format].operators.operators

        for v in operators.values():
            try:
                eval(v.command).__repr__()
                return True
            except AttributeError:
                continue

        return False


    def draw_format_settings(self, context, format_name, operator, module_name, layout):
        module = get_panels(format_name)
        self.layout = layout

        format_preset.panel_func(self, context)

        layout.separator()
        layout.separator()

        module.draw(self, operator, module_name, layout)