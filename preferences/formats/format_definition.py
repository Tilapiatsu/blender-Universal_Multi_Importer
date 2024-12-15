from . import BVERSION
from .format import axis, Format, FormatOperators, FormatOperator, FormatImportSetting


class FormatDefinition:
    '''
    Stores all information to support import formats
    '''

    def __get_fbx_operators() -> FormatOperator:
        f = FormatOperator('default',
                           'bpy.ops.import_scene.fbx',
                           '5.4.0',
                           addon_name='io_scene_fbx')

        if BVERSION >= 4.3:
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


    def __get_gltf_operators() -> FormatOperator:
        f = FormatOperator('default',
                           'bpy.ops.import_scene.gltf',
                           '3.6.27',
                           addon_name='io_scene_gltf2')

        if BVERSION >= 4.3:
            f.supported_version = '4.3.47'

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


    def __get_abc_operators() -> FormatOperator:
        f = FormatOperator('default',
                           'bpy.ops.wm.alembic_import',
                           '0.0.0')

        return FormatOperators(f)


    def __get_dae_operators() -> FormatOperator:
        f = FormatOperator('default',
                           'bpy.ops.wm.collada_import',
                           '0.0.0')

        return FormatOperators(f)


    def __get_blend_operators() -> FormatOperator:
        f = FormatOperator('default',
                           'bpy.ops.import_scene.tila_import_blend',
                           '0.0.0')

        return FormatOperators(f)


    def __get_bvh_operators() -> FormatOperator:
        f = FormatOperator('default',
                           'bpy.ops.import_anim.bvh',
                           '1.0.1',
                           addon_name='io_anim_bvh')

        if BVERSION >= 3.2:
            pass

        elif BVERSION >= 3.0:
            f.supported_version = '1.0.0'

        return FormatOperators(f)


    def __get_obj_operators() -> FormatOperator:
        f = FormatOperator('default',
                           'bpy.ops.wm.obj_import',
                           '0.0.0')

        if BVERSION >= 3.3:
            pass

        else:
            f.command = 'bpy.ops.import_scene.obj'

        return FormatOperators(f)


    def __get_ply_operators() -> FormatOperator:
        f = FormatOperator('default',
                           'bpy.ops.wm.ply_import',
                           '0.0.0')

        if BVERSION >= 3.2:
            pass

        else:
            f.command = 'bpy.ops.import_mesh.ply'

        return FormatOperators(f)


    def __get_svg_operators() -> FormatOperator:
        f = FormatOperator('default',
                           'bpy.ops.import_curve.svg',
                           '0.0.0')

        if BVERSION >= 4.3:
            pass

        elif BVERSION >=4.0:
            f.addon_name = 'io_curve_svg'

        return FormatOperators(f)


    def __get_usd_operators() -> FormatOperator:
        f = FormatOperator('default',
                           'bpy.ops.wm.usd_import',
                           '0.0.0')

        return FormatOperators(f)


    def __get_x3d_operators() -> FormatOperator:
        f = FormatOperator('default',
                           'bpy.ops.import_scene.x3d',
                           '2.3.1',
                           addon_name='io_scene_x3d')

        if BVERSION >= 4.2:
            f.addon_name = 'bl_ext.blender_org.web3d_x3d_vrml2_format'
            f.pkg_id = 'web3d_x3d_vrml2_format'
            f.pkg_url = 'https://extensions.blender.org/add-ons/web3d-x3d-vrml2-format/'
            f.supported_version = '2.4.4'

        elif BVERSION >= 3.4:
            f.supported_version = '2.3.1'

        elif BVERSION >= 3.0:
            f.supported_version = '2.3.0'

        return FormatOperators(f)


    def __get_dxf_operators() -> FormatOperator:
        f = FormatOperator('default',
                           'bpy.ops.import_scene.dxf',
                           '0.9.8',
                           addon_name='io_import_dxf')

        if BVERSION >= 4.2:
            f.addon_name = 'bl_ext.blender_org.import_autocad_dxf_format_dxf'
            f.pkg_id = 'import_autocad_dxf_format_dxf'
            f.pkg_url = 'https://extensions.blender.org/add-ons/import-autocad-dxf-format-dxf/'
            f.supported_version = '0.9.10'

        elif BVERSION >= 4.1:
            f.supported_version = '0.9.8'

        elif BVERSION >= 3.5:
            f.supported_version = '0.9.8'

        elif BVERSION >= 3.0:
            f.supported_version = '0.9.6'

        return FormatOperators(f)


    def __get_pdb_operators() -> FormatOperator:
        f = FormatOperator('default',
                           'bpy.ops.import_mesh.atomic',
                           '1.8.1',
                           addon_name = 'io_mesh_atomic')

        if BVERSION >= 4.2:
            f.command = 'bpy.ops.import_mesh.pdb'
            f.addon_name = 'bl_ext.blender_org.atomic_blender_pdb_xyz'
            f.pkg_id = 'atomic_blender_pdb_xyz'
            f.pkg_url = 'https://extensions.blender.org/add-ons/atomic-blender-pdb-xyz/'
            f.supported_version = '1.9.1'

        elif BVERSION >= 4.0:
            f.command = 'bpy.ops.import_mesh.pdb'
            f.addon_name = 'io_mesh_atomic'
            f.supported_version = '1.8.1'

        else:
            f.command = 'bpy.ops.import_mesh.pdb'
            f.addon_name = 'io_mesh_atomic'
            f.supported_version = '1.8.0'


        return FormatOperators(f)


    def __get_xyz_operators() -> FormatOperator:
        f = FormatOperator('default',
                           'bpy.ops.import_mesh.atomic',
                           '1.8.1',
                           addon_name = 'io_mesh_atomic')

        if BVERSION >= 4.2:
            f.command = 'bpy.ops.import_mesh.xyz'
            f.addon_name = 'bl_ext.blender_org.atomic_blender_pdb_xyz'
            f.pkg_id = 'atomic_blender_pdb_xyz'
            f.pkg_url = 'https://extensions.blender.org/add-ons/atomic-blender-pdb-xyz/'
            f.supported_version = '1.9.1'

        elif BVERSION >= 4.0:
            f.command = 'bpy.ops.import_mesh.xyz'
            f.addon_name = 'io_mesh_atomic'
            f.supported_version = '1.8.1'

        else:
            f.command = 'bpy.ops.import_mesh.xyz'
            f.addon_name = 'io_mesh_atomic'
            f.supported_version = '1.8.0'

        return FormatOperators(f)


    def __get_max3ds_operators() -> FormatOperator:
        f = FormatOperator('default',
                           'bpy.ops.import_scene.max3ds',
                           '2.4.8',
                           addon_name = 'io_scene_3ds')

        s = FormatImportSetting()

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

        if BVERSION >= 4.2:
            f.addon_name = 'bl_ext.blender_org.autodesk_3ds_format'
            f.pkg_id = 'autodesk_3ds_format'
            f.pkg_url = 'https://extensions.blender.org/add-ons/autodesk-3ds-format/'
            f.supported_version = '2.7.5'

        elif BVERSION >= 4.1:
            f.supported_version = '2.4.9'

        f.import_settings = s

        return FormatOperators(f)


    def __get_image_operators() -> FormatOperator:
        data = FormatOperator(  'data',
                                'bpy.ops.image.open',
                                '0.0.0')

        plane = FormatOperator( 'plane',
                                'bpy.ops.import_image.to_plane',
                                '3.5.1',
                                addon_name='io_import_images_as_planes')

        operators = FormatOperators(data)

        if BVERSION >= 4.2:
            plane.command = 'bpy.ops.image.import_as_mesh_planes'
            plane.supported_version = '0.0.0'
            plane.addon_name = None

            empty = FormatOperator( 'empty',
                                    'bpy.ops.object.empty_image_add',
                                    '0.0.0')

            operators.add_operator(empty)

        elif BVERSION >= 4.0 :
            ref = FormatOperator( 'ref',
                                    'bpy.ops.object.load_reference_image',
                                    '0.0.0')

            background = FormatOperator('background',
                                        'bpy.ops.object.load_background_image',
                                        '0.0.0')

            operators.add_operator(ref)
            operators.add_operator(background)

        elif BVERSION >= 3.6:
            ref = FormatOperator( 'ref',
                                    'bpy.ops.object.load_reference_image',
                                    '0.0.0')

            background = FormatOperator('background',
                                        'bpy.ops.object.load_background_image',
                                        '0.0.0')
            operators.add_operator(ref)
            operators.add_operator(background)
            plane.supported_version = '3.5.0'

        elif BVERSION >= 3.4:
            ref = FormatOperator( 'ref',
                                    'bpy.ops.object.load_reference_image',
                                    '0.0.0')

            background = FormatOperator('background',
                                        'bpy.ops.object.load_background_image',
                                        '0.0.0')
            operators.add_operator(ref)
            operators.add_operator(background)
            plane.supported_version = '3.5.0'

        elif BVERSION >= 3.0:
            ref = FormatOperator( 'ref',
                                    'bpy.ops.object.load_reference_image',
                                    '0.0.0')

            background = FormatOperator('background',
                                        'bpy.ops.object.load_background_image',
                                        '0.0.0')
            operators.add_operator(ref)
            operators.add_operator(background)
            plane.supported_version = '3.4.0'

        operators.add_operator(plane)

        return operators


    def __get_stl_operators() -> FormatOperator:
        default = FormatOperator('default',
                           'bpy.ops.wm.stl_import',
                           '1.1.3',
                           addon_name='io_mesh_stl')

        operators = FormatOperators(default)

        if BVERSION >= 4.2:
            default.addon_name = None
            default.supported_version = '0.0.0'

        elif BVERSION >= 4.0:
            legacy = FormatOperator('legacy',
                                    'bpy.ops.import_mesh.stl',
                                    '0.0.0')

            operators.add_operator(legacy)

        else:
            default.command = 'bpy.ops.import_mesh.stl'

        return operators


    def __get_max_operators() -> FormatOperator:
        f = FormatOperator('default',
                           'bpy.ops.import_scene.max',
                           '1.6.0',
                           addon_name='bl_ext.blender_org.io_scene_max',
                           pkg_id='io_scene_max',
                           pkg_url='https://extensions.blender.org/add-ons/io-scene-max/')

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


    def __get_pes_operators() -> FormatOperator:
        f = FormatOperator('default',
                           'bpy.ops.import_scene.embroidery',
                           '0.9.4',
                           addon_name='bl_ext.blender_org.embroidery_importer',
                           pkg_id='embroidery_importer',
                           pkg_url='https://extensions.blender.org/add-ons/embroidery-importer/')

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


    fbx     = Format('fbx',
                     ['.fbx'],
                     __get_fbx_operators(),
                     generate_filter_glob=BVERSION <= 3.2).as_dict()

    gltf    = Format('gltf',
                     ['.glb', '.gltf'],
                     __get_gltf_operators(),
                     generate_filter_glob=BVERSION <= 3.2).as_dict()

    abc     = Format('abc',
                     ['.abc'],
                     __get_abc_operators()).as_dict()

    dae     = Format('dae',
                     ['.dae'],
                     __get_dae_operators(),
                     ignore=['files', 'name', 'directory']).as_dict()

    blend   = Format('blend',
                     ['.blend'],
                     __get_blend_operators()).as_dict()

    bvh     = Format('bvh',
                     ['.bvh'],
                     __get_bvh_operators(),
                     generate_filter_glob=True).as_dict()

    obj     = Format('obj',
                     ['.obj'],
                     __get_obj_operators(),
                     generate_filter_glob=BVERSION <= 3.2).as_dict()

    ply     = Format('ply',
                     ['.ply'],
                     __get_ply_operators(),
                     generate_filter_glob=BVERSION <= 3.2).as_dict()

    svg     = Format('svg',
                     ['.svg'],
                     __get_svg_operators(),
                     generate_filter_glob=BVERSION <= 3.2).as_dict()

    usd     = Format('usd',
                     ['.usd', '.usda', '.usdc', '.usdz'],
                     __get_usd_operators(),
                     generate_filter_glob=BVERSION <= 3.2).as_dict()

    x3d     = Format('x3d',
                     ['.x3d', '.wrl'],
                     __get_x3d_operators(),
                     generate_filter_glob=True).as_dict()

    dxf     = Format('dxf',
                     ['.dxf'],
                     __get_dxf_operators(),
                     generate_filter_glob=True).as_dict()

    pdb     = Format('pdb',
                     ['.pdb'],
                     __get_pdb_operators()).as_dict()

    xyz     = Format('xyz',
                     ['.xyz'],
                     __get_xyz_operators(),
                     generate_filter_glob=True).as_dict()

    stl     = Format('stl',
                     ['.stl'],
                     __get_stl_operators(),
                     generate_filter_glob=BVERSION <= 3.2).as_dict()

    image   = Format('image',
                     [	'.jpg', '.jpeg', '.gif', '.png', '.tif', '.tiff', '.bmp', '.cin', '.dpx', '.jp2', '.j2c', '.sig', '.rgb', '.bw',
                     '.hdr', '.exr',
                     '.mov', '.mp4', '.mkv', '.mpg', '.mpeg', '.dvd', '.vob', '.avi', '.dv', '.flv', '.webm'],
                     __get_image_operators(),
                     ignore=['files', 'filepath', 'directory']).as_dict()

    if BVERSION >= 3.6:
        max3ds  = Format('max3ds',
                        ['.3ds'],
                        __get_max3ds_operators(),
                        generate_filter_glob=True).as_dict()

    if BVERSION >= 4.2:
        max     = Format('max',
                        ['.max'],
                        __get_max_operators(),
                        generate_filter_glob=True).as_dict()

        pes     = Format('pes',
                        ['.pes', '.dst', '.exp', '.jef', '.pec', '.jpx', '.phc', '.vp3', '.10o', '.bro', '.dat', '.dsb', '.dsz', '.emd', '.exy', '.fxy', '.hus', '.inb', '.new', '.pcd', '.pcm', '.pcq', '.pcs', '.phb', '.sew', '.shv', '.stc', '.stx', '.tap', '.tbf', '.xxx', '.zhs', '.zxy', '.gcode'], # '.100', '.mit', '.ksm', '.u01', '.gt',
                        __get_pes_operators(),
                        generate_filter_glob=True).as_dict()
