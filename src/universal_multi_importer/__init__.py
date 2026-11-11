bl_info = {
    "name": "Universal Multi Importer",
    "author": "Tilapiatsu <tilapiatsu@hotmail.fr>",
    "description": "Batch Import many file formats at once, Batch process them",
    "blender": (3, 0, 0),
    "version": (2, 4, 3),
    "location": "File > Import > Universal Multi Importer (File / Folder) | Object > Command Batcher",
    "warning": "",
    "doc_url": "https://github.com/Tilapiatsu/blender-Universal_Multi_Importer",
    "tracker_url": ("https://github.com/Tilapiatsu/blender-Universal_Multi_Importer/issues/new"),
    "support": "COMMUNITY",
    "category": "Import-Export",
}


import bpy
import time


_INITIALIZATION_TIMEOUT = 12.0
_INITIALIZATION_INTERVAL = 0.25

_initialization_state = "UNREGISTERED"
_initialization_started = None
_initialization_timer = None

_import_module = None
_preferences_module = None
_formats_module = None
_operators_module = None
_discovery = None

_import_module_registered = False
_preferences_registered = False
_operators_registered = False


def _initialize_formats():

    global _initialization_state
    global _preferences_registered
    global _operators_registered
    global _operators_module

    if (
        _initialization_state != "INITIALIZING"
        or _discovery is None
        or _formats_module is None
        or _preferences_module is None
    ):
        return None

    complete = _discovery.update()

    elapsed = time.monotonic() - _initialization_started

    if not complete and elapsed < _INITIALIZATION_TIMEOUT:
        return _INITIALIZATION_INTERVAL

    if not complete:
        _discovery.expire_pending()

    try:
        # Populate COMPATIBLE_FORMATS and generate
        # the dynamic PropertyGroup classes.
        _formats_module.finalize_discovery(_discovery)

        # IMPORTANT:
        # Import main operators only after discovery.
        # OP_import.py uses COMPATIBLE_FORMATS to define
        # several class-level properties.
        from . import operators

        _operators_module = operators

        # Preserve the original registration order.
        _preferences_module.register()
        _preferences_registered = True

        _operators_module.register()
        _operators_registered = True

        _initialization_state = "READY" if not _discovery.unavailable else "DEGRADED"

        print(
            "UMI initialization finished:",
            _initialization_state,
        )

    except Exception as exc:
        _initialization_state = "FAILED"

        print("UMI initialization failed:", exc)
        raise

    return None


def register():

    global _initialization_state
    global _initialization_started
    global _initialization_timer

    global _import_module
    global _preferences_module
    global _formats_module
    global _discovery
    global _import_module_registered

    _initialization_state = "INITIALIZING"
    _initialization_started = time.monotonic()

    # 1. Register UMI's internal operators.
    from . import import_module

    _import_module = import_module
    _import_module.register()
    _import_module_registered = True

    # 2. Import preferences and format definitions.
    # Importing these must NOT register format classes.
    from . import preferences

    _preferences_module = preferences
    _formats_module = preferences.formats

    # 3. Create discovery service.
    _discovery = _formats_module.FormatDiscovery(_formats_module.COMPATIBLE_FORMATS)

    # 4. Defer all dependent registration.
    _initialization_timer = _initialize_formats

    bpy.app.timers.register(
        _initialization_timer,
        first_interval=_INITIALIZATION_INTERVAL,
    )


def unregister():

    global _initialization_state
    global _initialization_timer

    global _preferences_registered
    global _operators_registered
    global _import_module_registered

    # Cancel pending initialization.
    if _initialization_timer is not None and bpy.app.timers.is_registered(_initialization_timer):
        bpy.app.timers.unregister(_initialization_timer)

    _initialization_timer = None

    if _operators_module is None or _preferences_module is None or _import_module is None:
        return

    # Unregister in reverse dependency order.
    if _operators_registered:
        _operators_module.unregister()
        _operators_registered = False

    if _preferences_registered:
        _preferences_module.unregister()
        _preferences_registered = False

    if _import_module_registered:
        _import_module.unregister()
        _import_module_registered = False

    _initialization_state = "UNREGISTERED"
