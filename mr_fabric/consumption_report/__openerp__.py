# -*- coding: utf-8 -*-
{
    'name': "Consumption Report",

    'summary': "Consumption Report",

    'description': "Consumption Report",

    'author': "Rana Rizwan",
    'website': "http://www.bcube.com",

    # any module necessary for this one to work correctly
    'depends': ['base', 'report','purchase'],
    # always loaded
    'data': [
        'template.xml',
        'views/module_report.xml',
    ],
    'css': ['static/src/css/report.css'],
}
