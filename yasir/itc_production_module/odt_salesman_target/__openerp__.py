# -*- coding: utf-8 -*-
{
    'name': "OdooTec SalesMan Target",
    'description': """

    Using this module we can set target for money sales man.

 """,
    'author': "OdooTec",
    'website': "www.odootec.com",
    'category': 'Product',
    'version': '1.0.1',
    'depends': [
        'mail', 'product', 'sale', 'account', 'account_voucher', 'odt_mrp_base_product'
    ],
    'data': [
        # 'security/ir.model.access.csv',
        'views/sales_man_view.xml',
        'views/sales_man_target_view.xml'
        ],
    'demo': [],
    'installable': True,
    'auto_install': False,
    'application': True,
}
