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

class HrSalarySlip(models.AbstractModel):
    _name = 'report.salary_slip.salary_slip_report'

    @api.model
    def render_html(self,docids, data=None):
        report_obj = self.env['report']
        report = report_obj._get_report_from_name('salary_slip.salary_slip_report')
        records = self.env['hr.payslip'].browse(docids)

        rule = []
        rules = []
        for x in records.line_ids:
            if x.name not in rule and x.name != "Basic" and x.name != "House Rent" and x.name != "Medical Expense" and x.name != "Gross":
                rules.append(x)
                rule.append(x.name)

        def basic():
            total = 0
            for x in records.line_ids:
                if x.name == 'Basic':
                    if x.total:
                        total = total + x.total
            return total

        def rent():
            total = 0
            for x in records.line_ids:
                if x.name == 'House Rent':
                    if x.total:
                        total = total + x.total
            return total

        def medical():
            total = 0
            for x in records.line_ids:
                if x.name == 'Medical Expense':
                    if x.total:
                        total = total + x.total
            return total

        def gross():
            total = 0
            for x in records.line_ids:
                if x.name == 'Gross':
                    if x.total:
                        total = total + x.total
            return total

        def geturdu(attr):
            ruled = self.env['hr.salary.rule'].search([('name','=',attr)])
            return ruled.urdu_name

        docargs = {
            'doc_ids': docids,
            'doc_model': 'hr.payslip',
            'docs': records,
            'data': data,
            'basic' : basic,
            'rent' : rent,
            'medical' : medical,
            'gross' : gross,
            'rules': rules,
            'geturdu': geturdu
            }

        return report_obj.render('salary_slip.salary_slip_report', docargs)