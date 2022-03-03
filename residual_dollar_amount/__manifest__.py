# -*- coding: utf-8 -*-
{
    'name': "Residual amount in dollars",

    'summary': """
        Residual amount in dollars""",

    'description': """
        Calculate the residual amount of the invoice in dollars
        according to its rate as long as the invoice currency is VES
    """,

    'author': "ItSales",
    'website': "https://www.itsalescorp.com/",
    'category': 'accouny',
    'version': '13.0',
    'depends': ['base', 'account', 'invoice_sale_report'],
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
    ],
}
