# -*- coding: utf-8 -*-
{
    'name': 'OdooTec Purchase Discount Value',
    'version': '1.5',
    'category': 'Purchase',
    'summary': 'Discount Value in purchase',
    'sequence': 30,
    'author': 'OdooTec',
    'description': """
    This module will add a new field discount value.It is used for assign discount
      """,
    'depends': ['purchase_discount'
                ],
    'data': [
        'views/purchase_discount_view.xml'
    ],
    'installable': True,
    'application': True
}
