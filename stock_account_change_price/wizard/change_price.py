from odoo import api, fields, models


class ChangePrice(models.TransientModel):
    _inherit = 'stock.change.standard.price'

    date = fields.Date('Fecha', default=fields.Date.context_today)

    def change_price(self):
        self = self.with_context(default_date_for_move=self[0].date)
        return super(ChangePrice, self).change_price()