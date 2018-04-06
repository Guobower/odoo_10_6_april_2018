# -*- coding: utf-8 -*- 
from odoo import models, fields, api
from openerp.exceptions import Warning
from openerp.exceptions import ValidationError


###########################################
#     Expense Module
###########################################

class ExpenseAccounting(models.Model):
  _name = "expense.accounting"
  _rec_name = "record_field"
  

  date = fields.Date(string = "Date", required = True)
  journal = fields.Many2one('account.journal', required = True)
  record_field = fields.Char()
  expense_treeview = fields.One2many('expense.accounting.tree','expense_accounting_id')


  @api.onchange('journal','date')
  def record_name(self):
  	self.record_field = str(self.date) +  " " +str(self.journal.name)

  @api.multi
  def validate(self):
	journal_entries_lines = self.env['account.move.line'].search([])
	for x in self.expense_treeview:
  		journal_entries = self.env['account.move'].search([('expense_id','=',x.id)])
		if not journal_entries:
			create_journal_entry = journal_entries.create({
				'journal_id':self.journal.id,
				'date':x.date,
				'expense_id':x.id
				})
			create_line = journal_entries_lines.create({
				'account_id':x.account.id,
				'name':x.description,
				'debit':x.amount,
				'move_id':create_journal_entry.id,
				})
			create_line = journal_entries_lines.create({
				'account_id':self.journal.default_credit_account_id.id,
				'name':x.description,
				'credit':x.amount,
				'move_id':create_journal_entry.id,
				})
		else:
			for y in journal_entries.line_ids:
				if y.debit ==0:
					y.credit=x.amount
					y.description = x.description

				if y.credit ==0:
					y.debit=x.amount
					y.description = x.description




class AccountMoveRemoveValidation(models.Model):
	_inherit = "account.move"

	expense_id = fields.Integer(string="Expense Id")

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



class ExpenseAccountingTree(models.Model):
	_name = "expense.accounting.tree"

	description = fields.Char(string="Expense Description", required = True)
	amount = fields.Float(string="Expense Amount")
	account = fields.Many2one('account.account')
	expense_accounting_id = fields.Many2one('expense.accounting')
  	date = fields.Date(string = "Date", default=fields.Date.context_today)
  	employee = fields.Many2one('hr.employee')



	@api.multi
	def unlink(self):
		super(ExpenseAccountingTree, self).unlink()		

		move_idss = self.env['account.move'].search([('expense_id','=',self.id)])
		move_idss.unlink()

		return True


class EarlyPaymentDiscount(models.Model):
    _inherit = "account.payment"



    discount_amount = fields.Float("Discount Amount")
    total_amount = fields.Float("Total Amount")
    pay_discount = fields.Boolean(string = "Pay Discount")
    @api.onchange('journal_id')
    def check_discount(self):
    	account = self.env['account.account'].search([('name','=',"Discount")])
    	if self.payment_date <= self.invoice_ids.date_due:
    		self.pay_discount = True
    		self.total_amount = self.invoice_ids.amount_total
    		self.discount_amount = self.total_amount * .05
    		self.amount = self.total_amount - self.discount_amount
    		self.payment_difference_handling = "reconcile"
    		self.writeoff_account_id = account.id

    @api.onchange('pay_discount')
    def remove_discount(self):
    	if self.pay_discount == False:
    		self.amount = self.total_amount



	