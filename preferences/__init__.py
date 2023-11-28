from . import preferences
from .preferences import get_prefs

def register():
    preferences.register()


def unregister():
    preferences.unregister()