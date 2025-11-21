from universal_multi_importer.bversion import BVERSION
from universal_multi_importer.preferences.formats.format import axis, Format, FormatOperators, FormatOperator, FormatImportSetting

AS_GEOMETRY_NODES_DESCRIPTION = 'Importing as Geometry Node create a dynamic link beetween the source file and the blend file. The file is NOT imported per say, and if the file on disk is changed, the change will be replicated automatically in the blend file it is linked to.'
DEFAULT_DESCRIPTION = 'Default Build in module'
EXTENSION_DESCRIPTION = 'Blender Extension'


def fbx_operators() -> FormatOperators:
    f = FormatOperator('default',
                        'bpy.ops.import_scene.fbx',
                        '5.4.0',
                        addon_name='io_scene_fbx',
                        description=DEFAULT_DESCRIPTION)

    if BVERSION >= 5.0:
        f=FormatOperator('default',
                        'bpy.ops.wm.fbx_import',
                        '0.0.0',
                        description=DEFAULT_DESCRIPTION)

    elif BVERSION >= 4.5:
        f.supported_version = '5.13.0'

    elif BVERSION >= 4.4:
        f.supported_version = '5.12.7'

    elif BVERSION >= 4.3:
        f.supported_version = '5.12.5'

    elif BVERSION >= 4.2:
        f.supported_version = '5.12.4'

    elif BVERSION >= 4.1:
        f.supported_version = '5.11.7'

    elif BVERSION >= 4.002:
        f.supported_version = '5.8.13'

    elif BVERSION >= 4.0:
        f.supported_version = '5.8.12'

    elif BVERSION >= 3.608:
        f.supported_version = '5.4.1'

    elif BVERSION >= 3.6:
        f.supported_version = '5.4.0'

    elif BVERSION >= 3.5:
        f.supported_version = '4.37.5'

    elif BVERSION >= 3.4:
        f.supported_version = '4.37.1'

    elif BVERSION >= 3.3021:
        f.supported_version = '4.36.4'

    elif BVERSION >= 3.3:
        f.supported_version = '4.36.3'

    elif BVERSION >= 3.2:
        f.supported_version = '4.36.0'

    elif BVERSION >= 3.1:
        f.supported_version = '4.29.1'

    elif BVERSION >= 3.0:
        f.supported_version = '4.27.0'

    return FormatOperators(f)


def gltf_operators() -> FormatOperators:
    f = FormatOperator('default',
                        'bpy.ops.import_scene.gltf',
                        '3.6.27',
                        addon_name='io_scene_gltf2',
                        description=DEFAULT_DESCRIPTION)

    if BVERSION >= 5.0:
        f.supported_version = '5.0.21'

    elif BVERSION >= 4.5:
        f.supported_version = '4.5.47'

    elif BVERSION >= 4.401:
        f.supported_version = '4.4.56'

    elif BVERSION >= 4.4:
        f.supported_version = '4.4.55'

    elif BVERSION >= 4.3:
        f.supported_version = '4.3.47'

    elif BVERSION >= 4.204:
        f.supported_version = '4.2.80'

    elif BVERSION >= 4.203:
        f.supported_version = '4.2.70'

    elif BVERSION >= 4.202:
        f.supported_version = '4.2.69'

    elif BVERSION >= 4.2:
        f.supported_version = '4.2.57'

    elif BVERSION >= 4.101:
        f.supported_version = '4.1.63'

    elif BVERSION >= 4.1:
        f.supported_version = '4.1.62'

    elif BVERSION >= 4.002:
        f.supported_version = '4.0.44'

    elif BVERSION >= 4.0:
        f.supported_version = '4.0.43'

    elif BVERSION >= 3.605:
        f.supported_version = '3.6.28'

    elif BVERSION >= 3.6:
        f.supported_version = '3.6.27'

    elif BVERSION >= 3.5:
        f.supported_version = '3.5.30'

    elif BVERSION >= 3.401:
        f.supported_version = '3.4.50'

    elif BVERSION >= 3.4:
        f.supported_version = '3.4.49'

    elif BVERSION >= 3.3021:
        f.supported_version = '3.3.36'

    elif BVERSION >= 3.3:
        f.supported_version = '3.3.27'

    elif BVERSION >= 3.202:
        f.supported_version = '3.2.43'

    elif BVERSION >= 3.2:
        f.supported_version = '3.2.40'

    elif BVERSION >= 3.1:
        f.supported_version = '1.8.19'

    elif BVERSION >= 3.0:
        f.supported_version = '1.7.33'

    return FormatOperators(f)


