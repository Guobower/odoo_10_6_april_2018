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
from datetime import date
import datetime
from datetime import date, datetime, timedelta
import time
import calendar

class DailyAttendenceReport(models.AbstractModel):
    _name = 'report.daily_attendence_report.attendence'

    @api.model
    def render_html(self,docids, data=None):
        report_obj = self.env['report']
        report = report_obj._get_report_from_name('daily_attendence_report.attendence')
        active_wizard = self.env['daily.attend'].search([])

        emp_list = []
        for x in active_wizard:
            emp_list.append(x.id)
        emp_list = emp_list
        emp_list_max = max(emp_list) 

        record_wizard = self.env['daily.attend'].search([('id','=',emp_list_max)])
        record_wizard_del = self.env['daily.attend'].search([('id','!=',emp_list_max)])
        record_wizard_del.unlink()

        form = record_wizard.form
        to = record_wizard.to
        employee = record_wizard.employee

        attendence = self.env['actual.attendence'].search([('employee_id.id','=',employee.id),('date','>=',form),('date','<=',to)])
        dates = []
        def get_status(attr):
            if attr == 'present':
                return 'Present'
            elif attr == 'absent':
                return 'Absent'
            elif attr == 'leave':
                return 'Leave'
            elif attr == 'holiday':
                return 'Holiday'
            else:
                return '-'

        def holiday(attr):
            employee = self.env['hr.employee'].search([('id','=',attr.id)])

            holidays = 0
            for x in employee.leave_tree:
                holidays = holidays + x.allowed

            return holidays

        leaves = self.env['hr.holidays.status'].search([])

        def senddates(attr):
            dates.append(attr)

        def getleaves(emp,attr):
            total_leaves = 0
            print dates
            for x in dates:
                raw_date = datetime.strptime(x, '%Y-%m-%d')
                raw_date_time = datetime.strftime(raw_date, '%Y-%m-%d %H:%M:%S')
                emp_leave = self.env['hr.holidays'].search([('employee_id.id','=',emp.id),('holiday_status_id.id','=',attr.id),('date_from','<=',raw_date_time),('date_to','>=',raw_date_time)])
                if emp_leave:
                    total_leaves = total_leaves + 1

            return total_leaves

        docargs = {
            'doc_ids': docids,
            'doc_model': 'hr.employee',
            'docs': employee,
            'data': data,
            'form': form,
            'to': to,
            'attendence': attendence,
            'get_status': get_status,
            'holiday': holiday,
            'leaves': leaves,
            'senddates': senddates,
            'getleaves': getleaves,
            }

        return report_obj.render('daily_attendence_report.attendence', docargs)