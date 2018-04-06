# -*- coding: utf-8 -*- 
from odoo import models, fields, api
from openerp.exceptions import ValidationError


####################   Sales Booking Main Form #######################################

class sale_booking(models.Model): 
	_name 		 = 'sales.booking' 
	_description = 'Booking Module in Sales'
	# _rec_name = 'date_string'
	
	date 		 =  fields.Date(required=True, default=fields.Date.context_today)
	total 		 =	fields.Float(string="Total Amount", compute='_getTotalAmount')
	total_qty 	 =	fields.Float(string="Total Quantity", compute='_getTotalqty')
	avg			 =	fields.Float(string="Average", compute='_getTotalavg')
	user_id      = fields.Many2one('res.users',default=lambda self: self.env.user)
	name = fields.Char()


	order_line	 =	fields.One2many('sale.booking.treeview','sales_booking_id')

	@api.one
	def _getTotalAmount(self):
		self.total = sum(line.total for line in self.order_line)


	@api.one
	def _getTotalqty(self):
		self.qty = sum(line.qty for line in self.order_line)

	@api.one
	def _getTotalavg(self):
		if(self.total_qty>0):
			self.avg = self.total / self.total_qty


	@api.onchange('order_line','date')
	def get_total(self):
		total = 0
		total_qty = 0
		for x in self.order_line:
			total = total + x.total
			total_qty = total_qty + x.qty
		self.total = total
		self.total_qty = total_qty
		if(self.total_qty>0):
			self.avg = self.total / self.total_qty
		self.name = str(self.user_id.name) + " / "+ str(self.date)

	@api.model
	def create(self, vals):

		new_record = super(sale_booking, self).create(vals)

		
		for x in new_record.order_line:
			sales = self.env['sales.sugar'].search([('booking_id','=',x.id)])
			if not sales:
				generate_sales_form = sales.create({
					'customer': x.customer.id,
					'mill':x.mill.id,
					'rate':x.rate,
					'qty':x.qty,
					'total':x.total,
					'booking_id':x.id,
					'date':new_record.date,
					'remaining':x.qty
					})
			else:
				sales.customer = x.customer.id
				sales.mill_id =x.mill.id
				sales.rate =x.rate
				sales.qty = x.qty
				sales.total =x.total
				sales.date =new_record.date

		return new_record

	@api.multi
	def write(self, vals):
		super(sale_booking, self).write(vals)

		for x in self.order_line:
			sales = self.env['sales.sugar'].search([('booking_id','=',x.id)])
			if not sales:
				generate_sales_form = sales.create({
					'customer': x.customer.id,
					'mill':x.mill.id,
					'rate':x.rate,
					'qty':x.qty,
					'total':x.total,
					'booking_id':x.id,
					'date':self.date,
					'remaining':x.qty
					})
			else:
				sales.customer = x.customer.id
				sales.mill_id =x.mill.id
				sales.rate =x.rate
				sales.qty = x.qty
				sales.total =x.total
				sales.date =self.date
				sales.remaining = sales.qty - sales.delivered

		return True




