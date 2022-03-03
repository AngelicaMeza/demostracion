# -*- coding: utf-8 -*-

from odoo import models, fields, api, tools

class ResCurrency(models.Model):
    _inherit = 'res.currency'

    rounding = fields.Float(digits=(12,10))
