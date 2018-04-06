from odoo import models, fields, api
from openerp.exceptions import Warning
from openerp.exceptions import ValidationError


###################### Stock Summary #################################

class stock_summary(models.Model):
	_name = 'stock.summary.sugar'
	# _rec_name = 'ref_no'

	

	mill = fields.Many2one('product.template')
	qty	 = fields.Float(string="Total Quantity")
	supplier = fields.Many2one('res.partner',string="Party")
	purchase_id = fields.Integer()
	sold	 = fields.Float(string="Sold")
	stock_adda	 = fields.Float(string="Adda Stock")
	amanat	 = fields.Float(string="Amanat")
	for_sale	 = fields.Float(string="For Sale")
	amanat_of	 = fields.Many2one('res.partner',string="Amanat of")
	temporary	 = fields.Float()
	sales_id	 = fields.Many2one('sales.sugar')


	qty_c	 = fields.Float(string="Total Quantity C",compute = "compute_values")
	amanat_c	 = fields.Float(string="Amanat C",compute = "compute_values")
	for_sale_c	 = fields.Float(string="For Sale C",compute = "compute_values")


	@api.one
	def compute_values(self):
		# total_sale_open = 0
		# total_purchase_open = 0
		# total_purchase = 0
		# total_sales = 0
		# total_transfers = 0
		# total_loadings = 0

		# sales = self.env['sales.sugar'].search([('mill','=',self.mill.id)])
		# purchases = self.env['purchase.sugar'].search([('mill','=',self.mill.id)])
		# transfers = self.env['loading.sugar.tree'].search([('mill','=',self.mill.id),('transfer_type','=',"g2c"),('transfer_from','=',"supplier")])
		# loadings = self.env['loading.adda.tree'].search([('mill','=',self.mill.id)])
		# opening_sales = self.env['stock.open.line'].search([('mill','=',self.mill.id),('types','=',"sale")])
		# opening_purchase = self.env['stock.open.line'].search([('mill','=',self.mill.id),('types','=',"purchase")])

		
		# for x in purchases:
		# 	total_purchase = total_purchase + x.qty
		# for x in sales:
		# 	total_sales = total_sales + x.qty
		# for x in transfers:
		# 	print x.qty
		# 	total_transfers = total_transfers + x.qty
		# for x in loadings:
		# 	if x.mill_loading:
		# 		total_loadings = total_loadings + x.qty
		# for x in opening_sales:
		# 	total_sale_open = total_sale_open + x.qty
		# for x in opening_purchase:
		# 	total_purchase_open = total_purchase_open + x.qty


		# self.amanat_c = (total_sales+ total_sale_open)- (total_purchase + total_purchase_open) - total_transfers - total_loadings
		# self.for_sale_c =  (total_sales+ total_sale_open)-
		# self.qty_c = self.amanat_c + self.for_sale_c

		##########################################################################################################################

		purchase = 0
		purchases = self.env['purchase.sugar'].search([('mill','=',self.mill.id)])
		for x in purchases:
			purchase = purchase + x.qty

		purchases_open = self.env['stock.open.line'].search([('mill','=',self.mill.id),('types','=',"purchase")])
		for x in purchases_open:
			purchase = purchase + x.qty


		################# Sale ############################

		sale = 0
		sales = self.env['sales.sugar'].search([('mill','=',self.mill.id)])
		# sale = sum(x.qty for x in sales)
		for x in sales:
			sale = sale + x.qty

		sales_open = self.env['stock.open.line'].search([('mill','=',self.mill.id),('types','=',"sale")])
		# sale = sum(x.qty for x in sales_open)
		for x in sales_open:
			sale = sale + x.qty



		# ################# Transfers ############################

		transfer = 0
		# # transfers = self.env['loading.sugar.tree'].search([('mill','=',self.mill.id),('transfer_type','=',"g2c"),\
		# # 	('transfer_from','=',"supplier")])
		
		# # for x in transfers:
		# # 	transfer = transfer + x.qty

		loadings = self.env['loading.adda.tree'].search([('mill','=',self.mill.id)])
		for x in loadings:
			# if x.mill_loading:
			transfer = transfer + x.qty

		sale_return = 0
		returns = self.env['purchase.sugar'].search([('mill','=',self.mill.id),('sale_return','=',True)])
		for x in returns:
			sale_return = sale_return + x.qty


		# ################# Received ############################

		# receive = 0
		# received = self.env['loading.sugar.tree'].search([('mill','=',self.mill.id),('transfer_type','=',"c2g")])
		# for x in received:
		# 	if x.party.mill == False:
		# 		receive = receive + x.qty

		# received_loadings = self.env['loading.adda.tree'].search([('mill','=',self.mill.id)])
		# for x in received_loadings:
		# 	if x.mill_loading:
		# 		receive = receive + x.qty


		
		self.amanat_c = sale - transfer - sale_return
		self.for_sale_c = purchase - sale 
		# self.qty_c = self.amanat_c + self.for_sale_c
		




class AmanatsWizard(models.TransientModel):
	_name = 'amanats.wizard'

	
	@api.multi
	def update_values(self):
		all_summaries = self.env['stock.summary.sugar'].search([])
		for x in all_summaries:
			x.for_sale = x.for_sale_c
			x.amanat = x.amanat_c

		return {
				'type': 'ir.actions.act_window',
				'name': 'Customer Receipts',
				'res_model': 'stock.summary.sugar',
				'view_type': 'form',
				'view_mode': 'tree',
				'target' : 'current',
				# 'context': {'default_partner_id': to_open_invoices.partner_id.id,'default_receipts': True}
				}
	


