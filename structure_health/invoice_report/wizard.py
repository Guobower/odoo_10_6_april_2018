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
##############################################################################
from openerp import models, fields, api


class InvoiceWiseDetail(models.Model):
	_name = "invoice.reports"

	date_from = fields.Date("Date From",required=True)
	date_to = fields.Date("Date To",required=True)
	branch = fields.Many2many("branch",string="Branch",required=True)
	types = fields.Selection([('all','All'),('specfic', 'Specfic')], string="Invoice Type", required=True)
	b_types = fields.Selection([('all','All'),('specfic', 'Specfic')], string="Branch Filter", required=True)
	type_of_invoice = fields.Selection([
			('normal','Normal'),
			('massage', 'Massage'),
			('minibar', 'MiniBar'),
			('rejoining', 'Rejoining'),
			('change_package', 'Change Package'),
		], string='Type Of Invoice')
	stage_of_invoice = fields.Selection([
			('draft','Draft'),
			('open', 'Open'),
			('new', 'Paid'),
		], string='Stage Of Invoice',required="True")







	
