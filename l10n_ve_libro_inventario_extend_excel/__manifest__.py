
# -*- coding: utf-8 -*-
{
    'name': "Libro de Inventario extencion Excel",

    'summary': """
        Libro de Inventario extencion Excel
        """,

    'description': """
        Libro de Inventario extencion Excel
    """,
    'author': "IT Sales",
    'website': "https://www.itsalescorp.com/en/",

    'category': 'Contabilidad',
    'version': '0.1',

    # any module necessary for this one to work correctly
     "depends" : ['base','account','stock','jp_kardex_valorizado','l10n_ve_libro_inventario'],

    # always loaded
    'data': [
        'wizards/reporte_categoria.xml',
        
        ],  
    # only loaded in demonstration mode
    'demo': [
    ],
    'installable': True,
}

