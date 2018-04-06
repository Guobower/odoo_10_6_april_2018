# -*- coding: utf-8 -*-
{
    'name': "vat_invoice_extend",

    'summary': """
        vat_invoice_extend""",

    'description': """
        vat_invoice_extend
    """,

    'author': "Muhammad Awais",
    'website': "http://www.bcube.pk.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','account','sale'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
    ],
}