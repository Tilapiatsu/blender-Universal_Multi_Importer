import bpy, os, logging, tempfile, time
from os import path
from mathutils import Color
from .logger_const import LoggerColors, MessageType

def get_log_file():

    log_file = "UMI_" + time.strftime(f"%Y%m%d") + ".log"
    log_file = path.join(tempfile.gettempdir(), log_file)
    
    print('UMI : Log file path :', log_file)

    return log_file


def color_mult(c1, c2):
    return Color((c1.r * c2.r, c1.g * c2.g, c1.b * c2.b))

# From https://stackoverflow.com/questions/30919275/inserting-period-after-every-3-chars-in-a-string
def insert_str(my_str, each=50, char='\n'):
    my_str = str(my_str)
    return char.join(my_str[i:i+each] for i in range(0, len(my_str), each))

# from https://stackoverflow.com/questions/9475241/split-string-every-nth-character
def split_str(string, each=150):
    return [string[i:i+each] for i in range(0, len(string), each)]

class Message():
    def __init__(self, message='', color=Color((1,1,1))):
        self.message = message
        self.color = color


class MessageColored():
    def __init__(self):
        self._messages = []
        self.count = 0

    @property
    def messages(self):
        return self._messages

    def append(self, message:str, color:Color=Color((1,1,1))):
        splitted = split_str(message)
        for s in splitted:
            self._messages.append(Message(message=s, color=color))

        self.count += 1

    def __len__(self):
        return len(self._messages)
    
    def __getitem__(self, item):
        return self._messages[item]
    
    

class Logger():
    def __init__(self, log_name='ROOT'):
        self.log_name = log_name

        self.log_file = get_log_file()
        self.timeformat = '%m/%d/%Y %I:%M:%S %p'
        self.set_basic_config()

        self.successes = []
        self.failures = []
        self.warnings = []
        self.messages = MessageColored()
        self.message_types = []

        self._pretty = '---------------------'

        self.color = Color(LoggerColors.DEFAULT_COLOR())
        self.fontsize = 12
    
    def revert_parameters(self):
        self.successes = []
        self.failures = []
        self.warnings = []
        self.message_types = []
        self.messages = MessageColored()


    def info(self, message, skip_prefix=False, color=None):
        self.color = Color(LoggerColors.DEFAULT_COLOR())
        message = str(message)
        self.set_basic_config()
        if not skip_prefix:
            message = '{} : INFO - '.format(self.log_name) + message
        
        if color is not None:
            self.messages.append(message=message, color=Color(color))
        else:
            self.messages.append(message=message, color=Color(LoggerColors.DEFAULT_COLOR()))
            
        logging.info(message)
    
    def success(self, message, skip_prefix=False, show_message=True):
        message = str(message)
        self.set_basic_config()
        if not skip_prefix:
            message = '{} : SUCCESS - '.format(self.log_name) + message
            
        self.messages.append(message=message, color=Color(LoggerColors.SUCCESS_COLOR()))
        
        if show_message :
            logging.info(message)

    def debug(self, message, skip_prefix=False):
        message = str(message)
        self.set_basic_config()
        if not skip_prefix:
            message = '{} : DEBUG - '.format(self.log_name) + message
        self.messages.append(message=message, color=self.color * 0.2)
        logging.debug(message)

    def warning(self, message, skip_prefix=False):
        message = str(message)
        self.set_basic_config()
        if not skip_prefix:
            message = '{} : WARNING - '.format(self.log_name) + message
        self.messages.append(message=message, color= Color(LoggerColors.WARNING_COLOR()))
        logging.warning(message)

    def error(self, message, skip_prefix=False):
        message = str(message)
        self.set_basic_config()
        if not skip_prefix:
            message = '{} : ERROR - '.format(self.log_name) + message
        self.messages.append(message=message, color= Color(LoggerColors.ERROR_COLOR()))
        logging.error(message)

    def set_basic_config(self):
        self.format = '%(asctime)s - %(levelname)s :    %(message)s'
        logging.basicConfig(filename=self.log_file, level=logging.DEBUG, datefmt=self.timeformat, filemode='w', format=self.format)

    def store_success(self, success):
        success = str(success)
        self.successes.append(success)
        self.message_types.append(MessageType.SUCCESS)
    
    def store_failure(self, failure):
        failure = str(failure)
        self.failures.append(failure)
        self.message_types.append(MessageType.ERROR)

    def store_warning(self, warning):
        warning = str(warning)
        self.warnings.append(warning)
        self.message_types.append(MessageType.WARNING)

    def clear_message(self):
        self.messages = MessageColored()
    
    def clear_success(self):
        self.successes = []

    def clear_failure(self):
        self.failures = []
    
    def clear_warning(self):
        self.warnings = []

    def clear_message_types(self):
        self.message_types = []
    
    def clear_all(self):
        self.clear_message()
        self.clear_success()
        self.clear_failure()
        self.clear_warning()
        self.clear_message_types()

    def pretty(self, str):

        p = self._pretty

        for _ in str:
            p += '-'
        
        return p

    def separator(self):
        self.info('', True)
        self.info('----------------------------------------------------------', True)
        self.info('', True)