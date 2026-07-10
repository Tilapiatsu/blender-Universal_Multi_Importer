import platform
from ..format import Format, FormatOperators, FormatOperator, FormatImportSetting, axis
from ....bversion import BVERSION


EXTENSION_DESCRIPTION = "Blender Extension"
DEFAULT_DESCRIPTION = "Default Build in module"


def x3d_operators(format_operator: FormatOperator) -> None:
    if BVERSION >= 4.2:
        format_operator.addon_name = "bl_ext.blender_org.web3d_x3d_vrml2_format"
        format_operator.pkg_id = "web3d_x3d_vrml2_format"
        format_operator.pkg_url = "https://extensions.blender.org/add-ons/web3d-x3d-vrml2-format/"
        format_operator.supported_version = "2.5.1"
        format_operator.description = EXTENSION_DESCRIPTION


def dxf_operators(format_operator: FormatOperator) -> None:
    if BVERSION >= 4.2:
        format_operator.addon_name = "bl_ext.blender_org.import_autocad_dxf_format_dxf"
        format_operator.pkg_id = "import_autocad_dxf_format_dxf"
        format_operator.pkg_url = "https://extensions.blender.org/add-ons/import-autocad-dxf-format-dxf/"
        format_operator.supported_version = "0.9.10"
        format_operator.default_values = {"proj_scene": "TMERC"}
        format_operator.forced_properties = ["files", "directory"]
        format_operator.description = EXTENSION_DESCRIPTION


def pdb_operators(format_operator: FormatOperator) -> None:
    if BVERSION >= 4.2:
        format_operator.command = "bpy.ops.import_mesh.pdb"
        format_operator.addon_name = "bl_ext.blender_org.atomic_blender_pdb_xyz"
        format_operator.pkg_id = "atomic_blender_pdb_xyz"
        format_operator.pkg_url = "https://extensions.blender.org/add-ons/atomic-blender-pdb-xyz/"
        format_operator.supported_version = "1.9.1"
        format_operator.description = EXTENSION_DESCRIPTION


def xyz_operators(format_operator: FormatOperator) -> None:
    if BVERSION >= 4.2:
        format_operator.command = "bpy.ops.import_mesh.xyz"
        format_operator.addon_name = "bl_ext.blender_org.atomic_blender_pdb_xyz"
        format_operator.pkg_id = "atomic_blender_pdb_xyz"
        format_operator.pkg_url = "https://extensions.blender.org/add-ons/atomic-blender-pdb-xyz/"
        format_operator.supported_version = "1.9.1"
        format_operator.description = EXTENSION_DESCRIPTION


