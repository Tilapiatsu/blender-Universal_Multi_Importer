from ....ui.panel import draw_panel, draw_version_warning


class IMPORT_SCENE_SKPSettings:
    @draw_version_warning
    def draw(self, operator, module_name, layout):
        layout.use_property_split = True
        layout.use_property_decorate = False  # No animation.

        op = [
            [operator, "scenes_as_camera"],
            [operator, "import_camera"],
            [operator, "reuse_material"],
            [operator, "dedub_only"],
            [operator, "reuse_existing_groups"],
        ]

        draw_panel(layout, op, "SKPSettings_primary", "Primary", icon="OPTIONS")

        op = [
            [operator, "max_instance"],
            [operator, "dedub_type"],
            [operator, "import_scene"],
        ]

        draw_panel(layout, op, "SKPSettings_instance", "Instantiate Components", icon="MOD_PARTICLE_INSTANCE")
