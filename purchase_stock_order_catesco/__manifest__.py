# -*- coding: utf-8 -*-
{
    'name': "Campos de orden de compra Catesco",

    'summary': """Modulo que remueve los tipos de credito a la hora de crear una factura rectificativa""",

    'description': """
    """,
    'version': '1.0',
    'author': 'IT Sales',
    'category': 'invoice',

    # any module necessary for this one to work correctly
    'depends': ['base', 'stock','purchase', 'stock_account'],

    # always loaded
    'data': [
        "views/purchase_inherit.xml",
    ],

}
