# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class ObjectPayMixin(models.AbstractModel):
    _name = 'object.pay.mixin'


    def is_customer_pay(self):
        return False
    
    def is_supplier_pay(self):
        return False
    
    def get_partner(self):
        return False
    
    def get_payment_number(self):
        return False
    
    def get_payment_date(self):
        return False
    
    def get_payment_currency(self):
        return False
    
    def get_journal(self):
        return False

    def get_invoices(self):
        return False
    
    def get_payment_reference():
        return False
    
    def get_communication(self):
        return False

    def get_payment_amount(self):
        return False
    
    def pay_is_posted(self):
        return False