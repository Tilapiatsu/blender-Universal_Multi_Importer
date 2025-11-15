import os
from pathlib import Path
import shutil
import subprocess
import unittest

class TestUI(unittest.TestCase):

    def test_ui(self):
        
        BLENDER_EXE = str(Path(r'C:\Users\lhlau\Documents\Tilapiatsu\PortableApps\blender_launcher\builds\stable\blender-4.5.4-lts.b3efe983cc58\blender.exe'))
        if not BLENDER_EXE:
            self.skipTest('$BLENDER_EXE not set in environment, skipping')
        
        subprocess.run([
            BLENDER_EXE,
            '--factory-startup',
            '--python',
            'tests/_bl_run_operators_event_simulate.py',
            '--enable-event-simulate',
            '--',
            '--keep-open',
            '--actions',
            'area_maximize(ui_type="VIEW_3D")',

            # you already know what it is
            'operator("object.delete")',
            'event(type="RET", value="TAP")',
        ])

    def tearDown(self):
        try:
            import addon_testing
            installed_addon_folder = os.path.dirname(addon_testing.__file__)
            if os.path.isdir(installed_addon_folder):
                print('Removing ' + installed_addon_folder + '...')
                shutil.rmtree(installed_addon_folder)
        except ModuleNotFoundError:
            pass