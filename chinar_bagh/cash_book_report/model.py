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
    _name = 'report.cash_book_report.module_report'

    @api.model
    def render_html(self,docids, data=None):
        report_obj = self.env['report']
        report = report_obj._get_report_from_name('cash_book_report.module_report')
        active_wizard = self.env['cash.report'].search([])
        emp_list = []
        for x in active_wizard:
            emp_list.append(x.id)
        emp_list = emp_list
        emp_list_max = max(emp_list) 

        record_wizard = self.env['cash.report'].search([('id','=',emp_list_max)])

        record_wizard_del = self.env['cash.report'].search([('id','!=',emp_list_max)])
        record_wizard_del.unlink()
        date_from = record_wizard.date_from
        date_to = record_wizard.date_to
        idss = record_wizard.idss

        records = self.env['account.bank.statement'].search([('id','=',record_wizard.idss)])


        enteries = []
        for x in records.line_ids:
            if x.date >= record_wizard.date_from and x.date <= record_wizard.date_to:
                enteries.append(x)

        enteries.sort(key=lambda x: x.date)

        def get_open():
            value = 0
            rec = 0
            paid = 0
            for x in records.line_ids:
                if x.date < record_wizard.date_from:
                    rec = rec + x.received
                    paid = paid + x.paid
            value = rec - paid

            return value





        
        docargs = {
        
            'doc_ids': docids,
            'doc_model': 'account.bank.statement',
            'docs':records,
            'enteries':enteries,
            'get_open':get_open,

            }

        return report_obj.render('cash_book_report.module_report', docargs)