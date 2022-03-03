# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class PurchaseImport(models.Model):
	_name = 'purchase.import'

	#Secuence for import file's name 
	name = fields.Char(string="Name", default=lambda self: _('New'))
	@api.model
	def create(self, vals):
		if vals.get('name', _('New')) == _('New') or vals.get('name') == False:
			vals['name'] = self.env['ir.sequence'].next_by_code('purchases_imports.purchase_import') or _('New')
		return super().create(vals)
	
	#Left Group
	exporter = fields.Many2one('res.partner', string="Exporter")
	declarant = fields.Many2one('res.partner', string="Declarant")
	state = fields.Selection([
		('draft', 'Draft'),
		('in_proces', 'In proces'),
		('close', 'Close')
		], string='State', select=True, readonly=True, default='draft')
	customs_office = fields.Many2one('customs.office', string='Customs Office', ondelete="restrict")
	consignee = fields.Many2one('res.company', string="Consignee")

	#Right Group
	import_form_external = fields.Char(string="Import form")
	import_form = fields.Char(string="Import form N.º")
	import_form_date = fields.Date(string="Import form date")
	merchandise_status = fields.Many2one('merchandise.status', string='Merchandise status', ondelete="restrict")

	#associated expenses page
	stock_landed_cost_ids = fields.One2many('stock.landed.cost', 'purchase_import_id', string="Costs in Destinations")

	#Plant reception page
	reception_timestamp = fields.Datetime(string="Date and Time")
	received_by = fields.Many2one('hr.employee', string="Received by")

	#Associated invoices page
	invoice_ids = fields.One2many('account.move', 'purchase_import_id', string="Associated invoices", domain=[('state', '=', 'posted')])

	#DUA page
	#Percent
	percent_ADV = fields.Float(string="ADV")
	percent_TSA = fields.Float(string="TSA")
	percent_TSS = fields.Float(string="TSS")
	percent_IVA = fields.Float(string="IVA")

	#DUA paid
	DUA_ADV = fields.Float(string="ADV")
	DUA_TSA = fields.Float(string="TSA")
	DUA_TSS = fields.Float(string="TSS")
	DUA_IVA = fields.Float(string="IVA")

	#Associated purchases page
	purchase_ids = fields.One2many('purchase.order', 'purchase_import_id', string="Associated Purchase Orders", domain=[('state', 'in', ('done', 'purchase'))])

	#Change of state to manual closed
	def close_state(self):
		self.state = 'close'

	#Change to automatic draft status
	def _compute_inproces_state_test(self):
		if self.state == 'draft' and (len(self.invoice_ids) > 0 or len(self.purchase_ids) > 0):
			self.state = 'in_proces'
		elif self.state == 'in_proces' and len(self.invoice_ids) == 0 and len(self.purchase_ids) == 0:
			self.state = 'draft'
