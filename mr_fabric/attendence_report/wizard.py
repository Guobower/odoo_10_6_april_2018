# #-*- coding:utf-8 -*-
# ##############################################################################
# #
# #    OpenERP, Open Source Management Solution
# #    Copyright (C) 2011 OpenERP SA (<http://openerp.com>). All Rights Reserved
# #
# #    This program is free software: you can redistribute it and/or modify
# #    it under the terms of the GNU Affero General Public License as published by
# #    the Free Software Foundation, either version 3 of the License, or
# #    (at your option) any later version.
# #
# #    This program is distributed in the hope that it will be useful,
# #    but WITHOUT ANY WARRANTY; without even the implied warranty of
# #    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# #    GNU Affero General Public License for more details.
# #
# #    You should have received a copy of the GNU Affero General Public License
# #    along with this program.  If not, see <http://www.gnu.org/licenses/>.
# #
# ##############################################################################
from odoo import models, fields, api
from datetime import date
from datetime import date, timedelta
import datetime
from openerp.exceptions import Warning, ValidationError, UserError

class GeneratesAttendenceReport(models.Model):
	_name = "attend.report"

	employee = fields.Many2many('hr.employee',string="Employee")
	department = fields.Many2one('hr.department',string="Department")
	form = fields.Date(string="From")
	to = fields.Date(string="To")
	typed = fields.Selection([
		('all','All'),
		('department','Department Wise'),
		('specific','Specific'),
		],string='Employee(s)',default='all')

	@api.onchange('form','to')
	def onchange_namecard(self):
		if self.form and self.to:
			d1 = datetime.datetime.strptime(self.form, "%Y-%m-%d")
			d2 = datetime.datetime.strptime(self.to, "%Y-%m-%d")

			delta = (d2 - d1)
			if str(delta) > "31 days 0:00:00":
				remaining_date = delta - timedelta(days=31)
				print remaining_date
				required_date = d2 - remaining_date
				self.to = required_date
				return {'value':{}, 'warning':{
				'title': 'Warning', 'message': 'You can not add days more than 31.'}}