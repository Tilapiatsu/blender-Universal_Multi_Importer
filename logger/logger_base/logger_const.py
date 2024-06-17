from ...umi_const import get_umi_colors

default_color = (0.1, 0.5, 0.6)

class LoggerColors():
    def safe_get_color(func):
        def wrapper():
            umi_colors = get_umi_colors()
            if umi_colors is None:
                return default_color
            else:
                return getattr(umi_colors, func())


        return wrapper
    @staticmethod
    @safe_get_color
    def DEFAULT_COLOR   (): 
        return 'umi_info_color'

    @staticmethod
    @safe_get_color
    def SUCCESS_COLOR   (): 
        return 'umi_success_color'

    @staticmethod
    @safe_get_color
    def CANCELLED_COLOR (): 
        return 'mi_cancelled_color'

    @staticmethod
    @safe_get_color
    def WARNING_COLOR   (): 
        return 'umi_warning_color'

    @staticmethod
    @safe_get_color
    def ERROR_COLOR     (): 
        return 'umi_error_color'

    @staticmethod
    @safe_get_color
    def COMMAND_COLOR   (): 
        return 'umi_command_color'
    
    @staticmethod
    @safe_get_color
    def IMPORT_COLOR    (): 
        return 'umi_import_color'

class MessageType():
    MESSAGE = 'Message'
    SUCCESS = 'Success'
    WARNING = 'Warning'
    ERROR = 'Error'

SCROLL_OFFSET_INCREMENT = 50

