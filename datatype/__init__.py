from .datatype_class_creator import DataTypeClassCreator, DATATYPE_LIST


def register(datatype_classes):
    datatype_parser = DataTypeClassCreator(datatype_classes)
    datatype_parser.register_compatible_datatype()


def unregister(datatype_classes):
    datatype_parser = DataTypeClassCreator(datatype_classes)
    datatype_parser.unregister_compatible_datatype()