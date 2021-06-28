import bpy, os, logging, tempfile
from os import path
from mathutils import Color
import blf
import gpu

def get_log_file():
	try:
		filepath = bpy.data.filepath
	except AttributeError:
		filepath = ''
	if path.exists(filepath):
		log_file = path.join(path.dirname(filepath), '{}.log'.format(path.splitext(path.basename(filepath))[0]))
	else:
		tempf = tempfile.TemporaryFile().name
		log_file = '{}.log'.format(tempf) 

	return log_file

def color_mult(c1, c2):
	return Color((c1.r * c2.r, c1.g * c2.g, c1.b * c2.b))

class Logger(object):
	def __init__(self, context='ROOT'):
		self.context = context
		self.module_name = os.path.basename(os.path.dirname(os.path.realpath(__file__))).capitalize

		self.log_file = get_log_file()
		self.timeformat = '%m/%d/%Y %I:%M:%S %p'
		self.set_basic_config()

		self.successes = []
		self.failures = []
		self.messages = []

		self._pretty = '---------------------'

		self.color = bpy.context.preferences.themes['Default'].view_3d.object_selected
		self.fontsize = 12

	def info(self, message, skip_prefix=False):
		self.set_basic_config()
		if not skip_prefix:
			message = '{} : INFO - '.format(self.context) + message
		self.messages.append({'message':message, 'color':self.color})
		logging.info(message)
	
	def success(self, message, skip_prefix=False):
		self.set_basic_config()
		if not skip_prefix:
			message = '{} : SUCCESS - '.format(self.context) + message
		self.messages.append({'message':message, 'color':color_mult(self.color,  Color((0.5, 1.0, 0.5)))})
		logging.info(message)

	def debug(self, message, skip_prefix=False):
		self.set_basic_config()
		if not skip_prefix:
			message = '{} : DEBUG - '.format(self.context) + message
		self.messages.append({'message':message, 'color':self.color * 0.2})
		logging.debug(message)

	def warning(self, message, skip_prefix=False):
		self.set_basic_config()
		if not skip_prefix:
			message = '{} : WARNING - '.format(self.context) + message
		self.messages.append({'message':message, 'color':color_mult(self.color,  Color((1.0, 1.0, 0.5)))})
		logging.warning(message)

	def error(self, message, skip_prefix=False):
		self.set_basic_config()
		if not skip_prefix:
			message = '{} : ERROR - '.format(self.context) + message
		self.messages.append({'message':message, 'color':color_mult(self.color,  Color((1.0, 0.5, 0.5)))})
		logging.error(message)

	def set_basic_config(self):
		self.format = '{} : %(asctime)s - %(levelname)s : {} :    %(message)s'.format(self.module_name, self.context)
		logging.basicConfig(filename=self.log_file, level=logging.DEBUG, datefmt=self.timeformat, filemode='w', format=self.format)

	def store_success(self, success):
		self.successes.append(success)
	
	def store_failure(self, failure):
		self.failures.append(failure)

	def clear_message(self):
		self.messages = []
	
	def clear_success(self):
		self.successes = []

	def clear_failure(self):
		self.failures = []
	
	def clear_all(self):
		self.clear_message()
		self.clear_success()
		self.clear_failure()

	def pretty(self, str):

		p = self._pretty

		for c in str:
			p += '-'
		
		return p

	def separator(self):
		self.info('', True)
		self.info('----------------------------------------------------------', True)
		self.info('', True)

	def draw_callback_px(self, context):

		font_id = 0  # XXX, need to find out how best to get this.
		
		# draw some text
		blf.size(font_id, self.fontsize, 72)
		pos = 30
		for m in reversed(self.messages):
			blf.color(font_id, m['color'].r, m['color'].g, m['color'].b, 0.5)
			blf.position(font_id, self.fontsize, pos, 0)
			blf.draw(font_id, m['message'])
			pos += self.fontsize + 3

class LoggerProgress(Logger):
	def __init__(self, context='ROOT'):
		super(LoggerProgress, self).__init__(context)

	def init_progress_importer(self, file_name):

		pretty = self.pretty(file_name)

		self.info('----------------------------------------------------------' + pretty)
		self.info('----------------------------- Importing File "{}" -----------------------------'.format(file_name))
		self.info('----------------------------------------------------------' + pretty)

	def complete_progress_importer(self):
		self.separator()

		self.info('Import Completed with {} success and {} failure'.format(len(self.successes), len(self.failures)))
		for s in self.successes:
			self.success('{}'.format(s))
		for f in self.failures:
			self.error('{}'.format(f))