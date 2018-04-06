# -*- coding: utf-8 -*- 
from odoo import models, fields, api


####################   Customer Payments #######################################

class customer_payments_sugar(models.Model): 
	_name 		 = 'customer.payments.sugar' 
	_description = 'Customer Payments'
	_rec_name = 'date'


	date = fields.Date(required=True, default=fields.Date.context_today)
	total_amount = fields.Float()
	stages                  = fields.Selection([
		('draft', 'Draft'),
		('posted', 'Posted'),
		],string = "Stages", default = 'draft')

	payments_tree = fields.One2many('customer.payments.tree','customer_payments_id')


	@api.onchange('payments_tree')
	def get_total(self):
		total = 0
		for x in self.payments_tree:
			total = total + x.amount
		self.total_amount = total

	
	@api.multi
	def reset_draft(self):
		self.stages = "draft"


	@api.multi
	def post_entries(self):
		self.stages = "posted"
		journal_entries_lines = self.env['account.move.line'].search([])
		for lines in self.payments_tree:
			journal_entries = self.env['account.move'].search([('customer_payment_id','=',lines.id)])
			if not journal_entries:
				create_journal_entry = journal_entries.create({
						'journal_id': 2,
						'date':self.date,
						'customer_payment_id':lines.id,
						})
				create_debit = journal_entries_lines.create({
					'account_id':lines.bank.id,
					'partner_id':lines.customer.id,
					'name':"Received" + " "+ str(lines.amount) + "  " + "From" + "  "+str(lines.customer.name)+ " in " + str(lines.bank.code)+str(lines.bank.name)+  " "  + str(lines.remarks if lines.remarks else ""), 
					'debit':lines.amount,
					'move_id':create_journal_entry.id
					})
				create_credit = journal_entries_lines.create({
					'account_id':7,
					'partner_id':lines.customer.id,
					'name':"Received" + " "+ str(lines.amount) + "  " + "From" + "  "+str(lines.customer.name)+ " in " + str(lines.bank.code)+str(lines.bank.name)+  " "  + str(lines.remarks if lines.remarks else ""),  
					'credit':lines.amount,
					'move_id':create_journal_entry.id
					})
			else:
				for y in journal_entries.line_ids:
					if y.debit > 0 and y.credit ==0:
						y.account_id = lines.bank.id
						y.partner_id = lines.customer.id
						y.name = "Received" + " "+ str(lines.amount) + "  " + "From" + "  "+str(lines.customer.name)+ " in " + str(lines.bank.code) +str(lines.bank.name)+  " "  + str(lines.remarks if lines.remarks else "")
						y.debit = lines.amount
					else:
						y.partner_id = lines.customer.id
						y.name = "Received" + " "+ str(lines.amount) + "  " + "From" + "  "+str(lines.customer.name)+ " in " + str(lines.bank.code) +str(lines.bank.name)+  " "  + str(lines.remarks if lines.remarks else "")
						y.credit = lines.amount

class customer_payments_tree(models.Model): 
	_name 		 = 'customer.payments.tree'


	customer = fields.Many2one('res.partner', required = True)
	amount = fields.Float()
	bank = fields.Many2one('account.account')
	remarks = fields.Char()

	customer_payments_id = fields.Many2one('customer.payments.sugar')

	@api.multi
	def unlink(self):
		super(customer_payments_tree, self).unlink()

		journal_delete = self.env['account.move'].search([('customer_payment_id','=',self.id)])
		journal_delete.unlink()

		return True

	




####################   Supplier Payments #######################################

class customer_payments_sugar(models.Model): 
	_name 		 = 'supplier.payments.sugar' 
	_description = 'Supplier Payments'
	_rec_name = 'date'


	date = fields.Date(required=True, default=fields.Date.context_today)
	total_amount = fields.Float()
	stages                  = fields.Selection([
		('draft', 'Draft'),
		('posted', 'Posted'),
		],string = "Stages", default = 'draft')

	payments_tree = fields.One2many('supplier.payments.tree','supplier_payments_id')


	@api.onchange('payments_tree')
	def get_total(self):
		total = 0
		for x in self.payments_tree:
			total = total + x.amount
		self.total_amount = total

	@api.multi
	def reset_draft(self):
		self.stages = "draft"
		
	@api.multi
	def post_entries(self):
		self.stages = "posted"
		journal_entries_lines = self.env['account.move.line'].search([])
		for lines in self.payments_tree:
			journal_entries = self.env['account.move'].search([('supplier_payment_id','=',lines.id)])
			if not journal_entries:
				create_journal_entry = journal_entries.create({
						'journal_id': 2,
						'date':self.date,
						'supplier_payment_id':lines.id,
						})
				create_debit = journal_entries_lines.create({
					'account_id':13,
					'partner_id':lines.supplier.id,
					'name':"Paid" + " "+ str(lines.amount) + "  " + "To" + "  "+str(lines.supplier.name), 
					'debit':lines.amount,
					'move_id':create_journal_entry.id
					})
				create_credit = journal_entries_lines.create({
					'account_id':lines.payment_from.id,
					'partner_id':lines.supplier.id,
					'name':"Paid" + " "+ str(lines.amount) + "  " + "To" + "  "+str(lines.supplier.name),  
					'credit':lines.amount,
					'move_id':create_journal_entry.id
					})
			else:
				for y in journal_entries.line_ids:
					if y.credit > 0 and y.debit ==0:
						y.account_id = lines.payment_from.id
						y.partner_id = lines.supplier.id
						y.name = "Paid" + " "+ str(lines.amount) + "  " + "To" + "  "+str(lines.supplier.name) 
						y.credit = lines.amount
						 
					else:
						y.partner_id = lines.supplier.id
						y.name = "Paid" + " "+ str(lines.amount) + "  " + "To" + "  "+str(lines.supplier.name)
						y.debit = lines.amount
						


