# -*- coding: utf-8 -*-
# 
# OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 OdooTec (<http://odootec.com>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.     
#

from openerp import models, fields, api, _
import time


class hr_employee(models.Model):
    _inherit = 'hr.employee'

    eligible = fields.Boolean(string='Eligible for Leave?', readonly=False)
    holiday_line_ids = fields.One2many('hr.employee.leave.line', 'employee_id', 'Holiday Lines')


class hr_employee_leave_lines(models.Model):
    _name = 'hr.employee.leave.line'

    leave_status_id = fields.Many2one('hr.holidays.status', 'Leave Type', required=True)
    allocation_range = fields.Selection([('month', 'Month'), ('year', 'Year')],
                                        'Allocate automatic leaves every', required=True,
                                        help="Periodicity on which you want automatic allocation of leaves to eligible employees.")
    days_to_allocate = fields.Float('Days to Allocate',
                                    help="In automatic allocation of leaves, " \
                                         "given days will be allocated every month / year.")
    employee_id = fields.Many2one('hr.employee', ondelete='cascade')