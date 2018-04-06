# -*- coding: utf-8 -*- 
from odoo import models, fields, api
from openerp.exceptions import Warning
from openerp.exceptions import ValidationError


class loading_sugar(models.Model): 
	_name 		 = 'loading.sugar' 
	_description = 'Loading'
	# _rec_name = 'order_no'

	total		 = fields.Float(string="Total")
	date 		 =  fields.Date(required=True,string ="Work Date",default=fields.Date.context_today)

	brand = fields.Many2one('product.template')
	party = fields.Many2one('res.partner')
	adda = fields.Many2one('adda')


	c2g  = fields.One2many('loading.sugar.tree','c2g')
	g2c  = fields.One2many('loading.sugar.tree','g2c')
	c2c  = fields.One2many('loading.sugar.tree','c2c')
	g2g  = fields.One2many('loading.sugar.tree','g2g')
	
	@api.onchange('loading_tree')
	def get_total(self):
		total_qty = 0
		for x in self.loading_tree:
			
			total_qty = total_qty + x.qty
		self.total = total_qty

	@api.one
	@api.constrains('date')
	def single_date(self):

		dates = self.env['loading.sugar'].search([('date','=',self.date),('id','!=',self.id)])
		if dates:
			raise ValidationError('Date Already Exists')


	@api.onchange('date')
	def change_date(self):
		for x in self.c2g:
			x.date = self.date
		for x in self.g2c:
			x.date = self.date
		for x in self.c2c:
			x.date = self.date
		for x in self.g2g:
			x.date = self.date

###################### Sugar Loading Tree #################################

