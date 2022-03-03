# -*- coding: utf-8 -*-
{
    'name': "Modificacion de Mesa de Ayuda Catesco ",

    'summary': """Cambios al modulo de mesa de ayudo para Catesco""",

    'description': """
    """,
    'version': '1.0',
    'author': 'IT Sales',
    'category': 'invoice',

    # any module necessary for this one to work correctly
    'depends': ['base', 'helpdesk'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        "views/help_table.xml",
    ],

}
