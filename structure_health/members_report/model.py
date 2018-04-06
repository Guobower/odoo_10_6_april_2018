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
    _name = 'report.members_report.customer_report'

    @api.model
    def render_html(self,docids, data=None):
        report_obj = self.env['report']
        report = report_obj._get_report_from_name('members_report.customer_report')
        active_wizard = self.env['member.report'].search([])
        emp_list = []
        for x in active_wizard:
            emp_list.append(x.id)
        emp_list = emp_list
        emp_list_max = max(emp_list) 

        record_wizard = self.env['member.report'].search([('id','=',emp_list_max)])

        record_wizard_del = self.env['member.report'].search([('id','!=',emp_list_max)])
        record_wizard_del.unlink()
        date_from = record_wizard.date_from
        date_to = record_wizard.date_to
        types = record_wizard.types


        conti = []
        records = self.env['reg.form'].search([('stages','=','member'),('joining','>=',record_wizard.date_from),('joining','<=',record_wizard.date_to)])
        for x in records:
            conti.append(x)


        disconti = []
        record = self.env['reg.form'].search([('stages','=','non_member'),('write_date','>=',record_wizard.date_from),('write_date','<=',record_wizard.date_to)])
        for x in record:
            disconti.append(x)


        def get_type():
            new = 0
            if record_wizard.types == 'continue':
                new = 1
            if record_wizard.types == 'dis':
                new = 2

            return new


        def get_from():
            value = ""
            value = record_wizard.date_from
            return value

        def get_to():
            value = ""
            value = record_wizard.date_to
            return value


      
        
        docargs = {
        
            'doc_ids': docids,
            'doc_model': 'reg.form',
            'docs': records,
            'conti': conti,
            'disconti': disconti,
            'get_type': get_type,
            'get_from': get_from,
            'get_to': get_to,

            }

        return report_obj.render('members_report.customer_report', docargs)