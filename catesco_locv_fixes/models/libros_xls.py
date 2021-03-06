# coding: utf-8
##############################################################################

###############################################################################
import time
import math

from odoo import fields, models, api, exceptions, _
from odoo.exceptions import ValidationError
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT as DATETIME_FORMAT
from datetime import datetime, date, timedelta
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT
from io import BytesIO
import xlwt, base64

class FiscalBookWizard(models.TransientModel):
    _inherit = "fiscal.book.wizard"

    @api.model
    def xls_compra(self):
        format_new = "%d/%m/%Y"
        date_start = datetime.strptime(str(self.date_start), DATE_FORMAT)
        date_end = datetime.strptime(str(self.date_end), DATE_FORMAT)
        datos_compras = []
        purchasebook_ids = self.env['fiscal.book.line'].search(
            [('fb_id', '=', self.env.context['active_id'])], order='emission_date asc')
        emission_date = ' '
        sum_compras_credit = 0
        sum_total_with_iva = 0
        sum_vat_general_base = 0
        sum_vat_general_tax = 0
        sum_vat_reduced_base = 0
        sum_vat_reduced_tax = 0
        sum_vat_additional_base = 0
        sum_vat_additional_tax = 0
        sum_get_wh_vat = 0
        suma_vat_exempt = 0

        vat_reduced_base = 0
        vat_reduced_rate = 0
        vat_reduced_tax = 0
        vat_additional_base = 0
        vat_additional_rate = 0
        vat_additional_tax = 0

        ''' COMPRAS DE IMPORTACIONES'''

        sum_total_with_iva_importaciones = 0
        sum_vat_general_base_importaciones = 0
        suma_base_general_importaciones = 0
        sum_base_general_tax_importaciones = 0
        sum_vat_general_tax_importaciones = 0
        sum_vat_reduced_base_importaciones = 0
        sum_vat_reduced_tax_importaciones = 0
        sum_vat_additional_base_importaciones = 0
        sum_vat_additional_tax_importaciones = 0

        hola = 0
        #######################################
        compras_credit = 0
        origin = 0
        number = 0

        for h in purchasebook_ids:
            h_vat_general_base = 0.0
            h_vat_general_rate = 0.0
            h_vat_general_tax = 0.0
            vat_general_base_importaciones = 0
            vat_general_rate_importaciones = 0
            vat_general_general_rate_importaciones = 0
            vat_general_tax_importaciones = 0
            vat_reduced_base_importaciones = 0
            vat_reduced_rate_importaciones = 0
            vat_reduced_tax_importaciones = 0
            vat_additional_tax_importaciones = 0
            vat_additional_rate_importaciones = 0
            vat_additional_base_importaciones = 0
            vat_reduced_base = 0
            vat_reduced_rate = 0
            vat_reduced_tax = 0
            vat_additional_base = 0
            vat_additional_rate = 0
            vat_additional_tax = 0
            get_wh_vat = 0

            if h.type == 'ntp':
                compras_credit = h.invoice_id.amount_untaxed

            if h.doc_type == 'N/C':
                origin = h.affected_invoice
                if h.invoice_id:
                    if h.invoice_id.nro_ctrl:
                        busq1 = self.env['account.move'].search([('nro_ctrl', '=', h.invoice_id.nro_ctrl)])
                        if busq1:
                            for busq2 in busq1:
                                if busq2.type == 'in_invoice':
                                    number = busq2.name or ''

            sum_compras_credit += compras_credit
            if h.doc_type == 'N/C':
                suma_vat_exempt -= h.vat_exempt
            else:
                suma_vat_exempt += h.vat_exempt
            planilla = ''
            expediente = ''
            total = 0
            partner = self.env['res.partner'].search([('name','=', h.partner_name)])
           
            if len(partner) > 1:
                if h.invoice_id:
                    partner = h.invoice_id.partner_id
                elif h.iwdl_id:
                    partner = h.iwdl_id.invoice_id.partner_id
            if (partner.company_type == 'company' or partner.company_type == 'person') and (
                    partner.people_type_company or partner.people_type_individual) and (
                    partner.people_type_company == 'pjdo' or partner.people_type_individual == 'pnre' or partner.people_type_individual == 'pnnr'):
                '####################### NO ES PROVEDOR INTERNACIONAL########################################################3'
                if h.invoice_id:
    
                    ####################################################################
                    # Change currency USD to VES
                    ####################################################################
                    rate = self._get_VES_rate_from_invoice(h.invoice_id) if h.invoice_id.currency_id.name == 'USD' else 1
                    #####################################################################

                    #############################################################################
                    if (h.invoice_id.partner_id.people_type_company == 'pjnd' or h.invoice_id.partner_id.people_type_individual == 'pnnr') and h.invoice_id.currency_id != h.invoice_id.company_id.currency_id and h.invoice_id.x_studio_field_TJfMu:
                        total = h.invoice_id.amount_total * h.invoice_id.x_studio_field_l5IHS
                    else:
                        total = h.invoice_id.currency_id._convert(
                            h.invoice_id.amount_total, h.invoice_id.company_currency_id, h.invoice_id.company_id, h.invoice_id.date)
                    ##############################################################################
                  

                  
                    if h.doc_type == 'N/C':
                        sum_vat_additional_tax -= h.vat_additional_tax  # IMPUESTO DE IVA ALICUOTA ADICIONAL
                        sum_total_with_iva -= total  # Total monto con IVA
                        sum_vat_general_base -= h.vat_general_base # Base Imponible Alicuota general
                        sum_vat_general_tax -= h.vat_general_tax
                        sum_vat_reduced_base -= h.vat_reduced_base  # Base Imponible de alicuota Reducida
                        sum_vat_reduced_tax -= h.vat_reduced_tax  # Impuesto de IVA alicuota reducida
                        sum_vat_additional_base -= h.vat_additional_base  # BASE IMPONIBLE ALICUOTA ADICIONAL
                    else:
                        sum_vat_additional_tax += h.vat_additional_tax  # IMPUESTO DE IVA ALICUOTA ADICIONAL
                        sum_vat_reduced_base += h.vat_reduced_base  # Base Imponible de alicuota Reducida
                        sum_vat_reduced_tax += h.vat_reduced_tax  # Impuesto de IVA alicuota reducida
                        sum_vat_additional_base += h.vat_additional_base  # BASE IMPONIBLE ALICUOTA ADICIONAL
                        sum_total_with_iva += total
                        sum_vat_general_base += h.vat_general_base # Base Imponible Alicuota general
                        sum_vat_general_tax += h.vat_general_tax  
                     # Total monto con IVA
                    h_vat_general_base = h.vat_general_base
                    tax_base = 0
                    for iva in h.fbt_ids:
                        tax_base += iva.tax_amount 
                    if tax_base > 0:
                        h_vat_general_rate = '16'
                    
                    
                    # if h.fbt_ids[0].name[5:7] != '16':
                    #     h_vat_general_rate = '0'
                    # else:    
                    #     h_vat_general_rate =h.fbt_ids[0].name[5:7] if h.fbt_ids else False
                    h_vat_general_tax = h.vat_general_tax if h.vat_general_tax else 0.0
                    vat_reduced_base = h.vat_reduced_base
                    vat_reduced_rate = int(h.vat_reduced_base and h.vat_reduced_tax * 100 / h.vat_reduced_base)
                    vat_reduced_tax = h.vat_reduced_tax
                    vat_additional_base = h.vat_additional_base
                    vat_additional_rate = int(h.vat_additional_base and h.vat_additional_tax * 100 / h.vat_additional_base)
                    vat_additional_tax = h.vat_additional_tax
                    get_wh_vat = h.get_wh_vat

                    emission_date = datetime.strftime(datetime.strptime(str(h.emission_date), DEFAULT_SERVER_DATE_FORMAT),
                                                       format_new)
                ################################################
                elif h.iwdl_id.invoice_id:
                ################################################

                    ####################################################################
                    # Change currency USD to VES
                    ####################################################################
                    rate = self._get_VES_rate_from_invoice(h.iwdl_id.invoice_id) if h.iwdl_id.invoice_id.currency_id.name == 'USD' else 1
                    #####################################################################
                   
                    ###############################################################################
                    if (h.iwdl_id.invoice_id.partner_id.people_type_company == 'pjnd' or h.iwdl_id.invoice_id.partner_id.people_type_individual == 'pnnr') and h.iwdl_id.invoice_id.currency_id != h.iwdl_id.invoice_id.company_id.currency_id and h.iwdl_id.invoice_id.x_studio_field_TJfMu:
                        total = h.iwdl_id.invoice_id.amount_total * h.iwdl_id.invoice_id.x_studio_field_l5IHS
                    else:
                        total = h.iwdl_id.invoice_id.currency_id._convert(
                            h.iwdl_id.invoice_id.amount_total, h.iwdl_id.invoice_id.company_currency_id, h.iwdl_id.invoice_id.company_id, h.iwdl_id.invoice_id.date)
                    ################################################################################
                    
                    if h.doc_type == 'N/C':
                        sum_total_with_iva -= total  # Total monto con IVA
                        sum_vat_general_base -= h.vat_general_base  # Base Imponible Alicuota general
                        sum_vat_general_tax -= h.vat_general_tax  # Impuesto de IVA
                        sum_vat_reduced_base -= h.vat_reduced_base  # Base Imponible de alicuota Reducida
                        sum_vat_reduced_tax -= h.vat_reduced_tax
                    # Impuesto de IVA alicuota reducida
                        sum_vat_additional_base -= h.vat_additional_base  # BASE IMPONIBLE ALICUOTA ADICIONAL
                        sum_vat_additional_tax -= h.vat_additional_tax  # IMPUESTO DE IVA ALICUOTA ADICIONAL
                    else:
                        sum_total_with_iva += total
                        sum_vat_general_base += h.vat_general_base  # Base Imponible Alicuota general
                        sum_vat_general_tax += h.vat_general_tax  # Impuesto de IVA
                        sum_vat_reduced_base += h.vat_reduced_base  # Base Imponible de alicuota Reducida
                        sum_vat_reduced_tax += h.vat_reduced_tax
                    # Impuesto de IVA alicuota reducida
                        sum_vat_additional_base += h.vat_additional_base  # BASE IMPONIBLE ALICUOTA ADICIONAL
                        sum_vat_additional_tax += h.vat_additional_tax  # IMPUESTO DE IVA ALICUOTA ADICIONAL
                    # sum_vat_general_base += h.vat_general_base  # Base Imponible Alicuota general
                    # sum_vat_general_tax += h.vat_general_tax  # Impuesto de IVA
                    h_vat_general_base = h.vat_general_base
                   
                   
                    tax_base = 0
                    for iva in h.fbt_ids:
                        tax_base += iva.tax_amount 
                        
                    if tax_base > 0:
                        h_vat_general_rate = '16'
                    # if h.fbt_ids[0].name[5:7] != '16':
                    #     h_vat_general_rate = '0'
                    # else:
                    #     h_vat_general_rate =h.fbt_ids[0].name[5:7] if h.fbt_ids else False
                    h_vat_general_tax = h.vat_general_tax if h.vat_general_tax else 0.0
                    vat_reduced_base = h.vat_reduced_base
                    vat_reduced_rate = int(h.vat_reduced_base and h.vat_reduced_tax * 100 / h.vat_reduced_base)
                    vat_reduced_tax = h.vat_reduced_tax
                    vat_additional_base = h.vat_additional_base
                    vat_additional_rate = int(h.vat_additional_base and h.vat_additional_tax * 100 / h.vat_additional_base)
                    vat_additional_tax = h.vat_additional_tax
                    get_wh_vat = h.get_wh_vat

                    emission_date = datetime.strftime(
                        datetime.strptime(str(h.emission_date), DEFAULT_SERVER_DATE_FORMAT),
                        format_new)

            if (partner.company_type == 'company' or partner.company_type == 'person') and (
                    partner.people_type_company or partner.people_type_individual) and partner.people_type_company == 'pjnd':
                '############## ES UN PROVEEDOR INTERNACIONAL ##############################################'

                if h.invoice_id:
                    tasa = 1
                    # if h.invoice_id.currency_id.name == "USD":
                    #     tasa = self.obtener_tasa(h.invoice_id)
                    if h.invoice_id.fecha_importacion:
                        date_impor = h.invoice_id.fecha_importacion
                        emission_date = datetime.strftime(
                            datetime.strptime(str(date_impor), DEFAULT_SERVER_DATE_FORMAT),
                            format_new)
                        #############################################################################
                        if (h.invoice_id.partner_id.people_type_company == 'pjnd' or h.invoice_id.partner_id.people_type_individual == 'pnnr') and h.invoice_id.currency_id != h.invoice_id.company_id.currency_id and h.invoice_id.x_studio_field_TJfMu:
                            total = h.invoice_id.amount_total * h.invoice_id.x_studio_field_l5IHS
                        else:
                            total = (h.invoice_id.amount_total)
                        ##############################################################################
                    else:
                        date_impor = h.invoice_id.invoice_date
                        emission_date = datetime.strftime(
                            datetime.strptime(str(date_impor), DEFAULT_SERVER_DATE_FORMAT),
                            format_new)

                    planilla = h.invoice_id.nro_planilla_impor
                    expediente = h.invoice_id.nro_expediente_impor
                else:

                    date_impor = h.iwdl_id.invoice_id.fecha_importacion
                    emission_date = datetime.strftime(datetime.strptime(str(date_impor), DEFAULT_SERVER_DATE_FORMAT),
                                                      format_new)
                    planilla = h.iwdl_id.invoice_id.nro_planilla_impor
                    expediente = h.iwdl_id.invoice_id.nro_expediente_impor
                    tasa = 1
                    # if h.iwdl_id.invoice_id.currency_id.name == "USD":
                    #     tasa = self.obtener_tasa(h.iwdl_id.invoice_id)
                    ###############################################################################
                    if (h.iwdl_id.invoice_id.partner_id.people_type_company == 'pjnd' or h.iwdl_id.invoice_id.partner_id.people_type_individual == 'pnnr') and h.iwdl_id.invoice_id.currency_id != h.iwdl_id.invoice_id.company_id.currency_id and h.iwdl_id.invoice_id.x_studio_field_TJfMu:
                        total = h.iwdl_id.invoice_id.amount_total * h.iwdl_id.invoice_id.x_studio_field_l5IHS
                    else:
                        total = (h.iwdl_id.invoice_id.amount_total)
                    ################################################################################
                get_wh_vat = 0.0
                vat_reduced_base = 0
                vat_reduced_rate = 0
                vat_reduced_tax = 0
                vat_additional_base = 0
                vat_additional_rate = 0
                vat_additional_tax = 0
                'ALICUOTA GENERAL IMPORTACIONES'
                ###################################################################
                vat_general_base_importaciones = h.vat_general_base or total
                #################################################################
                vat_general_rate_importaciones = (h.vat_general_base and h.vat_general_tax * 100 / h.vat_general_base)
                vat_general_rate_importaciones = round(vat_general_rate_importaciones, 0)
                vat_general_tax_importaciones = h.vat_general_tax
                'ALICUOTA REDUCIDA IMPORTACIONES'
                vat_reduced_base_importaciones = h.vat_reduced_base
                vat_reduced_rate_importaciones = int(
                    h.vat_reduced_base and h.vat_reduced_tax * 100 / h.vat_reduced_base)
                vat_reduced_tax_importaciones = h.vat_reduced_tax
                'ALICUOTA ADICIONAL IMPORTACIONES'
                vat_additional_base_importaciones = h.vat_additional_base
                vat_additional_rate_importaciones = int(
                    h.vat_additional_base and h.vat_additional_tax * 100 / h.vat_additional_base)
                vat_additional_tax_importaciones = h.vat_additional_tax
                if h.doc_type == 'N/C':
                    sum_total_with_iva -= total  # Total monto con IVA
                    ###############################################################################
                    sum_vat_general_base_importaciones -= h.vat_general_base or total + h.vat_reduced_base + h.vat_additional_base # Base Imponible Alicuota general
                    ###############################################################################
                    sum_vat_general_tax_importaciones -= h.vat_general_tax + h.vat_additional_tax + h.vat_reduced_tax  # Impuesto de IVA
                else:
                    ###############################################################################
                    sum_vat_general_base_importaciones += h.vat_general_base or total + h.vat_reduced_base + h.vat_additional_base # Base Imponible Alicuota general
                    ###############################################################################
                    sum_vat_general_tax_importaciones += h.vat_general_tax + h.vat_additional_tax + h.vat_reduced_tax  # Impuesto de IVA
                    sum_total_with_iva += total
                 # Total monto con IVA
                'SUMA TOTAL DE TODAS LAS ALICUOTAS PARA LAS IMPORTACIONES'
                # sum_vat_general_base_importaciones += h.vat_general_base + h.vat_reduced_base + h.vat_additional_base  # Base Imponible Alicuota general
                # sum_vat_general_tax_importaciones += h.vat_general_tax + h.vat_additional_tax + h.vat_reduced_tax  # Impuesto de IVA

                'Suma total de Alicuota General'
                ####################################################################
                suma_base_general_importaciones += h.vat_general_base or sum_vat_general_base_importaciones
                ####################################################################
                sum_base_general_tax_importaciones += h.vat_general_tax

                ' Suma total de Alicuota Reducida'
                sum_vat_reduced_base_importaciones += h.vat_reduced_base  # Base Imponible de alicuota Reducida
                sum_vat_reduced_tax_importaciones += h.vat_reduced_tax  # Impuesto de IVA alicuota reducida
                'Suma total de Alicuota Adicional'
                sum_vat_additional_base_importaciones += h.vat_additional_base  # BASE IMPONIBLE ALICUOTA ADICIONAL
                sum_vat_additional_tax_importaciones += h.vat_additional_tax  # IMPUESTO DE IVA ALICUOTA ADICIONAL

                get_wh_vat = h.get_wh_vat
            if h.doc_type == 'N/C':    
                sum_get_wh_vat -= h.get_wh_vat  # IVA RETENIDO
            else:
                sum_get_wh_vat += h.get_wh_vat  # IVA RETENIDO

            if h_vat_general_base != 0:
                valor_base_imponible = h.vat_general_base
                valor_alic_general = h_vat_general_rate
                valor_iva = h_vat_general_tax
            else:
                valor_base_imponible = 0
                valor_alic_general = 0
                valor_iva = 0

            if get_wh_vat != 0:
                hola = get_wh_vat
            else:
                hola = 0

            if h.vat_exempt != 0:
                vat_exempt = h.vat_exempt

            else:
                vat_exempt = 0

            'Para las diferentes alicuotas que pueda tener el proveedor  internacional'
            'todas son mayor a 0'
            if vat_general_rate_importaciones > 0 and vat_reduced_rate_importaciones > 0 and vat_additional_rate_importaciones > 0:
                vat_general_general_rate_importaciones = str(vat_general_rate_importaciones) + ',' + ' ' + str(
                    vat_reduced_rate_importaciones) + ',' + ' ' + str(vat_additional_rate_importaciones) + ' '
            'todas son cero'
            if vat_general_rate_importaciones == 0 and vat_reduced_rate_importaciones == 0 and vat_additional_rate_importaciones == 0:
                vat_general_general_rate_importaciones = 0
            'Existe reducida y adicional'
            if vat_general_rate_importaciones == 0 and vat_reduced_rate_importaciones > 0 and vat_additional_rate_importaciones > 0:
                vat_general_general_rate_importaciones = str(vat_reduced_rate_importaciones) + ',' + ' ' + str(
                    vat_additional_rate_importaciones) + ' '
            'Existe general y adicional'
            if vat_general_rate_importaciones > 0 and vat_reduced_rate_importaciones == 0 and vat_additional_rate_importaciones > 0:
                vat_general_general_rate_importaciones = str(vat_general_rate_importaciones) + ',' + ' ' + str(
                    vat_additional_rate_importaciones) + ' '
            'Existe general y reducida'
            if vat_general_rate_importaciones > 0 and vat_reduced_rate_importaciones > 0 and vat_additional_rate_importaciones == 0:
                vat_general_general_rate_importaciones = str(vat_general_rate_importaciones) + ',' + ' ' + str(
                    vat_reduced_rate_importaciones) + ' '
            'Existe solo la general'
            if vat_general_rate_importaciones > 0 and vat_reduced_rate_importaciones == 0 and vat_additional_rate_importaciones == 0:
                vat_general_general_rate_importaciones = str(vat_general_rate_importaciones)
            'Existe solo la reducida'
            if vat_general_rate_importaciones == 0 and vat_reduced_rate_importaciones > 0 and vat_additional_rate_importaciones == 0:
                vat_general_general_rate_importaciones = str(vat_reduced_rate_importaciones)
            'Existe solo la adicional'
            if vat_general_rate_importaciones == 0 and vat_reduced_rate_importaciones == 0 and vat_additional_rate_importaciones > 0:
                vat_general_general_rate_importaciones = str(vat_additional_rate_importaciones)

            if h.invoice_id: 
                supplier_numb_invoice = h.invoice_id.supplier_invoice_number   
            else:
                supplier_numb_invoice = h.iwdl_id.supplier_invoice_number
            if h.debit_affected or h.credit_affected: 
                supplier_numb_invoice = "" 
          
            datos_compras.append({

                'emission_date': emission_date if emission_date else ' ',
                'partner_vat': h.partner_vat if h.partner_vat else ' ',
                'partner_name': h.partner_name,
                'people_type': h.people_type,
                'wh_number': h.wh_number if h.wh_number else ' ',
                'invoice_number':supplier_numb_invoice,
                'affected_invoice': h.affected_invoice,
                'ctrl_number': h.ctrl_number,
                'debit_affected': h.credit_affected,
                'credit_affected': h.debit_affected,  # h.credit_affected,
                'type': self.get_t_type(doc_type=h.doc_type),
                'doc_type': h.doc_type,
                'origin': origin,
                'number': number,
                'total_with_iva': total,
                'vat_exempt': vat_exempt,
                'compras_credit': compras_credit,
                'vat_general_base': valor_base_imponible,
                'vat_general_rate': valor_alic_general,
                'vat_general_tax': valor_iva,
                'vat_reduced_base': vat_reduced_base,
                'vat_reduced_rate': vat_reduced_rate,
                'vat_reduced_tax': vat_reduced_tax,
                'vat_additional_base': vat_additional_base,
                'vat_additional_rate': vat_additional_rate,
                'vat_additional_tax': vat_additional_tax,
                'get_wh_vat': hola,
                'vat_general_base_importaciones': vat_general_base_importaciones + vat_additional_base_importaciones + vat_reduced_base_importaciones,
                'vat_general_rate_importaciones': vat_general_general_rate_importaciones,
                'vat_general_tax_importaciones': vat_general_tax_importaciones + vat_reduced_tax_importaciones + vat_additional_tax_importaciones,
                'nro_planilla': planilla,
                'nro_expediente': expediente,
            })
        'SUMA TOTAL DE ALICUOTA ADICIONAL BASE'
        if sum_vat_additional_base != 0 and sum_vat_additional_base_importaciones > 0:
            sum_ali_gene_addi = sum_vat_additional_base
            sum_vat_additional_base = sum_vat_additional_base
        else:
            sum_ali_gene_addi = sum_vat_additional_base
        'SUMA TOTAL DE ALICUOTA ADICIONAL TAX'
        if sum_vat_additional_tax != 0 and sum_vat_additional_tax_importaciones > 0:
            sum_ali_gene_addi_credit = sum_vat_additional_tax
            sum_vat_additional_tax = sum_vat_additional_tax
        else:
            sum_ali_gene_addi_credit = sum_vat_additional_tax
        'SUMA TOTAL DE ALICUOTA GENERAL BASE'
        if sum_vat_general_base != 0 and suma_base_general_importaciones > 0:
            sum_vat_general_base = sum_vat_general_base
            sum_vat_general_tax = sum_vat_general_tax
        'SUMA TOTAL DE ALICUOTA REDUCIDA BASE'
        if sum_vat_reduced_base != 0 and sum_vat_reduced_base_importaciones > 0:
            sum_vat_reduced_base = sum_vat_reduced_base
            sum_vat_reduced_tax = sum_vat_reduced_tax

        ' IMPORTACIONES ALICUOTA GENERAL + ALICUOTA ADICIONAL'
        if sum_vat_additional_base_importaciones != 0:
            sum_ali_gene_addi_importaciones = sum_vat_additional_base_importaciones
        else:
            sum_ali_gene_addi_importaciones = sum_vat_additional_base_importaciones

        if sum_vat_additional_tax_importaciones != 0:
            sum_ali_gene_addi_credit_importaciones = sum_vat_additional_tax_importaciones
        else:
            sum_ali_gene_addi_credit_importaciones = sum_vat_additional_tax_importaciones

        total_compras_base_imponible = sum_vat_general_base + sum_ali_gene_addi + sum_vat_reduced_base + suma_base_general_importaciones + sum_ali_gene_addi_importaciones + sum_vat_reduced_base_importaciones + suma_vat_exempt
        total_compras_credit_fiscal = sum_vat_general_tax + sum_ali_gene_addi_credit + sum_vat_reduced_tax + sum_base_general_tax_importaciones + sum_ali_gene_addi_credit_importaciones + sum_vat_reduced_tax_importaciones

        #///////////////////////////////////////GENERANDO EXCEL////////////////////////////////////////////////////////
        fp = BytesIO()
        wb = xlwt.Workbook(encoding='utf-8')
        writer = wb.add_sheet('Nombre de hoja')
        xlwt.add_palette_colour("custom_colour", 0x21)
        wb.set_colour_RGB(0x21, 164,164,164)
        header_content_style = xlwt.easyxf("font: name Helvetica size 40 px, bold 1, height 200; align: horiz center;")
        header_content_style_left = xlwt.easyxf("font: name Helvetica size 40 px, bold 1, height 200; align: horiz left;")
        sub_header_style_1 = xlwt.easyxf(
            "font: name Helvetica size 10 px, bold 1, height 170; borders: left thin, right thin, top thin, bottom thin; align: horiz center;")
        sub_header_style = xlwt.easyxf(
            "font: name Helvetica size 10 px, bold 1, height 170; borders: left thin, right thin, top thin, bottom thin; align: horiz center; pattern: pattern solid,fore_colour custom_colour;")  # color pattern: pattern solid,fore_colour blue;
        sub_header_style_2 = xlwt.easyxf(
            "font: name Helvetica size 10 px, bold 1, height 170; borders: left thin, right thin, top thin, bottom thin; align: horiz left;")

        line_content_style_totales = xlwt.easyxf(
            "font: name Helvetica size 10 px, bold 1, height 170; borders: left thin, right thin, top thin, bottom thin; align: horiz right;",
            num_format_str='#,##0.00')
        libro_id = self.env['fiscal.book'].browse(self._context['active_id'])
        row = 1
        col = 0
        date_start = datetime.strftime(datetime.strptime(str(self.date_start), DEFAULT_SERVER_DATE_FORMAT),
                                       format_new)
        date_end = datetime.strftime(datetime.strptime(str(self.date_end), DEFAULT_SERVER_DATE_FORMAT), format_new)
        writer.write_merge(row, row, 1, 5, 'Nombre de la Empresa: ' + libro_id.company_id.name, header_content_style_left)
        row += 1
        writer.write_merge(row, row, 1, 5, 'RIF.: ' + libro_id.company_id.vat, header_content_style_left)
        row += 1
        street = street2 = ''
        if libro_id.company_id.street:
            street = libro_id.company_id.street
        if libro_id.company_id.street2:
            street2 = ', ' + libro_id.company_id.street2
        writer.write_merge(row, row, 1, 5, 'Direcci??n de la Empresa: ' + street + street2, header_content_style_left)
        row += 1
        writer.write_merge(row, row, 1, 55, 'LIBRO DE COMPRAS', header_content_style)
        row += 1
        writer.write_merge(row, row, 1, 55, 'Desde: ' + date_start + ' Hasta: ' + date_end, header_content_style)
        row += 1
        #aca va pre encabezado
        writer.write_merge(row, row, 22, 41, "Compras Internas", sub_header_style)
        writer.write_merge(row, row, 42, 51, "Compras de Importaciones", sub_header_style)
        writer.write_merge(row, row, 52, 55, "Compras de Importaciones", sub_header_style)
        row += 1
        writer.write_merge(row, row, 1, 1, "Nro. Op", sub_header_style)
        writer.write_merge(row, row, 2, 3, "Fecha Emisi??n Doc.", sub_header_style)
        writer.write_merge(row, row, 4, 4, "Nro. de RIF", sub_header_style)
        writer.write_merge(row, row, 5, 6, "Nombre ?? Raz??n Social", sub_header_style)
        writer.write_merge(row, row, 7, 7, "Tipo Prov.", sub_header_style)
        writer.write_merge(row, row, 8, 9, "Nro. de Factura", sub_header_style)
        writer.write_merge(row, row, 10, 11, "Nro. de Control", sub_header_style)
        writer.write_merge(row, row, 12, 13, "Nro. Nota de Cr??dito", sub_header_style)
        writer.write_merge(row, row, 14, 15, "Nro. Nota de D??bito", sub_header_style)
        writer.write_merge(row, row, 16, 17, "Tipo de Trans", sub_header_style)
        writer.write_merge(row, row, 18, 19, "Nro. Factura Afectada", sub_header_style)
        writer.write_merge(row, row, 20, 21, "Total Compras con IVA", sub_header_style)
        writer.write_merge(row, row, 22, 23, "Compras sin Derecho a Cr??dito", sub_header_style)
        writer.write_merge(row, row, 24, 25, "Base Imponible Alicuota General", sub_header_style)
        writer.write_merge(row, row, 26, 27, "% Alicuota General", sub_header_style)
        writer.write_merge(row, row, 28, 29, "Impuesto (I.V.A) Alicuota General", sub_header_style)
        writer.write_merge(row, row, 30, 31, "Base Imponible Alicuota Reducida", sub_header_style)
        writer.write_merge(row, row, 32, 33, "% Alicuota Reducida", sub_header_style)
        writer.write_merge(row, row, 34, 35, "Impuesto (I.V.A) Alicuota Reducida", sub_header_style)
        writer.write_merge(row, row, 36, 37, "Base Imponible Alicuota Adicional", sub_header_style)
        writer.write_merge(row, row, 38, 39, "% Alicuota Adicional", sub_header_style)
        writer.write_merge(row, row, 40, 41, "Impuesto (I.V.A) Alicuota Adicional", sub_header_style)
        writer.write_merge(row, row, 42, 43, "Base Imponible Alicuota General", sub_header_style)
        writer.write_merge(row, row, 44, 45, "% Alicuota General", sub_header_style)
        writer.write_merge(row, row, 46, 47, "Impuesto (I.V.A) Alicuota General", sub_header_style)
        writer.write_merge(row, row, 48, 49, "Nro. Planilla Importaci??n", sub_header_style)
        writer.write_merge(row, row, 50, 51, "Nro. Expediente Importaci??n", sub_header_style)
        writer.write_merge(row, row, 52, 53, "Nro. de Comprobante", sub_header_style)
        writer.write_merge(row, row, 54, 55, "IVA Ret (Vend.)", sub_header_style)
        contador_2 = 0
        for datos in datos_compras:
            
            row += 1
            contador_2 += 1
            writer.write_merge(row, row, 1, 1, contador_2, sub_header_style_1)
            writer.write_merge(row, row, 2, 3, datos.get('emission_date'), sub_header_style_1)
            writer.write_merge(row, row, 4, 4, datos.get('partner_vat'), sub_header_style_1)
            writer.write_merge(row, row, 5, 6, datos.get('partner_name'), sub_header_style_1)
            writer.write_merge(row, row, 7, 7, datos.get('people_type'), sub_header_style_1)
            # if datos.get('people_type') != 'N/DB':
            writer.write_merge(row, row, 8, 9, datos.get('invoice_number'), sub_header_style_1)
            writer.write_merge(row, row, 10, 11, datos.get('ctrl_number'), sub_header_style_1)
            # if datos.get('doc_type') == 'N/DB':
            writer.write_merge(row, row, 12, 13, datos.get('debit_affected'), sub_header_style_1)
            writer.write_merge(row, row, 14, 15, datos.get('credit_affected'), sub_header_style_1)
            writer.write_merge(row, row, 16, 17, datos.get('type'), sub_header_style_1)
            # if datos.get('doc_type') == 'N/DB':
            writer.write_merge(row, row, 18, 19, datos.get('affected_invoice'), sub_header_style_1)
            writer.write_merge(row, row, 20, 21, datos.get('total_with_iva'), sub_header_style_1)
            writer.write_merge(row, row, 22, 23, datos.get('vat_exempt'), sub_header_style_1)
            writer.write_merge(row, row, 24, 25, datos.get('vat_general_base'), sub_header_style_1)
            writer.write_merge(row, row, 26, 27, datos.get('vat_general_rate'), sub_header_style_1)
            writer.write_merge(row, row, 28, 29, datos.get('vat_general_tax'), sub_header_style_1)
            writer.write_merge(row, row, 30, 31, datos.get('vat_reduced_base'), sub_header_style_1)
            writer.write_merge(row, row, 32, 33, datos.get('vat_reduced_rate'), sub_header_style_1)
            writer.write_merge(row, row, 34, 35, datos.get('vat_reduced_tax'), sub_header_style_1)
            writer.write_merge(row, row, 36, 37, datos.get('vat_additional_base'), sub_header_style_1)
            writer.write_merge(row, row, 38, 39, datos.get('vat_additional_rate'), sub_header_style_1)
            writer.write_merge(row, row, 40, 41, datos.get('vat_additional_tax'), sub_header_style_1)
            writer.write_merge(row, row, 42, 43, datos.get('vat_general_base_importaciones'), sub_header_style_1)
            writer.write_merge(row, row, 44, 45, datos.get('vat_general_rate_importaciones'), sub_header_style_1)
            writer.write_merge(row, row, 46, 47, datos.get('vat_general_tax_importaciones'), sub_header_style_1)
            writer.write_merge(row, row, 48, 49, datos.get('nro_planilla'), sub_header_style_1)
            writer.write_merge(row, row, 50, 51, datos.get('nro_expediente'), sub_header_style_1)
            writer.write_merge(row, row, 52, 53, datos.get('wh_number'), sub_header_style_1)
            #################################################################################################
            writer.write_merge(row, row, 54, 55, datos.get('get_wh_vat'), sub_header_style_1)

        row += 2
        writer.write_merge(row, row, 18, 19, "Totales", sub_header_style)
        writer.write_merge(row, row, 20, 21, sum_total_with_iva, sub_header_style)
        writer.write_merge(row, row, 22, 23, suma_vat_exempt, sub_header_style)
        writer.write_merge(row, row, 24, 25, sum_vat_general_base, sub_header_style)
        writer.write_merge(row, row, 26, 27, "", sub_header_style)
        writer.write_merge(row, row, 28, 29, sum_vat_general_tax, sub_header_style)
        writer.write_merge(row, row, 30, 31, sum_vat_reduced_base, sub_header_style)
        writer.write_merge(row, row, 32, 33, "", sub_header_style)
        writer.write_merge(row, row, 34, 35, sum_vat_reduced_tax, sub_header_style)
        writer.write_merge(row, row, 36, 37, sum_vat_additional_base, sub_header_style)
        writer.write_merge(row, row, 38, 39, "", sub_header_style)
        writer.write_merge(row, row, 40, 41, sum_vat_additional_tax, sub_header_style)
        writer.write_merge(row, row, 42, 43, sum_vat_general_base_importaciones, sub_header_style)
        writer.write_merge(row, row, 44, 45, "", sub_header_style)
        writer.write_merge(row, row, 46, 47, sum_vat_general_tax_importaciones, sub_header_style)
        writer.write_merge(row, row, 48, 49, "", sub_header_style)
        writer.write_merge(row, row, 50, 51, "", sub_header_style)
        writer.write_merge(row, row, 52, 53, "", sub_header_style)
        writer.write_merge(row, row, 54, 55, sum_get_wh_vat, sub_header_style)

        row += 2

        writer.write_merge(row, row, 4, 27, "RESUMEN DE LIBRO DE COMPRAS", sub_header_style_1)
        writer.write_merge(row, row, 28, 32, "Base Imponible", sub_header_style_1)
        writer.write_merge(row, row, 33, 37, "Cr??dito Fiscal", sub_header_style_1)
        row += 1
        writer.write_merge(row, row, 4, 27, "Compras Internas no Gravadas y/o Sin Derecho a Cr??dito Fiscal", sub_header_style_2)
        writer.write_merge(row, row, 28, 32, suma_vat_exempt, sub_header_style_1)
        writer.write_merge(row, row, 33, 37, 0.00, sub_header_style_1)
        row += 1
        writer.write_merge(row, row, 4, 27, "Compras Internas gravadas por Alicuota General", sub_header_style_2)
        writer.write_merge(row, row, 28, 32, sum_vat_general_base, sub_header_style_1)
        writer.write_merge(row, row, 33, 37, sum_vat_general_tax, sub_header_style_1)
        row += 1
        writer.write_merge(row, row, 4, 27, "Compras Internas gravadas por Alicuota General mas Alicuota Adicional", sub_header_style_2)
        writer.write_merge(row, row, 28, 32, sum_ali_gene_addi, sub_header_style_1)
        writer.write_merge(row, row, 33, 37, sum_ali_gene_addi_credit, sub_header_style_1)
        row += 1
        writer.write_merge(row, row, 4, 27, "Compras Internas gravadas por Alicuota Reducida", sub_header_style_2)
        writer.write_merge(row, row, 28, 32, sum_vat_reduced_base, sub_header_style_1)
        writer.write_merge(row, row, 33, 37, sum_vat_reduced_tax, sub_header_style_1)
        row += 1
        writer.write_merge(row, row, 4, 27, "Importaciones gravadas Al??cuota General", sub_header_style_2)
        writer.write_merge(row, row, 28, 32, suma_base_general_importaciones, sub_header_style_1)
        writer.write_merge(row, row, 33, 37, sum_base_general_tax_importaciones, sub_header_style_1)
        row += 1
        writer.write_merge(row, row, 4, 27, "Importaciones gravadas por Al??cuota General mas Adicional", sub_header_style_2)
        writer.write_merge(row, row, 28, 32, sum_ali_gene_addi_importaciones, sub_header_style_1)
        writer.write_merge(row, row, 33, 37, sum_ali_gene_addi_credit_importaciones, sub_header_style_1)
        row += 1
        writer.write_merge(row, row, 4, 27, "Importaciones gravadas por Alicuota Reducida", sub_header_style_2)
        writer.write_merge(row, row, 28, 32, sum_vat_reduced_base_importaciones, sub_header_style_1)
        writer.write_merge(row, row, 33, 37, sum_vat_reduced_tax_importaciones, sub_header_style_1)
        row += 1
        writer.write_merge(row, row, 4, 27, "Total Compras y Cr??ditos Fiscales", sub_header_style_2)
        writer.write_merge(row, row, 28, 32, total_compras_base_imponible, sub_header_style_1)
        writer.write_merge(row, row, 33, 37, total_compras_credit_fiscal, sub_header_style_1)
        row += 1
        writer.write_merge(row, row, 4, 27, "Total IVA Retenido", sub_header_style_2)
        writer.write_merge(row, row, 28, 32, "", sub_header_style_1)
        writer.write_merge(row, row, 33, 37, sum_get_wh_vat, sub_header_style_1)

        wb.save(fp)
        out = base64.encodestring(fp.getvalue())
        self.write({'state': 'get', 'report': out, 'name': 'Libro de Compras.xls'})
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'fiscal.book.wizard',
            'name': 'Fiscal Book Report',
            'view_mode': 'form',
            'view_type': 'form',
            'res_id': self.id,
            'views': [(False, 'form')],
            'target': 'new',
        }
