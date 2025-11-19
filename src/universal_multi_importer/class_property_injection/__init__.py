from .class_property_injection import ClassPropertyInjection

def register(classes:tuple, property_list:tuple[dict]):
    property_injection = ClassPropertyInjection(classes, property_list)
    property_injection.register()


def unregister(classes:tuple, property_list:tuple[dict]):
    property_injection = ClassPropertyInjection(classes, property_list)
    property_injection.unregister()