class loading_sugar_tree(models.Model): 
	_name 		 = 'loading.sugar.tree' 
	# _description = 'Loading'
	# _rec_name = 'order_no'
	transfer_type = fields.Selection([
		('c2g', 'Client to Goods'),
		('g2c', 'Goods to Client'),
		('c2c', 'Client to Client'),
		('g2g', 'Goods to Goods'),
		],string = "Transfer Type")
	party = fields.Many2one('res.partner')
	to = fields.Many2one('res.partner')
	customer	 = fields.Many2one('res.partner')
	supplier     = fields.Many2one('res.partner')
	mill		 = fields.Many2one('product.template')
	qty			 = fields.Float(string="Quantity")
	adda		 = fields.Many2one('adda')
	for_sale		 = fields.Float(string = "For Sale",compute = "get_for_sale", store = True)
	adda_transferred		 = fields.Many2one('adda',string ="Adda Transferred")
	date 		 = fields.Date(required=True)
	memo = fields.Char(string = "Memo")
	transfer_from = fields.Selection([('mill', 'Mill'), ('supplier', 'Supplier')],default = "supplier" )
	auto_sale_id = fields.Many2one('sale.booking.treeview')
	c2g   = fields.Many2one('loading.sugar')
	g2c   = fields.Many2one('loading.sugar')
	c2c   = fields.Many2one('loading.sugar')
	g2g   = fields.Many2one('loading.sugar')


	@api.onchange('mill')
	def get_id(self):
		if self.c2g:
			self.transfer_type = "c2g"
			date = self.c2g.date
		elif self.g2c:
			self.transfer_type = "g2c"
			date = self.g2c.date
		elif self.c2c:
			self.transfer_type = "c2c"
			date = self.c2c.date
		elif self.g2g:
			self.transfer_type = "g2g"
			date = self.g2g.date

		self.date = date

	@api.one
	@api.depends('mill','party')
	def get_for_sale(self):
		if self.g2c or self.c2c or self.c2g:
			for_sale_amount = self.env['amanats'].search([('customer','=',self.party.id),('mill','=',self.mill.id)])
			self.for_sale = for_sale_amount.amanat


	@api.onchange('c2g','g2c')
	def get_to_from(self):
		if self.g2c:
			if not self.mill:
				self.mill = self.g2c.brand.id
			if not self.party:	
				self.party = self.g2c.party.id
			if not self.adda:	
				self.adda = self.g2c.adda.id
		if self.c2g:
			if not self.mill:
				self.mill = self.c2g.brand.id
			if not self.party:	
				self.party = self.c2g.party.id
			if not self.adda:	
				self.adda = self.c2g.adda.id



		


	@api.model
	def create(self, vals):
		# vals['order_no'] = self.env['ir.sequence'].next_by_code('purchase.sugar')
		new_record = super(loading_sugar_tree, self).create(vals)
		if new_record.transfer_type == "c2g" or new_record.transfer_type == "g2c":
			# mill = new_record.mill.id
			# customer = new_record.party.id


			amanats = self.env['amanats'].search([('mill','=',new_record.mill.id),('customer','=',new_record.party.id)])
			if not amanats:
				create_amanat = amanats.create({
					'customer': new_record.party.id,
					'mill':new_record.mill.id,
					})
			amanats = self.env['amanats'].search([('mill','=',new_record.mill.id),('customer','=',new_record.party.id)])	
			amanats.update_values()
	

		# elif new_record.transfer_type == "g2c":

		# 	amanats = self.env['amanats'].search([('mill','=',new_record.mill.id),('customer','=',new_record.party.id)])
		# 	if not amanats:
		# 		create_amanat = amanats.create({
		# 			'customer': new_record.party.id,
		# 			'mill':new_record.mill.id,
		# 			})
		# 	amanats = self.env['amanats'].search([('mill','=',new_record.mill.id),('customer','=',new_record.party.id)])
		# 	amanats.update_values()


		elif new_record.transfer_type == "c2c":
			party_from = self.env['amanats'].search([('mill','=',new_record.mill.id),('customer','=',new_record.party.id)])

			if not party_from:
				create_amanat = party_from.create({
					'customer': new_record.party.id,
					'mill':new_record.mill.id,
					})
			party_from = self.env['amanats'].search([('mill','=',new_record.mill.id),('customer','=',new_record.party.id)])
			party_from.update_values()



			party_to = self.env['amanats'].search([('mill','=',new_record.mill.id),('customer','=',new_record.to.id)])

			if not party_to:
				create_amanat = party_to.create({
					'customer': new_record.to.id,
					'mill':new_record.mill.id,
					})
			party_to = self.env['amanats'].search([('mill','=',new_record.mill.id),('customer','=',new_record.to.id)])
			party_to.update_values()

		
		return new_record

	@api.multi
	def write(self, vals):

		if self.transfer_type == "c2g" or self.transfer_type == "g2c":
			mill = self.mill.id
			party = self.supplier.id

		# elif self.transfer_type == "g2c":
		# 	mill = self.mill.id
		# 	party = self.customer.id


		elif self.transfer_type == "c2c":
			party_f = self.party.id
			party_t = self.to.id
			mill = self.mill.id


		super(loading_sugar_tree, self).write(vals)


		if self.transfer_type == "c2g" or self.transfer_type == "g2c":

			amanats_before = self.env['amanats'].search([('mill','=',mill),('customer','=',party)])
			if amanats_before:
				amanats_before.update_values()

		elif self.transfer_type == "c2c":

			party_from_before = self.env['amanats'].search([('mill','=',mill),('customer','=',party_f)])
			party_to_before = self.env['amanats'].search([('mill','=',mill),('customer','=',party_t)])

			if party_from_before:
				party_from_before.update_values()
				party_to_before.update_values()


		if self.transfer_type == "c2g" or self.transfer_type == "g2c":

			amanats = self.env['amanats'].search([('mill','=',self.mill.id),('customer','=',self.party.id)])
			if not amanats:
				create_amanat = amanats.create({
						'customer': self.party.id,
						'mill':self.mill.id,
						})
			amanats = self.env['amanats'].search([('mill','=',self.mill.id),('customer','=',self.party.id)])
			amanats.update_values()


		# elif self.transfer_type == "g2c":


		# 	amanats = self.env['amanats'].search([('mill','=',self.mill.id),('customer','=',self.party.id)])
		# 	if not amanats:
		# 		create_amanat = amanats.create({
		# 				'customer': self.party.id,
		# 				'mill':self.mill.id,
		# 				})
		# 	amanats = self.env['amanats'].search([('mill','=',self.mill.id),('customer','=',self.party.id)])
		# 	amanats.update_values()


		elif self.transfer_type == "c2c":
			party_from = self.env['amanats'].search([('mill','=',self.mill.id),('customer','=',self.party.id)])
			party_to = self.env['amanats'].search([('mill','=',self.mill.id),('customer','=',self.to.id)])
			if not party_from:
				create_amanat = party_from.create({
					'customer': self.party.id,
					'mill':self.mill.id,
					})
			party_from = self.env['amanats'].search([('mill','=',self.mill.id),('customer','=',self.party.id)])
			party_from.update_values()


			if not party_to:
				create_amanat = party_to.create({
					'customer': self.to.id,
					'mill':self.mill.id,
					})
			party_to = self.env['amanats'].search([('mill','=',self.mill.id),('customer','=',self.to.id)])
			party_to.update_values()


		return True

	@api.multi
	def unlink(self):


		if self.transfer_type == "c2g" or self.transfer_type == "g2c":

			mill = self.mill.id
			party = self.supplier.id

		# elif self.transfer_type == "g2c":
		# 	mill = self.mill.id
		# 	party = self.customer.id

		elif self.transfer_type == "c2c":
			party_f = self.party.id
			party_t = self.to.id
			mill = self.mill.id


			party_from = self.env['amanats'].search([('mill','=',mill),('customer','=',party_f)])
			party_to = self.env['amanats'].search([('mill','=',mill),('customer','=',party_t)])
			if party_from:
				party_from.update_values()
				party_to.update_values()

		amanats = self.env['amanats'].search([('mill','=',mill),('customer','=',party)])
		if amanats:
			amanats.update_values()
			
		super(loading_sugar_tree, self).unlink()


		return True



