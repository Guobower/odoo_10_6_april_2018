# -*- coding: utf-8 -*-
from random import *
from datetime import datetime, timedelta
from odoo import models, fields, api


class taxes_champion(models.Model):
	_inherit = 'account.invoice'

	due_date      = fields.Date(string="Due Date")
	give_discount = fields.Boolean(string="Give Discount")
	days          = fields.Integer(string="Days")
	percent       = fields.Float(string="Percent")



	@api.onchange('date_invoice')
	def due_Date(self):
		if self.payment_term_id and self.date_invoice:
			start_date = datetime.strptime(self.date_invoice,"%Y-%m-%d")
			if self.payment_term_id.name == "15 Days":
				self.due_date = start_date + timedelta(days=15)
			elif self.payment_term_id.name == "30 Days":
				self.due_date = start_date + timedelta(days=30)
			elif self.payment_term_id.name == "60 Net Days":
				self.due_date = start_date + timedelta(days=60)
			elif self.payment_term_id.name == "90 Days":
				self.due_date = start_date + timedelta(days=90)
			else:
				self.due_date = self.date_invoice



class turkina_extend(models.Model):
	_inherit = 'sale.order'

	give_discount = fields.Boolean(string="Give Discount")
	days          = fields.Integer(string="Days")
	percent       = fields.Float(string="Percent")

class AccInvLineExt(models.Model):
	_inherit = 'account.invoice.line'

	afterTaxAmt = fields.Float(string='Tax Amount', required=False, digits=(6,3))

	@api.onchange('price_subtotal','quantity','price_unit','invoice_line_tax_ids')
	def onchange_price_subtotal(self):
		if self.invoice_line_tax_ids:
			amt = 0
			for x in self.invoice_line_tax_ids:
				tax = x.amount / 100
				amt =  amt + (tax * self.price_subtotal)
			self.afterTaxAmt = amt

class SaleLineExt(models.Model):
	_inherit = 'sale.order.line'

	afterTaxAmt = fields.Float(string='Tax Amount', required=False, digits=(6,3))

	@api.onchange('price_subtotal','product_uon_qty','price_unit','tax_id')
	def onchange_price_subtotal(self):
		if self.tax_id:
			amt = 0
			for x in self.tax_id:
				tax = x.amount / 100
				amt =  amt + (tax * self.price_subtotal)
			self.afterTaxAmt = amt


class ResPartnerExt(models.Model):
	_inherit = 'res.partner'

	vat = fields.Char(string="VAT", required=False, )


class ResCompanyExt(models.Model):
	_inherit = 'res.company'

	vat = fields.Char(string="VAT", required=False, )


class SaleOrderExt(models.Model):
	_inherit = 'sale.order'

	@api.multi
	def action_invoice_create(self):
		new_record = super(SaleOrderExt, self).action_invoice_create()
		rec =  self.env['sale.order.line'].search([('order_id', '=', self.id)])
		records = self.env['account.invoice'].search([('origin', '=', self.name)])
		if records:
			for x, y in map(None, records.invoice_line_ids, rec):
				x.afterTaxAmt = y.afterTaxAmt
		return new_record
