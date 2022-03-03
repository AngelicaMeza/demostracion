# Copyright 2019 Tecnativa - David Vidal
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import fields, models




class TaxCustom(models.Model):
    _name = "tax.custom"
    _description = "Custom Tax"

    # sequence = fields.Integer(help="Gives the order to apply discounts")
    name = fields.Char(string="Nombre Impuesto", required=True)
    tax_amount = fields.Float(digits="Impuesto", required=True, default=0.0)
   
    company_id = fields.Many2one(
        comodel_name="res.company",
        string="Company",
        default=lambda self: self.env.company,
    )

    account_id = fields.Many2one(
        comodel_name="account.account",
        string="Cuenta",
        # domain="[('user_type_id.type', 'not in', ['receivable', 'payable'])]",
    )
    account_analytic_id = fields.Many2one(
        comodel_name="account.analytic.account", string="Cuenta Anlitica",
    )

    def name_get(self):
        result = []
        for one in self:
            result.append((one.id, "{} ({:.2f}%)".format(one.name, one.tax_amount)))
        return result

   