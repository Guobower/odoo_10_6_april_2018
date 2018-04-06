# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime, timedelta , date


class test2(models.Model):
	""" MAin FOrm class  """
	_name = 'saif.stock'
	_rec_name = 'date'


	date = fields.Date("Date",read=['portal.group_portal'], default=lambda self: fields.date.today())
	state = fields.Selection([('draft','Draft'),('validate',' Validate')],default='draft')
	saif_tree_link= fields.One2many('saif.stock.tree','part_id',read=['portal.group_portal'])

	@api.multi
	def validate(self):
		if self.state == 'draft':
			self.state = 'validate'

	@api.multi
	def reset(self):
		if self.state == 'validate':
			self.state = 'draft'



class saif_extension_tree(models.Model):
	""" tree class """
	_name = 'saif.stock.tree'

	# product = fields.Char(string='Product')
	product = fields.Many2one('product.product',string='Product')
	issued = fields.Float(string='Issued')
	received = fields.Float(string='Received')
	issued_to = fields.Char(string='Issued to')
	remarks = fields.Char(string='Remarks')
	part_id = fields.Many2one('saif.stock')
	date = fields.Date('Date',default=date.today())


	@api.onchange('issued')
	def get_issued(self):
		if self.issued:
			self.received = 0.00


	@api.onchange('received')
	def get_received(self):
		if self.received:
			self.issued = 0.00
