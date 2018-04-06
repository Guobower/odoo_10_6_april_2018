# -*- coding: utf-8 -*-
{
    'name': "OdooTec UnPaid Leaves",
    'description': """
        Calculate salary of unpaid leaves.
        display number of unpaid leaves in employee form.

 """,
    'author': "OdooTec",
    'website': "www.odootec.com",
    'category': 'Hr',
    'version': '1.0.1',
    'depends': [
        'mail', 'hr_holidays', 'hr_payroll'
    ],
    'data': [
        'views/hr_holidays_view.xml',
        # 'views/hr_employee_view.xml',
        'views/hr_contract_view.xml',
        'data/payslip_rule.xml',
        ],
    'demo': [],
    'installable': True,
    'auto_install': False,
    'application': True,
}
