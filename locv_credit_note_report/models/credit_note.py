# -*- coding: utf-8 -*-

from odoo import models, fields, api


class CreditNote(models.Model):
    _name = 'account.move'
    _inherit = ['account.move', 'object.pay.mixin']

    # intefaz para reporte de pago del asiento

    def is_customer_pay(self):
        self.ensure_one()
        return self.type == 'out_refund'
    
    def get_payment_number(self):
        self.ensure_one()
        return self.name
    
    def get_payment_date(self):
        self.ensure_one()
        return self.date    
    
    def get_invoices(self):
        self.ensure_one()
        return self.reversed_entry_id
    
    def get_communication(self):
        self.ensure_one()
        return self.ref

    def get_payment_amount(self):
        self.ensure_one()
        return self.amount_total
    
    def get_partner(self):
        self.ensure_one()
        return self.partner_id
    
    def get_payment_currency(self):
        self.ensure_one()
        return self.currency_id
    
    def get_journal(self):
        self.ensure_one()
        return self.journal_id
    
    def pay_is_posted(self):
        self.ensure_one()
        return self.invoice_payment_state == 'paid' and self.reversed_entry_id.state == 'posted'