class sale_booking_treeview(models.Model):

	_name 		 = 'sale.booking.treeview'
	_description = 'Tree View of sales booking'

	customer	 = fields.Many2one('res.partner')
	mill		 = fields.Many2one('product.template')
	qty			 = fields.Float(string="Quantity")
	rate		 = fields.Float(string="Rate")
	total		 = fields.Float(string="Total")
	sales_booking_id = fields.Many2one('sales.booking')



	@api.onchange('qty','rate')
	def get_total(self):
		new=0
		over_qty=0
		purchase_qty = self.env['purchase.sugar'].search([('mill','=',self.mill.id)])
		for x in purchase_qty:
			new = new + x.qty
		sales_qty = self.env['sales.booking'].search([])
		for x in sales_qty:
			for y in x.order_line:
				if y.mill.id == self.mill.id:
					over_qty = over_qty + y.qty
		over_qty = over_qty + self.qty	
		self.total = self.qty * self.rate	
		if over_qty > new:
			diff_over_qty=over_qty-new
			self.total = self.qty * self.rate
			return {'value':{},'warning':{'title':
					'warning','message':"Sorry You have not sufficient stock You require %s You sale oversale Stock %s" %(new,diff_over_qty)}}

		else:
			self.total = self.qty * self.rate




		# for x in purchase_qty:
		# 	new = new + x.qty
		# if self.qty>new:
		# 	self.total = self.qty * self.rate
		# 	over_qty=self.qty-new
		# 	msg = "Sory You Have Not Sufficient Stock You Require %s You sale oversale Stock %s" %(new,over_qty)
		# 	raise ValidationError(msg) 

		# else:
		# 	self.total = self.qty * self.rate

	@api.multi
	def unlink(self):
		super(sale_booking_treeview, self).unlink()

		sales_delivery = self.env['sales.sugar'].search([('booking_id','=',self.id)])
		sales_delivery.unlink()

		return True

###########################     Sales Main Form   ################################

