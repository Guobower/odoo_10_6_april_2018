# -*- coding: utf-8 -*- 
from odoo import models, fields, api
import datetime
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta
from openerp.exceptions import Warning
from openerp.exceptions import ValidationError
import math
class plot_form(models.Model): 
	_inherit = 'product.template'
	type = fields.Selection([
		('consu','Consumable'),
		('service','Service'),
		('product','Stockable')], string='Product Type', default='product', required=True,
		help='A stockable product is a product for which you manage stock. The "Inventory" app has to be installed.\n'
			 'A consumable product, on the other hand, is a product for which stock is not managed.\n'
			 'A service is a non-material product you provide.\n'
			 'A digital content is a non-material product you sell online. The files attached to the products are the one that are sold on '
			 'the e-commerce such as e-books, music, pictures,... The "Digital Product" module has to be installed.')

	plot_size = fields.Many2one('plot.size', 'Size (Marla/Kanal)')
	plot_location = fields.Many2many(comodel_name='plot.factor',
						relation='user_course_rel',
						column1='name',
						column2='factor_id')
	status_selection = fields.Selection([
		('sold','Sold'),
		('hold','Hold'),
		('available','Available')] , string='Status')
	plot_customer = fields.Many2one('res.partner', 'Customer')
	plot_file_no = fields.Char('File No')
	plot_rate_marla = fields.Float (string = "Rate per Marla")
	total_plot_price = fields.Float(string = "Total Price")
	plot_width = fields.Float (string = "Width")
	plot_length = fields.Float (string = "Length")
	plot_scheme_name = fields.Many2one('scheme.name', 'Scheme Name')
	plot_block = fields.Char (string = "Block")
	plot_sector = fields.Char (string = "Sector")
	plot_khasra_no = fields.Char (string = "Khasra No")
	plot_sq_ft = fields.Float (string = "Sq Ft")
	property_dealer = fields.Many2one('res.partner', string = "Property Dealer" , domain = [('plot_property_dealer','=',True)])
	plot_commission = fields.Float(string="Commission")
	plot_amount = fields.Float(string="Commission Amount", compute='_compute_total')
	plot_history_ids = fields.One2many('plot.history','plot_product_history_id',string='Plot History')
	total_marla = fields.Float(string="Marla")

	@api.onchange('plot_width','plot_length')
	def calculate_sq_ft(self):
		self.plot_sq_ft = self.plot_width * self.plot_length

	@api.onchange('plot_size','plot_rate_marla')
	def calculate_total_price(self):
		self.total_plot_price = self.plot_rate_marla * self.plot_size.size

	@api.onchange('plot_size')
	def calculate_total_price(self):
		if self.plot_size:
			self.total_plot_price = self.plot_size.price
			if self.plot_size.unit == "marla":
				self.plot_rate_marla = self.total_plot_price/self.plot_size.size
			elif self.plot_size.unit == "kanal":
				self.plot_rate_marla = self.total_plot_price/(self.plot_size.size * 20)
			else:
				raise Warning("You have not mentioned price and size of Plot..!")
	@api.one
	@api.depends('plot_commission', 'total_plot_price')
	def _compute_total(self):
		self.plot_amount = self.total_plot_price * (self.plot_commission / 100)

	@api.onchange('plot_size')
	def calculate_total_price(self):
		if self.plot_size:
			self.total_plot_price = self.plot_size.price
			if self.plot_size.unit == "marla":
				self.total_marla = self.plot_size.size
				self.plot_rate_marla = self.total_plot_price/self.total_marla
			elif self.plot_size.unit == "kanal":
				self.total_marla = self.plot_size.size * 20
				self.plot_rate_marla = self.total_plot_price/self.total_marla
			else:
				raise Warning("You have not mentioned price and size of Plot..!")


class plot_factor(models.Model):
	_name = "plot.factor"
	name = fields.Char()
	factor_id = fields.Float()

class plot_size(models.Model):
	_name = "plot.size"
	_rec_name = 'size'
	price = fields.Float()
	unit = fields.Selection([
		('marla', 'Marla'),
		('kanal', 'Kanal'),], string='Unit')
	size = fields.Float()
	type_of_plot = fields.Selection([
		('residential', 'Residential'),
		('commercial', 'Commercial'),], string='Type')
	# plot_difference = fields.Float(string="Plot Difference")

