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

class SampleDevelopmentReport(models.AbstractModel):
    _name = 'report.increment_letter.letter_increment'

    @api.model
    def render_html(self,docids, data=None):
        report_obj = self.env['report']
        report = report_obj._get_report_from_name('increment_letter.letter_increment')
        records = self.env['employee.increment'].browse(docids)

        def getsalary(attr):
            employee = self.env['hr.employee'].search([('card_no.id','=',attr.employee_card.id)])
            salary = employee.department_id.name

            return salary

        def getinr(attr):
            employee = self.env['hr.employee'].search([('card_no.id','=',attr.employee_card.id)])
            salary = int(employee.salary)

            return salary

        docargs = {
            'doc_ids': docids,
            'doc_model': 'employee.increment',
            'docs': records,
            'data': data,
            'getsalary': getsalary,
            'getinr': getinr
            }

        return report_obj.render('increment_letter.letter_increment', docargs)