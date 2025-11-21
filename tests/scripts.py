from pathlib import Path
import importlib.util

def get_script(name:str):
    script_path = Path(__file__).parent.parent / 'scripts'
    
    try:
        script = next(script_path.glob(f'**/{name}.py'))
    except StopIteration:
        print('file not found')
        raise FileNotFoundError

    spec = importlib.util.spec_from_file_location(name, script)
    my_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(my_module)

    return my_module