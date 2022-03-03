# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import UserError
from odoo.tools.float_utils import float_round

class ReturnPickinge(models.TransientModel):
    _inherit = 'stock.return.picking'



    reason_line = fields.Text('Motivo de Devolucion' ,required=True)

    def _create_returns(self):
        res = super(ReturnPickinge, self)._create_returns()
        stock = self.env['stock.picking'].search([('id','=',res[0])])
        stock.reason_return = self.reason_line
        return res

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    reason_return = fields.Text('Motivo de Devolucion', readonly=True)