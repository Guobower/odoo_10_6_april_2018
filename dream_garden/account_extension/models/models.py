# -*- coding: utf-8 -*-

from odoo import models, fields, api

class AccountExtension(models.Model):
	""" MAin FOrm class  """
	_inherit = 'account.bank.statement.line'

	paid = fields.Float(string='Paid')
	received = fields.Float(string='Received')
	proj	 = fields.Many2one('project.project',string='Project')
	account	 = fields.Many2one('account.account',string='Account')

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

# class AccountExtension_new(models.Model):
# 	""" MAin FOrm class  """
# 	_inherit = 'account.bank.statement'

# 	proj	 = fields.Many2one('project.project',string='Project', required=True)
# 	account	 = fields.Many2one('account.account',string='Acount', required=True)
