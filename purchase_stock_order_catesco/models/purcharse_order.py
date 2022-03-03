# -*- coding: utf-8 -*-
from odoo import models, fields, api



class PurchaseOrder(models.Model):

    _inherit = 'purchase.order'

    
    selected_user = fields.Many2one('res.users', 'Requisitor Responsable')
    receive_id = fields.Boolean('Mercancia Recibida en Compras', default=False)







