# -*- coding: utf-8 -*-
{
    'name': "locv_move_report",
    'summary': """ Reporte de Pago para Asientos de anticipos y retenciones de IVA """,
    'author': "Oscar Llovera",
    'category': 'Uncategorized',
    'version': '0.1',
    'depends': ['locv_account_advance_payment', 'locv_withholding_iva'],
    'data': [
        'report/move_payment.xml',
        'views/views.xml',
    ],
}
