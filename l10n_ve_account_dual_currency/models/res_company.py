from odoo import api, fields, models
from odoo.exceptions import UserError

class ResCompany(models.Model):
    _inherit = 'res.company'

    @api.model
    def _get_default_second_currency(self):
        currency = self.env.ref('base.USD', raise_if_not_found=False)
        if currency is None:
            company_currency = self.env.company.currency_id
            currency = self.env['res.currency'].search([('id', '!=', company_currency.id)], limit=1)
        return currency


    second_currency_id = fields.Many2one('res.currency', string='Moneda Secundaria', 
        default=_get_default_second_currency)
