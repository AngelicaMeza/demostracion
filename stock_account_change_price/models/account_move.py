from odoo import models, fields, api


class AccountMove(models.Model):
    _inherit = 'account.move'

    @api.model_create_multi
    def create(self, vals_list):
        moves  = super().create(vals_list)
        date = self._context.get('default_date_for_move')
        if date:
            moves.write({'date': date})
        return moves