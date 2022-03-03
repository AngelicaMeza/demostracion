# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class AccountMove(models.Model):
	_inherit = 'account.move'

	purchase_import_id = fields.Many2one('purchase.import')
	importer_invoice = fields.Boolean(related='partner_id.importer')
	customs_agent_invoice = fields.Boolean(related='partner_id.customs_agent')

	#state change for import file 
	def button_draft(self):
		super().button_draft()
		self.purchase_import_id._compute_inproces_state_test()

	def action_post(self):
		res = super().action_post()
		res.purchase_import_id._compute_inproces_state_test()
		return res


