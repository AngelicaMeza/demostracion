# -*- coding: utf-8 -*-
{
    'name': "purchase_hide_edit_button_in_view_purchase_requisition_form",

    'summary': """
        Ocultar boton editar en la vista formulario de Acuerdos de Compra""",

    'description': """
        Luego que un Acuerdo de compra queda en estado Confirmado, el botón Editar debe quedar deshabilitado para todos los usuarios, menos el administrador.
    """,

    'author': "ITSALES",
    'website': "https://www.itsalescorp.com/",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'purchase',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'purchase_requisition' ],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        #'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        #'demo/demo.xml',
    ],
}
