# -*- coding: utf-8 -*-
{
    'name': "catesco_locv_fixes",
    'summary': """Catesco Vzla location fixes""",
    'description': """Catesco fixes to the Venezuelan location""",
    'author': "ItSales",
    'website': "https://www.itsalescorp.com/",
    'category': 'account',
    'version': '13.0',
    'depends': ['base', 'locv_fiscal_book', 'locv_withholding_iva', 'locv_withholding_islr'],
    'data': [
        'views/views.xml',
    ],
}
