# -*- coding: utf-8 -*-
{
    'name': "leave_encashment",

    'summary': """
        Nayyab""",

    'description': """
        leave_encashment
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','employee_mr_fabric'],

    # always loaded
    'data': [
        'templates.xml',
    ],

}