def max3ds_operators() -> FormatOperators:
    f = FormatOperator(
        "default", "bpy.ops.import_scene.max3ds", "2.4.8", addon_name="io_scene_3ds", description=EXTENSION_DESCRIPTION
    )

    s = FormatImportSetting()

    if BVERSION >= 4.2:
        # Include
        s.add_set_boolean_setting("Include", "use_image_search", "Image Search", True)
        s.add_set_enum_setting(
            "Include",
            "object_filter",
            "Object Filter",
            {"WORLD", "MESH", "LIGHT", "CAMERA", "EMPTY"},
            (
                ("WORLD", "World".rjust(11), "", "WORLD_DATA", 0x1),
                ("MESH", "Mesh".rjust(11), "", "MESH_DATA", 0x2),
                ("LIGHT", "Light".rjust(12), "", "LIGHT_DATA", 0x4),
                ("CAMERA", "Camera".rjust(11), "", "CAMERA_DATA", 0x8),
                ("EMPTY", "Empty".rjust(11), "", "EMPTY_AXIS", 0x10),
            ),
            options={"ENUM_FLAG"},
        )

        s.add_set_boolean_setting("Include", "use_keyframes", "Animation", True)
        s.add_set_boolean_setting("Include", "use_collection", "Collection", False)
        s.add_set_boolean_setting("Include", "use_cursor", "Cursor Origin", False)

        # Transform
        s.add_set_float_setting("Transform", "constrain_size", "Constrain Size", 1.0)
        s.add_set_boolean_setting("Transform", "use_scene_unit", "Scene Unit", False)
        s.add_set_boolean_setting("Transform", "use_apply_transform", "Apply Transform", True)
        s.add_set_enum_setting("Transform", "axis_forward", "Forward", "Y", enum_items=axis())
        s.add_set_enum_setting("Transform", "axis_up", "Up", "Z", enum_items=axis())

    elif BVERSION >= 4.0:
        # Include
        s.add_set_boolean_setting("Include", "use_image_search", "Image Search", True)
        s.add_set_enum_setting(
            "Include",
            "object_filter",
            "Object Filter",
            {"WORLD", "MESH", "LIGHT", "CAMERA", "EMPTY"},
            (
                ("WORLD", "World".rjust(11), "", "WORLD_DATA", 0x1),
                ("MESH", "Mesh".rjust(11), "", "MESH_DATA", 0x2),
                ("LIGHT", "Light".rjust(12), "", "LIGHT_DATA", 0x4),
                ("CAMERA", "Camera".rjust(11), "", "CAMERA_DATA", 0x8),
                ("EMPTY", "Empty".rjust(11), "", "EMPTY_AXIS", 0x10),
            ),
            options={"ENUM_FLAG"},
        )

        s.add_set_boolean_setting("Include", "use_keyframes", "Collection", True)
        s.add_set_boolean_setting("Include", "use_cursor", "Cursor Origin", False)

        # Transform
        s.add_set_float_setting("Transform", "constrain_size", "Constrain Size", 1.0)
        s.add_set_boolean_setting("Transform", "use_scene_unit", "Scene Unit", False)
        s.add_set_boolean_setting("Transform", "use_center_pivot", "Pivot Origin", False)
        s.add_set_boolean_setting("Transform", "use_apply_transform", "Apply Transform", True)
        s.add_set_boolean_setting("Transform", "use_world_matrix", "World Space", False)
        s.add_set_enum_setting("Transform", "axis_forward", "Forward", "Y", enum_items=axis())
        s.add_set_enum_setting("Transform", "axis_up", "Up", "Z", enum_items=axis())

    else:
        # Transform
        s.add_set_float_setting("Transform", "constrain_size", "Constrain Size", 1.0)
        s.add_set_boolean_setting("Transform", "use_image_search", "Image Search", True)
        s.add_set_boolean_setting("Transform", "use_apply_transform", "Apply Transform", True)
        s.add_set_boolean_setting("Transform", "read_keyframe", "Read Keyframe", True)
        s.add_set_boolean_setting("Transform", "use_world_matrix", "World Space", False)
        s.add_set_enum_setting("Transform", "axis_forward", "Forward", "Y", enum_items=axis())
        s.add_set_enum_setting("Transform", "axis_up", "Up", "Z", enum_items=axis())

    if BVERSION >= 4.2:
        f.addon_name = "bl_ext.blender_org.autodesk_3ds_format"
        f.pkg_id = "autodesk_3ds_format"
        f.pkg_url = "https://extensions.blender.org/add-ons/autodesk-3ds-format/"
        f.supported_version = "3.0.1"

    elif BVERSION >= 4.1:
        f.supported_version = "2.4.9"

    elif BVERSION >= 4.0:
        f.supported_version = "2.4.8"

    elif BVERSION >= 3.6:
        f.command = "bpy.ops.import_scene.autodesk_3ds"
        f.supported_version = "2.3.4"

    f.import_settings = s

    return FormatOperators(f)


