# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.
from datetime import datetime, timedelta
import base64
from io import StringIO
from odoo import api, fields, models
from datetime import date
from odoo.tools.float_utils import float_round
from odoo.exceptions import Warning
from io import BytesIO
import xlwt
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT

class ReporteCategoria(models.TransientModel):
    _inherit = "stock.move.report.categoria"

   
    excel_report = fields.Binary('Descargar xls', filters='.xls', readonly=True)
    name_excel = fields.Char('File Name', size=32)



    def print_excel(self):
        self.datos()
        if self.excel_report:
            self.excel_report = False
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
        sub_header_style = xlwt.easyxf(
            "font: name Helvetica size 10 px, bold 1, height 170; borders: left thin, right thin, top thin, bottom thin; align: horiz center; pattern: pattern solid,fore_colour custom_colour;")  # color pattern: pattern solid,fore_colour blue;
        sub_header_style_2 = xlwt.easyxf(
            "font: name Helvetica size 10 px, bold 1, height 170; borders: left thin, right thin, top thin, bottom thin; align: horiz left;")

        line_content_style_totales = xlwt.easyxf(
            "font: name Helvetica size 10 px, bold 1, height 170; borders: left thin, right thin, top thin, bottom thin; align: horiz right;",
            num_format_str='#,##0.00')

        row = 1
        col = 0
        date_start = datetime.strftime(datetime.strptime(str(self.date_from), DEFAULT_SERVER_DATE_FORMAT),
                                       format_new)
        date_end = datetime.strftime(datetime.strptime(str(self.date_to), DEFAULT_SERVER_DATE_FORMAT), format_new)
        today_date = datetime.strftime(datetime.strptime(str(self.date_today), DEFAULT_SERVER_DATE_FORMAT), format_new)

        writer.write_merge(row, row, 1, 5, 'Nombre de la Empresa: ' + self.company_id.name, header_content_style_left)
        writer.write_merge(row, row, 12, 15, 'Fecha ' + today_date, header_content_style_left)
        row += 1
        writer.write_merge(row, row, 1, 5, 'RIF.: ' + self.company_id.vat, header_content_style_left)
        row += 1
        street = street2 = ''

        writer.write_merge(row, row, 1, 15, 'Reporte de Movimiento de Inventario '+self.category_id.name +' Periodo '+str(self.date_to.year), header_content_style)
        row += 1
        writer.write_merge(row, row, 1, 15, 'Desde: ' + date_start + ' Hasta: ' + date_end, header_content_style)
        row += 1
        writer.write_merge(row, row, 6, 9, 'Inventario Inicial ' , sub_header_style)
        writer.write_merge(row, row, 10, 13, 'Entradas del Mes' , sub_header_style)
        writer.write_merge(row, row, 16, 19, 'Salidas del Mes ' , sub_header_style)
        writer.write_merge(row, row, 22, 25, 'Ajustes del Mes' , sub_header_style)
        writer.write_merge(row, row, 28, 31, 'Inventario Final', sub_header_style)

        row += 1
        writer.write_merge(row, row, 1, 2, "Código", sub_header_style)
        writer.write_merge(row, row, 3, 4, "Unidad Descripción", sub_header_style)
        writer.write_merge(row, row, 5, 6, "Existencia Inicial", sub_header_style)
        writer.write_merge(row, row, 7, 8, "Costo Inicial ", sub_header_style)
        writer.write_merge(row, row, 9, 10, "Total Bolivares", sub_header_style)
        writer.write_merge(row, row, 11, 12, "Cantidad Entradas", sub_header_style)
        writer.write_merge(row, row, 13, 14, "Costo de Entradas", sub_header_style)
        writer.write_merge(row, row, 15, 16, "Total Bolivares", sub_header_style)
        writer.write_merge(row, row, 17, 18, "Cantidad Salidas", sub_header_style)
        writer.write_merge(row, row, 19, 20, "Costo de Salidas", sub_header_style)
        writer.write_merge(row, row, 21, 22, "Total Bolivares", sub_header_style)
        writer.write_merge(row, row, 23, 24, "Cantidad Ajutada", sub_header_style)
        writer.write_merge(row, row, 25, 26, "Costo de Ajuste", sub_header_style)
        writer.write_merge(row, row, 27, 28, "Total Bolivares", sub_header_style)
        writer.write_merge(row, row, 29, 30, "Stock Final", sub_header_style)
        writer.write_merge(row, row, 31, 32, "Costo Promedio", sub_header_style)
        writer.write_merge(row, row, 33, 34, "Total Bolivares", sub_header_style)


        total_general_inicial=0
        total_general_entradas=0
        total_general_salida=0
        total_general_ajuste=0
        total_general=0
        cat_general_inicial=0
        cat_general_entradas=0
        cat_general_salida=0
        cat_general_ajuste=0
        cat_general=0
        
        
        
        
        
        
        
        for line in self.libro:
            row += 1
            writer.write_merge(row, row, 1, 2,"LINEA:"+line.name.name, header_content_style)
            total_bolivares_inicial = 0
            total_bolivares_entradas= 0
            total_bolivares_salida = 0
            total_bolivares_ajuste= 0
            total_bolivares= 0
            linea_bolivares_inicial= 0
            linea_bolivares_entradas= 0
            linea_bolivares_salida= 0
            linea_bolivares_ajuste= 0
            linea_bolivares= 0
            for data in line.line_id:
                row += 1
                writer.write_merge(row, row, 1, 2, data.name.default_code, header_content_style)
                writer.write_merge(row, row, 3, 4, data.name.name, header_content_style)
                writer.write_merge(row, row, 5, 6, self.float_format(data.cantidad_inicial), header_content_style)
                writer.write_merge(row, row, 7, 8, self.float_format(data.costo_intradas), header_content_style)
                writer.write_merge(row, row, 9, 10, self.float_format(data.total_bolivares_inicial), header_content_style)
                writer.write_merge(row, row, 11, 12, self.float_format(data.cantidad_entradas), header_content_style)
                writer.write_merge(row, row, 13, 14, self.float_format(data.costo_entradas), header_content_style)
                writer.write_merge(row, row, 15, 16, self.float_format(data.total_bolivares_entradas), header_content_style)
                writer.write_merge(row, row, 17, 18, self.float_format(data.cantidad_salidas), header_content_style)
                writer.write_merge(row, row, 19, 20, self.float_format(data.costo_salidas), header_content_style)
                writer.write_merge(row, row, 21, 22, self.float_format(data.total_bolivares_salida), header_content_style)
                writer.write_merge(row, row, 23, 24, self.float_format(data.cantidad_ajuste), header_content_style)
                writer.write_merge(row, row, 25, 26, self.float_format(data.costo_ajuste), header_content_style)
                writer.write_merge(row, row, 27, 28, self.float_format(data.total_bolivares_ajuste), header_content_style)
                writer.write_merge(row, row, 29, 30, self.float_format(data.total), header_content_style)
                writer.write_merge(row, row, 31, 32, self.float_format(data.promedio), header_content_style)
                writer.write_merge(row, row, 33, 34, self.float_format(data.total_bolivares), header_content_style)

                total_bolivares_inicial = data.total_bolivares_inicial  + total_bolivares_inicial
                total_bolivares_entradas =data.total_bolivares_entradas + total_bolivares_entradas
                total_bolivares_salida = data.total_bolivares_salida + total_bolivares_salida
                total_bolivares_ajuste = data.total_bolivares_ajuste + total_bolivares_ajuste 
                total_bolivares = data.total_bolivares + total_bolivares 
                linea_bolivares_inicial = linea_bolivares_inicial + data.cantidad_inicial 
                linea_bolivares_entradas=linea_bolivares_entradas + data.cantidad_entradas
                linea_bolivares_salida=linea_bolivares_salida + data.cantidad_salidas
                linea_bolivares_ajuste=linea_bolivares_ajuste + data.cantidad_ajuste
                linea_bolivares=linea_bolivares + data.total    
                total_general_inicial=data.total_bolivares_inicial  + total_general_inicial
                total_general_entradas= total_general_entradas + data.total_bolivares_entradas
                total_general_salida=data.total_bolivares_salida +  total_general_salida
                total_general_ajuste=data.total_bolivares_ajuste +  total_general_ajuste
                total_general=total_general + data.total_bolivares    
                cat_general_inicial=cat_general_inicial + data.cantidad_inicial 
                cat_general_entradas= cat_general_entradas  + data.cantidad_entradas
                cat_general_salida=cat_general_salida + data.cantidad_salidas
                cat_general_ajuste=cat_general_ajuste + data.cantidad_ajuste
                cat_general=cat_general + data.total
            
            row += 1
            writer.write_merge(row, row, 1, 4, 'TOTAL POR LINEA', sub_header_style)
            writer.write_merge(row, row, 5, 6, self.float_format(linea_bolivares_inicial), header_content_style)
            writer.write_merge(row, row, 9, 10, self.float_format(total_bolivares_inicial), header_content_style)
            writer.write_merge(row, row, 11, 12, self.float_format(linea_bolivares_entradas), header_content_style)
            writer.write_merge(row, row, 15, 16, self.float_format(total_bolivares_entradas), header_content_style)
            writer.write_merge(row, row, 17, 18, self.float_format(linea_bolivares_salida), header_content_style)
            writer.write_merge(row, row, 21, 22, self.float_format(total_bolivares_salida), header_content_style)
            writer.write_merge(row, row, 23, 24, self.float_format(linea_bolivares_ajuste), header_content_style)
            writer.write_merge(row, row, 27, 28, self.float_format(total_bolivares_ajuste), header_content_style)
            writer.write_merge(row, row, 29, 30, self.float_format(linea_bolivares), header_content_style)
            writer.write_merge(row, row, 33, 34,self.float_format(total_bolivares), header_content_style)


        row += 1
        writer.write_merge(row, row, 1, 4, 'TOTAL GENERAL', sub_header_style)
        writer.write_merge(row, row, 5, 6, self.float_format(cat_general_inicial), header_content_style)
        writer.write_merge(row, row, 9, 10, self.float_format(total_general_inicial), header_content_style)
        writer.write_merge(row, row, 11, 12, self.float_format(cat_general_entradas), header_content_style)
        writer.write_merge(row, row, 15, 16, self.float_format(total_general_entradas), header_content_style)
        writer.write_merge(row, row, 17, 18, self.float_format(cat_general_salida), header_content_style)
        writer.write_merge(row, row, 21, 22, self.float_format(total_general_salida), header_content_style)
        writer.write_merge(row, row, 23, 24, self.float_format(cat_general_ajuste), header_content_style)
        writer.write_merge(row, row, 27, 28, self.float_format(total_general_ajuste), header_content_style)
        writer.write_merge(row, row, 29, 30, self.float_format(cat_general), header_content_style)
        writer.write_merge(row, row, 33, 34,self.float_format(total_general), header_content_style)

        
        
        
       





        wb.save(fp)
        out = base64.encodestring(fp.getvalue())
        self.write({'excel_report': out, 'name_excel': 'Libro Inventario.xls'})
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'stock.move.report.categoria',
            'name': 'Libro Inventario',
            'view_mode': 'form',
            'view_type': 'form',
            'res_id': self.id,
            'views': [(False, 'form')],
            'target': 'new',
        }
        

