# -*- coding: utf-8 -*-
{
    'name': "Payment History for Crown  City",

    'summary': "Payment History for Crown  City",

    'description': "Payment History for Crown  City",

    'author': "Muhammmad Kamran",
    'website': "http://www.bcube.com",

    # any module necessary for this one to work correctly
    'depends': ['base', 'report'],
    # always loaded
    'data': [
        'template.xml',
        'views/module_report.xml',
    ],
    'css': ['static/src/css/report.css'],
}
