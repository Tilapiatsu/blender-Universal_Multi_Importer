from typing import Callable


default_color = (0.1, 0.5, 0.6)


class LoggerColors:
    def __init__(self, get_colors: Callable) -> None:
        self.get_colors = get_colors

    def safe_get_color(func):
        def wrapper(self):
            colors = self.get_colors()
            if colors is None:
                return default_color
            else:
                return getattr(colors, func())

        return wrapper

    @safe_get_color
    def DEFAULT_COLOR():
        return "info_color"

    @safe_get_color
    def SUCCESS_COLOR():
        return "success_color"

    @safe_get_color
    def CANCELLED_COLOR():
        return "cancelled_color"

    @safe_get_color
    def WARNING_COLOR():
        return "warning_color"

    @safe_get_color
    def ERROR_COLOR():
        return "error_color"

    @safe_get_color
    def COMMAND_COLOR():
        return "command_color"

    @safe_get_color
    def COMMAND_WARNING_COLOR():
        return "command_warning_color"

    @safe_get_color
    def IMPORT_COLOR():
        return "import_color"


class MessageType:
    MESSAGE = "Message"
    SUCCESS = "Success"
    WARNING = "Warning"
    ERROR = "Error"


SCROLL_OFFSET_INCREMENT = 50
