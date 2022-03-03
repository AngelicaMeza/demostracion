# -*- coding: utf-8 -*-
{
    'name': "MRP_extend_export_excel",
    'summary': """Export mrp report in excel""",
    'description': """Export mrp report in excel""",
    'author': "IT Sales",
    'website': "https://www.itsalescorp.com/",
    'category': 'account',
    'version': '13.0',
    'depends': ['base', 'stock','mrp'],
    'data': [
        'views/assets.xml',
        'reports/report.xml',
        'wizard/statement_wizard_view.xml',
       

    ],
     'qweb': ['static/src/xml/mrp.xml'],
}
