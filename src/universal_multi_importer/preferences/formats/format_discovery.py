from __future__ import annotations

import addon_utils
import bpy


class FormatDiscovery:
    def __init__(self, compatible_formats):
        self.compatible_formats = compatible_formats

        self.available = set()
        self.properties = {}

        self.pending = {}
        self.unavailable = {}

        # Snapshot provider state once, after startup.
        self.enabled_addons = set(bpy.context.preferences.addons.keys())

        self.installed_addons = {module.__name__ for module in addon_utils.modules()}

    @staticmethod
    def resolve_command(command_string):
        try:
            command = bpy

            for part in command_string.split(".")[1:]:
                command = getattr(command, part, None)

                if command is None:
                    return None

            return command

        except (AttributeError, RuntimeError):
            return None

    def _handle_missing(self, key, operator):

        provider = operator.addon_name

        if provider is None:
            self.pending[key] = "Operator not registered"
            return

        if provider not in self.installed_addons:
            self.unavailable[key] = "Provider not installed"
            return

        if provider not in self.enabled_addons:
            self.unavailable[key] = "Provider disabled"
            return

        self.pending[key] = "Waiting for provider registration"

    def update(self):
        self.available.clear()
        self.properties.clear()
        self.pending.clear()
        self.unavailable.clear()

        for format_name, format in self.compatible_formats.all_formats.items():
            for operator_name, operator in format.operators.items():
                key = (format_name, operator_name)

                if operator.invalid:
                    self.unavailable[key] = "Invalid operator definition"
                    continue

                # Operators exposing a bpy.types module.
                if operator.module is not None:
                    module = getattr(
                        bpy.types,
                        operator.module,
                        None,
                    )

                    if module is not None:
                        self.available.add(key)
                    else:
                        self._handle_missing(key, operator)

                    continue

                # Regular bpy.ops operators.
                command = self.resolve_command(operator.command)

                if command is None:
                    self._handle_missing(key, operator)
                    continue

                try:
                    rna = command.get_rna_type()
                    properties = tuple(rna.properties)

                except (KeyError, RuntimeError, AttributeError):
                    self._handle_missing(key, operator)
                    continue

                self.available.add(key)
                self.properties[key] = properties

        return not self.pending

    def expire_pending(self):
        for key, reason in self.pending.items():
            self.unavailable[key] = f"Registration timeout: {reason}"

        self.pending.clear()
