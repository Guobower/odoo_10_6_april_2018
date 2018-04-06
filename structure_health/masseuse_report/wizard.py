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


class MasseuseWiseDetail(models.Model):
	_name = "masseuse.reports"

	date_from = fields.Date("Date From",required=True)
	date_to = fields.Date("Date To",required=True)
	masseuse = fields.Many2many("hr.employee",string="Masseuse",required=True)
	branch = fields.Many2one("branch",string="Branch",required=True)
	stages = fields.Selection([
		('draft', 'Draft'),
		('booked', 'Booked'),
		('avail', 'Availed'),
		('cancel', 'Cancelled'),
	], string="Stages")







	
