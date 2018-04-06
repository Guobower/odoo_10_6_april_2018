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
    _name = 'report.leave_encashment_report.customer_report'

    @api.model
    def render_html(self,docids, data=None):
        report_obj = self.env['report']
        report = report_obj._get_report_from_name('leave_encashment_report.customer_report')
        active_wizard = self.env['encashment.report'].search([])
        emp_list = []
        for x in active_wizard:
            emp_list.append(x.id)
        emp_list = emp_list
        emp_list_max = max(emp_list) 

        record_wizard = self.env['encashment.report'].search([('id','=',emp_list_max)])

        record_wizard_del = self.env['encashment.report'].search([('id','!=',emp_list_max)])
        record_wizard_del.unlink()

        date_from = record_wizard.date_from
        date_to = record_wizard.date_to
        # rep_types = record_wizard.rep_types
        # card_types = record_wizard.card_types
        # dep_types = record_wizard.dep_types
        # card_no = record_wizard.card_no
        # depart = record_wizard.depart

        accounts = []
        rec = self.env['hr.department'].search([])
        for x in rec:
            accounts.append(x)

        records = []
        def get_rec(attr):
            del records[:]
            rec = self.env['leave.encashment.tree'].search([('name.department_id.id','=',attr),('laeve_tree.date_from','=',date_from),('laeve_tree.date_to','=',date_to)])
            for x in rec:
                records.append(x)





        docargs = {
        
            'doc_ids': docids,
            'doc_model': 'account.invoice',
            'date_from': date_from,
            'date_to': date_to,
            'accounts': accounts,
            'records': records,
            'get_rec': get_rec,
    
            }

        return report_obj.render('leave_encashment_report.customer_report', docargs)