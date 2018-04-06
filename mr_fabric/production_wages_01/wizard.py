from odoo import models, fields, api

class MrfabricsheetForm(models.Model):
	_name = "mrfabric.sheet"

	date_from= fields.Date(string="Date From")
	date_to= fields.Date(string="Date To") 
	
	work_order = fields.Many2many('mrp.production',string="WO ")

	production = fields.Many2one('purchase.production.unit',string="Production")