class supplier_payments_tree(models.Model): 
	_name 		 = 'supplier.payments.tree'


	supplier = fields.Many2one('res.partner',required = True)
	amount = fields.Float()
	bank = fields.Many2one('banks.pakistan')
	remarks = fields.Char()
	payment_from = fields.Many2one('account.account', string = "Bank")

	supplier_payments_id = fields.Many2one('supplier.payments.sugar')

	@api.multi
	def unlink(self):
		super(supplier_payments_tree, self).unlink()

		journal_delete = self.env['account.move'].search([('supplier_payment_id','=',self.id)])
		journal_delete.unlink()

		return True


class banks_pakistan(models.Model): 
	_name 		 = 'banks.pakistan'

	name = fields.Char()



####################   Inter Party Payments #######################################

class inter_payments_sugar(models.Model): 
	_name 		 = 'inter.payments.sugar' 
	_description = 'Inter Party Payments'
	_rec_name = 'date'


	date = fields.Date(required=True, default=fields.Date.context_today)
	total_amount = fields.Float()
	stages                  = fields.Selection([
		('draft', 'Draft'),
		('posted', 'Posted'),
		],string = "Stages", default = 'draft')

	payments_tree = fields.One2many('inter.payments.tree','inter_payments_id')


	@api.onchange('payments_tree')
	def get_total(self):
		total = 0
		for x in self.payments_tree:
			total = total + x.amount
		self.total_amount = total


	@api.multi
	def reset_draft(self):
		self.stages = "draft"
		
	@api.multi
	def post_entries(self):
		self.stages = "posted"
		journal_entries_lines = self.env['account.move.line'].search([])
		for lines in self.payments_tree:
			journal_entries = self.env['account.move'].search([('inter_payment_id','=',lines.id)])
			if not journal_entries:
				create_journal_entry = journal_entries.create({
						'journal_id': 2,
						'date':self.date,
						'inter_payment_id':lines.id,
						})
				create_debit = journal_entries_lines.create({
					'account_id':13,
					'partner_id':lines.to.id,
					'name':"Payment from" + " "+ str(lines.payment_from.name) + "  " + "To" + "  "+str(lines.to.name), 
					'debit':lines.amount,
					'move_id':create_journal_entry.id
					})
				create_credit = journal_entries_lines.create({
					'account_id':7,
					'partner_id':lines.to.id,
					'name':"Payment from" + " "+ str(lines.payment_from.name) + "  " + "To" + "  "+str(lines.to.name),  
					'credit':lines.amount,
					'move_id':create_journal_entry.id
					})
			else:
				for y in journal_entries.line_ids:
					if y.credit > 0 and y.debit ==0:
						y.partner_id = lines.payment_from.id
						y.name = "Payment from" + " "+ str(lines.payment_from.name) + "  " + "To" + "  "+str(lines.to.name)
						y.credit = lines.amount
						 
					else:
						y.partner_id = lines.to.id
						y.name = "Payment from" + " "+ str(lines.payment_from.name) + "  " + "To" + "  "+str(lines.to.name)
						y.debit = lines.amount

		


class inter_payments_tree(models.Model): 
	_name 		 = 'inter.payments.tree'


	to = fields.Many2one('res.partner',required = True)
	payment_from = fields.Many2one('res.partner',required = True,string = "From")
	amount = fields.Float()
	bank = fields.Many2one('banks.pakistan')
	remarks = fields.Char()

	inter_payments_id = fields.Many2one('inter.payments.sugar')


class banks_pakistan(models.Model): 
	_name 		 = 'banks.pakistan'

	name = fields.Char()