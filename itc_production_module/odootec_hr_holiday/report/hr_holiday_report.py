# -*- coding: utf-8 -*-
#
# Cybrosys <http://www.odootec.com>, Copyright (C) 2015 - Today.
#
# This program is free software: you can redistribute it and/or modify
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

from openerp.report import report_sxw
from openerp import api, models
from datetime import timedelta, datetime


class HrHolidaysParser(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context=None):
        super(HrHolidaysParser, self).__init__(cr, uid, name, context=context)
        self.localcontext.update({
            'get_data': self._get_data,
        })
        self.context = context
        self.from_date = ''
        self.to_date = ''
        self.employee_ids = False


    def _get_data(self, data):
        self.from_date = data['form']['start_date']
        self.to_date = data['form']['end_date']
        self.employee_ids = data['form']['employee_ids']
        employee_obj = self.pool.get('hr.employee')
        user_rec = self.pool.get('res.users').browse(self.cr, self.uid, self.uid)
        res = {'data': []}
        for employee in self.employee_ids:
            data_item =[]
            employee_rec = employee_obj.browse(self.cr, self.uid, employee)
            data_item.append(employee_rec.name)
            initial_balance = self.get_initial_balance(employee)
            data_item.append(initial_balance)
            deduction = self.get_deduction(employee)
            data_item.append(deduction)
            data_item.append(initial_balance - deduction)
            res['data'].append(data_item)
        return res

    def get_initial_balance(self, employee_id):
        holiday_obj = self.pool.get('hr.holidays')
        holiday_allocation_ids = holiday_obj.search(self.cr, self.uid, [('employee_id', '=', employee_id),
                                                             ('type', '=', 'add'),
                                                             ('state', '=', 'validate')])
        initial_balance = 0
        if holiday_allocation_ids:
            for id in holiday_allocation_ids:
                holiday_rec = holiday_obj.browse(self.cr, self.uid, id)
                if not holiday_rec.holiday_status_id.limit:
                    initial_balance += holiday_rec.number_of_days
                initial_balance += holiday_rec.number_of_days
        holiday_request_ids = holiday_obj.search(self.cr, self.uid, [('employee_id', '=', employee_id),
                                                             ('type', '=', 'remove'),
                                                             ('date_to', '<', self.from_date),
                                                             ('state', '=', 'validate')])
        if holiday_request_ids:
            for id in holiday_request_ids:
                holiday_rec = holiday_obj.browse(self.cr, self.uid, id)
                if not holiday_rec.holiday_status_id.limit:
                    initial_balance += holiday_rec.number_of_days
        return initial_balance

    def get_deduction(self, employee_id):
        holiday_obj = self.pool.get('hr.holidays')
        holiday_request_ids = holiday_obj.search(self.cr, self.uid, [('employee_id', '=', employee_id),
                                                             ('type', '=', 'remove'),
                                                             ('date_from', '>=', self.from_date),
                                                             ('date_from', '<=', self.to_date),
                                                             ('date_to', '<=', self.to_date),
                                                             ('date_to', '>=', self.from_date),
                                                             ('state', '=', 'validate')])
        deduction = 0
        if holiday_request_ids:
            for id in holiday_request_ids:
                holiday_rec = holiday_obj.browse(self.cr, self.uid, id)
                if not holiday_rec.holiday_status_id.limit:
                    deduction += holiday_rec.number_of_days
        return -deduction

class HrHolidaysReport(models.AbstractModel):
    _name = 'report.odootec_hr_holiday.hr_holiday_report'
    _inherit = 'report.abstract_report'
    _template = 'odootec_hr_holiday.hr_holiday_report'
    _wrapped_report_class = HrHolidaysParser
