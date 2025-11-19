
import unittest

class TestFormatDefinition(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Install add-on"""
        from zip_addon import zip_main
        from manifest_info import get_manifest_info
        manifest = get_manifest_info()
        cls.zip_path = zip_main(manifest['id'])
        if cls.zip_path is None:
            raise Exception('Failed to create zip file')

        import bpy
        from manifest_info import get_manifest_info
        manifest = get_manifest_info()
        bpy.ops.preferences.addon_install(filepath=cls.zip_path)
        bpy.ops.preferences.addon_enable(module=manifest['id'])


    def test_format_definition(self):
        """Check if all formats are registered correctly"""
        import bpy
        from universal_multi_importer.preferences.formats.format_definition import FormatDefinition

        self.assertTrue(hasattr(FormatDefinition, 'fbx'))