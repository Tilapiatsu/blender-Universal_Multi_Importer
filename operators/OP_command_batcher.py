import bpy
import time, math
from ..preferences.formats.properties import PG_Operator
from ..logger import LOG, LoggerColors
from ..umi_const import get_umi_settings

def draw_operators(self, context, layout, operators, operator_name:str, operator_id_name:str) -> None:
    box = layout.box()
    row = box.row()

    row.label(text='Commands', icon='SCRIPTPLUGINS')

    rows = len(operators) if len(operators) > 2 else 2
    row = box.row()
    col1 = row.column(align=True)
    col1.template_list('UMI_UL_operator_list', '', self.umi_settings, operator_name, self.umi_settings, operator_id_name, rows=rows)
    col1.prop(self.umi_settings.umi_global_import_settings, 'ignore_command_batcher_errors')

    col2 = row.column()

    col2.separator()

    col2.operator('scene.umi_add_operator', text='', icon='ADD')
    col2.separator()
    move = col2.operator('scene.umi_move_operator', text='', icon='TRIA_UP')
    move.direction = 'UP'

    move = col2.operator('scene.umi_move_operator', text='', icon='TRIA_DOWN')
    move.direction = 'DOWN'
    col2.separator()
    col2.operator('scene.umi_clear_operators', text='', icon='TRASH')


def draw_command_batcher(self, context, layout):
    col = layout.column()
    tabs = col.row(align=True)
    tabs.prop_tabs_enum(self.umi_settings, 'umi_command_batcher_settings')
    col2 = col.column(align=True)

    if self.umi_settings.umi_command_batcher_settings == "PRE_PROCESS":
        col2.label(text='These operators will be executed ONCE before importing/processing the selected elements')
        draw_operators(self, context, col2, self.umi_settings.umi_pre_operators, 'umi_pre_operators', 'umi_pre_operator_idx')
    elif self.umi_settings.umi_command_batcher_settings == "EACH_ELEMENTS":
        col2.label(text='These operators will be executed on EACH imported/selected elements')
        draw_operators(self, context, col2, self.umi_settings.umi_each_operators, 'umi_each_operators', 'umi_each_operator_idx')
    elif self.umi_settings.umi_command_batcher_settings == "POST_PROCESS":
        col2.label(text='These operators will be executed ONCE after all elements are imported/processed')
        draw_operators(self, context, col2, self.umi_settings.umi_post_operators, 'umi_post_operators', 'umi_post_operator_idx')

    box = col.box()
    row = box.row()
    row.label(text='Presets', icon='PRESET')

    rows = len(self.umi_settings.umi_presets) if len(self.umi_settings.umi_presets) > 2 else 2
    row = box.row()
    row.template_list('UMI_UL_preset_list', '', self.umi_settings, 'umi_presets', self.umi_settings, 'umi_preset_idx', rows=rows)
    col2 = row.column()
    col2.separator()
    col2.operator('scene.umi_add_preset', text='', icon='ADD')
    col2.separator()
    col2.operator('scene.umi_move_preset', text='', icon='TRIA_UP').direction = 'UP'
    col2.operator('scene.umi_move_preset', text='', icon='TRIA_DOWN').direction = 'DOWN'
    col2.separator()
    col2.operator('scene.umi_clear_presets', text='', icon='TRASH')


    if self.bl_label == CommandBatcher.bl_label:
        box = col.box()
        box.label(text='Log Display', icon='WORDWRAP_ON')
        row = box.row(align=True)
        row.use_property_split = True
        row.use_property_decorate = False
        row.prop(self.umi_settings.umi_global_import_settings, 'show_log_on_3d_view')
        col = row.column(align=True)
        col.prop(self.umi_settings.umi_global_import_settings, 'auto_hide_text_when_finished')
        if self.umi_settings.umi_global_import_settings.auto_hide_text_when_finished:
            col.prop(self.umi_settings.umi_global_import_settings, 'wait_before_hiding')


