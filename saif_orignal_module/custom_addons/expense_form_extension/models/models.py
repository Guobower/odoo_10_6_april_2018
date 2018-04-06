# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import Warning, ValidationError

class saif_extension(models.Model):
	_name	='saif.extension'
	_rec_name = 'employee'

	employee 	 = fields.Many2one('hr.employee',string="Employee")
	date = fields.Date(string='Date', required=True)
	department	 = fields.Many2one('hr.department',string="Department")
	amount = fields.Float(string='Amount')
	returned = fields.Float(string='Returned')
	net = fields.Float(string='Net')
	payment_bank = fields.Boolean(string='Payment Through Bank')
	cash_book	 = fields.Many2one('account.bank.statement',string='Cash Book')
	s_bank	 = fields.Many2one('account.journal',string='Bank')
	s_counter	 = fields.Many2one('account.account',string='Counter Account')
	description	 = fields.Char(string='Description', required=True)
	e_currency	 = fields.Many2one('res.currency',string='Currency', required=True)
	proj	 = fields.Many2one('project.project',string='Project', required=True)
	saif_tree_link = fields.One2many('saif.ext.tree','part_id')
	seq = fields.Char("CE No.",readonly=True)

	@api.model
	def create(self, vals):
		vals['seq'] = self.env['ir.sequence'].next_by_code('ch.seq')
		new_record = super(saif_extension, self).create(vals) 
		return new_record


	state = fields.Selection([
		('exp', 'Expenses'),
		('adv', 'Advance'),
		('reim', 'Reimbursement'),
		('reim_sal', 'Reimbursement Salary'),
		('arr_sal', 'Arrears Salary'),
		('arr', 'Arrears'),
		],default='exp',string ="Type")

	status = fields.Selection([
		('draft', 'Draft'),
		('val', 'Validate'),
		],default='draft')

	@api.multi
	def val(self):
		self.status = "val"

		cash_enteries = self.env['account.bank.statement'].search([('journal_id.type','=',self.cash_book.journal_id.type),('proj.id','=',self.proj.id)])
		if cash_enteries:
			for x in cash_enteries.line_ids:
				if x.ref == self.seq:
					x.unlink()

		if cash_enteries:
			inv = []
			for invo in self.saif_tree_link:
				inv.append({
					'date':invo.expense_date,
					'name':invo.expense_note,
					'partner_id':self.employee.id,
					'ref':self.seq,
					'amount':invo.expense_amount,
					'line_ids':cash_enteries.id,
					})
			
			cash_enteries.line_ids = inv
			inv=[]


	@api.multi
	def cancel(self):
		self.status = "draft"

	@api.onchange('saif_tree_link')
	def on_change_amount(self):
		if self.saif_tree_link:
			self.amount = 0.0
			for x in self.saif_tree_link:
				self.amount = self.amount + x.expense_amount


class saif_extension_tree(models.Model):
	_name='saif.ext.tree'
	expense_date = fields.Date(string='Expense Date', required=True)
	expense_note = fields.Char(string='Expense Note', required=True)
	expense_amount = fields.Float("Total Amount")
	part_id = fields.Many2one('saif.extension')



