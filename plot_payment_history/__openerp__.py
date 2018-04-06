# -*- coding: utf-8 -*-
{
    'name': "crowncity report",

    'summary': "crowncity report payment",

    'description': "sale order report",

    'author': "yasir rauf",
    'website': "http://www.bcube.com",

    # any module necessary for this one to work correctly
    'depends': ['base', 'report','sale'],
    # always loaded
    'data': [
        'template.xml',
        'views/module_report.xml',
    ],
    'css': ['static/src/css/report.css'],
}
