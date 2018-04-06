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


class EncashmentDetail(models.Model):
	_name = "encashment.report"

	date_from = fields.Date("Date From",required=True)
	date_to = fields.Date("Date To",required=True)
	# rep_types = fields.Selection([('card','Card No'),('dep', 'Department')], string="Report Type", required=True)
	# card_types = fields.Selection([('all','All'),('sep', 'Specfic')], string="Filter Type")
	# dep_types = fields.Selection([('all','All'),('sep', 'Specfic')], string="Filter Type")
	# card_no = fields.Many2many("emp.card.num",string="Crad No")
	# depart = fields.Many2many("hr.department",string="Department")
	







	
