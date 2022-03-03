# -*- coding: utf-8 -*-
{
    'name': "Only Self Warehouse",

    'summary': """
        Resticciones para la visibilidad de almacenes y ubicaciones
        """,

    'description': """
        Asignación de almacenes por usuario, solo permitiendo la visibilidad de los asignados
        Restricción de localizaciones por usuario asignado, , solo permitiendo la visibilidad de las asignadas
    """,

    'author': "ItSales",
    'website': "http://www.itsalescorp.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Stock',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'stock'],

    # always loaded
    'data': [
        'security/rules.xml',
        'views/views.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