class LoadingAdda(models.Model):
	_name = 'loading.adda'

	
	date = fields.Date(string ="Work Date", required = True  ,default=fields.Date.context_today)

	loading_lines = fields.One2many('loading.adda.tree','loading_id')
	mill_loading = fields.One2many('loading.adda.tree','mill_loading')

	adda = fields.Many2one('adda')
	mill = fields.Many2one('product.product',string = "Brand")
	party = fields.Many2one('res.partner')
	mill_loaded = fields.Many2one('res.partner')





	@api.one
	@api.constrains('date')
	def single_date(self):

		dates = self.env['loading.adda'].search([('date','=',self.date),('id','!=',self.id)])
		if dates:
			raise ValidationError('Date Already Exists')


	@api.onchange('date')
	def change_date(self):
		for x in self.loading_lines:
			x.date = self.date
		for x in self.mill_loading:
			x.date = self.date


class LoadingAddaTree(models.Model):
	_name = 'loading.adda.tree'

	adda = fields.Many2one('adda')
	mill = fields.Many2one('product.product',string = "Brand")
	party = fields.Many2one('res.partner')
	mill_loaded = fields.Many2one('res.partner')
	qty = fields.Float(string = "Quantity")
	destination = fields.Char(string = "Destination")
	vehicle_no = fields.Char(string = "Vehicle No")
	billty_no = fields.Char(string = "Billty No")
	date = fields.Date()


	loading_id = fields.Many2one('loading.adda')
	mill_loading = fields.Many2one('loading.adda')


	@api.onchange('loading_id','mill_loading')
	def get_to_from(self):
		if self.loading_id:
			if not self.adda:
				self.adda = self.loading_id.adda.id
			if not self.mill:	
				self.mill = self.loading_id.mill.id
			if not self.party:	
				self.party = self.loading_id.party.id
		if self.mill_loading:
			if not self.adda:
				self.adda = self.mill_loading.adda.id
			if not self.mill:	
				self.mill = self.mill_loading.mill.id
			if not self.party:	
				self.party = self.mill_loading.party.id
			if not self.mill_loaded:	
				self.mill_loaded = self.mill_loading.mill_loaded.id




	@api.onchange('adda','party')
	def get_id(self):
		if self.loading_id:
			self.date = self.loading_id.date
		elif self.mill_loading:
			self.date = self.mill_loading.date



	@api.model
	def create(self, vals):
		# vals['order_no'] = self.env['ir.sequence'].next_by_code('purchase.sugar')
		new_record = super(LoadingAddaTree, self).create(vals)


		amanats = self.env['amanats'].search([('mill','=',new_record.mill.id),('customer','=',new_record.party.id)])
		if not amanats:
			create_amanat = amanats.create({
						'customer': new_record.party.id,
						'mill':new_record.mill.id,
						})
		amanats = self.env['amanats'].search([('mill','=',new_record.mill.id),('customer','=',new_record.party.id)])
		amanats.update_values()

		amanats_mill = self.env['amanats'].search([('mill','=',new_record.mill.id),('customer','=',new_record.mill_loaded.id)])
		if not amanats_mill:
			if new_record.mill_loaded:
				create_amanat = amanats_mill.create({
							'customer': new_record.mill_loaded.id,
							'mill':new_record.mill.id,
							})
		amanats_mill = self.env['amanats'].search([('mill','=',new_record.mill.id),('customer','=',new_record.mill_loaded.id)])
		amanats_mill.update_values()


		
		return new_record

	@api.multi
	def write(self, vals):


		mill = self.mill.id
		customer = self.party.id
		mill_loaded = self.mill_loaded.id



		super(LoadingAddaTree, self).write(vals)


		amanats_before = self.env['amanats'].search([('mill','=',mill),('customer','=',customer)])
		amanats_mill_before = self.env['amanats'].search([('mill','=',mill),('customer','=',mill_loaded)])
		if amanats_before:
			amanats_before.update_values()
		if amanats_mill_before:
			amanats_mill_before.update_values()


		amanats = self.env['amanats'].search([('mill','=',self.mill.id),('customer','=',self.party.id)])
		if not amanats:
			create_amanat = amanats.create({
						'customer': self.party.id,
						'mill':self.mill.id,
						})
		amanats = self.env['amanats'].search([('mill','=',self.mill.id),('customer','=',self.party.id)])
		amanats.update_values()

		amanats_mill = self.env['amanats'].search([('mill','=',self.mill.id),('customer','=',self.mill_loaded.id)])
		if not amanats_mill:
			if self.mill_loaded:
				create_amanat = amanats_mill.create({
							'customer': self.mill_loaded.id,
							'mill':self.mill.id,
							})
		amanats_mill = self.env['amanats'].search([('mill','=',self.mill.id),('customer','=',self.mill_loaded.id)])
		amanats_mill.update_values()





		return True

	@api.multi
	def unlink(self):


		mill = self.mill.id
		customer = self.customer.id
		mill_loaded =self.mill_loaded.id




		super(LoadingAddaTree, self).unlink()

		amanats_before = self.env['amanats'].search([('mill','=',mill),('customer','=',customer)])
		amanats_mill_before = self.env['amanats'].search([('mill','=',mill),('customer','=',mill_loaded)])
		if amanats_before:
			amanats_before.update_values()
		if amanats_mill_before:
			amanats_mill_before.update_values()

		return True



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
		total_sale_open = 0
		total_purchase_open = 0
		total_purchase = 0
		total_sales = 0
		total_transfers = 0
		total_loadings = 0

		sales = self.env['sales.sugar'].search([('mill','=',self.mill.id)])
		purchases = self.env['purchase.sugar'].search([('mill','=',self.mill.id)])
		transfers = self.env['loading.sugar.tree'].search([('mill','=',self.mill.id),('transfer_type','=',"g2c"),('transfer_from','=',"supplier")])
		loadings = self.env['loading.adda.tree'].search([('mill','=',self.mill.id)])
		opening_sales = self.env['stock.open.line'].search([('mill','=',self.mill.id),('types','=',"sale")])
		opening_purchase = self.env['stock.open.line'].search([('mill','=',self.mill.id),('types','=',"purchase")])

		
		for x in purchases:
			total_purchase = total_purchase + x.qty
		for x in sales:
			total_sales = total_sales + x.qty
		for x in transfers:
			print x.qty
			total_transfers = total_transfers + x.qty
		for x in loadings:
			if x.mill_loading:
				total_loadings = total_loadings + x.qty
		for x in opening_sales:
			total_sale_open = total_sale_open + x.qty
		for x in opening_purchase:
			total_purchase_open = total_purchase_open + x.qty


		self.qty_c = total_purchase + total_purchase_open- total_transfers - total_loadings
		self.amanat_c = total_sales+ total_sale_open - total_transfers - total_loadings
		self.for_sale_c = self.qty_c - self.amanat_c

	@api.multi
	def test_act(self):
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
				'target' : 'new',
				# 'context': {'default_partner_id': to_open_invoices.partner_id.id,'default_receipts': True}
				}