class CommandBatcher(bpy.types.Operator):
    bl_idname = "object.tila_umi_command_batcher"
    bl_label = "Command Batcher"
    bl_options = {'REGISTER'}

    importer_mode : bpy.props.BoolProperty(name='Importer_mode', default=False)
    execute_each_process : bpy.props.BoolProperty(name='Execute Each process commands', default=True)
    execute_pre_process : bpy.props.BoolProperty(name='Execute Pre process commands', default=True)
    execute_post_process : bpy.props.BoolProperty(name='Execute Post process commands', default=True)

    finished = False
    current_command = None
    progress = 0
    processing = False
    process_complete = False
    canceled = False
    end = False
    counter = 0
    counter_start_time = 0.0
    counter_end_time = 0.0
    delta = 0.0
    previous_counter = 0
    objects_to_process = []
    current_object_to_process = None
    _timer = None

    def fill_operator_to_process(self, each_only=False):
        if self.execute_each_process:
            self.operators_to_process = [o.operator for o in self.umi_settings.umi_each_operators if o.enabled]
            self.operators_to_process.reverse()

        if not each_only:
            if self.execute_pre_process:
                self.pre_operators_to_process = [o.operator for o in self.umi_settings.umi_pre_operators if o.enabled]
                self.pre_operators_to_process.reverse()

            if self.execute_post_process:
                self.post_operators_to_process = [o.operator for o in self.umi_settings.umi_post_operators if o.enabled]
                self.post_operators_to_process.reverse()

    def decrement_counter(self):
        self.counter = self.counter + (self.counter_start_time - self.counter_end_time)*1000

    def store_delta_start(self):
        self.counter_start_time = time.perf_counter()

    def store_delta_end(self):
        self.counter_end_time = time.perf_counter()

    def log_end_text(self):
        LOG.info('-----------------------------------')
        if self.canceled:
            LOG.info('Batch Process cancelled !', color=LoggerColors.CANCELLED_COLOR())
        else:
            if False in self.process_succeeded:
                LOG.info('Batch Process completed with errors !', color=LoggerColors.ERROR_COLOR())
                LOG.esc_message = '[Esc] to Hide'
                LOG.message_offset = 4
            else:
                LOG.info('Batch Process completed successfully !', color=LoggerColors.SUCCESS_COLOR())
                LOG.esc_message = '[Esc] to Hide'
                LOG.message_offset = 4
        LOG.info('Click [ESC] to hide this text ...')
        LOG.info('-----------------------------------')
        self.end_text_written = True
        bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)

    def invoke(self, context, event):
        self.umi_settings = get_umi_settings()
        if not self.importer_mode:
            bpy.ops.scene.umi_load_preset_list()

            wm = context.window_manager
            return wm.invoke_props_dialog(self, width=900)

        return self.execute(context)

    def finish(self, context, canceled=False):
        if not self.importer_mode:
            bpy.types.SpaceView3D.draw_handler_remove(self._handle, 'WINDOW')
        self.revert_parameters(context)
        bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)
        self.umi_settings.umi_batcher_is_processing = False
        if canceled:
            return {'CANCELLED'}
        else:
            return {'FINISHED'}

    def modal(self, context, event):
        if self.start_time == 0 :
            self.start_time = time.perf_counter()
        if not self.importer_mode and not self.end and event.type in {'ESC'} and event.value == 'PRESS':
            if not self.importer_mode:
                LOG.warning('Cancelling...')
            self.cancel(context)

            self.counter = self.umi_settings.umi_global_import_settings.wait_before_hiding
            self.end = True
            LOG.completed = True
            return {'RUNNING_MODAL'}

        if not self.importer_mode and self.end:

            if not self.end_text_written:
                self.log_end_text()
                LOG.completed = True
                bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)

            if event.type in {'WHEELUPMOUSE'} and event.ctrl and event.shift:
                LOG.scroll(up=True, multiplier=9)
            elif event.type in {'WHEELDOWNMOUSE'} and event.ctrl and event.shift:
                LOG.scroll(up=False, multiplier=9)
            if event.type in {'WHEELUPMOUSE'} and event.ctrl:
                LOG.scroll(up=True)
                bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)
                return {'PASS_THROUGH'}
            elif event.type in {'WHEELDOWNMOUSE'} and event.ctrl:
                LOG.scroll(up=False)
                bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)
                return {'PASS_THROUGH'}

            if self.umi_settings.umi_global_import_settings.auto_hide_text_when_finished:
                self.store_delta_start()

                if self.counter == self.umi_settings.umi_global_import_settings.wait_before_hiding:
                    self.previous_counter = self.counter
                    self.store_delta_end()

                remaining_seconds = math.ceil(self.counter)

                if remaining_seconds < self.previous_counter:
                    LOG.info(f'Hidding in {remaining_seconds}s ...')
                    self.previous_counter = remaining_seconds

                if self.counter <= 0:
                    return self.finish(context, self.canceled)

            if event.type in {'ESC'} and event.value == 'PRESS':
                return self.finish(context, self.canceled)

            if self.umi_settings.umi_global_import_settings.auto_hide_text_when_finished:
                self.previous_counter = remaining_seconds
                self.store_delta_end()
                self.decrement_counter()
                bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)

            return {'RUNNING_MODAL'}

        if event.type == 'TIMER':
            if self.start_time == 0:
                self.start_time = time.perf_counter()

            if not self.pre_processing and not self.processing and self.current_object_to_process is None and len(self.objects_to_process): # Process can start
                self.next_object()

            elif self.pre_processing:
                pass

            elif self.current_object_to_process is None and len(self.objects_to_process):
                self.processing = False

            elif self.current_object_to_process is None and len(self.objects_to_process) == 0 and not self.post_process_done and not self.post_processing:
                if len(self.post_operators_to_process) and self.execute_post_process:
                    LOG.info(f'Start Post-Processing commands', color=LoggerColors.DEFAULT_COLOR())
                    self.post_processing = True
                    self.each_process_done = True
                else:
                    self.each_process_done = True
                    self.post_process_done = True

            elif self.current_object_to_process is None and len(self.objects_to_process) == 0 and self.post_process_done:
                if not self.importer_mode:
                    LOG.complete_progress_importer(show_successes=False, duration=round(time.perf_counter() - self.start_time, 2))
                    self.counter = self.umi_settings.umi_global_import_settings.wait_before_hiding
                else:
                    self.finished = True
                self.end = True

            if self.finished:
                return self.finish(context)

            if self.current_command is None and len(self.pre_operators_to_process):
                self.current_command = self.pre_operators_to_process.pop()

            elif not self.pre_process_done and self.current_command is None and not len(self.pre_operators_to_process):
                if not self.importer_mode:
                    LOG.info(f'Start processing Each Element commands', color=LoggerColors.DEFAULT_COLOR())
                self.pre_process_done = True
                self.pre_processing = False

            if self.pre_process_done and self.current_command is None and len(self.operators_to_process):
                self.current_command = self.operators_to_process.pop()
                return {'PASS_THROUGH'}

            elif not self.each_process_done and self.pre_process_done and self.current_command is None and not len(self.operators_to_process):
                self.current_object_to_process = None

            if self.each_process_done and self.current_command is None and len(self.post_operators_to_process):
                self.current_command = self.post_operators_to_process.pop()

            elif self.each_process_done and self.current_command is None and not len(self.post_operators_to_process):
                self.post_process_done = True
                return {'PASS_THROUGH'}

            if self.finished:
                self.end = True
                return {'PASS_THROUGH'}

            elif self.current_object_to_process is None and not self.each_process_done and not self.pre_processing:
                return {'PASS_THROUGH'}

            else:
                try: # Executing command
                    self.progress += 100 / self.number_of_operations_to_perform
                    self.current_operation_number += 1

                    LOG.info(f'Executing command {self.current_operation_number}/{self.number_of_operations_to_perform} - {round(self.progress,2)}% : "{self.current_command}"', color=LoggerColors.COMMAND_COLOR())
                    override = {}
                    if self.pre_process_done and not self.each_process_done:
                        override["selected_objects"] = [bpy.data.objects[self.current_object_to_process.name]]
                    with bpy.context.temp_override(**override):
                        exec(self.current_command, {'bpy':bpy})

                    LOG.store_success('Command executed successfully')
                    self.process_succeeded.append(True)
                except Exception as e:
                    message = f'{context.selected_objects[0].name} : Command "{self.current_command}" is not valid - {e}'
                    LOG.error(message)
                    LOG.store_failure(message)
                    self.process_succeeded.append(False)

                self.current_command = None

        return {'PASS_THROUGH'}

    def execute(self, context):
        self.completed = False
        self.succeedeed = False
        self.end_text_written = False
        self.start_time = 0
        self.process_succeeded = []
        self.umi_settings = get_umi_settings()
        LOG.esc_message = '[Esc] to Cancel'
        LOG.message_offset = 15

        if not self.importer_mode:
            LOG.revert_parameters()

        self.objects_to_process = [o for o in bpy.context.selected_objects]
        if self.execute_each_process and not len(self.objects_to_process):
            self.report({'ERROR_INVALID_INPUT'}, 'UMI : You need to select at least one object.')
            return {'CANCELLED'}

        if not self.importer_mode and not len(self.umi_settings.umi_each_operators):
            self.report({'ERROR_INVALID_INPUT'}, 'UMI : You need to add at least one command.')
            return {'CANCELLED'}

        self.progress = 0
        self.number_of_operations_to_perform = 0
        self.number_of_object_to_process = len(self.objects_to_process)
        self.current_operation_number = 0
        self.current_object_number = 0
        self.operators_to_process = []
        self.pre_operators_to_process = []
        self.post_operators_to_process = []
        self.pre_process_done = False
        self.each_process_done = False
        self.post_process_done = False
        self.pre_processing = False
        self.post_processing = False

        self.fill_operator_to_process()

        number_of_operations = len(self.operators_to_process)
        number_of_objects = len(self.objects_to_process)

        self.number_of_operations_to_perform = number_of_operations * number_of_objects + len(self.pre_operators_to_process) + len(self.post_operators_to_process)

        if not self.importer_mode:
            args = (context,)
            self._handle = bpy.types.SpaceView3D.draw_handler_add(LOG.draw_callback_px, args, 'WINDOW', 'POST_PIXEL')

        if len(self.pre_operators_to_process) and self.execute_pre_process:
            self.pre_processing = True
            LOG.info(f'Start Pre-Processing commands', color=LoggerColors.DEFAULT_COLOR())
        else:
            self.pre_process_done = True

        self.register_timer(context)
        self.umi_settings.umi_batcher_is_processing = True
        return {'RUNNING_MODAL'}

    def draw(self, context):
        draw_command_batcher(self, context, self.layout)

    def revert_parameters(self, context):
        self.finished = False
        self.progress = 0
        self.processing = False
        self.process_complete = False
        self.canceled = False
        self.end = False
        self.completed = False
        self.end_text_written = False
        self.process_succeeded = []
        context.window_manager.event_timer_remove(self._timer)
        if not self.importer_mode:
            LOG.clear_all()
            LOG.revert_parameters()

    def cancel(self, context):
        self.canceled = True
        if self._timer is not None:
            wm = context.window_manager
            wm.event_timer_remove(self._timer)

    def register_timer(self, context):
        wm = context.window_manager
        self._timer = wm.event_timer_add(0.01, window=context.window)
        wm.modal_handler_add(self)

    def next_object(self):
        if self.importer_mode:
            if self.umi_settings.umi_format_import_settings.umi_import_cancelled:
                self.canceled = True
                return
        else:
            LOG.separator()

        self.current_object_to_process = self.objects_to_process.pop()
        self.current_object_number += 1
        self.object_progress = round(self.current_object_number * 100 / self.number_of_object_to_process, 2)

        LOG.info(f'Processing object {self.current_object_number}/{self.number_of_object_to_process} - {self.object_progress}% : {self.current_object_to_process.name}')
        if not len(self.operators_to_process):
            self.fill_operator_to_process(each_only=True)

# function to append the operator in the File>Import menu
def menu_func_object(self, context):
    self.layout.separator()
    op = self.layout.operator(CommandBatcher.bl_idname, text="Command Batcher", icon='SHORTDISPLAY')
    op.importer_mode = False

classes = (CommandBatcher,)

def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)

    bpy.types.VIEW3D_MT_object.append(menu_func_object)


def unregister():
    bpy.types.VIEW3D_MT_object.remove(menu_func_object)

    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)

if __name__ == "__main__":
    register()