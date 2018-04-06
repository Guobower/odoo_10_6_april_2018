# -*- coding: utf-8 -*-
{
    'name': "OdooTec Product Target",
    'description': """

 """,
    'author': "OdooTec",
    'website': "www.odootec.com",
    'category': 'Product',
    'version': '1.0.1',
    'depends': [
        'mail', 'product', 'sale'
    ],
    'data': [
        'views/product_view.xml',
        # 'security/ir.model.access.csv'
        ],
    'demo': [],
    'installable': True,
    'auto_install': False,
    'application': True,
}
