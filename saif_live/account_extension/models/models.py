# -*- coding: utf-8 -*-

from odoo import models, fields, api

class AccountExtension(models.Model):
	""" MAin FOrm class  """
	_inherit = 'account.bank.statement.line'

	paid = fields.Float(string='Paid')
	received = fields.Float(string='Received')
	proj	 = fields.Many2one('project.project',string='Project', required=True)

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
