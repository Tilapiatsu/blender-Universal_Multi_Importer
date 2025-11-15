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

"""Utility file for running unittest within Blender executable instead of virtual environment."""
# Testing pipeline from Spencer Magnusson: https://github.com/semagnum/addon_testing/tree/main

# you can run with:
# blender.exe --background --factory-startup --python tests/__init__.py

from pathlib import Path
import unittest

if __name__ == '__main__':
    loader = unittest.TestLoader()
    path = str(Path(__file__).parent)
    suite = loader.discover(path)
    runner = unittest.TextTestRunner()
    runner.run(suite)

    # quit Blender after running
    import bpy
    bpy.ops.wm.quit_blender()