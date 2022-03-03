# coding: utf-8


import tempfile
import binascii
import io
import xlsxwriter
import logging
# import openpyxl
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
import xlwt
import base64
from datetime import datetime
from io import StringIO
# import pandas as pd
from io import BytesIO
from odoo import fields, models, api, exceptions, _
from odoo.exceptions import ValidationError
from odoo.tools import float_round

class StatementWizard(models.TransientModel):

    _name = "mrp.wizard.xls"
    _description = "Wizard statement."

    file_download = fields.Binary('Archivo XLS',
    # default=lambda self: self.createdd(), 
     readonly=True)
    name_excel = fields.Char('File Name',default='Excels', size=32)


    
    
    def createdd(self):
        print('aja')
        id = self.env.context.get('id_active')
        aja = self.env['mrp.bom'].search([('id', '=', id)], limit=1)
        doc = self._get_pdf_line(id, product_id=aja.product_id, qty=1, unfolded=True)
        excel = self.create_excel(doc)
        
        
        return excel

    def create_excel(self, docs):
        format_new = "%d/%m/%Y"



        fp = BytesIO()
        wb = xlwt.Workbook(encoding='utf-8')
        writer = wb.add_sheet('Nombre de hoja')
        xlwt.add_palette_colour("custom_colour", 0x21)
        wb.set_colour_RGB(0x21, 164,164,164)
        header_content_style = xlwt.easyxf("font: name Helvetica size 40 px, bold 1, height 200; align: horiz center;")
        header_content_style_left = xlwt.easyxf("font: name Helvetica size 40 px, bold 1, height 200; align: horiz left;")
        sub_header_style_1 = xlwt.easyxf(
            "font: name Helvetica size 10 px, bold 1, height 170; borders: left thin, right thin, top thin, bottom thin; align: horiz center;")
        sub_header_style_1_1 = xlwt.easyxf(
            "font: name Helvetica size 10 px, bold 1, height 170; borders: left thin, right thin, top thin, bottom thin; align: horiz left;")
        sub_header_style = xlwt.easyxf(
            "font: name Helvetica size 10 px, bold 1, height 170; borders: left thin, right thin, top thin, bottom thin; align: horiz center; pattern: pattern solid,fore_colour custom_colour;")  # color pattern: pattern solid,fore_colour blue;
        sub_header_style_2 = xlwt.easyxf(
            "font: name Helvetica size 10 px, bold 1, height 170; borders: left thin, right thin, top thin, bottom thin; align: horiz left;")

        line_content_style_totales = xlwt.easyxf(
            "font: name Helvetica size 10 px, bold 1, height 170; borders: left thin, right thin, top thin, bottom thin; align: horiz right;",
            num_format_str='#,##0.00')
        
        row = 1
       
        writer.write_merge(row, row, 1, 5, 'BoM Structure & Cost ', header_content_style_left)
        row += 1
        writer.write_merge(row, row, 1, 5, docs['bom_prod_name'], header_content_style_left)
        row += 1
        writer.write_merge(row, row, 1, 5, docs['code'], header_content_style_left)
        row += 1
        level = 1
       
        for line in docs['lines']:
            if line['level'] > level:
                level=line['level']
               
        writer.write_merge(row, row, 1, level+1, "Product", sub_header_style)
        writer.write_merge(row, row, level+2, level+2, "BoM ", sub_header_style)
        writer.write_merge(row, row, level+3, level+3, "Ruta de Producción", sub_header_style)
        writer.write_merge(row, row, level+4, level+4, "BoM Version", sub_header_style)
        writer.write_merge(row, row, level+5, level+5, "ECOs", sub_header_style)
        writer.write_merge(row, row, level+6, level+6, "Quantity", sub_header_style)
        writer.write_merge(row, row,level+7, level+7, "Unit of Measure", sub_header_style)
        writer.write_merge(row, row, level+8, level+8, "Product Cost", sub_header_style)
        writer.write_merge(row, row, level+9, level+9, "BoM Cost", sub_header_style)
        
        
        row += 1
        writer.write_merge(row, row, 1, 1, docs['bom_prod_name'], sub_header_style_1_1)
        writer.write_merge(row, row,level+2, level+2, docs['code'] if docs.get('code',False) else '', sub_header_style_1)
        writer.write_merge(row, row,level+3, level+3, docs['route'] if docs.get('route',False) else '', sub_header_style_1)
        writer.write_merge(row, row, level+4, level+4, 1 if docs.get('code',False) else '', sub_header_style_1)
        writer.write_merge(row, row,  level+5, level+5, '', sub_header_style_1)
        writer.write_merge(row, row,level+6, level+6, round(docs['bom_qty'],3), sub_header_style_1)
        writer.write_merge(row, row, level+7, level+7,docs['lines'][0]['uom'], sub_header_style_1)
        writer.write_merge(row, row,  level+8, level+8,docs['price'] if docs.get('price',False) else '', sub_header_style_1)
        writer.write_merge(row, row, level+9, level+9,docs['total'], sub_header_style_1)
        
        for line in docs['lines']:
            row += 1
            space = ''
            # for number in range(line['level']):
            #     space = space+'      '

            writer.write_merge(row, row, line['level']+1, line['level']+1, line['name'], sub_header_style_1_1)
            writer.write_merge(row, row, level+2, level+2, line['code'] if line.get('code',False) else '', sub_header_style_1)
            writer.write_merge(row, row, level+3, level+3, line['route'] if line.get('route',False) else '', sub_header_style_1)
            writer.write_merge(row, row, level+4, level+4, 1 if line.get('code',False) else '', sub_header_style_1)
            writer.write_merge(row, row,level+5, level+5, '', sub_header_style_1)
            writer.write_merge(row, row, level+6, level+6, round(line['quantity'],3), sub_header_style_1)
            writer.write_merge(row, row, level+7, level+7,line['uom'], sub_header_style_1)
            writer.write_merge(row, row, level+8, level+8,line['prod_cost'] if line.get('prod_cost',False) else '', sub_header_style_1)
            writer.write_merge(row, row, level+9, level+9,line['bom_cost'], sub_header_style_1)
        
        row += 1
        writer.write_merge(row, row, level+8, level+8, docs['price'] if docs.get('price',False) else 0, sub_header_style_1)
        writer.write_merge(row, row, level+9, level+9,docs['total'], sub_header_style_1)

        wb.save(fp)
        out = base64.encodestring(fp.getvalue())
        self.write({'name_excel': 'Bom Structure.xls','file_download':out})

        
        return {
            'type': 'ir.actions.act_window',
            'res_model': "mrp.wizard.xls",
            'name': 'Exportar Reporte',
            'view_mode': 'form',
            'view_type': 'form',
            'res_id': self.id,
            'views': [(False, 'form')],
            'target': 'new',
        }



   

    def _get_pdf_line(self, bom_id, product_id=False, qty=1, child_bom_ids=[], unfolded=False):

        def get_sub_lines(bom, product_id, line_qty, line_id, level):
            data = self._get_bom(bom_id=bom.id, product_id=product_id, line_qty=line_qty, line_id=line_id, level=level)
            bom_lines = data['components']
            lines = []
            for bom_line in bom_lines:
                lines.append({
                    'name': bom_line['prod_name'],
                    'type': 'bom',
                    'quantity': bom_line['prod_qty'],
                    'uom': bom_line['prod_uom'],
                    'prod_cost': bom_line['prod_cost'],
                    'bom_cost': bom_line['total'],
                    'level': bom_line['level'],
                    'code': bom_line['code'],
                     'route':self.env['mrp.bom'].search([('id', '=', bom_line['child_bom'])]).routing_id.display_name or '',
                    'child_bom': bom_line['child_bom'],
                    'prod_id': bom_line['prod_id']
                })
                if bom_line['child_bom'] and (unfolded or bom_line['child_bom'] in child_bom_ids):
                    line = self.env['mrp.bom.line'].browse(bom_line['line_id'])
                    lines += (get_sub_lines(line.child_bom_id, line.product_id.id, bom_line['prod_qty'], line, level + 1))
            if data['operations']:
                lines.append({
                    'name': _('Operations'),
                    'type': 'operation',
                    'quantity': data['operations_time'],
                    'uom': _('minutes'),
                    'bom_cost': data['operations_cost'],
                    'level': level,
                })
                for operation in data['operations']:
                    if unfolded or 'operation-' + str(bom.id) in child_bom_ids:
                        lines.append({
                            'name': operation['name'],
                            'type': 'operation',
                            'quantity': operation['duration_expected'],
                            'uom': _('minutes'),
                            'bom_cost': operation['total'],
                            'level': level + 1,
                        })
            return lines

        bom = self.env['mrp.bom'].browse(bom_id)
        product_id = product_id or bom.product_id.id or bom.product_tmpl_id.product_variant_id.id
        data = self._get_bom(bom_id=bom_id, product_id=product_id, line_qty=qty)
        pdf_lines = get_sub_lines(bom, product_id, qty, False, 1)
        data['components'] = []
        data['lines'] = pdf_lines
        return data


    def _get_bom(self, bom_id=False, product_id=False, line_qty=False, line_id=False, level=False):
        bom = self.env['mrp.bom'].browse(bom_id)
        company = bom.company_id or self.env.company
        bom_quantity = line_qty
        if line_id:
            current_line = self.env['mrp.bom.line'].browse(int(line_id))
            bom_quantity = current_line.product_uom_id._compute_quantity(line_qty, bom.product_uom_id) or 0
        # Display bom components for current selected product variant
        if product_id:
            product = self.env['product.product'].browse(int(product_id))
        else:
            product = bom.product_id or bom.product_tmpl_id.product_variant_id
        if product:
            price = product.uom_id._compute_price(product.with_context(force_company=company.id).standard_price, bom.product_uom_id) * bom_quantity
            attachments = self.env['mrp.document'].search(['|', '&', ('res_model', '=', 'product.product'),
            ('res_id', '=', product.id), '&', ('res_model', '=', 'product.template'), ('res_id', '=', product.product_tmpl_id.id)])
        else:
            # Use the product template instead of the variant
            price = bom.product_tmpl_id.uom_id._compute_price(bom.product_tmpl_id.with_context(force_company=company.id).standard_price, bom.product_uom_id) * bom_quantity
            attachments = self.env['mrp.document'].search([('res_model', '=', 'product.template'), ('res_id', '=', bom.product_tmpl_id.id)])
        operations = []
        if bom.product_qty > 0:
            operations = self._get_operation_line(bom.routing_id, float_round(bom_quantity / bom.product_qty, precision_rounding=1, rounding_method='UP'), 0)
        lines = {
            'bom': bom,
            'bom_qty': bom_quantity,
            'bom_prod_name': product.display_name,
            'route':bom.routing_id.display_name,
            'currency': company.currency_id,
            'product': product,
            'code': bom and bom.display_name or '',
            'price': price,
            'total': sum([op['total'] for op in operations]),
            'level': level or 0,
            'operations': operations,
            'operations_cost': sum([op['total'] for op in operations]),
            'attachments': attachments,
            'operations_time': sum([op['duration_expected'] for op in operations])
        }
        components, total = self._get_bom_lines(bom, bom_quantity, product, line_id, level)
        lines['components'] = components
        lines['total'] += total
        return lines

    def _get_bom_lines(self, bom, bom_quantity, product, line_id, level):
        components = []
        total = 0
        for line in bom.bom_line_ids:
            line_quantity = (bom_quantity / (bom.product_qty or 1.0)) * line.product_qty
            if line._skip_bom_line(product):
                continue
            company = bom.company_id or self.env.company
            price = line.product_id.uom_id._compute_price(line.product_id.with_context(force_company=company.id).standard_price, line.product_uom_id) * line_quantity
            if line.child_bom_id:
                factor = line.product_uom_id._compute_quantity(line_quantity, line.child_bom_id.product_uom_id) / line.child_bom_id.product_qty
                sub_total = self._get_price(line.child_bom_id, factor, line.product_id)
            else:
                sub_total = price
            sub_total = self.env.company.currency_id.round(sub_total)
            components.append({
                'prod_id': line.product_id.id,
                'prod_name': line.product_id.display_name,
                'code': line.child_bom_id and line.child_bom_id.display_name or '',
                'prod_qty': line_quantity,
                'prod_uom': line.product_uom_id.name,
                'prod_cost': company.currency_id.round(price),
                'parent_id': bom.id,
                'line_id': line.id,
                'level': level or 0,
                'total': sub_total,
                'child_bom': line.child_bom_id.id,
                'phantom_bom': line.child_bom_id and line.child_bom_id.type == 'phantom' or False,
                'attachments': self.env['mrp.document'].search(['|', '&',
                    ('res_model', '=', 'product.product'), ('res_id', '=', line.product_id.id), '&', ('res_model', '=', 'product.template'), ('res_id', '=', line.product_id.product_tmpl_id.id)]),

            })
            total += sub_total
        return components, total

    def _get_operation_line(self, routing, qty, level):
        operations = []
        total = 0.0
        for operation in routing.operation_ids:
            operation_cycle = float_round(qty / operation.workcenter_id.capacity, precision_rounding=1, rounding_method='UP')
            duration_expected = operation_cycle * operation.time_cycle + operation.workcenter_id.time_stop + operation.workcenter_id.time_start
            total = ((duration_expected / 60.0) * operation.workcenter_id.costs_hour)
            operations.append({
                'level': level or 0,
                'operation': operation,
                'name': operation.name + ' - ' + operation.workcenter_id.name,
                'duration_expected': duration_expected,
                'total': self.env.company.currency_id.round(total),
            })
        return operations
    
    def _get_price(self, bom, factor, product):
        price = 0
        if bom.routing_id:
            # routing are defined on a BoM and don't have a concept of quantity.
            # It means that the operation time are defined for the quantity on
            # the BoM (the user produces a batch of products). E.g the user
            # product a batch of 10 units with a 5 minutes operation, the time
            # will be the 5 for a quantity between 1-10, then doubled for
            # 11-20,...
            operation_cycle = float_round(factor, precision_rounding=1, rounding_method='UP')
            operations = self._get_operation_line(bom.routing_id, operation_cycle, 0)
            price += sum([op['total'] for op in operations])

        for line in bom.bom_line_ids:
            if line._skip_bom_line(product):
                continue
            if line.child_bom_id:
                qty = line.product_uom_id._compute_quantity(line.product_qty * factor, line.child_bom_id.product_uom_id) / line.child_bom_id.product_qty
                sub_price = self._get_price(line.child_bom_id, qty, line.product_id)
                price += sub_price
            else:
                prod_qty = line.product_qty * factor
                company = bom.company_id or self.env.company
                not_rounded_price = line.product_id.uom_id._compute_price(line.product_id.with_context(force_comany=company.id).standard_price, line.product_uom_id) * prod_qty
                price += company.currency_id.round(not_rounded_price)
        return price

    