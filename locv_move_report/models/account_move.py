# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class AccountMove(models.Model):
    _inherit = 'account.move'

    iva_doc_line = fields.One2many('account.wh.iva.line', 'move_id')
    # display report action in ui
    display_button_payment_report = fields.Boolean(compute='_compute_display_button_payment_report')

    def get_object_pay(self):
        self.ensure_one()

        if self.advance_apply_ids:
            return self.advance_apply_ids[0]
        elif self.iva_doc_line:
            return self.iva_doc_line.retention_id
        else:
            return False
    

    def _compute_display_button_payment_report(self):
        for move in self:
            move.display_button_payment_report = move._display_button_report()
    
    def _display_button_report(self):
        self.ensure_one()
        object_pay = self.get_object_pay()
        if object_pay and object_pay.is_customer_pay() and object_pay.pay_is_posted():
            return True
        return False
    

    def action_report_payment(self):
        self.ensure_one()
        report = self.env.ref('locv_account_advance_payment.advance_payment_invoice_report').read()[0]
        return report