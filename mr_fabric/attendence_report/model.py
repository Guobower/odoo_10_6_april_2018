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
from datetime import date, timedelta
import datetime

class EmployeeWiseAttendence(models.AbstractModel):
    _name = 'report.attendence_report.attendence_report'

    @api.model
    def render_html(self,docids, data=None):
        report_obj = self.env['report']
        report = report_obj._get_report_from_name('attendence_report.attendence_report')
        active_wizard = self.env['attend.report'].search([])

        emp_list = []
        for x in active_wizard:
            emp_list.append(x.id)
        emp_list = emp_list
        emp_list_max = max(emp_list) 

        record_wizard = self.env['attend.report'].search([('id','=',emp_list_max)])
        record_wizard_del = self.env['attend.report'].search([('id','!=',emp_list_max)])
        record_wizard_del.unlink()

        form = record_wizard.form
        to = record_wizard.to
        typed = record_wizard.typed
        department = record_wizard.department

        d1 = datetime.datetime.strptime(record_wizard.form, "%Y-%m-%d")
        d2 = datetime.datetime.strptime(record_wizard.to, "%Y-%m-%d")

        delta = d2 - d1
        dates = []
        for i in range(delta.days + 1):
            dates.append((d1 + timedelta(days=i)).strftime('%Y-%m-%d'))

        if typed == 'specific':
            employees = []
            for x in record_wizard.employee:
                employees.append(x)

        if typed == 'department':
            employees = self.env['hr.employee'].search([('department_id.id','=',department.id)])

        if typed == 'all':
            employees = self.env['hr.employee'].search([])

        size = len(dates)

        def getattend(date,employee,attr):
            attendence = self.env['actual.attendence'].search([('date','=',date),('employee_id.id','=',employee.id)])
            
            if attr == 'entry':
                if attendence.checkin:
                    return '{0:02.0f}:{1:02.0f}'.format(*divmod(attendence.checkin * 60, 60))
                else: 
                    return "-"
            
            if attr == 'exit':
                if attendence.checkout:
                    return '{0:02.0f}:{1:02.0f}'.format(*divmod(attendence.checkout * 60, 60))
                else: 
                    return "-"
            
            if attr == 'total':
                if attendence.total_time:
                    return '{0:02.0f}:{1:02.0f}'.format(*divmod(attendence.total_time * 60, 60))
                else: 
                    return "-"
            
            if attr == 'real':
                if attendence.total_time:
                    return attendence.total_time
                else: 
                    return 0

        docargs = {
            'doc_ids': docids,
            'doc_model': 'hr.employee',
            'data': data,
            'form': form,
            'to': to,
            'employees': employees,
            'dates': dates,
            'getattend': getattend,
            'size': size
            }

        return report_obj.render('attendence_report.attendence_report', docargs)