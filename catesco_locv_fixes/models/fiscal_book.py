import time
from odoo import fields, models, api, exceptions, _
from odoo.exceptions import UserError

from datetime import timedelta, datetime, date
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT

class FiscalBook(models.Model):
    _inherit = 'fiscal.book'

    def update_book_lines_taxes_fields(self):
        """ Update taxes data for every line in the fiscal book given,
        extrating de data from the fiscal book taxes associated.
        @param fb_id: fiscal book line id.
        """
        tax_amount = 0
        fbl_obj = self.env['fiscal.book.line']
        field_names = ['vat_reduced_base', 'vat_reduced_tax',
                       'vat_general_base', 'vat_general_tax',
                       'vat_additional_base', 'vat_additional_tax']
        tax_type = {'reduced': 'reducido', 'general': 'general',
                    'additional': 'adicional'}
        for fbl_brw in self.fbl_ids:
            # if fbl_brw.doc_type == 'N/C' or fbl_brw.doc_type == 'N/D':
            #     sign = -1
            # else:
            sign = 1
            data = {}.fromkeys(field_names, 0.0)
            busq = ' '
            local_period = self.get_time_period(self.time_period)
 
            if fbl_brw.iwdl_id.invoice_id:
              
               for line in fbl_brw.iwdl_id.invoice_id.invoice_line_ids:
                   for tax in line.tax_ids:
                       busq = tax.appl_type

                   for field_name in field_names:
                        field_tax, field_amount = field_name[4:].split('_')
                        ####################################################################################
                        if (fbl_brw.iwdl_id.invoice_id.partner_id.people_type_company == 'pjnd' or fbl_brw.iwdl_id.invoice_id.partner_id.people_type_individual == 'pnnr') and fbl_brw.iwdl_id.invoice_id.currency_id != fbl_brw.iwdl_id.invoice_id.company_id.currency_id and fbl_brw.iwdl_id.invoice_id.x_studio_field_TJfMu:
                            base = line.price_subtotal * fbl_brw.iwdl_id.invoice_id.x_studio_field_l5IHS
                            tax_amount = (line.price_total - line.price_subtotal) * fbl_brw.iwdl_id.invoice_id.x_studio_field_l5IHS
                        else:
                            base = fbl_brw.iwdl_id.invoice_id.currency_id._convert(line.price_subtotal, fbl_brw.iwdl_id.invoice_id.company_currency_id, fbl_brw.iwdl_id.invoice_id.company_id, fbl_brw.iwdl_id.invoice_id.date)
                            tax_amount = fbl_brw.iwdl_id.invoice_id.currency_id._convert(line.price_total - line.price_subtotal, fbl_brw.iwdl_id.invoice_id.company_currency_id, fbl_brw.iwdl_id.invoice_id.company_id, fbl_brw.iwdl_id.invoice_id.date)
                        ####################################################################################
                        if busq:
                            if busq == tax_type[field_tax]:
                                    data[field_name] += field_amount == 'base' and base * sign \
                                                        or tax_amount * sign
               if fbl_brw.iwdl_id.invoice_id.state != 'cancel' and local_period.get('dt_from') <= fbl_brw.iwdl_id.invoice_id.date <= local_period.get('dt_to'):
                   fbl_brw.write(data)

            elif fbl_brw.invoice_id:
                
                for line in fbl_brw.invoice_id.invoice_line_ids:
                    for tax in line.tax_ids:
                        busq = tax.appl_type
                    for field_name in field_names:
                        field_tax, field_amount = field_name[4:].split('_')
                        ####################################################################################
                        if (fbl_brw.invoice_id.partner_id.people_type_company == 'pjnd' or fbl_brw.invoice_id.partner_id.people_type_individual == 'pnnr') and fbl_brw.invoice_id.currency_id != fbl_brw.invoice_id.company_id.currency_id and fbl_brw.invoice_id.x_studio_field_TJfMu:
                            base = line.price_subtotal * fbl_brw.invoice_id.x_studio_field_l5IHS
                            tax_amount = (line.price_total - line.price_subtotal) * fbl_brw.invoice_id.x_studio_field_l5IHS
                        else:
                            base = fbl_brw.invoice_id.currency_id._convert(line.price_subtotal, fbl_brw.invoice_id.company_currency_id, fbl_brw.invoice_id.company_id, fbl_brw.invoice_id.date)
                            tax_amount = fbl_brw.invoice_id.currency_id._convert(line.price_total - line.price_subtotal, fbl_brw.invoice_id.company_currency_id, fbl_brw.invoice_id.company_id, fbl_brw.invoice_id.date)
                        ####################################################################################
                        if busq:
                            if busq == tax_type[field_tax]:  # account.tax
                                # if not fbt_brw.fbl_id.iwdl_id.invoice_id.name: #facura de account.wh.iva.line
                                #     data[field_name] += field_amount == 'base' and (
                                #         fbt_brw.fbl_id.invoice_id.factura_id.amount_gravable if fbt_brw.base_amount == 0 else fbt_brw.base_amount) * sign \
                                #                         or fbt_brw.tax_amount * sign
                                # else:
                                data[field_name] += field_amount == 'base' and base * sign \
                                                    or tax_amount * sign

                if fbl_brw.invoice_id.state != 'cancel':
                    fbl_brw.write(data)
        return True


    def link_book_lines_and_taxes(self, fb_id):
        """ Updates the fiscal book taxes. Link the tax with the corresponding
        book line and update the fields of sum taxes in the book.
        @param fb_id: the id of the current fiscal book """

        #        fbl_obj = self.env['fiscal.book.line']
 #       ait_obj = self.env['account.invoice.tax']
        ut_obj = self.env['l10n.ut']
        fbt_obj = self.env['fiscal.book.taxes']
        # write book taxes
        data = []
        tax_data = {}
        exento = 0.0
        base_exento = 0
        amount = 0
        name = ' '
        local_period = self.get_time_period(self.time_period)
        base = 0
        fiscal_book = self.browse(fb_id)
        for fbl in fiscal_book.fbl_ids:

            if fbl.iwdl_id.invoice_id:

                fiscal_taxes = self.env['fiscal.book.taxes']
                line_taxes = {'fb_id': fb_id, 'fbl_id': fbl.id, 'base_amount': 0.0, 'tax_amount': 0.0, 'name': ' ', }
                fiscal_book = self.browse(fb_id)
                f_xc = ut_obj.sxc(
                    fbl.iwdl_id.invoice_id.currency_id.id,
                    fbl.iwdl_id.invoice_id.company_id.currency_id.id,
                    fbl.iwdl_id.invoice_id.invoice_date)
                # if fbl.doc_type == 'N/C' or fbl.doc_type == 'N/D':
                #     sign = -1
                # else:
                sign = 1
                sum_base_imponible = 0
                amount_field_data = {'total_with_iva':
                                        0.0,
                                     'vat_sdcf': 0.0, 'vat_exempt': 0.0, 'vat_general_base': 0.0,}

                for ait in fbl.iwdl_id.tax_line:
                    busq = self.env['account.tax'].search([('id', '=', ait.id_tax)])
                    if busq:
                        if ait.amount == 0:
                            base = ait.base
                            name = ait.name
                            amount_field_data['vat_exempt'] += exento * sign
                        else:
                            base = ait.base
                            amount = ait.amount
                            name = ait.name
                        if (ait.amount + ait.base) > 0:
                            amount_field_data['total_with_iva'] += (ait.amount + ait.base)* sign
                            if busq.appl_type == 'sdcf':
                                    amount_field_data['vat_sdcf'] += base * sign
                            if busq.appl_type == 'exento':
                                amount_field_data['vat_exempt'] += base * sign
                            if busq.appl_type == 'general':
                                amount_field_data['vat_general_base'] += base * sign

                        tax_data.update({'fb_id': fb_id,
                                         'fbl_id': fbl.id,
                                        # 'ait_id': busq.id,
                                         'base_amount': amount_field_data['vat_general_base'],
                                         'tax_amount': ait.amount})

                        line_taxes.update({'fb_id': fb_id,
                                           'fbl_id': fbl.id,
                                           'base_amount':  base,
                                           'tax_amount': amount,
                                           'name': name,
                                           'type': fiscal_book.type

                                           })
                    fbl.write(amount_field_data)
                    if line_taxes:
                        fiscal_taxes.create(line_taxes)
                    else:
                        data.append((0, 0, {'fb_id': fb_id,
                                            'fbl_id': fbl.id,

                                            }))
                        self.write({'fbt_ids': data})
                
                if  fbl.iwdl_id.invoice_id.state == 'cancel' or ():
        
                        fbl.update({
                            'total_with_iva': 0,
                            'void_form' : '03-ANU',
                            'vat_sdcf': fbl.invoice_id.company_currency_id.round(fbl.vat_sdcf),
                            'vat_exempt': 0,
                            'vat_general_base': 0,
                            'vat_general_tax': 0,
                            'vat_reduced_base': 0,
                            'vat_reduced_tax': 0,
                            'vat_additional_base': 0,
                            'vat_additional_tax': 0,
                            'get_wh_vat': 0,
                            'wh_rate': 0


                        })

                elif local_period.get('dt_from') <= fbl.iwdl_id.retention_id.period_id <= local_period.get('dt_to') and (fbl.iwdl_id.invoice_id.date < local_period.get('dt_from') or fbl.iwdl_id.invoice_id.date > local_period.get('dt_to')):
                        
                        fbl.update({
                            'total_with_iva': 0,
                            'vat_sdcf': fbl.invoice_id.company_currency_id.round(fbl.vat_sdcf),
                            'vat_exempt': 0,
                            'vat_general_base': 0,
                            'vat_general_tax': 0,
                            'vat_reduced_base': 0,
                            'vat_reduced_tax': 0,
                            'vat_additional_base': 0,
                            'vat_additional_tax': 0,
                    


                        })


            elif fbl.invoice_id:

                ####################################################################
                # Change currency USD to VES
                ####################################################################
                if (fbl.invoice_id.partner_id.people_type_company == 'pjnd' or fbl.invoice_id.partner_id.people_type_individual == 'pnnr') and fbl.invoice_id.currency_id != fbl.invoice_id.company_id.currency_id and fbl.invoice_id.x_studio_field_TJfMu:
                    rate = fbl.invoice_id.x_studio_field_l5IHS
                else:
                    rate = self._get_rate_from_invoice(fbl.invoice_id) if fbl.invoice_id.currency_id != fbl.invoice_id.company_currency_id else 1
                ####################################################################
                
                fiscal_book = self.browse(fb_id)
                fiscal_taxes = self.env['fiscal.book.taxes']
                line_taxes = {'fb_id': fb_id, 'fbl_id': fbl.id,'base_amount': 0.0 , 'tax_amount': 0.0, 'name': ' ',}
                f_xc = ut_obj.sxc(
                    fbl.invoice_id.currency_id.id,
                    fbl.invoice_id.company_id.currency_id.id,
                    fbl.invoice_id.invoice_date)
                busq = ' '
         
                sign = 1
                sum_base_imponible = 0
                amount_field_data = {
                	'total_with_iva': 0.0,
                    'vat_sdcf': 0.0,
                    'vat_exempt': 0.0,
                    'vat_general_base': 0.0
                }


                for line in fbl.invoice_id.invoice_line_ids:
                    amount = 0
                    base = 0
                    busq =  ''
                    tax = ' '

                    for tax in line.tax_ids:
                        busq = tax.appl_type
                        name = tax.name
                    if busq:
                        if (line.price_total - line.price_subtotal) == 0:
                            base = line.price_subtotal
                            amount = 0
                            amount_field_data['vat_exempt'] += exento * sign
                        else:
                            base = (line.price_subtotal)
                            amount = (line.price_total - line.price_subtotal)

                        if ((line.price_total - line.price_subtotal) == 0 or (line.price_total - line.price_subtotal) > 0) and line.price_total > 0:
                            amount_field_data['total_with_iva'] += line.price_total * sign
                            if busq == 'sdcf':
                                amount_field_data['vat_sdcf'] += base * sign
                            if busq == 'exento':
                                amount_field_data['vat_exempt'] += base * sign
                            if busq == 'general':
                                amount_field_data['vat_general_base'] += base * sign

                        tax_data.update({'fb_id': fb_id,
                                         'fbl_id': fbl.id,
                                    #     'ait_id': fbl.id,
                                         'base_amount': base,
                                         'tax_amount': amount})
                        if fbl.invoice_id.state == 'cancel':
                            line_taxes.update({'fb_id': fb_id,
                                            'fbl_id': fbl.id,
                                            'base_amount': 0, #multiplied by rate
                                            'tax_amount': 0, #multiplied by rate
                                            'name': name,
                                            'type': fiscal_book.type

                            })               
                        else:
                            line_taxes.update({'fb_id': fb_id,
                                            'fbl_id': fbl.id,
                                            'base_amount': fbl.invoice_id.company_currency_id.round(base * rate), #multiplied by rate
                                            'tax_amount': fbl.invoice_id.company_currency_id.round(amount * rate), #multiplied by rate
                                            'name': name,
                                            'type': fiscal_book.type

                            })

                    fbl.write(amount_field_data)
                    if line_taxes:
                        fiscal_taxes.create(line_taxes)
                    else:
                        data.append((0, 0, {'fb_id': fb_id,
                                            'fbl_id': fbl.id,

                                            }))
                        self.write({'fbt_ids': data})

                if fbl.invoice_id.state == 'cancel':
         
                    fbl.update({
                        'total_with_iva': 0,
                        'void_form' : '03-ANU',
                        'vat_sdcf': fbl.invoice_id.company_currency_id.round(fbl.vat_sdcf * rate),
                        'vat_exempt': 0,
                        'vat_general_base': 0,
                        'vat_general_tax': 0,
                        'vat_reduced_base': 0,
                        'vat_reduced_tax': 0,
                        'vat_additional_base': 0,
                        'vat_additional_tax': 0

                    })
                else:
                    fbl.write({
                    'total_with_iva': fbl.invoice_id.company_currency_id.round(fbl.total_with_iva * rate),
                    'vat_sdcf': fbl.invoice_id.company_currency_id.round(fbl.vat_sdcf * rate),
                    'vat_exempt': fbl.invoice_id.company_currency_id.round(fbl.vat_exempt * rate),
                    'vat_general_base': fbl.invoice_id.company_currency_id.round(fbl.vat_general_base * rate)
                })

        self.update_book_taxes_summary()
        self.update_book_lines_taxes_fields()
        self.update_book_taxes_amount_fields()
        return True
