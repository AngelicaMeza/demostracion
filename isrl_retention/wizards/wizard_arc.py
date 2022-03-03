from datetime import datetime, timedelta
from odoo.tools.misc import DEFAULT_SERVER_DATE_FORMAT

from odoo import models, fields, api, _, tools
from odoo.exceptions import UserError
import openerp.addons.decimal_precision as dp
import logging

import io
from io import BytesIO
from datetime import date
import xlsxwriter
import shutil
import base64
import csv
import xlwt
import xml.etree.ElementTree as ET

_logger = logging.getLogger(__name__)

class WiizarXml(models.TransientModel):
    _name = "account.arc.wizard"

    name  = fields.Many2one(comodel_name='res.partner', string='Empresa')
    date_from = fields.Date(string='Date From', default=lambda *a:datetime(date.today().year, 1, 1, 00, 00))
    date_today = fields.Date(string='Date Today', default=lambda *a:datetime.now().strftime('%Y-%m-%d'))
    date_to = fields.Date('Date To', default=lambda *a:(datetime(date.today().year, 12, 31, 00, 00)))
    isrl_id = fields.Many2many(comodel_name='islr.wh.doc', string='ISLR')
    company_id = fields.Many2one('res.company', string='Company', required=True,default=lambda self: self.env.company)

    def get_isrl_id(self):
        self.isrl_id = self.env['islr.wh.doc'].search([
            ('date_uid','>=',self.date_from),
            ('date_uid','<=',self.date_to),
            ('partner_id','=',self.name.id),
            ('state','=','done'),
            ('type','in',('in_invoice','in_refund','in_receipt'))
            ],order="date_uid asc")

    def print_pdf(self):
        self.get_isrl_id()
        return {'type': 'ir.actions.report','report_name': 'isrl_retention.report_arc','report_type':"qweb-pdf" }
    

    def separate_months(self):

        montlydata = []
        # for islrs in self.isrl_id:
        #     if islrs.date_ret.month not in months:
        #         months.append(islrs.date_ret.month)
        months=[1,2,3,4,5,6,7,8,9,10,11,12]
        
        for month in months:
            current = self.isrl_id.filtered(lambda r: r.date_ret.month == month)
            montlydata.append(current)  
        
        montlydata


        return montlydata

    def get_month(self, month):
        months = {
            0 : 'Enero',
            1 : 'Febrero',
            2 : 'Marzo',
            3 : 'Abril',
            4 :'Mayo',
            5 : 'Junio',
            6 : 'Julio',
            7 : 'Agosto',
            8 : 'Septiembre',
            9 : 'Octubre',
            10 : 'Noviembre',
            11 : 'Diciembre',


        }
        return months[month]