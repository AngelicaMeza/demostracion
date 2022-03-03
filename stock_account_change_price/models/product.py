from odoo import models, fields, api


class ProductProduct(models.Model):
    _inherit = 'product.product'

    def _change_standard_price(self, new_price, counterpart_account_id=False):
        return super(ProductProduct, self)._change_standard_price(new_price, counterpart_account_id)