def abc_operators() -> FormatOperators:
    f = FormatOperator('default',
                        'bpy.ops.wm.alembic_import',
                        '0.0.0',
                        description=DEFAULT_DESCRIPTION)

    return FormatOperators(f)


def dae_operators() -> FormatOperators:
    f = FormatOperator('default',
                        'bpy.ops.wm.collada_import',
                        '0.0.0',
                        description=DEFAULT_DESCRIPTION)

    return FormatOperators(f)


def blend_operators() -> FormatOperators:
    f = FormatOperator('default',
                        'bpy.ops.import_scene.tila_import_blend',
                        '0.0.0',
                        import_data=True)

    return FormatOperators(f)


def bvh_operators() -> FormatOperators:
    f = FormatOperator('default',
                        'bpy.ops.import_anim.bvh',
                        '1.0.1',
                        addon_name='io_anim_bvh',
                        description=DEFAULT_DESCRIPTION)

    if BVERSION >= 3.2:
        pass

    elif BVERSION >= 3.0:
        f.supported_version = '1.0.0'

    return FormatOperators(f)


def obj_operators() -> FormatOperators:
    f = FormatOperator('default',
                        'bpy.ops.wm.obj_import',
                        '0.0.0',
                        description=DEFAULT_DESCRIPTION)

    gn = FormatOperator(    'geometry_node',
                            'bpy.ops.import_scene.tila_import_as_geometry_node',
                            '0.0.0',
                            default_values = {'import_module': 'OBJ'},
                            description = AS_GEOMETRY_NODES_DESCRIPTION)


    if BVERSION >= 3.3:
        pass

    else:
        f.command = 'bpy.ops.import_scene.obj'

    operators = FormatOperators(f)

    if BVERSION >= 4.5:
        operators.add_operator(gn)

    return operators


def ply_operators() -> FormatOperators:
    f = FormatOperator('default',
                        'bpy.ops.wm.ply_import',
                        '0.0.0',
                        description=DEFAULT_DESCRIPTION)

    gn = FormatOperator(    'geometry_node',
                            'bpy.ops.import_scene.tila_import_as_geometry_node',
                            '0.0.0',
                            default_values = {'import_module': 'PLY'},
                            description = AS_GEOMETRY_NODES_DESCRIPTION)

    if BVERSION >= 3.6:
        pass

    else:
        f.command = 'bpy.ops.import_mesh.ply'

    operators = FormatOperators(f)

    if BVERSION >= 4.5:
        operators.add_operator(gn)

    return operators


def svg_operators() -> FormatOperators:
    f = FormatOperator('default',
                        'bpy.ops.import_curve.svg',
                        '0.0.0',
                        description=DEFAULT_DESCRIPTION)

    if BVERSION >= 4.3:
        pass

    elif BVERSION >=4.0:
        f.addon_name = 'io_curve_svg'

    return FormatOperators(f)


def usd_operators() -> FormatOperators:
    f = FormatOperator('default',
                        'bpy.ops.wm.usd_import',
                        '0.0.0',
                        description=DEFAULT_DESCRIPTION)

    return FormatOperators(f)


def x3d_operators() -> FormatOperators:
    f = FormatOperator('default',
                        'bpy.ops.import_scene.x3d',
                        '2.3.1',
                        addon_name='io_scene_x3d',
                        description=DEFAULT_DESCRIPTION)

    if BVERSION >= 4.2:
        f.addon_name = 'bl_ext.blender_org.web3d_x3d_vrml2_format'
        f.pkg_id = 'web3d_x3d_vrml2_format'
        f.pkg_url = 'https://extensions.blender.org/add-ons/web3d-x3d-vrml2-format/'
        f.supported_version = '2.5.1'
        f.description = EXTENSION_DESCRIPTION

    elif BVERSION >= 3.4:
        f.supported_version = '2.3.1'

    elif BVERSION >= 3.0:
        f.supported_version = '2.3.0'

    return FormatOperators(f)


