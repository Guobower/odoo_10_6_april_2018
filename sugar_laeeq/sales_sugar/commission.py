# -*- coding: utf-8 -*- 
from odoo import models, fields, api
from openerp.exceptions import Warning
from openerp.exceptions import ValidationError
import datetime



class SugarCommission(models.Model): 
	_name 		 = 'sugar.commission' 
	_description = 'Sugar Commission'



	date = fields.Date()
	transaction_type = fields.Char(string = "Commission Type")
	party	     = fields.Many2one('res.partner',string = "Party")
	mill		 = fields.Many2one('product.template',required=True)
	qty			 = fields.Float(string="Quantity",digits=(19,0))
	rate		 = fields.Float(string="Rate",digits=(19,0))
	total		 = fields.Float(string="Amount", compute ="get_total",store = True,digits=(19,0))
	commission_agent = fields.Many2one('res.partner', string ="Commission Agent")
	comm_type = fields.Selection([('no', 'No'),('rec', 'Received'), ('paid', 'Paid')],string = "Comm Rate")
	comm_amount = fields.Float(string = "Comm Amount", compute ="get_total",store = True,digits=(19,0))
	comm_rate = fields.Float(string = "Comm Rate",digits=(19,0))
	sale_id = fields.Integer()
	purchase_id = fields.Integer()
	cleared = fields.Boolean()
	commission_bill_id = fields.Many2one('sugar.commission')

	state       = fields.Selection([('draft', 'Draft'),('clearance', 'Sent for Clearance'), ('validate', 'Validate'), ('cancelled', 'Cancel')],default = "draft" )




	@api.one
	@api.depends('qty','rate','comm_rate','commission_agent')
	def get_total(self):
		self.total = self.qty * self.rate
		self.comm_amount = self.qty * self.comm_rate

class SugarCommissionBills(models.Model): 
	_name 		 = 'sugar.commission.bill' 
	_description = 'Sugar Commission Bill' 


	date = fields.Date(required = True)
	last_date = fields.Date(required = True)
	party	     = fields.Many2one('res.partner',string = "Party", required = True)
	state       = fields.Selection([('draft', 'Draft'),('posted', 'Sent for Clearance'), ('validate', 'Validate'), ('cancelled', 'Cancel')],default = "draft" )


	commissions = fields.One2many('sugar.commission','commission_bill_id')


	@api.multi
	def get_commissions(self):
		for x in self.commissions:
			x.commission_bill_id = False
		commissions = self.env['sugar.commission'].search([('party','=',self.party.id),('date','<=',self.last_date),('state','in',["draft","clearance"])])
		for x in commissions:
			x.commission_bill_id = self.id


	@api.multi
	def send_for_clearance(self):
		for x in self.commissions:
			x.state = "clearance"
			x.cleared = True