class plot_scheme_name(models.Model):
	_name = "scheme.name"
	_rec_name = 'name'
	
	name = fields.Char()
	address = fields.Text()


class sale_order_plot_extended(models.Model):
	_inherit = 'sale.order'

	state = fields.Selection([
		('draft', 'Booked'),
		('sent', 'Sold'),
		], string='Status', readonly=True, copy=False, index=True, track_visibility='onchange', default='draft')
	plot_number = fields.Many2one('product.template','Plot Number', domain=[('status_selection','=','available')] )
	plot_file_no = fields.Char('File No')
	ms_new = fields.Char(string='MS', required=True)
	plot_size = fields.Many2one('plot.size', 'Size (Marla)')
	plot_location = fields.Many2many(comodel_name='plot.factor',
						relation='user_course_rel',
						column1='name',
						column2='factor_id')
	plot_rate_marla = fields.Float (string = "Rate per Marla")
	total_plot_price = fields.Float(string = "Total Price")
	price_char = fields.Char(string = "Price")
	plot_width = fields.Float (string = "Width")
	plot_length = fields.Float (string = "Length")
	plot_scheme_name = fields.Many2one('scheme.name', 'Scheme Name')
	plot_block = fields.Char (string = "Block")
	plot_sector = fields.Char (string = "Sector")
	plot_sq_ft = fields.Float (string = "Sq Ft")
	property_dealer = fields.Many2one('res.partner', 'Property Dealer', domain = [('plot_property_dealer','=',True)])
	start_date = fields.Date(string = "Start Date")
	end_date = fields.Date(string = "End Date")
	total_payable = fields.Float(string = "Total Payable")
	total_paid = fields.Float(string = "Total Paid",compute='_compute_total_paid', store = True)
	installment_plan_ids = fields.Many2one('plot.installment.plan', 'Installment Plan')
	# installment_plan = fields.Selection([
	#     ('monthly','Monthly'),
	#     ('quarterly','Quarterly'),
	#     ('six_months','Six Months'),
	#     ('bimonthly','Bimonthly'),
	#     ('lump_sum','Lump sum')] , string="Installment Plan")
	no_of_installments = fields.Integer(string = "No of Installments")
	remaining = fields.Float(compute='_compute_remaining', store = True)
	plot_token = fields.Float(string = "Token")
	plot_advance = fields.Float(string = "Advance")
	plot_discount = fields.Float(string = "Discount")
	plot_net = fields.Float(string = "Net")
	plot_payment_id = fields.One2many('account.invoice','plot_file_link',string='Payment History')
	plot_invoice_id = fields.Many2one('account.invoice')
	rate_per_installment = fields.Float("Amount per Installment")
	# diff_in_installment = fields.Float("Difference Installment")
	plot_application_no = fields.Char (string = "Application No")
	plot_registration_no = fields.Char (string = "Registration No")
	total_marla = fields.Float(string="Marla")
	plot_commission = fields.Float(string="Dealer Commission")
	mc_commission = fields.Float(string="MC Commission")
	plot_amount = fields.Float(string="Dealer Commission Amount", compute='_compute_total')
	ms_commission_amount = fields.Float(string="MC Commission Amount", compute='_compute_ms_commission_amount')

	address = fields.Char(string="Address")
	contact_no = fields.Char(string="Contact No")
	
	plot_history_ids = fields.One2many('plot.history','plot_sale_history_id',string='Plot History')
	Transfer_to = fields.Char(string="TF/RF")
		

	@api.multi
	def plot_link_invoice(self):

		# print "111111111111111111111111111"
		plot_record=self.env['sale.order'].search([])
		record = 1
		for x in plot_record:
			record = record + 1
			x._compute_total_paid()
			x._compute_remaining()

			print "xxxxxxxxxxxxxxxxxxxxxxxx"
			print record
			print "xxxxxxxxxxxxxxxxxxxxxxxxx"
		# record = 1
		# for x in plot_record:
		# 	record = record + 1
		# 	invoice_records_link=self.env['account.invoice'].search([('name','=',x.plot_sector)])
		# 	for y in invoice_records_link:
		# 		y.plot_file_link=x.id
		# 	print record
		# 	print "xxxxxxxxxxxxxxxxxxxxxxxxxxxx"

	@api.one
	def _compute_total_paid(self):
		total_value=0.0
		for x in self.plot_payment_id:
			total_value = int(total_value) + int(x.total_paid)
		self.total_paid = total_value


	# @api.onchange('ms_new')
	# def check_ms(self):
	# 	if self.ms_new:
	# 		already_rec_name=self.env['sale.order'].search([('ms_new','=',self.ms_new)])
	# 		abc="Already exist"
	# 		xyz="MS no please Enter the Another"
	# 		if already_rec_name:
	# 			print "ok"
	# 			if self.ms_new=="":
	# 				print "emphty"
	# 			else:
	# 				self.ms_new=""
	# 			return {'value':{},'warning':{'title':
	# 			'warning','message':"%s %s %s"%(abc,already_rec_name.ms_new,xyz)}}


	
	@api.one
	def _compute_remaining(self):
		self.remaining=self.plot_net - self.total_paid

	@api.one
	@api.depends('mc_commission', 'total_plot_price')
	def _compute_ms_commission_amount(self):
		self.ms_commission_amount =self.mc_commission

	@api.one
	@api.depends('plot_commission', 'total_plot_price')
	def _compute_total(self):
		self.plot_amount = self.plot_commission

	@api.onchange('partner_id')
	def address_contact(self):
		if self.partner_id:
			customer_form = self.env['res.partner'].search([('id','=',self.partner_id.id)])
			self.address = "%s %s %s %s %s %s" %(customer_form.street or '', customer_form.street2 or '', customer_form.city or '', customer_form.state_id.name or '',customer_form.zip or '',customer_form.country_id.name or '')
			self.contact_no = customer_form.mobile





	@api.onchange('plot_width','plot_length')
	def calculate_sq_ft(self):
		self.plot_sq_ft = self.plot_width * self.plot_length

	# @api.onchange('plot_size')
	# def calculate_total_price(self):
	# 	if self.plot_size:
	# 		self.total_plot_price = self.plot_size.price
	# 		if self.plot_size.unit == "marla":
	# 			self.total_marla = self.plot_size.size
	# 			self.plot_rate_marla = self.total_plot_price/self.total_marla
	# 		elif self.plot_size.unit == "kanal":
	# 			self.total_marla = self.plot_size.size * 20
	# 			self.plot_rate_marla = self.total_plot_price/self.total_marla
	# 		else:
	# 			raise Warning("You have not mentioned price and size of Plot..!")

	# @api.multi
	# def validate_stage(self):
	# 	self.getValuesOnValidate()
	# 	self._create_plot_purchase_invoice(self.property_dealer.id, self.plot_amount, self.date_order, self.plot_file_no, self.plot_number)
	# 	self.write({'state': 'sent'})

	# @api.onchange('start_date','end_date','installment_plan_ids')
	# def calculate_installments(self):
	# 	if self.start_date and self.end_date:
	# 		start_date = datetime.strptime(self.start_date,"%Y-%m-%d")
	# 		self.end_date = start_date + timedelta(days=36*365/12)
	# 		if self.installment_plan_ids.name == 'monthly':
	# 			self.no_of_installments = int(self._date_subtraction(self.start_date, self.end_date)) / (365/12)
	# 		elif self.installment_plan_ids.name == 'quarterly':
	# 			self.no_of_installments = int(self._date_subtraction(self.start_date, self.end_date)) / (3*365/12)
	# 		elif self.installment_plan_ids.name == 'six_months':
	# 			self.no_of_installments = int(self._date_subtraction(self.start_date, self.end_date)) / (6*365/12)
	# 	# if self.start_date:
	# 		elif self.installment_plan_ids.name == 'bimonthly':
	# 			self.no_of_installments = (int(self._date_subtraction(self.start_date, self.end_date)) / (365/12))/2

	# def _date_subtraction(self,start_date,end_date):
	# 	SDate = datetime.strptime(start_date,"%Y-%m-%d")
	# 	EDate = datetime.strptime(end_date,"%Y-%m-%d")
	# 	timedelta = EDate - SDate
	# 	return timedelta.days
	# @api.onchange('plot_token','plot_advance')
	# def calculate_net_price(self):
	# 	if self.plot_token or self.plot_advance:
	# 		self.plot_net = self.total_plot_price - (self.plot_token + self.plot_advance)


	# @api.onchange('plot_discount')
	# def net_price_with_dis(self):
	# 	if self.installment_plan_ids.name == "lump_sum":
	# 		if self.plot_discount:
	# 			self.plot_net = self.total_plot_price - (self.total_plot_price * (self.plot_discount/100))


	# @api.onchange('plot_net')
	# def calculate_payable_price(self):
	# 	if self.plot_net:
	# 		self.total_payable = self.plot_net
	# 		self.remaining=self.plot_net - self.total_paid

	# @api.onchange('installment_plan_ids')
	# def calculate_rate_per_installment(self):
	# 	if self.installment_plan_ids:
	# 		self.rate_per_installment = self.installment_plan_ids.amount
	# @api.onchange('plot_number')
	# def get_plot_number_details(self):
	# 	if self.plot_number:
	# 		self.plot_width = self.plot_number.plot_width
	# 		self.plot_length = self.plot_number.plot_length
	# 		self.plot_block = self.plot_number.plot_block
	# 		self.plot_sector = self.plot_number.plot_sector
	# 		self.plot_location = self.plot_number.plot_location
	# 		self.plot_scheme_name = self.plot_number.plot_scheme_name.id

	# @api.multi
	# def updatequtation(self):
	# 	if self.plot_number:
	# 		if self.plot_number.plot_file_no:
	# 			self.plot_file_no = self.plot_number.plot_file_no
	# 			self.plot_number.plot_customer = self.partner_id.id
	# 			self.plot_number.status_selection = "sold"
	# @api.multi
	# def token_invoice(self):
	# 	description = "Token Amount"
	# 	self._create_plot_invoice(description, self.plot_token, self.id, self.partner_id.id, self.start_date ,self.end_date, self.plot_file_no, self.plot_number)
	# 	self.plot_payment_id = self._prepare_payment_history_line(self.plot_invoice_id.id, self.plot_invoice_id.date_invoice, self.plot_invoice_id.date_due, self.plot_token)
	# @api.multi
	# def advance_invoice(self):
	# 	description = "Advance Amount"
	# 	if self.installment_plan_ids.name == 'lump_sum':
	# 		self._create_plot_invoice(description, self.plot_net, self.id, self.partner_id.id, self.date_order ,self.date_order, self.plot_file_no, self.plot_number)
	# 		self.plot_payment_id = self._prepare_payment_history_line(self.plot_invoice_id.id, self.plot_invoice_id.date_invoice, self.plot_invoice_id.date_due, self.plot_net)
	# 	else:
	# 		self._create_plot_invoice(description, self.plot_advance, self.id, self.partner_id.id, self.date_order ,self.date_order, self.plot_file_no, self.plot_number)
	# 		self.plot_payment_id = self._prepare_payment_history_line(self.plot_invoice_id.id, self.plot_invoice_id.date_invoice, self.plot_invoice_id.date_due, self.plot_advance)

	# @api.multi
	# def installment_invoice(self):
	# 	description = " "
	# 	start_date = datetime.strptime(self.start_date,"%Y-%m-%d")
	# 	date_due = datetime.strptime(self.start_date,"%Y-%m-%d")
	# 	date_due = start_date + timedelta(days=5)
	# 	if self.installment_plan_ids.pipt_ids:
	# 		for line in self.installment_plan_ids.pipt_ids:
	# 			description = line.name + " From "+str(start_date)+" To "+str(date_due)
	# 			if self.installment_plan_ids.name == 'monthly':
	# 				start_date = start_date + timedelta(days=365/12)
	# 				date_due = start_date + timedelta(days=5)
	# 			elif self.installment_plan_ids.name == 'quarterly':
	# 				start_date = start_date + timedelta(days=3*365/12)
	# 				date_due = start_date + timedelta(days=5)
	# 			elif self.installment_plan_ids.name == 'six_months':
	# 				start_date = start_date + timedelta(days=6*365/12)
	# 				date_due = start_date + timedelta(days=5)
	# 			elif self.installment_plan_ids.name == 'bimonthly':
	# 				start_date = start_date + relativedelta(months=+2)
	# 				date_due = start_date + timedelta(days=5)
	# 			elif self.installment_plan_ids == 'lump_sum':
	# 				start_date = start_date + timedelta(days=365/12)
	# 				date_due = start_date + timedelta(days=5)
	# 			self._create_plot_invoice(description, line.amount, self.id, self.partner_id.id, start_date , date_due, self.plot_file_no, self.plot_number)
	# 			self.plot_payment_id = self._prepare_payment_history_line(self.plot_invoice_id.id, self.plot_invoice_id.date_invoice, self.plot_invoice_id.date_due, self.plot_invoice_id.amount_total)
		
	# def _create_plot_invoice(self, description, amount, sale_order_id, partner_id, start_date ,end_date, plot_file_no, plot_number):
	# 	invoice_recs            = self.env['account.invoice']
	# 	account_id              = self.env['account.account'].search([('code','=',110200)])
	# 	account_id_invoice_line = self.env['account.account'].search([('code','=',200000)])
	# 	invoice_line_data       = [
	# 	(0, 0,
	# 		{
	# 			'quantity': 1,
	# 			'name': description,
	# 			'account_id': account_id_invoice_line.id,
	# 			'price_unit': amount,
	# 			'plot_file_no' :plot_file_no,
	# 			'plot_number' : plot_number.id
	# 		}
	# 	)
	# 	]
	# 	res = {
	# 	'partner_id' : partner_id,
	# 	'account_id' : account_id.id,
	# 	'invoice_line_ids' : invoice_line_data,
	# 	'date_invoice': start_date,
	# 	'date_due' : end_date,
	# 	'plot_inv_description' : description,
	# 	'sale_order_id':sale_order_id,
	# 	'plot_file_no' : plot_file_no,
	# 	'plot_number' : plot_number.id
	# 	}
	# 	invoice_recs.create(res)
	# 	invoice_ids  =  invoice_recs.search([('sale_order_id','=',sale_order_id)])
	# 	for line in invoice_ids:
	# 		if line.plot_inv_description == description:
	# 			self.plot_invoice_id = line.id

	# def _prepare_payment_history_line(self, plot_invoice_id, invoice_date, due_date, amount):
	# 	new_data = []
	# 	data = {
	# 	'plot_invoice_id' : plot_invoice_id,
	# 	'invoice_date' : invoice_date,
	# 	'due_date' : due_date,
	# 	'amount' : amount,
	# 	}
	# 	new_data.append((0, 0, data))
	# 	return new_data

	# def _create_plot_purchase_invoice(self, partner_id, amount, date_order, plot_file_no, plot_number):
	# 	invoice_recs            = self.env['account.invoice']
	# 	account_id              = self.env['account.account'].search([('code','=',110200)])
	# 	account_id_invoice_line = self.env['account.account'].search([('code','=',200000)])
	# 	invoice_line_data       = [
	# 	(0, 0,
	# 		{
	# 			'quantity': 1,
	# 			'name': "Property Dealer",
	# 			'account_id': account_id_invoice_line.id,
	# 			'price_unit': amount,
	# 			'plot_file_no' :plot_file_no,
	# 			'plot_number' : plot_number.id
	# 		}
	# 	)
	# 	]
	# 	res = {
	# 	'partner_id' : partner_id,
	# 	'account_id' : account_id.id,
	# 	'invoice_line_ids' : invoice_line_data,
	# 	'type' : 'in_invoice',
	# 	'date_invoice': date_order,
	# 	'plot_inv_description': "Property Dealer",
	# 	'plot_file_no' : plot_file_no,
	# 	'plot_number' : plot_number.id
	# 	# 'date_due' : end_date,
	# 	}
	# 	invoice_recs.create(res)

	# def getValuesOnValidate(self):
	# 	if self.plot_number:
	# 		self.plot_number.plot_commission = self.plot_commission
	# 		self.plot_number.plot_amount = self.plot_amount
	# 		self.plot_number.property_dealer = self.property_dealer.id
	# 		self.plot_number.plot_customer  = self.partner_id.id