def dxf_operators() -> FormatOperators:
    f = FormatOperator('default',
                        'bpy.ops.import_scene.dxf',
                        '0.9.8',
                        addon_name='io_import_dxf',
                        description=DEFAULT_DESCRIPTION)

    if BVERSION >= 4.2:
        f.addon_name = 'bl_ext.blender_org.import_autocad_dxf_format_dxf'
        f.pkg_id = 'import_autocad_dxf_format_dxf'
        f.pkg_url = 'https://extensions.blender.org/add-ons/import-autocad-dxf-format-dxf/'
        f.supported_version = '0.9.10'
        f.default_values = {'proj_scene': 'TMERC'}
        f.forced_properties = ['files', 'directory']
        f.description = EXTENSION_DESCRIPTION

    elif BVERSION >= 3.6:
        f.supported_version = '0.9.8'

    elif BVERSION >= 3.0:
        f.supported_version = '0.9.6'

    return FormatOperators(f)


def pdb_operators() -> FormatOperators:
    f = FormatOperator('default',
                        'bpy.ops.import_mesh.atomic',
                        '1.8.1',
                        addon_name = 'io_mesh_atomic',
                        description=DEFAULT_DESCRIPTION)

    if BVERSION >= 4.2:
        f.command = 'bpy.ops.import_mesh.pdb'
        f.addon_name = 'bl_ext.blender_org.atomic_blender_pdb_xyz'
        f.pkg_id = 'atomic_blender_pdb_xyz'
        f.pkg_url = 'https://extensions.blender.org/add-ons/atomic-blender-pdb-xyz/'
        f.supported_version = '1.9.1'
        f.description = EXTENSION_DESCRIPTION

    elif BVERSION >= 3.5:
        f.command = 'bpy.ops.import_mesh.pdb'
        f.addon_name = 'io_mesh_atomic'
        f.supported_version = '1.8.1'

    else:
        f.command = 'bpy.ops.import_mesh.pdb'
        f.addon_name = 'io_mesh_atomic'
        f.supported_version = '1.8.0'


    return FormatOperators(f)


def xyz_operators() -> FormatOperators:
    f = FormatOperator('default',
                        'bpy.ops.import_mesh.atomic',
                        '1.8.1',
                        addon_name = 'io_mesh_atomic',
                        description=DEFAULT_DESCRIPTION)

    if BVERSION >= 4.2:
        f.command = 'bpy.ops.import_mesh.xyz'
        f.addon_name = 'bl_ext.blender_org.atomic_blender_pdb_xyz'
        f.pkg_id = 'atomic_blender_pdb_xyz'
        f.pkg_url = 'https://extensions.blender.org/add-ons/atomic-blender-pdb-xyz/'
        f.supported_version = '1.9.1'
        f.description = EXTENSION_DESCRIPTION

    elif BVERSION >= 3.5:
        f.command = 'bpy.ops.import_mesh.xyz'
        f.addon_name = 'io_mesh_atomic'
        f.supported_version = '1.8.1'

    else:
        f.command = 'bpy.ops.import_mesh.xyz'
        f.addon_name = 'io_mesh_atomic'
        f.supported_version = '1.8.0'

    return FormatOperators(f)


