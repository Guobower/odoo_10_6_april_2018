# -*- coding: utf-8 -*-
{
    'name': "Inward Gatepass",

    'summary': "Inward Gatepass",

    'description': "Inward Gatepass",

    'author': "Rana Rizwan",
    'website': "http://www.bcube.pk",

    # any module necessary for this one to work correctly
    'depends': ['base', 'report', 'hr','mrp','purchase_mr_fabric'],
    # always loaded
    'data': [
        'template.xml',
        'views/module_report.xml',
    ],
    'css': ['static/src/css/report.css'],
}
