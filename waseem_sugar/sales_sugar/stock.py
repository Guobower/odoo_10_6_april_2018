# -*- coding: utf-8 -*- 
from odoo import models, fields, api
from openerp.exceptions import Warning
from openerp.exceptions import ValidationError







	

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
		for x in self.line_ids:
			description = x.name


		self.label = description



class loading_sugar(models.Model): 
	_name 		 = 'loading.sugar' 
	_description = 'Loading'
	# _rec_name = 'order_no'

	total		 = fields.Float(string="Total")
	date 		 =  fields.Date(required=True,string ="Work Date",default=fields.Date.context_today)

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



		


	@api.model
	def create(self, vals):
		# vals['order_no'] = self.env['ir.sequence'].next_by_code('purchase.sugar')
		new_record = super(loading_sugar_tree, self).create(vals)
		if new_record.transfer_type == "c2g":
			remaining_transfers = self.env['remaining.transfers'].search([('supplier','=',new_record.party.id),('mill','=',new_record.mill.id)])
			for x in remaining_transfers:
				x.received = x.received + new_record.qty
				x.remaining = x.purchased - x.received

			adda_wise = self.env['adda.wise'].search([('adda','=',new_record.adda.id),('mill','=',new_record.mill.id)])
			if not adda_wise:
				create_entry = adda_wise.create({
					'adda':new_record.adda.id,
					'mill':new_record.mill.id,
					'stock_in':new_record.qty,
					'remaining':new_record.qty,
					})
			else:
				adda_wise.stock_in = adda_wise.stock_in + new_record.qty
				adda_wise.remaining = adda_wise.stock_in - adda_wise.stock_out

			amanats = self.env['amanats'].search([('mill','=',new_record.mill.id),('customer','=',new_record.party.id)])
			if not amanats:
				create_amanat = amanats.create({
					'customer': new_record.party.id,
					'mill':new_record.mill.id,
					})
			amanats = self.env['amanats'].search([('mill','=',new_record.mill.id),('customer','=',new_record.party.id)])	
			# for x in amanats:
			# 	if x.mill.mill == False:
			# 		x.received = x.received + new_record.qty
			# 		x.amanat = (x.sales - x.purchases) - (x.delivered - x.received) + x.amanat_transfers

			# relevant_summary = self.env['stock.summary.sugar'].search([('mill','=',new_record.mill.id)])
			# for x in relevant_summary:
			# 	x.qty = x.qty + new_record.qty
			# 	x.amanat = x.amanat + new_record.qty
			# 	x.for_sale = x.qty - x.amanat	

		elif new_record.transfer_type == "g2c":
			adda_wise = self.env['adda.wise'].search([('adda','=',new_record.adda.id),('mill','=',new_record.mill.id)])
			for x in adda_wise:
				x.stock_out = x.stock_out + new_record.qty
				x.remaining = x.stock_in - x.stock_out


			mill_wise = self.env['mill.wise'].search([('brand','=',new_record.mill.id)])
			for x in mill_wise:
				x.assigned = x.assigned + new_record.qty
				x.amanat = x.amanat - new_record.qty

			
			if new_record.party.mill == False:
				amanats = self.env['amanats'].search([('mill','=',new_record.mill.id),('customer','=',new_record.party.id)])
				if not amanats:
					create_amanat = amanats.create({
						'customer': new_record.party.id,
						'mill':new_record.mill.id,
						})
				amanats = self.env['amanats'].search([('mill','=',new_record.mill.id),('customer','=',new_record.party.id)])
				for x in amanats:

					x.delivered = x.delivered + new_record.qty
					x.amanat = (x.sales - x.purchases) - (x.delivered - x.received) + x.amanat_transfers

			relevant_summary = self.env['stock.summary.sugar'].search([('mill','=',new_record.mill.id)])
			for x in relevant_summary:
				if new_record.transfer_from == "supplier":
					x.qty = x.qty - new_record.qty
					x.amanat = x.amanat - new_record.qty
					x.for_sale = x.qty - x.amanat	
				# if new_record.transfer_type == "c2g":
				# 	x.stock_adda = x.stock_adda + new_record.qty
					# x.stock_adda = x.stock_adda - new_record.qty




		elif new_record.transfer_type == "g2g":
			adda_wise_from = self.env['adda.wise'].search([('adda','=',new_record.adda.id),('mill','=',new_record.mill.id)])
			adda_wise_to = self.env['adda.wise'].search([('adda','=',new_record.adda_transferred.id),('mill','=',new_record.mill.id)])
			if not adda_wise_from:
				create_entry = adda_wise_from.create({
					'adda':new_record.adda.id,
					'mill':new_record.mill.id,
					'stock_out':new_record.qty,
					'remaining':(new_record.qty)*-1,
					})
			else:
				adda_wise_from.stock_out = adda_wise_from.stock_out + new_record.qty
				adda_wise_from.remaining = adda_wise_from.stock_in - adda_wise_from.stock_out


			if not adda_wise_to:
				create_entry = adda_wise_to.create({
					'adda':new_record.adda_transferred.id,
					'mill':new_record.mill.id,
					'stock_in':new_record.qty,
					'remaining':new_record.qty,
					})
			else:
				adda_wise_to.stock_in = adda_wise_to.stock_in + new_record.qty
				adda_wise_to.remaining = adda_wise_to.stock_in - adda_wise_to.stock_out

		elif new_record.transfer_type == "c2c":
			party_from = self.env['amanats'].search([('mill','=',new_record.mill.id),('customer','=',new_record.party.id)])
			party_to = self.env['amanats'].search([('mill','=',new_record.mill.id),('customer','=',new_record.to.id)])
			if not party_from:
				create_amanat = amanats.create({
					'customer': new_record.party.id,
					'mill':new_record.mill.id,
					})
			party_from = self.env['amanats'].search([('mill','=',new_record.mill.id),('customer','=',new_record.party.id)])
			for x in party_from:
				x.amanat_transfers = x.amanat_transfers - new_record.qty


			party_to = self.env['amanats'].search([('mill','=',new_record.mill.id),('customer','=',new_record.to.id)])

			if not party_to:
				create_amanat = party_to.create({
					'customer': new_record.to.id,
					'mill':new_record.mill.id,
					})
			party_to = self.env['amanats'].search([('mill','=',new_record.mill.id),('customer','=',new_record.to.id)])
			for x in party_to:
				x.amanat_transfers = x.amanat_transfers + new_record.qty









		# relevant_summary = self.env['stock.summary.sugar'].search([('mill','=',new_record.mill.id)])
		# for x in relevant_summary:
		# 	# if new_record.transfer_type == "c2g":
		# 	# 	x.stock_adda = x.stock_adda + new_record.qty
		# 	if new_record.transfer_type == "g2c":
		# 		# x.stock_adda = x.stock_adda - new_record.qty
		# 		x.qty = x.qty - new_record.qty
		# 		x.amanat = x.amanat - new_record.qty
		# 		x.for_sale = x.qty - x.amanat	



		
		return new_record

	@api.multi
	def write(self, vals):
		before_write = self.qty

		if self.transfer_type == "c2g":
			remaining_transfers = self.env['remaining.transfers'].search([('supplier','=',self.party.id),('mill','=',self.mill.id)])
			for x in remaining_transfers:
				x.received = x.received - self.qty

			adda_wise = self.env['adda.wise'].search([('adda','=',self.adda.id),('mill','=',self.mill.id)])
			for x in adda_wise:
				x.stock_in = x.stock_in - self.qty

			
			
			amanats = self.env['amanats'].search([('mill','=',new_record.mill.id),('customer','=',new_record.party.id)])
			for x in amanats:
				x.received = x.received - self.qty


			# relevant_summary = self.env['stock.summary.sugar'].search([('mill','=',self.mill.id)])
			# for x in relevant_summary:
			# 	x.qty = x.qty - self.qty
			# 	x.amanat = x.amanat - self.qty
				




		elif self.transfer_type == "g2c":
			adda_wise = self.env['adda.wise'].search([('adda','=',self.adda.id),('mill','=',self.mill.id)])
			for x in adda_wise:
				x.stock_out = x.stock_out - self.qty

			mill_wise = self.env['mill.wise'].search([('brand','=',self.mill.id)])
			for x in mill_wise:
				x.assigned = x.assigned - self.qty
				x.amanat = x.amanat + self.qty

			

			if self.party.mill == False:	
				amanats = self.env['amanats'].search([('mill','=',self.mill.id),('customer','=',self.party.id)])

				for x in amanats:
					x.delivered = x.delivered -self.qty

			relevant_summary = self.env['stock.summary.sugar'].search([('mill','=',self.mill.id)])
			for x in relevant_summary:
				if self.transfer_from == "supplier":
					x.qty = x.qty + self.qty
					x.amanat = x.amanat + self.qty
					x.for_sale = x.qty - x.amanat


		elif self.transfer_type == "g2g":
			adda_wise_from = self.env['adda.wise'].search([('adda','=',self.adda.id),('mill','=',self.mill.id)])
			adda_wise_to = self.env['adda.wise'].search([('adda','=',self.adda_transferred.id),('mill','=',self.mill.id)])
			for x in adda_wise_from:
				x.stock_out = x.stock_out - self.qty
			for x in adda_wise_to:
				x.stock_in = x.stock_in - self.qty

		elif self.transfer_type == "c2c":
			party_from = self.env['amanats'].search([('mill','=',self.mill.id),('customer','=',self.party.id)])
			party_to = self.env['amanats'].search([('mill','=',self.mill.id),('customer','=',self.to.id)])
			for x in party_from:
				x.amanat_transfers = x.amanat_transfers + self.qty

			for x in party_to:
				x.amanat_transfers = x.amanat_transfers - self.qty




		super(loading_sugar_tree, self).write(vals)
		after_write = self.qty
		difference =  after_write - before_write


		if self.transfer_type == "c2g":
			remaining_transfers = self.env['remaining.transfers'].search([('supplier','=',self.party.id),('mill','=',self.mill.id)])
			for x in remaining_transfers:
				x.received = x.received + self.qty
				x.remaining = x.purchased - x.received


			adda_wise = self.env['adda.wise'].search([('adda','=',self.adda.id),('mill','=',self.mill.id)])
			for x in adda_wise:
				x.stock_in = x.stock_in + self.qty
				x.remaining = x.stock_in - x.stock_out

			# relevant_summary = self.env['stock.summary.sugar'].search([('mill','=',self.mill.id)])
			# for x in relevant_summary:
			# 	x.qty = x.qty + self.qty
			# 	x.amanat = x.amanat + self.qty
			# 	x.for_sale = x.qty - x.amanat



			amanats = self.env['amanats'].search([('mill','=',self.mill.id),('customer','=',self.party.id)])
			if not amants:
				create_amanat = amanats.create({
						'customer': self.party.id,
						'mill':self.mill.id,
						})

			amanats = self.env['amanats'].search([('mill','=',self.mill.id),('customer','=',self.party.id)])
			for x in amanats:
				x.received = x.received + self.qty
				x.amanat = (x.sales - x.purchases) - (x.delivered - x.received) + x.amanat_transfers


		elif self.transfer_type == "g2c":
			adda_wise = self.env['adda.wise'].search([('adda','=',self.adda.id),('mill','=',self.mill.id)])
			for x in adda_wise:
				x.stock_out = x.stock_out + self.qty
				x.remaining = x.stock_in - x.stock_out


			mill_wise = self.env['mill.wise'].search([('brand','=',self.mill.id)])
			for x in mill_wise:
				x.assigned = x.assigned + self.qty
				x.amanat = x.amanat - self.qty

			amanats = self.env['amanats'].search([('mill','=',self.mill.id),('customer','=',self.party.id)])
			if not amanats:
				create_amanat = amanats.create({
						'customer': self.party.id,
						'mill':self.mill.id,
						})

			if self.party.mill == False:
				amanats = self.env['amanats'].search([('mill','=',self.mill.id),('customer','=',self.party.id)])
				for x in amanats:
					x.delivered = x.delivered + self.qty
					x.amanat = (x.sales - x.purchases) - (x.delivered - x.received) + x.amanat_transfers

			relevant_summary = self.env['stock.summary.sugar'].search([('mill','=',self.mill.id)])
			for x in relevant_summary:
				if self.transfer_from == "supplier":
					x.qty = x.qty - self.qty
					x.amanat = x.amanat - self.qty
					x.for_sale = x.qty - x.amanat


		elif self.transfer_type == "g2g":
			adda_wise_from = self.env['adda.wise'].search([('adda','=',self.adda.id),('mill','=',self.mill.id)])
			adda_wise_to = self.env['adda.wise'].search([('adda','=',self.adda_transferred.id),('mill','=',self.mill.id)])
			for x in adda_wise_from:
				x.stock_out = x.stock_out + self.qty
				x.remaining = x.stock_in - x.stock_out
			for x in adda_wise_to:
				x.stock_in = x.stock_in + self.qty
				x.remaining = x.stock_in - x.stock_out

		elif self.transfer_type == "c2c":
			party_from = self.env['amanats'].search([('mill','=',self.mill.id),('customer','=',self.party.id)])
			party_to = self.env['amanats'].search([('mill','=',self.mill.id),('customer','=',self.to.id)])
			if not party_from:
				create_amanat = amanats.create({
					'customer': self.party.id,
					'mill':self.mill.id,
					})
			party_from = self.env['amanats'].search([('mill','=',self.mill.id),('customer','=',self.party.id)])
			for x in party_from:
				x.amanat_transfers = x.amanat_transfers - self.qty

			if not party_to:
				create_amanat = amanats.create({
					'customer': self.to.id,
					'mill':self.mill.id,
					})
			party_to = self.env['amanats'].search([('mill','=',self.mill.id),('customer','=',self.to.id)])
			for x in party_to:
				x.amanat_transfers = x.amanat_transfers + self.qty










		return True

	@api.multi
	def unlink(self):


		if self.transfer_type == "c2g":
			remaining_transfers = self.env['remaining.transfers'].search([('supplier','=',self.party.id),('mill','=',self.mill.id)])
			for x in remaining_transfers:
				x.received = x.received - self.qty
				x.remaining = x.purchased - x.received

			adda_wise = self.env['adda.wise'].search([('adda','=',self.adda.id),('mill','=',self.mill.id)])
			for x in adda_wise:
				x.stock_in = x.stock_in - self.qty
				x.remaining = x.stock_in - x.stock_out

			amanats = self.env['amanats'].search([('mill','=',self.mill.id),('customer','=',self.supplier.id)])
			for x in amanats:
				x.received = x.received - self.qty
				x.amanat = (x.sales - x.purchases) - (x.delivered - x.received) + x.amanat_transfers


			# relevant_summary = self.env['stock.summary.sugar'].search([('mill','=',self.mill.id)])
			# for x in relevant_summary:
			# 	x.qty = x.qty - self.qty
			# 	x.amanat = x.amanat - self.qty
			# 	x.for_sale = x.qty - x.amanat

		elif self.transfer_type == "g2c":
			adda_wise = self.env['adda.wise'].search([('adda','=',self.adda.id),('mill','=',self.mill.id)])
			for x in adda_wise:
				x.stock_out = x.stock_out - self.qty
				x.remaining = x.stock_in - x.stock_out

			mill_wise = self.env['mill.wise'].search([('brand','=',self.mill.id)])
			for x in mill_wise:
				x.assigned = x.assigned - self.qty
				x.amanat = x.amanat + self.qty


			if self.party.mill == False:
				amanats = self.env['amanats'].search([('mill','=',self.mill.id),('customer','=',self.customer.id)])
				for x in amanats:
					x.delivered = x.delivered - self.qty
					x.amanat = (x.sales - x.purchases) - (x.delivered - x.received) + x.amanat_transfers

			relevant_summary = self.env['stock.summary.sugar'].search([('mill','=',self.mill.id)])
			for x in relevant_summary:
				if self.transfer_from == "supplier":
					x.qty = x.qty + self.qty
					x.amanat = x.amanat + self.qty
					x.for_sale = x.qty - x.amanat

		elif self.transfer_type == "g2g":
			adda_wise_from = self.env['adda.wise'].search([('adda','=',self.adda.id),('mill','=',self.mill.id)])
			adda_wise_to = self.env['adda.wise'].search([('adda','=',self.adda_transferred.id),('mill','=',self.mill.id)])
			for x in adda_wise_from:
				x.stock_out = x.stock_out - self.qty
				x.remaining = x.stock_in - x.stock_out
			for x in adda_wise_to:
				x.stock_in = x.stock_in - self.qty
				x.remaining = x.stock_in - x.stock_out


		elif self.transfer_type == "c2c":
			party_from = self.env['amanats'].search([('mill','=',new_record.mill.id),('customer','=',new_record.party.id)])
			party_to = self.env['amanats'].search([('mill','=',new_record.mill.id),('customer','=',new_record.to.id)])
			for x in party_from:
				x.amanat_transfers = x.amanat_transfers + self.qty

			for x in party_to:
				x.amanat_transfers = x.amanat_transfers - self.qty




		super(loading_sugar_tree, self).unlink()

		return True




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
	total_received_c = fields.Float(string = "Total Received",compute = "compute_values")
	total_transfers_c = fields.Float(string = "Total Transfers",compute = "compute_values")
	gdtrf_c = fields.Float(string = "GD-TRF",compute = "compute_values")
	avtrf_c = fields.Float(string = "AV-TRF",compute = "compute_values")
	purchase_rem_t_c = fields.Float(string = "PRT",compute = "compute_values")
	sale_rem_t_c = fields.Float(string = "SRT",compute = "compute_values")


	@api.one
	def compute_values(self):
		purchase = 0
		sale = 0
		transfer = 0
		receive = 0
		amanat_transfer = 0

		purchases = self.env['purchase.sugar'].search([('mill','=',self.mill.id),('supplier','=',self.customer.id)])
		for x in purchases:
			purchase = purchase + x.qty

		purchases_open = self.env['stock.open.line'].search([('mill','=',self.mill.id),('party','=',self.customer.id),('types','=',"purchase")])
		for x in purchases_open:
			purchase = purchase + x.qty

		sales = self.env['sales.sugar'].search([('mill','=',self.mill.id),('customer','=',self.customer.id)])
		for x in sales:
			sale = sale + x.qty

		sales_open = self.env['stock.open.line'].search([('mill','=',self.mill.id),('party','=',self.customer.id),('types','=',"sale")])
		for x in sales_open:
			sale = sale + x.qty




		# transfers = self.env['loading.sugar.tree'].search([('mill','=',self.mill.id),('transfer_type','=',"g2c"),\
		# 	('party','=',self.customer.id),('transfer_from','=',"supplier")])
		# for x in transfers:
		# 	transfer = transfer + x.qty

		loadings = self.env['loading.adda.tree'].search([('mill','=',self.mill.id),('party','=',self.customer.id)])
		for x in loadings:
			transfer = transfer + x.qty

		received = self.env['loading.sugar.tree'].search([('mill','=',self.mill.id),('transfer_type','=',"c2g"),\
			('party','=',self.customer.id)])
		for x in received:
			if x.party.mill == False:
				receive = receive + x.qty

		received_loadings = self.env['loading.adda.tree'].search([('mill','=',self.mill.id),('mill_loaded','=',self.customer.id)])
		for x in received_loadings:
			if x.mill_loading:
				receive = receive + x.qty

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


		total_received_goods = 0
		received_total_goods = self.env['loading.sugar.tree'].search([('mill','=',self.mill.id),('transfer_type','=',"c2g"),\
			('party','=',self.customer.id)])
		for x in received_total_goods:
			
			total_received_goods = total_received_goods + x.qty

		total_transfers_goods = 0
		total_transfers_goods_records = self.env['loading.sugar.tree'].search([('mill','=',self.mill.id),('transfer_type','=',"g2c"),\
			('party','=',self.customer.id)])
		for x in total_transfers_goods_records:
			total_transfers_goods = total_transfers_goods + x.qty



		self.purchases_c = purchase
		self.sales_c = sale
		self.delivered_c = transfer
		self.received_c = receive
		self.amanat_transfers_c = amanat_transfers
		self.amanat_c = (self.sales_c - self.purchases_c) - (self.delivered_c - self.received_c) + self.amanat_transfers_c
		self.gdtrf_c = (goods_transferred + goods_transferred_mill) - (supplier_goods_loading+ supplier_adda_loading)
		self.avtrf_c = self.amanat_c - self.gdtrf_c
		self.total_received_c = total_received_goods
		self.total_transfers_c = total_transfers_goods
		self.purchase_rem_t_c = self.purchases_c - self.total_received_c
		self.sale_rem_t_c = self.sales_c - self.total_transfers_c


