from . import BVERSION

class IMPORT_SCENE_BLENDSettings():
    def draw(self, operator, module_name, layout):
        layout.use_property_split = True
        layout.use_property_decorate = False  # No animation.

        module = layout.row(align=True)
        module.prop(operator, 'import_module', expand=True)
        
        layout.separator()
        
        data = layout.box()
        data.label(text='Import Data', icon='IMPORT')

        row = data.row()
        row.alignment = 'EXPAND'
        col1 = row.column(align=True)
        col1.alignment = 'RIGHT'
        draw_import_data(col1, operator, 'Action', 'import_actions', 'ACTION')
        draw_import_data(col1, operator, 'Armature', 'import_armatures', 'OUTLINER_OB_ARMATURE')
        draw_import_data(col1, operator, 'Brushes', 'import_brushes', 'BRUSH_DATA')
        draw_import_data(col1, operator, 'Cameras', 'import_cameras', 'CAMERA_DATA')
        draw_import_data(col1, operator, 'Cache Files', 'import_cache_files', 'FILE_CACHE')
        draw_import_data(col1, operator, 'Curves', 'import_curves', 'OUTLINER_OB_CURVE')
        draw_import_data(col1, operator, 'Hair Curves', 'import_hair_curves', 'OUTLINER_OB_CURVES')
        draw_import_data(col1, operator, 'Fonts', 'import_fonts', 'OUTLINER_OB_FONT')
        draw_import_data(col1, operator, 'Grease Pencils', 'import_grease_pencils', 'OUTLINER_OB_GREASEPENCIL')
        draw_import_data(col1, operator, 'Collections', 'import_collections', 'OUTLINER_COLLECTION')
        draw_import_data(col1, operator, 'Images', 'import_images', 'IMAGE_DATA')
        draw_import_data(col1, operator, 'Lights', 'import_lights', 'LIGHT')
        draw_import_data(col1, operator, 'Line Styles', 'import_linestyles', 'LINE_DATA')
        draw_import_data(col1, operator, 'Lattices', 'import_lattices', 'LATTICE_DATA')
        draw_import_data(col1, operator, 'Masks', 'import_masks', 'MOD_MASK')
        draw_import_data(col1, operator, 'Materials', 'import_materials', 'MATERIAL')
        draw_import_data(col1, operator, 'Metaballs', 'import_metaballs', 'OUTLINER_OB_META')

        col2 = row.column(align=True)
        col2.alignment = 'RIGHT'
        draw_import_data(col2, operator, 'Meshes', 'import_meshes', 'MESH_DATA')
        draw_import_data(col2, operator, 'Movie Clips', 'import_movieclips', 'FILE_MOVIE')
        draw_import_data(col2, operator, 'Node Groups', 'import_node_groups', 'NODETREE')
        draw_import_data(col2, operator, 'Objects', 'import_objects', 'OBJECT_DATA')
        draw_import_data(col2, operator, 'Paint Curves', 'import_paint_curves', 'CURVE_BEZCURVE')
        draw_import_data(col2, operator, 'Palettes', 'import_palettes', 'RESTRICT_COLOR_ON')
        draw_import_data(col2, operator, 'Particles', 'import_particles', 'PARTICLE_DATA')
        draw_import_data(col2, operator, 'Point Clouds', 'import_pointclouds', 'OUTLINER_OB_FONT')
        if BVERSION >=4.1:
            icon = 'LIGHTPROBE_SPHERE'
        else:
            icon = 'LIGHTPROBE_CUBEMAP'
        draw_import_data(col2, operator, 'Light Probes', 'import_lightprobes', icon)
        draw_import_data(col2, operator, 'Scene', 'import_scenes', 'SCENE_DATA')
        draw_import_data(col2, operator, 'Sounds', 'import_sounds', 'PLAY_SOUND')
        draw_import_data(col2, operator, 'Speakers', 'import_speakers', 'PLAY_SOUND')
        draw_import_data(col2, operator, 'Texts', 'import_texts', 'FILE_TEXT')
        draw_import_data(col2, operator, 'Textures', 'import_textures', 'TEXTURE')
        draw_import_data(col2, operator, 'Volumes', 'import_volumes', 'VOLUME_DATA')
        draw_import_data(col2, operator, 'Worlds', 'import_worlds', 'WORLD')
        draw_import_data(col2, operator, 'Workspaces', 'import_workspaces', 'WORKSPACE')

        col3 = row.column(align=True)
        col3.alignment = 'RIGHT'
        col3.label(text='')

def draw_import_data(layout, operator, name, prop_name, icon):
    row1 = layout.row()
    row1.alignment = 'RIGHT'
    row1.label(text=name)
    row1.label(text='', icon=icon)
    row1.prop(operator, prop_name, text='')
