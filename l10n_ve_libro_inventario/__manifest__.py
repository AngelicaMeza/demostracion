
# -*- coding: utf-8 -*-
{
    'name': "Libro de Inventario",

    'summary': """
        Libro de Inventario
        """,

    'description': """
        Libro de Inventario
    """,
    'author': "IT Sales",
    'website': "https://www.itsalescorp.com/en/",

    'category': 'Contabilidad',
    'version': '0.1',

    # any module necessary for this one to work correctly
     "depends" : ['base','account','stock','jp_kardex_valorizado'],

    # always loaded
    'data': [
        'wizards/reporte_product.xml',
        'wizards/reporte_categoria.xml',
        'report/listado_movimiento_inventario.xml',
        'report/inventory_valuation_detail_template.xml',
        'security/ir.model.access.csv',
        ],  
    # only loaded in demonstration mode
    'demo': [
    ],
    'installable': True,
}

