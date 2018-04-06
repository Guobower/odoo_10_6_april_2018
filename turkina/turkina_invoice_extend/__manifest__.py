# -*- coding: utf-8 -*-
{
    'name': "turkina_invoice_extend",

    'summary': """
        turkina_invoice_extend""",

    'description': """
        turkina_invoice_extend
    """,

    'author': "Nayyab",
    'website': "http://www.oxenlab.com",

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