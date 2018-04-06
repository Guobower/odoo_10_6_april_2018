# -*- coding: utf-8 -*-
# 
# OpenERP, Open Source Management Solution
# Copyright (C) 2004-2010 OdooTec (<http://odootec.com>).
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
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
from datetime import datetime
from dateutil.relativedelta import relativedelta
import time
from .. import utils


class hr_holiday(models.Model):
    _inherit = 'hr.holidays'

    def _check_date(self, cr, uid, ids, context=None):
        for holiday in self.browse(cr, uid, ids, context=context):
            domain = [
                ('date_from', '<=', holiday.date_to),
                ('date_to', '>=', holiday.date_from),
                ('employee_id', '=', holiday.employee_id.id),
                ('id', '!=', holiday.id),
                ('type', '=', holiday.type),
                ('state', 'not in', ['cancel', 'refuse']),
            ]
            nholidays = self.search_count(cr, uid, domain, context=context)
            if nholidays:
                return False
        return True

    _constraints = [
        (_check_date, 'You can not have 2 leaves that overlaps on same day!', ['date_from', 'date_to']),
    ]

    def run_monthly_scheduler(self, cr, uid, context=None):
        """ Runs at the end of every month to allocate Leaves to all
        eligible employees.
        """
        vals = {}
        employee_obj = self.pool.get('hr.employee')
        employee_ids = employee_obj.search(cr, uid, [('eligible', '=', True)], context=context)
        for emp in employee_obj.browse(cr, uid, employee_ids, context=context):
            if emp.eligible and emp.holiday_line_ids:
                for line in emp.holiday_line_ids:
                    if line.allocation_range == 'month':
                        date_from_dt = datetime.now() - relativedelta(months=1) + relativedelta(day=1)
                        date_to_dt = datetime.now() - relativedelta(months=1) + relativedelta(day=31)
                        date_from = datetime.strftime(date_from_dt, '%Y-%m-%d')
                        date_to = datetime.strftime(date_to_dt, '%Y-%m-%d')
                        allocate_ids = self.search(cr, uid, [('date_from', '>=', date_from),
                                                             ('date_to', '<=', date_to),
                                                             ('type', '=', 'add'),
                                                             ('employee_id', '=', emp.id),
                                                             ('holiday_status_id', '=', line.leave_status_id.id)],
                                                   context=context)

                        if allocate_ids:
                            continue
                        if emp.joining_date:
                            joining_date = datetime.strptime(emp.joining_date, '%Y-%m-%d')
                        elif emp.contract_id:
                            joining_date = datetime.strptime(emp.contract_id.date_start, '%Y-%m-%d')
                        else:
                            continue
                        if joining_date <= date_to_dt:
                            if date_from_dt < joining_date <= date_to_dt:
                                days_to_allocate = (line.days_to_allocate / 30) * (date_to_dt.day - joining_date.day + 1)
                            else:
                                days_to_allocate = line.days_to_allocate
                            vals = {
                                'name': 'Monthly Allocation of ' + line.leave_status_id.name + ' Leaves',
                                'number_of_days_temp': days_to_allocate,
                                'date_from': date_from,
                                'date_to': date_to,
                                'employee_id': emp.id,
                                'holiday_status_id': line.leave_status_id.id,
                                'type': 'add',
                            }
                    if line.allocation_range == 'year':
                        date_from_dt = datetime.now() - relativedelta(years=1) + relativedelta(month=1) \
                                       + relativedelta(day=1)
                        date_to_dt = datetime.now() - relativedelta(years=1) \
                                     + relativedelta(month=12) + relativedelta(day=31)
                        date_from = datetime.strftime(date_from_dt, '%Y-%m-%d')
                        date_to = datetime.strftime(date_to_dt, '%Y-%m-%d')
                        allocate_ids = self.search(cr, uid, [('date_from', '>=', date_from),
                                                             ('date_to', '<=', date_to),
                                                             ('type', '=', 'add'),
                                                             ('employee_id', '=', emp.id),
                                                             ('holiday_status_id', '=', line.leave_status_id.id)],
                                                   context=context)
                        if allocate_ids:
                            continue
                        if emp.joining_date:
                            joining_date = datetime.strptime(emp.joining_date, '%Y-%m-%d')
                        elif emp.contract_id:
                            joining_date = datetime.strptime(emp.contract_id.date_start, '%Y-%m-%d')
                        else:
                            continue
                        if joining_date <= date_to_dt:
                            if date_from_dt < joining_date <= date_to_dt:
                                days_to_allocate = (line.days_to_allocate / 360) * (date_to_dt.day - joining_date.day + 1)
                            else:
                                days_to_allocate = line.days_to_allocate

                            vals = {
                                'name': 'Yearly Allocation of ' + line.leave_status_id.type + ' Leaves',
                                'number_of_days_temp': days_to_allocate,
                                'employee_id': emp.id,
                                'holiday_status_id': line.leave_status_id.id,
                                'type': 'add',
                            }
                    if vals:
                        leave_id = self.create(cr, uid, vals, context=context)
                        self.holidays_validate(cr, uid, [leave_id], context=context)
