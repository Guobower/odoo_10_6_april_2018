# -*- coding: utf-8 -*-
{
    'name': "OdooTec Hr Holiday Customization",
    'summary': """ Leave Management""",
    'description': """
        Automatic process for allocating leaves at the end of every month or year.
        Leave Report

 """,
    'author': "OdooTec",
    'website': "www.odootec.com",
    'category': 'HR',
    'version': '1.0.1',
    'depends': [
        'mail','hr_holidays'
    ],
    'data': [
        'views/hr_holiday_view.xml',
        'views/hr_employee_view.xml',
        # 'views/report.xml',
        # 'views/hr_holiday_report.xml',
        'wizard/holiday_analysis_view.xml',
        # 'security/ir.model.access.csv',
    ],
    'demo': [],
    'installable': True,
    'auto_install': False,
    'application': True,
}
