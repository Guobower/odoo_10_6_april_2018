# -*- coding: utf-8 -*-
{
    'name': "Appointment Letter",

    'summary': "Appointment Letter",

    'description': "Appointment Letter",

    'author': "Malik Rahman",
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
