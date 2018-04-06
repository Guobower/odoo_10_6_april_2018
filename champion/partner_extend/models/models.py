# -*- coding: utf-8 -*-

from odoo import models, fields, api

class partner_champion(models.Model):
	_inherit = 'res.partner'

	tax_payment = fields.Many2many('account.tax',string="Tax on Payments")
	buyer_type  = fields.Selection([
		('Registered','Registered'),
		('Unregistered','Unregistered')
		],string="Buyer Type")
   # filer_type   = fields.Selection([('filer', 'Filer'),('nonfiler', 'Non Filer')],string="Type")
	filer_type = fields.Selection([('filer', 'Filer'), ('nonfiler', 'Non Filer')], string="Type", default='filer')

class tax_champion(models.Model):
	_inherit = 'account.tax'


	payment_sec = fields.Char(string="Payment Section")


class fiscal_champion(models.Model):
	_inherit = 'account.fiscal.position'

	nonfiler = fields.Boolean(string="Non Filer")