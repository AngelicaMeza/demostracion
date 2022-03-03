from odoo import api, fields, models


class AccountInvoiceReport(models.Model):
    _inherit = 'account.invoice.report'

    amount_untaxed_dollar = fields.Float('Total libre de impuestos $')

    @api.model
    def _select(self):
        select = super()._select()
        select = select + '\n, -line.amount_currency_dollar as amount_untaxed_dollar'
        return select


