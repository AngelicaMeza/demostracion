# -*- coding: utf-8 -*-
##############################################################################
#
#    autor: Tysamnca.
#
##############################################################################

from odoo import fields, models, api
from odoo.exceptions import RedirectWarning, UserError, ValidationError, AccessError
from odoo.tools import float_is_zero, float_compare, safe_eval, date_utils, email_split, email_escape_char, email_re
import json
import re

class account_payment(models.Model):
    _inherit = 'account.payment'

    check_payment_iva = fields.Boolean('Pago de Impuestos')




    


class AccountMove(models.Model):
    _inherit = "account.move"


    
   

    @api.depends('type', 'line_ids.amount_residual')
    def _compute_payments_widget_reconciled_info(self):
        for move in self:
            if move.state != 'posted' or not move.is_invoice(include_receipts=True):
                move.invoice_payments_widget = json.dumps(False)
                continue
            reconciled_vals = move._get_reconciled_info_JSON_values()
            for data in reconciled_vals:
                # rate = self._get_rate_from_invoice(fbl.invoice_id) if fbl.invoice_id.currency_id != fbl.invoice_id.company_currency_id else 1

                payment = self.env['account.payment'].search([('id','=',data['account_payment_id'])])
                for invoice in payment.invoice_ids:
                    rate = self._get_rate_from_invoice(invoice) if payment.currency_id != invoice.currency_id else 1

                    if payment.check_payment_iva and payment.currency_id != invoice.currency_id:
                        data['amount']= payment.amount / rate

            #     date.date = 
            if reconciled_vals:
                info = {
                    'title': ('Less Payment'),
                    'outstanding': False,
                    'content': reconciled_vals,
                }
                move.invoice_payments_widget = json.dumps(info, default=date_utils.json_default)
            else:
                move.invoice_payments_widget = json.dumps(False)



    def _get_rate_from_invoice(self, invoice_id):
        return invoice_id.company_currency_id._get_conversion_rate(invoice_id.currency_id, invoice_id.company_currency_id, invoice_id.company_id, invoice_id.date)






class AccountMoveLine(models.Model):
    _inherit = "account.move.line"



    def _reconcile_lines(self, debit_moves, credit_moves, field):
        """ This function loops on the 2 recordsets given as parameter as long as it
            can find a debit and a credit to reconcile together. It returns the recordset of the
            account move lines that were not reconciled during the process.
        """
        (debit_moves + credit_moves).read([field])
        to_create = []
        cash_basis = debit_moves and debit_moves[0].account_id.internal_type in ('receivable', 'payable') or False
        cash_basis_percentage_before_rec = {}
        dc_vals ={}
        while (debit_moves and credit_moves):
            debit_move = debit_moves[0]
            credit_move = credit_moves[0]
            company_currency = debit_move.company_id.currency_id
            # We need those temporary value otherwise the computation might be wrong below
            temp_amount_residual = min(debit_move.amount_residual, -credit_move.amount_residual)
            temp_amount_residual_currency = min(debit_move.amount_residual_currency, -credit_move.amount_residual_currency)
            dc_vals[(debit_move.id, credit_move.id)] = (debit_move, credit_move, temp_amount_residual_currency)
            amount_reconcile = min(debit_move[field], -credit_move[field])

            #Remove from recordset the one(s) that will be totally reconciled
            # For optimization purpose, the creation of the partial_reconcile are done at the end,
            # therefore during the process of reconciling several move lines, there are actually no recompute performed by the orm
            # and thus the amount_residual are not recomputed, hence we have to do it manually.
            if amount_reconcile == debit_move[field]:
                debit_moves -= debit_move
            else:
                debit_moves[0].amount_residual -= temp_amount_residual
                debit_moves[0].amount_residual_currency -= temp_amount_residual_currency

            if amount_reconcile == -credit_move[field]:
                credit_moves -= credit_move
            else:
                credit_moves[0].amount_residual += temp_amount_residual
                credit_moves[0].amount_residual_currency += temp_amount_residual_currency
            #Check for the currency and amount_currency we can set
            currency = False
            amount_reconcile_currency = 0
            if field == 'amount_residual_currency':
                currency = credit_move.currency_id.id
                amount_reconcile_currency = temp_amount_residual_currency
                amount_reconcile = temp_amount_residual
            elif bool(debit_move.currency_id) != bool(credit_move.currency_id):
                # If only one of debit_move or credit_move has a secondary currency, also record the converted amount
                # in that secondary currency in the partial reconciliation. That allows the exchange difference entry
                # to be created, in case it is needed. It also allows to compute the amount residual in foreign currency.
                currency = debit_move.currency_id or credit_move.currency_id
                currency_date = debit_move.currency_id and credit_move.date or debit_move.date
                
                for line in self:
                    for line2 in line.payment_id:
                        if line2.check_payment_iva == True:
                            for invoice in line2.invoice_ids:
                                amount_reconcile_currency = company_currency._convert(amount_reconcile, currency, debit_move.company_id, invoice.date)
                        else:
                            amount_reconcile_currency = company_currency._convert(amount_reconcile, currency, debit_move.company_id, currency_date)
                if amount_reconcile_currency == 0:
                    amount_reconcile_currency = company_currency._convert(amount_reconcile, currency, debit_move.company_id, currency_date)
 
                currency = currency.id

            if cash_basis:
                tmp_set = debit_move | credit_move
                cash_basis_percentage_before_rec.update(tmp_set._get_matched_percentage())

            # for line in self:
            #     for line2 in line.payment_id:
            #         if line2.check_payment_iva == True:
            #             for invoice in line2.invoice_ids:
            #                 amount_reconcile_currency = company_currency._convert(amount_reconcile, currency, debit_move.company_id, invoice.date)
            
            to_create.append({
                'debit_move_id': debit_move.id,
                'credit_move_id': credit_move.id,
                'amount': amount_reconcile,
                'amount_currency': amount_reconcile_currency,
                'currency_id': currency,
            })

        cash_basis_subjected = []
        part_rec = self.env['account.partial.reconcile']
        for partial_rec_dict in to_create:
            debit_move, credit_move, amount_residual_currency = dc_vals[partial_rec_dict['debit_move_id'], partial_rec_dict['credit_move_id']]
            # /!\ NOTE: Exchange rate differences shouldn't create cash basis entries
            # i. e: we don't really receive/give money in a customer/provider fashion
            # Since those are not subjected to cash basis computation we process them first
            if not amount_residual_currency and debit_move.currency_id and credit_move.currency_id:
                part_rec.create(partial_rec_dict)
            else:
                cash_basis_subjected.append(partial_rec_dict)

        for after_rec_dict in cash_basis_subjected:
            new_rec = part_rec.create(after_rec_dict)
            # if the pair belongs to move being reverted, do not create CABA entry
            if cash_basis and not (
                    new_rec.debit_move_id.move_id == new_rec.credit_move_id.move_id.reversed_entry_id
                    or
                    new_rec.credit_move_id.move_id == new_rec.debit_move_id.move_id.reversed_entry_id
            ):
                new_rec.create_tax_cash_basis_entry(cash_basis_percentage_before_rec)
        return debit_moves+credit_moves
