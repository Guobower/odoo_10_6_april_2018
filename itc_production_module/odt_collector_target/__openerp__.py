# -*- coding: utf-8 -*-
{
    'name': "OdooTec Collector Target",
    'description': """

    Using this module we can set target for money collector.

 """,
    'author': "OdooTec",
    'website': "www.odootec.com",
    'category': 'Product',
    'version': '1.0.1',
    'depends': [
        'mail', 'product', 'sale', 'account', 'account_voucher'
    ],
    'data': [
        # 'security/ir.model.access.csv',
        'views/account_voucher_view.xml',
        'views/collector_view.xml'
        ],
    'demo': [],
    'installable': True,
    'auto_install': False,
    'application': True,
}