class plot_payment_history(models.Model):
	_inherit = "account.invoice"
	
	plot_payment_history_tree = fields.Many2one('sale.order',readonly=True)
	total_paid = fields.Float(string ="paid",compute='_compute_total_paid_amount')
	plot_file_link = fields.Many2one('sale.order')
	plot_description = fields.Char(string = "Plot Description")

	@api.one
	def _compute_total_paid_amount(self):
		self.total_paid = self.amount_total - self.residual


	@api.multi
	def update(self):
		invoice_recs = self.env['account.invoice'].search([])
		for x in invoice_recs:
			x.plot_description = x.comment


	@api.multi
	def Ms_number(self):
		print "1111111111111111111111"
		plot_file_ms=self.env['sale.order'].search([])
		for x in plot_file_ms:
			invoice_ms_no=self.env['account.invoice'].search([('name','=',x.plot_registration_no)])
			for z in invoice_ms_no:
				z.plot_payment_history_tree=x.ms_new

			

	# due_date = fields.Date(string="Due Date")
	# amount = fields.Float(string="Amount")
	# payment_paid = fields.Boolean(string="Paid")
	# plot_payment_history_id = fields.Many2one('sale.order','Payment ID')
	# plot_invoice_id = fields.Many2one('account.invoice')

	# @api.multi
	# def unlink(self):
	# 	invoice_recs = self.env['account.invoice'].search([('id','=',self.plot_invoice_id.id)])
	# 	if invoice_recs:
	# 		invoice_recs.unlink()
	# 	result = super(plot_payment_history, self).unlink()
	# 	return result

