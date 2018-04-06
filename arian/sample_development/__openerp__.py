# -*- coding: utf-8 -*-
{
    'name': "Sample Development Report",

    'summary': "Sample Development Report",

    'description': "Sample Development Report",

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
