from universal_multi_importer.preferences.formats.panels import draw_panel, draw_version_warning

class IMPORT_SCENE_SOUNDSettings():
    @draw_version_warning
    def draw(self, operator, module_name,  layout):

        layout.use_property_split = True
        layout.use_property_decorate = False

        op=[[operator, 'relative_path'],
            [operator, 'cache'],
            [operator, 'mono']]

        draw_panel(layout, op, 'AUDIOSettings_options', 'Options', 'OPTIONS')
