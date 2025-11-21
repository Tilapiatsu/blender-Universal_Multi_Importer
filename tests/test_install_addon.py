# Unit testing template for Blender add-ons
# Copyright (C) 2025 Spencer Magnusson

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import unittest
import importlib.util

class TestAddon(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Install add-on"""
        from tests.scripts import get_script
        from tests.manifest_info import get_manifest_info

        zip_main = get_script('zip_addon').zip_main

        manifest = get_manifest_info()
        cls.zip_path = zip_main(manifest['id'])
        if cls.zip_path is None:
            raise Exception('Failed to create zip file')

        import bpy
        bpy.ops.preferences.addon_install(filepath=cls.zip_path)
        bpy.ops.preferences.addon_enable(module=manifest['id'])

    def setUp(self):
        """Run homefile, resetting the file"""
        import bpy
        bpy.ops.wm.read_homefile()

    def test_disable_enable(self):
        """Validate enabling or disabling the add-on"""
        from manifest_info import get_manifest_info
        manifest = get_manifest_info()
        try:
            import bpy
            bpy.ops.preferences.addon_disable(module=manifest['id'])
            bpy.ops.preferences.addon_enable(module=manifest['id'])
        except Exception as e:
            self.fail(str(e))

    def test_format_definition(self):
        """Check if all formats are registered correctly"""
        import bpy
        from manifest_info import get_manifest_info
        manifest = get_manifest_info()

        from universal_multi_importer.preferences.formats.format_definition import FormatDefinition
        fd = FormatDefinition()

        self.assertTrue(hasattr(fd, 'fbx'))

    def test_umi_properties(self):
        """Check if all addon settings are registered correctly"""
        import bpy
        from manifest_info import get_manifest_info
        manifest = get_manifest_info()

        addon_preferences = bpy.context.preferences.addons[manifest['id']].preferences

        self.assertTrue(hasattr(addon_preferences, 'umi_settings'))
        self.assertTrue(hasattr(addon_preferences.umi_settings, 'umi_addon_dependencies'))
        self.assertTrue(hasattr(addon_preferences.umi_settings, 'umi_all_addon_dependencies_installed'))
        self.assertTrue(hasattr(addon_preferences.umi_settings, 'umi_all_addon_dependencies_enabled'))
        self.assertTrue(hasattr(addon_preferences.umi_settings, 'umi_addon_dependency_need_reboot'))
        self.assertTrue(hasattr(addon_preferences.umi_settings, 'umi_batcher_is_processing'))
        self.assertTrue(hasattr(addon_preferences.umi_settings, 'umi_presets'))
        self.assertTrue(hasattr(addon_preferences.umi_settings, 'umi_format_import_settings'))
        self.assertTrue(hasattr(addon_preferences.umi_settings, 'umi_file_selection_started'))
        self.assertTrue(hasattr(addon_preferences.umi_settings, 'umi_file_selection_done'))
        self.assertTrue(hasattr(addon_preferences.umi_settings, 'umi_import_directory'))
        self.assertTrue(hasattr(addon_preferences.umi_settings, 'umi_current_item_index'))
        self.assertTrue(hasattr(addon_preferences.umi_settings, 'umi_global_import_settings'))
        self.assertTrue(hasattr(addon_preferences.umi_settings, 'umi_ready_to_import'))
        self.assertTrue(hasattr(addon_preferences.umi_settings, 'umi_file_selection'))
        self.assertTrue(hasattr(addon_preferences.umi_settings, 'umi_file_extension_selection_items'))
        self.assertTrue(hasattr(addon_preferences.umi_settings, 'umi_file_stat_selected_count'))
        self.assertTrue(hasattr(addon_preferences.umi_settings, 'umi_file_stat_selected_size'))
        self.assertTrue(hasattr(addon_preferences.umi_settings, 'umi_file_stat_selected_formats'))
        self.assertTrue(hasattr(addon_preferences.umi_settings, 'umi_file_selected_format_items'))
        self.assertTrue(hasattr(addon_preferences.umi_settings, 'umi_file_extension_selection'))
        self.assertTrue(hasattr(addon_preferences.umi_settings, 'umi_import_batch_settings'))
        self.assertTrue(hasattr(addon_preferences.umi_settings, 'umi_updating_batcher_variable'))
        self.assertTrue(hasattr(addon_preferences.umi_settings, 'umi_each_operators'))
        self.assertTrue(hasattr(addon_preferences.umi_settings, 'umi_current_format_setting_imported'))
        self.assertTrue(hasattr(addon_preferences.umi_settings, 'umi_imported_data'))
        self.assertTrue(hasattr(addon_preferences.umi_settings, 'umi_last_setting_to_get'))
        self.assertTrue(hasattr(addon_preferences.umi_settings, 'umi_current_format_setting_cancelled'))
        self.assertTrue(hasattr(addon_preferences.umi_settings, 'umi_file_format_current_settings'))

        self.assertTrue(hasattr(addon_preferences, 'umi_colors'))
        self.assertTrue(hasattr(addon_preferences.umi_colors, 'umi_cancelled_color'))
        self.assertTrue(hasattr(addon_preferences.umi_colors, 'umi_command_color'))
        self.assertTrue(hasattr(addon_preferences.umi_colors, 'umi_command_warning_color'))
        self.assertTrue(hasattr(addon_preferences.umi_colors, 'umi_error_color'))
        self.assertTrue(hasattr(addon_preferences.umi_colors, 'umi_import_color'))
        self.assertTrue(hasattr(addon_preferences.umi_colors, 'umi_info_color'))
        self.assertTrue(hasattr(addon_preferences.umi_colors, 'umi_success_color'))
        self.assertTrue(hasattr(addon_preferences.umi_colors, 'umi_warning_color'))

    def test_addon_panel_exists(self):
        """Check if add-on panel exists"""
        import bpy
        self.assertTrue(hasattr(bpy.types, 'OBJECT_PT_test'))

    def test_addon_operator(self):
        """Check for and run add-on operator"""
        import bpy
        bpy.ops.object.test()

    @classmethod
    def tearDownClass(cls):
        """Uninstall add-on"""
        import bpy
        from manifest_info import get_manifest_info
        manifest = get_manifest_info()

        bpy.ops.preferences.addon_disable(module=manifest['id'])

        import os
        import shutil
        os.unlink(cls.zip_path)

        # get folder of addon_testing, remove folder
        # import addon_testing
        # installed_addon_folder = os.path.dirname(addon_testing.__file__)
        # print('Removing ' + installed_addon_folder + '...')
        # shutil.rmtree(installed_addon_folder)