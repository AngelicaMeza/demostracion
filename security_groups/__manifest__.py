# -*- coding: utf-8 -*-
{
    'name': "security_groups",
    'summary': """ Security Groups, access rigths and record rules""",
    'description': """""",
    'author': "IT Sales",
    'website': "http://www.itsalescorp.com",
    'category': 'Uncategorized',
    'version': '0.1',
    'depends': ['base','stock','product','mrp'],
    'data': [
        'security/category_rules.xml',
        'views/views.xml',
        'security/groups.xml',
        'security/ir.model.access.csv'
    ],
}
