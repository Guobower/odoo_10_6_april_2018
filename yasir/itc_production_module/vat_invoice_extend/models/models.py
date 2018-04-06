# -*- coding: utf-8 -*-
from openerp import models, fields, api

class AccInvLineExt(models.Model):
	_inherit = 'account.invoice.line'

	afterTaxAmt = fields.Float(string='Tax Amount', required=False, digits=(6,3))

	@api.onchange('price_subtotal','quantity','price_unit','invoice_line_tax_id')
	def onchange_price_subtotal(self):
		if self.invoice_line_tax_id:
			amt = 0
			for x in self.invoice_line_tax_id:
				amt =  amt + (self.invoice_line_tax_id.amount * self.price_subtotal)
			self.afterTaxAmt = amt

class SaleLineExt(models.Model):
	_inherit = 'sale.order.line'

	afterTaxAmt = fields.Float(string='Tax Amount', required=False, digits=(6,3))

	@api.onchange('price_subtotal','product_uom_qty','tax_id','price_unit','discount')
	def onchange_price_subtotal(self):
		if self.tax_id:
			amt = 0.0
			disAmt = 0.0
			for x in self.tax_id:
				if self.discount > 0.0:
					disAmt = (1 - (self.discount/100)) * self.product_uom_qty * self.price_unit
					amt =  amt + (disAmt * (self.tax_id.amount))
				if self.discount == 0.0:
					amt =  amt + (self.tax_id.amount * self.product_uom_qty * self.price_unit)
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
			for x, y in map(None, records.invoice_line, rec):
				x.afterTaxAmt = y.afterTaxAmt
		return new_record
