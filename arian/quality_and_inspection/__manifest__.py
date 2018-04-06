{
	'name': 'Quality and Inspection', 
	'description': 'Manage Quality and Inspection Documents', 
	'author': 'Muhammad Kamran', 
	'depends': ['sale','commercial_packing_list'], 
	'application': True,
	'data': [
		'views/template.xml',
	 	'security/inwardpass_security.xml',
	 	'security/ir.model.access.csv',
	 	],
}