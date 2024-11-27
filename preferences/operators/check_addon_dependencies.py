import bpy
from ..formats import COMPATIBLE_FORMATS
from ...umi_const import get_umi_settings
from ...bversion import AddonVersion

class UI_UMICheckAddonDependencies(bpy.types.Operator):
    bl_idname = "preferences.umi_check_addon_dependency"
    bl_label = "Check Addon Dependency"
    bl_options = {'REGISTER', 'UNDO'}
    bl_description = "Check if Importers addons are installed and enable"


    def execute(self, context):
        umi_settings = get_umi_settings()
        addon_dependencies = umi_settings.umi_addon_dependencies
        addon_dependencies.clear()

        for name in COMPATIBLE_FORMATS.all_formats.keys():
            for module_name, module  in COMPATIBLE_FORMATS.all_formats[name]['operator'].items():
                ad = addon_dependencies.add()

                ad.format_name      = name
                ad.module_name      = module_name

                addon_name          = module['addon_name'] if module['addon_name'] is not None else ''
                ad.addon_name       = addon_name

                av = AddonVersion(addon_name)
                ad.local_version    = str(av.local_version)
                ad.remote_version   = str(av.remote_version)
                ad.is_outdated      = av.is_outdated

                pkg_id              = module['pkg_id'] if module['pkg_id'] is not None else ''
                ad.pkg_id           = pkg_id

                pkg_url             = module['pkg_url'] if module['pkg_url'] is not None else ''
                ad.pkg_url          = pkg_url

                ad.is_extension     = COMPATIBLE_FORMATS.is_format_extension(name, module_name)
                ad.is_installed     = COMPATIBLE_FORMATS.is_format_installed(addon_name)
                ad.is_enabled       = COMPATIBLE_FORMATS.is_format_enabled(addon_name)

        umi_settings.umi_all_addon_dependencies_installed = COMPATIBLE_FORMATS.is_all_formats_installed
        umi_settings.umi_all_addon_dependencies_enabled = COMPATIBLE_FORMATS.is_all_formats_enabled
        umi_settings.umi_addon_dependency_need_reboot = COMPATIBLE_FORMATS.need_reboot

        return {'FINISHED'}

class UI_UMIInstallExtension(bpy.types.Operator):
    bl_idname = "extensions.umi_install_extension"
    bl_label = "Install Extension"
    bl_options = {'REGISTER', 'UNDO'}
    bl_description = "Install Extension and refresh UMI Dependencies list"

    pkg_id : bpy.props.StringProperty(name='Package ID', default='')
    repo_index : bpy.props.IntProperty(name='Repository Index', default=0)

    def execute(self, context):
        bpy.ops.extensions.package_install(pkg_id=self.pkg_id, repo_index=self.repo_index)
        bpy.ops.preferences.umi_check_addon_dependency()
        return {'FINISHED'}

class UI_UMIEnableAddon(bpy.types.Operator):
    bl_idname = "preferences.umi_addon_enable"
    bl_label = "Enable Addon"
    bl_options = {'REGISTER', 'UNDO'}
    bl_description = "Enable Addon and refresh UMI Dependencies list"

    module : bpy.props.StringProperty(name='Addon Name', default='')

    def execute(self, context):
        assert self.module in COMPATIBLE_FORMATS.all_valid_addons
        bpy.ops.preferences.addon_enable(module=self.module)
        bpy.ops.preferences.umi_check_addon_dependency()
        return {'FINISHED'}
    
classes = (UI_UMICheckAddonDependencies, UI_UMIInstallExtension, UI_UMIEnableAddon)

def register():
    
	from bpy.utils import register_class
	for cls in classes:
		register_class(cls)

def unregister():
	from bpy.utils import unregister_class
	for cls in reversed(classes):
		unregister_class(cls)