def max_operators() -> FormatOperators:
    f = FormatOperator(
        "default",
        "bpy.ops.import_scene.max",
        "1.9.1",
        addon_name="bl_ext.blender_org.io_scene_max",
        pkg_id="io_scene_max",
        pkg_url="https://extensions.blender.org/add-ons/io-scene-max/",
        description=EXTENSION_DESCRIPTION,
    )

    s = FormatImportSetting()

    # Include
    s.add_set_boolean_setting("Include", "use_image_search", "Image Search", True)
    s.add_set_enum_setting(
        "Include",
        "object_filter",
        "Object Filter",
        {"MATERIAL", "UV", "EMPTY", "ARMATURE"},
        [
            ("MATERIAL", "Material".rjust(12), "", "MATERIAL_DATA", 0x1),
            ("UV", "UV Maps".rjust(11), "", "UV_DATA", 0x2),
            ("EMPTY", "Empty".rjust(11), "", "EMPTY_AXIS", 0x4),
            ("ARMATURE", "Armature".rjust(11), "", "ARMATURE_DATA", 0x8),
        ],
        options={"ENUM_FLAG"},
    )
    s.add_set_boolean_setting("Include", "use_collection", "Collection", False)

    # Transform
    s.add_set_float_setting("Transform", "scale_objects", "Scale", 1.0)
    s.add_set_boolean_setting("Transform", "use_apply_matrix", "Apply Matrix", True)
    s.add_set_enum_setting("Transform", "axis_forward", "Forward", "Y", enum_items=axis())
    s.add_set_enum_setting("Transform", "axis_up", "Up", "Z", enum_items=axis())

    f.import_settings = s

    return FormatOperators(f)


def pes_operators() -> FormatOperators:
    f = FormatOperator(
        "default",
        "bpy.ops.import_scene.embroidery",
        "0.9.6",
        addon_name="bl_ext.blender_org.embroidery_importer",
        pkg_id="embroidery_importer",
        pkg_url="https://extensions.blender.org/add-ons/embroidery-importer/",
        description=EXTENSION_DESCRIPTION,
    )

    s = FormatImportSetting()

    # Import
    s.add_set_boolean_setting("Import", "show_jump_wires", "Import Jump Wires", True)
    s.add_set_boolean_setting("Import", "do_create_material", "Create Matertial", True)
    s.add_set_boolean_setting("Import", "create_collection", "Create a Collection", False)

    # Thickness
    s.add_set_enum_setting(
        "Thickness",
        "line_depth",
        "Thickness Type",
        "GEOMETRY_NODES",
        (
            ("NO_THICKNESS", "No thickness (curve only)", "Only curves, no thickness"),
            (
                "GEOMETRY_NODES",
                "Using geometry nodes",
                "Create a geometry node setup to add thickness. Most versatile.",
            ),
            ("BEVEL", "Using bevel", "Adds thickness through the bevel property"),
        ),
    )
    s.add_set_float_setting("Thickness", "thread_thickness", "Thread Thickness", 0.2)

    f.import_settings = s

    return FormatOperators(f)


def skp_operators() -> FormatOperators:
    f = FormatOperator(
        "default",
        "bpy.ops.import_scene.skp",
        "0.27.0",
        addon_name="sketchup_importer",
        # pkg_id="sketchup_importer",
        pkg_url="https://github.com/RedHaloStudio/Sketchup_Importer/releases",
        external_addon=True,
        description=EXTENSION_DESCRIPTION,
    )

    operators = FormatOperators(f)

    return operators


class FormatDefinition:
    """
    Stores all information to support import formats
    """

    if BVERSION >= 3.6:
        max3ds = Format("max3ds", [".3ds"], max3ds_operators(), generate_filter_glob=True)

    if BVERSION >= 4.2:
        max = Format("max", [".max"], max_operators(), generate_filter_glob=True)

        pes = Format(
            "pes",
            [
                ".pes",
                ".dst",
                ".exp",
                ".jef",
                ".pec",
                ".jpx",
                ".phc",
                ".vp3",
                ".10o",
                ".bro",
                ".dat",
                ".dsb",
                ".dsz",
                ".emd",
                ".exy",
                ".fxy",
                ".hus",
                ".inb",
                ".new",
                ".pcd",
                ".pcm",
                ".pcq",
                ".pcs",
                ".phb",
                ".sew",
                ".shv",
                ".stc",
                ".stx",
                ".tap",
                ".tbf",
                ".xxx",
                ".zhs",
                ".zxy",
                ".gcode",
            ],  # '.100', '.mit', '.ksm', '.u01', '.gt',
            pes_operators(),
            generate_filter_glob=True,
        )

        if platform.system() == "Windows":
            skp = Format("skp", [".skp"], skp_operators(), generate_filter_glob=True)
