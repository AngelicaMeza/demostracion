# coding: utf-8
###########################################################################


from enum import Flag
import time
from typing import Tuple

from odoo.addons import decimal_precision as dp
from odoo import models, fields, api, exceptions, _


class AccountWhIvaLine(models.Model):
    _inherit = 'account.wh.iva.line'

    def load_taxes(self):
        awilt = self.env['account.wh.iva.line.tax']
        partner = self.env['res.partner']
        for rec in self:
            if rec.invoice_id:
                rate = rec.retention_id.type == 'out_invoice' and \
                    partner._find_accounting_partner(
                        rec.invoice_id.company_id.partner_id).wh_iva_rate or \
                    partner._find_accounting_partner(
                        rec.invoice_id.partner_id).wh_iva_rate
                rec.write({'wh_iva_rate': rate})

                #crear el id en las lineas
                self.write({'retention_id': rec.invoice_id.wh_iva_id.id})

                # Clean tax lines of the withholding voucher
                #awilt.search([('wh_vat_line_id', '=', rec.id)]).unlink()
                # Filter withholdable taxes

                for line_ids in rec.invoice_id.invoice_line_ids:
                    # Load again tax lines of the withholding voucher
                    ##########################################################################################################################################################3
                    if (line_ids.move_id.partner_id.people_type_company == 'pjnd' or line_ids.move_id.partner_id.people_type_individual == 'pnnr') and line_ids.move_id.currency_id != line_ids.move_id.company_id.currency_id and line_ids.move_id.x_studio_field_TJfMu:
                        monto_total = line_ids.price_total * line_ids.move_id.x_studio_field_l5IHS
                        monto_subtotal = line_ids.price_subtotal * line_ids.move_id.x_studio_field_l5IHS
                    else:
                        monto_total = rec.invoice_id.currency_id._convert(line_ids.price_total, rec.invoice_id.company_currency_id, rec.invoice_id.company_id, rec.invoice_id.date)
                        monto_subtotal = rec.invoice_id.currency_id._convert(line_ids.price_subtotal, rec.invoice_id.company_currency_id, rec.invoice_id.company_id, rec.invoice_id.date)
                    ##########################################################################################################################################################3
                    if len(line_ids.tax_ids) > 1:
                        taxxx = line_ids.tax_ids[0]
                    else:
                        taxxx = line_ids.tax_ids
                    for tax in taxxx:
                        taxd = tax.id
                    awilt.create({'wh_vat_line_id': rec.id,
                                  'id_tax': taxd,
                               #   'tax_id': tax.tax_id.id,
                                  'move_id': rec.invoice_id.id,
                                  'base': monto_subtotal,
                                  'amount': monto_total - monto_subtotal
                                  })

        return True