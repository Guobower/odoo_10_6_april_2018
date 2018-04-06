# -*- coding: utf-8 -*-
{
    'name': "demand_report",

    'summary': "demand_report",

    'description': "demand_report",

    'author': "Rana Rizwan",
    'website': "http://www.bcube.com",

    # any module necessary for this one to work correctly
    'depends': ['base', 'report','purchase','fabric_demand'],
    # always loaded
    'data': [
        'template.xml',
        'views/module_report.xml',
    ],
    'css': ['static/src/css/report.css'],
}
