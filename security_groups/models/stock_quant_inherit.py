from odoo import api, fields, models, _


class StockQuantInherit(models.Model):

	_inherit = 'stock.quant'
	value = fields.Monetary('Value', compute='_compute_value', groups='stock.group_stock_manager,security_groups.group_menuitem_stock_report_2,security_groups.group_menuitem_stock_report_3')
	inventory_quantity = fields.Float(
		'Inventoried Quantity', compute='_compute_inventory_quantity',
		inverse='_set_inventory_quantity', groups='stock.group_stock_manager,security_groups.group_menuitem_stock_report_2,security_groups.group_menuitem_stock_report_3')
	currency_id = fields.Many2one('res.currency', compute='_compute_value', groups='stock.group_stock_manager,security_groups.group_menuitem_stock_report_2,security_groups.group_menuitem_stock_report_3')

	@api.model
	def action_view_quants(self):
		self = self.with_context(search_default_internal_loc=1)
		if self.user_has_groups('stock.group_production_lot,stock.group_stock_multi_locations'):
			# fixme: erase the following condition when it'll be possible to create a new record
			# from a empty grouped editable list without go through the form view.
			if self.search_count([
				('company_id', '=', self.env.company.id),
				('location_id.usage', 'in', ['internal', 'transit'])
			]):
				self = self.with_context(
					search_default_productgroup=1,
					search_default_locationgroup=1
				)
		if not self.user_has_groups('stock.group_stock_multi_locations'):
			company_user = self.env.company
			warehouse = self.env['stock.warehouse'].search([('company_id', '=', company_user.id)], limit=1)
			if warehouse:
				self = self.with_context(default_location_id=warehouse.lot_stock_id.id)

		# If user have rights to write on quant, we set quants in inventory mode.
		if self.user_has_groups('stock.group_stock_manager,security_groups.group_menuitem_stock_report_2,security_groups.group_menuitem_stock_report_3'):
			self = self.with_context(inventory_mode=True)
		return self._get_quants_custom_action(extend=True)


	@api.model
	def _is_custom_inventory_mode(self):
		return self.env.context.get('inventory_mode') is True and (self.user_has_groups('stock.group_stock_manager,security_groups.group_menuitem_stock_report_2,security_groups.group_menuitem_stock_report_3'))


	@api.model
	def _get_quants_custom_action(self, domain=None, extend=False):
		""" Returns an action to open quant view.
		Depending of the context (user have right to be inventory mode or not),
		the list view will be editable or readonly.

		:param domain: List for the domain, empty by default.
		:param extend: If True, enables form, graph and pivot views. False by default.
		"""
		self._quant_tasks()
		ctx = dict(self.env.context or {})
		ctx.pop('group_by', None)
		action = {
			'name': _('Update Quantity'),
			'view_type': 'tree',
			'view_mode': 'list',
			'res_model': 'stock.quant',
			'type': 'ir.actions.act_window',
			'context': ctx,
			'domain': domain or [],
			'help': """
				<p class="o_view_nocontent_empty_folder">No Stock On Hand</p>
				<p>This analysis gives you an overview of the current stock
				level of your products.</p>
				"""
		}

		target_action = self.env.ref('stock.dashboard_open_quants', False)
		if target_action:
			action['id'] = target_action.id

		if self._is_custom_inventory_mode():
			action['view_id'] = self.env.ref('stock.view_stock_quant_tree_editable').id
			# fixme: erase the following condition when it'll be possible to create a new record
			# from a empty grouped editable list without go through the form view.
			if not self.search_count([
				('company_id', '=', self.env.company.id),
				('location_id.usage', 'in', ['internal', 'transit'])
			]):
				action['context'].update({
					'search_default_productgroup': 0,
					'search_default_locationgroup': 0
				})
		else:
			action['view_id'] = self.env.ref('stock.view_stock_quant_tree').id
			# Enables form view in readonly list
			action.update({
				'view_mode': 'tree,form',
				'views': [
					(action['view_id'], 'list'),
					(self.env.ref('stock.view_stock_quant_form').id, 'form'),
				],
			})
		if extend:
			action.update({
				'view_mode': 'tree,form,pivot,graph',
				'views': [
					(action['view_id'], 'list'),
					(self.env.ref('stock.view_stock_quant_form').id, 'form'),
					(self.env.ref('stock.view_stock_quant_pivot').id, 'pivot'),
					(self.env.ref('stock.stock_quant_view_graph').id, 'graph'),
				],
			})
		return action