class plot_payment_update(models.Model):
	_inherit = "account.payment"




	# @api.multi
	# def post(self):
	# 	result = super(plot_payment_update,self).post()
	# 	if self.invoice_ids:
	# 		payment_history = self.env["plot.payment.history"].search([('plot_invoice_id','=',self.invoice_ids.id)])
	# 		print payment_history
	# 		for line in payment_history:
	# 			line.payment_paid = True
	# 			line.plot_payment_history_id.total_payable = line.plot_payment_history_id.total_payable - self.invoice_ids.amount_total
	# 			line.plot_payment_history_id.total_paid = line.plot_payment_history_id.total_paid + self.invoice_ids.amount_total
	# 			line.plot_payment_history_id.remaining = line.plot_payment_history_id.total_payable
	# 			line.amount = self.invoice_ids.amount_total



class plot_invoice_update(models.Model):
	_inherit = "account.invoice"

	plot_inv_description = fields.Text("Description")
	sale_order_id = fields.Many2one('sale.order','Sale ID')
	transfer_charges_id = fields.Many2one('plot.transfer','Transfer Charges ID')
	plot_file_no = fields.Char('File No')
	plot_number = fields.Many2one('product.template','Plot Number' )
	# sale_order_link = fields.Many2one('sale.order' )
	plot_payment_history_tree = fields.Char()
	plot_sale_order = fields.Many2one('sale.order')

	# @api.onchange('plot_payment_history_tree')
	# def customer_file(self):
	# 	# sale_order_mc_no=self.env['sale.order'].search([('ms_new','=',self.plot_payment_history_tree.ms_new)])
	# 	self.partner_id=self.plot_payment_history_tree.partner_id.id

	@api.onchange('plot_sale_order')
	def customer_file(self):
		self.plot_payment_history_tree=self.plot_sale_order.ms_new

