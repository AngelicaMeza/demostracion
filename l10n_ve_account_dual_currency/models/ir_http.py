from odoo import api, fields, models
from odoo.http import request


class Http(models.AbstractModel):
    _inherit = 'ir.http'

    def session_info(self):
        res = super().session_info()
        user = request.env.user
        if user.company_id.second_currency_id:
            res['second_currency'] = res['currencies'][user.company_id.second_currency_id.id]
        return res