class sale_sugar(models.Model): 
	_name 		 = 'sales.sugar' 
	_description = 'Sales delivery Sugar industry'
	_rec_name = 'order_no'

	customer	 = fields.Many2one('res.partner' , readonly = True)
	mill		 = fields.Many2one('product.template', readonly = True)
	rate		 = fields.Float(string="Rate", readonly = True)
	qty			 = fields.Float(string="Quantity" , readonly = True)
	total		 = fields.Float(string="Total" , readonly = True)
	date 		 =  fields.Date(required=True, readonly = True)
	delivered	 = fields.Float(string="Delivered")
	remaining	 = fields.Float(string="Remaining")
	booking_id   = fields.Char()
	order_no = fields.Char(index=True, readonly=True)

	order_line	 =	fields.One2many('sale.sugar.treeview','sales_sugar_id')

	@api.onchange('order_line')
	def delivery_total(self):
		total = 0
		for x in self.order_line:
			total = total + x.qty_del
		self.delivered = total
		self.remaining = self.qty - self.delivered

	@api.onchange('qty','rate')
	def get_total(self):
		self.total = self.qty * self.rate
		self.remaining = self.qty - self.delivered

	@api.model
	def create(self, vals):
		vals['order_no'] = self.env['ir.sequence'].next_by_code('sales.sugar')
		
		new_record = super(sale_sugar, self).create(vals)
		amanat_supplier = self.env['res.partner'].search([('name','=',"Amanat")])
		relevant_summary = self.env['stock.summary.sugar'].search([('sales_id','=',new_record.id)])
		relevant_sale_orders = self.env['sales.sugar'].search([('mill','=',new_record.mill.id),('remaining','>',0)])
		

		generate_summary = relevant_summary.create({
			'supplier': amanat_supplier.id,
			'mill':new_record.mill.id,
			'amanat_of':new_record.customer.id, 
			'amanat':new_record.remaining,
			'sales_id':new_record.id
			})


		
		journal_entries = self.env['account.move'].search([])
		

		journal_entries_lines = self.env['account.move.line'].search([])
		create_journal_entry = journal_entries.create({
				'journal_id': 1,
				'date':new_record.date,
				'ref':new_record.order_no,
				'name':new_record.order_no
				})
		create_debit = journal_entries_lines.create({
			'account_id':7,
			'partner_id':new_record.customer.id,
			'name':str(new_record.mill.name) + " "+ str(new_record.qty) + " @ " + str(new_record.rate), 
			'debit':new_record.total,
			'move_id':create_journal_entry.id
			})
		create_credit = journal_entries_lines.create({
			'account_id':17,
			'partner_id':new_record.customer.id,
			'name':new_record.mill.name + " "+ str(new_record.qty) + " @ " + str(new_record.rate), 
			'credit':new_record.total,
			'move_id':create_journal_entry.id
			})

		stock_history = self.env['stock.history.sugar']

		create_amanat = stock_history.create({
				'mill':new_record.mill.id,
				'qty':(new_record.remaining)* -1,
				'date':new_record.date,
				'amanat_id':new_record.id,
				# 'party':new_record.customer.id,
				'ref_no':new_record.order_no,
				'type_transaction':"Amanat",
				'delivery_to':new_record.customer.name,
				# 'total':new_record.sales_sugar_id.qty

				})
		return new_record

	@api.multi
	def write(self, vals):
		super(sale_sugar, self).write(vals)

		amanat_supplier = self.env['res.partner'].search([('name','=',"Amanat")])
		relevant_summary = self.env['stock.summary.sugar'].search([('sales_id','=',self.id)])
		relevant_sale_orders = self.env['sales.sugar'].search([('mill','=',self.mill.id),('remaining','>',0)])

		if not relevant_summary:
			generate_summary = relevant_summary.create({
				'supplier': amanat_supplier.id,
				'mill':self.mill.id,
				'amanat_of':self.customer.id, 
				'amanat':self.remaining,
				'sales_id':self.id
				})
		else:
			if self.remaining == 0:
				relevant_summary.unlink()
			else:
				relevant_summary.amanat = self.remaining
				relevant_summary.mill = self.mill.id
				relevant_summary.amanat_of = self.customer.id
				relevant_summary.amanat = self.remaining
			

		journal_entry = self.env['account.move'].search([('ref','=',self.order_no)])
		
		journal_entry.date = self.date

		journal_entry_line = self.env['account.move.line'].search([('move_id.ref','=',self.order_no)])
		for x in journal_entry_line:
			print x.id
			x.partner_id = self.customer.id
			x.name = self.mill.name + " "+ str(self.qty) + " @ " + str(self.rate)
			if x.debit > 0:
				x.debit = self.total
			elif x.credit > 0:
				x.credit = self.total

		amanat = self.env['stock.history.sugar'].search([('amanat_id','=',self.id)])
		if not amanat and self.qty > 0:
			create_amanat = amanat.create({
				'mill':self.mill.id,
				'qty':(self.remaining)* -1,
				'date':self.date,
				'amanat_id':self.id,
				# 'party':new_record.customer.id,
				'ref_no':self.order_no,
				'type_transaction':"Amanat",
				'delivery_to':self.customer.name,
				# 'total':new_record.sales_sugar_id.qty

				})
		if self.qty > 0:
			amanat.qty = self.remaining * -1
			amanat.mill = self.mill.id
			amanat.date = self.date
			delivery_to = self.customer.name
		elif self.qty == 0:
			amanat.unlink()


		return True

	@api.multi
	def unlink(self):

		journal_entry = self.env['account.move'].search([('ref','=',self.order_no)])
		journal_entry.unlink()
		amanat = self.env['stock.history.sugar'].search([('amanat_id','=',self.id)])
		amanat_stock_summary = self.env['stock.summary.sugar'].search([('sales_id','=',self.id)])
		for x in amanat:
			x.unlink()
		for y in amanat_stock_summary:
			y.unlink()
		super(sale_sugar, self).unlink()

		return True