def max3ds_operators() -> FormatOperators:
    f = FormatOperator('default',
                        'bpy.ops.import_scene.max3ds',
                        '2.4.8',
                        addon_name = 'io_scene_3ds',
                        description=EXTENSION_DESCRIPTION)

    s = FormatImportSetting()

    if BVERSION >= 4.2:
        # Include
        s.add_set_boolean_setting('Include', 'use_image_search', 'Image Search', True)
        s.add_set_enum_setting('Include',
                                'object_filter',
                                'Object Filter',
                                {'WORLD', 'MESH', 'LIGHT', 'CAMERA', 'EMPTY'},
                                (('WORLD', "World".rjust(11), "", 'WORLD_DATA', 0x1),
                                ('MESH', "Mesh".rjust(11), "", 'MESH_DATA', 0x2),
                                ('LIGHT', "Light".rjust(12), "", 'LIGHT_DATA', 0x4),
                                ('CAMERA', "Camera".rjust(11), "", 'CAMERA_DATA', 0x8),
                                ('EMPTY', "Empty".rjust(11), "", 'EMPTY_AXIS', 0x10),),
                                options={'ENUM_FLAG'})

        s.add_set_boolean_setting('Include', 'use_keyframes', 'Animation', True)
        s.add_set_boolean_setting('Include', 'use_collection', 'Collection', False)
        s.add_set_boolean_setting('Include', 'use_cursor', 'Cursor Origin', False)

        # Transform
        s.add_set_float_setting('Transform', 'constrain_size', 'Constrain Size', 1.0)
        s.add_set_boolean_setting('Transform', 'use_scene_unit', 'Scene Unit', False)
        s.add_set_boolean_setting('Transform', 'use_apply_transform', 'Apply Transform', True)
        s.add_set_enum_setting('Transform', 'axis_forward', 'Forward', 'Y', enum_items=axis())
        s.add_set_enum_setting('Transform', 'axis_up', 'Up', 'Z', enum_items=axis())

    elif BVERSION >= 4.0:
        # Include
        s.add_set_boolean_setting('Include', 'use_image_search', 'Image Search', True)
        s.add_set_enum_setting('Include',
                                'object_filter',
                                'Object Filter',
                                {'WORLD', 'MESH', 'LIGHT', 'CAMERA', 'EMPTY'},
                                (('WORLD', "World".rjust(11), "", 'WORLD_DATA', 0x1),
                                ('MESH', "Mesh".rjust(11), "", 'MESH_DATA', 0x2),
                                ('LIGHT', "Light".rjust(12), "", 'LIGHT_DATA', 0x4),
                                ('CAMERA', "Camera".rjust(11), "", 'CAMERA_DATA', 0x8),
                                ('EMPTY', "Empty".rjust(11), "", 'EMPTY_AXIS', 0x10),),
                                options={'ENUM_FLAG'})

        s.add_set_boolean_setting('Include', 'use_keyframes', 'Collection', True)
        s.add_set_boolean_setting('Include', 'use_cursor', 'Cursor Origin', False)

        # Transform
        s.add_set_float_setting('Transform', 'constrain_size', 'Constrain Size', 1.0)
        s.add_set_boolean_setting('Transform', 'use_scene_unit', 'Scene Unit', False)
        s.add_set_boolean_setting('Transform', 'use_center_pivot', 'Pivot Origin', False)
        s.add_set_boolean_setting('Transform', 'use_apply_transform', 'Apply Transform', True)
        s.add_set_boolean_setting('Transform', 'use_world_matrix', 'World Space', False)
        s.add_set_enum_setting('Transform', 'axis_forward', 'Forward', 'Y', enum_items=axis())
        s.add_set_enum_setting('Transform', 'axis_up', 'Up', 'Z', enum_items=axis())

    else:
        # Transform
        s.add_set_float_setting('Transform', 'constrain_size', 'Constrain Size', 1.0)
        s.add_set_boolean_setting('Transform', 'use_image_search', 'Image Search', True)
        s.add_set_boolean_setting('Transform', 'use_apply_transform', 'Apply Transform', True)
        s.add_set_boolean_setting('Transform', 'read_keyframe', 'Read Keyframe', True)
        s.add_set_boolean_setting('Transform', 'use_world_matrix', 'World Space', False)
        s.add_set_enum_setting('Transform', 'axis_forward', 'Forward', 'Y', enum_items=axis())
        s.add_set_enum_setting('Transform', 'axis_up', 'Up', 'Z', enum_items=axis())

    if BVERSION >= 4.2:
        f.addon_name = 'bl_ext.blender_org.autodesk_3ds_format'
        f.pkg_id = 'autodesk_3ds_format'
        f.pkg_url = 'https://extensions.blender.org/add-ons/autodesk-3ds-format/'
        f.supported_version = '3.0.0'

    elif BVERSION >= 4.1:
        f.supported_version = '2.4.9'

    elif BVERSION >= 4.0:
        f.supported_version = '2.4.8'

    elif BVERSION >= 3.6:
        f.command = 'bpy.ops.import_scene.autodesk_3ds'
        f.supported_version = '2.3.4'

    f.import_settings = s

    return FormatOperators(f)


