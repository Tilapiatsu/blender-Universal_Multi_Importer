import bpy
import time, math, re, itertools
from ..logger import LOG, LoggerColors
from ..umi_const import get_umi_settings, DATATYPE_PREFIX, DATATYPE_LIST, init_current_item_index
from .command_batcher_const import COMMAND_BATCHER_INPUT_STRING, get_command_batcher_output_string


def which_keywords(sentence: str, input_string: list[str], delimitator: tuple[str] = ('<', '>')) -> list[str]:
    keywords = []

    keyword_pattern = re.compile(r'[{0}]([a-zA-Z0-9_]+)[{1}]'.format(delimitator[0], delimitator[1]), re.IGNORECASE)

    matches = keyword_pattern.finditer(sentence)

    while(sum(1 for _ in matches)):
        matches = keyword_pattern.finditer(sentence)
        m = next(matches)
        match = m.groups()[0]
        valid:bool = True
        if match not in input_string:
            print(f'Invalid Keyword : <{match}>')
            valid = False

        if valid:
            if match not in keywords:
                keywords.append(match)
            sentence = sentence[m.end():]

    return keywords


def replace_keywords(sentence: str, input_string: list[str], output_string: list, delimitator: tuple[str] = ('<', '>')) -> str:
    result_sentence = [sentence for _ in range(len(output_string))]

    for i,o in enumerate(output_string):
        keyword_pattern = re.compile(r'[{0}]([a-zA-Z0-9_]+)[{1}]'.format(delimitator[0], delimitator[1]), re.IGNORECASE)

        matches = keyword_pattern.finditer(result_sentence[i])

        while(sum(1 for _ in matches)):
            matches = keyword_pattern.finditer(result_sentence[i])
            m = next(matches)
            match = m.groups()[0]
            valid:bool = True
            if match not in input_string:
                print(f'Invalid Keyword : <{match}>')
                valid = False

            if valid:
                if match == 'OBJECTS' and o[input_string.index(match)] == '':
                    result_sentence[i] = '<PASS>'
                    continue
                output = o[input_string.index(match)]
            else:
                output = 'INVALID_KEYWORD'

            sub_sentence:str = result_sentence[i][m.start():]
            sub_sentence = sub_sentence.replace(f'{delimitator[0]}{match}{delimitator[1]}', output, 1)
            result_sentence[i] = result_sentence[i][:m.start()] + sub_sentence

    return result_sentence

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
    current_element_to_process = None
    _timer = None

    @property
    def element_to_process(self):
        return next(self.element_to_process_iter)

    @property
    def element_to_process_count(self):
        self.element_to_process_iter, bak = itertools.tee(self.element_to_process_iter, 2)
        count = sum(1 for _ in bak)
        return count

    def feed_data_from_object_selection(self):
        for o in bpy.context.selected_objects:
            for d in ['data', 'animation_data', 'material_slots', 'modifiers']:
                dd = getattr(o, d)
                print(repr(dd))

                if dd is None:
                    continue

                if d in ['material_slots', 'modifiers']:
                    for m in dd:
                        if d == 'material_slots':
                            ddd = getattr(m, 'material')
                        elif d == 'modifiers':
                            ddd = m
                        data = self.umi_settings.umi_imported_data.add()
                        data.data = repr(ddd)
                        data.data_type = repr(ddd).replace('bpy.data.', '').split('[')[0]
                        # data.name = ddd.name
                        data.name = getattr(ddd, 'name', '')
                else:
                    data = self.umi_settings.umi_imported_data.add()
                    data.data = repr(dd)
                    data.data_type = repr(dd).replace('bpy.data.', '').split('[')[0]
                    data.name = getattr(dd, 'name', '')

    def fill_operator_to_process(self, each_only=False):
        if self.execute_each_process:
            self.operators_to_process = [o for o in self.umi_settings.umi_each_operators if o.enabled]
            self.operators_to_process.reverse()

        if not each_only:
            if self.execute_pre_process:
                self.pre_operators_to_process = [o for o in self.umi_settings.umi_pre_operators if o.enabled]
                self.pre_operators_to_process.reverse()

            if self.execute_post_process:
                self.post_operators_to_process = [o for o in self.umi_settings.umi_post_operators if o.enabled]
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
            return wm.invoke_props_dialog(self, width=self.umi_settings.umi_window_width)

        return self.execute(context)

    def finish(self, context, canceled=False):
        for d in DATATYPE_LIST:
            self.umi_settings.umi_current_item_index[d['name']].index += self.processed_elements[d['name']] + 1

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

            if not self.pre_processing and not self.processing and self.current_element_to_process is None and self.element_to_process_count: # Process can start
                self.next_object()

            elif self.pre_processing:
                pass

            elif self.current_element_to_process is None and self.element_to_process_count > 0:
                self.processing = False

            elif self.current_element_to_process is None and self.element_to_process_count == 0 and not self.post_process_done and not self.post_processing:
                if len(self.post_operators_to_process) and self.execute_post_process:
                    LOG.info(f'Start Post-Processing commands', color=LoggerColors.DEFAULT_COLOR())
                    self.post_processing = True
                    self.each_process_done = True
                else:
                    self.each_process_done = True
                    self.post_process_done = True

            elif self.current_element_to_process is None and self.element_to_process_count == 0 and self.post_process_done:
                if not self.importer_mode:
                    LOG.complete_progress_importer(show_successes=False, duration=round(time.perf_counter() - self.start_time, 2))
                    self.counter = self.umi_settings.umi_global_import_settings.wait_before_hiding
                else:
                    self.finished = True
                self.end = True

            if self.finished:
                return self.finish(context)

            # Feed Pre-Process Operator
            if self.current_command is None and len(self.pre_operators_to_process):
                self.current_command = self.pre_operators_to_process.pop()

            # Pre-Process Done
            elif not self.pre_process_done and self.current_command is None and not len(self.pre_operators_to_process):
                if not self.importer_mode:
                    LOG.info(f'Start processing Each Element commands', color=LoggerColors.DEFAULT_COLOR())
                self.pre_process_done = True
                self.pre_processing = False

            # Feed Each-Process Command
            if self.pre_process_done and self.current_command is None and len(self.operators_to_process):
                self.current_command = self.operators_to_process.pop()
                return {'PASS_THROUGH'}

            # Each-Process Done
            elif not self.each_process_done and self.pre_process_done and self.current_command is None and not len(self.operators_to_process):
                self.current_element_to_process = None

            # Feed Post-Process Command
            if self.each_process_done and self.current_command is None and len(self.post_operators_to_process):
                self.current_command = self.post_operators_to_process.pop()

            # Post-Process Done
            elif self.each_process_done and self.current_command is None and not len(self.post_operators_to_process):
                self.post_process_done = True
                return {'PASS_THROUGH'}

            if self.finished:
                self.end = True
                return {'PASS_THROUGH'}

            elif self.current_element_to_process is None and not self.each_process_done and not self.pre_processing:
                return {'PASS_THROUGH'}

            else:
                command = self.current_command.operator
                try: # Executing command
                    # if the current command is valid for the current data type
                    if not getattr(self.current_command, f'{DATATYPE_PREFIX}_{self.current_element_to_process[0]}'):
                        self.current_command = None
                        LOG.info(f'Skipping : command does NOT applied to this data type : {self.current_element_to_process[0]}', color=LoggerColors.COMMAND_WARNING_COLOR())
                        return {'PASS_THROUGH'}

                    self.progress += 100 / self.number_of_operations_to_perform

                    ob = None if self.current_element_to_process[0] != 'objects' else self.current_element_to_process[1]

                    # keywords = which_keywords(command, COMMAND_BATCHER_INPUT_STRING)

                    command_output_strings = get_command_batcher_output_string(
                                                                                self.global_processed_elements,
                                                                                self.processed_elements[self.current_element_to_process[0]] + self.umi_settings.umi_current_item_index[self.current_element_to_process[0]].index,
                                                                                self.current_element_name_to_process,
                                                                                self.current_element_to_process[2],
                                                                                ob)

                    # Replace Keyword with Proper Value
                    commands = replace_keywords(    command,
                                                    COMMAND_BATCHER_INPUT_STRING,
                                                    command_output_strings
                                                )

                    self.current_operation_number += 1
                    for c in commands:
                        if c == '<PASS>':
                            continue
                        LOG.info(f'Executing command {self.current_operation_number}/{self.number_of_operations_to_perform} - {round(self.progress,2)}% : "{c}"', color=LoggerColors.COMMAND_COLOR())
                        override = {}
                        if self.pre_process_done and not self.each_process_done:
                            if self.current_element_to_process[0] == 'objects':
                                override["selected_objects"] = [bpy.data.objects[self.current_element_to_process[1].name]]

                        with bpy.context.temp_override(**override):
                            exec(c, {'bpy':bpy})

                        LOG.store_success('Command executed successfully')

                    if not self.current_element_proccessed[self.current_element_to_process[0]]:
                        self.current_element_proccessed[self.current_element_to_process[0]] = True

                    self.process_succeeded.append(True)

                except Exception as e:
                    message = f'{self.current_element_to_process[0]} : Command "{command}" is not valid - {e}'
                    LOG.error(message)
                    LOG.store_failure(message)
                    self.process_succeeded.append(False)

                if self.umi_settings.umi_global_import_settings.force_refresh_viewport_after_each_command:
                    bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)
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
            init_current_item_index(self.umi_settings)
            self.feed_data_from_object_selection()


        self.objects_to_process = [o for o in bpy.context.selected_objects]
        self.data_to_process =  [eval(d.data) for d in self.umi_settings.umi_imported_data]
        element_list = (list(zip(['objects' for _ in self.objects_to_process], self.objects_to_process, [f'bpy.data.objects["{o.name}"]' for o in self.objects_to_process], [o.name for o in self.objects_to_process])) +
                        list(zip([d.data_type for d in self.umi_settings.umi_imported_data], self.data_to_process, [d.data for d in self.umi_settings.umi_imported_data], [d.name for d in self.umi_settings.umi_imported_data])))

        self.element_to_process_iter = iter(element_list)

        if self.execute_each_process and not (self.element_to_process_count + len(self.data_to_process)):
            self.report({'ERROR_INVALID_INPUT'}, 'UMI : You need to select at least one object.')
            return {'CANCELLED'}

        if not self.importer_mode and not len(self.umi_settings.umi_each_operators):
            self.report({'ERROR_INVALID_INPUT'}, 'UMI : You need to add at least one command.')
            return {'CANCELLED'}

        self.progress = 0
        self.number_of_operations_to_perform = 0
        self.number_of_object_to_process = len(self.objects_to_process)
        self.number_of_data_to_process = len(self.data_to_process)
        self.number_of_element_to_process = self.number_of_object_to_process + self.number_of_data_to_process
        self.current_operation_number = 0
        self.current_element_number = 0
        self.processed_elements = {t['name']:0 for t in DATATYPE_LIST}
        self.global_processed_elements = 0
        self.operators_to_process = []
        self.pre_operators_to_process = []
        self.post_operators_to_process = []
        self.pre_process_done = False
        self.each_process_done = False
        self.post_process_done = False
        self.pre_processing = False
        self.post_processing = False
        self.current_element_proccessed = {t['name']:False for t in DATATYPE_LIST}

        self.fill_operator_to_process()

        number_of_operations = len(self.operators_to_process)
        number_of_elements = len(self.objects_to_process) + len(self.data_to_process)

        self.number_of_operations_to_perform = number_of_operations * number_of_elements + len(self.pre_operators_to_process) + len(self.post_operators_to_process)

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
        self.processed_elements = {t['name']:0 for t in DATATYPE_LIST}
        self.current_element_proccessed = {t['name']:False for t in DATATYPE_LIST}
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
        self._timer = wm.event_timer_add(0.001, window=context.window)
        wm.modal_handler_add(self)

    def next_object(self):
        if self.importer_mode:
            if self.umi_settings.umi_format_import_settings.umi_import_cancelled:
                self.canceled = True
                return
        else:
            LOG.separator()

        # Feed new element to process
        self.current_element_to_process = self.element_to_process

        # Remove data from umi_imported_data
        for i,d in enumerate(self.umi_settings.umi_imported_data):
            if d.data == self.current_element_to_process[2]:
                self.umi_settings.umi_imported_data.remove(i)
                break

        # increment processed element
        if self.current_element_proccessed[self.current_element_to_process[0]]:
            self.processed_elements[self.current_element_to_process[0]] += 1

        self.global_processed_elements += 1
        self.current_element_name_to_process = self.current_element_to_process[3]
        self.current_element_number += 1
        self.element_progress = round(self.current_element_number * 100 / self.number_of_element_to_process, 2)
        self.current_element_proccessed[self.current_element_to_process[0]] = False

        LOG.info(f'Processing item {self.current_element_number}/{self.number_of_element_to_process} - {self.element_progress}% : {self.current_element_to_process[1].name}')
        if not len(self.operators_to_process):
            self.fill_operator_to_process(each_only=True)

# function to append the operator in the File>Import menu
def menu_func_object(self, context):
    self.layout.separator()
    op = self.layout.operator(CommandBatcher.bl_idname, text="Command Batcher", icon='SHORTDISPLAY')
    op.importer_mode = False
    op.execute_pre_process = True
    op.execute_each_process = True
    op.execute_post_process = True

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