class create_mill_stock_history(models.Model): 
	_inherit		 = 'product.template'



	@api.model
	def create(self, vals):
		new_record = super(create_mill_stock_history, self).create(vals)

		create_mill = self.env['stock.summary.sugar'].create({
					'mill':new_record.id,
					})


		return new_record



class Adda(models.Model):
	_name = 'adda'
	# _rec_name = 'ref_no'

	

	name = fields.Char()
	city	 = fields.Char()
	address = fields.Char()
	phone = fields.Char()


class RemainingTransfers(models.Model):
	_name = 'remaining.transfers'

	

	supplier = fields.Many2one('res.partner')
	mill = fields.Many2one('product.product')
	purchased = fields.Float()
	received = fields.Float()
	remaining = fields.Float()


class AddaWise(models.Model):
	_name = 'adda.wise'

	

	adda = fields.Many2one('adda')
	mill = fields.Many2one('product.product')
	stock_in = fields.Float(string = "Stock In")
	stock_out = fields.Float(string = "Stock Out")
	remaining = fields.Float()

class MillWise(models.Model):
	_name = 'mill.wise'

	

	mill = fields.Many2one('res.partner')
	brand = fields.Many2one('product.product')
	total_purchase = fields.Float(string = "Total Purchases")
	total_sale = fields.Float(string = "Total Sales")
	amanat = fields.Float()
	assigned = fields.Float()
	loaded = fields.Float()
	remaining = fields.Float()
	total_purchase_c = fields.Float(string = "Total Purchases C",compute = "compute_values")
	loaded_c = fields.Float(string = "Loaded C",compute = "compute_values")
	remaining_c = fields.Float(string = "Remaining C",compute = "compute_values")




	@api.one
	def compute_values(self):
		total_purchase = 0
		total_loadings = 0
		total_opening = 0

		purchases = self.env['purchase.sugar'].search([('mill','=',self.brand.id),('supplier','=',self.mill.id)])
		loadings = self.env['loading.adda.tree'].search([('mill','=',self.brand.id)])
		opening = self.env['stock.open.line'].search([('mill','=',self.brand.id),('party','=',self.mill.id),('types','=',"purchase")])
		
		for x in purchases:
			total_purchase = total_purchase + x.qty
		
		for x in loadings:
			if x.mill_loading:
				total_loadings = total_loadings + x.qty

		for x in opening:
			total_opening = total_opening + x.qty

		self.total_purchase_c = total_purchase + total_opening
		self.loaded_c = total_loadings
		self.remaining_c = self.total_purchase_c - self.loaded_c



	



