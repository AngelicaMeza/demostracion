from odoo import api, fields, models


class Invoice(models.Model):
    _inherit = 'account.move'

    currency_dollar_id = fields.Many2one('res.currency', default=lambda self: self.env.ref('base.USD'))
    amount_untaxed_dollar = fields.Float(compute='_compute_amount_untaxed_dollar',
        string='Base Imponible $', store=True)
    
    @api.depends('date', 'currency_dollar_id', 'amount_untaxed')
    def _compute_amount_untaxed_dollar(self):
        for invoice in self:
            if invoice.date and invoice.currency_dollar_id:
                amount = invoice.currency_id._convert(invoice.amount_untaxed, invoice.currency_dollar_id, 
                    invoice.company_id, invoice.date)
                invoice.amount_untaxed_dollar = amount
            else:
                invoice.amount_untaxed_dollar = 0


class InvoiceLine(models.Model):
    _inherit = 'account.move.line'

    amount_currency_dollar = fields.Float(string='Subtotal $', compute='_compute_amount_currency_dollar', store=True)

    @api.depends('move_id', 'move_id.amount_untaxed_dollar', 'balance')
    def _compute_amount_currency_dollar(self):
        for line in self:
            company = line.move_id.company_id
            currency = company.currency_id
            dollar = line.move_id.currency_dollar_id
            date = line.date
            if currency and company and date:
                amount = currency._convert(line.balance, dollar, company, date)
            else:
                amount = 0
            line.amount_currency_dollar = amount

