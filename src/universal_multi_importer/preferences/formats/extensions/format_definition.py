from ..formats import Format
from ....bversion import BVERSION
from ....bversion.version import Version


class FormatDefinition:
    """
    Stores all information to support import formats
    """

    fbx = Format("fbx", [".fbx"], fbx_operators(), generate_filter_glob=BVERSION < 3.3)

    gltf = Format("gltf", [".glb", ".gltf"], gltf_operators(), generate_filter_glob=BVERSION < 3.2)

    abc = Format("abc", [".abc"], abc_operators())

    if BVERSION < 5.0:
        dae = Format("dae", [".dae"], dae_operators())

    blend = Format("blend", [".blend"], blend_operators())

    bvh = Format("bvh", [".bvh"], bvh_operators(), generate_filter_glob=True)

    obj = Format("obj", [".obj"], obj_operators(), generate_filter_glob=BVERSION < 3.3)

    ply = Format("ply", [".ply"], ply_operators(), generate_filter_glob=BVERSION < 3.4)

    svg = Format("svg", [".svg"], svg_operators(), generate_filter_glob=BVERSION < 3.3)

    usd = Format("usd", [".usd", ".usda", ".usdc", ".usdz"], usd_operators(), generate_filter_glob=BVERSION < 3.3)

    x3d = Format("x3d", [".x3d", ".wrl"], x3d_operators(), generate_filter_glob=True)

    dxf = Format("dxf", [".dxf"], dxf_operators(), generate_filter_glob=True)

    pdb = Format("pdb", [".pdb"], pdb_operators(), generate_filter_glob=BVERSION > 3.6)

    xyz = Format("xyz", [".xyz"], xyz_operators(), generate_filter_glob=BVERSION > 3.6)

    stl = Format("stl", [".stl"], stl_operators(), generate_filter_glob=BVERSION < 3.3)

    image = Format(
        "image",
        [
            ".jpg",
            ".jpeg",
            ".gif",
            ".png",
            ".tif",
            ".tiff",
            ".tga",
            ".bmp",
            ".cin",
            ".dpx",
            ".jp2",
            ".j2c",
            ".sig",
            ".rgb",
            ".bw",
            ".webp",
            ".hdr",
            ".exr",
            ".mov",
            ".mp4",
            ".mkv",
            ".mpg",
            ".mpeg",
            ".dvd",
            ".vob",
            ".avi",
            ".dv",
            ".flv",
            ".webm",
        ],
        image_operators(),
    )

    sound = Format(
        "sound",
        [".wav", ".flac", ".mp2", ".mp3", ".aac", ".ogg", ".pcm", ".opus", ".l16", ".aiff", ".au"],
        sound_operators(),
        ignore=["files", "filepath", "directory"],
    )

    vdb = Format("vdb", [".vdb"], vdb_operators())

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