class plot_invoice_update(models.Model):
	_inherit = "account.invoice.line"
	plot_file_no = fields.Char('File No')
	plot_number = fields.Many2one('product.template','Plot Number' )



class plot_transfer(models.Model):
	_name = "plot.transfer"
	_rec_name = "plot_file_no"
	name = fields.Char('Name')
	plot_number = fields.Many2one('product.template','Plot Number' )
	plot_file_no = fields.Many2one('sale.order')
	plot_transfer_type = fields.Many2one('plot.transfer.type','Type')
	plot_customer_from = fields.Many2one('res.partner', 'Owner')
	plot_customer = fields.Many2one('res.partner', 'Applicant')
	plot_reg_date = fields.Date('Date')
	plot_reg_date_from = fields.Date('Date')
	plot_date = fields.Date('Date')
	plot_application_no = fields.Char('Transfer Application No')
	plot_reg_no = fields.Char('Transfer Registration No')
	plot_allotment_no = fields.Char('Allotment Letter')
	plot_poss_no = fields.Char('Possession Letter')
	plot_description = fields.Text('Remarks')
	plot_transfer_fee = fields.Float('Transfer Fee')
	plot_doc_received = fields.Boolean('Documents Received')

	plot_size = fields.Many2one('plot.size', 'Size (Marla)')
	plot_location = fields.Many2many(comodel_name='plot.factor',
						relation='user_course_rel',
						column1='name',
						column2='factor_id')
	plot_rate_marla = fields.Float (string = "Rate per Marla")
	total_plot_price = fields.Float(string = "Total Price")
	plot_width = fields.Float (string = "Width")
	plot_length = fields.Float (string = "Length")
	plot_scheme_name = fields.Many2one('scheme.name', 'Scheme Name')
	plot_block = fields.Char (string = "Block")
	plot_sector = fields.Char (string = "Sector")
	plot_khasra_no = fields.Char (string = "Khasra No")
	plot_sq_ft = fields.Float (string = "Sq Ft")
	stages = fields.Selection([
		('draft','Draft'),
		('under_process','Under Process'),
		('cancelled','Cancelled'),
		('transfered','Transferred')] , default="draft", string="Stages")

	transfer_charges = fields.Float('Transfer Charges')
	total_marla = fields.Float(string="Marla")


	@api.onchange('plot_file_no')
	def select_all(self):
		self.plot_customer_from=self.plot_file_no.partner_id.id
		self.plot_reg_date_from=self.plot_file_no.date_order
		self.plot_application_no=self.plot_file_no.plot_application_no
		self.plot_reg_no=self.plot_file_no.plot_registration_no

	
	@api.onchange('plot_size')
	def calculate_total_price(self):
		if self.plot_size:
			self.total_plot_price = self.plot_size.price
			if self.plot_size.unit == "marla":
				self.total_marla = self.plot_size.size
				self.plot_rate_marla = self.total_plot_price/self.total_marla
			elif self.plot_size.unit == "kanal":
				self.total_marla = self.plot_size.size * 20
				self.plot_rate_marla = self.total_plot_price/self.total_marla
			else:
				raise Warning("You have not mentioned price and size of Plot..!")
	@api.onchange('plot_number','plot_file_no')
	def onchange_plot_file_num(self):
		if self.plot_number and self.plot_file_no:
			self.plot_size = self.plot_number.plot_size.id
			self.plot_width = self.plot_number.plot_width
			self.plot_length = self.plot_number.plot_length
			self.plot_sq_ft = self.plot_number.plot_sq_ft
			self.plot_rate_marla = self.plot_number.plot_rate_marla
			self.total_plot_price = self.plot_number.total_plot_price
			self.plot_scheme_name = self.plot_number.plot_scheme_name.id
			self.plot_block = self.plot_number.plot_block
			self.plot_sector = self.plot_number.plot_sector
			self.plot_location = self.plot_number.plot_location.id
			self.plot_khasra_no  = self.plot_number.plot_khasra_no
			self.plot_customer_from = self.plot_number.plot_customer.id



	# @api.multi
	# def transfer_invoice(self):
	# 	record_transfer=self.env['plot.transfer'].search([])
	# 	for x in record_transfer:
	# 		record_invoice=self.env['account.invoice'].search([('date_invoice','>=',x.plot_reg_date),('name','=',x.plot_allotment_no)])
	# 		for y in record_invoice:
	# 			y.partner_id=x.plot_customer.id

	
	@api.multi
	def validate(self):
		self.write({'stages': 'transfered'})
		if self.plot_number or self.plot_file_no:
			# plot_reg_recs = self.env['sale.order'].search([('plot_number','=',self.plot_number.id),('ms_new','=',self.plot_file_no.name)])
			# plot_reg_recs = self.env['sale.order'].search([('plot_number','=',self.plot_number.id),('ms_new','=',self.plot_file_no.ms_new)])
			# if plot_reg_recs:
			# 	print self.ensure_one()
			self.plot_file_no.plot_history_ids |= self.plot_file_no.plot_history_ids.create({
				'plot_from':  self.plot_customer_from.name,
				'plot_to': self.plot_customer.name,
				'plot_allotment_no': self.plot_allotment_no,
				'plot_poss_no': self.plot_poss_no,
				'plot_date': self.plot_reg_date,
				})
			self.plot_file_no.partner_id = self.plot_customer.id
			self.plot_file_no.address = "%s %s %s %s %s %s" %(self.plot_customer.street or '', self.plot_customer.street2 or '', self.plot_customer.city or '', self.plot_customer.state_id.name or '',self.plot_customer.zip or '',self.plot_customer.country_id.name or '')
			self.plot_file_no.contact_no = self.plot_customer.mobile
			self.plot_file_no.Transfer_to = self.plot_customer.name
			# self.plot_number.plot_history_ids |= self.plot_number.plot_history_ids.create({
			# 		'plot_from':  self.plot_customer_from.name,
			# 		'plot_to': self.plot_customer.name,
			# 		'plot_allotment_no': self.plot_allotment_no,
			# 		'plot_poss_no': self.plot_poss_no,
			# 		})
	# @api.multi
	# def transferChargesInvoice(self):
	# 	invoice_records = self.env['account.invoice'].search([('transfer_charges_id','=',self.id)])
	# 	invoice_records.unlink()
	# 	description = "Transfer Charges"
	# 	self._createTransferChargesInvoice(self.plot_customer.id, self.transfer_charges, self.id, self.plot_date, self.plot_file_no, self.plot_number,description)
	# def _createTransferChargesInvoice(self, partner_id, amount, current_id, plot_date, plot_file_no, plot_number, description):
	# 	invoice_recs            = self.env['account.invoice']
	# 	account_id              = self.env['account.account'].search([('code','=',110200)])
	# 	account_id_invoice_line = self.env['account.account'].search([('code','=',200000)])
	# 	invoice_line_data       = [
	# 	(0, 0,
	# 		{
	# 			'quantity': 1,
	# 			'name': description,
	# 			'account_id': account_id_invoice_line.id,
	# 			'price_unit': amount,
	# 			'plot_file_no' :plot_file_no,
	# 			'plot_number' : plot_number.id
	# 		}
	# 	)
	# 	]
	# 	res = {
	# 	'partner_id' : partner_id,
	# 	'account_id' : account_id.id,
	# 	'invoice_line_ids' : invoice_line_data,
	# 	'transfer_charges_id': current_id,
	# 	'date_invoice': plot_date,
	# 	'plot_inv_description': description,
	# 	'plot_file_no' : plot_file_no,
	# 	'plot_number' : plot_number.id
	# 	}
	# 	invoice_recs.create(res)

