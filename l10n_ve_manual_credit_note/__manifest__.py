# -*- coding: utf-8 -*-
{
    'name': "Notas de Credito Manuales",

    'description': """
        Permite la creacion de notas de credito manuales
    """,
    'author': "IT Sales",
    'website': "https://www.itsalescorp.com/en/",
    'category': 'Invoice',
    'version': '0.1',
    'depends': ['base', 'sale', 'purchase', 'account', 'mrp', 'account_debit_note', 'locv_fiscal_book'],
    'data': [
        'views/manual_credit_note.xml',
    ],
}
