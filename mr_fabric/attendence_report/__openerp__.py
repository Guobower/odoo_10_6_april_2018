# -*- coding: utf-8 -*-
{
    'name': "Employee Wise Attendence",

    'summary': "Employee Wise Attendence",

    'description': "Employee Wise Attendence",

    'author': "Muhammmad Kamran",
    'website': "http://www.bcube.pk",

    # any module necessary for this one to work correctly
    'depends': ['base','web','report', 'hr','employee_mr_fabric','shift_schedule','hr_attendance'],
    # always loaded
    'data': [
        'template.xml',
        'views/module_report.xml',
    ],
    'css': ['static/src/css/report.css'],
}
