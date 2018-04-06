# -*- coding: utf-8 -*-
{
    'name': "Report for Cost of Sample",

    'summary': "Report for Cost of Sample",

    'description': "Report for Cost of Sample",

    'author': "Muhammmad Kamran",
    'website': "http://www.bcube.com",

    # any module necessary for this one to work correctly
    'depends': ['base', 'report'],
    # always loaded
    'data': [
        'template.xml',
        'views/module_report.xml',
        'security/inwardpass_security.xml',
        'security/ir.model.access.csv',
    ],
    'css': ['static/src/css/report.css'],
}
