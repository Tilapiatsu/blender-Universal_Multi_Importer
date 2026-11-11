from ....ui.panel import draw_panel, draw_version_warning, draw_no_settings, draw_import_as_geometry_node_settings


class IMPORT_SCENE_SPZSettings:
    @draw_version_warning
    def draw(self, operator, module_name, layout):
        if module_name == "default":
            draw_no_settings(layout)

        if module_name == "geometry_node":
            draw_import_as_geometry_node_settings(layout, operator, "SPZGNSettings")
