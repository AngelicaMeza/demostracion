from odoo import api, fields, models, tools, _

class Partner(models.Model):
	
	_inherit = "res.partner"

	importer = fields.Boolean(string="Importer")
	customs_agent = fields.Boolean(string="Customs Agent")
	