from . import properties
from .properties import PG_Operator, PG_ImportSettings

def register():
    properties.register()


def unregister():
    properties.unregister()