import bpy
from typing import Optional
from dataclasses import dataclass


@dataclass
class ImportSession:
    file_extension_selection_items: Optional[list[tuple[str, str, str]]]
    file_selected_format_items: Optional[list[tuple[str, str, str]]]

    def __init__(self) -> None:
        pass

    def set_file_extension_selection_items(self, extensions: list[str]) -> None:
        self.file_extension_selection_items = [(e, e, "") for e in extensions]

    def set_file_selected_format_items(self, formats: list[str]) -> None:
        self.file_selected_format_items = [(f, f, "") for f in formats]
