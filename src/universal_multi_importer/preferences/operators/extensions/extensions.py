import bpy
from ....bversion import AddonVersion
from ....preferences.formats import COMPATIBLE_FORMATS


class UI_UMIInstallExtension(bpy.types.Operator):
    bl_idname = "extensions.umi_install_extension"
    bl_label = "Install Extension"
    bl_options = {"REGISTER", "UNDO"}
    bl_description = "Install Extension and refresh UMI Dependencies list"

    pkg_id: bpy.props.StringProperty(name="Package ID", default="")
    repo_index: bpy.props.IntProperty(name="Repository Index", default=0)
    enable_on_install: bpy.props.BoolProperty(name="Enable On Install", default=True)

    @property
    def is_extension_installed(self):
        bpy.ops.preferences.addon_refresh()
        av = AddonVersion("bl_ext.blender_org." + self.pkg_id)
        return av.is_installed

    def execute(self, context):
        bpy.ops.extensions.package_install(
            "INVOKE_DEFAULT", pkg_id=self.pkg_id, repo_index=self.repo_index, enable_on_install=self.enable_on_install
        )

        # while not self.is_extension_installed:
        #     pass

        bpy.ops.preferences.umi_check_addon_dependency("INVOKE_DEFAULT")
        return {"FINISHED"}


class UI_UMIEnableAddon(bpy.types.Operator):
    bl_idname = "preferences.umi_addon_enable"
    bl_label = "Enable Addon"
    bl_options = {"REGISTER", "UNDO"}
    bl_description = "Enable Addon and refresh UMI Dependencies list"

    module: bpy.props.StringProperty(name="Addon Name", default="")

    def execute(self, context):
        assert self.module in COMPATIBLE_FORMATS.all_valid_addons
        bpy.ops.preferences.addon_enable(module=self.module)
        bpy.ops.preferences.umi_check_addon_dependency()
        return {"FINISHED"}


classes = (UI_UMIInstallExtension, UI_UMIEnableAddon)


def register():

    from bpy.utils import register_class

    for cls in classes:
        register_class(cls)


def unregister():
    from bpy.utils import unregister_class

    for cls in reversed(classes):
        unregister_class(cls)