class sale_sugar_treeview(models.Model):

	_name 		 = 'sale.sugar.treeview'
	_description = 'Tree View of sales module sugar industry'

	customer            = fields.Many2one('res.partner')
	delivery_from		= fields.Many2one('res.partner')
	qty_del				= fields.Float(string="Quantity Delivered")
	date				= fields.Date(required=True,default=fields.Date.context_today)
	sales_sugar_id      = fields.Many2one('sales.sugar')
	loading_id          = fields.Many2one('loading.sugar.tree')
	

	@api.model
	def create(self, vals):

		new_record = super(sale_sugar_treeview, self).create(vals)

		stock_summary = self.env['stock.summary.sugar'].search([('supplier','=',new_record.delivery_from.id),('mill','=',new_record.sales_sugar_id.mill.id)])
		if stock_summary:
			stock_summary.qty = stock_summary.qty - new_record.qty_del

		
		stock_history = self.env['stock.history.sugar'].search([])
		create_stock_history = stock_history.create({
				'mill':new_record.sales_sugar_id.mill.id,
				'qty':(new_record.qty_del)* -1,
				'date':new_record.date,
				'delivery_id':new_record.id,
				'party':new_record.delivery_from.id,
				'ref_no':new_record.sales_sugar_id.order_no,
				'type_transaction':"Sale",
				'delivery_to':new_record.sales_sugar_id.customer.name,
				'total':new_record.sales_sugar_id.qty

				})
	 
		return new_record

	@api.multi
	def write(self, vals):
		before_write = self.qty_del
		super(sale_sugar_treeview, self).write(vals)
		after_write = self.qty_del

		difference = after_write - before_write


		stock_summary = self.env['stock.summary.sugar'].search([('supplier','=',self.delivery_from.id),('mill','=',self.sales_sugar_id.mill.id)])
		if stock_summary:
			stock_summary.qty = stock_summary.qty - difference

		stock_history = self.env['stock.history.sugar'].search([('delivery_id','=',self.id)])
		stock_history.mill = self.sales_sugar_id.mill.id
		stock_history.qty = (self.qty_del)*-1
		stock_history.date = self.date
		stock_history.party = self.delivery_from.id
		stock_history.delivery_to = self.sales_sugar_id.customer.name
		stock_history.total = self.sales_sugar_id.qty
		ref_no = self.sales_sugar_id.order_no

		return True

	@api.multi
	def unlink(self):
		stock_summary = self.env['stock.summary.sugar'].search([('supplier','=',self.delivery_from.id),('mill','=',self.sales_sugar_id.mill.id)])
		if stock_summary:
			for x in stock_summary:
				stock_summary.qty = x.qty + self.qty_del
		history_record = self.env['stock.history.sugar'].search([('delivery_id','=',self.id)])
		if history_record:
			for x in history_record:
				x.unlink()
		super(sale_sugar_treeview, self).unlink()
		

		return True



########################## Purchase Booking Form ############################################

class purchase_booking(models.Model): 
	_name 		 = 'purchase.booking' 
	_description = 'Booking Module in Purchase'
	# _rec_name = 'str(date)'
	
	date 		 =  fields.Date(required=True, default=fields.Date.context_today)
	total 		 =	fields.Float(string="Total Amount")
	total_qty 		 =	fields.Float(string="Total Quantity")
	avg			 =	fields.Float(string="Average")
	user_id      = fields.Many2one('res.users',default=lambda self: self.env.user)
	name         = fields.Char()

	order_line	 =	fields.One2many('purchase.booking.treeview','purchase_booking_id' )
	


	@api.model
	def create(self, vals):

		new_record = super(purchase_booking, self).create(vals)

		for x in new_record.order_line:
			purchase = self.env['purchase.sugar'].search([('p_booking_id','=',x.id)])
			if not purchase:
				generate_purchase_form = purchase.create({
					'supplier': x.supplier.id,
					'mill':x.mill.id,
					'rate':x.rate,
					'qty':x.qty,
					'total':x.total,
					'p_booking_id':x.id,
					'date':new_record.date,
					'remaining':x.qty
					})

			else:
				purchase.supplier = x.supplier.id
				purchase.mill =x.mill.id
				purchase.rate =x.rate
				purchase.qty = x.qty
				purchase.total = x.total
				purchase.date = new_record.date


		return new_record

	@api.multi
	def write(self, vals):
		super(purchase_booking, self).write(vals)
		for x in self.order_line:
			purchase = self.env['purchase.sugar'].search([('p_booking_id','=',x.id)])
			if not purchase:
				generate_purchase_form = purchase.create({
					'supplier': x.supplier.id,
					'mill':x.mill.id,
					'rate':x.rate,
					'qty':x.qty,
					'total':x.total,
					'p_booking_id':x.id,
					'date':self.date
					})
			else:
				purchase.supplier = x.supplier.id
				purchase.mill =x.mill.id
				purchase.rate =x.rate
				purchase.qty = x.qty
				purchase.total = x.total
				purchase.date = self.date

		return True




	@api.onchange('order_line','date')
	def get_total(self):
		total = 0
		total_qty = 0
		for x in self.order_line:
			total = total + x.total
			total_qty = total_qty + x.qty
		self.total = total
		self.total_qty = total_qty
		if(self.total_qty>0):
			self.avg = self.total / self.total_qty

		self.name = str(self.user_id.name) + " / "+ str(self.date) 



