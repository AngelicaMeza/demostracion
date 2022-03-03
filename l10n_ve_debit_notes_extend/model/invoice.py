# coding: utf-8
###########################################################################


import time

from odoo import api,fields,models, exceptions
from odoo.fields import _
#from odoo.tools.translate import _

from odoo.tools import float_compare


class AccountDebitNote(models.TransientModel):
    _inherit = 'account.debit.note'


    def create_debit(self):
        the_lines = []
        debited = super().create_debit()
        if self.move_ids.type in ['out_refund','in_refund']:
            etso = self.env['account.move'].search([('id', '=',debited['res_id'])])
            lines = self.env['account.move.line'].search([('move_id', '=',debited['res_id'])])
            for pe in etso.invoice_line_ids:
                the_lines.append({
                        'move_id':etso.id,
                        'product_id':pe.product_id,
                        'price_unit': pe.price_unit*-1,
                        'name': pe.name,
                        'account_id': pe.account_id,
                        # 'locality': pe.locality,
                        'analytic_account_id': pe.analytic_account_id,
                        'analytic_tag_ids': pe.analytic_tag_ids,
                        'concept_id': pe.concept_id,
                        'quantity': pe.quantity,
                        'discount': pe.discount,
                        'tax_ids': pe.tax_ids,
                        'product_uom_id': pe.product_uom_id,
                        'debit':pe.debit
                        })
            etso.update({'invoice_line_ids':False})
            for esto in the_lines:
                self.env['account.move.line'].with_context(check_move_validity=False).create({
                        'price_unit': esto['price_unit'],
                        'name': esto['name'],
                        'account_id':esto['account_id'].id,
                        'concept_id': esto['concept_id'].id,
                        'move_id':etso.id   ,
                        'product_id':esto['product_id'].id,
                        # 'locality': esto['locality'],
                        'analytic_account_id': esto['analytic_account_id'].id,
                        'analytic_tag_ids': esto['analytic_tag_ids'],
                        'quantity': esto['quantity'],
                        'discount': esto['discount'],
                        'tax_ids': esto['tax_ids'].ids,
                        'product_uom_id': esto['product_uom_id'].id,
                        })
        return debited       
        
        
        
        
        
