# -*- coding: utf-8 -*-
{
    'name': "invoice_sale_report",
    'summary': """
        Modulo para visualizacion de reporte de factura en Ventas.
    """,
    'author': "ITSales",
    'category': 'Accounting/Accounting',
    'version': '0.1',
    'depends': ['account', 'sale','web_dashboard'],
    'data': [
        'views/views.xml',
        'views/templates.xml',
        'report/invoice_report.xml',
    ],
}
