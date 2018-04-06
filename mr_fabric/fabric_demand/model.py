# -*- coding: utf-8 -*- 
from odoo import models, fields, api
from odoo import models, fields 

class FabricDemand(models.Model): 
	_name = 'fabric.demand' 
	_description = 'Fabric Demand'
	_rec_name = 'style_name'
	style_no = fields.Many2one('style.number',string='Style No')  
	style_name = fields.Char(string='Style Name')
	buyer = fields.Many2one('res.partner', required=True, string='Buyer') 
	tree_link = fields.One2many('demand.tree','tree_link')

		# return {
		# 	'name': 'new_form',
		# 	'view_type': 'form',
		# 	'view_mode': 'form',
		# 	'res_model': 'fabric.demand',
		# 	'view_id': False,
		# 	'type': 'ir.actions.act_window',
		# }

class fabric_demand_tree(models.Model):
	"""docstring for TodoTask_tree"""
	_name='demand.tree'

	fabric_description= fields.Char(string='FABRIC DESCRIPTION')
	fabric_no = fields.Many2one('seperate.fabric',string='Fabric')
	reference=fields.Char(string=' REFERENCE')  	
	colour = fields.Char(string='Colour')
	gsm=fields.Float(string='GSM')
	quantity=fields.Float(string='Quantity')  	
	tree_link=fields.Many2one('fabric.demand')

