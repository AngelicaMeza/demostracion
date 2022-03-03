# Copyright 2019 Tecnativa S.L. - David Vidal
# Copyright 2020-2021 Tecnativa - Pedro M. Baeza
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "Account IMPUESTOS ADUANALES",
    "version": "13.0.2.0.1",
    "category": "Accounting",
    "author": "Tecnativa, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/server-backend",
    "license": "AGPL-3",
    "depends": ["account","locv_validation_facturacion"],
    "data": [
       
        "views/account_invoice_views.xml",
        "views/custom_tax_views.xml",
        'security/ir.model.access.csv',
        # "views/report_account_invoice.xml",
    ],
    "application": False,
    "installable": True,
}
