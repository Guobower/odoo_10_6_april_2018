# -*- coding: utf-8 -*-
{
    'name': "Attendence Module Extension",

    'summary': "Attendence Module Extension",

    'description': "Attendence Module Extension",

    'author': "Ehtisham Faisal",
    'website': "http://www.oxenlab.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','hr'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/templates.xml',
    ],
}