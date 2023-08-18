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
		self.esc_message = ''
		self.message_offset = 0
		self.scroll_offset = 0
		self.completed = False
		self.show_log = True

		self._pretty = '---------------------'

		self.color = bpy.context.preferences.themes['Default'].view_3d.object_selected
		self.fontsize = 12
	
	def revert_parameters(self):
		self.scroll_offset = 0
		self.completed = False
		self.successes = []
		self.failures = []
		self.messages = []
	
	def info(self, message, skip_prefix=False, color=None):
		self.set_basic_config()
		if not skip_prefix:
			message = '{} : INFO - '.format(self.context) + message
		
		if color is not None:
			self.messages.append({'message':message, 'color':Color(color)})
		else:
			self.messages.append({'message':message, 'color':self.color})
			
		logging.info(message)
	
	def success(self, message, skip_prefix=False, show_message=True):
		self.set_basic_config()
		if not skip_prefix:
			message = '{} : SUCCESS - '.format(self.context) + message
			
		self.messages.append({'message':message, 'color':color_mult(self.color,  Color((0.5, 1.0, 0.5)))})
		
		if show_message :
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
		if not self.show_log:
			return
		
		font_id = 0  # XXX, need to find out how best to get this.

		# draw some text
		blf.size(font_id, self.fontsize, 72)
		pos = 30
		line_width = self.fontsize + 3
		for m in reversed(self.messages):
			blf.color(font_id, m['color'].r, m['color'].g, m['color'].b, 0.5)
			blf.position(font_id, self.fontsize, pos + self.scroll_offset, 0)
			blf.draw(font_id, m['message'])
			pos += line_width
		
		for area in bpy.context.screen.areas:
			if area.type == 'VIEW_3D':
				self.view3d = area
				break
		else:
			self.view3d = None

		if self.view3d is None:
			offset = 1500
		else:
			offset = self.view3d.width - 85

		# [ESC]
		blf.color(font_id, self.color.r,self.color.g,self.color.b, 0.5)
		blf.position(font_id, offset - self.message_offset, self.fontsize, 0)
		blf.draw(font_id, self.esc_message)
		
		# [SCROLL]
		if self.completed:
			message = "[CTRL] + [SCROLL_WHEEL] to parse Log"
			blf.position(font_id, offset -155, self.fontsize + line_width, 0)
			blf.draw(font_id, message)
	


class LoggerProgress(Logger):
	def __init__(self, context='ROOT'):
		super(LoggerProgress, self).__init__(context)

	def init_progress_importer(self, file_name):

		pretty = self.pretty(file_name)

		self.info('----------------------------------------------------------' + pretty)
		self.info('----------------------------- Importing File "{}" -----------------------------'.format(file_name))
		self.info('----------------------------------------------------------' + pretty)

	def complete_progress_importer(self, duration=0, show_successes=True, size=0, batch_count=0):
		self.separator()

		self.info(f'Completed with {len(self.successes)} success(es) and {len(self.failures)} failure(s)')
		stats = f'{duration}s'
		if size:
			stats += f' | {round(size, 2)}MB'
		if batch_count:
			stats += f' | {batch_count} batche(s)'
		
		self.info(stats)
		if show_successes:
			for s in self.successes:
				self.success('{}'.format(s))
		for f in self.failures:
			self.error('{}'.format(f))