from odoo import api, fields, models, _
from odoo.exceptions import RedirectWarning, UserError, ValidationError, AccessError
from odoo.tools import float_is_zero, float_compare, safe_eval, date_utils, email_split, email_escape_char, email_re
from odoo.tools.misc import formatLang, format_date, get_lang

from collections import defaultdict
from datetime import date, timedelta
from itertools import groupby
from itertools import zip_longest
from hashlib import sha256
from json import dumps

import json
import re

class AccountMove(models.Model):
    _inherit = "account.move"

    creation_rate = fields.Float(string="Tasa en ultima modificacion")

    @api.onchange('date')
    def _creation_rate_onchange(self):
        tasa = self.company_id.currency_id._get_rates(self.company_id, self.date).get(self.company_id.currency_id.id)
        if tasa:
            self.creation_rate = tasa
        else:
            raise ValidationError(_('No existen tasas para la fecha contable de la factura'))

    #############################################################################################################
    # Se extiende esta funcion para agregar en el onchange el campo por el cual ahora deben
    # cambiar las conversiones 
    #############################################################################################################

    @api.onchange('date', 'currency_id', 'x_studio_field_TJfMu')
    def _onchange_currency(self):
        if not self.currency_id:
            return
        if self.is_invoice(include_receipts=True):
            company_currency = self.company_id.currency_id
            has_foreign_currency = self.currency_id and self.currency_id != company_currency

            for line in self._get_lines_onchange_currency():
                new_currency = has_foreign_currency and self.currency_id
                line.currency_id = new_currency
                line._onchange_currency()
        else:
            self.line_ids._onchange_currency()

        self._recompute_dynamic_lines(recompute_tax_base_amount=True)


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    #############################################################################################################
    # Se extiende esta funcion para el calculo de los asientos contables con la tasa reflejada
    # en la factura
    #############################################################################################################
    @api.model
    def _get_fields_onchange_subtotal_model(self, price_subtotal, move_type, currency, company, date):
        ''' This method is used to recompute the values of 'amount_currency', 'debit', 'credit' due to a change made
        in some business fields (affecting the 'price_subtotal' field).

        :param price_subtotal:  The untaxed amount.
        :param move_type:       The type of the move.
        :param currency:        The line's currency.
        :param company:         The move's company.
        :param date:            The move's date.
        :return:                A dictionary containing 'debit', 'credit', 'amount_currency'.
        '''
        if move_type in self.move_id.get_outbound_types():
            sign = 1
        elif move_type in self.move_id.get_inbound_types():
            sign = -1
        else:
            sign = 1
        price_subtotal *= sign

        if currency and currency != company.currency_id:
            # Multi-currencies.
            ###################################################################################
            if self.move_id and (self.move_id.partner_id.people_type_company == 'pjnd' or self.move_id.partner_id.people_type_individual == 'pnnr') and self.move_id.x_studio_field_TJfMu:
                balance = price_subtotal * self.move_id.x_studio_field_l5IHS
            else:
                balance = currency._convert(price_subtotal, company.currency_id, company, date)
            ####################################################################################
            return {
                'amount_currency': price_subtotal,
                'debit': balance > 0.0 and balance or 0.0,
                'credit': balance < 0.0 and -balance or 0.0,
            }
        else:
            # Single-currency.
            return {
                'amount_currency': 0.0,
                'debit': price_subtotal > 0.0 and price_subtotal or 0.0,
                'credit': price_subtotal < 0.0 and -price_subtotal or 0.0,
            }