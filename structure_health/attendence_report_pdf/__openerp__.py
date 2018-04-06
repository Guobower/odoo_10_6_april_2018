# -*- coding: utf-8 -*-
{
    'name': "Member Wise Attendence",

    'summary': "Member Wise Attendence",

    'description': "Member Wise Attendence",

    'author': "Muhammmad Kamran",
    'website': "http://www.bcube.pk",

    # any module necessary for this one to work correctly
    'depends': ['base','web','report','reg_form'],
    # always loaded
    'data': [
        'template.xml',
        'views/module_report.xml',
    ],
    'css': ['static/src/css/report.css'],
}
