import bpy

class ClassPropertyInjection():
    _property_type = {  'STRING': 'bpy.props.StringProperty',
                        'ENUM': 'bpy.props.EnumProperty',
                        'BOOLEAN': 'bpy.props.BoolProperty',
                        'FLOAT': 'bpy.props.FloatProperty',
                        'INT': 'bpy.props.IntProperty'}

    def __init__(self, classes:tuple, property_list:tuple[dict]):
        self._classes = classes
        self._property_list = property_list
        self._properties = None
        self._property_classes = None

    @property
    def property_list(self):
        if self._properties is None:
            self._properties = []

            for d in dir(bpy.data):
                if d.startswith('_'):
                    continue

                data_type = getattr(bpy.data, d)

                if not isinstance(data_type, bpy.types.bpy_prop_collection):
                    continue

                self._properties.append(d)

        return self._properties

    @property
    def property_classes(self):
        if self._property_classes is None:
            self._property_classes = []
            for c in self._classes:
                self._property_classes.append(self.inject_property_class(c))

        return self._property_classes

    def inject_property_class(self, property_class:type) -> None:
        for prop in self._property_list:
            command = f'{self._property_type[prop["type"]]}(name="{prop["name"]}", default={prop["default"]}, description="{prop["description"]}", set=callable_set)'
            property_class.__annotations__[f'{prop["property"]}'] = eval(command, {'callable_set':prop["set"], 'bpy': bpy})

        return property_class

    def register(self):
        for c in self.property_classes:
            print('UMI : Inject properties in Class :', c)
            if c is None:
                continue
            try:
                bpy.utils.register_class(c)
            except [ValueError, TypeError] as e:
                print(e, c)
                continue

    def unregister(self):
        for c in reversed(self.datatype_classes):
            if c is None:
                continue
            try:
                bpy.utils.unregister_class(c)
            except ValueError:
                continue