class purchase_booking_treeview(models.Model):

	_name 		 = 'purchase.booking.treeview'
	_description = 'Tree View of purchase booking'

	supplier	 = fields.Many2one('res.partner')
	mill		 = fields.Many2one('product.template')
	qty			 = fields.Float(string="Quantity")
	rate		 = fields.Float(string="Rate")
	total		 = fields.Float(string="Total")
	purchase_booking_id = fields.Many2one('purchase.booking')



	# @api.model
	# def create(self, vals):

	# 	new_record = super(purchase_booking_treeview, self).create(vals)
	# 	relevant_summary = self.env['stock.summary.sugar'].search([('mill','=',new_record.mill.id),('supplier','=',new_record.supplier.id)])
	# 	if not relevant_summary:
	# 		generate_summary = relevant_summary.create({
	# 			'supplier': new_record.supplier.id,
	# 			'mill':new_record.mill.id,
	# 			'qty':new_record.qty
	# 			})
	# 	else:
	# 		relevant_summary.qty = relevant_summary.qty + new_record.qty



	# 	return new_record

	# @api.multi
	# def write(self, vals):
	# 	super(purchase_booking_treeview, self).write(vals)
	# 	relevant_summary = self.env['stock.summary.sugar'].search([('mill','=',self.mill.id),('supplier','=',self.supplier.id)])
	# 	if not relevant_summary:
	# 		generate_summary = relevant_summary.create({
	# 			'supplier': self.supplier.id,
	# 			'mill':self.mill.id,
	# 			'qty':self.qty
	# 			})
	# 	else:
	# 		relevant_summary.qty = relevant_summary.qty + self.qty

	# 	return True


	@api.multi
	def unlink(self):
		# relevant_summary = self.env['stock.summary.sugar'].search([('mill','=',self.mill.id),('supplier','=',self.supplier.id)])
		# relevant_summary.qty = relevant_summary.qty - self.qty		
		super(purchase_booking_treeview, self).unlink()

		purchase_delivery = self.env['purchase.sugar'].search([('p_booking_id','=',self.id)])
		purchase_delivery.unlink()

		return True

	@api.onchange('qty','rate')
	def get_total(self):
		self.total = self.qty * self.rate

############################### Purchase Main Form #####################################

