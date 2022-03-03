# coding: utf-8
##############################################################################
import time

from odoo import api
from odoo import fields, models
from odoo import exceptions
from odoo.tools.translate import _

class IslrWhDocInvoices(models.Model):
    _inherit = "islr.wh.doc.invoices"

    @api.model
    def _get_wh(self, iwdl_id, concept_id):
        """ Return a dictionary containing all the values of the retention of an
        invoice line.
        @param concept_id: Withholding reason
        """
        # TODO: Change the signature of this method
        # This record already has the concept_id built-in
        #context = self._context or {}
        #ids = isinstance(self.ids, (int)) and [self.ids] or self.ids
        ixwl_obj = self.env['islr.xml.wh.line']
        iwdl_obj = self.env['islr.wh.doc.line']
        #iwdl_brw = iwdl_obj.browse(iwdl_id)
        residual_ut = 0.0
        subtract_write_ut = 0.0

        ut_date = iwdl_id.islr_wh_doc_id.date_uid
        ut_obj = self.env['l10n.ut']
        money2ut = ut_obj.compute
        ut2money = ut_obj.compute_ut_to_money

        vendor, buyer, wh_agent = self._get_partners(iwdl_id.invoice_id)
        self.wh_agent = wh_agent
        apply_income = not vendor.islr_exempt
        residence = self._get_residence(vendor, buyer)
        #TODO revisar donde se configura este parametro
        nature = self._get_nature(vendor)
        #nature = False

        concept_id = iwdl_id.concept_id.id
        # rate_base,rate_minimum,rate_wh_perc,rate_subtract,rate_code,rate_id,
        # rate_name
        # Add a Key in context to store date of ret fot U.T. value
        # determination
        # TODO: Future me, this context update need to be checked with the
        # other date in the withholding in order to take into account the
        # Retención de ingresos del cliente.
        #context.update({
        #    'wh_islr_date_ret':
        #    iwdl_brw.islr_wh_doc_id.date_uid or
        #    iwdl_brw.islr_wh_doc_id.date_ret or False
        #})
        base = 0
        wh_concept = 0.0

        # Using a clousure to make this call shorter
        f_xc = ut_obj.sxc(
            iwdl_id.invoice_id.currency_id.id,
            iwdl_id.invoice_id.company_id.currency_id.id,
            iwdl_id.invoice_id.date)
        #PROVEEDORES
        if iwdl_id.invoice_id.type in ('in_invoice', 'in_refund'):
            for line in iwdl_id.xml_ids:
                ######################################################################3
                if (line.account_invoice_id.partner_id.people_type_company == 'pjnd' or line.account_invoice_id.partner_id.people_type_individual == 'pnnr') and line.account_invoice_id.currency_id != line.account_invoice_id.company_id.currency_id and line.account_invoice_id.x_studio_field_TJfMu:
                    base += line.account_invoice_line_id.price_subtotal * line.account_invoice_id.x_studio_field_l5IHS
                else:
                    base += f_xc(line.account_invoice_line_id.price_subtotal)
                ######################################################################3

            # rate_base, rate_minimum, rate_wh_perc, rate_subtract, rate_code,
            # rate_id, rate_name, rate2 = self._get_rate(
            #    cr, uid, ail_brw.concept_id.id, residence, nature, base=base,
            #    inv_brw=ail_brw.move_id, context=context)
            rate_tuple = self._get_rate(concept_id, residence, nature, base=base,
                inv_brw=iwdl_id.invoice_id)

            if rate_tuple[7]:
                apply_income = True
                residual_ut = (
                    (rate_tuple[0] / 100.0) * (rate_tuple[2] / 100.0) *
                    rate_tuple[7]['cumulative_base_ut'])
                residual_ut -= rate_tuple[7]['cumulative_tax_ut']
                residual_ut -= rate_tuple[7]['subtrahend']
            else:
                apply_income = (apply_income and
                                base >= rate_tuple[0] * rate_tuple[1] / 100.0)
            wh = 0.0
            subtract = apply_income and rate_tuple[3] or 0.0
            subtract_write = 0.0
            sb_concept = subtract
            for line in iwdl_id.xml_ids:
                ##################################################################
                if (line.account_invoice_id.partner_id.people_type_company == 'pjnd' or line.account_invoice_id.partner_id.people_type_individual == 'pnnr') and line.account_invoice_id.currency_id != line.account_invoice_id.company_id.currency_id and line.account_invoice_id.x_studio_field_TJfMu:
                    base_line = line.account_invoice_line_id.price_subtotal * line.account_invoice_id.x_studio_field_l5IHS
                else:
                    base_line = f_xc(line.account_invoice_line_id.price_subtotal)
                ##################################################################
                base_line_ut = money2ut(base_line, ut_date)
                values = {}
                if apply_income and not rate_tuple[7]:
                    wh_calc = ((rate_tuple[0] / 100.0) *
                               (rate_tuple[2] / 100.0) * base_line)
                    if subtract >= wh_calc:
                        wh = 0.0
                        subtract -= wh_calc
                    else:
                        wh = wh_calc - subtract
                        subtract_write = subtract
                        subtract = 0.0
                    values = {
                        'wh': wh,
                        'raw_tax_ut': money2ut(wh, ut_date),
                        'sustract': subtract or subtract_write,
                    }
                elif apply_income and rate_tuple[7]:
                    tax_line_ut = (base_line_ut * (rate_tuple[0] / 100.0) *
                                   (rate_tuple[2] / 100.0))
                    if residual_ut >= tax_line_ut:
                        wh_ut = 0.0
                        residual_ut -= tax_line_ut
                    else:
                        wh_ut = tax_line_ut + residual_ut
                        subtract_write_ut = residual_ut
                        residual_ut = 0.0
                    wh = ut2money(wh_ut, ut_date)
                    values = {
                        'wh': wh,
                        'raw_tax_ut': wh_ut,
                        'sustract': ut2money(
                            residual_ut or subtract_write_ut,
                            ut_date),
                    }
                type_person = ''
                if nature == False and residence == True:
                    type_person = 'PJDO'
                elif nature == False and residence == False:
                    type_person = 'PJND'
                if nature == True and residence == True:
                    type_person = 'PNRE'
                if nature == True and residence == False:
                    type_person = 'PNNR'
                name_rates = self.env['islr.rates'].write({
                                                        'name': type_person
                                                         })
                values.update({
                    'base': base_line * (rate_tuple[0] / 100.0),
                    'raw_base_ut': base_line_ut,
                    'rate_id': rate_tuple[5],
                    'porcent_rete': rate_tuple[2],
                    'concept_code': rate_tuple[4],
                })
                #ixwl_obj.write(line.id, values)
                line.write(values)
                wh_concept += wh
        else:   #CLIENTES
            for line in iwdl_id.invoice_id.invoice_line_ids:
                if line.concept_id.id == concept_id:
                    base += f_xc(line.price_subtotal)

            rate_tuple = self._get_rate(concept_id, residence, nature, base=0.0,
                inv_brw=iwdl_id.invoice_id)

            if rate_tuple[7]:
                apply_income = True
            else:
                apply_income = (apply_income and
                                base >= rate_tuple[0] * rate_tuple[1] / 100.0)
            sb_concept = apply_income and rate_tuple[3] or 0.0
            if apply_income:
                wh_concept = ((rate_tuple[0] / 100.0) *
                              rate_tuple[2] * base / 100.0)
                wh_concept -= sb_concept
        values = {
            'amount': wh_concept,
            'raw_tax_ut': money2ut(wh_concept, ut_date),
            'subtract': sb_concept,
            'base_amount': base * (rate_tuple[0] / 100.0),
            'raw_base_ut': money2ut(base, ut_date),
            'retencion_islr': rate_tuple[2],
            # 'islr_rates_id': rate_tuple[5],
        }
        iwdl_id.write(values)
        return True