class CreateMill(models.Model): 
	_inherit		 = 'res.partner'

	mill = fields.Boolean()
	brands = fields.Many2many('product.product')
	comm_rate = fields.Float(string = "Commission Rate")
	rec = fields.Float(string = "Rec",compute = "compute_net")
	pay = fields.Float(string = "Pay",compute = "compute_net")
	net = fields.Float(string = "Net",compute = "compute_net")
	actual_balance = fields.Float(string = "Actual Balance",compute = "compute_net")
	entry_level = fields.Float(string = "Entry Level",compute = "compute_net")
	clearance_level = fields.Float(string = "Clearance Level",compute = "compute_net")


	@api.one
	def compute_net(self):
		entries = self.env['account.move.line'].search([('partner_id.id','=',self.id),'|',('account_id.user_type_id','=','Receivable'),\
			('account_id.user_type_id','=','Payable')])

		
		receipts = 0
		payments = 0
		funds_flow_entry = self.env['funds.flow.tree'].search([('stages','=',"entry")])
		for x in funds_flow_entry:
			if x.type_transaction == "jv" and x.customer.id == self.id:
				receipts = receipts + x.amount
			if x.type_transaction == "jv" and x.supplier.id == self.id:
				payments = payments + x.amount
			if x.type_transaction == "bp" and x.party.id == self.id:
				payments = payments + x.amount
			if x.type_transaction == "br" and x.party.id == self.id:
				receipts = receipts + x.amount

		receipts_clearance = 0
		payments_clearance = 0
		funds_flow_clearance = self.env['funds.flow.tree'].search([('stages','=',"clearing")])
		for x in funds_flow_clearance:
			if x.type_transaction == "jv" and x.customer.id == self.id:
				receipts_clearance = receipts_clearance + x.amount
			if x.type_transaction == "jv" and x.supplier.id == self.id:
				payments_clearance = payments_clearance + x.amount
			if x.type_transaction == "bp" and x.party.id == self.id:
				payments_clearance = payments_clearance + x.amount
			if x.type_transaction == "br" and x.party.id == self.id:
				receipts_clearance = receipts_clearance + x.amount



		debits = 0
		credits = 0
		debits_actual = 0
		credits_actual = 0
		for x in entries:
			debits = debits + x.debit
			credits = credits + x.credit
			if x.move_id.state == "posted":
				debits_actual = debits_actual + x.debit
				credits_actual = credits_actual + x.credit
		self.rec = debits
		self.pay = credits
		self.net = self.rec - self.pay
		self.actual_balance = debits_actual - credits_actual
		self.entry_level = receipts - payments
		self.clearance_level = receipts_clearance - payments_clearance

	@api.onchange('net')
	def get_net(self):
		self.comm_rate = self.net



	@api.model
	def create(self, vals):
		new_record = super(CreateMill, self).create(vals)

		summary = self.env['summary.entry'].search([])
		create_journal_entry = summary.create({
			'customer': new_record.id,
			})
			
		summary_clearance = self.env['summary.clearance'].search([])
		create_journal_entry = summary_clearance.create({
			'customer': new_record.id,
			})

		if new_record.mill == True:
			for x in new_record.brands:
				create_mill = self.env['mill.wise'].create({
							'mill':new_record.id,
							'brand':x.id,
							})




		return new_record

	@api.multi
	def write(self, vals):

		super(CreateMill, self).write(vals)

		if self.mill == True:
			for x in self.brands:
				mill = self.env['mill.wise'].search([('mill','=',self.id),('brand','=',x.id)])
				if not mill:
					create_mill = self.env['mill.wise'].create({
								'mill':self.id,
								'brand':x.id,
								})

		amanats = self.env['amanats'].search([('customer','=',self.id)])
		for x in amanats:
			x.update_values()


		return True



###################### Overwrite function for creating journal entry #################################

class AccountMoveRemoveValidation(models.Model):
	_inherit = "account.move"

	customer_payment_id = fields.Integer()
	supplier_payment_id = fields.Integer()
	inter_payment_id = fields.Integer()
	funds_flow_id = fields.Many2one('funds.flow.tree')
	label = fields.Char(compute="compute_label")

	@api.multi
	def assert_balanced(self):
		if not self.ids:
			return True
		prec = self.env['decimal.precision'].precision_get('Account')

		self._cr.execute("""\
			SELECT      move_id
			FROM        account_move_line
			WHERE       move_id in %s
			GROUP BY    move_id
			HAVING      abs(sum(debit) - sum(credit)) > %s
			""", (tuple(self.ids), 10 ** (-max(5, prec))))
		# if len(self._cr.fetchall()) != 0:
		#     raise UserError(_("Cannot create unbalanced journal entry."))
		return True

	@api.one
	def compute_label(self):
		# pass
		description=0
		for x in self.line_ids:
			description = x.name


		self.label = description

	