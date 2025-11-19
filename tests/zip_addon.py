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

import os
import zipfile
import ast
from pathlib import Path

from addon_path import addon_path

allowed_file_extensions = ('.py', 'LICENSE', '.md', '.dat', '.toml')
ignore_folders = ('doc_assets', 'venv', 'tests', '.vscode', '__pycache__')


def zipdir(path:Path, ziph: zipfile.ZipFile, zip_subdir_name):
    for root, dirs, files in os.walk(path):
        if any(root.__contains__(folder) for folder in ignore_folders):
            continue

        root = Path(root)
        
        for file in files:
            if any(file.endswith(ext) for ext in allowed_file_extensions):
                zip_subfolder_path = root.relative_to(path)
                orig_hier = os.path.join(root, file)
                arc_hier = os.path.join(zip_subdir_name, zip_subfolder_path, file)
                ziph.write(orig_hier, arc_hier)


def generate_zip_filename(addon_name: str) -> str:
    major, minor, patch = get_addon_version(addon_path / '__init__.py')
    return '{}_v{}.{}.{}.zip'.format(addon_name, major, minor, patch)


def get_addon_version(init_path):
    with open(init_path, 'r') as f:
        node = ast.parse(f.read())

    n: ast.Module
    for n in ast.walk(node):
        for b in n.body:
            if isinstance(b, ast.Assign) and isinstance(b.value, ast.Dict) and (
                    any(t.id == 'bl_info' for t in b.targets)):
                bl_info_dict = ast.literal_eval(b.value)
                return bl_info_dict['version']
    raise ValueError('Cannot find bl_info')


def zip_main(addon_name: str):
    filename = generate_zip_filename(addon_name)
    lower_name = addon_name.lower()
    destination = Path(__file__).parent.parent / 'builds'
    if not os.path.exists(destination):
        os.mkdir(destination)
    filepath = os.path.join(destination, filename)
    try:
        zipf = zipfile.ZipFile(filepath, 'w', zipfile.ZIP_DEFLATED)
        zipdir(addon_path, zipf, lower_name)
        zipf.close()
        print('Successfully created zip file: {}'.format(filepath))
        return filepath
    except Exception as e:
        print('Failed to create {}: {}'.format(filename, e))
        return None

if __name__ == '__main__':
    zip_main('universal_multi_importer')