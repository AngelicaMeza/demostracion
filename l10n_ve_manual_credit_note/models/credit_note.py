# -*- coding: utf-8 -*-

from odoo import models, fields, api


class DebitNote(models.Model):
    _inherit = 'account.move'

    credit_note_number = fields.Char('Numero de Factura Afectada')
    credit_note_date = fields.Date('Fecha de Factura Afectada')
    # invoice_affected_amount_bs = fields.Float('Monto de Factura Afectada Bs.')
    # invoice_affected_amount_usd = fields.Float('Monto de Factura Afectada $')
    # is_manual_debit_note = fields.Boolean(default=False)
    # is_manual_credit_note = fields.Boolean(default=False)
