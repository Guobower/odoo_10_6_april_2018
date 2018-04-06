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
    _name = 'report.trainer_report.customer_report'

    @api.model
    def render_html(self,docids, data=None):
        report_obj = self.env['report']
        report = report_obj._get_report_from_name('trainer_report.customer_report')
        active_wizard = self.env['trainer.reports'].search([])
        emp_list = []
        for x in active_wizard:
            emp_list.append(x.id)
        emp_list = emp_list
        emp_list_max = max(emp_list) 

        record_wizard = self.env['trainer.reports'].search([('id','=',emp_list_max)])

        record_wizard_del = self.env['trainer.reports'].search([('id','!=',emp_list_max)])
        record_wizard_del.unlink()

        branch = record_wizard.branch
        trainer = record_wizard.trainer



        record = self.env['reg.form'].search([('branch','=',record_wizard.branch.id),('current_trainer','=',record_wizard.trainer.id),('stages','=','member')])



        docargs = {
        
            'doc_ids': docids,
            'doc_model': 'reg.form',
            'branch': branch.name,
            'trainer': trainer.name,
            'record': record,
    
            }

        return report_obj.render('trainer_report.customer_report', docargs)