# -*- coding: utf-8 -*-

from odoo import api, fields, models, tools, _

class LandedCost(models.Model):
	_inherit = 'stock.landed.cost'
	purchase_import_id = fields.Many2one('purchase.import')