import bpy, os, tempfile, time

def get_latest_log_file():
    tempdir = tempfile.gettempdir()
    tempfiles = os.listdir(tempdir)

    assert len(tempfiles)
    tempfiles = [f for f in tempfiles if os.path.basename(f).startswith('UMI_')]
    
    assert len(tempfiles)
    tempfiles = sorted(tempfiles)
    log_file = os.path.join(tempdir, tempfiles[0])

    return log_file


class UI_UMIOpenLogFile(bpy.types.Operator):
    bl_idname = "scene.umi_open_log_file"
    bl_label = "Open Log File"
    bl_options = {'REGISTER', 'UNDO'}
    bl_description = "Open Last Log File"


    def execute(self, context):
        log_file = get_latest_log_file()
        if not os.path.exists(log_file):
            self.report({'ERROR'}, 'UMI : No valid log file found')
            return {'CANCELLED'}
        
        filename = os.path.basename(log_file)
        if filename in bpy.data.texts:
              bpy.data.texts.remove(bpy.data.texts[filename])

        bpy.data.texts.load(log_file)

        text = bpy.data.texts[filename]
        
        bpy.ops.wm.window_new()
        log_win = context.window_manager.windows[-1]
        log_ed = log_win.screen.areas[0]
        log_ed.type = 'TEXT_EDITOR'
        log_ed.spaces[0].text = text
        log_ed.spaces[0].show_line_numbers = False
        log_ed.spaces[0].show_syntax_highlight = False
        bpy.ops.text.move(type='FILE_TOP')

        return {'FINISHED'}
    
classes = (UI_UMIOpenLogFile,)

def register():
	from bpy.utils import register_class
	for cls in classes:
		register_class(cls)

def unregister():
	from bpy.utils import unregister_class
	for cls in reversed(classes):
		unregister_class(cls)