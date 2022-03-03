# -*- coding: utf-8 -*-

from odoo import models, fields, api 

class PickingTypeInherit(models.Model):
    _inherit = "stock.picking.type"
    tipo_operacion_especial = fields.Boolean('Tipo de operación especial', help="Selecione si el tipo de operacion es especial")
    
