
import unittest
import importlib.util

class TestFormatDefinition(unittest.TestCase):
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
        manifest = get_manifest_info()
        bpy.ops.preferences.addon_install(filepath=cls.zip_path)
        bpy.ops.preferences.addon_enable(module=manifest['id'])


    def test_format_definition(self):
        """Check if all formats are registered correctly"""
        import bpy
        from universal_multi_importer.preferences.formats.format_definition import FormatDefinition

        self.assertTrue(hasattr(FormatDefinition, 'fbx'))
    

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