class account_bank_extension(models.Model):
	_inherit = 'account.bank.statement'

	proj = fields.Many2one('project.project',string='Project', required=True)
	check = fields.Boolean(compute="check_status")
	hide_bol = fields.Boolean()

	@api.one
	def check_status(self):
		users = self.env['res.users'].search([('id','=',self._uid)])
		if users.branch_user == True:
			self.check = True

	@api.onchange('name')
	def get_proj(self):
		users = self.env['res.users'].search([('id','=',self._uid)])
		if users.branch_user == True:
			self.proj = users.proj.id
			self.hide_bol = True


	@api.multi
	def post(self):
		value = 0
		rec = self.env['account.journal'].search([('id','=',self.journal_id.id)])
		value = rec.default_debit_account_id.id
		journal_entries = self.env['account.move'].search([])
		journal_entries_lines = self.env['account.move.line'].search([])
		for x in self.line_ids:
			if x.account and x.e_check == False:
				create_journal = journal_entries.create({
					'journal_id': self.journal_id.id,
					'date':self.date,
					'ref' : self.name,
					})

				if x.received > 0.00 and x.paid == 0.00:

					b = journal_entries_lines.create({
						'account_id':x.account.id,
						'partner_id':x.partner_id.id,
						'name':x.name,
						'voucher_no':x.voucher_no,
						'payess_name':x.payess_name.id,
						'proj':x.proj.id,
						'debit':x.received,
						'credit':0.0,
						'move_id':create_journal.id,
						})

					c = journal_entries_lines.create({
						'account_id':value,
						'partner_id':x.partner_id.id,
						'name':x.name,
						'voucher_no':x.voucher_no,
						'payess_name':x.payess_name.id,
						'proj':x.proj.id,
						'debit':0.0,
						'credit':x.received,
						'move_id':create_journal.id,
						})

					x.ecube_journal = create_journal.id
					x.e_check = True

				if x.paid > 0.00 and x.received == 0.00:

					b = journal_entries_lines.create({
						'account_id':x.account.id,
						'partner_id':x.partner_id.id,
						'name':x.name,
						'voucher_no':x.voucher_no,
						'payess_name':x.payess_name.id,
						'proj':x.proj.id,
						'debit':0.0,
						'credit':x.paid,
						'move_id':create_journal.id,
						})

					c = journal_entries_lines.create({
						'account_id':value,
						'partner_id':x.partner_id.id,
						'name':x.name,
						'voucher_no':x.voucher_no,
						'payess_name':x.payess_name.id,
						'proj':x.proj.id,
						'debit':x.paid,
						'credit':0.0,
						'move_id':create_journal.id,
						})

					x.ecube_journal = create_journal.id
					x.e_check = True

	@api.model
	def create(self, vals):
		new_record = super(account_bank_extension, self).create(vals)
		rec = self.env['account.bank.statement'].search([])
		for x in rec:
			if x.proj.id == new_record.proj.id:
				for y in x.line_ids:
					if y.statement_id.id != new_record.id:
						if y.e_check == False:
							raise  ValidationError('Post Pending Enteries In Previous Cash Books')

		return new_record


class account_bank_extension_line(models.Model):
	_inherit = 'account.bank.statement.line'


	voucher_no  = fields.Char(string="Voucher No.")
	payess_name = fields.Many2one('res.partner',string="Payees Name")
	account = fields.Many2one('account.account',string="Account")
	ecube_journal = fields.Many2one('account.move',string="Journal")
	proj = fields.Many2one('project.project',string='Project')
	e_check = fields.Boolean()
	check_val = fields.Boolean()
	paid = fields.Float(string='Paid')
	received = fields.Float(string='Received')

	@api.onchange('date')
	def get_hide(self):
		users = self.env['res.users'].search([('id','=',self._uid)])
		if users.branch_user == True:
			self.check_val = True


	
	@api.onchange('paid')
	def paid_amount(self):
		negative=-1
		if self.paid:
			self.amount= self.paid * negative
			self.received=0

	@api.onchange('received')
	def received_amount(self):
		if self.received:
			self.amount= self.received
			self.paid=0

	@api.multi
	def unlink(self):
		if self.e_check == True:
			raise  ValidationError('Post Pending')

		super(account_bank_extension_line, self).unlink()

		return True






	# employee = fields.Many2one('hr.employee',string="Employee")

	# @api.multi
	# def process_reconciliation(self,data,uid,id):
	# 	new_record = super(account_bank_extension_line, self).process_reconciliation(data,uid,id)
	# 	records = self.env['account.bank.statement.line'].search([('id','=',self.id)])
	# 	journal_entery =  self.env['account.move'].search([], order='id desc', limit=1)
	# 	for x in journal_entery.line_ids:
	# 		x.voucher_no = records.voucher_no
	# 		x.payess_name = records.payess_name.id
	# 		x.employee = records.employee.id
	# 	return new_record

class account_move_line(models.Model):
	_inherit = 'account.move.line'

	voucher_no = fields.Char(string="Voucher No.")
	payess_name = fields.Many2one('res.partner',string="Payees Name")
	proj = fields.Many2one('project.project',string='Project')

	# employee = fields.Many2one('hr.employee',string="Employee")

class account_move_extend(models.Model):
	_inherit = 'account.move'

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



class user_extend(models.Model):
	_inherit = 'res.users'

	proj = fields.Many2one('project.project',string='Project')
	branch_user = fields.Boolean(string="Branch User") 


	