def image_operators() -> FormatOperators:
    data = FormatOperator(  'data',
                            'bpy.ops.image.open',
                            '0.0.0',
                            import_objects=False,
                            description=DEFAULT_DESCRIPTION)

    plane = FormatOperator( 'plane',
                            'bpy.ops.import_image.to_plane',
                            '3.5.1',
                            addon_name='io_import_images_as_planes',
                            description=DEFAULT_DESCRIPTION)

    operators = FormatOperators(data)

    if BVERSION >= 4.2:
        plane.command = 'bpy.ops.image.import_as_mesh_planes'
        plane.supported_version = '0.0.0'
        plane.addon_name = None
        plane.forced_properties = ['files', 'directory']

        empty = FormatOperator( 'empty',
                                'bpy.ops.object.empty_image_add',
                                '0.0.0',
                                description=DEFAULT_DESCRIPTION)

        operators.add_operator(empty)

    elif BVERSION >= 4.0 :
        ref = FormatOperator( 'ref',
                                'bpy.ops.object.load_reference_image',
                                '0.0.0',
                                description=DEFAULT_DESCRIPTION)

        background = FormatOperator('background',
                                    'bpy.ops.object.load_background_image',
                                    '0.0.0',
                                    description=DEFAULT_DESCRIPTION)

        operators.add_operator(ref)
        operators.add_operator(background)

    elif BVERSION >= 3.6:
        ref = FormatOperator( 'ref',
                                'bpy.ops.object.load_reference_image',
                                '0.0.0',
                                description=DEFAULT_DESCRIPTION)

        background = FormatOperator('background',
                                    'bpy.ops.object.load_background_image',
                                    '0.0.0',
                                    description=DEFAULT_DESCRIPTION)
        operators.add_operator(ref)
        operators.add_operator(background)
        plane.supported_version = '3.5.0'

    elif BVERSION >= 3.4:
        ref = FormatOperator( 'ref',
                                'bpy.ops.object.load_reference_image',
                                '0.0.0',
                                description=DEFAULT_DESCRIPTION)

        background = FormatOperator('background',
                                    'bpy.ops.object.load_background_image',
                                    '0.0.0',
                                    description=DEFAULT_DESCRIPTION)
        operators.add_operator(ref)
        operators.add_operator(background)
        plane.supported_version = '3.5.0'

    elif BVERSION >= 3.0:
        ref = FormatOperator( 'ref',
                                'bpy.ops.object.load_reference_image',
                                '0.0.0',
                                description=DEFAULT_DESCRIPTION)

        background = FormatOperator('background',
                                    'bpy.ops.object.load_background_image',
                                    '0.0.0',
                                    description=DEFAULT_DESCRIPTION)
        operators.add_operator(ref)
        operators.add_operator(background)
        plane.supported_version = '3.4.0'

    operators.add_operator(plane)

    return operators


def sound_operators() -> FormatOperators:
    data = FormatOperator(  'data',
                            'bpy.ops.sound.open',
                            '0.0.0',
                            import_objects=False,
                            description=DEFAULT_DESCRIPTION)
    operators = FormatOperators(data)
    operators.add_operator(data)

    return operators