class plot_transfer_type(models.Model):
	_name = "plot.transfer.type"
	name = fields.Char('Name')



class plot_history(models.Model):
	_name = "plot.history"
	plot_from = fields.Char('From')
	plot_to = fields.Char('To')
	plot_date = fields.Date('Date')
	plot_allotment_no = fields.Char('Allotment Letter')
	plot_poss_no = fields.Char('Possession Letter')
	plot_transfer_ref = fields.Char('Transfer Reference')
	plot_sale_history_id = fields.Many2one('sale.order', 'Sale ID')
	plot_product_history_id = fields.Many2one('product.template', 'Product ID')



class plot_installment_plan(models.Model):
	_name = "plot.installment.plan"
	_rec_name = "record_name"
	record_name = fields.Char('Name')
	name = fields.Selection([
		('monthly','Monthly'),
		('quarterly','Quarterly'),
		('six_months','Six Months'),
		('bimonthly','Bimonthly'),
		('lump_sum','Lump sum')] , string="Installment Plan")
	plot_size_ids = fields.Many2one('plot.size', 'Plot Size')
	plot_no_installments = fields.Integer('No of Installments')
	amount = fields.Float('Amount')
	total_amount = fields.Float('Total Amount', required=True)
	advance_amount = fields.Float('Advance Amount')
	pipt_ids = fields.One2many('plot.installment.plan.tree','pip_id', 'PIPT IDS')
	stages = fields.Selection([
		('draft','Draft'),
		('validate','Validated')] , default="draft", string="Stages")

	@api.onchange('name','plot_size_ids')
	def getRecordName(self):
		if self.name and self.plot_size_ids:
			self.record_name = str(self.name)+" "+str(self.plot_size_ids.size)+" "+str(self.plot_size_ids.unit)
	@api.multi
	def genrate(self):
		if self.plot_no_installments:
			self.pipt_ids.unlink()
			for x in xrange(0,self.plot_no_installments):
				self.pipt_ids.create({
					'name':  "Installment No: "+str(x+1)+"",
					'amount': self.amount,
					'pip_id': self.id,
					})

	@api.multi
	def validate(self):
		if self.total_amount:
			if self.total_amount != sum(line.amount for line in self.pipt_ids):
				raise ValidationError("The Amount in Lines is not equal to total amount i.e %s" % self.total_amount)
			else:
				self.write({'stages': 'validate'})

	@api.onchange('advance_amount')
	def _onchange_advance_amount(self):
		total_amount = self.total_amount
		if self.advance_amount:
			self.total_amount = total_amount - self.advance_amount

	@api.onchange('plot_size_ids')
	def _onchange_plot_size_ids(self):
		if self.plot_size_ids:
			self.total_amount = self.plot_size_ids.price


class plot_installment_plan_tree(models.Model):
	_name = "plot.installment.plan.tree"
	name = fields.Char('Description')
	amount = fields.Float('Amount')
	pip_id = fields.Many2one('plot.installment.plan', 'PIP ID')
