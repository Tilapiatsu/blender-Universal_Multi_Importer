import bpy


class TILA_UL_umi_operator_list(bpy.types.UIList):
	bl_idname = "UMI_UL_operator_list"

	def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
		scn = context.scene

		grid = layout.grid_flow(columns=2, align=True, even_columns=True)
		row = grid.row()
		row.alignment = 'LEFT'
		row.label(text=f'{item.operator}')

		row = grid.row(align=True)
		row.alignment = 'RIGHT'

		row.operator('scene.umi_edit_operator', text='', icon='GREASEPENCIL').id = index
		row.operator('scene.umi_duplicate_operator', text='', icon='PASTEDOWN').id = index
		row.separator()
		row.operator('scene.umi_remove_operator', text='', icon='PANEL_CLOSE').id = index

class TILA_UL_umi_preset_list(bpy.types.UIList):
	bl_idname = "UMI_UL_preset_list"

	def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
		scn = context.scene

		grid = layout.grid_flow(columns=2, align=True, even_columns=True)
		row = grid.row()
		row.alignment = 'LEFT'
		row.label(text=f'{item.name}')

		row = grid.row(align=True)
		row.alignment = 'RIGHT'

		row.operator('scene.umi_edit_preset', text='', icon='GREASEPENCIL').id = index
		row.operator('scene.umi_duplicate_preset', text='', icon='PASTEDOWN').id = index
		row.separator()
		row.operator('scene.umi_load_preset_operator', text='', icon='TRIA_UP').filepath = item.path
		row.operator('scene.umi_save_preset_operator', text='', icon='PRESET_NEW').filepath = item.path
		row.separator()
		row.operator('scene.umi_remove_preset', text='', icon='PANEL_CLOSE').id = index
