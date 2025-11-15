from pathlib import Path
import tomllib
import logging

def get_manifest_info():
    toml_file = Path(__file__).parent.parent / 'blender_manifest.toml'
    with open(toml_file, 'rb') as f:
        config = tomllib.load(f)

    logging.debug(config)

    return config