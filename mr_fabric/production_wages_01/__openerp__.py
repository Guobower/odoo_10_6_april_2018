# -*- coding: utf-8 -*-
{
    'name': "Mr Fabric Sheet",

    'summary': "Mr Fabric Sheet",

    'description': "Mr Fabric Sheet",

    'author': "Rana Rizwan",
    'website': "http://www.bcube.pk",

    # any module necessary for this one to work correctly
    'depends': ['base', 'report','purchase','mrp','purchase_mr_fabric'],
    # always loaded
    'data': [
        'template.xml',
        'views/module_report.xml',
    ],
    'css': ['static/src/css/report.css'],
}
