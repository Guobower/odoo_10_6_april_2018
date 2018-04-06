# -*- coding: utf-8 -*-
{
    'name': "Vat Invoice Turkina",

    'summary': "Vat Invoice",

    'description': "Vat Invoice",

    'author': "Muhammad Awais",
    'website': "http://www.bcube.pk",

    # any module necessary for this one to work correctly
    'depends': ['base', 'report','turkina_invoice_extend','account','account_accountant'],
    # always loaded
    'data': [
        'template.xml',
        'views/module_report.xml',
    ],
    'css': ['static/src/css/report.css'],
}
