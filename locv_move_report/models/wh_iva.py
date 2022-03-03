# -*- coding: utf-8 -*-

from odoo import api, fields, models, _

class WhIva(models.Model):
    _name = 'account.wh.iva'
    _inherit = ['account.wh.iva', 'object.pay.mixin']

    # intefaz para reporte de pago del asiento

    def is_customer_pay(self):
        self.ensure_one()
        return self.type == 'out_invoice'
    
    def is_supplier_pay(self):
        self.ensure_one()
        return self.type == 'in_invoice'
    
    def get_partner(self):
        self.ensure_one()
        return self.partner_id
    
    def get_payment_number(self):
        self.ensure_one()
        return self.wh_lines[0].move_id.name
    
    def get_payment_date(self):
        self.ensure_one()
        return self.date_ret
    
    def get_payment_currency(self):
        self.ensure_one()
        return self.currency_id
    
    def get_journal(self):
        self.ensure_one()
        return self.journal_id
    
    def get_invoices(self):
        self.ensure_one()
        return self.mapped('wh_lines.invoice_id')
    
    def get_payment_reference():
        self.ensure_one()
        return self.wh_lines[0].move_id.ref
    
    def get_communication(self):
        self.ensure_one()
        return self.name

    def get_payment_amount(self):
        self.ensure_one()
        return self.total_tax_ret
    
    def pay_is_posted(self):
        self.ensure_one()
        return self.state == 'done' and self.wh_lines[0].move_id.state == 'posted'
    