class purchase_sugar(models.Model): 
	_name 		 = 'purchase.sugar' 
	_description = 'Purchase delivery Sugar industry'
	_rec_name = 'order_no'

	supplier	 = fields.Many2one('res.partner')
	mill		 = fields.Many2one('product.template')
	rate		 = fields.Float(string="Rate")
	qty			 = fields.Float(string="Quantity")
	received	 = fields.Float(string="Received")
	remaining	 = fields.Float(string="Remaining")
	total		 = fields.Float(string="Total")
	date 		 =  fields.Date(required=True)
	p_booking_id        =  fields.Integer()
	order_no = fields.Char(index=True, readonly=True)
	sugar_tree_id = fields.One2many('purchase.sugar.tree','sugar_tree')





	@api.onchange('qty','rate')
	def get_total(self):
		self.total = self.qty * self.rate

	@api.model
	def create(self, vals):
		vals['order_no'] = self.env['ir.sequence'].next_by_code('purchase.sugar')
		new_record = super(purchase_sugar, self).create(vals)

		stock_summary = self.env['stock.summary.sugar'].search([('supplier','=',new_record.supplier.id),('mill','=',new_record.mill.id)])

		if not stock_summary:
			stock_summary.create({
				'supplier': new_record.supplier.id,
				'mill':new_record.mill.id,
				'qty':new_record.qty, 
				})
		else:
			stock_summary.qty = stock_summary.qty + new_record.qty




		stock_history = self.env['stock.history.sugar'].search([])
		create_stock_history = stock_history.create({
				'mill':new_record.mill.id,
				'qty':new_record.qty,
				'date':new_record.date,
				'purchase_id':new_record.id,
				'party':new_record.supplier.id,
				'ref_no':new_record.order_no,
				'type_transaction':"Purchase"
				})

		journal_entries = self.env['account.move'].search([])
		journal_entries_lines = self.env['account.move.line'].search([])
		create_journal_entry = journal_entries.create({
				'journal_id': 2,
				'date':new_record.date,
				'ref':new_record.order_no,
				'name':new_record.order_no
				})
		create_debit = journal_entries_lines.create({
			'account_id':18,
			'partner_id':new_record.supplier.id,
			'name':new_record.mill.name + " "+ str(new_record.qty) + " @ " + str(new_record.rate), 
			'debit':new_record.total,
			'move_id':create_journal_entry.id
			})
		create_credit = journal_entries_lines.create({
			'account_id':13,
			'partner_id':new_record.supplier.id,
			'name':new_record.mill.name + " "+ str(new_record.qty) + " @ " + str(new_record.rate), 
			'credit':new_record.total,
			'move_id':create_journal_entry.id
			})



		return new_record

	@api.multi
	def write(self, vals):
		before_write = self.qty
		super(purchase_sugar, self).write(vals)
		after_write = self.qty
		difference = after_write - before_write

		stock_summary = self.env['stock.summary.sugar'].search([('supplier','=',self.supplier.id),('mill','=',self.mill.id)])
		if not stock_summary:
			stock_summary.create({
				'supplier': self.supplier.id,
				'mill':self.mill.id,
				'qty':difference, 
				})
		else:
			stock_summary.qty = stock_summary.qty + difference


		stock_history = self.env['stock.history.sugar'].search([('purchase_id','=',self.id)])
		print stock_history
		stock_history.mill = self.mill.id
		stock_history.qty = self.qty
		stock_history.date = self.date
		stock_history.party = self.supplier.id
		stock_history.ref_no = self.order_no

		journal_entry = self.env['account.move'].search([('ref','=',self.order_no)])
		print journal_entry
		
		journal_entry.date = self.date

		journal_entry_line = self.env['account.move.line'].search([('move_id.ref','=',self.order_no)])
		for x in journal_entry_line:
			print x.id
			x.partner_id = self.supplier.id
			x.name = self.mill.name + " "+ str(self.qty) + " @ " + str(self.rate)
			if x.debit > 0:
				x.debit = self.total
			elif x.credit > 0:
				x.credit = self.total
		return True

	@api.multi
	def unlink(self):

		stock_summary = self.env['stock.summary.sugar'].search([('supplier','=',self.supplier.id),('mill','=',self.mill.id)])
		if not stock_summary:
			stock_summary.create({
				'supplier': self.supplier.id,
				'mill':self.mill.id,
				'qty':self.qty * -1, 
				})
		else:
			stock_summary.qty = stock_summary.qty - self.qty



		stock_history = self.env['stock.history.sugar'].search([('purchase_id','=',self.id)])
		stock_history.unlink()
		journal_entry = self.env['account.move'].search([('ref','=',self.order_no)])
		journal_entry.unlink()

		super(purchase_sugar, self).unlink()

		return True

class purchase_sugar_tree(models.Model):
	_name 		 = 'purchase.sugar.tree'

	date		 = fields.Date(string='Date')
	qty			 = fields.Float(string="Quantity")
	sugar_tree   = fields.Many2one('purchase.sugar')


###################### Stock History #################################