class LoadingAdda(models.Model):
	_name = 'loading.adda'

	
	date = fields.Date(string ="Work Date", required = True  ,default=fields.Date.context_today)

	loading_lines = fields.One2many('loading.adda.tree','loading_id')
	mill_loading = fields.One2many('loading.adda.tree','mill_loading')

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


	@api.model
	def create(self, vals):
		# vals['order_no'] = self.env['ir.sequence'].next_by_code('purchase.sugar')
		new_record = super(LoadingAddaTree, self).create(vals)



		if new_record.mill_loading: 
			mill_wise = self.env['mill.wise'].search([('brand','=',new_record.mill.id),('mill','=',new_record.mill_loaded.id)])
			if not mill_wise:
				raise ValidationError('Associate brand with the mill')
			else:
				for x in mill_wise:
					x.loaded = x.loaded + new_record.qty
					x.remaining = x.total_purchase - x.loaded


			amanats = self.env['amanats'].search([('mill','=',new_record.mill.id),('customer','=',new_record.party.id)])
			for x in amanats:
				x.delivered = x.delivered + new_record.qty
				x.amanat = (x.sales - x.purchases) - (x.delivered - x.received) + x.amanat_transfers


			relevant_summary = self.env['stock.summary.sugar'].search([('mill','=',new_record.mill.id)])
			for x in relevant_summary:
				x.qty = x.qty - new_record.qty
				x.amanat = x.amanat - new_record.qty
				x.for_sale = x.qty - x.amanat

		
		return new_record

	@api.multi
	def write(self, vals):


		if self.mill_loading:
			mill_wise = self.env['mill.wise'].search([('brand','=',self.mill.id),('mill','=',self.mill_loaded.id)])
			for x in mill_wise:
				x.loaded = x.loaded - self.qty
				x.remaining = x.total_purchase - x.loaded


			amanats = self.env['amanats'].search([('mill','=',self.mill.id),('customer','=',self.party.id)])
			for x in amanats:
				x.delivered = x.delivered - self.qty
				x.amanat = (x.sales - x.purchases) - (x.delivered - x.received) + x.amanat_transfers


			relevant_summary = self.env['stock.summary.sugar'].search([('mill','=',self.mill.id)])
			for x in relevant_summary:
				x.qty = x.qty + self.qty
				x.amanat = x.amanat + self.qty
				x.for_sale = x.qty - x.amanat


		super(LoadingAddaTree, self).write(vals)


		if self.mill_loading:
			amanats = self.env['amanats'].search([('mill','=',self.mill.id),('customer','=',self.party.id)])
			for x in amanats:
				x.delivered = x.delivered + self.qty
				x.amanat = (x.sales - x.purchases) - (x.delivered - x.received) + x.amanat_transfers
		

			mill_wise = self.env['mill.wise'].search([('brand','=',self.mill.id),('mill','=',self.mill_loaded.id)])
			if not mill_wise:
				raise ValidationError('Associate brand with the mill')
			else:
				for x in mill_wise:
					x.loaded = x.loaded + self.qty
					x.remaining = x.total_purchase - x.loaded

			relevant_summary = self.env['stock.summary.sugar'].search([('mill','=',self.mill.id)])
			for x in relevant_summary:
				x.qty = x.qty - self.qty
				x.amanat = x.amanat - self.qty
				x.for_sale = x.qty - x.amanat


		return True

	@api.multi
	def unlink(self):

		if self.mill_loading:
			amanats = self.env['amanats'].search([('mill','=',self.mill.id),('customer','=',self.party.id)])
			for x in amanats:
				x.delivered = x.delivered - self.qty
				x.amanat = (x.sales - x.purchases) - (x.delivered - x.received) + x.amanat_transfers

			mill_wise = self.env['mill.wise'].search([('brand','=',self.mill.id),('mill','=',self.mill_loaded.id)])
			for x in mill_wise:
				x.loaded = x.loaded - self.qty
				x.remaining = x.total_purchase - x.loaded


			relevant_summary = self.env['stock.summary.sugar'].search([('mill','=',self.mill.id)])
			for x in relevant_summary:
				x.qty = x.qty + self.qty
				x.amanat = x.amanat + self.qty
				x.for_sale = x.qty - x.amanat




		super(LoadingAddaTree, self).unlink()

		return True



	



class CreateMill(models.Model): 
	_inherit		 = 'res.partner'

	mill = fields.Boolean()
	brands = fields.Many2many('product.product')
	comm_rate = fields.Float(string = "Commission Rate")
	rec = fields.Float(string = "Rec",compute = "compute_net")
	pay = fields.Float(string = "Pay",compute = "compute_net")
	net = fields.Float(string = "Net",compute = "compute_net")


	@api.one
	def compute_net(self):
		entries = self.env['account.move.line'].search([('partner_id.id','=',self.id),'|',('account_id.user_type_id','=','Receivable'),('account_id.user_type_id','=','Payable')])


		debits = 0
		credits = 0
		for x in entries:
			debits = debits + x.debit
			credits = credits + x.credit
		self.rec = debits
		self.pay = credits
		self.net = self.rec - self.pay

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

		return True

	