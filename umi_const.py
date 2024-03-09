import os
import bpy

ADDON_FOLDER_PATH = os.path.dirname(__file__)
ADDON_PACKAGE = __package__

def get_prefs():
	return bpy.context.preferences.addons[ADDON_PACKAGE].preferences

def get_umi_settings():
	return get_prefs().umi_settings