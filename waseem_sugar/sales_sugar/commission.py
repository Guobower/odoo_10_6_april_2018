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