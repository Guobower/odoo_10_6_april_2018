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


class RegionWiseDetail(models.Model):
	_name = "membership.reports"

	date_from = fields.Date("Date From")
	date_to = fields.Date("Date To")
	branch = fields.Many2one("branch",string="Branch",required=True)
	types = fields.Selection([('active', 'Active Member'), ('nonactive', 'Non Active Member'),('discontinue', 'Discontinue Member'),('new', 'New Member'),('diet', 'Diet Plan Member'),('health', 'Health Assessment Member'),('package', 'Package Wise Member'),('premium', 'Premium Member'),('daily','Daily Base Member'),('temp', 'Temporary Base Member')], string="Report Type", required=True)
	package_type = fields.Many2one('package.type',string="Package Type")
	tick = fields.Boolean()


	@api.onchange('types')
	def get_type(self):
		if self.types:
			if self.types == 'discontinue' or self.types == 'new':
				self.tick = True
			else:
				self.tick = False






	
