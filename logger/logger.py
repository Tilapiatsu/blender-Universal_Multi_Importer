import bpy
import blf
from .logger_base import Logger, SCROLL_OFFSET_INCREMENT
from ..blender_version import BVERSION

class LoggerProgress(Logger):
	def __init__(self, log_name='ROOT'):
		super(LoggerProgress, self).__init__(log_name)
		self.esc_message = '[Esc] to Cancel'
		self.message_offset = 15
		self.scroll_offset = 0
		self.completed = False
		self.show_log = True
		
	def revert_parameters(self):
		super(LoggerProgress, self).revert_parameters()
		self.scroll_offset = 0
		self.completed = False
	
	def scroll(self, up=True, multiplier=1.0):
		sign = -1.0 if up else 1.0
		self.scroll_offset += sign * SCROLL_OFFSET_INCREMENT * multiplier

	def draw_callback_px(self, context):
		if not self.show_log and not self.completed:
			return
		
		font_id = 0  # XXX, need to find out how best to get this.

		# draw some text
		if BVERSION >= 4.0:
			blf.size(font_id, self.fontsize)
		else:
			blf.size(font_id, self.fontsize, 72)
		pos = 30
		line_width = self.fontsize + 3
		
		for m in reversed(self.messages):
			blf.color(font_id, m.color.r, m.color.g, m.color.b, 0.8)
			blf.position(font_id, self.fontsize, pos + self.scroll_offset, 0)
			blf.draw(font_id, m.message)
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
			blf.position(font_id, offset -155, self.fontsize + line_width * 2, 0)
			blf.draw(font_id, message)
			message = "[CTRL] + [SHIFT] + [SCROLL_WHEEL] to parse Log Faster"
			blf.position(font_id, offset -250, self.fontsize + line_width, 0)
			blf.draw(font_id, message)

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
				self.success(f'{s}')
		for f in self.warnings:
			self.warning(f'{f}')
		for f in self.failures:
			self.error(f'{f}')