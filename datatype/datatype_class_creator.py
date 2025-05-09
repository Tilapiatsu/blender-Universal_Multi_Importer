import bpy
from ..bversion import BVERSION

def get_datalist():
    datatype_list = [
                        'actions',
                        'armatures',
                        'brushes',
                        'cache_files',
                        'cameras',
                        'collections',
                        'curves',
                        'fonts',
                        'grease_pencils',
                        'images',
                        'lattices',
                        'libraries',
                        'lightprobes',
                        'lights',
                        'linestyles',
                        'masks',
                        'materials',
                        'meshes',
                        'metaballs',
                        'movieclips',
                        'node_groups',
                        'objects',
                        'paint_curves',
                        'palettes',
                        'particles',
                        'scenes',
                        'screens',
                        'shape_keys',
                        'sounds',
                        'speakers',
                        'texts',
                        'textures',
                        'volumes',
                        'window_managers',
                        'workspaces',
                        'worlds'
                    ]

    if BVERSION >= 3.1:
        datatype_list.append('pointclouds')

    if BVERSION >= 3.3:
        datatype_list.append('hair_curves')

    if BVERSION >= 4.3:
        datatype_list.append('grease_pencils_v3')

    datatype_list.sort()
    return datatype_list


DATATYPE_LIST = get_datalist()


class DataTypeClassCreator():
    def __init__(self, classes:list):
        self._classes = classes
        self._datatypes = None
        self._datatype_classes = None

    @property
    def datatype_list(self):
        if self._datatypes is None:
            self._datatypes = []

            for d in dir(bpy.data):
                if d.startswith('_'):
                    continue

                data_type = getattr(bpy.data, d)

                if not isinstance(data_type, bpy.types.bpy_prop_collection):
                    continue

                self._datatypes.append(d)

        # print(self._datatypes)
        return self._datatypes

    @property
    def datatype_classes(self):
        if self._datatype_classes is None:
            self._datatype_classes = []
            for c in self._classes:
                self._datatype_classes.append(self.create_datatype_class(c['class'], c['prefix']))

        return self._datatype_classes

    def create_datatype_class(self, datatype_class:type, prop_prefix:str) -> None:
        for datatype in DATATYPE_LIST:
            if datatype == 'objects':
                default_value = True
            else:
                default_value = False

            datatype_class.__annotations__[f'{prop_prefix}_{datatype}'] = bpy.props.BoolProperty(name=f'{datatype}'.replace('_', ' ').title(), default=default_value)

        return datatype_class

    def register_compatible_datatype(self):
        for c in self.datatype_classes:
            print('UMI : Register datatype :', c)
            if c is None:
                continue
            try:
                bpy.utils.register_class(c)
            except [ValueError, TypeError] as e:
                print(e, c)
                continue

    def unregister_compatible_datatype(self):
        for c in reversed(self.datatype_classes):
            if c is None:
                continue
            try:
                bpy.utils.unregister_class(c)
            except ValueError:
                continue
