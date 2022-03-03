# -*- coding: utf-8 -*-

from odoo import api, models, fields, _



class AccountAdvancePayment(models.Model):
    _name = 'account.advanced.payment'
    _inherit = ['account.advanced.payment', 'object.pay.mixin']
    
    # intefaz para reporte de pago del asiento

    def is_customer_pay(self):
        self.ensure_one()
        return self.is_customer
    
    def is_supplier_pay(self):
        self.ensure_one()
        return self.is_supplier
    
    def get_partner(self):
        self.ensure_one()
        return self.partner_id
    
    def get_payment_number(self):
        self.ensure_one()
        return self.move_apply_id.name
    
    def get_payment_date(self):
        self.ensure_one()
        return self.date_apply
    
    def get_payment_currency(self):
        self.ensure_one()
        return self.amount_currency_apply
    
    def get_journal(self):
        self.ensure_one()
        return self.journal_id
    
    def get_invoices(self):
        self.ensure_one()
        return self.invoice_id
    
    def get_payment_reference():
        self.ensure_one()
        return self.name
    
    def get_communication(self):
        self.ensure_one()
        return self.ref

    def get_payment_amount(self):
        self.ensure_one()
        return self.amount_apply
    
    def pay_is_posted(self):
        self.ensure_one()
        return self.state == 'paid' and self.move_apply_id.state == 'posted'
    

