# -*- coding: utf-8 -*-
{
    'name': "RST Performa Invoice",

    'summary': "RST Performa Invoice",

    'description': "RST Performa Invoice",

    'author': "Muhammmad Kamran",
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
