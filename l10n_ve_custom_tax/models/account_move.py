# Copyright 2019 Tecnativa - David Vidal
# Copyright 2020-2021 Tecnativa - Pedro M. Baeza
# Copyright 2021 Tecnativa - Víctor Martínez
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import _, api, exceptions, fields, models
from odoo.tools import config


class AccountInvoice(models.Model):
    _inherit = 'account.move'

    custom_tax_id = fields.Many2one('tax.custom', readonly=True, 
    states={'draft': [('readonly', False)]},
    string='Impuesto Aduanal'
    )

    amount_custom_tax = fields.Monetary(
        string="Impuesto Aduanal",
        compute="_compute_amount",
        currency_field="currency_id",
        readonly=True,
        compute_sudo=True,
    )
    amount_untaxed_before_custom_tax = fields.Monetary(
        string="Cantidad antes del impuesto",
        compute="_compute_amount",
        currency_field="currency_id",
        readonly=True,
        compute_sudo=True,
    )



    @api.onchange('custom_tax_id','line_ids','currency_id')
    def _onchange_custom_tax(self):

        self.line_ids -= self.line_ids.filtered("is_custom_tax")
        if self.custom_tax_id:
            self.ensure_one()
            in_draft_mode = self != self._origin
            model = "account.move.line"
            tax = self.custom_tax_id
            create_method = in_draft_mode and self.env[model].new or self.env[model].create
            # for tax in self.invoice_global_tax_ids.filtered("tax"):
            sign = -1 if self.type in {"in_invoice", "out_refund"} else 1
            disc_amount = ((tax.tax_amount*self.amount_untaxed_before_custom_tax) /(100))* sign if self.amount_untaxed_before_custom_tax > 0 else ((tax.tax_amount*self.amount_untaxed) /(100))* sign
            
            if self.currency_id != self.company_id.currency_id:
                amount_currency = disc_amount
                disc_amount = self.currency_id._convert(disc_amount,self.company_id.currency_id , self.company_id, self.date) 
            else:
                amount_currency = 0 
            main_tax = []
            for i in self.invoice_line_ids:
                if i.tax_ids.amount>0:
                    main_tax = i.tax_ids
                    break

                        # i
                    # the_tax = self.env['account.tax'].search([('name','=',jeje[0][0] if jeje[0][0]])
            create_method(
                {
                    "is_custom_tax": True,
                    # TODO: This field is not properly saved, probably due to ORM glitch
                    # "invoice_global_tax_id": tax.id,
                    "move_id": self.id,
                    "name": (tax.name),
                    "debit": disc_amount < 0.0 and -disc_amount or 0.0, 
                    "credit": disc_amount > 0.0 and disc_amount or 0.0,
                    "account_id": tax.account_id.id,
                    "analytic_account_id": tax.account_analytic_id.id,
                    "exclude_from_invoice_tab": True,
                    "amount_currency": amount_currency if disc_amount<0 else amount_currency*-1,
                    "tax_ids": main_tax,
                    # "always_set_currency_id": self.currency_id,
                    "currency_id": self.currency_id if self.currency_id != self.company_id.currency_id else False
                }
            )
        self._recompute_dynamic_lines(recompute_all_taxes=True)
    
    
    def _compute_amount(self):
        """Modify totals computation for including global discounts."""
        aja = super()._compute_amount()
        for record in self:
            record._compute_amount_custom_tax()
            self._recompute_dynamic_lines(recompute_all_taxes=True)
            # self._onchange_custom_tax()
        
        return aja


    def _compute_amount_custom_tax(self):
        """Perform totals computation of a move with global discounts."""
        if self.people_type_individual1 == 'pnnr' or self.people_type_company1 == 'pjnd':
            pass
        else:
            self.custom_tax_id = False
        if not self.custom_tax_id:
            self.amount_custom_tax = 0.0
            self.amount_untaxed_before_custom_tax = 0.0
            return
        round_curr = self.currency_id.round
        
        self.amount_custom_tax = ((self.custom_tax_id.tax_amount*self.amount_untaxed) /(100))
        self.amount_untaxed_before_custom_tax = self.amount_untaxed
        self.amount_untaxed = self.amount_untaxed + self.amount_custom_tax
        self.amount_total = self.amount_untaxed + self.amount_tax
        amount_total_company_signed = self.amount_total
        amount_untaxed_signed = self.amount_untaxed
        if (
            self.currency_id
            and self.company_id
            and self.currency_id != self.company_id.currency_id
        ):
            date = self.invoice_date or fields.Date.today()
            amount_total_company_signed = self.currency_id._convert(
                self.amount_total, self.company_id.currency_id, self.company_id, self.date
            )
            amount_untaxed_signed = self.currency_id._convert(
                self.amount_untaxed, self.company_id.currency_id, self.company_id, self.date
            )
        sign = self.type in ["in_refund", "out_refund"] and -1 or 1
        self.amount_total_company_signed = amount_total_company_signed * sign
        self.amount_total_signed = self.amount_total * sign
        self.amount_untaxed_signed = amount_untaxed_signed * sign

        for line in self.line_ids.filtered("is_custom_tax"):
            if self.currency_id != self.company_id.currency_id:
                if line.credit:
                    line.credit=self.currency_id._convert(self.amount_custom_tax, self.company_id.currency_id, self.company_id, self.date)
                    line.amount_currency = self.amount_custom_tax * sign
                if line.debit:
                    line.amount_currency = self.amount_custom_tax
                    line.debit=self.currency_id._convert(self.amount_custom_tax, self.company_id.currency_id, self.company_id, self.date)
            else:
                if line.credit:
                    line.credit=self.amount_custom_tax * sign
                if line.debit:
                    line.debit=self.amount_custom_tax * sign
        # self._recompute_dynamic_lines(recompute_all_taxes=True)

class AccountInvoiceLine(models.Model):
    _inherit = 'account.move.line'

    is_custom_tax= fields.Boolean(string='custom_tax')