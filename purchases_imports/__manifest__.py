# -*- coding: utf-8 -*-
{
	'name': "Purchases and Imports",
	'summary': """Purchases and Imports""",
	'description': """Management of import files for invoices and purchase orders""",
	'author': "IT Sales",
	'website': "https://www.itsalescorp.com/",
	'category': 'Account',
	'version': '13.0',
	'depends': ['base','account', 'purchase', 'stock_landed_costs'],
	'data': [
		'security/ir.model.access.csv',
		'views/views.xml',
		'views/account_move_view.xml',
		'views/res_partner_view.xml',
		'views/purchase_view.xml',
		'views/stock_landed_cost_view.xml',
		'views/masters.xml',
		'data/sequence.xml',
	],
}