class stock_history(models.Model):
	_name = 'stock.history.sugar'
	_rec_name = 'ref_no'

	

	mill = fields.Many2one('product.template')
	qty	 = fields.Float(string="Quantity")
	date	 = fields.Date(string="Date")
	party = fields.Many2one('res.partner',string="Party")
	ref_no = fields.Char()
	purchase_id = fields.Integer()
	delivery_id = fields.Integer()
	type_transaction = fields.Char(string = "Type")
	delivery_to = fields.Char(string = "Delivered To")
	total	 = fields.Float(string="Total")
	amanat_id = fields.Integer()



###################### Stock Summary #################################

class stock_summary(models.Model):
	_name = 'stock.summary.sugar'
	# _rec_name = 'ref_no'

	

	mill = fields.Many2one('product.template')
	qty	 = fields.Float(string="Quantity")
	supplier = fields.Many2one('res.partner',string="Party")
	purchase_id = fields.Integer()
	sold	 = fields.Float(string="Sold")
	amanat	 = fields.Float(string="Amanat")
	amanat_of	 = fields.Many2one('res.partner',string="Amanat of")
	sales_id	 = fields.Many2one('sales.sugar')


	@api.multi
	def write(self, vals):
		super(stock_summary, self).write(vals)

		for x in self:
			if self.qty == 0 and self.amanat == 0:
				x.unlink()
	

###################### Overwrite function for creating journal entry #################################

class AccountMoveRemoveValidation(models.Model):
	_inherit = "account.move"

	customer_payment_id = fields.Integer()
	supplier_payment_id = fields.Integer()
	inter_payment_id = fields.Integer()

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


###################### Sale Purchase History #################################

class SalePurchaseHistory(models.Model):
	_name = "sale.purchase"

	party            = fields.Many2one('res.partner', readonly = True)
	mill		     = fields.Many2one('product.template', readonly = True)
	qty			     = fields.Float(string="Quantity", readonly = True)
	rate		     = fields.Float(string="Rate", readonly = True)
	total		     = fields.Float(string="Total", readonly = True)
	type_transaction = fields.Char(string = "Type", readonly = True)



###################### Sugar Loading Form #################################

class loading_sugar(models.Model): 
	_name 		 = 'loading.sugar' 
	_description = 'Loading'
	# _rec_name = 'order_no'

	total		 = fields.Float(string="Total")
	date 		 =  fields.Date(required=True)

	loading_tree  = fields.One2many('loading.sugar.tree','loading_id')
	
	@api.onchange('loading_tree')
	def get_total(self):
		total_qty = 0
		for x in self.loading_tree:
			
			total_qty = total_qty + x.qty
		self.total = total_qty

	


###################### Sugar Loading Tree #################################

