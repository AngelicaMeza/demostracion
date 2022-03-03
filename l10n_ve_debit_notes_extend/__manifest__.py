{
    'name': 'add copy lines to diit and credit notes',
    'version': '1.0',
    'category': 'Sales',
    'depends': ['sale_management','account','mrp','purchase'],
    'data': [
        'views/invocie_lines.xml',
        # 'views/res_config_setting.xml',
    ],
    'license': 'OPL-1',
    'installable': True,
    'application': True,
    'auto_install': False,
}
