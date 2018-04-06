# -*- coding: utf-8 -*-
{
    'name': "Omer Fiaz - Daily Shipment Report",

    'summary': "Omer Fiaz - Daily Shipment Report",

    'description': "Omer Fiaz - Daily Shipment Report",

    'author': "Muhammad Kamran",
    'website': "http://www.bcube.com",

    # any module necessary for this one to work correctly
    'depends': ['base','report'],
    # always loaded
    'data': [
        'template.xml',
        'views/module_report.xml',
    ],
    'css': ['static/src/css/report.css'],
}
