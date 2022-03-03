# -*- coding: utf-8 -*-
{
    'name': "Grupos tipo de operacion inventario",
    'summary': """Grupos tipo de operacion en transferencias inventario""",
    'description': """ Modelo que extiende la vista tree de inventario para limitar la 
    visibilidad de los tipos de operacion para usuarios que estén en grupos determinados""",
    'author': "IT Sales",
    'website': "www.itsalescorp.com",
    'category': 'Uncategorized',
    'version': '0.1',
    'depends': ['base','stock'],
    'data': [
        'security/security.xml',
        'views/inherit_vpicktree_view.xml',
    ],
}
