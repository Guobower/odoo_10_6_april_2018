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
    _name = 'report.receiveable_branch_wise.customer_report'

    @api.model
    def render_html(self,docids, data=None):
        report_obj = self.env['report']
        report = report_obj._get_report_from_name('receiveable_branch_wise.customer_report')
        active_wizard = self.env['receive.branch'].search([])
        emp_list = []
        for x in active_wizard:
            emp_list.append(x.id)
        emp_list = emp_list
        emp_list_max = max(emp_list) 

        record_wizard = self.env['receive.branch'].search([('id','=',emp_list_max)])

        record_wizard_del = self.env['receive.branch'].search([('id','!=',emp_list_max)])
        record_wizard_del.unlink()
        date = record_wizard.date
        branch = record_wizard.branch

        journal_cust = []
        rec = self.env['account.move.line'].search([('date','>',record_wizard.date),('move_id.branch','=',record_wizard.branch.id)])
        for x in rec:
            if x.partner_id:
                if x.partner_id.id not in journal_cust:
                    journal_cust.append(x.partner_id.id)

        cust = []
        records = self.env['res.partner'].search([])
        for x in journal_cust:
            for z in records:
                if x == z.id:
                    cust.append(z)


        def get_bal(attr):
            value = 0
            for y in records:
                if y.id == attr:
                    value = y.credit - y.debit

            return value

        

        docargs = {
        
            'doc_ids': docids,
            'doc_model': 'res.partner',
            'cust': cust,
            'get_bal': get_bal,
    
            }

        return report_obj.render('receiveable_branch_wise.customer_report', docargs)