def stl_operators() -> FormatOperators:
    default = FormatOperator('default',
                        'bpy.ops.wm.stl_import',
                        '1.1.3',
                        addon_name='io_mesh_stl',
                        description=DEFAULT_DESCRIPTION)

    gn = FormatOperator(    'geometry_node',
                            'bpy.ops.import_scene.tila_import_as_geometry_node',
                            '0.0.0',
                            default_values = {'import_module': 'STL'},
                            description = AS_GEOMETRY_NODES_DESCRIPTION)

    operators = FormatOperators(default)

    if BVERSION >= 4.5:
        operators.add_operator(gn)

    if BVERSION >= 4.2:
        default.addon_name = None
        default.supported_version = '0.0.0'

    elif BVERSION >= 4.0:
        legacy = FormatOperator('legacy',
                                'bpy.ops.import_mesh.stl',
                                '0.0.0',
                                description=DEFAULT_DESCRIPTION)

        operators.add_operator(legacy)

    elif BVERSION >= 3.6:
        legacy = FormatOperator('legacy',
                                'bpy.ops.import_mesh.stl',
                                '0.0.0',
                                description=DEFAULT_DESCRIPTION)

        operators.add_operator(legacy)

    else:
        default.command = 'bpy.ops.import_mesh.stl'

    return operators


def max_operators() -> FormatOperators:
    f = FormatOperator('default',
                        'bpy.ops.import_scene.max',
                        '1.7.0',
                        addon_name='bl_ext.blender_org.io_scene_max',
                        pkg_id='io_scene_max',
                        pkg_url='https://extensions.blender.org/add-ons/io-scene-max/',
                        description=EXTENSION_DESCRIPTION)

    s = FormatImportSetting()

    # Include
    s.add_set_boolean_setting('Include', 'use_image_search', 'Image Search', True)
    s.add_set_enum_setting('Include',
                            'object_filter',
                            'Object Filter',
                            {'MATERIAL', 'UV', 'EMPTY', 'ARMATURE'},
                            [('MATERIAL', "Material".rjust(12), "", 'MATERIAL_DATA', 0x1),
                            ('UV', "UV Maps".rjust(11), "", 'UV_DATA', 0x2),
                            ('EMPTY', "Empty".rjust(11), "", 'EMPTY_AXIS', 0x4),
                            ('ARMATURE', "Armature".rjust(11), "", 'ARMATURE_DATA', 0x8),],
                            options={'ENUM_FLAG'})
    s.add_set_boolean_setting('Include', 'use_collection', 'Collection', False)

    # Transform
    s.add_set_float_setting('Transform', 'scale_objects', 'Scale', 1.0)
    s.add_set_boolean_setting('Transform', 'use_apply_matrix', 'Apply Matrix', True)
    s.add_set_enum_setting('Transform', 'axis_forward', 'Forward', 'Y', enum_items=axis())
    s.add_set_enum_setting('Transform', 'axis_up', 'Up', 'Z', enum_items=axis())

    f.import_settings = s

    return FormatOperators(f)


def pes_operators() -> FormatOperators:
    f = FormatOperator('default',
                        'bpy.ops.import_scene.embroidery',
                        '0.9.6',
                        addon_name='bl_ext.blender_org.embroidery_importer',
                        pkg_id='embroidery_importer',
                        pkg_url='https://extensions.blender.org/add-ons/embroidery-importer/',
                        description=EXTENSION_DESCRIPTION)

    s = FormatImportSetting()

    # Import
    s.add_set_boolean_setting('Import', 'show_jump_wires', 'Import Jump Wires', True)
    s.add_set_boolean_setting('Import', 'do_create_material', 'Create Matertial', True)
    s.add_set_boolean_setting('Import', 'create_collection', 'Create a Collection', False)

    # Thickness
    s.add_set_enum_setting('Thickness',
                            'line_depth',
                            'Thickness Type',
                            'GEOMETRY_NODES',
                            ((   "NO_THICKNESS",
                                "No thickness (curve only)",
                                "Only curves, no thickness"),
                            (   "GEOMETRY_NODES",
                                "Using geometry nodes",
                                "Create a geometry node setup to add thickness. Most versatile."),
                            ("BEVEL",
                                "Using bevel",
                                "Adds thickness through the bevel property")))
    s.add_set_float_setting('Thickness', 'thread_thickness', 'Thread Thickness', 0.2)

    f.import_settings = s

    return FormatOperators(f)


def vdb_operators() -> FormatOperators:
    op = FormatOperator(    'default',
                            'bpy.ops.object.volume_import',
                            '0.0.0',
                            description=DEFAULT_DESCRIPTION)

    operators = FormatOperators(op)
    operators.add_operator(op)

    gn = FormatOperator(    'geometry_node',
                            'bpy.ops.import_scene.tila_import_as_geometry_node',
                            '0.0.0',
                            default_values = {'import_module': 'VDB'},
                            description = AS_GEOMETRY_NODES_DESCRIPTION)

    if BVERSION >= 4.5:
        operators.add_operator(gn)

    return operators


