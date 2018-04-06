{
    'name': 'OdooTec MRP Main Product',
    'version': '1.0',
    'category': 'MRP',
    'sequence': 10,
    'summary': "Categorize the manufacturing product into base and sub product.",
    'description':"Categorize the manufacturing product into base and sub product",
    'author': 'OdooTec',
    'depends': ['mrp'],
    'data': [
        'views/product_template.xml',
        'views/work_order_view.xml'

       ],
    'installable': True,
    'auto_install': False,
}


