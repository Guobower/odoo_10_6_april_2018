# -*- coding: utf-8 -*- 
from odoo import models, fields, api
from openerp.exceptions import Warning
from openerp.exceptions import ValidationError
import datetime



class ProfitReport(models.Model): 
	_name 		 = 'profit.report' 
	_description = 'Profit Report'



	date_from = fields.Date(string = "Date From")
	date_to = fields.Date(string = "Date To")

	profit_lines = fields.One2many('profit.report.lines','profit_id')

	@api.multi
	def get_profit(self):
		profit_lines = self.env['profit.report.lines']
		products = self.env['product.template'].search([])
		self.profit_lines.unlink()
		for x in products:
			self.profit_lines.create({
				'mill':x.id,
				'profit_id':self.id
				})

		for y in self.profit_lines:
			total_sales = 0	
			total_sales_value = 0	
			sales = self.env['sales.sugar'].search([('mill','=',y.mill.id),('date','>=',self.date_from),('date','<=',self.date_to)])
			for qty in sales:
				total_sales = total_sales + qty.qty
				total_sales_value = total_sales_value + qty.total
			y.qty_sold = total_sales
			y.amount_sold = total_sales_value
			if y.qty_sold >0:
				y.sale_rate = y.amount_sold / y.qty_sold
			pre_purchases = self.env['purchase.sugar'].search([('mill','=',y.mill.id),('date','<',self.date_from)]).sorted(key=lambda r: r.date)
			pre_sales = self.env['sales.sugar'].search([('mill','=',y.mill.id),('date','<',self.date_from)]).sorted(key=lambda r: r.date)

		for prod in self.profit_lines:
			if prod.qty_sold == 0:
				prod.unlink()


class ProfitReportLines(models.Model): 
	_name 		 = 'profit.report.lines' 
	_description = 'Profit Report'


	mill		 = fields.Many2one('product.template')
	qty_sold			 = fields.Float(string="Quantity Sold",digits=(19,0))
	amount_sold			 = fields.Float(string="Sale Value",digits=(19,0))
	sale_rate		 = fields.Float(string="Average Sale Rate",digits=(19,0))
	purchase_rate		 = fields.Float(string="Average Purchase Rate",digits=(19,0))
	profit_unit = fields.Float(string ="Profit Per Unit")
	total_profit = fields.Float(string ="Total Profit")
	profit_id = fields.Many2one('profit.report')