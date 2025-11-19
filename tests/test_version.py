import unittest

class TestVersion(unittest.TestCase):
    def test_version(self):
        """Sanity check for Version format"""
        from universal_multi_importer.bversion.version import Version
        v1string = Version('4.5.23')
        v2string = Version('4.5.24')
        v3string = Version('4.4.24')
        v4string = Version('5.4.24')

        v1tuple = Version((4, 5, 23))
        v2tuple = Version((4, 5, 24))
        v3tuple = Version((4, 4, 24))
        v4tuple = Version((5, 4, 24))

        self.assertEqual(v1string.version, (4, 5, 23))
        self.assertEqual(v1string.as_float, 4.523)
        self.assertEqual(str(v1string), '4.5.23')

        self.assertEqual(v1tuple.version, (4, 5, 23))
        self.assertEqual(v1tuple.as_float, 4.523)
        self.assertEqual(str(v1tuple), '4.5.23')

        self.assertGreater(v2string, v1string)
        self.assertGreater(v2string, v3string)
        self.assertGreater(v4string, v3string)

        self.assertGreater(v2tuple, v1tuple)
        self.assertGreater(v2tuple, v3tuple)
        self.assertGreater(v4tuple, v3tuple)

        self.assertLess(v1string, v2string)
        self.assertLess(v3string, v2string)
        self.assertLess(v3string, v4string)

        self.assertLess(v1tuple, v2tuple)
        self.assertLess(v3tuple, v2tuple)
        self.assertLess(v3tuple, v4tuple)

        self.assertGreaterEqual(v2string, v1string)
        self.assertGreaterEqual(v2string, v3string)
        self.assertGreaterEqual(v4string, v3string)

        self.assertGreaterEqual(v2tuple, v1tuple)
        self.assertGreaterEqual(v2tuple, v3tuple)
        self.assertGreaterEqual(v4tuple, v3tuple)

        self.assertGreaterEqual(v2string, v2tuple)

        self.assertLessEqual(v1string, v2string)
        self.assertLessEqual(v3string, v2string)
        self.assertLessEqual(v3string, v4string)

        self.assertLessEqual(v1tuple, v2tuple)
        self.assertLessEqual(v3tuple, v2tuple)
        self.assertLessEqual(v3tuple, v4tuple)

        self.assertLessEqual(v2string, v2tuple)

    def test_bversion(self):
        """Check BVERSION value"""
        import bpy
        from universal_multi_importer.bversion import BVERSION
        self.assertEqual(bpy.app.version, BVERSION.version)