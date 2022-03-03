# -*- coding: utf-8 -*-
{
    'name': "Remover tipos de creditos",

    'summary': """Modulo que remueve los tipos de credito a la hora de crear una factura rectificativa""",

    'description': """
    """,
    'version': '1.0',
    'author': 'IT Sales',
    'category': 'invoice',

    # any module necessary for this one to work correctly
    'depends': ['base', 'account'],

    # always loaded
    'data': [
        "wizard/change_credit_note_wizard.xml",
    ],

}
