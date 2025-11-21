import bpy
import os
from universal_multi_importer.umi_const import get_umi_settings
from universal_multi_importer.preferences.formats.properties.properties import update_file_stats

def get_file_selection():
    umi_settings = get_umi_settings()
    idx = umi_settings.umi_file_selection_idx
    file_selection = umi_settings.umi_file_selection

    active = file_selection[idx] if len(file_selection) else None

    return idx, file_selection, active


class UI_Select(bpy.types.Operator):
    bl_idname = "scene.umi_select_file"
    bl_label = "Select File"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}
    bl_description = "Select Files"

    action: bpy.props.EnumProperty(items=[("SELECT", "Select", ""), ("DESELECT", "Deselect", "")])
    mode: bpy.props.EnumProperty(items=[('ALL', 'All', ''), ('EXTENSION', 'Extension', ''), ('SIZE', 'Size', ''), ('NAME', 'name', ''), ('MD5', 'md5', '')])

    @classmethod
    def poll(cls, context):
        umi_settings = get_umi_settings()
        return len(umi_settings.umi_file_selection)
    
    @property
    def bool_action(self):
        return True if self.action == "SELECT" else False
    
    def invoke(self, context, event):
        self.umi_settings = get_umi_settings()
        return self.execute(context)

    def execute(self, context):
        _, self.file_selection, _ = get_file_selection()
        
        self.umi_settings.umi_file_stat_update = False

        if self.mode == "ALL":
            for f in self.file_selection:
                f.check = self.bool_action
        elif self.mode == "EXTENSION":
            for f in self.file_selection:
                if os.path.splitext(f.name)[1].lower() == self.umi_settings.umi_file_extension_selection:
                    f.check = self.bool_action
        elif self.mode == "SIZE":
            for f in self.file_selection:
                if f.size > self.umi_settings.umi_file_size_min_selection and f.size < self.umi_settings.umi_file_size_max_selection:
                    f.check = self.bool_action
        elif self.mode == "NAME":
            for f in self.file_selection:
                name = os.path.splitext(f.name)[0]
                ref = self.umi_settings.umi_file_name_selection

                if not self.umi_settings.umi_file_name_include_folder_selection:
                    name = os.path.basename(name)

                if not self.umi_settings.umi_file_name_case_sensitive_selection:
                    name = name.lower()
                    ref = ref.lower()
                    
                if ref in name:
                    f.check = self.bool_action
        elif self.mode == 'MD5':
            bpy.ops.import_scene.tila_universal_multi_importer_md5_check()
            wm = context.window_manager
            self._timer = wm.event_timer_add(0.01, window=context.window)
            wm.modal_handler_add(self)
            return {'RUNNING_MODAL'}
            

        self.umi_settings.umi_file_stat_update = True
        update_file_stats(self, context)
        return {'FINISHED'}
    
    def modal(self, context, event):
        if self.umi_settings.umi_md5_generation_status != 'DONE':
            return {'RUNNING_MODAL'}
        else:
            self.check_md5(self.file_selection)
            self.umi_settings.umi_md5_generation_status != 'NOT_STARTED'
            context.window_manager.event_timer_remove(self._timer)
            self.umi_settings.umi_file_stat_update = True
            update_file_stats(self, context)
            bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)
            return {'FINISHED'}

    def check_md5(self, file_selection):
        md5 = [f.md5 for f in file_selection]
        duplicates = self.list_duplicates(md5)
        
        for d in duplicates:
            for dd in range(len(d[1])):
                if dd == 0 and file_selection[d[1][dd]].check:
                    continue
                file_selection[d[1][dd]].check = self.bool_action
    
    # from https://stackoverflow.com/questions/5419204/index-of-duplicates-items-in-a-python-list
    def list_duplicates(self, seq):
        from collections import defaultdict
        tally = defaultdict(list)
        for i,item in enumerate(seq):
            tally[item].append(i)
        return ((key,locs) for key,locs in tally.items() 
                                if len(locs)>1)

classes = ( UI_Select, 
            )

def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)


def unregister():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)

if __name__ == "__main__":
    register()