class loading_sugar_tree(models.Model):
	_name 		 = 'loading.sugar.tree' 
	# _description = 'Loading'
	# _rec_name = 'order_no'

	customer	 = fields.Many2one('res.partner')
	supplier     = fields.Many2one('res.partner')
	mill		 = fields.Many2one('product.template')
	qty			 = fields.Float(string="Quantity")
	date 		 = fields.Date(required=True)
	loading_id   = fields.Many2one('loading.sugar')


	@api.model
	def create(self, vals):
		remaining_adjustable=0
		total_purchase_qty=0
		record_list=[]
		# print "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
		# vals['order_no'] = self.env['ir.sequence'].next_by_code('purchase.sugar')
		new_record = super(loading_sugar_tree, self).create(vals)
		print new_record.supplier
		# print "sssssssssssssssssssssssssssss"

		sales_order = self.env['sales.sugar'].search([('customer','=',new_record.customer.id),('remaining','>',0),('mill','=',new_record.mill.id)])
		sales_order = sorted(sales_order, key=lambda x: x.date)
		remaining_adjustable = new_record.qty
		for x in sales_order:
			print x.qty
			# print "mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm"
			if remaining_adjustable > x.remaining:
				qty_adjusted = x.remaining   
				
			else:
				qty_adjusted = remaining_adjustable

			remaining_adjustable = remaining_adjustable - qty_adjusted
			if qty_adjusted > 0:
				link_to_sale_order = self.env['sale.sugar.treeview'].create({
						'delivery_from':new_record.supplier.id,
						'qty_del':qty_adjusted,
						'date':new_record.date,
						'sales_sugar_id':x.id,
						'loading_id':new_record.id
						})
				delivered = 0
				for y in x.order_line:
					delivered = delivered + y.qty_del
				x.delivered = delivered
				x.remaining = x.qty - x.delivered 
		
		
		purchase_qty_tree=0
		link_to_sale_orde=0
		remaining_adjustable1=0
		qty_adjusted1=0
		total_qty=0
		delivered=0
		# vals['order_no'] = self.env['ir.sequence'].next_by_code('purchase.sugar')
		# new_record = super(loading_sugar_tree, self).create(vals)
		PurchaseSugar = self.env['purchase.sugar'].search([('supplier','=',new_record.supplier.id),('remaining','>',0),('mill','=',new_record.mill.id)])
		PurchaseSugar = sorted(PurchaseSugar, key=lambda x: x.date)
		remaining_adjustable1 = new_record.qty
		for x in PurchaseSugar:
			# total_qty = total_qty + x.qty
			if remaining_adjustable1 > x.remaining:
				qty_adjusted1 = x.remaining   
				
			else:
				qty_adjusted1 = remaining_adjustable1

			remaining_adjustable1 = remaining_adjustable1 - qty_adjusted1
			remaining_qty_purchase= x.remaining - qty_adjusted1
			if qty_adjusted1 > 0:
				link_to_sale_order = self.env['purchase.sugar.tree'].create({
					'date':new_record.date,
					'qty':qty_adjusted1,
					'sugar_tree':x.id
						})

				for y in x.sugar_tree_id:
					delivered = delivered + y.qty
				x.remaining = remaining_qty_purchase
				x.received = delivered
			else:
				raise ValidationError("Sorry You have not sufficient stock You require")
				return {'value':{},'warning':{'title':
				'warning','message':"Extra loading Quantity"}}
		return new_record



	@api.multi
	def write(self, vals):
		super(loading_sugar_tree, self).write(vals)

		linked_loading = self.env['sale.sugar.treeview'].search([('loading_id','=',self.id)])
		if linked_loading:
			for x in linked_loading: 
				sales_order = self.env['sales.sugar'].search([('id','=',x.sales_sugar_id.id)])
				sales_order.delivered = sales_order.delivered - x.qty_del
				sales_order.remaining = sales_order.qty - sales_order.delivered
				x.unlink()	

		sales_order = self.env['sales.sugar'].search([('customer','=',self.customer.id),('remaining','>',0),('mill','=',self.mill.id)])
		sales_order = sorted(sales_order, key=lambda x: x.date)
		remaining_adjustable = self.qty
		for y in sales_order:
			if remaining_adjustable > y.remaining:
				qty_adjusted = y.remaining   
			else:
				qty_adjusted = remaining_adjustable
			remaining_adjustable = remaining_adjustable - qty_adjusted
			if qty_adjusted > 0:
				link_to_sale_order = self.env['sale.sugar.treeview'].create({
						'delivery_from':self.supplier.id,
						'qty_del':qty_adjusted,
						'date':self.date,
						'sales_sugar_id':y.id,
						'loading_id':self.id
						})
				delivered = 0
				for z in y.order_line:
					delivered = delivered + z.qty_del
				y.delivered = delivered
				y.remaining = y.qty - y.delivered
		return True

	@api.multi
	def unlink(self):

		linked_loading = self.env['sale.sugar.treeview'].search([('loading_id','=',self.id)])
		if linked_loading:
			for x in linked_loading:
				sales_order = self.env['sales.sugar'].search([('id','=',x.sales_sugar_id.id)])
				for y in sales_order:
					y.delivered = y.delivered - x.qty_del
					y.remaining = y.qty - y.delivered 
				x.unlink()
		super(loading_sugar_tree, self).unlink()

		return True


	