class ModuleName:
    def __init__(self):
        self._module_name : str = None

    @property
    def module_name(self) -> str:
        if self._module_name is None:
            self._module_name = self._get_module_name()

        return self._module_name

    @staticmethod
    def _get_module_name() -> str:
        import addon_utils
        from pathlib import Path

        for m in addon_utils.modules():
            if m.bl_info.get("name") != 'Universal Multi Importer':
                continue

            return Path(m.__file__).parent.stem