# -*- encoding: utf-8 -*-
{
    'name': 'Attendance Calculation',
    'category': 'HR',
    "author": "Mostafa Mohamed",
    'version': "8.0.M.M",
    'license': 'AGPL-3',
    'description': """
    """,
    'depends': ['hr_payroll'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/attendance_view.xml',
        'views/hr_employee_view.xml',
        'views/delay_view.xml',
        'wizard/import_time_view.xml',
        'wizard/clean_dummy_attendance_view.xml',
    ],
    'installable': True,
}
