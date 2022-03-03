# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions, _


class AccountMove(models.Model):
    _inherit = "account.move"

    amount_residual_dollar = fields.Float(string="Dollar amount Due", compute="_compute_dollar_amount_due", store=True, readonly=False)

    @api.depends('amount_residual', 'amount_untaxed')
    def _compute_dollar_amount_due(self):
        for rec in self:
            if rec.currency_id == rec.company_id.currency_id:
                rec.amount_residual_dollar = rec.amount_residual / rec.x_studio_tasa_1
            elif rec.currency_id == rec.company_id.second_currency_id:
                rec.amount_residual_dollar = rec.amount_residual
