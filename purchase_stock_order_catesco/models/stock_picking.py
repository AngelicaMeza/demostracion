# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.tools.translate import _




class StockPicking(models.Model):
    _inherit = 'stock.picking'

    
    selected_user_purchased = fields.Many2one('res.users', related='move_lines.purchase_line_id.order_id.selected_user',
        string="Requisitor Responsable", readonly=True)
    selected_receive_id = fields.Boolean(related='move_lines.purchase_line_id.order_id.receive_id',
        string="Recibido en Compra", readonly=True)


    es_operacion_especial = fields.Boolean(related='picking_type_id.tipo_operacion_especial',
        string="Es una operacion especial", readonly=True)

    deliver_to = fields.Many2one('hr.employee', 'Entregar a:')
    deliver_by = fields.Many2one('res.users', 'Entregado por:')
    deliver_to_code = fields.Char(related='deliver_to.employee_code',
        string="Código", readonly=True)
    # receive_id_purchase = fields.Boolean(related='purchase_id.receive_id',
    #                                      string='Mercancia Recibida en Compras', readonly=True, store=True)




class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    employee_code = fields.Char(
        'Código', size=64,
        # required=True,
        # readonly=False,
        # default=None,
        )
    _sql_constraints = [
            ('hr_employee_code_unique', 'UNIQUE (employee_code)', 'El Código de empleado debe ser unico'),
        ]

    def function():
        print('aja')