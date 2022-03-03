from odoo import api, fields, models
from odoo.models import NewId


class AccountMove(models.Model):
    _inherit = 'account.move'


    second_currency_id = fields.Many2one('res.currency', related='company_id.second_currency_id', 
        store=True, ondelete='restrict')


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'


    second_currency_id = fields.Many2one('res.currency', related='move_id.second_currency_id', 
        store=True)
    second_currency_debit = fields.Monetary(currency_field='second_currency_id', default=0.0,
        compute='_compute_second_currency_amount', string='Debe $', store=True)
    second_currency_credit = fields.Monetary(currency_field='second_currency_id', default=0.0,
        compute='_compute_second_currency_amount', string='Haber $', store=True)

    @api.depends('amount_currency', 'debit', 'credit', 'second_currency_id', 'company_id', 'company_currency_id', 'currency_id')
    def _compute_second_currency_amount(self):
        currency_usd = self.env.ref('base.USD', raise_if_not_found=False)
        for line in self:
            if isinstance(line.id, NewId):
                line.second_currency_debit = line.second_currency_credit = 0.0
                continue

            if line.currency_id and line.currency_id == currency_usd:
                line.set_amount_debit_and_credit_amount_currency()
            else:
                amount_currency = line._get_amount_currency(line.balance)
                if amount_currency > 0.0:
                    line.second_currency_debit, line.second_currency_credit = (amount_currency, 0.0)
                else:
                    line.second_currency_debit, line.second_currency_credit = (0.0, abs(amount_currency))

    def _get_amount_currency(self, amount):
        self.ensure_one()
        currency = self.company_currency_id
        date = self.date
        company = self.company_id
        second_currency = self.second_currency_id
        return currency._convert(amount, second_currency, company, date)
    
    def set_amount_debit_and_credit_amount_currency(self):
        if self.amount_currency > 0.0:
            self.second_currency_debit, self.second_currency_credit = (self.amount_currency, 0.0)
        else:
            self.second_currency_debit, self.second_currency_credit = (0.0, abs(self.amount_currency))
        


