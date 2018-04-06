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
    _name = 'report.membership_reports.customer_report'

    @api.model
    def render_html(self,docids, data=None):
        report_obj = self.env['report']
        report = report_obj._get_report_from_name('membership_reports.customer_report')
        active_wizard = self.env['membership.reports'].search([])
        emp_list = []
        for x in active_wizard:
            emp_list.append(x.id)
        emp_list = emp_list
        emp_list_max = max(emp_list) 

        record_wizard = self.env['membership.reports'].search([('id','=',emp_list_max)])

        record_wizard_del = self.env['membership.reports'].search([('id','!=',emp_list_max)])
        record_wizard_del.unlink()
        date_from = record_wizard.date_from
        date_to = record_wizard.date_to
        branch = record_wizard.branch
        types = record_wizard.types
        package_type = record_wizard.package_type
        numb = 0
        record = self.env['reg.form'].search([('branch','=',record_wizard.branch.id)])

        if types == 'active':
            rep_type = "ACTIVE MEMBERS"
            membership = []
            for x in record:
                if x.stages == 'member':
                    membership.append(x)

        if types == 'nonactive':
            rep_type = "NON ACTIVE MEMBERS"
            membership = []
            for x in record:
                if x.stages == 'non_member':
                    membership.append(x)

        if types == 'discontinue':
            numb = 1
            rep_type = "DISCONTINUE MEMBERS"
            membership = []
            for x in record:
                if x.stages == 'non_member':
                    rec = self.env['mail.tracking.value'].search([('mail_message_id.res_id','=',x.id)])
                    if rec:
                        for z in rec:
                            if z.field == 'stages' and z.new_value_char == 'Non Active Members':
                                if str(z.mail_message_id.date[:10]) >= date_from and str(z.mail_message_id.date[:10]) <= date_to:
                                    membership.append(x)


        if types == 'new':
            numb = 1
            rep_type = "NEW MEMBERS"
            membership = []
            for x in record:
                if x.stages == 'member':
                    if x.joining:
                        if x.joining >= date_from and x.joining <= date_to:
                            membership.append(x)


        if types == 'diet':
            rep_type = "DIET PLAN MEMBERS"
            membership = []
            for x in record:
                if x.stages == 'member':
                    if x.diet_plan == True:
                        membership.append(x)


        if types == 'health':
            rep_type = "HEALTH ASSESMENT MEMBERS"
            membership = []
            for x in record:
                if x.stages == 'member':
                    if x.health == True:
                        membership.append(x)



        if types == 'package':
            pack_type = record_wizard.package_type.name
            new = pack_type.upper()
            rep_type = new + ' '+ "PACKAGE MEMBERS"
            membership = []
            for x in record:
                if x.stages == 'member':
                    if x.package.package_type.id == record_wizard.package_type.id:
                        membership.append(x)


        if types == 'daily':
            rep_type = "DAILY BASE MEMBERS"
            membership = []
            for x in record:
                if x.stages == 'member':
                    if x.daily == True:
                        membership.append(x)


        if types == 'temp':
            rep_type = "TEMPORARY BASE MEMBERS"
            membership = []
            for x in record:
                if x.stages == 'member':
                    if x.temp == True:
                        membership.append(x)

        

        docargs = {
        
            'doc_ids': docids,
            'doc_model': 'reg.form',
            'membership': membership,
            'rep_type': rep_type,
            'date_from': date_from,
            'date_to': date_to,
            'branch': branch.name,
            'numb': numb,
    
            }

        return report_obj.render('membership_reports.customer_report', docargs)