# -*- coding: utf-8 -*-
{
    'name': "Mrp Operation Tasks",
    'description': """
        Create Tasks in Routing Operations
 """,
    'author': "OdooTec",
    'website': "www.odootec.com",
    'category': 'Accounting',
    'version': '1.0.1',
    'depends': [
        'mail', 'mrp_operations_extension',
    ],
    'data': [
        'views/mrp_routing_view.xml',
        'views/mrp_workcenter_view.xml',
        'views/project_task_view.xml',
        'security/ir.model.access.csv'
        ],
    'demo': [],
    'installable': True,
    'auto_install': False,
    'application': True,
}
