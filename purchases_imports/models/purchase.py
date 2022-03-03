from odoo import api, fields, models, _
from odoo.exceptions import AccessError, UserError, ValidationError

class PurchaseOrder(models.Model):
	_inherit = "purchase.order"


	purchase_import_id = fields.Many2one('purchase.import')
	importer_purchase= fields.Boolean(related='partner_id.importer')
	customs_agent_purchase = fields.Boolean(related='partner_id.customs_agent')
	tipo_related = fields.Selection(related='x_studio_tipo')


	#state change for import file 
	def button_cancel(self):
		super().button_cancel()
		self.purchase_import_id._compute_inproces_state_test()

	def button_confirm(self):
		res = super().button_confirm()
		self.purchase_import_id._compute_inproces_state_test()
		return res
