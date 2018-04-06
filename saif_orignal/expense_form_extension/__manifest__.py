# -*- coding: utf-8 -*-
{
    'name': "expense_form_extension",

    'summary': """
        Changes in Expenses Form""",

    'description': """
        Changes in Expenses Form
    """,

    'author': "Awais",
    'website': "http://ecube.com",

    'category': 'Uncategorized',
    'version': '0.1',

    'depends': ['base','hr_expense','account','hr_contract'],

    # always loaded
    'data': [
        'views/views.xml',
    ],
}
