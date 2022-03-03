# -*- coding: utf-8 -*-

from odoo import models, fields, api


class AccountMove(models.Model):
    _inherit = 'account.move'

    def get_object_pay(self):
        self.ensure_one()
        # El reporte de pago es llamado desde la nota de credito, la cual pertenece es el 
        # mismo modelo account.move, ademas que contiene todos los datos especificos del pago.
        # Por lo tanto el metodo devuelve a su misma instancia como objeto de pago.
        if self.type == 'out_refund':
            return self
        else:
            return super().get_object_pay()
