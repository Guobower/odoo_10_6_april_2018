# -*- coding: utf-8 -*-
{
    'name': "OdooTec Duration",
    'description': """
    create new field for duration between delivery and confirm

 """,
    'author': "OdooTec",
    'website': "www.odootec.com",
    'category': 'Sale',
    'version': '1.0.1',
    'depends': [
        'mail', 'product', 'sale_delivery_date'
    ],
    'data': [
        'views/sale_order_view.xml',
        'views/purchase_order_view.xml'
        ],
    'demo': [],
    'installable': True,
    'auto_install': False,
    'application': True,
}
