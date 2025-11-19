from pathlib import Path
import tomllib
import logging

from addon_path import addon_path

def get_manifest_info():
    toml_file = addon_path / 'blender_manifest.toml'
    with open(toml_file, 'rb') as f:
        config = tomllib.load(f)

    logging.debug(config)

    return config