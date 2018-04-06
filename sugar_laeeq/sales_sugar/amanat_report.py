from odoo import models, fields, api
from openerp.exceptions import Warning
from openerp.exceptions import ValidationError


class Amanats(models.Model):
	_name = 'amanats'

	
	customer = fields.Many2one('res.partner',string = "Party")
	mill = fields.Many2one('product.product')
	purchases = fields.Float(string = "Purchases")
	sales = fields.Float(string = "Sales")
	delivered = fields.Float(string = "Transferred")
	received = fields.Float(string = "Received")
	amanat = fields.Float(string = "Amanat")
	amanat_transfers = fields.Float(string = "Amanat Transfers")

	purchases_c = fields.Float(string = "Purchases_C" , compute = "compute_values")
	sales_c = fields.Float(string = "Sales_C", compute = "compute_values")
	delivered_c = fields.Float(string = "Transferred_C",compute = "compute_values")
	received_c = fields.Float(string = "Received_C",compute = "compute_values")
	amanat_c = fields.Float(string = "Amanat_C",compute = "compute_values")
	amanat_transfers_c = fields.Float(string = "Amanat Transfers_C",compute = "compute_values")
	gdtrf_c = fields.Float(string = "GD-TRF",compute = "compute_values")
	avtrf_c = fields.Float(string = "AV-TRF",compute = "compute_values")


	@api.one
	def compute_values(self):



		################# Purchase ############################

		purchase = 0
		purchases = self.env['purchase.sugar'].search([('mill','=',self.mill.id),('supplier','=',self.customer.id)])
		for x in purchases:
			purchase = purchase + x.qty

		purchases_open = self.env['stock.open.line'].search([('mill','=',self.mill.id),('party','=',self.customer.id),('types','=',"purchase")])
		for x in purchases_open:
			purchase = purchase + x.qty


		################# Sale ############################

		sale = 0
		sales = self.env['sales.sugar'].search([('mill','=',self.mill.id),('customer','=',self.customer.id)])
		# sale = sum(x.qty for x in sales)
		for x in sales:
			sale = sale + x.qty

		sales_open = self.env['stock.open.line'].search([('mill','=',self.mill.id),('party','=',self.customer.id),('types','=',"sale")])
		# sale = sum(x.qty for x in sales_open)
		for x in sales_open:
			sale = sale + x.qty



		################# Transfers ############################

		transfer = 0
		transfers = self.env['loading.sugar.tree'].search([('mill','=',self.mill.id),('transfer_type','=',"g2c"),\
			('party','=',self.customer.id),('transfer_from','=',"supplier")])
		
		for x in transfers:
			transfer = transfer + x.qty

		loadings = self.env['loading.adda.tree'].search([('mill','=',self.mill.id),('party','=',self.customer.id)])
		for x in loadings:
			if x.mill_loading:
				transfer = transfer + x.qty

		################# Received ############################

		receive = 0
		received = self.env['loading.sugar.tree'].search([('mill','=',self.mill.id),('transfer_type','=',"c2g"),\
			('party','=',self.customer.id)])
		for x in received:
			if x.party.mill == False:
				receive = receive + x.qty

		received_loadings = self.env['loading.adda.tree'].search([('mill','=',self.mill.id),('mill_loaded','=',self.customer.id)])
		for x in received_loadings:
			if x.mill_loading:
				receive = receive + x.qty


		################# Amanats Transfers ############################

		# amanat_transfer = 0
		amanat_rec = 0
		amanat_sent = 0
		amanat_received = self.env['loading.sugar.tree'].search([('mill','=',self.mill.id),('to','=',self.customer.id)\
			,('transfer_type','=',"c2c")])
		for x in amanat_received:
			amanat_rec = amanat_rec + x.qty
		amanat_sent_qty = self.env['loading.sugar.tree'].search([('mill','=',self.mill.id),('party','=',self.customer.id)\
			,('transfer_type','=',"c2c")])
		for x in amanat_sent_qty:
			amanat_sent = amanat_sent + x.qty
		amanat_transfers = amanat_rec - amanat_sent


		################# Available for Transfers ############################

		goods_transferred = 0
		goods_supplier = self.env['loading.sugar.tree'].search([('mill','=',self.mill.id),('transfer_type','=',"g2c"),\
			('party','=',self.customer.id),('transfer_from','=',"mill")])
		for x in goods_supplier:
			goods_transferred = goods_transferred + x.qty

		goods_transferred_mill = 0
		goods_mill = self.env['loading.sugar.tree'].search([('mill','=',self.mill.id),('transfer_type','=',"c2g"),\
			('party','=',self.customer.id)])
		for x in goods_mill:
			if x.party.mill == True:
				goods_transferred_mill = goods_transferred_mill + x.qty

		
		supplier_goods_loading = 0
		goods_supplier_loading = self.env['loading.adda.tree'].search([('mill','=',self.mill.id),('party','=',self.customer.id)])
		for x in goods_supplier_loading:
			if x.mill_loading:
				supplier_goods_loading = supplier_goods_loading + x.qty

		supplier_adda_loading = 0
		goods_adda_loading = self.env['loading.adda.tree'].search([('mill','=',self.mill.id),('mill_loaded','=',self.customer.id)])
		for x in goods_adda_loading:
			if x.mill_loading:
				supplier_adda_loading = supplier_adda_loading + x.qty



		self.purchases_c = purchase
		self.sales_c = sale
		self.delivered_c = transfer
		self.received_c = receive
		self.amanat_transfers_c = amanat_transfers
		self.amanat_c = (self.sales_c - self.purchases_c) - (self.delivered_c - self.received_c) + self.amanat_transfers_c
		self.gdtrf_c = ( goods_transferred + goods_transferred_mill ) - ( supplier_goods_loading+ supplier_adda_loading )
		self.avtrf_c = self.amanat_c - self.gdtrf_c


	@api.multi
	def update_values(self):

		self.write({
			'purchases':self.purchases_c,
			'sales':100,
			'delivered':self.delivered_c,
			'received':self.received_c,
			# 'amanat_tranfers':self.amanat_tranfers_c,
			'amanat':self.amanat_c,
			})


		return True


class AmanatsWizard(models.TransientModel):
	_name = 'amanats.wizard'

	
	@api.multi
	def update_values(self):
		print "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
		all_summaries = self.env['stock.summary.sugar']
		for x in all_summaries:
			x.for_sale = x.for_sale_c
		print "yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy"

		return {
				'type': 'ir.actions.act_window',
				'name': 'Customer Receipts',
				'res_model': 'stock.summary.sugar',
				'view_type': 'form',
				'view_mode': 'tree',
				'target' : 'current',
				# 'context': {'default_partner_id': to_open_invoices.partner_id.id,'default_receipts': True}
				}
	


