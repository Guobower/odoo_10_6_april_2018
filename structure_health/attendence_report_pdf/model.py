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
    _name = 'report.attendence_report_pdf.attendence_report'

    @api.model
    def render_html(self,docids, data=None):
        report_obj = self.env['report']
        report = report_obj._get_report_from_name('attendence_report_pdf.attendence_report')
        active_wizard = self.env['attend.report'].search([])

        emp_list = []
        for x in active_wizard:
            emp_list.append(x.id)
        emp_list = emp_list
        emp_list_max = max(emp_list) 

        record_wizard = self.env['attend.report'].search([('id','=',emp_list_max)])
        record_wizard_del = self.env['attend.report'].search([('id','!=',emp_list_max)])
        record_wizard_del.unlink()

        member = record_wizard.member
        to = record_wizard.to
        form = record_wizard.form

        members = []
        for x in member:
            members.append(x)

        d1 = datetime.datetime.strptime(record_wizard.form, "%Y-%m-%d")
        d2 = datetime.datetime.strptime(record_wizard.to, "%Y-%m-%d")

        delta = d2 - d1
        dates = []
        for i in range(delta.days + 1):
            dates.append((d1 + timedelta(days=i)).strftime('%Y-%m-%d'))

        size = len(dates)

        def getattend(date,member):
            attendence = self.env['struct.attend'].search([('date','=',date),('employee_id.id','=',member.id)])
            
            if attendence:
                for x in attendence:
                    if x.time:
                        return x.time
                    else: 
                        return "-"
            else: 
                return "-"

        docargs = {
            'doc_ids': docids,
            'doc_model': 'reg.form',
            'data': data,
            'member' : member,
            'to' : to,
            'form' : form,
            'members': members,
            'size': size,
            'dates': dates,
            'getattend': getattend
            }

        return report_obj.render('attendence_report_pdf.attendence_report', docargs)