class FormatDefinition:
    '''
    Stores all information to support import formats
    '''

    fbx     = Format('fbx',
                     ['.fbx'],
                     fbx_operators(),
                     generate_filter_glob=BVERSION < 3.3)

    gltf    = Format('gltf',
                     ['.glb', '.gltf'],
                     gltf_operators(),
                     generate_filter_glob=BVERSION < 3.2)

    abc     = Format('abc',
                     ['.abc'],
                     abc_operators())

    if BVERSION < 5.0:
        dae     = Format('dae',
                    ['.dae'],
                    dae_operators())

    blend   = Format('blend',
                     ['.blend'],
                     blend_operators())

    bvh     = Format('bvh',
                     ['.bvh'],
                     bvh_operators(),
                     generate_filter_glob=True)

    obj     = Format('obj',
                     ['.obj'],
                     obj_operators(),
                     generate_filter_glob=BVERSION < 3.3)

    ply     = Format('ply',
                     ['.ply'],
                     ply_operators(),
                     generate_filter_glob=BVERSION < 3.4)

    svg     = Format('svg',
                     ['.svg'],
                     svg_operators(),
                     generate_filter_glob=BVERSION < 3.3)

    usd     = Format('usd',
                     ['.usd', '.usda', '.usdc', '.usdz'],
                     usd_operators(),
                     generate_filter_glob=BVERSION < 3.3)

    x3d     = Format('x3d',
                     ['.x3d', '.wrl'],
                     x3d_operators(),
                     generate_filter_glob=True)

    dxf     = Format('dxf',
                     ['.dxf'],
                     dxf_operators(),
                     generate_filter_glob=True)

    pdb     = Format('pdb',
                     ['.pdb'],
                     pdb_operators(),
                     generate_filter_glob=BVERSION < 3.6)

    xyz     = Format('xyz',
                     ['.xyz'],
                     xyz_operators(),
                     generate_filter_glob=True)

    stl     = Format('stl',
                     ['.stl'],
                     stl_operators(),
                     generate_filter_glob=BVERSION < 3.3)

    image   = Format('image',
                     [	'.jpg', '.jpeg', '.gif', '.png', '.tif', '.tiff', '.bmp', '.cin', '.dpx', '.jp2', '.j2c', '.sig', '.rgb', '.bw', '.webp',
                     '.hdr', '.exr',
                     '.mov', '.mp4', '.mkv', '.mpg', '.mpeg', '.dvd', '.vob', '.avi', '.dv', '.flv', '.webm'],
                     image_operators())

    sound = Format('sound',
                   ['.wav', '.flac', '.mp2', '.mp3', '.aac', '.ogg', '.pcm', '.opus', '.l16', '.aiff', '.au'],
                   sound_operators(),
                   ignore=['files', 'filepath', 'directory'])

    vdb = Format(   'vdb',
                    ['.vdb'],
                    vdb_operators())

    if BVERSION >= 3.6:
        max3ds  = Format('max3ds',
                        ['.3ds'],
                        max3ds_operators(),
                        generate_filter_glob=True)

    if BVERSION >= 4.2:
        max     = Format('max',
                        ['.max'],
                        max_operators(),
                        generate_filter_glob=True)

        pes     = Format('pes',
                        ['.pes', '.dst', '.exp', '.jef', '.pec', '.jpx', '.phc', '.vp3', '.10o', '.bro', '.dat', '.dsb', '.dsz', '.emd', '.exy', '.fxy', '.hus', '.inb', '.new', '.pcd', '.pcm', '.pcq', '.pcs', '.phb', '.sew', '.shv', '.stc', '.stx', '.tap', '.tbf', '.xxx', '.zhs', '.zxy', '.gcode'], # '.100', '.mit', '.ksm', '.u01', '.gt',
                        pes_operators(),
                        generate_filter_glob=True)
