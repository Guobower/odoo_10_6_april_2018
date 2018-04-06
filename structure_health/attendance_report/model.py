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
###################################################
from openerp import models, fields, api
from datetime import timedelta,datetime,date
from dateutil.relativedelta import relativedelta
import time

class SampleDevelopmentReport(models.AbstractModel):
    _name = 'report.attendance_report.customer_report'

    @api.model
    def render_html(self,docids, data=None):
        report_obj = self.env['report']
        report = report_obj._get_report_from_name('attendance_report.customer_report')
        active_wizard = self.env['attend.report'].search([])
        emp_list = []
        for x in active_wizard:
            emp_list.append(x.id)
        emp_list = emp_list
        emp_list_max = max(emp_list) 

        record_wizard = self.env['attend.report'].search([('id','=',emp_list_max)])

        record_wizard_del = self.env['attend.report'].search([('id','!=',emp_list_max)])
        record_wizard_del.unlink()
        date_from = record_wizard.date_from
        date_to = record_wizard.date_to
        types = record_wizard.types
        customer = record_wizard.customer
        all_rec = self.env['struct.attend'].search([])


        if types == 'specfic':
            cust = []
            for y in customer:
                cust.append(y)


        if types == 'all':
            cust = []
            for y in all_rec:
                if y.employee_id not in cust:
                    cust.append(y.employee_id)


        dates = []
        for x in cust:
            if types == 'specfic':
                records = self.env['struct.attend'].search([('date','>=',record_wizard.date_from),('date','<=',record_wizard.date_to),('employee_id','=',x.name)])
            if types == 'all':
                records = self.env['struct.attend'].search([('date','>=',record_wizard.date_from),('date','<=',record_wizard.date_to),('employee_id','=',x)])
            for x in records:
                dates.append(x)



        final_records = []
        def get_cust(attr):
            del final_records[:]
            cust_attend = []
            cust_date = []
            cust_time = []

            for x in dates:
                if x.employee_id == attr:
                    cust_attend.append(x)

            for y in cust_attend:
                if y.date not in cust_date:
                    cust_date.append(y.date)

            for z in cust_date:
                del cust_time[:]
                for a in cust_attend:
                    if z == a.date:
                        cust_time.append(a.time)
                cust_time.sort()

                for b in cust_attend:
                    if cust_time[0] == b.time:
                        final_records.append(b)



        def get_from():
            value = ""
            value = record_wizard.date_from
            return value
            

        def get_to():
            value = ""
            value = record_wizard.date_to
            return value
            

        def get_id():
            value = 0
            if record_wizard.types == 'specfic':
                value = 1
            if record_wizard.types == 'all':
                value = 2

            return value


      
        
        docargs = {
        
            'doc_ids': docids,
            'doc_model': 'struct.attend',
            'cust': cust,
            'get_from': get_from,
            'get_cust': get_cust,
            'get_id': get_id,
            'get_to': get_to,
            'final_records': final_records,

            }

        return report_obj.render('attendance_report.customer_report', docargs)