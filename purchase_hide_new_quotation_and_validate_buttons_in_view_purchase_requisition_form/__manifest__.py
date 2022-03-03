# -*- coding: utf-8 -*-
{
    'name': "purchase_hide_new_quotation_and_validate_buttons_in_view_purchase_requisition_form",

    'summary': """
        Ocultar los botones 'Nuevo presupuesto' y 'Validar' en Acuerdos de compra""",

    'description': """
        Se ocultan los botones 'Nuevo presupuesto' y 'Validar' para todos los usuarios excepto para los que pertenecen al grupo
        * Puede validar acuerdos de compra 
    """,

    'author': "ITSALES",
    'website': "https://www.itsalescorp.com/",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'purchase',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'purchase_requisition'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        #'views/templates.xml',
        'security/groups.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        #'demo/demo.xml',
    ],
}
