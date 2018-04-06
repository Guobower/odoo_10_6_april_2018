#-*- coding:utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2011 OpenERP SA (<http://openerp.com>). All Rights Reserved
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###################################################
from openerp import models, fields, api
from datetime import timedelta,datetime,date
from dateutil.relativedelta import relativedelta
import time

class SampleDevelopmentReport(models.AbstractModel):
	_name = 'report.stock_report.customer_report'

	@api.model
	def render_html(self,docids, data=None):
		report_obj = self.env['report']
		report = report_obj._get_report_from_name('stock_report.customer_report')
		active_wizard = self.env['stocks.reports'].search([])
		emp_list = []
		for x in active_wizard:
			emp_list.append(x.id)
		emp_list = emp_list
		emp_list_max = max(emp_list) 

		record_wizard = self.env['stocks.reports'].search([('id','=',emp_list_max)])

		record_wizard_del = self.env['stocks.reports'].search([('id','!=',emp_list_max)])
		record_wizard_del.unlink()

		branch = record_wizard.branch
		product = record_wizard.product
		types = record_wizard.types
		
		rec = self.env['product.template'].search([('branch','=',record_wizard.branch.id)])

		if types == 'all':
			prod = []
			for x in rec:
				prod.append(x)

		if types == 'specfic':
			prod = []
			for x in product:
				prod.append(x)


		def get_purchase(attr):
			value = 0
			for x in rec:
				if x.id == attr:
					value = x.total_purchase

			return value


		def get_sale(attr):
			value = 0
			for x in rec:
				if x.id == attr:
					value = x.total_sale

			return value

		def get_remain(attr):
			value = 0
			for x in rec:
				if x.id == attr:
					value = x.remaining

			return value
		 


		docargs = {
		
			'doc_ids': docids,
			'doc_model': 'product.template',
			'branch': branch.name,
			'prod': prod,
			'get_purchase': get_purchase,
			'get_sale': get_sale,
			'get_remain': get_remain,
	
			}

		return report_obj.render('stock_report.customer_report', docargs)