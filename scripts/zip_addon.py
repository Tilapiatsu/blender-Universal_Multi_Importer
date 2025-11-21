# /// script
# dependencies = []
# ///

import os
import zipfile
import ast
import argparse
from typing import Union, Optional, Dict
from pathlib import Path


allowed_file_extensions = ('.py', 'LICENSE', '.md', '.dat', '.toml')
ignore_folders = ('doc_assets', 'venv', 'tests', '.vscode', '__pycache__', 'site_package')

def main(args: Optional[set]=None) -> None:
    """Command line entry point."""
    parser = argparse.ArgumentParser(
        description="Zip addon, and move it in a build folder",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument(
        "--addon-id",
        required=True,
        help="The ID of the addon. The folder in which the addon is located need to have the same ID.",
    )

    namespace = parser.parse_args(args)

    addon_id: str = namespace.addon_id

    zip_main(addon_id)

def get_addon_path(addon_name:str) -> Path:
    """Retreive the addon path."""
    return Path(__file__).parent.parent / 'src' / addon_name

def zipdir(path:Path, ziph: zipfile.ZipFile, zip_subdir_name):
    """Zip the directory while exclude unnecessary files"""
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
    """Generate an zip filename in this format : addon_id_vx.x.x"""
    major, minor, patch = get_addon_version(get_addon_path(addon_name) / '__init__.py')
    return '{}_v{}.{}.{}.zip'.format(addon_name, major, minor, patch)

def get_addon_version(init_path):
    """Retreive the addon version from bl_info in __init__.py."""
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
    """ Zip the addon."""
    filename = generate_zip_filename(addon_name)
    lower_name = addon_name.lower()
    destination = Path(__file__).parent.parent / 'builds'
    if not os.path.exists(destination):
        os.mkdir(destination)
    filepath = os.path.join(destination, filename)
    try:
        zipf = zipfile.ZipFile(filepath, 'w', zipfile.ZIP_DEFLATED)
        zipdir(get_addon_path(addon_name), zipf, lower_name)
        zipf.close()
        print('Successfully created zip file: {}'.format(filepath))
        return filepath
    except Exception as e:
        print('Failed to create {}: {}'.format(filename, e))
        return None

if __name__ == '__main__':
    main()