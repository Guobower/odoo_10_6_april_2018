from odoo import models, fields, api
from datetime import datetime, date, timedelta

class PartnerLedgerReport(models.AbstractModel):
	_name = 'report.daily_sale_purchase.daily_sale_purchase_report'

	@api.model
	def render_html(self,docids, data=None):

		report_obj = self.env['report']
		report = report_obj._get_report_from_name('daily_sale_purchase.daily_sale_purchase_report')
		active_wizard = self.env['daily.sale.purchase'].search([])
		emp_list = []
		for x in active_wizard:
			emp_list.append(x.id)
		emp_list = emp_list
		emp_list_max = max(emp_list) 

		record_wizard = self.env['daily.sale.purchase'].search([('id','=',emp_list_max)])
		record_wizard_del = self.env['daily.sale.purchase'].search([('id','!=',emp_list_max)])
		record_wizard_del.unlink()

		date = record_wizard.date
		print date

		products = []

		sales = self.env['sales.sugar'].search([('date','=',date)])
		purchases = self.env['purchase.sugar'].search([('date','=',date)])

		for x in sales:
			if x.mill not in products:
				products.append(x.mill)

		for x in purchases:
			if x.mill not in products:
				products.append(x.mill)

		
		print products

		purchase_lines = []
		def getpurchases(attr):
			del purchase_lines[:]
			lines = self.env['purchase.sugar'].search([('date','=',date),('mill.id','=',attr.id)])

			for x in lines:
				purchase_lines.append(x)

			len_purchase_lines = len(purchase_lines)

		sale_lines = []
		def getsales(attr):
			del sale_lines[:]
			lines = self.env['sales.sugar'].search([('date','=',date),('mill.id','=',attr.id)])

			for x in lines:
				sale_lines.append(x)

		def findlenght(attr):
			print attr
			print len(attr)
			return (len(attr))
			
		docargs = {
			'doc_ids': docids,
			'doc_model': 'res.partner',
			'data': data,
			'products': products,
			'getpurchases': getpurchases,
			'getsales': getsales,
			'purchase_lines': purchase_lines,
			'sale_lines': sale_lines,
			'findlenght': findlenght
		}

		return report_obj.render('daily_sale_purchase.daily_sale_purchase_report', docargs)