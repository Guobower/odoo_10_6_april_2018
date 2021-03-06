# -*- coding: utf-8 -*-
import re
from openerp import models, fields, api

class DailyForm(models.Model):
	_name = 'daily.production'
	_rec_name = 'date'

	date = fields.Date(string="Date",required=True)
	daily_id = fields.One2many('daily.production.tree','daily_tree')
	daily_consump = fields.One2many('daily.consumption.tree','daily_tree_consume',readonly=True)

	# @api.multi
	# def orignal_qty(self):
	# 	record=self.env['daily.production'].search([])
	# 	for x in record:
	# 		for z in x.daily_id:
	# 			z.qty=z.qty_kg
	@api.multi
	def get_data(self):
		self.daily_consump.unlink()
		records = []
		for x in self.daily_id:
			for z in self.daily_consump:
				records.append(z.product.id)
			for y in x.product.product_receipe.receipe_id:
				if y.product:
					value = y.ratio * x.qty_lit
					new = y.ratio * x.qty_kg
					value = value / 100
					new = new / 100
					if y.product.id not in records:
						create_record = self.env['daily.consumption.tree'].create({
							'product':y.product.id,
							'qty_lit':value,
							'qty_kg':new,
							'date':self.date,
							'daily_tree_consume':self.id
							})
					else:
						for line in self.daily_consump:
							if line.product.id == y.product.id:
								line.qty_lit = line.qty_lit + value
								line.qty_kg = line.qty_kg + new



class DailyFormTree(models.Model):
	_name = 'daily.production.tree'

	product = fields.Many2one('product.product',string="Product",required=True)
	uom = fields.Selection([
		('Ltr', 'Ltr'),
		('Ml', 'Ml'),
		('Kg', 'Kg'),
		('G', 'G'),
		('Mg','Mg'),], string='Uom',required=True)
	qty_kg = fields.Float(string="Quantity(Kg)",default=1.00)
	rate = fields.Float(string="Consumption Rate")
	qty = fields.Float(string="Quantity")
	qty_lit = fields.Float(string="Quantity(Litre)",default=1.00)
	date = fields.Date(string="Date")
	daily_tree = fields.Many2one('daily.production')

	@api.onchange('product')
	def get_date(self):
		if self.product:
			self.date = self.daily_tree.date

	@api.onchange('qty')
	def get_qty(self):
		new = 0
		if self.product:
			if self.product.attribute_value_ids:
				for x in self.product.attribute_value_ids:
					if x.attribute_id.name == 'size' or "Size":
						if re.findall(r"[-+]?\d*\.\d+|\d+", x.name):
							n = float(re.findall("[-+]?\d*\.\d+|\d+", x.name)[0])
							if self.uom == 'Ltr':
								self.qty_lit = self.qty * float(n)
								if self.product.product_receipe.wpl:
									self.qty_kg = self.qty_lit / float(self.product.product_receipe.wpl)
							if self.uom == 'Ml':
								n = n * 1000
								self.qty_lit = self.qty * float(n)
								if self.product.product_receipe.wpl:
									self.qty_kg = self.qty_lit / float(self.product.product_receipe.wpl)
							if self.uom == 'Kg':
								self.qty_kg = self.qty * float(n)
								if self.product.product_receipe.wpl:
									self.qty_lit = self.qty_kg * float(self.product.product_receipe.wpl)
							if self.uom == 'G':
								n = n * 1000
								self.qty_kg = self.qty * float(n)
								if self.product.product_receipe.wpl:
									self.qty_lit = self.qty_kg * float(self.product.product_receipe.wpl)
							if self.uom == 'Mg':
								n = n * 1000000
								self.qty_kg = self.qty * float(n)
								if self.product.product_receipe.wpl:
									self.qty_lit = self.qty_kg * float(self.product.product_receipe.wpl)





	# @api.onchange('qty_lit','qty_kg')
	# def get_value(self):
	# 	if self.product:
	# 		print "22xxxxxxxxxxxxxxxxxxxxxxxxxxxx"
	# 		if self.product.product_receipe.wpl:
	# 			print "zzzzzzzzzzzzzzzzzzzzzzzzzzzzz"
	# 			if self.uom == "Ltr" or "Ml":
	# 				self.qty_kg = self.qty_lit / self.product.product_receipe.wpl
	# 			if self.uom == "Kg" or "G" or "Mg":
	# 				print "112122232345fdfd"
	# 				print self.qty_kg
	# 				print float(self.product.product_receipe.wpl)
	# 				self.qty_lit = self.qty_kg * float(self.product.product_receipe.wpl)
	# 				print self.qty_lit



class DailyConsumeTree(models.Model):
	_name = 'daily.consumption.tree'

	product = fields.Many2one('product.product',string="Product")
	qty_kg = fields.Float(string="Qunatity(Kg)")
	qty_lit = fields.Float(string="Qunatity(Litre)")
	date = fields.Date(string="Date")
	daily_tree_consume = fields.Many2one('daily.production')



